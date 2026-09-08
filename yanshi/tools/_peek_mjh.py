# -*- coding: utf-8 -*-
"""查看满江红解读卡片内容"""
import re

s = open('manjianghong-qiujin.html', 'rb').read().decode('utf-8')
mj = re.search(r'<section[^>]*id="jielu"[^>]*>(.*?)(?=<section)', s, re.S)
j = mj.group(1)
# 松匹配：按 v-no 分卡
for m in re.finditer(r'<span class="v-no">(\d+)</span>', j):
    seg = j[m.end():m.end() + 1200]
    vl = re.search(r'<div class="v-line"[^>]*>(.*?)</div>', seg, re.S)
    print('卡%s: %s' % (m.group(1), re.sub(r'<[^>]+>', '', vl.group(1)).strip()[:70] if vl else '?'))
