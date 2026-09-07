# -*- coding: utf-8 -*-
"""修复指定Python文件中的ASCII引号（数据区）"""
import sys

path = sys.argv[1] if len(sys.argv) > 1 else r'D:\App\Apps\yanshi\tools\data_nvwa.py'
with open(path, 'r', encoding='utf-8') as f:
    src = f.read()

out = []
i = 0
n = len(src)
in_str = False
str_char = None
in_comment = False
cn_open = False

while i < n:
    c = src[i]
    nxt = src[i+1] if i+1 < n else ''
    if not in_str and c == '#':
        in_comment = True
    if in_comment:
        out.append(c)
        if c == '\n':
            in_comment = False
        i += 1
        continue
    if not in_str:
        if c == '"' or c == "'":
            in_str = True
            str_char = c
            cn_open = False
            out.append(c)
            i += 1
            continue
        out.append(c)
        i += 1
        continue
    if c == '\\':
        out.append(c)
        if nxt:
            out.append(nxt)
            i += 2
        else:
            i += 1
        continue
    if c == str_char:
        j = i + 1
        while j < n and src[j] in ' \t':
            j += 1
        if j >= n or src[j] in ',)]}:\n+':
            out.append(c)
            in_str = False
            str_char = None
            i += 1
            continue
        else:
            if not cn_open:
                out.append('\u201c')
                cn_open = True
            else:
                out.append('\u201d')
                cn_open = False
            i += 1
            continue
    out.append(c)
    i += 1

fixed = ''.join(out)
with open(path, 'w', encoding='utf-8') as f:
    f.write(fixed)
print('Fixed:', path, len(fixed), 'chars')
