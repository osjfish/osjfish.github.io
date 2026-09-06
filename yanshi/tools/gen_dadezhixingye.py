# -*- coding: utf-8 -*-
"""《大道之行也》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。
中文引号用 ~L~ / ~R~ 占位，生成前替换为 \\u201c / \\u201d。
拼音必须放在注释 data-note 里，原文保持纯净：[[词|（拼音）释义]]"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dadezhixingye-liji.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'dadezhixingye_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "大道之行也，天下为公。",
    "选贤与能，讲信修睦。",
    "故人不独亲其亲，不独子其子，",
    "使老有所终，壮有所用，幼有所长，",
    "矜、寡、孤、独、废疾者皆有所养，",
    "男有分，女有归。",
    "货恶其弃于地也，不必藏于己；",
    "力恶其不出于身也，不必为己。",
    "是故谋闭而不兴，盗窃乱贼而不作，",
    "故外户而不闭。",
    "是谓大同。",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "纲领总起 · 天下为公", "第 1–2 句",
     "开门见山提出大同社会的总纲领——大道施行，天下公有。选拔贤能之人，讲求诚信，培养和睦，为下文具体描绘大同社会奠定基调。"),
    ("第二部分", "人人得所 · 各安其位", "第 3–6 句",
     "从人际关系、社会保障、男女职分三个层面，描绘大同社会中人人各得其所的理想图景。不独亲亲子子，老壮幼废疾皆有所养，男有分女有归——这是大同社会最核心的人文关怀。"),
    ("第三部分", "大公无私 · 是谓大同", "第 7–11 句",
     "从财物观念和劳动态度两方面，写大同社会大公无私的精神境界。货不藏己、力不为己，因而奸谋不兴、盗贼不作、外户不闭——最终收束于~L~大同~R~二字，点明主旨。"),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
(0, "[[大道|古代指政治上的最高理想]][[之|用于主谓之间，取消句子独立性，无实义]][[行|施行，实行]][[也|句末语气词，表停顿]]，[[天下为公|天下是公共的。为，是]]。",
 "在大道施行的时候，天下是公共的。",
 fixq("开篇即提出全文总纲。~L~大道之行也~R~以~L~也~R~字顿住，如警钟长鸣；~L~天下为公~R~四字掷地有声，是全文的灵魂所在。这一句不仅是对理想政治的概括，更是儒家社会理想的最高宣言——天下不属于一家一姓，而属于全体人民。"),
 ["总纲", "判断句"]),

(0, "[[选|选拔，推举]][[贤|（xián）品德高尚的人，形容词作名词]][[与|（jǔ）通~L~举~R~，推举，选拔]][[能|有才干的人，形容词作名词]]，[[讲|讲求，崇尚]][[信|诚信]][[修|培养，修治]][[睦|（mù）和睦]]。",
 "选拔推举品德高尚、有才干的人，讲求诚信，培养和睦气氛。",
 fixq("承接上句，写大同社会的用人准则与道德风尚。~L~选贤与能~R~是唯才是举，~L~讲信修睦~R~是以德化人。贤能在位则政治清明，信睦修明则社会和谐——这两句八字，概括了大同社会在政治与道德两个维度的理想状态。~L~与~R~通~L~举~R~，是本文重要的通假字。"),
 ["通假字", "词类活用", "对偶"]),

(1, "[[故|所以，连词]][[人不独亲其亲|人们不只是敬爱自己的父母。第一个~L~亲~R~是动词，以……为亲（奉养）；第二个~L~亲~R~是名词，父母]]，[[不独子其子|不只是疼爱自己的子女。第一个~L~子~R~是动词，以……为子（抚育）；第二个~L~子~R~是名词，子女]]，",
 "所以人们不只是敬爱自己的父母，不只是疼爱自己的子女，",
 fixq("写大同社会中人际关系的超越。~L~不独亲其亲，不独子其子~R~——两个~L~不独~R~，打破了血缘的局限，把对亲人的爱推广到所有人。第一个~L~亲~R~~L~子~R~是意动用法（以……为亲/子），第二个是名词，一词两用，精炼之至。这是儒家~L~老吾老以及人之老，幼吾幼以及人之幼~R~理想的经典表述。"),
 ["意动用法", "一词多义", "推己及人"]),

(1, "[[使|让，使]][[老|老年人，形容词作名词]][[有所终|有终老的保障。所终，指安享晚年的地方和条件]]，[[壮|壮年人，形容词作名词]][[有所用|能发挥才能，为社会效力]]，[[幼|幼童，形容词作名词]][[有所长|（zhǎng）有成长的条件和保障]]，",
 "使老年人有终老的保障，壮年人能发挥才能，幼童能顺利成长，",
 fixq("写大同社会的社会保障体系。老、壮、幼三个年龄段各得其所——老有所终是养老，壮有所用是就业，幼有所长是教育。三个~L~有所~R~排比，节奏铿锵，把大同社会对每一个生命的关怀写得具体而微。~L~老~R~~L~壮~R~~L~幼~R~皆形容词作名词，是本文词类活用的典型。"),
 ["排比", "词类活用", "社会保障"]),

(1, "[[矜|（guān）通~L~鳏~R~，老而无妻的人]]、[[寡|（guǎ）老而无夫的人]]、[[孤|幼而无父的人]]、[[独|老而无子的人]]、[[废疾|有残疾而不能做事的人]][[者|……的人，代词]][[皆|都]][[有所养|有供养的保障]]，",
 "使老而无妻、老而无夫、幼而无父、老而无子以及有残疾的人都能得到供养，",
 fixq("写大同社会对弱势群体的关怀。矜、寡、孤、独、废疾——五种最需要帮助的人，在大同社会里~L~皆有所养~R~。这五个词后来成为中国文化中对社会弱势群体的经典概括，~L~鳏寡孤独~R~至今仍是成语。一个社会的文明程度，往往看它如何对待最弱势的人——儒家早在两千多年前就有此洞见。"),
 ["通假字", "文化常识", "排比"]),

(1, "[[男有分|（fèn）男子有职分，指有稳定的职业。分，职分，职守]]，[[女有归|女子有归宿，指及时出嫁。归，女子出嫁]]。",
 "男子有固定的职业，女子有美满的归宿。",
 fixq("写大同社会中男女各安其位。~L~男有分~R~是说人人有工作，~L~女有归~R~是说人人有家庭。这两句在今天看来有时代局限，但在古代社会，它表达的是人人各得其所、社会安定有序的理想。~L~分~R~读 fèn 不读 fēn，~L~归~R~古义为女子出嫁，都是古今异义的考点。"),
 ["古今异义", "对偶"]),

(2, "[[货|财物]][[恶|（wù）憎恶，厌恶]][[其|它，指财物]][[弃|丢弃，抛弃]][[于|在，介词]][[地|地面]][[也|句中语气词，表停顿]]，[[不必|不一定]][[藏|私藏，据为己有]][[于己|为自己（私藏）]]；",
 "财物，人们厌恶它被丢弃在地上，但不一定是为了私藏；",
 fixq("写大同社会的财物观念。~L~货恶其弃于地也~R~——人们珍惜财物，不愿浪费，但~L~不必藏于己~R~——不是为了据为己有，而是为了物尽其用。这是一种超越私有制的财富观：珍惜劳动成果，但不贪求个人占有。~L~恶~R~读 wù 不读 è，是易错多音字。"),
 ["古今异义", "多音字", "财富观"]),

(2, "[[力|力气，力量]][[恶|（wù）憎恶，厌恶]][[其|它，指力气]][[不出于身|不从自己身上使出。于，从]][[也|句中语气词，表停顿]]，[[不必|不一定]][[为己|为了自己（的私利）]]。",
 "力气，人们厌恶它不从自己身上使出，但不一定是为了自己的私利。",
 fixq("写大同社会的劳动态度。与上句对举：上句写~L~货~R~（财物），此句写~L~力~R~（劳动）。人们愿意出力，不是为了个人私利，而是出于对劳动本身的珍视和对社会的责任。~L~力恶其不出于身~R~——人人都愿意为社会贡献力量，这是大同社会最动人的精神境界。两句一正一反，把大公无私的理想写得淋漓尽致。"),
 ["对偶", "劳动观", "大公无私"]),

(2, "[[是故|因此，所以]][[谋|奸诈之心，图谋]][[闭|闭塞，杜绝]][[而|连词，表转折，却]][[不兴|不兴起，不发生]]，[[盗窃|偷窃和劫夺财物的行为]][[乱贼|指造反和害人的事。乱，造反；贼，害人]][[而|连词，表转折，却]][[不作|不兴起，不发生]]，",
 "因此奸诈之心闭塞而不会兴起，盗窃、造反和害人的事情不会发生，",
 fixq("写大同社会的安定局面。因为人人为公，所以奸谋不生、盗贼不作。~L~谋闭而不兴~R~~L~盗窃乱贼而不作~R~——两个~L~而不~R~，从反面写出社会的太平。~L~乱贼~R~在古文中指造反害人，与今义~L~乱臣贼子~R~相近，但~L~贼~R~古义为害人，与今义~L~小偷~R~不同，是古今异义考点。"),
 ["古今异义", "反面写", "排比"]),

(2, "[[故|所以]][[外户|从外面把门带上。外，从外面，名词作状语]][[而|连词，表转折，却]][[不闭|不用门闩插门。闭，关门，这里指用门闩锁门]]。",
 "所以（家家户户）都不用从外面把门关上。",
 fixq("以~L~外户而不闭~R~的细节，写大同社会的路不拾遗、夜不闭户。这是太平盛世最经典的意象——门不用锁，因为没有盗贼。~L~外~R~是名词作状语（从外面），~L~闭~R~指用门闩插门。这一句看似平淡，实则是对大同社会最有力的证明：理想不是空洞的口号，而是夜不闭户的日常。"),
 ["名词作状语", "细节描写", "路不拾遗"]),

(2, "[[是|这，指示代词]][[谓|叫做，称为]][[大同|指理想社会。同，有和平、平等的意思]]。",
 "这就叫做~L~大同~R~。",
 fixq("以~L~是谓大同~R~四字收束全文，简洁有力。~L~大同~R~二字，是对全文理想社会的最高概括，也是中国文化中最具影响力的社会理想之一。从孙中山的~L~天下为公~R~到今天的~L~大同~R~理想，这篇短文的影响跨越了两千多年。以判断句作结，与开头~L~天下为公~R~首尾呼应，结构完整。"),
 ["判断句", "主旨句", "首尾呼应"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"睦","py":"mù","q":"讲信修□","tip":fixq("「睦」目字旁，音 mù，意为和睦，勿写~L~穆~R~~L~沐~R~")},
    {"w":"矜","py":"guān","q":"□、寡、孤、独","tip":fixq("「矜」矛字旁，此处通~L~鳏~R~读 guān，意为老而无妻，勿读 jīn")},
    {"w":"寡","py":"guǎ","q":"矜、□、孤、独","tip":fixq("「寡」宀字头，音 guǎ，意为老而无夫，勿写~L~卦~R~")},
    {"w":"分","py":"fèn","q":"男有□，女有归","tip":fixq("「分」八字头，此处读 fèn，意为职分，勿读 fēn")},
    {"w":"恶","py":"wù","q":"货□其弃于地也","tip":fixq("「恶」心字底，此处读 wù，意为憎恶，勿读 è")},
    {"w":"贼","py":"zéi","q":"盗窃乱□而不作","tip":fixq("「贼」贝字旁，音 zéi，古义为害人，勿写~L~贱~R~")},
    {"w":"闭","py":"bì","q":"故外户而不□","tip":fixq("「闭」门字框，音 bì，意为关门，勿写~L~闲~R~~L~困~R~")},
    {"w":"谓","py":"wèi","q":"是□大同","tip":fixq("「谓」言字旁，音 wèi，意为叫做，勿写~L~为~R~~L~渭~R~")},
    {"w":"与","py":"jǔ","q":"选贤□能","tip":fixq("「与」独体字，此处通~L~举~R~读 jǔ，意为推举，勿读 yǔ")},
    {"w":"修","py":"xiū","q":"讲信□睦","tip":fixq("「修」亻旁，音 xiū，意为培养，勿写~L~休~R~")},
    {"w":"藏","py":"cáng","q":"不必□于己","tip":fixq("「藏」草字头，此处读 cáng，意为私藏，勿读 zàng")},
    {"w":"弃","py":"qì","q":"货恶其□于地也","tip":fixq("「弃」廾字底，音 qì，意为丢弃，勿写~L~异~R~")},
    {"w":"终","py":"zhōng","q":"使老有所□","tip":fixq("「终」纟字旁，音 zhōng，意为终老，勿写~L~中~R~")},
    {"w":"归","py":"guī","q":"女有□","tip":fixq("「归」彐字旁，音 guī，古义为女子出嫁，勿写~L~旧~R~")},
    {"w":"废","py":"fèi","q":"□疾者皆有所养","tip":fixq("「废」广字头，音 fèi，意为残疾，勿写~L~费~R~")},
]

DICT_NOTES = [
    {"w":"大道","q":"大道之行也","a":"古代指政治上的最高理想"},
    {"w":"之","q":"大道之行也","a":"用于主谓之间，取消句子独立性，无实义"},
    {"w":"行","q":"大道之行也","a":"施行，实行"},
    {"w":"天下为公","q":"天下为公","a":"天下是公共的。为，是"},
    {"w":"贤","q":"选贤与能","a":"（xián）品德高尚的人，形容词作名词"},
    {"w":"与","q":"选贤与能","a":"（jǔ）通~L~举~R~，推举，选拔"},
    {"w":"能","q":"选贤与能","a":"有才干的人，形容词作名词"},
    {"w":"讲","q":"讲信修睦","a":"讲求，崇尚"},
    {"w":"信","q":"讲信修睦","a":"诚信"},
    {"w":"修","q":"讲信修睦","a":"培养，修治"},
    {"w":"睦","q":"讲信修睦","a":"（mù）和睦"},
    {"w":"故","q":"故人不独亲其亲","a":"所以，连词"},
    {"w":"亲其亲","q":"不独亲其亲","a":"第一个~L~亲~R~是动词，以……为亲（奉养）；第二个~L~亲~R~是名词，父母"},
    {"w":"子其子","q":"不独子其子","a":"第一个~L~子~R~是动词，以……为子（抚育）；第二个~L~子~R~是名词，子女"},
    {"w":"老","q":"使老有所终","a":"老年人，形容词作名词"},
    {"w":"有所终","q":"使老有所终","a":"有终老的保障"},
    {"w":"壮","q":"壮有所用","a":"壮年人，形容词作名词"},
    {"w":"有所用","q":"壮有所用","a":"能发挥才能，为社会效力"},
    {"w":"幼","q":"幼有所长","a":"幼童，形容词作名词"},
    {"w":"有所长","q":"幼有所长","a":"（zhǎng）有成长的条件和保障"},
    {"w":"矜","q":"矜、寡、孤、独","a":"（guān）通~L~鳏~R~，老而无妻的人"},
    {"w":"寡","q":"矜、寡、孤、独","a":"（guǎ）老而无夫的人"},
    {"w":"孤","q":"矜、寡、孤、独","a":"幼而无父的人"},
    {"w":"独","q":"矜、寡、孤、独","a":"老而无子的人"},
    {"w":"废疾","q":"废疾者皆有所养","a":"有残疾而不能做事的人"},
    {"w":"皆","q":"皆有所养","a":"都"},
    {"w":"有所养","q":"皆有所养","a":"有供养的保障"},
    {"w":"分","q":"男有分","a":"（fèn）职分，职守，指职业"},
    {"w":"归","q":"女有归","a":"女子出嫁，这里指归宿"},
    {"w":"货","q":"货恶其弃于地也","a":"财物"},
    {"w":"恶","q":"货恶其弃于地也","a":"（wù）憎恶，厌恶"},
    {"w":"弃","q":"货恶其弃于地也","a":"丢弃，抛弃"},
    {"w":"不必","q":"不必藏于己","a":"不一定"},
    {"w":"藏","q":"不必藏于己","a":"私藏，据为己有"},
    {"w":"力","q":"力恶其不出于身也","a":"力气，力量"},
    {"w":"出于身","q":"力恶其不出于身也","a":"从自己身上使出。于，从"},
    {"w":"为己","q":"不必为己","a":"为了自己（的私利）"},
    {"w":"是故","q":"是故谋闭而不兴","a":"因此，所以"},
    {"w":"谋","q":"是故谋闭而不兴","a":"奸诈之心，图谋"},
    {"w":"闭","q":"是故谋闭而不兴","a":"闭塞，杜绝"},
    {"w":"兴","q":"谋闭而不兴","a":"兴起，发生"},
    {"w":"盗窃","q":"盗窃乱贼而不作","a":"偷窃和劫夺财物的行为"},
    {"w":"乱贼","q":"盗窃乱贼而不作","a":"指造反和害人的事。乱，造反；贼，害人"},
    {"w":"作","q":"盗窃乱贼而不作","a":"兴起，发生"},
    {"w":"外户","q":"故外户而不闭","a":"从外面把门带上。外，从外面，名词作状语"},
    {"w":"闭","q":"故外户而不闭","a":"用门闩插门，关门"},
    {"w":"是","q":"是谓大同","a":"这，指示代词"},
    {"w":"谓","q":"是谓大同","a":"叫做，称为"},
    {"w":"大同","q":"是谓大同","a":"指理想社会。同，有和平、平等的意思"},
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
    <p>《大道之行也》选自《礼记·礼运》，是儒家经典中描绘理想社会的名篇。全文仅百余字，却以凝练的笔墨勾勒出一个~L~天下为公~R~的大同世界，成为中国思想史上影响最深远的社会理想之一。</p>
    <p>文章通过对大同社会的描绘，表达了儒家对公平、正义、和睦的理想社会的追求，也寄托了古人对美好生活的向往。</p>
  </div>
  <div class="box">
    <h3>作品简介</h3>
    <p>《礼记》是儒家经典之一，是战国至秦汉年间儒家学者解释说明经书《仪礼》的文章选集，共四十九篇。《礼运》是《礼记》中的一篇，大约是战国末年或秦汉之际儒家学者托名孔子答问的著作。</p>
    <p>~L~大道之行也~R~是《礼运》开头部分孔子向弟子言偃（子游）讲述大同、小康之别的一段话，描绘了~L~大同~R~社会的理想图景，是儒家社会理想的集中体现。</p>
    <p class="note">※ 《礼记》与《周礼》《仪礼》合称~L~三礼~R~，是古代礼乐文化的理论形态，对中国文化影响深远。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>春秋战国之变：</b>春秋战国时期，周室衰微，诸侯争霸，礼崩乐坏，社会动荡。面对乱世，儒家学者提出了各种社会改革方案，~L~大同~R~理想正是在这样的背景下产生的——它既是对上古社会的追忆，也是对未来社会的构想。</p>
    <p><b>孔子的社会理想：</b>孔子生活在春秋末期，他向往西周初年的礼乐文明，提出~L~仁~R~的学说，主张~L~克己复礼~R~。《礼运》中托名孔子的~L~大同~R~之说，是对孔子社会理想的进一步发展和系统化。</p>
    <p><b>大同与小康：</b>《礼运》将社会分为~L~大同~R~与~L~小康~R~两个层次。大同是~L~天下为公~R~的理想社会，小康是~L~天下为家~R~的现实社会。本文所选的是~L~大同~R~部分，代表了儒家最高的社会理想。</p>
  </div>
  <div class="box">
    <h3>思想渊源</h3>
    <p>~L~天下为公~R~的思想，源于上古氏族社会的原始共产主义观念。儒家将其理想化、理论化，成为批判现实、指引未来的思想武器。从《礼记》的~L~大同~R~到陶渊明的~L~桃花源~R~，从洪秀全的~L~太平天国~R~到孙中山的~L~天下为公~R~，这一理想贯穿了中国两千多年的思想史。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>经典诵读《大道之行也》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1Yv4y1c72J&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="经典诵读《大道之行也》"></iframe>
        <a href="https://www.bilibili.com/video/BV1Yv4y1c72J" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>文化解读：天下为公的浪漫</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1npwCz5EmS&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="文化解读《大道之行也》"></iframe>
        <a href="https://www.bilibili.com/video/BV1npwCz5EmS" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">结构严谨，层层递进</div>
        <p>全文以~L~大道之行也，天下为公~R~总起，然后从用人准则（选贤与能，讲信修睦）、人际关系（不独亲其亲，不独子其子）、社会保障（老有所终……皆有所养）、男女职分（男有分，女有归）、财物观念（货恶其弃于地……）、劳动态度（力恶其不出于身……）六个方面逐层展开，最后以~L~是谓大同~R~收束。总分总结构，逻辑严密，一气呵成。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">排比铺陈，气势充沛</div>
        <p>文章大量运用排比句式，如~L~老有所终，壮有所用，幼有所长~R~~L~矜、寡、孤、独、废疾者皆有所养~R~~L~货恶其弃于地也……力恶其不出于身也~R~。排比的运用使文章节奏铿锵，气势充沛，把大同社会的美好图景铺陈得淋漓尽致，读来令人心向往之。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">正反对照，理想鲜明</div>
        <p>文章既有正面的理想描绘（天下为公、选贤与能），又有反面的结果推论（谋闭不兴、盗贼不作、外户不闭）。正反对照，使大同社会的优越性更加突出。特别是~L~外户而不闭~R~的细节，以小见大，用最朴素的生活场景证明了理想社会的真实可感。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">语言凝练，言简义丰</div>
        <p>全文仅百余字，却涵盖了政治、经济、文化、社会等各个方面。~L~天下为公~R~四字、~L~大同~R~二字，都成为中国文化中的经典概念。文章用词精确，如~L~亲其亲~R~~L~子其子~R~的意动用法，~L~矜寡孤独~R~的并列结构，都体现了文言文高度凝练的特点。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">大道之行也，天下为公。</div>
        <p>全文总纲，也是中国思想史上最著名的政治宣言之一。~L~大道~R~指最高的政治理想，~L~天下为公~R~指天下属于全体人民。这八个字，超越了一家一姓的私天下观念，提出了公天下的理想。从儒家的大同理想到孙中山的三民主义，~L~天下为公~R~始终是中国进步思想的旗帜。以判断句开篇，斩钉截铁，气势非凡。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">故人不独亲其亲，不独子其子。</div>
        <p>写大同社会中人际关系的超越。两个~L~不独~R~，打破了血缘的局限。第一个~L~亲~R~~L~子~R~是意动用法，第二个是名词，一词两用，精炼之至。这是孟子~L~老吾老以及人之老，幼吾幼以及人之幼~R~的先声，也是儒家~L~仁~R~的思想的推广——从爱亲人到爱所有人，是大同社会最核心的人文精神。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">是故谋闭而不兴，盗窃乱贼而不作，故外户而不闭。</div>
        <p>从反面写大同社会的安定。因为人人为公，所以奸谋不生、盗贼不作、夜不闭户。三个短句层层递进，从内心（谋闭）到行为（盗贼不作）再到生活细节（外户不闭），把太平盛世写得具体可感。~L~外户而不闭~R~是路不拾遗、夜不闭户的经典意象，以小见大，是全文最生动的一笔。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《大道之行也》通过对~L~大同~R~社会的描绘，表达了儒家对公平、正义、和睦的理想社会的追求。在这个社会里，天下是公共的，贤能之人被选拔任用，人人诚实守信、和睦相处；人们不只爱自己的亲人，而是把爱推广到所有人；老弱病残皆有所养，男女各安其位；财物不被私藏，劳动不为私利——最终达到奸谋不兴、盗贼不作、夜不闭户的太平境界。</p>
    <p>这一理想虽然产生于两千多年前，但它所表达的对公平正义、社会保障、大公无私的追求，至今仍有深刻的现实意义。~L~天下为公~R~的理念，已经成为中华民族共同的精神财富，激励着一代又一代人为美好社会而奋斗。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 一词多义 · 活用 · 句式 · 文化常识</span></div>

  <div class="box">
    <h3>通假字</h3>
    <div class="tw"><table>
      <tr><th>字</th><th>通假</th><th>例句</th><th>释义</th></tr>
      <tr><td class="kai">与</td><td>通~L~举~R~</td><td>选贤与能</td><td>推举，选拔（读 jǔ）</td></tr>
      <tr><td class="kai">矜</td><td>通~L~鳏~R~</td><td>矜、寡、孤、独</td><td>老而无妻的人（读 guān）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">大道</td><td>古代指政治上的最高理想</td><td>宽阔的道路</td><td>大道之行也</td></tr>
      <tr><td class="kai">归</td><td>女子出嫁，归宿</td><td>返回，归还</td><td>女有归</td></tr>
      <tr><td class="kai">分</td><td>职分，职守（读 fèn）</td><td>分开，分配（读 fēn）</td><td>男有分</td></tr>
      <tr><td class="kai">贼</td><td>害人（动词/名词）</td><td>小偷，盗贼</td><td>盗窃乱贼而不作</td></tr>
      <tr><td class="kai">货</td><td>财物（泛指一切物资）</td><td>商品，货物</td><td>货恶其弃于地也</td></tr>
      <tr><td class="kai">不必</td><td>不一定</td><td>不需要，用不着</td><td>不必藏于己</td></tr>
      <tr><td class="kai">乱</td><td>造反，叛乱</td><td>混乱，杂乱</td><td>盗窃乱贼而不作</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>一词多义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="2">亲</td><td>以……为亲（意动用法，动词）</td><td>不独亲其亲（第一个）</td></tr>
      <tr><td>父母（名词）</td><td>不独亲其亲（第二个）</td></tr>
      <tr><td class="kai" rowspan="2">子</td><td>以……为子（意动用法，动词）</td><td>不独子其子（第一个）</td></tr>
      <tr><td>子女（名词）</td><td>不独子其子（第二个）</td></tr>
      <tr><td class="kai" rowspan="2">为</td><td>是（判断动词）</td><td>天下为公</td></tr>
      <tr><td>为了（介词）</td><td>不必为己</td></tr>
      <tr><td class="kai" rowspan="2">故</td><td>所以（连词）</td><td>故人不独亲其亲</td></tr>
      <tr><td>所以（连词，与~L~是~R~连用）</td><td>是故谋闭而不兴</td></tr>
      <tr><td class="kai" rowspan="2">闭</td><td>闭塞，杜绝</td><td>谋闭而不兴</td></tr>
      <tr><td>用门闩插门，关门</td><td>故外户而不闭</td></tr>
      <tr><td class="kai" rowspan="2">恶</td><td>憎恶，厌恶（读 wù）</td><td>货恶其弃于地也</td></tr>
      <tr><td>坏人，罪恶（读 è）</td><td>无恶不作（成语）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>词类活用</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">亲</td><td>名词的意动用法</td><td>以……为亲（奉养）</td><td>不独亲其亲</td></tr>
      <tr><td class="kai">子</td><td>名词的意动用法</td><td>以……为子（抚育）</td><td>不独子其子</td></tr>
      <tr><td class="kai">老</td><td>形容词作名词</td><td>老年人</td><td>使老有所终</td></tr>
      <tr><td class="kai">壮</td><td>形容词作名词</td><td>壮年人</td><td>壮有所用</td></tr>
      <tr><td class="kai">幼</td><td>形容词作名词</td><td>幼童</td><td>幼有所长</td></tr>
      <tr><td class="kai">贤</td><td>形容词作名词</td><td>品德高尚的人</td><td>选贤与能</td></tr>
      <tr><td class="kai">能</td><td>形容词作名词</td><td>有才干的人</td><td>选贤与能</td></tr>
      <tr><td class="kai">外</td><td>名词作状语</td><td>从外面</td><td>故外户而不闭</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">判断句</td><td>天下为公</td><td>~L~为~R~表判断，~L~天下是公共的~R~</td></tr>
      <tr><td class="kai">判断句</td><td>是谓大同</td><td>~L~谓~R~表判断，~L~这就叫做大同~R~</td></tr>
      <tr><td class="kai">省略句</td><td>（人）不独亲其亲</td><td>承前省略主语~L~人~R~</td></tr>
      <tr><td class="kai">固定句式</td><td>有所终 / 有所用 / 有所养</td><td>~L~有所+动词~R~，表示~L~有……的（地方/条件/保障）~R~</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>《礼记》</dt><dd>儒家经典之一，战国至秦汉年间儒家学者解释说明《仪礼》的文章选集，共四十九篇。与《周礼》《仪礼》合称~L~三礼~R~。内容涉及礼制、礼意、哲学、伦理等，是研究中国古代社会的重要文献。</dd></div>
      <div class="g-item"><dt>大同</dt><dd>儒家提出的理想社会。~L~大~R~是程度副词，意为最、极；~L~同~R~有和平、平等之意。~L~大同~R~即最和平、最平等的社会。与~L~小康~R~相对，是儒家最高的社会理想。</dd></div>
      <div class="g-item"><dt>小康</dt><dd>与~L~大同~R~相对的社会形态。~L~天下为家~R~，人们各亲其亲、各子其子，靠礼义维持秩序。禹、汤、文、武、成王、周公之治即为~L~小康~R~。~L~小康~R~是低于~L~大同~R~的现实社会理想。</dd></div>
      <div class="g-item"><dt>鳏寡孤独</dt><dd>泛指没有劳动力而又没有亲属供养的人。鳏（矜）：老而无妻；寡：老而无夫；孤：幼而无父；独：老而无子。《孟子》中也有~L~鳏寡孤独~R~的说法，是中国文化中对弱势群体的经典概括。</dd></div>
      <div class="g-item"><dt>天下为公</dt><dd>天下是公众的，不属于一家一姓。这是大同社会最核心的特征，也是中国政治思想中最具影响力的理念之一。近代孙中山将其作为民权主义的口号，影响深远。</dd></div>
      <div class="g-item"><dt>选贤与能</dt><dd>选拔推举品德高尚、有才干的人。~L~与~R~通~L~举~R~。这是大同社会的用人原则，与~L~世卿世禄~R~的世袭制相对，体现了唯才是举的政治理想。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《大道之行也》礼记</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">先秦 · 《礼记》</div>
  <h1 class="hero-title">大道之行也</h1>
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
  <div class="sec-sub">全文百余字，分三部分：纲领总起、人人得所、大公无私。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《大道之行也》</div>
  <div>《礼记·礼运》· 先秦儒家经典</div>
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
