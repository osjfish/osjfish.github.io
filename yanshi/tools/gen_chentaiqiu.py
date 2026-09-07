# -*- coding: utf-8 -*-
"""生成《陈太丘与友期》交互式教学课件"""
import re, json, os

BENCH = r"D:\App\Apps\yanshi\jichengtiansiyeyou-sushi.html"
OUT = r"D:\App\Apps\yanshi\chentaiqiuyouqi-shishuoxinyu.html"
LS_KEY = "chentaiqiu_fs"

with open(BENCH, encoding="utf-8") as f:
    bench = f.read()

css = bench[bench.index("<style>")+7:bench.index("</style>")]
js_start = bench.index("<script>\n(function(){")
js_end = bench.index("</script>\n<script>\nvar DICT_WORDS")
main_js = bench[js_start+8:js_end]

HERO_SIDE = "南朝宋 · 刘义庆"
HERO_TITLE = "陈太丘与友期"
PAGE_TITLE = "《陈太丘与友期》刘义庆"

BG_LEAD = [
    "《陈太丘与友期》选自《世说新语·方正》，记述了七岁孩童陈元方驳斥失信友人的故事。全文仅一百余字，通过一场简短的对话，塑造了一个明白事理、落落大方的少年形象，也揭示了“信”与“礼”的重要。",
    "友人失信在先，又对子骂父，元方据理驳斥，句句在理。“入门不顾”的收尾，既有少年人的率真，也留下了关于宽容与教养的思考空间，历来被视为《世说新语》中最富教育意义的名篇之一。"
]

AUTHOR_BOX = [
    ("作者简介", [
        "刘义庆（403—444），南朝宋彭城人，宋武帝刘裕之侄，袭封临川王。爱好文学，招聚才学之士，编撰《世说新语》《幽明录》等。",
        "《世说新语》分三十六门，记载东汉末至东晋士族言谈轶事。语言精炼，人物传神，是魏晋风度的集中写照，也是我国最早的文言志人小说集。"
    ])
]

BG_BOX = [
    ("写作背景", [
        "<b>陈太丘：</b>陈寔（104—187），字仲弓，东汉颍川许县（今河南许昌）人，曾任太丘长，故称“陈太丘”。他以德行著称，与子陈纪、陈谌并称“三君”，是东汉名士的代表。",
        "<b>陈元方：</b>陈纪（129—199），字元方，陈寔长子，以至德称名，官至大鸿胪。文中所记是他七岁时的故事。",
        "<b>方正之门：</b>本文选自《世说新语·方正》。“方正”指为人正直、不阿权贵。陈元方面对友人的无礼，据理力争、不卑不亢，正是“方正”品格的体现。",
        "<b>魏晋重礼：</b>魏晋士族极重礼法与家教。“信”是立身之本，“礼”是待人之道。友人“日中不至”是无信，“对子骂父”是无礼，元方的驳斥正击中这两点。"
    ])
]

MEDIA = [
    ("《陈太丘与友期行》诵读", "BV1J44y1x7ot", "陈太丘与友期行诵读"),
    ("趣味动画学《陈太丘与友期行》", "BV1tX4y1n7Eh", "趣味动画学陈太丘与友期行"),
]

