# -*- coding: utf-8 -*-
"""修复gen脚本中ASCII引号问题：将字符串内部的"替换为中文引号（交替左右）"""
path = r"D:\App\Apps\yanshi\tools\gen_huangdindexinzhuang.py"
with open(path, 'r', encoding='utf-8') as f:
    src = f.read()

out = []
i = 0
n = len(src)
in_str = False
str_char = None
in_comment = False
in_triple = False
cn_quote_open = False  # tracking Chinese quote pair state

while i < n:
    c = src[i]
    nxt = src[i+1] if i+1 < n else ''
    nxt2 = src[i+2] if i+2 < n else ''

    # Triple quotes
    if c == '"' and nxt == '"' and nxt2 == '"':
        if in_triple:
            out.append('"""'); in_triple = False; i += 3; continue
        elif not in_str:
            out.append('"""'); in_triple = True; i += 3; continue

    if in_triple:
        out.append(c); i += 1; continue

    # Comments
    if not in_str and c == '#':
        in_comment = True
    if in_comment:
        out.append(c)
        if c == '\n': in_comment = False
        i += 1; continue

    # String start
    if not in_str:
        if c == '"' or c == "'":
            in_str = True; str_char = c; cn_quote_open = False
            out.append(c); i += 1; continue
        out.append(c); i += 1; continue

    # Inside string
    if c == '\\':
        out.append(c)
        if nxt: out.append(nxt); i += 2
        else: i += 1
        continue

    if c == str_char:
        # Check if closing delimiter
        j = i + 1
        while j < n and src[j] in ' \t':
            j += 1
        if j >= n or src[j] in ',)]}:\n+':
            out.append(c); in_str = False; str_char = None; i += 1; continue
        else:
            # Inner quote: alternate left/right
            if not cn_quote_open:
                out.append('\u201c')  # left "
                cn_quote_open = True
            else:
                out.append('\u201d')  # right "
                cn_quote_open = False
            i += 1; continue

    out.append(c); i += 1

fixed = ''.join(out)
with open(path, 'w', encoding='utf-8') as f:
    f.write(fixed)
print("Fixed. Length:", len(fixed))
