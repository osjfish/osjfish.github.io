# -*- coding: utf-8 -*-
"""生成《假如生活欺骗了你》课件（外国现代诗，短篇，逐句解读）。"""
import io, json, re

SRC = r"D:\App\Apps\yanshi\chibi-dumu.html"
OUT = r"D:\App\Apps\yanshi\jiarushenghuoqipianleni-puxijin.html"
LS_KEY = "jiarushenghuo_fs"

LQ = "\u201c"
RQ = "\u201d"

def A(word, note):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)

# 逐句数据：(原文带注释标记, 内容概括, 手法分析)
CARDS = [
("假如生活" + A("欺骗","用拟人的手法，将生活比作会欺骗人的对象，亲切而生动") + "了你，",
 "开篇直接点题，以一个假设的情境引入——假如生活欺骗了你。",
 "以" + LQ + "欺骗" + RQ + "一词拟人，将抽象的生活挫折具象化为一种欺骗行为，语气平等亲切，如同朋友间的对话。"),
("不要" + A("悲伤","悲痛哀伤") + "，不要" + A("心急","心里急躁") + "！",
 "面对生活的欺骗，诗人给出的第一个劝告：不要悲伤，不要心急。",
 "两个" + LQ + "不要" + RQ + "构成反复，语气坚定而亲切，以祈使句直接劝告，如长者叮咛、朋友劝慰。"),
(A("忧郁","忧伤愁闷") + "的日子里须要" + A("镇静","情绪稳定或平静") + "：",
 "在忧郁的日子里，需要保持镇静。",
 "LQ" + "须要" + RQ + "比" + LQ + "需要" + RQ + "语气更重，强调一种必须做到的态度；冒号引出下文的信念。"),
("相信吧，快乐的日子将会" + A("来临","来到、到来") + "。",
 "诗人给出信念：相信快乐的日子一定会到来。",
 "LQ" + "相信吧" + RQ + "以呼告语气强化劝告的力量；" + LQ + "将会来临" + RQ + "用将来时态表达对未来的确信，积极乐观。"),
(A("心儿","心，口语化的亲切说法") + "永远" + A("向往","因热爱、羡慕某种事物或境界而希望得到或达到") + "着未来；",
 "第二节转入内心：心永远向往着未来。",
 "LQ" + "心儿" + RQ + "是口语化的昵称，比" + LQ + "心" + RQ + "更亲切；" + LQ + "永远" + RQ + "强调时间上的持续性，表达对未来的执着信念。"),
("现在却常是忧郁：",
 "然而现实中，现在却常常充满忧郁。",
 "LQ" + "却" + RQ + "表转折，将" + LQ + "向往未来" + RQ + "与" + LQ + "现在忧郁" + RQ + "对照，承认现实的艰难，使乐观不流于空洞。"),
("一切都是" + A("瞬息","一眨眼一呼吸的短时间，形容极短的时间") + "，一切都将会过去；",
 "诗人指出：一切艰难困苦都是短暂的，都会过去。",
 "两个" + LQ + "一切" + RQ + "构成反复，强调普遍性；" + LQ + "瞬息" + RQ + "与" + LQ + "将会过去" + RQ + "呼应，从时间维度消解痛苦的绝对性。"),
("而那过去了的，就会成为" + A("亲切","亲近、亲密") + "的" + A("怀恋","怀念、留恋") + "。",
 "全诗点睛：过去的痛苦，终将成为亲切的怀恋。",
 "LQ" + "亲切的怀恋" + RQ + "是全诗的诗眼——痛苦的经历一旦过去，回望时便带有了温情与意义。这是哲理的升华，也是积极人生态度的最高表达。"),
]

FULLTEXT = [
 "假如生活欺骗了你，",
 "不要悲伤，不要心急！",
 "忧郁的日子里须要镇静：",
 "相信吧，快乐的日子将会来临。",
 "心儿永远向往着未来；",
 "现在却常是忧郁：",
 "一切都是瞬息，一切都将会过去；",
 "而那过去了的，就会成为亲切的怀恋。",
]

