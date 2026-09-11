# -*- coding: utf-8 -*-
"""清理编号 h3 里重复的括号：<h3>一、第1—4段（第1—4段）</h3> → <h3>一、第1—4段</h3>"""
import os, re, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\App\Apps\yanshi'
CN = '一二三四五六七八九十'
pat = re.compile(r'(<h3[^>]*>\s*[' + CN + r']、\s*[^<（）]*?)（([^（）<]*)）(\s*</h3>)')
n = 0
for f in sorted(os.listdir(ROOT)):
    if not f.endswith('.html'):
        continue
    p = os.path.join(ROOT, f)
    s = open(p, encoding='utf-8').read()

    def rep(m):
        global n
        a, b, c = m.group(1), m.group(2), m.group(3)
        head = a.split('、', 1)[-1].strip()
        if b and b in head:
            n += 1
            return a.rstrip() + c
        return m.group(0)

    s2 = pat.sub(rep, s)
    if s2 != s:
        open(p, 'w', encoding='utf-8').write(s2)
        print('清理', f)
print('共清理', n)
