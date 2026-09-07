# -*- coding: utf-8 -*-
"""生成《统一》聂鲁达课件（短篇现代诗，逐句解读）。"""
import io, json, re

SRC = r"D:\App\Apps\yanshi\zuguoawoqinaidezuguo-shuting.html"
OUT = r"D:\App\Apps\yanshi\tongyi-nieluda.html"
LS_KEY = "tongyi_fs"

LQ = "\u201c"
RQ = "\u201d"

def A(word, note):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)

CARDS = [
("所有的叶是这" + A("一片","量词，用于扁平而薄的东西，这里指叶子") + "，",
 "首句提出一个惊人的判断：所有的叶，本质上都是这一片叶。",
 LQ + "所有的叶" + RQ + "是全称判断，" + LQ + "这一片" + RQ + "是单称判断，两者之间形成巨大的张力——世界上有千千万万片叶子，但在诗人看来，它们本质上都是同一片叶。这一句开篇点题，提出了" + LQ + "统一" + RQ + "的核心命题：繁多的表象背后，是统一的本质。"),
("所有的花是这" + A("一朵","量词，用于花或花朵状的东西") + "，",
 "次句延续上句的判断：所有的花，本质上都是这一朵花。",
 LQ + "所有的花" + RQ + "与上句" + LQ + "所有的叶" + RQ + "构成排比，" + LQ + "这一朵" + RQ + "与" + LQ + "这一片" + RQ + "对应。两句句式相同，节奏一致，如层层递进的推理，强化了" + LQ + "统一" + RQ + "的命题。叶和花是植物最常见的部分，也是最能体现" + LQ + "繁多" + RQ + "的事物——世界上没有两片完全相同的叶子，也没有两朵完全相同的花，但诗人却说它们本质上是统一的。"),
(A("繁多","种类多、数量大") + "是个" + A("谎言","不真实的话、骗人的话") + "。",
 "第三句是全诗的诗眼：繁多是个谎言——我们看到的千差万别，其实只是表象。",
 LQ + "繁多是个谎言" + RQ + "是一个惊人的悖论。在常识中，" + LQ + "繁多" + RQ + "是客观事实——世界上确实有千千万万种不同的事物。但诗人却说这是" + LQ + "谎言" + RQ + "，因为在本质层面，所有的事物都是统一的。这一句是全诗的转折点：前两句提出" + LQ + "统一" + RQ + "的命题，这一句否定" + LQ + "繁多" + RQ + "的真实性，后三句则用推理来论证这个命题。"),
("因为一切" + A("果实","植物所结的可以吃的东西，这里泛指植物的果实") + "并无" + A("差异","差别、不同") + "，",
 "第四句开始论证：因为一切果实，本质上并没有差别。",
 LQ + "因为" + RQ + "引出推理，解释为什么" + LQ + "繁多是个谎言" + RQ + "。" + LQ + "一切果实并无差异" + RQ + "——从表面看，苹果、梨、桃、橘子各不相同，但它们的本质都是植物的果实，都包含着生命的种子，都承担着繁衍的使命。在本质层面，它们确实没有差异。这一句从果实入手，论证了" + LQ + "统一" + RQ + "的命题。"),
("所有树木" + A("无非","不外乎、只不过") + "一棵，",
 "第五句继续推理：所有的树木，本质上只不过是同一棵树。",
 LQ + "无非" + RQ + "是" + LQ + "不外乎、只不过" + RQ + "的意思，语气肯定而不容置疑。" + LQ + "所有树木无非一棵" + RQ + "——世界上有千千万万棵树，松树、柏树、柳树、杨树各不相同，但它们的本质都是树，都有根、干、枝、叶，都进行光合作用，都遵循生命的规律。在本质层面，它们确实是同一棵树。这一句从树木入手，进一步论证了" + LQ + "统一" + RQ + "的命题。"),
("整片大地是一朵花。",
 "末句收束全诗：整片大地，本质上就是一朵花。",
 LQ + "整片大地是一朵花" + RQ + "是全诗的升华。前面几句从叶、花、果实、树木等具体事物论证" + LQ + "统一" + RQ + "，这一句将范围扩大到" + LQ + "整片大地" + RQ + "，将本质归结为" + LQ + "一朵花" + RQ + "。" + LQ + "一朵花" + RQ + "象征着生命、美好和统一——整片大地，本质上就是一个统一的生命体，一朵盛开的花。这一句将全诗的哲理推向极致，也使诗歌的意境达到了顶峰。"),
]

