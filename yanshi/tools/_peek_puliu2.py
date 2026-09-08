# -*- coding: utf-8 -*-
"""蒲柳人家：全部卡片文本 + hero + kai"""
import re

s = open('puliurenjia-liushaotang.html', 'rb').read().decode('utf-8')
# body 开头 600 字
b = s.find('<body')
print('=== BODY 开头 ===')
print(s[b:b + 620])
print()
mj = re.search(r'<section[^>]*id="jielu"[^>]*>(.*?)(?=<section)', s, re.S)
j = mj.group(1)
print('=== 17 卡文本 ===')
for m in re.finditer(r'<div class="v-no">(\d+)</div>', j):
    seg = j[m.end():m.end() + 1500]
    vl = re.search(r'<div class="v-line">(.*?)</div>', seg, re.S)
    if vl:
        print('卡%s: %s' % (m.group(1), re.sub(r'<[^>]+>', '', vl.group(1)).strip()[:64]))
print()
i = s.find('class="kai"')
print('=== KAI ===')
print(s[i - 60:i + 160])
