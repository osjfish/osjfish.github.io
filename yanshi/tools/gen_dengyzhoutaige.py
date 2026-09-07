# -*- coding: utf-8 -*-
"""生成《登幽州台歌》课件（中国古诗，短篇，逐句解读+译文+赏析）。"""
import io, json, re

SRC = r"D:\App\Apps\yanshi\chibi-dumu.html"
OUT = r"D:\App\Apps\yanshi\dengyouzhoutaige-chenziang.html"
LS_KEY = "dengyzhoutaige_fs"

LQ = "\u201c"
RQ = "\u201d"

def A(word, note):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)

# 逐句数据：(原文带注释标记, 译文, 赏析, [标签])
CARDS = [
("前不见" + A("古人","古代的贤明君主。此处指像燕昭王那样能礼贤下士的明君") + "，",
 "向前看不见古代的贤明君主。",
 "起句以" + LQ + "前不见古人" + RQ + "写时间的辽远——诗人登上幽州台，向前眺望，看不见古代的贤明君主（如燕昭王）。" + LQ + "古人" + RQ + "不是泛指古人，而是特指那些能够礼贤下士、重用人才的明君。一个" + LQ + "不见" + RQ + "，写出了诗人对古代明君的向往，也暗示了自己生不逢时的感慨。",
 ["时间感","用典"]),
("后不见" + A("来者","后世的贤明君主") + "。",
 "向后也看不见后世的贤明君主。",
 "次句承接上句，" + LQ + "后不见来者" + RQ + "写时间的另一端——向后看，也看不见后世的贤明君主。前两句形成时间上的前后对照：前无古人，后无来者。诗人将自己置于时间的长河中，向前看不到古代的明君，向后看不到后世的明主——自己恰恰处在一个没有明君的时代。这种时间上的孤独感，为下文的空间孤独感蓄势。",
 ["时间感","前后对照"]),
(A("念","想到、思虑") + "天地之" + A("悠悠","辽阔、无穷无尽的样子") + "，",
 "想到天地是这样的辽阔无穷。",
 "第三句由时间转入空间。" + LQ + "念天地之悠悠" + RQ + "——诗人想到天地是这样的辽阔无穷，宇宙是这样的浩瀚无垠。" + LQ + "悠悠" + RQ + "二字，写出了天地的辽阔、宇宙的无穷，也反衬出人的渺小与孤独。在无穷的天地面前，个人是何等的微不足道；而在这无穷的天地中，又有谁能理解自己、重用自己呢？",
 ["空间感","反衬"]),
("独" + A("怆(chuàng)然","悲伤凄恻的样子。怆，读 chuàng") + "而" + A("涕(tì)","眼泪。古义为眼泪，今义多指鼻涕") + "下。",
 "独自悲伤凄恻，眼泪不禁流了下来。",
 "末句是全诗的情感高潮。" + LQ + "独怆然而涕下" + RQ + "——诗人独自悲伤，眼泪不禁流了下来。一个" + LQ + "独" + RQ + "字，是全诗的诗眼：前两句写时间的孤独（前不见古人，后不见来者），第三句写空间的孤独（天地悠悠，人何其渺小），末句以一个" + LQ + "独" + RQ + "字收束，将时间与空间的孤独凝聚为一个人的孤独——在这无穷的宇宙中，只有我一个人，怀才不遇，知音难觅，怎能不悲伤流泪？" + LQ + "涕" + RQ + "古义为眼泪，与今义（鼻涕）不同，需特别注意。",
 ["诗眼","时空交错","怀才不遇"]),
]

FULLTEXT = [
 "前不见古人，",
 "后不见来者。",
 "念天地之悠悠，",
 "独怆然而涕下。",
]

BG_LEAD = [
 "陈子昂（661—702），唐代文学家，初唐诗文革新人物之一。万岁通天元年（696），契丹李尽忠、孙万荣等攻陷营州，武则天派武攸宜率军征讨，陈子昂以右拾遗随军参谋。武攸宜出身亲贵，不晓军事，陈子昂屡次进谏，不但不被采纳，反而被降为军曹。诗人满怀报国之志，却屡遭挫折，在随军北征途中登上幽州台，写下了这首千古名篇。",
 "全诗仅四句二十余字，却以苍茫的笔调写出了天地的辽阔与人生的孤独。前两句写时间感——前不见古人，后不见来者；后两句写空间感与孤独——念天地之悠悠，独怆然而涕下。时空交错，将个人的怀才不遇置于无穷的宇宙背景之下，形成了一种震撼人心的孤独感与悲壮感。这首诗是陈子昂的代表作，也是唐代诗歌中最著名的咏怀诗之一。",
]

