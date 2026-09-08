# -*- coding: utf-8 -*-
"""深挖3篇问题课件的错误内容量级与结构完整性"""
import re

CASES = {
    'puliurenjia-liushaotang.html': ['鲁迅', '呐喊', '刘绍棠', '蒲柳人家'],
    'zaoer-sunhong.html': ['朱自清', '背影', '孙鸿', '枣儿'],
    'manjianghong-qiujin.html': ['辛弃疾', '带湖', '淳熙', '秋瑾', '小住京华', '京华'],
}

for f, keys in CASES.items():
    s = open(f, 'rb').read().decode('utf-8', errors='ignore')
    print('=' * 14, f, '=' * 14)
    # 各区是否存在
    secs = re.findall(r'<section[^>]*id="([a-z]+)"', s)
    print('  sections:', secs, '| acc缺失' if 'acc' not in secs else '')
    # 关键词在各区分布
    for key in keys:
        hits = []
        for sec in ['bg', 'jielu', 'app', 'acc', 'practice'] + ['hero']:
            if sec == 'hero':
                m = re.search(r'<div class="hero".*?<main', s, re.S)
                if m and key in m.group(0):
                    hits.append('hero')
            else:
                mm = re.search(r'<section[^>]*id="%s"[^>]*>(.*?)(?=<section|<footer|$)' % sec, s, re.S)
                if mm and key in mm.group(1):
                    hits.append(sec)
        print(f'    {key}: {hits}')
    # 作者简介盒内容（背景区第一个box）
    mbg = re.search(r'<section[^>]*id="bg"[^>]*>(.*?)(?=<section)', s, re.S)
    if mbg:
        p = re.search(r'<h3>作者简介</h3>\s*<p>(.*?)</p>', mbg.group(1), re.S)
        if p:
            print('    作者简介首句:', re.sub(r'<[^>]+>', '', p.group(1)).strip()[:80])
    print()
