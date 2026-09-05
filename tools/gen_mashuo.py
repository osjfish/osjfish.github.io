# -*- coding: utf-8 -*-
"""《马说》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。
中文引号用 ~L~ / ~R~ 占位，生成前替换为 \\u201c / \\u201d。
拼音必须放在注释 data-note 里，原文保持纯净：[[词|（拼音）释义]]"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mashuo-hanyu.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'mashuo_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "世有伯乐，然后有千里马。",
    "千里马常有，而伯乐不常有。",
    "故虽有名马，祗辱于奴隶人之手，骈死于槽枥之间，不以千里称也。",
    "马之千里者，一食或尽粟一石。",
    "食马者不知其能千里而食也。",
    "是马也，虽有千里之能，食不饱，力不足，才美不外见，且欲与常马等不可得，安求其能千里也？",
    "策之不以其道，食之不能尽其材，鸣之而不能通其意，执策而临之，曰：~L~天下无马！~R~",
    "呜呼！其真无马邪？其真不知马也！",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "提出论点 · 伯乐难逢", "第 1–3 句",
     "开门见山提出~L~世有伯乐，然后有千里马~R~的论点，指出千里马被埋没的根本原因在于伯乐不常有，进而描写名马~L~祗辱于奴隶人之手，骈死于槽枥之间~R~的悲惨命运。"),
    ("第二部分", "分析原因 · 才美不外见", "第 4–6 句",
     "从千里马的食量与养马者的无知入手，分析千里马被埋没的具体原因——食不饱、力不足、才美不外见，连用反问，痛斥食马者的愚妄。"),
    ("第三部分", "痛斥讽喻 · 不知马也", "第 7–8 句",
     "以排比句痛斥食马者~L~策之不以其道，食之不能尽其材，鸣之而不能通其意~R~的荒唐，最后以~L~其真无马邪？其真不知马也~R~的感叹收束，点明主旨，余味无穷。"),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
(0, "[[世|世上，世间]]有[[伯乐|春秋时人，姓孙名阳，善相马，这里指善于识别人才的人]]，[[然后|这样以后，然后]]有[[千里马|能日行千里的马，这里指杰出的人才]]。",
 "世上有了伯乐，然后才会有千里马。",
 fixq("开门见山，提出全文论点。~L~世有伯乐，然后有千里马~R~——先有伯乐，后有千里马，强调伯乐对千里马的决定性作用。这句话表面说马，实则喻人：人才常有，但能识别人才的人不常有。开篇即立意高远，为全文奠定~L~借马喻人~R~的基调。"),
 ["论点", "托物寓意"]),

(0, "千里马[[常|常常，经常]]有，[[而|但是，连词，表转折]]伯乐不常有。",
 "千里马是经常有的，但是伯乐却不经常有。",
 fixq("承上句，进一步点明伯乐难逢的现实。~L~常有~R~与~L~不常有~R~对举，形成强烈反差——千里马并不稀缺，稀缺的是识马的伯乐。这一反差，正是人才被埋没的根源。~L~而~R~字表转折，见出作者的惋惜与愤慨。"),
 ["对比", "转折"]),

(0, "[[故|所以，因此]][[虽|即使]]有[[名马|名贵的马]]，[[祗|（zhǐ）通~L~只~R~，只是，仅仅]][[辱|受屈辱，被埋没]][[于|在，介词]][[奴隶人|奴仆，这里指马夫，养马的人]][[之|的，结构助词]][[手|手里，指手下]]，[[骈死|（pián）并列而死。骈，两马并驾，引申为并列]]于[[槽枥|（cáo lì）马槽。槽，喂牲口的食器；枥，马棚]]之间，不[[以|用，凭，介词]][[千里|指日行千里的本领]][[称|（chēng）著称，称呼]][[也|句末语气词，表陈述]]。",
 "所以即使有了名贵的马，也只是在马夫的手里受屈辱，和普通的马一同死在马厩里，不能凭借日行千里的本领而著称。",
 fixq("描写千里马被埋没的悲惨命运。~L~祗辱~R~~L~骈死~R~两个词，极写千里马的屈辱与不幸——它不是死于疆场，而是死于槽枥之间，与常马同死，连~L~千里~R~之名都不为人知。~L~奴隶人之手~R~与~L~槽枥之间~R~对举，见出千里马所处环境的恶劣。这一句是对人才被埋没现象的沉痛控诉。"),
 ["通假字", "描写", "控诉"]),

(1, "马[[之|定语后置的标志，无实义]]千里[[者|……的（马），定语后置的标志]]，[[一食|吃一顿。食，吃]][[或|有时]][[尽|（jìn）形容词作动词，吃尽，吃完]][[粟|（sù）小米，这里泛指粮食]][[一石|（dàn）一石（粮食）。石，容量单位，十斗为一石]]。",
 "日行千里的马，吃一顿有时能吃完一石粮食。",
 fixq("写千里马的食量之大，为下文~L~食不饱~R~蓄势。~L~马之千里者~R~是定语后置句，正常语序为~L~千里之马~R~。~L~一食或尽粟一石~R~以夸张的笔法写千里马的食量——它之所以能日行千里，是因为它的食量远超常马。这一句为下文分析千里马被埋没的原因埋下伏笔：食马者不知其能千里而食也。"),
 ["定语后置", "夸张", "伏笔"]),

(1, "[[食|（sì）通~L~饲~R~，喂养]]马[[者|……的人]][[不知|不懂得，不知道]][[其|它，代词，指千里马]][[能|能够，动词]]千里[[而|连词，表顺承，就]][[食|（sì）通~L~饲~R~，喂养]][[也|句末语气词，表陈述]]。",
 "喂马的人不懂得它能日行千里，（所以）不按照千里马的食量来喂养它。",
 fixq("点出千里马被埋没的直接原因——食马者的无知。两个~L~食~R~字都读 sì，通~L~饲~R~，是喂养的意思。~L~不知其能千里而食也~R~——食马者不知道这是千里马，自然不会按千里马的标准喂养它。这一句承上启下：上句写千里马的食量，此句写食马者的无知，下句便写由此导致的恶果。"),
 ["通假字", "承上启下"]),

(1, "[[是|这，这样的，指示代词]]马[[也|句中语气词，表停顿]]，[[虽|即使]]有千里[[之|的，结构助词]][[能|才能，能力，名词]]，[[食|吃，动词]]不饱，力不足，[[才美|才能和美好的素质]]不[[外见|（xiàn）不表现在外面。见，通~L~现~R~，表现，显现]]，[[且|犹，尚且]][[欲|想要]][[与|和，跟，介词]][[常马|普通的马]][[等|等同，一样]][[不可得|不能够得到，做不到]]，[[安|怎么，哪里，疑问代词]][[求|要求，苛求]][[其|它，代词]][[能|能够]]千里[[也|句末语气词，表反问]]？",
 "这样的马，即使有日行千里的才能，却吃不饱，力气不足，才能和美好的素质不能表现在外面，想要跟普通的马等同尚且做不到，又怎么能要求它日行千里呢？",
 fixq("分析千里马被埋没的恶果，连用~L~食不饱，力不足，才美不外见~R~三个短句，层层递进，把千里马的困境写得触目惊心。~L~且欲与常马等不可得，安求其能千里也~R~以反问收束，语气强烈——连普通马的水平都达不到，还谈什么日行千里？这一反问，既是对食马者无知的痛斥，也是对人才被埋没的深切同情。"),
 ["通假字", "反问", "层层递进"]),

(2, "[[策|（cè）名词作动词，用马鞭驱赶]][[之|它，代词，指千里马]]不[[以|按照，介词]][[其|它的，代词]][[道|正确的方法，这里指驱使千里马的正确方法]]，[[食|（sì）通~L~饲~R~，喂养]][[之|它]]不能[[尽|竭尽，使……竭尽，形容词的使动用法]][[其|它的]][[材|（cái）通~L~才~R~，才能，才干]]，[[鸣|（马）鸣叫]][[之|音节助词，无实义]][[而|连词，表转折，却]]不能[[通|通晓，懂得]][[其|它的]][[意|意思，心意]]，[[执|拿着，握着]][[策|马鞭，名词]][[而|连词，表修饰]][[临|面对，面对着]][[之|它]]，[[曰|说]]：~L~天下无马！~R~",
 "用马鞭驱赶它，不按照驱使千里马的正确方法；喂养它，不能使它竭尽才能；听它嘶鸣，却不能通晓它的意思。拿着马鞭面对着它，说：~L~天下没有千里马！~R~",
 fixq("全文最精彩的一段，以排比句痛斥食马者的愚妄。~L~策之不以其道，食之不能尽其材，鸣之而不能通其意~R~三句排比，从驱使、喂养、理解三个层面，写尽食马者的无知与荒唐。~L~执策而临之，曰：天下无马！~R~——一边糟蹋千里马，一边感叹天下无马，这一画面极具讽刺意味。食马者的荒唐，正是统治者不识人才、摧残人才的真实写照。"),
 ["排比", "通假字", "使动用法", "讽刺"]),

(2, "[[呜呼|（wū hū）叹词，相当于~L~唉~R~]]！[[其|表示反问语气，难道]][[真|真的，确实]]无马[[邪|（yé）通~L~耶~R~，句末语气词，表疑问或反问，相当于~L~吗~R~]]？[[其|表示推测语气，恐怕，大概]][[真|真的，确实]][[不知|不懂得，不认识]]马[[也|句末语气词，表感叹]]！",
 "唉！难道真的没有千里马吗？恐怕是真的不认识千里马啊！",
 fixq("全文收束句，以感叹与反问点明主旨。~L~其真无马邪？~R~是反问——天下并非没有千里马；~L~其真不知马也！~R~是感叹——问题在于食马者不认识千里马。两个~L~其~R~字，一表反问，一表推测，语气曲折有致。这一句把全文的愤慨推向高潮，也把~L~借马喻人~R~的主旨点明：不是天下无人才，而是统治者不识人才。"),
 ["通假字", "反问", "主旨句", "收束"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"祗","py":"zhǐ","q":"□辱于奴隶人之手","tip":fixq("「祗」示字旁，音 zhǐ，通~L~只~R~，意为只是，勿写~L~只~R~~L~抵~R~")},
    {"w":"骈","py":"pián","q":"□死于槽枥之间","tip":fixq("「骈」马字旁，音 pián，意为两马并驾，引申并列，勿写~L~拼~R~~L~便~R~")},
    {"w":"槽","py":"cáo","q":"骈死于□枥之间","tip":fixq("「槽」木字旁，音 cáo，意为喂牲口的食器，勿写~L~糟~R~~L~曹~R~")},
    {"w":"枥","py":"lì","q":"骈死于槽□之间","tip":fixq("「枥」木字旁，音 lì，意为马棚，勿写~L~历~R~~L~厉~R~")},
    {"w":"粟","py":"sù","q":"一食或尽□一石","tip":fixq("「粟」米字底，音 sù，意为小米，泛指粮食，勿写~L~栗~R~~L~票~R~")},
    {"w":"石","py":"dàn","q":"一食或尽粟一□","tip":fixq("「石」此处读 dàn（去声），容量单位，十斗为一石，勿读 shí")},
    {"w":"邪","py":"yé","q":"其真无马□","tip":fixq("「邪」此处读 yé，通~L~耶~R~，句末语气词，勿读 xié")},
    {"w":"策","py":"cè","q":"□之不以其道","tip":fixq("「策」竹字头，音 cè，意为马鞭，名词作动词，勿写~L~册~R~~L~测~R~")},
    {"w":"材","py":"cái","q":"食之不能尽其□","tip":fixq("「材」木字旁，音 cái，通~L~才~R~，意为才能，勿写~L~才~R~~L~财~R~")},
    {"w":"见","py":"xiàn","q":"才美不外□","tip":fixq("「见」此处读 xiàn，通~L~现~R~，意为表现，勿读 jiàn")},
    {"w":"食","py":"sì","q":"□之不能尽其材","tip":fixq("「食」此处读 sì，通~L~饲~R~，意为喂养，勿读 shí")},
    {"w":"辱","py":"rǔ","q":"祗□于奴隶人之手","tip":fixq("「辱」辰字底，音 rǔ，意为受屈辱，勿写~L~褥~R~~L~唇~R~")},
    {"w":"奴","py":"nú","q":"祗辱于□隶人之手","tip":fixq("「奴」女字旁，音 nú，意为奴仆，勿写~L~如~R~~L~努~R~")},
    {"w":"隶","py":"lì","q":"祗辱于奴□人之手","tip":fixq("「隶」独体字，音 lì，意为奴仆，附属，勿写~L~逮~R~~L~康~R~")},
    {"w":"称","py":"chēng","q":"不以千里□也","tip":fixq("「称」禾字旁，此处读 chēng，意为著称，勿读 chèn")},
    {"w":"鸣","py":"míng","q":"□之而不能通其意","tip":fixq("「鸣」口字旁，音 míng，意为（鸟/兽）叫，勿写~L~呜~R~~L~明~R~")},
    {"w":"执","py":"zhí","q":"□策而临之","tip":fixq("「执」提手旁，音 zhí，意为拿着，勿写~L~挚~R~~L~纨~R~")},
    {"w":"临","py":"lín","q":"执策而□之","tip":fixq("「临」丨字旁，音 lín，意为面对，勿写~L~监~R~~L~邻~R~")},
    {"w":"呜","py":"wū","q":"□呼！其真无马邪","tip":fixq("「呜」口字旁，音 wū，叹词，勿写~L~乌~R~~L~鸣~R~")},
    {"w":"呼","py":"hū","q":"呜□！其真无马邪","tip":fixq("「呼」口字旁，音 hū，叹词，勿写~L~乎~R~~L~忽~R~")},
    {"w":"伯","py":"bó","q":"世有□乐","tip":fixq("「伯」单人旁，音 bó，伯乐是善相马者，勿写~L~百~R~~L~柏~R~")},
    {"w":"乐","py":"lè","q":"世有伯□","tip":fixq("「乐」此处读 lè，伯乐是人名，勿读 yuè")},
    {"w":"尽","py":"jìn","q":"一食或□粟一石","tip":fixq("「尽」尸字头，音 jìn，形容词作动词~L~吃尽~R~，勿写~L~进~R~")},
    {"w":"通","py":"tōng","q":"鸣之而不能□其意","tip":fixq("「通」走之底，音 tōng，意为通晓，勿写~L~同~R~")},
    {"w":"意","py":"yì","q":"鸣之而不能通其□","tip":fixq("「意」心字底，音 yì，意为意思，心意，勿写~L~义~R~~L~易~R~")},
]

DICT_NOTES = [
    {"w":"世","q":"世有伯乐","a":"世上，世间"},
    {"w":"伯乐","q":"世有伯乐","a":"春秋时人，姓孙名阳，善相马，这里指善于识别人才的人"},
    {"w":"然后","q":"然后有千里马","a":"这样以后，然后"},
    {"w":"千里马","q":"然后有千里马","a":"能日行千里的马，这里指杰出的人才"},
    {"w":"常","q":"千里马常有","a":"常常，经常"},
    {"w":"而","q":"而伯乐不常有","a":"但是，连词，表转折"},
    {"w":"故","q":"故虽有名马","a":"所以，因此"},
    {"w":"虽","q":"故虽有名马","a":"即使"},
    {"w":"名马","q":"故虽有名马","a":"名贵的马"},
    {"w":"祗","q":"祗辱于奴隶人之手","a":"（zhǐ）通~L~只~R~，只是，仅仅"},
    {"w":"辱","q":"祗辱于奴隶人之手","a":"受屈辱，被埋没"},
    {"w":"于","q":"祗辱于奴隶人之手","a":"在，介词"},
    {"w":"奴隶人","q":"祗辱于奴隶人之手","a":"奴仆，这里指马夫，养马的人"},
    {"w":"之","q":"祗辱于奴隶人之手","a":"的，结构助词"},
    {"w":"手","q":"祗辱于奴隶人之手","a":"手里，指手下"},
    {"w":"骈死","q":"骈死于槽枥之间","a":"（pián）并列而死。骈，两马并驾，引申为并列"},
    {"w":"槽枥","q":"骈死于槽枥之间","a":"（cáo lì）马槽。槽，喂牲口的食器；枥，马棚"},
    {"w":"以","q":"不以千里称也","a":"用，凭，介词"},
    {"w":"千里","q":"不以千里称也","a":"指日行千里的本领"},
    {"w":"称","q":"不以千里称也","a":"（chēng）著称，称呼"},
    {"w":"也","q":"不以千里称也","a":"句末语气词，表陈述"},
    {"w":"之","q":"马之千里者","a":"定语后置的标志，无实义"},
    {"w":"者","q":"马之千里者","a":"……的（马），定语后置的标志"},
    {"w":"一食","q":"一食或尽粟一石","a":"吃一顿。食，吃"},
    {"w":"或","q":"一食或尽粟一石","a":"有时"},
    {"w":"尽","q":"一食或尽粟一石","a":"（jìn）形容词作动词，吃尽，吃完"},
    {"w":"粟","q":"一食或尽粟一石","a":"（sù）小米，这里泛指粮食"},
    {"w":"一石","q":"一食或尽粟一石","a":"（dàn）一石（粮食）。石，容量单位，十斗为一石"},
    {"w":"食","q":"食马者不知其能千里而食也","a":"（sì）通~L~饲~R~，喂养"},
    {"w":"者","q":"食马者不知其能千里而食也","a":"……的人"},
    {"w":"不知","q":"食马者不知其能千里而食也","a":"不懂得，不知道"},
    {"w":"其","q":"食马者不知其能千里而食也","a":"它，代词，指千里马"},
    {"w":"能","q":"食马者不知其能千里而食也","a":"能够，动词"},
    {"w":"而","q":"食马者不知其能千里而食也","a":"连词，表顺承，就"},
    {"w":"是","q":"是马也","a":"这，这样的，指示代词"},
    {"w":"也","q":"是马也","a":"句中语气词，表停顿"},
    {"w":"能","q":"虽有千里之能","a":"才能，能力，名词"},
    {"w":"食","q":"食不饱","a":"吃，动词"},
    {"w":"才美","q":"才美不外见","a":"才能和美好的素质"},
    {"w":"外见","q":"才美不外见","a":"（xiàn）不表现在外面。见，通~L~现~R~，表现，显现"},
    {"w":"且","q":"且欲与常马等不可得","a":"犹，尚且"},
    {"w":"欲","q":"且欲与常马等不可得","a":"想要"},
    {"w":"与","q":"且欲与常马等不可得","a":"和，跟，介词"},
    {"w":"常马","q":"且欲与常马等不可得","a":"普通的马"},
    {"w":"等","q":"且欲与常马等不可得","a":"等同，一样"},
    {"w":"不可得","q":"且欲与常马等不可得","a":"不能够得到，做不到"},
    {"w":"安","q":"安求其能千里也","a":"怎么，哪里，疑问代词"},
    {"w":"求","q":"安求其能千里也","a":"要求，苛求"},
    {"w":"策","q":"策之不以其道","a":"（cè）名词作动词，用马鞭驱赶"},
    {"w":"之","q":"策之不以其道","a":"它，代词，指千里马"},
    {"w":"以","q":"策之不以其道","a":"按照，介词"},
    {"w":"其","q":"策之不以其道","a":"它的，代词"},
    {"w":"道","q":"策之不以其道","a":"正确的方法，这里指驱使千里马的正确方法"},
    {"w":"食","q":"食之不能尽其材","a":"（sì）通~L~饲~R~，喂养"},
    {"w":"尽","q":"食之不能尽其材","a":"竭尽，使……竭尽，形容词的使动用法"},
    {"w":"材","q":"食之不能尽其材","a":"（cái）通~L~才~R~，才能，才干"},
    {"w":"鸣","q":"鸣之而不能通其意","a":"（马）鸣叫"},
    {"w":"之","q":"鸣之而不能通其意","a":"音节助词，无实义"},
    {"w":"而","q":"鸣之而不能通其意","a":"连词，表转折，却"},
    {"w":"通","q":"鸣之而不能通其意","a":"通晓，懂得"},
    {"w":"其","q":"鸣之而不能通其意","a":"它的"},
    {"w":"意","q":"鸣之而不能通其意","a":"意思，心意"},
    {"w":"执","q":"执策而临之","a":"拿着，握着"},
    {"w":"策","q":"执策而临之","a":"马鞭，名词"},
    {"w":"而","q":"执策而临之","a":"连词，表修饰"},
    {"w":"临","q":"执策而临之","a":"面对，面对着"},
    {"w":"之","q":"执策而临之","a":"它"},
    {"w":"曰","q":"曰：天下无马","a":"说"},
    {"w":"天下","q":"天下无马","a":"天底下，全天下"},
    {"w":"无马","q":"天下无马","a":"没有（千里）马"},
    {"w":"呜呼","q":"呜呼！其真无马邪","a":"（wū hū）叹词，相当于~L~唉~R~"},
    {"w":"其","q":"其真无马邪","a":"表示反问语气，难道"},
    {"w":"真","q":"其真无马邪","a":"真的，确实"},
    {"w":"邪","q":"其真无马邪","a":"（yé）通~L~耶~R~，句末语气词，表疑问或反问，相当于~L~吗~R~"},
    {"w":"其","q":"其真不知马也","a":"表示推测语气，恐怕，大概"},
    {"w":"不知","q":"其真不知马也","a":"不懂得，不认识"},
    {"w":"也","q":"其真不知马也","a":"句末语气词，表感叹"},
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
    <p>《马说》是唐代文学家韩愈的一篇托物寓意的杂文，全文约一百五十五字，以千里马为喻，深刻揭露了封建统治者不识人才、摧残人才的社会现象，抒发了作者怀才不遇的愤懑之情。</p>
    <p>文章短小精悍，论证严密，情感充沛，是中国古代议论文的经典之作，也是初中语文的重点篇目。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>韩愈（768—824），字退之，河南河阳（今河南孟州）人，世称~L~韩昌黎~R~，唐代著名文学家、思想家，古文运动的倡导者，~L~唐宋八大家~R~之首。贞元八年进士，官至吏部侍郎，卒谥~L~文~R~，故称~L~韩文公~R~。</p>
    <p>韩愈在文学上主张~L~文以载道~R~~L~文道合一~R~，反对六朝以来浮华的骈文，倡导质朴自由的古文，对后世散文发展影响深远。苏轼赞其~L~文起八代之衰，而道济天下之溺~R~。其散文气势磅礴，说理透彻，代表作有《师说》《进学解》《祭十二郎文》等。</p>
    <p class="note">※ 韩愈三岁而孤，由兄嫂抚养长大，早年仕途不顺，曾三试吏部而不中，对人才被埋没的现象有切身体会。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>写作缘起：</b>韩愈初入仕途时，曾三试吏部而不中，后又因直言进谏被贬阳山令。他一生仕途坎坷，对中唐时期统治者不识人才、摧残人才的现象有深切体会。《马说》大约作于贞元十一年至十六年（795—800）之间，正是韩愈仕途失意之时，借千里马的遭遇抒发自己怀才不遇的愤懑。</p>
    <p><b>中唐社会：</b>中唐时期，藩镇割据，宦官专权，朋党之争激烈，社会矛盾尖锐。统治者昏庸腐朽，大量有识之士得不到重用，人才被埋没的现象十分严重。韩愈以~L~千里马~R~喻人才，以~L~食马者~R~喻统治者，对这一社会现象进行了深刻的批判。</p>
    <p><b>古文运动：</b>韩愈倡导古文运动，主张文章应反映现实、表达思想。《马说》虽短，却论点鲜明、论证严密、情感充沛，是古文运动~L~文以载道~R~主张的典范之作。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>~L~说~R~是古代的一种议论文体，用以陈述作者对某个问题的见解，可以叙事，可以议论，可以抒情，写法较为自由。《马说》就是~L~说~R~体的典范之作，全文托物寓意，借千里马的遭遇表达作者对人才问题的见解。文章虽短，却包含了论点、论据、论证三个要素，结构完整，逻辑严密。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>诵读《马说》——不是没有人才，是你不识才</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1yd4y1k7qx&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="诵读《马说》"></iframe>
        <a href="https://www.bilibili.com/video/BV1yd4y1k7qx" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>央视频·唐宋八大家：原来《马说》是这么写出来的</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV13u4y1h7CL&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="唐宋八大家·马说"></iframe>
        <a href="https://www.bilibili.com/video/BV13u4y1h7CL" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>形象分析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">千里马——怀才不遇的人才</div>
        <p>文中的千里马，是杰出人才的化身。它有~L~一食或尽粟一石~R~的食量，有日行千里的才能，却因食马者的无知而~L~食不饱，力不足，才美不外见~R~，最终~L~祗辱于奴隶人之手，骈死于槽枥之间~R~。千里马的悲剧，正是封建社会中人才被埋没、被摧残的真实写照。它的遭遇令人同情，它的命运引人深思。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">食马者——愚妄浅薄的统治者</div>
        <p>文中的食马者，是昏庸统治者的化身。他~L~不知其能千里而食也~R~，~L~策之不以其道，食之不能尽其材，鸣之而不能通其意~R~，一边糟蹋千里马，一边~L~执策而临之，曰：天下无马！~R~食马者的无知与荒唐，正是封建统治者不识人才、摧残人才的真实写照。作者对食马者的批判，就是对统治者的批判。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">伯乐——善于识别人才的人</div>
        <p>伯乐在文中着墨不多，却是全文的关键。~L~世有伯乐，然后有千里马~R~——伯乐的存在，是千里马得以施展才能的前提。然而~L~伯乐不常有~R~，这正是千里马被埋没的根本原因。伯乐象征着能够识别人才、重用人才的贤明统治者，作者呼唤伯乐，就是呼唤统治者能够重视人才、善用人才。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">托物寓意，物我合一</div>
        <p>全文以千里马为喻，句句写马，又句句写人。千里马的~L~才美不外见~R~即人才的怀才不遇，食马者的~L~不知马~R~即统治者的不识人才，伯乐的~L~不常有~R~即贤明君主的稀缺。物与志高度统一，千里马的遭遇就是封建社会人才命运的缩影。托物寓意的手法，使文章既生动形象，又含蓄深刻。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">论点鲜明，论证严密</div>
        <p>文章开篇即提出论点~L~世有伯乐，然后有千里马~R~，然后从三个层面展开论证：一是~L~伯乐不常有~R~导致千里马被埋没（反面论证）；二是食马者的无知导致千里马~L~才美不外见~R~（因果论证）；三是食马者~L~不知马~R~却感叹~L~天下无马~R~（对比论证）。最后以~L~其真无马邪？其真不知马也~R~点明主旨，收束全文。全文虽短，却论点鲜明、论据充分、论证严密，是古代议论文的典范。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">排比反问，气势磅礴</div>
        <p>文章善用排比和反问，增强了语言的气势和感染力。~L~策之不以其道，食之不能尽其材，鸣之而不能通其意~R~三句排比，把食马者的无知写得淋漓尽致；~L~且欲与常马等不可得，安求其能千里也？~R~~L~其真无马邪？其真不知马也！~R~两个反问（感叹），把作者的愤慨推向高潮。排比与反问的交替使用，使文章气势磅礴，情感充沛，读来令人动容。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">短小精悍，言简意丰</div>
        <p>全文仅一百五十五字，却包含了论点、论据、论证三个要素，塑造了千里马、食马者、伯乐三个形象，表达了对人才问题的深刻见解。文章语言精炼，一字千金，如~L~祗辱~R~~L~骈死~R~等词，极写千里马的不幸；~L~不知~R~~L~不能~R~等词，极写食马者的无知。短小的篇幅中蕴含着丰富的内涵，是~L~以小见大~R~的典范。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">世有伯乐，然后有千里马。</div>
        <p>全文论点句，也是千古传诵的名句。这句话表面说马，实则喻人——先有识别人才的人，后有被识别的人才。它强调了伯乐对千里马的决定性作用，也暗示了人才被埋没的根源在于伯乐不常有。开篇即立意高远，为全文奠定~L~借马喻人~R~的基调，也使文章的论点一目了然。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">祗辱于奴隶人之手，骈死于槽枥之间。</div>
        <p>描写千里马悲惨命运的名句。~L~祗辱~R~写其受屈辱，~L~骈死~R~写其与常马同死，~L~奴隶人之手~R~~L~槽枥之间~R~写其所处环境的恶劣。两个~L~于~R~字，把千里马的不幸定格在两个具体的场景中，令人触目惊心。这一句是对人才被埋没现象的沉痛控诉，也是作者怀才不遇的真实写照。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">其真无马邪？其真不知马也！</div>
        <p>全文收束句，以反问与感叹点明主旨。~L~其真无马邪？~R~是反问——天下并非没有千里马；~L~其真不知马也！~R~是感叹——问题在于食马者不认识千里马。两个~L~其~R~字，一表反问，一表推测，语气曲折有致。这一句把全文的愤慨推向高潮，也把~L~借马喻人~R~的主旨点明：不是天下无人才，而是统治者不识人才。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《马说》通过对千里马被埋没、被摧残的遭遇的描写，揭露了封建统治者不识人才、摧残人才的社会现象，抒发了作者怀才不遇的愤懑之情，也表达了对统治者能够重视人才、善用人才的呼唤。</p>
    <p>文章的深刻之处，在于它不是简单地同情千里马的遭遇，而是通过千里马的悲剧，揭示了封建社会人才问题的根源——伯乐不常有，食马者不知马。作者以~L~其真无马邪？其真不知马也！~R~的感叹收束全文，把批判的矛头直指统治者的昏庸与无知，使文章的主题超越了个人的失意，具有普遍的社会意义。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 词类活用 · 句式 · 文化常识</span></div>

  <div class="box">
    <h3>通假字（本文核心考点）</h3>
    <div class="tw"><table>
      <tr><th>本字</th><th>通假</th><th>读音</th><th>例句</th><th>释义</th></tr>
      <tr><td class="kai">祗</td><td>通~L~只~R~</td><td>zhǐ</td><td>祗辱于奴隶人之手</td><td>只是，仅仅</td></tr>
      <tr><td class="kai">食</td><td>通~L~饲~R~</td><td>sì</td><td>食马者不知其能千里而食也</td><td>喂养</td></tr>
      <tr><td class="kai">见</td><td>通~L~现~R~</td><td>xiàn</td><td>才美不外见</td><td>表现，显现</td></tr>
      <tr><td class="kai">材</td><td>通~L~才~R~</td><td>cái</td><td>食之不能尽其材</td><td>才能，才干</td></tr>
      <tr><td class="kai">邪</td><td>通~L~耶~R~</td><td>yé</td><td>其真无马邪</td><td>句末语气词，表疑问/反问，相当于~L~吗~R~</td></tr>
    </table></div>
    <p class="note">※ 本文通假字密集，是核心考点。注意~L~食~R~字在文中有两种读音：读 shí 时意为~L~吃~R~（如~L~一食~R~~L~食不饱~R~），读 sì 时通~L~饲~R~意为~L~喂养~R~（如~L~食马者~R~~L~食之~R~）。</p>
  </div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">然后</td><td>这样以后</td><td>连词，表接着</td><td>然后有千里马</td></tr>
      <tr><td class="kai">奴隶</td><td>奴仆，这里指马夫</td><td>被剥削没有人身自由的人</td><td>祗辱于奴隶人之手</td></tr>
      <tr><td class="kai">一食</td><td>吃一顿</td><td>一顿饭</td><td>一食或尽粟一石</td></tr>
      <tr><td class="kai">或</td><td>有时</td><td>或者</td><td>一食或尽粟一石</td></tr>
      <tr><td class="kai">是</td><td>这，这样的</td><td>判断动词，是</td><td>是马也</td></tr>
      <tr><td class="kai">等</td><td>等同，一样</td><td>等待</td><td>且欲与常马等不可得</td></tr>
      <tr><td class="kai">安</td><td>怎么，哪里</td><td>安全，安定</td><td>安求其能千里也</td></tr>
      <tr><td class="kai">道</td><td>正确的方法</td><td>道路</td><td>策之不以其道</td></tr>
      <tr><td class="kai">临</td><td>面对，面对着</td><td>靠近，到达</td><td>执策而临之</td></tr>
      <tr><td class="kai">称</td><td>著称（读 chēng）</td><td>称呼；适合（读 chèn）</td><td>不以千里称也</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>词类活用</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">策</td><td>名词作动词</td><td>用马鞭驱赶</td><td>策之不以其道</td></tr>
      <tr><td class="kai">尽</td><td>形容词作动词（使动）</td><td>竭尽，使……竭尽</td><td>食之不能尽其材</td></tr>
      <tr><td class="kai">外</td><td>名词作状语</td><td>在外面</td><td>才美不外见</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">定语后置</td><td>马之千里者</td><td>~L~之……者~R~是定语后置的标志，正常语序为~L~千里之马~R~</td></tr>
      <tr><td class="kai">状语后置</td><td>祗辱于奴隶人之手</td><td>~L~于奴隶人之手~R~是状语，正常语序为~L~于奴隶人之手祗辱~R~</td></tr>
      <tr><td class="kai">状语后置</td><td>策之不以其道</td><td>~L~不以其道~R~是状语，正常语序为~L~不以其道策之~R~</td></tr>
      <tr><td class="kai">反问句</td><td>安求其能千里也？</td><td>~L~安~R~表反问，意为~L~怎么~R~</td></tr>
      <tr><td class="kai">反问句</td><td>其真无马邪？</td><td>~L~其……邪~R~表反问，意为~L~难道……吗~R~</td></tr>
      <tr><td class="kai">省略句</td><td>（食马者）执策而临之</td><td>承前省略主语~L~食马者~R~</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>一词多义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="4">食</td><td>吃，读 shí</td><td>一食或尽粟一石</td></tr>
      <tr><td>吃，读 shí</td><td>食不饱</td></tr>
      <tr><td>通~L~饲~R~，喂养，读 sì</td><td>食马者不知其能千里而食也</td></tr>
      <tr><td>通~L~饲~R~，喂养，读 sì</td><td>食之不能尽其材</td></tr>
      <tr><td class="kai" rowspan="2">策</td><td>名词作动词，用马鞭驱赶</td><td>策之不以其道</td></tr>
      <tr><td>马鞭，名词</td><td>执策而临之</td></tr>
      <tr><td class="kai" rowspan="2">能</td><td>能够，动词</td><td>不知其能千里而食也</td></tr>
      <tr><td>才能，能力，名词</td><td>虽有千里之能</td></tr>
      <tr><td class="kai" rowspan="3">其</td><td>它，代词（指千里马）</td><td>不知其能千里而食也</td></tr>
      <tr><td>表示反问语气，难道</td><td>其真无马邪</td></tr>
      <tr><td>表示推测语气，恐怕</td><td>其真不知马也</td></tr>
      <tr><td class="kai" rowspan="3">而</td><td>表转折，但是</td><td>而伯乐不常有</td></tr>
      <tr><td>表顺承，就</td><td>不知其能千里而食也</td></tr>
      <tr><td>表修饰</td><td>执策而临之</td></tr>
      <tr><td class="kai" rowspan="4">之</td><td>的，结构助词</td><td>奴隶人之手</td></tr>
      <tr><td>定语后置的标志</td><td>马之千里者</td></tr>
      <tr><td>它，代词（指千里马）</td><td>策之不以其道</td></tr>
      <tr><td>音节助词，无实义</td><td>鸣之而不能通其意</td></tr>
      <tr><td class="kai" rowspan="2">虽</td><td>即使</td><td>故虽有名马</td></tr>
      <tr><td>即使</td><td>虽有千里之能</td></tr>
      <tr><td class="kai" rowspan="2">以</td><td>用，凭，介词</td><td>不以千里称也</td></tr>
      <tr><td>按照，介词</td><td>策之不以其道</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>伯乐</dt><dd>春秋时人，姓孙名阳，善相马。传说伯乐在虞坂（今山西平陆）见一匹千里马拉盐车上太行，马伏地而鸣，伯乐下车而哭，马仰天长嘶。后以~L~伯乐~R~指善于识别人才的人。</dd></div>
      <div class="g-item"><dt>千里马</dt><dd>指能日行千里的骏马。古代有~L~千里马，一日而千里~R~的说法。文中以千里马喻杰出的人才。</dd></div>
      <div class="g-item"><dt>~L~说~R~文体</dt><dd>古代的一种议论文体，用以陈述作者对某个问题的见解，可以叙事、议论、抒情，写法自由。如《马说》《师说》《爱莲说》《捕蛇者说》等。</dd></div>
      <div class="g-item"><dt>唐宋八大家</dt><dd>指唐代韩愈、柳宗元和宋代欧阳修、苏洵、苏轼、苏辙、王安石、曾巩八位散文家。他们是古文运动的代表人物，其散文风格质朴自由，对后世影响深远。韩愈居八大家之首。</dd></div>
      <div class="g-item"><dt>古文运动</dt><dd>唐代中叶由韩愈、柳宗元倡导的散文革新运动，主张恢复先秦两汉的散文传统，反对六朝以来浮华的骈文，提倡~L~文以载道~R~~L~文道合一~R~。古文运动奠定了唐宋古文的基础，对后世散文发展影响深远。</dd></div>
      <div class="g-item"><dt>槽枥</dt><dd>马槽。槽，喂牲口的食器；枥，马棚。~L~骈死于槽枥之间~R~指千里马与普通马一同死在马厩里，比喻人才被埋没。</dd></div>
      <div class="g-item"><dt>一石</dt><dd>石（dàn），古代容量单位，十斗为一石。~L~一食或尽粟一石~R~以夸张的笔法写千里马的食量之大。</dd></div>
      <div class="g-item"><dt>托物寓意</dt><dd>通过对某一事物的描写，寄托作者的思想感情或见解的写作手法。《马说》是托物寓意的典范，借千里马的遭遇表达作者对人才问题的见解。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《马说》韩愈</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">唐 · 韩愈</div>
  <h1 class="hero-title">马说</h1>
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
  <div class="sec-sub">全文约一百五十五字，分三部分：提出论点、分析原因、痛斥讽喻。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《马说》</div>
  <div>韩愈 · 唐（768—824）· 字退之，世称韩昌黎，唐宋八大家之首</div>
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
