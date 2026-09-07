# -*- coding: utf-8 -*-
"""生成《未选择的路》课件（外国现代诗，短篇，逐句解读）。"""
import io, json, re

SRC = r"D:\App\Apps\yanshi\chibi-dumu.html"
OUT = r"D:\App\Apps\yanshi\weixuanzedelu-fuluosite.html"
LS_KEY = "weixuanzelu_fs"

LQ = "\u201c"
RQ = "\u201d"

def A(word, note):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)

CARDS = [
("黄色的树林里分出两条路，",
 "第一节开篇，写诗人来到一片黄色的树林中，面前出现了两条岔路。",
 "LQ" + "黄色的树林" + RQ + "点明季节（秋天），也渲染了一种苍茫、萧瑟的氛围；" + LQ + "两条路" + RQ + "是全诗的核心意象，象征人生道路的选择。"),
("可惜我不能同时去" + A("涉足","进入某种环境或范围。此处指走上那条路") + "，",
 "诗人感叹自己不能同时踏上两条路——人生的选择具有排他性。",
 "LQ" + "可惜" + RQ + "直接表达遗憾之情；" + LQ + "不能同时去涉足" + RQ + "写出了选择的必然性与排他性——你只能选一条，不能两条都走。"),
("我在那路口久久" + A("伫立","长时间地站着") + "，",
 "诗人在路口久久站立，沉思该选哪一条路。",
 "LQ" + "久久伫立" + RQ + "写出了选择的慎重与艰难——这不是一个可以轻易做出的决定，而是需要反复权衡的人生抉择。"),
("我向着一条路" + A("极目","用尽目力（远望）") + "望去，",
 "诗人极目远眺一条路的尽头，试图看清它的走向。",
 "LQ" + "极目望去" + RQ + "写出了诗人对未来的探询——他想知道选择这条路会通向何方，但未来总是难以预知的。"),
("直到它消失在丛林深处。",
 "然而那条路蜿蜒曲折，最终消失在丛林深处，看不清尽头。",
 "LQ" + "消失在丛林深处" + RQ + "象征未来的不可预知——无论你怎么眺望，都无法看清人生道路的终点。这为下文的选择增添了神秘感与不确定性。"),
("但我却选了另外一条路，",
 "第二节转折，诗人最终选择了另一条路——那条人迹更少的路。",
 "LQ" + "但" + RQ + "表转折，说明诗人的选择出乎常情——大多数人会选那条看起来更好走的路，而诗人却选了另一条。"),
("它" + A("荒草萋萋","形容草长得茂盛的样子。萋萋，草茂盛") + "，十分" + A("幽寂","幽静寂寞") + "，",
 "诗人选择的这条路荒草茂盛、幽静寂寞，少有人来。",
 "LQ" + "荒草萋萋" + RQ + LQ + "幽寂" + RQ + "写出了这条路的荒凉与冷僻——正因为少有人走，才显得更加幽静。这是诗人选择的路的特征。"),
("显得更诱人，更美丽；",
 "在诗人眼中，这条荒草萋萋的路反而显得更诱人、更美丽。",
 "LQ" + "更诱人，更美丽" + RQ + "两个" + LQ + "更" + RQ + "构成比较，写出了诗人对这条少有人走的路的独特审美——未知的、充满挑战的道路反而更有吸引力。"),
("虽然在这条小路上，",
 "诗人承认：虽然这条小路看起来更诱人美丽，",
 "LQ" + "虽然" + RQ + "表让步，引出下文的转折——这条路虽美，但也有它的现实状况。"),
("很少留下旅人的足迹。",
 "但这条路上很少有旅人走过——它是一条人迹罕至的路。",
 "LQ" + "很少留下旅人的足迹" + RQ + "点明了这条路的本质——人迹更少。这正是诗人选择它的原因，也是全诗" + LQ + "未选择的路" + RQ + "的深意所在。"),
("那天清晨落叶满地，",
 "第三节回溯选择那天的情景：清晨，落叶铺满了地面。",
 "LQ" + "清晨" + RQ + LQ + "落叶满地" + RQ + "营造了一种宁静而略带萧瑟的氛围，也暗示这是一个崭新的开始——清晨是一天的开始，选择是人生的新起点。"),
("两条路都未经脚印污染。",
 "因为是清晨，两条路上都还没有行人的脚印——它们同样纯净，同样未知。",
 "LQ" + "未经脚印污染" + RQ + "用" + LQ + "污染" + RQ + "一词，将行人的脚印视为对道路的" + LQ + "污染" + RQ + "，表达了诗人对原始、未被涉足的道路的珍视。两条路都还纯净，选择因此更加自由。"),
("啊，留下一条路等改日再见！",
 "诗人感叹：就把另一条路留到以后再走吧！",
 "LQ" + "啊" + RQ + "是感叹词，表达了一种无奈与自我安慰；" + LQ + "等改日再见" + RQ + "是诗人对自己的安慰——虽然今天只能选一条，但以后还有机会走另一条。"),
("但我知道路径" + A("延绵","延续不断") + "无尽头，",
 "然而诗人清醒地知道：道路绵延无尽，一旦选择，就很难回头。",
 "LQ" + "但" + RQ + "再次转折，打破了上一句的自我安慰；" + LQ + "延绵无尽头" + RQ + "写出了人生道路的漫长与不可逆——一旦走上一条路，就会越走越远，难以回头。"),
("恐怕我难以再回返。",
 "诗人坦言：恐怕自己再也无法回到这个路口，重新选择了。",
 "LQ" + "恐怕" + RQ + LQ + "难以再回返" + RQ + "写出了选择的不可逆性——人生没有回头路，每一个选择都意味着放弃其他可能。这是全诗最深刻的感慨之一。"),
("也许多少年后在某个地方，",
 "第四节展望未来：也许多年以后，在某个地方，",
 "LQ" + "也许" + RQ + "表达了一种不确定的推测——未来会怎样，谁也无法预知；" + LQ + "多少年后" + RQ + "将时间拉远，为全诗的哲理升华做铺垫。"),
("我将轻声叹息将往事回顾：",
 "诗人会轻声叹息着，回顾今天做出的这个选择。",
 "LQ" + "轻声叹息" + RQ + "是全诗情感最微妙的地方——不是悔恨，也不是庆幸，而是一种复杂的、难以言说的感慨。" + LQ + "将往事回顾" + RQ + "引出下文对选择的总结。"),
("一片树林里分出两条路——",
 "诗人回顾往事：当年在那片树林里，有两条路摆在面前。",
 "此句与首节" + LQ + "黄色的树林里分出两条路" + RQ + "呼应，形成首尾圆合的结构。破折号引出下文的总结——选择的结果。"),
("而我选择了人迹更少的一条，",
 "而我，选择了那条人迹更少的路。",
 "LQ" + "人迹更少的一条" + RQ + "是全诗的核心——诗人选择了一条不寻常的路。这不是一个简单的选择，而是一种人生态度：不随波逐流，敢于走自己的路。"),
("从此决定了我一生的道路。",
 "全诗点睛：正是这个选择，决定了我一生的道路。",
 "LQ" + "从此决定了我一生的道路" + RQ + "是全诗的诗眼——一个看似偶然的选择，却决定了整个人生的走向。这是对选择之重要性的深刻概括，也是全诗哲理的最高升华。"),
]

