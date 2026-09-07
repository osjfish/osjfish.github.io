# -*- coding: utf-8 -*-
import json, re, html, io, os
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(TOOLS_DIR, '..', 'beiying-zhuziqing.html'))
OUT = os.path.normpath(os.path.join(TOOLS_DIR, '..', 'jiuyingfalianjunyuanzhengzhongguozhibateleishangweidexin-yuguo.html'))
src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>')+7:src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0+8:src.index('</script>',s0)].replace('beiying_fs','jiuying_fs')
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;border-left:3px solid #b8934a;padding-left:8px;margin:12px 0 6px;color:#8a6d2b;}'

FULLTEXT = [
"\u201c先生：您征求我对远征中国的意见。您认为这次远征是体面的，出色的。多谢您对我的想法予以重视。在您看来，打着维多利亚女王和拿破仑皇帝双重旗号对中国的远征，是由法国和英国共同分享的光荣，而您想知道，我对英法的这个胜利会给予多少赞誉。\u201d",
"\u201c既然您想了解我的看法，那就请往下读吧：\u201d",
"\u201c在世界的某个角落，有一个世界奇迹。这个奇迹叫圆明园。艺术有两个来源，一是理想，理想产生欧洲艺术；一是幻想，幻想产生东方艺术。圆明园在幻想艺术中的地位就如同巴特农神庙在理想艺术中的地位。一个几乎是超人的民族的想象力所能产生的成就尽在于此。和巴特农神庙不一样，这不是一件稀有的、独一无二的作品；这是幻想的某种规模巨大的典范，如果幻想能有一个典范的话。请您想象有一座言语无法形容的建筑，某种恍若月宫的建筑，这就是圆明园。请您用大理石，用玉石，用青铜，用瓷器建造一个梦，用雪松做它的屋架，给它上上下下缀满宝石，披上绸缎，这儿盖神殿，那儿建后宫，造城楼，里面放上神像，放上异兽，饰以琉璃，饰以珐琅，饰以黄金，施以脂粉，请同是诗人的建筑师建造一千零一夜的一千零一个梦，再添上一座座花园，一方方水池，一眼眼喷泉，加上成群的天鹅、朱鹭和孔雀，总而言之，请假设人类幻想的某种令人眼花缭乱的洞府，其外貌是神庙，是宫殿，那就是这座名园。为了创建圆明园，曾经耗费了两代人的长期劳动。这座大得犹如一座城市的建筑物是世世代代的结晶，为谁而建？为了各国人民。因为，岁月创造的一切都是属于人类的。过去的艺术家、诗人、哲学家都知道圆明园，伏尔泰就谈起过圆明园。人们常说：希腊有巴特农神庙，埃及有金字塔，罗马有斗兽场，巴黎有圣母院，而东方有圆明园。要是说，大家没有看见过它，但大家梦见过它。这是某种令人惊骇而不知名的杰作，在不可名状的晨曦中依稀可见，宛如在欧洲文明的地平线上瞥见的亚洲文明的剪影。\u201d",
"\u201c这个奇迹已经消失了。\u201d",
"\u201c有一天，两个来自欧洲的强盗闯进了圆明园。一个强盗洗劫财物，另一个强盗在放火。似乎得胜之后，便可以动手行窃了。他们对圆明园进行了大规模的劫掠，赃物由两个胜利者均分。我们看到，这整个事件还与额尔金的名字有关，这名字又使人不能不忆起巴特农神庙。从前他们对巴特农神庙怎么干，现在对圆明园也怎么干，不同的只是干得更彻底，更漂亮，以至于荡然无存。我们把欧洲所有大教堂的财宝加在一起，也许还抵不上东方这座了不起的富丽堂皇的博物馆。那儿不仅仅有艺术珍品，还有大堆的金银制品。丰功伟绩！收获巨大！两个胜利者，一个塞满了腰包，这是看得见的，另一个装满了箱箧。他们手挽手，笑嘻嘻地回到欧洲。这就是这两个强盗的故事。\u201d",
"\u201c我们欧洲人是文明人，中国人在我们眼中是野蛮人。这就是文明对野蛮所干的事情。\u201d",
"\u201c将受到历史制裁的这两个强盗，一个叫法兰西，另一个叫英吉利。不过，我要抗议，感谢您给了我这样一个抗议的机会。治人者的罪行不是治于人者的过错；政府有时会是强盗，而人民永远也不会是强盗。\u201d",
"\u201c法兰西帝国吞下了这次胜利的一半赃物，今天，帝国居然还天真地以为自己就是真正的物主，把圆明园富丽堂皇的破烂拿来展出。我希望有朝一日，解放了的干干净净的法兰西会把这份战利品归还给被掠夺的中国，那才是真正的物主。\u201d",
"\u201c现在，我证实，发生了一次偷窃，有两名窃贼。\u201d",
"\u201c先生，以上就是我对远征中国的全部赞誉。\u201d",
"维克多·雨果","1861年11月25日于高城居",
]

PARTS = [
("第一部分","致信缘由 · 欲抑先扬","第 1–2 段","巴特勒上尉征求雨果对远征中国的意见，企图借文豪之声名为侵略捧场。雨果以\u201c体面\u201d\u201c出色\u201d\u201c光荣\u201d\u201c赞誉\u201d等词假意承接，埋下反语伏笔，引出下文。"),
("第二部分","盛赞圆明园 · 东方奇迹","第 3 段","全文最长的段落。雨果以瑰丽的想象和铺陈的笔法，盛赞圆明园是\u201c世界奇迹\u201d，是幻想艺术的典范，是亚洲文明的剪影。越是赞美，后文被焚毁越令人痛心。"),
("第三部分","奇迹消失 · 强盗行径","第 4–5 段","以\u201c这个奇迹已经消失了\u201d独立成段，骤转直下。揭露英法联军劫掠、纵火、分赃的强盗行径，以\u201c丰功伟绩\u201d\u201c收获巨大\u201d等反语辛辣讽刺。"),
("第四部分","文明野蛮 · 抗议谴责","第 6–8 段","以\u201c文明对野蛮\u201d的颠倒对比，戳破欧洲中心论的虚伪。明确指出两个强盗是法兰西和英吉利，区分政府与人民，抗议侵略罪行，期盼赃物归还。"),
("第五部分","证实偷窃 · 首尾呼应","第 9–10 段","以\u201c发生了一次偷窃，有两名窃贼\u201d作结，斩钉截铁。\u201c全部赞誉\u201d与开篇\u201c多少赞誉\u201d呼应，反语贯穿始终，余味辛辣。"),
]