BG_LEAD = [
 "普希金（1799—1837），俄国伟大的诗人、小说家，被誉为" + LQ + "俄罗斯文学之父" + RQ + "。1825年，普希金被幽禁在米哈伊洛夫斯克村，此时他的女友奥西波娃要去送别被流放的丈夫，临行前向诗人索诗留念。普希金提笔写下这首短诗，题在奥西波娃的纪念册上。",
 "全诗仅两节八句，以平等亲切的劝告口吻写成，没有具体意象，却蕴含深刻的人生哲理。诗人以自己的逆境体验为底色，告诉读者：面对生活的挫折，不要悲伤，不要心急，要相信快乐的日子终将到来；而那过去了的痛苦，终会成为亲切的怀恋。这首诗是普希金最广为流传的作品之一，也是世界诗歌史上最著名的哲理短诗之一。",
]

AUTHOR = [
 "亚历山大·谢尔盖耶维奇·普希金（1799—1837），俄国伟大的诗人、小说家，19世纪俄国浪漫主义文学的主要代表，同时也是现实主义文学的奠基人，被誉为" + LQ + "俄罗斯文学之父" + RQ + LQ + "俄罗斯诗歌的太阳" + RQ + "。他的创作对俄国文学和语言的发展影响深远，高尔基称他为" + LQ + "一切开端的开端" + RQ + "。",
 "普希金出身贵族，从小受到良好的教育。他一生创作丰富，代表作有诗歌《自由颂》《致恰达耶夫》《致大海》《假如生活欺骗了你》，诗体小说《叶甫盖尼·奥涅金》，小说《上尉的女儿》《黑桃皇后》等。1837年，普希金因与丹特士决斗而重伤不治，年仅38岁。",
]

STORY = [
 ("题诗纪念册","1825年，普希金被幽禁在米哈伊洛夫斯克村。他的女友奥西波娃要去西伯利亚看望被流放的丈夫，临行前向普希金索诗留念。诗人提笔在她的纪念册上写下了这首短诗。"),
 ("逆境中的信念","写作此诗时，普希金正处于人生的低谷：因写作歌颂自由的诗歌被沙皇政府流放，后又被幽禁在乡村，与外界隔绝。然而正是在这样的逆境中，诗人写出了这首充满乐观精神的哲理诗——他自己就是" + LQ + "不要悲伤，不要心急" + RQ + "的践行者。"),
 ("翻译与版本","本诗以戈宝权的译本为准，是统编版语文教材七年级下册的课文。戈宝权（1913—2000）是中国著名的翻译家、外国文学研究家，他的俄苏文学翻译影响深远。"),
 ("世界影响","这首诗仅有两节八句，却被译成数十种文字，在全世界广为流传。它以最朴素的语言表达了最深刻的人生哲理，成为无数人在逆境中自我勉励的座右铭。"),
]

APP_ART = [
 ("平等亲切的劝告语气","全诗以第二人称" + LQ + "你" + RQ + "写成，诗人不是高高在上的说教者，而是与读者平等对话的朋友。" + LQ + "不要悲伤，不要心急" + RQ + LQ + "相信吧" + RQ + "——祈使句与呼告语的运用，使全诗如长者叮咛、朋友劝慰，亲切而有力量。"),
 ("积极乐观的人生态度","面对生活的欺骗，诗人没有愤世嫉俗，也没有消极沉沦，而是给出了坚定的劝告：不要悲伤，不要心急，要镇静，要相信快乐的日子终将到来。这种积极乐观的态度贯穿全诗，是诗人在逆境中依然保持的信念。"),
 ("深刻的哲理意味","全诗最深刻的哲理在末句：" + LQ + "而那过去了的，就会成为亲切的怀恋。" + RQ + "痛苦的经历一旦成为过去，回望时便不再是纯粹的痛苦，而是带有了温情与意义——正是那些艰难的时刻，塑造了我们的人生。这是对苦难的审美升华，也是对人生的深刻洞察。"),
 ("无意象的哲理诗","全诗没有一个具体的意象（没有景物、没有人物、没有场景），纯以抽象的道理和情感动人。这在诗歌中是难得的——大多数诗歌需要意象来承载情感，而本诗仅凭语言的节奏和道理的深刻就打动了无数读者，足见诗人的功力。"),
]

