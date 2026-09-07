# -*- coding: utf-8 -*-
import re, io
h = io.open(r"D:\App\Apps\yanshi\daishangtadeyanjing-liucixin.html", encoding="utf-8-sig").read()
# Extract card text
cards = re.findall(r'<div class="v-line">(.*?)</div>', h, re.S)
cs = re.sub(r'<[^>]+>', '', ''.join(cards))
cs = re.sub(r'\s+', '', cs)

# Extract fulltext - find all pl divs between fulltext marker and verseList
ft_start = h.find('<div id="fulltext"')
ft_end = h.find('<div class="verse-list"')
ft_section = h[ft_start:ft_end]
pl_divs = re.findall(r'<div class="pl">(.*?)</div>', ft_section, re.S)
fs = re.sub(r'<[^>]+>', '', ''.join(pl_divs))
fs = re.sub(r'\s+', '', fs)

print('card:', len(cs), 'full:', len(fs), 'match:', cs == fs)
if cs != fs:
    for i in range(min(len(cs), len(fs))):
        if cs[i] != fs[i]:
            print('DIFF at', i)
            print('  card:', repr(cs[max(0,i-15):i+15]))
            print('  full:', repr(fs[max(0,i-15):i+15]))
            break
    if len(cs) != len(fs):
        print('length diff:', len(cs) - len(fs))
        if len(cs) > len(fs):
            print('extra in card:', repr(cs[len(fs):len(fs)+50]))
        else:
            print('extra in full:', repr(fs[len(cs):len(cs)+50]))
