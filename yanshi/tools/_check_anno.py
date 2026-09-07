# -*- coding: utf-8 -*-
import io, re
path = r'D:\App\Apps\yanshi\dengjiaxian-yangzhenning.html'
html = io.open(path, encoding='utf-8-sig').read()
cards = re.findall(r'<div class="verse" id="l(\d+)".*?<div class="v-line">(.*?)</div>', html, re.S)
for n, content in cards:
    cnt = content.count('anno-word')
    if cnt == 0:
        # strip tags for preview
        text = re.sub(r'<[^>]+>', '', content)[:60]
        print('Card %s (0 anno): %s' % (n, text))
print('---')
print('Total cards:', len(cards))
print('Cards with 0 anno:', sum(1 for _, c in cards if 'anno-word' not in c))