APP_FAME = [
 ("假如生活欺骗了你，不要悲伤，不要心急！",
  "开篇直接点题，以假设的情境引入，随即给出坚定的劝告。两个" + LQ + "不要" + RQ + "构成反复，语气斩钉截铁，如朋友在耳边叮咛。" + LQ + "欺骗" + RQ + "一词拟人，将生活的挫折具象化，使抽象的道理有了温度。"),
 ("忧郁的日子里须要镇静：相信吧，快乐的日子将会来临。",
  "在承认忧郁的同时，给出了应对之道——镇静，以及信念——相信快乐终将到来。" + LQ + "须要" + RQ + "比" + LQ + "需要" + RQ + "语气更重，强调这是一种必须做到的态度。" + LQ + "相信吧" + RQ + "以呼告强化力量，" + LQ + "将会来临" + RQ + "用将来时表达确信。"),
 ("一切都是瞬息，一切都将会过去；而那过去了的，就会成为亲切的怀恋。",
  "全诗的精华与诗眼所在。两个" + LQ + "一切" + RQ + "强调普遍性，" + LQ + "瞬息" + RQ + "与" + LQ + "将会过去" + RQ + "从时间维度消解痛苦的绝对性。末句" + LQ + "亲切的怀恋" + RQ + "是哲理的升华——苦难一旦过去，回望时便有了温情与意义。这是对人生的深刻洞察，也是全诗最广为传诵的名句。"),
]

APP_THEME = [
 "本诗以平等亲切的劝告口吻，表达了诗人面对生活挫折时积极乐观的人生态度。诗人告诉读者：假如生活欺骗了你，不要悲伤，不要心急，在忧郁的日子里要保持镇静，要相信快乐的日子终将到来；心儿永远向往着未来，而一切艰难困苦都是短暂的，终将过去；更重要的是，那过去了的痛苦，终会成为亲切的怀恋。",
 "全诗没有具体意象，纯以哲理和情感动人，是世界诗歌史上最著名的哲理短诗之一。它所传达的积极乐观精神和对苦难的审美升华，使它成为无数人在逆境中自我勉励的座右铭，也体现了普希金作为" + LQ + "俄罗斯诗歌的太阳" + RQ + "的人格力量。",
]

ACC = [
 ("重点词语", [
   ("欺骗","用虚伪的言行隐瞒真相，使人上当。诗中拟人，指生活中的挫折与不顺。"),
   ("悲伤","悲痛哀伤。"),
   ("心急","心里急躁。"),
   ("忧郁","忧伤愁闷。"),
   ("镇静","情绪稳定或平静。"),
   ("来临","来到、到来。"),
   ("向往","因热爱、羡慕某种事物或境界而希望得到或达到。"),
   ("瞬息","一眨眼一呼吸的短时间，形容极短的时间。"),
   ("亲切","亲近、亲密。"),
   ("怀恋","怀念、留恋。"),
 ]),
 ("用字与读音", [
   ("欺","读 qī，一声；易误读为 qí。"),
   ("骗","读 piàn，四声；" + LQ + "欺骗" + RQ + "不要写成" + LQ + "欺偏" + RQ + "。"),
   ("郁","读 yù，四声；" + LQ + "忧郁" + RQ + "不要写成" + LQ + "忧豫" + RQ + "。"),
   ("镇","读 zhèn，四声；金字旁，" + LQ + "镇静" + RQ + "不要写成" + LQ + "震静" + RQ + "。"),
   ("瞬","读 shùn，四声；目字旁，" + LQ + "瞬息" + RQ + "形容时间极短。"),
   ("恋","读 liàn，四声；" + LQ + "怀恋" + RQ + "不要写成" + LQ + "怀峦" + RQ + "。"),
 ]),
 ("修辞方法", [
   ("拟　人", LQ + "假如生活欺骗了你" + RQ + "——将" + LQ + "生活" + RQ + "拟人化，仿佛生活是一个会欺骗人的对象，使抽象的道理具象化、亲切化。"),
   ("反　复", LQ + "不要悲伤，不要心急" + RQ + "——两个" + LQ + "不要" + RQ + "反复，强化劝告的语气；" + LQ + "一切都是瞬息，一切都将会过去" + RQ + "——两个" + LQ + "一切" + RQ + "反复，强调普遍性。"),
   ("对　比", LQ + "心儿永远向往着未来；现在却常是忧郁" + RQ + "——" + LQ + "未来" + RQ + "与" + LQ + "现在" + RQ + "对比，" + LQ + "向往" + RQ + "与" + LQ + "忧郁" + RQ + "对比，在对照中凸显信念的力量。"),
   ("呼　告", LQ + "相信吧" + RQ + "——直接呼告读者，强化劝告的感染力，使读者感到诗人就在面前说话。"),
 ]),
 ("写作借鉴", [
   ("以劝告口吻说理","全诗以第二人称" + LQ + "你" + RQ + "写成，诗人不是说教者，而是与读者平等对话的朋友。这种口吻使抽象的哲理变得亲切可感。"),
   ("无意象的哲理表达","全诗没有一个具体意象，纯以道理和情感动人。这需要极强的语言功力——用最朴素的语言表达最深刻的道理。"),
   ("层层递进的结构","第一节：面对挫折的态度（不要悲伤、不要心急、要镇静、要相信）；第二节：内心的信念（向往未来、承认现实、一切都会过去、过去的成为怀恋）。由外到内，由态度到哲理，层层递进。"),
   ("积极乐观的基调","全诗虽写" + LQ + "生活欺骗" + RQ + LQ + "忧郁" + RQ + "，但基调始终是积极乐观的。承认现实的艰难，但不被现实压倒——这是本诗最可贵的精神。"),
 ]),
]

