# -*- coding: utf-8 -*-
"""《渡荆门送别》李白 课件生成器 —— 复用《背影》CSS/JS框架。
古诗版式：逐句解读，卡片summary用"译文 · 赏析"。
短篇不分part直接逐句。积累区用古诗骨架。"""
import json, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dujingmensongbie-libai.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'dujingmen_fs')


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


def annotate_text(text, word_list):
    items = sorted(word_list, key=lambda x: -len(x[0]))
    used = set()
    for w, n in items:
        if w in used:
            continue
        idx = text.find(w)
        while idx != -1:
            before = text[:idx]
            open_count = before.count('<span class="anno-word"')
            close_count = before.count('</span>')
            if open_count > close_count:
                idx = text.find(w, idx + 1)
                continue
            replacement = '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
            text = text[:idx] + replacement + text[idx + len(w):]
            used.add(w)
            break
    return text


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "渡远荆门外，来从楚国游。",
    "山随平野尽，江入大荒流。",
    "月下飞天镜，云生结海楼。",
    "仍怜故乡水，万里送行舟。",
]

# 每句注释词表（文言字词：读音+释义+用法）
ANNO = [
    [("渡远", "乘船远行。渡，乘船过河。远，远行。"), ("荆门", "即荆门山，在今湖北宜都西北，长江南岸，与北岸虎牙山对峙，形势险要，自古为楚蜀交通咽喉。"), ("外", "之外，指荆门以西的蜀地以东。"), ("来从", "来到。从，跟随、到。"), ("楚国", "古楚国之地，今湖北、湖南一带，春秋时属楚国。"), ("游", "游历、游览。")],
    [("山", "山峦，指蜀地的群山。"), ("随", "随着、跟随。"), ("平野", "平坦广阔的原野。"), ("尽", "消失、到了尽头。"), ("江", "长江。"), ("入", "流入、进入。"), ("大荒", "辽阔无边的原野。荒，边远的地方。"), ("流", "奔流、流淌。")],
    [("月", "月亮。"), ("下", "落下、从空中落下。"), ("飞", "飞一样地、快速地。"), ("天镜", "天上的镜子，比喻月亮倒映在江水中，如一面飞来的明镜。"), ("云生", "云彩兴起。生，产生、兴起。"), ("结", "凝结、形成。"), ("海楼", "即海市蜃楼，这里形容江上云霞变幻的美丽景象。")],
    [("仍", "仍然、还。副词。"), ("怜", "怜爱、喜爱。"), ("故乡水", "指从故乡流来的长江水。李白故乡在蜀地，长江流经蜀地，故称。"), ("万里", "形容路途遥远。"), ("送行舟", "送我乘坐的船远行。行舟，行驶的船。")],
]

# 每句: (译文, 赏析)
YISHANG = [
    ("我乘舟远行，渡过荆门山之外，来到楚地漫游。",
     "首联点明出发地和目的地。~L~渡远~R~写诗人乘舟远行，~L~荆门外~R~点出途经之地，~L~楚国游~R~点明此行目的。叙事中见出诗人年少远游的豪情，为全诗奠定雄浑开阔的基调。"),
    ("山峦随着平坦的原野渐渐消失，长江奔流入辽阔无边的原野。",
     "颔联写舟行所见的壮阔景象。~L~随~R~~L~入~R~两个动词，写出山势由高到低、江水由狭到阔的动态变化；~L~平野~R~~L~大荒~R~意境开阔，见出诗人胸襟的宽广。这两句是写长江出峡的名句。"),
    ("月亮倒映在江中，如同从天上飞来的明镜；云霞兴起，结成了海市蜃楼般的奇景。",
     "颈联写江上的美丽夜景。~L~月下飞天镜~R~以~L~天镜~R~比喻江中月影，想象奇特；~L~云生结海楼~R~以~L~海楼~R~形容云霞变幻，瑰丽壮观。两句一静一动，一近一远，画面奇幻，体现李白浪漫主义诗风。"),
    ("我依然怜爱这来自故乡的江水，它不辞万里，送我远行的小舟。",
     "尾联由景入情，点明主旨。诗人不说自己思念故乡，而说故乡之水~L~万里送行舟~R~，将思乡之情寄托于江水，构思巧妙，含蓄深沉。~L~怜~R~字见出诗人对故乡的深情，余味悠长。"),
]

