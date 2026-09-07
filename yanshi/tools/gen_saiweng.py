# -*- coding: utf-8 -*-
"""生成《塞翁失马》交互式教学课件"""
import json, os

BENCH = r"D:\App\Apps\yanshi\jichengtiansiyeyou-sushi.html"
OUT = r"D:\App\Apps\yanshi\saiwengshima-huainanzi.html"
LS_KEY = "saiweng_fs"

with open(BENCH, encoding="utf-8") as f:
    bench = f.read()

css = bench[bench.index("<style>")+7:bench.index("</style>")]
js_start = bench.index("<script>\n(function(){")
js_end = bench.index("</script>\n<script>\nvar DICT_WORDS")
main_js = bench[js_start+8:js_end]

HERO_SIDE = "西汉 · 刘安"
HERO_TITLE = "塞翁失马"
PAGE_TITLE = "《塞翁失马》刘安"

BG_LEAD = [
    "《塞翁失马》选自《淮南子·人间训》，是一则著名的寓言故事。文章通过边塞老翁失马、得马、儿子折髀、父子相保的故事，揭示了“祸兮福之所倚，福兮祸之所伏”的道理，阐明了祸福相依、事物在一定条件下可以相互转化的辩证思想。",
    "“塞翁失马，焉知非福”后来成为成语，比喻虽然一时受到损失，却可能因此得到好处，也指坏事在一定条件下可变为好事。这则寓言以极简的叙事，蕴含着深刻的辩证法思想，是中国古代寓言中的经典之作。"
]

AUTHOR_BOX = [
    ("刘安与《淮南子》", [
        "刘安（前179—前122），西汉沛县（今属江苏）人，汉高祖刘邦之孙，袭封淮南王。他好读书、善文辞，曾招集宾客方术之士数千人，集体编撰《淮南子》（又名《淮南鸿烈》）。",
        "《淮南子》共二十一篇，是西汉时期杂家的代表著作，以道家思想为主，糅合儒、法、阴阳等家学说，内容涉及哲学、政治、历史、自然科学等诸多方面。书中保存了大量神话传说和寓言故事，如《女娲补天》《后羿射日》《塞翁失马》等，想象丰富，寓意深刻。"
    ])
]

BG_BOX = [
    ("写作背景", [
        "<b>《人间训》：</b>本文选自《淮南子·人间训》。“人间”指人世间的吉凶祸福。该篇主要论述祸福、得失、利害的相互转化，包含多则寓言故事，《塞翁失马》是其中最著名的一则。",
        "<b>汉初思潮：</b>西汉初年，统治者吸取秦亡教训，推行黄老之学，主张清静无为、与民休息。《淮南子》以道家思想为主，强调事物的变化与转化，正是这一时代思潮的反映。“祸兮福之所倚，福兮祸之所伏”的辩证思想，在《塞翁失马》中得到了生动的体现。",
        "<b>边塞背景：</b>故事发生在“近塞”——靠近边塞的地方。西汉时期，北方匈奴经常侵扰边境，边塞战事频繁。“胡人大入塞，丁壮者引弦而战”的描写，正是汉代边塞生活的真实写照。在这样的背景下，“失马”“得马”“折髀”“相保”的祸福转化，更具现实意义。"
    ])
]

MEDIA = [
    ("《塞翁失马》诵读", "BV1hP4y1h7ur", "塞翁失马诵读"),
    ("成语故事《塞翁失马》动画", "BV1kM4y1g78t", "塞翁失马动画"),
]