FULLTEXT = [
 "黄色的树林里分出两条路，",
 "可惜我不能同时去涉足，",
 "我在那路口久久伫立，",
 "我向着一条路极目望去，",
 "直到它消失在丛林深处。",
 "但我却选了另外一条路，",
 "它荒草萋萋，十分幽寂，",
 "显得更诱人，更美丽；",
 "虽然在这条小路上，",
 "很少留下旅人的足迹。",
 "那天清晨落叶满地，",
 "两条路都未经脚印污染。",
 "啊，留下一条路等改日再见！",
 "但我知道路径延绵无尽头，",
 "恐怕我难以再回返。",
 "也许多少年后在某个地方，",
 "我将轻声叹息将往事回顾：",
 "一片树林里分出两条路——",
 "而我选择了人迹更少的一条，",
 "从此决定了我一生的道路。",
]

BG_LEAD = [
 "罗伯特·弗罗斯特（1874—1963），美国20世纪最受欢迎的诗人之一，曾四度获得普利策诗歌奖。《未选择的路》是他最著名的诗作之一，写于1915年，收录于诗集《山间低地》。诗中描写了一个旅人在秋日树林中面对两条岔路的选择，以象征手法写出了人生道路选择的必然性、不可逆性与深远影响。",
 "全诗四节二十行，以林中岔路的选择象征人生道路的选择。诗人没有写选择了哪条路的具体经历，而是聚焦于" + LQ + "未选择" + RQ + "——那条没有走的路，恰恰是最令人念念不忘的。这首诗语言朴素自然，意境深远，是美国诗歌中被引用最多、也最被误读的作品之一。",
]

