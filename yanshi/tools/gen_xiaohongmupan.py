# -*- coding: utf-8 -*-
"""生成《萧红墓畔口占》戴望舒课件（短篇现代诗，逐句解读）。"""
import io, json, re

SRC = r"D:\App\Apps\yanshi\zuguoawoqinaidezuguo-shuting.html"
OUT = r"D:\App\Apps\yanshi\xiaohongmupankouzhan-daiwangshu.html"
LS_KEY = "xiaohongmupan_fs"

LQ = "\u201c"
RQ = "\u201d"

def A(word, note):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)

CARDS = [
("走六小时" + A("寂寞","孤单冷清") + "的" + A("长途","遥远的路程") + "，",
 "首句写诗人跋山涉水前往萧红墓前的行程：走了六小时，一路寂寞。",
 LQ + "六小时" + RQ + "以具体的时间写路途之远，也写诗人心中思念之深；" + LQ + "寂寞" + RQ + "既指旅途中的孤单，也指失去友人后的孤寂；" + LQ + "长途" + RQ + "双关，既是实际的路程，也是人生与阴阳相隔的遥远距离。"),
("到你" + A("头边","头旁、墓前") + "放一束" + A("红山茶","红色的山茶花，花色艳红，花期在冬春之际") + "，",
 "次句写诗人到达墓前，将一束红山茶放在萧红的墓前。",
 LQ + "你" + RQ + "以第二人称直呼萧红，如对友人低语，亲切而沉痛；" + LQ + "红山茶" + RQ + "是全诗的核心意象——花色艳红，象征萧红热烈的生命和才华，也寄托着诗人的敬意与怀念；" + LQ + "放" + RQ + "一个朴素的动作，蕴含着深沉的情感。"),
("我" + A("等待","等候、期盼") + "着，" + A("长夜漫漫","形容夜晚漫长无边") + "，",
 "第三句由动作转入心境：诗人在墓前等待着，而长夜漫漫无尽。",
 LQ + "我等待着" + RQ + "——等待什么？诗人没有明说，留下空白：或许是等待与友人的灵魂对话，或许是等待黎明的到来，或许是等待一个更公平的时代；" + LQ + "长夜漫漫" + RQ + "既指实际的夜晚，也暗指抗战时期黑暗的社会现实，以及诗人心中无边的悲痛。"),
("你却" + A("卧听","躺着听") + "着" + A("海涛","海浪的声音") + A("闲话","闲谈、随意的话语") + "。",
 "末句是全诗的诗眼：萧红已长眠于地下，却仿佛在卧听海涛闲话——一种超然的宁静。",
 LQ + "却" + RQ + "表转折，将" + LQ + "我等待着" + RQ + "的焦灼与" + LQ + "你卧听" + RQ + "的宁静对照；" + LQ + "卧听海涛闲话" + RQ + "以拟人的手法，写萧红虽死犹生——她卧在墓中，仿佛在悠闲地听着海涛闲谈，超然于生死与时代之外。这一句将沉痛的悼念升华为一种宁静的永恒，意蕴深远，余味无穷。"),
]

FULLTEXT = [
 "走六小时寂寞的长途，",
 "到你头边放一束红山茶，",
 "我等待着，长夜漫漫，",
 "你却卧听着海涛闲话。",
]

BG_LEAD = [
 "《萧红墓畔口占》是戴望舒的代表作之一，1944年11月20日写于香港。当时萧红已病逝两年，戴望舒前往香港浅水湾萧红墓前凭吊，写下这首短诗。全诗仅四句，却以凝练的语言、深沉的情感和丰富的意象，成为中国现代诗歌史上悼念友人的经典之作。",
 "诗歌描绘了诗人跋涉六小时前往萧红墓前，献上一束红山茶，在漫漫长夜中等待，而萧红却仿佛在卧听海涛闲话的场景。诗中既有对友人早逝的沉痛悼念，也有对友人超然人格的赞美，更暗含着对黑暗时代的愤懑。" + LQ + "红山茶" + RQ + LQ + "长夜" + RQ + LQ + "海涛" + RQ + "等意象，使这首短诗意蕴丰富、余味无穷。",
]

