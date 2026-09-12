# -*- coding: utf-8 -*-
"""
逐篇深度体检 v3（只读）。覆盖 _audit_all / _audit_anno2 之外的项，重点：
  · 解读区 fulltext 的 <div class="pl"> 与 verse 卡片 .v-line 文本是否逐条一致（铁律）
  · 六区非空、空标题/空卡片、注释缺失属性
  · 题库字段完整性（□数=字数、拼音音节、tip、答案为空、题量为 0）
  · 积累区空释义、本地媒体文件是否丢失
  · 重复 id / 段号连续性
用法：python _audit_deep.py [--json out.json]
"""
import os, re, sys, json, collections, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}
TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')
NO = re.compile(r'<span class="no">.*?</span>', re.S)
SEC_IDS = ['bg', 'jielu', 'app', 'acc', 'practice']


def txt(s):
    return WS.sub('', html.unescape(TAG.sub('', NO.sub('', s))))


def norm(s):
    """去掉注音括号与标点差异，用于 pl/v-line 内容比对"""
    s = txt(s)
    s = re.sub(r'[（(][a-zA-Zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü0-9\s]*[)）]', '', s)
    s = re.sub(r'[，。、；：！？“”‘’＇\'…—·＜＞《》\s]', '', s)
    return s


def blocks(src, cls):
    """抓取 class 属性中包含 cls 的 <div>...</div> 的 innerHTML（按 div 深度配对）"""
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


def parse_dict(src, name):
    m = re.search(r'(?:var|let|const)?\s*%s\s*=\s*(\[.*?\])\s*;' % name, src, re.S)
    if not m:
        return None
    raw = m.group(1)
    try:
        return json.loads(raw)
    except Exception:
        pass
    out = []
    for blk in re.finditer(r'\{([^{}]*)\}', raw):
        d = {}
        for k in ('w', 'a', 'q', 'py', 'tip'):
            mm = re.search(r"""['"]?%s['"]?\s*:\s*(['"])(.*?)\1""" % k, blk.group(1), re.S)
            if mm:
                d[k] = mm.group(2)
        if d:
            out.append(d)
    return out