S = [
(0,"先生：您[[征求|寻求、请求（对方意见）]]我对远征中国的意见。您认为这次远征是[[体面|光荣、光彩（反语，实际指侵略的可耻）]]的，出色的。多谢您对我的想法予以重视。","巴特勒上尉致信雨果，征求其对远征中国的意见，认为这次远征\u201c体面\u201d\u201c出色\u201d。","开篇交代致信缘由。\u201c体面\u201d\u201c出色\u201d是巴特勒的看法，也是雨果后文反语讽刺的靶子，欲抑先扬。"),
(0,"在您看来，打着维多利亚女王和拿破仑皇帝[[双重旗号|两面旗帜，指英法两国共同出兵]]对中国的远征，是由法国和英国共同分享的光荣，而您想知道，我对英法的这个胜利会给予多少[[赞誉|称赞、赞美（反语）]]。","巴特勒认为英法联军打着两国君主旗号远征中国是\u201c光荣\u201d，想知道雨果会给予多少\u201c赞誉\u201d。","\u201c光荣\u201d\u201c赞誉\u201d再次铺垫反语。\u201c多少赞誉\u201d设下悬念，与结尾\u201c全部赞誉\u201d首尾呼应。"),
(0,"既然您想了解我的看法，那就请往下读吧：","过渡句，引出下文雨果的真实看法。","独立成段，语气平和却暗含锋芒——\u201c往下读\u201d三字，暗示下文将与巴特勒的期待截然不同。"),
(1,"在世界的某个角落，有一个世界奇迹。这个奇迹叫圆明园。","总起：称圆明园为\u201c世界奇迹\u201d，给予最高评价。","开门见山，\u201c世界奇迹\u201d四字总领全段。\u201c某个角落\u201d写其位置，却以\u201c世界\u201d限定\u201c奇迹\u201d，见出圆明园在人类文明中的地位。"),
(1,"艺术有两个来源，一是理想，理想产生欧洲艺术；一是幻想，幻想产生东方艺术。","提出艺术分类：欧洲艺术源于理想，东方艺术源于幻想。","分类论证。以\u201c理想\u201d与\u201c幻想\u201d对举，为下文将圆明园定位为\u201c幻想艺术的典范\u201d做理论铺垫。"),
(1,"圆明园在幻想艺术中的地位就如同巴特农神庙在理想艺术中的地位。","以巴特农神庙类比，指出圆明园在东方幻想艺术中的崇高地位。","类比论证。巴特农神庙是欧洲理想艺术的巅峰，以之类比圆明园，等量齐观，见出雨果对东方艺术的尊重。"),
(1,"一个几乎是超人的民族的想象力所能产生的成就尽在于此。","盛赞圆明园是中华民族想象力的最高成就。","\u201c超人的民族\u201d是对中华民族的高度赞美。\u201c尽在于此\u201d强调圆明园集中体现了东方想象力的最高成就。"),
(1,"和巴特农神庙不一样，这不是一件稀有的、独一无二的作品；这是幻想的某种规模巨大的典范，如果幻想能有一个典范的话。","辨析圆明园与巴特农神庙的不同：前者是规模巨大的幻想典范，而非单件稀有作品。","对比论证。先辨异，再以\u201c如果幻想能有一个典范的话\u201d这一假设句式，极写圆明园作为幻想艺术典范的独一无二，语气委婉而评价极高。"),
(1,"请您想象有一座言语无法形容的建筑，某种[[恍若月宫|仿佛像月中宫殿一样。恍若，仿佛、好像]]的建筑，这就是圆明园。","请巴特勒想象圆明园——一座言语无法形容、恍若月宫的建筑。","\u201c言语无法形容\u201d\u201c恍若月宫\u201d，以不可形容之词形容，极写圆明园之美。用\u201c请您想象\u201d的对话语气，将读者带入情境。"),
(1,"请您用大理石，用玉石，用青铜，用瓷器建造一个梦，用雪松做它的屋架，给它上上下下[[缀满|装饰得满满的。缀，用针线等连缀，这里指装饰]]宝石，披上绸缎，","铺陈圆明园的建筑材料：大理石、玉石、青铜、瓷器、雪松、宝石、绸缎，琳琅满目。","排比铺陈。一连串\u201c用……\u201d句式，列举珍贵材料，营造富丽堂皇之感。\u201c建造一个梦\u201d，将圆明园比作梦，见其虚幻之美。"),
(1,"这儿盖神殿，那儿建后宫，造城楼，里面放上神像，放上异兽，饰以[[琉璃|一种用铝和钠的硅酸化合物烧制成的釉料，多用于建筑装饰]]，饰以[[珐琅|（fà láng）用石英、长石等烧制成的釉质涂料，涂在金属胎上]]，饰以黄金，施以[[脂粉|胭脂粉，这里指彩饰、妆饰]]，","铺陈圆明园的建筑布局与装饰：神殿、后宫、城楼、神像、异兽，琉璃、珐琅、黄金、脂粉。","继续排比铺陈，由建筑到陈设再到装饰，由外到内，层次分明。\u201c饰以……饰以……饰以……施以……\u201d句式整齐，气势充沛。"),
(1,"请同是诗人的建筑师建造一千零一夜的一千零一个梦，再添上一座座花园，一方方水池，一眼眼喷泉，加上成群的天鹅、[[朱鹭|（zhū lù）一种红色的鹭鸟，羽毛美丽]]和孔雀，","以\u201c一千零一夜的一千零一个梦\u201d喻圆明园的奇幻，再添花园、水池、喷泉与珍禽。","比喻与排比结合。\u201c一千零一夜\u201d是阿拉伯民间故事集，以奇幻著称；\u201c一座座……一方方……一眼眼……\u201d叠词排比，写园中景物之丰富。"),
(1,"总而言之，请假设人类幻想的某种令人[[眼花缭乱|眼睛看见复杂纷繁的东西而感到迷乱。缭，缠绕]]的[[洞府|神话传说中神仙居住的地方，这里指宫殿园林]]，其外貌是神庙，是宫殿，那就是这座名园。","总结：圆明园是人类幻想的令人眼花缭乱的洞府，外貌如神庙如宫殿。","\u201c总而言之\u201d收束铺陈。\u201c洞府\u201d与前文\u201c月宫\u201d\u201c梦\u201d呼应，将圆明园定位为超越现实的幻想杰作。"),
(1,"为了创建圆明园，曾经耗费了两代人的长期劳动。这座大得犹如一座城市的建筑物是世世代代的结晶，为谁而建？为了各国人民。","指出圆明园耗费两代人长期劳动，是世世代代的结晶，属于各国人民。","\u201c为谁而建？为了各国人民\u201d，设问自答，点明圆明园是全人类的文化财富，为后文谴责侵略者掠夺人类文明成果铺垫。"),
(1,"因为，岁月创造的一切都是属于人类的。","升华：岁月创造的一切都属于全人类。","独句成段式的论断，铿锵有力。这是雨果的人类主义立场——文明成果属于全人类，侵略者掠夺的是全人类的财富。"),
(1,"过去的艺术家、诗人、哲学家都知道圆明园，[[伏尔泰|（1694—1778）法国启蒙思想家、文学家，曾在作品中赞美中国]]就谈起过圆明园。","以伏尔泰为例，说明圆明园在欧洲知识界早有盛名。","举例论证。伏尔泰是法国启蒙运动的泰斗，以他谈起过圆明园为例，增强说服力，也见出圆明园的国际声誉。"),
(1,"人们常说：希腊有巴特农神庙，埃及有金字塔，罗马有[[斗兽场|古罗马时期用于角斗士表演和公众娱乐的圆形竞技场]]，巴黎有圣母院，而东方有圆明园。","排比列举世界文明奇迹，将圆明园与巴特农神庙、金字塔、斗兽场、圣母院并列。","排比论证。四大西方文明奇迹与东方圆明园对举，以\u201c而\u201d字一转，突出圆明园在世界文明中的地位，等量齐观。"),
(1,"要是说，大家没有看见过它，但大家梦见过它。","即使没亲眼见过圆明园，人们也在梦中见过它。","\u201c梦见过它\u201d与前文\u201c幻想\u201d\u201c梦\u201d呼应，写圆明园之美已成为人类共同的文化想象，超越了亲眼所见。"),
(1,"这是某种令人[[惊骇|惊慌害怕。骇，惊吓、震惊]]而不知名的杰作，在[[不可名状|不能用语言形容。名，说出。状，形容]]的晨曦中依稀可见，宛如在欧洲文明的地平线上瞥见的亚洲文明的剪影。","总结圆明园是令人惊骇的杰作，如亚洲文明在欧洲文明地平线上的剪影。","比喻收束全段。\u201c剪影\u201d一词，将圆明园比作亚洲文明的轮廓，简洁而意蕴深远。\u201c不可名状\u201d与前文\u201c言语无法形容\u201d呼应。"),
(2,"这个奇迹已经消失了。","独立成段：圆明园这个世界奇迹已经消失了。","独句成段，斩钉截铁。与前文长篇盛赞形成巨大落差，情感骤转，为下文揭露强盗行径蓄势。\u201c已经\u201d二字，含无尽痛惜。"),
(2,"有一天，两个来自欧洲的强盗闯进了圆明园。一个强盗洗劫财物，另一个强盗在放火。","两个欧洲强盗闯进圆明园：一个劫掠，一个纵火。","\u201c强盗\u201d直接定性，与前文\u201c文明人\u201d形成尖锐对比。\u201c闯进\u201d写其野蛮，\u201c洗劫\u201d\u201c放火\u201d两个动作概括侵略罪行。"),
(2,"似乎得胜之后，便可以动手行窃了。他们对圆明园进行了大规模的[[劫掠|抢劫、掠夺。掠，夺取]]，赃物由两个胜利者均分。","侵略者以胜利者自居，大规模劫掠圆明园，赃物由英法均分。","\u201c似乎\u201d一词暗含否定——得胜之后便可以行窃，这是什么逻辑？\u201c胜利者\u201d是反语，实为强盗。\u201c均分\u201d写分赃的无耻。"),
(2,"我们看到，这整个事件还与[[额尔金|（1811—1863）英国外交官，1860年下令焚毁圆明园的英国全权代表]]的名字有关，这名字又使人不能不忆起巴特农神庙。","事件与额尔金有关，而额尔金的名字使人忆起巴特农神庙也曾遭其家族劫掠。","\u201c不能不忆起\u201d双重否定，强调联想之必然。额尔金的父亲曾劫掠巴特农神庙雕塑，父子两代皆为文化强盗，此处暗扣，见出侵略的惯犯本质。"),
(2,"从前他们对巴特农神庙怎么干，现在对圆明园也怎么干，不同的只是干得更彻底，更漂亮，以至于[[荡然无存|形容原有的东西完全失去，一点没有留下。荡然，空荡荡的样子]]。","英法对圆明园如法炮制巴特农神庙的劫掠，且更彻底更漂亮，以至圆明园荡然无存。","类比论证。\u201c更彻底，更漂亮\u201d是反语——\u201c漂亮\u201d实为破坏得更彻底。\u201c以至于荡然无存\u201d写毁灭之彻底，令人痛心。"),
(2,"我们把欧洲所有大教堂的财宝加在一起，也许还抵不上东方这座了不起的[[富丽堂皇|形容建筑物宏伟华丽。富丽，华丽。堂皇，气势盛大]]的博物馆。","欧洲所有大教堂的财宝加在一起，也抵不上圆明园这座博物馆。","对比论证。以欧洲所有大教堂的财宝与圆明园对比，极写圆明园价值之高、收藏之丰，为下文\u201c不仅仅有艺术珍品\u201d铺垫。"),
(2,"那儿不仅仅有艺术珍品，还有大堆的金银制品。","圆明园中不仅有艺术珍品，还有大量金银制品。","\u201c不仅仅……还有……\u201d递进句式，写圆明园收藏之丰富，也暗示侵略者劫掠的贪婪——不仅抢艺术品，还抢金银。"),
(2,"丰功伟绩！收获巨大！","反语：所谓\u201c丰功伟绩\u201d\u201c收获巨大\u201d。","独立成句的反语，感叹号加强语气。\u201c丰功伟绩\u201d本指伟大的功绩，这里指劫掠破坏的罪行；\u201c收获巨大\u201d本指收获丰富，这里指掠夺的赃物之多。反语辛辣，讽刺力极强。"),
(2,"两个胜利者，一个塞满了腰包，这是看得见的，另一个装满了[[箱箧|（xiāng qiè）箱子。箧，小箱子]]。","两个\u201c胜利者\u201d：一个塞满腰包，一个装满箱箧。","\u201c胜利者\u201d再次反语。\u201c塞满\u201d\u201c装满\u201d写贪婪，\u201c腰包\u201d\u201c箱箧\u201d写分赃的具体形态，如在目前。"),
(2,"他们手挽手，笑嘻嘻地回到欧洲。这就是这两个强盗的故事。","两个强盗手挽手、笑嘻嘻地回到欧洲——这就是他们的故事。","\u201c手挽手\u201d\u201c笑嘻嘻\u201d，神态描写，写侵略者分赃后的得意与无耻，如漫画般传神。\u201c这就是这两个强盗的故事\u201d收束全段，\u201c强盗\u201d再次定性，与开头呼应。"),
(3,"我们欧洲人是文明人，中国人在我们眼中是野蛮人。这就是文明对野蛮所干的事情。","欧洲人自视为文明人，视中国人为野蛮人——而这就是\u201c文明\u201d对\u201c野蛮\u201d所干的事。","\u201c文明\u201d\u201c野蛮\u201d全是反语。以欧洲人的视角自述，再以\u201c这就是文明对野蛮所干的事情\u201d反戈一击，戳破欧洲中心论的虚伪：真正野蛮的是侵略者。"),
(3,"将受到历史制裁的这两个强盗，一个叫法兰西，另一个叫英吉利。","明确指出：将受历史制裁的两个强盗，一个是法兰西，一个是英吉利。","\u201c一个叫法兰西，另一个叫英吉利\u201d，直呼国名，毫不留情。\u201c历史制裁\u201d，断言侵略者终将被历史审判，表现出雨果的远见与勇气。"),
(3,"不过，我要抗议，感谢您给了我这样一个抗议的机会。","雨果表示要抗议，并感谢巴特勒给了他抗议的机会。","\u201c不过\u201d一转，由谴责转入正面抗议。\u201c感谢\u201d是反语——巴特勒本想让雨果捧场，却给了他公开谴责的机会，适得其反。"),
(3,"[[治人者|统治别人的人，指统治者、政府]]的罪行不是[[治于人者|被别人统治的人，指人民、百姓]]的过错；政府有时会是强盗，而人民永远也不会是强盗。","区分政府与人民：统治者的罪行不是人民的过错，政府可能是强盗，但人民永远不是。","\u201c治人者\u201d\u201c治于人者\u201d化用孟子\u201c劳心者治人，劳力者治于人\u201d，文言色彩的对举，凝练有力。这一区分体现了雨果的人道主义立场——他谴责的是法国政府，而非法国人民。"),
(3,"法兰西帝国吞下了这次胜利的一半赃物，今天，帝国居然还天真地以为自己就是真正的物主，把圆明园富丽堂皇的破烂拿来展出。","法兰西帝国吞下一半赃物，还天真地以物主自居，把抢来的\u201c破烂\u201d展出。","\u201c吞下\u201d写贪婪，\u201c居然\u201d写荒谬，\u201c天真\u201d是反语（实为无耻）。\u201c富丽堂皇的破烂\u201d，矛盾修饰——在侵略者手中，艺术珍品成了\u201c破烂\u201d，见出对侵略者的蔑视。"),
(3,"我希望有朝一日，解放了的干干净净的法兰西会把这份战利品归还给被掠夺的中国，那才是真正的物主。","雨果希望未来解放了的法兰西将赃物归还给中国——中国才是真正的物主。","\u201c干干净净的法兰西\u201d，与\u201c吞下赃物\u201d的法兰西对比，寄托了雨果对祖国未来的期望。\u201c那才是真正的物主\u201d，明确中国的所有权，正义凛然。"),
(4,"现在，我证实，发生了一次偷窃，有两名窃贼。","雨果证实：发生了一次偷窃，有两名窃贼。","\u201c证实\u201d，如法庭宣判，斩钉截铁。\u201c偷窃\u201d\u201c窃贼\u201d，法律术语定性，比\u201c强盗\u201d更冷峻。独句成段，掷地有声。"),
(4,"先生，以上就是我对远征中国的全部赞誉。","收尾：以上就是雨果对远征中国的\u201c全部赞誉\u201d。","\u201c全部赞誉\u201d与开篇\u201c多少赞誉\u201d首尾呼应。\u201c赞誉\u201d是贯穿全文的反语——所谓\u201c赞誉\u201d，实为最严厉的谴责。以\u201c先生\u201d称呼巴特勒，礼貌中含冰冷的蔑视，余味辛辣。"),
]

