# -*- coding: utf-8 -*-
import urllib.request, json, urllib.parse, re

B3 = '96B2A4FF-42BF-2C4F-E7B0-9A0817073A8578687infoc'
B4 = '5B4FD9B5-9CCE-0D38-3F37-516C6BE42BE178687-026090523-HtEhsbb3r+fWgsPEe+58GtCn06ggnBFpNkE00qz6iocdLcVVS0B2ixZUSGjsoBAN'

def search(kw):
    url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=' + urllib.parse.quote(kw) + '&page=1&order=click'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.bilibili.com/',
        'Cookie': 'buvid3=' + B3 + '; buvid4=' + B4
    })
    d = json.loads(urllib.request.urlopen(req).read())
    return d.get('data', {}).get('result', [])

def clean(t):
    return re.sub(r'<[^>]+>', '', t)

for kw in ['曹刿论战 朗诵', '曹刿论战 讲解', '曹刿论战 动画', '曹刿论战 课本剧',
           '孔乙己 朗诵', '孔乙己 讲解', '孔乙己 话剧', '孔乙己 影视', '孔乙己 动画', '孔乙己 课本剧']:
    print('===', kw, '===')
    for r in search(kw)[:8]:
        print(r.get('bvid'), '|', clean(r.get('title', '')), '|', r.get('play'), 'plays |', r.get('duration'))
    print()
