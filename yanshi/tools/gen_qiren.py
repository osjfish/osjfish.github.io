# -*- coding: utf-8 -*-
"""生成《杞人忧天》交互式教学课件"""
import json, os

BENCH = r"D:\App\Apps\yanshi\jichengtiansiyeyou-sushi.html"
OUT = r"D:\App\Apps\yanshi\qirenyoutian-liezi.html"
LS_KEY = "qiren_fs"

with open(BENCH, encoding="utf-8") as f:
    bench = f.read()

css = bench[bench.index("<style>")+7:bench.index("</style>")]
js_start = bench.index("<script>\n(function(){")
js_end = bench.index("</script>\n<script>\nvar DICT_WORDS")
main_js = bench[js_start+8:js_end]

HERO_SIDE = "战国 · 列子"
HERO_TITLE = "杞人忧天"
PAGE_TITLE = "《杞人忧天》列子"

BG_LEAD = [
    "《杞人忧天》选自《列子·天瑞》，是一则著名的寓言故事。文章通过杞国人担忧天地崩坠而废寝忘食，经人开导后释然大喜的故事，讽刺了那种为不必要的事情而担忧的人，同时也蕴含着对宇宙自然的朴素思考。",
    "“杞人忧天”后来成为成语，比喻为不必要的事情而忧虑。但这则寓言的内涵不止于此——那位“晓之者”对天地的解释，虽然在今天看来并不科学，却代表了古人对宇宙自然的理性探索精神，具有朴素的唯物主义思想萌芽。"
]

AUTHOR_BOX = [
    ("列子与《列子》", [
        "列子，名御寇，战国时期郑国人，道家学派代表人物之一。其学本于黄帝、老子，主张清静无为。《列子》又名《冲虚真经》，是道家经典之一，旧题列御寇撰，今本可能为晋人张湛辑录整理。",
        "《列子》共八篇，包括《天瑞》《黄帝》《周穆王》《仲尼》《汤问》《力命》《杨朱》《说符》。书中保存了大量先秦寓言故事和神话传说，如《愚公移山》《夸父追日》《杞人忧天》等，想象丰富，寓意深刻，对后世文学影响深远。"
    ])
]

BG_BOX = [
    ("写作背景", [
        "<b>《天瑞》篇：</b>本文选自《列子·天瑞》。“天瑞”指天地间的祥瑞、自然现象。该篇主要论述宇宙万物的生成与变化，包含多则寓言故事，《杞人忧天》是其中最著名的一则。",
        "<b>战国思潮：</b>战国时期，百家争鸣，人们对宇宙自然的思考日益深入。道家学派关注天人关系，探讨宇宙本源。《列子》中对天地的解释——“天，积气耳”“地，积块耳”——虽然朴素，却代表了当时人们试图以自然原因解释自然现象的理性努力。",
        "<b>寓言传统：</b>先秦诸子善用寓言说理。《列子》中的寓言往往想象奇特、寓意深远，既有趣味性，又有思想性。《杞人忧天》以一个人的担忧为线索，通过对话展开，既讽刺了庸人自扰，也探讨了宇宙观，是寓言中的佳作。"
    ])
]

MEDIA = [
    ("《杞人忧天》课文诵读", "BV18D4y1o7nx", "杞人忧天诵读"),
    ("七年级语文《杞人忧天》动画", "BV13d4y1s74F", "杞人忧天动画"),
]