VERSES = [
    (
        "近塞上之人有善术者，马无故亡而入胡。",
        "靠近边塞一带的人中，有一个精通术数的人，（他的）马无缘无故逃跑到了胡人的住地。",
        "开篇交代故事的地点、人物和起因。“近塞上”点明地点——靠近边塞，为后文“胡人大入塞”埋下伏笔。“善术者”点明人物身份——精通术数（占卜、预测）的人，暗示他能预见祸福转化。“马无故亡而入胡”是故事的起点——马丢了，而且跑到了胡人那里，在常人看来是祸事。一个“故”字，强调马的走失毫无缘由，更添不幸之感。",
        [
            ("近塞上", "靠近边塞。近，靠近；塞上，边塞、边疆"),
            ("善术者", "精通术数的人。善，擅长、精通；术，术数，指占卜、预测等；者，……的人"),
            ("无故", "没有缘故、没有原因。故，缘故、原因"),
            ("亡", "逃跑，走失"),
            ("入胡", "进入胡人的住地。胡，古代对北方少数民族的称呼"),
        ]
    ),
    (
        "人皆吊之，其父曰：“此何遽不为福乎？”",
        "人们都来安慰他，那个老人说：“这怎么就不能是福气呢？”",
        "“人皆吊之”写常人的反应——马丢了，大家都来安慰，说明在常人看来这确实是祸事。“其父曰”引出老翁的与众不同——他不悲反问：“此何遽不为福乎？”一个反问，石破天惊，道出了全文的核心思想：祸福相依，坏事可能变成好事。“何遽”是反问词，相当于“怎么就”，语气强烈，引人深思。这位“善术者”的见识，果然与众不同。",
        [
            ("皆", "都"),
            ("吊", "对遭遇不幸的人表示安慰，慰问"),
            ("其父", "那个老人。其，那；父，对老年人的尊称，这里指“善术者”"),
            ("此", "这，指马亡入胡这件事"),
            ("何遽", "怎么就，表示反问。遽，就"),
            ("为", "是，成为"),
            ("福", "福气，好事"),
            ("乎", "语气词，相当于“呢”"),
        ]
    ),
    (
        "居数月，其马将胡骏马而归。",
        "过了几个月，那匹马带着胡人的骏马回来了。",
        "故事的第一个转折——祸转为福。“居数月”交代时间，说明祸福转化需要时间，不是立竿见影的。“其马将胡骏马而归”写结果——不仅丢的马回来了，还带回了胡人的骏马，可谓因祸得福。“将”字用得精妙，写出马是主动带领骏马回来的，而非被驱赶回来，更添几分传奇色彩。这一转折，印证了老翁“此何遽不为福乎”的预言。",
        [
            ("居", "经过，过了"),
            ("数月", "几个月。数，几、几个"),
            ("将", "带领，率领"),
            ("胡骏马", "胡人的好马。骏马，好马、良马"),
            ("而归", "而回来。而，表顺承"),
        ]
    ),
    (
        "人皆贺之，其父曰：“此何遽不能为祸乎？”",
        "人们都来祝贺他，那个老人说：“这怎么就不能是灾祸呢？”",
        "故事的第二个转折——福中藏祸。“人皆贺之”写常人的反应——马带回了骏马，大家都来祝贺，说明在常人看来这是好事。“其父曰”再次引出老翁的与众不同——他不喜反忧：“此何遽不能为祸乎？”同样的反问，同样的辩证思维，只是这次是从福中看到祸。与前文“此何遽不为福乎”形成工整的对称，一福一祸，一正一反，把祸福相依的道理阐述得淋漓尽致。",
        [
            ("贺", "祝贺，庆贺"),
            ("不能为祸", "不能成为灾祸。为，成为；祸，灾祸、坏事"),
            ("乎", "语气词，相当于“呢”"),
        ]
    ),
    (
        "家富良马，其子好骑，堕而折其髀。",
        "家中有很多好马，他的儿子喜欢骑马，（有一次）从马上摔下来，摔断了大腿。",
        "故事的第三个转折——福转为祸。“家富良马”写条件——因为马多了，才有了骑马的条件。“其子好骑”写原因——儿子喜欢骑马，为事故埋下伏笔。“堕而折其髀”写结果——从马上摔下来，摔断了大腿。“髀”指大腿，是人体的重要部位，摔断大腿是严重的伤害。这一转折，印证了老翁“此何遽不能为祸乎”的预言。得马是福，好骑是因，折髀是祸——福中藏祸，因果分明。",
        [
            ("富", "多，丰富。这里指有很多"),
            ("良马", "好马。良，好"),
            ("好骑", "喜欢骑马。好，喜欢、爱好"),
            ("堕", "落下，掉下。这里指从马上摔下来"),
            ("而", "表顺承，于是、就"),
            ("折", "折断，摔断"),
            ("髀", "大腿"),
        ]
    ),
    (
        "人皆吊之，其父曰：“此何遽不为福乎？”",
        "人们都来安慰他，那个老人说：“这怎么就不能是福气呢？”",
        "故事的第四个转折——祸中藏福。“人皆吊之”写常人的反应——儿子摔断了腿，大家都来安慰。“其父曰”第三次引出老翁的反问：“此何遽不为福乎？”与第一次失马时的反问完全相同，形成回环往复之美。老翁三次反问，一次比一次深刻：失马问福、得马问祸、折髀问福——他始终能从常人看到的反面看到另一面。这种辩证思维，正是“善术者”的智慧所在。",
        [
            ("吊", "对遭遇不幸的人表示安慰，慰问"),
            ("此", "这，指儿子折髀这件事"),
            ("何遽", "怎么就，表示反问"),
            ("为福", "成为福气"),
            ("乎", "语气词，相当于“呢”"),
        ]
    ),
    (
        "居一年，胡人大入塞，丁壮者引弦而战。近塞之人，死者十九。",
        "过了一年，胡人大举入侵边塞，壮年男子都拿起弓箭去作战。靠近边塞的人，十个中有九个死了。",
        "故事的高潮——大祸降临。“居一年”交代时间。“胡人大入塞”写事件——胡人大举入侵，这是边塞最可怕的灾难。“丁壮者引弦而战”写应对——壮年男子都上了战场。“近塞之人，死者十九”写惨烈——十个中有九个死了，战争的残酷触目惊心。“十九”是“十分之九”的意思，极言死亡人数之多。在这样的大背景下，前面的“失马”“得马”“折髀”都显得微不足道，而老翁的预言也即将迎来最终的验证。",
        [
            ("居", "经过，过了"),
            ("大入塞", "大举入侵边塞。大，大规模、大举；入，入侵；塞，边塞"),
            ("丁壮者", "壮年男子。丁壮，壮年"),
            ("引弦", "拉开弓弦。引，拉；弦，弓弦"),
            ("而战", "而去作战。而，表顺承"),
            ("近塞之人", "靠近边塞的人"),
            ("死者十九", "死的人有十分之九。十九，十分之九，形容绝大多数"),
        ]
    ),
    (
        "此独以跛之故，父子相保。",
        "唯独这个人（的儿子）因为瘸腿的缘故，（没有上战场，）父子俩都保全了性命。",
        "故事的结局——祸转为福，最终的圆满。“此独以跛之故”点明原因——因为儿子摔断了腿，成了跛子，不能上战场。“跛”指瘸腿，正是前文“折其髀”的结果。“父子相保”写结果——父子俩都保全了性命。在“死者十九”的大背景下，“父子相保”显得尤为珍贵。折髀本是祸，却因此免役保命，转为福——老翁“此何遽不为福乎”的预言最终应验。全文至此，祸福四次转化，环环相扣，辩证思想得到了最生动的诠释。",
        [
            ("此", "这，指这个老人（的儿子）"),
            ("独", "唯独，只有"),
            ("以", "因为"),
            ("跛", "瘸腿，腿有毛病"),
            ("之故", "的缘故。故，缘故、原因"),
            ("相保", "互相保全，都保全了性命。保，保全"),
        ]
    ),
]

