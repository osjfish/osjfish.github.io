# -*- coding: utf-8 -*-
"""替换gen_huangdindexinzhuang.py的代码区（从# ================= 生成 =================开始）"""
path = r"D:\App\Apps\yanshi\tools\gen_huangdindexinzhuang.py"
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find marker line
marker_idx = None
for i, line in enumerate(lines):
    if '================= 生成' in line:
        marker_idx = i
        break

print(f"Marker at line {marker_idx + 1}")
# Keep data section (before marker)
data_section = ''.join(lines[:marker_idx])

# Correct generator code
code_section = r'''# ================= 生成 =================
def annotate(text, notes):
    n = len(text)
    occ = [False] * n
    spans = []
    terms = []
    for word, note in notes:
        m = re.match(r"^(.*?)[\uff08(]([^\uff09)]*)[\uff09)]$", word)
        if m:
            w0 = m.group(1)
            py = m.group(2)
            note = "\uff08" + py + "\uff09" + note
        else:
            w0 = word
        terms.append((w0, note))
    for w0, note in sorted(terms, key=lambda x: -len(x[0])):
        if w0 not in text:
            continue
        start = 0
        while True:
            i = text.find(w0, start)
            if i == -1:
                break
            if not any(occ[i:i + len(w0)]):
                spans.append((i, i + len(w0), w0, note))
                for k in range(i, i + len(w0)):
                    occ[k] = True
            start = i + len(w0)
    spans.sort()
    out, pos = [], 0
    for s, e, w, nt in spans:
        out.append(text[pos:s])
        nt_esc = nt.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
        out.append('<span class="anno-word" data-note="%s">%s</span>' % (nt_esc, w))
        pos = e
    out.append(text[pos:])
    return "".join(out)

def esc(t):
    return htmlmod.escape(t, quote=True)

jielu = []
fulltext = []
for (pnum, ptitle, prange, pover, verses) in VERSES:
    jielu.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>'
                 % (esc(pnum), esc(ptitle), esc(prange)))
    jielu.append('      <div class="part-overview">%s</div>' % esc(pover))
    for (no, text, gk, sf, notes) in verses:
        fulltext.append('    <div class="pl">%s</div>' % esc(text))
        jielu.append('      <div class="verse" id="l%d" data-i="%d">' % (no, no - 1))
        jielu.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>'
                     % (no, annotate(text, notes)))
        jielu.append('        <details class="v-more">')
        jielu.append('          <summary>\u5185\u5bb9 \u00b7 \u624b\u6cd5</summary>')
        jielu.append('          <div class="d-body">')
        jielu.append('            <div class="v-sec"><b class="v-label">\u5185\u5bb9\u6982\u62ec</b>')
        jielu.append('              <div class="v-trans">%s</div>' % esc(gk))
        jielu.append('            </div>')
        jielu.append('            <div class="v-sec"><b class="v-label">\u624b\u6cd5\u5206\u6790</b>')
        jielu.append('              <div class="d-body"><p>%s</p></div>' % esc(sf))
        jielu.append('            </div>')
        jielu.append('          </div>')
        jielu.append('        </details>')
        jielu.append('      </div>')
    jielu.append('')

jielu = "\n".join(jielu)
fulltext = "\n".join(fulltext)

lead_html = "\n".join('    <p>%s</p>' % esc(p) for p in LEAD)
author_html = "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px;color:var(--ink2)\"" if i else "", esc(p))
                        for i, p in enumerate(AUTHOR))
bg_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' %
    (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:8px\"" if i else "", esc(par))
                           for i, par in enumerate(paras)))
    for (title, paras) in BG)
media_html = "".join(
    '      <div class="media">\n        <h4>%s</h4>\n        <iframe id="%s" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>\n        <a href="%s" target="_blank" rel="noopener">\u5728 B \u7ad9\u6253\u5f00\u539f\u89c6\u9891</a><button class="fsbtn" data-target="%s">\u5168\u5c4f\u64ad\u653e</button>\n      </div>'
    % (esc(title), fid, bvid, esc(title), url, fid)
    for (title, bvid, url, fid) in VIDEOS)

app_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n    <div class="fame">\n%s\n    </div>\n  </div>\n' %
    (esc(title), "\n".join(
        '      <div class="fame-card">\n        <div class="f-line">%s</div>\n        <p>%s</p>\n      </div>' %
        (esc(ft), esc(pc)) for (ft, pc) in items if title != "\u4e3b\u9898\u601d\u60f3"))
    for (title, items) in APP if title != "\u4e3b\u9898\u601d\u60f3")

theme_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' %
    (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px\"" if i else "", esc(pc))
                           for i, (ft, pc) in enumerate(items)))
    for (title, items) in APP if title == "\u4e3b\u9898\u601d\u60f3")

acc_html = "".join(
    '  <div class="box">\n    <div class="acc-cat">\n      <h3>%s</h3>\n%s\n    </div>\n  </div>\n' %
    (esc(title), "\n".join('      <div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>'
                           % (esc(w), esc(d)) for (w, d) in items))
    for (title, items) in ACC)

hero = '<header class="hero">\n  <div class="hero-side">%s</div>\n  <h1 class="hero-title">%s</h1>\n</header>' % (H, TITLE)

nav = '''<nav class="nav">
  <div class="nav-in">
    <a href="#bg">\u80cc\u666f</a>
    <a href="#jielu">\u89e3\u8bfb</a>
    <a href="#app">\u8d4f\u6790</a>
    <a href="#acc">\u79ef\u7d2f</a>
    <a href="#practice">\u7ec3\u4e60</a>
    <div class="tool">
      <select id="fsSel" class="fs-sel" title="\u6b63\u6587\u5b57\u4f53\u5927\u5c0f">
        <option value="100">100%</option>
        <option value="150">150%</option>
        <option value="200">200%</option>
        <option value="250">250%</option>
        <option value="300">300%</option>
      </select>
      <button id="btnAll">\u5c55\u5f00</button>
      <button id="btnRecite">\u80cc\u8bf5</button>
      <button id="btnPrint">\u6253\u5370</button>
    </div>
  </div>
