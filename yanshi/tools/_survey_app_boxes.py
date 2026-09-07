# -*- coding: utf-8 -*-
"""盘点各课件 app 区块中「艺术特色」类 box 的形态，为统一成琵琶行「一、二、三」分 box 做准备。"""
import re, glob, os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CN = '一二三四五六七八九十'

def strip_tags(s):
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', '', s)

def survey(path):
    with open(path, encoding='utf-8') as f:
        t = f.read()
    t = re.sub(r' data-page-node-id="[^"]*"', '', t)
    m = re.search(r'<section id="app"[^>]*>(.*?)<section id="acc"', t, re.S)
    if not m:
        return None
    app = m.group(1)
    boxes = re.findall(r'<div class="box"[^>]*>\s*(?:<h[23][^>]*>(.*?)</h[23]>(.*?))?(?=<div class="box"[^>]*>|\s*</section>)', app, re.S)
    # simpler: split app by box opens
    parts = re.split(r'<div class="box"[^>]*>', app)[1:]
    out = []
    for p in parts:
        hm = re.match(r'\s*<h3[^>]*>(.*?)</h3>', p, re.S)
        title = strip_tags(hm.group(1)) if hm else '(no-h3)'
        # detect numbered-box already? h3 starts with 一、二、
        numbered = bool(re.match(r'^[一二三四五六七八九十]、', title))
        body = p[hm.end():] if hm else p
        # forms inside body
        circled = len(re.findall(r'[①②③④⑤⑥⑦⑧⑨⑩]', body))
        boldparas = len(re.findall(r'<p>\s*<b[^>]*>(?!class)', body))
        out.append((title, numbered, circled, boldparas, len(body)))
    return out

for path in sorted(glob.glob(os.path.join(os.path.dirname(__file__), '..', '*.html'))):
    name = os.path.basename(path)
    if 'pipaxing' in name:
        continue
    r = survey(path)
    if r is None:
        continue
    interesting = []
    for (title, numbered, circled, boldparas, blen) in r:
        if numbered:
            interesting.append(f'[已编号box] {title}')
        elif circled >= 2 and blen > 500:
            interesting.append(f'[①②合并 {circled}点] {title}')
        elif boldparas >= 2:
            interesting.append(f'[多<b>段落 {boldparas}段] {title}')
    if interesting:
        print(f'== {name}')
        for s in interesting:
            print('   ', s)
