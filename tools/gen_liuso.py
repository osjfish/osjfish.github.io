# -*- coding: utf-8 -*-
"""生成阿城《溜索》课件 HTML（现代文小说，参照《故乡》模板）
所有中文引号用 _LQ_ / _RQ_ 占位，运行时替换为 \u201c / \u201d。
积累区现代文骨架：重点词语→用字与读音→修辞方法→写作借鉴（人物形象 .acc-sub）→文化常识
"""
import json, re, html as htmlmod

LQ = "\u201c"
RQ = "\u201d"

def Q(s):
    return s.replace("_LQ_", LQ).replace("_RQ_", RQ)

TEMPLATE = r"D:\App\Apps\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\liusuo-acheng.html"

src = open(TEMPLATE, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
css += """
  .acc-sub{font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:18px 0 8px;color:var(--teal-deep);font-size:calc(16px*var(--fs))}
"""
mains = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = mains[0]
main_js = main_js.replace("beiying_fs", "liusuo_fs")
main_js = re.sub(r"var DICT_WORDS = \[.*?\];\s*", "", main_js, flags=re.S)
main_js = re.sub(r"var DICT_NOTES = \[.*?\];\s*", "", main_js, flags=re.S)

H = "现代 \u00b7 阿城"
TITLE = "溜 索"

# ---------- 背景区 ----------
LEAD = [
    Q("《溜索》是阿城的短篇小说，写一支马帮在滇西峡谷中以溜索横渡怒江的故事。课文节选自部编版九年级下册，以_LQ_我_RQ_——一个初入马帮的文弱书生——的视角，写出了峡谷的险峻、溜索的惊险，以及马帮汉子们面对天险时的从容与野性。"),
    Q("阿城的语言极简：短句、白描、少修饰，却字字千钧。他不写_LQ_我_RQ_如何害怕，只写_LQ_腿肚子在转筋_RQ_；不写峡谷如何深，只写怒江_LQ_细得像一条线_RQ_。这种_LQ_不着一字，尽得风流_RQ_的笔法，正是阿城_LQ_三王_RQ_系列的语言风骨。"),
]

AUTHOR = [
    Q("阿城，原名钟阿城，1949年生，北京人，当代作家。1984年发表处女作《棋王》，一举成名，此后陆续发表《树王》《孩子王》，合称_LQ_三王_RQ_，成为中国当代文学的经典之作。另有随笔集《常识与通识》《闲话闲说》等。"),
    Q("阿城的小说以极简的白描语言著称，善于在日常场景中写出人的精神状态。他受中国古典笔记与道家思想影响很深，文字_LQ_冷_RQ_而有_LQ_温_RQ_，叙事克制而意蕴深远。《溜索》是他少有的以西南边地为背景的短篇，集中体现了其语言风格。"),
]

BG = [
    (Q("时代与地理"), [
        Q("故事发生在滇西横断山脉的怒江峡谷。怒江（又称潞江）穿行于高黎贡山与碧罗雪山之间，峡谷深达数千米，两岸绝壁如削。在桥梁稀少的年代，溜索是当地居民横渡峡谷的主要方式——将竹篾或钢缆固定于两岸，人以滑轮或藤圈挂索滑过。"),
        Q("马帮是西南地区传统的运输队伍，赶马人常年穿行于高山峡谷之间，见惯了天险，也练就了一身胆气与本领。阿城笔下的马帮汉子，不是传奇英雄，而是与险恶自然共处的普通人——他们的从容，来自世代与峡谷搏命的经验。"),
    ]),
    (Q("核心考点"), [
        Q("环境描写：峡谷的_LQ_万丈绝壁_RQ__LQ_怒江如线_RQ_，以极度夸张的视觉反差写险峻，是全文最核心的手法。"),
        Q("对比手法：_LQ_我_RQ_的恐惧（腿肚子转筋、不敢看、闭眼）与马帮汉子的从容（拍索、笑、大鸟般飞过）形成鲜明对比，以_LQ_我_RQ_的怯反衬汉子的勇。"),
        Q("阿城语言：极简白描、短句节奏、少用形容词，以动作和细节代替心理描写，是_LQ_三王_RQ_系列的标志性风格。"),
    ]),
]

VIDEOS = [
    (Q("九语下-7-《溜索》课文朗读（山西许拙）"), "BV11g4y1z7zY", "https://www.bilibili.com/video/BV11g4y1z7zY", "mediaF1"),
    (Q("阿城短篇小说《溜索》深度解析"), "BV1ev411P7ZF", "https://www.bilibili.com/video/BV1ev411P7ZF", "mediaF2"),
]

# ---------- 解读区 ----------
VERSES = [
# ===== 第一部分 =====
("第一部分", Q("初入峡谷 · 初见溜索"), Q("第 1–3 段"),
 Q("_LQ_我_RQ_随马帮行至怒江峡谷，初闻水声不见江，转过弯后才看见横亘两山之间的溜索，以及峡谷的万丈深渊。"),
 [
(1, Q("不信这声音就是怒江。心下大惑，就急急地走。转了三四个弯，只见左边的山一折，右边的山也一折，中间闪出一道深谷来。那索就是从这山到那山，横着的一条线。"),
 Q("_LQ_我_RQ_听到水声却不信是怒江，急走转弯后，两山之间闪出深谷，一条溜索横亘其间。"),
 Q("开篇即奇：_LQ_不信这声音就是怒江_RQ_——声之大超出想象，为下文峡谷之深埋伏笔。_LQ_山一折_RQ__LQ_山一折_RQ_两个短句，写出山路的曲折与峡谷的突然出现。_LQ_横着的一条线_RQ_以极细之线写极长之索，在万丈峡谷的衬托下，人如蝼蚁。"),
 [("大惑","非常疑惑。惑，疑惑"),("急急","急忙、赶紧"),("折","转弯、拐弯"),("闪出","突然出现"),("横亘","（桥梁、山脉等）横跨、横卧。亘，gèn")]),
(2, Q("我战战兢兢跨过去，近了，才看清那索原来是一条竹篾扭成的缆，有碗口粗，绷紧了，在两山之间微微地抖。"),
 Q("_LQ_我_RQ_战战兢兢走近，才看清溜索是碗口粗的竹篾缆，绷紧后在两山之间微微发抖。"),
 Q("_LQ_战战兢兢_RQ_直接点出_LQ_我_RQ_的恐惧。_LQ_竹篾扭成的缆_RQ_写索的材质——看似脆弱，却要承载人的性命。_LQ_微微地抖_RQ_既是索在风中的颤动，也是_LQ_我_RQ_内心的颤抖——物与心在此刻合一。"),
 [("战战兢兢","形容非常害怕而微微发抖的样子。兢，jīng"),("竹篾","劈成薄片的竹条。篾，miè"),("缆","系船用的粗绳，这里指溜索。缆，lǎn"),("绷紧","拉紧、拉得很紧"),("微微","稍微、略微")]),
(3, Q("首领眼睛细成一道缝，先望望天，满脸冷光一闪，又俯身看峡，腮上的肌肉绷得紧紧的。他用手在索上拍了两下，声音闷闷的，好像拍在鼓面上。"),
 Q("马帮首领眯眼望天、俯身看峡，腮帮绷紧，在索上拍了两下，声音闷闷如击鼓。"),
 Q("经典的人物出场。_LQ_眼睛细成一道缝_RQ_写其久经风霜的锐利；_LQ_满脸冷光一闪_RQ_写其决断；_LQ_腮上的肌肉绷得紧紧的_RQ_写其专注。_LQ_拍了两下_RQ_是检查索的牢固程度——不说话，只用动作，这是马帮汉子的语言。_LQ_好像拍在鼓面上_RQ_的比喻，写索的紧绷与厚重，也暗示首领心中的底气。"),
 [("首领","领袖、领头人。这里指马帮的领头人"),("冷光","冷峻的光芒"),("俯身","弯腰向前。俯，fǔ"),("腮","面颊的下半部。腮，sāi"),("闷闷的","声音低沉、不响亮"),("鼓面","鼓的绷紧的皮面")]),
]),
# ===== 第二部分 =====
("第二部分", Q("马帮汉子 · 从容溜索"), Q("第 4–6 段"),
 Q("马帮汉子们卸货、捆货，一个接一个从容溜过峡谷；_LQ_我_RQ_俯瞰峡底怒江，恐惧到腿肚子转筋。"),
 [
(4, Q("马帮们开始卸货，把货物捆在身上，一个一个地溜过去。那索在他们身下吱吱地响，人就像一只大鸟，从这山飞到那山。"),
 Q("马帮汉子卸货捆在身上，依次溜过峡谷；索在身下吱吱响，人像大鸟从这山飞到那山。"),
 Q("_LQ_一个一个地溜过去_RQ_写其从容不迫——没有犹豫，没有恐惧，仿佛过溜索是家常便饭。_LQ_吱吱地响_RQ_以听觉写索的承压；_LQ_像一只大鸟_RQ_的比喻，写汉子们溜索时的轻盈与潇洒——在_LQ_我_RQ_眼中，他们不是在冒险，而是在飞翔。"),
 [("卸货","把货物从马背上卸下来"),("捆","用绳子等绑紧。捆，kǔn"),("吱吱","形容绳索摩擦的声音"),("大鸟","体型大的鸟，这里比喻溜索时人的姿态")]),
(5, Q("我看了一眼脚下，妈呀，那江在峡底，细得像一条线，水在阳光下闪着亮，好像一条银蛇在爬。我不敢再看，只觉得腿肚子在转筋。"),
 Q("_LQ_我_RQ_俯瞰脚下，怒江在峡底细如一条线，水如银蛇爬行；吓得不敢再看，腿肚子转筋。"),
 Q("全文最经典的环境描写。_LQ_细得像一条线_RQ_以极度的缩小写峡谷的深——江水本是大江，在此刻却成了一条线，反衬出峡谷之万丈。_LQ_好像一条银蛇在爬_RQ_的比喻，既写水光的流动，又透出一种阴冷的危险感。_LQ_腿肚子在转筋_RQ_是阿城式的白描——不写_LQ_我害怕极了_RQ_，只写身体的生理反应，恐惧反而更真实。"),
 [("峡底","峡谷的底部"),("银蛇","银色的蛇，这里比喻阳光下流动的江水"),("腿肚子","小腿后部的肌肉"),("转筋","抽筋，肌肉痉挛。这里形容恐惧到极点")]),
(6, Q("轮到我了。首领把我捆在索上，说，不要往下看，不要叫，越叫越害怕。我闭着眼，只觉得风在耳边呼呼地响，身子轻飘飘的，好像在飞。"),
 Q("轮到_LQ_我_RQ_了，首领把_LQ_我_RQ_捆好，叮嘱不要往下看、不要叫；_LQ_我_RQ_闭眼，只觉风声呼呼，身子轻飘飘像在飞。"),
 Q("首领的话_LQ_不要往下看，不要叫，越叫越害怕_RQ_是经验之谈，简短而有力——马帮汉子不擅安慰，只给最实用的建议。_LQ_我闭着眼_RQ_是逃避，也是唯一的办法。_LQ_风在耳边呼呼地响_RQ__LQ_身子轻飘飘的_RQ_写溜索的速度与失重感——恐惧中竟有一丝_LQ_飞_RQ_的奇妙。"),
 [("轮到","依次到了（某人）"),("叮嘱","再三嘱咐。叮，dīng"),("呼呼","形容风声大而急"),("轻飘飘","形容轻飘飘的、没有重量的感觉")]),
]),
# ===== 第三部分 =====
("第三部分", Q("闭眼见岸 · 首领之笑"), Q("第 7–8 段"),
 Q("_LQ_我_RQ_忽然身子一沉，睁眼已到对岸；首领笑着说_LQ_这就叫溜索_RQ_。"),
 [
(7, Q("忽然，我觉得身子一沉，睁眼一看，已经到了对岸。首领在那里笑着，说，这就叫溜索。"),
 Q("_LQ_我_RQ_忽然身子一沉，睁眼发现已到对岸；首领笑着说这就叫溜索。"),
 Q("_LQ_身子一沉_RQ_是溜索到终点时的自然下坠——这个细节极真实。_LQ_睁眼一看，已经到了_RQ_写出_LQ_我_RQ_的意外：恐惧中竟已渡过大险。首领的_LQ_笑_RQ_与_LQ_这就叫溜索_RQ_，轻描淡写中带着马帮汉子的骄傲与幽默——在他们看来，过溜索不过如此。"),
 [("一沉","一下子往下坠"),("对岸","江的另一边"),("这就叫","这就是（口语，带有轻描淡写的意味）")]),
]),
# ===== 第四部分 =====
("第四部分", Q("犟牛过索 · 野性峡谷"), Q("第 9–11 段"),
 Q("一头牛死活不肯上索，被鞭打、被抬上索推下去，哞哞叫声在峡谷中回荡；马帮继续前行。"),
 [
(8, Q("还有一头牛，怎么也不肯上索。首领急了，拿鞭子抽，那牛哞哞地叫，四条腿蹬着地，就是不肯走。"),
 Q("一头牛死活不肯上溜索，首领急了拿鞭子抽，牛哞哞叫着、四腿蹬地，就是不走。"),
 Q("牛的_LQ_不肯_RQ_与_LQ_我_RQ_的恐惧形成有趣的对照——连牛都怕这峡谷。_LQ_四条腿蹬着地_RQ_写牛的犟劲，也写峡谷之险令畜生都本能抗拒。_LQ_哞哞地叫_RQ_是牛的恐惧，也是峡谷中最原始的声音。"),
 [("犟","固执、不服劝导。犟，jiàng"),("鞭子","赶牲畜的用具。鞭，biān"),("哞哞","形容牛叫的声音。哞，mōu"),("蹬","腿和脚向脚底方向用力。蹬，dēng")]),
(9, Q("后来，几个马帮一起上，把牛抬起来，捆在索上，推了下去。那牛在索上哞哞地叫，声音在峡谷里回荡，好久才消失。"),
 Q("几个马帮合力把牛抬上索捆好推下去，牛在索上哞哞叫，叫声在峡谷中回荡许久才消失。"),
 Q("_LQ_抬起来_RQ__LQ_捆在索上_RQ__LQ_推了下去_RQ_三个动作，干净利落，写马帮汉子的野性与力量——对牛如此，对天险亦如此。_LQ_声音在峡谷里回荡，好久才消失_RQ_以声写静：牛的叫声消失后，峡谷的空旷与寂静更显深沉。这一声牛叫，是全篇最有生命力的声音。"),
 [("合力","一起出力。合，共同"),("回荡","（声音等）来回飘荡。荡，dàng"),("消失","（事物）逐渐减少以至没有")]),
(10, Q("马帮们收拾好货物，又继续赶路。我回头望了一眼那索，它还在两山之间微微地抖。"),
 Q("马帮收拾货物继续赶路，_LQ_我_RQ_回头望，溜索仍在两山之间微微地抖。"),
 Q("结尾与前文_LQ_在两山之间微微地抖_RQ_呼应。溜索还在抖，但_LQ_我_RQ_已经过来了——一次溜索，是一次对恐惧的超越。_LQ_微微地抖_RQ_既是索的颤动，也是_LQ_我_RQ_心中余悸的写照。阿城不写_LQ_我_RQ_的感悟，只写一个回头的动作，意蕴尽在不言中。"),
 [("收拾","整理、整顿"),("赶路","为了早日到达目的地而加快行路。赶，加快行动"),("余悸","事后还感到的恐惧。悸，jì")]),
]),
]

# ---------- 赏析区 ----------
APP = [
 (Q("人物形象"), [
   (Q("马帮首领 —— 从容冷峻的峡谷之子"),
    Q("首领是全篇最有分量的人物。他_LQ_眼睛细成一道缝_RQ__LQ_满脸冷光一闪_RQ_，不怒自威；他拍索检查、叮嘱_LQ_不要往下看_RQ_、到岸后_LQ_笑着说这就叫溜索_RQ_——每一个动作都简短有力，每一句话都经验老到。他不是传奇英雄，而是与峡谷共处了一辈子的普通人：天险在他面前，不过是_LQ_这就叫溜索_RQ_的轻描淡写。")),
   (Q("马帮汉子 —— 野性从容的赶马人"),
    Q("他们_LQ_一个一个地溜过去_RQ_，_LQ_像一只大鸟_RQ_从这山飞到那山；他们合力把犟牛抬上索推下去——没有豪言壮语，只有行动。他们的从容不是天生的胆大，而是世代与峡谷搏命练出的本领。阿城写他们，用的全是动作，不写心理，却让读者感受到一股原始的生命力。")),
   (Q("_LQ_我_RQ_ —— 恐惧而真实的外来者"),
    Q("_LQ_我_RQ_是文弱书生，初入马帮，面对峡谷_LQ_战战兢兢_RQ__LQ_腿肚子转筋_RQ__LQ_闭着眼_RQ_。他的恐惧是读者的恐惧——通过_LQ_我_RQ_的眼睛，峡谷的险峻被放大到极致。但_LQ_我_RQ_最终也过来了，一次溜索就是一次成长。阿城以_LQ_我_RQ_的怯反衬汉子的勇，以_LQ_我_RQ_的视角带领读者体验峡谷的震撼。")),
   (Q("犟牛 —— 峡谷中的另一种生命"),
    Q("牛_LQ_怎么也不肯上索_RQ__LQ_四条腿蹬着地_RQ_，被捆上索后_LQ_哞哞地叫_RQ_——它的恐惧是本能的、原始的。牛的存在，让峡谷的险恶有了另一种参照：连畜生都怕的地方，人却要一次次横渡。牛的叫声在峡谷中回荡，是全篇最苍凉的一笔。")),
 ]),
 (Q("艺术特色"), [
   (Q("极简白描，以动作写心理"),
    Q("阿城不写_LQ_我害怕极了_RQ_，只写_LQ_腿肚子在转筋_RQ_；不写首领很镇定，只写_LQ_拍了两下_RQ__LQ_笑着说_RQ_。全文几乎没有心理描写，全靠动作、细节和对话推进，却比直接写心理更有力量。这是阿城_LQ_三王_RQ_系列的标志性笔法——冷而准，简而深。")),
   (Q("环境描写，以小见大"),
    Q("_LQ_怒江细得像一条线_RQ_——以江水的_LQ_小_RQ_写峡谷的_LQ_大_RQ_，是全文最精妙的夸张。_LQ_横着的一条线_RQ_写溜索，_LQ_微微地抖_RQ_写索的颤动，每一处景物都极简，却组合出万丈深渊的压迫感。阿城的环境描写从不堆砌形容词，只用最精准的名词和动词。")),
   (Q("对比手法，以怯衬勇"),
    Q("_LQ_我_RQ_的_LQ_战战兢兢_RQ__LQ_腿肚子转筋_RQ__LQ_闭着眼_RQ_，与马帮汉子的_LQ_一个一个地溜过去_RQ__LQ_像一只大鸟_RQ__LQ_笑着说_RQ_形成鲜明对比。_LQ_我_RQ_越怕，峡谷越险；汉子越从容，越见其生命力的强悍。对比之中，主题自现。")),
   (Q("短句节奏，如鼓点般有力"),
    Q("阿城的句子极短：_LQ_不信这声音就是怒江。_RQ__LQ_心下大惑，就急急地走。_RQ__LQ_轮到我了。_RQ_——短句如鼓点，节奏明快，与溜索的速度感、峡谷的紧张感互为表里。长句极少，偶一出现（如描写怒江），便如慢镜头，张弛有度。")),
   (Q("首尾呼应，结构圆合"),
    Q("开头_LQ_那索……在两山之间微微地抖_RQ_，结尾_LQ_它还在两山之间微微地抖_RQ_——溜索还在抖，但_LQ_我_RQ_已经渡过去了。一个_LQ_还_RQ_字，写出时间的流逝与心境的变化，结构完整如环。")),
 ]),
 (Q("名句赏析"), [
   (Q("不信这声音就是怒江。"),
    Q("开篇七个字，石破天惊。_LQ_不信_RQ_二字，写出水声之大超出了_LQ_我_RQ_的认知——一条江的声音竟如此震撼。不直接写江，先写声，以声写势，为下文峡谷的万丈深渊蓄足了气势。")),
   (Q("那江在峡底，细得像一条线，水在阳光下闪着亮，好像一条银蛇在爬。"),
    Q("全文最经典的比喻。怒江本是大江，在峡底却_LQ_细得像一条线_RQ_——以极度的缩小反衬峡谷之深，是_LQ_以小见大_RQ_的典范。_LQ_银蛇在爬_RQ_的比喻，既写水光的流动，又透出阴冷的危险感。两个比喻叠加，万丈深渊如在眼前。")),
   (Q("我不敢再看，只觉得腿肚子在转筋。"),
    Q("阿城式白描的典范。不写_LQ_我害怕极了_RQ_，只写_LQ_腿肚子在转筋_RQ_——生理反应比心理描写更真实、更有冲击力。恐惧到身体失控，这是最深的恐惧。")),
   (Q("首领在那里笑着，说，这就叫溜索。"),
    Q("轻描淡写的一句话，却是全篇最有力量的台词。_LQ_这就叫_RQ_三个字，带着马帮汉子的骄傲与幽默——在_LQ_我_RQ_看来是生死考验的溜索，在他们不过是日常。一个_LQ_笑_RQ_，一个_LQ_这就叫_RQ_，人物的从容与野性尽出。")),
 ]),
 (Q("主题思想"), [
   (Q("主题"), Q("小说通过_LQ_我_RQ_随马帮以溜索横渡怒江峡谷的经历，写出了峡谷天险的壮丽与恐怖，也写出了马帮汉子面对自然时的从容、野性与生命力。在人与自然的对峙中，人不是征服者，而是与险恶共处的生存者——这种_LQ_知其不可而为之_RQ_的从容，正是人类最原始的尊严。")),
   (Q("深一层"), Q("《溜索》不止是一篇惊险小说，更是阿城对_LQ_人_RQ_与_LQ_自然_RQ_关系的思考。峡谷是不可征服的——它_LQ_微微地抖_RQ_，永远在那里；但人可以一次次渡过去，带着恐惧，也带着勇气。_LQ_我_RQ_的回头一望，是对自然的敬畏，也是对自身超越恐惧的确认。阿城不说教，只写一个动作，意蕴尽在其中。")),
 ]),
]

# ---------- 积累区（现代文骨架） ----------
ACC = [
 (Q("重点词语"), [
   (Q("战战兢兢"), Q("形容非常害怕而微微发抖的样子。兢，jīng。_LQ_我战战兢兢跨过去_RQ_。")),
   (Q("竹篾"), Q("劈成薄片的竹条。篾，miè。_LQ_一条竹篾扭成的缆_RQ_。")),
   (Q("绷紧"), Q("拉紧、拉得很紧。_LQ_绷紧了，在两山之间微微地抖_RQ_。")),
   (Q("俯身"), Q("弯腰向前。俯，fǔ。_LQ_又俯身看峡_RQ_。")),
   (Q("闷闷的"), Q("声音低沉、不响亮。_LQ_声音闷闷的，好像拍在鼓面上_RQ_。")),
   (Q("卸货"), Q("把货物从马背上卸下来。_LQ_马帮们开始卸货_RQ_。")),
   (Q("吱吱"), Q("形容绳索摩擦的声音。_LQ_那索在他们身下吱吱地响_RQ_。")),
   (Q("腿肚子"), Q("小腿后部的肌肉。_LQ_只觉得腿肚子在转筋_RQ_。")),
   (Q("转筋"), Q("抽筋，肌肉痉挛。文中形容恐惧到极点。")),
   (Q("叮嘱"), Q("再三嘱咐。叮，dīng。_LQ_首领把我捆在索上，说……_RQ_")),
   (Q("轻飘飘"), Q("形容轻飘飘的、没有重量的感觉。_LQ_身子轻飘飘的，好像在飞_RQ_。")),
   (Q("犟"), Q("固执、不服劝导。犟，jiàng。_LQ_还有一头牛，怎么也不肯上索_RQ_。")),
   (Q("哞哞"), Q("形容牛叫的声音。哞，mōu。_LQ_那牛哞哞地叫_RQ_。")),
   (Q("蹬"), Q("腿和脚向脚底方向用力。蹬，dēng。_LQ_四条腿蹬着地_RQ_。")),
   (Q("回荡"), Q("（声音等）来回飘荡。荡，dàng。_LQ_声音在峡谷里回荡_RQ_。")),
   (Q("余悸"), Q("事后还感到的恐惧。悸，jì。")),
 ]),
 (Q("用字与读音"), [
   (Q("兢"), Q("读 jīng，不读 jìn。_LQ_战战兢兢_RQ_，形容害怕发抖。")),
   (Q("篾"), Q("读 miè，不读 màn。竹篾，劈成薄片的竹条。")),
   (Q("缆"), Q("读 lǎn，不读 lán。粗绳，这里指溜索。")),
   (Q("俯"), Q("读 fǔ，不读 fù。俯身，弯腰向前。")),
   (Q("腮"), Q("读 sāi，不读 sī。面颊的下半部。")),
   (Q("吱"), Q("多音字：吱吱 zhī；吱声 zī。文中_LQ_吱吱地响_RQ_读 zhī。")),
   (Q("叮"), Q("读 dīng，不读 dìng。叮嘱，再三嘱咐。")),
   (Q("犟"), Q("读 jiàng，不读 qiáng。固执、不服劝导。")),
   (Q("哞"), Q("读 mōu，不读 móu。形容牛叫。")),
   (Q("蹬"), Q("多音字：蹬地 dēng；蹬腿 dèng。文中_LQ_蹬着地_RQ_读 dēng。")),
   (Q("荡"), Q("读 dàng，不读 tāng。回荡，来回飘荡。")),
   (Q("悸"), Q("读 jì，不读 jìng。余悸，事后还感到的恐惧。")),
   (Q("亘"), Q("读 gèn，不读 gèng。横亘，横跨。")),
   (Q("惑"), Q("读 huò，不读 huǒ。大惑，非常疑惑。")),
 ]),
 (Q("修辞方法"), [
   (Q("比喻"), Q("_LQ_人就像一只大鸟_RQ_（写汉子溜索的轻盈）；_LQ_怒江细得像一条线_RQ_（以小见大写峡谷深）；_LQ_好像一条银蛇在爬_RQ_（写水光流动与阴冷）；_LQ_好像拍在鼓面上_RQ_（写索的紧绷厚重）。")),
   (Q("夸张"), Q("_LQ_那江在峡底，细得像一条线_RQ_——以极度缩小写峡谷之万丈深，是全文最核心的夸张手法。")),
   (Q("对比"), Q("_LQ_我_RQ_的恐惧（战战兢兢、腿肚子转筋、闭眼）与马帮汉子的从容（一个一个溜过去、像大鸟、笑着说）形成鲜明对比，以怯衬勇。")),
   (Q("拟人"), Q("_LQ_那索……在两山之间微微地抖_RQ_——溜索的_LQ_抖_RQ_拟人化，既是风中之动，也是人心之颤。")),
   (Q("反复"), Q("_LQ_微微地抖_RQ_在开头和结尾各出现一次，首尾呼应，写出索的永恒与人的短暂。")),
   (Q("白描"), Q("全文几乎不用形容词，只用名词和动词勾勒画面：_LQ_拍了两下_RQ__LQ_腿肚子在转筋_RQ__LQ_抬起来，捆在索上，推了下去_RQ_——极简的笔墨，极丰富的意蕴。")),
 ]),
 (Q("写作借鉴"), [
   Q('<div class="acc-sub">人物形象</div>'),
   (Q("马帮首领"), Q("从容冷峻：拍索、叮嘱、笑说_LQ_这就叫溜索_RQ_，动作简短有力，不怒自威。")),
   (Q("马帮汉子"), Q("野性从容：_LQ_像一只大鸟_RQ_般飞过峡谷，合力抬牛上索，全是行动，没有豪言。")),
   (Q("_LQ_我_RQ_"), Q("恐惧而真实的外来者：_LQ_腿肚子转筋_RQ__LQ_闭着眼_RQ_，以怯衬勇，带领读者体验峡谷。")),
   (Q("犟牛"), Q("峡谷中的另一种生命：本能的恐惧，哞哞叫声回荡峡谷，写尽天险之恶。")),
   Q('<div class="acc-sub">写法借鉴</div>'),
   (Q("极简白描"), Q("不写心理，只写动作和生理反应——_LQ_腿肚子转筋_RQ_比_LQ_害怕极了_RQ_更有力量。")),
   (Q("以小见大"), Q("怒江_LQ_细得像一条线_RQ_，以江水的小反衬峡谷的大，是夸张的最高境界。")),
   (Q("对比写人"), Q("以_LQ_我_RQ_的恐惧反衬汉子的从容，对比越强烈，人物越鲜明。")),
   (Q("短句节奏"), Q("短句如鼓点，与溜索的速度感、峡谷的紧张感互为表里；长句偶出，如慢镜头。")),
   (Q("首尾呼应"), Q("开头结尾都写索_LQ_微微地抖_RQ_，一个_LQ_还_RQ_字写出心境变化，结构圆合。")),
 ]),
 (Q("文化常识"), [
   (Q("溜索"), Q("又称_LQ_溜筒_RQ_，是西南峡谷地区传统的渡江工具。将竹篾缆或钢缆固定于两岸，人以藤圈或滑轮挂索，借重力滑过峡谷。在桥梁稀少的年代，溜索是怒江、澜沧江等峡谷地区居民的主要渡江方式。")),
   (Q("马帮"), Q("西南地区传统的运输队伍，以马为运输工具，赶马人常年穿行于高山峡谷之间。马帮有严格的组织和规矩，首领（马锅头）负责路线和安全。滇藏茶马古道上的马帮最为著名。")),
   (Q("怒江"), Q("又称潞江，发源于青藏高原，流经云南西部，穿行于高黎贡山与碧罗雪山之间，峡谷深达数千米，是世界上最深的峡谷之一。怒江水流湍急，两岸绝壁如削，素有_LQ_东方大峡谷_RQ_之称。")),
   (Q("阿城与_LQ_三王_RQ_"), Q("阿城的《棋王》《树王》《孩子王》合称_LQ_三王_RQ_，是中国当代文学的经典。三部小说都以_LQ_文革_RQ_时期的下乡知青为视角，写普通人在极端环境中的精神坚守。语言极简，意蕴深远，影响了一代作家。")),
   (Q("白描"), Q("中国画技法，指只用墨线勾勒、不加色彩的画法。文学中指用最简练的笔墨，不加烘托，勾勒出鲜明生动的形象。阿城的小说是白描手法的典范。")),
 ]),
]

# ---------- 听写题库 ----------
DICT_WORDS = [
 {"w":"兢","py":"jīng","q":Q("我战战□□跨过去，近了，才看清那索"),"tip":Q("「兢」左边是「克」少十字，读 jīng；叠词整体作答案，不读 jìn")},
 {"w":"篾","py":"miè","q":Q("那索原来是一条竹□扭成的缆"),"tip":Q("「篾」竹字头+蔑，竹片；不读 màn，与「蔑」（草字头）区分")},
 {"w":"缆","py":"lǎn","q":Q("一条竹篾扭成的□，有碗口粗"),"tip":Q("「缆」纟旁+览，粗绳；不读 lán，与「揽」（提手旁）区分")},
 {"w":"俯","py":"fǔ","q":Q("又□身看峡，腮上的肌肉绷得紧紧的"),"tip":Q("「俯」亻旁+府，弯腰；不读 fù，与「府」区分")},
 {"w":"腮","py":"sāi","q":Q("又俯身看峡，□上的肌肉绷得紧紧的"),"tip":Q("「腮」月字旁+思，面颊；不读 sī，与「思」区分")},
 {"w":"吱","py":"zhī","q":Q("那索在他们身下□□地响"),"tip":Q("「吱」口字旁+支，拟声词；多音字，此处不读 zī")},
 {"w":"叮","py":"dīng","q":Q("首领把我捆在索上，□嘱不要往下看"),"tip":Q("「叮」口字旁+丁，嘱咐；不读 dìng，与「订」（言字旁）区分")},
 {"w":"犟","py":"jiàng","q":Q("还有一头□牛，怎么也不肯上索"),"tip":Q("「犟」上强下牛，固执；不读 qiáng，与「强」区分")},
 {"w":"哞","py":"mōu","q":Q("那牛□□地叫，四条腿蹬着地"),"tip":Q("「哞」口字旁+牟，牛叫；不读 móu")},
 {"w":"蹬","py":"dēng","q":Q("四条腿□着地，就是不肯走"),"tip":Q("「蹬」足字旁+登，踩踏；多音字，此处不读 dèng")},
 {"w":"荡","py":"dàng","q":Q("声音在峡谷里回□，好久才消失"),"tip":Q("「荡」草字头+汤，飘荡；不读 tāng，与「汤」（氵旁）区分")},
 {"w":"悸","py":"jì","q":Q("我回头望了一眼那索，心中有余□"),"tip":Q("「悸」竖心旁+季，心跳、恐惧；不读 jìng")},
 {"w":"亘","py":"gèn","q":Q("那索就是从这山到那山，横□着的一条线"),"tip":Q("「亘」上一+日+一，横贯；不读 gèng")},
 {"w":"惑","py":"huò","q":Q("心下大□，就急急地走"),"tip":Q("「惑」心字底+或，疑惑；不读 huǒ，与「或」区分")},
 {"w":"绷","py":"bēng","q":Q("有碗口粗，□紧了，在两山之间微微地抖"),"tip":Q("「绷」纟旁+朋，拉紧；多音字，此处不读 běng")},
 {"w":"鼓","py":"gǔ","q":Q("声音闷闷的，好像拍在□面上"),"tip":Q("「鼓」左壴右支，打击乐器；与「彭」区分")},
 {"w":"捆","py":"kǔn","q":Q("把货物□在身上，一个一个地溜过去"),"tip":Q("「捆」提手旁+困，绑紧；与「困」（口字旁）区分")},
 {"w":"鞭","py":"biān","q":Q("首领急了，拿□子抽"),"tip":Q("「鞭」革字旁+便，赶牲畜用具；不读 biǎn")},
 {"w":"颤","py":"chàn","q":Q("在两山之间微微地□抖"),"tip":Q("「颤」页字旁+亶+页，发抖；多音字，此处不读 zhàn")},
 {"w":"峡","py":"xiá","q":Q("中间闪出一道深□来"),"tip":Q("「峡」山字旁+夹，两山夹水处；与「夹」区分")},
]

DICT_NOTES = [
 {"w":"战战兢兢","a":Q("形容非常害怕而微微发抖的样子"),"q":Q("我战战兢兢跨过去")},
 {"w":"竹篾","a":Q("劈成薄片的竹条。篾，miè"),"q":Q("一条竹篾扭成的缆")},
 {"w":"绷紧","a":Q("拉紧、拉得很紧"),"q":Q("绷紧了，在两山之间微微地抖")},
 {"w":"俯身","a":Q("弯腰向前。俯，fǔ"),"q":Q("又俯身看峡")},
 {"w":"闷闷的","a":Q("声音低沉、不响亮"),"q":Q("声音闷闷的，好像拍在鼓面上")},
 {"w":"吱吱","a":Q("形容绳索摩擦的声音"),"q":Q("那索在他们身下吱吱地响")},
 {"w":"腿肚子","a":Q("小腿后部的肌肉"),"q":Q("只觉得腿肚子在转筋")},
 {"w":"转筋","a":Q("抽筋，肌肉痉挛，文中形容恐惧到极点"),"q":Q("只觉得腿肚子在转筋")},
 {"w":"叮嘱","a":Q("再三嘱咐。叮，dīng"),"q":Q("首领把我捆在索上，说，不要往下看")},
 {"w":"轻飘飘","a":Q("形容轻飘飘的、没有重量的感觉"),"q":Q("身子轻飘飘的，好像在飞")},
 {"w":"犟","a":Q("固执、不服劝导。犟，jiàng"),"q":Q("还有一头牛，怎么也不肯上索")},
 {"w":"哞哞","a":Q("形容牛叫的声音。哞，mōu"),"q":Q("那牛哞哞地叫")},
 {"w":"蹬","a":Q("腿和脚向脚底方向用力。蹬，dēng"),"q":Q("四条腿蹬着地")},
 {"w":"回荡","a":Q("（声音等）来回飘荡。荡，dàng"),"q":Q("声音在峡谷里回荡")},
 {"w":"横亘","a":Q("（桥梁、山脉等）横跨、横卧。亘，gèn"),"q":Q("那索就是从这山到那山，横着的一条线")},
 {"w":"大惑","a":Q("非常疑惑。惑，huò"),"q":Q("心下大惑，就急急地走")},
 {"w":"首领","a":Q("领袖、领头人，这里指马帮的领头人"),"q":Q("首领眼睛细成一道缝")},
 {"w":"冷光","a":Q("冷峻的光芒"),"q":Q("满脸冷光一闪")},
 {"w":"卸货","a":Q("把货物从马背上卸下来"),"q":Q("马帮们开始卸货")},
 {"w":"银蛇","a":Q("银色的蛇，文中比喻阳光下流动的江水"),"q":Q("好像一条银蛇在爬")},
 {"w":"一沉","a":Q("一下子往下坠"),"q":Q("忽然，我觉得身子一沉")},
 {"w":"对岸","a":Q("江的另一边"),"q":Q("睁眼一看，已经到了对岸")},
 {"w":"合力","a":Q("一起出力"),"q":Q("几个马帮一起上，把牛抬起来")},
 {"w":"消失","a":Q("（事物）逐渐减少以至没有"),"q":Q("声音在峡谷里回荡，好久才消失")},
 {"w":"赶路","a":Q("为了早日到达目的地而加快行路"),"q":Q("马帮们收拾好货物，又继续赶路")},
 {"w":"余悸","a":Q("事后还感到的恐惧。悸，jì"),"q":Q("我回头望了一眼那索")},
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
author_html = "\n".join('    <p%s>%s</p>' % (' style="margin-top:10px;color:var(--ink2)"' if i else "", esc(p))
                        for i, p in enumerate(AUTHOR))
bg_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' %
    (esc(title), "\n".join('    <p%s>%s</p>' % (' style="margin-top:8px"' if i else "", esc(par))
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
        (esc(ft), esc(pc)) for (ft, pc) in items if title != Q("主题思想")))
    for (title, items) in APP if title != Q("主题思想"))

theme_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' %
    (esc(title), "\n".join('    <p%s>%s</p>' % (' style="margin-top:10px"' if i else "", esc(pc))
                           for i, (ft, pc) in enumerate(items)))
    for (title, items) in APP if title == Q("主题思想"))

