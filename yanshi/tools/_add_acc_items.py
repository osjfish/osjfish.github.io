# -*- coding: utf-8 -*-
"""
把缺失的「注释默写词」补进积累区，使默写题有据可依。
用法：python _add_acc_items.py spec.json [--apply]
spec: { "文件名.html": [["词","释义"], ...] }
插入到 acc 区中 h3 含「词语」的 acc-cat（无则第一个）末尾，保持原类名。
"""
import os, re, sys, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT_RE = re.compile(r'<div class="acc-cat">')
GLO_RE = re.compile(r'<div class="glossary">')
H3_RE = re.compile(r'<h3>(.*?)</h3>', re.S)
W_RE = re.compile(r'<span class="acc-w(?:ord)?">(.*?)</span>', re.S)
DT_RE = re.compile(r'<dt>(.*?)</dt>', re.S)
KAI_RE = re.compile(r'<td class="kai">(.*?)</td>', re.S)
TAG = re.compile(r'<[^>]+>')


def close_of(seg, start):
    """从 start 处的 <div ...> 开标签起做 div 深度扫描，返回其闭合 </div> 的起始下标"""
    p = seg.index('>', start) + 1
    depth = 1
    while depth > 0:
        nd = seg.find('<div', p)
        cd = seg.find('</div>', p)
        if cd < 0:
            return len(seg)
        if nd >= 0 and nd < cd:
            depth += 1
            p = nd + 4
        else:
            depth -= 1
            p = cd + 6
    return p - 6


def add(src, items):
    i = src.find('id="acc"')
    if i < 0:
        return src, 0, '无 acc 区'
    j = src.find('id="practice"', i)
    if j < 0:
        j = len(src)
    seg = src[i:j]
    cats = list(CAT_RE.finditer(seg))
    if cats:
        pick = None
        for m in cats:
            h = H3_RE.search(seg, m.start(), m.start() + 400)
            if h and '词语' in h.group(1):
                pick = m
                break
        if pick is None:
            pick = cats[0]
        end = close_of(seg, pick.start())
        cls_w = 'acc-word' if 'acc-word' in seg else 'acc-w'
        cls_d = 'acc-exp' if 'acc-exp' in seg else 'acc-d'
        have = set(TAG.sub('', x).strip() for x in W_RE.findall(seg))
        fmt = ('\n      <div class="acc-item"><span class="%s">%%s</span>'
               '<span class="%s">%%s</span></div>' % (cls_w, cls_d))
    else:
        glo = GLO_RE.search(seg)
        if not glo:
            return src, 0, '无 acc-cat/glossary'
        end = close_of(seg, glo.start())
        have = set(TAG.sub('', x).strip() for x in DT_RE.findall(seg))
        have |= set(TAG.sub('', x).strip() for x in KAI_RE.findall(seg))
        fmt = '\n        <div class="g-item"><dt>%s</dt><dd>%s</dd></div>'

    todo = [(w, a) for w, a in items if w not in have]
    if not todo:
        return src, 0, '已存在'
    block = ''.join(
        fmt % (w, a if a.rstrip().endswith(('。', '；', '》')) else a.rstrip() + '。')
        for w, a in todo)
    newseg = seg[:end] + block + seg[end:]
    return src[:i] + newseg + src[j:], len(todo), ''


def main():
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    apply = '--apply' in sys.argv
    tot = 0
    for fn, items in sorted(spec.items()):
        p = os.path.join(ROOT, fn)
        if not os.path.exists(p):
            print('!! 缺失', fn)
            continue
        src = open(p, encoding='utf-8').read()
        new, n, msg = add(src, items)
        if new != src and apply:
            open(p, 'w', encoding='utf-8').write(new)
        tot += n
        print('%-52s +%d %s' % (fn[:50], n, msg))
    print('\n合计补入: %d 条  %s' % (tot, '已写入' if apply else '（dry-run）'))


if __name__ == '__main__':
    main()