# 逐句: (原文, 译文, 赏析, [(词,注释),...])
VERSES = [
    (
        "杞国有人忧天地崩坠，身亡所寄，废寝食者。",
        "杞国有个人担忧天会崩塌、地会陷落，自己没有地方存身，（于是）睡不着觉、吃不下饭。",
        "开篇交代故事的起因和主人公。“忧天地崩坠”是杞人担忧的内容——天塌地陷，在古人看来是最可怕的灾难。“身亡所寄”写担忧的程度——连存身之处都没有了。“废寝食者”三字极写其忧之深——到了寝食俱废的地步。一个为天地而忧的形象，寥寥数笔便跃然纸上。",
        [
            ("杞国", "春秋时期的诸侯国，在今河南杞县一带"),
            ("忧", "担忧，忧虑"),
            ("崩坠", "崩塌坠落。崩，倒塌；坠，坠落"),
            ("身亡所寄", "自己没有地方存身。亡，同“无”，没有；寄，依附、存身"),
            ("废寝食", "睡不着觉，吃不下饭。废，停止、废止"),
        ]
    ),
    (
        "又有忧彼之所忧者，因往晓之，曰：“天，积气耳，亡处亡气。若屈伸呼吸，终日在天中行止，奈何忧崩坠乎？”",
        "又有一个为他的忧愁而担心的人，于是前去开导他，说：“天，不过是聚积的气体罢了，没有哪个地方没有空气。你一举一动、一呼一吸，整天都在天空里活动，怎么还担心天会塌下来呢？”",
        "“晓之者”出场，故事进入对话阶段。他对天的解释是“积气耳”——天不过是聚积的气体，这在当时是一种朴素的自然观。“亡处亡气”强调无处不在；“若屈伸呼吸，终日在天中行止”以人的日常活动为例，说明天不会崩坠；“奈何忧崩坠乎”以反问作结，语气亲切而有说服力。这个解释虽然不科学，却体现了以自然原因解释自然现象的理性精神。",
        [
            ("忧彼之所忧", "为他的忧愁而担心。彼，他，指杞人"),
            ("因", "于是，就"),
            ("往晓之", "前去开导他。晓，开导、告知；之，代词，指杞人"),
            ("积气", "聚积的气体"),
            ("耳", "语气词，相当于“罢了”"),
            ("亡处亡气", "没有哪个地方没有气。亡，同“无”"),
            ("若", "你"),
            ("屈伸", "指身体的弯曲和伸展，即一举一动"),
            ("行止", "行动和停留，这里指活动"),
            ("奈何", "为何，为什么"),
        ]
    ),
    (
        "其人曰：“天果积气，日月星宿，不当坠耶？”",
        "那个人说：“天如果真是聚积的气体，那日月星辰不就会掉下来吗？”",
        "杞人的追问，逻辑清晰——既然天是气体，那日月星辰挂在天上，岂不是会掉下来？这个追问很有道理，也说明杞人并非完全的“庸人自扰”，他是在认真思考宇宙问题。“不当坠耶”的反问，既表现了他的疑虑，也推动了对话的深入。",
        [
            ("其人", "那个人，指杞人"),
            ("果", "果然，果真"),
            ("星宿", "星辰。宿，星的位次，这里泛指星辰"),
            ("不当坠耶", "不应当掉下来吗？当，应当；耶，语气词，相当于“吗”"),
        ]
    ),
    (
        "晓之者曰：“日月星宿，亦积气中之有光耀者，只使坠，亦不能有所中伤。”",
        "开导他的人说：“日月星辰，也是气体中发光的东西，即使掉下来，也不会有什么伤害。”",
        "晓之者进一步解释日月星辰的本质——也是气体，不过是发光的气体。“只使坠，亦不能有所中伤”是关键：即使掉下来，也不会伤人。这个回答虽然在科学上不正确（陨石确实可能伤人），但在当时的认知水平下，是一种合理的推测。它体现了古人试图消除恐惧、以理性态度面对自然的努力。",
        [
            ("光耀", "发光。光，发光；耀，照耀"),
            ("只使", "即使，纵使"),
            ("中伤", "伤害。中，击中、伤害"),
        ]
    ),
    (
        "其人曰：“奈地坏何？”",
        "那个人说：“地陷下去怎么办呢？”",
        "杞人又追问地的问题——天的问题解决了，地的问题又来了。“奈地坏何”是固定句式，意思是“对地坏怎么办”。这个追问说明杞人的担忧是系统性的——天地都在他的忧虑范围之内。同时也推动对话进入第二个层次：地的本质是什么？",
        [
            ("奈……何", "固定句式，对……怎么办，把……怎么样"),
            ("坏", "倒塌，陷落"),
        ]
    ),
    (
        "晓之者曰：“地，积块耳，充塞四虚，亡处亡块。若躇步跐蹈，终日在地上行止，奈何忧其坏？”",
        "开导他的人说：“地，不过是聚积的土块罢了，填满了四方的虚空之处，没有哪个地方没有土块。你踩踏行走，整天都在地上活动，怎么还担心地会陷下去呢？”",
        "晓之者对地的解释与对天的解释对称——天是“积气”，地是“积块”。“充塞四虚，亡处亡块”强调地的无处不在；“若躇步跐蹈，终日在地上行止”以人的日常踩踏为例，说明地不会坏；“奈何忧其坏”以反问作结，与前文“奈何忧崩坠乎”呼应，结构工整。天地对举，气块对称，体现了古人对称思维的特点。",
        [
            ("积块", "聚积的土块。块，土块"),
            ("充塞", "填满，塞满"),
            ("四虚", "四方的虚空之处。四，四方；虚，空虚之处"),
            ("躇步跐蹈", "泛指人的站立行走。躇，立；步，行；跐，踩；蹈，踏"),
            ("行止", "行动和停留"),
            ("奈何", "为何，为什么"),
        ]
    ),
    (
        "其人舍然大喜，晓之者亦舍然大喜。",
        "那个人听了，消除了疑虑，非常高兴；开导他的人也消除了疑虑，非常高兴。",
        "结尾两个“舍然大喜”，一写杞人，一写晓之者，相映成趣。杞人“舍然大喜”是因为担忧消除——从“废寝食”到“大喜”，变化之大，正见其忧之深、释之彻。晓之者“亦舍然大喜”则耐人寻味——他也在为杞人担忧，如今杞人释然，他也释然。两个“大喜”不仅结束了故事，也留下了思考：杞人的担忧真的完全消除了吗？晓之者的解释真的正确吗？这正是寓言的余味。",
        [
            ("舍然", "消除疑虑的样子。舍，同“释”，解除、消除"),
            ("大喜", "非常高兴"),
            ("亦", "也"),
        ]
    ),
]