DICT_WORDS = [
{"w":"誉","py":"yù","q":"我对英法的这个胜利会给予多少赞□","tip":"「誉」言字旁，称赞；不要写成「誊」（téng，抄写）"},
{"w":"勒","py":"lè","q":"打着维多利亚女王和拿破□皇帝双重旗号","tip":"「勒」革字旁，雕刻、强制；不要写成「勤」"},
{"w":"恍","py":"huǎng","q":"某种□若月宫的建筑","tip":"「恍」竖心旁，仿佛；不要写成「晃」（日字旁，摇晃）"},
{"w":"缀","py":"zhuì","q":"给它上上下下□满宝石","tip":"「缀」绞丝旁，装饰、连结；不要写成「辍」（chuò，停止）"},
{"w":"珐","py":"fà","q":"饰以琉璃，饰以□琅","tip":"「珐」王字旁，珐琅；不要写成「法」（三点水）"},
{"w":"琅","py":"láng","q":"饰以琉璃，饰以珐□","tip":"「琅」王字旁，珐琅；不要写成「郎」（耳字旁）"},
{"w":"脂","py":"zhī","q":"饰以黄金，施以□粉","tip":"「脂」月字旁，油脂；不要写成「指」（提手旁）"},
{"w":"鹭","py":"lù","q":"加上成群的天鹅、朱□和孔雀","tip":"「鹭」鸟字底，鹭鸟；上面是「路」，不要少写"},
{"w":"缭","py":"liáo","q":"令人眼花□乱的洞府","tip":"「缭」绞丝旁，缠绕；不要写成「嘹」（口字旁，嘹亮）"},
{"w":"骇","py":"hài","q":"这是某种令人惊□而不知名的杰作","tip":"「骇」马字旁，惊吓；不要写成「该」（言字旁）"},
{"w":"曦","py":"xī","q":"在不可名状的晨□中依稀可见","tip":"「曦」日字旁，阳光；笔画多，右边是「羲」，不要漏写"},
{"w":"瞥","py":"piē","q":"宛如在欧洲文明的地平线上□见的亚洲文明的剪影","tip":"「瞥」目字底，短时间地大略看看；不要写成「憋」（心字底）"},
{"w":"劫","py":"jié","q":"他们对圆明园进行了大规模的掠□","tip":"「劫」力字旁，强取、灾难；不要写成「却」（卩字旁）"},
{"w":"掠","py":"lüè","q":"他们对圆明园进行了大规模的□劫","tip":"「掠」提手旁，夺取；不要写成「惊」（竖心旁）"},
{"w":"赃","py":"zāng","q":"□物由两个胜利者均分","tip":"「赃」贝字旁，贪污受贿或盗窃所得的财物；与「脏」（月字旁，不干净）区分"},
{"w":"箧","py":"qiè","q":"另一个装满了箱□","tip":"「箧」竹字头，小箱子；不要写成「惬」（竖心旁，惬意）"},
{"w":"制裁","py":"zhì cái","q":"将受到历史□□的这两个强盗","tip":"「裁」衣字旁，判定；不要写成「栽」（木字旁，栽种）"},
]