AUTHOR = [
 "罗伯特·弗罗斯特（Robert Frost，1874—1963），美国20世纪最著名的诗人之一，出生于旧金山，11岁时随母亲迁居新英格兰。他当过纺织工人、教师、农场主，长期生活在新英格兰的乡村，其诗歌多以新英格兰的乡村生活和自然景色为题材，语言朴素自然，寓意深刻。",
 "弗罗斯特曾四度获得普利策诗歌奖（1924、1931、1937、1943），是美国历史上获此殊荣最多的诗人。1961年，他应邀在肯尼迪总统的就职典礼上朗诵诗歌，成为美国文化史上的标志性事件。代表作有《白桦树》《修墙》《雪夜林边驻马》《未选择的路》等。",
]

STORY = [
 ("写作缘起","1912年，弗罗斯特38岁，他做出了一个重大决定：卖掉农场，举家迁往英国，专心写诗。在英国期间，他结识了庞德等诗人，出版了第一部诗集《一个男孩的意愿》（1913）和第二部《波士顿以北》（1914）。1915年回美国后，他写下了《未选择的路》——这首诗某种程度上也是对自己人生选择的回顾。"),
 ("诗人的自白","弗罗斯特本人曾说，这首诗是" + LQ + "关于我朋友爱德华·托马斯的" + RQ + "。托马斯是一位英国诗人，每次和弗罗斯特在乡间散步时，总会对选择哪条路犹豫不决，事后又常常后悔没走另一条。弗罗斯特以这首诗调侃朋友的优柔寡断，但诗中蕴含的哲理却远远超出了个人轶事。"),
 ("最被误读的诗","《未选择的路》是美国诗歌中被引用最多、也最被误读的作品。许多人把它解读为" + LQ + "走自己的路，让别人说去吧" + RQ + "式的个人主义宣言，但弗罗斯特本人却说这首诗" + LQ + "很微妙" + RQ + "——诗中" + LQ + "轻声叹息" + RQ + "的复杂情感，以及" + LQ + "未选择的路" + RQ + "的念念不忘，都暗示了选择的惆怅与遗憾，而非简单的自豪。"),
 ("统编版译文","本诗以顾子欣的译本为准，是统编版语文教材七年级下册的课文。顾子欣（1939— ）是中国著名的翻译家，主要译作有英诗、英美小说等。"),
]

