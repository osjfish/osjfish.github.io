# -*- coding: utf-8 -*-
"""七下 16 篇审计问题修复（幂等，二进制读写保留行尾；按文件名定点操作，不用 add -A）"""
import os

BASE = r'D:\App\Apps\yanshi'

def load(fn):
    return open(BASE + '\\' + fn, 'rb').read().decode('utf-8')

def save(fn, h):
    open(BASE + '\\' + fn, 'wb').write(h.encode('utf-8'))

def sub1(h, old, new, tag):
    n = h.count(old)
    if n == 0 and h.count(new) >= 1:
        print('  skip (already fixed):', tag)
        return h
    assert n == 1, 'sub1 %s: found %d' % (tag, n)
    return h.replace(old, new)

# ---------- 1) 邓稼先：卡片叠字 有有 ----------
fn = 'dengjiaxian-yangzhenning.html'
h = load(fn)
h = sub1(h, '是有方向、有有意识地前进的', '是有方向、有意识地前进的', fn)
save(fn, h); print('OK', fn)

# ---------- 2) 说和做：卡片叠字 是是 ----------
fn = 'shuohezuo-zangkejia.html'
h = load(fn)
h = sub1(h, '这仅是是闻一多先生的一个方面', '这仅是闻一多先生的一个方面', fn)
save(fn, h); print('OK', fn)

# ---------- 3) 最后一课：空转注释 ----------
fn = 'zuihouyike-dude.html'
h = load(fn)
old = '<span class="anno-word" data-note="这些鸽子">这些鸽子</span>'
new = '<span class="anno-word" data-note="以鸽子作比，暗指被强迫学德语的学生们，写出孩子的天真与亡国的悲愤">这些鸽子</span>'
h = sub1(h, old, new, fn + '/pigeon')
save(fn, h); print('OK', fn)

# ---------- 4) 叶圣陶：全文两处笔误 + 卡片补 5 处课文删节 ----------
fn = 'yeshengtaoxianshengersanshi-zhangzhongxing.html'
h = load(fn)
# 4a. 全文：郁达夫有才任情 -> 才任情（课文原文无"有"）
h = sub1(h, '郁达夫有才任情', '郁达夫才任情', fn + '/you')
# 4b. 全文：句号应在引号外（部分引用）
h = sub1(h, '惟德是辅。”', '惟德是辅”。', fn + '/punct')
# 4c. 卡片补回 5 处课文删节（锚点=课文前文，插入其后）
INS = [
    ('就应该有所谓白话指什么', '（如有孔乙己的白话，鲁迅的白话，北京市民的白话，等等）'),
    ('除了少数人、个别文体', '（如小说、戏剧里的对话）'),
    ('但更多的是来于认识', '（纵使是不很明确的）'),
    ('就必致付之一笑', '。这里为题目所限，不能牵涉过多，甚至挑起论辩'),
    ('细心体会，求速成办不到', '（多念像话的文）'),
]
for anchor, ins in INS:
    h = sub1(h, anchor, anchor + ins, fn + '/ins:' + ins[:12])
save(fn, h); print('OK', fn)

# ---------- 5) 太空一日：卡片小标题与课文一致 ----------
fn = 'taikongyiri-yangliwei.html'
h = load(fn)
old = '<div class="v-line">我<span class="anno-word" data-note="从高处往下看。瞰，读 kàn">俯瞰</span>到了什么</div>'
new = '<div class="v-line">我看到了什么</div>'
h = sub1(h, old, new, fn + '/heading')
save(fn, h); print('OK', fn)

# ---------- 6) 三个拼音文件名纠正（含 _list.json） ----------
RENAMES = [
    ('dengyzhoutaige-chenziang.html',  'dengyouzhoutaige-chenziang.html'),
    ('weixuanzelu-fuluosite.html',     'weixuanzedelu-fuluosite.html'),
    ('youshancun-luyou.html',          'youshanxicun-luyou.html'),
]
lp = r'D:\App\Apps\_list.json'
lj = open(lp, 'rb').read().decode('utf-8')
for old_fn, new_fn in RENAMES:
    src = os.path.join(BASE, old_fn)
    dst = os.path.join(BASE, new_fn)
    if os.path.exists(src):
        os.rename(src, dst)
        print('renamed', old_fn, '->', new_fn)
    elif os.path.exists(new_fn):
        print('skip rename (done):', new_fn)
    else:
        raise AssertionError('file missing: ' + old_fn)
    # _list.json 同步
    old_ref = './yanshi/' + old_fn
    new_ref = './yanshi/' + new_fn
    if old_ref in lj:
        assert lj.count(old_ref) == 1
        lj = lj.replace(old_ref, new_ref)
        print('  _list.json updated:', new_ref)
    elif new_ref in lj:
        print('  _list.json skip (done)')
    else:
        raise AssertionError('list ref not found: ' + old_ref)
open(lp, 'wb').write(lj.encode('utf-8'))
print('ALL FIXED')