AUTHOR = [
 "戴望舒（1905—1950），原名戴朝安，又名戴梦鸥，浙江杭县（今杭州）人，中国现代著名诗人、翻译家，象征派诗歌的代表人物，被誉为" + LQ + "雨巷诗人" + RQ + "。1923年入上海大学中文系，1925年入震旦大学学习法语，1932年赴法国留学。",
 "戴望舒的诗歌深受法国象征派影响，善于以含蓄的意象、朦胧的意境表达细腻的情感。1928年发表《雨巷》一诗，一举成名。1930年代后，他的诗风逐渐从象征主义转向现实主义，关注社会现实和人民疾苦。主要作品有诗集《我的记忆》《望舒草》《望舒诗稿》《灾难的岁月》等。1950年2月28日，戴望舒因哮喘病在北京逝世，年仅45岁。",
]

STORY = [
 ("萧红之死","萧红（1911—1942），原名张廼莹，黑龙江呼兰人，中国现代著名女作家。1942年1月22日，萧红因肺病和误诊在香港玛丽医院病逝，年仅31岁。她的遗体火化后，骨灰由友人端木蕻良葬于香港浅水湾丽都花园前的坡地上。1944年11月，戴望舒前往浅水湾凭吊萧红墓，写下了这首《萧红墓畔口占》。"),
 ("口占的含义","" + LQ + "口占" + RQ + "指不起草、随口吟成的诗。这首诗是戴望舒在萧红墓前即兴吟成的，没有经过反复推敲，却正因为如此，情感格外真挚自然。全诗语言朴素，没有华丽的辞藻，却字字含情，句句含泪。"),
 ("红山茶的寓意","萧红墓在香港浅水湾，面向大海。墓边长有山茶树，冬春之际开出艳红的花朵。戴望舒在墓前放一束红山茶，既是就地取材，也是精心选择——红山茶花色艳红，象征萧红热烈的生命和才华；花期在寒冬，象征萧红在苦难中依然绽放的精神。"),
 ("时代背景","1944年正值抗日战争最艰苦的时期。香港于1941年沦陷，戴望舒曾因参加抗日活动被日本宪兵逮捕入狱，受尽折磨。" + LQ + "长夜漫漫" + RQ + "既是写墓前的夜晚，也是暗指黑暗的时代。诗人在这样的时代悼念友人，心中的悲痛与愤懑可想而知。"),
]

APP_ART = [
 ("朴素的语言","全诗无华丽辞藻，纯用白描。" + LQ + "走六小时" + RQ + LQ + "放一束" + RQ + LQ + "等待着" + RQ + LQ + "卧听着" + RQ + "，都是最朴素的口语，却蕴含着最深沉的情感。这种以朴素写深情的手法，正是戴望舒后期诗歌的特点。"),
 ("丰富的意象","诗中" + LQ + "红山茶" + RQ + LQ + "长夜" + RQ + LQ + "海涛" + RQ + "三个核心意象，各有深意：红山茶象征热烈的生命，长夜暗指黑暗的时代，海涛代表永恒的自然。三个意象交织在一起，使这首仅四句的短诗意蕴丰富。"),
 ("对比的手法","诗中多处运用对比：" + LQ + "我等待着" + RQ + "的焦灼与" + LQ + "你卧听" + RQ + "的宁静对比；" + LQ + "长夜漫漫" + RQ + "的黑暗与" + LQ + "红山茶" + RQ + "的艳红对比；生者的痛苦与死者的超然对比。这些对比使诗歌的情感张力大大增强。"),
 ("第二人称的运用","全诗以第二人称" + LQ + "你" + RQ + "称呼萧红，如对友人低语，亲切而沉痛。" + LQ + "到你头边" + RQ + LQ + "你却卧听" + RQ + "，仿佛萧红就在面前，诗人在与她对话。这种写法拉近了生与死的距离，也使情感更加真挚动人。"),
 ("含蓄的结尾","末句" + LQ + "你却卧听着海涛闲话" + RQ + "是全诗的点睛之笔。诗人没有直接写悲痛，而是以一个宁静的画面收尾——萧红卧在墓中，仿佛在悠闲地听海涛闲谈。这种将沉痛升华为宁静的写法，使诗歌余味无穷，也体现了戴望舒作为象征派诗人的含蓄之美。"),
]

