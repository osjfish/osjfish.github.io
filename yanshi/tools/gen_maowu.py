# -*- coding: utf-8 -*-
"""《茅屋为秋风所破歌》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。
中文引号用 ~L~ / ~R~ 占位，生成前替换为 \u201c / \u201d。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maowu-dufu.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'maowu_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "八月秋高风怒号，卷我屋上三重茅。",
    "茅飞渡江洒江郊，高者挂罥长林梢，下者飘转沉塘坳。",
    "南村群童欺我老无力，忍能对面为盗贼。",
    "公然抱茅入竹去，唇焦口燥呼不得，归来倚杖自叹息。",
    "俄顷风定云墨色，秋天漠漠向昏黑。",
    "布衾多年冷似铁，娇儿恶卧踏里裂。",
    "床头屋漏无干处，雨脚如麻未断绝。",
    "自经丧乱少睡眠，长夜沾湿何由彻！",
    "安得广厦千万间，大庇天下寒士俱欢颜！风雨不动安如山。",
    "呜呼！何时眼前突兀见此屋，吾庐独破受冻死亦足！",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "秋风破屋 · 茅飞江郊", "第 1–5 句",
     "起笔写秋风破屋的情景。风怒号、卷茅飞、挂林梢、沉塘坳，一连串动态描写，把一场狂风写得触目惊心，也为全诗奠定了凄苦的基调。"),
    ("第二部分", "群童抱茅 · 倚杖叹息", "第 6–10 句",
     "写南村群童公然抱茅而去，诗人老无力、呼不得，只能归来倚杖叹息。群童之顽劣与诗人之无奈形成对照，见出诗人晚年的困顿与辛酸。"),
    ("第三部分", "夜雨湿床 · 长夜难眠", "第 11–18 句",
     "风定云墨，秋雨连绵。布衾冷铁、娇儿恶卧、屋漏无干、雨脚如麻，由屋外到屋内，由环境到心境，层层递进，写尽长夜沾湿之苦。"),
    ("第四部分", "广厦庇寒 · 吾庐独破", "第 19–24 句",
     fixq("由自身苦难一跃而及天下寒士，发出~L~安得广厦千万间~R~的宏愿，更以~L~吾庐独破受冻死亦足~R~的牺牲精神收束全诗，境界顿开，光耀千古。")),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
(0, "八月[[秋高|秋高气爽，指八月天高气爽]]风[[怒号(háo)|大声吼叫，形容风势猛烈]]，",
 "八月里秋高气爽，狂风大声吼叫。",
 fixq("以~L~怒号~R~写风，拟人手法，开篇即为全诗定下凄苦动荡的基调。~L~八月秋高~R~本是天清气爽之时，却忽起狂风，乐景反衬哀情。"),
 ["拟人", "反衬"]),

(0, "卷我屋上[[三重(chóng)茅|几层茅草。~L~三~R~虚指，形容多层；重，层]]。",
 "卷走了我屋顶上好几层茅草。",
 fixq("~L~卷~R~字极写风力之猛，~L~三重~R~见出受害之深。屋茅被卷，是全诗苦难的起点。"),
 ["炼字"]),

(0, "茅飞渡江洒江郊，",
 "茅草乱飞，渡过浣花溪，散落在对岸江边。",
 fixq("由~L~卷~R~到~L~飞~R~到~L~洒~R~，三个动词连贯而下，写出茅草被风卷走后的散乱之态，也见出诗人追望不及的无奈。"),
 ["炼字", "连贯动作"]),

(0, "高者[[挂罥(juàn)|挂结、悬挂。罥，挂]][[长(cháng)林梢|高高的树梢。长，高]]，",
 "飞得高的茅草挂结在高高的树梢上。",
 fixq("~L~挂罥~R~写高者之态，~L~长林梢~R~点出其高不可及。诗人眼睁睁看着茅草挂在树梢，却无法取下，焦灼可见。"),
 ["细节"]),

(0, "下者[[飘转|飘落旋转]]沉[[塘坳(ào)|低洼积水的地方。坳，低洼处]]。",
 "飞得低的茅草飘飘转转，沉入池塘的低洼处。",
 "高者挂树梢、下者沉塘坳，一高一低，写尽茅草的不可收拾。" if False else fixq("高者挂树梢、下者沉塘坳，一高一低，写尽茅草的不可收拾。~L~沉~R~字写出低处茅草没入水中的绝望，诗人的凄苦不言而喻。"),
 ["对比", "细节"]),

(1, "南村群童欺我[[老无力|年老无力]]，",
 "南村的一群孩童欺负我年老无力。",
 fixq("由自然之苦转入人事之苦。~L~群童~R~与~L~老无力~R~形成对照，诗人年迈体衰，连孩童都敢欺负他，辛酸之态如在目前。"),
 ["对照"]),

(1, "[[忍能|竟能忍心这样。忍，狠心；能，这样]]对面为盗贼。",
 fixq("竟能忍心这样当面做~L~贼~R~抢东西。"),
 fixq("~L~忍能对面~R~四字，把群童的顽劣与诗人的愤懑写得入木三分。称群童为~L~盗贼~R~，是激愤之语，并非真的深责孩童，而是悲苦至极的宣泄。"),
 ["炼字", "激愤之语"]),

(1, "[[公然|明目张胆地]]抱茅入竹去，",
 "明目张胆地抱着茅草跑进竹林里去了。",
 fixq("~L~公然~R~二字，写出群童毫无顾忌的情态，也反衬诗人的无可奈何。~L~入竹去~R~写出群童逃入竹林的身影，诗人追之不及。"),
 ["细节"]),

(1, "[[唇焦口燥|嘴唇干燥，形容呼喊得筋疲力尽]]呼不得，",
 "我喊得唇焦口燥，也喝止不住他们。",
 fixq("~L~唇焦口燥~R~写诗人呼喊之苦，~L~呼不得~R~写呼喊之无效。四字一短语，把诗人的焦急、疲惫与无奈浓缩其中。"),
 ["细节", "炼字"]),

(1, "归来[[倚杖|拄着拐杖]]自叹息。",
 "回到家中，只能拄着拐杖独自叹息。",
 fixq("由~L~呼不得~R~到~L~自叹息~R~，诗人的情绪由焦急转为无奈。~L~倚杖~R~二字，既写出年迈之态，也写出孤独无依之境。这一叹，叹的是自身的衰老，也是世道的艰难。"),
 ["细节", "情感"]),

(2, "[[俄顷|一会儿，顷刻之间]]风定云墨色，",
 "一会儿风停了，天空中的云黑得像墨一样。",
 fixq("由白天的风转入傍晚的雨。~L~俄顷~R~写时间之短，~L~云墨色~R~以比喻写乌云之浓，预示着一场大雨即将来临，苦难由风转雨，层层加深。"),
 ["比喻", "过渡"]),

(2, "秋天[[漠漠|灰蒙蒙、阴沉迷蒙的样子]]向昏黑。",
 "秋季的天空阴沉迷蒙，渐渐黑了下来。",
 fixq("~L~漠漠~R~叠词，渲染出阴沉压抑的氛围。~L~向昏黑~R~写出时间推移，暮色四合，诗人的心境也随之沉入黑暗。"),
 ["叠词", "氛围"]),

(2, "[[布衾(qīn)|布被子。衾，被子]]多年冷似铁，",
 "布被子盖了多年，又冷又硬，像铁板一样。",
 fixq("~L~冷似铁~R~以比喻写布被的冰冷坚硬，见出诗人生活的贫困。~L~多年~R~二字，说明这种贫困不是一时，而是长久如此。"),
 ["比喻", "细节"]),

(2, "[[娇儿|爱子]][[恶卧|睡相不好，睡觉时蹬被]]踏里裂。",
 "娇儿睡相不好，把被里子都蹬破了。",
 fixq("布被本已冷似铁，又被娇儿蹬破，雪上加霜。~L~恶卧~R~写孩童天真无知之态，~L~踏里裂~R~写家境的贫寒，于平淡叙述中见出深沉的辛酸。"),
 ["细节", "以小见大"]),

(2, "床头屋漏无干处，",
 "屋顶漏雨，床头没有一点干燥的地方。",
 fixq("由被子写到屋顶，~L~屋漏~R~呼应开头~L~卷我屋上三重茅~R~，首尾照应。~L~无干处~R~三字，写尽漏雨之严重，也写尽生存之窘迫。"),
 ["照应", "细节"]),

(2, "[[雨脚|雨点，像线条一样落下的雨]]如麻未断绝。",
 "雨点像麻线一样密集，下个不停。",
 fixq("~L~雨脚如麻~R~以比喻写雨之密集，~L~未断绝~R~写雨之持久。屋外大雨，屋内小漏，布被冷湿，诗人的苦难在雨夜中达到顶点。"),
 ["比喻", "氛围"]),

(2, "自经[[丧(sāng)乱|战乱，指安史之乱。丧，丧事，引申为死难]]少睡眠，",
 "自从经历了安史之乱，我就很少能睡个安稳觉。",
 fixq("由眼前的夜雨宕开一笔，写到安史之乱。~L~丧乱~R~是时代大背景，诗人的个人苦难与时代苦难紧密相连，~L~少睡眠~R~既是因雨夜，也是因忧国忧民。"),
 ["宕开", "时代背景"]),

(2, "长夜[[沾湿|被雨水沾湿]]何由[[彻|到，这里指到天亮]]！",
 "这漫长的黑夜，又湿又冷，如何才能挨到天亮！",
 fixq("~L~长夜~R~双关，既指这漫长的雨夜，也指战乱以来的艰难岁月。~L~何由彻~R~以反问收束，把痛苦、绝望与期盼交织在一起，为下文的宏愿蓄势。"),
 ["双关", "反问", "蓄势"]),

(3, "[[安得|怎么能得到，哪里能得到]][[广厦(shà)|宽敞的大屋。厦，大屋子]]千万间，",
 "怎么才能得到千万间宽敞高大的房屋！",
 fixq("笔锋陡转，由自身苦难一跃而及天下。~L~安得~R~二字，既是发问，也是祈愿。~L~千万间~R~以夸张写数量之多，见出诗人胸怀之广。"),
 ["转折", "夸张", "宏愿"]),

(3, "大[[庇(bì)|遮蔽，掩护]]天下[[寒士|贫寒的读书人]]俱欢颜！",
 "普遍地遮蔽天下所有贫寒的读书人，让他们个个都喜笑颜开！",
 fixq("~L~大庇~R~写庇护之广，~L~天下寒士~R~写受众之众，~L~俱欢颜~R~写效果之好。诗人由一己之苦想到天下之苦，由一己之愿升华为普世之愿，境界豁然开阔。"),
 ["境界升华"]),

(3, "风雨不动安如山。",
 "在风雨中也安稳得像山一样，纹丝不动。",
 fixq("~L~安如山~R~以比喻写广厦的稳固，与开头~L~风怒号~R~~L~卷我屋上三重茅~R~的飘摇形成强烈对比。这是诗人理想中的居所，也是对太平盛世的向往。"),
 ["比喻", "对比"]),

(3, "[[呜呼|叹词，相当于~L~唉~R~]]！何时眼前[[突兀(wù)|高耸的样子]]见此屋，",
 "唉！什么时候眼前能高耸地出现这样的房屋，",
 fixq("~L~呜呼~R~一叹，由理想回到现实。~L~突兀~R~写广厦高耸之态，~L~见此屋~R~是诗人最热切的期盼。这一问，问的是何时天下寒士才能得庇，也是何时乱世才能终结。"),
 ["叹词", "反问"]),

(3, "吾庐独破受冻死亦足！",
 "那么唯独我的茅屋破漏，让我受冻而死，也心甘情愿！",
 fixq("全诗的最强音。诗人宁愿自己独破受冻而死，也要换取天下寒士的安居。~L~独破~R~与~L~广厦千万间~R~形成对比，~L~死亦足~R~以决绝之语写牺牲精神，读来令人动容。这正是杜甫~L~诗圣~R~精神的集中体现。"),
 ["对比", "牺牲精神", "诗圣精神"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"罥","py":"juàn","q":"高者挂□长林梢","tip":fixq("「罥」四字头（网字头），音 juàn，意为悬挂，勿写~L~绢~R~~L~捐~R~")},
    {"w":"坳","py":"ào","q":"下者飘转沉塘□","tip":fixq("「坳」土字旁，音 ào，意为低洼处，勿写~L~拗~R~~L~傲~R~")},
    {"w":"衾","py":"qīn","q":"布□多年冷似铁","tip":fixq("「衾」衣字旁，音 qīn，意为被子，勿写~L~裘~R~~L~枕~R~")},
    {"w":"丧","py":"sāng","q":"自经□乱少睡眠","tip":fixq("「丧」此处读 sāng（平声），意为死难、丧事，勿读 sàng")},
    {"w":"厦","py":"shà","q":"安得广□千万间","tip":fixq("「厦」厂字头，音 shà，意为大屋子，勿写~L~夏~R~")},
    {"w":"庇","py":"bì","q":"大□天下寒士俱欢颜","tip":fixq("「庇」广字头，音 bì，意为遮蔽，勿写~L~屁~R~~L~比~R~")},
    {"w":"兀","py":"wù","q":"何时眼前突□见此屋","tip":fixq("「兀」儿字底，音 wù，意为高耸，勿写~L~元~R~~L~无~R~")},
    {"w":"见","py":"xiàn","q":"何时眼前突兀□此屋","tip":fixq("「见」此处通~L~现~R~，读 xiàn，意为出现，勿读 jiàn")},
    {"w":"号","py":"háo","q":"八月秋高风怒□","tip":fixq("「号」此处读 háo（阳平），意为吼叫，勿读 hào")},
    {"w":"重","py":"chóng","q":"卷我屋上三□茅","tip":fixq("「重」此处读 chóng，意为层，勿读 zhòng")},
    {"w":"长","py":"cháng","q":"高者挂罥□林梢","tip":fixq("「长」此处读 cháng，意为高，勿读 zhǎng")},
    {"w":"顷","py":"qǐng","q":"俄□风定云墨色","tip":fixq("「顷」页字旁，音 qǐng，意为片刻，勿写~L~倾~R~")},
    {"w":"漠漠","py":"mò mò","q":"秋天□□向昏黑","tip":fixq("「漠漠」三点水，音 mò mò，叠词形容阴沉迷蒙")},
    {"w":"娇","py":"jiāo","q":"□儿恶卧踏里裂","tip":fixq("「娇」女字旁，音 jiāo，意为可爱的，勿写~L~骄~R~")},
    {"w":"燥","py":"zào","q":"唇焦口□呼不得","tip":fixq("「燥」火字旁，音 zào，意为干燥，勿写~L~躁~R~（跺脚）")},
    {"w":"倚","py":"yǐ","q":"归来□杖自叹息","tip":fixq("「倚」单人旁，音 yǐ，意为靠着，勿写~L~椅~R~")},
    {"w":"塘","py":"táng","q":"下者飘转沉□坳","tip":fixq("「塘」土字旁，音 táng，意为水池，勿写~L~糖~R~")},
    {"w":"梢","py":"shāo","q":"高者挂罥长林□","tip":fixq("「梢」木字旁，音 shāo，意为树枝的末端，勿写~L~稍~R~")},
    {"w":"渡","py":"dù","q":"茅飞□江洒江郊","tip":fixq("「渡」三点水，音 dù，意为过江，勿写~L~度~R~")},
    {"w":"洒","py":"sǎ","q":"茅飞渡江□江郊","tip":fixq("「洒」三点水，音 sǎ，意为散落，勿写~L~酒~R~")},
    {"w":"彻","py":"chè","q":"长夜沾湿何由□","tip":fixq("「彻」双人旁，音 chè，意为到（天亮），勿写~L~撤~R~")},
    {"w":"庐","py":"lú","q":"吾□独破受冻死亦足","tip":fixq("「庐」广字头，音 lú，意为简陋的房屋，勿写~L~芦~R~")},
    {"w":"墨","py":"mò","q":"俄顷风定云□色","tip":fixq("「墨」土字底，音 mò，意为黑色，勿写~L~默~R~")},
    {"w":"麻","py":"má","q":"雨脚如□未断绝","tip":fixq("「麻」广字头，音 má，比喻雨点密集，勿写~L~嘛~R~")},
]

DICT_NOTES = [
    {"w":"秋高","q":"八月秋高风怒号","a":"秋高气爽，指八月天高气爽"},
    {"w":"怒号","q":"八月秋高风怒号","a":"大声吼叫，形容风势猛烈。号，háo"},
    {"w":"三重茅","q":"卷我屋上三重茅","a":fixq("几层茅草。~L~三~R~虚指，形容多层；重，chóng，层")},
    {"w":"挂罥","q":"高者挂罥长林梢","a":"挂结、悬挂。罥，juàn"},
    {"w":"长","q":"高者挂罥长林梢","a":"高。长，cháng"},
    {"w":"塘坳","q":"下者飘转沉塘坳","a":"低洼积水的地方。坳，ào，低洼处"},
    {"w":"忍能","q":"忍能对面为盗贼","a":"竟能忍心这样。忍，狠心；能，这样"},
    {"w":"对面","q":"忍能对面为盗贼","a":"当面"},
    {"w":"公然","q":"公然抱茅入竹去","a":"明目张胆地"},
    {"w":"唇焦口燥","q":"唇焦口燥呼不得","a":"嘴唇干燥，形容呼喊得筋疲力尽"},
    {"w":"呼不得","q":"唇焦口燥呼不得","a":"喝止不住"},
    {"w":"倚杖","q":"归来倚杖自叹息","a":"拄着拐杖"},
    {"w":"俄顷","q":"俄顷风定云墨色","a":"一会儿，顷刻之间"},
    {"w":"风定","q":"俄顷风定云墨色","a":"风停了"},
    {"w":"漠漠","q":"秋天漠漠向昏黑","a":"灰蒙蒙、阴沉迷蒙的样子"},
    {"w":"向昏黑","q":"秋天漠漠向昏黑","a":"渐渐黑下来。向，接近、渐渐"},
    {"w":"布衾","q":"布衾多年冷似铁","a":"布被子。衾，qīn，被子"},
    {"w":"娇儿","q":"娇儿恶卧踏里裂","a":"爱子"},
    {"w":"恶卧","q":"娇儿恶卧踏里裂","a":"睡相不好，睡觉时蹬被"},
    {"w":"踏里裂","q":"娇儿恶卧踏里裂","a":"把被里子蹬破了"},
    {"w":"雨脚","q":"雨脚如麻未断绝","a":"雨点，像线条一样落下的雨"},
    {"w":"丧乱","q":"自经丧乱少睡眠","a":"战乱，指安史之乱。丧，sāng，死难"},
    {"w":"何由彻","q":"长夜沾湿何由彻","a":"如何挨到天亮。彻，到（天亮）"},
    {"w":"安得","q":"安得广厦千万间","a":"怎么能得到，哪里能得到"},
    {"w":"广厦","q":"安得广厦千万间","a":"宽敞的大屋。厦，shà，大屋子"},
    {"w":"大庇","q":"大庇天下寒士俱欢颜","a":"全部遮蔽、掩护。庇，bì"},
    {"w":"寒士","q":"大庇天下寒士俱欢颜","a":"贫寒的读书人"},
    {"w":"俱","q":"大庇天下寒士俱欢颜","a":"都"},
    {"w":"欢颜","q":"大庇天下寒士俱欢颜","a":"欢笑的容颜"},
    {"w":"突兀","q":"何时眼前突兀见此屋","a":"高耸的样子。兀，wù"},
    {"w":"见","q":"何时眼前突兀见此屋","a":fixq("同~L~现~R~，出现。见，xiàn，通假字")},
    {"w":"吾庐","q":"吾庐独破受冻死亦足","a":"我的茅屋。庐，lú，简陋的房屋"},
    {"w":"独破","q":"吾庐独破受冻死亦足","a":"唯独破漏"},
    {"w":"亦足","q":"吾庐独破受冻死亦足","a":"也心甘情愿。足，满足、值得"},
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
    <p>上元二年（761）秋，杜甫流寓成都草堂。一日狂风大作，卷走屋上茅草；入夜又逢大雨，屋漏床湿，诗人彻夜难眠。由自身的苦难，他想到天下千千万万和自己一样流离失所的寒士，于是写下这首千古名篇。</p>
    <p>全诗以~L~茅屋为秋风所破~R~为题，却不止于写一己之苦。结尾~L~安得广厦千万间，大庇天下寒士俱欢颜~R~的宏愿，与~L~吾庐独破受冻死亦足~R~的牺牲精神，使这首诗超越了个人悲叹，成为中国文学史上最动人的人道主义宣言之一。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>杜甫（712—770），字子美，自号少陵野老，祖籍襄阳，生于河南巩县。唐代伟大的现实主义诗人，被后世尊为~L~诗圣~R~，其诗被称为~L~诗史~R~。与李白并称~L~李杜~R~。曾任左拾遗、检校工部员外郎，故世称~L~杜工部~R~。</p>
    <p>杜甫一生历经开元盛世与安史之乱，诗歌深刻反映了唐代由盛转衰的社会现实，风格沉郁顿挫。代表作有~L~三吏~R~~L~三别~R~、《春望》《登高》《茅屋为秋风所破歌》《闻官军收河南河北》等。</p>
    <p class="note">※ 杜甫的诗~L~穷年忧黎元，叹息肠内热~R~，始终把个人命运与国家人民紧密相连，《茅屋为秋风所破歌》正是这种精神的集中体现。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>安史之乱：</b>天宝十四载（755），安禄山、史思明发动叛乱，历时八年，使大唐由盛转衰。战乱中，人民流离失所，杜甫也被迫辗转逃难，历经艰辛。</p>
    <p><b>流寓成都：</b>乾元二年（759）末，杜甫弃官入蜀，在亲友帮助下于成都浣花溪畔营建草堂，总算有了一个栖身之所。但草堂简陋，生活依然困苦。</p>
    <p><b>写作缘起：</b>上元二年（761）秋，一场大风卷走了草堂的茅草，随后大雨滂沱，诗人在~L~布衾多年冷似铁~R~~L~床头屋漏无干处~R~的凄苦中彻夜难眠，由自身遭遇推及天下寒士，写下此诗。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《茅屋为秋风所破歌》是<b>歌行体</b>古诗，属古体诗。~L~歌~R~是古代诗歌的一种体裁，句式自由，可长可短，可换韵，便于铺陈叙事、抒发情感。全诗二十四句，以七言为主，间以九言、二言，长短交错，节奏随情感起伏而变化。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>雅坤朗诵《茅屋为秋风所破歌》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1Q441127sM&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="雅坤朗诵《茅屋为秋风所破歌》"></iframe>
        <a href="https://www.bilibili.com/video/BV1Q441127sM" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>奇然沈谧仁演唱《茅屋为秋风所破歌》MV（四川卫视花开天下）</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1e64y1Z7SX&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="奇然沈谧仁《茅屋为秋风所破歌》MV"></iframe>
        <a href="https://www.bilibili.com/video/BV1e64y1Z7SX" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>人物形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">忧国忧民的诗人形象</div>
        <p>诗中的杜甫，是一个衰老、贫困、却始终心怀天下的诗人形象。他~L~老无力~R~，被群童欺负也只能~L~倚杖自叹息~R~；他~L~布衾多年冷似铁~R~，在漏雨的茅屋中彻夜难眠。然而，正是这样一个自身难保的人，在最痛苦的时刻想到的不是自己，而是~L~天下寒士~R~，甚至愿意以~L~吾庐独破受冻死亦足~R~来换取他人的安居。这种由己及人、舍己为人的精神，正是~L~诗圣~R~最动人的人格光辉。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">叙事与抒情结合</div>
        <p>全诗前三部分以叙事为主：秋风破屋、群童抱茅、夜雨湿床，按时间顺序层层推进，把诗人的苦难写得具体可感。第四部分则由叙事转入抒情，发出~L~安得广厦千万间~R~的宏愿。叙事是抒情的基础，抒情是叙事的升华，二者水乳交融。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">长短句交错，节奏随情而变</div>
        <p>全诗以七言为主，但间以~L~呜呼！~R~（二言）、~L~安得广厦千万间~R~（九言）等长短句式。前三部分句式较整齐，节奏沉郁；第四部分句式加长，节奏变得激昂奔放，与诗人情感的升华同步。~L~呜呼~R~一叹，如异军突起，把情感推向高潮。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">虚实结合，由实入虚</div>
        <p>前三部分写的是眼前实景：风、茅、群童、夜雨、布衾，都是具体可感的事物。第四部分~L~安得广厦千万间~R~则转入虚写，是诗人的理想与祈愿。由实入虚，由己及人，使诗歌的境界从个人的茅屋拓展到天下的广厦，从一时的苦难升华到永恒的人道主义关怀。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">语言质朴，炼字精当</div>
        <p>全诗语言朴素自然，如话家常，却字字千钧。~L~卷~R~~L~飞~R~~L~洒~R~~L~挂罥~R~~L~飘转~R~~L~沉~R~等动词，把风卷茅草的过程写得历历在目；~L~冷似铁~R~~L~如麻~R~~L~安如山~R~等比喻，贴切而有力。~L~怒号~R~~L~漠漠~R~~L~突兀~R~等词语，各尽其妙。质朴中见功力，自然中见匠心。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">安得广厦千万间，大庇天下寒士俱欢颜！</div>
        <p>全诗的核心名句。~L~安得~R~二字，既是发问，也是祈愿，道出了千百年来穷苦人民的共同渴望。~L~广厦千万间~R~以夸张写数量之多，~L~大庇天下寒士~R~写庇护之广，~L~俱欢颜~R~写效果之好。诗人由一己之苦想到天下之苦，由一己之愿升华为普世之愿，境界豁然开阔，成为中国文学史上最著名的人道主义宣言。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">何时眼前突兀见此屋，吾庐独破受冻死亦足！</div>
        <p>全诗的最强音，也是杜甫人格的写照。~L~突兀~R~写广厦高耸之态，~L~见此屋~R~是最热切的期盼。而~L~吾庐独破受冻死亦足~R~一句，以决绝之语写出牺牲精神——诗人宁愿自己独破受冻而死，也要换取天下寒士的安居。这种~L~先天下之忧而忧，后天下之乐而乐~R~的精神，正是杜甫被尊为~L~诗圣~R~的根本原因。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《茅屋为秋风所破歌》通过描写诗人自己茅屋被秋风所破、夜雨湿床的苦难经历，表达了对天下寒士的深切同情，抒发了~L~安得广厦千万间，大庇天下寒士俱欢颜~R~的美好理想，展现了诗人忧国忧民、舍己为人的崇高精神。</p>
    <p>诗歌的深刻之处，在于它不是停留在对个人苦难的悲叹上，而是由己及人，由小见大，把个人的命运与天下人的命运紧密联系在一起。诗人自己身处困境，却心系天下，甚至愿意以自身的牺牲换取他人的幸福。这种博大的胸怀和崇高的精神，使这首诗超越了时代，具有永恒的价值。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 词类活用 · 句式 · 文化常识</span></div>

  <div class="box">
    <h3>通假字</h3>
    <div class="tw"><table>
      <tr><th>字</th><th>通假</th><th>例句</th><th>释义</th></tr>
      <tr><td class="kai">见</td><td>通~L~现~R~</td><td>何时眼前突兀见此屋</td><td>出现。读 xiàn</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">秋天</td><td>秋季的天空</td><td>秋季</td><td>秋天漠漠向昏黑</td></tr>
      <tr><td class="kai">盗贼</td><td>抢东西的人（激愤之语）</td><td>偷窃或抢劫财物的人</td><td>忍能对面为盗贼</td></tr>
      <tr><td class="kai">寒士</td><td>贫寒的读书人</td><td>贫寒的人（泛指）</td><td>大庇天下寒士俱欢颜</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>词类活用</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">怒</td><td>形容词作状语</td><td>愤怒地、猛烈地</td><td>八月秋高风怒号</td></tr>
      <tr><td class="kai">墨</td><td>名词作状语</td><td>像墨一样（黑）</td><td>俄顷风定云墨色</td></tr>
      <tr><td class="kai">铁</td><td>名词作状语</td><td>像铁一样（冷硬）</td><td>布衾多年冷似铁</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">反问句</td><td>长夜沾湿何由彻！</td><td>~L~何由~R~即~L~由何~R~，如何才能。以反问加强语气</td></tr>
      <tr><td class="kai">感叹句</td><td>安得广厦千万间，大庇天下寒士俱欢颜！</td><td>以感叹抒发强烈愿望</td></tr>
      <tr><td class="kai">省略句</td><td>（茅）高者挂罥长林梢，（茅）下者飘转沉塘坳</td><td>承前省略主语~L~茅~R~</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>歌行体</dt><dd>古代诗歌的一种体裁，属古体诗。~L~歌~R~与~L~行~R~本为乐曲名称，后成为诗体。句式自由，可长可短，可换韵，便于铺陈叙事、抒发情感。</dd></div>
      <div class="g-item"><dt>安史之乱</dt><dd>唐玄宗天宝十四载（755）至代宗广德元年（763），由安禄山、史思明发动的叛乱。历时八年，使唐朝由盛转衰，是杜甫诗歌的重要时代背景。</dd></div>
      <div class="g-item"><dt>成都草堂</dt><dd>杜甫在成都浣花溪畔营建的居所，又称~L~浣花草堂~R~。乾元二年（759）末杜甫入蜀，次年在亲友帮助下建成草堂，是杜甫一生中相对安定的时期。</dd></div>
      <div class="g-item"><dt>诗圣</dt><dd>后世对杜甫的尊称。杜甫的诗歌深刻反映社会现实，忧国忧民，人格崇高，被尊为~L~诗圣~R~，其诗被称为~L~诗史~R~。</dd></div>
      <div class="g-item"><dt>三重茅</dt><dd>~L~三~R~在古汉语中常为虚指，表示~L~多~R~。~L~三重茅~R~即多层茅草，并非确指三层。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《茅屋为秋风所破歌》杜甫</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">唐 · 杜甫</div>
  <h1 class="hero-title">茅屋为秋风所破歌</h1>
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
  <div class="sec-sub">全诗二十四句，分四部分：秋风破屋、群童抱茅、夜雨湿床、广厦庇寒。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《茅屋为秋风所破歌》</div>
  <div>杜甫 · 唐（712—770）· 上元二年（761）秋作于成都草堂</div>
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