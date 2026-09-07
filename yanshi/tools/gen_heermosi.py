# -*- coding: utf-8 -*-
"“”生成《赫耳墨斯和雕像者》课件 HTML（伊索寓言，短篇）“”"
import json, re, html as htmlmod

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\heermosihediaoxiangzhe-yisuoyuyan.html"

src = open(TEMPLATE, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
css += "\n  .acc-sub{font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:8px;color:var(--teal-deep);margin:14px 0 6px;font-size:calc(16px*var(--fs))}\n"
mains = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = mains[0].replace("beiying_fs", "heermosi_fs")

H = "古希腊·伊索"
TITLE = "赫耳墨斯和雕像者"

LEAD = [
    "《赫耳墨斯和雕像者》选自《伊索寓言》，是一篇短小精悍的寓言故事。赫耳墨斯是古希腊神话中的神使，又是商人的庇护神。他想知道自己在人间受到多大的尊重，便化作凡人来到雕像者的店里。他先问宙斯雕像的价格，又问赫拉雕像的价格，最后看到自己的雕像，心想人们会更尊重他，不料雕像者却说他的雕像“算添头，白送”。故事以辛辣的讽刺，揭露了那些爱慕虚荣、自高自大的人往往不被人重视的现实。",
    "本文是统编版七年级上册第六单元的教读课文，与《蚊子和狮子》同属《寓言四则》。学习时要把握寓言篇幅短小、寓意深刻的特点，通过人物的语言和心理描写分析人物形象，理解故事的寓意。",
]

AUTHOR = [
    "伊索（约公元前6世纪），古希腊著名的寓言家。据传说，伊索原是萨摩斯岛的奴隶，因才智出众被主人释放为自由民，后游历希腊各地，讲述寓言故事。公元前5世纪末，“伊索”这个名字已为古希腊人所熟知，人们把古希腊寓言都归在他的名下。",
    "《伊索寓言》相传为伊索所著，实际是古希腊人在相当长的历史时期内的集体创作，经后人整理汇编而成。全书共收录寓言300余则，大多以动物为主人公，采用拟人化手法，用简短的故事揭示深刻的道理，语言精练，寓意深刻，对后世欧洲寓言创作产生了深远影响。名篇有《狐狸和葡萄》《农夫和蛇》《龟兔赛跑》《蚊子和狮子》等。",
]

BG = [
    ("寓言知识", [
        "寓言是文学作品的一种体裁，以比喻性的故事寄寓意味深长的道理，给人以启示。寓言早在我国春秋战国时代就已经盛行，诸子百家的著作中都有不少优秀寓言流传下来。在国外，古希腊的《伊索寓言》是最著名的寓言集。",
        "寓言的基本特征：①篇幅短小，语言精练；②主人公可以是人，也可以是拟人化的动植物或其他事物；③多用夸张、拟人、比喻等手法；④具有鲜明的哲理性和讽刺性，故事背后蕴含深刻的道理。",
        "《赫耳墨斯和雕像者》是《伊索寓言》中的名篇，以神为主人公，通过对话和心理描写，讽刺了爱慕虚荣的人。故事短小精悍，寓意深刻，是寓言的典范之作。",
    ]),
    ("古希腊神话背景", [
        "赫耳墨斯（Hermes）是古希腊神话中的众神使者，宙斯与迈亚之子。他是商业、旅行、畜牧、体育等的保护神，也是商人的庇护神。他行走如飞，多才多艺，发明了尺、数和字母，也是希腊字母的创造者。在罗马神话中，他被称为墨丘利（Mercury）。",
        "宙斯（Zeus）是古希腊神话中的众神之王，统治宇宙万物的至高无上的主神。赫拉（Hera）是宙斯的妻子，众神之后，掌管婚姻和家庭。在古希腊神话体系中，宙斯、赫拉、赫耳墨斯都是重要的神祇，但地位不同——宙斯最高，赫拉次之，赫耳墨斯再次之。故事中雕像价格的差异，正反映了他们在人间受到的不同程度的尊重。",
    ]),
]

VIDEOS = [
    ("课文朗读《赫耳墨斯和雕像者》",
     "BV1rb3q6MEy2",
     "https://www.bilibili.com/video/BV1rb3q6MEy2",
     "mediaF1"),
    ("伊索寓言《赫耳墨斯与雕像者》",
     "BV1n6RRYiEm3",
     "https://www.bilibili.com/video/BV1n6RRYiEm3",
     "mediaF2"),
]

VERSES = [
("", "全文解读", "全文",
 "赫耳墨斯化作凡人来到雕像店，通过询问宙斯、赫拉和自己雕像的价格，发现自己并不被人重视，讽刺了爱慕虚荣的人。",
 [
(1, "赫耳墨斯想知道他在人间受到多大的尊重，就化作凡人，来到一个雕像者的店里。",
 "赫耳墨斯想知道自己在人间受尊重的程度，化作凡人来到雕像店。",
 "开篇交代故事的起因和人物动机：“想知道他在人间受到多大的尊重”，直接点出赫耳墨斯的虚荣心——他最关心的不是别的，而是自己受尊重的程度；“化作凡人”是神话的典型情节，神变成凡人来试探人间，为下文的对话铺垫。",
 [("赫耳墨斯","（hè ěr mò sī）古希腊神话中的神使，商业和商人的庇护神"),("尊重","尊敬、敬重。尊，尊敬"),("化作","变成。化，变化"),("凡人","平常的人、普通人（与“神”相对）。凡，平常"),("雕像者","雕刻雕像的工匠。雕像，雕刻的人像")]),
(2, "他看见宙斯的雕像，问道：“值多少钱？”雕像者说：“一个银元。”",
 "赫耳墨斯问宙斯雕像的价格，雕像者回答一个银元。",
 "第一次问答。宙斯是众神之王，他的雕像只值“一个银元”，价格并不高。这为下文赫耳墨斯的心理落差埋下伏笔——连最高的神都只值一个银元，赫耳墨斯的雕像能值多少呢？对话简洁，符合寓言精练的特点。",
 [("宙斯","（zhòu sī）古希腊神话中的众神之王"),("银元","旧时使用的银质硬币。元，货币单位")]),
(3, "赫耳墨斯又笑着问道：“赫拉的雕像值多少钱？”雕像者说：“还要贵一点。”",
 "赫耳墨斯又笑着问赫拉雕像的价格，雕像者说还要贵一点。",
 "第二次问答。“又笑着问道”中的“笑”字值得玩味——这是一种什么笑？是觉得宙斯的雕像太便宜的轻蔑之笑，还是觉得自己的雕像会更贵的得意之笑？结合下文他对自己的定位，这“笑”中含着虚荣和自负。赫拉是宙斯的妻子、众神之后，雕像“还要贵一点”，价格比宙斯还高，这也出乎常理，增加了故事的讽刺意味。",
 [("赫拉","（hè lā）古希腊神话中的众神之后，宙斯的妻子"),("贵","价格高、价值大")]),
(4, "后来，赫耳墨斯看见自己的雕像，心想他身为神使，又是商人的庇护神，人们对他会更尊重些，于是问道：“这个值多少钱？”",
 "赫耳墨斯看到自己的雕像，心想自己身为神使和商人庇护神，人们会更尊重他，便问自己雕像的价格。",
 "心理描写是全文的关键。“心想他身为神使，又是商人的庇护神，人们对他会更尊重些”——赫耳墨斯对自己的定位很高，认为自己既是神使又是商人庇护神，应该比宙斯和赫拉更受尊重。这种自我膨胀的心理，与下文雕像者的回答形成巨大反差，是讽刺效果的核心。“于是问道”中的“于是”写出他的自信满满，迫不及待想听到自己雕像的高价。",
 [("神使","神的使者。赫耳墨斯是众神的使者"),("庇护神","保护、庇护的神。庇护，包庇、保护"),("尊重","尊敬、重视")]),
(5, "雕像者回答说：“假如你买了那两个，这个算添头，白送。”",
 "雕像者回答说，如果买了那两个，赫耳墨斯的雕像算添头，白送。",
 "故事的高潮和结局，也是全文最具讽刺力的一句。“假如你买了那两个，这个算添头，白送”——赫耳墨斯的雕像不仅不值钱，而且是“添头”（买东西时额外赠送的），“白送”（免费赠送）。这与赫耳墨斯“人们对他会更尊重些”的心理预期形成天壤之别，虚荣心得以彻底破灭。雕像者的回答平淡而冷酷，却如同一记响亮的耳光，打在爱慕虚荣者的脸上。",
 [("假如","如果、假使（表示假设）。假，假设"),("添头","（tiān tou）买东西时商家额外赠送的东西。添，增加"),("白送","免费赠送、不要钱。白，无代价")]),
(6, "这个故事适用于那些爱慕虚荣而不被人重视的人。",
 "点明寓意：故事适用于爱慕虚荣而不被人重视的人。",
 "独句成段，直接点明寓意。“爱慕虚荣而不被人重视”是对赫耳墨斯形象的精准概括，也是故事的教训。“适用于”一词说明这则寓言具有普遍意义——它不仅适用于赫耳墨斯，也适用于所有像他一样爱慕虚荣、自高自大的人。寓言的结尾往往直接点明寓意，这是寓言的典型结构。",
 [("爱慕虚荣","喜欢表面上的光彩、荣耀。爱慕，喜爱；虚荣，表面上的荣耀"),("重视","认为人的德才优良或事物的作用重要而认真对待。重，重要")]),
]),
]

APP = [
("人物形象", [
("赫耳墨斯", "爱慕虚荣、自高自大、自命不凡的神。他“想知道他在人间受到多大的尊重”，最关心的是自己的地位和名誉；他“笑着”问赫拉雕像的价格，笑中含着轻蔑和得意；他“心想他身为神使，又是商人的庇护神，人们对他会更尊重些”，自我膨胀到了极点。然而现实是残酷的——他的雕像“算添头，白送”，虚荣心彻底破灭。赫耳墨斯的形象具有典型意义，代表了所有那些自视甚高、实则无足轻重的人。"),
("雕像者", "冷静、务实、直言不讳的商人。他的回答简短而准确：宙斯的雕像“一个银元”，赫拉的“还要贵一点”，赫耳墨斯的“算添头，白送”。他不因为对方是神（虽然赫耳墨斯化作了凡人）而阿谀奉承，而是如实报价。雕像者的存在是一面镜子，照出了赫耳墨斯的虚荣，也照出了现实的冷酷——在人间，神的地位并不像神自己想象的那样高。"),
]),
("艺术特色", [
("篇幅短小，寓意深刻", "全文仅200余字，却讲述了一个完整的故事，塑造了鲜明的人物形象，揭示了深刻的道理。这是寓言的典型特征——以极简的篇幅承载极深的寓意。故事按照“问宙斯→问赫拉→问自己”的顺序展开，三问三答，层层递进，最后以“白送”二字戛然而止，余味无穷。"),
("对话描写精练传神", "全文主要由对话构成，人物的语言极其精练。赫耳墨斯的三问，从平静到“笑着”到自信满满，语气的变化折射出心理的变化；雕像者的三答，从“一个银元”到“还要贵一点”到“算添头，白送”，价格的落差构成了强烈的讽刺。对话中没有多余的修饰，却字字珠玑。"),
("心理描写画龙点睛", "文中只有一处心理描写——“心想他身为神使，又是商人的庇护神，人们对他会更尊重些”，但这一处心理描写至关重要。它揭示了赫耳墨斯的内心世界，让读者看到他虚荣、自负的本质，也为下文的戏剧性转折做足了铺垫。正是因为有了这份“自信”，下文的“白送”才更具讽刺力。"),
("对比手法突出主题", "全文贯穿着对比：赫耳墨斯的自我定位（“人们对他会更尊重些”）与现实（“算添头，白送”）的对比；宙斯、赫拉雕像的价格与赫耳墨斯雕像价格的对比；赫耳墨斯的“笑”与最终的尴尬的对比。对比使人物形象更加鲜明，讽刺效果更加强烈。"),
("讽刺手法辛辣有力", "寓言最突出的艺术特色是讽刺。作者不直接议论，而是通过赫耳墨斯的言行和雕像者的回答，让读者在笑声中看清爱慕虚荣者的可笑与可悲。“算添头，白送”五个字，是全文最辛辣的讽刺——一个自视甚高的神，在人间竟然连一个银元都不值，这种巨大的落差本身就是最有力的批判。"),
]),
("名句赏析", [
("“心想他身为神使，又是商人的庇护神，人们对他会更尊重些。”", "这是全文唯一的心理描写，也是理解人物形象的关键。“身为神使，又是商人的庇护神”——赫耳墨斯给自己列了两个“光环”，觉得自己身份特殊、地位不凡；“人们对他会更尊重些”——“更”字说明他是在与宙斯、赫拉比较，觉得自己应该比他们更受尊重。这种自我膨胀的心理，与下文“白送”的现实形成强烈反差，是讽刺效果的核心。"),
("“假如你买了那两个，这个算添头，白送。”", "全文最具讽刺力的一句话，也是故事的点睛之笔。“假如你买了那两个”——先设条件，说明赫耳墨斯的雕像不能单独出售；“这个算添头”——“添头”是买东西时赠送的，说明赫耳墨斯的雕像没有独立价值；“白送”——免费赠送，说明他的雕像一文不值。三个短句层层递进，把赫耳墨斯的身价贬到了极点，虚荣心得以彻底破灭。"),
("“这个故事适用于那些爱慕虚荣而不被人重视的人。”", "寓言的结尾，直接点明寓意。“爱慕虚荣而不被人重视”是对赫耳墨斯形象的精准概括，也是故事的教训。“适用于”说明这则寓言具有普遍的警示意义——它不仅是讲给赫耳墨斯听的，也是讲给所有像他一样的人听的。这种卒章显志的写法，是寓言的典型结构。"),
]),
("主题思想", [
("讽刺爱慕虚荣、自高自大的人", "文章通过赫耳墨斯自命不凡、最终碰壁的故事，辛辣地讽刺了那些爱慕虚荣、自高自大、自视甚高的人。赫耳墨斯身为神使和商人庇护神，觉得自己应该比宙斯、赫拉更受尊重，结果他的雕像“算添头，白送”——现实给了他最响亮的耳光。故事告诉我们：越是爱慕虚荣、自高自大的人，往往越不被人重视。"),
("揭示自我认知与他人评价的落差", "故事深刻揭示了自我认知与他人评价之间往往存在巨大落差。赫耳墨斯认为自己“人们对他会更尊重些”，但在雕像者眼中，他的雕像一文不值。这种落差不仅存在于神的世界，也存在于现实生活中——很多人对自己的评价远远高于他人对自己的评价。故事提醒我们：要有自知之明，不要高估自己在别人心中的地位。"),
("寓言的普遍警示意义", "作为一则寓言，《赫耳墨斯和雕像者》具有超越时空的普遍意义。它不仅适用于古希腊，也适用于今天；不仅适用于神，也适用于每一个普通人。故事告诫我们：要谦虚谨慎，不要爱慕虚荣；要正确认识自己，不要自高自大。只有脚踏实地、谦虚待人，才能赢得真正的尊重。"),
]),
]

ACC = [
("重点词语", [
("赫耳墨斯", "（hè ěr mò sī）古希腊神话中的神使，商业和商人的庇护神。"),
("尊重", "尊敬、敬重。"),
("化作", "变成。"),
("凡人", "平常的人、普通人（与“神”相对）。"),
("雕像者", "雕刻雕像的工匠。"),
("宙斯", "（zhòu sī）古希腊神话中的众神之王。"),
("赫拉", "（hè lā）古希腊神话中的众神之后，宙斯的妻子。"),
("神使", "神的使者。"),
("庇护神", "保护、庇护的神。"),
("添头", "（tiān tou）买东西时商家额外赠送的东西。"),
("白送", "免费赠送、不要钱。"),
("爱慕虚荣", "喜欢表面上的光彩、荣耀。"),
]),
("用字与读音", [
("赫", "读hè，不读hǎo。左右结构，赤字旁。“赫耳墨斯”的“赫”。"),
("墨", "读mò，不读mì。上下结构，土字底。"),
("斯", "读sī，不读shī。左右结构，斤字旁。"),
("宙", "读zhòu，不读zòu。上下结构，宝盖头。“宙斯”的“宙”。"),
("拉", "多音字。①lā：拉扯、赫拉。②lá：拉口子。本课“赫拉”读lā。"),
("庇", "读bì，不读pì。半包围结构，广字头。“庇护”的“庇”。"),
("添", "读tiān，不读tiǎn。左右结构，三点水。“添头”的“添”。"),
("慕", "读mù，不读mò。上下结构，小字底。“爱慕”的“慕”，下面是“”不是“小”。"),
("虚", "读xū，不读xǖ。半包围结构，虎字头。“虚荣”的“虚”。"),
]),
("修辞方法", [
("对比", "寓言最突出的修辞手法。赫耳墨斯的自我定位（“人们对他会更尊重些”）与现实（“算添头，白送”）形成强烈对比；宙斯、赫拉雕像的价格与赫耳墨斯雕像的价格形成对比。对比使讽刺效果更加强烈。"),
("反复", "赫耳墨斯三次发问（“值多少钱？”“值多少钱？”“这个值多少钱？”），雕像者三次回答，构成反复。反复手法使故事层层递进，也为最后的戏剧性转折蓄势。"),
("心理描写", "文中“心想他身为神使，又是商人的庇护神，人们对他会更尊重些”是心理描写，揭示了赫耳墨斯虚荣自负的内心世界，为下文的转折铺垫。"),
("讽刺", "全文贯穿着辛辣的讽刺。作者不直接议论，而是通过人物的言行和对话，让读者在笑声中看清爱慕虚荣者的可笑与可悲。“算添头，白送”是全文最辛辣的讽刺。"),
]),
("写作借鉴", [
("用对话推动情节", "本文主要由对话构成，人物的语言推动着情节的发展。三问三答，层层递进，最后以“白送”二字戛然而止。写叙事类文章时，可以用对话来推动情节、塑造人物，使文章简洁生动。"),
("用心理描写揭示人物", "文中虽只有一处心理描写，却至关重要。它揭示了赫耳墨斯虚荣自负的本质，也为下文的转折做足了铺垫。写人物时，要善于运用心理描写，深入人物内心，揭示其性格特征。"),
("用对比增强讽刺效果", "本文最突出的写法是对比——自我认知与现实评价的对比、不同雕像价格的对比。对比使人物形象更加鲜明，讽刺效果更加强烈。在写作中，可以运用对比手法，突出矛盾，增强表达效果。"),
("卒章显志点明寓意", "寓言的典型结构是先讲故事，最后点明寓意。本文结尾“这个故事适用于那些爱慕虚荣而不被人重视的人”，直接点明故事的教训。写寓言或哲理短文时，可以采用卒章显志的写法，在结尾点明主旨。"),
]),
("文化常识", [
("伊索与《伊索寓言》", "伊索（约公元前6世纪），古希腊寓言家。《伊索寓言》相传为伊索所著，实际是古希腊人集体创作的寓言集，共300余则，大多以动物为主人公，采用拟人化手法，寓意深刻。名篇有《狐狸和葡萄》《农夫和蛇》《龟兔赛跑》等。"),
("寓言的特点", "寓言是文学体裁的一种，以比喻性的故事寄寓意味深长的道理。特点：①篇幅短小，语言精练；②主人公可以是人或拟人化的动植物；③多用夸张、拟人、比喻；④具有哲理性和讽刺性。"),
("古希腊神话体系", "古希腊神话是古希腊人关于神和英雄的故事传说。宙斯是众神之王，赫拉是众神之后，赫耳墨斯是神使和商业庇护神。古希腊神话对西方文学、艺术产生了深远影响。"),
("赫耳墨斯的神职", "赫耳墨斯（Hermes）是古希腊神话中的神使，宙斯与迈亚之子。他是商业、旅行、畜牧、体育的保护神，也是商人的庇护神。他行走如飞，多才多艺。在罗马神话中称为墨丘利（Mercury）。"),
]),
]

DICT_WORDS = [
 {"w":"赫","py":"hè","q":"□耳墨斯想知道他在人间受到多大的尊重","tip":"「赫」赤字旁，读hè；不要写成「郝」（右耳旁）"},
 {"w":"墨","py":"mò","q":"赫耳□斯想知道他在人间受到多大的尊重","tip":"「墨」土字底，读mò；不要写成「默」（黑字旁）"},
 {"w":"斯","py":"sī","q":"赫耳墨□想知道他在人间受到多大的尊重","tip":"「斯」斤字旁，读sī；不要写成「期」（月字旁）"},
 {"w":"尊","py":"zūn","q":"想知道他在人间受到多大的□重","tip":"「尊」寸字底，敬重；不要写成「遵」（走之底，遵守）"},
 {"w":"凡","py":"fán","q":"就化作□人，来到一个雕像者的店里","tip":"「凡」几字旁，平常；不要写成「烦」（火字旁）"},
 {"w":"雕","py":"diāo","q":"来到一个□像者的店里","tip":"「雕」隹字旁，雕刻；不要写成「凋」（两点水，凋零）"},
 {"w":"像","py":"xiàng","q":"来到一个雕□者的店里","tip":"「像」单人旁，比照人物制成的形象；与「象」（大象）区分"},
 {"w":"宙","py":"zhòu","q":"他看见斯□的雕像，问道","tip":"「宙」宝盖头，读zhòu；不要写成「庙」（广字头）"},
 {"w":"银","py":"yín","q":"雕像者说：“一个□元。”","tip":"「银」金字旁，金属元素；不要写成「很」（双人旁）"},
 {"w":"元","py":"yuán","q":"雕像者说：“一个银□。”","tip":"「元」二字头，货币单位；不要写成「无」"},
 {"w":"赫","py":"hè","q":"□拉的雕像值多少钱？","tip":"「赫」赤字旁，读hè；「赫拉」是古希腊神话中的众神之后"},
 {"w":"拉","py":"lā","q":"赫□的雕像值多少钱？","tip":"「拉」提手旁，读lā；不要写成「啦」（口字旁）"},
 {"w":"贵","py":"guì","q":"雕像者说：“还要□一点。”","tip":"「贵」贝字旁，价格高；不要写成「遗」（走之底）"},
 {"w":"使","py":"shǐ","q":"心想他身为神□，又是商人的庇护神","tip":"「使」单人旁，使者；不要写成「史」（口字头）"},
 {"w":"庇","py":"bì","q":"又是商人的□护神","tip":"「庇」广字头，读bì，不读pì；保护"},
 {"w":"护","py":"hù","q":"又是商人的庇□神","tip":"「护」提手旁，保护；不要写成「户」（户字头）"},
 {"w":"添","py":"tiān","q":"这个算□头，白送","tip":"「添」三点水，增加；读tiān，不读tiǎn"},
 {"w":"慕","py":"mù","q":"这个故事适用于那些爱□虚荣而不被人重视的人","tip":"「慕」小字底（下面是「」），读mù；不要写成「幕」（巾字底）"},
 {"w":"虚","py":"xū","q":"这个故事适用于那些爱慕□荣而不被人重视的人","tip":"「虚」虎字头，读xū；不要写成「虑」（心字底，考虑）"},
]

DICT_NOTES = [
 {"w":"赫耳墨斯","a":"古希腊神话中的神使，商业和商人的庇护神","q":"赫耳墨斯想知道他在人间受到多大的尊重"},
 {"w":"尊重","a":"尊敬、敬重","q":"想知道他在人间受到多大的尊重"},
 {"w":"化作","a":"变成","q":"就化作凡人"},
 {"w":"凡人","a":"平常的人、普通人（与神相对）","q":"就化作凡人"},
 {"w":"雕像者","a":"雕刻雕像的工匠","q":"来到一个雕像者的店里"},
 {"w":"宙斯","a":"古希腊神话中的众神之王","q":"他看见宙斯的雕像"},
 {"w":"赫拉","a":"古希腊神话中的众神之后，宙斯的妻子","q":"赫拉的雕像值多少钱"},
 {"w":"神使","a":"神的使者","q":"心想他身为神使"},
 {"w":"庇护神","a":"保护、庇护的神","q":"又是商人的庇护神"},
 {"w":"添头","a":"买东西时商家额外赠送的东西","q":"这个算添头"},
 {"w":"白送","a":"免费赠送、不要钱","q":"这个算添头，白送"},
 {"w":"爱慕虚荣","a":"喜欢表面上的光彩、荣耀","q":"那些爱慕虚荣而不被人重视的人"},
 {"w":"重视","a":"认为重要而认真对待","q":"不被人重视的人"},
]

# ================= 生成 =================
def annotate(text, notes):
    n = len(text)
    occ = [False] * n
    spans = []
    terms = []
    for word, note in notes:
        m = re.match(r"^(.*?)[（(]([^）)]*)[）)]$", word)
        if m:
            w0 = m.group(1)
            py = m.group(2)
            note = "（" + py + "）" + note
        else:
            w0 = word
        terms.append((w0, note))
    for w0, note in sorted(terms, key=lambda x: -len(x[0])):
        if w0 not in text:
            continue
        start = 0
        while True:
            i = text.find(w0, start)
            if i == -1:
                break
            if not any(occ[i:i + len(w0)]):
                spans.append((i, i + len(w0), w0, note))
                for k in range(i, i + len(w0)):
                    occ[k] = True
            start = i + len(w0)
    spans.sort()
    out, pos = [], 0
    for s, e, w, nt in spans:
        out.append(text[pos:s])
        nt_esc = nt.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
        out.append('<span class="anno-word" data-note="%s">%s</span>' % (nt_esc, w))
        pos = e
    out.append(text[pos:])
    return "".join(out)

def esc(t):
    return htmlmod.escape(t, quote=True)

jielu = []
fulltext = []
for (pnum, ptitle, prange, pover, verses) in VERSES:
    jielu.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>'
                 % (esc(pnum), esc(ptitle), esc(prange)))
    jielu.append('      <div class="part-overview">%s</div>' % esc(pover))
    for (no, text, gk, sf, notes) in verses:
        fulltext.append('    <div class="pl">%s</div>' % esc(text))
        jielu.append('      <div class="verse" id="l%d" data-i="%d">' % (no, no - 1))
        jielu.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>'
                     % (no, annotate(text, notes)))
        jielu.append('        <details class="v-more">')
        jielu.append('          <summary>内容 · 手法</summary>')
        jielu.append('          <div class="d-body">')
        jielu.append('            <div class="v-sec"><b class="v-label">内容概括</b>')
        jielu.append('              <div class="v-trans">%s</div>' % esc(gk))
        jielu.append('            </div>')
        jielu.append('            <div class="v-sec"><b class="v-label">手法分析</b>')
        jielu.append('              <div class="d-body"><p>%s</p></div>' % esc(sf))
        jielu.append('            </div>')
        jielu.append('          </div>')
        jielu.append('        </details>')
        jielu.append('      </div>')
    jielu.append('')