APP_FAME = [
 ("走六小时寂寞的长途，到你头边放一束红山茶，",
  "前两句叙事，写诗人跋涉六小时前往萧红墓前，献上一束红山茶。" + LQ + "六小时" + RQ + "以具体时间写路途之远，也写思念之深；" + LQ + "寂寞" + RQ + "既指旅途孤单，也指失友之痛；" + LQ + "红山茶" + RQ + "是核心意象，花色艳红，象征萧红热烈的生命和才华。" + LQ + "你" + RQ + "以第二人称直呼萧红，如对友人低语，亲切而沉痛。这两句纯用白描，没有一个多余的字，却字字含情。"),
 ("我等待着，长夜漫漫，你却卧听着海涛闲话。",
  "后两句是全诗的精华。" + LQ + "我等待着" + RQ + "留下空白——等待什么？与友人灵魂对话？等待黎明？等待公平的时代？" + LQ + "长夜漫漫" + RQ + "既指夜晚，也暗指黑暗的抗战时代。末句" + LQ + "你却卧听着海涛闲话" + RQ + "以拟人和对比，将萧红的超然宁静与诗人的焦灼等待对照，将沉痛的悼念升华为一种永恒的宁静。这是中国现代诗歌中最经典的结尾之一。"),
]

APP_THEME = [
 "《萧红墓畔口占》通过描绘诗人跋涉六小时前往萧红墓前献花、在漫漫长夜中等待的场景，表达了对友人萧红早逝的沉痛悼念，对萧红超然人格的赞美，以及对黑暗时代的愤懑。",
 "全诗仅四句，却蕴含着丰富的情感和深刻的意蕴。" + LQ + "红山茶" + RQ + "象征热烈的生命，" + LQ + "长夜" + RQ + "暗指黑暗的时代，" + LQ + "海涛闲话" + RQ + "代表永恒的宁静。诗人将个人的悲痛置于广阔的自然和时代背景之中，使这首短诗具有了超越个人情感的普遍意义，成为中国现代诗歌史上悼念友人的经典之作。",
]

