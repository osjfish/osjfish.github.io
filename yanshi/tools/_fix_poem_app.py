# -*- coding: utf-8 -*-
"""古诗 app 区对齐琵琶行/天下第一楼范式：
- h3="名句赏析：诗句" → h3="名句赏析"，诗句进卡内 f-line
- 无 f-line 标签的散文卡（艺术特色/主题思想单流文本）→ 拆掉 fame>fame-card 壳，<p> 直接放 box
- 已有 f-line 的名句卡组保持不动
"""
import re

FILES = ['chibi-dumu','dengyouzhoutaige-chenziang','duanzhang-bianzhilin','fengyuyin-ludi',
         'haiyan-gaoerji','jiarushenghuoqipianleni-puxijin','qiantanghuchunxing-baijuyi',
         'tongyi-nieluda','weixuanzedelu-fuluosite','wenwangchanglingzuoqianlongbiaoyaoyouciji-libai',
         'xiaohongmupankouzhan-daiwangshu','youshanxicun-luyou','yueye-shenyinmo','yujiaaoqiusi-fanzhongyan']

def balanced_close(text, start):
    depth = 0
    for m in re.finditer(r'<div\b|</div>', text[start:]):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return start + m.end()
    raise ValueError('unbalanced')

def unwrap_fame(body):
    """body = '<div class=\"fame\">…</div>'；无 f-line 时拆壳返回 box 内直放内容"""
    inner = body[len('<div class="fame">'):-len('</div>')]
    out = []
    pos = 0
    while True:
        k = inner.find('<div class="fame-card">', pos)
        if k < 0:
            out.append(inner[pos:]); break
        end = balanced_close(inner, k)
        card = inner[k + len('<div class="fame-card">'):end - len('</div>')]
        out.append(inner[pos:k]); out.append(card.strip())
        pos = end
    content = ''.join(out).strip()
    return re.sub(r'\n{3,}', '\n  ', content)

for name in FILES:
    F = 'yanshi/%s.html' % name
    s = open(F, encoding='utf-8').read()
    s, _pn = re.subn(' data-page-node-id="[^"]*"', '', s)
    i = s.find('<section id="app"'); j = s.find('<section id="acc"')
    seg = s[i:j]
    changed = {'quote': 0, 'unwrap': 0, 'keep': 0}
    out = []; pos = 0
    while True:
        k = seg.find('<div class="box">', pos)
        if k < 0:
            out.append(seg[pos:]); break
        end = balanced_close(seg, k)
        box = seg[k:end]
        m = re.match(r'<div class="box">\s*<h3>([^<]*)</h3>\s*(.*)$', box, re.S)
        assert m, box[:80]
        title, rest = m.group(1), m.group(2)
        if rest.lstrip().startswith('<div class="fame">'):
            fame_end = balanced_close(rest, rest.find('<div class="fame">'))
            fame = rest[:fame_end]; tail = rest[fame_end:]
            has_fline = 'class="f-line"' in fame
            if title.startswith('名句赏析：'):
                quote = title[len('名句赏析：'):]
                inner = fame[len('<div class="fame">'):-len('</div>')]
                # 每张卡头部插 f-line（此类 box 都是单卡），保留卡开标签
                cm = re.match(r'\s*(<div class="fame-card">)(\s*)(<p>)', inner)
                assert cm, inner[:100]
                inner2 = (inner[:cm.start(2)] + '\n        <div class="f-line">%s</div>%s'
                          % (quote, cm.group(2))) + inner[cm.start(3):]
                new_box = '<div class="box">\n    <h3>名句赏析</h3>\n    <div class="fame">%s</div>\n  </div>' % inner2
                out.append(seg[pos:k]); out.append(new_box); changed['quote'] += 1
            elif not has_fline:
                new_box = '<div class="box">\n    <h3>%s</h3>\n    %s\n  </div>' % (title, unwrap_fame(fame))
                out.append(seg[pos:k]); out.append(new_box); changed['unwrap'] += 1
            else:
                out.append(seg[pos:k]); out.append(box); changed['keep'] += 1
        else:
            out.append(seg[pos:k]); out.append(box); changed['keep'] += 1
        pos = end
    new_seg = ''.join(out)
    # 校验
    assert new_seg.count('<div') == new_seg.count('</div>')
    assert '名句赏析：' not in new_seg
    # 无 f-line 的 fame 壳应清零
    for mm in re.finditer(r'<div class="fame">(.*?)</div>\s*</div>', new_seg, re.S):
        pass
    s = s[:i] + new_seg + s[j:]
    open(F, 'w', encoding='utf-8', newline='').write(s)
    print('%-30s 拆名句x%d 拆散文壳x%d 保留x%d' % (name, changed['quote'], changed['unwrap'], changed['keep']))
