# -*- coding: utf-8 -*-
"""五篇自选课件全面体检：内容一致性 / 听写库 / 结构 / 引号 / 视频 / JSON / key 唯一性。"""
import io, re, os, sys, json, glob

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import data_taohuayuanji as M1
import data_zuiwengtingji as M2
import data_chun as M3
import data_zitengluopubu as M4
import data_denglong as M5

MODS = [
    ('桃花源记', M1, 'classic'),
    ('醉翁亭记', M2, 'classic'),
    ('春', M3, 'modern'),
    ('紫藤萝瀑布', M4, 'modern'),
    ('灯笼', M5, 'modern'),
]

QCHARS = '“”"‘’\'「」『』'

def norm(s):
    if not s:
        return ''
    return re.sub(r'[\s%s\u3000]' % QCHARS, '', s)

def plain(s):
    return re.sub(r'\[\[([^|\]]+)\|[^\]]+\]\]', r'\1', s or '')

FAIL, WARN, INFO = {}, {}, {}
def add(d, name, msg):
    d.setdefault(name, []).append(msg)

# ---------- beiying 拼音字符集基准 ----------
BY = io.open(os.path.join(ROOT, 'beiying-zhuziqing.html'), encoding='utf-8-sig').read()
BY_PYSET = set()
_m = re.search(r'var DICT_WORDS = (\[.*?\]);', BY, re.S)
if _m:
    try:
        for _w in json.loads(_m.group(1)):
            BY_PYSET.update(c for c in _w.get('py', '') if not c.isspace())
    except Exception as e:
        INFO['_global'] = ['beiying DICT_WORDS 解析失败: %s' % e]

# ---------- 全库 localStorage key 扫描 ----------
KEYMAP = {}
for f in glob.glob(os.path.join(ROOT, '*.html')):
    try:
        t = io.open(f, encoding='utf-8-sig').read()
    except Exception:
        continue
    ks = set(re.findall(r"'([A-Za-z0-9_]+_fs)'", t))
    if ks:
        KEYMAP[os.path.basename(f)] = ks