ACC = [
 ("重点词语", [
   ("寂寞","孤单冷清。"),
   ("长途","遥远的路程。"),
   ("头边","头旁、墓前。"),
   ("红山茶","红色的山茶花，花色艳红，花期在冬春之际。"),
   ("等待","等候、期盼。"),
   ("长夜漫漫","形容夜晚漫长无边。"),
   ("卧听","躺着听。"),
   ("海涛","海浪的声音。"),
   ("闲话","闲谈、随意的话语。"),
 ]),
 ("用字与读音", [
   ("寂","读 jì，四声；" + LQ + "寂寞" + RQ + "不要写成" + LQ + "寂莫" + RQ + "（" + LQ + "莫" + RQ + "草字头）。"),
   ("寞","读 mò，四声；" + LQ + "寂寞" + RQ + "都是宝盖头，不要写成" + LQ + "寂漠" + RQ + "（" + LQ + "漠" + RQ + "三点水）。"),
   ("途","读 tú，二声；走之底，" + LQ + "长途" + RQ + "不要写成" + LQ + "长涂" + RQ + "（" + LQ + "涂" + RQ + "三点水）。"),
   ("茶","读 chá，二声；草字头+人+木，" + LQ + "山茶" + RQ + "不要写成" + LQ + "山荼" + RQ + "（" + LQ + "荼" + RQ + "读 tú）。"),
   ("漫","读 màn，四声；三点水，" + LQ + "漫漫" + RQ + "形容漫长，不要写成" + LQ + "慢慢" + RQ + "（" + LQ + "慢" + RQ + "竖心旁，指速度慢）。"),
   ("涛","读 tāo，一声；三点水，" + LQ + "海涛" + RQ + "不要写成" + LQ + "海滔" + RQ + "（" + LQ + "滔" + RQ + "三点水+舀，读 tāo，指大水弥漫）。"),
 ]),
 ("修辞方法", [
   ("白　描", LQ + "走六小时寂寞的长途，到你头边放一束红山茶" + RQ + "——纯用白描手法，以最朴素的语言写最真挚的情感，没有一个多余的字。"),
   ("象　征", LQ + "红山茶" + RQ + "——象征萧红热烈的生命和才华；" + LQ + "长夜漫漫" + RQ + "——象征黑暗的抗战时代；" + LQ + "海涛" + RQ + "——象征永恒的自然。"),
   ("对　比", LQ + "我等待着" + RQ + "的焦灼与" + LQ + "你卧听" + RQ + "的宁静对比；生者的痛苦与死者的超然对比；" + LQ + "长夜" + RQ + "的黑暗与" + LQ + "红山茶" + RQ + "的艳红对比。"),
   ("拟　人", LQ + "你却卧听着海涛闲话" + RQ + "——将已故的萧红拟人化，仿佛她在墓中悠闲地听海涛闲谈，超然于生死之外。"),
   ("双　关", LQ + "长夜漫漫" + RQ + "——既指实际的夜晚漫长，也暗指抗战时期黑暗的社会现实，一语双关。"),
 ]),
 ("写作借鉴", [
   ("以朴素写深情","全诗无华丽辞藻，纯用口语化的朴素语言，却蕴含着最深沉的情感。" + LQ + "走六小时" + RQ + LQ + "放一束" + RQ + "，简单的动作中蕴含着无尽的思念。这种以朴素写深情的手法，比直接抒情更有力量。"),
   ("意象的精心选择","" + LQ + "红山茶" + RQ + LQ + "长夜" + RQ + LQ + "海涛" + RQ + "三个意象，各有深意，又相互关联。红山茶是诗人献上的，长夜是诗人所处的，海涛是萧红所听的——三个意象将生者与死者、人与自然、现在与永恒联系在一起。"),
   ("留白的艺术","" + LQ + "我等待着" + RQ + "——等待什么？诗人没有明说，留下了广阔的想象空间。这种留白比直接说明更有感染力，读者可以根据自己的理解去填充。"),
   ("结尾的升华","末句" + LQ + "你却卧听着海涛闲话" + RQ + "将沉痛的悼念升华为一种宁静的永恒。诗人没有停留在悲痛上，而是以一个超然的画面收尾，使诗歌余味无穷。这种结尾的升华，是戴望舒作为象征派诗人的拿手好戏。"),
 ]),
 ("文化常识", [
   ("萧红","（1911—1942）原名张廼莹，黑龙江呼兰人，中国现代著名女作家。代表作有《生死场》《呼兰河传》《马伯乐》等。1942年1月22日病逝于香港，年仅31岁。"),
   ("口占","指不起草、随口吟成的诗。古代诗人常有" + LQ + "口占一绝" + RQ + "的说法，即当场随口吟成一首绝句。"),
   ("象征派","20世纪初传入中国的现代主义诗歌流派，源于法国。象征派诗歌强调用含蓄的意象、朦胧的意境表达内心的情感，反对直白的说教。戴望舒是中国象征派诗歌的代表人物。"),
   ("山茶花","常绿灌木或小乔木，冬春之际开花，花色有红、白、粉等。红山茶花色艳红，花期在寒冬，常被用来象征热烈的生命和不屈的精神。"),
 ]),
]

