# -*- coding: utf-8 -*-
import os, re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\App\Apps\yanshi'


def app(src):
    a = re.search(r'<style[^>]*>(.*?)</style>', src, re.S)
    s = re.sub(r'<script[^>]*>.*?</script>', '', src[a.end():], flags=re.S)
    i = s.find('id="app"')
    j = s.find('id="acc"', i)
    return s[i:j if j > 0 else len(s)]


for f in sys.argv[1:]:
    src = open(os.path.join(ROOT, f), encoding='utf-8').read()
    t = app(src)
    print('=' * 66)
    print(f)
    # 按顺序输出 app-group 与 box h3
    for m in re.finditer(r'<div class="app-group"[^>]*>(.*?)</div>|<h3[^>]*>(.*?)</h3>', t, re.S):
        if m.group(1) is not None:
            print('  ▍【组】%s' % re.sub(r'<[^>]+>', '', m.group(1)).strip())
        else:
            print('       - %s' % re.sub(r'<[^>]+>', '', m.group(2)).strip())
