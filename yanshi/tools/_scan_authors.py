# -*- coding: utf-8 -*-
"""全库扫描：每篇课文的 hero 作者行 + 作者简介首句，供核对张冠李戴"""
import glob, re, json

out = []
for f in sorted(glob.glob('*.html')):
    s = open(f, 'rb').read().decode('utf-8', errors='ignore')
    # hero 侧栏第一行：朝代 · 作者
    m = re.search(r'<div class="hero-side[^"]*"[^>]*>\s*<div>([^<]{1,30})</div>', s, re.S)
    side = m.group(1).strip() if m else '?'
    # 选自行（kai 块附近：作者 · 现代 · 选自…）
    m2 = re.search(r'<div class="kai">([^<]{1,30})</div>\s*<div>([^<]{1,60})</div>', s, re.S)
    kai = (m2.group(1).strip() + ' ｜ ' + m2.group(2).strip()) if m2 else '?'
    out.append({'f': f, 'side': side, 'kai': kai})

for o in out:
    print('%-62s | %-18s | %s' % (o['f'], o['side'], o['kai'][:56]))
