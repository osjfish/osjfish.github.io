# -*- coding: utf-8 -*-
"""《野望》王绩 课件生成器 —— 复用《背影》CSS/JS框架。
古诗版式：逐句解读，卡片summary用"译文 · 赏析"。
短篇不分part直接逐句。积累区用古诗骨架。"""
import json, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'yewang-wangji.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'yewang_fs')


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
    "东皋薄暮望，徙倚欲何依。",
    "树树皆秋色，山山唯落晖。",
    "牧人驱犊返，猎马带禽归。",
    "相顾无相识，长歌怀采薇。",
]

# 每句注释词表（文言字词：读音+释义+用法）
ANNO = [
    [("东皋", "（gāo）东边的高地。皋，水边高地。王绩隐居的地方。"), ("薄暮", "（bó mù）傍晚。薄，迫近。"), ("望", "眺望、远望。"), ("徙倚", "（xǐ yǐ）徘徊、来回走动。"), ("欲何依", "想要依靠什么呢？何，什么。依，依靠、归依。")],
    [("树树", "每一棵树。叠词，强调无一例外。"), ("皆", "都、全。副词。"), ("秋色", "秋天的景色。"), ("山山", "每一座山。叠词。"), ("唯", "只、只有。副词。"), ("落晖", "（huī）落日的光辉。晖，阳光。")],
    [("牧人", "放牧的人。"), ("驱", "驱赶、赶着。"), ("犊", "（dú）小牛。这里指牛群。"), ("返", "返回、回来。"), ("猎马", "猎人骑着的马。"), ("带", "带着、带回。"), ("禽", "鸟兽的总称，这里指猎获的鸟兽。"), ("归", "归来、回家。")],
    [("相顾", "互相看。顾，看。"), ("无相识", "没有认识的人。相识，认识的人、朋友。"), ("长歌", "放声高歌。长，拉长声音。"), ("怀", "怀念、心念。"), ("采薇", "《诗经·小雅》中有《采薇》篇，写戍卒的思乡之情。这里指隐居不仕、坚守节操。薇，一种野菜。")],
]

# 每句: (译文, 赏析)
YISHANG = [
    ("傍晚时分站在东皋纵目远望，我徘徊不定，不知该归依何方。",
     "首联点明时间（薄暮）、地点（东皋）、事件（望），~L~徙倚欲何依~R~化用曹操《短歌行》~L~绕树三匝，何枝可依~R~，表现诗人彷徨无依的孤独心境，为全诗奠定感情基调。"),
    ("层层树林都染上秋天的色彩，重重山岭披覆着落日的余光。",
     "颔联写远景，是全景式的秋景描写。~L~树树~R~~L~山山~R~叠词，强调无一例外；~L~皆~R~~L~唯~R~对举，见出秋景的萧瑟与苍茫；~L~落晖~R~点出时间，与首联~L~薄暮~R~呼应。"),
    ("牧人驱赶着牛群返还家园，猎人带着猎物驰过我的身旁。",
     "颈联写近景，是秋景中的人物活动。~L~驱犊返~R~~L~带禽归~R~，动静结合，画面生动；牧人猎人皆有所归，反衬诗人的孤独无依，为尾联抒情蓄势。"),
    ("大家相对无言彼此互不相识，我长啸高歌，真想隐居在山冈！",
     "尾联由景入情，点明主旨。~L~相顾无相识~R~写诗人的孤独；~L~长歌怀采薇~R~用伯夷、叔齐采薇而食的典故，表达诗人隐居不仕、坚守节操的志向，余味悠长。"),
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
    {"w":"皋","py":"gāo","q":"东□薄暮望，徙倚欲何依","tip":"「皋」白字头，音 gāo，水边高地，勿写「高」"},
    {"w":"薄","py":"bó","q":"东皋□暮望，徙倚欲何依","tip":"「薄」草字头，音 bó，迫近，勿读 báo（厚度小）"},
    {"w":"徙","py":"xǐ","q":"东皋薄暮望，□倚欲何依","tip":"「徙」双人旁，音 xǐ，迁移、徘徊，勿写「徒」（tú，步行）"},
    {"w":"倚","py":"yǐ","q":"东皋薄暮望，徙□欲何依","tip":"「倚」单人旁，音 yǐ，靠着，「徙倚」指徘徊，勿写「奇」"},
    {"w":"晖","py":"huī","q":"树树皆秋色，山山唯落□","tip":"「晖」日字旁，音 huī，阳光，勿写「辉」（光字旁）"},
    {"w":"犊","py":"dú","q":"牧人驱□返，猎马带禽归","tip":"「犊」牛字旁，音 dú，小牛，勿写「读」（言字旁）"},
    {"w":"薇","py":"wēi","q":"相顾无相识，长歌怀采□","tip":"「薇」草字头，音 wēi，一种野菜，勿写「微」（双人旁）"},
    {"w":"暮","py":"mù","q":"东皋薄□望，徙倚欲何依","tip":"「暮」日字底，音 mù，傍晚，勿写「幕」（巾字底）"},
]