APP_BOXES = [
    ("人物形象", [
        ("睿智通达的塞翁", "塞翁是故事的核心人物，也是中国古代寓言中智者的典型。他“善术”——精通术数，能预见祸福转化。面对失马，他不悲；面对得马，他不喜；面对折髀，他不忧。三次“此何遽不为福乎/祸乎”的反问，展现了他超越常人的辩证思维和通达态度。他不是消极地听天由命，而是积极地看到事物的另一面，这种智慧正是道家“祸福相依”思想的体现。"),
        ("随波逐流的众人", "“人皆吊之”“人皆贺之”——众人的反应代表了常人的思维方式：看到表面的祸就悲，看到表面的福就喜，缺乏对事物深层转化的洞察。众人与塞翁形成鲜明对比，在对比中凸显了塞翁的睿智，也讽刺了常人的短视。"),
    ]),
    ("艺术特色", [
        ("叙事极简，一波四折", "全文仅一百余字，却有四次祸福转化：失马（祸）→得马（福）→折髀（祸）→相保（福）。四次转化环环相扣、层层递进，每一次转化都出人意料又在情理之中。叙事极简而情节曲折，是寓言文学的典范。"),
        ("对比鲜明，主旨突出", "善用对比：塞翁的通达与众人的短视对比；“人皆吊之”与“人皆贺之”对比；“死者十九”与“父子相保”对比。在对比中，祸福相依的主旨得到了有力的凸显。"),
        ("反复咏叹，回环往复", "塞翁三次反问，其中“此何遽不为福乎”出现两次，“此何遽不能为祸乎”出现一次。相同的句式在不同的情境中反复出现，形成回环往复之美，既强化了人物形象，也深化了主题思想。"),
        ("以小见大，寓意深刻", "以一个边塞家庭的得失祸福，揭示了宇宙间事物发展变化的普遍规律——矛盾双方在一定条件下可以相互转化。故事虽小，寓意却大，是“以小见大”写作手法的经典运用。"),
    ]),
    ("名句赏析", [
        ("此何遽不为福乎？", "塞翁的经典反问，也是全文的核心句。“何遽”是“怎么就”的意思，以反问语气表达肯定的意思——这可能就是福气。这句话出现在失马和折髀两个“祸”的情境中，每次都预示着祸将转福。它不仅是塞翁个人的智慧，更蕴含着深刻的辩证法思想：事物不是一成不变的，坏事在一定条件下可以变成好事。"),
        ("此何遽不能为祸乎？", "塞翁的另一句经典反问，与“此何遽不为福乎”形成对称。这句话出现在得马这个“福”的情境中，预示着福中将藏祸。它提醒人们：好事也可能变成坏事，不要被一时的幸运冲昏头脑。一福一祸，一正一反，两句反问合在一起，完整地表达了“祸兮福之所倚，福兮祸之所伏”的辩证思想。"),
        ("近塞之人，死者十九。此独以跛之故，父子相保。", "全文的高潮与结局。“死者十九”极写战争的残酷——十个中有九个死了；“父子相保”写塞翁一家的幸运——因为儿子跛腿免役，父子都保全了性命。在“十九”与“相保”的强烈对比中，祸福转化的主题得到了最震撼的体现。折髀本是祸，却因此免死，转为大福——塞翁的预言最终应验，全文的辩证思想也在此得到了最生动的诠释。"),
    ]),
    ("主题思想", [
        "本文通过记述边塞老翁失马、得马、儿子折髀、父子相保的故事，揭示了“祸兮福之所倚，福兮祸之所伏”的道理，阐明了祸福相依、事物在一定条件下可以相互转化的辩证思想。",
        "故事告诉我们：事物不是一成不变的，好事和坏事在一定条件下可以相互转化。因此，在顺境中不要得意忘形，在逆境中不要灰心丧气，要以辩证的眼光看待事物的发展变化。同时，塞翁的形象也体现了道家“清静无为”“顺其自然”的人生态度——不被一时的得失所左右，保持内心的平和与通达。",
        "当然，我们也应注意：祸福转化是有条件的，不能消极地等待“坏事变好事”，而应积极地创造条件，促使事物向有利的方向转化。这才是这则寓言给我们的真正启示。"
    ]),
]

