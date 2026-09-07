# -*- coding: utf-8 -*-
"""生成《月夜》沈尹默课件（短篇现代诗，逐句解读）。"""
import io, json, re

SRC = r"D:\App\Apps\yanshi\zuguoawoqinaidezuguo-shuting.html"
OUT = r"D:\App\Apps\yanshi\yueye-shenyinmo.html"
LS_KEY = "yueye_fs"

LQ = "\u201c"
RQ = "\u201d"

def A(word, note):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)

# 逐句数据：(原文带注释标记, 内容概括, 手法分析)
CARDS = [
("霜风" + A("呼呼","状声词，形容风声大而急") + "的" + A("吹着","风吹动着；" + LQ + "着" + RQ + "表动作持续") + "，",
 "首句写听觉：深秋的寒风呼呼地吹着，营造出清冷萧瑟的氛围。",
 LQ + "霜风" + RQ + "点明季节——深秋，寒风凛冽；" + LQ + "呼呼" + RQ + "是叠音状声词，摹写风声，使读者如闻其声；" + LQ + "的" + RQ + "是早期白话诗的用法，相当于后来的" + LQ + "地" + RQ + "。"),
("月光" + A("明明","形容月光明亮皎洁") + "的照着。",
 "次句写视觉：皎洁的月光明亮地照耀着大地，与首句的寒风形成对照。",
 LQ + "明明" + RQ + "叠音词，摹写月光的明亮；两句" + LQ + "呼呼" + RQ + LQ + "明明" + RQ + "对仗工整，一写听觉一写视觉，一冷一亮，构成了月夜的典型环境。"),
("我和一株" + A("顶高","最高、极高；" + LQ + "顶" + RQ + "表程度，相当于" + LQ + "最" + RQ) + "的树" + A("并排","排列在一条线上，不分前后") + A("立着","站立着；" + LQ + "着" + RQ + "表状态持续") + "，",
 "第三句由景入人：" + LQ + "我" + RQ + "与一株最高的树并排站立，人与树并置，形成一幅剪影。",
 LQ + "一株顶高的树" + RQ + "中" + LQ + "顶高" + RQ + "是口语化的程度表达，比" + LQ + "最高" + RQ + "更朴素；" + LQ + "并排立着" + RQ + "写人与树并肩而立的姿态，暗示人的独立与尊严，树成为人的精神对照物。"),
("却没有" + A("靠着","倚靠、依傍着") + "。",
 "末句是全诗的诗眼：" + LQ + "我" + RQ + "虽然与树并排立着，却没有依靠它——独立不倚。",
 LQ + "却" + RQ + "表转折，将" + LQ + "并排立着" + RQ + "与" + LQ + "没有靠着" + RQ + "对照，点出全诗主旨：人格的独立与不依附。短短四字，意蕴无穷——在寒风中、在明月下，人既与自然并立，又保持自我的独立，这正是五四时期个性解放精神的诗意表达。"),
]

FULLTEXT = [
 "霜风呼呼的吹着，",
 "月光明明的照着。",
 "我和一株顶高的树并排立着，",
 "却没有靠着。",
]

BG_LEAD = [
 "《月夜》是沈尹默的代表作，1918年1月发表于《新青年》第四卷第一号，是中国现代文学史上最早的白话诗之一。全诗仅四句，却以凝练的语言、鲜明的意象和深刻的哲理，成为中国现代诗歌的经典之作。",
 "诗歌描绘了一个霜风呼啸、明月高照的夜晚，" + LQ + "我" + RQ + "与一株顶高的树并排立着，却没有靠着。人与树并立而不依傍，象征着五四时期知识分子追求人格独立、个性解放的精神。这首诗开创了中国白话诗的先河，以其简洁含蓄的风格影响了一代诗人。",
]

AUTHOR = [
 "沈尹默（1883—1971），原名君默，字中，后改名尹默，浙江吴兴（今湖州）人，中国现代著名诗人、书法家、学者。早年留学日本，1912年回国后任北京大学教授，是《新青年》杂志的重要编辑和撰稿人之一。",
 "沈尹默是新文化运动的重要参与者，也是中国现代白话诗的先驱之一。1918年，他在《新青年》上发表了《月夜》《鸽子》《人力车夫》等白话诗，与胡适、刘半农等人共同推动了中国诗歌的现代化转型。他的诗歌风格简洁含蓄，善于以白描手法营造意境。除诗歌外，沈尹默在书法领域也有极高成就，被誉为" + LQ + "20世纪十大书法家" + RQ + "之一。",
]