AUTHOR = [
 "陈子昂（661—702），字伯玉，梓州射洪（今四川射洪）人，唐代文学家，初唐诗文革新人物之一。因曾任右拾遗，后世称陈拾遗。他主张改革六朝以来浮靡的诗风，提倡" + LQ + "汉魏风骨" + RQ + LQ + "风雅兴寄" + RQ + "，是唐代诗歌革新的先驱。",
 "陈子昂出身富豪之家，少年时任侠使气，后发愤读书。24岁中进士，因上书论政得到武则天赏识，任麟台正字，后升右拾遗。他曾两次从军边塞，对边防事务颇有远见。圣历元年（698），因父老解官回乡，不久父死。居丧期间，权臣武三思指使射洪县令段简罗织罪名，加以迫害，陈子昂最终冤死狱中，年仅42岁。代表作有《登幽州台歌》《感遇》三十八首、《蓟丘览古》七首等。",
]

STORY = [
 ("幽州台","幽州台，即蓟北楼，故址在今北京西南，是战国时燕昭王所建。燕昭王为了振兴燕国，在台上放置千金，广招天下贤士，因此又称" + LQ + "黄金台" + RQ + "。陈子昂登上此台，自然会想到燕昭王礼贤下士的故事，对比自己的怀才不遇，感慨万千。"),
 ("随军北征","万岁通天元年（696），契丹叛乱，武则天派武攸宜率军征讨，陈子昂以右拾遗随军参谋。武攸宜是武则天的侄子，出身亲贵，不懂军事，前锋大败，举军震恐。陈子昂屡次进谏，提出破敌之策，不但不被采纳，反而被降为军曹。诗人满怀报国之志，却遭此打击，心中悲愤难平。"),
 ("登台赋诗","在随军北征途中，陈子昂登上幽州台，眺望北方苍茫的原野，想到燕昭王筑台招贤的往事，对比自己的遭遇，写下了《登幽州台歌》和《蓟丘览古》七首。《登幽州台歌》是其中最著名的一首，以短短四句写出了千古孤独。"),
 ("古体诗","《登幽州台歌》是一首古体诗，不讲究近体诗的格律对仗。全诗四句，前两句每句五字，后两句每句六字，句式长短错落，节奏急促而苍凉。古体诗的自由形式，恰好适合表达诗人奔放而悲怆的情感。"),
]

APP_ART = [
 ("时空交错，意境苍茫","全诗最突出的艺术特色是时空交错。前两句" + LQ + "前不见古人，后不见来者" + RQ + "写时间——向前看不到古代的明君，向后看不到后世的明主，诗人被夹在时间的长河中，前无古人后无来者；后两句" + LQ + "念天地之悠悠，独怆然而涕下" + RQ + "写空间——天地辽阔无穷，人何其渺小，在这无穷的宇宙中只有我一个人孤独流泪。时间与空间交织，形成了一种苍茫辽阔的意境。"),
 ("" + LQ + "独" + RQ + "字的力量","全诗的诗眼是末句的" + LQ + "独" + RQ + "字。前两句写时间的孤独，第三句写空间的孤独，末句以一个" + LQ + "独" + RQ + "字收束——在这无穷的时间和空间中，只有我一个人。" + LQ + "独" + RQ + "字将时间与空间的孤独凝聚为一个人的孤独，将个人的怀才不遇置于宇宙的背景之下，形成了一种震撼人心的力量。"),
 ("怀才不遇的孤独","全诗的情感核心是怀才不遇的孤独。陈子昂有报国之志、有济世之才，却不被重用，反而被降职。登上幽州台，想到燕昭王筑台招贤的往事，对比自己的遭遇，怎能不悲？" + LQ + "前不见古人" + RQ + "是向往古代的明君，" + LQ + "后不见来者" + RQ + "是对当世的失望，" + LQ + "独怆然而涕下" + RQ + "是怀才不遇的悲愤。全诗没有一句直接写" + LQ + "怀才不遇" + RQ + "，但字字都是怀才不遇的感慨。"),
 ("句式错落，节奏苍凉","全诗句式长短错落：前两句五字，后两句六字。五字句短促有力，如感叹；六字句舒缓悠长，如悲吟。" + LQ + "前不见古人，后不见来者" + RQ + "节奏急促，如脱口而出的感叹；" + LQ + "念天地之悠悠，独怆然而涕下" + RQ + "节奏舒缓，如深沉的悲吟。句式的错落与节奏的变化，恰好表达了诗人由激愤到悲凉的情感变化。"),
]

