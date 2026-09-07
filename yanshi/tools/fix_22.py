# -*- coding: utf-8 -*-
"""七上 22 篇审计问题修复 v2（幂等，二进制读写保留原行尾）"""
import re

BASE = r'D:\App\Apps\yanshi'

def load(fn):
    return open(BASE + '\\' + fn, 'rb').read().decode('utf-8')

def save(fn, h):
    open(BASE + '\\' + fn, 'wb').write(h.encode('utf-8'))

def sub1(h, old, new, tag):
    n = h.count(old)
    if n == 0 and h.count(new) == 1:
        print('  skip (already fixed):', tag)
        return h
    assert n == 1, 'sub1 %s: found %d' % (tag, n)
    return h.replace(old, new)

def subre(h, pattern, new, tag):
    n = len(re.findall(pattern, h))
    assert n == 1, 'subre %s: found %d' % (tag, n)
    return re.sub(pattern, new, h)

def fix_lq(h, fn):
    """{LQ}/{RQ} -> 按嵌套深度换成 “” / ‘’（幂等）"""
    if '{LQ}' not in h and '{RQ}' not in h:
        print('  skip (no placeholders):', fn)
        return h
    out, stack, i = [], [], 0
    while True:
        a, b = h.find('{LQ}', i), h.find('{RQ}', i)
        cand = [x for x in (a, b) if x != -1]
        if not cand:
            out.append(h[i:])
            break
        j = min(cand)
        out.append(h[i:j])
        if h[j:j+4] == '{LQ}':
            stack.append(j)
            out.append('‘' if len(stack) >= 2 else '“')
        else:
            assert stack, '%s: unmatched {RQ} @%d' % (fn, j)
            out.append('’' if len(stack) >= 2 else '”')
            stack.pop()
        i = j + 4
    assert not stack, '%s: unclosed {LQ}' % fn
    return ''.join(out)

# ---------- 1) yudesiji: 畸形注释 span（内嵌 span） ----------
fn = 'yudesiji-liuzhanqiu.html'
h = load(fn)
old = ('<span class="anno-word" data-note="形容简洁、不拖泥带水。文中指'
       '<span class="anno-word" data-note="版画的一种，在木刻上刻画图形后印出来的画。特点是线条分明、简洁有力">木刻</span>'
       '画面的简洁有力">干净利落</span>')
new = ('<span class="anno-word" data-note="形容简洁、不拖泥带水。文中指木刻画面的简洁有力。'
       '木刻，版画的一种，特点是线条分明、简洁有力">干净利落</span>')
h = sub1(h, old, new, fn + '/span')
save(fn, h)
print('OK', fn)

# ---------- 2) jinianbaiqiuen: 畸形注释 span + {LQ}/{RQ} ----------
fn = 'jinianbaiqiuen-maozedong.html'
h = load(fn)
old = ('<span class="anno-word" data-note="帝国主义和'
       '<span class="anno-word" data-note="工人阶级，在资本主义社会中不占有生产资料、靠出卖劳动力为生的阶级">无产阶级</span>'
       '革命时代的马克思主义，是列宁在领导俄国革命和国际共产主义运动中创立的理论体系">列宁主义</span>认为：资本主义国家的')
new = ('<span class="anno-word" data-note="帝国主义和无产阶级革命时代的马克思主义，是列宁在领导俄国革命和国际共产主义运动中创立的理论体系">列宁主义</span>'
       '认为：资本主义国家的'
       '<span class="anno-word" data-note="工人阶级，在资本主义社会中不占有生产资料、靠出卖劳动力为生的阶级">无产阶级</span>')
h = sub1(h, old, new, fn + '/span')
h = fix_lq(h, fn)
save(fn, h)
print('OK', fn)

# ---------- 3) qieduji: {LQ}/{RQ} ----------
fn = 'qieduji-linhaiyin.html'
h = load(fn)
h = fix_lq(h, fn)
save(fn, h)
print('OK', fn)

# ---------- 4) huangdindexinzhuang: 典礼 w 不在例句 -> 游行大典 ----------
fn = 'huangdindexinzhuang-antusheng.html'
h = load(fn)
h = subre(h,
    r'\{"w":\s*"典礼",\s*"a":\s*"郑重举行的仪式",\s*"q":\s*"以便举在陛下头顶上去参加游行大典"\}',
    '{"w": "游行大典", "a": "郑重举行的隆重仪式", "q": "以便举在陛下头顶上去参加游行大典"}',
    fn + '/note')
save(fn, h)
print('OK', fn)

# ---------- 5) zaishengmingderen: 占位符 + 两条词语题 ----------
fn = 'zaishengmingderen-hailunkailun.html'
h = load(fn)
h = sub1(h, '也作{LQ}依本画葫芦{RQ}', '也作“依本画葫芦”', fn + '/ph1')
h = sub1(h, '（跟{LQ}有形{RQ}相对）', '（跟“有形”相对）', fn + '/ph2')
old_g = '{"w": "给予", "a": "给", "q": "并给予我光明、希望、快乐和自由"}'
new_g = '{"w": "给予", "a": "交付、送上；使别人得到", "q": "并给予我光明、希望、快乐和自由"}'
h = sub1(h, old_g, new_g, fn + '/give')
old_t = '{"w": "触摸", "a": "用手接触后轻轻移动", "q": "因为当时除了手能摸到的东西以外"}, '
h = sub1(h, old_t, '', fn + '/touch')
h = fix_lq(h, fn)
save(fn, h)
print('OK', fn)
print('ALL FIXED')
