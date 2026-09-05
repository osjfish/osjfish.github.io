# -*- coding: utf-8 -*-
"""B站视频检索（绕过 412 风控）。
步骤：1) finger/spi 取 buvid3/buvid4 作为 cookie；2) search/all/v2 带 cookie+Referer 检索；
3) web-interface/view 校验 state==0。
用法：python bili_search.py "桃花源记 朗诵" 5
"""
import sys, json, urllib.request, urllib.parse, time

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
REFERER = 'https://www.bilibili.com/'


def _get(url, cookie=None):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': REFERER})
    if cookie:
        req.add_header('Cookie', cookie)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode('utf-8'))


def get_cookie():
    spi = _get('https://api.bilibili.com/x/frontend/finger/spi')
    d = spi.get('data', {})
    b3 = d.get('b_3')
    b4 = d.get('b_4')
    return 'buvid3=%s; buvid4=%s' % (b3, b4)


def search(keyword, cookie, topn=5):
    q = urllib.parse.quote(keyword)
    url = 'https://api.bilibili.com/x/web-interface/search/all/v2?keyword=%s&order=click' % q
    data = _get(url, cookie)
    out = []
    for item in data.get('data', {}).get('result', []):
        if item.get('result_type') != 'video':
            continue
        for v in item.get('data', []):
            out.append({
                'bvid': v.get('bvid'),
                'title': v.get('title', '').replace('<em class="keyword">', '').replace('</em>', ''),
                'author': v.get('author', ''),
                'play': v.get('play', 0),
                'duration': v.get('duration', ''),
                'aid': v.get('aid'),
            })
            if len(out) >= topn:
                return out
    return out


def state_of(bvid, cookie):
    try:
        d = _get('https://api.bilibili.com/x/web-interface/view?bvid=%s' % bvid, cookie)
        return d.get('data', {}).get('state', -1), d.get('code', -1)
    except Exception as e:
        return -2, str(e)


def main():
    kw = sys.argv[1] if len(sys.argv) > 1 else '桃花源记'
    topn = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    cookie = get_cookie()
    time.sleep(0.3)
    res = search(kw, cookie, topn)
    print('=== %s ===' % kw)
    for v in res:
        st, code = state_of(v['bvid'], cookie)
        flag = 'OK' if st == 0 else ('STATE=%s' % st)
        print('[%s] %s | %s | 播放%s | %s分%s | %s' % (
            flag, v['bvid'], v['author'], v['play'],
            v['duration'][:2] if v['duration'] else '?', v['duration'][3:5] if v['duration'] else '',
            v['title']))


if __name__ == '__main__':
    main()
