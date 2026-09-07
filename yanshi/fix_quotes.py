# -*- coding: utf-8 -*-
import re

with open(r'D:\App\Apps\yanshi\gen_zhuangzihaoliang.py', 'r', encoding='utf-8') as f:
    content = f.read()

def repl(m):
    s = m.group(0)
    inner = s[1:-1]
    ascii_q = '\u0022'
    if ascii_q in inner:
        parts = inner.split(ascii_q)
        new_inner = parts[0]
        for j, p in enumerate(parts[1:]):
            if j % 2 == 0:
                new_inner += '\u201c' + p
            else:
                new_inner += '\u201d' + p
        inner = new_inner
    return s[0] + inner + s[-1]

content = re.sub(r'\u0022[^\u0022\n]*\u0022', repl, content)

with open(r'D:\App\Apps\yanshi\gen_zhuangzihaoliang.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('done')