DICT_NOTES = [
{"w":"征求","a":"寻求、请求（对方意见）","q":"您征求我对远征中国的意见"},
{"w":"体面","a":"光荣、光彩（文中是反语，实际指侵略的可耻）","q":"您认为这次远征是体面的"},
{"w":"赞誉","a":"称赞、赞美（文中是反语）","q":"我对英法的这个胜利会给予多少赞誉"},
{"w":"双重旗号","a":"两面旗帜，指英法两国共同出兵","q":"打着维多利亚女王和拿破仑皇帝双重旗号"},
{"w":"恍若月宫","a":"仿佛像月中宫殿一样。恍若，仿佛、好像","q":"某种恍若月宫的建筑"},
{"w":"缀满","a":"装饰得满满的。缀，装饰","q":"给它上上下下缀满宝石"},
{"w":"琉璃","a":"一种用铝和钠的硅酸化合物烧制成的釉料，多用于建筑装饰","q":"饰以琉璃"},
{"w":"珐琅","a":"（fà láng）用石英、长石等烧制成的釉质涂料，涂在金属胎上","q":"饰以珐琅"},
{"w":"脂粉","a":"胭脂粉，文中指彩饰、妆饰","q":"施以脂粉"},
{"w":"朱鹭","a":"（zhū lù）一种红色的鹭鸟，羽毛美丽","q":"加上成群的天鹅、朱鹭和孔雀"},
{"w":"眼花缭乱","a":"眼睛看见复杂纷繁的东西而感到迷乱。缭，缠绕","q":"令人眼花缭乱的洞府"},
{"w":"洞府","a":"神话传说中神仙居住的地方，文中指宫殿园林","q":"令人眼花缭乱的洞府"},
{"w":"伏尔泰","a":"（1694—1778）法国启蒙思想家、文学家，曾在作品中赞美中国","q":"伏尔泰就谈起过圆明园"},
{"w":"斗兽场","a":"古罗马时期用于角斗士表演和公众娱乐的圆形竞技场","q":"罗马有斗兽场"},
{"w":"惊骇","a":"惊慌害怕。骇，惊吓、震惊","q":"令人惊骇而不知名的杰作"},
{"w":"不可名状","a":"不能用语言形容。名，说出。状，形容","q":"在不可名状的晨曦中依稀可见"},
{"w":"劫掠","a":"抢劫、掠夺。掠，夺取","q":"他们对圆明园进行了大规模的劫掠"},
{"w":"额尔金","a":"（1811—1863）英国外交官，1860年下令焚毁圆明园的英国全权代表","q":"这整个事件还与额尔金的名字有关"},
{"w":"荡然无存","a":"形容原有的东西完全失去，一点没有留下。荡然，空荡荡的样子","q":"以至于荡然无存"},
{"w":"富丽堂皇","a":"形容建筑物宏伟华丽。富丽，华丽。堂皇，气势盛大","q":"东方这座了不起的富丽堂皇的博物馆"},
{"w":"箱箧","a":"（xiāng qiè）箱子。箧，小箱子","q":"另一个装满了箱箧"},
{"w":"治人者","a":"统治别人的人，指统治者、政府","q":"治人者的罪行不是治于人者的过错"},
{"w":"治于人者","a":"被别人统治的人，指人民、百姓","q":"治人者的罪行不是治于人者的过错"},
{"w":"丰功伟绩","a":"伟大的功绩（文中是反语，指劫掠破坏的罪行）","q":"丰功伟绩！收获巨大！"},
{"w":"制裁","a":"用强力管束并惩处","q":"将受到历史制裁的这两个强盗"},
{"w":"窃贼","a":"偷东西的人","q":"发生了一次偷窃，有两名窃贼"},
]