STORY = [
 ("白话诗的先河","1917年，胡适在《新青年》上发表《文学改良刍议》，提出以白话文代替文言文的主张。1918年1月，《新青年》第四卷第一号发表了胡适、沈尹默、刘半农三人的九首白话诗，这是中国现代文学史上第一次集中发表白话诗。《月夜》便是其中之一，它以完全白话的语言、自由的句式，打破了旧体诗的格律束缚。"),
 ("五四精神的写照","写作此诗时，正值新文化运动高潮。五四时期的知识分子追求民主与科学，强调个性解放和人格独立。《月夜》中" + LQ + "我和一株顶高的树并排立着，却没有靠着" + RQ + "，正是这种独立不倚、不依附他人的精神写照——人可以与伟大的事物并立，却不必依附于它。"),
 ("书法与诗歌","沈尹默不仅是诗人，更是书法大家。他的书法初学褚遂良，后遍临晋唐诸家，形成了秀逸遒劲的风格。《月夜》的简洁凝练，与他书法中" + LQ + "笔简意赅" + RQ + "的审美追求一脉相承。"),
]

APP_ART = [
 ("白描手法","全诗无华丽辞藻，纯用白描。" + LQ + "霜风呼呼的吹着，月光明明的照着" + RQ + "，仅用两个叠音词便勾勒出月夜的典型环境；" + LQ + "我和一株顶高的树并排立着" + RQ + "，如同一幅剪影画，简洁而有力。"),
 ("意象的象征","诗中的" + LQ + "树" + RQ + "是核心意象。" + LQ + "顶高的树" + RQ + "象征着伟大、崇高的事物，可以是传统、权威、他人，也可以是某种精神支柱。人与树" + LQ + "并排立着" + RQ + "，意味着人敢于与伟大者并立；" + LQ + "却没有靠着" + RQ + "，意味着人保持独立，不依附于任何外在力量。"),
 ("叠音词的运用","" + LQ + "呼呼" + RQ + LQ + "明明" + RQ + "两组叠音词，一摹风声一摹月光，对仗工整，音韵和谐，使诗歌具有音乐美。同时，叠音词的运用也增强了画面的感染力，使读者如临其境、如闻其声。"),
 ("含蓄的哲理","全诗最深刻之处在于末句" + LQ + "却没有靠着" + RQ + "。短短四字，蕴含着丰富的哲理：人格的独立、个性的解放、不依附于人的自尊。诗人没有直接说教，而是通过一个简单的动作——" + LQ + "立着" + RQ + "与" + LQ + "靠着" + RQ + "的对比，将深刻的哲理蕴含在具体的形象之中，言有尽而意无穷。"),
]

APP_FAME = [
 ("霜风呼呼的吹着，月光明明的照着。",
  "开篇两句对仗工整，一写听觉一写视觉，勾勒出月夜的典型环境。" + LQ + "霜风" + RQ + "点明深秋季节，寒风凛冽；" + LQ + "月光" + RQ + "点明夜晚，月色皎洁。" + LQ + "呼呼" + RQ + LQ + "明明" + RQ + "两组叠音词，音韵和谐，如闻其声、如见其景。这两句纯用白描，没有一个多余的字，却营造出清冷而明亮的月夜氛围，为下文人的出场做了铺垫。"),
 ("我和一株顶高的树并排立着，却没有靠着。",
  "后两句是全诗的精华所在。" + LQ + "我" + RQ + "的出场，使客观的月夜有了人的存在；" + LQ + "一株顶高的树" + RQ + "成为人的精神对照物。" + LQ + "并排立着" + RQ + "写人与树并肩而立的姿态，暗示人敢于与伟大者并立；" + LQ + "却没有靠着" + RQ + "以一个转折，点出全诗主旨——独立不倚、不依附于人。这是五四时期个性解放精神的诗意表达，也是中国现代诗歌中最经典的哲理诗句之一。"),
]

APP_THEME = [
 "《月夜》通过描绘一个霜风呼啸、明月高照的夜晚，" + LQ + "我" + RQ + "与一株顶高的树并排立着却没有靠着的场景，表达了诗人对人格独立、个性解放的追求和赞美。",
 "全诗仅四句，却蕴含着深刻的哲理：人可以与伟大的事物并立，却不必依附于它；在寒风中、在明月下，人保持着自我的独立与尊严。这种独立不倚的精神，正是五四时期知识分子追求个性解放的真实写照，也使这首诗成为中国现代白话诗的经典之作。",
]