ACC = [
    ("通假字", [
        ("（本文无通假字）", "《塞翁失马》全文无通假字。"),
    ]),
    ("古今异义", [
        ("术", "古义：术数，指占卜、预测等（善术者）；今义：技术、方法"),
        ("亡", "古义：逃跑、走失（马无故亡而入胡）；今义：死亡、灭亡"),
        ("吊", "古义：对遭遇不幸的人表示安慰（人皆吊之）；今义：悬挂、吊起"),
        ("父", "古义：对老年人的尊称（其父曰）；今义：父亲"),
        ("居", "古义：经过、过了（居数月）；今义：居住"),
        ("将", "古义：带领、率领（其马将胡骏马而归）；今义：将要、将军"),
        ("十九", "古义：十分之九（死者十九）；今义：数字十九"),
        ("相", "古义：互相（父子相保）；今义：相貌、互相（多义）"),
    ]),
    ("一词多义", [
        ("之", "代词，指塞翁：人皆吊之 / 结构助词，的：近塞上之人 / 代词，指马：人皆贺之"),
        ("其", "代词，他的：其父曰 / 代词，那：其马将胡骏马而归 / 代词，其中的：其人舍然大喜"),
        ("而", "表顺承：堕而折其髀 / 表修饰：引弦而战 / 表转折：人不知而不愠"),
        ("为", "是：此何遽不为福乎 / 成为：不能为祸乎 / 被：为天下笑"),
        ("以", "因为：此独以跛之故 / 用：以刀劈狼首 / 认为：皆以美于徐公"),
        ("故", "缘故、原因：马无故亡而入胡 / 所以：故君子有不战"),
        ("善", "擅长、精通：有善术者 / 好：善哉 / 友好：素善留侯张良"),
    ]),
    ("词类活用", [
        ("富", "形容词作动词，有很多、多。例：家富良马"),
        ("好", "形容词作动词，喜欢、爱好。例：其子好骑"),
    ]),
    ("文言句式", [
        ("省略句", "“马无故亡而入胡”省略定语“其”，即“（其）马无故亡而入胡”；“人皆吊之”省略介词“于”，即“人皆吊（于）之”"),
        ("反问句", "“此何遽不为福乎？”“此何遽不能为祸乎？”，“何遽……乎”表反问，相当于“怎么就……呢”"),
        ("被动句", "（本文无典型被动句）"),
        ("判断句", "（本文无典型判断句，以叙事为主）"),
    ]),
    ("文化常识", [
        ("《淮南子》", "西汉淮南王刘安招集宾客编撰，又名《淮南鸿烈》，共二十一篇。以道家思想为主，糅合儒、法、阴阳等家，是杂家代表著作。书中保存了大量神话传说和寓言故事。"),
        ("刘安", "（前179—前122），西汉沛县人，汉高祖刘邦之孙，袭封淮南王。好读书、善文辞，招集宾客数千人编撰《淮南子》。后因谋反事泄，自杀身亡。"),
        ("塞", "边塞、边疆，指靠近国界的险要地方。文中“近塞上”“大入塞”皆指北方边塞。西汉时期，北方匈奴经常侵扰边境，边塞战事频繁。"),
        ("胡", "古代对北方和西方少数民族的称呼。秦汉时主要指匈奴。文中“入胡”“胡骏马”“胡人大入塞”中的“胡”皆指匈奴。"),
        ("术数", "古代关于天文、历法、占卜、预测等的学问。“善术者”指精通术数、能预测吉凶的人。"),
        ("丁壮", "壮年男子。古代男子到了一定年龄要服兵役、劳役，称为“丁”。“丁壮者引弦而战”指壮年男子都上了战场。"),
        ("祸福相依", "道家的重要思想，语出《老子》：“祸兮福之所倚，福兮祸之所伏。”意思是祸中藏着福，福中藏着祸，二者在一定条件下可以相互转化。《塞翁失马》是这一思想最生动的寓言诠释。"),
    ]),
]

