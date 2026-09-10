# -*- coding: utf-8 -*-
"""提取全库 <style> 块，做规则并集与冲突分析。"""
import os, re, json, hashlib, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))

STYLE_RE = re.compile(r'<style[^>]*>(.*?)</style>', re.S)

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def parse_rules(css):
    """返回 [(selector, decl_text)]，按出现顺序"""
    out = []
    i = 0
    n = len(css)
    while i < n:
        # 找下一个 {
        j = css.find('{', i)
        if j < 0:
            break
        sel = norm(css[i:j])
        # decl 到匹配的 }
        depth = 1
        k = j + 1
        while k < n and depth:
            if css[k] == '{':
                depth += 1
            elif css[k] == '}':
                depth -= 1
            k += 1
        decl = norm(css[j+1:k-1])
        if sel and not sel.startswith('@'):
            out.append((sel, decl))
        else:
            # @media 等，递归内部
            if sel.startswith('@media'):
                inner = parse_rules(css[j+1:k-1])
                for s2, d2 in inner:
                    out.append((sel + ' >> ' + s2, d2))
        i = k
    return out

groups = collections.defaultdict(list)
nostyle = []
allrules = collections.defaultdict(lambda: collections.defaultdict(list))  # sel -> decl -> [files]

for f in files:
    p = os.path.join(ROOT, f)
    src = open(p, encoding='utf-8').read()
    m = STYLE_RE.search(src)
    if not m:
        nostyle.append(f)
        continue
    css = m.group(1)
    h = hashlib.md5(norm(css).encode()).hexdigest()[:8]
    groups[h].append(f)
    for sel, decl in parse_rules(css):
        allrules[sel][decl].append(f)

print('文件总数', len(files))
print('无 style 块:', nostyle)
print('CSS 变体数', len(groups))
for h, fs in sorted(groups.items(), key=lambda x: -len(x[1])):
    print('  %s  %3d  e.g. %s' % (h, len(fs), fs[0]))

print('\n=== 选择器冲突（同一 selector 有多种声明）===')
nconf = 0
for sel in sorted(allrules):
    ds = allrules[sel]
    if len(ds) > 1:
        nconf += 1
        print('\n--- %s  (%d 种)' % (sel, len(ds)))
        for decl, fs in sorted(ds.items(), key=lambda x: -len(x[1])):
            print('   [%3d] %s' % (len(fs), decl[:220]))
print('\n冲突选择器数', nconf, '总选择器数', len(allrules))

out = {'groups': {h: fs for h, fs in groups.items()},
       'nostyle': nostyle,
       'rules': {sel: {d: fs for d, fs in ds.items()} for sel, ds in allrules.items()}}
json.dump(out, open(os.path.join(ROOT, 'tools', '_css_union.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('\nwrote tools/_css_union.json')
