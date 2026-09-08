# -*- coding: utf-8 -*-
"""app 区顶层裸分类卡 <div class="fame-card"><h3>CAT</h3>…</div>
→ <div class="box"><h3>CAT</h3> + fame 包装（保留内部已有的 fame>fame-card 结构）"""
import re, sys

FILES = [
    'yanshi/chibi-dumu.html',
    'yanshi/dengyouzhoutaige-chenziang.html',
    'yanshi/duanzhang-bianzhilin.html',
    'yanshi/fengyuyin-ludi.html',
    'yanshi/haiyan-gaoerji.html',
    'yanshi/jiarushenghuoqipianleni-puxijin.html',
    'yanshi/qiantanghuchunxing-baijuyi.html',
    'yanshi/tongyi-nieluda.html',
    'yanshi/weixuanzedelu-fuluosite.html',
    'yanshi/wenwangchanglingzuoqianlongbiaoyaoyouciji-libai.html',
    'yanshi/xiaohongmupankouzhan-daiwangshu.html',
    'yanshi/youshanxicun-luyou.html',
    'yanshi/yueye-shenyinmo.html',
    'yanshi/yujiaaoqiusi-fanzhongyan.html',
]

def balanced_close(text, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', text[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start + m.end()
    raise ValueError('unbalanced')

open_re = re.compile(r'<div class="fame-card">\s*<h3>([^<]+)</h3>')

for F in FILES:
    s = open(F, encoding='utf-8').read()
    i = s.find('<section id="app"')
    j = s.find('<section id="acc"'); j = j if j > i else s.find('</section>', i)
    app = s[i:j]
    changed = 0
    while True:
        m = open_re.search(app)
        if not m:
            break
        cat = m.group(1)
        content_start = m.end()
        card_open = app.rfind('<div class="fame-card">', 0, content_start)
        assert card_open != -1
        card_end = balanced_close(app, card_open)
        content = app[content_start:card_end - len('</div>')]
        cstrip = content.lstrip()
        if cstrip.startswith('<div class="fame">'):
            # 内容已是 fame 块（内含条目卡）——原样放进 box
            new = '<div class="box">\n    <h3>%s</h3>\n    %s\n  </div>' % (cat, cstrip.rstrip())
        else:
            new = ('<div class="box">\n    <h3>%s</h3>\n    <div class="fame">\n      <div class="fame-card">%s\n      </div>\n    </div>\n  </div>'
                   % (cat, content.rstrip()))
        app = app[:card_open] + new + app[card_end:]
        changed += 1
    # 校验：app 区不再有裸分类卡，div 平衡
    assert not open_re.search(app), F + ': leftover'
    assert app.count('<div') == app.count('</div>'), F + ': unbalanced'
    s = s[:i] + app + s[j:]
    open(F, 'w', encoding='utf-8', newline='').write(s)
    print('%-52s x%d' % (F.split('/')[-1], changed))