ACC = [
 ("重点词语", [
   ("霜风","深秋寒冷的风。"),
   ("呼呼","状声词，形容风声大而急。"),
   ("明明","形容月光明亮皎洁。"),
   ("顶高","最高、极高。" + LQ + "顶" + RQ + "表程度，相当于" + LQ + "最" + RQ + "。"),
   ("并排","排列在一条线上，不分前后。"),
   ("靠着","倚靠、依傍着。"),
 ]),
 ("用字与读音", [
   ("霜","读 shuāng，一声；雨字头+相，" + LQ + "霜风" + RQ + "指深秋寒风。"),
   ("呼呼","读 hū hū，状声词；口字旁，" + LQ + "呼" + RQ + "不要写成" + LQ + "乎" + RQ + "。"),
   ("照","读 zhào，四声；" + LQ + "照着" + RQ + "不要写成" + LQ + "照着" + RQ + "（" + LQ + "昭" + RQ + "日字旁，读 zhāo）。"),
   ("株","读 zhū，一声；木字旁，量词，用于树木。"),
   ("并","读 bìng，四声；" + LQ + "并排" + RQ + "不要写成" + LQ + "并排" + RQ + "（" + LQ + "迸" + RQ + "走之底，读 bèng）。"),
   ("靠","读 kào，四声；" + LQ + "靠着" + RQ + "不要写成" + LQ + "靠着" + RQ + "（" + LQ + "犒" + RQ + "牛字旁，读 kào）。"),
 ]),
 ("修辞方法", [
   ("白　描", LQ + "霜风呼呼的吹着，月光明明的照着" + RQ + "——纯用白描手法，不加修饰，以最朴素的语言勾勒出月夜的典型环境。"),
   ("对　偶", LQ + "霜风呼呼的吹着，月光明明的照着" + RQ + "——两句对仗工整，一写听觉一写视觉，" + LQ + "呼呼" + RQ + "对" + LQ + "明明" + RQ + "，" + LQ + "吹着" + RQ + "对" + LQ + "照着" + RQ + "。"),
   ("叠　音", LQ + "呼呼" + RQ + LQ + "明明" + RQ + "——两组叠音词，一摹风声一摹月光，增强了诗歌的音乐美和画面感。"),
   ("象　征", LQ + "一株顶高的树" + RQ + "——象征伟大、崇高的事物，可以是传统、权威或精神支柱；人与树并立而不依傍，象征人格的独立。"),
   ("对　比", LQ + "并排立着" + RQ + "与" + LQ + "没有靠着" + RQ + "对比，在并立与不依傍之间凸显独立人格的可贵。"),
 ]),
 ("写作借鉴", [
   ("以小见大","全诗仅四句，写的是一个极小的场景——月夜中人与树并立，却蕴含着人格独立的大主题。这种以小见大的写法，使诗歌言简意赅、意蕴无穷。"),
   ("白描手法","全诗无华丽辞藻，纯用白描。" + LQ + "霜风" + RQ + LQ + "月光" + RQ + LQ + "树" + RQ + LQ + "我" + RQ + "，几个简单的意象便构成了一幅完整的画面。这种朴素的写法，反而使诗歌更有力量。"),
   ("哲理蕴含于形象","诗人没有直接说教，而是通过" + LQ + "立着" + RQ + "与" + LQ + "靠着" + RQ + "的对比，将独立不倚的哲理蕴含在具体的形象之中。这种写法比直接说理更有感染力，也更符合诗歌的审美特征。"),
   ("口语化的语言","" + LQ + "顶高" + RQ + LQ + "并排" + RQ + LQ + "靠着" + RQ + "都是口语化的表达，朴素自然。这在1918年是革命性的——它打破了旧体诗的文言传统，开创了白话诗的先河。"),
 ]),
 ("文化常识", [
   ("白话诗","又称新诗，是五四运动后兴起的以白话写作、打破旧体诗词格律束缚的诗歌形式。1918年《新青年》第四卷第一号发表胡适、沈尹默、刘半农三人的九首白话诗，是中国现代文学史上第一次集中发表白话诗。"),
   ("《新青年》","中国现代文学史上最重要的刊物之一，1915年创刊于上海，原名《青年杂志》，1916年改名《新青年》。它是新文化运动的主要阵地，倡导民主与科学，反对旧道德、旧文学，发表了大量白话文学作品。"),
   ("新文化运动","1915年兴起的思想文化革新运动，以《新青年》为主要阵地，倡导民主与科学，反对旧道德、旧文学，主张文学革命。新文化运动推动了中国社会的现代化转型，也催生了中国现代文学。"),
 ]),
]

