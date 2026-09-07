# -*- coding: utf-8 -*-
"""生成夏浩然《"飞天"凌空》课件 HTML（新闻特写类）"""
import json, re, html as htmlmod

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\feitianlingkong-xiahaoran.html"

src = open(TEMPLATE, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
mains = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = mains[0].replace("beiying_fs", "feitian_fs")

H = "现代 · 夏浩然"
TITLE = "\u201c飞天\u201d凌空"

LEAD = [
    "1982年11月，第九届亚洲运动会在印度新德里举行。11月24日，女子10米跳台跳水决赛中，16岁的中国姑娘吕伟以精彩的表现夺得金牌。这篇新闻特写由夏浩然、樊云芳发自新德里，以极具画面感的笔触，定格了吕伟跳水夺冠那1.7秒的精彩瞬间。",
    "文章不同于一般消息的概括叙述，而是运用电影特写镜头般的手法，把吕伟跳水的全过程分解为起跳、腾空、入水三个慢镜头，用细腻的描写和生动的比喻，让读者如临其境、如见其人。文章发表后被誉为\u201c特写中的珍品\u201d，是中国新闻特写的经典之作。",
]

AUTHOR = [
    "夏浩然，当代体育新闻记者，长期从事体育报道工作。樊云芳，当代女记者，以细腻生动的特写写作著称。两人合作采写了大量体育新闻特写，善于捕捉运动场上最精彩的瞬间，用文学化的笔法展现体育之美。",
    "这篇特写写于1982年11月24日，发自印度新德里亚运会赛场，报道了吕伟夺得女子10米跳台跳水金牌的盛况。文章以1.7秒的跳水动作为核心，用慢镜头般的笔法逐层展开，既有新闻的真实性，又有文学的感染力，是新闻特写的典范之作。",
]

BG = [
    ("写作背景", [
        "1982年新德里亚运会：第九届亚洲运动会于1982年11月19日至12月4日在印度新德里举行。中国代表团共获得61枚金牌，首次跃居亚运会金牌总数第一，标志着中国亚洲体育强国地位的确立。",
        "吕伟夺金：1982年11月24日，女子10米跳台跳水决赛中，16岁的中国选手吕伟以完美的表现夺得金牌，她的队友周继红获得银牌。吕伟的跳水动作\u201c5136\u201d（向前翻腾一周半转体三周）获得了9.5分的高分。",
        "新闻特写的兴起：20世纪80年代，中国新闻界开始重视新闻特写这一文体，强调用文学化的笔法报道新闻事实，增强新闻的可读性和感染力。这篇《\u201c飞天\u201d凌空》正是这一时期新闻特写的代表作。",
    ]),
    ("文体知识", [
        "新闻特写的定义：新闻特写是截取新闻事件中最具有价值、最生动感人、最富有特征的片段和部分予以放大，从而鲜明再现典型人物、事件、场景的一种新闻体裁。",
        "新闻特写的特点：一是生动性，用细腻的描写和生动的比喻再现现场；二是聚焦性，截取最精彩的瞬间或片段集中笔墨描写；三是现场感，让读者如临其境、如见其人；四是真实性，必须基于真实的新闻事实，不能虚构。",
        "新闻特写与消息的区别：消息侧重概括叙述，强调时效性和全面性；特写侧重细致描写，强调生动性和感染力。消息告诉读者\u201c发生了什么\u201d，特写让读者\u201c看到了什么\u201d。",
    ]),
]

VIDEOS = [
    ("课文诵读《\u201c飞天\u201d凌空》",
     "BV1nL411b7RN",
     "https://www.bilibili.com/video/BV1nL411b7RN",
     "mediaF1"),
    ("1.7秒惊艳世界！看懂《\u201c飞天\u201d凌空》里的跳水传奇",
     "BV1d3gN6iEy5",
     "https://www.bilibili.com/video/BV1d3gN6iEy5",
     "mediaF2"),
]

VERSES = [
(1, "她站在10米高台的前沿，沉静自若，风度优雅，白云似在她的头顶飘浮，飞鸟掠过她的身旁。这是达卡多拉游泳场的8000名观众一齐翘首而望、屏息敛声的一刹那。",
 "第一段（起跳前）：描写吕伟站在10米高台上的静态形象和全场观众屏息以待的紧张气氛。",
 "以静写动，先写吕伟\u201c沉静自若，风度优雅\u201d的从容姿态，再用\u201c白云飘浮\u201d\u201c飞鸟掠过\u201d的动态景物衬托高台的高耸和人物的镇定。\u201c8000名观众一齐翘首而望、屏息敛声\u201d从侧面渲染紧张气氛，\u201c一刹那\u201d点明这是关键时刻，为下文的精彩跳水蓄势。",
 [("沉静自若","沉着镇定，不慌不忙。自若，不变常态"),("风度优雅","举止姿态优美高雅。风度，举止姿态"),("掠过","轻轻擦过或拂过。掠，轻轻擦过"),("达卡多拉","印度新德里的一个游泳场名称"),("翘首而望","抬起头来望。翘首，抬起头"),("屏息敛声","暂时抑止呼吸和语声，形容紧张专注。屏，抑止；敛，收束"),("一刹那","极短的时间。刹，chà")]),

(2, "轻舒双臂，向上举起，只见吕伟轻轻一蹬，就向空中飞去。一瞬间，她那修长美妙的身体犹如被空气托住了，衬着蓝天白云，酷似敦煌壁画中凌空翔舞的\u201c飞天\u201d。",
 "第二段（起跳）：描写吕伟起跳的瞬间动作和腾空而起的优美姿态，以\u201c飞天\u201d比喻点题。",
 "动作描写精准有力：\u201c轻舒\u201d\u201c向上举起\u201d\u201c轻轻一蹬\u201d\u201c向空中飞去\u201d，一连串动词写出起跳的轻盈有力。\u201c犹如被空气托住\u201d用比喻写腾空时的从容，\u201c酷似敦煌壁画中凌空翔舞的\u2018飞天\u2019\u201d是全文的核心比喻，既写出姿态的优美，又呼应标题，赋予跳水动作以艺术的美感和文化的意蕴。",
 [("轻舒","轻轻舒展。舒，伸展"),("蹬","腿和脚向脚底方向用力。这里指起跳时用力踏台"),("修长","细长。修，长"),("犹如","好像、如同"),("托住","支撑住。托，用手掌或其他东西向上承受"),("酷似","极其相似。酷，程度深的"),("敦煌壁画","甘肃敦煌莫高窟的壁画，以飞天形象著称"),("凌空","高高地在空中。凌，升高、在空中"),("翔舞","飞翔舞动。翔，盘旋地飞")]),

(3, "紧接着，是向前翻腾一周半，同时伴随着旋风般的空中转体三周，动作疾如流星，又潇洒自如，1.7秒的时间对她似乎特别慷慨，让她从容不迫地展示身体优美的线条，从前伸的手指，一直延续到绷直的足尖。",
 "第三段（空中翻腾转体）：描写吕伟在空中翻腾一周半、转体三周的高难度动作，突出动作的快速、优美和从容。",
 "这一段是全文最精彩的\u201c慢镜头\u201d描写。\u201c旋风般\u201d\u201c疾如流星\u201d用比喻写动作的快速，\u201c潇洒自如\u201d\u201c从容不迫\u201d写姿态的优美从容。\u201c1.7秒的时间对她似乎特别慷慨\u201d用拟人手法，把时间写得有情有义，在极短的时间里吕伟却能从容展示优美线条，更见其技艺高超。\u201c从前伸的手指，一直延续到绷直的足尖\u201d以细节描写写身体线条的舒展完美。",
 [("翻腾","上下滚动。这里指跳水时身体向前翻转"),("旋风般","像旋风一样，形容快速。旋风，螺旋状的疾风"),("转体","身体绕纵轴转动。体育术语"),("疾如流星","快得像流星一样。疾，快；流星，星际空间闯入大气的发光体"),("潇洒自如","举止自然大方，不受拘束。潇洒，举止自然大方"),("慷慨","不吝惜。这里用拟人手法，说时间给了她充分展示的机会"),("从容不迫","非常镇静、不慌不忙的样子。从容，镇静"),("线条","这里指身体的轮廓和姿态"),("绷直","拉紧伸直。绷，拉紧"),("足尖","脚尖。足，脚")]),

(4, "还没等观众从眼花缭乱中反应过来，她已经展开身体，像轻盈的、笔直的箭，\u201c哧\u201d地插进碧波之中，几串白色的气泡拥抱了这位自天而降的仙女，四面水花则悄然不惊。",
 "第四段（入水）：描写吕伟入水的瞬间，以\u201c箭\u201d的比喻和\u201c悄然不惊\u201d的水花写入水的完美。",
 "这一段写跳水的最后一个动作——入水。\u201c还没等观众从眼花缭乱中反应过来\u201d从观众角度写动作之快，\u201c像轻盈的、笔直的箭\u201d用比喻写入水时身体的笔直和轻盈，\u201c哧\u201d拟声词写入水的干脆利落。\u201c几串白色的气泡拥抱了这位自天而降的仙女\u201d用拟人和比喻，把气泡写得有情，把吕伟比作仙女，极写其优美。\u201c四面水花则悄然不惊\u201d以极小的水花反衬入水技术的完美，\u201c压水花\u201d是跳水评分的重要标准。",
 [("眼花缭乱","眼睛看见复杂纷繁的东西而感到迷乱。缭乱，纷乱"),("轻盈","形容女子身材苗条，动作轻快。盈，充满"),("笔直","很直。笔，像笔一样直"),("哧","拟声词，形容快速插入水中的声音"),("碧波","碧绿色的水波。碧，青绿色"),("气泡","气体在液体中形成的球状或半球状体"),("拥抱","为表示亲爱而相抱。这里用拟人手法写气泡环绕"),("自天而降","从天上降落下来。形容从高台跃下入水"),("悄然不惊","寂静无声，没有惊动。悄然，形容寂静无声"),("水花","水受到冲击而形成的许多小水泡")]),

(5, "\u201c妙！好极了！\u201d站在我们旁边的一名外国记者跳了起来。这时，整个游泳场都沸腾了，如梦初醒的观众用震耳欲聋的掌声和欢呼声，来向他们喜爱的运动员表达由衷的赞赏。",
 "第五段（观众反应）：描写跳水结束后外国记者和全场观众的热烈反应，从侧面烘托吕伟表演的精彩。",
 "这一段从正面描写转向侧面烘托。先写一名外国记者\u201c跳了起来\u201d的激动反应和\u201c妙！好极了！\u201d的赞叹，以点带面；再写\u201c整个游泳场都沸腾了\u201d的全场反应，\u201c沸腾\u201d一词写出气氛的热烈。\u201c如梦初醒\u201d呼应前文观众的\u201c屏息敛声\u201d，说明观众刚才看得入了神；\u201c震耳欲聋\u201d写掌声欢呼声之大，\u201c由衷\u201d写赞赏的真诚。侧面描写比直接说\u201c表演很精彩\u201d更有感染力。",
 [("沸腾","液体达到一定温度时急剧转化为气体的现象。这里比喻情绪高涨、场面热烈"),("如梦初醒","好像刚从梦中醒过来，比喻从糊涂、错误的境地中刚刚醒悟过来。这里指观众刚才看得入了神，现在才反应过来"),("震耳欲聋","耳朵都快震聋了，形容声音很大。欲，将要"),("由衷","出于本心。衷，内心"),("赞赏","赞美赏识。赏，赞美")]),

(6, "吕伟精彩的表演，将游泳场的气氛推向了高潮。她的这个动作\u201c5136\u201d，让几位裁判亮出了9.5分的高分。",
 "第六段（裁判评分）：交代吕伟的动作编号和裁判给出的高分，用专业数据证明表演的精彩。",
 "这一段简洁有力，\u201c将游泳场的气氛推向了高潮\u201d总结上文观众的热烈反应。\u201c5136\u201d是跳水动作的专业编号（向前翻腾一周半转体三周），体现了新闻的专业性和准确性；\u201c9.5分的高分\u201d用具体分数证明表演的精彩，比空泛的赞美更有说服力。裁判的高分与观众的欢呼相互印证，从专业和大众两个层面肯定了吕伟的表现。",
 [("高潮","比喻事物高度发展的阶段。这里指气氛最热烈的时刻"),("5136","跳水动作编号，指向前翻腾一周半转体三周"),("裁判","体育比赛中负责评判成绩的人员"),("亮出","显示出、展示出。亮，显示"),("高分","很高的分数。跳水满分10分，9.5分是极高的分数")]),

(7, "这位年方16的中国姑娘，赢得了金牌。她的娇小苗条的女伴、17岁的周继红，以接近的分数赢得了银牌。",
 "第七段（比赛结果）：交代吕伟夺得金牌、周继红夺得银牌的比赛结果，点明两人的年龄和体型特征。",
 "这一段交代比赛结果，\u201c年方16\u201d突出吕伟的年轻，\u201c娇小苗条\u201d写她的体型特征（与跳水运动员的体型要求一致）。\u201c她的娇小苗条的女伴、17岁的周继红\u201d用同位语结构介绍银牌得主，\u201c接近的分数\u201d说明两人水平接近，中国跳水队人才济济。这一段简洁明了，是新闻报道中必要的结果交代。",
 [("年方","年龄才。方，才、刚刚"),("娇小苗条","身材小巧纤细。娇小，娇嫩小巧；苗条，细长柔美"),("女伴","女性同伴。伴，同伴"),("周继红","（1965— ）中国女子跳水运动员，1982年亚运会银牌得主，后任中国跳水队领队"),("接近","靠近、相距不远。这里指分数差距很小"),("银牌","体育比赛中第二名获得的奖牌")]),

(8, "当一个印度观众了解到这个姑娘是中国跳水集训队中最年轻的新秀时，惊讶不已。他说：\u201c了不起，你们中国的人才太多了！\u201d",
 "第八段（侧面烘托）：以印度观众的惊讶和赞叹收束全文，从侧面烘托中国跳水事业的人才辈出。",
 "这一段是全文的结尾，以一个印度观众的反应收束，意蕴丰富。\u201c最年轻的新秀\u201d再次强调吕伟的年轻和潜力，\u201c惊讶不已\u201d写印度观众的意外。\u201c了不起，你们中国的人才太多了！\u201d借印度观众之口，赞美中国跳水事业的人才辈出，比作者直接赞美更客观、更有说服力。这个结尾既是对吕伟个人的赞美，也是对中国体育事业的肯定，言有尽而意无穷。",
 [("集训队","集中训练的队伍。集训，集中训练"),("新秀","新出现的优秀人才。秀，特别优异的"),("惊讶不已","惊讶不止。不已，不止、不停"),("了不起","不平凡、（优点）突出。口语，表示赞叹"),("人才","有品德有才能的人或有某种特长的人")]),
]

APP = [
("新闻特写文体特点", [
    ("生动性：细腻描写，如临其境",
     "全文用细腻的笔触描写吕伟跳水的全过程，从起跳的\u201c轻舒双臂\u201d到腾空的\u201c旋风般的空中转体\u201d，再到入水的\u201c哧地插进碧波之中\u201d，每一个动作都写得具体可感。读者仿佛置身于达卡多拉游泳场，亲眼目睹了这1.7秒的精彩瞬间。"),
    ("聚焦性：截取瞬间，放大细节",
     "文章没有泛泛报道整个比赛过程，而是聚焦于吕伟跳水那1.7秒的精彩瞬间，把这一瞬间分解为起跳、腾空、入水三个慢镜头，用大量笔墨细致描写每一个动作细节。这种\u201c以小见大\u201d的聚焦手法，是新闻特写的核心特征。"),
    ("现场感：多角度描写，如见其人",
     "文章从多个角度营造现场感：正面描写吕伟的动作姿态，侧面描写观众的反应（屏息敛声→沸腾欢呼），用外国记者和印度观众的评价烘托，用裁判的9.5分证明。正面与侧面结合，视觉与听觉并用，让读者如临其境、如见其人。"),
    ("真实性：基于事实，不虚构",
     "文章虽然运用了大量文学化的描写手法，但所有内容都基于真实的新闻事实：吕伟确实在1982年新德里亚运会上夺得金牌，动作\u201c5136\u201d确实获得了9.5分，周继红确实获得了银牌。真实是新闻的生命，特写的生动性必须建立在真实性的基础之上。"),
]),
("艺术特色", [
    ("比喻精妙，形象生动",
     "全文运用了大量精妙的比喻：\u201c酷似敦煌壁画中凌空翔舞的\u2018飞天\u2019\u201d写腾空姿态的优美，\u201c旋风般的空中转体\u201d写动作的快速，\u201c疾如流星\u201d写速度之快，\u201c像轻盈的、笔直的箭\u201d写入水的笔直，\u201c自天而降的仙女\u201d写姿态的优美。这些比喻既准确又生动，赋予跳水动作以艺术的美感。"),
    ("拟人传神，赋予情感",
     "\u201c1.7秒的时间对她似乎特别慷慨\u201d把时间拟人化，写时间对吕伟的\u201c偏爱\u201d，更见其技艺高超；\u201c几串白色的气泡拥抱了这位自天而降的仙女\u201d把气泡拟人化，写气泡对吕伟的\u201c拥抱\u201d，极写入水的优美。拟人手法赋予客观事物以人的情感，使描写更加生动传神。"),
    ("动静结合，以静衬动",
     "开头写吕伟\u201c沉静自若\u201d的静态和观众\u201c屏息敛声\u201d的安静，为下文的精彩跳水蓄势；中间写跳水的动态过程，动作快速有力；结尾写\u201c悄然不惊\u201d的水花和观众\u201c沸腾\u201d的欢呼，动静交织。以静衬动，动静结合，使文章节奏起伏有致。"),
    ("侧面烘托，意蕴丰富",
     "文章大量运用侧面烘托手法：观众的\u201c屏息敛声\u201d和\u201c沸腾欢呼\u201d，外国记者的\u201c妙！好极了！\u201d，裁判的9.5分，印度观众的\u201c你们中国的人才太多了\u201d。这些侧面描写从不同角度烘托吕伟表演的精彩，比直接赞美更有说服力，也使文章意蕴更加丰富。"),
]),
("主题思想", [
    ("",
     "这篇新闻特写通过定格1982年新德里亚运会上中国跳水姑娘吕伟夺得女子10米跳台金牌那1.7秒的精彩瞬间，赞美了吕伟高超的跳水技艺和优美的体育姿态，展现了中国跳水运动的高水平和人才辈出的可喜局面，也体现了新闻特写\u201c用文学笔法报道新闻事实\u201d的独特魅力。文章借印度观众之口发出\u201c你们中国的人才太多了\u201d的赞叹，表达了对中国体育事业蓬勃发展的自豪和肯定。"),
]),
]

ACC = [
("重点词语", [
    ("沉静自若","沉着镇定，不慌不忙。自若，不变常态。"),
    ("风度优雅","举止姿态优美高雅。风度，举止姿态。"),
    ("翘首而望","抬起头来望。翘首，抬起头。"),
    ("屏息敛声","暂时抑止呼吸和语声，形容紧张专注。屏，抑止；敛，收束。"),
    ("一刹那","极短的时间。刹，chà。"),
    ("修长","细长。修，长。"),
    ("酷似","极其相似。酷，程度深的。"),
    ("凌空","高高地在空中。凌，升高、在空中。"),
    ("潇洒自如","举止自然大方，不受拘束。潇洒，举止自然大方。"),
    ("从容不迫","非常镇静、不慌不忙的样子。从容，镇静。"),
    ("眼花缭乱","眼睛看见复杂纷繁的东西而感到迷乱。缭乱，纷乱。"),
    ("轻盈","形容女子身材苗条，动作轻快。盈，充满。"),
    ("悄然不惊","寂静无声，没有惊动。悄然，形容寂静无声。"),
    ("沸腾","比喻情绪高涨、场面热烈。"),
    ("如梦初醒","好像刚从梦中醒过来，比喻从糊涂的境地中刚刚醒悟过来。"),
    ("震耳欲聋","耳朵都快震聋了，形容声音很大。欲，将要。"),
    ("由衷","出于本心。衷，内心。"),
    ("新秀","新出现的优秀人才。秀，特别优异的。"),
]),
("用字与读音", [
    ("翘首","（qiáo）抬起头。不读qiào（翘尾巴）。"),
    ("屏息","（bǐng）抑止呼吸。不读píng（屏风）。"),
    ("一刹那","（chà）极短的时间。不读shā（刹车）。"),
    ("酷似","（kù）极其相似。不读gù。"),
    ("凌空","（líng）升高、在空中。不读lín。"),
    ("旋风","（xuàn）螺旋状的疾风。不读xuán（旋转）。"),
    ("悄然","（qiǎo）形容寂静无声。不读qiāo（悄悄）。"),
    ("绷直","（bēng）拉紧伸直。不读běng（绷脸）。"),
]),
("修辞方法", [
    ("比喻","全文大量运用比喻：\u201c酷似敦煌壁画中凌空翔舞的\u2018飞天\u2019\u201d\u201c旋风般的空中转体\u201d\u201c疾如流星\u201d\u201c像轻盈的、笔直的箭\u201d\u201c自天而降的仙女\u201d，比喻精妙，形象生动。"),
    ("拟人","\u201c1.7秒的时间对她似乎特别慷慨\u201d把时间拟人化；\u201c几串白色的气泡拥抱了这位自天而降的仙女\u201d把气泡拟人化，赋予客观事物以人的情感。"),
    ("拟声","\u201c哧\u201d地插进碧波之中\u201d用拟声词写入水的干脆利落，增强现场感。"),
    ("侧面烘托","通过观众的反应、外国记者的赞叹、裁判的高分、印度观众的评价，从侧面烘托吕伟表演的精彩。"),
]),
("写作借鉴", [
    ("慢镜头分解","把1.7秒的跳水动作分解为起跳、腾空、入水三个慢镜头，逐层细致描写，让读者看清每一个动作细节。"),
    ("正面与侧面结合","正面描写吕伟的动作姿态，侧面描写观众、记者、裁判的反应，多角度烘托，比单一的正面描写更有感染力。"),
    ("精妙的比喻","用\u201c飞天\u201d\u201c箭\u201d\u201c流星\u201d等精妙的比喻写跳水动作，既准确又生动，赋予体育动作以艺术的美感。"),
    ("以小见大","聚焦于1.7秒的跳水瞬间，通过这一个\u201c小\u201d场景，展现中国跳水事业的高水平和人才辈出的\u201c大\u201d主题。"),
]),
("文化常识", [
    ("敦煌飞天","敦煌莫高窟壁画中的飞天形象，是佛教中干闼婆和紧那罗的化身，以凌空飞舞、飘逸优美著称，是中国古代艺术的经典形象。"),
    ("跳水动作编号","跳水动作由4位数字组成：第1位指动作方向（1=向前，2=向后，3=反身，4=向内，5=转体），第2位指翻腾周数，第3位指转体周数，第4位指入水姿势。\u201c5136\u201d即向前翻腾一周半转体三周。"),
    ("1982年新德里亚运会","第九届亚洲运动会，1982年11月19日至12月4日在印度新德里举行。中国代表团首次跃居金牌总数第一，共获61枚金牌。"),
    ("吕伟","（1966— ）中国女子跳水运动员，江苏扬州人，1982年新德里亚运会女子10米跳台金牌得主。"),
]),
]

DICT_WORDS = [
    {"w":"翘","py":"qiáo","q":"这是达卡多拉游泳场的8000名观众一齐□首而望","tip":"「翘」羽字旁，抬起；读qiáo不读qiào"},
    {"w":"屏","py":"bǐng","q":"一齐翘首而望、□息敛声的一刹那","tip":"「屏」尸字头，抑止；读bǐng不读píng"},
    {"w":"刹","py":"chà","q":"屏息敛声的一□那","tip":"「刹」立刀旁，极短时间；读chà不读shā"},
    {"w":"酷","py":"kù","q":"衬着蓝天白云，□似敦煌壁画中凌空翔舞的「飞天」","tip":"「酷」酉字旁，程度深；不读gù"},
    {"w":"凌","py":"líng","q":"酷似敦煌壁画中□空翔舞的「飞天」","tip":"「凌」两点水，升高在空中；不读lín"},
    {"w":"潇","py":"xiāo","q":"动作疾如流星，又□洒自如","tip":"「潇」三点水，举止自然大方；与「萧」（草字头）区分"},
    {"w":"绷","py":"bēng","q":"从前伸的手指，一直延续到□直的足尖","tip":"「绷」绞丝旁，拉紧；读bēng不读běng"},
    {"w":"悄","py":"qiǎo","q":"四面水花则□然不惊","tip":"「悄」竖心旁，寂静；读qiǎo不读qiāo"},
    {"w":"腾","py":"téng","q":"这时，整个游泳场都沸□了","tip":"「腾」月字旁，奔跑跳跃；与「滕」（水字旁）区分"},
    {"w":"衷","py":"zhōng","q":"来向他们喜爱的运动员表达由□的赞赏","tip":"「衷」衣字中间，内心；与「哀」（āi）区分"},
]

DICT_NOTES = [
    {"w":"沉静自若","a":"沉着镇定，不慌不忙","q":"她站在10米高台的前沿，沉静自若，风度优雅"},
    {"w":"翘首而望","a":"抬起头来望","q":"8000名观众一齐翘首而望"},
    {"w":"屏息敛声","a":"暂时抑止呼吸和语声，形容紧张专注","q":"一齐翘首而望、屏息敛声的一刹那"},
    {"w":"酷似","a":"极其相似","q":"酷似敦煌壁画中凌空翔舞的「飞天」"},
    {"w":"凌空","a":"高高地在空中","q":"酷似敦煌壁画中凌空翔舞的「飞天」"},
    {"w":"潇洒自如","a":"举止自然大方，不受拘束","q":"动作疾如流星，又潇洒自如"},
    {"w":"从容不迫","a":"非常镇静、不慌不忙的样子","q":"让她从容不迫地展示身体优美的线条"},
    {"w":"眼花缭乱","a":"眼睛看见复杂纷繁的东西而感到迷乱","q":"还没等观众从眼花缭乱中反应过来"},
    {"w":"轻盈","a":"形容女子身材苗条，动作轻快","q":"像轻盈的、笔直的箭"},
    {"w":"悄然不惊","a":"寂静无声，没有惊动","q":"四面水花则悄然不惊"},
    {"w":"沸腾","a":"比喻情绪高涨、场面热烈","q":"整个游泳场都沸腾了"},
    {"w":"如梦初醒","a":"好像刚从梦中醒过来","q":"如梦初醒的观众用震耳欲聋的掌声和欢呼声"},
    {"w":"震耳欲聋","a":"耳朵都快震聋了，形容声音很大","q":"用震耳欲聋的掌声和欢呼声"},
    {"w":"由衷","a":"出于本心","q":"来向他们喜爱的运动员表达由衷的赞赏"},
    {"w":"新秀","a":"新出现的优秀人才","q":"中国跳水集训队中最年轻的新秀"},
]

# ================= 生成 =================
def annotate(text, notes):
    n = len(text); occ = [False] * n; spans = []; terms = []
    for word, note in notes:
        m = re.match(r"^(.*?)[（(]([^）)]*)[）)]$", word)
        if m: w0 = m.group(1); note = "\uff08" + m.group(2) + "\uff09" + note
        else: w0 = word
        terms.append((w0, note))
    for w0, note in sorted(terms, key=lambda x: -len(x[0])):
        if w0 not in text: continue
        start = 0
        while True:
            i = text.find(w0, start)
            if i == -1: break
            if not any(occ[i:i + len(w0)]):
                spans.append((i, i + len(w0), w0, note))
                for k in range(i, i + len(w0)): occ[k] = True
            start = i + len(w0)
    spans.sort(); out, pos = [], 0
    for s, e, w, nt in spans:
        out.append(text[pos:s])
        nt_esc = nt.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
        out.append('<span class="anno-word" data-note="%s">%s</span>' % (nt_esc, w))
        pos = e
    out.append(text[pos:])
    return "".join(out)

def esc(t): return htmlmod.escape(t, quote=True)

jielu = []; fulltext = []
for (no, text, gk, sf, notes) in VERSES:
    fulltext.append('    <div class="pl">%s</div>' % esc(text))
    jielu.append('      <div class="verse" id="l%d" data-i="%d">' % (no, no - 1))
    jielu.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (no, annotate(text, notes)))
    jielu.append('        <details class="v-more"><summary>内容 · 手法</summary><div class="d-body">')
    jielu.append('            <div class="v-sec"><b class="v-label">内容概括</b><div class="v-trans">%s</div></div>' % esc(gk))
    jielu.append('            <div class="v-sec"><b class="v-label">手法分析</b><div class="d-body"><p>%s</p></div></div>' % esc(sf))
    jielu.append('          </div></details></div>')