# Build verses
verses_html_parts = []
for i in range(4):
    annotated = annotate_text(FULLTEXT[i], ANNO[i])
    idx = i + 1
    verses_html_parts.append('      <div class="verse" id="l%d" data-i="%d">' % (idx, idx - 1))
    verses_html_parts.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx, fixq(annotated)))
    verses_html_parts.append('        <details class="v-more">')
    verses_html_parts.append('          <summary>译文 · 赏析</summary>')
    verses_html_parts.append('          <div class="d-body">')
    verses_html_parts.append('            <div class="v-sec"><b class="v-label">译文</b>')
    verses_html_parts.append('              <div class="v-trans">%s</div>' % fixq(YISHANG[i][0]))
    verses_html_parts.append('            </div>')
    verses_html_parts.append('            <div class="v-sec"><b class="v-label">赏析</b>')
    verses_html_parts.append('              <div class="d-body"><p>%s</p></div>' % fixq(YISHANG[i][1]))
    verses_html_parts.append('            </div>')
    verses_html_parts.append('          </div>')
    verses_html_parts.append('        </details>')
    verses_html_parts.append('      </div>')
verses_html = '\n'.join(verses_html_parts)
full_html = '\n'.join('    <div class="pl">%s</div>' % fixq(p) for p in FULLTEXT)
anno_count = sum(len(a) for a in ANNO)


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"荆","py":"jīng","q":"渡远□门外，来从楚国游","tip":"「荆」立刀旁，音 jīng，荆门山，勿写「京」"},
    {"w":"荒","py":"huāng","q":"山随平野尽，江入大□流","tip":"「荒」草字头，音 huāng，边远，「大荒」指辽阔原野，勿写「慌」（竖心旁）"},
    {"w":"镜","py":"jìng","q":"月下飞天□，云生结海楼","tip":"「镜」金字旁，音 jìng，镜子，「天镜」比喻江中月影，勿写「境」（土字旁）"},
    {"w":"蜃蜃","py":"shèn shèn","q":"云生结海□（海市□楼）","tip":"「蜃」虫字旁，音 shèn，大蛤蜊，传说蜃吐气成楼阁，「海市蜃楼」，勿写「唇」（口字旁）"},
    {"w":"怜","py":"lián","q":"仍□故乡水，万里送行舟","tip":"「怜」竖心旁，音 lián，怜爱、喜爱，勿写「连」（走之底）"},
    {"w":"渡","py":"dù","q":"□远荆门外，来从楚国游","tip":"「渡」三点水，音 dù，乘船过河，勿写「度」（广字头）"},
    {"w":"野","py":"yě","q":"山随平□尽，江入大荒流","tip":"「野」里字旁，音 yě，原野，「平野」指平坦的原野，勿写「也」"},
    {"w":"舟","py":"zhōu","q":"仍怜故乡水，万里送行□","tip":"「舟」舟字旁，音 zhōu，船，「行舟」指行驶的船，勿写「船」"},
]