APP_BOXES = [
    ("人物形象", [
        ("庸人自扰的杞人", "杞人是故事的主角。他“忧天地崩坠”到了“废寝食”的地步，看似可笑，实则是一个认真思考宇宙问题的人——他追问“日月星宿不当坠耶”“奈地坏何”，逻辑清晰，并非毫无道理的胡思乱想。他的可笑之处在于：为目前不可能发生的事情过度担忧，以至于影响正常生活。从“废寝食”到“舍然大喜”，他的情绪变化之大，正见其性格的单纯与执着。"),
        ("热心理性的晓之者", "晓之者是故事中的智者形象。他“忧彼之所忧”，主动前去开导，可见其热心。他对天地的解释——“天，积气耳”“地，积块耳”——虽然在今天看来并不科学，却代表了古人以自然原因解释自然现象的理性努力，具有朴素的唯物主义思想萌芽。他善于用日常经验（屈伸呼吸、躇步跐蹈）来说明抽象道理，循循善诱，是一位合格的“启蒙者”。"),
    ]),
    ("艺术特色", [
        ("对话推动，结构工整", "全文以对话推动情节发展，结构清晰。杞人两问（天坠、地坏），晓之者两答（积气、积块），问答之间形成工整的对称结构。“奈何忧崩坠乎”与“奈何忧其坏”前后呼应，“积气耳”与“积块耳”天地对举，读来既有节奏感，又有逻辑美。"),
        ("层层递进，逻辑严密", "杞人的担忧由天及地，层层递进：先忧天崩，再忧日月星辰坠，最后忧地坏。晓之者的解释也相应地由天及地，逐一化解。整个对话逻辑严密，环环相扣，读者在阅读中既能感受到辩论的趣味，也能体会到古人的宇宙观。"),
        ("寓理于事，意在言外", "作为寓言，本文的主旨不在故事本身，而在故事之外。“杞人忧天”既讽刺了为不必要之事担忧的人，也探讨了宇宙自然的本质。晓之者的解释虽然朴素，却体现了理性探索精神。一则短寓言，包含了讽刺、哲理、科学思想萌芽等多重意蕴，耐人寻味。"),
        ("细节传神，人物鲜活", "“废寝食者”四字写杞人忧之深；“舍然大喜”四字写其释之彻；晓之者“亦舍然大喜”则见其热心。寥寥数语，人物形象便鲜活可感。这种以极简笔墨刻画人物的手法，正是先秦寓言的魅力所在。"),
    ]),
    ("名句赏析", [
        ("天，积气耳，亡处亡气。", "晓之者对天的本质解释。“积气耳”三字，以朴素的自然观否定了天的神秘性——天不过是聚积的气体，不是什么神灵居所。“亡处亡气”强调气的无处不在。这个解释虽然在科学上不完全正确（天并非单纯的气体），但在两千多年前，能以自然物质解释天的本质，是一种了不起的理性思考，具有朴素唯物主义思想的萌芽。"),
        ("地，积块耳，充塞四虚，亡处亡块。", "晓之者对地的本质解释，与对天的解释形成工整的对称。“积块耳”说地是聚积的土块，“充塞四虚”说地填满了四方虚空，“亡处亡块”说地无处不在。天地对举，气块对称，体现了古人对称思维的特点。这种解释虽然朴素，却试图以物质构成来解释大地的本质，是古人宇宙观的重要组成部分。"),
        ("其人舍然大喜，晓之者亦舍然大喜。", "全文收尾，两个“舍然大喜”相映成趣。杞人之喜，是担忧消除后的释然；晓之者之喜，是助人成功后的欣慰。两个“大喜”不仅结束了故事，也留下了思考空间：杞人的担忧真的完全消除了吗？晓之者的解释真的无懈可击吗？这种开放式的结尾，使寓言的意蕴更加丰富。"),
    ]),
    ("主题思想", [
        "本文通过记述杞国人担忧天地崩坠、经人开导后释然大喜的故事，讽刺了那种为不必要的事情而过度忧虑的人，告诉人们不要为不切实际的事情而担忧。",
        "同时，这则寓言也蕴含着更深层的思想内涵：晓之者对天地的解释——“天，积气耳”“地，积块耳”——虽然朴素，却代表了古人以自然原因解释自然现象的理性努力，具有朴素的唯物主义思想萌芽。杞人的追问也并非毫无道理，他对宇宙自然的思考，体现了人类对未知世界的探索精神。因此，“杞人忧天”既是讽刺，也是思考——在嘲笑庸人自扰的同时，也应肯定人类对宇宙的好奇与探索。"
    ]),
]