APP_FAME = [
 ("前不见古人，后不见来者。",
  "这两句是全诗的时间维度。" + LQ + "前不见古人" + RQ + "——向前看，看不见古代的贤明君主（如燕昭王）；" + LQ + "后不见来者" + RQ + "——向后看，也看不见后世的贤明君主。诗人将自己置于时间的长河中，前无古人，后无来者，自己恰恰处在一个没有明君的时代。这两句以极简的笔墨写出了时间的辽远与生不逢时的感慨，是千古传诵的名句。"),
 ("念天地之悠悠，独怆然而涕下。",
  "这两句是全诗的空间维度与情感高潮。" + LQ + "念天地之悠悠" + RQ + "——想到天地是这样的辽阔无穷，宇宙是这样的浩瀚无垠；" + LQ + "独怆然而涕下" + RQ + "——在这无穷的天地中，只有我一个人，独自悲伤流泪。" + LQ + "悠悠" + RQ + "写出天地的辽阔，反衬人的渺小；" + LQ + "独" + RQ + "字是全诗的诗眼，将时间与空间的孤独凝聚为一个人的孤独。这两句将个人的怀才不遇置于宇宙的背景之下，形成了震撼人心的力量。"),
]

APP_THEME = [
 "本诗通过描写诗人登上幽州台的所见所感，表达了诗人怀才不遇、知音难觅的孤独与悲愤。诗人以" + LQ + "前不见古人，后不见来者" + RQ + "写时间的辽远——向往古代的明君，失望于当世；以" + LQ + "念天地之悠悠，独怆然而涕下" + RQ + "写空间的辽阔与个人的孤独——在无穷的宇宙中，只有自己一个人，怀才不遇，怎能不悲？",
 "全诗将个人的命运置于无穷的时间与空间之中，形成了一种苍茫辽阔的意境和震撼人心的孤独感。这首诗不仅是陈子昂个人怀才不遇的感慨，也道出了古往今来所有怀才不遇之士的共同心声，因此能够引起千古读者的共鸣。" + LQ + "独怆然而涕下" + RQ + "的" + LQ + "独" + RQ + "字，是全诗的诗眼，也是中国文学中最著名的孤独意象之一。",
]