APP_ART = [
 ("象征手法：路=人生道路","全诗最核心的艺术手法是象征。" + LQ + "黄色的树林里分出两条路" + RQ + "——" + LQ + "路" + RQ + "象征人生道路，" + LQ + "两条路" + RQ + "象征人生中面临的选择，" + LQ + "路口" + RQ + "象征做出选择的时刻，" + LQ + "丛林深处" + RQ + "象征未来的不可预知。整首诗就是一个完整的象征体系，以具体的行路选择写出抽象的人生哲理。"),
 ("选择的惆怅与必然性","诗中写出了选择的多重感受：" + LQ + "可惜我不能同时去涉足" + RQ + "是选择的排他性带来的遗憾；" + LQ + "久久伫立" + RQ + "是选择的慎重与艰难；" + LQ + "恐怕我难以再回返" + RQ + "是选择的不可逆性；" + LQ + "轻声叹息" + RQ + "是回望选择时复杂的感慨。诗人没有美化选择，而是写出了选择的全部重量。"),
 (LQ + "未选择" + RQ + "的深意","全诗题为" + LQ + "未选择的路" + RQ + "，但诗中大量笔墨写的是" + LQ + "选择了" + RQ + "的那条路。" + LQ + "未选择" + RQ + "的深意在于：那条没有走的路，恰恰是最令人念念不忘的——人生中，我们常常怀念那些没有做出的选择，想象" + LQ + "如果当初选了另一条路会怎样" + RQ + "。这种" + LQ + "未选择" + RQ + "的惆怅，是人类共通的情感体验。"),
 ("朴素自然的语言风格","弗罗斯特的诗歌语言以朴素自然著称。全诗没有生僻的词汇，没有华丽的修辞，几乎就是日常口语——" + LQ + "黄色的树林里分出两条路" + RQ + LQ + "可惜我不能同时去涉足" + RQ + "，像是在讲一个简单的故事。然而正是在这种朴素中，蕴含着最深刻的人生哲理，这正是弗罗斯特的高明之处。"),
]

APP_FAME = [
 ("黄色的树林里分出两条路，可惜我不能同时去涉足，我在那路口久久伫立。",
  "开篇三句，写出了选择的情境与心境。" + LQ + "黄色的树林" + RQ + "点明秋景，渲染苍茫氛围；" + LQ + "两条路" + RQ + "是核心意象，象征人生选择；" + LQ + "不能同时去涉足" + RQ + "写出选择的排他性；" + LQ + "久久伫立" + RQ + "写出选择的慎重。三句诗，将人生面临重大选择时的情境与心境写得淋漓尽致。"),
("但我却选了另外一条路，它荒草萋萋，十分幽寂，显得更诱人，更美丽；虽然在这条小路上，很少留下旅人的足迹。",
  "这几句写出了诗人的选择及其原因。" + LQ + "但" + RQ + "表转折，说明选择出乎常情；" + LQ + "荒草萋萋" + RQ + LQ + "幽寂" + RQ + "写出这条路的荒凉冷僻；" + LQ + "更诱人，更美丽" + RQ + "写出诗人对这条路的独特审美；" + LQ + "很少留下旅人的足迹" + RQ + "点明这是一条人迹更少的路。选择少有人走的路，本身就是一种人生态度。"),
("也许多少年后在某个地方，我将轻声叹息将往事回顾：一片树林里分出两条路——而我选择了人迹更少的一条，从此决定了我一生的道路。",
  "全诗的精华与诗眼所在。" + LQ + "也许" + RQ + "表达对未来的不确定；" + LQ + "轻声叹息" + RQ + "是全诗情感最微妙的地方——不是悔恨，也不是庆幸，而是一种复杂的感慨；" + LQ + "人迹更少的一条" + RQ + "点明选择的实质；" + LQ + "从此决定了我一生的道路" + RQ + "是全诗的哲理升华——一个选择，决定一生。这几句是美国诗歌中被引用最多的名句之一。"),
]

APP_THEME = [
 "本诗以林中岔路的选择为象征，写出了人生道路选择的必然性、不可逆性与深远影响。诗人描写了一个旅人在秋日树林中面对两条岔路时的犹豫与选择：他久久伫立，极目远眺，最终选择了那条荒草萋萋、人迹更少的路；他知道路径延绵无尽头，恐怕难以再回返；多年以后，他会轻声叹息着回顾这个选择——正是选择了人迹更少的一条路，决定了他一生的道路。",
 "全诗的深刻之处在于：它没有简单地赞美" + LQ + "走自己的路" + RQ + "，而是写出了选择的全部复杂性——有遗憾（不能同时走两条路），有慎重（久久伫立），有不可逆（难以再回返），有回望时的复杂感慨（轻声叹息）。" + LQ + "未选择的路" + RQ + "这个题目本身就暗示了：那条没有走的路，才是最令人念念不忘的。这是对人生选择的深刻洞察，也是人类共通的情感体验。",
]

