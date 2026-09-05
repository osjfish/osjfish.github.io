# -*- coding: utf-8 -*-
"""《登飞来峰》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。
中文引号用 ~L~ / ~R~ 占位，生成前替换为 \u201c / \u201d。
注释格式：[[词|（拼音）释义]]，原文纯净，拼音在 data-note 里。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'dengfeilaifeng-wanganshi.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'dengfeilaifeng_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "飞来山上千寻塔，闻说鸡鸣见日升。",
    "不畏浮云遮望眼，自缘身在最高层。",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "登高望远 · 鸡鸣日升", "第 1–2 句",
     fixq("首句~L~飞来山上千寻塔~R~，点出飞来峰和峰顶高塔，~L~千寻~R~以夸张写塔之高。次句~L~闻说鸡鸣见日升~R~，虚写在高塔上雄鸡报晓时便能看到日出的壮丽景象，以~L~闻说~R~二字点明是传闻，虚实结合，进一步烘托塔的高峻。两句写景，为下文抒怀蓄势。")),
    ("第二部分", "借景抒怀 · 站高望远", "第 3–4 句",
     fixq("后两句由写景转入抒怀，是全诗的主旨所在。~L~不畏浮云遮望眼~R~，~L~浮云~R~既是眼前实景，又比喻奸佞小人或困难障碍；~L~不畏~R~二字，写出诗人的坚定与自信。~L~自缘身在最高层~R~，点明~L~不畏~R~的原因——因为自己站在最高处，所以不怕浮云遮挡视线。这两句蕴含着~L~站得高，看得远~R~的深刻哲理，也表达了诗人高瞻远瞩、不畏奸邪的政治抱负和进取精神。")),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
# ===== 第一部分：登高望远 =====
(0, "飞来山上千[[寻|（xún）古代长度单位，八尺（一说七尺）为一寻。~L~千寻~R~形容极高，是夸张说法]]塔，",
 "飞来峰上有一座极高的塔，",
 fixq("首句点题，~L~飞来山上千寻塔~R~，七个字交代了地点（飞来山）、事物（塔）和特征（千寻）。~L~飞来峰~R~在今浙江杭州西湖灵隐寺前，相传东晋时印度僧人慧理登此山，叹曰：~L~此乃中天竺国灵鹫山之小岭，不知何以飞来？~R~因名飞来峰。~L~千寻~R~是古代长度单位，八尺（一说七尺）为一寻，~L~千寻~R~即八千尺，是夸张说法，形容塔极高。以~L~千寻~R~写塔高，为下文~L~鸡鸣见日升~R~和~L~身在最高层~R~做了铺垫——正因为塔极高，才能在鸡鸣时看到日出，才能站在最高层不畏浮云。"),
 ["点题", "夸张", "铺垫"]),

(0, "[[闻说|听说。闻，听；说，言说、传说]]鸡鸣见日升。",
 "听说在鸡鸣时分，从塔上就能看到太阳升起。",
 fixq("~L~闻说鸡鸣见日升~R~，是虚写——诗人并没有真的在鸡鸣时分登塔看日出，而是~L~闻说~R~（听说）有这样的景象。~L~闻说~R~二字，点明这是传闻，是虚写。但正是这虚写的景象，进一步烘托了塔的高峻——塔高到了在鸡鸣时分（天还未大亮）就能看到日出的程度。~L~鸡鸣~R~是天将亮未亮之时，~L~见日升~R~是看到日出，在通常情况下，地面上的人要等到天大亮才能看到日出，而在高塔上，鸡鸣时分就能看到，足见塔之高。这一句虚实结合，以虚写实，既写出了塔的高峻，又为下文的哲理抒怀蓄势。"),
 ["虚写", "虚实结合", "烘托"]),

# ===== 第二部分：借景抒怀 =====
(1, "不畏[[浮云|（fú yún）飘浮的云彩。诗中既是眼前实景，又比喻奸佞小人或困难障碍]]遮[[望眼|远望的视线。望，向远处看；眼，眼睛、视线]]，",
 "不怕飘浮的云彩遮住我远望的视线，",
 fixq("~L~不畏浮云遮望眼~R~，是全诗的转折，由写景转入抒怀。~L~浮云~R~一语双关，既是诗人登高时眼前看到的实景（山间飘浮的云彩），又比喻朝廷中的奸佞小人或人生道路上的困难障碍。在中国古典诗歌中，~L~浮云蔽日~R~是一个常见的比喻，比喻奸佞小人蒙蔽君主、陷害忠良。如西汉陆贾《新语》：~L~邪臣之蔽贤，犹浮云之障日月也。~R~李白《登金陵凤凰台》：~L~总为浮云能蔽日，长安不见使人愁。~R~王安石在这里反用其意——~L~不畏~R~浮云遮望眼，一个~L~不畏~R~，写出了诗人的坚定与自信，他不怕奸佞小人的阻挠，不怕困难障碍的遮挡。~L~遮望眼~R~的~L~望眼~R~，既是远望的视线，又暗指政治上的远见卓识。这一句为下句~L~自缘身在最高层~R~的哲理点明做了铺垫。"),
 ["一语双关", "比喻", "转折", "用典"]),

(1, "[[自缘|只因为。自，只；缘，因为]]身在最高层。",
 "只因为我自己站在最高的地方。",
 fixq("~L~自缘身在最高层~R~，是全诗的点睛之笔，也是千古传诵的哲理名句。~L~自缘~R~即只因为，~L~自~R~是只的意思，~L~缘~R~是因为的意思。这一句点明了~L~不畏浮云遮望眼~R~的原因——因为自己站在最高处，所以不怕浮云遮挡视线。这两句诗蕴含着深刻的哲理：~L~站得高，看得远~R~，只有站在最高处，才能不被浮云遮挡视线，才能看得更远、更清楚。在政治上，这意味着只有具备高远的志向和开阔的胸襟，才能不被眼前的困难和奸佞的阻挠所迷惑，才能高瞻远瞩、明辨是非。这首诗写于王安石三十岁左右，当时他初入仕途，正值意气风发之时，这两句诗既是他个人胸怀的写照，也预示了他后来推行变法、不畏艰难的政治家风范。~L~身在最高层~R~的~L~最高层~R~，既是指塔的最高层，又是指政治上的最高境界和人生的最高追求。这两句诗与苏轼《题西林壁》~L~不识庐山真面目，只缘身在此山中~R~有异曲同工之妙——王安石说~L~身在最高层~R~所以不畏浮云，苏轼说~L~身在此山中~R~所以不识真面目，一正一反，都蕴含着深刻的哲理，可对照阅读。"),
 ["哲理", "点睛之笔", "名句", "对比"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"寻","py":"xún","q":"飞来山上千□塔，闻说鸡鸣见日升","tip":fixq("「寻」此处读 xún，古代长度单位，八尺为一寻，~L~千寻~R~形容极高，勿读 xín")},
    {"w":"浮","py":"fú","q":"不畏□云遮望眼，自缘身在最高层","tip":fixq("「浮」三点水，音 fú，飘浮，勿写~L~俘~R~（俘虏）~L~蜉~R~（蜉蝣）")},
    {"w":"遮","py":"zhē","q":"不畏浮云□望眼，自缘身在最高层","tip":fixq("「遮」走之底（辶），音 zhē，遮挡，勿写~L~蔗~R~（甘蔗）~L~鹧~R~（鹧鸪）")},
    {"w":"缘","py":"yuán","q":"不畏浮云遮望眼，自□身在最高层","tip":fixq("「缘」绞丝旁，音 yuán，因为，勿写~L~原~R~（原来）~L~源~R~（水源）")},
    {"w":"峰","py":"fēng","q":"飞来□上千寻塔，闻说鸡鸣见日升","tip":fixq("「峰」山字旁，音 fēng，山峰，勿写~L~锋~R~（刀锋）~L~蜂~R~（蜜蜂）")},
    {"w":"升","py":"shēng","q":"飞来山上千寻塔，闻说鸡鸣见日□","tip":fixq("「升」撇字头，音 shēng，上升，勿写~L~生~R~（生命）~L~声~R~（声音）")},
    {"w":"畏","py":"wèi","q":"不□浮云遮望眼，自缘身在最高层","tip":fixq("「畏」田字底，音 wèi，害怕，勿写~L~喂~R~（喂养）~L~偎~R~（依偎）")},
    {"w":"塔","py":"tǎ","q":"飞来山上千寻□，闻说鸡鸣见日升","tip":fixq("「塔」土字旁，音 tǎ，佛教建筑，勿写~L~搭~R~（搭配）~L~嗒~R~（嘀嗒）")},
]

DICT_NOTES = [
    {"w":"千寻","q":"飞来山上千寻塔","a":"形容极高。寻，xún，古代长度单位，八尺（一说七尺）为一寻；~L~千寻~R~是夸张说法"},
    {"w":"闻说","q":"闻说鸡鸣见日升","a":"听说。闻，听；说，言说、传说"},
    {"w":"鸡鸣","q":"闻说鸡鸣见日升","a":"雄鸡报晓，指天将亮未亮之时"},
    {"w":"见日升","q":"闻说鸡鸣见日升","a":"看到日出。形容塔极高，在鸡鸣时分就能看到日出"},
    {"w":"不畏","q":"不畏浮云遮望眼","a":"不怕。畏，wèi，害怕"},
    {"w":"浮云","q":"不畏浮云遮望眼","a":"飘浮的云彩。诗中一语双关，既是眼前实景，又比喻奸佞小人或困难障碍"},
    {"w":"遮","q":"不畏浮云遮望眼","a":"遮挡、遮蔽。读 zhē"},
    {"w":"望眼","q":"不畏浮云遮望眼","a":"远望的视线。望，向远处看；眼，眼睛、视线。暗指政治上的远见卓识"},
    {"w":"自缘","q":"自缘身在最高层","a":"只因为。自，只；缘，因为"},
    {"w":"最高层","q":"自缘身在最高层","a":"最高的地方。既指塔的最高层，又指政治上的最高境界和人生的最高追求"},
]


# ---------------- 组装 ----------------
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
    <p>《登飞来峰》是北宋政治家、文学家王安石的名篇，作于宋仁宗皇祐二年（1050）前后。当时王安石三十岁左右，初入仕途，任鄞县（今浙江宁波）知县，途经杭州飞来峰，登高望远，写下了这首千古传诵的七言绝句。</p>
    <p>全诗仅二十八字，却蕴含着深刻的哲理。前两句写景，以~L~千寻塔~R~和~L~鸡鸣见日升~R~写塔之高峻；后两句抒怀，~L~不畏浮云遮望眼，自缘身在最高层~R~，由登高望远生发哲理，表达了诗人高瞻远瞩、不畏奸邪的政治抱负和进取精神。这首诗是王安石早期的代表作，也是他后来推行变法、不畏艰难的政治家风范的先声。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>王安石（1021—1086），字介甫，号半山，抚州临川（今江西抚州）人。北宋著名的政治家、思想家、文学家、改革家，~L~唐宋八大家~R~之一。封荆国公，世称~L~王荆公~R~。谥号~L~文~R~，故又称~L~王文公~R~。</p>
    <p>王安石在政治上主持了著名的~L~王安石变法~R~（熙宁变法），推行青苗法、募役法、方田均税法等一系列改革措施，旨在富国强兵，改变北宋积贫积弱的局面。变法虽然最终失败，但对北宋乃至后世产生了深远影响。</p>
    <p>在文学上，王安石的散文雄健峭拔，诗歌遒劲清新，词作虽不多但风格高峻。代表作有《泊船瓜洲》《元日》《梅花》《登飞来峰》《伤仲永》《游褒禅山记》等。其诗~L~春风又绿江南岸，明月何时照我还~R~~L~遥知不是雪，为有暗香来~R~等都是千古传诵的名句。</p>
    <p class="note">※ 《登飞来峰》写于王安石三十岁左右，正值他初入仕途、意气风发之时。诗中~L~不畏浮云遮望眼，自缘身在最高层~R~的豪情，与他后来推行变法、不畏艰难的政治家风范一脉相承。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>北宋积贫积弱：</b>北宋建立后，虽然经济文化繁荣，但在军事上积弱不振，对辽和西夏的战争屡屡失利，每年要付出大量~L~岁币~R~。同时，官僚机构臃肿，军队庞大，财政困难，史称~L~积贫积弱~R~。年轻的王安石对此有清醒的认识，立志改革。</p>
    <p><b>初入仕途：</b>王安石于庆历二年（1042）考中进士，时任淮南判官，后任鄞县知县。在鄞县任上，他兴修水利、放贷青苗，积累了丰富的地方治理经验，也为后来的变法奠定了实践基础。《登飞来峰》即作于这一时期。</p>
    <p><b>飞来峰：</b>飞来峰在今浙江杭州西湖灵隐寺前，是一座石灰岩山峰，高约二百米。相传东晋咸和元年（326），印度僧人慧理登此山，叹曰：~L~此乃中天竺国灵鹫山之小岭，不知何以飞来？~R~因名飞来峰。峰上有塔，名~L~飞来峰塔~R~（已毁），王安石登的就是这座塔。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《登飞来峰》是一首<b>七言绝句</b>，全诗四句，每句七字，共二十八字。首句入韵（~L~塔~R~字不入韵，首句可押可不押），二、四句押韵（~L~升~R~~L~层~R~同属下平声十蒸韵）。全诗格律严谨，是七言绝句的典范之作。</p>
    <p>这首诗的结构是典型的~L~起承转合~R~：首句~L~飞来山上千寻塔~R~起，点题写景；次句~L~闻说鸡鸣见日升~R~承，继续写景、烘托塔高；第三句~L~不畏浮云遮望眼~R~转，由写景转入抒怀；第四句~L~自缘身在最高层~R~合，点明主旨、升华哲理。起承转合，章法井然。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>诵读客朗诵王安石《登飞来峰》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1H2kAYtEvo&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="诵读客朗诵《登飞来峰》"></iframe>
        <a href="https://www.bilibili.com/video/BV1H2kAYtEvo" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>深度解读王安石《登飞来峰》——什么样的人才算有先见之明</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1nHRuBaE26&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="深度解读《登飞来峰》"></iframe>
        <a href="https://www.bilibili.com/video/BV1nHRuBaE26" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">青年王安石——高瞻远瞩的改革家</div>
        <p>《登飞来峰》中的抒情主人公，是一个高瞻远瞩、胸怀大志、坚定自信的青年政治家形象。</p>
        <p><b>登高望远的视野：</b>诗人登上飞来峰上的千寻高塔，站在最高处，俯瞰群山，远望日出。~L~千寻塔~R~的高，~L~鸡鸣见日升~R~的远，都衬托出诗人视野的开阔。他不是站在平地上仰望，而是站在最高处俯视——这种~L~身在最高层~R~的姿态，正是一个政治家高瞻远瞩的象征。</p>
        <p><b>不畏浮云的坚定：</b>~L~不畏浮云遮望眼~R~，一个~L~不畏~R~，写出了诗人的坚定与自信。~L~浮云~R~比喻奸佞小人或困难障碍，诗人不怕它们的遮挡和阻挠。这种~L~不畏~R~的精神，正是一个改革家必备的品格——王安石后来推行变法，遭到保守派的强烈反对，但他始终不改其志，这种精神在这首早期的诗中已经显露无遗。</p>
        <p><b>身在最高层的自信：</b>~L~自缘身在最高层~R~，诗人之所以~L~不畏浮云~R~，是因为他~L~身在最高层~R~。这个~L~最高层~R~，既是塔的最高层，又是政治上的最高境界和人生的最高追求。诗人相信，只要自己站得高、看得远，就不会被眼前的困难和奸佞的阻挠所迷惑。这种自信，来自于他对自己政治理想的坚定信念，也来自于他对国家前途的深刻洞察。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">借景抒怀，寓理于景</div>
        <p>《登飞来峰》最大的艺术特色，是借景抒怀、寓理于景。全诗前两句写景，后两句抒怀，但景与情、景与理不是割裂的，而是水乳交融的。</p>
        <p>前两句写飞来峰上的千寻高塔，写鸡鸣时分在塔上看到日出的景象。这些景物描写不是为写景而写景，而是为下文的哲理抒怀做铺垫——正因为塔~L~千寻~R~之高，才能~L~鸡鸣见日升~R~；正因为站在~L~最高层~R~，才能~L~不畏浮云遮望眼~R~。景是理的基础，理是景的升华。</p>
        <p>后两句~L~不畏浮云遮望眼，自缘身在最高层~R~，表面上是写登高望远的感受，实际上蕴含着深刻的人生哲理和政治抱负。~L~浮云~R~既是眼前的实景，又比喻奸佞小人；~L~最高层~R~既是塔的最高处，又比喻政治上的高远境界。这种一语双关、寓理于景的手法，使诗歌既形象生动，又意蕴深远，读后令人回味无穷。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">一语双关——浮云的比喻义</div>
        <p>~L~浮云~R~是这首诗中最关键的意象，它一语双关，既有字面意义，又有比喻意义。</p>
        <p><b>字面意义：</b>~L~浮云~R~就是飘浮的云彩，是诗人登高时眼前看到的实景。山间云雾缭绕，飘浮的云彩可能会遮挡视线，这是登高时常见的自然现象。</p>
        <p><b>比喻意义：</b>在中国古典诗歌中，~L~浮云蔽日~R~是一个常见的比喻，比喻奸佞小人蒙蔽君主、陷害忠良。这个比喻最早见于西汉陆贾《新语》：~L~邪臣之蔽贤，犹浮云之障日月也。~R~后来李白《登金陵凤凰台》~L~总为浮云能蔽日，长安不见使人愁~R~，用的就是这个比喻。王安石在这里反用其意——李白因~L~浮云蔽日~R~而~L~愁~R~，王安石却~L~不畏~R~浮云遮望眼，因为他~L~身在最高层~R~。这种反用，既体现了王安石的创新精神，也表达了他不同于李白的坚定与自信。</p>
        <p><b>引申意义：</b>~L~浮云~R~还可以引申为人生道路上的困难障碍、名缰利锁、世俗偏见等。~L~不畏浮云遮望眼~R~，就是不怕这些困难和障碍的遮挡，始终保持清醒的头脑和远大的目光。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">起承转合，章法井然</div>
        <p>《登飞来峰》是七言绝句~L~起承转合~R~结构的典范：</p>
        <p><b>起（首句）：</b>~L~飞来山上千寻塔~R~，点题写景，交代地点和事物，以~L~千寻~R~写塔之高，为全诗奠定~L~高~R~的基调。</p>
        <p><b>承（次句）：</b>~L~闻说鸡鸣见日升~R~，承接首句，继续写景，以~L~鸡鸣见日升~R~进一步烘托塔的高峻，~L~闻说~R~二字点明是虚写，虚实结合。</p>
        <p><b>转（第三句）：</b>~L~不畏浮云遮望眼~R~，笔锋一转，由写景转入抒怀，~L~不畏~R~二字引出诗人的坚定态度，~L~浮云~R~一语双关，为下文的哲理点明蓄势。</p>
        <p><b>合（末句）：</b>~L~自缘身在最高层~R~，收束全诗，点明~L~不畏~R~的原因，升华哲理，~L~最高层~R~一语双关，余味无穷。</p>
        <p>起承转合，四句之间环环相扣、层层递进，章法井然，是七言绝句的典范之作。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">不畏浮云遮望眼，自缘身在最高层。</div>
        <p>全诗的点睛之笔，也是千古传诵的哲理名句。这两句诗表面上是写登高望远的感受——不怕浮云遮挡视线，只因为自己站在最高处。实际上蕴含着深刻的哲理：~L~站得高，看得远~R~，只有站在最高处，才能不被浮云遮挡视线，才能看得更远、更清楚。</p>
        <p>在政治上，这两句诗意味着：只有具备高远的志向和开阔的胸襟，才能不被眼前的困难和奸佞的阻挠所迷惑，才能高瞻远瞩、明辨是非。~L~浮云~R~比喻奸佞小人或困难障碍，~L~最高层~R~比喻政治上的高远境界。王安石写这首诗时三十岁左右，初入仕途，这两句诗既是他个人胸怀的写照，也预示了他后来推行变法、不畏艰难的政治家风范。</p>
        <p>这两句诗与苏轼《题西林壁》~L~不识庐山真面目，只缘身在此山中~R~有异曲同工之妙，可对照阅读：王安石说~L~身在最高层~R~所以不畏浮云，强调的是~L~站得高~R~；苏轼说~L~身在此山中~R~所以不识真面目，强调的是~L~跳出局~R~。一正一反，都蕴含着深刻的哲理，都是中国古典诗歌中哲理诗的典范。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>与苏轼《题西林壁》对比</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">两首哲理诗的对照阅读</div>
        <p>王安石《登飞来峰》和苏轼《题西林壁》是北宋两首最著名的哲理诗，都写登高望远，都蕴含深刻哲理，可对照阅读：</p>
        <p><b>王安石《登飞来峰》：</b>~L~不畏浮云遮望眼，自缘身在最高层。~R~强调的是~L~站得高，看得远~R~——只要站在最高处，就不怕浮云遮挡视线。这是一种~L~入世~R~的哲学，强调积极进取、勇攀高峰、高瞻远瞩。</p>
        <p><b>苏轼《题西林壁》：</b>~L~不识庐山真面目，只缘身在此山中。~R~强调的是~L~当局者迷，旁观者清~R~——因为自己身在山中，所以看不到山的全貌。这是一种~L~超脱~R~的哲学，强调跳出局外、换位思考、全面客观。</p>
        <p><b>对比：</b>两首诗一正一反，一个说~L~身在最高层~R~所以看得远，一个说~L~身在此山中~R~所以看不清。王安石的~L~最高层~R~是主动攀登的结果，苏轼的~L~此山中~R~是被动局限的状态。一个强调~L~进~R~（积极进取），一个强调~L~出~R~（超脱局外）。两首诗从不同角度揭示了认识事物的规律，都具有永恒的哲理价值。有趣的是，王安石和苏轼在政治上是变法派和保守派的代表，但在文学上却各有千秋，两首哲理诗交相辉映，成为中国文学史上的佳话。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《登飞来峰》通过描写诗人登上飞来峰高塔、登高望远的所见所感，表达了诗人高瞻远瞩、不畏奸邪的政治抱负和积极进取的人生态度，蕴含着~L~站得高，看得远~R~的深刻哲理。</p>
    <p>这首诗的深刻之处在于，它不仅是一首写景诗，更是一首哲理诗和政治抒情诗。诗人以~L~登飞来峰~R~为题，却不止于写登峰——飞来峰的高塔，正是诗人心中崇高理想的象征；~L~不畏浮云遮望眼~R~的坚定，正是诗人面对政治困难和奸佞阻挠时的态度；~L~自缘身在最高层~R~的自信，正是诗人对自己政治理想和远见卓识的信念。这首诗写于王安石的青年时期，是他一生积极进取、不畏艰难精神的起点，也是他后来推行变法的政治宣言的先声。千百年来，~L~不畏浮云遮望眼，自缘身在最高层~R~这两句诗激励着无数人勇攀高峰、追求真理，成为中华民族精神的重要象征。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">古今异义 · 一词多义 · 修辞 · 文化常识</span></div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">寻</td><td>古代长度单位，八尺为一寻</td><td>寻找、寻求</td><td>飞来山上千寻塔</td></tr>
      <tr><td class="kai">闻</td><td>听、听说</td><td>用鼻子嗅气味</td><td>闻说鸡鸣见日升</td></tr>
      <tr><td class="kai">缘</td><td>因为</td><td>缘分、边缘、缘故</td><td>自缘身在最高层</td></tr>
      <tr><td class="kai">自</td><td>只、仅仅</td><td>自己、自然</td><td>自缘身在最高层</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>一词多义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="2">寻</td><td>古代长度单位（xún）</td><td>飞来山上千寻塔</td></tr>
      <tr><td>寻找、寻求（xún）</td><td>寻向所志（《桃花源记》）</td></tr>
      <tr><td class="kai" rowspan="2">闻</td><td>听、听说（wén）</td><td>闻说鸡鸣见日升</td></tr>
      <tr><td>闻名、著称（wén）</td><td>不求闻达于诸侯（《出师表》）</td></tr>
      <tr><td class="kai" rowspan="2">缘</td><td>因为（yuán）</td><td>自缘身在最高层</td></tr>
      <tr><td>沿着、顺着（yuán）</td><td>缘溪行（《桃花源记》）</td></tr>
      <tr><td class="kai" rowspan="2">遮</td><td>遮挡、遮蔽（zhē）</td><td>不畏浮云遮望眼</td></tr>
      <tr><td>通~L~庶~R~，众多（zhè）</td><td>（罕见用法）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>修辞方法</h3>
    <div class="glossary">
      <div class="g-item"><dt>夸张</dt><dd>~L~飞来山上千寻塔~R~，~L~千寻~R~是夸张说法，形容塔极高。古代八尺为一寻，千寻即八千尺，实际飞来峰塔并没有这么高，诗人用夸张手法突出塔的高峻，为下文的哲理抒怀做铺垫。</dd></div>
      <div class="g-item"><dt>一语双关</dt><dd>~L~不畏浮云遮望眼~R~中的~L~浮云~R~，既是眼前实景（飘浮的云彩），又比喻奸佞小人或困难障碍；~L~自缘身在最高层~R~中的~L~最高层~R~，既是塔的最高层，又比喻政治上的高远境界。一语双关，使诗歌意蕴深远。</dd></div>
      <div class="g-item"><dt>用典（反用）</dt><dd>~L~浮云~R~的比喻源自西汉陆贾《新语》~L~邪臣之蔽贤，犹浮云之障日月也~R~，李白《登金陵凤凰台》~L~总为浮云能蔽日，长安不见使人愁~R~用的就是这个典故。王安石反用其意——李白因浮云蔽日而愁，王安石却不畏浮云遮眼，因为他身在最高层。反用典故，体现了王安石的创新精神和坚定自信。</dd></div>
      <div class="g-item"><dt>虚实结合</dt><dd>首句~L~飞来山上千寻塔~R~是实写，写眼前的实景；次句~L~闻说鸡鸣见日升~R~是虚写，~L~闻说~R~二字点明是听说的传闻，并非诗人亲眼所见。虚实结合，以虚写实，进一步烘托了塔的高峻。</dd></div>
    </div>
  </div>

  <div class="box">
    <h3>哲理赏析（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>站得高，看得远</dt><dd>~L~不畏浮云遮望眼，自缘身在最高层~R~蕴含的核心哲理是：只有站在最高处，才能不被浮云遮挡视线，才能看得更远、更清楚。这既是登高望远的自然规律，也是认识事物的普遍规律——只有具备高远的视野和开阔的胸襟，才能不被眼前的局部现象所迷惑，才能把握事物的本质和全局。</dd></div>
      <div class="g-item"><dt>不畏艰难，积极进取</dt><dd>~L~不畏浮云遮望眼~R~的~L~不畏~R~，表达了诗人不怕困难、不畏奸邪的坚定态度。在人生道路上，总会遇到各种~L~浮云~R~（困难、障碍、偏见、阻挠），但只要我们~L~身在最高层~R~（有高远的志向和坚定的信念），就不会被这些~L~浮云~R~所迷惑，就能勇往直前、积极进取。</dd></div>
      <div class="g-item"><dt>与苏轼《题西林壁》对比</dt><dd>王安石~L~不畏浮云遮望眼，自缘身在最高层~R~强调~L~站得高~R~（入世、进取）；苏轼~L~不识庐山真面目，只缘身在此山中~R~强调~L~跳出局~R~（超脱、客观）。一正一反，一个说~L~身在最高层~R~所以看得远，一个说~L~身在此山中~R~所以看不清。两首诗从不同角度揭示了认识事物的规律，可对照阅读。</dd></div>
    </div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">因果倒装</td><td>不畏浮云遮望眼，自缘身在最高层。</td><td>正常语序应为~L~自缘身在最高层，（故）不畏浮云遮望眼~R~，诗人先果后因，突出~L~不畏~R~的坚定态度</td></tr>
      <tr><td class="kai">省略句</td><td>（余）不畏浮云遮望眼</td><td>省略主语~L~余~R~（我）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>飞来峰</dt><dd>在今浙江杭州西湖灵隐寺前，是一座石灰岩山峰，高约二百米。相传东晋咸和元年（326），印度僧人慧理登此山，叹曰：~L~此乃中天竺国灵鹫山之小岭，不知何以飞来？~R~因名飞来峰。峰上多石窟造像，为江南著名古迹。</dd></div>
      <div class="g-item"><dt>寻（古代长度单位）</dt><dd>古代长度单位，八尺为一寻（一说七尺）。~L~千寻~R~即八千尺，是夸张说法，形容极高。类似的长度单位还有：仞（七尺或八尺）、丈（十尺）、尺（十寸）等。</dd></div>
      <div class="g-item"><dt>浮云蔽日（典故）</dt><dd>~L~浮云蔽日~R~是中国古典诗歌中常见的比喻，比喻奸佞小人蒙蔽君主、陷害忠良。最早见于西汉陆贾《新语》：~L~邪臣之蔽贤，犹浮云之障日月也。~R~李白《登金陵凤凰台》：~L~总为浮云能蔽日，长安不见使人愁。~R~王安石在《登飞来峰》中反用其意。</dd></div>
      <div class="g-item"><dt>七言绝句</dt><dd>近体诗的一种，全诗四句，每句七字，共二十八字。二、四句押韵，首句可押可不押。格律严谨，是中国古典诗歌中最精炼的体裁之一。《登飞来峰》是七言绝句的典范之作。</dd></div>
      <div class="g-item"><dt>唐宋八大家</dt><dd>唐代和宋代八位散文家的合称，即唐代的韩愈、柳宗元，宋代的欧阳修、苏洵、苏轼、苏辙、王安石、曾巩。王安石是~L~唐宋八大家~R~之一，其散文雄健峭拔，论点鲜明，逻辑严密。</dd></div>
      <div class="g-item"><dt>王安石变法</dt><dd>北宋宋神宗熙宁年间（1068—1077），王安石主持的一场政治改革运动，又称~L~熙宁变法~R~。变法推行青苗法、募役法、方田均税法、农田水利法、保甲法等一系列措施，旨在富国强兵，改变北宋积贫积弱的局面。变法虽然最终因保守派反对而失败，但对北宋乃至后世产生了深远影响。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《登飞来峰》王安石</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">北宋 · 王安石</div>
  <h1 class="hero-title">登飞来峰</h1>
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
  <div class="sec-sub">全诗四句，分两部分：登高望远、借景抒怀。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《登飞来峰》</div>
  <div>王安石 · 北宋（1021—1086）· 皇祐年间作于杭州 · 七言绝句</div>
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

# Final pass: replace any remaining ~L~/~R~ placeholders
HTML = fixq(HTML)

io.open(OUT, 'w', encoding='utf-8').write(HTML)
print('OK', OUT, 'verses=', total, 'anno=', anno_count, 'words=', len(DICT_WORDS), 'notes=', len(DICT_NOTES))
