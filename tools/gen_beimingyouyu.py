# -*- coding: utf-8 -*-
"""《北冥有鱼》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'beimingyouyu-zhuangzi.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'beimingyouyu_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "北冥有鱼，其名为鲲。",
    "鲲之大，不知其几千里也；",
    "化而为鸟，其名为鹏。",
    "鹏之背，不知其几千里也；",
    "怒而飞，其翼若垂天之云。",
    "是鸟也，海运则将徙于南冥。",
    "南冥者，天池也。",
    "《齐谐》者，志怪者也。",
    "《谐》之言曰：~L~鹏之徙于南冥也，水击三千里，抟扶摇而上者九万里，去以六月息者也。~R~",
    "野马也，尘埃也，生物之以息相吹也。",
    "天之苍苍，其正色邪？其远而无所至极邪？",
    "其视下也，亦若是则已矣。",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "鲲鹏变化 · 硕大无比", "第 1–5 句",
     "从北冥之鱼写起，极写鲲鹏之大。鲲化而为鹏，鹏背几千里，怒飞而翼若垂天之云——以夸张的笔法，塑造出一个硕大无比、力大无穷的鲲鹏形象，为下文写其南飞蓄势。"),
    ("第二部分", "海运徙冥 · 志怪佐证", "第 6–9 句",
     "写大鹏借海运之风南迁南冥，并引《齐谐》之言佐证。水击三千里、抟扶摇而上九万里、去以六月息——极写大鹏南飞的气势，也暗示其~L~有所待~R~：必须凭借大风才能高飞。"),
    ("第三部分", "天地之辩 · 万物皆有所待", "第 10–12 句",
     "以野马尘埃、天之苍苍作比，说明大鹏高飞九万里，往下看也不过如此。万物皆~L~有所待~R~，大鹏如此，人亦如此——这是庄子~L~逍遥游~R~思想的核心：只有无所待，才能真正逍遥。"),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
(0, "[[北冥|（míng）北海。冥，通~L~溟~R~，海]][[有|有]][[鱼|鱼]]，[[其|它的，代词]][[名|名字]][[为|叫做，是]][[鲲|（kūn）大鱼名]]。",
 "北海里有一条鱼，它的名字叫做鲲。",
 fixq("开篇即异想天开——北海有鱼，其名为鲲。~L~北冥~R~设喻辽远，~L~鲲~R~之名古奥神秘。庄子以极为简洁的笔墨，把读者带入一个浩瀚无垠的神话世界。~L~冥~R~通~L~溟~R~，是本文第一个通假字。这一句看似平淡，实则为下文鲲鹏的巨大变化埋下伏笔。"),
 ["通假字", "起笔", "神话"]),

(0, "[[鲲之大|鲲的巨大。之，用于主谓之间，取消句子独立性]]，[[不知|不知道]][[其|它，指鲲]][[几千里|几千里（长），虚指，极言其大]][[也|句末语气词，表陈述]]；",
 "鲲的巨大，不知道它有几千里长；",
 fixq("极写鲲之大。~L~不知其几千里也~R~——不写具体尺寸，而以~L~不知~R~二字，给读者留下无限想象空间。这是庄子特有的夸张笔法：不说~L~大~R~，而说~L~不知其几千里~R~，比直接说~L~很大~R~更有力量。~L~之~R~用于主谓之间取消句子独立性，是文言常见用法。"),
 ["夸张", "之的用法"]),

(0, "[[化|变化]][[而|连词，表顺承，就]][[为|成为，变成]][[鸟|鸟类]]，[[其|它的]][[名|名字]][[为|叫做]][[鹏|（péng）大鸟名]]。",
 "鲲变化成为鸟，它的名字叫做鹏。",
 fixq("写鲲化为鹏，是全文第一个大转折。鱼化鸟，从水中到天上，空间骤变，想象奇绝。~L~化而为鸟~R~四字，简洁有力，一个~L~化~R~字，写出了生命形态的根本转变。鲲是水中之极大，鹏是空中之极大——庄子以~L~化~R~字，把两个极大的世界连在一起。"),
 ["想象", "化", "转折"]),

(0, "[[鹏之背|鹏的脊背。之，的，结构助词]]，[[不知|不知道]][[其|它，指鹏]][[几千里|几千里（宽），虚指，极言其大]][[也|句末语气词]]；",
 "鹏的脊背，不知道它有几千里宽；",
 fixq("与~L~鲲之大~R~对举，极写鹏之大。上句写鲲的~L~大~R~（长度），此句写鹏的~L~背~R~（宽度），角度不同而夸张如一。重复~L~不知其几千里也~R~的句式，形成回环往复的节奏，强化了鲲鹏硕大无比的印象。这种重复不是啰嗦，而是庄子有意为之的强调。"),
 ["对偶", "夸张", "重复"]),

(0, "[[怒|（nù）振奋，这里指用力鼓动翅膀]][[而|连词，表修饰]][[飞|飞翔]]，[[其|它的]][[翼|翅膀]][[若|好像，如同]][[垂天之云|悬挂在天空的云。垂，悬挂]]。",
 "（鹏）用力鼓动翅膀飞翔，它的翅膀就像悬挂在天空的云。",
 fixq("写鹏起飞时的雄姿。~L~怒而飞~R~的~L~怒~R~不是愤怒，而是振奋、鼓动——一个~L~怒~R~字，写出了大鹏积力爆发、一飞冲天的气势。~L~其翼若垂天之云~R~，以~L~垂天之云~R~喻翅膀，既是夸张，又是画面：一只巨鸟，翅膀如漫天云层，遮天蔽日。这是中国文学史上最著名的大鹏形象的源头。"),
 ["炼字", "比喻", "大鹏形象"]),

(1, "[[是|这，指示代词]][[鸟|鸟]][[也|句中语气词，表停顿]]，[[海运|海水运动，这里指汹涌的海涛；一说指鹏鸟在海面飞行]][[则|就，连词]][[将|将要]][[徙|（xǐ）迁移]][[于|到，介词]][[南冥|南海。冥，通~L~溟~R~]]。",
 "这只鸟，海水运动的时候就要迁徙到南海去。",
 fixq("写大鹏的目标——南冥。从北冥到南冥，是从最北到最南，空间跨度极大。~L~海运则将徙~R~——大鹏迁徙必须等待~L~海运~R~（大风），这暗示了大鹏~L~有所待~R~：它虽然巨大，但仍需凭借外力才能飞行。这是庄子~L~逍遥游~R~思想的伏笔：再大的事物，只要有所待，就不算真正的逍遥。"),
 ["有所待", "伏笔", "空间"]),

(1, "[[南冥者|南海啊。者，表提顿，与~L~也~R~配合表判断]]，[[天池|天然形成的水池。天，天然；池，水池]][[也|句末语气词，表判断]]。",
 "南海，是天然形成的大水池。",
 fixq("解释南冥，用判断句~L~……者，……也~R~的格式。~L~天池~R~二字，极言南海的浩瀚与神圣——不是人工开凿，而是天然形成。这一句既是对南冥的说明，也与开头~L~北冥~R~呼应：北冥有鱼，南冥是天池，一北一南，一鱼一鸟，构成完整的空间结构。"),
 ["判断句", "呼应", "天池"]),

(1, "[[《齐谐》|书名，齐国俳谐之书，记载怪异之事]][[者|表提顿，与~L~者也~R~配合表判断]]，[[志|记载]][[怪|怪异的事物，形容词作名词]][[者也|表判断，~L~是……的~R~]]。",
 "《齐谐》这本书，是记载怪异事物的书。",
 fixq("引入《齐谐》作为佐证。庄子行文，常常先讲寓言，再引古书佐证——这是~L~重言~R~的手法，借古人之言增强说服力。~L~志怪~R~的~L~怪~R~是形容词作名词，指怪异的事物。《齐谐》虽已失传，但通过庄子的引用，我们知道它是一部记载奇闻异事的书，与大鹏的神话性质正相契合。"),
 ["重言", "词类活用", "佐证"]),

(1, "[[《谐》之言|《齐谐》上的话。之，的，结构助词]][[曰|说]]：~L~[[鹏之徙于南冥也|鹏迁徙到南海的时候。之，用于主谓之间，取消句子独立性；于，到]][[水击|击水，拍打水面。指鹏鸟奋飞时双翼拍打水面]][[三千里|三千里（远），虚指]][[抟|（tuán）盘旋飞翔]][[扶摇|旋风]][[而上|而向上飞。而，连词，表修饰]][[者九万里|（高达）九万里。者，表停顿]][[去|离开，这里指离开北海]][[以|凭借]][[六月息|六月的大风。息，气息，这里指风]][[者也|表判断]]~R~。",
 "《齐谐》上的话说：~L~鹏迁徙到南海的时候，翅膀拍打水面，激起三千里的浪涛，乘着旋风盘旋飞至九万里的高空，凭借着六月的大风离开。~R~",
 fixq("引《齐谐》之言，极写大鹏南飞的气势。~L~水击三千里~R~写起飞时的力量，~L~抟扶摇而上者九万里~R~写飞升的高度，~L~去以六月息者也~R~写飞行的凭借——三个短句，从力到高到因，把大鹏南飞写得惊心动魄。但~L~以六月息~R~三字，再次强调~L~有所待~R~：大鹏再大，也需凭借大风。这是庄子的深意：伟大如大鹏，仍未达逍遥之境。"),
 ["引用", "有所待", "夸张"]),

(2, "[[野马|山野中的雾气，奔腾如野马。古今异义]][[也|句中语气词，表停顿]]，[[尘埃|扬在空中的土叫尘，细碎的尘粒叫埃]][[也|句中语气词]]，[[生物|概指各种有生命的东西]][[之|用于主谓之间，取消句子独立性]][[以|用，凭借]][[息|气息]][[相吹|互相吹拂]][[也|句末语气词]]。",
 "山野中的雾气，空气中的尘埃，都是生物用气息吹拂的结果。",
 fixq("以野马尘埃作比，说明万物皆~L~有所待~R~。野马尘埃看似微小，也是靠气息吹拂才能飘动——与大鹏靠大风飞行，本质相同。~L~野马~R~是古今异义词，古义指山野中的雾气，今义指野生动物。庄子以小见大：大鹏需要大风，尘埃需要气息，大小虽异，~L~有所待~R~则一。"),
 ["古今异义", "以小见大", "有所待"]),

(2, "[[天之苍苍|天色深蓝。之，用于主谓之间]][[苍苍|深蓝色]]，[[其|表示选择，是……还是……]][[正色|真正的颜色。正，真正的；色，颜色]][[邪|（yé）通~L~耶~R~，句末语气词，呢，吗]]？[[其|还是]][[远|高远]][[而|连词，表因果，因而]][[无所至极|没有尽头。至极，到尽头]][[邪|（yé）通~L~耶~R~，呢，吗]]？",
 "天色深蓝，是它真正的颜色吗？还是因为天高远而看不到尽头呢？",
 fixq("以人仰视苍天作比，说明人的认知有限。我们看天是深蓝的，但那是天的本色吗？还是因为天太高远，我们看不到尽头？两个~L~其……邪~R~的选择问句，把认知的相对性写得深刻而生动。~L~邪~R~通~L~耶~R~，是通假字。这一句是庄子认识论的体现：人的认知受限于视角和距离，没有绝对的~L~正色~R~。"),
 ["通假字", "选择问句", "认知相对性"]),

(2, "[[其|它，指鹏]][[视下|往下看。视，看；下，下方]][[也|句中语气词]]，[[亦|也]][[若是|像这样。若，像；是，这样]][[则已矣|就罢了。则已，就罢了；矣，句末语气词]]。",
 "鹏从高空往下看，也不过像人在地面上看天一样罢了。",
 fixq("收束全文，点明主旨。大鹏高飞九万里，往下看人间，也不过像我们抬头看天一样——视角不同，感受则一。~L~亦若是则已矣~R~，~L~亦~R~~L~则已矣~R~，语气平淡而意蕴深远：万物皆有所待，认知皆有局限，这就是庄子~L~逍遥游~R~的起点——只有超越~L~有所待~R~，才能达到真正的逍遥自由。全文以问句起，以陈述结，余味无穷。"),
 ["主旨", "逍遥游", "收束"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"鲲","py":"kūn","q":"其名为□","tip":fixq("「鲲」鱼字旁，音 kūn，大鱼名，勿写~L~昆~R~~L~琨~R~")},
    {"w":"鹏","py":"péng","q":"其名为□","tip":fixq("「鹏」鸟字旁，音 péng，大鸟名，勿写~L~朋~R~~L~棚~R~")},
    {"w":"抟","py":"tuán","q":"□扶摇而上者九万里","tip":fixq("「抟」提手旁，音 tuán，意为盘旋，勿写~L~传~R~~L~转~R~")},
    {"w":"徙","py":"xǐ","q":"海运则将□于南冥","tip":fixq("「徙」彳旁，音 xǐ，意为迁移，勿写~L~徒~R~~L~陡~R~")},
    {"w":"冥","py":"míng","q":"北□有鱼","tip":fixq("「冥」秃宝盖，通~L~溟~R~读 míng，意为海，勿写~L~瞑~R~")},
    {"w":"邪","py":"yé","q":"其正色□","tip":fixq("「邪」耳字旁，通~L~耶~R~读 yé，语气词，勿读 xié")},
    {"w":"埃","py":"āi","q":"尘□也","tip":fixq("「埃」土字旁，音 āi，意为尘埃，勿写~L~挨~R~~L~唉~R~")},
    {"w":"翼","py":"yì","q":"其□若垂天之云","tip":fixq("「翼」羽字底，音 yì，意为翅膀，勿写~L~冀~R~")},
    {"w":"垂","py":"chuí","q":"其翼若□天之云","tip":fixq("「垂」独体字，音 chuí，意为悬挂，勿写~L~捶~R~~L~锤~R~")},
    {"w":"苍苍","py":"cāng cāng","q":"天之□□","tip":fixq("「苍」草字头，音 cāng，意为深蓝，叠词整体作答案，勿写~L~仓~R~")},
    {"w":"谐","py":"xié","q":"《齐□》者","tip":fixq("「谐」言字旁，音 xié，书名，勿写~L~皆~R~~L~楷~R~")},
    {"w":"扶摇","py":"fú yáo","q":"抟□□而上者九万里","tip":fixq("「扶摇」旋风，叠词整体作答案，~L~扶~R~提手旁，~L~摇~R~提手旁")},
    {"w":"怒","py":"nù","q":"□而飞","tip":fixq("「怒」心字底，音 nù，此处意为振奋，非愤怒，勿写~L~恕~R~")},
    {"w":"极","py":"jí","q":"无所至□","tip":fixq("「极」木字旁，音 jí，意为尽头，勿写~L~及~R~~L~级~R~")},
]

DICT_NOTES = [
    {"w":"北冥","q":"北冥有鱼","a":"（míng）北海。冥，通~L~溟~R~，海"},
    {"w":"其","q":"其名为鲲","a":"它的，代词"},
    {"w":"为","q":"其名为鲲","a":"叫做，是"},
    {"w":"鲲","q":"其名为鲲","a":"（kūn）大鱼名"},
    {"w":"之","q":"鲲之大","a":"用于主谓之间，取消句子独立性"},
    {"w":"几千里","q":"不知其几千里也","a":"几千里（长/宽），虚指，极言其大"},
    {"w":"化","q":"化而为鸟","a":"变化"},
    {"w":"而","q":"化而为鸟","a":"连词，表顺承，就"},
    {"w":"为","q":"化而为鸟","a":"成为，变成"},
    {"w":"鹏","q":"其名为鹏","a":"（péng）大鸟名"},
    {"w":"之","q":"鹏之背","a":"的，结构助词"},
    {"w":"怒","q":"怒而飞","a":"（nù）振奋，这里指用力鼓动翅膀"},
    {"w":"而","q":"怒而飞","a":"连词，表修饰"},
    {"w":"若","q":"其翼若垂天之云","a":"好像，如同"},
    {"w":"垂天之云","q":"其翼若垂天之云","a":"悬挂在天空的云。垂，悬挂"},
    {"w":"是","q":"是鸟也","a":"这，指示代词"},
    {"w":"海运","q":"海运则将徙于南冥","a":"海水运动，这里指汹涌的海涛；一说指鹏鸟在海面飞行"},
    {"w":"则","q":"海运则将徙于南冥","a":"就，连词"},
    {"w":"徙","q":"海运则将徙于南冥","a":"（xǐ）迁移"},
    {"w":"于","q":"海运则将徙于南冥","a":"到，介词"},
    {"w":"南冥","q":"南冥者，天池也","a":"南海。冥，通~L~溟~R~"},
    {"w":"天池","q":"南冥者，天池也","a":"天然形成的水池"},
    {"w":"齐谐","q":"《齐谐》者，志怪者也","a":"书名，齐国俳谐之书，记载怪异之事"},
    {"w":"志","q":"志怪者也","a":"记载"},
    {"w":"怪","q":"志怪者也","a":"怪异的事物，形容词作名词"},
    {"w":"曰","q":"《谐》之言曰","a":"说"},
    {"w":"水击","q":"水击三千里","a":"击水，拍打水面。指鹏鸟奋飞时双翼拍打水面"},
    {"w":"抟","q":"抟扶摇而上者九万里","a":"（tuán）盘旋飞翔"},
    {"w":"扶摇","q":"抟扶摇而上者九万里","a":"旋风"},
    {"w":"去","q":"去以六月息者也","a":"离开，这里指离开北海"},
    {"w":"以","q":"去以六月息者也","a":"凭借"},
    {"w":"息","q":"去以六月息者也","a":"气息，这里指风"},
    {"w":"野马","q":"野马也，尘埃也","a":"山野中的雾气，奔腾如野马。古今异义"},
    {"w":"尘埃","q":"野马也，尘埃也","a":"扬在空中的土叫尘，细碎的尘粒叫埃"},
    {"w":"生物","q":"生物之以息相吹也","a":"概指各种有生命的东西"},
    {"w":"相吹","q":"生物之以息相吹也","a":"互相吹拂"},
    {"w":"苍苍","q":"天之苍苍","a":"深蓝色"},
    {"w":"其","q":"其正色邪","a":"表示选择，是……还是……"},
    {"w":"正色","q":"其正色邪","a":"真正的颜色"},
    {"w":"邪","q":"其正色邪","a":"（yé）通~L~耶~R~，句末语气词，呢，吗"},
    {"w":"无所至极","q":"其远而无所至极邪","a":"没有尽头。至极，到尽头"},
    {"w":"亦","q":"亦若是则已矣","a":"也"},
    {"w":"若是","q":"亦若是则已矣","a":"像这样。若，像；是，这样"},
    {"w":"则已矣","q":"亦若是则已矣","a":"就罢了。则已，就罢了；矣，句末语气词"},
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
    <p>《北冥有鱼》节选自《庄子·逍遥游》，是庄子哲学的经典名篇。文章以鲲鹏变化的寓言，阐述了~L~万物皆有所待~R~的道理，表达了对绝对自由（逍遥）的向往。</p>
    <p>全文想象奇绝，气势磅礴，以浪漫主义的笔法，把读者带入一个浩瀚无垠的神话世界，是中国文学史上最富想象力的篇章之一。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>庄子（约前369—前286），名周，战国时期宋国蒙（今河南商丘东北）人，道家学派的代表人物，与老子并称~L~老庄~R~。他曾做过蒙地的漆园吏，后辞官不仕，过着清贫的生活。</p>
    <p>庄子继承并发展了老子的道家思想，主张~L~道法自然~R~~L~无为而治~R~，追求精神的绝对自由。其文汪洋恣肆，想象丰富，善用寓言说理，具有浓厚的浪漫主义色彩。《庄子》一书，又名《南华经》，是道家经典之一。</p>
    <p class="note">※ 庄子的文章，~L~意出尘外，怪生笔端~R~，鲁迅赞其~L~汪洋辟阖，仪态万方，晚周诸子之作，莫能先也~R~。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>战国乱世：</b>庄子生活在战国中期，诸侯争霸，战乱频仍，社会动荡。面对残酷的现实，庄子不愿同流合污，转而追求精神的超越与自由。《逍遥游》正是在这样的背景下产生的——它既是对现实的逃避，也是对自由的向往。</p>
    <p><b>道家思想：</b>老子提出~L~道~R~的概念，主张顺应自然。庄子进一步发展了这一思想，提出~L~逍遥游~R~的境界——超越一切外物的束缚，达到精神的绝对自由。鲲鹏寓言正是这一思想的形象化表达。</p>
    <p><b>寓言传统：</b>庄子善用寓言说理，~L~寓言十九~R~（十句话里九句是寓言）。鲲鹏、蜩与学鸠、藐姑射之山的神人……这些寓言形象，成为中国文学中最经典的意象。</p>
  </div>
  <div class="box">
    <h3>《逍遥游》题解</h3>
    <p>~L~逍遥~R~是悠然自得的样子，~L~游~R~是游历、活动。~L~逍遥游~R~即悠然自得地活动，指精神的绝对自由。庄子认为，万物皆~L~有所待~R~（有所凭借），大鹏需要大风，列子需要御风，都不算真正的逍遥。只有~L~无己~R~~L~无功~R~~L~无名~R~，顺应自然，才能达到~L~乘天地之正，而御六气之辩，以游无穷~R~的逍遥境界。</p>
    <p>本文是《逍遥游》的开头部分，通过鲲鹏的寓言，引出~L~小大之辩~R~和~L~有所待~R~的主题，是理解庄子哲学的入口。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>经典诵读《北冥有鱼》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1yT411w7Bk&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="经典诵读《北冥有鱼》"></iframe>
        <a href="https://www.bilibili.com/video/BV1yT411w7Bk" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>趣味动画学《北冥有鱼》</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1rz42167fA&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="趣味动画《北冥有鱼》"></iframe>
        <a href="https://www.bilibili.com/video/BV1rz42167fA" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>鲲鹏形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">硕大无比，力大无穷</div>
        <p>庄子笔下的鲲鹏，是中国文学史上最著名的宏大形象。鲲~L~不知其几千里~R~，鹏背~L~不知其几千里~R~，翼~L~若垂天之云~R~——作者不写具体尺寸，而以~L~不知~R~~L~若~R~等模糊的比喻，给读者留下无限想象空间。这种~L~大~R~，不是数字的大，而是境界的大：它从北冥到南冥，从水中到天上，跨越了整个世界。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">有所待者，未达逍遥</div>
        <p>鲲鹏虽然巨大，但它~L~有所待~R~：必须等待~L~海运~R~（大风）才能迁徙，必须凭借~L~六月息~R~才能高飞。庄子写鲲鹏之大，正是为了说明：即使伟大如鲲鹏，只要有所凭借，就不算真正的逍遥。这是庄子的深意——~L~大~R~不等于~L~自由~R~，只有超越一切凭借，才能达到逍遥之境。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">想象奇绝，浪漫瑰丽</div>
        <p>庄子的想象，前无古人。鱼化鸟、北冥到南冥、水击三千里、抟扶摇九万里——这些意象，突破了现实的束缚，把读者带入一个浩瀚无垠的神话世界。这种浪漫主义的想象，深刻影响了后世文学：从李白的~L~大鹏一日同风起~R~到毛泽东的~L~鲲鹏展翅九万里~R~，鲲鹏形象成为中国文学中最经典的宏大意象。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">寓言说理，寓哲于象</div>
        <p>庄子不直接讲道理，而是通过寓言形象来说理。鲲鹏的寓言，既写了~L~大~R~，又写了~L~有所待~R~；野马尘埃的比喻，说明小物也有所待；天之苍苍的问句，探讨认知的相对性。抽象的哲学道理，通过具体的形象表达出来，既生动又深刻，~L~言在此而意在彼~R~。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">夸张排比，气势磅礴</div>
        <p>文章大量运用夸张和排比。~L~不知其几千里也~R~重复出现，~L~水击三千里，抟扶摇而上者九万里~R~数字递增，形成磅礴的气势。句式长短交错，节奏张弛有度，读来如闻天风海雨，令人心神俱醉。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">层层铺垫，卒章显志</div>
        <p>文章从北冥之鱼写起，到鲲鹏变化，到海运南飞，到《齐谐》佐证，到野马尘埃，到天之苍苍，最后以~L~其视下也，亦若是则已矣~R~收束。层层铺垫，步步推进，最后一句点明主旨：万物皆有所待，认知皆有局限。结构严谨，余味无穷。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">怒而飞，其翼若垂天之云。</div>
        <p>写大鹏起飞的雄姿。~L~怒~R~字是句眼——不是愤怒，而是振奋、积力爆发。一个~L~怒~R~字，写出了大鹏蓄积力量、一飞冲天的气势。~L~若垂天之云~R~的比喻，既是夸张，又是画面：翅膀如漫天云层，遮天蔽日。这一句，是中国文学史上最著名的大鹏形象的经典描写，李白~L~大鹏一日同风起，扶摇直上九万里~R~即由此化出。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">水击三千里，抟扶摇而上者九万里。</div>
        <p>写大鹏南飞的气势。~L~水击三千里~R~写起飞时的力量，~L~抟扶摇而上者九万里~R~写飞升的高度。从三千里到九万里，数字递增，气势越来越大。~L~击~R~~L~抟~R~两个动词，精准有力：~L~击~R~是拍水，~L~抟~R~是盘旋。这一句，把大鹏飞行的力量和高度写得惊心动魄，是全文最有气势的句子。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">天之苍苍，其正色邪？其远而无所至极邪？</div>
        <p>以人仰视苍天作比，探讨认知的相对性。两个选择问句，不给出答案，而是把问题留给读者：我们看到的天是深蓝的，但那是天的本色吗？还是因为天太高远，我们看不到尽头？这种怀疑精神，是庄子哲学的精髓——人的认知受限于视角和距离，没有绝对的真理。句式整齐，语气悠远，令人深思。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《北冥有鱼》通过鲲鹏变化的寓言，阐述了~L~万物皆有所待~R~的道理。鲲鹏虽然硕大无比、力大无穷，但它必须凭借大风才能高飞远徙——这说明任何事物都有所凭借，都受限于外部条件。</p>
    <p>庄子写鲲鹏之~L~大~R~，正是为了说明~L~大~R~不等于~L~自由~R~。真正的逍遥，是超越一切凭借和束缚，达到~L~乘天地之正，而御六气之辩，以游无穷~R~的境界。本文作为《逍遥游》的开头，以瑰丽的想象和深刻的哲理，为全文奠定了基调，也成为中国哲学和文学中最经典的篇章之一。</p>
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
      <tr><td class="kai">冥</td><td>通~L~溟~R~</td><td>北冥有鱼</td><td>海（读 míng）</td></tr>
      <tr><td class="kai">邪</td><td>通~L~耶~R~</td><td>其正色邪</td><td>句末语气词，呢，吗（读 yé）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">野马</td><td>山野中的雾气，奔腾如野马</td><td>野生动物的一种</td><td>野马也，尘埃也</td></tr>
      <tr><td class="kai">海运</td><td>海水运动，指汹涌的海涛</td><td>海洋运输</td><td>海运则将徙于南冥</td></tr>
      <tr><td class="kai">天池</td><td>天然形成的水池</td><td>高山湖泊名（如长白山天池）</td><td>南冥者，天池也</td></tr>
      <tr><td class="kai">怒</td><td>振奋，这里指用力鼓动翅膀</td><td>愤怒，生气</td><td>怒而飞</td></tr>
      <tr><td class="kai">去</td><td>离开</td><td>前往，到……去</td><td>去以六月息者也</td></tr>
      <tr><td class="kai">息</td><td>气息，这里指风</td><td>休息，消息</td><td>去以六月息者也</td></tr>
      <tr><td class="kai">正色</td><td>真正的颜色</td><td>态度严肃，颜色纯正</td><td>其正色邪</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>一词多义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="3">之</td><td>用于主谓之间，取消句子独立性</td><td>鲲之大 / 鹏之徙于南冥也</td></tr>
      <tr><td>的，结构助词</td><td>鹏之背 / 《谐》之言</td></tr>
      <tr><td>代词，它</td><td>久之，目似瞑（《狼》）</td></tr>
      <tr><td class="kai" rowspan="3">其</td><td>它的，代词</td><td>其名为鲲 / 其翼若垂天之云</td></tr>
      <tr><td>它，代词</td><td>不知其几千里也</td></tr>
      <tr><td>表示选择，是……还是……</td><td>其正色邪？其远而无所至极邪？</td></tr>
      <tr><td class="kai" rowspan="3">而</td><td>连词，表顺承</td><td>化而为鸟</td></tr>
      <tr><td>连词，表修饰</td><td>怒而飞 / 抟扶摇而上</td></tr>
      <tr><td>连词，表因果</td><td>其远而无所至极邪</td></tr>
      <tr><td class="kai" rowspan="2">以</td><td>凭借</td><td>去以六月息者也</td></tr>
      <tr><td>用</td><td>生物之以息相吹也</td></tr>
      <tr><td class="kai" rowspan="2">名</td><td>名字</td><td>其名为鲲</td></tr>
      <tr><td>命名，取名（动词）</td><td>名之者谁（《醉翁亭记》）</td></tr>
      <tr><td class="kai" rowspan="2">为</td><td>叫做，是</td><td>其名为鲲</td></tr>
      <tr><td>成为，变成</td><td>化而为鸟</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>词类活用</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">怪</td><td>形容词作名词</td><td>怪异的事物</td><td>《齐谐》者，志怪者也</td></tr>
      <tr><td class="kai">水</td><td>名词作状语</td><td>在水面上</td><td>水击三千里</td></tr>
      <tr><td class="kai">南</td><td>名词作状语</td><td>向南</td><td>海运则将徙于南冥（南冥：南海）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">判断句</td><td>南冥者，天池也</td><td>~L~……者，……也~R~表判断</td></tr>
      <tr><td class="kai">判断句</td><td>《齐谐》者，志怪者也</td><td>~L~……者，……者也~R~表判断</td></tr>
      <tr><td class="kai">倒装句（介词结构后置）</td><td>去以六月息者也</td><td>正常语序为~L~以六月息去~R~，~L~凭借六月的大风离开~R~</td></tr>
      <tr><td class="kai">省略句</td><td>（鲲）化而为鸟</td><td>承前省略主语~L~鲲~R~</td></tr>
      <tr><td class="kai">固定句式</td><td>其正色邪？其远而无所至极邪？</td><td>~L~其……邪？其……邪？~R~表选择，~L~是……呢？还是……呢？~R~</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>庄子与《庄子》</dt><dd>庄子（约前369—前286），名周，战国时宋国人，道家学派代表人物，与老子并称~L~老庄~R~。《庄子》又名《南华经》，道家经典之一，共三十三篇，分内篇、外篇、杂篇。其文汪洋恣肆，想象丰富，善用寓言说理。</dd></div>
      <div class="g-item"><dt>逍遥游</dt><dd>《庄子》首篇，是庄子哲学的总纲。~L~逍遥~R~指悠然自得，~L~游~R~指活动。~L~逍遥游~R~即精神的绝对自由。庄子认为，万物皆~L~有所待~R~（有所凭借），只有~L~无己~R~~L~无功~R~~L~无名~R~，才能达到真正的逍遥。</dd></div>
      <div class="g-item"><dt>鲲鹏</dt><dd>庄子创造的神话形象。鲲是北冥中的大鱼，化而为鹏，鹏是大鸟。鲲鹏后来成为中国文学中最经典的宏大意象，象征远大志向和磅礴气势。李白《上李邕》~L~大鹏一日同风起，扶摇直上九万里~R~即用此典。</dd></div>
      <div class="g-item"><dt>《齐谐》</dt><dd>书名，齐国俳谐之书，记载怪异之事。已失传。庄子引其言佐证大鹏南飞之事，是~L~重言~R~（借古人之言）手法的运用。~L~齐谐~R~后来成为志怪小说的代称，如《搜神记》《聊斋志异》等都受其影响。</dd></div>
      <div class="g-item"><dt>有所待</dt><dd>庄子哲学概念，指事物有所凭借、有所依赖。大鹏需要大风，列子需要御风，都是~L~有所待~R~。庄子认为，只有~L~无所待~R~（不依赖任何外物），才能达到真正的逍遥自由。这是《逍遥游》的核心概念。</dd></div>
      <div class="g-item"><dt>六月息</dt><dd>六月的大风。~L~息~R~本义为气息，这里指风。古人认为六月海上有大风，称为~L~六月息~R~。大鹏凭借六月的大风从北冥飞往南冥，说明即使是神鸟，也需要凭借外力。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《北冥有鱼》庄子</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">先秦 · 庄子</div>
  <h1 class="hero-title">北冥有鱼</h1>
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
  <div class="sec-sub">全文十二句，分三部分：鲲鹏变化、海运徙冥、天地之辩。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《北冥有鱼》</div>
  <div>庄子 · 先秦（约前369—前286）· 名周，道家代表</div>
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