FULLTEXT = [
 "所有的叶是这一片，",
 "所有的花是这一朵，",
 "繁多是个谎言。",
 "因为一切果实并无差异，",
 "所有树木无非一棵，",
 "整片大地是一朵花。",
]

BG_LEAD = [
 "《统一》是智利诗人聂鲁达的作品，由陈实翻译，收入统编版语文九年级下册。全诗仅六句，却以严密的推理和惊人的判断，表达了世界统一性的深刻哲理：繁多的表象背后，是统一的本质。",
 "诗歌以" + LQ + "所有的叶是这一片，所有的花是这一朵" + RQ + "开篇，提出" + LQ + "统一" + RQ + "的命题；继而以" + LQ + "繁多是个谎言" + RQ + "否定繁多的真实性；最后以" + LQ + "因为一切果实并无差异，所有树木无非一棵，整片大地是一朵花" + RQ + "三句，用严密的推理论证了" + LQ + "统一" + RQ + "的命题。全诗结构严谨，哲理深刻，是世界诗歌史上最著名的哲理短诗之一。",
]

AUTHOR = [
 "巴勃罗·聂鲁达（1904—1973），原名内夫塔利·里卡多·雷耶斯·巴索阿尔托，智利著名诗人、外交家，1971年诺贝尔文学奖获得者。13岁开始发表诗作，1923年发表第一部诗集《黄昏》，1924年发表成名作《二十首情诗和一支绝望的歌》，从此享誉拉美文坛。",
 "聂鲁达的诗歌创作经历了从浪漫主义到现实主义、从个人情诗到政治抒情的转变。早期作品情感细腻、意象优美，后期作品关注社会现实、歌颂人民和祖国。他的诗歌气势磅礴、情感真挚、语言丰富，对拉美和世界诗歌产生了深远影响。主要作品有《二十首情诗和一支绝望的歌》《地球上的居所》《漫歌》《爱情十四行诗一百首》等。1973年9月23日，聂鲁达在智利圣地亚哥逝世，享年69岁。",
]

STORY = [
 ("写作背景","《统一》写于20世纪70年代，是聂鲁达晚年的作品，原收录在诗集《世界末日》中。当时，诗人已认识到原子能时代的危险，该诗集的主题均为" + LQ + "启示" + RQ + "。在核战争阴影笼罩世界的背景下，聂鲁达思考人类的命运和世界的本质，写下了这首《统一》。他想告诉人们：尽管世界上有千差万别的事物和民族，但在本质上，人类是统一的，世界是统一的——认识到这种统一性，或许才能避免人类的自我毁灭。"),
 ("陈实的翻译","本诗的译者是陈实，中国著名的西班牙语文学翻译家。陈实的翻译忠实于原作，语言简洁有力，很好地传达了聂鲁达诗歌的哲理和气势。" + LQ + "所有的叶是这一片" + RQ + LQ + "繁多是个谎言" + RQ + LQ + "整片大地是一朵花" + RQ + "等名句，经陈实的翻译，已成为中国读者耳熟能详的诗句。"),
 ("哲理的渊源","《统一》所表达的" + LQ + "世界统一性" + RQ + "的思想，在哲学史上有着深远的渊源。古希腊哲学家巴门尼德提出" + LQ + "存在是一" + RQ + "的命题，认为万物的本质是统一的；中国古代哲学也有" + LQ + "万物一体" + RQ + LQ + "天人合一" + RQ + "的思想。聂鲁达的《统一》以诗歌的形式，重新表达了这一古老的哲学命题，使抽象的哲理变得具体可感、生动有力。"),
]

