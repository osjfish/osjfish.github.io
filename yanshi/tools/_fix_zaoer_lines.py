# -*- coding: utf-8 -*-
"""zaoer 戏剧正文修复：
- fulltext：多回合台词拆成独立 <div class="pl">，说话人加"："（舞台提示括号后），叙述独立成段——对齐《天下第一楼》。
- 卡片 v-line：同样位置插 <br> 与"："（文本节点层面操作，注释 span 原样保留）。
- 断言：每张卡清洗文本变换前后一致；卡片↔正文逐字一致。"""
import re

F = 'yanshi/zaoer-sunhong.html'
QOPEN = {'“': '”', '"': '"', '「': '」', '『': '』'}

s = open(F, encoding='utf-8').read()
s, n0 = re.subn(' data-page-node-id="[^"]*"', '', s)

# ---------- 分析器 ----------
def sentences(t):
    out = []; start = 0; i = 0; q = None
    while i < len(t):
        ch = t[i]
        if q:
            if ch == q: q = None
        elif ch in QOPEN:
            q = QOPEN[ch]
        elif ch in '。？！':
            out.append((start, i + 1)); start = i + 1
        i += 1
    if start < len(t): out.append((start, len(t)))
    return out

def build_segs(t):
    """说话人名开头的句子开新段；段=(start,end,kind,colon) kind='d'台词/'n'叙述"""
    starts = [0]; kinds = {0: ('n', None)}
    for (a, b) in sentences(t):
        sent = t[a:b]
        m = re.match(r'(老人|男孩)', sent)
        if m:
            if a > 0:
                starts.append(a)
            rest = sent[m.end():]
            if rest.startswith('（'):
                k = t.find('）', a + m.end())
                kinds[a] = ('d', k + 1) if (k != -1 and k < b) else ('n', None)
            elif rest[:1] in (' ', '\u3000'):
                kinds[a] = ('d', a + m.end())
            else:
                kinds[a] = ('n', None)
    starts = sorted(set(starts))
    segs = []
    for idx, st in enumerate(starts):
        en = starts[idx + 1] if idx + 1 < len(starts) else len(t)
        kind, colon = kinds.get(st, ('n', None))
        if t[st:en].strip():
            segs.append((st, en, kind, colon))
    return segs

def piece_of(t, seg):
    a, b, kind, colon = seg
    piece = t[a:b]
    if colon is not None:
        c = colon - a                # 段内相对位置（指向空格或台词首字）
        j = c
        while j < len(piece) and piece[j] in ' \u3000':
            j += 1
        piece = piece[:c] + '：' + piece[j:]
    return piece

def tokenize(html):
    return re.split(r'(<[^>]+>)', html)

# ---------- 1) fulltext ----------
i = s.find('id="fulltext"')
j = s.find('<div class="verse-list"', i)
ft = s[i:j]
old_pls = re.findall(r'<div class="pl">(.*?)</div>', ft, re.S)
new_ft_parts = []
last = 0
groups = []   # 每原 pl 的新 pl 文本列表
total = 0
for m in re.finditer(r'<div class="pl">.*?</div>', ft, re.S):
    new_ft_parts.append(ft[last:m.start()])
    t = re.match(r'<div class="pl">(.*?)</div>', m.group(0), re.S).group(1)
    pieces = [piece_of(t, sg) for sg in build_segs(t)]
    groups.append(pieces)
    for p in pieces:
        new_ft_parts.append('<div class="pl">%s</div>\n    ' % p)
        total += 1
    last = m.end()
new_ft_parts.append(ft[last:])
new_ft = ''.join(new_ft_parts)
# 正文自检：剥空白去冒号后内容不变
strip_all = lambda x: re.sub(r'：', '', re.sub(r'\s+', '', x))
for oi, op in enumerate(old_pls):
    assert strip_all(''.join(groups[oi])) == strip_all(op), 'fulltext pl %d drift' % (oi + 1)
assert s.count(ft[:200]) == 1
s = s[:i] + new_ft + s[j:]
print('fulltext pl: %d -> %d' % (len(old_pls), total))

# ---------- 2) 卡片 ----------
vlines = re.findall(r'<div class="v-line">.*?</div>', s, re.S)
assert len(vlines) == 16, len(vlines)
ok = 0
for gi, vl in enumerate(vlines):
    html = vl[len('<div class="v-line">'):-len('</div>')]
    parts = tokenize(html)
    t = ''.join(p for p in parts if p and not p.startswith('<'))
    segs = build_segs(t)
    # clean 层编辑
    edits = {}   # clean_pos -> [(str, is_br)]
    skips = []   # (a,b) 吞掉的空格区间
    for idx, sg in enumerate(segs):
        if idx > 0:
            edits.setdefault(sg[0], []).append(('<br>', True))
        if sg[3] is not None:
            edits.setdefault(sg[3], []).append(('：', False))
            k = sg[3]
            while k < len(t) and t[k] in ' \u3000':
                k += 1
            if k > sg[3]:
                skips.append((sg[3], k))
    def in_skip(pos):
        return any(a <= pos < b for a, b in skips)
    buf = []; clen = 0
    for tok in parts:
        if tok.startswith('<'):
            buf.append(tok); continue
        out = []
        for off, ch in enumerate(tok):
            pos = clen + off
            for st, _ in edits.get(pos, []):
                out.append(st)
            if not in_skip(pos):
                out.append(ch)
        endpos = clen + len(tok)
        for st, _ in edits.get(endpos, []):
            out.append(st)
        clen += len(tok)
        buf.append(''.join(out))
    new_vl = ''.join(buf)
    # 校验：剥标签去空白去冒号后与原文一致；冒号数 = 原冒号数 + 台词段数
    strip_all = lambda x: re.sub(r'：', '', re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', x)))
    assert strip_all(new_vl) == strip_all(html), 'card %d drift' % (gi + 1)
    ncolon = new_vl.count('：') - html.count('：')
    assert ncolon == sum(1 for sg in segs if sg[2] == 'd'), 'card %d colon count' % (gi + 1)
    # 与正文一致性：剥标签去空白去冒号后逐字相同
    ft_clean = strip_all(''.join(groups[gi]))
    card_clean = strip_all(new_vl)
    if card_clean != ft_clean:
        print('MISMATCH card %d:\n  card=%r\n  ft  =%r' % (gi + 1, card_clean[:150], ft_clean[:150]))
    assert s.count(vl) == 1, 'vline %d not unique' % (gi + 1)
    s = s.replace(vl, '<div class="v-line">' + new_vl + '</div>', 1)
    ok += 1
print('cards ok:', ok)

assert s.count('<div') == s.count('</div>'), 'div unbalanced'
assert 'data-page-node-id' not in s
open(F, 'w', encoding='utf-8', newline='').write(s)
print('written')