jielu = "\n".join(jielu)
fulltext = "\n".join(fulltext)

lead_html = "\n".join('    <p>%s</p>' % esc(p) for p in LEAD)
author_html = "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px;color:var(--ink2)\"" if i else "", esc(p))
                        for i, p in enumerate(AUTHOR))
bg_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' %
    (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:8px\"" if i else "", esc(par))
                           for i, par in enumerate(paras)))
    for (title, paras) in BG)
media_html = "".join(
    '      <div class="media">\n        <h4>%s</h4>\n        <iframe id="%s" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>\n        <a href="%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="%s">全屏播放</button>\n      </div>'
    % (esc(title), fid, bvid, esc(title), url, fid)
    for (title, bvid, url, fid) in VIDEOS)

app_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n    <div class="fame">\n%s\n    </div>\n  </div>\n' %
    (esc(title), "\n".join(
        '      <div class="fame-card">\n        <div class="f-line">%s</div>\n        <p>%s</p>\n      </div>' %
        (esc(ft), esc(pc)) for (ft, pc) in items if title != "主题思想"))
    for (title, items) in APP if title != "主题思想")

theme_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' %
    (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px\"" if i else "", esc(pc))
                           for i, (ft, pc) in enumerate(items)))
    for (title, items) in APP if title == "主题思想")