ACC = [
    ("通假字", [
        ("亡", "通“无”，没有。例：身亡所寄 / 亡处亡气"),
        ("舍", "通“释”，解除、消除。例：其人舍然大喜"),
    ]),
    ("古今异义", [
        ("崩", "古义：倒塌（天地崩坠）；今义：崩溃、崩裂"),
        ("寄", "古义：依附、存身（身亡所寄）；今义：寄托、邮寄"),
        ("废", "古义：停止、废止（废寝食）；今义：废弃、残废"),
        ("晓", "古义：开导、告知（因往晓之）；今义：知道、明白"),
        ("只使", "古义：即使、纵使（只使坠）；今义：只使用"),
        ("中伤", "古义：伤害（亦不能有所中伤）；今义：诬蔑别人使受损害"),
        ("躇步跐蹈", "古义：泛指人的站立行走；今义：无此常用词"),
    ]),
    ("一词多义", [
        ("忧", "担忧：杞国有人忧天地崩坠 / 为……担忧：又有忧彼之所忧者"),
        ("亡", "同“无”，没有：身亡所寄 / 灭亡：亡国"),
        ("之", "代词，指杞人：因往晓之 / 结构助词，的：忧彼之所忧者 / 代词，指道理：亦不能有所中伤"),
        ("其", "代词，指地：奈何忧其坏 / 代词，他的：其人曰"),
        ("因", "于是：因往晓之 / 凭借：因势利导"),
        ("若", "你：若屈伸呼吸 / 好像：若隐若现"),
        ("止", "停留：终日在天中行止 / 停止：止有剩骨"),
    ]),
    ("词类活用", [
        ("（本文无典型词类活用）", "《杞人忧天》中无典型的词类活用现象。"),
    ]),
    ("文言句式", [
        ("判断句", "“天，积气耳”“地，积块耳”，“耳”表判断，相当于“是……罢了”"),
        ("省略句", "“废寝食者”省略主语“其人”，即“（其人）废寝食者”；“终日在天中行止”省略主语“若”"),
        ("固定句式", "“奈……何”表询问，相当于“对……怎么办”：奈地坏何？；“奈何……乎”表反问，相当于“为什么……呢”：奈何忧崩坠乎？"),
        ("倒装句", "“身亡所寄”中“所寄”为“所”字结构，作“亡”的宾语，正常语序为“身无所寄”"),
    ]),
    ("文化常识", [
        ("《列子》", "道家经典之一，又名《冲虚真经》，旧题战国列御寇撰，今本可能为晋人张湛辑录。共八篇，保存了大量先秦寓言和神话传说，如《愚公移山》《夸父追日》《杞人忧天》等。"),
        ("列子", "名御寇，战国时期郑国人，道家学派代表人物之一。其学本于黄帝、老子，主张清静无为。唐玄宗时被封为“冲虚真人”，《列子》因此又称《冲虚真经》。"),
        ("杞国", "春秋时期诸侯国，姒姓，相传为夏禹后裔所建，在今河南杞县一带。公元前445年为楚所灭。“杞人忧天”的故事即发生于此，“杞人”后来成为无端忧虑者的代称。"),
        ("寓言", "文学作品的一种体裁，以比喻性的故事寄寓意味深长的道理。先秦诸子善用寓言说理，《列子》《庄子》《韩非子》等书中保存了大量经典寓言。寓言通常篇幅短小、寓意深刻，主人公可以是人，也可以是拟人化的动植物。"),
        ("天瑞", "《列子》第一篇，“天瑞”指天地间的祥瑞、自然现象。该篇主要论述宇宙万物的生成与变化，认为万物皆由“道”化生，包含多则寓言故事。《杞人忧天》即选自该篇。"),
    ]),
]