DICT_NOTES = [
    {"w":"渡远","a":"乘船远行。渡，乘船过河。远，远行","q":"渡远荆门外"},
    {"w":"荆门","a":"即荆门山，在今湖北宜都西北，长江南岸","q":"渡远荆门外"},
    {"w":"楚国","a":"古楚国之地，今湖北、湖南一带","q":"来从楚国游"},
    {"w":"游","a":"游历、游览","q":"来从楚国游"},
    {"w":"平野","a":"平坦广阔的原野","q":"山随平野尽"},
    {"w":"尽","a":"消失、到了尽头","q":"山随平野尽"},
    {"w":"大荒","a":"辽阔无边的原野。荒，边远的地方","q":"江入大荒流"},
    {"w":"天镜","a":"天上的镜子，比喻月亮倒映在江水中","q":"月下飞天镜"},
    {"w":"海楼","a":"即海市蜃楼，这里形容江上云霞变幻的景象","q":"云生结海楼"},
    {"w":"仍","a":"仍然、还。副词","q":"仍怜故乡水"},
    {"w":"怜","a":"怜爱、喜爱","q":"仍怜故乡水"},
    {"w":"故乡水","a":"指从故乡流来的长江水。李白故乡在蜀地","q":"仍怜故乡水"},
    {"w":"万里","a":"形容路途遥远","q":"万里送行舟"},
    {"w":"行舟","a":"行驶的船","q":"万里送行舟"},
    {"w":"随","a":"随着、跟随","q":"山随平野尽"},
    {"w":"入","a":"流入、进入","q":"江入大荒流"},
    {"w":"结","a":"凝结、形成","q":"云生结海楼"},
    {"w":"云生","a":"云彩兴起。生，产生、兴起","q":"云生结海楼"},
    {"w":"飞","a":"飞一样地、快速地","q":"月下飞天镜"},
    {"w":"下","a":"落下、从空中落下","q":"月下飞天镜"},
]


