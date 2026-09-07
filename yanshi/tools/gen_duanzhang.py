# -*- coding: utf-8 -*-
"""生成《断章》卞之琳课件（短篇现代诗，逐句解读）。"""
import io, json, re

SRC = r"D:\App\Apps\yanshi\zuguoawoqinaidezuguo-shuting.html"
OUT = r"D:\App\Apps\yanshi\duanzhang-bianzhilin.html"
LS_KEY = "duanzhang_fs"

LQ = "\u201c"
RQ = "\u201d"

def A(word, note):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)

CARDS = [
("你站在" + A("桥","架在水面上的通道") + "上" + A("看风景","观赏景色") + "，",
 "首句设定场景：你站在桥上，观赏着眼前的风景。",
 LQ + "你" + RQ + "是诗中的主体，" + LQ + "站在桥上" + RQ + "是一个经典的观景位置；" + LQ + "看风景" + RQ + "点明" + LQ + "你" + RQ + "的动作——你是观察者，风景是被观察者。这一句看似平常，却为下一句的转折埋下了伏笔。"),
(A("看风景的人","观赏景色的人，指楼上的人") + "在楼上看你。",
 "次句转折：当你在桥上看风景时，楼上看风景的人正在看着你。",
 LQ + "看风景的人" + RQ + "与上句" + LQ + "看风景" + RQ + "构成顶真（前一句末尾的词语在后一句开头重复），使两句紧密相连；" + LQ + "在楼上看你" + RQ + "完成了视角的转换——你从观察者变成了被观察者。这一句是全诗哲理的起点：每个人既是看风景的人，也是别人眼中的风景。"),
(A("明月","明亮的月亮") + A("装饰","在身体或物体的表面加些附属的东西，使美观") + "了你的" + A("窗子","窗户") + "，",
 "第三句由白天转入夜晚：明月的银辉洒进你的窗子，装饰了你的窗户。",
 LQ + "明月" + RQ + "是中国古典诗歌中最经典的意象之一，象征美好、思念、永恒；" + LQ + "装饰" + RQ + "一词将明月拟人化，仿佛明月是一位艺术家，精心装点着你的窗子；" + LQ + "你的窗子" + RQ + "是你的私人空间，明月的进入使这个空间变得美好而诗意。"),
("你装饰了别人的" + A("梦","睡眠时体内体外各种刺激引起的表象活动") + "。",
 "末句是全诗的诗眼：你装饰了别人的梦——你不仅是别人眼中的风景，更是别人梦中的美好。",
 LQ + "你装饰了" + RQ + "与上句" + LQ + "明月装饰了" + RQ + "构成对仗和回环，将" + LQ + "你" + RQ + "与" + LQ + "明月" + RQ + "并置——你如明月一般美好，装饰了别人的梦境；" + LQ + "别人的梦" + RQ + "将现实与梦境相连，使诗的意境更加悠远。这一句将全诗的哲理推向极致：人与人之间相互关联、互为风景，你在装饰别人的梦时，别人也在装饰你的梦。"),
]

FULLTEXT = [
 "你站在桥上看风景，",
 "看风景的人在楼上看你。",
 "明月装饰了你的窗子，",
 "你装饰了别人的梦。",
]

BG_LEAD = [
 "《断章》是卞之琳的代表作，1935年10月写于日本京都，收入诗集《鱼目集》。全诗仅四句，却以精巧的结构、丰富的意象和深刻的哲理，成为中国现代诗歌史上最著名的短诗之一，也是被引用和讨论最多的现代诗之一。",
 "诗歌描绘了" + LQ + "你" + RQ + "在桥上看风景、楼上的人看" + LQ + "你" + RQ + "、明月装饰" + LQ + "你" + RQ + "的窗子、" + LQ + "你" + RQ + "装饰别人的梦四个场景，通过视角的转换和回环的结构，表达了人与人之间相互关联、互为风景的深刻哲理。" + LQ + "你站在桥上看风景，看风景的人在楼上看你" + RQ + "已成为中国现代诗歌中最经典的名句之一。",
]

AUTHOR = [
 "卞之琳（1910—2000），江苏海门人，中国现代著名诗人、翻译家、文学研究家。1929年入北京大学英文系，1933年毕业。1930年代开始写诗，是" + LQ + "汉园三诗人" + RQ + "（卞之琳、何其芳、李广田）之一。",
 "卞之琳的诗歌深受法国象征派和英国现代派影响，善于以精巧的结构、含蓄的意象和冷静的笔触表达深刻的哲理。他的诗风" + LQ + "平淡中见奇崛" + RQ + "，常常在最平常的场景中蕴含最深刻的哲理。主要作品有诗集《三秋草》《鱼目集》《慰劳信集》《十年诗草》等，译著有《莎士比亚悲剧四种》等。2000年12月2日，卞之琳在北京逝世，享年90岁。",
]

