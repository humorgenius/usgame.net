#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
内容入库：把缓存好的 .docx 变成站点的 Markdown 页面 + WebP 图片。

读 docs/content-map.csv 拿栏目/标题/slug（那一步的门禁已经过了），本脚本只做转换：
  .docx ──┬─ 段落/标题/表格 ──> src/content/articles/<lang>/<slug>.md
          └─ word/media/*     ──> public/media/<sha1>.webp（全局去重，同图只存一份）

用法:
  python scripts/ingest.py --limit 2          # 先试 2 篇
  python scripts/ingest.py --only 12,24       # 只做指定 idx
  python scripts/ingest.py                    # 全量 73 篇
  python scripts/ingest.py --dry              # 只统计，不落盘
"""
import os, re, sys, csv, csv as _csv, zipfile, hashlib, json, argparse, datetime
import xml.etree.ElementTree as ET
from io import BytesIO

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
VML = "{urn:schemas-microsoft-com:vml}"

ROOT = r"D:/【建立网站】/GTA6/usgame.net"
DOCX_DIR = r"E:/hermes-workspace/temp/docx_all"
MAP_CSV = os.path.join(ROOT, "docs/content-map.csv")
CONTENT_DIR = os.path.join(ROOT, "src/content/articles")
MEDIA_DIR = os.path.join(ROOT, "public/media")

CJK = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")
LATIN = re.compile(r"[A-Za-z]")

MAX_W = 1600          # 正文图最长边
QUALITY = 82
COVER_W = 1600


def cjk_ratio(s):
    n = len(CJK.findall(s)) + len(LATIN.findall(s))
    return len(CJK.findall(s)) / n if n else 0.0


# ----------------------------------------------------------------- 解析 docx
def rels(z):
    """rId -> word/media/... 的实际路径"""
    out = {}
    try:
        root = ET.fromstring(z.read("word/_rels/document.xml.rels"))
    except KeyError:
        return out
    for rel in root:
        tgt = rel.get("Target", "")
        if "media/" in tgt:
            out[rel.get("Id")] = "word/" + tgt.lstrip("./").replace("../", "")
    return out


def para_images(p, rmap):
    """该段落里出现的图片（保持文档顺序）"""
    ids = []
    for blip in p.iter(f"{A}blip"):
        rid = blip.get(f"{R}embed")
        if rid and rid in rmap:
            ids.append(rmap[rid])
    for im in p.iter(f"{VML}imagedata"):
        rid = im.get(f"{R}id")
        if rid and rid in rmap:
            ids.append(rmap[rid])
    return ids


def walk(p):
    """段落 -> [(kind, text)]，kind ∈ text/bold/italic；保留强调"""
    out = []
    for node in p:
        tag = node.tag
        if tag == f"{W}r":
            txt = "".join(t.text or "" for t in node.iter(f"{W}t"))
            if not txt:
                continue
            pr = node.find(f"{W}rPr")
            b = i = False
            if pr is not None:
                b = pr.find(f"{W}b") is not None
                i = pr.find(f"{W}i") is not None
            out.append(("bi"[0] if b else ("it" if i else "text"), txt))
        elif tag == f"{W}hyperlink":
            txt = "".join(t.text or "" for t in node.iter(f"{W}t"))
            if txt:
                out.append(("text", txt))
    return out


def inline(parts):
    """把 run 列表拼成一行 Markdown，保留加粗/斜体"""
    s = ""
    for kind, txt in parts:
        txt = txt.replace("\\", "\\\\").replace("*", "\\*").replace("_", "\\_")
        if kind == "b":
            s += f"**{txt}**"
        elif kind == "it":
            s += f"*{txt}*"
        else:
            s += txt
    return re.sub(r"\s+", " ", s).strip()


def parse_docx(path):
    """-> [{'k':'h'|'p'|'li'|'tbl'|'img', ...}] 按文档顺序"""
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
        rmap = rels(z)
        blocks, need = [], {}
        for el in root.find(f"{W}body"):
            if el.tag == f"{W}p":
                pr = el.find(f"{W}pPr")
                style = ""
                numpr = False
                if pr is not None:
                    st = pr.find(f"{W}pStyle")
                    style = st.get(f"{W}val", "") if st is not None else ""
                    numpr = pr.find(f"{W}numPr") is not None
                imgs = para_images(el, rmap)
                for m in imgs:
                    blocks.append({"k": "img", "src": m})
                    need[m] = True
                txt = inline(walk(el))
                if not txt:
                    continue
                if "Heading" in style or "标题" in style:
                    lvl = re.sub(r"\D", "", style) or "3"
                    blocks.append({"k": "h", "lvl": int(lvl), "t": txt})
                elif numpr or re.match(r"^[-•·]\s*", txt):
                    blocks.append({"k": "li", "t": re.sub(r"^[-•·]\s*", "", txt)})
                else:
                    blocks.append({"k": "p", "t": txt})
            elif el.tag == f"{W}tbl":
                rows = []
                for tr in el.findall(f"{W}tr"):
                    cells = []
                    for tc in tr.findall(f"{W}tc"):
                        cells.append(inline([x for p in tc.findall(f"{W}p") for x in walk(p)]))
                    rows.append(cells)
                if rows:
                    blocks.append({"k": "tbl", "rows": rows})
        media = {}
        for name in z.namelist():
            if name.startswith("word/media/"):
                media[name] = z.read(name)
    return blocks, media


def split_at(blocks):
    """中英切分：第一个拉丁为主的标题块，必要时前移一格（英文标题是普通段落的情形）"""
    for j, b in enumerate(blocks):
        if b["k"] == "h" and j >= 3 and len(b["t"]) >= 12 and cjk_ratio(b["t"]) < 0.05:
            k = j
            prev = blocks[k - 1]
            if not (prev["k"] == "h") and cjk_ratio(prev.get("t", "")) < 0.05 and len(prev.get("t", "")) >= 12:
                k -= 1
            return k
    for j, b in enumerate(blocks):
        if j >= 4 and b["k"] in ("h", "p") and cjk_ratio(b.get("t", "")) < 0.05:
            return j
    return None


# ----------------------------------------------------------------- 图片
def sha(b):
    return hashlib.sha1(b).hexdigest()[:12]


def to_webp(raw, maxw=MAX_W):
    from PIL import Image
    im = Image.open(BytesIO(raw))
    im = im.convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = BytesIO()
    im.save(buf, "WEBP", quality=QUALITY, method=5)
    return buf.getvalue(), im.size


def ensure_media(store, raw, dry):
    """全局去重：同一张图只落一份 /media/<hash>.webp"""
    h = sha(raw)
    if h in store:
        return store[h]
    # 已经有这个哈希的图就复用，不重复编码（改版式后重跑整批会快很多）
    exist = os.path.join(MEDIA_DIR, f"{h}.webp")
    if os.path.exists(exist):
        try:
            from PIL import Image
            with Image.open(exist) as im:
                wh = im.size
            store[h] = {"url": f"/media/{h}.webp", "bytes": os.path.getsize(exist), "size": wh}
            return store[h]
        except Exception:
            pass
    try:
        webp, size = to_webp(raw)
    except Exception as e:
        store[h] = None
        return None
    if not dry:
        os.makedirs(MEDIA_DIR, exist_ok=True)
        with open(os.path.join(MEDIA_DIR, f"{h}.webp"), "wb") as f:
            f.write(webp)
    store[h] = {"url": f"/media/{h}.webp", "bytes": len(webp), "size": size}
    return store[h]


# ----------------------------------------------------------------- 正文
PUNCT_END = re.compile(r"[。．\.!！?？,，;；:：]\s*$")


def norm(s):
    """去掉书名号与《GTA6》前缀，用于判断某段是不是标题的重复"""
    return re.sub(r"[《》\s]", "", re.sub(r"^《GTA6?》\s*", "", (s or "").strip()))


# 编号领起的小节名，例如 "5. Downtown / Tequesta（市中心 / 特奎斯塔）"、
# "3、载具改装"。这类文字必然是标题，只是不含中英对照时会很长。
NUM_LEAD = re.compile(r"^\d{1,2}\s*[\.、]\s*\S")


def is_heading_like(t):
    """原稿的标题样式很不统一：不少小节名是普通段落。判据要保守——
    结尾无句读，且（普通段落）要够短、（编号领起的小节名）可放宽。

    踩过的坑：原先只用「≤28 字 + 后面紧跟图片或 60 字以上长段」两条卡，
    于是 "5. Downtown / Tequesta（市中心 / 特奎斯塔）"（33 字）和
    "6. Vice City Port（罪恶都市港）"（后面正文仅 44 字）被漏成了正文，
    同一篇文章里 1/2/3/4/7 是标题、5/6 不是 —— 读者一眼就看出来。
    """
    if not t or PUNCT_END.search(t):
        return False
    if NUM_LEAD.match(t):
        return len(t) <= 80
    return 2 <= len(t) <= 28


def promote(blocks, title):
    """把「像标题的普通段落」升级成 h，并给图片补 alt；返回升级了几处"""
    n = 0
    for k, b in enumerate(blocks):
        if b["k"] != "p" or not is_heading_like(b["t"]) or norm(b["t"]) == norm(title):
            continue
        nxt = blocks[k + 1] if k + 1 < len(blocks) else None
        # 编号领起的小节名，后面接短句也是标题（"6. Vice City Port" 的正文
        # 就只有一句 44 字的话）；普通段落仍要求后接长文，免得把正文碎句升上来。
        numbered = bool(NUM_LEAD.match(b["t"]))
        listed = bool(nxt) and nxt["k"] == "img"
        plain = bool(nxt) and nxt["k"] == "p" and (numbered or len(nxt["t"]) >= 60)
        if listed or plain:
            b["k"], b["lvl"] = "h", 3
            n += 1
    last = title
    for b in blocks:
        if b["k"] == "h":
            last = b["t"]
        elif b["k"] == "img":
            b["alt"] = last[:70]
    return n


def drop_title(blocks, title):
    """正文开头常把标题又写一遍，有时是普通段落、有时是「小标题」样式，两种都要去掉。
    漏掉标题样式的那次，正文里会多出一个和 <h1> 重复的 h2，还会把目录的第一项
    变成文章标题本身。"""
    while blocks and blocks[0]["k"] in ("p", "h") and norm(blocks[0].get("t", "")) == norm(title):
        blocks = blocks[1:]
    return blocks


def add_jsapi(md):
    """给所有 YouTube 嵌入补 enablejsapi=1。

    页面上的「播放中的视频滚出视口后自动浮到右下角」依赖这个参数：
    跨域 iframe 读不到播放状态，只能通过 postMessage 向播放器要，
    而播放器只对带 enablejsapi=1 的嵌入响应。
    少了它的后果很隐蔽 —— 不报错，视频就是不浮起来，所以在这里兜住，
    免得哪天重新入库、参数丢了没人发现。"""
    def fix(m):
        u = m.group(0)
        if "enablejsapi" in u:
            return u
        return u + ("&amp;" if "?" in u else "?") + "enablejsapi=1"
    return re.sub(r'https://www\.youtube(?:-nocookie)?\.com/embed/[\w-]+(?:\?[^"\'\s>]*)?', fix, md)


def md_with_images(blocks, store, dry, cover_hint=True):
    """第二遍：把图片插到它原本的位置，并返回第一张作为封面"""
    parts, bullet, cover = [], [], None
    for b in blocks:
        if b["k"] == "img":
            info = ensure_media(store, b["raw"], dry)
            if not info:
                continue
            if cover is None:
                cover = info["url"]
            if not cover_hint:
                continue
            parts += [f"![{b.get('alt', '')}]({info['url']})", ""]
            continue
        if b["k"] == "li":
            bullet.append(b["t"]); continue
        if bullet:
            parts += [f"- {x}" for x in bullet] + [""]; bullet = []
        if b["k"] == "h":
            parts += ["## " + b["t"] if b["lvl"] <= 3 else "### " + b["t"], ""]
        elif b["k"] == "p":
            parts += [b["t"], ""]
        elif b["k"] == "tbl":
            rows = b["rows"]; w = max(len(r) for r in rows)
            rows = [r + [""] * (w - len(r)) for r in rows]
            parts.append("| " + " | ".join(rows[0]) + " |")
            parts.append("| " + " | ".join(["---"] * w) + " |")
            parts += ["| " + " | ".join(r) + " |" for r in rows[1:]]
            parts.append("")
    if bullet:
        parts += [f"- {x}" for x in bullet] + [""]
    return "\n".join(parts).strip(), cover


SENT_END = "。！？；!?;"


def make_desc(lede, limit=158):
    """SEO 描述：在句末切断，别切在半句中间（页面导语用的不是这个字段）。"""
    s = re.sub(r"\s+", " ", lede).strip()
    if len(s) <= limit:
        return s
    best = -1
    for i, ch in enumerate(s[:limit]):
        if ch in SENT_END:
            best = i + 1
        elif ch == "." and i + 1 < len(s) and s[i + 1] == " ":
            best = i + 1
    if best >= max(40, int(limit * 0.4)):
        return s[:best].strip()
    return s[:limit].rstrip(" ,，、") + "…"


def localize_title(t, lang):
    """中文标题没带 GTA 字样的补上《GTA6》。

    为什么：73 个中文标题取自原稿文件名，而文件名自己就不统一 ——
    4 个带《GTA6》、69 个不带；英文侧 73 个则全都带 GTA6。所以这不是加词，
    是把作者自己用过的那套写法补齐。GTA6 是中文检索里最值钱的词，
    它得同时出现在 H1 和 <title> 里，光在正文里出现不算数。
    已经有 GTA 字样的一律不动，保留作者原本的写法。可逆：原始文件名未改动。
    """
    # 判据必须只认「GTA6」：写成「与《GTA5》全面对比…」的稿子含 GTA 字样、
    # 却一次没提 GTA6，用宽松的 GTA 判据会把它漏过去（实际漏了 2 篇）。
    u = t.upper().replace(" ", "")
    if lang == "zh" and "GTA6" not in u and "GTAVI" not in u:
        return "《GTA6》" + t
    return t


def yaml(s):
    return '"' + str(s).replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    ap.add_argument("--only", type=str)
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    rows = list(csv.DictReader(open(MAP_CSV, encoding="utf-8-sig")))
    if args.only:
        keep = {int(x) for x in args.only.split(",")}
        rows = [r for r in rows if int(r["idx"]) in keep]
    if args.limit:
        rows = rows[:args.limit]

    store, stats = {}, {"pages": 0, "img_slots": 0, "img_uniq": 0, "img_bytes": 0,
                        "sections": 0, "tables": 0, "chars": 0, "promoted": 0, "skipped": []}
    for r in rows:
        path = os.path.join(DOCX_DIR, r["src"])
        if not os.path.exists(path):
            stats["skipped"].append(r["slug_en"]); continue
        blocks, media = parse_docx(path)
        # 给图片块挂上原始字节 + 上下文 alt
        last_h = ""
        for b in blocks:
            if b["k"] == "h":
                last_h = b["t"]
            elif b["k"] == "img":
                b["raw"] = media.get(b["src"], b"")
                b["alt"] = last_h[:70]
        sp = split_at(blocks)
        if sp is None:
            stats["skipped"].append(r["slug_en"]); continue
        zh, en = blocks[:sp], blocks[sp:]

        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
        # 先各算一遍封面：中英两半共用同一篇文章，英文半边偶尔一张图都没有
        # （图都落在中文那半），此时借用中文的封面 —— 否则英文卡片是空的。
        cov = {}
        for _lang, _seg in (("zh", zh), ("en", en)):
            if _seg:
                _hit = next((b for b in _seg if b["k"] == "img" and b.get("raw")), None)
                if _hit:
                    _info = ensure_media(store, _hit["raw"], args.dry)
                    if _info:
                        cov[_lang] = _info["url"]
        for lang, seg in (("zh", zh), ("en", en)):
            if not seg:
                continue
            title = localize_title(r["title_zh"] if lang == "zh" else r["title_en"], lang)
            seg = drop_title(list(seg), title)
            stats["promoted"] += promote(seg, title)
            body, cover = md_with_images(seg, store, args.dry)
            if not body:
                continue
            if not cover:
                cover = cov.get("zh") if lang == "en" else None
            if cover:  # 封面由版式渲染成 hero，正文里再去掉同一张
                b0, sep, b1 = body.partition("## ")
                b0 = re.sub(r"^!\[[^\]]*\]\(" + re.escape(cover) + r"\)\s*$", "", b0, flags=re.M)
                body = (b0 + sep + b1).strip()
            # 页面导语 = 正文第一段（完整），SEO 描述 = 同一段的句末截断
            paras = [b["t"] for b in seg if b["k"] == "p"]
            # 原文开头常是规格行（"OS: Windows 10 64-bit"），当导语会莫名其妙 —— 优先取像句子的那段
            lede = next((p for p in paras if len(p) >= 60), paras[0] if paras else title)
            lede = re.sub(r"\s+", " ", lede).strip()
            desc = make_desc(lede)
            fm = [
                "---",
                f"title: {yaml(title)}",
                f"description: {yaml(desc)}",
                f"dek: {yaml(lede)}",
                f"lang: {lang}",
                f"slug: {yaml(r['slug_en'])}",
                f"section: {r['section']}",
                f"subcategory: {r['subcat'] or 'null'}",
                f"order: {int(r['idx'])}",
                f"date: {mtime:%Y-%m-%d}",
                f"updated: {mtime:%Y-%m-%d}",
                f"cover: {yaml(cover or '')}",
                f"sourceFile: {yaml(r['src'])}",
                "draft: false",
                "---",
                "",
            ]
            outdir = os.path.join(CONTENT_DIR, lang)
            if not args.dry:
                os.makedirs(outdir, exist_ok=True)
                with open(os.path.join(outdir, f"{r['slug_en']}.md"), "w", encoding="utf-8") as f:
                    f.write("\n".join(fm) + add_jsapi(body) + "\n")
            stats["pages"] += 1
            stats["chars"] += len(body)
            stats["sections"] += sum(1 for b in seg if b["k"] == "h")
            stats["tables"] += sum(1 for b in seg if b["k"] == "tbl")
            stats["img_slots"] += sum(1 for b in seg if b["k"] == "img")

    stats["img_uniq"] = len([v for v in store.values() if v])
    stats["img_bytes"] = sum(v["bytes"] for v in store.values() if v)
    print(json.dumps(stats, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
