import urllib.request, json
bvs = ['BV1w64y1z7Yn','BV1Td4y1k7Nm','BV12V4y197qh','BV1an2UY2EoE','BV18J411u7sy','BV11v411P7Bz','BV13K41137ML','BV1LGRFYTErS','BV1Te411c7ft']
req = urllib.request.Request('https://api.bilibili.com/x/frontend/finger/spi', headers={'User-Agent':'Mozilla/5.0'})
d = json.loads(urllib.request.urlopen(req).read())
b3, b4 = d['data']['b_3'], d['data']['b_4']
for bv in bvs:
    req = urllib.request.Request('https://api.bilibili.com/x/web-interface/view?bvid=' + bv, headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.bilibili.com/','Cookie':'buvid3=' + b3 + '; buvid4=' + b4})
    r = json.loads(urllib.request.urlopen(req).read())
    if r['code'] == 0:
        print(bv + ' OK state=' + str(r['data']['state']) + ' | ' + r['data']['title'][:50])
    else:
        print(bv + ' FAIL ' + r['message'])
