# -*- coding: utf-8 -*-
import io
p = r'D:\App\Apps\yanshi\tools\gen_lunjiaoyang.py'
h = io.open(p, encoding='utf-8').read()
lines = h.split('\n')
for i, line in enumerate(lines):
    stripped = line.lstrip()
    if stripped.startswith('\u201c') and (stripped.endswith('\u201d,') or stripped.endswith('\u201d')):
        idx1 = line.index('\u201c')
        line = line[:idx1] + '"' + line[idx1+1:]
        idx2 = line.rindex('\u201d')
        line = line[:idx2] + '"' + line[idx2+1:]
        lines[i] = line
h = '\n'.join(lines)
io.open(p, 'w', encoding='utf-8').write(h)
print('restored delimiter quotes')