ACC = [
 ("重点词语", [
   ("涉足","进入某种环境或范围。诗中指走上那条路。"),
   ("伫立","长时间地站着。"),
   ("极目","用尽目力（远望）。"),
   ("荒草萋萋","形容草长得茂盛的样子。萋萋，草茂盛。"),
   ("幽寂","幽静寂寞。"),
   ("延绵","延续不断。"),
   ("回返","返回、回头。"),
   ("人迹","人的足迹。"),
 ]),
 ("用字与读音", [
   ("伫","读 zhù，四声；单人旁，" + LQ + "伫立" + RQ + "指长时间站立；勿写" + LQ + "贮" + RQ + "（贝字旁）。"),
   ("萋","读 qī，一声；草字头，" + LQ + "萋萋" + RQ + "形容草茂盛；勿写" + LQ + "凄" + RQ + "（两点水）。"),
   ("寂","读 jì，四声；宝盖头，" + LQ + "幽寂" + RQ + "指幽静寂寞。"),
   ("延","读 yán，二声；" + LQ + "延绵" + RQ + "指延续不断；勿写" + LQ + "沿" + RQ + "（三点水）。"),
   ("绵","读 mián，二声；绞丝旁，" + LQ + "延绵" + RQ + "；勿写" + LQ + "棉" + RQ + "（木字旁）。"),
   ("迹","读 jì，四声；" + LQ + "人迹" + RQ + "指人的足迹；勿写" + LQ + "际" + RQ + "（左耳旁）。"),
 ]),
 ("修辞方法", [
   ("象　征", LQ + "路" + RQ + "象征人生道路，" + LQ + "两条路" + RQ + "象征人生选择，" + LQ + "路口" + RQ + "象征选择时刻，" + LQ + "丛林深处" + RQ + "象征未来的不可预知。全诗是一个完整的象征体系。"),
   ("反　复", LQ + "更诱人，更美丽" + RQ + "——两个" + LQ + "更" + RQ + "反复，强调诗人对这条路的独特审美；首尾" + LQ + "树林里分出两条路" + RQ + "反复呼应，形成圆合结构。"),
   ("对　比", "两条路的对比：一条" + LQ + "极目望去" + RQ + "（看起来好走），一条" + LQ + "荒草萋萋" + RQ + "（人迹更少）；选择前的" + LQ + "久久伫立" + RQ + "与选择后的" + LQ + "轻声叹息" + RQ + "对比。"),
   ("拟　人", LQ + "路径延绵无尽头" + RQ + "——将路径拟人化，仿佛它有自己的意志，一直延伸下去，不肯给人回头的机会。"),
 ]),
 ("写作借鉴", [
   ("以小见大的象征","以林中岔路的选择这一小事，写出人生道路选择这一大主题。象征手法的运用使抽象的哲理变得具体可感。"),
   ("聚焦" + LQ + "未选择" + RQ + "","全诗题为" + LQ + "未选择的路" + RQ + "，但大量笔墨写" + LQ + "选择了" + RQ + "的路。" + LQ + "未选择" + RQ + "的念念不忘，恰恰是最深刻的情感——这种写法比直接写" + LQ + "选择了正确的路" + RQ + "更有张力。"),
   ("朴素中见深刻","全诗语言朴素自然，几乎是日常口语，但蕴含着最深刻的人生哲理。这种" + LQ + "于无声处听惊雷" + RQ + "的写法，是诗歌的高境界。"),
   ("首尾圆合的结构","首节" + LQ + "黄色的树林里分出两条路" + RQ + "，末节" + LQ + "一片树林里分出两条路" + RQ + "——首尾呼应，形成圆合结构，使全诗浑然一体。"),
 ]),
]