jielu = "\n".join(jielu); fulltext = "\n".join(fulltext)

lead_html = "\n".join('    <p>%s</p>' % esc(p) for p in LEAD)
author_html = "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px;color:var(--ink2)\"" if i else "", esc(p)) for i, p in enumerate(AUTHOR))
bg_html = "".join('  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' % (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:8px\"" if i else "", esc(par)) for i, par in enumerate(paras))) for (title, paras) in BG)
media_html = "".join('      <div class="media">\n        <h4>%s</h4>\n        <iframe id="%s" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>\n        <a href="%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="%s">全屏播放</button>\n      </div>' % (esc(title), fid, bvid, esc(title), url, fid) for (title, bvid, url, fid) in VIDEOS)
app_html = "".join('  <div class="box">\n    <h3>%s</h3>\n    <div class="fame">\n%s\n    </div>\n  </div>\n' % (esc(title), "\n".join('      <div class="fame-card">\n        <div class="f-line">%s</div>\n        <p>%s</p>\n      </div>' % (esc(ft), esc(pc)) for (ft, pc) in items if title != "主题思想")) for (title, items) in APP if title != "主题思想")
theme_html = "".join('  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' % (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px\"" if i else "", esc(pc)) for i, (ft, pc) in enumerate(items))) for (title, items) in APP if title == "主题思想")
acc_html = "".join('  <div class="box">\n    <div class="acc-cat">\n      <h3>%s</h3>\n%s\n    </div>\n  </div>\n' % (esc(title), "\n".join('      <div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>' % (esc(w), esc(d)) for (w, d) in items)) for (title, items) in ACC)