APP_ART = [
 ("严密的推理结构","全诗六句，构成了一个严密的推理过程：前两句提出命题（所有的叶是这一片，所有的花是这一朵），第三句否定反命题（繁多是个谎言），后三句用归纳推理论证命题（果实无差异→树木无非一棵→大地是一朵花）。这种" + LQ + "提出命题—否定反命题—论证命题" + RQ + "的结构，使全诗逻辑严密、层层递进，具有很强的说服力。"),
 ("惊人的悖论","" + LQ + "繁多是个谎言" + RQ + "是全诗最惊人的判断。在常识中，" + LQ + "繁多" + RQ + "是客观事实，但诗人却说这是" + LQ + "谎言" + RQ + "。这种悖论式的表达，打破了读者的常识预期，引发了深刻的思考：我们看到的千差万别，真的是事物的本质吗？还是说，本质层面的统一才是真实的？这种悖论式的表达，使诗歌具有了强烈的思想冲击力。"),
 ("归纳推理的运用","后三句运用了归纳推理的方法：从果实（一切果实并无差异）到树木（所有树木无非一棵），再到大地（整片大地是一朵花），范围逐步扩大，结论逐步升华。这种从具体到抽象、从个别到一般的推理，使" + LQ + "统一" + RQ + "的命题得到了有力的论证，也使诗歌的意境逐步扩大，最后达到" + LQ + "整片大地是一朵花" + RQ + "的顶峰。"),
 ("排比与反复","前两句" + LQ + "所有的叶是这一片，所有的花是这一朵" + RQ + "构成排比，句式相同，节奏一致，如层层递进的推理，强化了" + LQ + "统一" + RQ + "的命题。后三句" + LQ + "一切果实并无差异，所有树木无非一棵，整片大地是一朵花" + RQ + "也构成排比和递进，范围逐步扩大，结论逐步升华。排比和反复的运用，使诗歌具有音乐美和气势感。"),
 ("以小见大的手法","全诗从叶、花、果实、树木等最常见的小事物入手，最后升华到" + LQ + "整片大地是一朵花" + RQ + "的宏大境界。这种以小见大的手法，使抽象的哲理变得具体可感，也使诗歌的意境逐步扩大。读者从最熟悉的叶子和花朵开始，跟随诗人的推理，最后到达" + LQ + "整片大地" + RQ + "的宏大视野，整个过程自然而有力。"),
]

APP_FAME = [
 ("所有的叶是这一片，所有的花是这一朵，繁多是个谎言。",
  "前三句是全诗的核心，提出了" + LQ + "统一" + RQ + "的命题并否定了" + LQ + "繁多" + RQ + "的真实性。" + LQ + "所有的叶是这一片" + RQ + LQ + "所有的花是这一朵" + RQ + "两句排比，提出了一个惊人的判断：千千万万片叶子，本质上都是同一片叶；千千万万朵花，本质上都是同一朵花。" + LQ + "繁多是个谎言" + RQ + "则直接否定了常识中的" + LQ + "繁多" + RQ + "，认为千差万别只是表象，统一才是本质。这三句如同一记重锤，打破了读者的常识预期，引发了深刻的思考。"),
 ("因为一切果实并无差异，所有树木无非一棵，整片大地是一朵花。",
  "后三句用严密的归纳推理论证了" + LQ + "统一" + RQ + "的命题。" + LQ + "一切果实并无差异" + RQ + "——从表面看，各种果实各不相同，但本质上都是植物的果实，都包含着生命的种子；" + LQ + "所有树木无非一棵" + RQ + "——各种树木各不相同，但本质上都是树，都遵循生命的规律；" + LQ + "整片大地是一朵花" + RQ + "——将范围扩大到整片大地，将本质归结为一朵花，象征着生命、美好和统一。这三句从具体到抽象、从个别到一般，推理严密，意境逐步扩大，最后达到全诗的顶峰。"),
]

APP_THEME = [
 "《统一》通过严密的推理和惊人的判断，表达了世界统一性的深刻哲理：繁多的表象背后，是统一的本质。诗人告诉我们，尽管世界上有千差万别的事物，但在本质层面，它们是统一的——所有的叶都是同一片叶，所有的花都是同一朵花，整片大地就是一朵花。",
 "这首诗写于原子能时代的阴影之下，聂鲁达想通过" + LQ + "统一" + RQ + "的命题启示人们：人类虽然有不同的民族、国家和文化，但在本质上是统一的——认识到这种统一性，或许才能避免人类的自我毁灭。全诗结构严谨，哲理深刻，意境宏大，是世界诗歌史上最著名的哲理短诗之一，也是聂鲁达晚年诗歌的代表作。",
]

