# -*- coding: utf-8 -*-
import io
path = r'D:\App\Apps\yanshi\tools\gen_dengjiaxian.py'
src = io.open(path, encoding='utf-8').read()
lines = src.split('\n')
bad = []
for i, line in enumerate(lines, 1):
    if line.count('"') > 2 and not line.strip().startswith('#'):
        bad.append((i, line.count('"'), line.strip()[:80]))
print('Lines with >2 quotes:', len(bad))
for b in bad:
    print(b)
