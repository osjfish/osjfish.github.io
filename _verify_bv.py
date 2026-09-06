import urllib.request, json, os
os.chdir(r'D:\App\Apps')

# Get buvid cookie
req = urllib.request.Request("https://api.bilibili.com/x/frontend/finger/spi", headers={"User-Agent":"Mozilla/5.0"})
resp = urllib.request.urlopen(req).read().decode()
data = json.loads(resp)
b3 = data['data']['b_3']
b4 = data['data']['b_4']
cookie = f"buvid3={b3}; buvid4={b4}"

bvs = [
    ("秋天的怀念-朗读", "BV1Xk4y1w7yG"),
    ("秋天的怀念-讲解", "BV114eneyEN5"),
    ("散步-朗读", "BV1GY4y1X7wq"),
    ("散步-讲解", "BV1mR4ZevEcs"),
    ("敬业与乐业-朗读", "BV16p4y1S7CL"),
    ("敬业与乐业-讲解", "BV1f64y1e7WQ"),
]

for name, bv in bvs:
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv}"
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0", "Referer":"https://www.bilibili.com/", "Cookie":cookie})
    try:
        resp = urllib.request.urlopen(req, timeout=10).read().decode()
        d = json.loads(resp)
        if d.get('code') == 0:
            print(f"[OK] {name} {bv}: state={d['data']['state']} title={d['data']['title'][:40]}")
        else:
            print(f"[FAIL] {name} {bv}: code={d.get('code')} msg={d.get('message')}")
    except Exception as e:
        print(f"[ERR] {name} {bv}: {e}")
