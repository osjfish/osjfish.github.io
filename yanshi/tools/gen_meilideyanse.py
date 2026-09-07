# -*- coding: utf-8 -*-
"""《美丽的颜色》艾芙·居里 课件生成器 —— 复用《背影》CSS/JS框架。
现代散文版式：逐段解读，卡片summary用"内容 · 手法"。
外国作者卷首标"法国 · 艾芙·居里"。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'meilideyanse-aifujuli.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'yanse_fs')


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
    "玛丽·斯可罗多夫斯卡的学生生活中最愉快的时期，是在顶楼里度过的；玛丽·居里现在又要在一个残破的小屋里，尝到新的极大的快乐了。这是一种奇异的新的开始，这种艰苦而且微妙的快乐（无疑地在玛丽以前没有一个妇女体验过），两次都挑选了最简陋的布景。",
    "娄蒙路的棚屋，可以说是不舒服的典型。在夏天，因为棚顶是玻璃的，棚屋里面燥热得像温室。在冬天，简直不知道是应该希望下霜还是应该希望下雨。若是下雨，雨水就以一种令人厌烦的轻柔的声音，一滴一滴地落在地上，落在工作台上，落在这两个物理学家的标上记号永不放仪器的地方；若是下霜，就连人都冻僵了，没有方法补救。那个炉子即使把它烧到炽热的程度，也令人完全失望。走到差不多可以碰着它的地方，才能感受一点儿暖气，可是离开一步，立刻就回到寒带去了。",
    "不过，玛丽和比埃尔更要习惯忍受室外的严寒。他们炼制沥青铀矿的设备极其简陋，由于没有把有害气体排出去的~L~通风罩~R~，炼制的大部分工作就必须在院子的露天地里进行。每逢骤雨猝至，这两位物理学家就匆忙把设备搬进棚屋，大开着门窗让空气流通，以便继续工作，而不至于因烟窒息。",
    "这种极特殊的治疗结核症的方法，玛丽多半没有对佛提埃大夫吹嘘过！后来她写过这样一段话：~L~我们没有钱，没有实验室，而且几乎没有人帮助我们把这件既重要而又困难的工作做好。这像是要由无中创出有来。假如我过学生生活的几年是卡西密尔·德卢斯基从前说的~L~我的姨妹一生中的英勇岁月~R~，我可以毫不夸大地说，现在这个时期是我丈夫和我的共同生活中的英勇时期。~R~",
    "~L~……然而我们生活中最美好而且最快乐的几年，还是在这个简陋的旧棚屋中度过的，我们把精力完全用在工作上。我有时候就在屋里踱来踱去，嘴里不停地谈着我正在做的实验，用相当微弱的声音——因为我怕我的思想被打断。有时候我丈夫和我，在我们的小屋里，一面等仪器冷却，一面坐在那里，我们就谈着现在和将来的工作……当我们把这些困难克服了的时候，我们是多么快乐啊！~R~",
    "比埃尔·居里在某一天晚上说：~L~我真想知道它是什么颜色，它是什么样子。~R~在黑暗中，在寂静中，两个人的脸都转向这些微光，转向这射线的神秘来源，转向镭，转向他们的镭！玛丽的身体前倾，热切地望着，她此时的姿势，就像一小时前在她睡着了的孩子床头看着孩子一样。",
    "她的伴侣用手轻轻地抚摩她的头发。",
    "她永远记得看荧光的这一晚，永远记得这种神妙世界的奇观。",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "简陋棚屋 · 艰苦实验", "第 1–3 段",
     "写居里夫妇在娄蒙路棚屋中进行科学实验的艰苦条件：夏天燥热如温室，冬天严寒如寒带，没有通风罩，大部分工作在露天进行。"),
    ("第二部分", "英勇岁月 · 快乐时光", "第 4–5 段",
     "引用玛丽·居里的话，写她把这段艰苦时期称为~L~英勇时期~R~，同时也是~L~最美好而且最快乐的几年~R~，表现科学家对科学的热爱与献身精神。"),
    ("第三部分", "发现镭光 · 美丽颜色", "第 6–8 段",
     "写居里夫妇在夜晚看到镭发出的美丽荧光的动人场景，玛丽望着镭的目光如同望着自己的孩子，表现科学家对科学发现的深情与喜悦。"),
]

# 每段注释词表
ANNO = [
    # P1
    [("玛丽·斯可罗多夫斯卡", "玛丽·居里婚前的名字，波兰人"), ("顶楼", "房屋的最高层，这里指玛丽在巴黎求学时住的简陋阁楼"), ("残破", "残缺破损"), ("小屋", "这里指娄蒙路的棚屋实验室"), ("尝到", "体验到、感受到"), ("奇异", "奇特、不同寻常"), ("艰苦", "艰难困苦"), ("微妙", "深奥玄妙，难以捉摸"), ("无疑地", "毫无疑问地"), ("体验过", "亲身经历过"), ("简陋", "（房屋、设备等）简单粗陋、不完备"), ("布景", "舞台或摄影场所布置的景物，这里指生活和工作的环境")],
    # P2
    [("娄蒙路", "巴黎的一条路名，居里夫妇的实验室所在地"), ("棚屋", "用竹木等搭成的简陋小屋"), ("典型", "具有代表性的人物或事件"), ("棚顶", "棚屋的顶部"), ("燥热", "（天气）干燥炎热"), ("温室", "培育植物的温暖房间，这里形容棚屋夏天极热"), ("下霜", "降霜，气温降到零度以下"), ("令人厌烦", "让人感到讨厌、不耐烦"), ("轻柔", "轻而柔和"), ("物理学家", "研究物理学的科学家"), ("标上记号", "做上标记"), ("仪器", "科学技术上用于实验、计量等的装置"), ("冻僵", "因寒冷而肢体僵硬，不能活动"), ("补救", "采取行动矫正差错、扭转不利形势"), ("炉子", "取暖、做饭或冶炼用的设备"), ("炽热", "（chì）极热"), ("失望", "感到没有希望，失去信心"), ("碰着", "接触到"), ("暖气", "暖和的气体"), ("寒带", "南极圈、北极圈以内的气候带，气候寒冷，这里形容棚屋冬天极冷")],
    # P3
    [("比埃尔", "比埃尔·居里（1859—1906），法国物理学家，玛丽·居里的丈夫"), ("忍受", "把痛苦、困难等勉强承受下来"), ("室外", "房屋外面"), ("严寒", "（气候）极冷"), ("炼制", "用加热等方法提炼"), ("沥青铀矿", "一种含铀的矿石，是提炼镭的原料"), ("极其", "非常、极端"), ("有害气体", "对人体健康有害的气体"), ("排出去", "排放到外面"), ("通风罩", "排出有害气体的装置"), ("露天", "房屋外面，上面没有遮盖"), ("每逢", "每次遇到"), ("骤雨猝至", "（cù）暴雨突然到来"), ("匆忙", "急急忙忙"), ("搬进", "搬入"), ("空气流通", "空气流动、交换"), ("不至于", "不会达到某种程度"), ("窒息", "因外界氧气不足或呼吸系统发生障碍而呼吸困难甚至停止呼吸")],
    # P4
    [("极特殊", "非常特别"), ("治疗", "用药物、手术等消除疾病"), ("结核症", "结核病，由结核杆菌引起的慢性传染病"), ("多半", "大概、很可能"), ("佛提埃大夫", "给玛丽·居里看病的医生"), ("吹嘘", "夸大地或无中生有地说自己或别人的优点"), ("实验室", "进行科学实验的房间或场所"), ("几乎", "差不多、接近"), ("无中创出有来", "从没有的东西中创造出有的东西，形容极其困难"), ("假如", "如果"), ("卡西密尔·德卢斯基", "玛丽·居里的姐夫"), ("姨妹", "妻子的妹妹"), ("英勇岁月", "勇敢出众的年月，指艰苦奋斗的时期"), ("毫不夸大", "一点也不夸大，实事求是"), ("共同生活", "一起生活"), ("英勇时期", "勇敢奋斗的时期")],
    # P5
    [("然而", "但是，表转折"), ("美好", "好（多用于生活、前途、愿望等抽象事物）"), ("精力", "精神和体力"), ("完全", "全部、全然"), ("踱来踱去", "慢步行走，来回走动"), ("不停地", "持续不断地"), ("谈着", "谈论着"), ("实验", "为了检验某种科学理论或假设而进行的操作"), ("相当", "表示程度高，但不到~L~很~R~的程度"), ("微弱", "小而弱"), ("思想", "念头、想法"), ("打断", "使中断"), ("仪器冷却", "实验仪器温度降低"), ("克服", "用坚强的意志和力量战胜（缺点、错误、坏现象、不利条件等）"), ("多么", "用在感叹句里，表示程度很高")],
    # P6
    [("某一天", "有一天（不确定的一天）"), ("真想", "非常想"), ("颜色", "由物体发射、反射或透过的光波通过视觉所产生的印象，这里指镭的荧光颜色"), ("样子", "形状、模样"), ("黑暗", "没有光"), ("寂静", "没有声音，很静"), ("微光", "微弱的光"), ("射线", "波长较短的电磁波，包括X射线、γ射线等，这里指镭发出的射线"), ("神秘", "使人摸不透的、高深莫测的"), ("来源", "事物所从来的地方"), ("镭", "（léi）一种放射性金属元素，由居里夫妇发现"), ("身体前倾", "身体向前倾斜"), ("热切", "热烈恳切"), ("姿势", "身体呈现的样子"), ("床头", "床的一端"), ("看着", "注视着")],
    # P7
    [("伴侣", "夫妻或夫妻中的一方，这里指比埃尔·居里"), ("轻轻地", "用很少力量地、温和地"), ("抚摩", "用手轻轻按着并来回移动"), ("头发", "人的前额以上、两耳以上和后颈部以上生长的毛")],
    # P8
    [("永远", "表示时间长久，没有终止"), ("记得", "想得起来、没有忘掉"), ("荧光", "某些物质受光线或其他射线照射时发出的光，这里指镭发出的光"), ("神妙", "神奇巧妙"), ("世界", "这里指镭的放射性现象所展现的未知领域"), ("奇观", "雄伟美丽而又罕见的景象或出奇少见的事情")],
]

# 每段: (内容概括, 手法分析)
CONTENT_TECH = [
    ("开篇点题：玛丽·居里学生时代最愉快的时期在顶楼度过，现在又要在残破的小屋里尝到新的极大的快乐。这种艰苦而微妙的快乐，两次都挑选了最简陋的布景。",
     "开篇将~L~顶楼~R~与~L~残破的小屋~R~并置，暗示玛丽一生与简陋环境的不解之缘；~L~艰苦而且微妙的快乐~R~是全文的文眼，~L~两次都挑选了最简陋的布景~R~拟人手法，赋予快乐以主动性，为全文奠定基调。"),
    ("写娄蒙路棚屋的恶劣条件：夏天燥热如温室，冬天不知该希望下霜还是下雨——下雨则漏水，下霜则冻僵；炉子烧到炽热也无济于事，离开一步就回到寒带。",
     "~L~不知道是应该希望下霜还是应该希望下雨~R~用两难选择写冬天的难熬；~L~落在地上，落在工作台上，落在……~R~排比写雨水的无孔不入；~L~离开一步，立刻就回到寒带去了~R~夸张写炉子的无用，环境描写生动传神。"),
    ("写居里夫妇在室外严寒中工作：没有通风罩，炼制沥青铀矿的大部分工作必须在露天进行；骤雨猝至时匆忙搬设备，大开门窗通风，以免因烟窒息。",
     "~L~通风罩~R~加引号，强调这一基本设备的缺失；~L~骤雨猝至~R~~L~匆忙~R~~L~大开着门窗~R~等动作描写，见科学家在恶劣条件下的坚持；环境的艰苦与工作的执着形成对比。"),
    ("玛丽戏称这种在严寒中工作是~L~极特殊的治疗结核症的方法~R~，并引用她的话：没有钱、没有实验室、几乎无人帮助，~L~像是要由无中创出有来~R~，称这段时期为~L~英勇时期~R~。",
     "~L~极特殊的治疗结核症的方法~R~幽默中见辛酸；直接引用玛丽的话，真实可信；~L~由无中创出有来~R~比喻科学创业的艰难；~L~英勇岁月~R~~L~英勇时期~R~反复出现，突出科学家的献身精神。"),
    ("继续引用玛丽的话：最美好最快乐的几年在简陋棚屋中度过，她在屋里踱来踱去谈实验，与丈夫等仪器冷却时谈工作，克服困难时无比快乐。",
     "~L~踱来踱去~R~~L~用相当微弱的声音~R~细节描写，见玛丽对实验的痴迷；~L~一面等仪器冷却，一面坐在那里~R~温馨画面，见夫妻情深与志同道合；引用增强了文章的真实性和感染力。"),
    ("写发现镭的那个夜晚：比埃尔说想知道镭是什么颜色，两人在黑暗中转向微光，转向镭，转向他们的镭；玛丽身体前倾，热切地望着，姿势如同望着睡着的孩子。",
     "~L~转向这些微光，转向这射线的神秘来源，转向镭，转向他们的镭~R~排比，层层递进，情感逐步加深；~L~就像一小时前在她睡着了的孩子床头看着孩子一样~R~比喻，将科学家对镭的深情比作母爱，感人至深。"),
    ("比埃尔用手轻轻地抚摩玛丽的头发。",
     "独句成段，以极简的动作描写收束发现镭的场景；~L~轻轻地抚摩~R~充满温情与爱意，是对妻子辛劳的抚慰，也是对共同成就的欣慰；无声胜有声，余味悠长。"),
    ("玛丽永远记得看荧光的这一晚，永远记得这种神妙世界的奇观。",
     "~L~永远记得~R~反复出现，强调这一晚的难忘；~L~神妙世界的奇观~R~点明题旨——镭的荧光是美丽的，科学家的精神世界更是美丽的；以抒情笔调收束全文，余韵无穷。"),
]

# Build S data
S = []
part_map = [0, 0, 0, 1, 1, 2, 2, 2]
for i in range(8):
    annotated = annotate_text(FULLTEXT[i], ANNO[i])
    S.append((part_map[i], annotated, CONTENT_TECH[i][0], CONTENT_TECH[i][1]))


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"炽","py":"chì","q":"那个炉子即使把它烧到□热的程度，也令人完全失望","tip":"「炽」火字旁，音 chì，热烈旺盛，勿写「织」（绞丝旁）"},
    {"w":"猝","py":"cù","q":"每逢骤雨□至，这两位物理学家就匆忙把设备搬进棚屋","tip":"「猝」反犬旁，音 cù，突然，勿写「卒」（十字底）"},
    {"w":"窒","py":"zhì","q":"而不至于因烟□息","tip":"「窒」穴宝盖，音 zhì，阻塞不通，勿写「至」"},
    {"w":"嘘","py":"xū","q":"玛丽多半没有对佛提埃大夫吹□过","tip":"「嘘」口字旁，音 xū，慢慢地吐气，「吹嘘」指夸大地说，勿写「虚」（虎字头）"},
    {"w":"踱来踱去","py":"duó lái duó qù","q":"我有时候就在屋里□□□□，嘴里不停地谈着我正在做的实验","tip":"「踱」足字旁，音 duó，慢步行走，勿写「度」（广字头）"},
    {"w":"镭镭","py":"léi léi","q":"转向这射线的神秘来源，转向□，转向他们的□","tip":"「镭」金字旁，音 léi，放射性金属元素，勿写「雷」（雨字头）"},
    {"w":"荧","py":"yíng","q":"她永远记得看□光的这一晚","tip":"「荧」草字头，音 yíng，微弱的光亮，「荧光」，勿写「莹」（玉字旁）"},
    {"w":"摩","py":"mó","q":"她的伴侣用手轻轻地抚□她的头发","tip":"「摩」手字底，音 mó，接触并轻轻移动，「抚摩」，勿写「磨」（石字旁）"},
    {"w":"陋","py":"lòu","q":"两次都挑选了最简□的布景","tip":"「陋」左耳旁，音 lòu，不好看、粗劣，「简陋」，勿写「漏」（三点水）"},
    {"w":"燥","py":"zào","q":"棚屋里面□热得像温室","tip":"「燥」火字旁，音 zào，干燥，「燥热」，勿写「躁」（足字旁，急躁）"},
    {"w":"僵","py":"jiāng","q":"若是下霜，就连人都冻□了，没有方法补救","tip":"「僵」单人旁，音 jiāng，僵硬，「冻僵」，勿写「疆」（弓字旁）"},
    {"w":"沥","py":"lì","q":"他们炼制□青铀矿的设备极其简陋","tip":"「沥」三点水，音 lì，液体的点滴，「沥青」，勿写「历」（厂字头）"},
]

DICT_NOTES = [
    {"w":"炽热","a":"（chì）极热","q":"那个炉子即使把它烧到炽热的程度"},
    {"w":"简陋","a":"（房屋、设备等）简单粗陋、不完备","q":"两次都挑选了最简陋的布景"},
    {"w":"燥热","a":"（天气）干燥炎热","q":"棚屋里面燥热得像温室"},
    {"w":"冻僵","a":"因寒冷而肢体僵硬，不能活动","q":"若是下霜，就连人都冻僵了"},
    {"w":"炼制","a":"用加热等方法提炼","q":"他们炼制沥青铀矿的设备极其简陋"},
    {"w":"沥青铀矿","a":"一种含铀的矿石，是提炼镭的原料","q":"他们炼制沥青铀矿的设备极其简陋"},
    {"w":"骤雨猝至","a":"（cù）暴雨突然到来","q":"每逢骤雨猝至"},
    {"w":"窒息","a":"因外界氧气不足或呼吸系统发生障碍而呼吸困难甚至停止呼吸","q":"而不至于因烟窒息"},
    {"w":"吹嘘","a":"夸大地或无中生有地说自己或别人的优点","q":"玛丽多半没有对佛提埃大夫吹嘘过"},
    {"w":"无中创出有来","a":"从没有的东西中创造出有的东西，形容极其困难","q":"这像是要由无中创出有来"},
    {"w":"英勇岁月","a":"勇敢出众的年月，指艰苦奋斗的时期","q":"我的姨妹一生中的英勇岁月"},
    {"w":"踱来踱去","a":"慢步行走，来回走动","q":"我有时候就在屋里踱来踱去"},
    {"w":"微弱","a":"小而弱","q":"用相当微弱的声音"},
    {"w":"射线","a":"波长较短的电磁波，这里指镭发出的射线","q":"转向这射线的神秘来源"},
    {"w":"镭","a":"（léi）一种放射性金属元素，由居里夫妇发现","q":"转向镭，转向他们的镭"},
    {"w":"热切","a":"热烈恳切","q":"玛丽的身体前倾，热切地望着"},
    {"w":"伴侣","a":"夫妻或夫妻中的一方，这里指比埃尔·居里","q":"她的伴侣用手轻轻地抚摩她的头发"},
    {"w":"抚摩","a":"用手轻轻按着并来回移动","q":"她的伴侣用手轻轻地抚摩她的头发"},
    {"w":"荧光","a":"某些物质受光线或其他射线照射时发出的光，这里指镭发出的光","q":"她永远记得看荧光的这一晚"},
    {"w":"神妙","a":"神奇巧妙","q":"永远记得这种神妙世界的奇观"},
    {"w":"奇观","a":"雄伟美丽而又罕见的景象或出奇少见的事情","q":"永远记得这种神妙世界的奇观"},
    {"w":"微妙","a":"深奥玄妙，难以捉摸","q":"这种艰苦而且微妙的快乐"},
    {"w":"布景","a":"舞台或摄影场所布置的景物，这里指生活和工作的环境","q":"两次都挑选了最简陋的布景"},
    {"w":"寒带","a":"南极圈、北极圈以内的气候带，气候寒冷，这里形容棚屋冬天极冷","q":"立刻就回到寒带去了"},
    {"w":"通风罩","a":"排出有害气体的装置","q":"由于没有把有害气体排出去的~L~通风罩~R~"},
    {"w":"结核症","a":"结核病，由结核杆菌引起的慢性传染病","q":"这种极特殊的治疗结核症的方法"},
    {"w":"实验室","a":"进行科学实验的房间或场所","q":"我们没有钱，没有实验室"},
    {"w":"克服","a":"用坚强的意志和力量战胜（缺点、错误、坏现象、不利条件等）","q":"当我们把这些困难克服了的时候"},
    {"w":"前倾","a":"身体向前倾斜","q":"玛丽的身体前倾，热切地望着"},
    {"w":"寂静","a":"没有声音，很静","q":"在黑暗中，在寂静中"},
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
    <p>《美丽的颜色》是法国作家艾芙·居里为母亲玛丽·居里所写传记《居里夫人传》中的节选。文章以饱含深情的笔触，记述了居里夫妇在巴黎娄蒙路简陋棚屋中发现镭的过程，展现了科学家在极端艰苦条件下对科学的执着热爱与献身精神。</p>
    <p>题目~L~美丽的颜色~R~一语双关：既指镭发出的美丽荧光，也指科学家美丽的精神世界。全文以~L~艰苦而且微妙的快乐~R~为线索，将环境的恶劣与精神的愉悦对照，感人至深。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>艾芙·居里（1904—2007），法国作家，玛丽·居里和比埃尔·居里的小女儿。她自幼受到良好的家庭教育，后来成为一名优秀的钢琴家和作家。她为母亲撰写的传记《居里夫人传》（1937年出版），以生动细腻的笔触展现了玛丽·居里伟大的一生，在全世界产生了广泛影响。</p>
    <p>艾芙·居里在写作中查阅了大量书信和文献，并采访了许多了解居里夫人的人，使传记既真实可信又富有文学色彩。本文即选自这部传记。</p>
  </div>
  <div class="box">
    <h3>居里夫妇与镭的发现</h3>
    <p><b>玛丽·居里</b>（1867—1934），原名玛丽·斯可罗多夫斯卡，波兰裔法国物理学家、化学家。1891年赴巴黎大学求学，1895年与法国物理学家比埃尔·居里结婚。</p>
    <p><b>发现镭：</b>1898年，居里夫妇从沥青铀矿中发现了两种新的放射性元素——钋（pō）和镭（léi）。为了提炼出纯净的镭，他们在娄蒙路的一个废弃棚屋里工作了四年（1899—1902），从数吨沥青铀矿渣中提炼出0.1克氯化镭。1903年，居里夫妇与贝克勒尔共同获得诺贝尔物理学奖。1911年，玛丽·居里因发现钋和镭获得诺贝尔化学奖，成为第一位两次获得诺贝尔奖的科学家。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>传记写作：</b>艾芙·居里在母亲去世后，为了让世人了解这位伟大女性的真实面貌，花费数年时间搜集资料，撰写了《居里夫人传》。她没有将母亲写成不食人间烟火的圣人，而是写出了她作为妻子、母亲和科学家的真实生活。</p>
    <p><b>以小见大：</b>本文选取居里夫妇发现镭过程中的几个生活片段——棚屋的艰苦、玛丽的回忆、看荧光的夜晚——以小见大，展现科学家的精神世界。文章大量引用玛丽·居里的原话，增强了真实性和感染力。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文朗读《美丽的颜色》艾芙·居里</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1N5iLeKE52&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读《美丽的颜色》"></iframe>
        <a href="https://www.bilibili.com/video/BV1N5iLeKE52" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>课文讲解《美丽的颜色》艾芙·居里</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1zK411w7af&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文讲解《美丽的颜色》"></iframe>
        <a href="https://www.bilibili.com/video/BV1zK411w7af" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">玛丽·居里——在艰苦中追求科学之美的伟大科学家</div>
        <p><b>吃苦耐劳，坚韧不拔：</b>在娄蒙路棚屋中，夏天燥热如温室，冬天严寒如寒带，没有通风罩，大部分工作在露天进行。但玛丽和比埃尔忍受了这一切，从数吨矿渣中提炼出0.1克镭，展现了惊人的毅力。</p>
        <p><b>热爱科学，以苦为乐：</b>玛丽称这段艰苦时期为~L~英勇时期~R~，也是~L~最美好而且最快乐的几年~R~。她在屋里踱来踱去谈实验，用微弱的声音生怕打断思路，对科学的热爱使她忘记了环境的艰苦。</p>
        <p><b>深情温柔，内心丰富：</b>发现镭的夜晚，玛丽~L~身体前倾，热切地望着~R~镭的微光，姿势~L~就像一小时前在她睡着了的孩子床头看着孩子一样~R~——她对科学发现的深情，如同母爱一般真挚。</p>
        <p><b>谦逊朴实，不慕虚荣：</b>玛丽说~L~我们没有钱，没有实验室，而且几乎没有人帮助我们~R~，她从不夸耀自己的成就，而是以~L~由无中创出有来~R~的实干精神，默默奉献于科学事业。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">以小见大，细节传神</div>
        <p>文章没有铺陈居里夫妇的全部科学成就，而是选取棚屋生活、玛丽的回忆、看荧光的夜晚等几个小片段，以小见大，展现科学家的精神世界。~L~踱来踱去~R~~L~用相当微弱的声音~R~~L~身体前倾，热切地望着~R~等细节描写，生动传神，如在目前。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">引用原话，真实感人</div>
        <p>文章大量引用玛丽·居里的原话：~L~这像是要由无中创出有来~R~~L~现在这个时期是我丈夫和我的共同生活中的英勇时期~R~~L~我们生活中最美好而且最快乐的几年~R~。直接引用增强了文章的真实性和感染力，使读者仿佛亲耳聆听科学家的心声。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比鲜明，苦乐交织</div>
        <p>环境的艰苦（燥热、严寒、漏雨、没有通风罩）与精神的快乐（~L~极大的快乐~R~~L~最美好而且最快乐~R~）形成鲜明对比；~L~最简陋的布景~R~与~L~神妙世界的奇观~R~形成对比。在苦与乐的交织中，科学家的形象更加高大。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">语言质朴，深情蕴藉</div>
        <p>文章语言质朴无华，没有华丽的辞藻，但字里行间饱含深情。~L~她的伴侣用手轻轻地抚摩她的头发~R~独句成段，以极简的动作写尽夫妻情深；~L~她永远记得看荧光的这一晚~R~反复咏叹，余味悠长。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《美丽的颜色》通过记述居里夫妇在简陋棚屋中发现镭的过程，赞美了科学家在极端艰苦条件下对科学的执着热爱与献身精神，展现了他们美丽的精神世界。</p>
    <p>题目~L~美丽的颜色~R~一语双关：既指镭在黑暗中发出的美丽荧光，也指居里夫妇不畏艰苦、献身科学的美丽心灵。文章告诉我们：真正的快乐不在于物质的享受，而在于对理想的追求和对事业的奉献；科学的美丽，不仅在于它揭示了自然的奥秘，更在于追求它的人所展现的精神光辉。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">重点词语 · 用字与读音 · 修辞 · 写作借鉴</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">炽热</span><span class="acc-d">（chì）极热。</span></div>
      <div class="acc-item"><span class="acc-w">简陋</span><span class="acc-d">（房屋、设备等）简单粗陋、不完备。</span></div>
      <div class="acc-item"><span class="acc-w">燥热</span><span class="acc-d">（天气）干燥炎热。</span></div>
      <div class="acc-item"><span class="acc-w">冻僵</span><span class="acc-d">因寒冷而肢体僵硬，不能活动。</span></div>
      <div class="acc-item"><span class="acc-w">炼制</span><span class="acc-d">用加热等方法提炼。</span></div>
      <div class="acc-item"><span class="acc-w">沥青铀矿</span><span class="acc-d">一种含铀的矿石，是提炼镭的原料。</span></div>
      <div class="acc-item"><span class="acc-w">骤雨猝至</span><span class="acc-d">（cù）暴雨突然到来。</span></div>
      <div class="acc-item"><span class="acc-w">窒息</span><span class="acc-d">因外界氧气不足或呼吸系统发生障碍而呼吸困难甚至停止呼吸。</span></div>
      <div class="acc-item"><span class="acc-w">吹嘘</span><span class="acc-d">夸大地或无中生有地说自己或别人的优点。</span></div>
      <div class="acc-item"><span class="acc-w">踱来踱去</span><span class="acc-d">（duó）慢步行走，来回走动。</span></div>
      <div class="acc-item"><span class="acc-w">微弱</span><span class="acc-d">小而弱。</span></div>
      <div class="acc-item"><span class="acc-w">射线</span><span class="acc-d">波长较短的电磁波，这里指镭发出的射线。</span></div>
      <div class="acc-item"><span class="acc-w">镭</span><span class="acc-d">（léi）一种放射性金属元素，由居里夫妇发现。</span></div>
      <div class="acc-item"><span class="acc-w">热切</span><span class="acc-d">热烈恳切。</span></div>
      <div class="acc-item"><span class="acc-w">抚摩</span><span class="acc-d">（mó）用手轻轻按着并来回移动。</span></div>
      <div class="acc-item"><span class="acc-w">荧光</span><span class="acc-d">（yíng）某些物质受光线或其他射线照射时发出的光。</span></div>
      <div class="acc-item"><span class="acc-w">神妙</span><span class="acc-d">神奇巧妙。</span></div>
      <div class="acc-item"><span class="acc-w">奇观</span><span class="acc-d">雄伟美丽而又罕见的景象或出奇少见的事情。</span></div>
      <div class="acc-item"><span class="acc-w">微妙</span><span class="acc-d">深奥玄妙，难以捉摸。</span></div>
      <div class="acc-item"><span class="acc-w">布景</span><span class="acc-d">舞台或摄影场所布置的景物，这里指生活和工作的环境。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">炽</span><span class="acc-d">（chì）火字旁，热烈旺盛。不读 zhì，不写~L~织~R~。</span></div>
      <div class="acc-item"><span class="acc-w">猝</span><span class="acc-d">（cù）反犬旁，突然。不读 zú，不写~L~卒~R~。</span></div>
      <div class="acc-item"><span class="acc-w">窒</span><span class="acc-d">（zhì）穴宝盖，阻塞不通。不写~L~至~R~。</span></div>
      <div class="acc-item"><span class="acc-w">踱</span><span class="acc-d">（duó）足字旁，慢步行走。不读 dù，不写~L~度~R~。</span></div>
      <div class="acc-item"><span class="acc-w">镭</span><span class="acc-d">（léi）金字旁，放射性金属元素。不写~L~雷~R~（雨字头）。</span></div>
      <div class="acc-item"><span class="acc-w">荧</span><span class="acc-d">（yíng）草字头，微弱的光亮。与~L~莹~R~（玉字旁，光洁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">摩</span><span class="acc-d">（mó）手字底，接触并轻轻移动。与~L~磨~R~（石字旁，摩擦）区分。</span></div>
      <div class="acc-item"><span class="acc-w">燥</span><span class="acc-d">（zào）火字旁，干燥。与~L~躁~R~（足字旁，急躁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">僵</span><span class="acc-d">（jiāng）单人旁，僵硬。与~L~疆~R~（弓字旁，边疆）区分。</span></div>
      <div class="acc-item"><span class="acc-w">陋</span><span class="acc-d">（lòu）左耳旁，粗劣。与~L~漏~R~（三点水，漏雨）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞方法</h3>
      <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">~L~棚屋里面燥热得像温室~R~~L~就像一小时前在她睡着了的孩子床头看着孩子一样~R~，比喻生动贴切。</span></div>
      <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">~L~落在地上，落在工作台上，落在……~R~排比写雨水的无孔不入；~L~转向这些微光，转向这射线的神秘来源，转向镭，转向他们的镭~R~排比层层递进。</span></div>
      <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">~L~离开一步，立刻就回到寒带去了~R~夸张写炉子的无用；~L~由无中创出有来~R~夸张写创业的艰难。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">环境的艰苦与精神的快乐对比；~L~最简陋的布景~R~与~L~神妙世界的奇观~R~对比。</span></div>
      <div class="acc-item"><span class="acc-w">反复</span><span class="acc-d">~L~永远记得~R~反复出现，强调这一晚的难忘；~L~英勇~R~反复出现，突出科学家的献身精神。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">以小见大</span><span class="acc-d">通过几个生活片段展现人物的精神世界，避免平铺直叙的流水账。写人作文可借鉴这种选材方法。</span></div>
      <div class="acc-item"><span class="acc-w">细节描写</span><span class="acc-d">~L~踱来踱去~R~~L~身体前倾，热切地望着~R~~L~轻轻地抚摩~R~等细节，使人物形象生动可感。</span></div>
      <div class="acc-item"><span class="acc-w">引用原话</span><span class="acc-d">直接引用人物的话，增强真实性和感染力。写人物传记或回忆性文章时可适当引用。</span></div>
      <div class="acc-item"><span class="acc-w">环境烘托</span><span class="acc-d">以恶劣的环境烘托人物的坚韧与伟大，~L~苦~R~越写越足，~L~乐~R~越显珍贵。</span></div>
      <div class="acc-item"><span class="acc-w">独句成段</span><span class="acc-d">~L~她的伴侣用手轻轻地抚摩她的头发。~R~独句成段，以极简的动作写尽深情，有余味。</span></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《美丽的颜色》艾芙·居里</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">法国 · 艾芙·居里</div>
  <h1 class="hero-title">美丽的颜色</h1>
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
  <div class="sec-sub">全文八段，分三部分：简陋棚屋与艰苦实验、英勇岁月与快乐时光、发现镭光与美丽颜色。每段含内容概括与手法分析，点击可展开。</div>
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
  <div class="kai">《美丽的颜色》</div>
  <div>艾芙·居里 · 法国 · 选自《居里夫人传》 · 传记文学</div>
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
