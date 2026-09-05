# -*- coding: utf-8 -*-
import urllib.request, json

B3='926EF02B-FFD7-5504-0AD0-6C02719F848728781infoc'
B4='06EE6446-8192-F525-71D9-0B9634E507A928781-026090602-HtEhsbb3r+fWgsPEe+58GtCn06ggnBFpNkE00qz6iocdLcVVS0B2ixZUSGjsoBAN'

candidates = {
    '木兰诗-朗诵': 'BV1ba4y1G7cu',
    '木兰诗-歌曲': 'BV1zW41147no',
    '望岳-朗诵': 'BV1bf4y1F7M3',
    '望岳-赏析': 'BV1PT42127RL',
    '登飞来峰-朗诵': 'BV1H2kAYtEvo',
    '登飞来峰-赏析': 'BV1nHRuBaE26',
}

for name, bvid in candidates.items():
    url='https://api.bilibili.com/x/web-interface/view?bvid='+bvid
    req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.bilibili.com/','Cookie':'buvid3='+B3+'; buvid4='+B4})
    try:
        data=json.loads(urllib.request.urlopen(req,timeout=15).read())
        if data.get('code')==0:
            d=data['data']
            print('OK  %s | %s | state=%d | %s' % (name, bvid, d.get('state',-1), d.get('title','')[:50]))
        else:
            print('FAIL %s | %s | code=%s %s' % (name, bvid, data.get('code'), data.get('message','')))
    except Exception as e:
        print('ERR  %s | %s | %s' % (name, bvid, e))