def annotate(text):
    def rep(m):
        w,n = m.group(1),m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n,quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)

verses = []
idx = 0
for pi,part in enumerate(PARTS):
    verses.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>' % (part[0],part[1],part[2]))
    verses.append('      <div class="part-overview">%s</div>' % part[3])
    for (p,txt,gai,shou) in S:
        if p != pi: continue
        idx += 1
        verses.append('      <div class="verse" id="l%d" data-i="%d">' % (idx,idx-1))
        verses.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx,annotate(txt)))
        verses.append('        <details class="v-more"><summary>内容 · 手法</summary>')
        verses.append('          <div class="d-body">')
        verses.append('            <div class="v-sec"><b class="v-label">内容概括</b><div class="v-trans">%s</div></div>' % gai)
        verses.append('            <div class="v-sec"><b class="v-label">手法分析</b><div class="d-body"><p>%s</p></div></div>' % shou)
        verses.append('          </div></details></div>')
verses_html = '\n'.join(verses)
full_html = '\n'.join('    <div class="pl">%s</div>' % p for p in FULLTEXT)

# Load HTML template parts from beiying
# We'll construct the HTML directly
BG_HTML = '''<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>1860年，英法联军发动第二次鸦片战争，攻入北京，劫掠并焚毁了被誉为\u201c万园之园\u201d的圆明园。事后，法国上尉巴特勒致信雨果，企图借文豪之声名为侵略\u201c捧场\u201d。雨果没有狭隘的民族主义情绪，反而以人类良知的立场，写下这封义正辞严的信，强烈谴责英法联军的强盗行径。</p>
    <p>文章以书信形式展开，先以\u201c体面\u201d\u201c赞誉\u201d等反语假意承接，再以瑰丽的笔墨盛赞圆明园的艺术价值，最后以\u201c强盗\u201d\u201c窃贼\u201d等词无情揭露侵略者的罪行。反语贯穿始终，对比鲜明，气势充沛，是一篇充满人道主义精神的战斗檄文。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>维克多·雨果（1802—1885），法国19世纪伟大的浪漫主义文学家，法国文学史上卓越的资产阶级民主作家，被称为\u201c法兰西的莎士比亚\u201d。其作品包括诗歌、小说、剧本、散文和文艺评论，在法国乃至世界文学史上有广泛影响。代表作有长篇小说《巴黎圣母院》《悲惨世界》《九三年》，诗集《惩罚集》《静观集》等。</p>
    <p style="margin-top:10px;color:var(--ink2)">雨果一生反对专制、追求正义，具有强烈的人道主义精神。1851年路易·波拿巴发动政变后，雨果因反对帝制被迫流亡国外长达19年。这封信写于1861年11月25日，正是他流亡期间。面对本国政府的侵略罪行，他没有站在狭隘的民族立场上，而是以人类良知的名义公开谴责，表现出非凡的勇气与正直。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>第二次鸦片战争：</b>1856年至1860年，英法联合发动侵华战争。1860年10月，英法联军攻入北京，对圆明园进行了大规模的劫掠，随后纵火焚烧，使这座\u201c万园之园\u201d化为一片废墟。</p>
    <p style="margin-top:8px"><b>巴特勒的来信：</b>法军上尉巴特勒参与了远征中国，他致信雨果，认为这次远征是\u201c体面的\u201d\u201c出色的\u201d，想借雨果的显赫声名为侵略\u201c捧场\u201d，询问雨果会给予\u201c多少赞誉\u201d。</p>
    <p style="margin-top:8px"><b>雨果的回应：</b>雨果没有被狭隘的民族主义蒙蔽，也没有被\u201c爱国狂热\u201d裹挟。他以人类文明的立场，公开谴责本国政府的侵略罪行，为被掠夺的中国鸣不平。这封信最初发表于1862年雨果的诗集《惩罚集》中。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>诵读《就英法联军远征中国致巴特勒上尉的信》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV17F411V74Z&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="诵读雨果《就英法联军远征中国致巴特勒上尉的信》"></iframe>
        <a href="https://www.bilibili.com/video/BV17F411V74Z" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>英法联军入侵北京，火烧圆明园</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV13e4y1B7ti&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="英法联军入侵北京火烧圆明园"></iframe>
        <a href="https://www.bilibili.com/video/BV13e4y1B7ti" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>'''