STORY = [
 ("写作缘起","1935年，卞之琳赴日本京都游学。一天，他在京都的一座桥上散步，看到桥下的风景和桥上的行人，忽然产生了一个灵感：每个人都在看风景，同时也在成为别人的风景。回到住处后，他写下了这首仅四句的短诗。诗的题目" + LQ + "断章" + RQ + "，意为" + LQ + "片段的章节" + RQ + "，暗示这只是人生长卷中的一个片段。"),
 ("哲理的争议","《断章》发表后，引发了广泛的讨论。有人认为这是一首爱情诗——" + LQ + "你" + RQ + "和" + LQ + "看风景的人" + RQ + "之间存在着微妙的情感；有人认为这是一首哲理诗——表达了相对主义和相互关联的世界观；还有人认为这是一首关于" + LQ + "距离" + RQ + "的诗——人与人之间永远存在着不可逾越的距离。卞之琳本人则说，这首诗的意思是" + LQ + "人与人之间，物与物之间，互相关联，互相依存" + RQ + "。"),
 ("结构的精巧","《断章》的结构极为精巧：前两句写白天，后两句写夜晚；前两句写" + LQ + "看" + RQ + "，后两句写" + LQ + "装饰" + RQ + "；第一句的" + LQ + "你" + RQ + "是观察者，第二句的" + LQ + "你" + RQ + "是被观察者；第三句的" + LQ + "你" + RQ + "是被装饰者，第四句的" + RQ + "你" + RQ + "是装饰者。这种回环往复的结构，使全诗如同一座精巧的迷宫，每读一遍都有新的发现。"),
]

APP_ART = [
 ("回环的结构","全诗四句，构成一个完美的回环：你看风景→人看你→明月装饰你→你装饰别人的梦。每一句的主语都是下一句的宾语，每一句的客体都是下一句的主体。这种回环结构使诗歌具有音乐美和建筑美，也强化了" + LQ + "人与人之间相互关联" + RQ + "的主题。"),
 ("顶真的手法","前两句" + LQ + "看风景" + RQ + "与" + LQ + "看风景的人" + RQ + "构成顶真——前一句末尾的" + LQ + "看风景" + RQ + "在后一句开头重复，使两句紧密相连，一气呵成。这种手法不仅增强了诗歌的音乐美，也暗示了" + LQ + "看" + RQ + "与" + RQ + "被看" + RQ + "之间的转换是自然而然、不可分割的。"),
 ("视角的转换","全诗通过视角的不断转换，表达了相对主义的哲理：第一句" + LQ + "你" + RQ + "是观察者，第二句" + LQ + "你" + RQ + "是被观察者；第三句" + LQ + "你" + RQ + "是被装饰者，第四句" + LQ + "你" + RQ + "是装饰者。没有绝对的观察者，也没有绝对的被观察者——每个人都在看，也都在被看；每个人都在装饰，也都在被装饰。"),
 ("意象的丰富","诗中" + LQ + "桥" + RQ + LQ + "楼" + RQ + LQ + "明月" + RQ + LQ + "窗子" + RQ + LQ + "梦" + RQ + "五个意象，各有深意：桥和楼是观察的位置，明月是美好的象征，窗子是私人空间的入口，梦是理想与想象的世界。五个意象交织在一起，构成了一幅从现实到梦境、从白天到夜晚的完整画卷。"),
 ("含蓄的哲理","全诗没有直接说理，而是通过四个场景的并置和回环，将哲理蕴含在形象之中。读者可以从不同角度解读：可以读成爱情诗，可以读成哲理诗，可以读成关于距离的诗。这种" + LQ + "形象大于思想" + RQ + "的特点，正是《断章》成为经典的重要原因。"),
]

APP_FAME = [
 ("你站在桥上看风景，看风景的人在楼上看你。",
  "前两句是全诗最著名的部分，也是中国现代诗歌中最经典的名句之一。" + LQ + "你站在桥上看风景" + RQ + "设定了一个平常的场景——你在桥上看风景；" + LQ + "看风景的人在楼上看你" + RQ + "以顶真手法完成视角的转换——你从观察者变成了被观察者。这两句的精妙之处在于：它揭示了一个普遍的真理——每个人都在看风景，同时也在成为别人的风景。没有绝对的观察者，也没有绝对的被观察者。这种相对主义的哲理，通过一个最平常的场景表达出来，言简意赅，意蕴无穷。"),
 ("明月装饰了你的窗子，你装饰了别人的梦。",
  "后两句将场景从白天转入夜晚，从现实转入梦境。" + LQ + "明月装饰了你的窗子" + RQ + "以拟人的手法，写明月的银辉洒进你的窗子，使你的空间变得美好；" + LQ + "你装饰了别人的梦" + RQ + "将" + LQ + "你" + RQ + "与" + LQ + "明月" + RQ + "并置——你如明月一般美好，装饰了别人的梦境。这两句与前两句构成回环：明月装饰你，你装饰别人；那么谁在装饰明月呢？答案是：别人也在装饰你的梦。这种回环往复的结构，使全诗的意境更加悠远，哲理更加深刻。"),
]

