# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, json, re

B3='926EF02B-FFD7-5504-0AD0-6C02719F848728781infoc'
B4='06EE6446-8192-F525-71D9-0B9634E507A928781-026090602-HtEhsbb3r+fWgsPEe+58GtCn06ggnBFpNkE00qz6iocdLcVVS0B2ixZUSGjsoBAN'

def clean(t):
    return re.sub(r'<[^>]+>', '', t)

def search(kw):
    url='https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword='+urllib.parse.quote(kw)+'&page=1&order=click'
    req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.bilibili.com/','Cookie':'buvid3='+B3+'; buvid4='+B4})
    data=json.loads(urllib.request.urlopen(req,timeout=15).read())
    results=[]
    if data.get('data') and data['data'].get('result'):
        for v in data['data']['result'][:8]:
            results.append((v.get('bvid',''), clean(v.get('title','')), v.get('author',''), v.get('play',0)))
    return results

for kw in ['木兰诗 朗诵','木兰诗 歌曲','望岳 杜甫 朗诵','望岳 赏析','登飞来峰 王安石 朗诵','登飞来峰 赏析']:
    print('=== '+kw+' ===')
    for bvid,title,author,play in search(kw):
        print('  %s | %s | %s | play=%s' % (bvid, title[:55], author, play))
    print()
