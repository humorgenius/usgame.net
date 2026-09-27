#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build-content-page.py — 把一篇 .doc 成稿渲染成一个双语内容页（A 方案风格）。

这是正式导入流水线（阶段 5）的雏形，先跑通一篇文章看效果。

【发现的结构】每个 .doc 里**中英文同装一个文件**：
    中文标题(Heading3) → 中文正文 → 英文标题(Heading3) → 英文正文
所以「中英配对」这件事不存在，切分点 = 第一个以拉丁字母为主的 Heading3。
两个语言的章节数量、顺序、表格、图片位一一对应（本脚本会断言这一点）。

用法:
  python build-content-page.py <源文件.doc> <输出目录> [slug]
"""
import os, re, sys, zipfile
import xml.etree.ElementTree as ET
from html import escape
from PIL import Image

DESIGN = r"D:/【建立网站】/GTA6/usgame.net/design"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE_SRC = os.path.join(DESIGN, "A-neon-vice", "index.html")
TEMPLATE = os.path.join(SCRIPT_DIR, "page-template.html")
IMG_OUT = os.path.join(DESIGN, "assets", "img")

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


# ---------------------------------------------------------------- parsing ----
def cjk_ratio(s):
    return (sum(1 for ch in s if "\u4e00" <= ch <= "\u9fff") / len(s)) if s else 0


def bold_run(r):
    b = r.find(W + "b")
    return b is not None and b.get(W + "val") not in ("0", "false")


def italic_run(r):
    i = r.find(W + "i")
    return i is not None and i.get(W + "val") not in ("0", "false")


def runs_html(p):
    """paragraph -> html, honouring <w:b/> / <w:i/> so the article keeps its emphasis."""
    out = []
    for r in p.iter(W + "r"):
        txt = "".join(t.text or "" for t in r.iter(W + "t"))
        if not txt:
            continue
        t = escape(txt)
        if bold_run(r):
            t = f"<strong>{t}</strong>"
        if italic_run(r):
            t = f"<em>{t}</em>"
        out.append(t)
    return "".join(out)


def to_docx(path):
    """legacy .doc -> .docx via LibreOffice (measured 2.7s/file); .docx passes straight through."""
    if path.lower().endswith(".docx"):
        return path
    soff = r"C:/Program Files/LibreOffice/program/soffice.exe"
    if not os.path.exists(soff):
        raise SystemExit("需要 LibreOffice 转换 .doc：C:\\Program Files\\LibreOffice\\program\\soffice.exe 不存在")
    out = os.path.join(SCRIPT_DIR, "_docx_cache")
    os.makedirs(out, exist_ok=True)
    stem = os.path.splitext(os.path.basename(path))[0]
    dest = os.path.join(out, stem + ".docx")
    if not os.path.exists(dest) or os.path.getmtime(dest) < os.path.getmtime(path):
        import subprocess
        subprocess.run([soff, "--headless", "--norestore", "--convert-to", "docx",
                        "--outdir", out, path], capture_output=True, timeout=300)
    if not os.path.exists(dest):
        raise SystemExit("转换失败: " + path)
    return dest


def parse_docx(path):
    z = zipfile.ZipFile(path)
    names = set(z.namelist())
    # OOXML relationship targets are relative to word/ — normalise before using them as zip names
    from posixpath import normpath
    rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
    rid2media = {}
    for r in rels:
        t = r.get("Target") or ""
        if "media/" not in t:
            continue
        name = normpath("word/" + t)
        if name not in names:
            cand = [n for n in names if n.endswith(t.split("media/")[-1])]
            if not cand:
                continue
            name = cand[0]
        rid2media[r.get("Id")] = name
    root = ET.fromstring(z.read("word/document.xml"))
    blocks = []
    for el in root.find(W + "body"):
        tag = el.tag.replace(W, "")
        if tag == "p":
            st = el.find(f".//{W}pStyle")
            style = st.get(W + "val") if st is not None else "Normal"
            txt = "".join(t.text or "" for t in el.iter(W + "t")).strip()
            media = [rid2media[b.get(f"{R}embed")] for b in el.iter(f"{A}blip")
                     if b.get(f"{R}embed") in rid2media]
            if txt or media:
                blocks.append({"k": "h" if "Heading" in style else "p",
                               "raw": txt, "html": runs_html(el), "media": media})
        elif tag == "tbl":
            rows = [["".join(t.text or "" for t in tc.iter(W + "t")).strip()
                     for tc in tr.findall(W + "tc")] for tr in el.findall(W + "tr")]
            if rows:
                blocks.append({"k": "table", "rows": rows})
    return blocks, z


def split_locales(blocks):
    for i, b in enumerate(blocks):
        if b["k"] == "h" and len(b["raw"]) > 25 and cjk_ratio(b["raw"]) < 0.05:
            return blocks[:i], blocks[i:]
    raise SystemExit("找不到中英切分点 —— 检查这篇稿子是否含英文段落")


# ------------------------------------------------------------- rendering ----
def render_media(blocks, z, slug, mapping, figcap, alt):
    os.makedirs(IMG_OUT, exist_ok=True)
    for b in blocks:
        out = []
        for m in b.get("media", []):
            if m not in mapping:
                n = len(mapping) + 1
                name = f"art-{slug}-{n}"
                tmp = os.path.join(IMG_OUT, "_tmp_" + name)
                open(tmp, "wb").write(z.read(m))
                im = Image.open(tmp)
                if im.mode in ("P", "RGBA", "LA"):
                    im = im.convert("RGBA")
                    bg = Image.new("RGB", im.size, (11, 7, 16))
                    bg.paste(im, mask=im.split()[-1])
                    im = bg
                else:
                    im = im.convert("RGB")
                if im.width > 1400:
                    im = im.resize((1400, round(im.height * 1400 / im.width)), Image.LANCZOS)
                im.save(os.path.join(IMG_OUT, name + ".webp"), "WEBP", quality=84, method=5)
                os.remove(tmp)
                mapping[m] = {"slug": name, "w": im.width, "h": im.height}
            out.append(mapping[m])
        b["media"] = out
    return blocks


def render_body(blocks, figcap, alt):
    """-> (intro_blocks_html, sections). First paragraph is promoted to the dek by the caller."""
    intro, sections, cur, pending = [], [], None, []

    def target():
        return cur["html"] if cur else intro

    def flush_ul():
        if pending:
            target().append("<ul>" + "".join(f"<li>{x}</li>" for x in pending) + "</ul>")
            pending.clear()

    for b in blocks:
        if b["k"] == "h":
            flush_ul()
            cur = {"id": f"sec-{len(sections) + 1}", "title": b["raw"], "html": []}
            sections.append(cur)
            continue
        if b["k"] == "table":
            flush_ul()
            head, *rest = b["rows"]
            th = "".join(f'<th scope="col">{escape(c)}</th>' for c in head)
            trs = "".join("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in r) + "</tr>" for r in rest)
            target().append(f'<div class="tbl-scroll"><table><thead><tr>{th}</tr></thead>'
                            f"<tbody>{trs}</tbody></table></div>")
            continue
        for m in b["media"]:
            flush_ul()
            target().append(
                f'<figure><img src="../assets/img/{m["slug"]}.webp" alt="{escape(alt)}"'
                f' width="{m["w"]}" height="{m["h"]}" loading="lazy" decoding="async">'
                f"<figcaption>{escape(figcap)}</figcaption></figure>")
        txt = b["raw"]
        if not txt:
            continue
        if txt.startswith(("- ", "– ")):
            pending.append(b["html"][2:].strip())
            continue
        flush_ul()
        if txt.startswith(("“", '"')) and len(txt) < 400:
            target().append(f"<blockquote>{b['html']}</blockquote>")
        else:
            target().append(f"<p>{b['html']}</p>")
    flush_ul()
    return intro, sections


def read_time(text, locale):
    if locale == "zh":
        return max(1, round(len(re.findall(r"[\u4e00-\u9fff]", text)) / 380))
    return max(1, round(len(text.split()) / 230))


def extract_shell():
    src = open(STYLE_SRC, encoding="utf-8").read()
    return (re.search(r"<style[^>]*>(.*?)</style>", src, re.S).group(1),
            re.search(r"<script(?![^>]*src)[^>]*>(.*?)</script>", src, re.S).group(1),
            re.search(r"<header[\s\S]*?</header>", src).group(0),
            re.search(r"<footer[\s\S]*?</footer>", src).group(0))


def plain(s):
    return re.sub(r"<[^>]+>", "", s)


# ------------------------------------------------------------------- main ----
if __name__ == "__main__":
    SRC, OUTDIR = sys.argv[1], sys.argv[2]
    SLUG = sys.argv[3] if len(sys.argv) > 3 else "wanted-level"

    blocks, z = parse_docx(to_docx(SRC))
    zh_all, en_all = split_locales(blocks)
    zh_title_raw, en_title_raw = zh_all[0]["raw"], en_all[0]["raw"]

    mapping = {}
    zh_body = render_media(zh_all[1:], z, SLUG, mapping, "GTA6 官方素材截图 · 图注待替换",
                           "GTA6 通缉系统示意截图")
    en_body = render_media(en_all[1:], z, SLUG, mapping, "Official GTA6 screenshot · caption to be replaced",
                           "GTA6 wanted system screenshot")

    zh_intro, zh_secs = render_body(zh_body, "GTA6 官方素材截图 · 图注待替换", "GTA6 通缉系统示意截图")
    en_intro, en_secs = render_body(en_body, "Official GTA6 screenshot · caption to be replaced",
                                    "GTA6 wanted system screenshot")

    # --- gate: the two locales must be structurally parallel -------------------
    zh_tables = sum(1 for b in zh_body if b["k"] == "table")
    en_tables = sum(1 for b in en_body if b["k"] == "table")
    zh_imgs = sum(len(b["media"]) for b in zh_body)
    en_imgs = sum(len(b["media"]) for b in en_body)
    problems = []
    if len(zh_secs) != len(en_secs):
        problems.append(f"章节数不一致 ZH={len(zh_secs)} EN={len(en_secs)}")
    if zh_tables != en_tables:
        problems.append(f"表格数不一致 ZH={zh_tables} EN={en_tables}")
    if zh_imgs != en_imgs:
        problems.append(f"图片位不一致 ZH={zh_imgs} EN={en_imgs}")
    for k, v in (("ZH", zh_title_raw), ("EN", en_title_raw)):
        if any(c in v for c in '"&<>'):
            problems.append(f"{k} 标题含需转义字符: {v}")
    if problems:
        print("!! 结构门禁未通过:")
        for p in problems:
            print("   -", p)

    zh_dek = plain(zh_intro[0]) if zh_intro else ""
    en_dek = plain(en_intro[0]) if en_intro else ""
    zh_rest = zh_intro[1:]
    en_rest = en_intro[1:]

    def secs_html(secs):
        return "\n".join(f'<section id="{s["id"]}"><h2>{escape(s["title"])}</h2>'
                         + "".join(s["html"]) + "</section>" for s in secs)

    def toc_html(secs):
        return "".join(f'<li><a href="#{s["id"]}">{escape(s["title"])}</a></li>' for s in secs)

    style, script, header, footer = extract_shell()
    html = open(TEMPLATE, encoding="utf-8").read()
    reps = {
        "__STYLE__": style, "__SCRIPT__": script, "__HEADER__": header, "__FOOTER__": footer,
        "__EN_TITLE__": escape(en_title_raw, quote=False),
        "__ZH_TITLE__": escape(zh_title_raw, quote=False),
        "__EN_TITLE_ATTR__": escape(en_title_raw, quote=True),
        "__ZH_TITLE_ATTR__": escape(zh_title_raw, quote=True),
        "__EN_DEK__": escape(en_dek, quote=False),
        "__ZH_DEK__": escape(zh_dek, quote=False),
        "__EN_DEK_ATTR__": escape(en_dek, quote=True),
        "__ZH_DEK_ATTR__": escape(zh_dek, quote=True),
        "__EN_BODY__": "".join(en_rest) + secs_html(en_secs),
        "__ZH_BODY__": "".join(zh_rest) + secs_html(zh_secs),
        "__EN_TOC__": toc_html(en_secs), "__ZH_TOC__": toc_html(zh_secs),
        "__EN_MIN__": str(read_time(" ".join(b.get("raw", "") for b in en_body), "en")),
        "__ZH_MIN__": str(read_time(" ".join(b.get("raw", "") for b in zh_body), "zh")),
        "__SLUG_EN__": SLUG, "__SLUG_ZH__": SLUG,
    }
    for k, v in reps.items():
        html = html.replace(k, v)
    left = sorted(set(re.findall(r"__[A-Z_]+__", html)))
    if left:
        print("!! 未替换的占位符:", left)

    os.makedirs(OUTDIR, exist_ok=True)
    dest = os.path.join(OUTDIR, "index.html")
    open(dest, "w", encoding="utf-8").write(html)
    print(f"OK  {dest}   {len(html)} chars")
    print(f"    ZH  {len(zh_secs)} sections / {zh_tables} tables / {zh_imgs} figures / "
          f"{reps['__ZH_MIN__']} min read")
    print(f"    EN  {len(en_secs)} sections / {en_tables} tables / {en_imgs} figures / "
          f"{reps['__EN_MIN__']} min read")
    print(f"    images -> " + ", ".join(v["slug"] + ".webp" for v in mapping.values()))
    print("    结构门禁: " + ("通过" if not problems else "未通过"))