DICT_NOTES = [
    {"w":"东皋","a":"（gāo）东边的高地，王绩隐居的地方","q":"东皋薄暮望"},
    {"w":"薄暮","a":"（bó mù）傍晚。薄，迫近","q":"东皋薄暮望"},
    {"w":"徙倚","a":"（xǐ yǐ）徘徊、来回走动","q":"徙倚欲何依"},
    {"w":"欲何依","a":"想要依靠什么呢？何，什么。依，依靠","q":"徙倚欲何依"},
    {"w":"皆","a":"都、全。副词","q":"树树皆秋色"},
    {"w":"唯","a":"只、只有。副词","q":"山山唯落晖"},
    {"w":"落晖","a":"（huī）落日的光辉。晖，阳光","q":"山山唯落晖"},
    {"w":"犊","a":"（dú）小牛，这里指牛群","q":"牧人驱犊返"},
    {"w":"禽","a":"鸟兽的总称，这里指猎获的鸟兽","q":"猎马带禽归"},
    {"w":"相顾","a":"互相看。顾，看","q":"相顾无相识"},
    {"w":"相识","a":"认识的人、朋友","q":"相顾无相识"},
    {"w":"长歌","a":"放声高歌。长，拉长声音","q":"长歌怀采薇"},
    {"w":"怀","a":"怀念、心念","q":"长歌怀采薇"},
    {"w":"采薇","a":"《诗经·小雅》有《采薇》篇，这里指隐居不仕、坚守节操。薇，野菜","q":"长歌怀采薇"},
    {"w":"秋色","a":"秋天的景色","q":"树树皆秋色"},
    {"w":"返","a":"返回、回来","q":"牧人驱犊返"},
    {"w":"归","a":"归来、回家","q":"猎马带禽归"},
    {"w":"驱","a":"驱赶、赶着","q":"牧人驱犊返"},
    {"w":"带","a":"带着、带回","q":"猎马带禽归"},
    {"w":"望","a":"眺望、远望","q":"东皋薄暮望"},
]


