# -*- coding: utf-8 -*-
"""zaoer app/acc/practice 对齐范例（beiying/tianxiadiyilou）结构。
输入为 HEAD 原始形态：app = 子sec-head + fame-grid>fame-card(h4+p)；acc = 子sec-head + acc-box；practice = practice-box + 旧版浮层。
"""
import re

F = 'yanshi/zaoer-sunhong.html'
s = open(F, encoding='utf-8').read()
s, n0 = re.subn(' data-page-node-id="[^"]*"', '', s)
orig_len = len(s)

def balanced_close(text, start):
    pos_depth = 0
    for m in re.finditer(r'<div\b|</div>', text[start:]):
        pos_depth += 1 if m.group(0) == '<div' else -1
        if pos_depth == 0:
            return start + m.end()
    raise ValueError('unbalanced div at %d' % start)

# ---------- 1) app ----------
i = s.find('<section id="app"'); j = s.find('<section id="acc"')
app = s[i:j]
main_head = app[:app.find('</div>') + len('</div>')]  # 第一行 sec-head（赏 析）

# 子栏分组
sub_re = re.compile(r'[ \t]*<div class="sec-head"><h2>(人物形象|艺术特色|名句赏析|主题思想)</h2>(?:<span class="no">[^<]*</span>)?</div>\s*\n?')
groups = []  # (cat, segment)
positions = [m for m in sub_re.finditer(app)]
assert len(positions) == 4, 'expect 4 sub heads, got %d' % len(positions)
for k, m in enumerate(positions):
    end = positions[k + 1].start() if k + 1 < len(positions) else app.find('</section>')
    groups.append((m.group(1), app[m.end():end]))

card_re = re.compile(r'<div class="fame-card">\s*<h4>([^<]*)</h4>\s*(<p>.*?</p>)\s*</div>', re.S)

def make_box(h3, items):
    body = ''.join(
        '<div class="fame-card">\n        <div class="f-line">%s</div>\n        %s\n      </div>\n      ' % (t, b)
        for t, b in items)
    return ('  <div class="box">\n    <h3>%s</h3>\n    <div class="fame">\n      %s\n    </div>\n  </div>\n' % (h3, body))

new_app = '<section id="app">\n  ' + main_head.strip() + '\n'
total_cards = 0
for cat, seg in groups:
    cards = card_re.findall(seg)
    total_cards += len(cards)
    if cat == '主题思想':
        # theme 段：优先取裸 <p>（theme-box），否则取卡片
        ps = re.findall(r'<p>.*?</p>', seg, re.S)
        if ps:
            body = '\n      '.join(ps)
            new_app += '  <div class="box">\n    <h3>主题思想</h3>\n      %s\n  </div>\n' % body
        else:
            assert cards, 'theme group empty'
            new_app += make_box('主题思想', cards)
    else:
        assert cards, 'group %s has no cards' % cat
        new_app += make_box(cat, cards)
assert total_cards == 9, 'expect 9 cards total, got %d' % total_cards
new_app += '</section>'
s = s[:i] + new_app + s[j:]

# ---------- 2) acc ----------
i = s.find('<section id="acc"'); j = s.find('<section id="practice"')
acc = s[i:j]
regex_head = re.compile(r'[ \t]*<div class="sec-head"><h2>([^<]+)</h2><span class="no">([^<]*)</span></div>[ \t]*\n?')
search_from = 0
converted = []
while True:
    m = regex_head.search(acc, search_from)
    if not m:
        break
    cat = m.group(1)
    if cat == '积 累':  # 主栏头，跳过
        search_from = m.end()
        continue
    rest = acc[m.end():]
    b = rest.find('<div class="acc-box">')
    assert rest[:b].strip() == '', 'gap after head %s: %r' % (cat, rest[:b][:80])
    end = balanced_close(rest, b)
    body = rest[b + len('<div class="acc-box">'):end - len('</div>')]
    body = re.sub(r'^\s+|\s+$', '', body)
    box_new = ('  <div class="box">\n    <div class="acc-cat"><h3>%s</h3></div>\n    %s\n  </div>' % (cat, body))
    acc = acc[:m.start()] + box_new + rest[end:]
    converted.append(cat)
    search_from = m.start() + len(box_new)
assert len(converted) == 5, 'expect 5 acc cats, got %s' % converted
s = s[:i] + acc + s[j:]

# ---------- 3) practice ----------
i = s.find('<section id="practice"'); j = s.find('</section>', i)
prac = s[i:j]
prac, n2 = re.subn(r'<div class="practice-box">',
                   '<div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>\n    <div class="ptools">', prac)
assert n2 == 1
k = prac.find('<div id="dictate"')
assert k >= 0, 'legacy dictate not found'
end = balanced_close(prac, k)
while end < len(prac) and prac[end] in '\r\n':
    end += 1
prac = prac[:k] + prac[end:]
assert prac.count('id="dictate"') == 0 and 'dict-top' not in prac

# 3b. sec-head 文案对齐范例：练 习
prac = prac.replace('<h2>全屏听写</h2><span class="no">字形 · 词语</span>',
                    '<h2>练 习</h2><span class="no">字形 · 词语 · 全屏听写</span>')
s = s[:i] + prac + s[j:]

# ---------- 校验 ----------
assert s.count('<div') == s.count('</div>'), 'div unbalanced'
assert s.count('id="dictate"') == 1
assert 'practice-box' not in s and 'acc-box' not in s and 'theme-box' not in s and 'fame-grid' not in s
assert 'data-page-node-id' not in s
open(F, 'w', encoding='utf-8', newline='').write(s)
print('OK  removed pollution=%d, delta=%d' % (n0, len(s) - orig_len))