APP_HTML = '''<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">论证 · 语言 · 名句</span></div>
  <div class="box">
    <h3>论证思路</h3>
    <p style="margin-bottom:14px;color:var(--ink2)">本文是一篇以书信形式写成的驳论文，论证思路清晰，层层递进。</p>
    <div class="fame">
      <div class="fame-card"><div class="f-line">引出话题 · 欲抑先扬（第1–2段）</div><p>开篇交代致信缘由，复述巴特勒的观点——远征中国是\u201c体面的\u201d\u201c出色的\u201d\u201c光荣\u201d，想知道雨果会给予\u201c多少赞誉\u201d。雨果不急于反驳，而是以\u201c既然您想了解我的看法，那就请往下读吧\u201d从容引出下文。\u201c体面\u201d\u201c赞誉\u201d等词已暗藏反语锋芒，为全文的讽刺基调定调。</p></div>
      <div class="fame-card"><div class="f-line">盛赞奇迹 · 铺陈蓄势（第3段）</div><p>全文最长的段落，雨果以瑰丽的想象和铺陈的笔法，盛赞圆明园是\u201c世界奇迹\u201d。先以巴特农神庙类比，确立其在幻想艺术中的崇高地位；再以\u201c请您用大理石，用玉石……\u201d的排比句式，铺陈圆明园的材料、建筑、陈设、装饰，营造出富丽堂皇、如梦如幻的境界；最后以\u201c亚洲文明的剪影\u201d收束。越是赞美，后文被焚毁越令人痛心，这是典型的\u201c以美衬丑\u201d。</p></div>
      <div class="fame-card"><div class="f-line">揭露罪行 · 反语讽刺（第4–5段）</div><p>以\u201c这个奇迹已经消失了\u201d独立成段，骤转直下。第5段揭露英法联军劫掠、纵火、分赃的强盗行径：\u201c两个强盗闯进了圆明园\u201d\u201c一个强盗洗劫财物，另一个强盗在放火\u201d。以\u201c丰功伟绩！收获巨大！\u201d的反语辛辣讽刺，以\u201c手挽手，笑嘻嘻地回到欧洲\u201d的神态描写刻画侵略者的无耻。\u201c强盗\u201d一词贯穿全段，与前文\u201c文明人\u201d形成尖锐对比。</p></div>
      <div class="fame-card"><div class="f-line">抗议谴责 · 区分朝野（第6–8段）</div><p>以\u201c文明对野蛮\u201d的颠倒对比，戳破欧洲中心论的虚伪。明确指出\u201c两个强盗，一个叫法兰西，另一个叫英吉利\u201d，直呼国名，毫不留情。同时以\u201c治人者的罪行不是治于人者的过错；政府有时会是强盗，而人民永远也不会是强盗\u201d区分政府与人民，体现人道主义立场。最后期盼\u201c解放了的干干净净的法兰西会把这份战利品归还给被掠夺的中国\u201d，正义凛然。</p></div>
      <div class="fame-card"><div class="f-line">证实偷窃 · 首尾呼应（第9–10段）</div><p>以\u201c现在，我证实，发生了一次偷窃，有两名窃贼\u201d作结，如法庭宣判，斩钉截铁。\u201c先生，以上就是我对远征中国的全部赞誉\u201d，\u201c全部赞誉\u201d与开篇\u201c多少赞誉\u201d首尾呼应，反语贯穿始终。所谓\u201c赞誉\u201d，实为最严厉的谴责，余味辛辣。</p></div>
    </div>
  </div>
  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card"><div class="f-line">反语贯穿，辛辣有力</div><p>反语是本文最突出的修辞特色。\u201c体面\u201d\u201c出色\u201d\u201c光荣\u201d\u201c赞誉\u201d\u201c胜利者\u201d\u201c丰功伟绩\u201d\u201c收获巨大\u201d\u201c文明\u201d，这些褒义词在文中全是反语——字面赞美，实则谴责。反语的运用，比直接怒斥更有力量：它以巴特勒的逻辑回击巴特勒，以欧洲人的\u201c文明\u201d标准衡量欧洲人的行为，让虚伪不攻自破。</p></div>
      <div class="fame-card"><div class="f-line">对比鲜明，爱憎分明</div><p>全文处处对比：圆明园的\u201c世界奇迹\u201d与\u201c荡然无存\u201d的对比；\u201c文明人\u201d与\u201c强盗\u201d的对比；\u201c文明\u201d与\u201c野蛮\u201d的对比（颠倒使用）；\u201c治人者\u201d与\u201c治于人者\u201d的对比；\u201c吞下赃物的法兰西\u201d与\u201c干干净净的法兰西\u201d的对比。对比中见爱憎，对比中显立场。</p></div>
      <div class="fame-card"><div class="f-line">铺陈排比，气势充沛</div><p>第3段盛赞圆明园时，大量运用铺陈和排比：\u201c请您用大理石，用玉石，用青铜，用瓷器建造一个梦\u201d\u201c饰以琉璃，饰以珐琅，饰以黄金，施以脂粉\u201d\u201c一座座花园，一方方水池，一眼眼喷泉\u201d\u201c希腊有巴特农神庙，埃及有金字塔，罗马有斗兽场，巴黎有圣母院\u201d。排比句式整齐，气势充沛，如江河奔涌，与后文的短句反语形成节奏上的张弛对比。</p></div>
      <div class="fame-card"><div class="f-line">书信形式，亲切而有力</div><p>本文以书信形式写成，以\u201c先生\u201d称呼巴特勒，以\u201c您\u201d对话，语气亲切自然。但在亲切的对话中，蕴含着最严厉的谴责——\u201c请您想象\u201d\u201c请往下读吧\u201d，看似客气，实则将对方置于被审判的位置。书信的私人化形式与公开谴责的内容形成张力，使文章既有说服力，又有感染力。</p></div>
    </div>
  </div>
  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card"><div class="f-line">在世界的某个角落，有一个世界奇迹。这个奇迹叫圆明园。</div><p>开篇总起，\u201c世界奇迹\u201d四字给予圆明园最高评价。\u201c某个角落\u201d写位置之远，却以\u201c世界\u201d限定\u201c奇迹\u201d，见出圆明园在人类文明中的地位。简洁有力，为下文的铺陈奠定基调。</p></div>
      <div class="fame-card"><div class="f-line">这个奇迹已经消失了。</div><p>独句成段，斩钉截铁。与前文长篇盛赞形成巨大落差，情感骤转。\u201c已经\u201d二字，含无尽痛惜——如此伟大的文明奇迹，竟已不复存在。这一句是全文情感的转折点，由赞美转入谴责，力量千钧。</p></div>
      <div class="fame-card"><div class="f-line">我们欧洲人是文明人，中国人在我们眼中是野蛮人。这就是文明对野蛮所干的事情。</div><p>全文最辛辣的反语。\u201c文明人\u201d\u201c野蛮人\u201d全是反语——以欧洲人的视角自述，再以\u201c这就是文明对野蛮所干的事情\u201d反戈一击。真正\u201c野蛮\u201d的是劫掠纵火的侵略者，真正\u201c文明\u201d的是创造了圆明园的中华民族。颠倒使用\u201c文明\u201d\u201c野蛮\u201d，戳破欧洲中心论的虚伪。</p></div>
      <div class="fame-card"><div class="f-line">治人者的罪行不是治于人者的过错；政府有时会是强盗，而人民永远也不会是强盗。</div><p>全文最深刻的论断。\u201c治人者\u201d\u201c治于人者\u201d化用孟子\u201c劳心者治人，劳力者治于人\u201d，文言色彩的对举，凝练有力。雨果谴责的是法国政府的侵略罪行，而非法国人民——这一区分体现了他的人道主义立场和清醒的政治头脑，也使他的谴责更有分量、更具说服力。</p></div>
      <div class="fame-card"><div class="f-line">现在，我证实，发生了一次偷窃，有两名窃贼。</div><p>如法庭宣判，斩钉截铁。\u201c证实\u201d一词，将侵略罪行定性为法律意义上的\u201c偷窃\u201d，\u201c窃贼\u201d比\u201c强盗\u201d更冷峻。独句成段，掷地有声，是全文的结论，也是对巴特勒\u201c多少赞誉\u201d的最终回答。</p></div>
    </div>
  </div>
  <div class="box">
    <h3>主题思想</h3>
    <p>《就英法联军远征中国致巴特勒上尉的信》以书信形式，愤怒地谴责了英法联军劫掠并焚毁圆明园的强盗行径，表达了对被侵略、被掠夺的中国人民的深切同情，展现了雨果博大的人道主义胸怀和公正的人类立场。</p>
    <p style="margin-top:10px">文章的深刻之处在于：雨果作为一名法国人，没有被狭隘的民族主义和\u201c爱国狂热\u201d裹挟，而是站在人类文明的立场上，公开谴责本国政府的侵略罪行。他以\u201c治人者的罪行不是治于人者的过错\u201d区分政府与人民，以\u201c岁月创造的一切都是属于人类的\u201d确立文明的人类属性。这种超越民族、超越国家的人类良知，在今天依然具有震撼人心的力量。</p>
    <p style="margin-top:10px;color:var(--ink3)">※ 这封信最初发表于1862年雨果的诗集《惩罚集》中。150多年后的今天，圆明园的残垣断壁依然在无声地诉说着那段历史，而雨果的这封信依然是人类良知的声音。</p>
  </div>
</section>'''

