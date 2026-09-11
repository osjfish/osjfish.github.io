# -*- coding: utf-8 -*-
"""校验：div 平衡 + app-group 与编号 box 的配对关系"""
import os, re, io, sys, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\App\Apps\yanshi'
CN = '一二三四五六七八九十'
NUM_RE = re.compile(r'^\s*(?:<[^>]+>)?\s*([' + CN + r'])、')

files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
bad = []
ngrp = 0
nbad_pair = []
for f in files:
    src = open(os.path.join(ROOT, f), encoding='utf-8').read()
    # div 平衡（只数 div 开合，忽略属性里的字符串）
    body = re.sub(r'<script[^>]*>.*?</script>', '', src, flags=re.S)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.S)
    o = len(re.findall(r'<div\b', body))
    c = len(re.findall(r'</div>', body))
    if c > o:
        bad.append((f, o, c))
    a = re.search(r'<style[^>]*>(.*?)</style>', src, re.S).end()
    i = src.find('id="app"', a)
    j = src.find('id="acc"', i)
    if i < 0:
        continue
    t = src[i:j if j > 0 else len(src)]
    grps = list(re.finditer(r'<div class="app-group"[^>]*>(.*?)</div>', t, re.S))
    ngrp += len(grps)
    # 每个 app-group 后面必须紧跟至少一个编号 box
    for g in grps:
        tail = t[g.end():]
        m = re.search(r'<div class="box"[^>]*>\s*<h3[^>]*>(.*?)</h3>', tail, re.S)
        if not m:
            nbad_pair.append((f, '组标题后无 box'))
            continue
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if not NUM_RE.match(title):
            nbad_pair.append((f, '组标题后首块非编号: ' + title))
    # 编号 box 必须有归属组（主题思想类除外）
    pos = 0
    for m in re.finditer(r'<div class="box"[^>]*>\s*<h3[^>]*>(.*?)</h3>', t, re.S):
        title = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if not NUM_RE.match(title):
            continue
        before = t[:m.start()]
        lastg = before.rfind('<div class="app-group"')
        # 组标题与编号块之间不能隔着一个「主题思想」块
        if lastg < 0:
            nbad_pair.append((f, '编号块无归属: ' + title))

print('div 闭合多于开启的文件:', len(bad), bad[:8])
print('app-group 总数:', ngrp)
print('配对异常:', len(nbad_pair))
for x in nbad_pair[:25]:
    print('   ', x)
