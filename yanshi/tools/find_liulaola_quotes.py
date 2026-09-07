# -*- coding: utf-8 -*-
"""Find remaining quote patterns in 刘姥姥"""
import re

p = r'D:\App\Apps\yanshi\liulaolaojindaguanyuan-caoxueqin.html'
with open(p, 'r', encoding='utf-8') as f:
    h = f.read()

for m in re.finditer(r'" \+', h):
    start = max(0, m.start() - 30)
    end = min(len(h), m.end() + 30)
    print(repr(h[start:end]))
    print('---')