# ---------------- 组装 ----------------
BG = fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《渡荆门送别》是唐代大诗人李白青年时期出蜀远游时所作的一首五言律诗。开元十三年（725），二十五岁的李白怀着~L~仗剑去国，辞亲远游~R~的豪情，离开故乡蜀地，乘舟沿长江东下，途经荆门山时写下了这首名篇。</p>
    <p>全诗以~L~渡~R~字起笔，写舟行所见的壮阔景象，最后以~L~仍怜故乡水，万里送行舟~R~收束，将思乡之情寄托于滔滔江水，意境开阔，情感真挚，是李白山水诗的代表作之一。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>李白（701—762），字太白，号青莲居士，唐代伟大的浪漫主义诗人，被后人誉为~L~诗仙~R~。祖籍陇西成纪（今甘肃静宁西南），出生于碎叶（今吉尔吉斯斯坦托克马克），幼时随父迁居绵州昌隆（今四川江油）青莲乡。</p>
    <p>李白的诗风雄奇豪放，想象丰富，语言流转自然，音律和谐多变。他善于从民歌、神话中汲取营养，构成其特有的瑰丽绚烂的色彩，是屈原以来最杰出的浪漫主义诗人。与杜甫并称~L~李杜~R~。有《李太白集》。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>出蜀远游：</b>开元十三年（725），二十五岁的李白离开生活多年的蜀地，~L~仗剑去国，辞亲远游~R~。他乘舟沿长江东下，出三峡，过荆门，开始了漫游天下的生涯。《渡荆门送别》即写于此次出蜀途中。</p>
    <p><b>荆门山：</b>荆门山在今湖北宜都西北，长江南岸，与北岸虎牙山对峙，是长江出三峡后的险要之处。过了荆门，长江进入中游平原，地势豁然开朗，景色与蜀地的崇山峻岭截然不同，诗人因此写下这首诗。</p>
    <p><b>~L~送别~R~之意：</b>题目中的~L~送别~R~，不是送别友人，而是指故乡之水~L~万里送行舟~R~——诗人不说自己送别故乡，而说故乡之水送别自己，构思巧妙，含蓄深沉。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>古诗朗读《渡荆门送别》李白</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1HG4y167xV&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="古诗朗读《渡荆门送别》"></iframe>
        <a href="https://www.bilibili.com/video/BV1HG4y167xV" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>古诗赏析《渡荆门送别》李白</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1k5411t7T4&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="古诗赏析《渡荆门送别》"></iframe>
        <a href="https://www.bilibili.com/video/BV1k5411t7T4" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">艺术 · 主题 · 名句</span></div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">意境开阔，气势雄浑</div>
        <p>全诗以~L~渡~R~字起笔，写舟行所见：山峦随着平野消失，长江奔流入大荒，月影如天镜飞来，云霞似海楼变幻。画面开阔，气势雄浑，展现了长江出峡后的壮丽景象，也见出诗人年少远游的豪迈胸襟。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">想象奇特，比喻精妙</div>
        <p>~L~月下飞天镜~R~以~L~天镜~R~比喻江中月影，想象月亮从天上飞落江中，化静为动，奇特瑰丽；~L~云生结海楼~R~以~L~海楼~R~（海市蜃楼）形容云霞变幻，瑰丽壮观。两个比喻体现了李白浪漫主义的诗风。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">动静结合，远近相宜</div>
        <p>颔联~L~山随平野尽，江入大荒流~R~写远景、动态，山势由高到低，江水由狭到阔；颈联~L~月下飞天镜，云生结海楼~R~写近景、静中含动，月影如镜，云霞变幻。动静结合，远近相宜，画面层次分明。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">构思巧妙，含蓄深沉</div>
        <p>尾联~L~仍怜故乡水，万里送行舟~R~，诗人不说自己思念故乡，而说故乡之水怜爱自己、万里相送，将思乡之情寄托于江水，化无情为有情，构思巧妙，含蓄深沉。~L~怜~R~字见出诗人对故乡的深情，余味悠长。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《渡荆门送别》通过描写舟行荆门所见的壮阔景象，抒发了诗人对祖国大好河山的热爱，同时也表达了对故乡的深切思念。</p>
    <p>诗人年少出蜀，胸怀~L~仗剑去国，辞亲远游~R~的豪情，面对长江出峡后的壮丽景象，意气风发；但在豪情之中，也蕴含着对故乡的不舍——~L~仍怜故乡水，万里送行舟~R~，将思乡之情写得含蓄而深沉。全诗意境开阔，情感真挚，是李白山水诗的代表作。</p>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">~L~山随平野尽，江入大荒流~R~</div>
        <p>这两句是写长江出峡的名句。~L~随~R~字写出山峦随着平野的出现而逐渐消失的动态，~L~入~R~字写出长江奔流入辽阔原野的气势。一~L~随~R~一~L~入~R~，将静景写动，画面开阔，气势雄浑，与杜甫~L~星垂平野阔，月涌大江流~R~有异曲同工之妙。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">~L~月下飞天镜，云生结海楼~R~</div>
        <p>这两句写江上夜景，想象奇特。~L~飞天镜~R~将江中月影比作从天上飞来的明镜，化静为动；~L~结海楼~R~将云霞变幻比作海市蜃楼，瑰丽壮观。一~L~飞~R~一~L~结~R~，动词精准，画面奇幻，充分体现了李白浪漫主义的诗风。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">~L~仍怜故乡水，万里送行舟~R~</div>
        <p>尾联由景入情，点明主旨。诗人不说自己思念故乡，而说故乡之水~L~万里送行舟~R~，将思乡之情寄托于江水，化无情为有情。~L~怜~R~字见出诗人对故乡的深情，~L~万里~R~写路途之遥，更见思乡之切。以景结情，余味悠长。</p>
      </div>
    </div>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 考点 · 修辞 · 文化</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>文体与格律</h3>
      <div class="acc-item"><span class="acc-w">五言律诗</span><span class="acc-d">简称~L~五律~R~，近体诗的一种，每首八句，每句五字，共四十字。要求颔联、颈联对仗，平仄协调，押韵严格。</span></div>
      <div class="acc-item"><span class="acc-w">押韵</span><span class="acc-d">本诗押~L~尤~R~韵：游（yóu）、流（liú）、楼（lóu）、舟（zhōu），韵脚在二、四、六、八句。</span></div>
      <div class="acc-item"><span class="acc-w">对仗</span><span class="acc-d">颔联~L~山随平野尽，江入大荒流~R~与颈联~L~月下飞天镜，云生结海楼~R~对仗工整。</span></div>
      <div class="acc-item"><span class="acc-w">~L~送别~R~之意</span><span class="acc-d">题目中的~L~送别~R~不是送别友人，而是指故乡之水~L~万里送行舟~R~，是诗人自指。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>易错字音形</h3>
      <div class="acc-item"><span class="acc-w">荆</span><span class="acc-d">（jīng）立刀旁，荆门山。不读 jīn，不写~L~京~R~。</span></div>
      <div class="acc-item"><span class="acc-w">荒</span><span class="acc-d">（huāng）草字头，边远。~L~大荒~R~指辽阔原野。与~L~慌~R~（竖心旁，慌张）区分。</span></div>
      <div class="acc-item"><span class="acc-w">镜</span><span class="acc-d">（jìng）金字旁，镜子。~L~天镜~R~比喻江中月影。与~L~境~R~（土字旁，环境）区分。</span></div>
      <div class="acc-item"><span class="acc-w">蜃</span><span class="acc-d">（shèn）虫字旁，大蛤蜊。~L~海市蜃楼~R~。不读 chén，不写~L~唇~R~。</span></div>
      <div class="acc-item"><span class="acc-w">怜</span><span class="acc-d">（lián）竖心旁，怜爱、喜爱。与~L~连~R~（走之底）区分。</span></div>
      <div class="acc-item"><span class="acc-w">渡</span><span class="acc-d">（dù）三点水，乘船过河。与~L~度~R~（广字头，度过）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文言梳理</h3>
      <div class="acc-sub">一词多义</div>
      <div class="acc-item"><span class="acc-w">尽</span><span class="acc-d">①消失、到尽头（山随平野尽）；②全部（尽人皆知）；③竭尽（尽善尽美）。</span></div>
      <div class="acc-item"><span class="acc-w">怜</span><span class="acc-d">①怜爱、喜爱（仍怜故乡水）；②怜悯、同情（可怜身上衣正单）；③可惜（可怜九月初三夜）。</span></div>
      <div class="acc-item"><span class="acc-w">游</span><span class="acc-d">①游历、游览（楚国游）；②游动（鱼游濠上）；③交往（交游）。</span></div>
      <div class="acc-sub">古今异义</div>
      <div class="acc-item"><span class="acc-w">大荒</span><span class="acc-d">古义：辽阔无边的原野。今义：大灾之年、严重歉收。</span></div>
      <div class="acc-item"><span class="acc-w">海楼</span><span class="acc-d">古义：海市蜃楼，形容云霞变幻。今义：海边的楼阁。</span></div>
      <div class="acc-sub">词类活用</div>
      <div class="acc-item"><span class="acc-w">飞</span><span class="acc-d">名词作状语，像飞一样（月下飞天镜）。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>核心考点</h3>
      <div class="acc-item"><span class="acc-w">~L~随~R~~L~入~R~炼字</span><span class="acc-d">颔联~L~随~R~~L~入~R~两个动词的表达效果：写出山势由高到低、江水由狭到阔的动态变化，化静为动。</span></div>
      <div class="acc-item"><span class="acc-w">比喻赏析</span><span class="acc-d">~L~天镜~R~比喻江中月影，~L~海楼~R~比喻云霞变幻，需掌握比喻的表达效果和李白浪漫主义诗风。</span></div>
      <div class="acc-item"><span class="acc-w">~L~送别~R~之意</span><span class="acc-d">题目中的~L~送别~R~不是送别友人，而是故乡之水送自己，需理解这一特殊的~L~送别~R~含义。</span></div>
      <div class="acc-item"><span class="acc-w">思乡之情</span><span class="acc-d">尾联~L~仍怜故乡水，万里送行舟~R~如何表达思乡之情：化无情为有情，含蓄深沉。</span></div>
      <div class="acc-item"><span class="acc-w">意境分析</span><span class="acc-d">全诗意境开阔雄浑，需结合具体诗句分析画面特点和诗人情感。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞与手法</h3>
      <div class="acc-item"><span class="acc-w">对偶（对仗）</span><span class="acc-d">颔联、颈联对仗工整，是律诗的基本要求。</span></div>
      <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">~L~天镜~R~比喻江中月影，~L~海楼~R~比喻云霞变幻，想象奇特。</span></div>
      <div class="acc-item"><span class="acc-w">拟人</span><span class="acc-d">~L~故乡水~R~~L~万里送行舟~R~，将江水拟人化，化无情为有情。</span></div>
      <div class="acc-item"><span class="acc-w">动静结合</span><span class="acc-d">颔联动景，颈联静中含动，动静相宜。</span></div>
      <div class="acc-item"><span class="acc-w">借景抒情</span><span class="acc-d">以壮阔之景写豪迈之情，以故乡之水写思乡之情。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">荆门山</span><span class="acc-d">在今湖北宜都西北，长江南岸，与北岸虎牙山对峙，是长江出三峡后的险要之处，自古为楚蜀交通咽喉。</span></div>
      <div class="acc-item"><span class="acc-w">楚国</span><span class="acc-d">春秋战国时期的诸侯国，疆域主要在今湖北、湖南一带，都城在郢（今湖北荆州）。</span></div>
      <div class="acc-item"><span class="acc-w">海市蜃楼</span><span class="acc-d">（shèn）大气中由于光线折射而形成的自然现象，多出现在海边或沙漠，古人误以为是蜃（大蛤蜊）吐气而成。</span></div>
      <div class="acc-item"><span class="acc-w">李白出蜀</span><span class="acc-d">开元十三年（725），二十五岁的李白~L~仗剑去国，辞亲远游~R~，离开蜀地，开始漫游天下。此诗写于出蜀途中。</span></div>
      <div class="acc-item"><span class="acc-w">诗仙</span><span class="acc-d">李白的称号，与~L~诗圣~R~杜甫并称~L~李杜~R~。李白是屈原以来最杰出的浪漫主义诗人。</span></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《渡荆门送别》李白</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">唐 · 李白</div>
  <h1 class="hero-title">渡荆门送别</h1>
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
        <option value="100">100%%</option>
        <option value="150">150%%</option>
        <option value="200">200%%</option>
        <option value="250">250%%</option>
        <option value="300">300%%</option>
      </select>
      <button id="btnAll">展开</button>
      <button id="btnRecite">背诵</button>
      <button id="btnPrint">打印</button>
    </div>
  </div>
