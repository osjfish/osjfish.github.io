# -*- coding: utf-8 -*-
"""6篇退化篇解读区现状"""
import re

FILES = ['tongyi-nieluda.html', 'fengyuyin-ludi.html', 'duanzhang-bianzhilin.html',
         'weixuanzedelu-fuluosite.html', 'jiarushenghuoqipianleni-puxijin.html',
         'woweishimeerhuozhe-luosu.html']
for f in FILES:
    s = open(f, 'rb').read().decode('utf-8', errors='ignore')
    mj = re.search(r'<section[^>]*id="jielu"[^>]*>(.*?)(?=<section)', s, re.S)
    j = mj.group(1)
    print('=' * 10, f)
    print('  verseList:', 'verseList' in j, '| verse卡:', j.count('class="verse"'),
          '| details:', j.count('<details'), '| v-trans:', j.count('v-trans'),
          '| summary:', re.findall(r'<summary[^>]*>([^<]*)</summary>', j)[:2])
    for m in re.finditer(r'<span class="v-no">(\d+)</span>', j):
        seg = j[m.end():m.end() + 1200]
        vl = re.search(r'<div class="v-line"[^>]*>(.*?)</div>', seg, re.S)
        if vl:
            print('  卡%s: %s' % (m.group(1), re.sub(r'<[^>]+>', '', vl.group(1)).strip()[:52]))
    print()
