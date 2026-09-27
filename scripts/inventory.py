#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
73 篇 .doc 的内容盘点 + 栏目归属，产出两个 CSV：

  docs/content-inventory.csv  每篇的标题/章节/字数/表格/图片位（纯事实）
  docs/content-map.csv        上面的全部字段 + 栏目归属 + 英文 slug（供入库用）

前置：先把 .doc 批量转成 .docx（LibreOffice 一次调用传全部文件，见 README）：
  soffice --headless --convert-to docx --outdir <缓存目录> <源目录>/*.doc

⚠ 这些稿件的结构不统一，标题有三种落法，脚本按优先级判断：
  ① 标题是「普通段落」放在正文之前（角色档案类，如 布莱恩·赫德 / 露西亚 / 卡尔·汉普顿）
  ② 标题是第一个 Heading3（多数系统/新闻类）
  ③ 压根没有标题段，只有文件名可信 —— 所以 **中文标题一律取文件名**（作者自己的命名，73/73 可靠）

用法:  python scripts/inventory.py            # 盘点 + 分类
       python scripts/inventory.py --check    # 只跑门禁，不写文件
"""
import os, re, csv, sys, zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
DOCX_DIR = r"E:/hermes-workspace/temp/docx_all"
DOCS = r"D:/【建立网站】/GTA6/usgame.net/docs"

CJK = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")
LATIN = re.compile(r"[A-Za-z]")

# ---------------------------------------------------------------- 栏目归属
# 索引号 = 源文件按文件名排序后的序号（= content-inventory.csv 的 idx 列）
NEWS = (3, 4, 5, 6, 9, 13, 18, 38, 39, 48, 55, 61, 68)
CHARACTERS = (12, 16, 24, 25, 26, 28, 32, 36, 50, 64)
MAP = (19, 20, 35, 37, 46, 72)
VEHICLES = (34, 59, 69)
WEAPONS = (33,)
VIDEOS = (66, 67)
FAQ = (71,)
GUIDES = {
    "systems":    (2, 10, 15, 22, 23, 30, 31, 56, 58, 65, 73),
    "crime":      (27, 41, 42, 53, 54, 57, 60, 70),
    "world":      (14, 21, 44, 49, 52, 62),
    "activities": (11, 29, 40, 51, 63),
    "story":      (1, 7, 8, 17, 43, 45, 47),
}
CLASS = {i: ("news", "") for i in NEWS}
CLASS |= {i: ("characters", "") for i in CHARACTERS}
CLASS |= {i: ("map", "") for i in MAP}
CLASS |= {i: ("vehicles", "") for i in VEHICLES}
CLASS |= {i: ("weapons", "") for i in WEAPONS}
CLASS |= {i: ("videos", "") for i in VIDEOS}
CLASS |= {i: ("faq", "") for i in FAQ}
for _sub, _ids in GUIDES.items():
    CLASS |= {i: ("guides", _sub) for i in _ids}

# 这 9 篇的英文标题不是独立段落（英文侧没有对应标题行），只能按中文标题重新本地化。
# 其余 64 篇的英文标题就是英文侧第一个 Heading3，自动取。
EN_TITLE_OVERRIDES = {
    12: "All GTA6 Characters at a Glance: Backgrounds, Motives and Where They Fit",
    16: "GTA6 Cal Hampton Character Profile: The Paranoid Friend Who Never Leaves Home",
    17: "How GTA6 Is About to Reinvent the Best Experience in Gaming",
    24: "GTA6 Brian Heder Character Profile: The Complete Dossier on a Keys Smuggling Legend",
    25: "GTA6 Dre'Quan Priest Character Profile: From Street Hustler to Music Mogul",
    28: "GTA6 Raul Bautista Character Profile: The Confident Career Bank Robber",
    39: "GTA6 PC System Requirements: Predicted Minimum, Recommended and 4K Specs",
    64: "GTA6 Lucia Caminos Character Profile: Out of Prison and Ready to Rewrite Her Fate",
    71: "Six Big GTA6 Questions We Still Can't Answer",
}


def cjk_ratio(s):
    n = len(CJK.findall(s)) + len(LATIN.findall(s))
    return len(CJK.findall(s)) / n if n else 0.0


def parse(f):
    """-> [{'s':样式,'t':文本,'h':是否标题}, …]"""
    with zipfile.ZipFile(os.path.join(DOCX_DIR, f)) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    out = []
    for el in root.find(f"{W}body"):
        if el.tag != f"{W}p":
            continue
        pr = el.find(f"{W}pPr")
        st = ""
        if pr is not None:
            s = pr.find(f"{W}pStyle")
            st = s.get(f"{W}val", "") if s is not None else ""
        t = re.sub(r"\s+", " ", "".join(x.text or "" for x in el.iter(f"{W}t"))).strip()
        if t:
            out.append({"s": st, "t": t, "h": "Heading" in st or "标题" in st})
    return out


def split_at(ps):
    """中英切分点 = 第一个拉丁为主的标题段；若它前一段也是拉丁为主的正文段，
    说明英文标题是普通段落（落法①），切分点整体前移一格。"""
    for j, p in enumerate(ps):
        if p["h"] and j >= 3 and len(p["t"]) >= 12 and cjk_ratio(p["t"]) < 0.05:
            k = j
            prev = ps[k - 1]
            if k and not prev["h"] and cjk_ratio(prev["t"]) < 0.05 and len(prev["t"]) >= 12:
                k -= 1
            return k
    for j, p in enumerate(ps):
        if j >= 4 and len(p["t"]) >= 15 and cjk_ratio(p["t"]) < 0.05:
            return j
    return None


def title_zh(f):
    """作者自己的命名就是文件名，去掉书名号前缀。"""
    return re.sub(r"^《GTA6?》\s*", "", f[:-5]).strip()


def slugify(t):
    t = re.sub(r"['\u2019\u201c\u201d]", "", t.lower())
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", t)).strip("-")[:72]


def collect():
    rows = []
    for i, f in enumerate(sorted(x for x in os.listdir(DOCX_DIR) if x.endswith(".docx")), 1):
        ps = parse(f)
        sp = split_at(ps)
        zh, en = (ps[:sp], ps[sp:]) if sp is not None else (ps, [])
        sec = [p["t"] for p in zh if p["h"]]
        en_title = EN_TITLE_OVERRIDES.get(i) or next(
            (p["t"] for p in en if cjk_ratio(p["t"]) < 0.30 and len(p["t"]) >= 10), "")
        rows.append(dict(
            idx=i, src=f, section=CLASS[i][0], subcat=CLASS[i][1],
            title_zh=title_zh(f), title_en=en_title, slug_en=slugify(en_title),
            sections=len(sec), chars_zh=sum(len(p["t"]) for p in zh),
            chars_en=sum(len(p["t"]) for p in en),
            top_sections=" | ".join(sec[:4]), split_ok=sp is not None,
        ))
    return rows


def gate(rows):
    """入库前门禁：任何一条不过就退出 1，不允许半成品进流水线。"""
    bad = []
    if len(rows) != 73:
        bad.append(f"篇数应为 73，实为 {len(rows)}")
    for r in rows:
        if not r["split_ok"]:
            bad.append(f"[{r['idx']}] 找不到中英切分点")
        if len(r["title_zh"]) < 6:
            bad.append(f"[{r['idx']}] 中文标题过短")
        if len(r["title_en"]) < 10:
            bad.append(f"[{r['idx']}] 缺英文标题")
        if r["section"] not in {"news", "guides", "characters", "map",
                                "vehicles", "weapons", "videos", "faq"}:
            bad.append(f"[{r['idx']}] 栏目非法: {r['section']}")
    seen = {}
    for r in rows:
        seen.setdefault(r["slug_en"], []).append(r["idx"])
    for s, ids in seen.items():
        if len(ids) > 1:
            bad.append(f"slug 重复 {s!r}: {ids}")
    for r in rows:
        if r["section"] == "guides" and not r["subcat"]:
            bad.append(f"[{r['idx']}] guides 缺子类")
    return bad


def write_csv(path, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    rows = collect()
    bad = gate(rows)
    for b in bad:
        print("  ✗", b)
    if bad:
        sys.exit(1)

    if "--check" in sys.argv:
        print(f"门禁通过：{len(rows)} 篇，{len({r['section'] for r in rows})} 个栏目")
        return

    inv = [{k: v for k, v in r.items() if k != "subcat"} for r in rows]
    write_csv(os.path.join(DOCS, "content-inventory.csv"), inv)
    write_csv(os.path.join(DOCS, "content-map.csv"), rows)

    from collections import Counter
    print(f"门禁通过：{len(rows)} 篇 / 中文 {sum(r['chars_zh'] for r in rows):,} 字 / "
          f"英文 {sum(r['chars_en'] for r in rows):,} 字符 / {sum(r['sections'] for r in rows)} 个章节")
    print("栏目分布:", "  ".join(f"{k}={v}" for k, v in
          Counter(f"{r['section']}{'/' + r['subcat'] if r['subcat'] else ''}"
                  for r in rows).most_common()))


if __name__ == "__main__":
    main()