APP_THEME = [
 "《断章》通过描绘" + LQ + "你" + RQ + "在桥上看风景、楼上的人看" + LQ + "你" + RQ + "、明月装饰" + LQ + "你" + RQ + "的窗子、" + LQ + "你" + RQ + "装饰别人的梦四个场景，表达了人与人之间、物与物之间相互关联、互为风景的深刻哲理。",
 "全诗仅四句，却蕴含着丰富的意蕴。它可以读成一首爱情诗——" + LQ + "你" + RQ + "和" + LQ + "看风景的人" + RQ + "之间存在着微妙的情感；可以读成一首哲理诗——表达了相对主义和相互关联的世界观；也可以读成一首关于" + LQ + "距离" + RQ + "的诗——人与人之间永远存在着不可逾越的距离。这种多义性和开放性，正是《断章》成为中国现代诗歌经典的重要原因。",
]

ACC = [
 ("重点词语", [
   ("风景","一定地域内由山水、花草、树木、建筑物以及某些自然现象形成的可供人观赏的景象。"),
   ("装饰","在身体或物体的表面加些附属的东西，使美观。"),
   ("窗子","窗户。"),
   ("梦","睡眠时体内体外各种刺激引起的表象活动。"),
 ]),
 ("用字与读音", [
   ("桥","读 qiáo，二声；木字旁+乔，" + LQ + "桥梁" + RQ + "不要写成" + LQ + "桥粱" + RQ + "（" + LQ + "粱" + RQ + "米字旁，指高粱）。"),
   ("景","读 jǐng，三声；日字头+京，" + LQ + "风景" + RQ + "不要写成" + LQ + "风景" + RQ + "（" + LQ + "影" + RQ + "彡旁，读 yǐng）。"),
   ("装","读 zhuāng，一声；衣字旁+壮，" + LQ + "装饰" + RQ + "不要写成" + LQ + "妆饰" + RQ + "（" + LQ + "妆" + RQ + "女字旁，指化妆）。"),
   ("饰","读 shì，四声；饣旁+布，" + LQ + "装饰" + RQ + "不要写成" + LQ + "装饰" + RQ + "（" + LQ + "拭" + RQ + "提手旁，读 shì，指擦）。"),
   ("窗","读 chuāng，一声；穴字头+囱，" + LQ + "窗子" + RQ + "不要写成" + LQ + "窗子" + RQ + "（" + LQ + "疮" + RQ + "疒字头，读 chuāng）。"),
 ]),
 ("修辞方法", [
   ("顶　真", LQ + "你站在桥上看风景，看风景的人在楼上看你" + RQ + "——前一句末尾的" + LQ + "看风景" + RQ + "在后一句开头重复，使两句紧密相连，一气呵成。"),
   ("回　环", LQ + "明月装饰了你的窗子，你装饰了别人的梦" + RQ + "——" + LQ + "你" + RQ + "既是被装饰者，又是装饰者，与前两句" + LQ + "你" + RQ + "既是观察者又是被观察者构成回环，强化了相互关联的主题。"),
   ("对　偶", LQ + "明月装饰了你的窗子，你装饰了别人的梦" + RQ + "——两句结构相同，" + LQ + "明月" + RQ + "对" + LQ + "你" + RQ + "，" + LQ + "你的窗子" + RQ + "对" + LQ + "别人的梦" + RQ + "，对仗工整。"),
   ("拟　人", LQ + "明月装饰了你的窗子" + RQ + "——将明月拟人化，仿佛明月是一位艺术家，精心装点着你的窗子。"),
   ("象　征", LQ + "明月" + RQ + "——象征美好、思念、永恒；" + LQ + "梦" + RQ + "——象征理想、想象、美好的愿望。"),
 ]),
 ("写作借鉴", [
   ("以小见大","全诗仅四句，写的是最平常的场景——桥上看风景，却蕴含着最深刻的哲理——人与人之间相互关联、互为风景。这种以小见大的写法，使诗歌言简意赅，意蕴无穷。"),
   ("回环的结构","全诗四句构成一个完美的回环：你看风景→人看你→明月装饰你→你装饰别人的梦。这种回环结构不仅增强了诗歌的音乐美和建筑美，也强化了" + LQ + "相互关联" + RQ + "的主题。"),
   ("视角的转换","通过视角的不断转换（观察者→被观察者→被装饰者→装饰者），表达了相对主义的哲理。没有绝对的主体，也没有绝对的客体——一切都是相对的、相互关联的。"),
   ("含蓄的表达","全诗没有直接说理，而是通过四个场景的并置和回环，将哲理蕴含在形象之中。读者可以从不同角度解读，这种" + LQ + "形象大于思想" + RQ + "的特点，使诗歌具有永恒的魅力。"),
 ]),
 ("文化常识", [
   ("卞之琳","（1910—2000）江苏海门人，中国现代著名诗人、翻译家。" + LQ + "汉园三诗人" + RQ + "之一。代表作有《断章》《鱼目集》《十年诗草》等。"),
   ("汉园三诗人","指卞之琳、何其芳、李广田三位诗人，因1936年出版三人诗合集《汉园集》而得名。他们都是北京大学的学生，诗歌风格各有特色，但都注重意象的营造和哲理的表达。"),
   ("象征派","20世纪初传入中国的现代主义诗歌流派，源于法国。象征派诗歌强调用含蓄的意象、朦胧的意境表达内心的情感。卞之琳的诗歌深受象征派影响。"),
   ("顶真","修辞手法之一，指前一句末尾的词语在后一句开头重复，使句子之间紧密相连。如" + LQ + "看风景→看风景的人" + RQ + "。"),
 ]),
]

