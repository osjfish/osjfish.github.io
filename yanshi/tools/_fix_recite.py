# -*- coding: utf-8 -*-
"""Fix recite-mode defects in the three flagged files:
   - taikongyiri-yangliwei.html: remove dead inline onclicks; fulltext <p> -> <div class="pl">
   - jinianbaiqiuen-maozedong.html: fulltext <p> -> <div class="pl">
   - qieduji-linhaiyin.html: fulltext <p> -> <div class="pl">
"""
import re, os

ROOT = r"D:\App\Apps\yanshi"

FILES = [
    "taikongyiri-yangliwei.html",
    "jinianbaiqiuen-maozedong.html",
    "qieduji-linhaiyin.html",
]

def fulltext_range(s):
    start = s.find('<div id="fulltext"')
    if start == -1:
        return None
    tag_end = s.find('>', start)
    if tag_end == -1:
        return None
    content_start = tag_end + 1
    depth = 1
    i = content_start
    while i < len(s):
        if s.startswith('<div', i):
            depth += 1
            i += 4
        elif s.startswith('</div>', i):
            depth -= 1
            if depth == 0:
                return content_start, i
            i += 6
        else:
            i += 1
    return None

def fix_html(path):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    orig = s

    # 1) Remove dead inline onclicks from buttons that are also wired via addEventListener.
    s = re.sub(r'(<button\s+id="btnAll")\s+onclick="toggleAll\(\)"\s*', r'\1', s)
    s = re.sub(r'(<button\s+id="btnShowAll")\s+onclick="toggleAll\(\)"\s*', r'\1', s)
    s = re.sub(r'(<button\s+id="btnRecite")\s+onclick="toggleRecite\(\)"\s*', r'\1', s)
    s = re.sub(r'(<button\s+id="btnPrint")\s+onclick="window\.print\(\)"\s*', r'\1', s)

    # 2) Convert direct children <p> of #fulltext to <div class="pl">
    rng = fulltext_range(s)
    if rng:
        a, b = rng
        inner = s[a:b]
        inner2 = re.sub(r'<p\b[^>]*>', '<div class="pl">', inner)
        inner2 = re.sub(r'</p>', '</div>', inner2)
        if inner2 != inner:
            s = s[:a] + inner2 + s[b:]

    if s != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        print("FIXED", os.path.basename(path))
    else:
        print("no change", os.path.basename(path))

for fn in FILES:
    fix_html(os.path.join(ROOT, fn))