ACC = [
 ("重点词语", [
   ("一片","量词，用于扁平而薄的东西，这里指叶子。"),
   ("一朵","量词，用于花或花朵状的东西。"),
   ("繁多","种类多、数量大。"),
   ("谎言","不真实的话、骗人的话。"),
   ("果实","植物所结的可以吃的东西，这里泛指植物的果实。"),
   ("差异","差别、不同。"),
   ("无非","不外乎、只不过。"),
 ]),
 ("用字与读音", [
   ("繁","读 fán，二声；" + LQ + "繁多" + RQ + "不要写成" + LQ + "繁多" + RQ + "（" + LQ + "烦" + RQ + "火字旁，指烦恼）。"),
   ("谎","读 huǎng，三声；言字旁+荒，" + LQ + "谎言" + RQ + "不要写成" + LQ + "慌言" + RQ + "（" + LQ + "慌" + RQ + "竖心旁，指慌张）。"),
   ("实","读 shí，二声；" + LQ + "果实" + RQ + "不要写成" + LQ + "果实" + RQ + "（" + LQ + "食" + RQ + "食字旁，指食物）。"),
   ("差","读 chā，一声；多音字，此处读 chā（差别），不读 chà（差不多）、chāi（出差）、cī（参差）。"),
   ("非","读 fēi，一声；" + LQ + "无非" + RQ + "指不外乎，不要写成" + LQ + "无飞" + RQ + "（" + LQ + "飞" + RQ + "指飞翔）。"),
 ]),
 ("修辞方法", [
   ("排　比", LQ + "所有的叶是这一片，所有的花是这一朵" + RQ + "——两句排比，句式相同，节奏一致，强化了" + LQ + "统一" + RQ + "的命题；后三句也构成排比和递进。"),
   ("悖　论", LQ + "繁多是个谎言" + RQ + "——在常识中" + LQ + "繁多" + RQ + "是客观事实，但诗人却说这是" + LQ + "谎言" + RQ + "，这种悖论式的表达打破了读者的常识预期，引发深刻思考。"),
   ("归纳推理", LQ + "果实无差异→树木无非一棵→大地是一朵花" + RQ + "——从具体到抽象、从个别到一般，范围逐步扩大，结论逐步升华，论证了" + LQ + "统一" + RQ + "的命题。"),
   ("比　喻", LQ + "整片大地是一朵花" + RQ + "——将整片大地比作一朵花，象征着生命、美好和统一，使抽象的哲理变得具体可感。"),
 ]),
 ("写作借鉴", [
   ("严密的推理结构","全诗采用" + LQ + "提出命题—否定反命题—论证命题" + RQ + "的结构，逻辑严密，层层递进。这种结构使哲理诗具有了说服力，也使读者在阅读过程中跟随诗人的推理，逐步接受诗歌的观点。"),
   ("悖论式的表达","" + LQ + "繁多是个谎言" + RQ + "以悖论式的表达打破常识预期，引发深刻思考。这种表达比直接说理更有冲击力，也更能激发读者的思考——好的哲理诗，往往不是给出答案，而是提出问题。"),
   ("归纳推理的运用","从具体的果实、树木入手，逐步归纳出" + LQ + "整片大地是一朵花" + RQ + "的宏大结论。这种从具体到抽象的推理，使抽象的哲理变得具体可感，也使诗歌的意境逐步扩大。"),
   ("以小见大的手法","从最常见的叶子和花朵入手，最后升华到整片大地的宏大境界。这种以小见大的手法，使读者从最熟悉的事物开始，跟随诗人的思考，最后到达宏大的视野，整个过程自然而有力。"),
 ]),
 ("文化常识", [
   ("聂鲁达","（1904—1973）智利著名诗人，1971年诺贝尔文学奖获得者。代表作有《二十首情诗和一支绝望的歌》《漫歌》等。他的诗歌气势磅礴、情感真挚，对拉美和世界诗歌产生了深远影响。"),
   ("诺贝尔文学奖","根据阿尔弗雷德·诺贝尔的遗嘱设立的文学奖项，每年颁发给" + LQ + "在文学领域创作出具有理想倾向的最佳作品的人" + RQ + "。聂鲁达于1971年获得此奖。"),
   ("陈实","中国著名西班牙语文学翻译家，翻译了大量聂鲁达、博尔赫斯等拉美作家的作品。她的翻译忠实于原作，语言简洁有力，很好地传达了原作的精神。"),
   ("世界统一性","哲学中的一个重要命题，认为万物的本质是统一的，千差万别只是表象。古希腊哲学家巴门尼德、中国古代哲学的" + LQ + "万物一体" + RQ + "思想，都表达了类似的观点。"),
 ]),
]