WORDS = [
 {"w":"寂寞","py":"jì mò","q":"走六小时□□的长途，","tip":"「寂寞」都是宝盖头；勿写「寂莫」（莫草字头）或「寂漠」（漠三点水）"},
 {"w":"途","py":"tú","q":"走六小时寂寞的长□，","tip":"「途」走之底+余，读 tú 二声；勿写「涂」（三点水）"},
 {"w":"茶","py":"chá","q":"到你头边放一束红山□，","tip":"「茶」草字头+人+木，读 chá；勿写「荼」（读 tú，草字头+余）"},
 {"w":"漫漫","py":"màn màn","q":"我等待着，长夜□□，","tip":"「漫」三点水，形容漫长；勿写「慢慢」（慢竖心旁，指速度慢）"},
 {"w":"卧","py":"wò","q":"你却□听着海涛闲话。","tip":"「卧」臣字旁+卜，读 wò 四声；勿写「卧」（「臥」为繁体）"},
 {"w":"涛","py":"tāo","q":"你却卧听着海□闲话。","tip":"「涛」三点水+寿，读 tāo 一声；勿写「滔」（三点水+舀，指大水弥漫）"},
]

NOTES = [
 {"w":"寂寞","a":"孤单冷清","q":"走六小时寂寞的长途，"},
 {"w":"长途","a":"遥远的路程","q":"走六小时寂寞的长途，"},
 {"w":"头边","a":"头旁、墓前","q":"到你头边放一束红山茶，"},
 {"w":"红山茶","a":"红色的山茶花，花色艳红，花期在冬春之际","q":"到你头边放一束红山茶，"},
 {"w":"等待","a":"等候、期盼","q":"我等待着，长夜漫漫，"},
 {"w":"长夜漫漫","a":"形容夜晚漫长无边","q":"我等待着，长夜漫漫，"},
 {"w":"卧听","a":"躺着听","q":"你却卧听着海涛闲话。"},
 {"w":"海涛","a":"海浪的声音","q":"你却卧听着海涛闲话。"},
 {"w":"闲话","a":"闲谈、随意的话语","q":"你却卧听着海涛闲话。"},
]

VIDEOS = [
 ("在城市随处读诗：萧红墓畔口占（戴望舒）","BV1J54y1B7hm","萧红墓畔口占读诗"),
 ("基础教育精品课《萧红墓畔口占》","BV1cN4y1X7eS","萧红墓畔口占精品课"),
]

# ===== 读取框架 =====
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]
js_main = src[src.index("<script>") + 8 : src.index("var DICT_WORDS")]
js_main = js_main.replace("zuguoawoqinaidezuguo_fs", LS_KEY)
js_dict = src[src.index("var DICT_WORDS") : src.index("</script>", src.index("var DICT_WORDS"))]
js_dict = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", js_dict, flags=re.S)
js_dict = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", js_dict, flags=re.S)

def video(i, h4, bvid, atitle):
    return ('<div class="media"><h4>%s</h4>'
            '<iframe id="mediaF%d" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>'
            '<a href="https://www.bilibili.com/video/%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF%d">全屏播放</button></div>'
            % (h4, i, bvid, atitle, bvid, i))

