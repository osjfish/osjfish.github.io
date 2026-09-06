# -*- coding: utf-8 -*-
"""通用课件生成引擎 —— 复用《背影》课件的 CSS / JS 框架，按模式装配内容。
文言模式：解读卡片为「译文 · 赏析」（含可选 tags）。
现代文模式：解读卡片为「内容 · 手法」（内容概括 + 手法分析）。
"""
import json, re, html, io, os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beiying-zhuziqing.html')


def load_framework(old_key, new_key):
    """抽取框架 CSS / JS，并把 localStorage key 换成新篇目的。"""
    src = io.open(SRC, encoding='utf-8-sig').read()
    CSS = src[src.index('<style>') + 7: src.index('</style>')]
    s0 = src.index('<script>')
    JS = src[s0 + 8: src.index('</script>', s0)]
    JS = JS.replace(old_key, new_key)
    return CSS, JS


def annotate(text):
    """将 [[词|注释]] 标记转成可点击注释 span。"""
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def build_verses_modern(PARTS, S):
    """S 元素: (部分索引, 原文[带标记], 内容概括, 手法分析)"""
    out, idx = [], 0
    for pi, part in enumerate(PARTS):
        out.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>'
                   % (part[0], part[1], part[2]))
        out.append('      <div class="part-overview">%s</div>' % part[3])
        for (p, txt, gai, shou) in S:
            if p != pi:
                continue
            idx += 1
            out.append('      <div class="verse" id="l%d" data-i="%d">' % (idx, idx - 1))
            out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx, annotate(txt)))
            out.append('        <details class="v-more">')
            out.append('          <summary>内容 · 手法</summary>')
            out.append('          <div class="d-body">')
            out.append('            <div class="v-sec"><b class="v-label">内容概括</b>')
            out.append('              <div class="v-trans">%s</div>' % gai)
            out.append('            </div>')
            out.append('            <div class="v-sec"><b class="v-label">手法分析</b>')
            out.append('              <div class="d-body"><p>%s</p></div>' % shou)
            out.append('            </div>')
            out.append('          </div>')
            out.append('        </details>')
            out.append('      </div>')
    return '\n'.join(out), idx


def build_verses_classic(PARTS, S):
    """S 元素: (部分索引, 原文[带标记], 译文, 赏析, [标签列表])"""
    out, idx = [], 0
    for pi, part in enumerate(PARTS):
        out.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>'
                   % (part[0], part[1], part[2]))
        out.append('      <div class="part-overview">%s</div>' % part[3])
        for (p, txt, yi, shang, tags) in S:
            if p != pi:
                continue
            idx += 1
            out.append('      <div class="verse" id="l%d" data-i="%d">' % (idx, idx - 1))
            out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx, annotate(txt)))
            out.append('        <details class="v-more">')
            out.append('          <summary>译文 · 赏析</summary>')
            out.append('          <div class="d-body">')
            out.append('            <div class="v-sec"><b class="v-label">译　文</b>')
            out.append('              <div class="v-trans">%s</div>' % yi)
            out.append('            </div>')
            out.append('            <div class="v-sec"><b class="v-label">赏　析</b>')
            out.append('              <div class="d-body"><p>%s</p></div>' % shang)
            if tags:
                out.append('              <div class="tags">%s</div>' % ''.join('<span>%s</span>' % t for t in tags))
            out.append('            </div>')
            out.append('          </div>')
            out.append('        </details>')
            out.append('      </div>')
    return '\n'.join(out), idx


# 以下哨兵在 render() 中替换为真实内容
_SKELETON = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@</title>
<style>
@@CSS@@
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">@@HERO_SIDE@@</div>
  <h1 class="hero-title">@@HERO_TITLE@@</h1>
</header>

<nav class="nav">
  <div class="nav-in">
    <a href="#bg">背景</a>
    <a href="#jielu">解读</a>
    <a href="#app">赏析</a>
    <a href="#acc">积累</a>
    <a href="#practice">练习</a>
    <div class="tool">
      <select id="fsSel" class="fs-sel" title="正文字体大小">
        <option value="100">100%</option>
        <option value="150">150%</option>
        <option value="200">200%</option>
        <option value="250">250%</option>
        <option value="300">300%</option>
      </select>
      <button id="btnAll">展开</button>
      <button id="btnRecite">背诵</button>
      <button id="btnPrint">打印</button>
    </div>
  </div>
</nav>

<main class="wrap">
@@BG@@

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 词语 · 手法</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
@@FULLTEXT@@
  </div>
  <div class="verse-list" id="verseList">
@@VERSES@@
  </div>
</section>

<div class="divider"></div>
@@APP@@

<div class="divider"></div>
@@ACC@@

<div class="divider"></div>
<section id="practice" class="sec">
    <div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>
    <div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>
    <div class="ptools">
      <button data-mode="word" data-rand="5">随机五组字形</button>
      <button data-mode="word" data-all="1">全部字形</button>
      <button data-mode="note" data-rand="5">随机五组词语</button>
      <button data-mode="note" data-all="1">全部词语</button>
    </div>
  </section>

<footer>
  <div class="kai">@@FOOTER_TITLE@@</div>
  <div>@@FOOTER_LINE@@</div>
</footer>
</main>

<button class="top-btn" id="topBtn" title="回到顶部">↑</button>
<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>
<div class="dictate" id="dictate" hidden>
  <div class="dictate-top">
    <span class="dictate-mode" id="dictMode">字形听写</span>
    <span class="dictate-progress" id="dictProgress">第 1 / 5 题</span>
    <button class="dictate-fs" id="dictFsMinus">A−</button>
    <button class="dictate-fs" id="dictFsPlus">A+</button>
    <button class="dictate-exit" id="dictExit">退出</button>
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
</div>
<script>
@@JS@@
</script>
<script>
var DICT_WORDS = @@WORDS@@;
var DICT_NOTES = @@NOTES@@;
</script>

</body>
</html>
'''


def render(meta, bg, app, acc, fulltext_list, verses_html, words, notes, css, js):
    full_html = '\n'.join('    <div class="pl">%s</div>' % p for p in fulltext_list)
    h = _SKELETON
    h = h.replace('@@TITLE@@', meta['title'])
    h = h.replace('@@HERO_SIDE@@', meta['hero_side'])
    h = h.replace('@@HERO_TITLE@@', meta['hero_title'])
    h = h.replace('@@BG@@', bg)
    h = h.replace('@@FULLTEXT@@', full_html)
    h = h.replace('@@VERSES@@', verses_html)
    h = h.replace('@@APP@@', app)
    h = h.replace('@@ACC@@', acc)
    h = h.replace('@@FOOTER_TITLE@@', meta['footer_title'])
    h = h.replace('@@FOOTER_LINE@@', meta['footer_line'])
    h = h.replace('@@CSS@@', css)
    h = h.replace('@@JS@@', js)
    h = h.replace('@@WORDS@@', json.dumps(words, ensure_ascii=False))
    h = h.replace('@@NOTES@@', json.dumps(notes, ensure_ascii=False))
    return h
