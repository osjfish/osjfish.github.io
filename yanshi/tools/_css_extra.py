# -*- coding: utf-8 -*-
"""列出各文件 style 块中「基准(pipaxing)没有」的选择器及其取值。"""
import os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.S)

def norm(s): return re.sub(r'\s+', ' ', s).strip()

def parse_rules(css):
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find('{', i)
        if j < 0: break
        sel = norm(css[i:j])
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        out.append((sel, norm(css[j+1:k-1])))
        i = k
    return out

base = re.search(STYLE_RE, open(os.path.join(ROOT, 'pipaxing-baijuyi.html'), encoding='utf-8').read()).group(1)
# 基准 CSS 里若缺 style 标签的2个文件，其 CSS 也在 head 中，用宽松方式取
base_sels = set()
for sel, d in parse_rules(base):
    base_sels.add(sel)

extra = collections.defaultdict(collections.Counter)
for f in files:
    s = open(os.path.join(ROOT, f), encoding='utf-8').read()
    m = STYLE_RE.search(s)
    if not m:
        # 兜底：head 内裸 CSS
        h = re.search(r'<head[^>]*>(.*?)</head>', s, re.S)
        css = h.group(1) if h else ''
    else:
        css = m.group(1)
    for sel, d in parse_rules(css):
        if sel not in base_sels:
            extra[sel][d] += 1

print('基准选择器数', len(base_sels))
print('\n=== 基准之外出现的选择器 ===')
for sel in sorted(extra, key=lambda x: -sum(extra[x].values())):
    c = extra[sel]
    tot = sum(c.values())
    if tot < 2: continue
    print('\n--- %s  (%d 文件)' % (sel, tot))
    for d, n in c.most_common(4):
        print('     [%3d] %s' % (n, d[:300]))