VERSES = [
    (
        "陈太丘与友期行，期日中。",
        "陈太丘和朋友相约同行，约定的时间是正午。",
        "开篇极简，交代人物与约定。“期日中”三字点明时间——正午是最明确的时间节点，为下文“过中不至”的失信埋下伏笔。两个“期”字，前为动词（约定），后为名词（约定的时间），一词两用，精炼之至。",
        [
            ("陈太丘", "即陈寔，字仲弓，东汉人，曾任太丘长，故称"),
            ("期行", "相约同行。期，约定"),
            ("期日中", "约定的时间是正午。日中，正午时分"),
        ]
    ),
    (
        "过中不至，太丘舍去，去后乃至。",
        "过了正午朋友还没有到，陈太丘就不再等候而离开了，（太丘）离开后朋友才到。",
        "三句三层：“过中不至”写友人失信；“太丘舍去”写陈寔的决断——守信者不等无信之人；“去后乃至”写友人姗姗来迟。三个短句节奏紧凑，把一场失信的前因后果交代得清清楚楚，也为下文的冲突蓄势。",
        [
            ("过中", "过了正午"),
            ("不至", "没有到"),
            ("舍去", "不再等候就走了。舍，舍弃、放弃；去，离开"),
            ("乃至", "才到。乃，才"),
        ]
    ),
    (
        "元方时年七岁，门外戏。",
        "元方当时年龄七岁，在门外玩耍。",
        "插叙一笔，交代元方的年龄与处境。“时年七岁”强调其年幼——七岁孩童却能在接下来的对话中据理力争，更显其早慧。“门外戏”写他正在玩耍，并非刻意等候，为下文友人问元方的情节做了自然铺垫。",
        [
            ("元方", "陈纪，字元方，陈寔的长子"),
            ("时年", "当时年龄"),
            ("戏", "玩耍，嬉戏"),
        ]
    ),
    (
        "客问元方：“尊君在不？”答曰：“待君久不至，已去。”",
        "客人问元方：“你的父亲在吗？”元方回答说：“（我父亲）等了您很久您却还没有到，已经离开了。”",
        "对话开始。友人问“尊君在不”，用“尊君”是尊称，表面客气；元方答“待君久不至，已去”，用“君”回称，不卑不亢，且点明父亲是因久等不至才离开——暗指友人失信。七岁孩童应对得体，已见其教养。",
        [
            ("尊君", "对别人父亲的尊称。尊，敬辞"),
            ("不", "同“否”，句末语气词，表询问"),
            ("待", "等待"),
            ("君", "对对方的尊称，相当于“您”"),
            ("已去", "已经离开。已，已经"),
        ]
    ),
    (
        "友人便怒曰：“非人哉！与人期行，相委而去。”",
        "友人便生气地说：“真不是人啊！和别人相约同行，却丢下别人先离开了。”",
        "友人得知陈寔已走，不反省自己失信，反而发怒骂人。“非人哉”三字粗暴无礼，“相委而去”倒打一耙——明明是自己“过中不至”，却指责别人“相委而去”。友人的易怒与无礼，与元方的从容形成鲜明对比，也为下文元方的驳斥提供了靶子。",
        [
            ("便怒", "就生气了。便，就"),
            ("非人哉", "真不是人啊！哉，语气词，表感叹"),
            ("相委", "丢下别人。相，表示动作偏指一方；委，舍弃、丢下"),
            ("而去", "而离开。而，表转折，却"),
        ]
    ),
    (
        "元方曰：“君与家君期日中。日中不至，则是无信；对子骂父，则是无礼。”",
        "元方说：“您与我父亲约定在正午。正午您没到，就是不讲信用；对着孩子骂他的父亲，就是没有礼貌。”",
        "全文核心。元方的驳斥条理清晰、层层递进：先指出“君与家君期日中”的事实，再以两个“则是”推出结论——“日中不至”是无信，“对子骂父”是无礼。“信”与“礼”正是儒家立身之本，七岁孩童能如此精准地抓住要害，令人叹服。两个排比句斩钉截铁，气势如虹。",
        [
            ("家君", "对人谦称自己的父亲。家，谦辞，用于对别人称自己的辈分高或年纪大的亲属"),
            ("则", "就，便是"),
            ("无信", "不讲信用。信，信用"),
            ("无礼", "没有礼貌。礼，礼貌、礼节"),
        ]
    ),
    (
        "友人惭，下车引之。元方入门不顾。",
        "友人感到惭愧，下车来拉元方（表示好感）。元方头也不回地走进了大门。",
        "结尾三句，各有深意。“友人惭”写友人被驳后自知理亏；“下车引之”写其欲以行动表示歉意与好感；“元方入门不顾”写元方的态度——头也不回。这个收尾历来有争议：有人赞其刚直，有人议其过分。但正是这个开放性的结尾，让文章余味悠长——面对知错欲改的人，该不该给予宽容？七岁的元方用行动给出了他的答案。",
        [
            ("惭", "惭愧"),
            ("引之", "拉他。引，拉；之，代词，指元方"),
            ("入门", "走进家门"),
            ("不顾", "不回头看。顾，回头看"),
        ]
    ),
]

