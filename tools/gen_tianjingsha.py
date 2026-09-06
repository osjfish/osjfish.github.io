# -*- coding: utf-8 -*-
"""《天净沙·秋思》课件生成器 —— 元曲小令，复用《背影》CSS/JS框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tianjingsha-qiusi-mazhiyuan.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'tianjingsha_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


FULLTEXT = [
    "枯藤老树昏鸦，",
    "小桥流水人家，",
    "古道西风瘦马。",
    "夕阳西下，",
    "断肠人在天涯。",
]

PARTS = [
    ("第一部分", "秋景三联 · 萧瑟凄清", "第 1–3 句",
     fixq("前三句各用三个名词性短语并列，不用一个动词，构成三组意象画面：~L~枯藤老树昏鸦~R~写秋日黄昏的萧瑟，~L~小桥流水人家~R~写江南水乡的温馨，~L~古道西风瘦马~R~写游子旅途的艰辛。三组意象一冷一暖一苦，对比鲜明，为末二句的抒情做了充分的铺垫。这种~L~列锦~R~的手法，是元曲小令的经典写法。")),
    ("第二部分", "夕阳断肠 · 天涯游子", "第 4–5 句",
     fixq("~L~夕阳西下~R~点明时间，将前三句的意象统一在黄昏的背景之下，渲染出苍茫凄清的氛围。~L~断肠人在天涯~R~直抒胸臆，点明全曲主旨——漂泊天涯的游子，在秋日黄昏中愁肠寸断。~L~断肠~R~二字，将游子的思乡之苦写到极致，是全曲的点睛之笔。这首小令被誉为~L~秋思之祖~R~，短短二十八字，写尽了天涯游子的悲秋之情。")),
]

S = [
(0, "[[枯藤|干枯的藤蔓。枯，干枯；藤，藤蔓]]老树[[昏鸦|（hūn yā）黄昏时归巢的乌鸦。昏，黄昏；鸦，乌鸦]]，",
 "干枯的藤蔓缠绕着老树，黄昏时归巢的乌鸦栖息在枝头。",
 fixq("开篇即推出三组意象：~L~枯藤~R~~L~老树~R~~L~昏鸦~R~。三个名词性短语并列，不用一个动词，却构成了一幅萧瑟凄清的秋日黄昏图。~L~枯~R~字写藤蔓的干枯，~L~老~R~字写树木的苍老，~L~昏~R~字写时间的昏暗——三个修饰词，将秋日黄昏的萧瑟氛围渲染得淋漓尽致。~L~昏鸦~R~归巢，暗含~L~鸟尚有归处，人却漂泊无依~R~的对比，为下文~L~断肠人~R~做铺垫。这种纯用名词并列的~L~列锦~R~手法，是元曲小令的经典写法。"),
 ["列锦", "意象", "萧瑟", "起笔"]),

(0, "小桥[[流水|流动的水。流，流动；水，河水]]人家，",
 "小桥下流水潺潺，桥边有几户人家。",
 fixq("第二句意象一转，推出~L~小桥~R~~L~流水~R~~L~人家~R~三组温馨的意象。与上一句的萧瑟凄清形成鲜明对比——~L~小桥流水人家~R~是一幅宁静温馨的江南水乡图，人家的炊烟、流水的声响，都暗示着家的温暖。但这种温馨对漂泊的游子来说，不是慰藉，而是更深的刺激——别人有家可归，自己却漂泊天涯。以乐景写哀情，倍增其哀。这一句在全曲中起到了对比和反衬的作用，使游子的孤独更加突出。"),
 ["列锦", "对比", "以乐景写哀", "反衬"]),

(0, "[[古道|古老的道路。古，古老；道，道路]][[西风|（xī fēng）秋风。古代以西方为秋，故称秋风为西风]][[瘦马|（shòu mǎ）瘦弱的马。瘦，瘦弱；马，马匹]]。",
 "古老的道路上，秋风萧瑟，一匹瘦弱的马在艰难前行。",
 fixq("第三句又回到萧瑟的主题，推出~L~古道~R~~L~西风~R~~L~瘦马~R~三组意象。~L~古道~R~写道路的荒凉古老，~L~西风~R~写秋风的萧瑟寒冷，~L~瘦马~R~写马匹的瘦弱疲惫——马尚且如此，人何以堪？这一句将游子旅途的艰辛写得入木三分。~L~瘦马~R~的~L~瘦~R~字，不仅写马的瘦弱，也暗示游子的疲惫和憔悴。前三句九组意象，一冷一暖一苦，对比鲜明，为末二句的抒情蓄足了势。"),
 ["列锦", "意象", "旅途艰辛", "铺垫"]),

(1, "[[夕阳|傍晚的太阳。夕，傍晚；阳，太阳]]西下，",
 "夕阳向西缓缓落下。",
 fixq("第四句~L~夕阳西下~R~，点明时间，将前三句的九组意象统一在黄昏的背景之下。夕阳西下，本是一日将尽之时，也是游子最易思乡的时刻——~L~日暮乡关何处是~R~，黄昏总是与思乡联系在一起。这一句如电影的广角镜头，将前三句的近景拉远，渲染出苍茫凄清的整体氛围，也为末句~L~断肠人在天涯~R~的出场做了最后的铺垫。~L~西下~R~二字，写出夕阳的缓缓沉落，也暗示时光的流逝和游子的漂泊无依。"),
 ["点明时间", "渲染氛围", "铺垫"]),

(1, "[[断肠|形容极度悲痛。断肠，愁肠寸断，夸张手法]]人在[[天涯|天边，指极远的地方。天，天边；涯，边际]]。",
 "悲痛欲绝的游子，还漂泊在遥远的天边。",
 fixq("末句直抒胸臆，点明全曲主旨。~L~断肠人~R~指悲痛欲绝的游子，~L~断肠~R~二字用夸张手法，将游子的思乡之苦写到极致——不是一般的忧愁，而是愁肠寸断的悲痛。~L~在天涯~R~写游子漂泊之远，~L~天涯~R~即天边，极言距离之远。一个~L~在~R~字，写出了游子的孤独无依——他不是~L~归~R~，不是~L~回~R~，而是~L~在~R~，永远停留在漂泊的状态。这一句是全曲的点睛之笔，前面所有的意象都为这一句服务——枯藤老树的萧瑟、小桥流水的温馨、古道西风的艰辛、夕阳西下的苍茫，最终都汇聚到~L~断肠人在天涯~R~这七个字上。短短二十八字的小令，写尽了天涯游子的悲秋之情，被誉为~L~秋思之祖~R~，当之无愧。"),
 ["直抒胸臆", "夸张", "点睛之笔", "名句", "主旨"]),
]


DICT_WORDS = [
    {"w":"藤","py":"téng","q":"枯□老树昏鸦，小桥流水人家","tip":fixq("「藤」草字头，音 téng，藤蔓，植物的匍匐茎，勿写~L~腾~R~（奔腾，月字旁）")},
    {"w":"鸦","py":"yā","q":"枯藤老树昏□，小桥流水人家","tip":fixq("「鸦」鸟字旁，音 yā，乌鸦，~L~昏鸦~R~即黄昏归巢的乌鸦，勿写~L~鸭~R~（鸭子，甲字旁）")},
    {"w":"瘦","py":"shòu","q":"古道西风□马。夕阳西下","tip":fixq("「瘦」病字旁，音 shòu，瘦弱，~L~瘦马~R~即瘦弱的马，勿写~L~搜~R~（搜索，提手旁）")},
    {"w":"涯","py":"yá","q":"断肠人在天□","tip":fixq("「涯」三点水，音 yá，边际、尽头，~L~天涯~R~即天边，勿写~L~崖~R~（山崖，山字旁）")},
    {"w":"昏","py":"hūn","q":"枯藤老树□鸦，小桥流水人家","tip":fixq("「昏」日字底，音 hūn，黄昏、昏暗，~L~昏鸦~R~即黄昏时的乌鸦，勿写~L~婚~R~（结婚，女字旁）")},
    {"w":"断","py":"duàn","q":"□肠人在天涯","tip":fixq("「断」斤字旁，音 duàn，断开、断绝，~L~断肠~R~形容极度悲痛，勿写~L~段~R~（段落）")},
]

DICT_NOTES = [
    {"w":"枯藤","q":"枯藤老树昏鸦","a":"干枯的藤蔓。枯，干枯；藤，藤蔓"},
    {"w":"昏鸦","q":"枯藤老树昏鸦","a":"（hūn yā）黄昏时归巢的乌鸦。昏，黄昏；鸦，乌鸦"},
    {"w":"流水","q":"小桥流水人家","a":"流动的水。流，流动"},
    {"w":"人家","q":"小桥流水人家","a":"住户、人家，这里指桥边的村落"},
    {"w":"古道","q":"古道西风瘦马","a":"古老的道路。古，古老；道，道路"},
    {"w":"西风","q":"古道西风瘦马","a":"（xī fēng）秋风。古代以西方为秋，故称秋风为西风"},
    {"w":"瘦马","q":"古道西风瘦马","a":"（shòu mǎ）瘦弱的马。瘦，瘦弱"},
    {"w":"夕阳","q":"夕阳西下","a":"傍晚的太阳。夕，傍晚；阳，太阳"},
    {"w":"西下","q":"夕阳西下","a":"向西落下。西，向西；下，落下"},
    {"w":"断肠","q":"断肠人在天涯","a":"形容极度悲痛，愁肠寸断。夸张手法"},
    {"w":"天涯","q":"断肠人在天涯","a":"（tiān yá）天边，指极远的地方。涯，边际"},
    {"w":"列锦","q":"枯藤老树昏鸦","a":"修辞手法，纯用名词或名词性短语并列，不用动词，构成画面"},
]


def build_verses():
    out, idx = [], 0
    for pi, part in enumerate(PARTS):
        out.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>'
                   % (part[0], part[1], part[2]))
        out.append('      <div class="part-overview">%s</div>' % fixq(part[3]))
        for (p, txt, yi, shang, tags) in S:
            if p != pi:
                continue
            idx += 1
            out.append('      <div class="verse" id="l%d" data-i="%d">' % (idx, idx - 1))
            out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx, annotate(txt)))
            out.append('        <details class="v-more">')
            out.append('          <summary>译文 · 赏析</summary>')
            out.append('          <div class="d-body">')
            out.append('            <div class="v-sec"><b class="v-label">译　文</b>')
            out.append('              <div class="v-trans">%s</div>' % yi)
            out.append('            </div>')
            out.append('            <div class="v-sec"><b class="v-label">赏　析</b>')
            out.append('              <div class="d-body"><p>%s</p></div>' % shang)
            if tags:
                out.append('              <div class="tags">%s</div>' % ''.join('<span>%s</span>' % t for t in tags))
            out.append('            </div>')
            out.append('          </div>')
            out.append('        </details>')
            out.append('      </div>')
    return '\n'.join(out), idx


verses_html, total = build_verses()
full_html = '\n'.join('    <div class="pl">%s</div>' % p for p in FULLTEXT)
anno_count = sum(txt.count('[[') for (_, txt, _, _, _) in S)

BG = fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《天净沙·秋思》是元代戏曲家、散曲家马致远的代表作，被誉为~L~秋思之祖~R~。这首小令仅二十八字，却以凝练的语言、鲜明的意象、深沉的情感，写尽了天涯游子的悲秋之情，是中国古典诗歌中最著名的作品之一。</p>
    <p>全曲以~L~列锦~R~的手法，前三句各用三个名词性短语并列，推出九组意象：枯藤、老树、昏鸦、小桥、流水、人家、古道、西风、瘦马，不用一个动词，却构成了一幅萧瑟凄清的秋日黄昏图。末二句~L~夕阳西下，断肠人在天涯~R~直抒胸臆，点明主旨。全曲景中有情，情因景生，情景交融，是元曲小令的巅峰之作。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>马致远（约1250—约1321），字千里，号东篱，大都（今北京）人，元代著名戏曲家、散曲家，~L~元曲四大家~R~之一（与关汉卿、白朴、郑光祖并称）。他曾任江浙行省务官，晚年隐居，过着~L~酒中仙、尘外客~R~的闲适生活。</p>
    <p>马致远的散曲风格豪放洒脱，语言清丽，意境深远，被誉为~L~曲状元~R~。代表作有《天净沙·秋思》《汉宫秋》等。《天净沙·秋思》是他最著名的作品，被后人誉为~L~秋思之祖~R~，短短二十八字，写尽了天涯游子的悲秋之情。</p>
    <p class="note">※ 马致远与关汉卿、白朴、郑光祖并称~L~元曲四大家~R~，其散曲成就最高，被誉为~L~曲状元~R~。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>元代社会：</b>元朝是蒙古族建立的大一统王朝，民族矛盾和阶级矛盾尖锐。汉族文人地位低下，科举制度长期停废，许多文人漂泊江湖，靠写曲为生。马致远一生仕途不顺，漂泊在外，对游子的孤独和思乡之苦有深切的体会。</p>
    <p><b>散曲兴盛：</b>元代是散曲的黄金时代。散曲是一种新的诗歌形式，包括小令和套数两种。小令是单支曲子，形式短小，语言通俗，意境深远。《天净沙·秋思》就是一首越调·天净沙小令。</p>
    <p><b>悲秋传统：</b>中国文学有悠久的~L~悲秋~R~传统，从宋玉《九辩》~L~悲哉秋之为气也~R~开始，秋天就与悲伤、思乡联系在一起。马致远的《天净沙·秋思》继承了这一传统，并将其推向了极致。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《天净沙·秋思》是一首<b>元曲小令</b>。~L~天净沙~R~是曲牌名，属越调，句式为六六六、四六，共五句二十八字；~L~秋思~R~是题目，点明全曲的主题是秋日的思念。</p>
    <p>小令是散曲的一种，形式短小，通常只用一个曲牌，与词中的小令类似。但曲比词更自由，可以加衬字，语言更通俗。《天净沙·秋思》是小令中的杰作，前三句各用三个名词性短语并列（~L~列锦~R~手法），不用一个动词，却构成了完整的画面，是元曲艺术的典范。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>马致远《天净沙·秋思》朗诵</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1Yc411i7JY&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="天净沙秋思朗诵"></iframe>
        <a href="https://www.bilibili.com/video/BV1Yc411i7JY" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>【复原古曲 唱诗】《天净沙·秋思》马致远</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV17y4y1H7zL&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="天净沙秋思古曲复原"></iframe>
        <a href="https://www.bilibili.com/video/BV17y4y1H7zL" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>抒情主人公形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">断肠人——天涯漂泊的游子</div>
        <p>《天净沙·秋思》中的抒情主人公，是一位漂泊天涯、孤独愁苦的游子形象。他骑着瘦马，在古道上艰难前行，面对秋日黄昏的萧瑟景象，心中充满了思乡的悲愁。</p>
        <p><b>旅途的艰辛：</b>~L~古道西风瘦马~R~，古老的道路、萧瑟的秋风、瘦弱的马匹——马尚且如此瘦弱疲惫，游子的艰辛可想而知。~L~瘦马~R~的~L~瘦~R~字，不仅写马，也暗示游子的憔悴。</p>
        <p><b>孤独的处境：</b>~L~小桥流水人家~R~，别人有家可归，有温馨的生活，而自己却漂泊在天涯，无家可归。这种对比，使游子的孤独更加突出。</p>
        <p><b>断肠的悲痛：</b>~L~断肠人在天涯~R~，一个~L~断肠~R~，将游子的思乡之苦写到极致——不是一般的忧愁，而是愁肠寸断的悲痛。这个形象，是中国文学中最动人的游子形象之一，千百年来引起了无数漂泊者的共鸣。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">列锦手法——名词并置，不用动词</div>
        <p>前三句各用三个名词性短语并列：~L~枯藤老树昏鸦~R~~L~小桥流水人家~R~~L~古道西风瘦马~R~，九组意象，不用一个动词，却构成了三幅完整的画面。这种~L~列锦~R~的手法，给读者留下了广阔的想象空间，也使意象更加鲜明突出。读者可以根据自己的生活经验，将这些意象组合成完整的画面，产生强烈的艺术感染力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比反衬——以乐景写哀情</div>
        <p>~L~枯藤老树昏鸦~R~的萧瑟与~L~小桥流水人家~R~的温馨形成鲜明对比。人家的温馨，对漂泊的游子来说，不是慰藉，而是更深的刺激——别人有家可归，自己却漂泊天涯。以乐景写哀情，倍增其哀。这种对比反衬的手法，使游子的孤独和愁苦更加突出。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">情景交融——景中有情，情因景生</div>
        <p>全曲没有一句直接抒情（直到末句才直抒胸臆），但前三句的景物描写中处处含情。枯藤、老树、昏鸦、古道、西风、瘦马，这些意象本身就带有萧瑟、凄凉的感情色彩，与游子的悲愁心境相契合。末句~L~断肠人在天涯~R~直抒胸臆，将前面的景物描写与情感抒发融为一体，情景交融，天衣无缝。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">枯藤老树昏鸦，小桥流水人家，古道西风瘦马。</div>
        <p>这三句是全曲最著名的部分，也是中国古典诗歌中最经典的意象组合之一。九组名词性短语并列，不用一个动词，却构成了三幅画面：萧瑟的秋景、温馨的人家、艰辛的旅途。三组意象一冷一暖一苦，对比鲜明，为末句~L~断肠人在天涯~R~做了充分的铺垫。这种~L~列锦~R~手法，使语言极度凝练，意象极度鲜明，给读者留下了广阔的想象空间，被誉为~L~寥寥数语，深得唐人绝句妙境~R~。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">夕阳西下，断肠人在天涯。</div>
        <p>这两句是全曲的点睛之笔。~L~夕阳西下~R~点明时间，将前三句的意象统一在黄昏的背景之下，渲染出苍茫凄清的氛围。~L~断肠人在天涯~R~直抒胸臆，点明全曲主旨——漂泊天涯的游子，在秋日黄昏中愁肠寸断。~L~断肠~R~二字用夸张手法，将游子的思乡之苦写到极致。一个~L~在~R~字，写出了游子的孤独无依——他不是归，不是回，而是永远停留在漂泊的状态。这两句与前三句的景物描写融为一体，情景交融，使全曲的情感达到高潮。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《天净沙·秋思》通过描写秋日黄昏的萧瑟景象，抒发了天涯游子漂泊无依、思念家乡的深切悲愁，表达了对故乡的眷恋和对漂泊生活的厌倦。</p>
    <p>这首小令的深刻之处在于，它不仅写了一个游子的思乡之情，更写出了人类普遍的孤独感和归属感的渴望。~L~断肠人在天涯~R~，不仅仅是马致远一个人的感受，而是所有漂泊者的共同心声。千百年来，这首小令以其凝练的语言、鲜明的意象、深沉的情感，感动了无数读者，被誉为~L~秋思之祖~R~，成为中国古典诗歌中最著名的作品之一。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">曲牌 · 字音形 · 文言 · 意象 · 修辞 · 文化常识</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>文体与词牌</h3>
      <div class="acc-item"><span class="acc-w">元曲小令</span><span class="acc-d">《天净沙·秋思》是元曲小令，~L~天净沙~R~是曲牌名，属越调；~L~秋思~R~是题目。小令是散曲的一种，形式短小，单支曲子。</span></div>
      <div class="acc-item"><span class="acc-w">天净沙曲牌</span><span class="acc-d">越调曲牌，句式为六六六、四六，共五句二十八字，平韵。第一、二、三句可对，第四句可仄收，第五句平收。</span></div>
      <div class="acc-item"><span class="acc-w">散曲</span><span class="acc-d">元代新兴的诗歌形式，包括小令和套数。小令是单支曲子，套数是多支曲子联缀。散曲语言通俗，可加衬字，比词更自由。</span></div>
      <div class="acc-item"><span class="acc-w">元曲四大家</span><span class="acc-d">指关汉卿、白朴、马致远、郑光祖四位元代戏曲家。马致远被誉为~L~曲状元~R~，散曲成就最高。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>易错字音形</h3>
      <div class="acc-item"><span class="acc-w">藤</span><span class="acc-d">（téng）藤蔓，草字头，勿写~L~腾~R~（月字旁）。</span></div>
      <div class="acc-item"><span class="acc-w">鸦</span><span class="acc-d">（yā）乌鸦，鸟字旁，勿写~L~鸭~R~（甲字旁）。</span></div>
      <div class="acc-item"><span class="acc-w">瘦</span><span class="acc-d">（shòu）瘦弱，病字旁，勿写~L~搜~R~（提手旁）。</span></div>
      <div class="acc-item"><span class="acc-w">涯</span><span class="acc-d">（yá）边际，三点水，勿写~L~崖~R~（山字旁）。</span></div>
      <div class="acc-item"><span class="acc-w">昏</span><span class="acc-d">（hūn）黄昏，日字底，勿写~L~婚~R~（女字旁）。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文言梳理</h3>
      <div class="acc-sub">古今异义</div>
      <div class="tw"><table>
        <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
        <tr><td class="kai">人家</td><td>住户、村落</td><td>别人的家庭</td><td>小桥流水人家</td></tr>
        <tr><td class="kai">西风</td><td>秋风（古代以西方为秋）</td><td>从西边吹来的风</td><td>古道西风瘦马</td></tr>
        <tr><td class="kai">天涯</td><td>天边，极远的地方</td><td>天边（引申为距离远）</td><td>断肠人在天涯</td></tr>
      </table></div>
      <div class="acc-sub">词类活用</div>
      <div class="tw"><table>
        <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
        <tr><td class="kai">西</td><td>名词作状语</td><td>向西</td><td>夕阳西下</td></tr>
      </table></div>
      <div class="acc-sub">文言句式</div>
      <div class="tw"><table>
        <tr><th>句式</th><th>例句</th><th>说明</th></tr>
        <tr><td class="kai">列锦（名词并置）</td><td>枯藤老树昏鸦</td><td>纯用名词性短语并列，不用动词，构成画面</td></tr>
        <tr><td class="kai">省略句</td><td>（瘦马驮着）断肠人在天涯</td><td>承前省略，~L~瘦马~R~与~L~断肠人~R~的关系暗含其中</td></tr>
      </table></div>
    </div>
  </div>

  <div class="box">
    <h3>意象赏析（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>枯藤·老树·昏鸦</dt><dd>三组萧瑟意象，构成秋日黄昏的凄清画面。~L~枯~R~~L~老~R~~L~昏~R~三个修饰词，渲染出衰败、昏暗的氛围。~L~昏鸦~R~归巢，暗含~L~鸟尚有归处，人却漂泊无依~R~的对比。</dd></div>
      <div class="g-item"><dt>小桥·流水·人家</dt><dd>三组温馨意象，构成江南水乡的宁静画面。与上一句的萧瑟形成对比，以乐景写哀情——别人有家可归，自己却漂泊天涯，倍增其哀。</dd></div>
      <div class="g-item"><dt>古道·西风·瘦马</dt><dd>三组苍凉意象，写出游子旅途的艰辛。~L~古道~R~荒凉，~L~西风~R~寒冷，~L~瘦马~R~疲惫——马尚且如此，人何以堪？~L~瘦~R~字双关，既写马瘦，也暗示人瘦。</dd></div>
      <div class="g-item"><dt>夕阳</dt><dd>黄昏的意象，点明时间，渲染苍茫凄清的氛围。~L~日暮乡关何处是~R~，黄昏总是与思乡联系在一起，是中国古典诗歌中最常见的思乡意象。</dd></div>
      <div class="g-item"><dt>断肠人</dt><dd>全曲的核心意象，指悲痛欲绝的游子。~L~断肠~R~用夸张手法，将思乡之苦写到极致。~L~在天涯~R~写漂泊之远，一个~L~在~R~字，写出了永远漂泊的孤独感。</dd></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞与手法</h3>
      <div class="acc-item"><span class="acc-w">列锦</span><span class="acc-d">前三句纯用名词性短语并列，不用动词，构成画面，是元曲经典手法。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">~L~枯藤老树昏鸦~R~的萧瑟与~L~小桥流水人家~R~的温馨对比。</span></div>
      <div class="acc-item"><span class="acc-w">反衬（以乐景写哀）</span><span class="acc-d">人家的温馨反衬游子的孤独，倍增其哀。</span></div>
      <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">~L~断肠~R~形容极度悲痛，愁肠寸断。</span></div>
      <div class="acc-item"><span class="acc-w">情景交融</span><span class="acc-d">景中有情，情因景生，前三句写景，末句抒情，融为一体。</span></div>
    </div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>曲牌名</dt><dd>曲的曲调名称，如~L~天净沙~R~。曲牌规定了曲子的句式、字数、平仄、押韵等格律。与词牌类似，但曲比词更自由，可加衬字。</dd></div>
      <div class="g-item"><dt>越调</dt><dd>元曲的宫调之一，曲调风格悠扬。~L~天净沙~R~属越调。元曲有六宫十一调，不同宫调有不同的情感色彩。</dd></div>
      <div class="g-item"><dt>秋思之祖</dt><dd>后人对《天净沙·秋思》的美誉。王国维《人间词话》评此曲~L~寥寥数语，深得唐人绝句妙境~R~。</dd></div>
      <div class="g-item"><dt>悲秋传统</dt><dd>中国文学中以秋天为背景抒发悲伤情感的传统，始于宋玉《九辩》~L~悲哉秋之为气也~R~。马致远的《天净沙·秋思》是这一传统的巅峰之作。</dd></div>
      <div class="g-item"><dt>鸿雁传书</dt><dd>古代传说大雁可以传递书信。但本曲中~L~昏鸦~R~不是鸿雁，而是乌鸦，乌鸦归巢与游子无归形成对比。</dd></div>
      <div class="g-item"><dt>元曲</dt><dd>元代文学的代表形式，包括杂剧和散曲。杂剧是戏曲，散曲是诗歌。散曲又分小令和套数。《天净沙·秋思》是小令。</dd></div>
    </div>
  </div>

</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《天净沙·秋思》马致远</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">元 · 马致远</div>
  <h1 class="hero-title">天净沙·秋思</h1>
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
  <div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>
  <div class="sec-sub">全曲五句二十八字，分两部分：秋景三联、夕阳断肠。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《天净沙·秋思》</div>
  <div>马致远 · 元（约1250—约1321）· 号东篱，~L~曲状元~R~ · 越调·天净沙小令</div>
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
print('OK', OUT, 'verses=', total, 'anno=', anno_count, 'words=', len(DICT_WORDS), 'notes=', len(DICT_NOTES))