acc_html = "".join(
    '  <div class="box">\n    <div class="acc-cat">\n      <h3>%s</h3>\n%s\n    </div>\n  </div>\n' %
    (esc(title), "\n".join('      <div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>'
                           % (esc(w), esc(d)) for (w, d) in items))
    for (title, items) in ACC)

hero = '<header class="hero">\n  <div class="hero-side">%s</div>\n  <h1 class="hero-title">%s</h1>\n</header>' % (H, TITLE)

nav = """<nav class="nav">
  <div class="nav-in">
    <a href="#bg">背景</a>
    <a href="#jielu">解读</a>
    <a href="#app">赏析</a>
    <a href="#acc">积累</a>
    <a href="#practice">练习</a>
    <div class="tool">
      <select id="fsSel" class="fs-sel" title="正文字体大小">
        <option value="100">100%</option>
        <option value="150">150%</option>
        <option value="200">200%</option>
        <option value="250">250%</option>
        <option value="300">300%</option>
      </select>
      <button id="btnAll">展开</button>
      <button id="btnRecite">背诵</button>
      <button id="btnPrint">打印</button>
    </div>
  </div>
</nav>"""

main = """<main class="wrap">
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
%s
  </div>
  <div class="box">
    <h3>作者简介</h3>
%s
  </div>
%s  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
%s
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 词语 · 手法</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
%s
  </div>
  <div class="verse-list" id="verseList">
%s
  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">人物 · 艺术 · 名句</span></div>
%s
%s</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 字音 · 修辞 · 写法 · 文化</span></div>
%s</section>

<div class="divider"></div>
<section id="practice" class="sec">
    <div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>
    <div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>
    <div class="ptools">
      <button data-mode="word" data-rand="5">随机五组字形</button>
      <button data-mode="word" data-all="1">全部字形</button>
      <button data-mode="note" data-rand="5">随机五组词语</button>
      <button data-mode="note" data-all="1">全部词语</button>
    </div>
  </section>

<footer>
  <div class="kai">《赫耳墨斯和雕像者》</div>
  <div>伊索 · 古希腊 · 选自《伊索寓言》</div>
</footer>
</main>""" % (lead_html, author_html, bg_html, media_html, fulltext, jielu, app_html, theme_html, acc_html)

tail = """<button class="top-btn" id="topBtn" title="回到顶部">↑</button>
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
</div>"""

dict_js = ("var DICT_WORDS = %s;\nvar DICT_NOTES = %s;\n"
           % (json.dumps(DICT_WORDS, ensure_ascii=False),
              json.dumps(DICT_NOTES, ensure_ascii=False)))

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《赫耳墨斯和雕像者》伊索寓言</title>
<style>%s</style>
</head>
<body data-fs="100">

%s

%s

%s

%s

<script>
%s
</script>
<script>
%s</script>

</body>
</html>""" % (css, hero, nav, main, tail, main_js, dict_js)

open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, len(html), "chars")
print("verses:", sum(len(v[4]) for v in VERSES))
print("word dict:", len(DICT_WORDS), "note dict:", len(DICT_NOTES))
