# -*- coding: utf-8 -*-
"""琵琶行：赏析区顺序改为全库主流「形象 → 艺术特色 → 名句 → 主题」"""
import os, re, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
P = r'D:\App\Apps\yanshi\pipaxing-baijuyi.html'
CN = '一二三四五六七八九十'
NUM_RE = re.compile(r'^\s*(?:<[^>]+>)?\s*([' + CN + r'])、')


def balanced_div(s, start):
    """start 指向 '<div'，返回 (整块 html, 结束位置)"""
    assert s.startswith('<div', start)
    depth, i, n = 0, start, len(s)
    while i < n:
        j = s.find('<div', i)
        k = s.find('</div>', i)
        if k < 0:
            break
        if j >= 0 and j < k:
            depth += 1
            i = j + 4
        else:
            depth -= 1
            i = k + 6
            if depth == 0:
                return s[start:i], i
    raise ValueError('unbalanced')


src = open(P, encoding='utf-8').read()
a = re.search(r'<style[^>]*>(.*?)</style>', src, re.S).end()
i = src.find('id="app"', a)
j = src.find('id="acc"', i)
reg = src[i:j]

# 收集顶层块：app-group 行 + box
items = []   # (start, end, kind, title)
pos = 0
while True:
    m1 = re.compile(r'<div class="app-group"[^>]*>').search(reg, pos)
    m2 = re.compile(r'<div class="box"').search(reg, pos)
    cands = [(m.start(), 'g' if False else 'g') for m in [m1] if m] + \
            [(m.start(), 'b') for m in [m2] if m]
    if not cands:
        break
    st, kind = min(cands)
    if kind == 'g':
        e = reg.find('</div>', st) + 6
        items.append((st, e, 'g', re.sub(r'<[^>]+>', '', reg[st:e]).strip()))
    else:
        blk, e = balanced_div(reg, st)
        h = re.search(r'<h3[^>]*>(.*?)</h3>', blk, re.S)
        items.append((st, e, 'b', re.sub(r'<[^>]+>', '', h.group(1)).strip() if h else ''))
    pos = e

print('当前顺序:')
for st, e, k, t in items:
    print('   %s %s' % (k, t))

# 目标：把「名句赏析」box 移到最后一个编号 box 之后
ming_idx = [n for n, it in enumerate(items) if it[2] == 'b' and '名句' in it[3]]
num_idx = [n for n, it in enumerate(items) if it[2] == 'b' and NUM_RE.match(it[3])]
if not ming_idx or not num_idx:
    print('未找到名句块或编号块，跳过')
    sys.exit(0)
mi = ming_idx[0]
last_num = num_idx[-1]
if mi > last_num:
    print('名句块已在编号块之后，无需调整')
    sys.exit(0)

blocks = [reg[s:e] for s, e, k, t in items]


def title_of(b):
    if b.startswith('<div class="app-group"'):
        return None
    h = re.search(r'<h3[^>]*>(.*?)</h3>', b, re.S)
    return re.sub(r'<[^>]+>', '', h.group(1)).strip() if h else ''


xing = [b for n, b in enumerate(blocks) if title_of(b) and '形象' in title_of(b)]
grp = [b for n, b in enumerate(blocks) if b.startswith('<div class="app-group"')]
nums = [b for n, b in enumerate(blocks) if title_of(b) and NUM_RE.match(title_of(b))]
ming = [b for n, b in enumerate(blocks) if title_of(b) and '名句' in title_of(b)]
rest = [b for n, b in enumerate(blocks)
        if b not in xing and b not in grp and b not in nums and b not in ming]
if not (xing and grp and nums and ming):
    print('分类不全，跳过:', len(xing), len(grp), len(nums), len(ming))
    sys.exit(0)
# 主流顺序：形象 → 艺术特色(编号组) → 名句 → 其余
blocks = xing + grp + nums + ming + rest
head = reg[:items[0][0]]
tail = reg[items[-1][1]:]
newreg = head + '\n'.join(blocks) + tail
out = src[:i] + newreg + src[j:]
if '--apply' in sys.argv:
    open(P, 'w', encoding='utf-8').write(out)
print()
print('调整后顺序:')
for b in blocks:
    if b.startswith('<div class="app-group"'):
        print('   g %s' % re.sub(r'<[^>]+>', '', b).strip())
    else:
        h = re.search(r'<h3[^>]*>(.*?)</h3>', b, re.S)
        print('   b %s' % re.sub(r'<[^>]+>', '', h.group(1)).strip() if h else '?')
print('applied' if '--apply' in sys.argv else 'dry-run')
