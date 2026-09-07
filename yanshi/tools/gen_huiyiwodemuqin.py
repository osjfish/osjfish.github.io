# -*- coding: utf-8 -*-
"""《回忆我的母亲》朱德 课件生成器 —— 复用《背影》CSS/JS框架。
现代散文版式：逐段解读，卡片summary用"内容 · 手法"。
中文引号用 ~L~ / ~R~ 占位，生成前替换为 \u201c / \u201d。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'huiyiwodemuqin-zhude.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'huiyi_fs')


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


def annotate_text(text, word_list):
    """Apply annotations from word_list [(word, note), ...] to text, longest first."""
    items = sorted(word_list, key=lambda x: -len(x[0]))
    used = set()
    for w, n in items:
        if w in used:
            continue
        # Find first occurrence not already inside an annotation
        idx = text.find(w)
        while idx != -1:
            # Check if this position is inside an existing [[ ]]
            before = text[:idx]
            if before.count('[[') > before.count(']]'):
                idx = text.find(w, idx + 1)
                continue
            replacement = '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
            text = text[:idx] + replacement + text[idx + len(w):]
            used.add(w)
            break
    return text


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "得到母亲去世的消息，我很悲痛。我爱我母亲，特别是她勤劳一生，很多事情是值得我永远回忆的。",
    "我家是佃农。祖籍广东韶关，客籍人，在~L~湖广填四川~R~时迁移四川仪陇县马鞍场。世代为地主耕种，家境是贫苦的，和我们来往的朋友也都是老老实实的贫苦农民。",
    "母亲一共生了十三个儿女。因为家境贫穷，无法全部养活，只留下了八个。以后再生下的被迫溺死了。这在母亲心里是多么惨痛悲哀和无可奈何的事情啊！母亲把八个孩子一手养大成人。可是她的时间大半被家务和耕种占去了，没法多照顾孩子，只好让孩子们在地里爬着。",
    "母亲是个好劳动。从我能记忆时起，总是天不亮就起床。全家二十多口人，妇女们轮班煮饭，轮到就煮一年。母亲把饭煮了，还要种田，种菜，喂猪，养蚕，纺棉花。因为她身体高大结实，还能挑水挑粪。",
    "母亲这样地整日劳碌着。我到四五岁时就很自然地在旁边帮她的忙，到八九岁时就不但能挑能背，还会种地了。记得那时我从私塾回家，常见母亲在灶上汗流满面地烧饭，我就悄悄把书一放，挑水或放牛去了。有的季节里，我上午读书，下午种地；一到农忙，便整日在地里跟着母亲劳动。这个时期母亲教给我许多生产知识。",
    "佃户家庭的生活自然是艰苦的，可是由于母亲的聪明能干，也勉强过得下去。我们用桐子榨油来点灯，吃的是豌豆饭、菜饭、红薯饭、杂粮饭，把菜籽榨出的油放在饭里做调料。这类地主富人家看也不看的饭食，母亲却能做得使一家人吃起来有滋味。赶上丰年，才能缝上一些新衣服，衣服也是自己生产出来的。母亲亲手纺出线，请人织成布，染了颜色，我们叫它~L~家织布~R~，有铜钱那样厚。一套衣服老大穿过了，老二老三接着穿还穿不烂。",
    "勤劳的家庭是有规律有组织的。我的祖父是一个中国标本式的农民，到八九十岁还非耕田不可，不耕田就会害病，直到临死前不久还在地里劳动。祖母是家庭的组织者，一切生产事务由她管理分派，每年除夕就分派好一年的工作。每天天还没亮，母亲就第一个起身，接着听见祖父起来的声音，接着大家都离开床铺，喂猪的喂猪，砍柴的砍柴，挑水的挑水。母亲在家庭里极能任劳任怨。她性格和蔼，没有打骂过我们，也没有同任何人吵过架。因此，虽然在这样的大家庭里，长幼、伯叔、妯娌相处都很和睦。母亲同情贫苦的人——这是朴素的阶级意识，虽然自己不富裕，还周济和照顾比自己更穷的亲戚。她自己是很节省的。父亲有时吸点旱烟，喝点酒；母亲管束着我们，不允许我们染上一点。母亲那种勤劳俭朴的习惯，母亲那种宽厚仁慈的态度，至今还在我心中留有深刻的印象。",
    "但是灾难不因为中国农民的和平就不降临到他们身上。庚子年（1900）前后，四川连年旱灾，很多的农民饥饿、破产，不得不成群结队地去~L~吃大户~R~。我亲眼见到，六七百穿得破破烂烂的农民和他们的妻子儿女被所谓官兵一阵凶杀毒打，血溅四五十里，哭声动天。在这样的年月里，我家也遭受更多的困难，仅仅吃些小菜叶、高粱，通年没吃过白米。特别是乙未（1895）那一年，地主欺压佃户，要在租种的地上加租子，因为办不到，就趁大年除夕，威胁着我家要退佃，逼着我们搬家。在悲惨的情况下，我们一家人哭泣着连夜分散。从此我家被迫分两处住下。人手少了，又遇天灾，庄稼没收成，这是我家最悲惨的一次遭遇。母亲没有灰心，她对穷苦农民的同情和对为富不仁者的反感却更强烈了。母亲沉痛的三言两语的诉说以及我亲眼见到的许多不平事实，启发了我幼年时期反抗压迫追求光明的思想，使我决心寻找新的生活。",
    "我不久就离开母亲，因为我读书了。我是一个佃农家庭的子弟，本来是没有钱读书的。那时乡间豪绅地主的欺压，衙门差役的横蛮，逼得母亲和父亲决心节衣缩食培养出一个读书人来~L~支撑门户~R~。我念过私塾，光绪三十一年（1905）考了科举，以后又到更远的顺庆和成都去读书。这个时候的学费都是东挪西借来的，总共用了二百多块钱，直到我后来当护国军旅长时才还清。",
    "光绪三十四年（1908），我从成都读书回来，当了小学校长，这是我第一次接触社会。辛亥革命后，我离开家乡，远走云南，参加新军和同盟会。我到云南后，从家信中知道，我母亲对我这一举动不但不反对，还给我许多慰勉。",
    "从宣统元年（1909）到现在，我再没有回过一次家，只在民国八年（1919）我曾经把父亲和母亲接出来。但是他俩劳动惯了，离开土地就不舒服，所以还是回了家。父亲就在回家途中死了。母亲回家后继续劳动，一直到最后。",
    "中国共产党继续领导着中国革命，我将继续尽忠于我们的民族和人民，尽忠于我们的民族和人民的希望——中国共产党，使和母亲同样生活着的人能够过快乐的生活。这是我能做到的，一定能做到的。",
    "愿母亲在地下安息！",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "开篇点题 · 痛悼母亲", "第 1 段",
     "开篇点明写作缘由：母亲去世，~L~我~R~悲痛；以~L~勤劳一生~R~总领全文，奠定回忆与赞颂的基调。"),
    ("第二部分", "家境贫苦 · 母亲辛劳", "第 2–7 段",
     "回忆佃农家境与母亲的勤劳一生：生儿育女、整日劳碌、聪明能干、任劳任怨、宽厚仁慈，在艰苦中维持家庭，给~L~我~R~深刻影响。"),
    ("第三部分", "遭遇灾难 · 追求光明", "第 8–10 段",
     "写天灾人祸中家庭的悲惨遭遇，母亲没有灰心，反而加深了对穷苦人的同情和对为富不仁者的反感；母亲支持~L~我~R~读书、参加革命。"),
    ("第四部分", "思念母亲 · 尽忠人民", "第 11–13 段",
     "写与母亲的离别和母亲坚持劳动到最后；抒发对母亲的悼念，将对母亲的爱升华为对民族和人民的忠诚。"),
]

# 每段注释词表: [(词, 注), ...]
ANNO = [
    # P1
    [("去世", "（人）死去。世，人的一生"), ("悲痛", "悲伤哀痛"), ("勤劳一生", "勤劳了一辈子，概括母亲最突出的品格"), ("值得", "有价值、有意义"), ("回忆", "回想、记忆")],
    # P2
    [("佃农", "租种地主土地的农民。佃，diàn，租种"), ("祖籍", "祖先的原籍。籍，jí"), ("客籍人", "从外地迁徙来的住户，这里指客家人"), ("迁移", "离开原地搬到另一地"), ("世代", "世世代代、好几代"), ("耕种", "耕地种植"), ("家境", "家庭的经济状况"), ("贫苦", "贫穷困苦"), ("来往", "交往、交际"), ("老老实实", "淳朴、诚实、规矩")],
    # P3
    [("一共", "总共、加起来"), ("养活", "把幼儿养大成人"), ("溺死", "淹死。溺，nì，淹没在水里"), ("惨痛悲哀", "极其痛苦悲伤"), ("无可奈何", "没有办法，无法可想"), ("一手", "独自一个人、靠自己的力量"), ("养大成人", "抚养到成年"), ("家务", "家庭事务"), ("占去", "占用了"), ("爬着", "在地上爬行（形容无人照料）")],
    # P4
    [("好劳动", "劳动的好手，非常能干的劳动者"), ("记忆", "记得、回忆"), ("轮班", "轮流值班"), ("纺棉花", "把棉花纺成线。纺，fǎng，把丝棉纤维捻成线"), ("结实", "健壮、强健")],
    # P5
    [("劳碌", "忙碌劳累"), ("私塾", "旧时私人设立的教学场所。塾，shú"), ("汗流满面", "满脸是汗，形容劳累"), ("农忙", "农事繁忙的时节"), ("生产知识", "农业生产的知识和技能")],
    # P6
    [("勉强", "将就、凑合，能力不够还尽力做"), ("桐子", "油桐树的种子，可榨油。桐，tóng"), ("红薯", "甘薯、地瓜。薯，shǔ"), ("杂粮", "粗粮，除大米、小麦等主粮外的粮食"), ("菜籽", "蔬菜的种子，可榨油"), ("饭食", "饭和菜，泛指食物"), ("滋味", "味道，这里指好吃"), ("丰年", "丰收的年成"), ("家织布", "自己纺线织布做的布，区别于机织布"), ("铜钱", "古代铜质辅币，圆形中有方孔")],
    # P7
    [("标本式", "典型的、具有代表性的"), ("组织者", "负责安排、管理事务的人"), ("分派", "分别安排、分配"), ("除夕", "农历一年最后一天的夜晚"), ("任劳任怨", "做事不辞劳苦，不怕别人埋怨"), ("和蔼", "态度温和、亲切"), ("妯娌", "（zhóu li）哥哥和弟弟的妻子的合称"), ("和睦", "相处融洽、不争吵"), ("朴素", "朴实、不浮夸"), ("阶级意识", "对自己所属阶级的地位和利益的认识"), ("周济", "对穷困的人给予物质上的帮助"), ("旱烟", "用烟叶直接卷或装在烟袋里吸的烟"), ("管束", "加以约束，使不越轨"), ("勤劳俭朴", "勤劳节俭、朴素"), ("宽厚仁慈", "待人宽容厚道，仁爱慈善"), ("深刻", "程度深、不容易忘怀")],
    # P8
    [("降临", "来到、到来（多用于不幸的事）"), ("连年", "接连多年"), ("旱灾", "因长期干旱造成的灾害"), ("破产", "丧失全部财产，无法维持"), ("成群结队", "许多人聚集在一起，形成队伍"), ("吃大户", "旧社会饥民成群结队到地主家吃饭的斗争方式"), ("破破烂烂", "形容衣服破旧不堪"), ("凶杀毒打", "凶狠地屠杀、残酷地殴打"), ("血溅", "鲜血飞溅"), ("通年", "一整年、全年"), ("欺压", "欺负压迫"), ("退佃", "地主收回租给农民的土地"), ("连夜", "当天夜里、一夜之间"), ("收成", "农作物的收获情况"), ("为富不仁者", "靠剥削发财致富而没有好心肠的人"), ("反感", "不满、厌恶的情绪"), ("三言两语", "几句话，形容话很少"), ("不平", "不公正、不公平"), ("启发", "开导指点，使有所领悟"), ("反抗压迫", "反对并抵抗压迫"), ("追求光明", "向往和争取自由、幸福的社会")],
    # P9
    [("子弟", "儿子、弟弟等晚辈，这里指儿子"), ("豪绅", "地方上依仗权势欺压百姓的绅士。绅，shēn"), ("差役", "（chāi yì）旧时在衙门中当差的人"), ("横蛮", "粗暴、蛮横不讲理"), ("节衣缩食", "省吃省穿，泛指节俭"), ("支撑门户", "维持家庭的体面和地位"), ("科举", "隋唐至清代选拔官吏的考试制度"), ("顺庆", "地名，今四川南充一带"), ("东挪西借", "到处挪借钱款"), ("护国军", "1915年反对袁世凯称帝的军队"), ("旅长", "旅的军事长官，旅是军队编制单位")],
    # P10
    [("接触社会", "走上社会，与社会上的人交往"), ("辛亥革命", "1911年推翻清朝统治的资产阶级民主革命"), ("新军", "清末仿照西方军制编练的新式陆军"), ("同盟会", "中国同盟会，资产阶级革命政党，1905年成立"), ("家信", "家人之间往来的书信"), ("举动", "行动、行为"), ("慰勉", "安慰勉励。慰，wèi；勉，miǎn")],
    # P11
    [("接出来", "接到自己身边来"), ("劳动惯了", "习惯了劳动，不劳动就不舒服"), ("不舒服", "这里指不适应、不习惯"), ("途中", "路途中、半路上"), ("继续", "接着、延续下去")],
    # P12
    [("尽忠", "竭尽忠诚"), ("民族", "历史上形成的处于不同社会发展阶段的各种人的共同体"), ("希望", "这里指寄托理想的对象"), ("同样", "一样、没有差别"), ("快乐", "感到幸福或满意")],
    # P13
    [("安息", "安静地休息（多用于悼念死者）")],
]

# 每段: (内容概括, 手法分析)
CONTENT_TECH = [
    ("开篇点题：母亲去世，~L~我~R~悲痛；以~L~勤劳一生~R~总领全文，点明回忆的缘由。",
     "开门见山，直接抒情；~L~勤劳一生~R~是全文的文眼，总领下文对母亲的回忆；~L~永远回忆~R~奠定全文思念与赞颂的基调。"),
    ("交代家庭出身：佃农，祖籍广东，~L~湖广填四川~R~时迁居四川；世代为地主耕种，家境贫苦。",
     "交代背景，为下文写母亲的勤劳和家庭的苦难做铺垫；~L~老老实实~R~写农民的淳朴，也暗示被欺压的命运。"),
    ("写母亲生育之多与养育之难：十三个儿女只活八个，被迫溺死新生婴儿；母亲一手养大八个孩子，却无暇多照顾。",
     "以具体数字（十三、八）写母亲的苦难；~L~惨痛悲哀~R~~L~无可奈何~R~直接抒情，见母亲内心的痛苦；~L~在地里爬着~R~细节写孩子无人照料的辛酸。"),
    ("写母亲是劳动能手：天不亮起床，煮饭之外还要种田、种菜、喂猪、养蚕、纺棉花，甚至挑水挑粪。",
     "以一连串动词（煮、种、喂、养、纺、挑）写母亲的勤劳；~L~总是~R~写常年如此；排比短句，节奏紧凑，见母亲从早到晚不停劳作。"),
    ("写~L~我~R~在母亲影响下从小参加劳动：四五岁帮忙，八九岁能挑能背；母亲的身教让~L~我~R~学会劳动和生产知识。",
     "以~L~我~R~的成长侧面写母亲的影响；~L~汗流满面~R~细节写母亲的辛劳；~L~悄悄把书一放~R~写孩子的懂事，也见母亲榜样的力量。"),
    ("写母亲在艰苦生活中的聪明能干：用桐油点灯、粗粮细做、自纺自织~L~家织布~R~，衣服老大穿了老二老三接着穿。",
     "以具体的吃穿细节写母亲的勤俭持家；~L~看也不看~R~与~L~有滋味~R~对比，见母亲的能干；~L~铜钱那样厚~R~写家织布的结实，侧面写母亲的手艺。"),
    ("写勤劳家庭的组织性和母亲的品格：祖父勤劳、祖母持家，母亲任劳任怨、性格和蔼、同情穷人、节俭持家；母亲的勤劳俭朴和宽厚仁慈给~L~我~R~深刻印象。",
     "排比（喂猪的喂猪，砍柴的砍柴，挑水的挑水）写家庭劳动的有序；~L~没有打骂过~R~~L~没有同任何人吵过架~R~写母亲的宽厚；结尾两句~L~母亲那种……~R~反复，总结母亲的品格，抒发感激之情。"),
    ("写天灾人祸中农民的苦难和家庭的悲惨遭遇：四川旱灾、农民被官兵屠杀、我家被地主退佃逼迁；母亲没有灰心，反而加深了对穷苦人的同情和对为富不仁者的反感，启发~L~我~R~追求光明。",
     "~L~血溅四五十里，哭声动天~R~以夸张手法写农民被屠杀的惨状；~L~通年没吃过白米~R~写生活的极端困苦；~L~母亲没有灰心~R~笔锋一转，写母亲的坚强；结尾写母亲对~L~我~R~思想的启蒙，深化主题。"),
    ("写~L~我~R~离家读书的缘由：地主和差役的欺压，逼得父母节衣缩食供~L~我~R~读书；学费靠借贷，直到~L~我~R~当旅长才还清。",
     "~L~逼得~R~写读书是被迫的选择，见社会的黑暗；~L~东挪西借~R~~L~二百多块钱~R~~L~才还清~R~写求学的艰难，也见父母的决心和付出。"),
    ("写~L~我~R~走向社会和革命：当校长、参加新军和同盟会；母亲不但不反对，还写信慰勉。",
     "以时间为序写~L~我~R~的成长；~L~不但不反对，还给我许多慰勉~R~写母亲的深明大义，支持儿子的革命选择。"),
    ("写与母亲的长期分离：1909年后再没回家，1919年接父母出来但他们不习惯又回去了，父亲途中去世，母亲回家后继续劳动到最后。",
     "~L~劳动惯了，离开土地就不舒服~R~写劳动人民的本色；~L~一直到最后~R~写母亲终生勤劳，呼应开头~L~勤劳一生~R~。"),
    ("抒发对母亲的悼念升华为对民族和人民的忠诚：~L~我~R~将尽忠于民族和人民，让像母亲一样的劳苦大众过上快乐生活。",
     "由爱母亲到爱人民，由悼念母亲到献身革命，主题升华；~L~这是我能做到的，一定能做到的~R~反复，语气坚定，见革命信念。"),
    ("以祈愿收束全文，表达对母亲的深切悼念。",
     "独句成段，简短有力；~L~安息~R~与开头~L~悲痛~R~呼应，情感由悲痛转为崇敬与告慰。"),
]

# Build S data
S = []
part_map = [0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3]
for i in range(13):
    annotated = annotate_text(FULLTEXT[i], ANNO[i])
    S.append((part_map[i], annotated, CONTENT_TECH[i][0], CONTENT_TECH[i][1]))


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"佃","py":"diàn","q":"我家是□农，祖籍广东韶关","tip":"「佃」单人旁，音 diàn，租种地主土地，勿写「店」「甸」"},
    {"w":"籍","py":"jí","q":"客□人，在湖广填四川时迁移四川","tip":"「籍」竹字头，音 jí，籍贯、户籍，与「藉」（草字头）区分"},
    {"w":"溺","py":"nì","q":"以后再生下的被迫□死了","tip":"「溺」三点水，音 nì，淹没，勿写「弱」"},
    {"w":"碌","py":"lù","q":"母亲这样地整日劳□着","tip":"「碌」石字旁，音 lù，忙碌，勿写「绿」（绞丝旁）"},
    {"w":"塾","py":"shú","q":"记得那时我从私□回家","tip":"「塾」土字底，音 shú，旧时教学场所，勿写「熟」"},
    {"w":"桐","py":"tóng","q":"我们用□子榨油来点灯","tip":"「桐」木字旁，音 tóng，油桐树，勿写「铜」（金字旁）"},
    {"w":"薯","py":"shǔ","q":"吃的是豌豆饭、菜饭、红□饭","tip":"「薯」草字头，音 shǔ，红薯，勿写「暑」（日字头）"},
    {"w":"纺","py":"fǎng","q":"母亲亲手□出线，请人织成布","tip":"「纺」绞丝旁，音 fǎng，纺线，勿写「访」（言字旁）"},
    {"w":"怨","py":"yuàn","q":"母亲在家庭里极能任劳任□","tip":"「怨」心字底，音 yuàn，埋怨，勿写「愿」"},
    {"w":"妯","py":"zhóu","q":"长幼、伯叔、□娌相处都很和睦","tip":"「妯」女字旁，音 zhóu，「妯娌」指兄弟的妻子，勿写「轴」（车字旁）"},
    {"w":"娌","py":"li","q":"长幼、伯叔、妯□相处都很和睦","tip":"「娌」女字旁，音 li，「妯娌」合称，勿写「里」"},
    {"w":"济","py":"jì","q":"还周□和照顾比自己更穷的亲戚","tip":"「济」三点水，音 jì，周济、救济，勿写「挤」（提手旁）"},
    {"w":"俭","py":"jiǎn","q":"逼得母亲和父亲决心节衣□食培养出一个读书人","tip":"「俭」单人旁，音 jiǎn，节俭，与「检」（木字旁）区分"},
    {"w":"绅","py":"shēn","q":"那时乡间豪□地主的欺压","tip":"「绅」绞丝旁，音 shēn，绅士，勿写「伸」（单人旁）"},
    {"w":"差","py":"chāi","q":"衙门□役的横蛮","tip":"「差」此处读 chāi，差役，勿读 chà（差不多）"},
    {"w":"挪","py":"nuó","q":"这个时候的学费都是东□西借来的","tip":"「挪」提手旁，音 nuó，挪动、借贷，勿写「娜」（女字旁）"},
    {"w":"慰","py":"wèi","q":"还给我许多□勉","tip":"「慰」心字底，音 wèi，安慰，勿写「蔚」（草字头）"},
    {"w":"勉","py":"miǎn","q":"还给我许多慰□","tip":"「勉」力字旁，音 miǎn，勉励，勿写「免」"},
    {"w":"忠","py":"zhōng","q":"我将继续尽□于我们的民族和人民","tip":"「忠」心字底，音 zhōng，忠诚，勿写「中」"},
    {"w":"惨","py":"cǎn","q":"这在母亲心里是多么痛□悲哀","tip":"「惨」竖心旁，音 cǎn，悲惨，勿写「残」（歹字旁）"},
    {"w":"慈","py":"cí","q":"母亲那种宽厚仁□的态度","tip":"「慈」心字底，音 cí，仁慈，勿写「瓷」（瓦字旁）"},
    {"w":"榨","py":"zhà","q":"我们用桐子□油来点灯","tip":"「榨」木字旁，音 zhà，压出物体里的汁液，勿写「诈」（言字旁）"},
    {"w":"粱","py":"liáng","q":"仅仅吃些小菜叶、高□，通年没吃过白米","tip":"「粱」米字底，音 liáng，高粱，与「梁」（木字底，桥梁）区分"},
]

DICT_NOTES = [
    {"w":"佃农","a":"租种地主土地的农民。佃，diàn","q":"我家是佃农"},
    {"w":"客籍人","a":"从外地迁徙来的住户，这里指客家人","q":"祖籍广东韶关，客籍人"},
    {"w":"湖广填四川","a":"明清时期大规模移民运动，湖广地区人口迁入四川","q":"在~L~湖广填四川~R~时迁移四川仪陇县马鞍场"},
    {"w":"溺死","a":"淹死。溺，nì，淹没在水里","q":"以后再生下的被迫溺死了"},
    {"w":"无可奈何","a":"没有办法，无法可想","q":"这在母亲心里是多么惨痛悲哀和无可奈何的事情啊"},
    {"w":"好劳动","a":"劳动的好手，非常能干的劳动者","q":"母亲是个好劳动"},
    {"w":"劳碌","a":"忙碌劳累","q":"母亲这样地整日劳碌着"},
    {"w":"私塾","a":"旧时私人设立的教学场所","q":"记得那时我从私塾回家"},
    {"w":"农忙","a":"农事繁忙的时节","q":"一到农忙，便整日在地里跟着母亲劳动"},
    {"w":"桐子","a":"油桐树的种子，可榨油","q":"我们用桐子榨油来点灯"},
    {"w":"家织布","a":"自己纺线织布做的布，区别于机织布","q":"我们叫它~L~家织布~R~，有铜钱那样厚"},
    {"w":"标本式","a":"典型的、具有代表性的","q":"我的祖父是一个中国标本式的农民"},
    {"w":"任劳任怨","a":"做事不辞劳苦，不怕别人埋怨","q":"母亲在家庭里极能任劳任怨"},
    {"w":"妯娌","a":"（zhóu li）哥哥和弟弟的妻子的合称","q":"长幼、伯叔、妯娌相处都很和睦"},
    {"w":"周济","a":"对穷困的人给予物质上的帮助","q":"还周济和照顾比自己更穷的亲戚"},
    {"w":"管束","a":"加以约束，使不越轨","q":"母亲管束着我们，不允许我们染上一点"},
    {"w":"吃大户","a":"旧社会饥民成群结队到地主家吃饭的斗争方式","q":"不得不成群结队地去~L~吃大户~R~"},
    {"w":"为富不仁","a":"靠剥削发财致富的人没有好心肠","q":"她对穷苦农民的同情和对为富不仁者的反感却更强烈了"},
    {"w":"豪绅","a":"地方上依仗权势欺压百姓的绅士","q":"那时乡间豪绅地主的欺压"},
    {"w":"差役","a":"（chāi yì）旧时在衙门中当差的人","q":"衙门差役的横蛮"},
    {"w":"节衣缩食","a":"省吃省穿，泛指节俭","q":"逼得母亲和父亲决心节衣缩食培养出一个读书人"},
    {"w":"支撑门户","a":"维持家庭的体面和地位","q":"培养出一个读书人来~L~支撑门户~R~"},
    {"w":"慰勉","a":"安慰勉励","q":"还给我许多慰勉"},
    {"w":"尽忠","a":"竭尽忠诚","q":"我将继续尽忠于我们的民族和人民"},
    {"w":"勤劳一生","a":"勤劳了一辈子，概括母亲最突出的品格","q":"特别是她勤劳一生"},
    {"w":"宽厚仁慈","a":"待人宽容厚道，仁爱慈善","q":"母亲那种宽厚仁慈的态度"},
    {"w":"三言两语","a":"几句话，形容话很少","q":"母亲沉痛的三言两语的诉说"},
    {"w":"东挪西借","a":"到处挪借钱款","q":"这个时候的学费都是东挪西借来的"},
    {"w":"通年","a":"一整年、全年","q":"通年没吃过白米"},
    {"w":"连夜","a":"当天夜里、一夜之间","q":"我们一家人哭泣着连夜分散"},
]


# ---------------- 组装 ----------------
def build_verses():
    out, idx = [], 0
    for pi, part in enumerate(PARTS):
        out.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>'
                   % (part[0], part[1], part[2]))
        out.append('      <div class="part-overview">%s</div>' % fixq(part[3]))
        for si, (p, txt, content, technique) in enumerate(S):
            if p != pi:
                continue
            idx += 1
            out.append('      <div class="verse" id="l%d" data-i="%d">' % (idx, idx - 1))
            out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx, fixq(txt)))
            out.append('        <details class="v-more">')
            out.append('          <summary>内容 · 手法</summary>')
            out.append('          <div class="d-body">')
            out.append('            <div class="v-sec"><b class="v-label">内容概括</b>')
            out.append('              <div class="v-trans">%s</div>' % fixq(content))
            out.append('            </div>')
            out.append('            <div class="v-sec"><b class="v-label">手法分析</b>')
            out.append('              <div class="d-body"><p>%s</p></div>' % fixq(technique))
            out.append('            </div>')
            out.append('          </div>')
            out.append('        </details>')
            out.append('      </div>')
    return '\n'.join(out), idx


verses_html, total = build_verses()
full_html = '\n'.join('    <div class="pl">%s</div>' % fixq(p) for p in FULLTEXT)
anno_count = sum(len(a) for a in ANNO)

BG = fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《回忆我的母亲》是朱德同志为悼念母亲而写的一篇回忆性散文，发表于1944年4月5日延安《解放日报》。文章以质朴平实的语言，回忆了母亲勤劳的一生，赞颂了母亲的优秀品质，抒发了对母亲的深切悼念，并将对母亲的爱升华为对民族和人民的忠诚。</p>
    <p>全文以~L~勤劳一生~R~为线索，按时间顺序组织材料，从家境贫苦、母亲辛劳，到遭遇灾难、追求光明，再到思念母亲、尽忠人民，层层递进。语言朴素无华，却感人至深，是回忆性散文的典范之作。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>朱德（1886—1976），字玉阶，四川仪陇人。伟大的马克思主义者，伟大的无产阶级革命家、政治家、军事家，中国人民解放军的主要缔造者之一，中华人民共和国的开国元勋。曾任中国人民解放军总司令、中华人民共和国副主席、全国人大常委会委员长等职。</p>
    <p>朱德出身于佃农家庭，幼年在母亲的影响下参加劳动，后考入云南陆军讲武堂，参加辛亥革命和护国战争。1922年赴德国留学，同年加入中国共产党。他的一生是为中国人民解放事业和共产主义事业奋斗的一生。</p>
    <p class="note">※ 《回忆我的母亲》写于1944年，当时朱德的母亲钟太夫人于2月15日在四川仪陇老家逝世，享年八十六岁。朱德在延安得知消息后，写下这篇悼念文章。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>母亲逝世：</b>1944年2月15日，朱德的母亲钟太夫人在四川仪陇老家逝世。朱德当时在延安领导八路军抗战，无法回乡奔丧，于4月5日在延安《解放日报》发表《回忆我的母亲》一文，以寄托哀思。</p>
    <p><b>时代背景：</b>20世纪上半叶的中国，外有列强侵略，内有地主压迫，农民生活极端困苦。朱德的母亲就是千百万劳苦大众中的一员——她勤劳一生，却始终在贫困中挣扎。文章通过回忆母亲，也写出了旧中国农民的苦难和不屈。</p>
    <p><b>写作动机：</b>朱德在文中说：~L~我爱我母亲，特别是她勤劳一生，很多事情是值得我永远回忆的。~R~他写母亲，不仅是表达儿子的悼念，更是要通过母亲的形象，赞颂千百万劳动人民的优秀品质，并将对母亲的感情升华为对民族和人民的忠诚。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文朗读《回忆我的母亲》朱德</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1Jt4y1X7Fz&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读《回忆我的母亲》"></iframe>
        <a href="https://www.bilibili.com/video/BV1Jt4y1X7Fz" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>课文讲解《回忆我的母亲》</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1zK8QzNEDH&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文讲解《回忆我的母亲》"></iframe>
        <a href="https://www.bilibili.com/video/BV1zK8QzNEDH" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 主题</span></div>

  <div class="box">
    <h3>人物形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">母亲——勤劳一生的劳动妇女典范</div>
        <p><b>勤劳能干：</b>~L~母亲是个好劳动~R~，天不亮就起床，煮饭、种田、种菜、喂猪、养蚕、纺棉花、挑水挑粪，从早到晚不停劳作。她还能把粗粮做得~L~有滋味~R~，自纺自织~L~家织布~R~，在艰苦中维持家庭。</p>
        <p><b>任劳任怨、宽厚仁慈：</b>在二十多口人的大家庭里，母亲~L~极能任劳任怨~R~，性格和蔼，~L~没有打骂过我们，也没有同任何人吵过架~R~，长幼、伯叔、妯娌相处和睦。她同情贫苦人，虽然自己不富裕，还周济更穷的亲戚。</p>
        <p><b>坚强不屈、深明大义：</b>面对天灾人祸和地主的欺压，~L~母亲没有灰心~R~，反而加深了对穷苦人的同情和对为富不仁者的反感。她支持儿子读书、参加革命，~L~不但不反对，还给我许多慰勉~R~。</p>
        <p><b>终生劳动：</b>~L~劳动惯了，离开土地就不舒服~R~，回家后~L~继续劳动，一直到最后~R~。母亲的一生，是勤劳的一生，也是千百万劳动人民的缩影。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">以时间为序，线索清晰</div>
        <p>全文以~L~勤劳一生~R~为线索，按时间顺序组织材料：从家境出身、母亲辛劳，到遭遇灾难、追求光明，再到离别思念、尽忠人民。时间线索清晰，层次分明，将母亲的一生和~L~我~R~的成长交织在一起。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">语言质朴，情感真挚</div>
        <p>文章没有华丽的辞藻，没有刻意的煽情，用最朴素的语言写最平凡的事，却感人至深。~L~得到母亲去世的消息，我很悲痛~R~~L~愿母亲在地下安息~R~，寥寥数语，悲痛之情溢于言表。这种~L~于平淡中见深情~R~的写法，是回忆性散文的高境界。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">以小见大，主题升华</div>
        <p>文章写的是~L~我~R~的母亲，但母亲的形象代表了千百万劳动人民。结尾由爱母亲升华为爱人民、尽忠民族：~L~使和母亲同样生活着的人能够过快乐的生活~R~，将个人的悼念之情升华为革命的信念，以小见大，深化了主题。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">细节描写，生动传神</div>
        <p>文章善于用细节表现人物：~L~汗流满面地烧饭~R~写母亲的辛劳，~L~悄悄把书一放，挑水或放牛去了~R~写孩子的懂事，~L~一套衣服老大穿过了，老二老三接着穿还穿不烂~R~写家织布的结实和家庭的节俭。这些细节真实生动，如在眼前。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《回忆我的母亲》通过回忆母亲勤劳的一生，赞颂了母亲勤劳俭朴、宽厚仁慈、坚强不屈的优秀品质，抒发了对母亲的深切悼念和感激之情。</p>
    <p>文章的深刻之处在于，它没有停留在个人的母子之情上，而是将对母亲的爱升华为对民族和人民的忠诚——母亲是千百万劳动人民的一员，爱母亲就是爱人民，报答母亲就是要让~L~和母亲同样生活着的人能够过快乐的生活~R~。这种由家到国、由亲到民的情感升华，使文章具有了超越个人悼念的深刻社会意义。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">重点词语 · 用字与读音 · 修辞 · 写作借鉴</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">佃农</span><span class="acc-d">租种地主土地的农民。佃，diàn。</span></div>
      <div class="acc-item"><span class="acc-w">客籍人</span><span class="acc-d">从外地迁徙来的住户，这里指客家人。</span></div>
      <div class="acc-item"><span class="acc-w">溺死</span><span class="acc-d">淹死。溺，nì，淹没在水里。</span></div>
      <div class="acc-item"><span class="acc-w">无可奈何</span><span class="acc-d">没有办法，无法可想。</span></div>
      <div class="acc-item"><span class="acc-w">好劳动</span><span class="acc-d">劳动的好手，非常能干的劳动者。</span></div>
      <div class="acc-item"><span class="acc-w">劳碌</span><span class="acc-d">忙碌劳累。</span></div>
      <div class="acc-item"><span class="acc-w">私塾</span><span class="acc-d">旧时私人设立的教学场所。</span></div>
      <div class="acc-item"><span class="acc-w">标本式</span><span class="acc-d">典型的、具有代表性的。</span></div>
      <div class="acc-item"><span class="acc-w">任劳任怨</span><span class="acc-d">做事不辞劳苦，不怕别人埋怨。</span></div>
      <div class="acc-item"><span class="acc-w">妯娌</span><span class="acc-d">（zhóu li）哥哥和弟弟的妻子的合称。</span></div>
      <div class="acc-item"><span class="acc-w">周济</span><span class="acc-d">对穷困的人给予物质上的帮助。</span></div>
      <div class="acc-item"><span class="acc-w">管束</span><span class="acc-d">加以约束，使不越轨。</span></div>
      <div class="acc-item"><span class="acc-w">为富不仁</span><span class="acc-d">靠剥削发财致富的人没有好心肠。为富，靠剥削发财；不仁，没有好心肠。</span></div>
      <div class="acc-item"><span class="acc-w">豪绅</span><span class="acc-d">地方上依仗权势欺压百姓的绅士。</span></div>
      <div class="acc-item"><span class="acc-w">差役</span><span class="acc-d">（chāi yì）旧时在衙门中当差的人。</span></div>
      <div class="acc-item"><span class="acc-w">节衣缩食</span><span class="acc-d">省吃省穿，泛指节俭。</span></div>
      <div class="acc-item"><span class="acc-w">慰勉</span><span class="acc-d">安慰勉励。</span></div>
      <div class="acc-item"><span class="acc-w">尽忠</span><span class="acc-d">竭尽忠诚。</span></div>
      <div class="acc-item"><span class="acc-w">通年</span><span class="acc-d">一整年、全年。</span></div>
      <div class="acc-item"><span class="acc-w">连夜</span><span class="acc-d">当天夜里、一夜之间。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">佃</span><span class="acc-d">（diàn）租种。~L~佃农~R~即租种地主土地的农民。不读 tián。</span></div>
      <div class="acc-item"><span class="acc-w">籍</span><span class="acc-d">（jí）籍贯、户籍。竹字头，与~L~藉~R~（草字头，杂乱、垫）区分。</span></div>
      <div class="acc-item"><span class="acc-w">溺</span><span class="acc-d">（nì）淹没。~L~溺死~R~即淹死。不读 ruò。</span></div>
      <div class="acc-item"><span class="acc-w">塾</span><span class="acc-d">（shú）旧时教学场所。~L~私塾~R~。土字底，不写~L~熟~R~。</span></div>
      <div class="acc-item"><span class="acc-w">妯娌</span><span class="acc-d">（zhóu li）兄弟的妻子的合称。女字旁，不写~L~轴~R~~L~里~R~。</span></div>
      <div class="acc-item"><span class="acc-w">差</span><span class="acc-d">（chāi）~L~差役~R~。多音字，又读 chà（差不多）、chā（差别）、cī（参差）。</span></div>
      <div class="acc-item"><span class="acc-w">粱</span><span class="acc-d">（liáng）~L~高粱~R~。米字底，与~L~梁~R~（木字底，桥梁、房梁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">慈</span><span class="acc-d">（cí）仁爱。~L~仁慈~R~。心字底，不写~L~瓷~R~。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞方法</h3>
      <div class="acc-item"><span class="acc-w">反复</span><span class="acc-d">~L~母亲那种勤劳俭朴的习惯，母亲那种宽厚仁慈的态度~R~，两个~L~母亲那种~R~反复，强调母亲品格对~L~我~R~的深刻影响。</span></div>
      <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">~L~喂猪的喂猪，砍柴的砍柴，挑水的挑水~R~，排比写家庭劳动的有序和忙碌。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">~L~这类地主富人家看也不看的饭食，母亲却能做得使一家人吃起来有滋味~R~，以地主富人家的不屑与母亲的能干对比。</span></div>
      <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">~L~血溅四五十里，哭声动天~R~，以夸张手法写农民被屠杀的惨状。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">以时间为序</span><span class="acc-d">按时间顺序组织材料，从过去到现在，线索清晰，层次分明。写回忆性文章可借鉴这种结构。</span></div>
      <div class="acc-item"><span class="acc-w">以小见大</span><span class="acc-d">通过写自己的母亲，赞颂千百万劳动人民；由个人的悼念升华为对民族和人民的忠诚。选材要小，开掘要深。</span></div>
      <div class="acc-item"><span class="acc-w">细节描写</span><span class="acc-d">善于用具体细节表现人物品格，如~L~汗流满面地烧饭~R~~L~悄悄把书一放~R~等，真实生动，如在眼前。</span></div>
      <div class="acc-item"><span class="acc-w">语言质朴</span><span class="acc-d">不用华丽辞藻，用最朴素的语言写最平凡的事，于平淡中见深情。情感真挚是回忆性散文的灵魂。</span></div>
      <div class="acc-item"><span class="acc-w">首尾呼应</span><span class="acc-d">开头~L~得到母亲去世的消息，我很悲痛~R~，结尾~L~愿母亲在地下安息~R~，首尾呼应，结构完整。</span></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《回忆我的母亲》朱德</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 朱德</div>
  <h1 class="hero-title">回忆我的母亲</h1>
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
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 内容 · 手法</span></div>
  <div class="sec-sub">全文十三段，分四部分：开篇点题、家境贫苦与母亲辛劳、遭遇灾难与追求光明、思念母亲与尽忠人民。每段含内容概括与手法分析，点击可展开。</div>
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
      <button data-mode="note" data-rand="5">随机五组词语</button>
      <button data-mode="note" data-all="1">全部词语</button>
    </div>
  </section>

<footer>
  <div class="kai">《回忆我的母亲》</div>
  <div>朱德 · 现代 · 1944年作于延安 · 回忆性散文</div>
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
