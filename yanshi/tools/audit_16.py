# -*- coding: utf-8 -*-
"""七下 16 篇课件批量深度审计"""
import re, json, os, html as htmllib, sys

BASE = r'D:\App\Apps\yanshi'
FILES = [
    ('邓稼先',        'dengjiaxian-yangzhenning.html'),
    ('说和做',        'shuohezuo-zangkejia.html'),
    ('黄河颂',        'huanghesong-guangweiran.html'),
    ('最后一课',      'zuihouyike-dude.html'),
    ('土地的誓言',    'tudideshiyan-duanmuhongliang.html'),
    ('叶圣陶先生二三事','yeshengtaoxianshengersanshi-zhangzhongxing.html'),
    ('梅岭三章',      'meilingsanzhang-chenyi.html'),
    ('最苦与最乐',    'zuikuyuzuile-liangqichao.html'),
    ('一棵小桃树',    'yikexiaotaoshu-jiapingwa.html'),
    ('假如生活欺骗了你','jiarushenghuoqipianleni-puxijin.html'),
    ('未选择的路',    'weixuanzedelu-fuluosite.html'),
    ('登幽州台歌',    'dengyouzhoutaige-chenziang.html'),
    ('伟大的悲剧',    'weidadebeiju-ciweige.html'),
    ('太空一日',      'taikongyiri-yangliwei.html'),
    ('带上她的眼睛',  'daishangtadeyanjing-liucixin.html'),
    ('游山西村',      'youshanxicun-luyou.html'),
]

FAMOUS = {
    'dengjiaxian-yangzhenning.html': ['长期以来鲜为人知的科学家'],
    'shuohezuo-zangkejia.html': ['人家说了再做，我是做了再说'],
    'huanghesong-guangweiran.html': ['你是中华民族的摇篮'],
    'zuihouyike-dude.html': ['亡了国当了奴隶的人民'],
    'tudideshiyan-duanmuhongliang.html': ['我无时无刻不听见她呼唤我的名字'],
    'yeshengtaoxianshengersanshi-zhangzhongxing.html': ['躬行君子，则吾未之有得'],
    'meilingsanzhang-chenyi.html': ['此去泉台招旧部，旌旗十万斩阎罗'],
    'zuikuyuzuile-liangqichao.html': ['人生什么事最苦呢'],
    'yikexiaotaoshu-jiapingwa.html': ['我的小桃树'],
    'jiarushenghuoqipianleni-puxijin.html': ['不要悲伤，不要心急'],
    'weixuanzedelu-fuluosite.html': ['但我却选了另外一条路'],
    'dengyouzhoutaige-chenziang.html': ['前不见古人，后不见来者'],
    'weidadebeiju-ciweige.html': ['变得无比高尚'],
    'taikongyiri-yangliwei.html': ['我以为自己要牺牲了'],
    'daishangtadeyanjing-liucixin.html': ['再带一双眼睛去'],
    'youshanxicun-luyou.html': ['山重水复疑无路，柳暗花明又一村'],
}

REQ_IDS = ['btnAll','btnRecite','btnPrint','verseList','fulltext','topBtn',
           'annoPopup','dictate','mediaF1','mediaF2']
REQ_SECS = ['bg','jielu','app','acc','practice']

def clean(t):
    t = htmllib.unescape(t)
    return re.sub(r'\s+', '', t)

def strip_py(s):
    return re.sub(r'[（(][a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+[）)]', '', s)

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
    mstart = re.search(r'<div[^>]*id="fulltext"[^>]*>', h)
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
        ft_raw = re.sub(r'<span class="no">\d+</span>', '', ft_raw)
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
    v_texts = [strip_py(strip_annos(v)) for v in vlines]
    v_all = ''.join(v_texts)

    # 3a. every v-line must appear in fulltext
    for idx, vt in enumerate(v_texts):
        vt2 = strip_py(re.sub(r'[。！？；：，、]$', '', vt)); vt = strip_py(vt)
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
