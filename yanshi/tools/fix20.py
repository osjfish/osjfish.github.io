# -*- coding: utf-8 -*-
"""修复并行会话 20 篇课件的审计问题：
1) 4 篇卡片区正文失真（手工 patch 衍文/错字/注释单位 + 机械回填 span 间丢失标点）
2) 周亚夫引号嵌套改外双内单（3 处）
3) 3 篇听写题叠词/双字词整体作答
修复全程以背诵区（fulltext，已核与教材一致）为权威，修完做全文流比对 + §5.4.1 自检。"""
import io, re, json, difflib

BASE = r"D:\App\Apps"

def rd(fn):
    return io.open(BASE + "\\" + fn, encoding="utf-8-sig").read()

def wr(fn, s):
    io.open(BASE + "\\" + fn, "w", encoding="utf-8-sig").write(s)

def bal(x, start):
    i, depth = start, 0
    while i < len(x):
        no, nc = x.find('<div', i), x.find('</div>', i)
        if nc == -1: return len(x)
        if no != -1 and no < nc: depth += 1; i = no + 4
        else:
            depth -= 1; i = nc + 6
            if depth == 0: return i
    return len(x)

norm = lambda x: re.sub(r'\s+', '', x)
PUNCT = set('，。；：？！、—…“”‘’·')

# ============ 1) 手工 patch（衍文 / 错字 / 注释单位 / 引号嵌套）============
PATCHES = {
 'hezhouji-weixueyi.html': [
  ('为字共三十<span class="anno-word" data-note="同“又”，用来连接整数和零数。有，同“又”；奇，零数">有奇</span>四。',
   '为字共三十<span class="anno-word" data-note="同“又”，用来连接整数和零数">有</span>四。', 1),
 ],
 'beimingyouyu-zhuangzi.html': [
  ('<span class="anno-word" data-note="天色深蓝。之，用于主谓之间">天之苍苍</span><span class="anno-word" data-note="深蓝色">苍苍</span>，',
   '<span class="anno-word" data-note="天色深蓝。苍苍，深蓝色；之，用于主谓之间">天之苍苍</span>，', 1),
 ],
 'yugongyishan-liezi.html': [
  ('<span class="anno-word" data-note="把……怎么样，对……怎么办">如……何</span>',
   '如<span class="anno-word" data-note="太行、王屋，二山名">太行、王屋</span><span class="anno-word" data-note="“如……何”，即“把太行、王屋怎么样”">何</span>', 1),
  ('<span class="anno-word" data-note="可以吗？乎，语气词">可乎</span>”。',
   '<span class="anno-word" data-note="可以吗？乎，语气词">可乎</span>”？', 1),
 ],
 'zhouyafujunxiliu-simaqian.html': [
  ('<span class="anno-word" data-note="对……说">谓……曰</span><span class="anno-word" data-note="跟随皇帝的车马人员。从属，跟随的；车骑，车马和骑兵">从属车骑</span>：',
   '<span class="anno-word" data-note="告诉，对……说">谓</span><span class="anno-word" data-note="跟随皇帝的车马人员。从属，跟随的；车骑，车马和骑兵">从属车骑</span><span class="anno-word" data-note="说">曰</span>：', 1),
  ('将军令曰：“军中闻将军令，不闻天子之诏。””', '将军令曰：‘军中闻将军令，不闻天子之诏。’”', 1),
  ('<span class="anno-word" data-note="说">曰</span>：“<span class="anno-word" data-note="军营之中">军中</span>',
   '<span class="anno-word" data-note="说">曰</span>：‘<span class="anno-word" data-note="军营之中">军中</span>', 1),
  ('<span class="anno-word" data-note="皇帝的命令。诏，皇帝发布的命令">天子之诏</span>。””',
   '<span class="anno-word" data-note="皇帝的命令。诏，皇帝发布的命令">天子之诏</span>。’”', 1),
  ('将军有命令说：“军营中只听将军的命令，不听皇帝的诏令。””',
   '将军有命令说：‘军营中只听将军的命令，不听皇帝的诏令。’”', 1),
 ],
}

for fn, plist in PATCHES.items():
    s = rd(fn)
    for old, new, cnt in plist:
        n = s.count(old)
        if n == 0 and cnt in (1, 2):
            print('  (already applied)', fn, old[:40])
            continue
        assert n == cnt, '%s patch hit %d (want %d): %s' % (fn, n, cnt, old[:60])
        s = s.replace(old, new)
    wr(fn, s)
    print('patched', fn)

