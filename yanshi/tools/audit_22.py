# -*- coding: utf-8 -*-
"""七上 22 篇课件批量深度审计"""
import re, json, os, html as htmllib, sys

BASE = r'D:\App\Apps\yanshi'
FILES = [
    ('雨的四季',      'yudesiji-liuzhanqiu.html'),
    ('金色花',        'jinsehua-taigeer.html'),
    ('荷叶·母亲',    'heyemuqin-bingxin.html'),
    ('咏雪',          'yongxue-shishuoxinyu.html'),
    ('陈太丘与友期',  'chentaiqiuyouqi-shishuoxinyu.html'),
    ('再塑生命的人',  'zaishengmingderen-hailunkailun.html'),
    ('窃读记',        'qieduji-linhaiyin.html'),
    ('《论语》十二章','lunyushierzhang-lunyu.html'),
    ('纪念白求恩',    'jinianbaiqiuen-maozedong.html'),
    ('植树的牧羊人',  'zhishuduyangren-rangqiaonuo.html'),
    ('在山的那边',    'zaishadenabian-wangjiaxin.html'),
    ('猫',            'mao-zhengzhenduo.html'),
    ('鸟',            'niao-liangshiqiu.html'),
    ('动物笑谈',      'dongwuxiaotan-kanglaodelunzi.html'),
    ('皇帝的新装',    'huangdindexinzhuang-antusheng.html'),
    ('天上的街市',    'tianshangdejiashi-guomoruo.html'),
    ('太阳船',        'taiyangchuan-wuwangyao.html'),
    ('女娲造人',      'nvwazaoren-yuanke.html'),
    ('赫耳墨斯和雕像者','heermosihediaoxiangzhe-yisuoyuyan.html'),
    ('蚊子和狮子',    'wenziheshizi-yisuoyuyan.html'),
    ('塞翁失马',      'saiwengshima-huainanzi.html'),
    ('杞人忧天',      'qirenyoutian-liezi.html'),
]

FAMOUS = {
    'yudesiji-liuzhanqiu.html': ['我喜欢雨，无论什么季节的雨，我都喜欢'],
    'jinsehua-taigeer.html': ['假如我变成了一朵金色花'],
    'heyemuqin-bingxin.html': ['心中的雨点来了，除了你，谁是我在无遮拦天空下的荫蔽'],
    'yongxue-shishuoxinyu.html': ['未若柳絮因风起'],
    'chentaiqiuyouqi-shishuoxinyu.html': ['陈太丘与友期行', '下车引之'],
    'zaishengmingderen-hailunkailun.html': ['莎莉文'],
    'qieduji-linhaiyin.html': ['窃读'],
    'lunyushierzhang-lunyu.html': ['学而时习之', '温故而知新', '三人行，必有我师焉'],
    'jinianbaiqiuen-maozedong.html': ['毫不利己专门利人', '对技术精益求精'],
    'zhishuduyangren-rangqiaonuo.html': ['他做到了只有上天才能做到的事'],
    'zaishadenabian-wangjiaxin.html': ['在山的那边，是海'],
    'mao-zhengzhenduo.html': ['结局总是失踪或死亡'],
    'niao-liangshiqiu.html': ['玲珑饱满'],
    'dongwuxiaotan-kanglaodelunzi.html': ['怪诞不经'],
    'huangdindexinzhuang-antusheng.html': ['愚蠢得不可救药'],
    'tianshangdejiashi-guomoruo.html': ['好像闪着无数的明星'],
    'taiyangchuan-wuwangyao.html': ['航线'],
    'nvwazaoren-yuanke.html': ['天地开辟以后'],
    'heermosihediaoxiangzhe-yisuoyuyan.html': ['想知道他在人间受到多大的尊重'],
    'wenziheshizi-yisuoyuyan.html': ['蚊子飞到狮子面前'],
    'saiwengshima-huainanzi.html': ['近塞上之人有善术者'],
    'qirenyoutian-liezi.html': ['杞国有人忧天地崩坠'],
}

REQ_IDS = ['btnAll','btnRecite','btnPrint','verseList','fulltext','topBtn',
           'annoPopup','dictate','mediaF1','mediaF2']
REQ_SECS = ['bg','jielu','app','acc','practice']

def clean(t):
    t = htmllib.unescape(t)
    return re.sub(r'\s+', '', t)

def strip_annos(t):
    # keep anno-word inner text, drop other tags
    t = re.sub(r'<span class="anno-word"[^>]*>(.*?)</span>', r'\1', t, flags=re.S)
    t = re.sub(r'<[^>]+>', '', t)
    return clean(t)

total_fail = total_warn = 0
all_bvids = {}
all_fskeys = {}

