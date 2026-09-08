# -*- coding: utf-8 -*-
"""蒲柳人家：背景区与赏析区全文，评估保留"""
import re

s = open('puliurenjia-liushaotang.html', 'rb').read().decode('utf-8')
mbg = re.search(r'<section[^>]*id="bg"[^>]*>(.*?)(?=<section)', s, re.S)
print('===== 背景区全文 =====')
print(re.sub(r'\n\s*\n', '\n', mbg.group(1))[:4200])
ma = re.search(r'<section[^>]*id="app"[^>]*>(.*?)(?=<section)', s, re.S)
print()
print('===== 赏析区全文 =====')
print(re.sub(r'\n\s*\n', '\n', ma.group(1))[:3000])
