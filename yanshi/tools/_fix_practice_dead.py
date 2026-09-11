# -*- coding: utf-8 -*-
"""修复 4 篇练习功能失效：
1) xinglunan / yanmentaishouxing / yujiaao：IIFE 缺听写+打印整段 JS，4 个按钮全死。
2) taikongyiri：遗留版练习（openDict/dictFs）与标准脚本冲突，缺 .ptools 与浮层元素 → 脚本 null 报错，连注释弹窗都挂。
"""
import re, io, sys

ROOT = r'D:\App\Apps\yanshi'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

REF = 'ailianshuo-zhoudunyi.html'
src_ref = open(ROOT + '/' + REF, encoding='utf-8').read()
i = src_ref.index('/* ---------- 听写题库 ---------- */')
j = src_ref.index('\n})();', i)
BLOCK = src_ref[i:j + 1]   # 听写 + 打印整段（含结尾换行）
print('标准块长度:', len(BLOCK), '含 btnPrint:', "btnPrint" in BLOCK)

TARGETS = ['xinglunan-libai.html', 'yanmentaishouxing-lihe.html', 'yujiaao-liqingzhao.html']
for fn in TARGETS:
    p = ROOT + '/' + fn
    s = open(p, encoding='utf-8').read()
    if 'practice .ptools button' in s:
        print(fn, '已有接线，跳过')
        continue
    # 定位 IIFE 结尾的 })();（可能带缩进，如 "  })();"）
    m = None
    for m in re.finditer(r'\n[ \t]*\}\)\(\);', s):
        pass
    if not m:
        print(fn, '未找到 IIFE 结尾，跳过')
        continue
    k = m.start()
    s2 = s[:k] + '\n' + BLOCK + s[k + 1:]
    open(p, 'w', encoding='utf-8').write(s2)
    print(fn, '已插入听写+打印 JS')

# ---- taikongyiri：遗留版 → 标准结构 ----
fn = 'taikongyiri-yangliwei.html'
p = ROOT + '/' + fn
s = open(p, encoding='utf-8').read()

PRACTICE_NEW = '''<section id="practice" class="sec">
    <div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>
    <div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>
    <div class="ptools">
      <button data-mode="word" data-rand="5">随机五组字形</button>
      <button data-mode="word" data-all="1">全部字形</button>
      <button data-mode="note" data-rand="5">随机五组词语</button>
      <button data-mode="note" data-all="1">全部词语</button>
    </div>
  </section>'''

OVERLAY_NEW = '''<div class="dictate" id="dictate" hidden>
  <div class="dictate-top">
    <span class="dictate-mode" id="dictMode">字形听写</span>
    <span class="dictate-progress" id="dictProgress">第 1 / 5 题</span>
    <button class="dictate-fs" id="dictFsMinus">A−</button><button class="dictate-fs" id="dictFsPlus">A+</button><button class="dictate-exit" id="dictExit">退出</button>
  </div>
  <div class="dictate-card">
    <div class="dictate-py" id="dictPy"></div>
    <div class="dictate-line" id="dictLine"></div>
    <div class="dictate-hint" id="dictHint"></div>
    <div class="dictate-ans" id="dictAnsBox" hidden>
      <div class="dictate-word" id="dictWord"></div>
      <div class="dictate-tip" id="dictTip"></div>
    </div>
  </div>
  <div class="dictate-actions">
    <button id="dictPrev">上一题</button>
    <button class="primary" id="dictShow">显示答案</button>
    <button id="dictNext">下一题</button>
  </div>
</div>'''

# 1) 替换练习区
a = s.index('<section id="practice"')
b = s.index('</section>', a) + len('</section>')
s = s[:a] + PRACTICE_NEW + s[b:]
# 2) 替换遗留浮层（<div id="dictate" ...> 到 topBtn 前）
a = s.index('<div id="dictate"')
b = s.index('<button id="topBtn"', a)
s = s[:a] + OVERLAY_NEW + '\n' + s[b:]
open(p, 'w', encoding='utf-8').write(s)
print(fn, '练习区+浮层已换为标准结构')