WORDS = [
 {"w":"霜","py":"shuāng","q":"□风呼呼的吹着，","tip":"「霜」雨字头+相，读 shuāng 一声；勿写「孀」（女字旁）"},
 {"w":"呼呼","py":"hū hū","q":"霜风□□的吹着，","tip":"「呼」口字旁，状声词；勿写「乎」（无口字旁）"},
 {"w":"照","py":"zhào","q":"月光明明的□着。","tip":"「照」日字头+昭，读 zhào 四声；勿写「昭」（日字旁，读 zhāo）"},
 {"w":"株","py":"zhū","q":"我和一□顶高的树并排立着，","tip":"「株」木字旁+朱，量词，用于树木；勿写「珠」（王字旁）"},
 {"w":"并","py":"bìng","q":"我和一株顶高的树□排立着，","tip":"「并」读 bìng 四声；「并排」勿写「迸排」（迸读 bèng）"},
 {"w":"靠","py":"kào","q":"却没有□着。","tip":"「靠」非字头+告，读 kào 四声；勿写「犒」（牛字旁，读 kào）"},
]

NOTES = [
 {"w":"霜风","a":"深秋寒冷的风","q":"霜风呼呼的吹着，"},
 {"w":"呼呼","a":"状声词，形容风声大而急","q":"霜风呼呼的吹着，"},
 {"w":"明明","a":"形容月光明亮皎洁","q":"月光明明的照着。"},
 {"w":"顶高","a":"最高、极高；「顶」表程度，相当于「最」","q":"我和一株顶高的树并排立着，"},
 {"w":"并排","a":"排列在一条线上，不分前后","q":"我和一株顶高的树并排立着，"},
 {"w":"靠着","a":"倚靠、依傍着","q":"却没有靠着。"},
]

VIDEOS = [
 ("《月夜》沈尹默 诗朗诵","BV13M4y1G7x9","月夜沈尹默朗诵"),
 ("沈尹默：首先是个诗人，是一个思想者","BV1XB4y1z7yH","沈尹默人物介绍"),
]

# ===== 读取框架 =====
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]

# 提取主JS（到DICT_WORDS之前）
js_main = src[src.index("<script>") + 8 : src.index("var DICT_WORDS")]
js_main = js_main.replace("zuguoawoqinaidezuguo_fs", LS_KEY)

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
hero = '<header class="hero" id="top">\n  <div class="hero-inner">\n    <div class="hero-side">现代 · 沈尹默</div>\n    <h1 class="hero-title">月夜</h1>\n  </div>\n</header>'

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
      '<div class="sec-sub">全诗四句，以凝练的语言描绘了月夜中人与树并立而不依傍的场景，蕴含着人格独立的深刻哲理。每句含<b>注释</b>（点击可查看）、内容概括与手法分析。短篇诗歌不分部分，直接逐句解读。</div>',
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
       '<div class="sec-head"><h2>积 累</h2><span class="no">词语 · 读音 · 修辞 · 写作 · 文化</span></div>']
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
            '<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写 · 字形 / 词语</span></div>',
            '<div class="sec-sub">以全篇<b>易错字词</b>与<b>重点词语</b>为题库，点击按钮进入<b>全屏听写</b>：先看提示在纸上默写，再核对答案。随机五组适合随堂小测，全部适合系统复习。</div>',
            '<div class="ptools">',
            '<button data-mode="word" data-rand="5">随机五组字形</button>',
            '<button data-mode="word" data-all="1">全部字形</button>',
            '<button data-mode="note" data-rand="5">随机五组词语</button>',
            '<button data-mode="note" data-all="1">全部词语</button>',
            '</div></section>']

footer = '<footer>\n  <div class="kai">月夜</div>\n  <div>沈尹默 · 现代 · 中国现代白话诗先驱之作</div>\n  <div>人教版九年级语文下册课文</div>\n</footer>'

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
        '<title>月夜 · 沈尹默</title>\n'
        '<meta name="description" content="现代沈尹默《月夜》逐句解读、注释、赏析，含背景、原文（背诵模式）、解读、赏析、积累、练习，适合课堂教学。">\n'
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
print("月夜 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), anno_count, len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