def audit(fn):
    p = os.path.join(ROOT, fn)
    src = open(p, encoding='utf-8').read()
    body = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
    body = re.sub(r'<style\b[^>]*>.*?</style>', '', body, flags=re.S | re.I)
    plain = txt(body)
    iss = collections.defaultdict(list)

    # ---- 1. 六区齐全 ----
    pos = {}
    for sid in SEC_IDS:
        k = src.find('id="%s"' % sid)
        if k < 0:
            iss['缺区'].append(sid)
        else:
            pos[sid] = k
    if len(pos) == len(SEC_IDS) and [pos[s] for s in SEC_IDS] != sorted(pos.values()):
        iss['六区顺序错'].append(str([s for s in sorted(pos, key=lambda x: pos[x])]))

    # ---- 2. 各区非空 ----
    for sid in SEC_IDS:
        if sid not in pos:
            continue
        nxt = min([v for v in pos.values() if v > pos[sid]], default=len(src))
        seg = txt(src[pos[sid]:nxt])
        if len(seg) < 120:
            iss['区内容过少'].append('%s(%d字)' % (sid, len(seg)))

    # ---- 3. pl 与 v-line 一致性（铁律）----
    pls = [txt(x) for x in blocks(src, 'pl')]
    pls = [x for x in pls if x]
    vls = [txt(x) for x in blocks(src, 'v-line')]
    vls = [x for x in vls if x]
    if pls and vls:
        # pl 为全文句、v-line 为解读卡片句，允许粒度不同：拼接后内容须完全一致
        a, b = ''.join(norm(x) for x in pls), ''.join(norm(x) for x in vls)
        # 署名/日期落款（如信件末尾"维克多·雨果 1861年…"）不进解读卡片，允许 pl 尾部多出
        if a == b:
            pass
        elif a.startswith(b) and len(a) - len(b) <= 30:
            pass  # pl 尾部多出落款，属正常
        elif b.startswith(a) and len(b) - len(a) <= 30:
            pass  # v-line 尾部多出，属正常
        elif len(pls) != len(vls):
            iss['pl/v-line内容不符'].append('pl=%d v-line=%d' % (len(pls), len(vls)))
        else:
            for i, (x, y) in enumerate(zip(pls, vls)):
                if norm(x) != norm(y):
                    iss['pl/v-line内容不符'].append('第%d条 pl=%s vline=%s' % (i + 1, txt(x)[:18], txt(y)[:18]))
                    break
    elif vls and not pls:
        iss['无fulltext'].append('v-line=%d' % len(vls))

    # ---- 4. 注释 ----
    annos = re.findall(r'<span class="anno-word"([^>]*)>(.*?)</span>', src, re.S)
    for attr, inner in annos:
        w = txt(inner)
        if 'data-note' not in attr:
            iss['注释缺data-note'].append(w[:10])
            continue
        m = re.search(r'data-note="([^"]*)"', attr)
        if not m or not m.group(1).strip():
            iss['注释释义为空'].append(w[:10])
        elif m.group(1).strip() == w:
            iss['注释等于词'].append(w[:10])
    if not annos and len(plain) > 3000:
        iss['通篇无注释'].append('')

    # ---- 5. 重复 id ----
    ids = re.findall(r'\sid="([^"]+)"', src)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dup:
        iss['重复id'].append(','.join(dup[:4]))

    # ---- 6. 段号连续性 ----
    nos = sorted(int(x) for x in re.findall(r'<div class="verse" id="l(\d+)"', src))
    if nos and nos != list(range(1, len(nos) + 1)):
        iss['段号不连续'].append(str(nos[:12]))

    # ---- 7. 空标题 / 空卡片 ----
    for m in re.finditer(r'<h3>(.*?)</h3>', src, re.S):
        if not txt(m.group(1)):
            iss['空h3'].append('')
    for m in re.finditer(r'<div class="v-line">(.*?)</div>', src, re.S):
        if not txt(m.group(1)):
            iss['空v-line'].append('')

    # ---- 8. 题库 ----
    dw = parse_dict(src, 'DICT_WORDS')
    dn = parse_dict(src, 'DICT_NOTES')
    if dw is None and dn is None:
        iss['无题库'].append('')
    if dw is not None:
        if len(dw) == 0:
            iss['字形题量为0'].append('')
        for d in dw:
            if not isinstance(d, dict):
                continue
            w, q, py, tip = d.get('w', ''), d.get('q', ''), d.get('py', ''), d.get('tip', '')
            if not w:
                iss['字形题缺w'].append('')
                continue
            if not q:
                iss['字形题缺q'].append(w)
            if q and q.count('□') != len(w):
                iss['□数≠答案字数'].append('%s(%d/%d)' % (w, q.count('□'), len(w)))
            if py and len(py.split()) != len(w) and len(py.split()) != 1:
                iss['拼音音节数不符'].append('%s=%s' % (w, py))
            if not tip or tip.strip() == w:
                iss['字形题tip无效'].append(w)
            if w not in plain and not all(c in plain for c in w):
                iss['字形答案不在课文'].append(w)
    if dn is not None:
        if len(dn) == 0:
            iss['注释题量为0'].append('')
        for d in dn:
            if not isinstance(d, dict):
                continue
            if not d.get('w'):
                iss['注释题缺w'].append('')
            if not (d.get('a') or '').strip():
                iss['注释题释义为空'].append(d.get('w', '')[:10])
            if not (d.get('q') or '').strip():
                iss['注释题缺q'].append(d.get('w', '')[:10])

    # ---- 9. 积累区空释义 ----
    for m in re.finditer(r'<div class="acc-item">(.*?)</div>\s*(?=<div class="acc-item"|</div>)', src, re.S):
        seg = m.group(1)
        d = re.search(r'class="acc-(?:d|desc|exp)">(.*?)</span>', seg, re.S)
        if d is None or not txt(d.group(1)):
            iss['积累区空释义'].append(txt(seg)[:12])
    for m in re.finditer(r'<div class="g-item">(.*?)</div>', src, re.S):
        d = re.search(r'<dd>(.*?)</dd>', m.group(1), re.S)
        if d is None or not txt(d.group(1)):
            iss['词条空释义'].append(txt(m.group(1))[:12])

    # ---- 10. 本地媒体文件是否存在 ----
    for m in re.finditer(r'(?:src|href)="((?!https?:|//|#|data:)[^"]+)"', src):
        u = m.group(1)
        if u.endswith(('.mp4', '.jpg', '.png', '.webp', '.gif', '.mp3')):
            if not os.path.exists(os.path.join(ROOT, u)):
                iss['媒体文件缺失'].append(u)

    # ---- 11. 练习区四按钮 ----
    btns = re.findall(r'<button[^>]*id="(btn\w*)"[^>]*>(.*?)</button>', src, re.S)
    if len(btns) < 4:
        iss['练习按钮不足'].append(str(len(btns)))

    return iss, len(annos), len(dw or []), len(dn or []), len(plain)


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    agg = collections.defaultdict(list)
    rows = []
    for fn in files:
        iss, na, nw, nn, ln = audit(fn)
        rows.append((fn, na, nw, nn, ln))
        for k, v in iss.items():
            agg[k].append('%s: %s' % (fn, ';'.join(v[:4])))
    print('文件数:', len(files))
    print('平均注释/字形题/注释题: %.1f / %.1f / %.1f' % (
        sum(r[1] for r in rows) / len(rows),
        sum(r[2] for r in rows) / len(rows),
        sum(r[3] for r in rows) / len(rows)))
    print('=' * 66)
    for k in sorted(agg, key=lambda x: -len(agg[x])):
        print('\n【%s】 %d 篇' % (k, len(agg[k])))
        for line in agg[k][:30]:
            print('   ', line[:170])
        if len(agg[k]) > 30:
            print('    ... 另 %d 篇' % (len(agg[k]) - 30))
    if '--json' in sys.argv:
        json.dump({k: v for k, v in agg.items()},
                  open(sys.argv[sys.argv.index('--json') + 1], 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