WORDS = [
 {"w":"欺","py":"qī","q":"假如生活□骗了你，","tip":"「欺」欠字旁，读 qī 一声；勿写「期」（月字旁）"},
 {"w":"骗","py":"piàn","q":"假如生活欺□了你，","tip":"「骗」马字旁，读 piàn 四声；勿写「偏」（单人旁）"},
 {"w":"悲","py":"bēi","q":"不要□伤，不要心急！","tip":"「悲」心字底，读 bēi；勿写「辈」（车字旁）"},
 {"w":"郁","py":"yù","q":"□的日子里须要镇静：","tip":"「郁」右耳旁，读 yù 四声；「忧郁」勿写「忧豫」"},
 {"w":"镇","py":"zhèn","q":"忧郁的日子里须要□静：","tip":"「镇」金字旁，读 zhèn；「镇静」勿写「震静」（雨字头）"},
 {"w":"瞬","py":"shùn","q":"一切都是□息，一切都将会过去；","tip":"「瞬」目字旁，读 shùn 四声；形容时间极短，勿写「顺」"},
 {"w":"恋","py":"liàn","q":"就会成为亲切的怀□。","tip":"「恋」心字底，读 liàn 四声；「怀恋」勿写「怀峦」（山字头）"},
]

NOTES = [
 {"w":"欺骗","a":"用虚伪的言行隐瞒真相使人上当；诗中拟人，指生活中的挫折","q":"假如生活欺骗了你，"},
 {"w":"悲伤","a":"悲痛哀伤","q":"不要悲伤，不要心急！"},
 {"w":"心急","a":"心里急躁","q":"不要悲伤，不要心急！"},
 {"w":"忧郁","a":"忧伤愁闷","q":"忧郁的日子里须要镇静："},
 {"w":"镇静","a":"情绪稳定或平静","q":"忧郁的日子里须要镇静："},
 {"w":"来临","a":"来到、到来","q":"相信吧，快乐的日子将会来临。"},
 {"w":"心儿","a":"心，口语化的亲切说法","q":"心儿永远向往着未来；"},
 {"w":"向往","a":"因热爱、羡慕而希望得到或达到","q":"心儿永远向往着未来；"},
 {"w":"瞬息","a":"一眨眼一呼吸的短时间，形容极短","q":"一切都是瞬息，一切都将会过去；"},
 {"w":"亲切","a":"亲近、亲密","q":"就会成为亲切的怀恋。"},
 {"w":"怀恋","a":"怀念、留恋","q":"就会成为亲切的怀恋。"},
]

