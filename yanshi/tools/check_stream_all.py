# -*- coding: utf-8 -*-
import re, io
files = [
 r"D:\App\Apps\yanshi\daishangtadeyanjing-liucixin.html",
 r"D:\App\Apps\yanshi\zuihouyike-dude.html",
 r"D:\App\Apps\yanshi\huanghesong-guangweiran.html",
 r"D:\App\Apps\yanshi\meilingsanzhang-chenyi.html",
]
for fp in files:
    h = io.open(fp, encoding="utf-8-sig").read()
    cards = re.findall(r'<div class="v-line">(.*?)</div>', h, re.S)
    cs = re.sub(r'<[^>]+>', '', ''.join(cards))
    cs = re.sub(r'\s+', '', cs)
    ft_start = h.find('<div id="fulltext"')
    ft_end = h.find('<div class="verse-list"')
    ft_section = h[ft_start:ft_end]
    pl_divs = re.findall(r'<div class="pl">(.*?)</div>', ft_section, re.S)
    fs = re.sub(r'<[^>]+>', '', ''.join(pl_divs))
    fs = re.sub(r'\s+', '', fs)
    name = fp.split('\\')[-1]
    print('%s | card=%d full=%d match=%s' % (name, len(cs), len(fs), cs == fs))
    if cs != fs:
        for i in range(min(len(cs), len(fs))):
            if cs[i] != fs[i]:
                print('  DIFF at', i)
                print('    card:', repr(cs[max(0,i-15):i+15]))
                print('    full:', repr(fs[max(0,i-15):i+15]))
                break
        if len(cs) != len(fs):
            print('  length diff:', len(cs) - len(fs))
