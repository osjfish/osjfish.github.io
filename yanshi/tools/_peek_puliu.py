# -*- coding: utf-8 -*-
"""查看蒲柳人家结构：背景区各盒、解读卡片、赏析、练习，评估重写范围"""
import re

s = open('puliurenjia-liushaotang.html', 'rb').read().decode('utf-8')

mbg = re.search(r'<section[^>]*id="bg"[^>]*>(.*?)(?=<section)', s, re.S)
bg = mbg.group(1)
print('=== 背景区盒子与标题 ===')
for m in re.finditer(r'<h3[^>]*>([^<]*)</h3>', bg):
    print('  h3:', m.group(1))
print('  视频标题:', re.findall(r'<h4[^>]*>([^<]*)</h4>', bg))

mj = re.search(r'<section[^>]*id="jielu"[^>]*>(.*?)(?=<section)', s, re.S)
j = mj.group(1)
print()
print('=== 解读区 ===')
print('verse卡:', j.count('class="verse"'), '| v-no:', len(re.findall(r'class="v-no"', j)), '| part-head:', j.count('part-head'))
for m in re.finditer(r'<span class="v-no">(\d+)</span>', j):
    seg = j[m.end():m.end() + 1200]
    vl = re.search(r'<div class="v-line"[^>]*>(.*?)</div>', seg, re.S)
    if vl:
        print('  卡%s: %s' % (m.group(1), re.sub(r'<[^>]+>', '', vl.group(1)).strip()[:55]))

ma = re.search(r'<section[^>]*id="app"[^>]*>(.*?)(?=<section)', s, re.S)
print()
print('=== 赏析区 h3 ===', re.findall(r'<h3[^>]*>([^<]*)</h3>', ma.group(1)))
mp = re.search(r'<section[^>]*id="practice"[^>]*>(.*?)(?=<section|<footer)', s, re.S)
print()
print('=== 练习区按钮 ===', re.findall(r'<button[^>]*>([^<]+)</button>', mp.group(1))[:4])
print('=== hero 侧栏 ===')
mh = re.search(r'hero-side', s)
i = s.find('hero-side')
print(s[i:i + 260])