ACC = [
 ("文体与格律", [
   ("古体诗","本诗是一首古体诗，不讲究近体诗的格律对仗。全诗四句，前两句五字，后两句六字，句式长短错落。"),
   ("押韵","本诗不严格押韵，" + LQ + "者" + RQ + LQ + "下" + RQ + "古韵同属一个韵部（上古音中" + LQ + "者" + RQ + "读如" + LQ + "堵" + RQ + "，与" + LQ + "下" + RQ + "押韵）。"),
   ("句式特点","前两句五字句，节奏" + LQ + "二/三" + RQ + "（前不/见古人）；后两句六字句，节奏" + LQ + "一/二/三" + RQ + "（念/天地/之悠悠）。句式长短错落，节奏由急促到舒缓。"),
 ]),
 ("易错字音形", [
   ("怆","chuàng","竖心旁，悲伤凄恻义；勿写「创」（立刀旁）"),
   ("涕","tì","三点水，古义为眼泪（非鼻涕）；勿写「悌」（竖心旁）"),
   ("悠","yōu","心字底，「悠悠」形容辽阔；勿写「忧」（竖心旁）"),
   ("幽","yōu","山字底，「幽州」古地名；勿写「优」（单人旁）"),
 ]),
 ("文言梳理", [
   ("古今异义","涕：古义为眼泪（独怆然而涕下），今义多指鼻涕。这是本诗最重要的古今异义词。"),
   ("一词多义","念：文中义为" + LQ + "想到、思虑" + RQ + "（念天地之悠悠）；其他常见义有" + LQ + "思念" + RQ + LQ + "诵读" + RQ + LQ + "念头" + RQ + "。"),
   ("词类活用","本诗无明显词类活用。"),
   ("文言句式","本诗句式简短，无特殊文言句式。" + LQ + "前不见古人，后不见来者" + RQ + "是对仗句式（宽对）。"),
 ]),
 ("本文核心考点：炼字与时空", [
   ("" + LQ + "独" + RQ + "字","全诗的诗眼。将时间与空间的孤独凝聚为一个人的孤独，是全诗情感的焦点。"),
   ("" + LQ + "悠悠" + RQ + "","形容天地辽阔无穷，反衬人的渺小与孤独，是空间感的核心词。"),
   ("时空交错","前两句写时间（前/后），后两句写空间（天地/独），时空交错形成苍茫意境。"),
   ("用典","" + LQ + "古人" + RQ + "特指燕昭王等古代贤明君主，" + LQ + "幽州台" + RQ + "即黄金台，用燕昭王筑台招贤的典故。"),
 ]),
 ("修辞与手法", [
   ("对　比","时间对比：前不见古人 vs 后不见来者；空间对比：天地悠悠 vs 一人独泣。在对比中凸显孤独。"),
   ("衬　托","以天地的辽阔无穷反衬人的渺小与孤独，以宇宙的浩瀚反衬个人的无助。"),
   ("用　典","幽州台（黄金台）用燕昭王筑台招贤的典故，" + LQ + "古人" + RQ + "指古代贤明君主，暗含对明君的向往与对当世的失望。"),
   ("直抒胸臆","全诗不借景物，直接抒发怀才不遇的孤独与悲愤，" + LQ + "独怆然而涕下" + RQ + "是直抒胸臆的典范。"),
 ]),
 ("文化常识", [
   ("幽州台","即蓟北楼，故址在今北京西南，战国时燕昭王所建。台上置千金招贤，故又称" + LQ + "黄金台" + RQ + "。"),
   ("燕昭王","战国时燕国国君，以筑黄金台广招天下贤士而闻名。他重用乐毅等贤才，使燕国强大起来。"),
   ("右拾遗","唐代官名，属中书省，掌供奉讽谏、荐举人才。陈子昂曾任右拾遗，后世称陈拾遗。"),
   ("汉魏风骨","陈子昂提倡的诗歌革新主张，指继承汉魏诗歌刚健质朴、关心现实的传统，反对六朝浮靡诗风。"),
 ]),
]

WORDS = [
 {"w":"怆","py":"chuàng","q":"独□然而涕下。","tip":"「怆」竖心旁，读 chuàng 四声；悲伤义，勿写「创」（立刀旁）"},
 {"w":"涕","py":"tì","q":"独怆然而□下。","tip":"「涕」三点水，读 tì；古义为眼泪（非鼻涕），勿写「悌」（竖心旁）"},
 {"w":"悠悠","py":"yōu yōu","q":"念天地之□□，","tip":"「悠悠」心字底，读 yōu yōu；形容辽阔无穷，勿写「忧忧」（竖心旁）"},
 {"w":"幽","py":"yōu","q":"登□州台歌","tip":"「幽」山字底，读 yōu；「幽州」古地名，勿写「优」（单人旁）"},
]

NOTES = [
 {"w":"古人","a":"古代的贤明君主，特指燕昭王那样能礼贤下士的明君","q":"前不见古人，"},
 {"w":"来者","a":"后世的贤明君主","q":"后不见来者。"},
 {"w":"念","a":"想到、思虑","q":"念天地之悠悠，"},
 {"w":"悠悠","a":"辽阔、无穷无尽的样子","q":"念天地之悠悠，"},
 {"w":"怆然","a":"悲伤凄恻的样子。怆，读 chuàng","q":"独怆然而涕下。"},
 {"w":"涕","a":"眼泪。古义为眼泪，今义多指鼻涕","q":"独怆然而涕下。"},
]

