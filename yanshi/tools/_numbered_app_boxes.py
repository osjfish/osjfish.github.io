# -*- coding: utf-8 -*-
"""把 app 区块中赏析性分点 box 统一成琵琶行「一、二、三」独立分 box 样式。

范围：h3 ∈ {艺术特色, 情感脉络, 画面层次, 记梦结构, 内容赏析} 的 box。
覆盖六种旧形态，全部拆为 N 个 <div class="box"><h3>一、标题</h3><p>正文</p></div>：
  Form D fame-card：box 内 <div class="fame"> 包 N 张 fame-card（f-line=标题，其余=正文）
  Form B 纯段落：  <p><b>标题</b>正文</p> ×N
  Form B2 圈号段落：<p><b>① 标题</b>正文</p> ×N
  Form E strong：  <p><strong>1. 标题。</strong>正文</p> ×N
  Form F 原编号：  <p><b>一、标题。</b>正文</p> ×N
  Form A 单段圈号：<p>① <b>标题</b>：正文<br>② …</p>
标题清洗：去首部已有编号（①/1./一、）、去尾部句读；正文原样保留。
人物形象/抒情主人公形象/论证类/逻辑推理等 box 不动（琵琶行原样即单 box 或语义分组）。
"""
import re, glob, os, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(DIR, '..')
CN = '一二三四五六七八九十'
TARGET_TITLES = {'艺术特色', '情感脉络', '画面层次', '记梦结构', '内容赏析'}
CIRCLED = '①②③④⑤⑥⑦⑧⑨⑩'
DRY = '--write' not in sys.argv

# 签名剔除集：标签、空白、以及解析/清洗中会增删的字符
STRIPSET = CIRCLED + CN + '、．.。：:，第幅层（）0123456789０１２３４５６７８９'