APP_BOXES = [
    ("人物形象", [
        ("聪慧方正的陈元方", "元方是本文的核心人物。他年仅七岁，却能在友人发怒骂人时从容应对，以“无信”“无礼”两点精准驳斥，逻辑清晰、言辞犀利。“入门不顾”更见其刚直率真——面对无信无礼之人，他不屑于假以辞色。这个形象既是魏晋士族家教的缩影，也是中国文学中“早慧儿童”的经典原型。"),
        ("失信无礼的友人", "友人是反面形象。他“过中不至”是无信，得知陈寔已走后不反省自己，反而“非人哉”怒骂是无礼。但他被元方驳斥后“下车引之”，说明尚有羞耻之心、知过之意。这个人物并非脸谱化的坏人，而是一个有缺点但能知惭的普通人，使文章更具真实感与教育意义。"),
        ("守信重礼的陈太丘", "陈太丘虽未直接出场，但其形象贯穿全文。他“期日中”而“过中不至”便“舍去”，是守信的表现——不因为等无信之人而浪费自己的时间。他的家教也通过元方的言行得以体现：七岁孩童便能明辨信礼，正是家风熏陶的结果。"),
    ]),
    ("艺术特色", [
        ("对话传神，性格毕现", "全文以对话推动情节，人物语言极富个性。友人的话粗暴易怒（“非人哉！”），元方的话条理清晰（“则是无信……则是无礼”）。通过对话，一个无礼易怒的成年人和一个聪慧方正的孩童形象跃然纸上。"),
        ("对比鲜明，主题突出", "文章多处运用对比：友人的失信无礼与元方的知书达理对比；友人的“便怒”与后来的“惭”对比；陈太丘的守信与友人的无信对比。在对比中，“信”与“礼”的主题得到了有力的凸显。"),
        ("叙事极简，余味悠长", "全文仅一百余字，却有完整的起因、发展、高潮、结局。结尾“元方入门不顾”戛然而止，不置褒贬，却留下了关于宽容与教养的无限思考空间。这种“言有尽而意无穷”的笔法，正是《世说新语》的魅力所在。"),
        ("一词多义，精炼含蓄", "文中“期”字两用（“期行”之“期”为动词，“期日中”之“期”为名词），“不”通“否”，“相委”之“相”偏指一方——文言知识点密集而自然，是七年级学生学习文言文的绝佳范本。"),
    ]),
    ("名句赏析", [
        ("日中不至，则是无信；对子骂父，则是无礼。", "元方驳斥友人的核心句，也是全文的点睛之笔。两个“则是”构成排比，逻辑严密、斩钉截铁：先论“信”——约定日中而不至，是失信；再论“礼”——当着儿子的面骂父亲，是失礼。“信”与“礼”是儒家伦理的两大支柱，七岁孩童能如此精准地抓住要害，既见其早慧，也见其家教。此句历来被视为讲诚信、重礼仪的经典论述。"),
        ("元方入门不顾。", "全文收尾，也是最具争议的一笔。“入门不顾”四字，写出元方的刚直与率真——面对无信无礼之人，他不屑于假以辞色。但友人已“惭”且“下车引之”，有悔过之意，元方是否应该给予宽容？这个开放性的结尾，让文章超越了简单的道德说教，引发了关于教养、宽容与原则的深层思考。"),
    ]),
    ("主题思想", [
        "本文通过记述七岁的陈元方驳斥失信友人的故事，揭示了“信”与“礼”的重要：做人要守信用，待人要讲礼貌。",
        "文章同时塑造了一个聪慧方正、不卑不亢的少年形象，展现了魏晋士族重视家教、崇尚方正的社会风气。友人“下车引之”的悔过与元方“入门不顾”的刚直形成对照，也引发了关于原则与宽容的思考——坚守原则固然可贵，但面对知过能改之人，是否也应给予一份宽容？这正是此文超越时代的价值所在。"
    ]),
]

ACC = [
    ("通假字", [
        ("不", "通“否”，句末语气词，表询问。例：尊君在不？"),
    ]),
    ("古今异义", [
        ("期", "古义：约定（陈太丘与友期行）；今义：日期、期限"),
        ("去", "古义：离开（太丘舍去）；今义：前往、到……去"),
        ("顾", "古义：回头看（元方入门不顾）；今义：照顾、顾及"),
        ("儿女", "古义：子侄辈（本文未出现，《咏雪》中有）；今义：儿子和女儿"),
        ("引", "古义：拉（下车引之）；今义：引导、引用"),
    ]),
    ("一词多义", [
        ("期", "约定：陈太丘与友期行 / 约定的时间：期日中"),
        ("日", "太阳：日中 / 天：一日"),
        ("去", "离开：太丘舍去 / 距离：相去甚远"),
        ("不", "同“否”：尊君在不 / 否定副词：不去"),
        ("之", "代词，指元方：下车引之 / 结构助词，的：君子之交"),
        ("而", "表转折，却：相委而去 / 表顺承：取而代之"),
    ]),
    ("词类活用", [
        ("（本文无典型词类活用）", "《陈太丘与友期》中无典型的词类活用现象。"),
    ]),
    ("文言句式", [
        ("省略句", "“待君久不至，已去”省略主语“家君”，即“（家君）待君久不至，已去”"),
        ("判断句", "“日中不至，则是无信；对子骂父，则是无礼”，“则是”表判断"),
        ("倒装句", "“相委而去”中“相”为宾语前置，即“委相而去”（丢下我）"),
    ]),
    ("文化常识", [
        ("《世说新语》", "南朝宋刘义庆组织编撰的志人小说集，分三十六门，记载东汉末至东晋士族言谈轶事。本文选自“方正”门。"),
        ("陈太丘", "即陈寔（104—187），字仲弓，东汉人，曾任太丘长。以德行著称，与子陈纪、陈谌并称“三君”。太丘是古县名，在今河南永城西北。"),
        ("尊君 / 家君", "“尊君”是对别人父亲的尊称；“家君”是对人谦称自己的父亲。一敬一谦，体现了古人称谓中的礼仪文化。"),
        ("信与礼", "儒家伦理的两大支柱。“信”是立身之本，“人而无信，不知其可也”；“礼”是待人之道，“不学礼，无以立”。元方的驳斥正基于此。"),
        ("方正", "《世说新语》门类之一，指为人正直、不阿权贵、坚持原则。陈元方面对友人无礼，据理力争、不卑不亢，正是“方正”品格的体现。"),
    ]),
]