VIDEOS = [
 ("陈子昂《登幽州台歌》朗诵","BV12N4y1S7bg","陈子昂《登幽州台歌》朗诵"),
 ("康震老师讲古诗词——登幽州台歌","BV157411J7Y6","康震讲登幽州台歌"),
]

# ===== 读取框架 =====
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]
js_main = src[src.index("<script>") + 8 : src.index("var DICT_WORDS")]
js_main = js_main.replace("chibi_fs", LS_KEY)
js_dict = src[src.index("var DICT_WORDS") : src.index("</script>", src.index("var DICT_WORDS"))]
js_dict = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", js_dict, flags=re.S)
js_dict = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", js_dict, flags=re.S)

def video(i, h4, bvid, atitle):
    return ('<div class="media"><h4>%s</h4>'
            '<iframe id="mediaF%d" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>'
            '<a href="https://www.bilibili.com/video/%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF%d">全屏播放</button></div>'
            % (h4, i, bvid, atitle, bvid, i))

hero = '<header class="hero" id="top">\n  <div class="hero-inner">\n    <div class="hero-side">唐·陈子昂</div>\n    <h1 class="hero-title">登幽州台歌</h1>\n  </div>\n</header>'

nav = ('<nav class="nav"><div class="nav-in">'
       '<a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a>'
       '<div class="tool">'
       '<select id="fsSel" class="fs-sel" title="正文字体大小">'
       '<option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option>'
       '</select>'
       '<button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button>'
       '</div></div></nav>')

bg = ['<section id="bg">',
      '<div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>',
      '<div class="lead">']
for p in BG_LEAD: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>作者简介</h3>')
for p in AUTHOR: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>创作背景</h3>')
for t, p in STORY: bg.append('<p><b>' + t + '：</b>' + p + '</p>')
bg.append('</div></section>')

jl = ['<section id="jielu">',
      '<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>',
      '<div class="sec-sub">全诗四句，前两句写时间感（前不见古人，后不见来者），后两句写空间感与孤独（念天地之悠悠，独怆然而涕下）。每句含<b>注释</b>（生僻字、易错词均附读音）、译文与赏析，点击可展开。短篇诗歌不分部分，直接逐句解读。</div>',
      '<div class="texttools">',
      '<button id="btnShowAll" class="off" style="display:none">显示全部</button>',
      '</div>',
      '<div class="box media-box">',
      '<h3>朗诵 · 拓展</h3>',
      '<div class="media-grid">']
for i, (h4, bvid, at) in enumerate(VIDEOS):
    jl.append(video(i + 1, h4, bvid, at))
jl.append('</div></div>')

jl.append('<div class="fulltext poem" id="fulltext" style="display:none">')
for idx, line in enumerate(FULLTEXT, 1):
    jl.append('<div class="pl"><span class="no">%d</span>%s</div>' % (idx, line))
jl.append('</div>')