hero = '<header class="hero" id="top">\n  <div class="hero-inner">\n    <div class="hero-side">现代 · 戴望舒</div>\n    <h1 class="hero-title">萧红墓畔口占</h1>\n  </div>\n</header>'

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
      '<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 内容 / 手法</span></div>',
      '<div class="sec-sub">全诗四句，以凝练的语言描绘了诗人跋涉六小时前往萧红墓前献花、在漫漫长夜中等待的场景，蕴含着对友人早逝的沉痛悼念。每句含<b>注释</b>（点击可查看）、内容概括与手法分析。短篇诗歌不分部分，直接逐句解读。</div>',
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
for n, (orig, gai, shou) in enumerate(CARDS, 1):
    jl.append('<div class="verse" id="v%d">' % n)
    jl.append('  <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (n, orig))
    jl.append('  <details class="v-more">')
    jl.append('    <summary>内容 · 手法</summary>')
    jl.append('    <div class="d-body">')
    jl.append('      <div class="v-sec"><b class="v-label">内容概括</b>')
    jl.append('        <div class="v-trans">%s</div>' % gai)
    jl.append('      </div>')
    jl.append('      <div class="v-sec"><b class="v-label">手法分析</b>')
    jl.append('        <div class="d-body"><p>%s</p></div>' % shou)
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
       '<div class="sec-head"><h2>积 累</h2><span class="no">词语 · 读音 · 修辞 · 写作 · 文化</span></div>']
for cat, items in ACC:
    acc.append('<div class="box"><h3>%s</h3>' % cat)
    acc.append('<div class="tw"><table>')
    acc.append('<tr><th>词语</th><th>释义</th></tr>')
    for w, d in items:
        acc.append('<tr><td class="kai">%s</td><td>%s</td></tr>' % (w, d))
    acc.append('</table></div></div>')
acc.append('</section>')

practice = ['<section id="practice">',
            '<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写 · 字形 / 词语</span></div>',
            '<div class="sec-sub">以全篇<b>易错字词</b>与<b>重点词语</b>为题库，点击按钮进入<b>全屏听写</b>：先看提示在纸上默写，再核对答案。随机五组适合随堂小测，全部适合系统复习。</div>',
            '<div class="ptools">',
            '<button data-mode="word" data-rand="5">随机五组字形</button>',
            '<button data-mode="word" data-all="1">全部字形</button>',
            '<button data-mode="note" data-rand="5">随机五组词语</button>',
            '<button data-mode="note" data-all="1">全部词语</button>',
            '</div></section>']

footer = '<footer>\n  <div class="kai">萧红墓畔口占</div>\n  <div>戴望舒 · 现代 · 悼念友人的经典短诗</div>\n  <div>人教版九年级语文下册课文</div>\n</footer>'

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
        '<title>萧红墓畔口占 · 戴望舒</title>\n'
        '<meta name="description" content="现代戴望舒《萧红墓畔口占》逐句解读、注释、赏析，含背景、原文（背诵模式）、解读、赏析、积累、练习，适合课堂教学。">\n'
        '<style>' + css + '</style>\n</head>\n<body data-fs="100">\n\n'
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

# ===== 自检 =====
no_script = re.sub(r"<script>.*?</script>", "", html, flags=re.S)
body_text = re.sub(r"<[^>]+>", "", re.sub(r"<style>.*?</style>", "", no_script, flags=re.S))
assert body_text.count('"') == 0, "straight quotes in visible text: %d" % body_text.count('"')
assert "{LQ}" not in html and "{RQ}" not in html, "placeholder残留"
need = ["verseList", "fulltext", "btnAll", "btnRecite", "btnPrint", "btnShowAll", "fsSel", "annoPopup", "dictate", "topBtn", "mediaF1", "mediaF2"]
missing = [i for i in need if 'id="%s"' % i not in html]
assert not missing, "missing ids: %s" % missing
assert LS_KEY in js_main and "zuguoawoqinaidezuguo_fs" not in js_main
for it in WORDS:
    assert not any(c in it["q"] for c in it["w"]), "leak: %s" % it["w"]
    assert it["q"].count("\u25a1") == len(it["w"]), "box mismatch: %s" % it["w"]
    assert it["tip"] and it["tip"] != it["w"], "tip bad: %s" % it["w"]

anno_count = html.count('class="anno-word"')
print("萧红墓畔口占 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), anno_count, len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
