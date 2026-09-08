# -*- coding: utf-8 -*-
"""九下最近批次课件体检：作者/朝代/选自/标题/结构"""
import re

FILES = [
    'achangyushanhaijing-luxun.html',      # 聂鲁达？文件名对不上
    'haiyan-gaoerji.html',
    'tianxiadiyilou-hejiping.html',
    'tandushu-peigen.html',
    'buqiushenjie-manancun.html',
    'shanshuihuadeyijing-likeran.html',
    'wuyanzhimei-zhuguangqian.html',
    'quqianwomendexiangxiang-yetaotao.html',
    'zaoer-sunhong.html',
    'manjianghong-qiujin.html',
    'puliurenjia-liushaotang.html',
]

for f in FILES:
    s = open(f, 'rb').read().decode('utf-8', errors='ignore')
    # hero 侧栏（朝代·作者·选自）
    hero = re.search(r'<div class="hero-side[^"]*"[^>]*>(.*?)</div>\s*</div>', s, re.S)
    side = re.sub(r'<[^>]+>', ' | ', hero.group(1)) if hero else '(未找到hero-side)'
    side = re.sub(r'(\s*\|\s*)+', ' | ', side).strip(' |')
    title = re.search(r'class="hero-title[^"]*"[^>]*>(.*?)</', s, re.S)
    nav_a = re.search(r'<title>(.*?)</title>', s, re.S)
    secs = re.findall(r'<section[^>]*id="([a-z]+)"', s)
    print(f'--- {f}')
    print('    title:', (nav_a.group(1).strip() if nav_a else '?')[:40])
    print('    hero标题:', (title.group(1).strip() if title else '?')[:30])
    print('    侧栏:', side[:80])
    print('    sections:', secs)