WORDS = [
 {"w":"伫","py":"zhù","q":"我在那路口久久□立，","tip":"「伫」单人旁，读 zhù 四声；勿写「贮」（贝字旁）"},
 {"w":"萋萋","py":"qī qī","q":"它荒草□□，十分幽寂，","tip":"「萋萋」草字头，读 qī qī；形容草茂盛，勿写「凄凄」（两点水）"},
 {"w":"寂","py":"jì","q":"它荒草萋萋，十分幽□，","tip":"「寂」宝盖头，读 jì 四声；「幽寂」指幽静寂寞"},
 {"w":"延","py":"yán","q":"但我知道路径□绵无尽头，","tip":"「延」读 yán 二声；「延绵」指延续不断，勿写「沿」（三点水）"},
 {"w":"绵","py":"mián","q":"但我知道路径延□无尽头，","tip":"「绵」绞丝旁，读 mián 二声；勿写「棉」（木字旁）"},
 {"w":"迹","py":"jì","q":"而我选择了人□更少的一条，","tip":"「迹」读 jì 四声；「人迹」指人的足迹，勿写「际」（左耳旁）"},
]

NOTES = [
 {"w":"涉足","a":"进入某种环境或范围；诗中指走上那条路","q":"可惜我不能同时去涉足，"},
 {"w":"伫立","a":"长时间地站着","q":"我在那路口久久伫立，"},
 {"w":"极目","a":"用尽目力（远望）","q":"我向着一条路极目望去，"},
 {"w":"荒草萋萋","a":"形容草长得茂盛的样子。萋萋，草茂盛","q":"它荒草萋萋，十分幽寂，"},
 {"w":"幽寂","a":"幽静寂寞","q":"它荒草萋萋，十分幽寂，"},
 {"w":"延绵","a":"延续不断","q":"但我知道路径延绵无尽头，"},
 {"w":"回返","a":"返回、回头","q":"恐怕我难以再回返。"},
 {"w":"人迹","a":"人的足迹","q":"而我选择了人迹更少的一条，"},
]

VIDEOS = [
 ("诗歌朗诵《未选择的路》弗罗斯特","BV1Kd4y1M7jj","诗歌朗诵《未选择的路》"),
 ("细读经典：弗罗斯特《未选择的路》","BV1PyTF6ZEPH","细读经典《未选择的路》"),
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

hero = '<header class="hero" id="top">\n  <div class="hero-inner">\n    <div class="hero-side">美国·弗罗斯特</div>\n    <h1 class="hero-title">未选择的路</h1>\n  </div>\n</header>'

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
      '<div class="sec-sub">全诗四节二十行，以林中岔路的选择象征人生道路的选择。每句含<b>注释</b>（点击可查看）、内容概括与手法分析。短篇诗歌不分部分，直接逐句解读。</div>',
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
       '<div class="sec-head"><h2>积 累</h2><span class="no">词语 · 读音 · 修辞 · 写作</span></div>']
for cat, items in ACC:
    acc.append('<div class="box"><h3>%s</h3>' % cat)
    acc.append('<div class="tw"><table>')
    acc.append('<tr><th>词语</th><th>释义</th></tr>')
    for w, d in items:
        acc.append('<tr><td class="kai">%s</td><td>%s</td></tr>' % (w, d))
    acc.append('</table></div></div>')
acc.append('</section>')

practice = ['<section id="practice">',
            '<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写 · 字词 / 词语</span></div>',
            '<div class="sec-sub">以全篇<b>易错字词</b>与<b>重点词语</b>为题库，点击按钮进入<b>全屏听写</b>：先看提示在纸上默写，再核对答案。随机五组适合随堂小测，全部适合系统复习。</div>',
            '<div class="ptools">',
            '<button data-mode="word" data-rand="5">随机五组字形</button>',
            '<button data-mode="word" data-all="1">全部字形</button>',
            '<button data-mode="note" data-rand="5">随机五组词语</button>',
            '<button data-mode="note" data-all="1">全部词语</button>',
            '</div></section>']

footer = '<footer>\n  <div class="kai">未选择的路</div>\n  <div>弗罗斯特 · 美国 · 顾子欣译</div>\n</footer>'

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
        '<title>未选择的路</title>\n'
        '<meta name="description" content="美国弗罗斯特《未选择的路》逐句解读、注释、赏析，含背景、原文（背诵模式）、解读、赏析、积累、练习，适合课堂教学。">\n'
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
print("未选择的路 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), anno_count, len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