DICT_WORDS = [
    {"w":"杞","py":"qǐ","q":"□国有人忧天地崩坠","tip":"「杞」木字旁，古国名，读 qǐ；勿写「岂」「己」"},
    {"w":"坠","py":"zhuì","q":"天地崩□","tip":"「坠」土字底，坠落义，读 zhuì；勿写「堕」「队」"},
    {"w":"寝","py":"qǐn","q":"废□食者","tip":"「寝」宝盖头，睡觉义，读 qǐn；勿写「浸」「侵」"},
    {"w":"宿","py":"xiù","q":"日月星□","tip":"「宿」宝盖头，此处读 xiù（星辰义）；勿读 sù（住宿）"},
    {"w":"躇","py":"chú","q":"若□步跐蹈","tip":"「躇」足字旁，站立义，读 chú；勿写「著」「储」"},
    {"w":"跐","py":"cǐ","q":"若躇步□蹈","tip":"「跐」足字旁，踩踏义，读 cǐ；勿写「此」「疵」"},
    {"w":"舍","py":"shì","q":"其人□然大喜","tip":"「舍」此处通「释」，读 shì，消除义；勿读 shě（舍弃）"},
]

DICT_NOTES = [
    {"w":"杞国","a":"春秋诸侯国，在今河南杞县一带","q":"杞国有人忧天地崩坠"},
    {"w":"崩坠","a":"崩塌坠落。崩，倒塌；坠，坠落","q":"忧天地崩坠"},
    {"w":"身亡所寄","a":"自己没有地方存身。亡，同“无”；寄，依附、存身","q":"身亡所寄"},
    {"w":"废寝食","a":"睡不着觉，吃不下饭。废，停止","q":"废寝食者"},
    {"w":"忧彼之所忧","a":"为他的忧愁而担心。彼，他","q":"又有忧彼之所忧者"},
    {"w":"因","a":"于是，就","q":"因往晓之"},
    {"w":"晓之","a":"开导他。晓，开导；之，指杞人","q":"因往晓之"},
    {"w":"积气","a":"聚积的气体","q":"天，积气耳"},
    {"w":"耳","a":"语气词，相当于“罢了”","q":"天，积气耳"},
    {"w":"亡处亡气","a":"没有哪个地方没有气。亡，同“无”","q":"亡处亡气"},
    {"w":"若","a":"你","q":"若屈伸呼吸"},
    {"w":"屈伸","a":"指身体的弯曲和伸展，即一举一动","q":"若屈伸呼吸"},
    {"w":"行止","a":"行动和停留","q":"终日在天中行止"},
    {"w":"奈何","a":"为何，为什么","q":"奈何忧崩坠乎"},
    {"w":"果","a":"果然，果真","q":"天果积气"},
    {"w":"星宿","a":"星辰。宿，星的位次","q":"日月星宿"},
    {"w":"不当坠耶","a":"不应当掉下来吗？当，应当；耶，语气词","q":"不当坠耶"},
    {"w":"光耀","a":"发光","q":"亦积气中之有光耀者"},
    {"w":"只使","a":"即使，纵使","q":"只使坠"},
    {"w":"中伤","a":"伤害。中，击中","q":"亦不能有所中伤"},
    {"w":"奈……何","a":"固定句式，对……怎么办","q":"奈地坏何"},
    {"w":"积块","a":"聚积的土块。块，土块","q":"地，积块耳"},
    {"w":"充塞","a":"填满，塞满","q":"充塞四虚"},
    {"w":"四虚","a":"四方的虚空之处","q":"充塞四虚"},
    {"w":"躇步跐蹈","a":"泛指人的站立行走。躇，立；步，行；跐，踩；蹈，踏","q":"若躇步跐蹈"},
    {"w":"舍然","a":"消除疑虑的样子。舍，同“释”，解除","q":"其人舍然大喜"},
    {"w":"亦","a":"也","q":"晓之者亦舍然大喜"},
]

