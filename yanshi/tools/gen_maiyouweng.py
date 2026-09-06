# -*- coding: utf-8 -*-
"""《卖油翁》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maiyouweng-ouyangxiu.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'maiyouweng_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "陈康肃公善射，当世无双，公亦以此自矜。",
    "尝射于家圃，有卖油翁释担而立，睨之久而不去。",
    "见其发矢十中八九，但微颔之。",
    "康肃问曰：",
    "~L~汝亦知射乎？吾射不亦精乎？~R~",
    "翁曰：",
    "~L~无他，但手熟尔。~R~",
    "康肃忿然曰：",
    "~L~尔安敢轻吾射！~R~",
    "翁曰：",
    "~L~以我酌油知之。~R~",
    "乃取一葫芦置于地，以钱覆其口，徐以杓酌油沥之，自钱孔入，而钱不湿。",
    "因曰：",
    "~L~我亦无他，惟手熟尔。~R~",
    "康肃笑而遣之。",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "善射自矜 · 翁睨微颔", "第 1–3 句",
     "故事开端。陈尧咨善射，当世无双，以此自矜。尝射于家圃，卖油翁释担而立，睨之久而不去，见其发矢十中八九，但微颔之——以卖油翁的~L~睨~R~和~L~微颔~R~，暗示其对陈尧咨射技的不以为然，为下文对话蓄势。"),
    ("第二部分", "问答交锋 · 酌油献技", "第 4–15 句",
     "故事发展与结局。陈尧咨质问卖油翁~L~汝亦知射乎~R~，翁以~L~无他，但手熟尔~R~回应，激怒陈尧咨。翁以酌油示范——以钱覆葫芦口，杓酌油沥之，自钱孔入而钱不湿，以事实证明~L~手熟~R~的道理。陈尧咨最终~L~笑而遣之~R~，心服口服。"),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
(0, "[[陈康肃公|即陈尧咨，北宋人，字嘉谟，谥号康肃。公，对男子的尊称]] [[善射|擅长射箭。善，擅长、善于；射，射箭]]，[[当世|当代，当时]] [[无双|没有第二个，无人能比]]，公亦[[以|凭借，因为]][[此|这，指善射]][[自矜|（jīn）自夸。矜，夸耀、自夸]]。",
 "康肃公陈尧咨擅长射箭，当时世上没有第二个人能跟他相比，他也凭着这一点自夸。",
 fixq("开篇交代人物和背景。~L~善射~R~~L~当世无双~R~写陈尧咨射技之高超，~L~自矜~R~写其性格之骄傲。~L~亦~R~字见出他不仅射技好，而且以此为荣、颇为自得。这一句为全文奠定了人物性格基调——陈尧咨是一个有真本事但也骄傲自满的人，卖油翁的出现正是对他这份~L~自矜~R~的挑战。"),
 ["人物登场", "性格基调"]),

(0, "[[尝|曾经]][[射|射箭]]于[[家圃|（pǔ）家里（射箭的）园子。圃，园子]]，有卖油翁[[释担|放下担子。释，放下、释放；担，担子]]而[[立|站立]]，[[睨|（nì）斜着眼看，形容不在意的样子]]之[[久而|很久。久，长久；而，表修饰]]不[[去|离开]]。",
 "（他）曾在自家的园子里射箭，有个卖油的老翁放下担子站在那里，斜着眼看他，很久也不离开。",
 fixq("卖油翁登场。~L~释担而立~R~写其动作从容，~L~睨之~R~写其神态——斜着眼看，不是正眼相看，而是带着一种审视和不以为然。~L~久而不去~R~写他停留时间之长，说明他不是偶然路过，而是有意观察。一个~L~睨~R~字，活画出卖油翁沉着自信、不动声色的形象，也暗示了他对陈尧咨射技的真实态度。"),
 ["~L~睨~R~字", "神态描写"]),

(0, "见其[[发矢|（shǐ）射出箭。发，射出；矢，箭]]十中八九，[[但|只，只是]][[微颔|（hàn）微微点头。微，微微、稍微；颔，下巴，这里指点头]]之。",
 "（老翁）看到他射出的箭十支能中八九支，只是对他微微点头（表示略微赞许）。",
 fixq("~L~十中八九~R~写陈尧咨射技确实高超，~L~但微颔之~R~写卖油翁的反应——只是微微点头，没有大声喝彩，更没有惊叹。~L~但~R~字是关键：在常人看来~L~十中八九~R~已经非常了不起，但在卖油翁看来，这不过是~L~手熟~R~而已，不值得大惊小怪。~L~微颔~R~既是对射技的有限肯定，也是对~L~自矜~R~的含蓄否定，为下文~L~无他，但手熟尔~R~埋下伏笔。"),
 ["~L~但~R~字", "伏笔"]),

(1, "康肃问曰：",
 "陈尧咨问道：",
 fixq("简短过渡。卖油翁的~L~睨~R~和~L~微颔~R~终于引起了陈尧咨的注意——一个卖油老翁，竟敢如此轻视我的射技？于是质问。这一问，拉开了两人交锋的序幕。"),
 ["过渡", "交锋开始"]),

(1, "~L~[[汝|（rǔ）你，第二人称代词]]亦[[知|懂得，了解]]射乎？吾射不亦[[精|精湛，高明]]乎？~R~",
 "~L~你也懂得射箭吗？我的射箭技艺不也很精湛吗？~R~",
 fixq("陈尧咨的质问，连用两个反问，咄咄逼人。~L~汝亦知射乎~R~——你一个卖油的，也配谈射箭？语气中充满轻蔑。~L~吾射不亦精乎~R~——我的射技难道不高吗？语气中充满自负。两个~L~亦~R~字，见出陈尧咨的骄傲和对卖油翁的轻视。他以为自己的射技是~L~当世无双~R~的绝技，卖油翁的~L~微颔~R~是对他的冒犯。"),
 ["连用反问", "咄咄逼人"]),

(1, "翁曰：",
 "老翁说：",
 fixq("简短过渡。面对陈尧咨的质问，卖油翁不卑不亢，平静作答。"),
 ["过渡"]),

(1, "~L~[[无他|没有别的（奥妙）。无，没有；他，别的、其他]]，但手[[熟|熟练，娴熟]][[尔|同~L~耳~R~，相当于~L~罢了~R~，句末语气词，表限止]]。~R~",
 "~L~没有别的（奥妙），只是手法技艺熟练罢了。~R~",
 fixq("卖油翁的回答，仅七字，却石破天惊。~L~无他~R~否定了射技的神秘性，~L~但手熟尔~R~道出了本质——所谓高超技艺，不过是熟练而已。~L~但~R~~L~尔~R~两个限止词，把~L~当世无双~R~的射技贬为~L~手熟~R~，轻描淡写，却字字千钧。这句话既是对陈尧咨~L~自矜~R~的否定，也是全文主旨的第一次点题——熟能生巧。~L~尔~R~通~L~耳~R~，表限止语气，见出卖油翁的淡然与自信。"),
 ["主旨点题", "通假字", "七字千钧"]),

(1, "康肃[[忿然|（fèn）气愤的样子。忿，愤怒、气愤；然，……的样子]]曰：",
 "陈尧咨气愤地说：",
 fixq("~L~忿然~R~二字，写陈尧咨被激怒后的神态。卖油翁的~L~无他，但手熟尔~R~彻底戳破了他的骄傲——他引以为傲的~L~当世无双~R~的射技，在卖油翁看来不过是~L~手熟~R~而已，这让他无法接受。~L~忿然~R~与卖油翁的平静形成鲜明对比，见出两人修养和境界的差异。"),
 ["~L~忿然~R~", "对比"]),

(1, "~L~[[尔|你，第二人称代词]][[安|怎么，哪里，表反问]]敢[[轻|轻视，看轻]]吾射！~R~",
 "~L~你怎么敢轻视我射箭的本领！~R~",
 fixq("陈尧咨怒斥，~L~尔安敢轻吾射~R~——你怎么敢！~L~安~R~表反问，语气强烈；~L~轻~R~是形容词作动词，轻视。这句话充满了愤怒和傲慢，他无法容忍一个卖油翁对他的射技说三道四。但正是这份愤怒，反衬出卖油翁的从容——面对怒斥，卖油翁不慌不忙，要用事实说话。"),
 ["怒斥", "词类活用"]),

(1, "翁曰：",
 "老翁说：",
 fixq("简短过渡。面对怒斥，卖油翁依然平静——他要用行动证明自己的话。"),
 ["过渡"]),

(1, "~L~[[以|凭，靠，介词]]我[[酌油|（zhuó）倒油。酌，舀取，这里指倒油]]知之。~R~",
 "~L~凭我倒油（的经验）知道这个（道理）。~R~",
 fixq("卖油翁的回答，~L~以我酌油知之~R~——我不是凭空说的，我是凭自己倒油的经验知道的。这句话既回应了陈尧咨的质问，又引出了下文的酌油示范。~L~知之~R~的~L~之~R~指代~L~但手熟尔~R~的道理。卖油翁没有争辩，而是要用事实说话——这正是智者的做法：与其空谈道理，不如现身说法。"),
 ["以理服人", "引出示范"]),

(1, "[[乃|于是，就]]取一[[葫芦|古代盛物的器皿，这里指装油的葫芦]]置于地，[[以|用，拿，介词]]钱[[覆|覆盖，遮盖]]其口，[[徐|慢慢地，缓缓地]]以[[杓|（sháo）同~L~勺~R~，勺子]]酌油[[沥|（lì）下滴，滴入]]之，自钱孔入，而钱不湿。",
 "（老翁）于是取出一个葫芦放在地上，用一枚铜钱盖住葫芦口，慢慢地用勺子倒油（通过铜钱方孔）滴入葫芦，油从铜钱的孔中注入，但铜钱却没有被沾湿。",
 fixq("全文最精彩的描写。~L~乃取~R~~L~置~R~~L~覆~R~~L~酌~R~~L~沥~R~，一连串动词，写卖油翁酌油的全过程，动作从容不迫。~L~徐~R~字写其速度之慢——慢才能稳，稳才能准。~L~自钱孔入，而钱不湿~R~是结果，也是高潮：油从铜钱的方孔中注入，铜钱却丝毫未湿，这需要何等精准的手法！卖油翁以这一绝技，无声地证明了~L~但手熟尔~R~的道理——射箭如此，倒油亦如此，一切高超技艺皆源于熟练。"),
 ["动作描写", "高潮", "~L~徐~R~字"]),

(1, "[[因|于是，接着]]曰：",
 "（老翁）接着说：",
 fixq("简短过渡。酌油示范完毕，卖油翁再次点题。"),
 ["过渡"]),

(1, "~L~我亦无他，[[惟|只，只是]]手熟尔。~R~",
 "~L~我也没有别的（奥妙），只是手法熟练罢了。~R~",
 fixq("卖油翁再次点题，~L~我亦无他，惟手熟尔~R~——与上文~L~无他，但手熟尔~R~呼应，但多了一个~L~亦~R~字：你射箭是手熟，我倒油也是手熟，道理是一样的。~L~惟~R~与~L~但~R~同义，都是~L~只~R~的意思。这句话以自己的亲身实践印证了前面的道理，比空口说白话更有说服力。两次~L~手熟尔~R~，一虚一实，一答一证，把~L~熟能生巧~R~的主旨表达得淋漓尽致。"),
 ["呼应前文", "主旨升华", "一虚一实"]),

(1, "康肃[[笑而遣之|笑着把他打发走了。笑，尴尬地笑；而，表修饰；遣，打发、送走；之，代词，指卖油翁]]。",
 "陈尧咨笑着把他打发走了。",
 fixq("故事结局。~L~笑而遣之~R~，一个~L~笑~R~字，意味深长——这不是开心的笑，而是尴尬的笑、释然的笑、心服口服的笑。陈尧咨终于明白了卖油翁的道理，也认识到了自己的~L~自矜~R~是可笑的。~L~遣之~R~写他把卖油翁送走，没有道歉，没有拜师，但~L~笑~R~已经说明了一切。以~L~笑~R~收束全文，含蓄而有余味——骄傲者被现实教育后，只能以笑解嘲。"),
 ["结局", "~L~笑~R~字", "含蓄收束"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"矜","py":"jīn","q":"公亦以此自□","tip":fixq("「矜」矛字旁，音 jīn，意为夸耀，勿写~L~今~R~~L~衿~R~")},
    {"w":"圃","py":"pǔ","q":"尝射于家□","tip":fixq("「圃」口字框，音 pǔ，意为园子，勿写~L~浦~R~~L~蒲~R~")},
    {"w":"睨","py":"nì","q":"□之久而不去","tip":fixq("「睨」目字旁，音 nì，意为斜着眼看，勿写~L~倪~R~~L~霓~R~")},
    {"w":"矢","py":"shǐ","q":"见其发□十中八九","tip":fixq("「矢」独体字，音 shǐ，意为箭，勿写~L~失~R~~L~史~R~")},
    {"w":"颔","py":"hàn","q":"但微□之","tip":fixq("「颔」页字旁，音 hàn，意为点头，勿写~L~含~R~~L~函~R~")},
    {"w":"忿","py":"fèn","q":"康肃□然曰","tip":fixq("「忿」心字底，音 fèn，意为愤怒，勿写~L~愤~R~~L~分~R~")},
    {"w":"酌","py":"zhuó","q":"以我□油知之","tip":fixq("「酌」酉字旁，音 zhuó，意为舀取、倒，勿写~L~灼~R~~L~勺~R~")},
    {"w":"杓","py":"sháo","q":"徐以□酌油沥之","tip":fixq("「杓」木字旁，音 sháo，同~L~勺~R~，勿写~L~标~R~~L~钓~R~")},
    {"w":"沥","py":"lì","q":"徐以杓酌油□之","tip":fixq("「沥」三点水，音 lì，意为下滴，勿写~L~历~R~~L~厉~R~")},
    {"w":"覆","py":"fù","q":"以钱□其口","tip":fixq("「覆」西字头，音 fù，意为覆盖，勿写~L~复~R~~L~腹~R~")},
    {"w":"遣","py":"qiǎn","q":"康肃笑而□之","tip":fixq("「遣」走之底，音 qiǎn，意为打发，勿写~L~遗~R~~L~谴~R~")},
    {"w":"汝","py":"rǔ","q":"□亦知射乎","tip":fixq("「汝」三点水，音 rǔ，意为你，勿写~L~女~R~~L~如~R~")},
    {"w":"精","py":"jīng","q":"吾射不亦□乎","tip":fixq("「精」米字旁，音 jīng，意为精湛，勿写~L~睛~R~~L~清~R~")},
    {"w":"熟","py":"shú","q":"但手□尔","tip":fixq("「熟」四点底，音 shú，意为熟练，勿写~L~孰~R~~L~塾~R~")},
    {"w":"葫芦","py":"hú lu","q":"乃取一□□置于地","tip":fixq("「葫」草字头音 hú，「芦」草字头音 lu，指盛油的器皿")},
    {"w":"善射","py":"shàn shè","q":"陈康肃公□□","tip":fixq("「善」口字底音 shàn，「射」身字旁音 shè，意为擅长射箭")},
    {"w":"自矜","py":"zì jīn","q":"公亦以此□□","tip":fixq("「自」独体字音 zì，「矜」矛字旁音 jīn，意为自夸")},
    {"w":"释担","py":"shì dàn","q":"有卖油翁□□而立","tip":fixq("「释」采字旁音 shì，「担」提手旁音 dàn，意为放下担子")},
    {"w":"微颔","py":"wēi hàn","q":"但□□之","tip":fixq("「微」彳旁音 wēi，「颔」页字旁音 hàn，意为微微点头")},
    {"w":"忿然","py":"fèn rán","q":"康肃□□曰","tip":fixq("「忿」心字底音 fèn，「然」四点底音 rán，意为气愤的样子")},
]

DICT_NOTES = [
    {"w":"陈康肃公","q":"陈康肃公善射","a":"即陈尧咨，北宋人，字嘉谟，谥号康肃。公，对男子的尊称"},
    {"w":"善射","q":"陈康肃公善射","a":"擅长射箭。善，擅长、善于；射，射箭"},
    {"w":"当世","q":"当世无双","a":"当代，当时"},
    {"w":"无双","q":"当世无双","a":"没有第二个，无人能比"},
    {"w":"以","q":"公亦以此自矜","a":"凭借，因为"},
    {"w":"此","q":"公亦以此自矜","a":"这，指善射"},
    {"w":"自矜","q":"公亦以此自矜","a":"（jīn）自夸。矜，夸耀、自夸"},
    {"w":"尝","q":"尝射于家圃","a":"曾经"},
    {"w":"家圃","q":"尝射于家圃","a":"（pǔ）家里（射箭的）园子。圃，园子"},
    {"w":"释担","q":"有卖油翁释担而立","a":"放下担子。释，放下、释放；担，担子"},
    {"w":"睨","q":"睨之久而不去","a":"（nì）斜着眼看，形容不在意的样子"},
    {"w":"久而","q":"睨之久而不去","a":"很久。久，长久；而，表修饰"},
    {"w":"去","q":"睨之久而不去","a":"离开"},
    {"w":"发矢","q":"见其发矢十中八九","a":"（shǐ）射出箭。发，射出；矢，箭"},
    {"w":"但","q":"但微颔之","a":"只，只是"},
    {"w":"微颔","q":"但微颔之","a":"（hàn）微微点头。微，微微；颔，下巴，这里指点头"},
    {"w":"汝","q":"汝亦知射乎","a":"（rǔ）你，第二人称代词"},
    {"w":"知","q":"汝亦知射乎","a":"懂得，了解"},
    {"w":"精","q":"吾射不亦精乎","a":"精湛，高明"},
    {"w":"无他","q":"无他，但手熟尔","a":"没有别的（奥妙）。无，没有；他，别的、其他"},
    {"w":"熟","q":"但手熟尔","a":"熟练，娴熟"},
    {"w":"尔","q":"但手熟尔","a":"同~L~耳~R~，相当于~L~罢了~R~，句末语气词，表限止"},
    {"w":"忿然","q":"康肃忿然曰","a":"（fèn）气愤的样子。忿，愤怒；然，……的样子"},
    {"w":"尔","q":"尔安敢轻吾射","a":"你，第二人称代词"},
    {"w":"安","q":"尔安敢轻吾射","a":"怎么，哪里，表反问"},
    {"w":"轻","q":"尔安敢轻吾射","a":"轻视，看轻，形容词作动词"},
    {"w":"以","q":"以我酌油知之","a":"凭，靠，介词"},
    {"w":"酌油","q":"以我酌油知之","a":"（zhuó）倒油。酌，舀取，这里指倒油"},
    {"w":"之","q":"以我酌油知之","a":"代词，指~L~但手熟尔~R~的道理"},
    {"w":"乃","q":"乃取一葫芦置于地","a":"于是，就"},
    {"w":"葫芦","q":"乃取一葫芦置于地","a":"古代盛物的器皿，这里指装油的葫芦"},
    {"w":"置","q":"乃取一葫芦置于地","a":"放，放置"},
    {"w":"以","q":"以钱覆其口","a":"用，拿，介词"},
    {"w":"覆","q":"以钱覆其口","a":"覆盖，遮盖"},
    {"w":"徐","q":"徐以杓酌油沥之","a":"慢慢地，缓缓地"},
    {"w":"杓","q":"徐以杓酌油沥之","a":"（sháo）同~L~勺~R~，勺子"},
    {"w":"沥","q":"徐以杓酌油沥之","a":"（lì）下滴，滴入"},
    {"w":"自","q":"自钱孔入","a":"从，介词"},
    {"w":"而","q":"而钱不湿","a":"但是，却，表转折"},
    {"w":"因","q":"因曰","a":"于是，接着"},
    {"w":"惟","q":"惟手熟尔","a":"只，只是"},
    {"w":"笑而遣之","q":"康肃笑而遣之","a":"笑着把他打发走了。笑，尴尬地笑；遣，打发、送走"},
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
full_html = '\n'.join('    <div class="pl">%s</div>' % fixq(p) for p in FULLTEXT)

anno_count = sum(txt.count('[[') for (_, txt, _, _, _) in S)

BG = fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《卖油翁》是北宋文学家欧阳修的一篇文言笔记小说，选自《归田录》。文章通过陈尧咨善射自矜、卖油翁以酌油示范~L~手熟~R~道理的故事，阐明了~L~熟能生巧~R~的深刻哲理，也讽刺了那些有一技之长便骄傲自满的人。</p>
    <p>全文仅一百三十余字，却叙事生动、对话精彩、人物鲜明、哲理深刻，是中国古代笔记小说中的经典之作，也是初中语文的传统篇目。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>欧阳修（1007—1072），字永叔，号醉翁，晚号六一居士，吉州永丰（今江西吉安）人，北宋著名政治家、文学家、史学家，~L~唐宋八大家~R~之一。天圣八年进士，官至枢密副使、参知政事。死后谥号文忠，世称欧阳文忠公。</p>
    <p>欧阳修是北宋诗文革新运动的领袖，主张文章应~L~明道~R~~L~致用~R~，反对浮靡文风。他的散文说理畅达、抒情委婉，~L~三苏~R~、王安石、曾巩等皆出其门下。代表作有《醉翁亭记》《秋声赋》《朋党论》等，史学著作有《新五代史》《新唐书》（与宋祁合修）。</p>
    <p class="note">※ 欧阳修自称~L~六一居士~R~：吾家藏书一万卷，集录三代以来金石遗文一千卷，有琴一张，有棋一局，而常置酒一壶，以吾一翁老于此五物之间，是岂不为六一乎？</p>
  </div>
  <div class="box">
    <h3>创作背景</h3>
    <p><b>《归田录》：</b>欧阳修晚年辞官归隐后所作的笔记集，共二卷，多记朝廷轶事、士大夫趣闻，文笔简约生动。《卖油翁》即选自其中，是一篇寓理于事的小品文。</p>
    <p><b>写作意图：</b>欧阳修在《归田录》中常借小故事阐发人生哲理。《卖油翁》通过陈尧咨与卖油翁的对比，说明~L~熟能生巧~R~的道理——任何高超的技艺都不是天生的，而是长期练习的结果；同时也告诫人们，即使有一技之长，也不应骄傲自满。</p>
    <p><b>历史人物：</b>文中的~L~陈康肃公~R~即陈尧咨（970—1034），北宋人，字嘉谟，咸平三年状元，官至武信军节度使，谥号康肃。他以善射著称，传说其射技精湛，有~L~小由基~R~之称。欧阳修在文中借真实人物虚构故事，增强了文章的真实感和说服力。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>本文是一篇笔记小说（小品文），以短小的篇幅、生动的对话、鲜明的人物和深刻的哲理见长。笔记小说是中国古代散文的重要体裁，多记录轶事趣闻，篇幅短小，文笔简约。《卖油翁》是笔记小说中~L~寓理于事~R~的典范——故事是手段，说理是目的，事与理浑然一体。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>诵读经典：《卖油翁》欧阳修</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1uZ4y167pQ&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="诵读经典《卖油翁》"></iframe>
        <a href="https://www.bilibili.com/video/BV1uZ4y167pQ" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>AI翻拍演绎：《卖油翁》一勺油穿钱而过</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1cVNG6DEgq&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="AI翻拍《卖油翁》"></iframe>
        <a href="https://www.bilibili.com/video/BV1cVNG6DEgq" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">陈尧咨：有真才而骄傲自满</div>
        <p>陈尧咨是一个有真本事但骄傲自满的人。~L~善射，当世无双~R~写其射技确实高超，~L~自矜~R~写其性格骄傲。面对卖油翁的~L~微颔~R~，他连用两个反问质问，~L~汝亦知射乎？吾射不亦精乎？~R~咄咄逼人；听到~L~无他，但手熟尔~R~后，更是~L~忿然~R~怒斥~L~尔安敢轻吾射~R~。但在卖油翁酌油示范后，他最终~L~笑而遣之~R~——这个~L~笑~R~是尴尬的笑、释然的笑，说明他内心已经服气。陈尧咨的形象真实可感：有才能但也有缺点，被现实教育后能有所醒悟。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">卖油翁：沉着从容的智者</div>
        <p>卖油翁是一位沉着从容、大智若愚的智者。他~L~释担而立，睨之久而不去~R~，一个~L~睨~R~字见出其对陈尧咨射技的不以为然；面对质问，他平静回答~L~无他，但手熟尔~R~；面对怒斥，他不慌不忙~L~以我酌油知之~R~，然后以~L~自钱孔入，而钱不湿~R~的绝技证明了自己的话。他不卑不亢、以理服人、以技服人，是~L~熟能生巧~R~道理的化身。卖油翁的形象告诉我们：真正有本事的人，往往是最谦虚的人。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">寓理于事，以小见大</div>
        <p>文章通过卖油翁酌油这一小事，阐明了~L~熟能生巧~R~的大道理。叙事是手段，说理是目的，事与理高度统一。卖油翁的~L~酌油~R~和陈尧咨的~L~射箭~R~，看似毫不相干，本质却相同——都是~L~手熟~R~的结果。文章以小见大，从日常生活的小事中提炼出深刻的哲理，令人信服。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比鲜明，人物生动</div>
        <p>文章通篇运用对比：陈尧咨的~L~自矜~R~与卖油翁的~L~淡然~R~对比，陈尧咨的~L~忿然~R~与卖油翁的~L~从容~R~对比，~L~当世无双~R~的射技与~L~手熟尔~R~的评价对比，射箭与酌油两种技艺对比。对比之中，人物性格跃然纸上，文章主旨自然凸显。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对话精彩，言简意丰</div>
        <p>全文以对话推动情节，每个人的话都符合其身份性格。陈尧咨的话咄咄逼人、充满傲慢；卖油翁的话平静淡然、蕴含哲理。~L~无他，但手熟尔~R~仅七字，却石破天惊；~L~我亦无他，惟手熟尔~R~与前文呼应，一虚一实，把道理说透。对话不仅推动了情节，更塑造了人物，可谓~L~言简意丰~R~。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">细节传神，炼字精当</div>
        <p>文章的细节描写极为传神：~L~睨~R~写卖油翁的神态，~L~微颔~R~写其反应，~L~忿然~R~写陈尧咨的愤怒，~L~徐~R~写酌油的从容，~L~笑~R~写结局的释然。每一个字都经过锤炼，准确而生动。尤其是~L~睨~R~~L~颔~R~~L~忿~R~~L~遣~R~等字，以极简的笔墨写出极丰富的人物心理，是炼字的典范。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">无他，但手熟尔。</div>
        <p>全文的文眼和主旨句。仅七字，却石破天惊——把陈尧咨引以为傲的~L~当世无双~R~的射技，贬为~L~手熟~R~而已。~L~无他~R~否定了射技的神秘性，~L~但手熟尔~R~道出了本质：所谓高超技艺，不过是熟练而已。~L~但~R~~L~尔~R~两个限止词，轻描淡写，却字字千钧。这句话既是对陈尧咨~L~自矜~R~的否定，也是~L~熟能生巧~R~哲理的第一次点题。后来~L~熟能生巧~R~成为成语，广为流传。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">乃取一葫芦置于地，以钱覆其口，徐以杓酌油沥之，自钱孔入，而钱不湿。</div>
        <p>全文最精彩的动作描写。~L~取~R~~L~置~R~~L~覆~R~~L~酌~R~~L~沥~R~，一连串动词，写卖油翁酌油的全过程，动作从容不迫。~L~徐~R~字写其速度之慢——慢才能稳，稳才能准。~L~自钱孔入，而钱不湿~R~是结果，也是高潮：油从铜钱的方孔中注入，铜钱却丝毫未湿，这需要何等精准的手法！卖油翁以这一绝技，无声地证明了~L~但手熟尔~R~的道理。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">康肃笑而遣之。</div>
        <p>故事结局，仅六字却意味深长。~L~笑~R~字是关键——这不是开心的笑，而是尴尬的笑、释然的笑、心服口服的笑。陈尧咨终于明白了卖油翁的道理，也认识到了自己的~L~自矜~R~是可笑的。~L~遣之~R~写他把卖油翁送走，没有道歉，没有拜师，但~L~笑~R~已经说明了一切。以~L~笑~R~收束全文，含蓄而有余味——骄傲者被现实教育后，只能以笑解嘲。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《卖油翁》通过陈尧咨善射自矜、卖油翁以酌油示范~L~手熟~R~道理的故事，阐明了~L~熟能生巧~R~的深刻哲理：任何高超的技艺都不是天生的，而是长期反复练习的结果；同时也告诫人们，即使有一技之长，也不应骄傲自满。</p>
    <p>文章的深刻之处，在于它不是空洞地说教，而是通过具体的人物和事件，让读者自己领悟道理。卖油翁的~L~无他，但手熟尔~R~和~L~我亦无他，惟手熟尔~R~，一虚一实，一答一证，把~L~熟能生巧~R~的道理表达得淋漓尽致。同时，陈尧咨从~L~自矜~R~到~L~忿然~R~再到~L~笑而遣之~R~的转变，也告诉我们：人外有人，天外有天，谦虚使人进步，骄傲使人落后。这一哲理在今天仍有重要的现实意义。</p>
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
      <tr><td class="kai">尔</td><td>同~L~耳~R~</td><td>但手熟尔</td><td>相当于~L~罢了~R~，句末语气词，表限止</td></tr>
      <tr><td class="kai">杓</td><td>同~L~勺~R~</td><td>徐以杓酌油沥之</td><td>勺子</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">但</td><td>只，只是</td><td>但是（表转折）</td><td>但手熟尔</td></tr>
      <tr><td class="kai">去</td><td>离开</td><td>到某个地方</td><td>久而不去</td></tr>
      <tr><td class="kai">安</td><td>怎么，哪里</td><td>安全，安定</td><td>尔安敢轻吾射</td></tr>
      <tr><td class="kai">释</td><td>放下</td><td>解释，释放</td><td>释担而立</td></tr>
      <tr><td class="kai">尝</td><td>曾经</td><td>品尝，尝试</td><td>尝射于家圃</td></tr>
      <tr><td class="kai">轻</td><td>轻视（形容词作动词）</td><td>重量小（形容词）</td><td>尔安敢轻吾射</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>一词多义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="3">以</td><td>凭借，因为</td><td>公亦以此自矜</td></tr>
      <tr><td>凭，靠</td><td>以我酌油知之</td></tr>
      <tr><td>用，拿</td><td>以钱覆其口</td></tr>
      <tr><td class="kai" rowspan="2">尔</td><td>同~L~耳~R~，罢了</td><td>但手熟尔</td></tr>
      <tr><td>你，第二人称代词</td><td>尔安敢轻吾射</td></tr>
      <tr><td class="kai" rowspan="2">射</td><td>射箭（动词）</td><td>陈康肃公善射</td></tr>
      <tr><td>射箭的本领（名词）</td><td>吾射不亦精乎</td></tr>
      <tr><td class="kai" rowspan="2">而</td><td>表修饰</td><td>释担而立</td></tr>
      <tr><td>表转折，但是、却</td><td>而钱不湿</td></tr>
      <tr><td class="kai" rowspan="2">之</td><td>代词，指陈尧咨射箭</td><td>睨之久而不去</td></tr>
      <tr><td>代词，指~L~手熟~R~的道理</td><td>以我酌油知之</td></tr>
      <tr><td class="kai" rowspan="2">但</td><td>只，只是</td><td>但手熟尔</td></tr>
      <tr><td>只，只是</td><td>但微颔之</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>词类活用</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">轻</td><td>形容词作动词</td><td>轻视，看轻</td><td>尔安敢轻吾射</td></tr>
      <tr><td class="kai">射</td><td>动词作名词</td><td>射箭的本领</td><td>吾射不亦精乎</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">状语后置</td><td>尝射于家圃</td><td>正常语序为~L~尝于家圃射~R~，~L~于家圃~R~是状语</td></tr>
      <tr><td class="kai">反问句</td><td>汝亦知射乎</td><td>~L~乎~R~表反问，~L~吗~R~</td></tr>
      <tr><td class="kai">反问句</td><td>尔安敢轻吾射</td><td>~L~安~R~表反问，~L~怎么敢~R~</td></tr>
      <tr><td class="kai">省略句</td><td>（翁）乃取一葫芦置于地</td><td>承前省略主语~L~翁~R~</td></tr>
      <tr><td class="kai">省略句</td><td>（油）自钱孔入</td><td>承前省略主语~L~油~R~</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>笔记小说</dt><dd>中国古代以笔记形式写成的小说，多记录轶事趣闻，篇幅短小，文笔简约。《归田录》是欧阳修的笔记集，《卖油翁》是其中寓理于事的名篇。</dd></div>
      <div class="g-item"><dt>《归田录》</dt><dd>欧阳修晚年辞官归隐后所作的笔记集，共二卷，多记朝廷轶事、士大夫趣闻，文笔简约生动。书名~L~归田~R~，取~L~辞官归田~R~之意。</dd></div>
      <div class="g-item"><dt>唐宋八大家</dt><dd>唐代和宋代八位散文家的合称，即韩愈、柳宗元、欧阳修、苏洵、苏轼、苏辙、王安石、曾巩。欧阳修是北宋诗文革新运动的领袖，~L~三苏~R~、王安石、曾巩皆出其门下。</dd></div>
      <div class="g-item"><dt>陈尧咨</dt><dd>（970—1034）字嘉谟，北宋人，咸平三年状元，官至武信军节度使，谥号康肃。他以善射著称，有~L~小由基~R~之称（由基即春秋时楚国神箭手养由基）。文中的~L~陈康肃公~R~即指他。</dd></div>
      <div class="g-item"><dt>谥号</dt><dd>古代帝王、贵族、大臣等死后，根据其生平事迹评定的称号。~L~康肃~R~是陈尧咨的谥号，~L~康~R~表安乐抚民，~L~肃~R~表刚德克就。欧阳修谥号~L~文忠~R~。</dd></div>
      <div class="g-item"><dt>公</dt><dd>古代对男子的尊称，也用于爵位（公、侯、伯、子、男五等爵位之首）。文中~L~陈康肃公~R~的~L~公~R~是对陈尧咨的尊称。</dd></div>
      <div class="g-item"><dt>熟能生巧</dt><dd>成语，指熟练了就能产生巧办法、好办法。出自本文~L~无他，但手熟尔~R~。卖油翁以酌油~L~自钱孔入，而钱不湿~R~的绝技，生动诠释了这一道理。</dd></div>
      <div class="g-item"><dt>葫芦</dt><dd>古代常见的盛物器皿，一年生攀援草本植物的果实，外壳坚硬，可用来盛水、盛酒、盛油等。文中卖油翁用葫芦装油，以钱覆口酌油，是古代常见的生活场景。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《卖油翁》欧阳修</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">宋 · 欧阳修</div>
  <h1 class="hero-title">卖油翁</h1>
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
  <div class="sec-sub">全文分两部分：善射自矜翁睨微颔、问答交锋酌油献技。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《卖油翁》</div>
  <div>欧阳修 · 北宋（1007—1072）· 字永叔，号醉翁、六一居士</div>
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
