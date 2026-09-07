# -*- coding: utf-8 -*-
"""八下 19 篇体检·修复：{LQ}/{RQ} 占位符 + 回转注释"""
import os

BASE = r'D:\App\Apps\yanshi'
FILES = [
    'dazirandeyuyan-zhukezhen.html',
    'konglongwuchubuyou-aximofu.html',
    'beiyabiandeshazi-aximofu.html',
    'dayanguilai-liaopode.html',
    'shijiandejiaoyin-taoshilong.html',
    'yingyougewuzhizhijingshen-dingzhaozhong.html',
    'woyishengzhongdezhongyaojueze-wangxuan.html',
]

def fix_lrq(fn):
    p = os.path.join(BASE, fn)
    h = open(p, 'rb').read().decode('utf-8')
    n = h.count('{LQ}')
    out = []
    depth = 0  # 未闭合的双引号 “ 深度
    i = 0
    while i < len(h):
        if h.startswith('{LQ}', i):
            out.append('\u2018' if depth > 0 else '\u201c')
            i += 4
        elif h.startswith('{RQ}', i):
            out.append('\u2019' if depth > 0 else '\u201d')
            i += 4
        else:
            c = h[i]
            if c == '\u201c':
                depth += 1
            elif c == '\u201d':
                depth = max(0, depth - 1)
            out.append(c)
            i += 1
    h2 = ''.join(out)
    assert '{LQ}' not in h2 and '{RQ}' not in h2
    open(p, 'wb').write(h2.encode('utf-8'))
    print('LRQ OK', fn, '(%d pairs)' % n)

def rep(fn, old, new, cnt=1):
    p = os.path.join(BASE, fn)
    h = open(p, 'rb').read().decode('utf-8')
    c = h.count(old)
    assert c == cnt, 'ASSERT %s count=%d expect=%d: %r' % (fn, c, cnt, old[:40])
    h = h.replace(old, new)
    open(p, 'wb').write(h.encode('utf-8'))
    print('REP OK', fn, old[:20])

for f in FILES:
    fix_lrq(f)

# 回转注释修正
rep('zhuangziyuhuiziyouyuhaoliang-zhuangzi.html',
    '<span class="anno-word" data-note="鱼">鱼</span>',
    '<span class="anno-word" data-note="指鱼类">鱼</span>')
rep('zhuangziyuhuiziyouyuhaoliang-zhuangzi.html',
    '<span class="anno-word" data-note="问我">问我</span>',
    '<span class="anno-word" data-note="向我发问（怎么知道鱼快乐）">问我</span>')
rep('maitanweng-baijuyi.html',
    '<span class="anno-word" data-note="身上">身上</span>',
    '<span class="anno-word" data-note="指自己穿用">身上</span>')

print('ALL DONE')
