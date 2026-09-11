# -*- coding: utf-8 -*-
"""对照 0faf483^ 旧版，恢复被拆编号时删掉的赏析区组标题"""
import os, re, io, sys, json, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\App\Apps\yanshi'
OLD = r'D:\App\Apps\yanshi\tools\_oldapp\yanshi'
CN = '一二三四五六七八九十'
NUM_RE = re.compile(r'^\s*(?:<[^>]+>)?\s*([' + CN + r'])、')


def appboxes(src):
    a = re.search(r'<style[^>]*>(.*?)</style>', src, re.S)
    s = src[a.end():] if a else src
    s = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)
    i = s.find('id="app"')
    if i < 0:
        return []
    j = s.find('id="acc"', i)
    t = s[i:j if j > 0 else len(s)]
    out = []
    for m in re.finditer(r'<div class="box"[^>]*>(.*?)(?=<div class="box"|\Z)', t, re.S):
        h = re.search(r'<h3[^>]*>(.*?)</h3>', m.group(1), re.S)
        if h:
            out.append(re.sub(r'<[^>]+>', '', h.group(1)).strip())
    return out


files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
ok, miss, noneed = [], [], []
for f in files:
    cur = appboxes(open(os.path.join(ROOT, f), encoding='utf-8').read())
    if not any(NUM_RE.match(t) for t in cur):
        continue
    op = os.path.join(OLD, f)
    if not os.path.exists(op):
        miss.append(f)
        continue
    ob = appboxes(open(op, encoding='utf-8', errors='replace').read())
    lost = [t for t in ob if t not in cur and not NUM_RE.match(t)]
    if lost:
        ok.append((f, lost, ob, cur))
    else:
        noneed.append(f)

L = []
L.append('有编号块的篇数: %d' % (len(ok) + len(noneed) + len(miss)))
L.append('可从旧版恢复组标题: %d   旧版不可用: %d   旧版本来就没组标题: %d'
         % (len(ok), len(miss), len(noneed)))
L.append('')
L.append('=== 组标题取值分布 ===')
c = collections.Counter()
for f, lost, ob, cur in ok:
    for t in lost:
        c[t] += 1
for k, v in c.most_common(30):
    L.append('  %-22s %d' % (k, v))
L.append('')
L.append('=== 对照样例（前 15）===')
for f, lost, ob, cur in ok[:15]:
    L.append('%-46s 被删组标题=%s' % (f, lost))
    L.append('      旧: %s' % ob)
    L.append('      新: %s' % cur)
L.append('')
L.append('旧版不可用的篇: %s' % miss[:10])
open(os.path.join(ROOT, 'tools', '_recover_out.txt'), 'w', encoding='utf-8').write('\n'.join(L))
json.dump({f: lost for f, lost, ob, cur in ok},
          open(os.path.join(ROOT, 'tools', '_group_titles.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('done')