hero = '<header class="hero">\n  <div class="hero-side">%s</div>\n  <h1 class="hero-title">%s</h1>\n</header>' % (H, TITLE)
nav = '''<nav class="nav"><div class="nav-in"><a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a><div class="tool"><select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option></select><button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button></div></div></nav>'''

main = '''<main class="wrap">
<section id="bg" class="sec"><div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div><div class="lead">%s</div><div class="box"><h3>作者简介</h3>%s</div>%s<div class="box media-box"><h3>视听</h3><div class="media-grid">%s</div></div></section>
<div class="divider"></div>
<section id="jielu" class="sec"><div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 特写镜头 · 细节描写</span></div><button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button><div id="fulltext" class="poem" style="display:none">%s</div><div class="verse-list" id="verseList">%s</div></section>
<div class="divider"></div>
<section id="app" class="sec"><div class="sec-head"><h2>赏 析</h2><span class="no">文体 · 艺术 · 主题</span></div>%s%s</section>
<div class="divider"></div>
<section id="acc" class="sec"><div class="sec-head"><h2>积 累</h2><span class="no">词语 · 用字 · 修辞 · 写法 · 常识</span></div>%s</section>
<div class="divider"></div>
<section id="practice" class="sec"><div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div><div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div><div class="ptools"><button data-mode="word" data-rand="5">随机五组字形</button><button data-mode="word" data-all="1">全部字形</button><button data-mode="note" data-rand="5">随机五组词语</button><button data-mode="note" data-all="1">全部词语</button></div></section>
<footer><div class="kai">\u201c飞天\u201d凌空</div><div>夏浩然 · 新闻特写 · 1982年11月</div></footer>
</main>''' % (lead_html, author_html, bg_html, media_html, fulltext, jielu, app_html, theme_html, acc_html)