DICT_WORDS = [
    {"w":"寔","py":"shí","q":"陈太丘，即陈□","tip":"「寔」宝盖头，用于人名陈寔，读 shí；勿写「实」「是」"},
    {"w":"哉","py":"zāi","q":"非人□","tip":"「哉」口字旁，语气词表感叹，读 zāi；勿写「栽」「裁」"},
    {"w":"惭","py":"cán","q":"友人□，下车引之","tip":"「惭」竖心旁，惭愧义，读 cán；勿写「渐」「暂」"},
    {"w":"顾","py":"gù","q":"元方入门不□","tip":"「顾」页字旁，回头看义，读 gù；勿写「故」「雇」"},
    {"w":"委","py":"wěi","q":"相□而去","tip":"「委」禾字旁，舍弃义，读 wěi；勿写「萎」「魏」"},
    {"w":"引","py":"yǐn","q":"下车□之","tip":"「引」弓字旁，拉义，读 yǐn；勿写「张」「弘」"},
    {"w":"期","py":"qī","q":"陈太丘与友□行","tip":"「期」月字旁，约定义，读 qī；勿写「欺」「旗」"},
]

DICT_NOTES = [
    {"w":"陈太丘","a":"即陈寔，字仲弓，东汉人，曾任太丘长","q":"陈太丘与友期行"},
    {"w":"期行","a":"相约同行。期，约定","q":"陈太丘与友期行"},
    {"w":"期日中","a":"约定的时间是正午。日中，正午","q":"期日中"},
    {"w":"舍去","a":"不再等候就走了。舍，舍弃；去，离开","q":"太丘舍去"},
    {"w":"乃至","a":"才到。乃，才","q":"去后乃至"},
    {"w":"元方","a":"陈纪，字元方，陈寔的长子","q":"元方时年七岁"},
    {"w":"戏","a":"玩耍，嬉戏","q":"门外戏"},
    {"w":"尊君","a":"对别人父亲的尊称","q":"尊君在不"},
    {"w":"不","a":"同“否”，句末语气词，表询问","q":"尊君在不"},
    {"w":"君","a":"对对方的尊称，相当于“您”","q":"待君久不至"},
    {"w":"已去","a":"已经离开","q":"待君久不至，已去"},
    {"w":"非人哉","a":"真不是人啊！哉，语气词表感叹","q":"非人哉"},
    {"w":"相委","a":"丢下别人。相，偏指一方；委，舍弃","q":"相委而去"},
    {"w":"家君","a":"对人谦称自己的父亲","q":"君与家君期日中"},
    {"w":"则","a":"就，便是","q":"则是无信"},
    {"w":"无信","a":"不讲信用","q":"则是无信"},
    {"w":"无礼","a":"没有礼貌","q":"则是无礼"},
    {"w":"惭","a":"惭愧","q":"友人惭"},
    {"w":"引之","a":"拉他。引，拉；之，指元方","q":"下车引之"},
    {"w":"入门不顾","a":"走进家门不回头看。顾，回头看","q":"元方入门不顾"},
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
<div class="sec-sub">全文一百余字，分七句逐句解读。每句含注释、译文与赏析，点击可展开。</div>
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
  <div class="kai">《陈太丘与友期》</div>
  <div>刘义庆 · 南朝宋（403—444）· 选自《世说新语·方正》</div>
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