WORDS = [
 {"w":"繁","py":"fán","q":"□多是个谎言。","tip":"「繁」糸旁+每，读 fán 二声；「繁多」勿写「烦多」（烦火字旁，指烦恼）"},
 {"w":"谎","py":"huǎng","q":"繁多是个□言。","tip":"「谎」言字旁+荒，读 huǎng 三声；勿写「慌」（竖心旁，指慌张）"},
 {"w":"实","py":"shí","q":"因为一切果□并无差异，","tip":"「实」宝盖头+头，读 shí 二声；「果实」勿写「果食」（食字旁，指食物）"},
 {"w":"差","py":"chā","q":"因为一切果实并无□异，","tip":"「差」多音字，此处读 chā（差别），不读 chà/chāi/cī"},
 {"w":"非","py":"fēi","q":"所有树木无□一棵，","tip":"「非」读 fēi 一声；「无非」指不外乎，勿写「无飞」（飞指飞翔）"},
 {"w":"朵","py":"duǒ","q":"整片大地是一□花。","tip":"「朵」几字头+木，读 duǒ 三声；量词，用于花，勿写「躲」（身字旁）"},
]

NOTES = [
 {"w":"一片","a":"量词，用于扁平而薄的东西，这里指叶子","q":"所有的叶是这一片，"},
 {"w":"一朵","a":"量词，用于花或花朵状的东西","q":"所有的花是这一朵，"},
 {"w":"繁多","a":"种类多、数量大","q":"繁多是个谎言。"},
 {"w":"谎言","a":"不真实的话、骗人的话","q":"繁多是个谎言。"},
 {"w":"果实","a":"植物所结的可以吃的东西，这里泛指植物的果实","q":"因为一切果实并无差异，"},
 {"w":"差异","a":"差别、不同","q":"因为一切果实并无差异，"},
 {"w":"无非","a":"不外乎、只不过","q":"所有树木无非一棵，"},
]

VIDEOS = [
 ("《统一》聂鲁达 朗诵","BV1PaCiBJEsZ","统一聂鲁达朗诵"),
 ("《统一》聂鲁达 讲解","BV1ad4y1c74R","统一聂鲁达讲解"),
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

hero = '<header class="hero" id="top">\n  <div class="hero-inner">\n    <div class="hero-side">智利 · 聂鲁达</div>\n    <h1 class="hero-title">统一</h1>\n  </div>\n</header>'

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
      '<div class="sec-sub">全诗六句，以严密的推理和惊人的判断，表达了世界统一性的深刻哲理。每句含<b>注释</b>（点击可查看）、内容概括与手法分析。短篇诗歌不分部分，直接逐句解读。</div>',
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

footer = '<footer>\n  <div class="kai">统一</div>\n  <div>聂鲁达 · 智利 · 陈实译 · 世界统一性的哲理短诗</div>\n  <div>人教版九年级语文下册课文</div>\n</footer>'

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
        '<title>统一 · 聂鲁达</title>\n'
        '<meta name="description" content="智利聂鲁达《统一》逐句解读、注释、赏析，含背景、原文（背诵模式）、解读、赏析、积累、练习，适合课堂教学。">\n'
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
print("统一 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), anno_count, len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
