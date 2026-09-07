# -*- coding: utf-8 -*-
import urllib.request, json, sys

def get_buvid():
    req = urllib.request.Request("https://api.bilibili.com/x/frontend/finger/spi",
        headers={"User-Agent":"Mozilla/5.0"})
    d = json.loads(urllib.request.urlopen(req, timeout=15).read())
    return d["data"]["b_3"], d["data"]["b_4"]

def check(bv, b3, b4):
    req = urllib.request.Request("https://api.bilibili.com/x/web-interface/view?bvid="+bv,
        headers={"User-Agent":"Mozilla/5.0","Referer":"https://www.bilibili.com/",
                 "Cookie":"buvid3=%s; buvid4=%s"%(b3,b4)})
    d = json.loads(urllib.request.urlopen(req, timeout=15).read())
    code = d.get("code")
    title = d.get("data",{}).get("title","") if d.get("data") else d.get("message","")
    print("%s code=%s %s" % (bv, code, title[:50]))

b3,b4 = get_buvid()
for bv in sys.argv[1:]:
    check(bv, b3, b4)
