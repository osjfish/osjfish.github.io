# -*- coding: utf-8 -*-
"""八上 24 篇课件批量深度审计"""
import re, json, os, html as htmllib, sys

BASE = r'D:\App\Apps\yanshi'
FILES = [
    ('消息二则·百万大军',  'renminjiefangjunbaiwandajunhengduchangjiang-maozedong.html'),
    ('消息二则·三十万大军','wosanwandajunshenglinanduchangjiang-maozedong.html'),
    ('首届诺贝尔奖颁发',  'shojienuobeierjiangbanfa-loutoushe.html'),
    ('"飞天"凌空',        'feitianlingkong-xiahaoran.html'),
    ('一着惊海天',        'yizhejinghaitian-cainianchi.html'),
    ('国行公祭',          'guohanggongjiweiyoushijieheping-zhongsheng.html'),
    ('回忆我的母亲',      'huiyiwodemuqin-zhude.html'),
    ('列夫·托尔斯泰',     'liefutuoersitai-ciweige.html'),
    ('美丽的颜色',        'meilideyanse-aifujuli.html'),
    ('野望',              'yewang-wangji.html'),
    ('黄鹤楼',            'huanghelou-cuihao.html'),
    ('渡荆门送别',        'dujingmensongbie-libai.html'),
    ('永久的生命',        'yongjiudeshengming-yanwenjing.html'),
    ('我为什么而活着',    'woweishimeerhuozhe-luosu.html'),
    ('昆明的雨',          'kunmingdeyu-wangzengqi.html'),
    ('中国石拱桥',        'zhongguoshigongqiao-maoyisheng.html'),
    ('苏州园林',          'suzhouyuanlin-yetaotao.html'),
    ('蝉',                'chan-fabuer.html'),
    ('梦回繁华',          'menghuifanhua-maoning.html'),
    ('得道多助，失道寡助','deduoduozhushidaoguazhu-mengzi.html'),
    ('富贵不能淫',        'fuguibunengyin-mengzi.html'),
    ('行路难',            'xinglunan-libai.html'),
    ('雁门太守行',        'yanmentaishouxing-lihe.html'),
    ('渔家傲',            'yujiaao-liqingzhao.html'),
]

FAMOUS = {
    'renminjiefangjunbaiwandajunhengduchangjiang-maozedong.html': ['冲破敌阵，横渡长江'],
    'wosanwandajunshenglinanduchangjiang-maozedong.html': ['渡江战斗于二十日午夜开始'],
    'shojienuobeierjiangbanfa-loutoushe.html': ['瑞典国王'],
    'feitianlingkong-xiahaoran.html': ['犹如被空气托住了'],
    'yizhejinghaitian-cainianchi.html': ['刀尖上的舞蹈'],
    'guohanggongjiweiyoushijieheping-zhongsheng.html': ['国行公祭，法立典章'],
    'huiyiwodemuqin-zhude.html': ['世界上最可宝贵的财产'],
    'liefutuoersitai-ciweige.html': ['胡子、眉毛、头发'],
    'meilideyanse-aifujuli.html': ['我真想知道它是什么颜色'],
    'yewang-wangji.html': ['树树皆秋色，山山唯落晖'],
    'huanghelou-cuihao.html': ['晴川历历汉阳树，芳草萋萋鹦鹉洲'],
    'dujingmensongbie-libai.html': ['山随平野尽，江入大荒流'],
    'yongjiudeshengming-yanwenjing.html': ['凋谢和不朽混为一体'],
    'woweishimeerhuozhe-luosu.html': ['对于爱情的渴望，对于知识的追求'],
    'kunmingdeyu-wangzengqi.html': ['我想念昆明的雨'],
    'zhongguoshigongqiao-maoyisheng.html': ['石拱桥的桥洞成弧形'],
    'suzhouyuanlin-yetaotao.html': ['务必使游览者无论站在哪个点上'],
    'chan-fabuer.html': ['四年黑暗中的苦工'],
    'menghuifanhua-maoning.html': ['清明上河图'],
    'deduoduozhushidaoguazhu-mengzi.html': ['天时不如地利，地利不如人和'],
    'fuguibunengyin-mengzi.html': ['富贵不能淫，贫贱不能移，威武不能屈'],
    'xinglunan-libai.html': ['长风破浪会有时，直挂云帆济沧海'],
    'yanmentaishouxing-lihe.html': ['黑云压城城欲摧，甲光向日金鳞开'],
    'yujiaao-liqingzhao.html': ['九万里风鹏正举'],
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

    if 'data-page-node-id' in h:
        fails.append('node-id pollution (%d)' % h.count('data-page-node-id'))

    nph = len(re.findall(r'\{LQ\}|\{RQ\}|\[\[', h))
    if nph:
        fails.append('leftover placeholders {LQ}/{RQ}/[[: %d' % nph)

    nspan = len(re.findall(r'data-note="[^"]*<span', h))
    if nspan:
        fails.append('nested span inside data-note: %d' % nspan)

    for i in REQ_IDS:
        if 'id="%s"' % i not in h:
            fails.append('missing id=%s' % i)
    for s in REQ_SECS:
        if 'id="%s"' % s not in h:
            warns.append('missing section id=%s' % s)

    mstart = re.search(r'<div[^>]*id="fulltext"[^>]*>', h)
    ft_lines = []
    if mstart:
        seg = h[mstart.end():]
        mscript = re.search(r'<script', seg)
        if mscript:
            seg = seg[:mscript.start()]
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

    vlines = re.findall(r'<div class="v-line">(.*?)</div>', h, re.S) or \
             re.findall(r'<div class="verse-text">(.*?)</div>', h, re.S)
    v_texts = [strip_py(strip_annos(v)) for v in vlines]
    v_all = ''.join(v_texts)

    for idx, vt in enumerate(v_texts):
        vt2 = strip_py(re.sub(r'[。！？；：，、]$', '', vt)); vt = strip_py(vt)
        if vt and vt not in ft_all and vt2 not in ft_all:
            fails.append('card[%d] not in fulltext: %s' % (idx+1, vt[:40]))

    for fl in ft_lines:
        fl2 = re.sub(r'[。！？；：，、]$', '', fl)
        if fl not in v_all and fl2 not in v_all:
            fails.append('fulltext line not covered by cards: %s' % fl[:40])

    body = re.sub(r'<script>.*?</script>', '', h[h.index('<body'):], flags=re.S)
    body = re.sub(r'<style>.*?</style>', '', body, flags=re.S)
    body = re.sub(r'<[^>]+>', '', body)
    sq = body.count('"')
    if sq:
        fails.append('straight double quotes in visible text: %d' % sq)

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

    annos = re.findall(r'<span class="anno-word" data-note="([^"]*)">([^<]*)</span>', h)
    for note, word in annos:
        if not note.strip():
            fails.append('empty anno: %s' % word)
        elif clean(note) == clean(word):
            fails.append('rotate anno: %s' % word)
    if '[[' in h:
        fails.append('leftover [[ marker')

    bvs = re.findall(r'bvid=([A-Za-z0-9]+)', h)
    for b in bvs:
        all_bvids.setdefault(b, []).append(fn)

    keys = set(re.findall(r"localStorage\.(?:get|set|remove)Item\('([^']+_fs)'", h))
    if not keys:
        fails.append('no _fs localStorage key')
    for k in keys:
        all_fskeys.setdefault(k, []).append(fn)

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
