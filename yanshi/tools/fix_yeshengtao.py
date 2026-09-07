# -*- coding: utf-8 -*-
"""叶圣陶篇：卡片补 5 处课文删节 + 郁达夫补"有" + 引号归位（课文原文校准）"""
import re, html as H

fn = r'D:\App\Apps\yanshi\yeshengtaoxianshengersanshi-zhangzhongxing.html'
h = open(fn, 'rb').read().decode('utf-8')

def clean(t):
    return re.sub(r'\s+', '', H.unescape(re.sub(r'<[^>]+>', '', t)))

def make_map(raw):
    """返回 (cleaned, list_of_raw_positions)：cleaned[i] 对应 raw[pos[i]] 起点"""
    out, pos, i = [], [], 0
    while i < len(raw):
        m = re.match(r'<span class="anno-word"[^>]*>', raw[i:])
        if m:
            i += m.end(); continue
        if raw.startswith('</span>', i):
            i += 7; continue
        if raw.startswith('<', i):
            j = raw.find('>', i)
            i = j + 1; continue
        out.append(raw[i]); pos.append(i); i += 1
    return ''.join(out), pos

INSERTS = [
    ('郁达夫', '有'),
    ('白话指什么', '（如有孔乙己的白话，鲁迅的白话，北京市民的白话，等等）'),
    ('除了少数人、个别文体', '（如小说、戏剧里的对话）'),
    ('但更多的是来于认识', '（纵使是不很明确的）'),
    ('就必致付之一笑', '。这里为题目所限，不能牵涉过多，甚至挑起论辩'),
    ('这也要靠慢慢学', '（多念像话的文）'),
]

applied = 0
for anchor, ins in INSERTS:
    # 找包含锚点的 v-line（锚点须在 cleaned 文本中唯一可定位）
    pat = re.compile(r'(<div class="v-line">)(.*?)(</div>)', re.S)
    done = False
    for m in pat.finditer(h):
        body = m.group(2)
        cl, posmap = make_map(body)
        idx = cl.find(anchor)
        if idx == -1:
            continue
        if cl[idx:idx+len(anchor)+len(ins)] == anchor + ins:
            print('  skip (done):', ins[:12]); done = True; break
        # 插入点：锚点末尾之后
        raw_at = posmap[idx + len(anchor)]
        newbody = body[:raw_at] + ins + body[raw_at:]
        h = h[:m.start(2)] + newbody + h[m.end(2):]
        print('  inserted:', ins[:16], 'after', anchor[:10])
        done = True
        applied += 1
        break
    assert done, 'anchor not found: ' + anchor

# 引号：卡片 惟德是辅”。 -> 惟德是辅。”（课文原样，句号在引号内；注意注释 span 挡在中间）
n = h.count('辅</span>”。')
assert n == 1, 'quote count %d' % n
h = h.replace('辅</span>”。', '辅</span>。”')
print('  fixed quote')
applied += 1

open(fn, 'wb').write(h.encode('utf-8'))
print('ALL FIXED, applied =', applied)