def sig(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\s+', '', s)
    for ch in STRIPSET:
        s = s.replace(ch, '')
    return s

def clean_title(t, body):
    """标题清洗：去首部已有编号、去尾部句读；正文开头的（…）：补语并入标题。
    返回 (新标题, 新正文)。"""
    t = t.strip()
    body = body.strip()
    m = re.match(r'^第[一二三四五六七八九十\d]+[幅层](（([^）]*)）)?$', t)
    if m:
        t = m.group(2) or t  # 第X幅（Y）→ Y；第X幅 → 原样兜底
    else:
        t = re.sub(r'^[①②③④⑤⑥⑦⑧⑨⑩\d一二三四五六七八九十]+\s*[、.．]?\s*', '', t)
        t = re.sub(r'[。．.]+$', '', t).strip() or t  # 清洗后为空则兜底原样
    bm = re.match(r'^（([^）]+)）\s*[：:]\s*', body)
    if bm and t:
        t = t + '（' + bm.group(1) + '）'
        body = body[bm.end():]
    return t, body.lstrip('：:').strip()

def balanced_div(s, start):
    """从 start 处的 <div 提取平衡块，返回 (html, end)"""
    depth = 0
    for mo in re.finditer(r'<div\b[^>]*>|</div>', s[start:]):
        depth += 1 if mo.group(0).startswith('<div') else -1
        if depth == 0:
            return s[start:start + mo.end()], start + mo.end()
    raise ValueError('unbalanced div')

def parse_fame_cards(body):
    """Form D：box 内容为单个 fame div 包 N 张 fame-card。返回 [(title, body_html)] 或 None"""
    mo = re.search(r'<div class="fame"[^>]*>', body)
    if not mo:
        return None
    fame, fame_end = balanced_div(body, mo.start())
    if body[:mo.start()].strip() or body[fame_end:].strip():
        return None  # fame 区外还有内容，交人工
    cards = []
    pos = 0
    inner = fame[re.match(r'<div class="fame"[^>]*>', fame).end():fame.rfind('</div>')]
    while True:
        mo = re.search(r'<div class="fame-card"[^>]*>', inner[pos:])
        if not mo:
            break
        card, card_end = balanced_div(inner, pos + mo.start())
        pos = card_end
        lm = re.search(r'<div class="f-line"[^>]*>(.*?)</div>', card, re.S)
        if not lm:
            return None
        title = lm.group(1)
        rest = card[re.search(r'<div class="f-line"[^>]*>.*?</div>', card, re.S).end():]
        rest = re.sub(r'\s*</div>\s*$', '', rest)  # 去 card 自身闭合
        cards.append((title, rest))
    return (cards, '') if len(cards) >= 2 else None

def parse_paras(body):
    """Form B/B2/E/F：连续 <p><b>|<strong>标题</b>|</strong>正文</p>；
    返回 (pts, intro)，intro 为开头可选引入句（如"全诗情感跌宕起伏，一波三折："）。"""
    for tag in ('b', 'strong'):
        pat = re.compile(r'<p>\s*<' + tag + r'[^>]*>(.*?)</' + tag + r'>(.*?)</p>', re.S)
        paras = pat.findall(body)
        if len(paras) >= 2:
            rest = pat.sub('', body).strip()
            intro = ''
            if rest:
                im = re.match(r'<p>([^<]*)</p>\s*', body, re.S)
                if im and pat.sub('', body[im.end():]).strip() == '':
                    intro = im.group(1).strip()
                    rest = ''
            if rest == '':
                return [(t, b) for (t, b) in paras], intro
    return None

def parse_circled(body):
    """Form A：单个 <p> 内圈号分点（圈号在 <b> 外）"""
    if not any(c in body for c in CIRCLED):
        return None
    pm = re.search(r'<p>(.*)</p>', body, re.S)
    if not pm:
        return None
    inner = pm.group(1)
    parts = re.split(r'([' + CIRCLED + r'])', inner)
    pts = []
    for i in range(1, len(parts) - 1, 2):
        seg = parts[i + 1]
        tm = re.match(r'\s*<b>(.*?)</b>(.*)', seg, re.S)
        if not tm:
            return None
        tb = re.sub(r'(<br\s*/?>)+\s*$', '', tm.group(2).strip()).strip()
        pts.append((tm.group(1), tb))
    if len(pts) >= 2 and re.sub(r'<[^>]+>', '', parts[0]).strip() == '':
        return pts, ''
    return None

def parse_box(title, body):
    """box h3 后内容 → ([(title, body_html)], intro) 或 None（box 自身闭合已由 rfind 剥离）"""
    body = body.strip()
    for fn in (parse_fame_cards, parse_paras, parse_circled):
        r = fn(body)
        if r and len(r[0]) >= 2:
            return r
    return None

def transform_file(path, report):
    t = re.sub(r' data-page-node-id="[^"]*"', '', open(path, encoding='utf-8').read())
    m = re.search(r'<section id="app"[^>]*>(.*?)<section id="acc"', t, re.S)
    if not m:
        return False
    app = m.group(1)
    changed, skipped = [], []

    # 逐个目标 box：定位 h3 → 平衡提取整个 box → 解析 → 生成替换
    result, pos, last = [], 0, 0
    out = []
    idx = 0
    spans = []  # (start, end, replacement)
    for mo in re.finditer(r'<div class="box"[^>]*>\s*<h3[^>]*>([^<]*)</h3>', app):
        title = mo.group(1).strip()
        if title not in TARGET_TITLES:
            continue
        try:
            box, box_end = balanced_div(app, mo.start())
        except ValueError:
            skipped.append(f'{os.path.basename(path)}: {title} div 不平衡')
            continue
        head = re.match(r'<div class="box"[^>]*>\s*<h3[^>]*>[^<]*</h3>', box, re.S)
        body_inner = box[head.end():box.rfind('</div>')]
        r = parse_box(title, body_inner)
        if not r or len(r[0]) < 2:
            skipped.append(f'{os.path.basename(path)}: {title} 解析失败(0点)')
            continue
        pts, intro = r
        gen_pts = []
        for i, (pt, pb) in enumerate(pts):
            nt, nb = clean_title(pt, pb)
            if i == 0 and intro:
                nb = intro + '</p><p>' + nb
            gen_pts.append((nt, nb))
        def wrap_p(nb):
            s = nb.strip()
            # 已自带 <p> 标签（fame-card 正文）则不重复包
            if s.startswith('<p>') or s.startswith('<p '):
                return s
            return f'<p>{s}</p>'
        boxes = '\n  '.join(
            f'<div class="box">\n    <h3>{CN[i]}、{nt}</h3>\n    {wrap_p(nb)}\n  </div>'
            for i, (nt, nb) in enumerate(gen_pts))
        # 局部内容保全断言（字符多重集：清洗/引言并入只改变顺序，不允许丢字）
        from collections import Counter
        assert Counter(sig(body_inner)) == Counter(sig(boxes)), f'内容保全断言失败: {path} {title}'
        spans.append((mo.start(), box_end, boxes))
        changed.append((title, len(pts)))
    if not changed:
        return False
    # 从后往前替换
    new_app = app
    for (s, e, rep) in sorted(spans, key=lambda x: -x[0]):
        new_app = new_app[:s] + rep + new_app[e:]
    # 断言：div 平衡差不变
    bal = lambda x: len(re.findall(r'<div\b', x)) - len(re.findall(r'</div>', x))
    assert bal(app) == bal(new_app), f'div 平衡变化: {path}'
    t = t[:m.start(1)] + new_app + t[m.end(1):]
    for sk in skipped:
        report.append(f'  [SKIP] {sk}')
    report.append(f'  [OK] {os.path.basename(path)}: ' + ', '.join(f'{ti}×{n}点' for ti, n in changed))
    if not DRY:
        open(path, 'w', encoding='utf-8').write(t)
    return True

report = []
files = 0
for path in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    if 'pipaxing' in os.path.basename(path):
        continue
    if transform_file(path, report):
        files += 1
print('\n'.join(report))
print(f'\n涉及文件：{files}（{"DRY-RUN 未写入" if DRY else "已写入"}）')
