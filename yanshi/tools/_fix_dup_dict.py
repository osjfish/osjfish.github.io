# -*- coding: utf-8 -*-
"""删除 DICT_WORDS 中重复 (w,q) 条目（保留首个，原位删多余块，不改其余块格式）。
用法：python _fix_dup_dict.py            # dry-run 打印待删
      python _fix_dup_dict.py --apply     # 落地
"""
import os, re, sys

ROOT = r'D:\App\Apps\yanshi'
APPLY = '--apply' in sys.argv

def blocks_in(src, name):
    m = re.search(r'var\s+' + name + r'\s*=\s*(\[.*?\])\s*;', src, re.S)
    if not m:
        return None, []
    arr_start, arr_end = m.start(1), m.end(1)
    # 在 src 坐标内找块
    blocks = []
    for bm in re.finditer(r'\{[^{}]*\}', src):
        if arr_start <= bm.start() < arr_end:
            blocks.append((bm.start(), bm.end(), bm.group(0)))
    return (arr_start, arr_end), blocks

def keyof(b):
    wm = re.search(r'"w"\s*:\s*"([^"]*)"', b)
    qm = re.search(r'"q"\s*:\s*"([^"]*)"', b)
    return (wm.group(1) if wm else '', qm.group(1) if qm else '')

def fix_file(f):
    p = os.path.join(ROOT, f)
    src = open(p, encoding='utf-8').read()
    span, blocks = blocks_in(src, 'DICT_WORDS')
    if span is None:
        print('  SKIP(无 DICT_WORDS)', f); return 0
    seen = set(); remove = []  # (s,e)
    for s, e, b in blocks:
        k = keyof(b)
        if k in seen:
            remove.append((s, e))
        else:
            seen.add(k)
    if not remove:
        print('  无重复', f); return 0
    print('  待删 %d 块: %s' % (len(remove), [keyof(src[s:e]) for s, e in remove]))
    if not APPLY:
        return len(remove)
    new = src
    for s, e in sorted(remove, reverse=True):
        # 删块及其相邻逗号：优先删块后的逗号，否则删块前的逗号
        after = new[e:e+1]
        if after == ',':
            new = new[:s] + new[e+1:]
        elif new[s-1:s] == ',':
            new = new[:s-1] + new[e:]
        else:
            new = new[:s] + new[e:]
    # 校验：重新解析块数应减少
    _, blocks2 = blocks_in(new, 'DICT_WORDS')
    open(p, 'w', encoding='utf-8').write(new)
    removed = len(blocks) - len(blocks2)
    print('    落地：删除 %d 块（原 %d → 现 %d）' % (removed, len(blocks), len(blocks2)))
    return removed

if __name__ == '__main__':
    targets = ['chuangzaoxuanyan-taoxingzhi.html',
               'congbaicaoyuandaosanweishuwu-luxun.html']
    total = 0
    for f in targets:
        print('==', f)
        total += fix_file(f)
    print('合计待删/已删:', total)