tail = '''<button class="top-btn" id="topBtn" title="回到顶部">↑</button><div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div><div class="dictate" id="dictate" hidden><div class="dictate-top"><span class="dictate-mode" id="dictMode">字形听写</span><span class="dictate-progress" id="dictProgress">第 1 / 5 题</span><button class="dictate-fs" id="dictFsMinus">A−</button><button class="dictate-fs" id="dictFsPlus">A+</button><button class="dictate-exit" id="dictExit">退出</button></div><div class="dictate-card"><div class="dictate-py" id="dictPy"></div><div class="dictate-line" id="dictLine"></div><div class="dictate-hint" id="dictHint"></div><div class="dictate-ans" id="dictAnsBox" hidden><div class="dictate-word" id="dictWord"></div><div class="dictate-tip" id="dictTip"></div></div></div><div class="dictate-actions"><button id="dictPrev">上一题</button><button class="primary" id="dictShow">显示答案</button><button id="dictNext">下一题</button></div></div>'''

dict_js = "var DICT_WORDS = %s;\nvar DICT_NOTES = %s;\n" % (json.dumps(DICT_WORDS, ensure_ascii=False), json.dumps(DICT_NOTES, ensure_ascii=False))
html = '''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>\u201c飞天\u201d凌空 夏浩然</title><style>%s</style></head><body data-fs="100">%s%s%s%s<script>%s</script><script>%s</script></body></html>''' % (css, hero, nav, main, tail, main_js, dict_js)

open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, len(html), "chars")
print("verses:", len(VERSES), "word dict:", len(DICT_WORDS), "note dict:", len(DICT_NOTES))
