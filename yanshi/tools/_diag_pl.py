# -*- coding: utf-8 -*-
"""诊断 pl 与 v-line 的真实对应关系（只读，输出到 json）"""
import os, re, sys, json, collections, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}
TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')
NO = re.compile(r'<span class="no">.*?</span>', re.S)


def txt(s):
    return WS.sub('', html.unescape(TAG.sub('', NO.sub('', s))))


def blocks(src, cls):
    """抓取 class 属性中包含 cls 的 <div>...</div> 的 innerHTML"""
    out = []
    for m in re.finditer(r'<div class="[^"]*\b%s\b[^"]*"[^>]*>' % cls, src):
        p = m.end()
        depth = 1
        while depth > 0:
            nd = src.find('<div', p)
            cd = src.find('</div>', p)
            if cd < 0:
                break
            if nd >= 0 and nd < cd:
                depth += 1
                p = nd + 4
            else:
                depth -= 1
                p = cd + 6
        out.append(src[m.end():p - 6])
    return out


def norm(s):
    """去掉注音括号、标点差异（不再删句首数字——编号已由 NO 剔除）"""
    s = txt(s)
    s = re.sub(r'[（(][a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü0-9\s]*[)）]', '', s)
    s = re.sub(r'[，。、；：！？“”‘’＇\'…—·＜＞《》\s]', '', s)
    return s


def diag(fn):
    src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
    src = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
    src = re.sub(r'<style\b[^>]*>.*?</style>', '', src, flags=re.S | re.I)
    pls = [txt(x) for x in blocks(src, 'pl')]
    pls = [x for x in pls if x]
    vls = [txt(x) for x in blocks(src, 'v-line')]
    vls = [x for x in vls if x]
    if not pls or not vls:
        return None
    return {'file': fn, 'npl': len(pls), 'nvl': len(vls),
            'pl': pls, 'vl': vls,
            'pln': [norm(x) for x in pls], 'vln': [norm(x) for x in vls]}


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    only = sys.argv[1] if len(sys.argv) > 1 else None
    out = []
    for fn in files:
        d = diag(fn)
        if not d:
            continue
        # 归一化后是否一致
        if d['npl'] == d['nvl'] and d['pln'] == d['vln']:
            continue  # 仅是格式差异，误报
        out.append(d)
    print('归一化后仍不一致（条数或文本）:', len(out))
    for d in out:
        if only and only not in d['file']:
            continue
        print('=' * 70)
        print('%s  pl=%d vl=%d' % (d['file'], d['npl'], d['nvl']))

    if '--json' in sys.argv:
        json.dump(out, open(sys.argv[sys.argv.index('--json') + 1], 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