# ---------- 名句基准 ----------
FAMOUS = {
    '桃花源记': [
        '晋太元中，武陵人捕鱼为业。', '缘溪行，忘路之远近。',
        '忽逢桃花林，夹岸数百步，中无杂树，芳草鲜美，落英缤纷。',
        '渔人甚异之，复前行，欲穷其林。', '林尽水源，便得一山，山有小口，仿佛若有光。',
        '便舍船，从口入。初极狭，才通人。', '土地平旷，屋舍俨然，有良田、美池、桑竹之属。',
        '阡陌交通，鸡犬相闻。', '其中往来种作，男女衣着，悉如外人。',
        '黄发垂髫，并怡然自乐。', '见渔人，乃大惊，问所从来。具答之。',
        '便要还家，设酒杀鸡作食。', '自云先世避秦时乱，率妻子邑人来此绝境，不复出焉。',
        '问今是何世，乃不知有汉，无论魏晋。', '此人一一为具言所闻，皆叹惋。',
        '余人各复延至其家，皆出酒食。', '停数日，辞去。',
        '此中人语云：不足为外人道也。', '既出，得其船，便扶向路，处处志之。',
        '太守即遣人随其往，寻向所志，遂迷，不复得路。',
        '南阳刘子骥，高尚士也，闻之，欣然规往。', '未果，寻病终。后遂无问津者。',
    ],
    '醉翁亭记': [
        '环滁皆山也。', '其西南诸峰，林壑尤美。', '望之蔚然而深秀者，琅琊也。',
        '山行六七里，渐闻水声潺潺，而泻出于两峰之间者，酿泉也。',
        '峰回路转，有亭翼然临于泉上者，醉翁亭也。',
        '作亭者谁？山之僧智仙也。名之者谁？太守自谓也。',
        '醉翁之意不在酒，在乎山水之间也。', '山水之乐，得之心而寓之酒也。',
        '若夫日出而林霏开，云归而岩穴暝，晦明变化者，山间之朝暮也。',
        '野芳发而幽香，佳木秀而繁阴，风霜高洁，水落而石出者，山间之四时也。',
        '临溪而渔，溪深而鱼肥，酿泉为酒，泉香而酒洌。',
        '山肴野蔌，杂然而前陈者，太守宴也。',
        '宴酣之乐，非丝非竹，射者中，弈者胜，觥筹交错，起坐而喧哗者，众宾欢也。',
        '苍颜白发，颓然乎其间者，太守醉也。',
        '已而夕阳在山，人影散乱，太守归而宾客从也。',
        '树林阴翳，鸣声上下，游人去而禽鸟乐也。',
        '人知从太守游而乐，而不知太守之乐其乐也。',
        '醉能同其乐，醒能述以文者，太守也。太守谓谁？庐陵欧阳修也。',
        '伛偻提携，往来而不绝者，滁人游也。',
    ],
    '春': [
        '盼望着，盼望着，东风来了，春天的脚步近了。',
        '一切都像刚睡醒的样子，欣欣然张开了眼。',
        '山朗润起来了，水涨起来了，太阳的脸红起来了。',
        '小草偷偷地从土里钻出来，嫩嫩的，绿绿的。',
        '桃树、杏树、梨树，你不让我，我不让你，都开满了花赶趟儿。',
        '红的像火，粉的像霞，白的像雪。',
        '野花遍地是：杂样儿，有名字的，没名字的，散在草丛里，像眼睛，像星星，还眨呀眨的。',
        '吹面不寒杨柳风，不错的，像母亲的手抚摸着你。',
        '鸟儿将巢安在繁花嫩叶当中，高兴起来了，呼朋引伴地卖弄清脆的喉咙，唱出宛转的曲子，跟轻风流水应和着。',
        '牛背上牧童的短笛，这时候也成天在嘹亮地响。',
        '雨是最寻常的，一下就是三两天。可别恼。',
        '看，像牛毛，像花针，像细丝，密密地斜织着，人家屋顶上全笼着一层薄烟。',
        '树叶儿却绿得发亮，小草儿也青得逼你的眼。',
        '傍晚时候，上灯了，一点点黄晕的光，烘托出一片安静而和平的夜。',
        '春天像刚落地的娃娃，从头到脚都是新的，它生长着。',
        '春天像小姑娘，花枝招展的，笑着，走着。',
        '春天像健壮的青年，有铁一般的胳膊和腰脚，领着我们上前去。',
    ],
    '紫藤萝瀑布': [
        '我不由得停住了脚步。',
        '从未见过开得这样盛的藤萝，只见一片辉煌的淡紫色，像一条瀑布，从空中垂下，不见其发端，也不见其终极。',
        '只是深深浅浅的紫，仿佛在流动，在欢笑，在不停地生长。',
        '紫色的大条幅上，泛着点点银光，就像迸溅的水花。',
        '每一朵盛开的花就像是一个小小的张满了的帆，帆下带着尖底的舱。',
        '又像一个忍俊不禁的笑容，就要绽开似的。',
        '这里除了光彩，还有淡淡的芳香，香气似乎也是浅紫色的，梦幻一般轻轻地笼罩着我。',
        '忽然记起十多年前家门外也曾有过一大株紫藤萝。',
        '花和人都会遇到各种各样的不幸，但是生命的长河是无止境的。',
        '在这浅紫色的光辉和浅紫色的芳香中，我不觉加快了脚步。',
    ],
    '灯笼': [
        '小孩子喜欢火，喜欢亮光，却仿佛是天性。',
        '提起灯笼，就会想起三家村的犬吠，村中老头呵狗的声音。',
        '真的，灯笼的缘结得太多了，记忆的网里挤着的就都是。',
        '路上黑，打了灯笼去吧。',
        '雪夜驰马，荒郊店宿，每每令人忘路之远近。',
        '村犬遥遥向灯笼吠了，认得了是主人，近前来却又大摇其尾巴。',
        '最壮是塞外点兵，吹角连营，夜深星阑时候，将军在挑灯看剑。',
        '你听，正萧萧班马鸣也，我愿就是那灯笼下的马前卒。',
        '唉，壮，于今灯笼又不够了。应该数火把，数探海灯，数燎原的一把烈火！',
    ],
}