# ============ 2) 机械回填 span 间丢失的标点 ============
def fix_punct(fn):
    s = rd(fn)
    st = s.find('<div id="fulltext"')
    F = norm(''.join(re.sub(r'<[^>]+>', '', x)
                     for x in re.findall(r'<div class="pl[^"]*">(.*?)</div>', s[st:bal(s, st)], re.S)))
    jl_st = s.find('<div class="verse-list" id="verseList">')
    jl = s[jl_st: s.find('</section>', jl_st)]
    vls = [(m.start(1), m.group(1)) for m in re.finditer(r'<div class="v-line">(.*?)</div></div>', jl, re.S)]
    cmap = []   # (vl_idx, pos_in_vl_html)
    C = ''
    for vi, (off, h) in enumerate(vls):
        i, in_tag = 0, False
        while i < len(h):
            c = h[i]
            if c == '<': in_tag = True
            elif c == '>': in_tag = False
            elif not in_tag and not c.isspace():
                cmap.append((vi, i)); C += c
            i += 1
    ins = {}  # (vl_idx, pos) -> str
    manual = []
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, C, F).get_opcodes():
        if op == 'insert':
            frag = F[b1:b2]
            if all(c in PUNCT for c in frag):
                if a1 < len(cmap):
                    vi, pos = cmap[a1]
                else:
                    vi, pos = cmap[-1][0], len(vls[cmap[-1][0]][1])
                ins[(vi, pos)] = ins.get((vi, pos), '') + frag
            else:
                manual.append(('insert', frag, C[max(0,a1-12):a1]))
        elif op != 'equal':
            manual.append((op, C[a1:a2][:24], F[b1:b2][:24]))
    # 应用插入（每个 v-line 内从后往前）
    new_vls = []
    by_vl = {}
    for (vi, pos), frag in ins.items():
        by_vl.setdefault(vi, []).append((pos, frag))
    for vi, (off, h) in enumerate(vls):
        for pos, frag in sorted(by_vl.get(vi, []), reverse=True):
            h = h[:pos] + frag + h[pos:]
        new_vls.append(h)
    # 重建 jl：以 v-line 开标签切分逐段替换
    parts = re.split(r'(<div class="v-line">)', jl)
    rebuilt, vi = [], 0
    for i, p in enumerate(parts):
        if p == '<div class="v-line">':
            rebuilt.append(p); continue
        # p 是 v-line 内容及其后文；把第一个 v-line 的内容替换为新内容
        old_h = vls[vi][1] if vi < len(vls) else None
        if old_h is not None and p.startswith(old_h):
            rebuilt.append(new_vls[vi] + p[len(old_h):])
            vi += 1
        else:
            rebuilt.append(p)
    assert vi == len(vls), 'rebuild mismatch: %d/%d' % (vi, len(vls))
    s = s[:jl_st] + ''.join(rebuilt) + s[s.find('</section>', jl_st):]
    wr(fn, s)
    print('punct-backfill', fn, 'inserts=%d manual=%d' % (len(ins), len(manual)))
    for m in manual: print('   MANUAL:', m)
    return len(ins)


# 手工 patch 二：对齐后遗留的两处
PATCH2 = [
 ('beimingyouyu-zhuangzi.html', '去以六月息者也”。', '去以六月息者也。”', 1),
 ('yugongyishan-liezi.html', '可乎</span>”？', '可乎</span>”？', 1),
]
for fn, old, new, cnt in PATCH2:
    s = rd(fn)
    n = s.count(old)
    if n == 0:
        print('  (already applied)', fn, old[:30]); continue
    assert n == cnt, '%s hit %d: %s' % (fn, n, old[:40])
    wr(fn, s.replace(old, new))
    print('patch2', fn, old[:30])

for fn in ['hezhouji-weixueyi.html', 'beimingyouyu-zhuangzi.html',
           'yugongyishan-liezi.html', 'zhouyafujunxiliu-simaqian.html']:
    fix_punct(fn)

