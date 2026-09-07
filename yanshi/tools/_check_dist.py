# -*- coding: utf-8 -*-
import io, re
path = r'D:\App\Apps\yanshi\dengjiaxian-yangzhenning.html'
html = io.open(path, encoding='utf-8-sig').read()
cards = re.findall(r'<div class="verse" id="l(\d+)".*?<div class="v-line">(.*?)</div>', html, re.S)
dist = {}
for n, content in cards:
    cnt = content.count('anno-word')
    dist.setdefault(cnt, []).append(n)
for k in sorted(dist.keys()):
    print('%d anno: %d cards -> %s' % (k, len(dist[k]), ','.join(dist[k])))
