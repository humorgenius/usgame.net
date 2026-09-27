#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
全站链接审计：跑完 dist 里每个 HTML，把每个 <a href> 都验一遍。

三道门：
  1) 站内链接必须能在 dist 里找到落地文件
  2) 页内锚点 #xxx 必须真有 id="xxx"（不然点了没反应）
  3) 指向文章页的链接，其**链接文字必须能在目标页标题里对上**

第 3 条是关键：前两条只能证明「点的东西存在」，证明不了「它到得了文章」。
首页曾有一批 href="#news" 的卡片 —— 首页自己就有 id="news"，所以前两条一路放行，
但点下去只在页面里滚一下。假链接就是靠第 3 条抓出来的。

用法：python scripts/linkcheck.py    退出码 0 = 全通
"""
import os, re, sys, glob, html as H
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
LANG_SWITCH = {"EN", "中文", "English", "简体中文"}


def norm(s):
    s = H.unescape(s or "")
    return re.sub(r"[\s\u00a0]+", "", s).replace("\u201c", '"').replace("\u201d", '"')


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self._a, self._t = [], set(), None, []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        if d.get("name"):
            self.ids.add(d["name"])
        if tag == "a":
            self._a, self._t = d.get("href"), []

    def handle_data(self, data):
        if self._a is not None:
            self._t.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._a is not None:
            self.links.append((self._a, " ".join(self._t)))
            self._a = None


def to_file(url):
    u = url.split("#")[0].split("?")[0]
    if not u.startswith("/"):
        return None
    p = os.path.join(DIST, u.lstrip("/").replace("/", os.sep))
    return os.path.join(p, "index.html") if (u.endswith("/") or os.path.isdir(p)) else p


def read(f):
    return open(f, encoding="utf-8").read()


def title_of(url, cache):
    f = to_file(url)
    if not f or not os.path.exists(f):
        return None
    if url not in cache:
        h = read(f)
        m = (re.search(r'<h1 class="art-title">([^<]+)</h1>', h)
             or re.search(r"<h1[^>]*>([^<]+)</h1>", h)
             or re.search(r"<title>([^<]+?) \| USGAME</title>", h))
        cache[url] = H.unescape(m.group(1)).strip() if m else ""
    return cache[url]


def main():
    pages = {}
    for f in sorted(glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(f, DIST).replace("\\", "/")
        pages["/" + (rel[:-len("index.html")] if rel.endswith("/index.html") else rel)] = f

    parsed = {}
    for url, f in pages.items():
        p = Page(); p.feed(read(f)); parsed[url] = p

    n = {"内部": 0, "锚点": 0, "外链": 0, "其他": 0}
    problems, tcheck, tcache = [], 0, {}

    for url, p in parsed.items():
        for href, text in p.links:
            if not href:
                problems.append((url, "(空)", "没有 href")); continue
            if href.startswith("#"):
                n["锚点"] += 1
                frag = href[1:]
                if not frag:
                    problems.append((url, href, "空锚点，点了只会跳页顶"))
                elif frag not in p.ids:
                    problems.append((url, href, '本页没有 id="%s"' % frag))
            elif href.startswith("/"):
                n["内部"] += 1
                tf = to_file(href)
                if not tf or not os.path.exists(tf):
                    problems.append((url, href, "dist 里没有落地文件")); continue
                if "#" in href:
                    base, frag = href.split("#", 1)
                    tp = parsed.get("/" + base.strip("/") + "/")
                    if tp and frag and frag not in tp.ids:
                        problems.append((url, href, '目标页没有 id="%s"' % frag))
                if re.match(r"^/(en|zh)/[^/]+/[^/]+/$", href) and href != url:
                    if norm(text) in LANG_SWITCH or len(norm(text)) < 6:
                        continue
                    tt = title_of(href, tcache); tcheck += 1
                    if tt and norm(tt) not in norm(text):
                        problems.append((url, href, "链接文字与目标标题不符 | %s  ≠  %s"
                                         % (text.strip()[:38], tt[:38])))
            elif href.startswith(("http://", "https://")):
                n["外链"] += 1
            else:
                n["其他"] += 1

    print("页面数: %d" % len(pages))
    print("链接分类: " + "  ".join("%s %d" % (k, v) for k, v in n.items()))
    print("文字↔标题核对: %d 条" % tcheck)
    print()
    if problems:
        print("问题链接: %d 条" % len(problems))
        by = {}
        for u, h, why in problems:
            by.setdefault((h, why), []).append(u)
        for (h, why), us in sorted(by.items(), key=lambda x: -len(x[1])):
            print("  [%3d 次] %-38s %s" % (len(us), h[:38], why))
            print("           例: %s" % us[0])
        print()
        print("最脏的页面:")
        c = {}
        for u, h, why in problems:
            c[u] = c.get(u, 0) + 1
        for u, k in sorted(c.items(), key=lambda x: -x[1])[:10]:
            print("  %3d  %s" % (k, u))
        return 1
    print("问题链接: 0 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