DICT_WORDS = [
    {"w":"遽","py":"jù","q":"此何□不为福乎","tip":"「遽」走之底，就义，读 jù；勿写「遂」「据」"},
    {"w":"髀","py":"bì","q":"堕而折其□","tip":"「髀」骨字旁，大腿义，读 bì；勿写「脾」「碑」"},
    {"w":"跛","py":"bǒ","q":"此独以□之故","tip":"「跛」足字旁，瘸腿义，读 bǒ；勿写「破」「坡」"},
    {"w":"堕","py":"duò","q":"□而折其髀","tip":"「堕」土字底，落下义，读 duò；勿写「坠」「惰」"},
    {"w":"弦","py":"xián","q":"丁壮者引□而战","tip":"「弦」弓字旁，弓弦义，读 xián；勿写「玄」「炫」"},
    {"w":"塞","py":"sài","q":"近□上之人","tip":"「塞」此处读 sài（边塞义）；勿读 sāi（堵塞）或 sè（闭塞）"},
    {"w":"将","py":"jiāng","q":"其马□胡骏马而归","tip":"「将」此处读 jiāng（带领义）；勿读 jiàng（将领）"},
]

DICT_NOTES = [
    {"w":"近塞上","a":"靠近边塞。近，靠近；塞上，边塞","q":"近塞上之人有善术者"},
    {"w":"善术者","a":"精通术数的人。善，擅长；术，术数；者，……的人","q":"近塞上之人有善术者"},
    {"w":"无故","a":"没有缘故。故，缘故、原因","q":"马无故亡而入胡"},
    {"w":"亡","a":"逃跑，走失","q":"马无故亡而入胡"},
    {"w":"入胡","a":"进入胡人的住地。胡，古代对北方少数民族的称呼","q":"马无故亡而入胡"},
    {"w":"皆","a":"都","q":"人皆吊之"},
    {"w":"吊","a":"对遭遇不幸的人表示安慰，慰问","q":"人皆吊之"},
    {"w":"其父","a":"那个老人。其，那；父，对老年人的尊称","q":"其父曰"},
    {"w":"此","a":"这","q":"此何遽不为福乎"},
    {"w":"何遽","a":"怎么就，表示反问。遽，就","q":"此何遽不为福乎"},
    {"w":"为","a":"是，成为","q":"此何遽不为福乎"},
    {"w":"福","a":"福气，好事","q":"此何遽不为福乎"},
    {"w":"乎","a":"语气词，相当于“呢”","q":"此何遽不为福乎"},
    {"w":"居","a":"经过，过了","q":"居数月"},
    {"w":"将","a":"带领，率领","q":"其马将胡骏马而归"},
    {"w":"胡骏马","a":"胡人的好马。骏马，好马","q":"其马将胡骏马而归"},
    {"w":"贺","a":"祝贺，庆贺","q":"人皆贺之"},
    {"w":"不能为祸","a":"不能成为灾祸。为，成为；祸，灾祸","q":"此何遽不能为祸乎"},
    {"w":"富","a":"多，这里指有很多","q":"家富良马"},
    {"w":"良马","a":"好马。良，好","q":"家富良马"},
    {"w":"好骑","a":"喜欢骑马。好，喜欢","q":"其子好骑"},
    {"w":"堕","a":"落下，掉下，这里指从马上摔下来","q":"堕而折其髀"},
    {"w":"折","a":"折断，摔断","q":"堕而折其髀"},
    {"w":"髀","a":"大腿","q":"堕而折其髀"},
    {"w":"大入塞","a":"大举入侵边塞。大，大规模；入，入侵；塞，边塞","q":"胡人大入塞"},
    {"w":"丁壮者","a":"壮年男子。丁壮，壮年","q":"丁壮者引弦而战"},
    {"w":"引弦","a":"拉开弓弦。引，拉；弦，弓弦","q":"丁壮者引弦而战"},
    {"w":"死者十九","a":"死的人有十分之九。十九，十分之九","q":"近塞之人，死者十九"},
    {"w":"独","a":"唯独，只有","q":"此独以跛之故"},
    {"w":"以","a":"因为","q":"此独以跛之故"},
    {"w":"跛","a":"瘸腿，腿有毛病","q":"此独以跛之故"},
    {"w":"之故","a":"的缘故。故，缘故、原因","q":"此独以跛之故"},
    {"w":"相保","a":"互相保全，都保全了性命。保，保全","q":"父子相保"},
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
<div class="sec-sub">全文分八句逐句解读。每句含注释、译文与赏析，点击可展开。</div>
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
  <div class="kai">《塞翁失马》</div>
  <div>刘安 · 西汉（前179—前122）· 选自《淮南子·人间训》</div>
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
