# -*- coding: utf-8 -*-
"""格式对比矩阵：最近11篇 vs 4篇标杆"""
import re

NEW = ['achangyushanhaijing-luxun.html', 'haiyan-gaoerji.html', 'tianxiadiyilou-hejiping.html',
       'tandushu-peigen.html', 'buqiushenjie-manancun.html', 'shanshuihuadeyijing-likeran.html',
       'wuyanzhimei-zhuguangqian.html', 'quqianwomendexiangxiang-yetaotao.html',
       'zaoer-sunhong.html', 'manjianghong-qiujin.html', 'puliurenjia-liushaotang.html']
REF = ['pipaxing-baijuyi.html', 'changhenge-baijuyi.html', 'hongmenyan-shiji.html', 'beiying-zhuziqing.html']

def feats(s):
    f = {}
    secs = re.findall(r'<section[^>]*id="([a-z]+)"', s)
    f['六区'] = all(x in secs for x in ['bg', 'jielu', 'app', 'acc', 'practice'])
    f['hero-side'] = bool(re.search(r'class="hero-side', s))
    f['part-head+p-num'] = bool(re.search(r'class="part-head"', s)) and bool(re.search(r'class="p-num"', s))
    f['part-overview'] = 'part-overview' in s
    f['sec-sub'] = 'sec-sub' in s
    f['v-more折叠'] = 'v-more' in s
    f['acc-cat'] = 'acc-cat' in s or 'acc-item' in s or 'acc-w' in s
    f['anno-popup'] = 'annoPopup' in s
    f['按钮4'] = len(re.findall(r'data-mode="(word|note)"', s)) == 4
    f['视频2'] = len(re.findall(r'<iframe', s)) == 2
    f['dict题库'] = 'DICT_WORDS' in s
    f['size_KB'] = len(s) // 1024
    f['anno数'] = len(re.findall(r'class="anno-word"', s))
    f['verse卡'] = len(re.findall(r'class="verse"', s))
    return f

KEYS = ['六区', 'hero-side', 'part-head+p-num', 'part-overview', 'sec-sub', 'v-more折叠',
        'acc-cat', 'anno-popup', '按钮4', '视频2', 'dict题库', 'size_KB', 'anno数', 'verse卡']

print('%-46s' % '文件', ' '.join('%-6s' % k for k in KEYS))
for f in REF + NEW:
    s = open(f, 'rb').read().decode('utf-8', errors='ignore')
    d = feats(s)
    row = '%-46s' % f[:44]
    for k in KEYS:
        v = d[k]
        if k in ('size_KB', 'anno数', 'verse卡'):
            row += ' %-6d' % v
        else:
            row += ' %-6s' % ('Y' if v else 'N')
    print(row)
print()
print('说明: REF=标杆(前4行) NEW=最近批次(后11行)')
