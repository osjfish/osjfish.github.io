# -*- coding: utf-8 -*-
"“”生成《蚊子和狮子》课件 HTML（伊索寓言，短篇）“”"
import json, re, html as htmlmod

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\wenziheshizi-yisuoyuyan.html"

src = open(TEMPLATE, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
css += "\n  .acc-sub{font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:8px;color:var(--teal-deep);margin:14px 0 6px;font-size:calc(16px*var(--fs))}\n"
mains = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = mains[0].replace("beiying_fs", "wenzi_fs")

H = "古希腊·伊索"
TITLE = "蚊子和狮子"

LEAD = [
    "《蚊子和狮子》选自《伊索寓言》，是一篇短小精悍的寓言故事。蚊子向狮子发起挑战，它利用自己体型小、灵活的优势，专咬狮子鼻子周围没有毛的地方，狮子气得用爪子把自己的脸都抓破了，蚊子战胜了狮子。然而，蚊子在得意忘形地飞走时，却被蜘蛛网粘住了，将要被吃掉时才叹息自己同最强大的动物都较量过，不料被这小小的蜘蛛消灭了。故事告诉我们：不要因为一时的胜利而骄傲自满，骄兵必败。",
    "本文是统编版七年级上册第六单元的教读课文，与《赫耳墨斯和雕像者》同属《寓言四则》。学习时要把握寓言篇幅短小、寓意深刻的特点，通过蚊子的语言和动作描写分析其形象变化，理解故事的寓意。",
]

AUTHOR = [
    "伊索（约公元前6世纪），古希腊著名的寓言家。据传说，伊索原是萨摩斯岛的奴隶，因才智出众被主人释放为自由民，后游历希腊各地，讲述寓言故事。公元前5世纪末，“伊索”这个名字已为古希腊人所熟知，人们把古希腊寓言都归在他的名下。",
    "《伊索寓言》相传为伊索所著，实际是古希腊人在相当长的历史时期内的集体创作，经后人整理汇编而成。全书共收录寓言300余则，大多以动物为主人公，采用拟人化手法，用简短的故事揭示深刻的道理，语言精练，寓意深刻，对后世欧洲寓言创作产生了深远影响。名篇有《狐狸和葡萄》《农夫和蛇》《龟兔赛跑》《赫耳墨斯和雕像者》等。",
]

BG = [
    ("寓言知识", [
        "寓言是文学作品的一种体裁，以比喻性的故事寄寓意味深长的道理，给人以启示。寓言早在我国春秋战国时代就已经盛行，诸子百家的著作中都有不少优秀寓言流传下来。在国外，古希腊的《伊索寓言》是最著名的寓言集。",
        "寓言的基本特征：①篇幅短小，语言精练；②主人公可以是人，也可以是拟人化的动植物或其他事物；③多用夸张、拟人、比喻等手法；④具有鲜明的哲理性和讽刺性，故事背后蕴含深刻的道理。",
        "《蚊子和狮子》是《伊索寓言》中的名篇，以动物为主人公，通过拟人化的手法，讲述了蚊子战胜狮子却被蜘蛛消灭的故事，讽刺了那些骄傲自满、得意忘形的人。故事短小精悍，寓意深刻，是寓言的典范之作。",
    ]),
    ("狮子与蚊子的象征意义", [
        "在古希腊文化和世界各民族的文化中，狮子通常是力量、威严、勇猛的象征，被称为“百兽之王”。狮子体型庞大，力量惊人，是动物世界中的强者。而蚊子则是渺小、微弱的代表，体型微小，力量有限，是动物世界中的弱者。",
        "故事中，蚊子挑战狮子并战而胜之，说明弱者只要善于利用自己的优势，也能战胜强者；但蚊子战胜狮子后却被蜘蛛消灭，说明骄傲自满会导致失败。狮子和蚊子的形象具有强烈的对比意义，使故事的寓意更加鲜明。",
    ]),
]

VIDEOS = [
    ("课文朗读《蚊子和狮子》",
     "BV1sn3q6CEZq",
     "https://www.bilibili.com/video/BV1sn3q6CEZq",
     "mediaF1"),
    ("伊索寓言《蚊子和狮子》",
     "BV1XLVH6UEak",
     "https://www.bilibili.com/video/BV1XLVH6UEak",
     "mediaF2"),
]

VERSES = [
("", "全文解读", "全文",
 "蚊子挑战狮子并战而胜之，却在得意忘形时被蜘蛛网粘住，讽刺了骄傲自满的人。",
 [
(1, "蚊子飞到狮子面前，对他说：“我不怕你，你并不比我强。要说不是这样，你到底有什么力量呢？是用爪子抓，牙齿咬吗？女人同男人打架，也会这么干。我比你强得多。你要是愿意，我们来较量较量吧！”",
 "蚊子飞到狮子面前，发表了一通挑战宣言，表示自己不怕狮子，认为自己比狮子强得多，要求与狮子较量。",
 "开篇即写蚊子的挑战宣言，语言极有个性。“我不怕你，你并不比我强”——开门见山，态度傲慢；“你到底有什么力量呢？是用爪子抓，牙齿咬吗？”——用反问句质疑狮子的力量，语气轻蔑；“女人同男人打架，也会这么干”——把狮子的攻击方式比作女人打架，极尽嘲讽之能事；“我比你强得多”——自我膨胀到极点；“我们来较量较量吧”——主动挑战。整段话连用反问、对比，语气咄咄逼人，一个骄傲自大、目中无人的蚊子形象跃然纸上。",
 [("较量","（jiào liàng）用竞赛或斗争的方式比本领、实力的高低。较，比较"),("爪子","（zhuǎ zi）动物的有尖甲的脚。爪，读zhuǎ，不读zhǎo"),("牙齿","人和高等动物用于咀嚼食物的器官。牙，咀嚼器官"),("强","（qiáng）力量大、势力大（与“弱”相对）")]),
(2, "蚊子吹着喇叭冲过去，专咬狮子鼻子周围没有毛的地方。",
 "蚊子吹着喇叭冲过去，专咬狮子鼻子周围没有毛的地方。",
 "动作描写。“吹着喇叭”——蚊子飞行时发出嗡嗡声，作者用“吹着喇叭”来形容，既写出了蚊子的声音，又写出了它得意洋洋、耀武扬威的神态；“冲过去”——速度快、气势猛，写出了蚊子的勇敢和自信；“专咬狮子鼻子周围没有毛的地方”——蚊子很聪明，它知道狮子的弱点在哪里，专挑没有毛保护的地方咬，这是以己之长攻彼之短。“专”字写出蚊子的精准和狡猾。",
 [("喇叭","（lǎ ba）管乐器，这里比喻蚊子飞行时发出的嗡嗡声。喇，读lǎ"),("冲","（chōng）快速向前闯。冲，读chōng，不读chòng"),("鼻子","人和高等动物的嗅觉器官。鼻，嗅觉器官"),("周围","环绕着中心的部分。周，环绕")]),
(3, "狮子气得用爪子把自己的脸都抓破了。",
 "狮子气得用爪子把自己的脸都抓破了。",
 "侧面描写，写狮子的反应。“气得”——狮子被蚊子激怒了，但又无可奈何；“用爪子把自己的脸都抓破了”——狮子想抓蚊子，却抓不到，反而把自己的脸抓破了。“都”字写出狮子抓得很狠，也写出它的愤怒和无奈。这一句从侧面衬托出蚊子的胜利——狮子虽然强大，却对小小的蚊子束手无策，反而伤了自己。",
 [("爪子","（zhuǎ zi）动物的有尖甲的脚。爪，读zhuǎ"),("抓破","用尖甲划破。破，损坏、使损坏")]),
(4, "蚊子战胜了狮子，又吹着喇叭，唱着凯歌飞走，却被蜘蛛网粘住了。",
 "蚊子战胜了狮子，又吹着喇叭、唱着凯歌得意地飞走，却被蜘蛛网粘住了。",
 "故事的转折。“战胜了狮子”——蚊子确实赢了，这是事实；“又吹着喇叭，唱着凯歌飞走”——“又”字呼应上文的“吹着喇叭”，写出蚊子的得意忘形；“唱着凯歌”比“吹着喇叭”更进一步，蚊子不仅在炫耀，而且在庆祝胜利，骄傲到了极点；“却被蜘蛛网粘住了”——“却”字急转直下，蚊子在最得意的时候遭遇了灭顶之灾。“粘住了”三个字平淡而冷酷，却如同一记警钟，敲响了骄兵必败的警钟。",
 [("战胜","在战争或比赛中取得胜利。胜，胜利"),("凯歌","（kǎi gē）打了胜仗所唱的歌。凯，胜利"),("蜘蛛网","蜘蛛吐丝结成的网，用于捕捉昆虫。蛛，蜘蛛"),("粘住","（zhān zhù）黏的东西附着在物体上。粘，读zhān，不读nián")]),
(5, "蚊子将要被吃掉时，叹息说，自己同最强大的动物都较量过，不料被这小小的蜘蛛消灭了。",
 "蚊子将要被吃掉时叹息说，自己同最强大的动物都较量过，没想到被这小小的蜘蛛消灭了。",
 "蚊子的临终叹息，也是全文的点睛之笔。“将要被吃掉时”——蚊子已经到了生死关头；“叹息说”——“叹息”写出蚊子的悔恨和无奈；“自己同最强大的动物都较量过”——蚊子回顾自己的“辉煌战绩”，它确实战胜了狮子，这是值得骄傲的；“不料被这小小的蜘蛛消灭了”——“不料”写出蚊子的意外和悔恨，“小小的蜘蛛”与“最强大的动物”形成强烈对比，蚊子战胜了强者，却败在了弱者手中。这一声叹息，道尽了骄傲自满者的可悲下场。",
 [("叹息","叹气。叹，叹气"),("较量","（jiào liàng）比本领、实力的高低。较，比较"),("不料","没想到、没有预先料到。料，预料"),("消灭","（xiāo miè）使消灭、除掉。灭，使不存在")]),
(6, "这故事适用于那些打败过大人物，却被小人物打败的人。",
 "点明寓意：故事适用于那些打败过大人物却被小人物打败的人。",
 "独句成段，直接点明寓意。“打败过大人物，却被小人物打败”是对蚊子命运的精准概括，也是故事的教训。“适用于”说明这则寓言具有普遍意义——它不仅适用于蚊子，也适用于所有像蚊子一样骄傲自满、得意忘形的人。寓言的结尾往往直接点明寓意，这是寓言的典型结构。",
 [("打败","战胜、使失败。败，失败"),("大人物","指有地位、有势力的人。这里指狮子"),("小人物","指地位低微、不起眼的人。这里指蜘蛛")]),
]),
]

APP = [
("人物形象", [
("蚊子", "骄傲自大、目中无人、得意忘形，但又聪明勇敢、善于利用优势的形象。挑战狮子时，它“我不怕你，你并不比我强”“我比你强得多”，言语傲慢，目中无人；战斗时，它“专咬狮子鼻子周围没有毛的地方”，聪明地利用自己体型小、灵活的优势，以己之长攻彼之短，确实战胜了狮子；胜利后，它“又吹着喇叭，唱着凯歌飞走”，得意忘形，骄傲到了极点，最终被蜘蛛网粘住。蚊子的形象具有典型意义——它代表了那些取得一点成绩就骄傲自满、忘乎所以的人。"),
("狮子", "强大却笨拙、有勇无谋的形象。狮子是“百兽之王”，体型庞大，力量惊人，但面对小小的蚊子却束手无策——它“用爪子把自己的脸都抓破了”，想抓蚊子却抓不到，反而伤了自己。狮子的形象说明：强者也有弱点，面对弱者的灵活战术，强者也可能失败。狮子的存在是一面镜子，既衬托出蚊子的聪明，也反衬出蚊子的可悲——战胜了强大的狮子，却败在了小小的蜘蛛手中。"),
("蜘蛛", "沉默、耐心、伺机而动的形象。蜘蛛在故事中没有出场，只有“蜘蛛网粘住了”一句，但它的存在至关重要。蜘蛛不与蚊子正面较量，而是结网等待，蚊子自投罗网。蜘蛛的形象说明：真正的胜利者不一定是最强大的，而是最有耐心、最善于等待时机的。蜘蛛与蚊子形成对比——蚊子张扬、骄傲，蜘蛛沉默、耐心，最终沉默者战胜了张扬者。"),
]),
("艺术特色", [
("篇幅短小，寓意深刻", "全文仅200余字，却讲述了一个完整的故事，塑造了鲜明的人物形象，揭示了深刻的道理。这是寓言的典型特征——以极简的篇幅承载极深的寓意。故事按照“挑战→战斗→胜利→得意→覆灭→叹息”的顺序展开，情节跌宕起伏，最后以“被小人物打败”点明寓意，余味无穷。"),
("拟人手法生动形象", "全文采用拟人化手法，赋予蚊子、狮子、蜘蛛以人的思想、语言和行为。蚊子会发表挑战宣言，会“吹着喇叭”“唱着凯歌”，会“叹息”；狮子会“气得”抓破自己的脸。拟人手法使动物形象生动鲜活，也使故事更具感染力和教育意义。"),
("对比手法突出主题", "全文贯穿着对比：蚊子的渺小与狮子的强大的对比；蚊子战胜狮子的辉煌与被蜘蛛消灭的可悲的对比；“最强大的动物”与“小小的蜘蛛”的对比；“打败过大人物”与“被小人物打败”的对比。对比使人物形象更加鲜明，讽刺效果更加强烈，也使寓意更加深刻。"),
("动作描写传神到位", "文中的动作描写极其精练传神。“吹着喇叭冲过去”——写出蚊子的得意和勇猛；“专咬狮子鼻子周围没有毛的地方”——写出蚊子的聪明和精准；“用爪子把自己的脸都抓破了”——写出狮子的愤怒和无奈；“又吹着喇叭，唱着凯歌飞走”——写出蚊子的得意忘形。动作描写虽少，却字字传神。"),
("语言描写个性鲜明", "蚊子的挑战宣言是全文最精彩的语言描写。“我不怕你，你并不比我强”“我比你强得多”“我们来较量较量吧”——连用反问、对比，语气咄咄逼人，一个骄傲自大、目中无人的蚊子形象跃然纸上。语言描写不仅推动了情节发展，也深刻揭示了人物性格。"),
("卒章显志点明寓意", "寓言的典型结构是先讲故事，最后点明寓意。本文结尾“这故事适用于那些打败过大人物，却被小人物打败的人”，直接点明故事的教训。这种卒章显志的写法，使读者在读完故事后立刻明白其中的道理，符合寓言“寓教于乐”的特点。"),
]),
("名句赏析", [
("“我不怕你，你并不比我强。要说不是这样，你到底有什么力量呢？是用爪子抓，牙齿咬吗？女人同男人打架，也会这么干。我比你强得多。”", "蚊子的挑战宣言，是全文最精彩的语言描写。“我不怕你，你并不比我强”——开门见山，态度傲慢；“你到底有什么力量呢？”——用反问句质疑狮子的力量，语气轻蔑；“是用爪子抓，牙齿咬吗？”——列举狮子的攻击方式，暗示这些方式对自己无效；“女人同男人打架，也会这么干”——把狮子的攻击方式比作女人打架，极尽嘲讽之能事；“我比你强得多”——自我膨胀到极点。整段话连用反问、对比，语气咄咄逼人，一个骄傲自大、目中无人的蚊子形象跃然纸上。"),
("“蚊子吹着喇叭冲过去，专咬狮子鼻子周围没有毛的地方。”", "动作描写，写出蚊子的聪明和勇敢。“吹着喇叭”——比喻蚊子飞行时的嗡嗡声，既写出声音，又写出蚊子得意洋洋、耀武扬威的神态；“冲过去”——速度快、气势猛，写出蚊子的勇敢和自信；“专咬狮子鼻子周围没有毛的地方”——蚊子很聪明，它知道狮子的弱点在哪里，专挑没有毛保护的地方咬，这是以己之长攻彼之短。“专”字写出蚊子的精准和狡猾。"),
("“蚊子战胜了狮子，又吹着喇叭，唱着凯歌飞走，却被蜘蛛网粘住了。”", "故事的转折，也是全文最具讽刺力的一句。“战胜了狮子”——蚊子确实赢了；“又吹着喇叭，唱着凯歌飞走”——“又”字呼应上文，写出蚊子的得意忘形，“唱着凯歌”比“吹着喇叭”更进一步，骄傲到了极点；“却被蜘蛛网粘住了”——“却”字急转直下，蚊子在最得意的时候遭遇了灭顶之灾。“粘住了”三个字平淡而冷酷，却如同一记警钟，敲响了骄兵必败的警钟。"),
("“自己同最强大的动物都较量过，不料被这小小的蜘蛛消灭了。”", "蚊子的临终叹息，也是全文的点睛之笔。“同最强大的动物都较量过”——蚊子回顾自己的“辉煌战绩”，它确实战胜了狮子；“不料被这小小的蜘蛛消灭了”——“不料”写出蚊子的意外和悔恨，“小小的蜘蛛”与“最强大的动物”形成强烈对比，蚊子战胜了强者，却败在了弱者手中。这一声叹息，道尽了骄傲自满者的可悲下场。"),
]),
("主题思想", [
("讽刺骄傲自满、得意忘形的人", "文章通过蚊子战胜狮子却被蜘蛛消灭的故事，辛辣地讽刺了那些骄傲自满、得意忘形的人。蚊子战胜了强大的狮子，本是了不起的成就，但它“又吹着喇叭，唱着凯歌飞走”，得意忘形，最终被蜘蛛网粘住。故事告诉我们：骄傲是失败的根源，越是在胜利的时候，越要保持谦虚和警惕。"),
("揭示骄兵必败的道理", "故事深刻揭示了“骄兵必败”的道理。蚊子之所以能战胜狮子，是因为它善于利用自己的优势，以己之长攻彼之短；但它之所以被蜘蛛消灭，是因为它战胜狮子后骄傲自满、放松警惕，最终自投罗网。“骄兵必败”是亘古不变的真理——无论你多么强大，只要骄傲自满，就必然会失败。"),
("说明强者与弱者的辩证关系", "故事还说明了强者与弱者的辩证关系。蚊子是弱者，却战胜了强大的狮子——说明弱者只要善于利用自己的优势，也能战胜强者；蜘蛛比蚊子还弱小，却消灭了蚊子——说明强者也可能败在弱者手中。强与弱不是绝对的，而是相对的、可以转化的。故事提醒我们：不要轻视任何对手，也不要高估自己。"),
("寓言的普遍警示意义", "作为一则寓言，《蚊子和狮子》具有超越时空的普遍意义。它不仅适用于古希腊，也适用于今天；不仅适用于蚊子，也适用于每一个普通人。故事告诫我们：要谦虚谨慎，不要骄傲自满；要居安思危，不要得意忘形；要正确认识自己，不要高估自己的力量。只有保持谦虚和警惕，才能立于不败之地。"),
]),
]

ACC = [
("重点词语", [
("较量", "（jiào liàng）用竞赛或斗争的方式比本领、实力的高低。"),
("爪子", "（zhuǎ zi）动物的有尖甲的脚。"),
("喇叭", "（lǎ ba）管乐器，这里比喻蚊子飞行时发出的嗡嗡声。"),
("冲", "（chōng）快速向前闯。"),
("周围", "环绕着中心的部分。"),
("抓破", "用尖甲划破。"),
("战胜", "在战争或比赛中取得胜利。"),
("凯歌", "（kǎi gē）打了胜仗所唱的歌。"),
("蜘蛛网", "蜘蛛吐丝结成的网，用于捕捉昆虫。"),
("粘住", "（zhān zhù）黏的东西附着在物体上。"),
("叹息", "叹气。"),
("不料", "没想到、没有预先料到。"),
("消灭", "（xiāo miè）使消灭、除掉。"),
]),
("用字与读音", [
("较", "读jiào，不读jiǎo。左右结构，车字旁。“较量”的“较”。"),
("量", "多音字。①liàng：较量、力量。②liáng：测量、丈量。本课“较量”读liàng。"),
("爪", "多音字。①zhuǎ：爪子、鸡爪。②zhǎo：爪牙、张牙舞爪。本课“爪子”读zhuǎ。"),
("喇", "读lǎ，不读lá。左右结构，口字旁。“喇叭”的“喇”。"),
("叭", "读ba（轻声），不读bā。左右结构，口字旁。“喇叭”的“叭”。"),
("冲", "多音字。①chōng：冲锋、冲过去。②chòng：冲床、冲劲儿。本课“冲过去”读chōng。"),
("凯", "读kǎi，不读qǐ。左右结构，几字旁。“凯歌”的“凯”。"),
("蛛", "读zhū，不读zhú。左右结构，虫字旁。“蜘蛛”的“蛛”。"),
("粘", "多音字。①zhān：粘住、粘贴。②nián：同“黏”，粘液。本课“粘住”读zhān。"),
("叹", "读tàn，不读tán。左右结构，口字旁。“叹息”的“叹”。"),
("料", "读liào，不读liáo。左右结构，米字旁。“不料”的“料”。"),
("灭", "读miè，不读mié。独体字，火字底。“消灭”的“灭”。"),
]),
("修辞方法", [
("拟人", "全文采用拟人化手法，赋予蚊子、狮子、蜘蛛以人的思想、语言和行为。蚊子会发表挑战宣言，会“吹着喇叭”“唱着凯歌”，会“叹息”；狮子会“气得”抓破自己的脸。拟人手法使动物形象生动鲜活。"),
("对比", "全文贯穿着对比：蚊子的渺小与狮子的强大的对比；蚊子战胜狮子的辉煌与被蜘蛛消灭的可悲的对比；“最强大的动物”与“小小的蜘蛛”的对比；“打败过大人物”与“被小人物打败”的对比。对比使讽刺效果更加强烈。"),
("比喻", "“蚊子吹着喇叭”——把蚊子飞行时的嗡嗡声比作吹喇叭，既写出声音，又写出蚊子得意洋洋的神态。比喻手法使描写更加生动形象。"),
("反复", "文中两次写蚊子“吹着喇叭”——第一次是挑战时，第二次是胜利后。反复手法写出蚊子一贯的骄傲自大，也为下文的覆灭做了铺垫。"),
("反问", "蚊子的挑战宣言中连用反问句：“你到底有什么力量呢？是用爪子抓，牙齿咬吗？”反问句加强了语气，写出蚊子的轻蔑和傲慢。"),
]),
("写作借鉴", [
("用拟人手法塑造动物形象", "本文采用拟人化手法，赋予蚊子、狮子以人的思想、语言和行为，使动物形象生动鲜活。写童话或寓言时，可以运用拟人手法，让动物、植物或无生命的事物说话、做事，使文章更加生动有趣。"),
("用对比手法突出主题", "本文最突出的写法是对比——强与弱的对比、胜与败的对比、大人物与小人物的对比。对比使人物形象更加鲜明，讽刺效果更加强烈。在写作中，可以运用对比手法，突出矛盾，增强表达效果。"),
("用动作和语言描写揭示性格", "本文通过蚊子的语言（挑战宣言）和动作（“吹着喇叭冲过去”“唱着凯歌飞走”），深刻揭示了蚊子骄傲自大、得意忘形的性格特征。写人物时，要善于运用动作和语言描写，让人物“立”起来。"),
("卒章显志点明寓意", "寓言的典型结构是先讲故事，最后点明寓意。本文结尾“这故事适用于那些打败过大人物，却被小人物打败的人”，直接点明故事的教训。写寓言或哲理短文时，可以采用卒章显志的写法，在结尾点明主旨。"),
("情节跌宕起伏引人入胜", "本文情节按照“挑战→战斗→胜利→得意→覆灭→叹息”的顺序展开，跌宕起伏，引人入胜。特别是“却被蜘蛛网粘住了”一句，急转直下，出人意料，使故事更具吸引力。写叙事类文章时，要注意情节的起伏和转折。"),
]),
("文化常识", [
("伊索与《伊索寓言》", "伊索（约公元前6世纪），古希腊寓言家。《伊索寓言》相传为伊索所著，实际是古希腊人集体创作的寓言集，共300余则，大多以动物为主人公，采用拟人化手法，寓意深刻。名篇有《狐狸和葡萄》《农夫和蛇》《龟兔赛跑》等。"),
("寓言的特点", "寓言是文学体裁的一种，以比喻性的故事寄寓意味深长的道理。特点：①篇幅短小，语言精练；②主人公可以是人或拟人化的动植物；③多用夸张、拟人、比喻；④具有哲理性和讽刺性。"),
("狮子的文化象征", "狮子在世界各民族文化中通常是力量、威严、勇猛的象征，被称为“百兽之王”。在古希腊神话中，狮子是英雄赫拉克勒斯的十二项功绩之一（涅墨亚狮子）。狮子的形象常出现在文学、艺术和建筑中。"),
("蜘蛛的文化意象", "蜘蛛在不同文化中有不同的意象。在古希腊神话中，蜘蛛是织布女工阿拉克涅的化身（因与雅典娜比赛织布而被变成蜘蛛）。在许多文化中，蜘蛛象征着耐心、智慧和创造力，也象征着陷阱和危险。"),
]),
]

DICT_WORDS = [
 {"w":"较量较量","py":"jiào liàng jiào liàng","q":"我们来□□□□吧！","tip":"「较」车字旁读jiào；「量」日字底读liàng；叠词整体作答"},
 {"w":"爪","py":"zhuǎ","q":"是用□子抓，牙齿咬吗？","tip":"「爪」读zhuǎ（爪子），不读zhǎo（爪牙）；动物的有尖甲的脚"},
 {"w":"喇","py":"lǎ","q":"蚊子吹着□叭冲过去","tip":"「喇」口字旁，读lǎ，不读lá；「喇叭」"},
 {"w":"叭","py":"ba","q":"蚊子吹着喇□冲过去","tip":"「叭」口字旁，读ba（轻声）；「喇叭」"},
 {"w":"冲","py":"chōng","q":"蚊子吹着喇叭□过去","tip":"「冲」两点水，读chōng（冲锋），不读chòng（冲床）"},
 {"w":"鼻","py":"bí","q":"专咬狮子□子周围没有毛的地方","tip":"「鼻」自字底，读bí；嗅觉器官"},
 {"w":"围","py":"wéi","q":"专咬狮子鼻子周□没有毛的地方","tip":"「围」口字框，读wéi；环绕"},
 {"w":"抓","py":"zhuā","q":"狮子气得用爪子把自己的脸都□破了","tip":"「抓」提手旁，读zhuā；用手或爪取物"},
 {"w":"破","py":"pò","q":"狮子气得用爪子把自己的脸都抓□了","tip":"「破」石字旁，读pò；损坏"},
 {"w":"凯","py":"kǎi","q":"唱着□歌飞走","tip":"「凯」几字旁，读kǎi，不读qǐ；胜利"},
 {"w":"歌","py":"gē","q":"唱着凯□飞走","tip":"「歌」欠字旁，读gē；歌唱"},
 {"w":"蛛","py":"zhū","q":"却被蜘□网粘住了","tip":"「蛛」虫字旁，读zhū，不读zhú；蜘蛛"},
 {"w":"网","py":"wǎng","q":"却被蜘蛛□粘住了","tip":"「网」同字框，读wǎng；捕鱼捉鸟的器具"},
 {"w":"粘","py":"zhān","q":"却被蜘蛛网□住了","tip":"「粘」米字旁，读zhān（粘住），不读nián（粘液）"},
 {"w":"叹","py":"tàn","q":"蚊子将要被吃掉时，□息说","tip":"「叹」口字旁，读tàn，不读tán；叹气"},
 {"w":"息","py":"xī","q":"蚊子将要被吃掉时，叹□说","tip":"「息」心字底，读xī；呼吸时进出的气"},
 {"w":"料","py":"liào","q":"不□被这小小的蜘蛛消灭了","tip":"「料」米字旁，读liào，不读liáo；预料"},
 {"w":"灭","py":"miè","q":"不料被这小小的蜘蛛消□了","tip":"「灭」火字底，读miè，不读mié；使不存在"},
]

DICT_NOTES = [
 {"w":"较量","a":"用竞赛或斗争的方式比本领、实力的高低","q":"我们来较量较量吧"},
 {"w":"爪子","a":"动物的有尖甲的脚","q":"是用爪子抓，牙齿咬吗"},
 {"w":"喇叭","a":"管乐器，这里比喻蚊子飞行时发出的嗡嗡声","q":"蚊子吹着喇叭冲过去"},
 {"w":"冲","a":"快速向前闯","q":"蚊子吹着喇叭冲过去"},
 {"w":"周围","a":"环绕着中心的部分","q":"专咬狮子鼻子周围没有毛的地方"},
 {"w":"抓破","a":"用尖甲划破","q":"狮子气得用爪子把自己的脸都抓破了"},
 {"w":"战胜","a":"在战争或比赛中取得胜利","q":"蚊子战胜了狮子"},
 {"w":"凯歌","a":"打了胜仗所唱的歌","q":"唱着凯歌飞走"},
 {"w":"蜘蛛网","a":"蜘蛛吐丝结成的网，用于捕捉昆虫","q":"却被蜘蛛网粘住了"},
 {"w":"粘住","a":"黏的东西附着在物体上","q":"却被蜘蛛网粘住了"},
 {"w":"叹息","a":"叹气","q":"蚊子将要被吃掉时，叹息说"},
 {"w":"不料","a":"没想到、没有预先料到","q":"不料被这小小的蜘蛛消灭了"},
 {"w":"消灭","a":"使消灭、除掉","q":"不料被这小小的蜘蛛消灭了"},
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
  <div class="kai">《蚊子和狮子》</div>
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
<title>《蚊子和狮子》伊索寓言</title>
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