for title, fn in FILES:
    path = os.path.join(BASE, fn)
    h = open(path, encoding='utf-8').read()
    fails, warns = [], []

    # 0. node-id pollution
    if 'data-page-node-id' in h:
        fails.append('node-id pollution (%d)' % h.count('data-page-node-id'))

    # 0b. leftover template placeholders
    nph = len(re.findall(r'\{LQ\}|\{RQ\}|\[\[', h))
    if nph:
        fails.append('leftover placeholders {LQ}/{RQ}/[[: %d' % nph)

    # 0c. nested span inside data-note attribute (malformed HTML)
    nspan = len(re.findall(r'data-note="[^"]*<span', h))
    if nspan:
        fails.append('nested span inside data-note: %d' % nspan)

    # 1. required ids / sections
    for i in REQ_IDS:
        if 'id="%s"' % i not in h:
            fails.append('missing id=%s' % i)
    for s in REQ_SECS:
        if 'id="%s"' % s not in h:
            warns.append('missing section id=%s' % s)

    # 2. extract fulltext paragraphs (balanced: cut at next top-level boundary)
    mstart = re.search(r'<div id="fulltext"[^>]*>', h)
    ft_lines = []
    if mstart:
        seg = h[mstart.end():]
        mscript = re.search(r'<script', seg)
        if mscript:
            seg = seg[:mscript.start()]
        # cut at matching close: count div depth
        depth, cut = 1, None
        for m in re.finditer(r'<div\b|</div>', seg):
            depth += 1 if m.group(0).startswith('<div') else -1
            if depth == 0:
                cut = m.start()
                break
        if cut is not None:
            seg = seg[:cut]
        ft_raw = seg
        for part in re.split(r'<div class="pl">|<p[^>]*>|<br\s*/?>', ft_raw):
            part = re.sub(r'</p>|</div>', '', part)
            c = strip_annos(part)
            if c:
                ft_lines.append(c)
    else:
        fails.append('fulltext div not found')
    ft_all = ''.join(ft_lines)

    # 3. verses / v-lines (two templates: v-line | verse-text)
    vlines = re.findall(r'<div class="v-line">(.*?)</div>', h, re.S) or \
             re.findall(r'<div class="verse-text">(.*?)</div>', h, re.S)
    v_texts = [strip_annos(v) for v in vlines]
    v_all = ''.join(v_texts)

    # 3a. every v-line must appear in fulltext
    for idx, vt in enumerate(v_texts):
        vt2 = re.sub(r'[。！？；：，、]$', '', vt)
        if vt and vt not in ft_all and vt2 not in ft_all:
            fails.append('card[%d] not in fulltext: %s' % (idx+1, vt[:40]))

    # 3b. every fulltext paragraph must be covered by cards
    for fl in ft_lines:
        fl2 = re.sub(r'[。！？；：，、]$', '', fl)
        if fl not in v_all and fl2 not in v_all:
            fails.append('fulltext line not covered by cards: %s' % fl[:40])

    # 4. straight quotes in visible text (strip script/style, then tags)
    body = re.sub(r'<script>.*?</script>', '', h[h.index('<body'):], flags=re.S)
    body = re.sub(r'<style>.*?</style>', '', body, flags=re.S)
    body = re.sub(r'<[^>]+>', '', body)
    sq = body.count('"')
    if sq:
        fails.append('straight double quotes in visible text: %d' % sq)

    # 5. JSON banks
    mw = re.search(r'var DICT_WORDS = (\[.*?\]);', h, re.S)
    mn = re.search(r'var DICT_NOTES = (\[.*?\]);', h, re.S)
    words = notes = None
    try:
        if mw:
            words = json.loads(mw.group(1))
            for x in words:
                w, q = x['w'], x['q']
                if any(c in q for c in w):
                    fails.append('WORD leak: %s in %s' % (w, q[:30]))
                if q.count('□') != len(w):
                    fails.append('WORD box: %s (%d□ vs %d字)' % (w, q.count('□'), len(w)))
                py = x.get('py', '')
                n = len(py.split())
                if n != len(w) and n != 1:
                    fails.append('WORD py: %s (%d音节 vs %d字)' % (w, n, len(w)))
                tip = x.get('tip', '')
                if not tip or tip == w:
                    fails.append('WORD tip: %s' % w)
        if mn:
            notes = json.loads(mn.group(1))
            for x in notes:
                w, a, q = x['w'], x['a'], x['q']
                if a and a in q:
                    fails.append('NOTE leak: %s | %s' % (w, q[:30]))
                if w not in q:
                    warns.append('NOTE w not in q: %s' % w)
                if not a or a == w:
                    fails.append('NOTE empty/rotate: %s' % w)
    except Exception as e:
        fails.append('JSON parse: %s' % e)

    # 6. empty / rotation annotations
    annos = re.findall(r'<span class="anno-word" data-note="([^"]*)">([^<]*)</span>', h)
    for note, word in annos:
        if not note.strip():
            fails.append('empty anno: %s' % word)
        elif clean(note) == clean(word):
            fails.append('rotate anno: %s' % word)
    if '[[' in h:
        fails.append('leftover [[ marker')

    # 7. bvids
    bvs = re.findall(r'bvid=([A-Za-z0-9]+)', h)
    for b in bvs:
        all_bvids.setdefault(b, []).append(fn)

    # 8. localStorage key
    keys = set(re.findall(r"localStorage\.(?:get|set|remove)Item\('([^']+_fs)'", h))
    if not keys:
        fails.append('no _fs localStorage key')
    for k in keys:
        all_fskeys.setdefault(k, []).append(fn)

    # 9. famous lines (WARN only)
    for ref in FAMOUS.get(fn, []):
        r = clean(ref)
        if r not in ft_all:
            warns.append('famous line not in fulltext: %s' % ref[:30])

    total_fail += len(fails)
    total_warn += len(warns)
    status = 'FAIL' if fails else ('WARN' if warns else 'PASS')
    print('=== %s [%s] %s ===' % (title, status, fn))
    print('  cards=%d pl=%d anno=%d words=%s notes=%s size=%d bvids=%d fskey=%s'
          % (len(vlines), len(ft_lines), len(annos),
             len(words) if words is not None else '-', len(notes) if notes is not None else '-',
             len(h), len(bvs), ','.join(keys) or '-'))
    for f in fails: print('  FAIL: %s' % f)
    for w in warns: print('  WARN: %s' % w)

print('=' * 50)
print('bvid collisions:')
for b, fs in all_bvids.items():
    if len(fs) > 1:
        print('  %s -> %s' % (b, fs))
print('fskey collisions:')
for k, fs in all_fskeys.items():
    if len(fs) > 1:
        print('  %s -> %s' % (k, fs))
print('FAIL 总数 = %d  WARN 总数 = %d' % (total_fail, total_warn))