BG_KEYS = {
    '桃花源记': ['陶渊明', '东晋', '浔阳'],
    '醉翁亭记': ['欧阳修', '北宋', '唐宋八大家', '醉翁', '滁'],
    '春': ['朱自清', '1898', '散文'],
    '紫藤萝瀑布': ['宗璞', '冯友兰', '散文'],
    '灯笼': ['吴伯箫', '散文'],
}

DUMP = []   # BG/APP/ACC 原文摘出供人工复核
ALL_BVID = {}

for name, mod, mode in MODS:
    print('=' * 70)
    print('【%s】mode=%s' % (name, mode))
    html = io.open(mod.OUT, encoding='utf-8').read()
    FT = norm(''.join(mod.FULLTEXT))

    # ---- 1. 基础结构 ----
    if '@@' in html:
        add(FAIL, name, 'HTML 残留 @@ 占位符')
    if mod.OLD_KEY in html:
        add(FAIL, name, '旧 key %s 未替换干净' % mod.OLD_KEY)
    if mod.NEW_KEY not in html:
        add(FAIL, name, '新 key %s 不在 HTML 中' % mod.NEW_KEY)
    keys_here = KEYMAP.get(os.path.basename(mod.OUT), set())
    for f2, ks in KEYMAP.items():
        if f2 != os.path.basename(mod.OUT) and mod.NEW_KEY in ks:
            add(FAIL, name, 'localStorage key %s 与 %s 冲突' % (mod.NEW_KEY, f2))
    ids = re.findall(r'id="([^"]+)"', html)
    dup_ids = set(i for i in ids if ids.count(i) > 1)
    if dup_ids:
        add(FAIL, name, 'HTML 重复 id: %s' % sorted(dup_ids)[:5])
    m = re.search(r'<title>(.*?)</title>', html)
    if not m or m.group(1) != mod.META['title']:
        add(FAIL, name, 'title 标签与 META.title 不一致')
    if re.search(r'<meta charset="UTF-8">', html) is None:
        add(FAIL, name, '缺 charset 声明')
    if html.count('class="pl"') != len(mod.FULLTEXT):
        add(FAIL, name, '全文行数 %d != FULLTEXT %d' % (html.count('class="pl"'), len(mod.FULLTEXT)))
    if html.count('class="verse"') != len(mod.S):
        add(FAIL, name, 'verse 卡数 %d != S %d' % (html.count('class="verse"'), len(mod.S)))
    if html.count('class="part-head"') != len(mod.PARTS) or html.count('class="part-overview"') != len(mod.PARTS):
        add(FAIL, name, 'part-head/overview 数与 PARTS %d 不符' % len(mod.PARTS))
    lno = [int(x) for x in re.findall(r'id="l(\d+)"', html)]
    if lno != list(range(1, len(mod.S) + 1)):
        add(FAIL, name, 'verse id 序列异常')
    dno = [int(x) for x in re.findall(r'data-i="(\d+)"', html)]
    if dno != list(range(0, len(mod.S))):
        add(FAIL, name, 'data-i 序列异常')
    # 模式标签
    if mode == 'modern':
        if '内容概括' not in html or '手法分析' not in html:
            add(FAIL, name, '现代文标签缺失')
        if '译　文' in html:
            add(FAIL, name, '现代文课件出现文言「译文」标签')
    else:
        if '译　文' not in html or '赏　析' not in html:
            add(FAIL, name, '文言标签缺失')
        if '内容概括' in html:
            add(FAIL, name, '文言课件出现现代文「内容概括」标签')
    # ACC 标签
    if mode == 'modern' and '文言现象' in html:
        add(FAIL, name, '现代文课件出现「文言现象」')
    if mode == 'classic' and '文言现象' not in html:
        add(WARN, name, '文言课件未见「文言现象」块')

    # ---- 2. 原文完整性：名句抽查（容许句尾标点差异）----
    def has_line(ref):
        r = norm(re.sub(r'[。！？；]$', '', ref))
        return r in FT or norm(ref) in FT
    miss = [s for s in FAMOUS.get(name, []) if not has_line(s)]
    if miss:
        add(FAIL, name, '名句缺失 %d 句: %s' % (len(miss), miss[0][:30]))
    else:
        INFO.setdefault(name, []).append('名句抽查 %d 句全部命中' % len(FAMOUS[name]))

    # ---- 3. 解读卡片文本 vs 全文一致性 ----
    for i, s in enumerate(mod.S):
        txt = plain(s[1])
        n = norm(txt)
        if n and n not in FT:
            add(FAIL, name, '卡片%d 文本不在全文中: %s…' % (i + 1, txt[:24]))
    # 覆盖率（全文被卡片覆盖的比例）
    cover = [False] * len(FT)
    seen_txt = set()
    for s in mod.S:
        n = norm(plain(s[1]))
        if not n:
            continue
        if n in seen_txt:
            add(WARN, name, '卡片文本重复: %s…' % n[:20])
        seen_txt.add(n)
        start = 0
        while True:
            k = FT.find(n, start)
            if k < 0:
                break
            for j in range(k, min(k + len(n), len(FT))):
                cover[j] = True
            start = k + 1
    gaps = []
    j = 0
    while j < len(cover):
        if not cover[j]:
            k = j
            while k < len(cover) and not cover[k]:
                k += 1
            if k - j >= 6:  # 忽略零星标点级碎片
                gaps.append(FT[j:k][:30])
            j = k
        else:
            j += 1
    if gaps:
        add(WARN, name, '全文有 %d 处未被卡片覆盖: %s' % (len(gaps), ' | '.join(gaps[:3])))
    else:
        INFO.setdefault(name, []).append('全文 100%% 被卡片覆盖（FT %d 字）' % len(FT))

    # ---- 4. 引号配对与直角引号（先剥标签再查，属性引号不算）----
    def strip_tags(s):
        return re.sub(r'<[^>]+>', '', s or '')
    for label, seg in (('BG', getattr(mod, 'BG', '')), ('APP', getattr(mod, 'APP', '')),
                       ('ACC', getattr(mod, 'ACC', '')), ('FULLTEXT', ''.join(mod.FULLTEXT))):
        seg = strip_tags(seg)
        q1, q2 = seg.count('“'), seg.count('”')
        if q1 != q2:
            add(FAIL, name, '%s 中文引号不配对：%d vs %d' % (label, q1, q2))
        sq = seg.count('"')
        if sq:
            add(FAIL, name, '%s 含 %d 个半角直引号，应为中文引号' % (label, sq))
    for i, s in enumerate(mod.S):
        seg = ''.join(str(x) for x in s[1:])
        if seg.count('“') != seg.count('”'):
            add(FAIL, name, '卡片%d 中文引号不配对' % (i + 1))
        if '"' in plain(s[1]):
            add(FAIL, name, '卡片%d 原文含半角直引号' % (i + 1))
    q1, q2 = html.count('“'), html.count('”')
    if q1 != q2:
        add(WARN, name, '整页引号不配对 %d vs %d（可能来自 JS 数据）' % (q1, q2))

    # ---- 5. 视频 iframe ----
    ifr = re.findall(r'<iframe[^>]*?src="([^"]+)"[^>]*?>', getattr(mod, 'BG', ''))
    if len(ifr) != 2:
        add(FAIL, name, 'BG 视频数 %d != 2' % len(ifr))
    bvids = []
    for src in ifr:
        bm = re.match(r'https?://player\.bilibili\.com/player\.html\?bvid=(BV[0-9A-Za-z]+)', src)
        if not bm:
            add(FAIL, name, 'iframe src 格式异常: %s' % src[:60])
        else:
            bvids.append(bm.group(1))
        if 'autoplay=0' not in src:
            add(WARN, name, 'iframe 未显式 autoplay=0: %s' % src[:60])
    if len(set(bvids)) != len(bvids):
        add(FAIL, name, '两个视频 bvid 相同')
    for b in bvids:
        ALL_BVID.setdefault(b, []).append(name)
    if 'mediaF1' not in getattr(mod, 'BG', '') or 'mediaF2' not in getattr(mod, 'BG', ''):
        add(WARN, name, 'BG 缺 mediaF1/mediaF2 id')

    # ---- 6. 听写库 WORDS ----
    ws = [d['w'] for d in mod.DICT_WORDS]
    if len(set(ws)) != len(ws):
        add(FAIL, name, 'WORDS 重复: %s' % sorted(set(w for w in ws if ws.count(w) > 1)))
    for d in mod.DICT_WORDS:
        w, py, q = d.get('w', ''), d.get('py', ''), d.get('q', '')
        tip = d.get('tip', '')
        if not w or not py or not q:
            add(FAIL, name, 'WORDS 字段缺失: %s' % d)
            continue
        if not tip:
            add(FAIL, name, 'WORDS「%s」缺 tip' % w)
        if w in q:
            add(FAIL, name, 'WORDS「%s」整词泄题: %s' % (w, q[:24]))
        elif len(w) > 1:
            char_leak = [c for c in w if c in q]
            if char_leak:
                add(WARN, name, 'WORDS「%s」多字答案但例句含单字 %s: %s' % (w, char_leak, q[:24]))
        runs = re.findall(r'□+', q)
        if len(runs) != 1 or len(runs[0]) != len(w):
            add(FAIL, name, 'WORDS「%s」□ 不为单段且长度不符: %s' % (w, q[:24]))
        if len(py.split()) != len(w):
            add(FAIL, name, 'WORDS「%s」音节数 %d != 字数 %d' % (w, len(py.split()), len(w)))
        if re.search(r'[^a-zāáǎàēéěèīíǐìōóǒòūúǔùüǖǘǚǜ\s]', py):
            add(FAIL, name, 'WORDS「%s」拼音含异常字符: %s' % (w, py))
        if norm(w) not in FT:
            add(FAIL, name, 'WORDS「%s」不在课文中（疑似杜撰）' % w)
        recon = q.replace('□' * len(w), w, 1) if '□' * len(w) in q else None
        if recon is None or norm(recon) not in FT:
            add(FAIL, name, 'WORDS「%s」例句还原后不在课文: %s' % (w, q[:28]))

    # ---- 7. 听写库 NOTES ----
    ns = [d['w'] for d in mod.DICT_NOTES]
    if len(set(ns)) != len(ns):
        add(FAIL, name, 'NOTES 重复: %s' % sorted(set(w for w in ns if ns.count(w) > 1)))
    for d in mod.DICT_NOTES:
        w, a, q = d.get('w', ''), d.get('a', ''), d.get('q', '')
        if not w or not a or not q:
            add(FAIL, name, 'NOTES 字段缺失: %s' % d)
            continue
        if a in q:
            add(FAIL, name, 'NOTES「%s」释义泄入例句' % w)
        if w not in q:
            add(WARN, name, 'NOTES「%s」词未出现在其例句中: %s' % (w, q[:24]))
        if norm(w) not in FT:
            add(FAIL, name, 'NOTES「%s」不在课文中（疑似杜撰）' % w)
        if norm(q) not in FT:
            add(WARN, name, 'NOTES「%s」例句非课文原句: %s' % (w, q[:28]))

    # ---- 8. 注释质量 ----
    annos = re.findall(r'<span class="anno-word" data-note="([^"]*)">([^<]*)</span>', html)
    if mode == 'modern':
        short = [(w, n) for n, w in annos if len(n) < 2]
        if short:
            add(WARN, name, '超短注释(<2字): %s' % short[:6])
    INFO.setdefault(name, []).append('注释 %d 处' % len(annos))

    # ---- 9. 背景区事实关键词 ----
    bg = getattr(mod, 'BG', '')
    missk = [k for k in BG_KEYS.get(name, []) if k not in bg]
    if missk:
        add(WARN, name, 'BG 缺事实关键词: %s' % missk)

    # ---- 10. 卡片内容充实度 ----
    for i, s in enumerate(mod.S):
        if mode == 'modern':
            gai, shou = s[2], s[3]
        else:
            gai, shou = s[2], s[3]
        if len(norm(gai)) < 4:
            add(WARN, name, '卡片%d 内容概括过短' % (i + 1))
        if len(norm(shou)) < 12:
            add(WARN, name, '卡片%d 手法/赏析过短: %s' % (i + 1, str(shou)[:30]))
    for p in mod.PARTS:
        if len(norm(p[3])) < 10:
            add(WARN, name, '部分「%s」overview 过短' % p[1])

    # ---- 11. HTML 内嵌 JSON 可解析且计数一致 ----
    m1 = re.search(r'var DICT_WORDS\s*=\s*(\[.*?\]);\s*var DICT_NOTES', html, re.S)
    m2 = re.search(r'var DICT_NOTES\s*=\s*(\[.*?\]);', html, re.S)
    try:
        hw = json.loads(m1.group(1)) if m1 else []
        hn = json.loads(m2.group(1)) if m2 else []
        if len(hw) != len(mod.DICT_WORDS):
            add(FAIL, name, 'HTML WORDS %d != 模块 %d' % (len(hw), len(mod.DICT_WORDS)))
        if len(hn) != len(mod.DICT_NOTES):
            add(FAIL, name, 'HTML NOTES %d != 模块 %d' % (len(hn), len(mod.DICT_NOTES)))
    except Exception as e:
        add(FAIL, name, 'HTML 内嵌 JSON 解析失败: %s' % e)

    INFO.setdefault(name, []).append('文件 %dKB / 段落 %d / 卡片 %d / 部分 %d'
                                     % (os.path.getsize(mod.OUT) // 1024, len(mod.FULLTEXT), len(mod.S), len(mod.PARTS)))

    # ---- 12. 摘出 BG/APP/ACC 供人工复核 ----
    DUMP.append('\n' + '#' * 30 + ' %s BG ' % name + '#' * 30 + '\n' + re.sub(r'<[^>]+>', '', getattr(mod, 'BG', '')))
    DUMP.append('\n' + '#' * 30 + ' %s APP ' % name + '#' * 30 + '\n' + re.sub(r'<[^>]+>', '', getattr(mod, 'APP', '')))
    DUMP.append('\n' + '#' * 30 + ' %s ACC ' % name + '#' * 30 + '\n' + re.sub(r'<[^>]+>', '', getattr(mod, 'ACC', '')))

# ---------- _list.json ----------
print('=' * 70)
print('【_list.json】')
try:
    lj = json.load(io.open(os.path.join(ROOT, '_list.json'), encoding='utf-8'))
    ents = lj if isinstance(lj, list) else lj.get('apps', [])
    names = [e.get('name') for e in ents]
    paths = [e.get('path') for e in ents]
    dups = sorted(set(n for n in names if names.count(n) > 1))
    if dups:
        add(FAIL, '_list', '重复条目: %s' % dups)
    for e in ents:
        p = os.path.join(ROOT, e.get('path', '').lstrip('./'))
        if not os.path.exists(p):
            add(FAIL, '_list', '路径不存在: %s' % e.get('path'))
    for nm in ['《桃花源记》', '《醉翁亭记》', '《春》', '《紫藤萝瀑布》', '《灯笼》']:
        if nm not in names:
            add(FAIL, '_list', '缺条目 %s' % nm)
    INFO.setdefault('_list', []).append('共 %d 条' % len(ents))
except Exception as e:
    add(FAIL, '_list', 'JSON 解析失败: %s' % e)

# ---------- 视频跨课件撞车 ----------
for b, files in ALL_BVID.items():
    if len(files) > 1:
        add(WARN, '_global', 'bvid %s 被多篇复用: %s' % (b, files))

# ---------- 汇总 ----------
print()
print('================ 汇总 ================')
allfail = 0
for src in (FAIL, WARN):
    for k in sorted(set(list(FAIL.keys()) + list(WARN.keys()))):
        pass
for name in sorted(set(list(FAIL.keys()) + list(WARN.keys()) + list(INFO.keys()))):
    for x in FAIL.get(name, []):
        print('FAIL [%s] %s' % (name, x))
        allfail += 1
    for x in WARN.get(name, []):
        print('WARN [%s] %s' % (name, x))
    for x in INFO.get(name, []):
        print('info [%s] %s' % (name, x))
print('--------------------------------------')
print('FAIL 总数 =', allfail)

io.open(os.path.join(TOOLS, '_audit_dump.txt'), 'w', encoding='utf-8').write('\n'.join(DUMP))
print('BG/APP/ACC 摘出 -> tools/_audit_dump.txt')
