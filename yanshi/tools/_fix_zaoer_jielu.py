# -*- coding: utf-8 -*-
"""zaoer jielu 卡片：<div class="v-body"><div class="summary">X</div><div class="v-sec">…</div>…</div>
→ 范例结构 <details class="v-more"><summary>X</summary><div class="d-body"><div class="v-sec">…</div>…</div></details>
内容概括 → v-trans 包裹；手法分析 → d-body 包裹（对齐 beiying 标杆）。"""
import re

F = 'yanshi/zaoer-sunhong.html'
s = open(F, encoding='utf-8').read()
s, n0 = re.subn(' data-page-node-id="[^"]*"', '', s)

i = s.find('<section id="jielu"'); j = s.find('<div class="divider"', i)
seg = s[i:j]

def balanced_close(text, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', text[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start + m.end()
    raise ValueError('unbalanced')

sec_re = re.compile(r'<div class="v-sec">\s*<b class="v-label">([^<]*)</b>\s*(?:<p>(.*?)</p>)\s*</div>', re.S)

def conv_sec(label, body):
    body = body.strip()
    if label == '内容概括':
        inner = '<div class="v-trans">%s</div>' % body
    else:
        inner = '<div class="d-body"><p>%s</p></div>' % body
    return ('<div class="v-sec"><b class="v-label">%s</b>\n              %s\n            </div>' % (label, inner))

out = []
pos = 0
converted = 0
while True:
    k = seg.find('<div class="v-body">', pos)
    if k < 0:
        out.append(seg[pos:]); break
    end = balanced_close(seg, k)
    content = seg[k + len('<div class="v-body">'):end - len('</div>')]
    m = re.match(r'\s*<div class="summary">([^<]*)</div>(.*)$', content, re.S)
    assert m, 'no summary in v-body @%d' % k
    summ = m.group(1).strip()
    secs = sec_re.findall(m.group(2))
    assert len(secs) == 2, 'expect 2 v-sec @%d, got %d' % (k, len(secs))
    inner = '\n            '.join(conv_sec(lb, bd) for lb, bd in secs)
    new = ('<details class="v-more">\n          <summary>%s</summary>\n          <div class="d-body">\n            %s\n          </div>\n        </details>'
           % (summ, inner))
    out.append(seg[pos:k]); out.append(new)
    pos = end
    converted += 1
seg_new = ''.join(out)
assert converted == 16, 'converted %d' % converted
assert 'v-body' not in seg_new and 'class="summary"' not in seg_new
assert seg_new.count('<details class="v-more">') == 16
assert seg_new.count('v-line') == 16 and seg_new.count('anno-word') == seg.count('anno-word'), 'anno drift'

s = s[:i] + seg_new + s[j:]
assert s.count('<div') == s.count('</div>'), 'div unbalanced'
assert 'data-page-node-id' not in s
open(F, 'w', encoding='utf-8', newline='').write(s)
print('OK converted=%d, pollution removed=%d' % (converted, n0))
