# -*- coding: utf-8 -*-
"""生成《庆祝奥林匹克运动复兴25周年》顾拜旦 课件（庄重演讲词）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\qingzhuaolinpikeyundongfuxing25zhounian-gubaidan.html"
FS_KEY = "aolinpike25_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
style += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:14px 0 6px;color:var(--ink);font-size:calc(16px * var(--fs));}'
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

LQ = "\u201c"
RQ = "\u201d"

paragraphs = [
    (
        "联邦主席、女士们、先生们：",
        "演讲的称呼语，庄重得体，符合国际会议演讲的礼仪。",
        "演讲手法：标准的西式演讲称呼，依次称呼联邦主席、女士们、先生们，体现对与会者的尊重，庄重正式，为全文奠定典雅庄重的基调。",
        [
            ("联邦主席", "指瑞士联邦主席，瑞士是委员会制国家，联邦主席为国家元首"),
        ],
    ),
    (
        "5年前，在巴黎，在1894年我宣布恢复奥林匹克运动会的地方，世界各国的代表们共聚一堂，同我们一起庆祝奥林匹克运动复兴二十周年。五年过去了，在这期间，整个世界分崩离析。所幸，奥林匹克主义并没有成为这场浩劫的牺牲品，而是无所畏惧、无可指摘地挺了过来。而今，它的眼前突然呈现出更为开阔的视野，这凸显了它即将扮演的崭新角色的意义。",
        "回顾五年前在巴黎庆祝复兴20周年的情景，指出五年来世界分崩离析（一战），但奥林匹克主义挺了过来，如今将扮演崭新角色。",
        "演讲手法：对比（五年前的庆祝 vs 五年的浩劫），突出奥林匹克主义的坚韧。拟人（奥林匹克主义挺了过来、眼前呈现视野），赋予奥林匹克主义以生命。成语（分崩离析、无所畏惧、无可指摘）典雅庄重，体现演讲的正式风格。",
        [
            ("共聚一堂", "聚集在同一个厅堂，指许多人聚集在一起"),
            ("分崩离析", "崩塌解体，四分五裂，形容国家或集团分裂瓦解"),
            ("浩劫", "大灾难"),
            ("牺牲品", "成为牺牲的物品，指被损害的对象"),
            ("无所畏惧", "什么也不怕，形容非常勇敢"),
            ("无可指摘", "没有什么可以指责的，形容完美"),
            ("凸显", "清楚地显露"),
        ],
    ),
    (
        "奥林匹克精神开始为渐趋平和而又充满自信的青少年所推崇。古文明的魅力，时有衰退，平和与自信正日益成为其有力的支撑。同时，它们也是那些即将在暴风骤雨中诞生的新生文明必不可少的支柱。然而，人类并非生而就平和自信。还在襁褓中的婴儿，就已开始担惊受怕。恐惧伴随着他成长的各个阶段，并在他行将就木时，给他致命一击使其崩溃。恐惧是人类工作和休息的天敌，面对它，人类学会用勇气来针锋相对。有些人认为，勇气这一高贵美德只有在我们的祖先身上才能看到，他们因此非常尊重先人。在他们的想象中，勇气之花在我们当代人的手中早已残败凋零了。但是如今，我们知道该在将来采取何种态度了。",
        "指出奥林匹克精神为平和自信的青少年所推崇，平和与自信是新生文明的支柱；分析人类天生恐惧，需要勇气来对抗，但勇气之花并未凋零。",
        "演讲手法：比喻（襁褓中的婴儿、行将就木、勇气之花），形象生动。拟人（恐惧伴随、给致命一击），将抽象的恐惧人格化。对比（古文明衰退 vs 平和自信日益成为支撑）。长句与短句结合，节奏富于变化，体现诗歌般的语言风格。",
        [
            ("推崇", "十分推重、崇敬"),
            ("衰退", "（身体、精神、意志、能力等）趋向衰弱"),
            ("暴风骤雨", "又猛又急的大风雨，比喻声势浩大、发展急速而猛烈"),
            ("襁褓", "（qiǎng bǎo）包裹婴儿的被子和带子"),
            ("担惊受怕", "担心害怕"),
            ("行将就木", "快要进棺材了，指人临近死亡。木，棺材"),
            ("致命一击", "导致死亡的打击"),
            ("崩溃", "完全破坏、垮掉"),
            ("天敌", "自然界中某种动物专门捕食或危害另一种动物，前者是后者的天敌"),
            ("针锋相对", "针尖对针尖，比喻双方策略、论点等尖锐地对立"),
            ("美德", "美好的品德"),
            ("残败凋零", "残缺衰败，草木零落，比喻事物衰败"),
        ],
    ),
    (
        "勇气是战争中的美德，它能够在时世中造就英雄。正如我最近在一篇关于教育学的文章中所暗示的那样，根除恐惧真正的、能持久发挥效用的良药，更多的是自信而非勇气。自信与它的姊妹平和总是携手并进、相辅相成。这样，我们又回到了适才我提到的奥林匹克主义的实质上来，这也正是奥林匹克主义区别于一般体育运动的地方，奥林匹克主义包括但又远远超越了一般的体育运动。",
        "指出勇气是战争中的美德，但根除恐惧的良药更多是自信而非勇气；自信与平和相辅相成，这正是奥林匹克主义区别于并超越一般体育运动的实质。",
        "演讲手法：比喻（良药、姊妹），将抽象概念具象化。对比（自信 vs 勇气），突出自信的重要。递进（包括但又远远超越），强调奥林匹克主义的丰富内涵。承上启下，从对恐惧和勇气的论述转入奥林匹克主义的实质。",
        [
            ("时世", "时代、世道"),
            ("造就", "培养使有成就"),
            ("根除", "彻底铲除"),
            ("持久", "保持长久"),
            ("效用", "效力和作用"),
            ("携手并进", "手拉着手一起前进，比喻共同努力"),
            ("相辅相成", "互相补充，互相配合"),
            ("适才", "刚才"),
            ("实质", "本质"),
        ],
    ),
    (
        "请允许我详细阐述一下二者的区别。运动员非常享受努力拼搏的乐趣。他喜欢施加于肌肉和神经上的那种压力感，因为压力往往给人一种胜利在望的感觉，即便有时到最后他未能获胜。这种享受，深入运动员的内心，某种程度上甚至可以说只涉及到自身。请想象一下，当这种愉悦向外喷涌，并与对大自然的热爱之情和对艺术的奔放激情融为一体；当它为灿烂阳光所萦绕，为音乐所振奋，或被嵌入圆柱式大厅时，会是怎样的情景。许久以前，就是在这般情景下，古代奥林匹克主义的绚丽梦想在阿尔弗斯河的两岸诞生了。奥林匹克主义曾在许多个世纪里，一直主导着古希腊社会。",
        "详细阐述奥林匹克主义与一般体育运动的区别：一般竞技只涉及自身享受，而奥林匹克主义将这种愉悦与自然、艺术融为一体，这正是古希腊奥林匹克主义的起源。",
        "演讲手法：对比（只涉及自身 vs 与自然艺术融为一体），突出奥林匹克主义的超越性。排比（为灿烂阳光所萦绕，为音乐所振奋，或被嵌入圆柱式大厅），描绘美好的运动场景。描写与议论结合，既有生动的场景描绘，又有深刻的理性分析。",
        [
            ("阐述", "深入论述"),
            ("拼搏", "尽全力去争夺"),
            ("压力感", "承受压力的感觉"),
            ("胜利在望", "胜利即将到来"),
            ("即便", "即使"),
            ("喷涌", "迅速地往外冒"),
            ("奔放", "（思想、感情、文章气势等）尽情流露，不受拘束"),
            ("融为一体", "融合为一个整体"),
            ("萦绕", "萦回，环绕"),
            ("嵌入", "牢固地或深深地固定或树立"),
            ("绚丽", "灿烂美丽"),
            ("阿尔弗斯河", "希腊的一条河流，古代奥林匹克运动会的举办地奥林匹亚位于此河附近"),
            ("主导", "决定并引导事物向某方面发展"),
        ],
    ),
    (
        "然后，我们来到了历史的转折关头。渴求进步但又常常因夸大某种正确思想而误入歧途的人类精神，开始致力于将青少年从平衡状态中挣脱出来。于是，青少年开始为呆板而复杂的教育枷锁所套牢，被在愚蠢的放纵和不明智的严厉交互作用下的道德说教以及拙劣肤浅的世界观所束缚。这就是为何我们要重启奥林匹克时代，并为体格训练的复兴隆重庆祝的原因。我们不断推动盎格鲁一撒克逊人的运动功利思想向古希腊遗留下来的一呼百应的体育观靠拢，两者逐渐融合为一体。当我在纽约和伦敦对举办奥运会的可能性做出评估之后，我向不朽的古希腊精神祈祷，希望它给这意外中诞生的结合体一剂理想主义的良药。先生们，这25年来我们成功兴建的事业大厦，便是这副模样。诸位适才不断向其表达敬意，若这敬意是针对我这建筑师而来的话，那我着实愧不敢当。它的建筑师不应受到如此赞美，他不过是听从了一种比个人意志更为强大的内心直觉的召唤。他愿意愉快地接受诸位对奥林匹克精神的赞美之辞，而他个人，不过是这一理想的第一个仆从。",
        "指出人类精神误入歧途导致青少年被教育枷锁套牢，因此需要重启奥林匹克时代；推动英美功利体育观与古希腊体育观融合；自谦只是奥林匹克理想的第一个仆从。",
        "演讲手法：比喻（教育枷锁、事业大厦、良药、仆从），形象生动。长句定语复杂（渴求进步但又常常因夸大某种正确思想而误入歧途的人类精神），体现庄重典雅的风格。对比（盎格鲁-撒克逊功利思想 vs 古希腊体育观），说明融合的必要。自谦（愧不敢当、第一个仆从），体现顾拜旦的谦逊品格。",
        [
            ("转折关头", "事物发展过程中改变方向的关键时刻"),
            ("误入歧途", "由于受煽惑而走上了错误的道路"),
            ("致力于", "把精力投放在某个方面"),
            ("呆板", "死板、不灵活"),
            ("枷锁", "枷和锁链，比喻所受的压迫和束缚"),
            ("套牢", "被牢牢地套住"),
            ("放纵", "纵容、不守规矩"),
            ("交互", "互相、交替"),
            ("道德说教", "讲解道德规范，多含贬义"),
            ("拙劣", "笨拙而低劣"),
            ("肤浅", "（学识）浅，（理解）不深"),
            ("世界观", "人们对世界的总的根本的看法"),
            ("束缚", "使受到约束限制"),
            ("重启", "重新开始"),
            ("体格训练", "身体锻炼"),
            ("隆重", "盛大庄重"),
            ("盎格鲁-撒克逊", "英国的主要民族，这里指英美的体育传统"),
            ("功利", "功效和利益，这里指注重实用效果"),
            ("一呼百应", "一声召唤，很多人响应，形容威望高"),
            ("靠拢", "挨近、靠近"),
            ("评估", "评议估计"),
            ("不朽", "永不磨灭"),
            ("祈祷", "向神祝告求福"),
            ("结合体", "结合在一起的整体"),
            ("理想主义", "以理想为基础的思想体系"),
            ("着实", "实在、确实"),
            ("愧不敢当", "感到惭愧，承当不起"),
            ("直觉", "未经充分逻辑推理的感性认识"),
            ("召唤", "叫人来（多用于抽象方面）"),
            ("仆从", "旧时指跟随在身旁的仆人"),
        ],
    ),
    (
        "之前我曾提及1914年6月所举办的周年庆典。当时我们认为，我们庆祝的是奥林匹克主义的完美实现。然而今天，我的印象反而是我正目睹它再次含苞怒放。一项运动，倘若只有有限一部分人被包含在内，在当今时代又怎能称得上完美呢？在当时，有这么多人可能确实是足够的，但今天则不然。它必须要面向大众。的确如此，有什么名义能将大众排除在奥林匹克精神之外呢？有什么样的贵族特权能令一个青年人身上的形体美、肌肉力量、锻炼的毅力以及获胜的意志非得同他的家谱或钱包挂钩呢？上述种种毫无法律依据的矛盾，存活在萌生它们的这个社会秩序里。在野蛮的军国主义协助下的极权姿态，给了它们致命一击。从道义上讲，这反而是可以自圆其说的。",
        "回顾1914年庆典，指出当时以为完美实现，今天则看到奥林匹克主义再次含苞怒放；强调奥林匹克运动必须面向大众，不能以贵族特权将大众排除在外。",
        "演讲手法：比喻（含苞怒放），形象表达奥林匹克主义的新生。反问（怎能称得上完美、有什么名义能将大众排除），强调面向大众的必要性。排比反问（有什么名义……有什么样的贵族特权……），气势充沛。对比（当时足够 vs 今天不然），说明时代变化对奥林匹克运动的新要求。",
        [
            ("周年庆典", "成立若干周年的庆祝活动"),
            ("目睹", "亲眼看到"),
            ("含苞怒放", "花骨朵儿盛开，比喻事物蓬勃发展"),
            ("倘若", "如果、假如"),
            ("面向大众", "面对普通民众，为大多数人服务"),
            ("名义", "做某事时用来作为依据的名称或称号"),
            ("贵族特权", "贵族阶层享有的特殊权利"),
            ("形体美", "身体形态的美"),
            ("毅力", "坚强持久的意志"),
            ("家谱", "家族记载世系和事迹的书"),
            ("挂钩", "比喻建立某种联系"),
            ("萌生", "开始发生"),
            ("社会秩序", "社会的正常状态和规则"),
            ("军国主义", "把国家完全置于军事控制之下，黩武侵略的思想和政策"),
            ("极权", "掌握全部权力，独断专行"),
            ("道义", "道德和正义"),
            ("自圆其说", "使自己的论点或谎话没有漏洞"),
        ],
    ),
    (
        "面对一个需要用基本原则来整顿的全新世界，某些过去一直被视为乌托邦的原则，如今却变得切实可行。人类必须吸收古文明遗留下来的全部精华，用以构筑未来。这其中就包括奥林匹克精神。当然，仅靠奥林匹克精神，并不足以保障社会层面的和平以及更公平、公正地分配人类生产劳动，分配满足物质生活的消费必需品，甚至不足以向青少年提供与他们的能力相当而与其家庭出身无关的才智培训机会。但是，奥林匹克精神致力于让社会底层的人们接触到现代工业所塑造的各种锻炼形式，享受到强身健体的乐趣。这就是完美的、民主的奥林匹克精神，今天我们要为它奠定基础。",
        "指出在全新世界中，过去视为乌托邦的原则变得切实可行；奥林匹克精神虽不能解决所有社会问题，但致力于让社会底层人们享受强身健体的乐趣，这就是完美的民主的奥林匹克精神。",
        "演讲手法：让步转折（当然……但是……），先承认奥林匹克精神的局限，再强调其独特价值，论证严密。排比（保障和平、公平分配、提供培训机会），列举奥林匹克精神不能解决的问题，反衬其核心价值。下定义（这就是完美的、民主的奥林匹克精神），点明主旨。",
        [
            ("整顿", "使紊乱的变为整齐，使不健全的健全起来"),
            ("乌托邦", "（Utopia）理想中最美好的社会，比喻不可能实现的空想"),
            ("切实可行", "从实际出发，能够实行"),
            ("精华", "事物最重要、最好的部分"),
            ("构筑", "建造、修筑"),
            ("仅靠", "只依靠"),
            ("保障", "保护（生命、财产、权利等），使不受侵犯和破坏"),
            ("公平", "处理事情合情合理，不偏袒哪一方面"),
            ("公正", "公平正直，没有偏私"),
            ("消费必需品", "满足日常生活需要的消费品"),
            ("才智", "才能和智慧"),
            ("社会底层", "社会中地位最低、生活最贫困的阶层"),
            ("强身健体", "使身体强壮健康"),
            ("奠定基础", "建立基础"),
        ],
    ),
    (
        "本次庆典是在欢乐祥和的气氛下举行的。古老的赫尔维蒂联邦最高委员会及其尊敬的主席、深得上帝与人类挚爱的瓦莱州派出的首席代表、这座美丽而又好客的城市的领导们、远近闻名的歌手，以及历经千挑万选、朝气蓬勃的体操团队，齐聚于此地，为这次盛会赋予了历史自觉性、公民精神、自然性、青春以及艺术性等五重声誉。",
        "描述本次庆典的欢乐祥和气氛，列举与会各方，指出庆典被赋予历史自觉性、公民精神、自然性、青春、艺术性五重声誉。",
        "演讲手法：排比式列举（赫尔维蒂联邦主席、瓦莱州代表、城市领导、歌手、体操团队），体现庆典的隆重和参与的广泛。长句结构复杂，典雅庄重。五重声誉的概括（历史自觉性、公民精神、自然性、青春、艺术性）凝练有力。",
        [
            ("祥和", "吉祥平和"),
            ("赫尔维蒂联邦", "瑞士的古称，赫尔维蒂是瑞士的拉丁名"),
            ("瓦莱州", "瑞士的一个州"),
            ("首席代表", "最高级别、第一位的代表"),
            ("好客", "乐于接待客人"),
            ("千挑万选", "经过很多次挑选"),
            ("朝气蓬勃", "形容充满了生命和活力"),
            ("齐聚", "聚集在一起"),
            ("赋予", "交给（重大任务、使命等）"),
            ("历史自觉性", "对历史的清醒认识和主动担当"),
            ("公民精神", "公民应有的责任感和参与意识"),
            ("声誉", "声望名誉"),
        ],
    ),
    (
        "愿钟爱勇敢者的幸运之神，厚待刚刚决定申办第7届现代奥林匹克运动会的比利时人民的美好愿望。",
        "祝福比利时人民申办第7届现代奥运会的美好愿望能够实现。",
        "演讲手法：拟人（幸运之神钟爱勇敢者、厚待），表达美好祝愿。句式简短，是演讲中常见的祝福式表达，庄重而温暖。",
        [
            ("钟爱", "特别喜爱"),
            ("厚待", "优厚地对待"),
            ("申办", "申请举办"),
        ],
    ),
    (
        "目前的形势，依然严峻。狂风骤雨之后，我们迎来破晓的黎明。待到中午时分，湛蓝的天空必将万里无云；收获者的双臂，捧满沉甸甸的金黄麦穗。",
        "指出当前形势依然严峻，但以破晓黎明和金黄麦穗的意象展望未来，表达对奥林匹克运动光明前景的坚定信念。",
        "演讲手法：比喻（狂风骤雨、破晓的黎明、湛蓝的天空、金黄麦穗），以自然景象比喻历史进程和美好未来，诗歌般的语言。时间顺序（破晓→中午）象征从艰难到光明的发展。以景结情，余味悠长，是全文最富诗意的段落。",
        [
            ("严峻", "严厉、严肃，形容形势严重"),
            ("狂风骤雨", "又猛又急的大风雨，比喻激烈的斗争或动荡"),
            ("破晓", "天刚亮"),
            ("湛蓝", "深蓝色（多用来形容天空、湖海等）"),
            ("万里无云", "天空晴朗，没有一丝云彩"),
            ("沉甸甸", "形容沉重"),
            ("麦穗", "麦秆顶端开花结实的部分"),
        ],
    ),
]

parts = [
    ("第一部分", "回顾历史，点明主题", "1–2 段", "以庄重称呼开场，回顾奥林匹克运动复兴20年来的历程，指出历经一战浩劫后奥林匹克主义挺了过来，将扮演崭新角色。"),
    ("第二部分", "阐述奥林匹克精神的内涵", "3–5 段", "论述平和与自信的重要性，指出自信比勇气更能根除恐惧；详细阐述奥林匹克主义与一般体育运动的区别，追溯古希腊奥林匹克主义的起源。"),
    ("第三部分", "重启奥林匹克时代，面向大众", "6–8 段", "分析青少年被教育枷锁束缚的现状，呼吁重启奥林匹克时代；强调奥林匹克运动必须面向大众，阐述完美的民主的奥林匹克精神的内涵。"),
    ("第四部分", "总结庆典，展望未来", "9–11 段", "描述庆典的五重声誉，祝福比利时申办奥运，以破晓黎明和金黄麦穗的诗意意象展望光明未来。"),
]

para_part = [0,0, 1,1,1, 2,2,2, 3,3,3]

fulltext_paras = [p[0] for p in paragraphs]

def annotate(text, annos):
    items = sorted(annos, key=lambda x: len(x[0]), reverse=True)
    result = text
    used = set()
    for word, note in items:
        if word in used:
            continue
        idx = result.find(word)
        if idx != -1:
            before = result[:idx]
            if before.count("<span") == before.count("</span>"):
                span = f'<span class="anno-word" data-note="{note}">{word}</span>'
                result = result[:idx] + span + result[idx+len(word):]
                used.add(word)
    return result

verse_html = ""
current_part = -1
for i, (orig, content, method, annos) in enumerate(paragraphs):
    pi = para_part[i]
    if pi != current_part:
        current_part = pi
        pname, ptitle, prange, poverview = parts[pi]
        verse_html += f'''      <div class="part-head"><span class="p-num">{pname}</span><h3>{ptitle}</h3><span class="range">{prange}</span></div>
      <div class="part-overview">{poverview}</div>
'''
    orig_ann = annotate(orig, annos)
    verse_html += f'''      <div class="verse" id="l{i+1}" data-i="{i}">
        <div class="v-top"><span class="v-no">{i+1}</span><div class="v-line">{orig_ann}</div></div>
        <details class="v-more">
          <summary>内容 · 手法</summary>
          <div class="d-body">
            <div class="v-sec"><b class="v-label">内容概括</b>
              <div class="v-trans">{content}</div>
            </div>
            <div class="v-sec"><b class="v-label">手法分析</b>
              <div class="d-body"><p>{method}</p></div>
            </div>
          </div>
        </details>
      </div>
'''

fulltext_html = ""
for para in fulltext_paras:
    fulltext_html += f'    <div class="pl">{para}</div>\n'

dict_words = [
    {"w":"崩","py":"bēng","q":"整个世界分□离析","tip":"「崩」山字头，倒塌；不要写成「绷」（绞丝旁）"},
    {"w":"析","py":"xī","q":"整个世界分崩离□","tip":"「析」木字旁，分开；不要写成「折」（提手旁）"},
    {"w":"劫","py":"jié","q":"并没有成为这场浩□的牺牲品","tip":"「劫」力字旁，灾难；不要写成「却」"},
    {"w":"襁","py":"qiǎng","q":"还在□褓中的婴儿","tip":"「襁」衣字旁，包裹婴儿的被子；生僻字，与「抢」区分"},
    {"w":"褓","py":"bǎo","q":"还在襁□中的婴儿","tip":"「褓」衣字旁，包裹婴儿的带子；生僻字，与「保」区分"},
    {"w":"凋","py":"diāo","q":"勇气之花在我们当代人的手中早已残败□零了","tip":"「凋」两点水，草木零落；不要写成「调」（言字旁）"},
    {"w":"携","py":"xié","q":"自信与它的姊妹平和总是□手并进","tip":"「携」提手旁，拉着；不要写成「镌」"},
    {"w":"绚","py":"xuàn","q":"古代奥林匹克主义的□丽梦想","tip":"「绚」绞丝旁，色彩华丽；不要写成「询」（言字旁）"},
    {"w":"枷","py":"jiā","q":"青少年开始为呆板而复杂的教育□锁所套牢","tip":"「枷」木字旁，古代刑具；不要写成「架」（木字旁，jià）"},
    {"w":"锁","py":"suǒ","q":"青少年开始为呆板而复杂的教育枷□所套牢","tip":"「锁」金字旁，锁链；不要写成「琐」（王字旁）"},
    {"w":"拙","py":"zhuō","q":"被在愚蠢的放纵和不明智的严厉交互作用下的道德说教以及□劣肤浅的世界观所束缚","tip":"「拙」提手旁，笨拙；不要写成「绌」（chù，绞丝旁）"},
    {"w":"肤","py":"fū","q":"拙劣□浅的世界观","tip":"「肤」月字旁，浅薄；不要写成「扶」（提手旁）"},
    {"w":"祷","py":"dǎo","q":"我向不朽的古希腊精神祈□","tip":"「祷」示字旁，向神祝告；不要写成「涛」（三点水）"},
    {"w":"绽","py":"zhàn","q":"我正目睹它再次含苞□放","tip":"「绽」绞丝旁，裂开；不要写成「淀」（三点水，diàn）"},
    {"w":"钧","py":"jūn","q":"有什么样的贵族特权能令一个青年人身上的形体美、肌肉力量、锻炼的□力以及获胜的意志","tip":"「毅」左边是「豙」，右边是「殳」；不要写成「毅力」的「毅」以外的写法"},
    {"w":"谱","py":"pǔ","q":"非得同他的家□或钱包挂钩呢","tip":"「谱」言字旁，记载世系的书；不要写成「普」"},
    {"w":"蛮","py":"mán","q":"在野□的军国主义协助下的极权姿态","tip":"「蛮」虫字底，粗野；不要写成「满」（三点水）"},
    {"w":"邦","py":"bāng","q":"某些过去一直被视为乌托□的原则","tip":"「邦」右耳旁，国家；「乌托邦」是音译词，固定写法"},
    {"w":"湛","py":"zhàn","q":"□蓝的天空必将万里无云","tip":"「湛」三点水，深；不要写成「堪」（提土旁）"},
    {"w":"穗","py":"suì","q":"捧满沉甸甸的金黄麦□","tip":"「穗」禾字旁，麦秆顶端的花实；不要写成「惠」"},
]

dict_notes = [
    {"w":"分崩离析","a":"崩塌解体，四分五裂，形容国家或集团分裂瓦解","q":"整个世界分崩离析"},
    {"w":"浩劫","a":"大灾难","q":"并没有成为这场浩劫的牺牲品"},
    {"w":"无所畏惧","a":"什么也不怕，形容非常勇敢","q":"而是无所畏惧、无可指摘地挺了过来"},
    {"w":"无可指摘","a":"没有什么可以指责的，形容完美","q":"而是无所畏惧、无可指摘地挺了过来"},
    {"w":"推崇","a":"十分推重、崇敬","q":"为渐趋平和而又充满自信的青少年所推崇"},
    {"w":"襁褓","a":"（qiǎng bǎo）包裹婴儿的被子和带子","q":"还在襁褓中的婴儿"},
    {"w":"行将就木","a":"快要进棺材了，指人临近死亡","q":"并在他行将就木时"},
    {"w":"针锋相对","a":"针尖对针尖，比喻双方尖锐对立","q":"人类学会用勇气来针锋相对"},
    {"w":"残败凋零","a":"残缺衰败，草木零落，比喻事物衰败","q":"勇气之花早已残败凋零了"},
    {"w":"相辅相成","a":"互相补充，互相配合","q":"自信与平和总是携手并进、相辅相成"},
    {"w":"绚丽","a":"灿烂美丽","q":"古代奥林匹克主义的绚丽梦想"},
    {"w":"误入歧途","a":"由于受煽惑而走上了错误的道路","q":"因夸大某种正确思想而误入歧途"},
    {"w":"枷锁","a":"枷和锁链，比喻压迫和束缚","q":"为呆板而复杂的教育枷锁所套牢"},
    {"w":"拙劣","a":"笨拙而低劣","q":"拙劣肤浅的世界观"},
    {"w":"肤浅","a":"（学识）浅，（理解）不深","q":"拙劣肤浅的世界观"},
    {"w":"一呼百应","a":"一声召唤，很多人响应，形容威望高","q":"古希腊遗留下来的一呼百应的体育观"},
    {"w":"愧不敢当","a":"感到惭愧，承当不起","q":"那我着实愧不敢当"},
    {"w":"含苞怒放","a":"花骨朵儿盛开，比喻事物蓬勃发展","q":"我正目睹它再次含苞怒放"},
    {"w":"乌托邦","a":"理想中最美好的社会，比喻空想","q":"被视为乌托邦的原则"},
    {"w":"奠定基础","a":"建立基础","q":"今天我们要为它奠定基础"},
    {"w":"朝气蓬勃","a":"形容充满了生命和活力","q":"历经千挑万选、朝气蓬勃的体操团队"},
    {"w":"严峻","a":"严厉、严肃，形容形势严重","q":"目前的形势，依然严峻"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《庆祝奥林匹克运动复兴25周年》顾拜旦</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">法国 · 顾拜旦</div>
  <h1 class="hero-title">庆祝奥林匹克运动复兴25周年</h1>
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
        <option value="100">100%</option>
        <option value="150">150%</option>
        <option value="200">200%</option>
        <option value="250">250%</option>
        <option value="300">300%</option>
      </select>
      <button id="btnAll">展开</button>
      <button id="btnRecite">背诵</button>
      <button id="btnPrint">打印</button>
    </div>
  </div>
</nav>

<main class="wrap">
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《庆祝奥林匹克运动复兴25周年》是顾拜旦于1919年4月在瑞士洛桑国际奥委会全体委员大会上发表的演讲。此时第一次世界大战刚刚结束，世界满目疮痍。顾拜旦以诗歌般的语言回顾了奥林匹克运动25年来的历程，阐述了奥林匹克精神的内涵与价值，呼吁重启奥林匹克时代，倡导面向大众的民主的奥林匹克精神。</p>
    <p>这是一篇庄重典雅的演讲词，语言富有诗意，大量使用比喻、排比、反问等修辞手法，兼具理性的深度和感性的魅力，是奥林匹克运动的重要文献。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>顾拜旦（1863—1937），全名皮埃尔·德·顾拜旦，法国教育家、社会活动家，现代奥林匹克运动的创始人，被誉为{LQ}现代奥林匹克之父{RQ}。1892年首次提出复兴奥林匹克运动的口号，1894年推动成立国际奥林匹克委员会，1896年第一届现代奥运会在希腊举行。1896年至1925年任国际奥委会主席。</p>
    <p style="margin-top:10px;color:var(--ink2)">顾拜旦设计了奥林匹克五环标志，倡导奥林匹克精神。他的著名诗作《体育颂》热情讴歌了体育的美丽、正义、勇气、荣誉、乐趣、活力、进步与和平。1937年在瑞士日内瓦去世，按其遗嘱，心脏安葬在希腊奥林匹亚。</p>
  </div>
  <div class="box">
    <h3>演讲背景</h3>
    <p><b>时间地点：</b>1919年4月，瑞士洛桑，国际奥委会全体委员大会。这次大会是第一次世界大战结束后国际奥委会的首次重要会议。</p>
    <p style="margin-top:8px"><b>历史背景：</b>1914年6月，国际奥委会在巴黎庆祝奥林匹克运动复兴20周年。但不久第一次世界大战爆发，整个世界分崩离析，奥林匹克运动也被迫中断。战后，顾拜旦发表这篇演讲，呼吁在废墟上重建奥林匹克精神。</p>
    <p style="margin-top:8px"><b>奥林匹克复兴：</b>1894年，顾拜旦在巴黎推动成立国际奥委会，决定恢复奥林匹克运动会。1896年第一届现代奥运会在希腊雅典举行。到1919年，正好是奥林匹克运动复兴25周年。</p>
  </div>
  <div class="box">
    <h3>文体知识</h3>
    <p><b>演讲词：</b>在公众场合发表的讲话。本文是国际会议上的正式演讲，语言庄重典雅，富有诗意，兼具理性深度和感性魅力。</p>
    <p style="margin-top:8px"><b>奥林匹克主义：</b>顾拜旦提出的概念，指一种将身体、意志和精神的各种品质均衡地结合起来并使之得到提高的人生哲学。它超越了一般的体育运动，强调体育与文化、教育的融合。</p>
    <p style="margin-top:8px"><b>演讲的语言特点：</b>本文语言诗歌化，大量使用比喻（含苞怒放、破晓的黎明、金黄麦穗）、排比、反问、拟人等修辞手法，长句与短句结合，节奏富于变化，典雅庄重而又激情澎湃。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文诵读《庆祝奥林匹克运动复兴25周年》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1GE411K7Fp&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读庆祝奥林匹克运动复兴25周年"></iframe>
        <a href="https://www.bilibili.com/video/BV1GE411K7Fp" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>央视纪录片：现代奥运之父顾拜旦</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1rE411e7Zz&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="顾拜旦纪录片"></iframe>
        <a href="https://www.bilibili.com/video/BV1rE411e7Zz" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 内容 · 演讲手法</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{fulltext_html}  </div>
  <div class="verse-list" id="verseList">
{verse_html}  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">演讲特色 · 语言艺术 · 论证 · 主题</span></div>

  <div class="box">
    <h3>演讲特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">庄重典雅，诗歌般的语言</div>
        <p>顾拜旦是教育家，也是诗人。这篇演讲语言典雅庄重，大量使用四字成语和书面语，如分崩离析、无所畏惧、无可指摘、行将就木、含苞怒放等。比喻如诗歌般优美（破晓的黎明、金黄麦穗），使演讲具有强烈的文学色彩和感染力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">理性与感性的统一</div>
        <p>演讲既有理性的分析——区分奥林匹克主义与一般体育运动、阐述民主的奥林匹克精神的内涵；又有感性的抒发——对恐惧的描绘、对美好未来的憧憬。理性与感性交融，使演讲既有说服力又有感染力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">视野宏大，立意高远</div>
        <p>演讲从人类文明的高度审视奥林匹克运动，将其与古文明的精华、新生文明的支柱、社会底层人们的福祉联系起来。顾拜旦不自居功（第一个仆从），而是将奥林匹克运动视为人类共同的事业，立意高远，胸怀博大。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>语言艺术</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">比喻丰富，形象生动</div>
        <p>{LQ}奥林匹克主义挺了过来{RQ}（拟人）、{LQ}勇气之花残败凋零{RQ}（比喻）、{LQ}教育枷锁{RQ}（比喻）、{LQ}含苞怒放{RQ}（比喻）、{LQ}破晓的黎明{RQ}{LQ}金黄麦穗{RQ}（比喻）。大量比喻使抽象的道理变得形象可感，也使语言富有诗意。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">排比与反问，气势充沛</div>
        <p>排比：{LQ}为灿烂阳光所萦绕，为音乐所振奋，或被嵌入圆柱式大厅{RQ}；{LQ}历史自觉性、公民精神、自然性、青春以及艺术性{RQ}。反问：{LQ}在当今时代又怎能称得上完美呢？{RQ}{LQ}有什么名义能将大众排除在奥林匹克精神之外呢？{RQ}排比增强气势，反问引人深思。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">长句短句结合，节奏富于变化</div>
        <p>长句如{LQ}渴求进步但又常常因夸大某种正确思想而误入歧途的人类精神……{RQ}，结构复杂，信息密集，体现庄重风格；短句如{LQ}目前的形势，依然严峻。{RQ}斩钉截铁，掷地有声。长短交错，节奏富于变化。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比鲜明，观点突出</div>
        <p>五年前的庆祝 vs 五年的浩劫；一般竞技只涉及自身 vs 奥林匹克主义与自然艺术融为一体；当时足够 vs 今天必须面向大众。多处对比使观点鲜明突出，也使论证更加严密。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>论证方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">道理论证：层层深入</div>
        <p>从平和与自信的重要性，到奥林匹克主义区别于一般体育运动，再到面向大众的民主精神，最后落脚于为完美的奥林匹克精神奠定基础。道理论证层层深入，逻辑严密，体现了思想家的深度。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比论证：正误分明</div>
        <p>勇气 vs 自信（根除恐惧的良药更多是自信）；一般体育运动 vs 奥林匹克主义（后者超越前者）；盎格鲁-撒克逊功利体育观 vs 古希腊体育观（需要融合）。对比使概念的内涵更加清晰。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">让步论证：客观全面</div>
        <p>{LQ}当然，仅靠奥林匹克精神，并不足以保障社会层面的和平……但是，奥林匹克精神致力于让社会底层的人们……{RQ}先承认局限，再强调价值，使论证更加客观全面，更有说服力。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《庆祝奥林匹克运动复兴25周年》回顾了奥林匹克运动复兴25年来的历程，阐述了奥林匹克精神的内涵——平和与自信、超越一般竞技、与自然艺术融合；分析了重启奥林匹克时代的必要性，强调奥林匹克运动必须面向大众，倡导完美的、民主的奥林匹克精神，表达了对奥林匹克运动光明未来的坚定信念和对人类和平进步的美好期望。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 字音形 · 修辞 · 写法 · 常识</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">分崩离析</span><span class="acc-d">崩塌解体，四分五裂，形容国家或集团分裂瓦解。</span></div>
      <div class="acc-item"><span class="acc-w">浩劫</span><span class="acc-d">大灾难。</span></div>
      <div class="acc-item"><span class="acc-w">无所畏惧</span><span class="acc-d">什么也不怕，形容非常勇敢。</span></div>
      <div class="acc-item"><span class="acc-w">无可指摘</span><span class="acc-d">没有什么可以指责的，形容完美。</span></div>
      <div class="acc-item"><span class="acc-w">推崇</span><span class="acc-d">十分推重、崇敬。</span></div>
      <div class="acc-item"><span class="acc-w">襁褓</span><span class="acc-d">（qiǎng bǎo）包裹婴儿的被子和带子。</span></div>
      <div class="acc-item"><span class="acc-w">行将就木</span><span class="acc-d">快要进棺材了，指人临近死亡。木，棺材。</span></div>
      <div class="acc-item"><span class="acc-w">相辅相成</span><span class="acc-d">互相补充，互相配合。</span></div>
      <div class="acc-item"><span class="acc-w">枷锁</span><span class="acc-d">枷和锁链，比喻压迫和束缚。</span></div>
      <div class="acc-item"><span class="acc-w">拙劣</span><span class="acc-d">（zhuō）笨拙而低劣。</span></div>
      <div class="acc-item"><span class="acc-w">乌托邦</span><span class="acc-d">理想中最美好的社会，比喻不可能实现的空想。</span></div>
      <div class="acc-item"><span class="acc-w">朝气蓬勃</span><span class="acc-d">形容充满了生命和活力。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">分崩离析</span><span class="acc-d">（bēng xī）「崩」山字头，「析」木字旁；不要写成「分崩离折」。</span></div>
      <div class="acc-item"><span class="acc-w">浩劫</span><span class="acc-d">（jié）力字旁；不要写成「浩却」。</span></div>
      <div class="acc-item"><span class="acc-w">襁褓</span><span class="acc-d">（qiǎng bǎo）均为衣字旁；生僻字，注意不要写成「抢保」。</span></div>
      <div class="acc-item"><span class="acc-w">凋零</span><span class="acc-d">（diāo）两点水；与「调」（diào，言字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">携手</span><span class="acc-d">（xié）提手旁；不要写成「镌手」。</span></div>
      <div class="acc-item"><span class="acc-w">绚丽</span><span class="acc-d">（xuàn）绞丝旁；与「询」（xún，言字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">枷锁</span><span class="acc-d">（jiā suǒ）「枷」木字旁，「锁」金字旁；不要写成「架锁」。</span></div>
      <div class="acc-item"><span class="acc-w">拙劣</span><span class="acc-d">（zhuō）提手旁；与「绌」（chù，绞丝旁，相形见绌）区分。</span></div>
      <div class="acc-item"><span class="acc-w">祈祷</span><span class="acc-d">（dǎo）示字旁；与「涛」（tāo，三点水）区分。</span></div>
      <div class="acc-item"><span class="acc-w">湛蓝</span><span class="acc-d">（zhàn）三点水；与「堪」（kān，提土旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">麦穗</span><span class="acc-d">（suì）禾字旁；不要写成「麦惠」。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞方法</h3>
      <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">教育枷锁、含苞怒放、破晓的黎明、金黄麦穗等，使抽象道理形象可感，语言富有诗意。</span></div>
      <div class="acc-item"><span class="acc-w">拟人</span><span class="acc-d">奥林匹克主义挺了过来、恐惧给致命一击、幸运之神厚待，赋予抽象事物以生命。</span></div>
      <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">为阳光所萦绕、为音乐所振奋、被嵌入圆柱式大厅；五重声誉的列举，增强气势。</span></div>
      <div class="acc-item"><span class="acc-w">反问</span><span class="acc-d">怎能称得上完美、有什么名义能将大众排除，引人深思，强调面向大众的必要性。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">勇气 vs 自信、一般竞技 vs 奥林匹克主义、当时 vs 今天，使观点鲜明。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">语言典雅</span><span class="acc-d">大量使用成语和书面语，使演讲庄重典雅，适合国际会议的正式场合。</span></div>
      <div class="acc-item"><span class="acc-w">善用比喻</span><span class="acc-d">以自然景象比喻历史进程和美好未来，使抽象道理形象化，也使语言富有诗意。</span></div>
      <div class="acc-item"><span class="acc-w">让步论证</span><span class="acc-d">先承认奥林匹克精神的局限，再强调其独特价值，使论证客观全面，更有说服力。</span></div>
      <div class="acc-item"><span class="acc-w">以景结情</span><span class="acc-d">结尾以破晓黎明和金黄麦穗的意象展望未来，余味悠长，是演讲的经典结尾方式。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">顾拜旦</span><span class="acc-d">（1863—1937）法国教育家，现代奥林匹克运动创始人，被誉为{LQ}现代奥林匹克之父{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">奥林匹克运动会</span><span class="acc-d">起源于古希腊，因举办地在奥林匹亚而得名。1896年第一届现代奥运会在希腊雅典举行，每4年一届。</span></div>
      <div class="acc-item"><span class="acc-w">国际奥委会</span><span class="acc-d">1894年在巴黎成立，是奥林匹克运动的最高权力机构，总部设在瑞士洛桑。</span></div>
      <div class="acc-item"><span class="acc-w">奥林匹克五环</span><span class="acc-d">顾拜旦1913年设计，蓝黄黑绿红五环相连，象征五大洲团结。</span></div>
      <div class="acc-item"><span class="acc-w">阿尔弗斯河</span><span class="acc-d">希腊的河流，古代奥林匹克运动会的举办地奥林匹亚位于此河附近。</span></div>
      <div class="acc-item"><span class="acc-w">盎格鲁-撒克逊</span><span class="acc-d">英国的主要民族，这里指英美的文化传统。</span></div>
      <div class="acc-item"><span class="acc-w">乌托邦</span><span class="acc-d">（Utopia）英国思想家莫尔虚构的理想社会，后泛指不可能实现的空想。</span></div>
    </div>
  </div>

</section>

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
  <div class="kai">《庆祝奥林匹克运动复兴25周年》</div>
  <div>顾拜旦 · 法国 · 1919年瑞士洛桑国际奥委会演讲</div>
</footer>
</main>

<button class="top-btn" id="topBtn" title="回到顶部">↑</button>
<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>
<div class="dictate" id="dictate" hidden>
  <div class="dictate-top">
    <span class="dictate-mode" id="dictMode">字形听写</span>
    <span class="dictate-progress" id="dictProgress">第 1 / 5 题</span>
    <button class="dictate-fs" id="dictFsMinus">A−</button>
    <button class="dictate-fs" id="dictFsPlus">A+</button>
    <button class="dictate-exit" id="dictExit">退出</button>
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
{main_js}
</script>
<script>
var DICT_WORDS = {json.dumps(dict_words, ensure_ascii=False)};
var DICT_NOTES = {json.dumps(dict_notes, ensure_ascii=False)};
</script>

</body>
</html>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Generated: {OUT}")
print(f"Paragraphs: {len(paragraphs)}")
print(f"Anno count: {sum(len(p[3]) for p in paragraphs)}")
print(f"Words: {len(dict_words)}, Notes: {len(dict_notes)}")