def make_media():
    items = []
    for i, (title, bv, t) in enumerate(MEDIA):
        fid = f"mediaF{i+1}"
        items.append(f'''<div class="media"><h4>{title}</h4><iframe id="{fid}" src="https://player.bilibili.com/player.html?bvid={bv}&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="{t}"></iframe><a href="https://www.bilibili.com/video/{bv}" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="{fid}">全屏播放</button></div>''')
    return "\n".join(items)

def make_bg():
    parts = ['<div class="lead">']
    for p in BG_LEAD:
        parts.append(f"<p>{p}</p>")
    parts.append("</div>")
    for title, paras in AUTHOR_BOX:
        parts.append(f'<div class="box"><h3>{title}</h3>')
        for p in paras:
            parts.append(f"<p>{p}</p>")
        parts.append("</div>")
    for title, paras in BG_BOX:
        parts.append(f'<div class="box"><h3>{title}</h3>')
        for p in paras:
            parts.append(f"<p>{p}</p>")
        parts.append("</div>")
    parts.append(f'<div class="box media-box"><h3>视听</h3><div class="media-grid">{make_media()}</div></div>')
    return "\n".join(parts)

def annotate(text, zhushi):
    result = text
    for word, note in sorted(zhushi, key=lambda x: -len(x[0])):
        if word in result:
            idx = result.index(word)
            before = result[:idx]
            if before.count('<span class="anno-word"') > before.count('</span>'):
                continue
            escaped_note = note.replace('"', '&quot;')
            replacement = f'<span class="anno-word" data-note="{escaped_note}">{word}</span>'
            result = result[:idx] + replacement + result[idx+len(word):]
    return result