jl.append('<div class="verse-list" id="verseList">')
for n, (orig, yi, shang, tags) in enumerate(CARDS, 1):
    jl.append('<div class="verse" id="v%d">' % n)
    jl.append('  <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (n, orig))
    jl.append('  <details class="v-more">')
    jl.append('    <summary>译文 · 赏析</summary>')
    jl.append('    <div class="d-body">')
    jl.append('      <div class="v-sec"><b class="v-label">译　文</b>')
    jl.append('        <div class="v-trans">%s</div>' % yi)
    jl.append('      </div>')
    jl.append('      <div class="v-sec"><b class="v-label">赏　析</b>')
    jl.append('        <div class="d-body"><p>%s</p></div>' % shang)
    if tags:
        jl.append('        <div class="tags">%s</div>' % ''.join('<span>%s</span>' % t for t in tags))
    jl.append('      </div>')
    jl.append('    </div>')
    jl.append('  </details>')
    jl.append('</div>')
jl.append('</div></section>')

app = ['<section id="app">',
       '<div class="sec-head"><h2>赏 析</h2><span class="no">艺术特色 · 名句 · 主题</span></div>']
app.append('<div class="fame-card"><h3>艺术特色</h3>')
for t, p in APP_ART:
    app.append('<p><b>%s</b>：%s</p>' % (t, p))
app.append('</div>')
app.append('<div class="fame-card"><h3>名句赏析</h3><div class="fame">')
for t, p in APP_FAME:
    app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div>')
app.append('<div class="fame-card"><h3>主题思想</h3>')
for p in APP_THEME: app.append('<p>' + p + '</p>')
app.append('</div></section>')

acc = ['<section id="acc">',
       '<div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 炼字 · 修辞 · 文化常识</span></div>']
for cat, items in ACC:
    acc.append('<div class="box"><h3>%s</h3>' % cat)
    if cat in ("文体与格律", "文言梳理", "本文核心考点：炼字与时空", "修辞与手法", "文化常识"):
        for w, d in items:
            acc.append('<p><b class="term">%s</b>%s</p>' % (w, d))
    else:
        acc.append('<div class="tw"><table>')
        acc.append('<tr><th>字词</th><th>注音</th><th>易错提示</th></tr>')
        for w, py, tip in items:
            acc.append('<tr><td class="kai">%s</td><td>%s</td><td>%s</td></tr>' % (w, py, tip))
        acc.append('</table></div>')
    acc.append('</div>')
acc.append('</section>')

practice = ['<section id="practice">',
            '<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写 · 字词 / 注释</span></div>',
            '<div class="sec-sub">以全篇<b>易错字词</b>与<b>重点注释</b>为题库，点击按钮进入<b>全屏听写</b>：先看提示在纸上默写，再核对答案。随机五组适合随堂小测，全部适合系统复习。</div>',
            '<div class="ptools">',
            '<button data-mode="word" data-rand="5">随机五组字形</button>',
            '<button data-mode="word" data-all="1">全部字形</button>',
            '<button data-mode="note" data-rand="5">随机五组注释</button>',
            '<button data-mode="note" data-all="1">全部注释</button>',
            '</div></section>']

footer = '<footer>\n  <div class="kai">登幽州台歌</div>\n  <div>陈子昂 · 唐</div>\n</footer>'

dictate_html = '''<div class="dictate" id="dictate" hidden>
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
</div>'''

html = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>登幽州台歌</title>\n'
        '<meta name="description" content="唐陈子昂《登幽州台歌》逐句注释、译文、赏析，生僻字与易错词附注音，含背景、原文（背诵模式）、解读、赏析、积累、练习，适合课堂教学。">\n'
        '<style>' + css + '</style>\n</head>\n<body>\n\n'
        + hero + '\n\n' + nav + '\n\n<main class="wrap">\n\n'
        + "\n".join(bg) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(jl) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(app) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(acc) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(practice) + '\n\n'
        + footer + '\n</main>\n\n'
        + '<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>\n'
        + '<button class="top-btn" id="topBtn" title="回到顶部">↑</button>\n\n'
        + dictate_html + '\n\n'
        + '<script>\n' + js_main + '\n' + js_dict + '\n</script>\n\n'
        + '</body>\n</html>\n')

no_script = re.sub(r"<script>.*?</script>", "", html, flags=re.S)
body_text = re.sub(r"<[^>]+>", "", re.sub(r"<style>.*?</style>", "", no_script, flags=re.S))
assert body_text.count('"') == 0, "straight quotes in visible text: %d" % body_text.count('"')
assert "{LQ}" not in html and "{RQ}" not in html, "placeholder残留"
need = ["verseList", "fulltext", "btnAll", "btnRecite", "btnPrint", "btnShowAll", "fsSel", "annoPopup", "dictate", "topBtn", "mediaF1", "mediaF2"]
missing = [i for i in need if 'id="%s"' % i not in html]
assert not missing, "missing ids: %s" % missing
assert LS_KEY in js_main and "chibi_fs" not in js_main
for it in WORDS:
    assert not any(c in it["q"] for c in it["w"]), "leak: %s" % it["w"]
    assert it["q"].count("\u25a1") == len(it["w"]), "box mismatch: %s" % it["w"]
    assert it["tip"] and it["tip"] != it["w"], "tip bad: %s" % it["w"]

anno_count = html.count('class="anno-word"')
print("登幽州台歌 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), anno_count, len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
