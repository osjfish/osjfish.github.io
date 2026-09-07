# -*- coding: utf-8 -*-
"""通用：pl / v-line 块内文本替换，保留并重新锚定注释 span（分段映射版）"""
import re

TAG = re.compile(r'<[^>]+>')
ANNO = re.compile(r'<span class="anno-word"[^>]*data-note="([^"]*)"[^>]*>([^<]*)</span>')
BLOCK = re.compile(r'(<div[^>]*class="(?:pl|v-line)"[^>]*>)(.*?)(</div>)', re.S)


def _span(note, word):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)


def _atoms(inner):
    """拆分为文本片段与注释片段"""
    out, idx = [], 0
    while idx < len(inner):
        m = ANNO.search(inner, idx)
        if not m:
            if idx < len(inner):
                out.append(('t', inner[idx:]))
            break
        if m.start() > idx:
            out.append(('t', inner[idx:m.start()]))
        out.append(('a', m.group(2), m.group(1)))
        idx = m.end()
    return out


def reanchor(inner, old, new, alias=None, log=None):
    """块内替换：仅重建被替换区，其余片段原样保留"""
    alias = alias or {}
    atoms = _atoms(inner)
    items, plain_parts, off = [], [], 0
    for a in atoms:
        if a[0] == 't':
            t = TAG.sub('', a[1])
            items.append([off, off + len(t), 't', a[1]])
            plain_parts.append(t)
            off += len(t)
        else:
            w = a[1]
            items.append([off, off + len(w), 'a', (a[1], a[2])])
            plain_parts.append(w)
            off += len(w)
    plain = ''.join(plain_parts)
    i = plain.find(old)
    if i < 0:
        return inner, 0
    j = i + len(old)

    def emit_html(kind, payload):
        return payload if kind == 't' else _span(payload[1], payload[0])

    pre, post, mid_a, post_edge = [], [], [], []
    for s, e, kind, payload in items:
        if e <= i:
            pre.append(emit_html(kind, payload))
        elif s >= j:
            post.append(emit_html(kind, payload))
        else:
            if kind == 'a':
                mid_a.append(payload)
            else:
                # 文本片段部分落在替换区：分别保留其前后两段纯文本
                t = TAG.sub('', payload)
                a1, b1 = max(0, i - s), min(len(t), j - s)
                if t[:a1]:
                    pre.append(t[:a1])
                if t[b1:]:
                    post_edge.append(t[b1:])

    region, used, dropped = new, [], []
    for word, note in mid_a:
        for cand in (word, alias.get(word, '')):
            if not cand:
                continue
            start, pos = 0, -1
            while True:
                p = region.find(cand, start)
                if p == -1:
                    break
                if not any(p < e and p + len(cand) > b for b, e in used):
                    pos = p
                    break
                start = p + 1
            if pos >= 0:
                sp = _span(note, cand)
                region = region[:pos] + sp + region[pos + len(cand):]
                shift = len(sp) - len(cand)
                used = [(b + shift if b > pos else b, e + shift if e > pos else e)
                        for b, e in used]
                used.append((pos, pos + len(sp)))
                break
        else:
            dropped.append((word, note))

    result = ''.join(pre) + region + ''.join(post_edge) + ''.join(post)
    # 跨替换区未能就地重锚的注释：在整段结果中按（别名优先）补锚
    if dropped:
        occ = [(m.start(), m.end()) for m in ANNO.finditer(result)]
        for word, note in dropped:
            for cand in (alias.get(word, ''), word):
                if not cand:
                    continue
                start, pos = 0, -1
                while True:
                    p = result.find(cand, start)
                    if p == -1:
                        break
                    if not any(p < e and p + len(cand) > b for b, e in occ):
                        pos = p
                        break
                    start = p + 1
                if pos >= 0:
                    sp = _span(note, cand)
                    result = result[:pos] + sp + result[pos + len(cand):]
                    shift = len(sp) - len(cand)
                    occ = [(b + shift if b > pos else b, e + shift if e > pos else e)
                           for b, e in occ]
                    occ.append((pos, pos + len(sp)))
                    break
            else:
                if log is not None:
                    log.append('drop anno: %s' % word)
    return result, 1


def blocks_sub(s, old, new, expect=None, alias=None, log=None, verbose=True):
    cnt = 0

    def repl(m):
        nonlocal cnt
        ni, ch = reanchor(m.group(2), old, new, alias, log)
        cnt += ch
        return m.group(1) + ni + m.group(3)

    s = re.sub(BLOCK, repl, s)
    if verbose:
        print('  %-30s -> %-26s x%d' % (old[:28], new[:24], cnt))
    if expect is not None:
        assert cnt == expect, 'count %d != %d for %s' % (cnt, expect, old)
    return s, cnt