</nav>

<main class="wrap">
%(bg)s

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 译文 · 赏析</span></div>
  <div class="sec-sub">五言律诗，八句四联。每句含译文与赏析，点击可展开。</div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
%(fulltext)s
  </div>
  <div class="verse-list" id="verseList">
%(verses)s
  </div>
</section>

<div class="divider"></div>
%(app)s

<div class="divider"></div>
%(acc)s

<div class="divider"></div>
<section id="practice" class="sec">
    <div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>
    <div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>
    <div class="ptools">
      <button data-mode="word" data-rand="5">随机五组字形</button>
      <button data-mode="word" data-all="1">全部字形</button>
      <button data-mode="note" data-rand="5">随机五组注释</button>
      <button data-mode="note" data-all="1">全部注释</button>
    </div>
  </section>

<footer>
  <div class="kai">《渡荆门送别》</div>
  <div>李白 · 唐 · 五言律诗 · 山水行旅</div>
</footer>
</main>

<button class="top-btn" id="topBtn" title="回到顶部">↑</button>
<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>
<div class="dictate" id="dictate" hidden>
  <div class="dictate-top">
    <span class="dictate-mode" id="dictMode">字形听写</span>
    <span class="dictate-progress" id="dictProgress">第 1 / 5 题</span>
    <button class="dictate-fs" id="dictFsMinus">A−</button><button class="dictate-fs" id="dictFsPlus">A+</button><button class="dictate-exit" id="dictExit">退出</button>
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
%(js)s
</script>
<script>
var DICT_WORDS = %(words)s;
var DICT_NOTES = %(notes)s;
</script>

</body>
</html>
''' % {
    'css': CSS,
    'js': JS,
    'bg': BG,
    'app': APP,
    'acc': ACC,
    'fulltext': full_html,
    'verses': verses_html,
    'words': json.dumps(DICT_WORDS, ensure_ascii=False),
    'notes': json.dumps(DICT_NOTES, ensure_ascii=False),
}

HTML = fixq(HTML)
io.open(OUT, 'w', encoding='utf-8').write(HTML)
print('OK', OUT, 'verses=4', 'anno=', anno_count, 'words=', len(DICT_WORDS), 'notes=', len(DICT_NOTES))
