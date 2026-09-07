# -*- coding: utf-8 -*-
"""八下 19 篇课件批量深度审计"""
import re, json, os, html as htmllib, sys

BASE = r'D:\App\Apps\yanshi'
FILES = [
    ('回延安',            'huiyanan-hejingzhi.html'),
    ('大自然的语言',      'dazirandeyuyan-zhukezhen.html'),
    ('恐龙无处不有',      'konglongwuchubuyou-aximofu.html'),
    ('被压扁的沙子',      'beiyabiandeshazi-aximofu.html'),
    ('大雁归来',          'dayanguilai-liaopode.html'),
    ('时间的脚印',        'shijiandejiaoyin-taoshilong.html'),
    ('关雎',              'guanju-shijing.html'),
    ('蒹葭',              'jianjia-shijing.html'),
    ('最后一次讲演',      'zuihouyicijiangyan-wenyiduo.html'),
    ('应有格物致知精神',  'yingyougewuzhizhijingshen-dingzhaozhong.html'),
    ('我一生中的重要抉择','woyishengzhongdezhongyaojueze-wangxuan.html'),
    ('庆祝奥林匹克运动复兴25周年','qingzhuaolinpikeyundongfuxing25zhounian-gubaidan.html'),
    ('壶口瀑布',          'hukoupubu-liangheng.html'),
    ('在长江源头各拉丹东','zaichangjiangyuantougeladandong-malihua.html'),
    ('登勃朗峰',          'dengbolangfeng-maketuweng.html'),
    ('一滴水经过丽江',    'yidishuijingguolijiang-alai.html'),
    ('庄子与惠子游于濠梁','zhuangziyuhuiziyouyuhaoliang-zhuangzi.html'),
    ('虽有嘉肴',          'suiyoujiayao-liji.html'),
    ('卖炭翁',            'maitanweng-baijuyi.html'),
]

FAMOUS = {
    'huiyanan-hejingzhi.html': ['几回回梦里回延安'],
    'dazirandeyuyan-zhukezhen.html': ['草长莺飞'],
    'konglongwuchubuyou-aximofu.html': ['不同科学领域之间是紧密相连的'],
    'beiyabiandeshazi-aximofu.html': ['斯石英'],
    'dayanguilai-liaopode.html': ['一只燕子的来临说明不了春天'],
    'shijiandejiaoyin-taoshilong.html': ['时间是没有脚的'],
    'guanju-shijing.html': ['关关雎鸠，在河之洲'],
    'jianjia-shijing.html': ['蒹葭苍苍，白露为霜'],
    'zuihouyicijiangyan-wenyiduo.html': ['我们不怕死，我们有牺牲的精神'],
    'yingyougewuzhizhijingshen-dingzhaozhong.html': ['真正的格物致知精神'],
    'woyishengzhongdezhongyaojueze-wangxuan.html': ['来扶植年轻人'],
    'qingzhuaolinpikeyundongfuxing25zhounian-gubaidan.html': ['自信'],
    'hukoupubu-liangheng.html': ['博大宽厚，柔中有刚'],
    'zaichangjiangyuantougeladandong-malihua.html': ['这一派奇美令人眩晕'],
    'dengbolangfeng-maketuweng.html': ['威严的穹顶'],
    'yidishuijingguolijiang-alai.html': ['我是一片雪'],
    'zhuangziyuhuiziyouyuhaoliang-zhuangzi.html': ['子非鱼，安知鱼之乐'],
    'suiyoujiayao-liji.html': ['教学相长'],
    'maitanweng-baijuyi.html': ['可怜身上衣正单，心忧炭贱愿天寒'],
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