</nav>'''

main = '''<main class="wrap">
<section id="bg" class="sec">
  <div class="sec-head"><h2>\u80cc \u666f</h2><span class="no">\u4f5c\u8005 \u00b7 \u65f6\u4ee3 \u00b7 \u7f18\u8d77</span></div>
  <div class="lead">
%s
  </div>
  <div class="box">
    <h3>\u4f5c\u8005\u7b80\u4ecb</h3>
%s
  </div>
%s  <div class="box media-box">
    <h3>\u89c6\u542c</h3>
    <div class="media-grid">
%s
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>\u89e3 \u8bfb</h2><span class="no">\u9010\u6bb5 \u00b7 \u8bcd\u8bed \u00b7 \u624b\u6cd5</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">\u663e\u793a\u5168\u90e8</button>
  <div id="fulltext" class="poem" style="display:none">
%s
  </div>
  <div class="verse-list" id="verseList">
%s
  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>\u8d4f \u6790</h2><span class="no">\u4eba\u7269 \u00b7 \u827a\u672f \u00b7 \u540d\u53e5</span></div>
%s
%s</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>\u79ef \u7d2f</h2><span class="no">\u8bcd\u8bed \u00b7 \u5b57\u97f3 \u00b7 \u4fee\u8f9e \u00b7 \u5199\u6cd5 \u00b7 \u6587\u5316</span></div>
%s</section>

<div class="divider"></div>
<section id="practice" class="sec">
    <div class="sec-head"><h2>\u7ec3 \u4e60</h2><span class="no">\u5168\u5c4f\u542c\u5199</span></div>
    <div class="sec-sub">\u70b9\u51fb\u6309\u94ae\u8fdb\u5165\u5168\u5c4f\u542c\u5199\u6a21\u5f0f\uff0c\u53ef\u6309 A\u2212 / A+ \u8c03\u8282\u5b57\u4f53\u5927\u5c0f\u3002</div>
    <div class="ptools">
      <button data-mode="word" data-rand="5">\u968f\u673a\u4e94\u7ec4\u5b57\u5f62</button>
      <button data-mode="word" data-all="1">\u5168\u90e8\u5b57\u5f62</button>
      <button data-mode="note" data-rand="5">\u968f\u673a\u4e94\u7ec4\u8bcd\u8bed</button>
      <button data-mode="note" data-all="1">\u5168\u90e8\u8bcd\u8bed</button>
    </div>
  </section>

<footer>
  <div class="kai">\u300a\u7687\u5e1d\u7684\u65b0\u88c5\u300b</div>
  <div>\u5b89\u5f92\u751f \u00b7 \u4e39\u9ea6 \u00b7 \u9009\u81ea\u300a\u5b89\u5f92\u751f\u7ae5\u8bdd\u548c\u6545\u4e8b\u9009\u300b</div>
  <div>\u53f6\u541b\u5065 \u8bd1</div>
</footer>
</main>''' % (lead_html, author_html, bg_html, media_html, fulltext, jielu, app_html, theme_html, acc_html)

tail = '''<button class="top-btn" id="topBtn" title="\u56de\u5230\u9876\u90e8">\u2191</button>
<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>
<div class="dictate" id="dictate" hidden>
  <div class="dictate-top">
    <span class="dictate-mode" id="dictMode">\u5b57\u5f62\u542c\u5199</span>
    <span class="dictate-progress" id="dictProgress">\u7b2c 1 / 5 \u9898</span>
    <button class="dictate-fs" id="dictFsMinus">A\u2212</button>
    <button class="dictate-fs" id="dictFsPlus">A+</button>
    <button class="dictate-exit" id="dictExit">\u9000\u51fa</button>
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
    <button id="dictPrev">\u4e0a\u4e00\u9898</button>
    <button class="primary" id="dictShow">\u663e\u793a\u7b54\u6848</button>
    <button id="dictNext">\u4e0b\u4e00\u9898</button>
  </div>
</div>'''

dict_js = ("var DICT_WORDS = %s;\nvar DICT_NOTES = %s;\n"
           % (json.dumps(DICT_WORDS, ensure_ascii=False),
              json.dumps(DICT_NOTES, ensure_ascii=False)))

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>\u300a\u7687\u5e1d\u7684\u65b0\u88c5\u300b\u5b89\u5f92\u751f</title>
<style>%s</style>
</head>
<body data-fs="100">

%s

%s

%s

%s

<script>
%s
</script>
<script>
%s</script>

</body>
</html>''' % (css, hero, nav, main, tail, main_js, dict_js)

open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, len(html), "chars")
print("verses:", sum(len(v[4]) for v in VERSES))
print("word dict:", len(DICT_WORDS), "note dict:", len(DICT_NOTES))
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(data_section + code_section)

print("File rewritten successfully")