VIDEOS = [
 ("经典诗歌朗诵《假如生活欺骗了你》普希金","BV1F3411M7oL","经典诗歌朗诵《假如生活欺骗了你》"),
 ("普希金：俄罗斯文学之父","BV1ZjpweJEd4","普希金人物介绍"),
]

# ===== 读取框架 =====
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]

# 提取主JS（到DICT_WORDS之前）
js_main = src[src.index("<script>") + 8 : src.index("var DICT_WORDS")]
js_main = js_main.replace("chibi_fs", LS_KEY)

# 提取听写JS（DICT_WORDS到script结束）
js_dict = src[src.index("var DICT_WORDS") : src.index("</script>", src.index("var DICT_WORDS"))]
js_dict = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", js_dict, flags=re.S)
js_dict = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", js_dict, flags=re.S)

def video(i, h4, bvid, atitle):
    return ('<div class="media"><h4>%s</h4>'
            '<iframe id="mediaF%d" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>'
            '<a href="https://www.bilibili.com/video/%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF%d">全屏播放</button></div>'
            % (h4, i, bvid, atitle, bvid, i))

# ===== 构建各区块 =====
hero = '<header class="hero" id="top">\n  <div class="hero-inner">\n    <div class="hero-side">俄国·普希金</div>\n    <h1 class="hero-title">假如生活欺骗了你</h1>\n  </div>\n</header>'

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

# 解读区
jl = ['<section id="jielu">',
      '<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 内容 / 手法</span></div>',
      '<div class="sec-sub">全诗两节八句，以平等亲切的劝告口吻写成，没有具体意象，却蕴含深刻的人生哲理。每句含<b>注释</b>（点击可查看）、内容概括与手法分析。短篇诗歌不分部分，直接逐句解读。</div>',
      '<div class="texttools">',
      '<button id="btnShowAll" class="off" style="display:none">显示全部</button>',
      '</div>',
      '<div class="box media-box">',
      '<h3>朗诵 · 拓展</h3>',
      '<div class="media-grid">']
for i, (h4, bvid, at) in enumerate(VIDEOS):
    jl.append(video(i + 1, h4, bvid, at))
jl.append('</div></div>')

# fulltext（背诵模式）
jl.append('<div class="fulltext poem" id="fulltext" style="display:none">')
for idx, line in enumerate(FULLTEXT, 1):
    jl.append('<div class="pl"><span class="no">%d</span>%s</div>' % (idx, line))
jl.append('</div>')

# verse cards
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

# 赏析区
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

# 积累区
acc = ['<section id="acc">',
       '<div class="sec-head"><h2>积 累</h2><span class="no">词语 · 读音 · 修辞 · 写作</span></div>']
for cat, items in ACC:
    acc.append('<div class="box"><h3>%s</h3>' % cat)
    acc.append('<div class="tw"><table>')
    acc.append('<tr><th>词语</th><th>释义</th></tr>')
    for w, d in items:
        acc.append('<tr><td class="kai">%s</td><td>%s</td></tr>' % (w, d))
    acc.append('</table></div></div>')
acc.append('</section>')

# 练习区
practice = ['<section id="practice">',
            '<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写 · 字词 / 词语</span></div>',
            '<div class="sec-sub">以全篇<b>易错字词</b>与<b>重点词语</b>为题库，点击按钮进入<b>全屏听写</b>：先看提示在纸上默写，再核对答案。随机五组适合随堂小测，全部适合系统复习。</div>',
            '<div class="ptools">',
            '<button data-mode="word" data-rand="5">随机五组字形</button>',
            '<button data-mode="word" data-all="1">全部字形</button>',
            '<button data-mode="note" data-rand="5">随机五组词语</button>',
            '<button data-mode="note" data-all="1">全部词语</button>',
            '</div></section>']

footer = '<footer>\n  <div class="kai">假如生活欺骗了你</div>\n  <div>普希金 · 俄国 · 戈宝权译</div>\n</footer>'

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

# ===== 组装 =====
html = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>假如生活欺骗了你</title>\n'
        '<meta name="description" content="俄国普希金《假如生活欺骗了你》逐句解读、注释、赏析，含背景、原文（背诵模式）、解读、赏析、积累、练习，适合课堂教学。">\n'
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

# ===== 自检 =====
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
print("假如生活欺骗了你 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), anno_count, len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
