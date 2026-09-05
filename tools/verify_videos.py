# -*- coding: utf-8 -*-
import urllib.request, json

B3 = '96B2A4FF-42BF-2C4F-E7B0-9A0817073A8578687infoc'
B4 = '5B4FD9B5-9CCE-0D38-3F37-516C6BE42BE178687-026090523-HtEhsbb3r+fWgsPEe+58GtCn06ggnBFpNkE00qz6iocdLcVVS0B2ixZUSGjsoBAN'

def verify(bvid):
    url = 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.bilibili.com/',
        'Cookie': 'buvid3=' + B3 + '; buvid4=' + B4
    })
    d = json.loads(urllib.request.urlopen(req).read())
    if d.get('code') == 0:
        info = d['data']
        print(f"  OK {bvid} | state={info.get('state')} | {info.get('title')} | {info.get('stat',{}).get('view')} views")
    else:
        print(f"  FAIL {bvid} | {d.get('message')}")

candidates = [
    # 曹刿论战
    'BV1NC4y1b7yr',  # 诵读江源
    'BV1dY411f7UW',  # 课文朗读
    'BV1bW4y1s7z2',  # 你见过这样的曹刿论战吗
    'BV1NU7fziEGm',  # 课本剧
    'BV1MS4y1D7qT',  # 史记动画片
    # 孔乙己
    'BV1k94y1S73S',  # 全文朗诵
    'BV1JE4m1R7ZV',  # 朗读并讲解
    'BV1kx4y1P758',  # 话剧完整版
    'BV1Sc411b7i4',  # 话剧修复版
    'BV1CM411p7Gu',  # 70秒讲完孔乙己 (动画)
]
for bv in candidates:
    verify(bv)
