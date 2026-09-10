# -*- coding: utf-8 -*-
"""统计全库 font-size 规则：主段 vs --fs 缩放段，各选择器取值分布。"""
import os, re, collections, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.S)
MARK = '正文字体缩放'

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

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
        out.append((sel, norm(css[j+1:k-1]), i, k))
        i = k
    return out

main_fs = collections.defaultdict(collections.Counter)   # sel -> Counter(decl)
scale_fs = collections.defaultdict(collections.Counter)
no_mark = []
per_file_scale = {}

for f in files:
    src = open(os.path.join(ROOT, f), encoding='utf-8').read()
    m = STYLE_RE.search(src)
    if not m:
        no_mark.append(f); continue
    css = m.group(1)
    p = css.find(MARK)
    if p < 0:
        no_mark.append(f)
        head, tail = css, ''
    else:
        # 从 MARK 所在那行的注释起点开始
        ls = css.rfind('\n', 0, p)
        head, tail = css[:ls], css[ls:]
    for sel, decl, _, _ in parse_rules(head):
        if 'font-size' in decl:
            main_fs[sel][decl] += 1
    sc = {}
    for sel, decl, _, _ in parse_rules(tail):
        if 'font-size' in decl and 'var(--fs)' in decl:
            scale_fs[sel][decl] += 1
            sc[sel] = decl
    per_file_scale[f] = sc

print('无缩放段文件:', no_mark)
print('\n=== 缩放段（--fs）选择器取值分布 ===')
for sel in sorted(scale_fs, key=lambda s: -sum(scale_fs[s].values())):
    c = scale_fs[sel]
    tot = sum(c.values())
    flag = '  <<< 分歧' if len(c) > 1 else ''
    print('%-34s 共%3d  %s' % (sel, tot, flag))
    for d, n in c.most_common():
        print('        [%3d] %s' % (n, d))

print('\n=== 主段 font-size 分歧 ===')
for sel in sorted(main_fs, key=lambda s: -sum(main_fs[s].values())):
    c = main_fs[sel]
    if len(c) > 1:
        print('--- %s' % sel)
        for d, n in c.most_common():
            print('   [%3d] %s' % (n, d))

json.dump({f: v for f, v in per_file_scale.items()},
          open(os.path.join(ROOT, 'tools', '_fs_scale_map.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