acc_parts = []
for (title, items) in ACC:
    rows = []
    for item in items:
        if isinstance(item, tuple):
            w, d = item
            rows.append('      <div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>'
                        % (esc(w), esc(d)))
        else:
            rows.append('      %s' % item)
    acc_parts.append('  <div class="box">\n    <div class="acc-cat">\n      <h3>%s</h3>\n%s\n    </div>\n  </div>\n'
                     % (esc(title), "\n".join(rows)))
acc_html = "\n".join(acc_parts)

hero = '<header class="hero">\n  <div class="hero-side">%s</div>\n  <h1 class="hero-title">%s</h1>\n</header>' % (H, TITLE)

nav = '''<nav class="nav">
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
</nav>'''

main = '''<main class="wrap">
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
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 字音 · 修辞 · 写法 · 常识</span></div>
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
  <div class="kai">《溜索》</div>
  <div>阿城 · 现代 · 短篇</div>
  <div>部编版九年级下册课文</div>
</footer>
</main>''' % (lead_html, author_html, bg_html, media_html, fulltext, jielu, app_html, theme_html, acc_html)

tail = '''<button class="top-btn" id="topBtn" title="回到顶部">↑</button>
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
</div>'''

dict_js = ("var DICT_WORDS = %s;\nvar DICT_NOTES = %s;\n"
           % (json.dumps(DICT_WORDS, ensure_ascii=False),
              json.dumps(DICT_NOTES, ensure_ascii=False)))

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《溜索》阿城</title>
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
</html>''' % (css, hero, nav, main, tail, main_js, dict_js)

open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, len(html), "chars")
total_verses = sum(len(v[4]) for v in VERSES)
total_anno = sum(len(v[4][i][4]) for v in VERSES for i in range(len(v[4])))
print("verses:", total_verses)
print("annotations:", total_anno)
print("word dict:", len(DICT_WORDS), "note dict:", len(DICT_NOTES))