ACC_HTML = '''<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 用字 · 修辞 · 写法</span></div>
  <div class="box"><div class="acc-cat"><h3>重点词语</h3>
    <div class="acc-item"><span class="acc-w">体面</span><span class="acc-d">光荣、光彩。文中是反语，实际指侵略的可耻。</span></div>
    <div class="acc-item"><span class="acc-w">赞誉</span><span class="acc-d">称赞、赞美。文中是反语，实为谴责。</span></div>
    <div class="acc-item"><span class="acc-w">恍若月宫</span><span class="acc-d">仿佛像月中宫殿一样。恍若，仿佛、好像。</span></div>
    <div class="acc-item"><span class="acc-w">缀满</span><span class="acc-d">装饰得满满的。缀，装饰。</span></div>
    <div class="acc-item"><span class="acc-w">琉璃</span><span class="acc-d">一种用铝和钠的硅酸化合物烧制成的釉料，多用于建筑装饰。</span></div>
    <div class="acc-item"><span class="acc-w">珐琅</span><span class="acc-d">（fà láng）用石英、长石等烧制成的釉质涂料，涂在金属胎上。</span></div>
    <div class="acc-item"><span class="acc-w">眼花缭乱</span><span class="acc-d">眼睛看见复杂纷繁的东西而感到迷乱。缭，缠绕。</span></div>
    <div class="acc-item"><span class="acc-w">惊骇</span><span class="acc-d">惊慌害怕。骇，惊吓、震惊。</span></div>
    <div class="acc-item"><span class="acc-w">不可名状</span><span class="acc-d">不能用语言形容。名，说出。状，形容。</span></div>
    <div class="acc-item"><span class="acc-w">劫掠</span><span class="acc-d">抢劫、掠夺。掠，夺取。</span></div>
    <div class="acc-item"><span class="acc-w">荡然无存</span><span class="acc-d">形容原有的东西完全失去，一点没有留下。荡然，空荡荡的样子。</span></div>
    <div class="acc-item"><span class="acc-w">富丽堂皇</span><span class="acc-d">形容建筑物宏伟华丽。富丽，华丽。堂皇，气势盛大。</span></div>
    <div class="acc-item"><span class="acc-w">箱箧</span><span class="acc-d">（xiāng qiè）箱子。箧，小箱子。</span></div>
    <div class="acc-item"><span class="acc-w">治人者</span><span class="acc-d">统治别人的人，指统治者、政府。</span></div>
    <div class="acc-item"><span class="acc-w">治于人者</span><span class="acc-d">被别人统治的人，指人民、百姓。</span></div>
    <div class="acc-item"><span class="acc-w">制裁</span><span class="acc-d">用强力管束并惩处。</span></div>
    <div class="acc-item"><span class="acc-w">窃贼</span><span class="acc-d">偷东西的人。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>用字与读音</h3>
    <div class="acc-item"><span class="acc-w">赞誉</span><span class="acc-d">（yù）称赞。不要写成"誊"（téng，抄写）。</span></div>
    <div class="acc-item"><span class="acc-w">恍若</span><span class="acc-d">（huǎng）仿佛。竖心旁，不要写成"晃"（日字旁，摇晃）。</span></div>
    <div class="acc-item"><span class="acc-w">缀满</span><span class="acc-d">（zhuì）装饰。绞丝旁，不要写成"辍"（chuò，停止）。</span></div>
    <div class="acc-item"><span class="acc-w">珐琅</span><span class="acc-d">（fà láng）涂料名。"珐"王字旁，不要写成"法"。</span></div>
    <div class="acc-item"><span class="acc-w">朱鹭</span><span class="acc-d">（lù）鸟名。鸟字底，上面是"路"，笔画多不要漏写。</span></div>
    <div class="acc-item"><span class="acc-w">眼花缭乱</span><span class="acc-d">（liáo）缠绕。绞丝旁，不要写成"嘹"（口字旁，嘹亮）。</span></div>
    <div class="acc-item"><span class="acc-w">惊骇</span><span class="acc-d">（hài）惊吓。马字旁，不要写成"该"（言字旁）。</span></div>
    <div class="acc-item"><span class="acc-w">晨曦</span><span class="acc-d">（xī）阳光。日字旁，右边是"羲"，笔画多不要漏写。</span></div>
    <div class="acc-item"><span class="acc-w">瞥见</span><span class="acc-d">（piē）短时间地大略看看。目字底，不要写成"憋"（心字底）。</span></div>
    <div class="acc-item"><span class="acc-w">劫掠</span><span class="acc-d">（lüè）夺取。提手旁，不要写成"惊"（竖心旁）。</span></div>
    <div class="acc-item"><span class="acc-w">赃物</span><span class="acc-d">（zāng）贪污受贿或盗窃所得的财物。贝字旁，与"脏"（月字旁，不干净）区分。</span></div>
    <div class="acc-item"><span class="acc-w">箱箧</span><span class="acc-d">（qiè）小箱子。竹字头，不要写成"惬"（竖心旁，惬意）。</span></div>
    <div class="acc-item"><span class="acc-w">制裁</span><span class="acc-d">（cái）判定。衣字旁，不要写成"栽"（木字旁，栽种）。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>修辞方法</h3>
    <div class="acc-item"><span class="acc-w">反语</span><span class="acc-d">本文最突出的修辞。"体面""出色""光荣""赞誉""胜利者""丰功伟绩""收获巨大""文明"等褒义词在文中全是反语——字面赞美，实则谴责。反语比直接怒斥更有力量，让虚伪不攻自破。</span></div>
    <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">圆明园的"世界奇迹"与"荡然无存"对比；"文明人"与"强盗"对比；"文明"与"野蛮"颠倒使用；"治人者"与"治于人者"对比；"吞下赃物的法兰西"与"干干净净的法兰西"对比。对比中见爱憎。</span></div>
    <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">"请您用大理石，用玉石，用青铜，用瓷器建造一个梦""饰以琉璃，饰以珐琅，饰以黄金，施以脂粉""一座座花园，一方方水池，一眼眼喷泉""希腊有巴特农神庙，埃及有金字塔，罗马有斗兽场，巴黎有圣母院"。排比铺陈，气势充沛。</span></div>
    <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">"恍若月宫的建筑""建造一个梦""一千零一夜的一千零一个梦""亚洲文明的剪影"。以"梦""月宫""剪影"喻圆明园，见其虚幻之美与文化象征意义。</span></div>
    <div class="acc-item"><span class="acc-w">类比</span><span class="acc-d">"圆明园在幻想艺术中的地位就如同巴特农神庙在理想艺术中的地位"，以巴特农神庙类比圆明园，等量齐观，见出雨果对东方艺术的尊重。</span></div>
    <div class="acc-item"><span class="acc-w">设问</span><span class="acc-d">"为谁而建？为了各国人民。"自问自答，点明圆明园是全人类的文化财富，为谴责侵略者掠夺人类文明成果铺垫。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>写作借鉴</h3>
    <div class="acc-item"><span class="acc-w">欲抑先扬</span><span class="acc-d">开篇不急于反驳，而是复述对方观点，以"体面""赞誉"等反语假意承接，为下文的谴责蓄势。先扬后抑，比直接怒斥更有力量。</span></div>
    <div class="acc-item"><span class="acc-w">以美衬丑</span><span class="acc-d">用大量笔墨盛赞圆明园的艺术价值，越是写其美，后文被焚毁越令人痛心，侵略者的罪行越显得丑恶。以美衬丑，比直接写丑更有感染力。</span></div>
    <div class="acc-item"><span class="acc-w">反语运用</span><span class="acc-d">反语是本文最有力的武器。使用反语要注意：一是立场要鲜明，让读者能明确读出字面背后的真实含义；二是要贯穿始终，形成统一的讽刺基调；三是要与正面论述结合，反语之外要有明确的正面论断。</span></div>
    <div class="acc-item"><span class="acc-w">铺陈排比</span><span class="acc-d">第3段盛赞圆明园时，大量运用铺陈和排比，句式整齐，气势充沛。铺陈要围绕中心，不可杂乱堆砌；排比分句之间要有逻辑层次（如由材料到建筑到陈设到装饰）。</span></div>
    <div class="acc-item"><span class="acc-w">书信体议论文</span><span class="acc-d">以书信形式写议论文，以"您"对话，语气亲切自然，却能蕴含最严厉的谴责。书信的私人化形式与公开谴责的内容形成张力，使文章既有说服力，又有感染力。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>文化常识</h3>
    <div class="acc-item"><span class="acc-w">圆明园</span><span class="acc-d">清代大型皇家园林，位于北京西北郊，始建于康熙年间，历经150余年建成，由圆明园、长春园、绮春园组成，被誉为"万园之园"。1860年被英法联军劫掠焚毁。</span></div>
    <div class="acc-item"><span class="acc-w">巴特农神庙</span><span class="acc-d">古希腊雅典卫城的主体建筑，供奉雅典娜女神，是欧洲理想艺术的巅峰之作。19世纪初，英国额尔金勋爵将神庙上的雕塑运走，现存大英博物馆。</span></div>
    <div class="acc-item"><span class="acc-w">伏尔泰</span><span class="acc-d">（1694—1778）法国启蒙思想家、文学家、哲学家，被誉为"法兰西思想之王"。他在作品中多次赞美中国的文化与制度，是欧洲"中国热"的代表人物。</span></div>
    <div class="acc-item"><span class="acc-w">额尔金</span><span class="acc-d">（1811—1863）英国外交官，1860年任英国对华全权代表，下令焚毁圆明园。其父老额尔金（1766—1841）曾任英国驻奥斯曼帝国大使，将巴特农神庙雕塑运走。父子两代皆为文化强盗。</span></div>
    <div class="acc-item"><span class="acc-w">第二次鸦片战争</span><span class="acc-d">1856年至1860年英法联合发动的侵华战争。1860年10月，英法联军攻入北京，劫掠并焚毁圆明园，迫使清政府签订《北京条约》。</span></div>
    <div class="acc-item"><span class="acc-w">驳论文</span><span class="acc-d">议论文的一种，以反驳对方的错误论点为主，往往先破后立。本文先复述巴特勒的错误观点，再以盛赞圆明园和揭露强盗行径进行反驳，最后确立自己的立场。</span></div>
  </div></div>
</section>'''

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《就英法联军远征中国致巴特勒上尉的信》雨果</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">
<header class="hero">
  <div class="hero-side">法国 · 雨果</div>
  <h1 class="hero-title">就英法联军远征中国致巴特勒上尉的信</h1>
