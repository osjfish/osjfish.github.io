# -*- coding: utf-8 -*-
"""九上 14 篇课件批量深度审计"""
import re, json, os, html as htmllib, sys

BASE = r'D:\App\Apps\yanshi'
FILES = [
    ('我爱这土地',            'woaizhetudi-aiqing.html'),
    ('乡愁',                  'xiangchou-yuguangzhong.html'),
    ('你是人间的四月天',      'nishirenjiandesiyuetian-linhuiyin.html'),
    ('我看',                  'wokan-mudan.html'),
    ('就英法联军远征中国致巴特勒上尉的信','jiuyingfalianjunyuanzhengzhongguozhibateleishangweidexin-yuguo.html'),
    ('论教养',                'lunjiaoyang-lihachiaofu.html'),
    ('精神的三间小屋',        'jingshendesanjianxiaowu-bishumin.html'),
    ('酬乐天扬州初逢席上见赠','chouletianyangzhouchufengxishangjianzeng-liuyuxi.html'),
    ('水调歌头',              'shuidiaogetou-sushi.html'),
    ('怀疑与学问',            'huaiyiyuxuewen-gujiegang.html'),
    ('谈创造性思维',          'tanchuangzaoxingsiwei-luojiafeiyinge.html'),
    ('创造宣言',              'chuangzaoxuanyan-taoxingzhi.html'),
    ('三顾茅庐',              'sangumaolu-luoguanzhong.html'),
    ('刘姥姥进大观园',        'liulaolaojindaguanyuan-caoxueqin.html'),
]

FAMOUS = {
    'woaizhetudi-aiqing.html': ['为什么我的眼里常含泪水'],
    'xiangchou-yuguangzhong.html': ['乡愁是一枚小小的邮票'],
    'nishirenjiandesiyuetian-linhuiyin.html': ['一树一树的花开'],
    'wokan-mudan.html': ['向晚的春风'],
    'jiuyingfalianjunyuanzhengzhongguozhibateleishangweidexin-yuguo.html': ['有一个世界奇迹'],
    'lunjiaoyang-lihachiaofu.html': ['良好的教养'],
    'jingshendesanjianxiaowu-bishumin.html': ['盛着我们的爱和恨'],
    'chouletianyangzhouchufengxishangjianzeng-liuyuxi.html': ['沉舟侧畔千帆过，病树前头万木春'],
    'shuidiaogetou-sushi.html': ['但愿人长久，千里共婵娟'],
    'huaiyiyuxuewen-gujiegang.html': ['学则须疑'],
    'tanchuangzaoxingsiwei-luojiafeiyinge.html': ['由于看图形的角度不同，四种答案全都正确'],
    'chuangzaoxuanyan-taoxingzhi.html': ['处处是创造之地，天天是创造之时，人人是创造之人'],
    'sangumaolu-luoguanzhong.html': ['汉室倾颓，奸臣窃命'],
    'liulaolaojindaguanyuan-caoxueqin.html': ['老刘，老刘，食量大似牛'],
}

REQ_IDS = ['btnAll','btnRecite','btnPrint','verseList','fulltext','topBtn',
           'annoPopup','dictate','mediaF1','mediaF2']
REQ_SECS = ['bg','jielu','app','acc','practice']

# 允许"卡片区不覆盖"的 fulltext 行（书信落款等非授课文本）
EXTRA_FT_OK = {
    'jiuyingfalianjunyuanzhengzhongguozhibateleishangweidexin-yuguo.html':
        ['维克多·雨果', '1861年11月25日于高城居'],
}

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
headtail = {}

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
        for part in re.split(r'<div[^>]*class="pl"[^>]*>|<p[^>]*>|<br\s*/?>', ft_raw):
            part = re.sub(r'</p>|</div>', '', part)
            c = strip_annos(part)
            if c:
                ft_lines.append(c)
    else:
        fails.append('fulltext div not found')
    ft_all = ''.join(ft_lines)

    # 供原文比对用：首2行+末2行
    if ft_lines:
        headtail[fn] = ft_lines[:2] + ['……'] + ft_lines[-2:]

    vlines = re.findall(r'<div[^>]*class="v-line"[^>]*>(.*?)</div>', h, re.S) or \
             re.findall(r'<div[^>]*class="verse-text"[^>]*>(.*?)</div>', h, re.S)
    v_texts = [strip_py(strip_annos(v)) for v in vlines]
    v_all = ''.join(v_texts)

    for idx, vt in enumerate(v_texts):
        vt2 = strip_py(re.sub(r'[。！？；：，、]$', '', vt)); vt = strip_py(vt)
        if vt and vt not in ft_all and vt2 not in ft_all:
            fails.append('card[%d] not in fulltext: %s' % (idx+1, vt[:40]))

    for fl in ft_lines:
        ok_extra = any(clean(e) in fl for e in EXTRA_FT_OK.get(fn, []))
        if ok_extra:
            continue
        fl_c = fl.strip('“”')
        fl_c2 = re.sub(r'[。！？；：，、]$', '', fl_c)
        if fl_c not in v_all and fl_c2 not in v_all:
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

print('=' * 50)
print('fulltext head/tail（供与部编版原文比对）:')
for fn, lines in headtail.items():
    print('--- %s' % fn)
    for l in lines:
        print('   %s' % (l[:60] + ('…' if len(l) > 60 else '')))