# ---------------- 组装 ----------------
BG = fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《野望》是隋末唐初诗人王绩的代表作，也是现存较早的一首成熟的五言律诗。诗人于隋末唐初的乱世中，弃官归隐东皋，在一个秋天的傍晚登高远望，写下了这首情景交融的名篇。</p>
    <p>全诗以~L~望~R~字统摄，先写薄暮秋景的萧瑟苍茫，再写牧人猎人皆有所归的热闹，最后以~L~相顾无相识，长歌怀采薇~R~收束，抒发了诗人孤独无依、向往隐居的情怀。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>王绩（约589—644），字无功，号东皋子，绛州龙门（今山西河津）人，隋末唐初诗人。他出身世家，早年仕隋，任秘书正字、六合县丞，因嗜酒被劾，弃官还乡。唐初以原官待诏门下省，后因不满官场，再次弃官归隐东皋，自号~L~东皋子~R~。</p>
    <p>王绩是唐代山水田园诗派的先驱，其诗多写饮酒、隐逸和田园风光，风格朴素自然，洗去了齐梁以来的浮华习气。《野望》是他最著名的作品，也是初唐五言律诗的代表作。有《王无功文集》。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>时代背景：</b>王绩生活在隋唐易代之际，社会动荡不安。他曾三仕三隐，最终选择归隐。《野望》写于他归隐东皋之后，诗中~L~东皋~R~即他隐居之地。</p>
    <p><b>心境背景：</b>诗人弃官归隐，虽有闲适之意，但内心并不平静。在一个秋天的傍晚，他登高远望，看到萧瑟的秋景和牧人猎人皆有所归，不禁感到孤独无依，于是写下这首诗，抒发彷徨苦闷和向往隐居的情怀。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>古诗朗读《野望》王绩</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV19cyUYkEqE&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="古诗朗读《野望》"></iframe>
        <a href="https://www.bilibili.com/video/BV19cyUYkEqE" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>古诗赏析《野望》王绩</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1fe411s7pc&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="古诗赏析《野望》"></iframe>
        <a href="https://www.bilibili.com/video/BV1fe411s7pc" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 主题</span></div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">情景交融，景中含情</div>
        <p>全诗以~L~望~R~字统摄，先写薄暮秋景：~L~树树皆秋色，山山唯落晖~R~，萧瑟苍茫；再写人物活动：~L~牧人驱犊返，猎马带禽归~R~，热闹温馨。景越热闹，越反衬诗人的孤独；景越萧瑟，越烘托诗人的彷徨。情景交融，景中含情。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">动静结合，远近相宜</div>
        <p>颔联写远景、静景：树林秋色、山岭落晖，是静态的全景；颈联写近景、动景：牧人驱犊、猎马带禽，是动态的特写。远近相宜，动静结合，画面层次分明，生动立体。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">用词精准，叠字传神</div>
        <p>~L~树树~R~~L~山山~R~叠词，强调每一棵树、每一座山都染上秋色、披覆落晖，无一例外，见出秋景的广袤与萧瑟；~L~皆~R~~L~唯~R~对举，用词精准，写出秋景的单调与苍茫。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">用典贴切，余味悠长</div>
        <p>~L~徙倚欲何依~R~化用曹操《短歌行》~L~绕树三匝，何枝可依~R~，表现彷徨无依；~L~长歌怀采薇~R~用伯夷、叔齐采薇而食、不食周粟的典故，表达隐居不仕、坚守节操的志向。用典贴切自然，余味悠长。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《野望》通过描写薄暮时分东皋的秋景，抒发了诗人孤独无依、彷徨苦闷的心情，表达了对隐居生活的向往和坚守节操的志向。</p>
    <p>诗人弃官归隐，看似闲适，内心却充满矛盾：在萧瑟的秋景中，在牧人猎人皆有所归的对照下，他感到~L~相顾无相识~R~的孤独，只能~L~长歌怀采薇~R~，以伯夷、叔齐自比，在隐居中寻求精神的慰藉。全诗语言朴素，意境苍凉，是初唐五言律诗的佳作。</p>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">~L~树树皆秋色，山山唯落晖~R~</div>
        <p>这两句是全诗写景的名句。~L~树树~R~~L~山山~R~叠词，强调范围之广，无一例外；~L~皆~R~~L~唯~R~对举，见出秋景的萧瑟与单调。诗人用朴素的语言，勾勒出一幅苍茫的秋山落日图，意境开阔而苍凉，为尾联的抒情做了有力的铺垫。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">~L~牧人驱犊返，猎马带禽归~R~</div>
        <p>这两句由静转动，由远及近，写秋景中的人物活动。牧人驱赶牛群回家，猎人带着猎物归来，画面温馨而热闹。然而，这一切都与诗人无关——别人皆有所归，自己却孤独无依。以乐景写哀情，反衬手法的运用，使诗人的孤独更加突出。</p>
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
      <div class="acc-item"><span class="acc-w">押韵</span><span class="acc-d">本诗押~L~微~R~韵：依（yī）、晖（huī）、归（guī）、薇（wēi），韵脚在二、四、六、八句。</span></div>
      <div class="acc-item"><span class="acc-w">对仗</span><span class="acc-d">颔联~L~树树皆秋色，山山唯落晖~R~与颈联~L~牧人驱犊返，猎马带禽归~R~对仗工整。</span></div>
      <div class="acc-item"><span class="acc-w">首联/颔联/颈联/尾联</span><span class="acc-d">律诗八句分为四联：一二句为首联，三四句为颔联，五六句为颈联，七八句为尾联。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>易错字音形</h3>
      <div class="acc-item"><span class="acc-w">皋</span><span class="acc-d">（gāo）白字头，水边高地。不读 gào，不写~L~高~R~。</span></div>
      <div class="acc-item"><span class="acc-w">薄</span><span class="acc-d">（bó）迫近。~L~薄暮~R~即傍晚。不读 báo（厚度小）。</span></div>
      <div class="acc-item"><span class="acc-w">徙</span><span class="acc-d">（xǐ）双人旁，迁移、徘徊。与~L~徒~R~（tú，步行）区分。</span></div>
      <div class="acc-item"><span class="acc-w">倚</span><span class="acc-d">（yǐ）单人旁，靠着。~L~徙倚~R~指徘徊。不写~L~奇~R~。</span></div>
      <div class="acc-item"><span class="acc-w">晖</span><span class="acc-d">（huī）日字旁，阳光。与~L~辉~R~（光字旁，光辉）区分。</span></div>
      <div class="acc-item"><span class="acc-w">犊</span><span class="acc-d">（dú）牛字旁，小牛。与~L~读~R~（言字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">薇</span><span class="acc-d">（wēi）草字头，野菜。与~L~微~R~（双人旁，微小）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文言梳理</h3>
      <div class="acc-sub">一词多义</div>
      <div class="acc-item"><span class="acc-w">依</span><span class="acc-d">①依靠、归依（欲何依）；②依照、按照（依此类推）。</span></div>
      <div class="acc-item"><span class="acc-w">顾</span><span class="acc-d">①看（相顾）；②回头看（顾野有麦场）；③拜访（三顾茅庐）；④反而、却（顾不如蜀鄙之僧哉）。</span></div>
      <div class="acc-sub">古今异义</div>
      <div class="acc-item"><span class="acc-w">相识</span><span class="acc-d">古义：认识的人、朋友（相顾无相识）。今义：彼此认识。</span></div>
      <div class="acc-item"><span class="acc-w">长歌</span><span class="acc-d">古义：放声高歌。今义：长时间地唱歌。</span></div>
      <div class="acc-sub">词类活用</div>
      <div class="acc-item"><span class="acc-w">秋色</span><span class="acc-d">名词作动词，染上秋天的颜色（树树皆秋色）。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>核心考点</h3>
      <div class="acc-item"><span class="acc-w">~L~望~R~字统摄</span><span class="acc-d">全诗以~L~望~R~字统领，写了哪些景？抒发了什么情？这是理解全诗的关键。</span></div>
      <div class="acc-item"><span class="acc-w">反衬手法</span><span class="acc-d">牧人猎人皆有所归，反衬诗人的孤独无依；热闹的场景反衬内心的苦闷。</span></div>
      <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">~L~徙倚欲何依~R~化用曹操诗句；~L~长歌怀采薇~R~用伯夷、叔齐的典故。需掌握典故含义。</span></div>
      <div class="acc-item"><span class="acc-w">叠词作用</span><span class="acc-d">~L~树树~R~~L~山山~R~叠词的表达效果：强调范围之广，增强节奏感和音韵美。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞与手法</h3>
      <div class="acc-item"><span class="acc-w">对偶（对仗）</span><span class="acc-d">颔联、颈联对仗工整，是律诗的基本要求。</span></div>
      <div class="acc-item"><span class="acc-w">叠词</span><span class="acc-d">~L~树树~R~~L~山山~R~，强调无一例外，增强节奏感。</span></div>
      <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">~L~何枝可依~R~~L~采薇~R~两个典故，含蓄地表达情感。</span></div>
      <div class="acc-item"><span class="acc-w">反衬</span><span class="acc-d">以乐景写哀情，以他人之归反衬自己无依。</span></div>
      <div class="acc-item"><span class="acc-w">动静结合</span><span class="acc-d">颔联静景，颈联动景，动静相宜。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">采薇</span><span class="acc-d">伯夷、叔齐是商末孤竹君之子，商亡后不食周粟，隐居首阳山采薇而食，最终饿死。后以~L~采薇~R~指隐居不仕、坚守节操。</span></div>
      <div class="acc-item"><span class="acc-w">东皋</span><span class="acc-d">王绩隐居之地，在今山西河津。王绩自号~L~东皋子~R~。</span></div>
      <div class="acc-item"><span class="acc-w">五言律诗的成熟</span><span class="acc-d">《野望》是现存较早的成熟五言律诗，在律诗发展史上有重要地位。此前的五言诗多为古体，平仄对仗不严格。</span></div>
      <div class="acc-item"><span class="acc-w">山水田园诗派</span><span class="acc-d">王绩是唐代山水田园诗派的先驱，后有王维、孟浩然等大家。山水田园诗多写自然风光和隐逸情怀。</span></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《野望》王绩</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">唐 · 王绩</div>
  <h1 class="hero-title">野望</h1>
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
  <div class="kai">《野望》</div>
  <div>王绩 · 唐 · 五言律诗 · 山水田园</div>
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