# ============ 3) 听写题修复 ============
DICT_FIX = {
 'guduzhilv-caowenxuan.html': {
   '朦': None, '胧': None, '浩': None, '荡': None, '叠': None,
   'add': [
     {"w": "朦朦胧胧", "py": "méng méng lóng lóng", "q": "除了□□□□的树烟，就什么也没有了",
      "tip": "AABB叠词整体作答；朦、胧均为月字旁，勿写「蒙」「拢」"},
     {"w": "浩浩荡荡", "py": "hào hào dàng dàng", "q": "再面对这□□□□的芦苇",
      "tip": "「浩」氵旁加告，「荡」草字头加汤；叠词整体作答"},
     {"w": "重重叠叠", "py": "chóng chóng dié dié", "q": "一样的芦苇，一样□□□□无边无际",
      "tip": "「叠」为层叠，勿写「迭」（走之旁，更迭义）；叠词整体作答"},
   ]},
 'liusuo-acheng.html': {
   '兢': None, '吱': None, '哞': None,
   'add': [
     {"w": "兢兢", "py": "jīng jīng", "q": "我战战□□跨过去，近了，才看清那索",
      "tip": "「兢」两个「克」并排，读 jīng 勿读 jìn；叠词整体作答"},
     {"w": "吱吱", "py": "zhī zhī", "q": "那索在他们身下□□地响",
      "tip": "「吱」口字旁加支，拟声词；此处读 zhī 不读 zī"},
     {"w": "哞哞", "py": "mōu mōu", "q": "那牛□□地叫，四条腿蹬着地",
      "tip": "「哞」口字旁加牟，牛叫声，勿读 móu"},
   ]},
 'congbaicaoyuandaosanweishuwu-luxun.html': {
   '藤': None,
   'add': [
     {"w": "臃", "py": "yōng", "q": "何首乌有□肿的根",
      "tip": "「臃」月字旁（肉），臃肿即隆肿胀大；勿写「雍」「痈」"},
   ]},
}

for fn, spec in DICT_FIX.items():
    s = rd(fn)
    m = re.search(r'var DICT_WORDS = (\[[\s\S]*?\]);', s)
    words = json.loads(m.group(1))
    drop = [w for w in spec if w != 'add']
    add = spec['add']
    words = [w for w in words if w['w'] not in drop] + add
    new = 'var DICT_WORDS = ' + json.dumps(words, ensure_ascii=False) + ';'
    s = s[:m.start()] + new + s[m.end():]
    wr(fn, s)
    print('dict-fixed', fn, 'now %d items' % len(words))

# ============ 4) 自检 ============
print('\n===== 自检 =====')
CHECK = ['hezhouji-weixueyi.html', 'beimingyouyu-zhuangzi.html', 'yugongyishan-liezi.html',
         'zhouyafujunxiliu-simaqian.html', 'guduzhilv-caowenxuan.html', 'liusuo-acheng.html',
         'congbaicaoyuandaosanweishuwu-luxun.html']
allok = True
for fn in CHECK:
    s = rd(fn)
    st = s.find('<div id="fulltext"')
    F = norm(''.join(re.sub(r'<[^>]+>', '', x)
                     for x in re.findall(r'<div class="pl[^"]*">(.*?)</div>', s[st:bal(s, st)], re.S)))
    jl = s[s.find('<div class="verse-list" id="verseList">'): s.find('</section>', s.find('<div class="verse-list" id="verseList">'))]
    C = norm(''.join(re.sub(r'<span class="anno-word"[^>]*>|</span>|<br\s*/?>', '', m.group(1))
                     for m in re.finditer(r'<div class="v-line">(.*?)</div></div>', jl, re.S)))
    ok1 = C == F
    words = json.loads(re.search(r'var DICT_WORDS = (\[[\s\S]*?\]);', s).group(1))
    leak = [w['w'] for w in words if any(c in w['q'] for c in w['w'])]
    nbox = [w['w'] for w in words if w['q'].count('□') != len(w['w'])]
    npy = [w['w'] for w in words if len(w['py'].split()) != len(w['w']) and len(w['py'].split()) != 1]
    ok2 = not (leak or nbox or npy)
    print('%-44s stream=%s dict=%s' % (fn, 'OK' if ok1 else 'MISMATCH!',
          'OK' if ok2 else 'leak=%s nbox=%s npy=%s' % (leak, nbox, npy)))
    allok = allok and ok1 and ok2
    if not ok1:
        for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, C, F).get_opcodes():
            if op != 'equal':
                print('    ', op, repr(C[a1:a2][:20]), repr(F[b1:b2][:20]))
print('\nALL OK' if allok else '\nHAS ISSUES')