def make_verses():
    parts = []
    for i, (orig, trans, appr, zhushi) in enumerate(VERSES):
        annotated = annotate(orig, zhushi)
        parts.append(f'''<div class="verse" id="l{i+1}" data-i="{i}">
  <div class="v-top"><span class="v-no">{i+1}</span><div class="v-line">{annotated}</div></div>
  <details class="v-more">
    <summary>译文 · 赏析</summary>
    <div class="d-body">
      <div class="v-sec"><b class="v-label">译　文</b>
        <div class="v-trans">{trans}</div>
      </div>
      <div class="v-sec"><b class="v-label">赏　析</b>
        <div class="d-body"><p>{appr}</p></div>
      </div>
    </div>
  </details>
</div>''')
    return "\n".join(parts)

def make_fulltext():
    parts = ['<div id="fulltext" class="poem" style="display:none">']
    for orig, _, _, _ in VERSES:
        parts.append(f'<div class="pl">{orig}</div>')
    parts.append("</div>")
    return "\n".join(parts)

def make_app():
    parts = []
    for title, items in APP_BOXES:
        parts.append(f'<div class="box"><h3>{title}</h3>')
        if title in ("人物形象", "艺术特色", "名句赏析"):
            parts.append('<div class="fame">')
            for sub, content in items:
                parts.append(f'<div class="fame-card"><div class="f-line">{sub}</div><p>{content}</p></div>')
            parts.append("</div>")
        else:
            for p in items:
                parts.append(f"<p>{p}</p>")
        parts.append("</div>")
    return "\n".join(parts)

def make_acc():
    parts = []
    for cat, items in ACC:
        parts.append(f'<div class="box"><div class="acc-cat"><h3>{cat}</h3>')
        for w, d in items:
            parts.append(f'<div class="acc-item"><span class="acc-w">{w}</span><span class="acc-d">{d}</span></div>')
        parts.append("</div></div>")
    return "\n".join(parts)

main_js = main_js.replace("chengtian_fs", LS_KEY)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{PAGE_TITLE}</title>
<style>
{css}
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">{HERO_SIDE}</div>
  <h1 class="hero-title">{HERO_TITLE}</h1>
</header>

<nav class="nav"><div class="nav-in"><a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a><div class="tool"><select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option></select><button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button></div></div></nav>

<main class="wrap">
<section id="bg" class="sec">
<div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
{make_bg()}
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>
<div class="sec-sub">全文分七句逐句解读。每句含注释、译文与赏析，点击可展开。</div>
<button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
{make_fulltext()}
<div class="verse-list" id="verseList">
{make_verses()}
</div></section>

<div class="divider"></div>
<section id="app" class="sec">
<div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>
{make_app()}
</section>

<div class="divider"></div>
<section id="acc" class="sec">
<div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 一词多义 · 活用 · 句式 · 文化常识</span></div>
{make_acc()}
</section>

<div class="divider"></div>
<section id="practice" class="sec">
<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>
<div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>
<div class="ptools"><button data-mode="word" data-rand="5">随机五组字形</button><button data-mode="word" data-all="1">全部字形</button><button data-mode="note" data-rand="5">随机五组注释</button><button data-mode="note" data-all="1">全部注释</button></div></section>

<footer>
  <div class="kai">《杞人忧天》</div>
  <div>列子 · 战国 · 选自《列子·天瑞》</div>
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
var DICT_WORDS = {json.dumps(DICT_WORDS, ensure_ascii=False)};
var DICT_NOTES = {json.dumps(DICT_NOTES, ensure_ascii=False)};
</script>

</body>
</html>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated: {OUT}")
print(f"Size: {os.path.getsize(OUT)} bytes")