</header>
<nav class="nav">
  <div class="nav-in">
    <a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a>
    <div class="tool">
      <select id="fsSel" class="fs-sel" title="正文字体大小">
        <option value="100">100%%</option><option value="150">150%%</option><option value="200">200%%</option><option value="250">250%%</option><option value="300">300%%</option>
      </select>
      <button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button>
    </div>
  </div>
</nav>
<main class="wrap">
%(bg)s
<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 词语 · 手法</span></div>
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
    <button data-mode="note" data-rand="5">随机五组词语</button>
    <button data-mode="note" data-all="1">全部词语</button>
  </div>
</section>
<footer>
  <div class="kai">《就英法联军远征中国致巴特勒上尉的信》</div>
  <div>维克多·雨果 · 法国 · 1861年11月25日于高城居</div>
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
%(js)s
</script>
<script>
var DICT_WORDS = %(words)s;
var DICT_NOTES = %(notes)s;
</script>
</body>
</html>
''' % {
    'css': CSS, 'js': JS, 'bg': BG_HTML, 'fulltext': full_html,
    'verses': verses_html, 'app': APP_HTML, 'acc': ACC_HTML,
    'words': json.dumps(DICT_WORDS, ensure_ascii=False),
    'notes': json.dumps(DICT_NOTES, ensure_ascii=False),
}

io.open(OUT, 'w', encoding='utf-8').write(HTML)
print('OK', OUT, 'verses=', idx, 'words=', len(DICT_WORDS), 'notes=', len(DICT_NOTES))

# Post-process: replace ASCII quotes adjacent to Chinese chars with Chinese quotes
# Only process content OUTSIDE <script> tags
h = io.open(OUT, encoding='utf-8').read()
import re as _re
parts = _re.split(r'(<script[\s\S]*?</script>)', h)
for i in range(len(parts)):
    if parts[i].startswith('<script'):
        continue
    # Opening quote: " followed by Chinese char
    parts[i] = _re.sub(r'"(?=[\u4e00-\u9fff])', '\u201c', parts[i])
    # Closing quote: " preceded by Chinese char or Chinese punctuation
    parts[i] = _re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])"', '\u201d', parts[i])
h = ''.join(parts)
io.open(OUT, 'w', encoding='utf-8').write(h)
print('post-processed quotes')