WORDS = [
 {"w":"桥","py":"qiáo","q":"你站在□上看风景，","tip":"「桥」木字旁+乔，读 qiáo 二声；勿写「侨」（单人旁）"},
 {"w":"景","py":"jǐng","q":"你站在桥上看风□，","tip":"「景」日字头+京，读 jǐng 三声；勿写「影」（彡旁，读 yǐng）"},
 {"w":"装","py":"zhuāng","q":"明月□饰了你的窗子，","tip":"「装」衣字旁+壮，读 zhuāng 一声；勿写「妆」（女字旁，指化妆）"},
 {"w":"饰","py":"shì","q":"明月装□了你的窗子，","tip":"「饰」饣旁+布，读 shì 四声；勿写「拭」（提手旁，指擦）"},
 {"w":"窗","py":"chuāng","q":"明月装饰了你的□子，","tip":"「窗」穴字头+囱，读 chuāng 一声；勿写「疮」（疒字头）"},
 {"w":"梦","py":"mèng","q":"你装饰了别人的□。","tip":"「梦」林字头+夕，读 mèng 四声；繁体「夢」，勿写「梦」（少一横）"},
]

NOTES = [
 {"w":"风景","a":"一定地域内由山水、花草、树木、建筑物等形成的可供人观赏的景象","q":"你站在桥上看风景，"},
 {"w":"看风景的人","a":"观赏景色的人，指楼上的人","q":"看风景的人在楼上看你。"},
 {"w":"明月","a":"明亮的月亮","q":"明月装饰了你的窗子，"},
 {"w":"装饰","a":"在身体或物体的表面加些附属的东西，使美观","q":"明月装饰了你的窗子，"},
 {"w":"窗子","a":"窗户","q":"明月装饰了你的窗子，"},
 {"w":"梦","a":"睡眠时体内体外各种刺激引起的表象活动","q":"你装饰了别人的梦。"},
]

VIDEOS = [
 ("《断章》卞之琳 朗诵","BV1g5411E7sd","断章卞之琳朗诵"),
 ("赏析现代诗《断章》","BV1wxNHePEcS","断章赏析"),
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

hero = '<header class="hero" id="top">\n  <div class="hero-inner">\n    <div class="hero-side">现代 · 卞之琳</div>\n    <h1 class="hero-title">断章</h1>\n  </div>\n</header>'

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
      '<div class="sec-sub">全诗四句，以精巧的回环结构和丰富的意象，表达了人与人之间相互关联、互为风景的深刻哲理。每句含<b>注释</b>（点击可查看）、内容概括与手法分析。短篇诗歌不分部分，直接逐句解读。</div>',
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

footer = '<footer>\n  <div class="kai">断章</div>\n  <div>卞之琳 · 现代 · 中国现代诗歌最著名的哲理短诗</div>\n  <div>人教版九年级语文下册课文</div>\n</footer>'

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
        '<title>断章 · 卞之琳</title>\n'
        '<meta name="description" content="现代卞之琳《断章》逐句解读、注释、赏析，含背景、原文（背诵模式）、解读、赏析、积累、练习，适合课堂教学。">\n'
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
print("断章 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), anno_count, len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
