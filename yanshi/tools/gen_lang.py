# -*- coding: utf-8 -*-
"""生成《狼》课件（文言模式）。自包含脚本。"""
import io, json, re, html

SRC = r"D:\App\Apps\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\lang-pusongling.html"
LS_KEY = "lang_fs"

def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", rep, text)

def plain(text):
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\1", text)

CARDS = [
(1, "一[[屠|宰杀牲畜，这里指屠户，宰杀牲畜卖肉的人]]晚归，担中肉尽，[[止|仅，只]]有剩骨。",
 "一个屠户傍晚回家，担子里的肉卖完了，只剩下骨头。",
 "开篇七个字交代时间、人物、事件，干净利落。“担中肉尽，止有剩骨”看似闲笔，实为全文伏笔——肉尽骨存，才有下文投骨之举，也才有两狼尾随之危。危局自平淡中悄然铺开。",
 ["伏笔", "叙事简洁"]),
(1, "途中两狼，[[缀行|（zhuì）紧跟着走了很远。缀，连接，这里是紧跟的意思]]甚远。",
 "路上遇到了两只狼，紧跟着走了很远。",
 "“缀行甚远”四字写尽狼之阴魂不散：不即不离，尾随不去，觊觎之意已在不言中。屠户担中有骨、夜路无人，两狼的“甚远”一步不落，杀机与悬念同时拉满。",
 ["悬念", "炼字"]),
(2, "屠惧，[[投以骨|把骨头投给狼。以，把]]。一狼得骨[[止|停止]]，一狼仍[[从|跟从]]。",
 "屠户害怕了，把骨头投给狼。一只狼得到骨头停下了，另一只狼仍然跟着。",
 "屠户的第一反应是“惧”，对策是“投骨”——幻想用退让换平安。然而一狼得骨止、一狼仍从：让步只换来片刻喘息，贪婪从不因退让而满足。情节于此初起波澜。",
 ["情节推进", "幻想退让"]),
(2, "​[[复|又]]投之，后狼止而前狼又至。",
 "屠户又拿起一块骨头扔过去，后得到骨头的那只狼停下了，可是先得到骨头的那只狼又跟了上来。",
 "“后狼止而前狼又至”九个字，把狼的轮番紧逼写得历历如绘：骨有限而狼无穷，投骨之策彻底失效。短句急促，正与屠户心中步步加深的慌乱相合。",
 ["细节传神", "情节推进"]),
(2, "骨已尽矣，而两狼之​[[并驱如故|像原来一样一起追赶。并，一起；故，旧，原来]]。",
 "骨头已经扔完了，但是两只狼像原来一样一起追赶。",
 "一个“矣”字，写出屠户走投无路之惊；一个“如故”，写出狼之贪得无厌。至此投骨幻想彻底破灭，矛盾激化到顶点——“惧”而退让的策略宣告破产，为下文屠户的转变蓄足了势。",
 ["虚字传神", "情节推进"]),
(3, "屠大[[窘|（jiǒng）处境困迫，为难]]，恐前后[[受其敌|遭受它们的攻击。敌，攻击]]。​[[顾|回头看]]野有麦场，场主[[积薪|堆积柴草。薪，柴草]]其中，[[苫蔽|（shàn bì）覆盖、遮盖]]成丘。",
 "屠户非常窘迫，恐怕前后一起受到狼的攻击。他看见野地里有一个麦场，场主人把柴草堆在麦场中，覆盖成小山似的。",
 "“大窘”写绝境：前有狼阻，后有狼追。危难中屠户开始动脑——“顾”字是全文转折点：寻场地、找掩护，由被动挨打转向主动求变。人的机智开始出场，与狼的凶残展开正面较量。",
 ["转折", "心理刻画"]),
(3, "屠乃奔倚其下，​[[弛|（chí）解除，卸下]]担持刀。狼不敢前，[[眈眈相向|（dān dān）凶狠注视的样子。形容狼瞪着眼睛逼视屠户]]。",
 "屠户于是跑过去倚靠在柴草堆下面，卸下担子拿起刀。两只狼都不敢向前，瞪眼朝着屠户。",
 "“奔倚”“弛担持刀”三个动作一气呵成，屠户的果决在此立起。刀一出，形势立变——“不敢前”三字写狼之色厉内荏，眈眈相向是虚张声势的僵持。人对狼，从此不再是猎物。",
 ["动作描写", "情节转折"]),
(4, "​[[少时|一会儿]]，一狼​[[径去|径直离开。径，径直]]，其一​[[犬坐于前|像狗一样蹲坐在前面。犬，名词作状语，像狗一样]]。​[[久之|时间长了]]，目似​[[瞑|（míng）闭上眼睛]]，[[意暇甚|神情很悠闲。意，神情；暇，从容、悠闲]]。",
 "过了一会儿，一只狼径直走开了，另一只狼像狗似的蹲坐在前面。时间长了，那只狼的眼睛似乎闭上了，神情很悠闲。",
 "狼的“战术”登场：一狼佯去绕后，一狼假寐诱敌。“目似瞑，意暇甚”把狼的伪装写到入骨——凶残之徒最擅伪装，麻痹对手正是它最后的杀招。表面松懈，实为最凶险的时刻。",
 ["细节描写", "拟人化"]),
(4, "屠​[[暴起|突然。暴，突然]]，以刀劈狼首，又数刀[[毙|杀死]]之。",
 "屠户突然跳起来，用刀劈狼的脑袋，又连砍几刀把狼杀死。",
 "“暴起”二字如惊雷炸响：屠户看清形势，不再迟疑，抢先出手。劈首、补刀，干净利落——从“惧”到“暴起”，屠户完成了由退让者到战斗者的转变。恶狼的伪装在雷霆一击前不堪一击。",
 ["动作描写", "情节高潮"]),
(4, "方欲行，转视积薪后，一狼​[[洞其中|在其中打洞。洞，名词作动词，打洞]]，意将​[[隧入|从通道进入。隧，名词作状语，从通道]]以攻其后也。身已半入，止露​[[尻|（kāo）屁股]]尾。",
 "屠户正想走，转身看柴草堆后面，另一只狼正在柴草堆中打洞，打算从通道进去，来攻击屠户的背后。身子已经钻进去一半，只露出屁股和尾巴。",
 "“转视”一念，救了屠户性命——狼之阴险至此和盘托出：假寐诱敌于前，打洞偷袭于后，前后夹击，用心歹毒。“身已半入，止露尻尾”的画面感极强，惊险之中透着讽刺：机关算尽，正自投罗网。",
 ["悬念", "讽刺"]),
(4, "屠自后断其​[[股|大腿]]，亦毙之。乃悟前狼​[[假寐|假装睡觉。寐，睡觉]]，​[[盖|原来是]]以诱敌。",
 "屠户从后面砍断了狼的大腿，也杀死了它。这才明白前面那只狼假装睡觉，原来是用来诱惑敌方的。",
 "补刀断股，彻底除患。“乃悟”二字轻轻收束一场惊险：前狼假寐、后狼洞入的连环诡计至此全盘揭穿。回头看“目似瞑，意暇甚”的悠闲模样，方知每一分松弛都是杀机——狼性之诈，至此写足。",
 ["情节收束", "结构呼应"]),
(5, "狼亦​[[黠|（xiá）狡猾]]矣，而顷刻两毙，禽兽之​[[变诈|巧变诡诈]]​[[几何|多少，意思是能有多少]]哉？[[止增笑耳|只是增加笑料罢了]]。",
 "狼也够狡猾的了，可是顷刻间两只狼都被杀死，禽兽的诡诈手段能有多少呢？只是给人增加笑料罢了。",
 "卒章显志，由事入理。狼不可谓不黠：缀行、分骨、佯寐、打洞，机关用尽；然而贪与诈在人的警觉与勇毅面前，不过顷刻两毙的笑料。“止增笑耳”四字冷峻幽默——对狼的嘲弄，也是对一切貌似强大的恶势力的宣判。",
 ["卒章显志", "议论"]),
]

PARTS = {
 1:("遇狼 · 悬念初起","第1段","屠户晚归，两狼缀行——故事在平静叙述中埋下杀机。"),
 2:("惧狼 · 退让失利","第2段","投骨退让幻想破灭，两狼并驱如故，矛盾步步升级。"),
 3:("御狼 · 危中求变","第3段","屠户大窘之下倚薪持刀，由被动挨打转为对峙周旋。"),
 4:("杀狼 · 智勇制胜","第4段","识破假寐诱敌、打洞偷袭的诡计，屠户暴起杀狼，前后夹击之局瓦解。"),
 5:("议狼 · 卒章显志","第5段","作者直发议论：狼虽黠，终两毙——点明全文主旨。"),
}

FULLTEXT = [
 "一屠晚归，担中肉尽，止有剩骨。途中两狼，缀行甚远。",
 "屠惧，投以骨。一狼得骨止，一狼仍从。复投之，后狼止而前狼又至。骨已尽矣，而两狼之并驱如故。",
 "屠大窘，恐前后受其敌。顾野有麦场，场主积薪其中，苫蔽成丘。屠乃奔倚其下，弛担持刀。狼不敢前，眈眈相向。",
 "少时，一狼径去，其一犬坐于前。久之，目似瞑，意暇甚。屠暴起，以刀劈狼首，又数刀毙之。方欲行，转视积薪后，一狼洞其中，意将隧入以攻其后也。身已半入，止露尻尾。屠自后断其股，亦毙之。乃悟前狼假寐，盖以诱敌。",
 "狼亦黠矣，而顷刻两毙，禽兽之变诈几何哉？止增笑耳。",
]

WORDS = [
 {"w":"缀","py":"zhuì","q":"途中两狼，□行甚远","tip":"「缀」绞丝旁，连接、紧跟义；勿写「辍」（中止义）"},
 {"w":"窘","py":"jiǒng","q":"屠大□，恐前后受其敌","tip":"「窘」穴字头，处境困迫义，读 jiǒng；勿写「窘」上下颠倒或「窖」"},
 {"w":"薪","py":"xīn","q":"场主积□其中","tip":"「薪」草字头，柴草义；勿写「新」「犁」"},
 {"w":"苫","py":"shàn","q":"场主积薪其中，□蔽成丘","tip":"「苫」草字头，用席、布等遮盖义，此处读 shàn；勿读 zhàn"},
 {"w":"弛","py":"chí","q":"屠乃奔倚其下，□担持刀","tip":"「弛」弓字旁，放松、卸下义；勿写「驰」（奔跑义）"},
 {"w":"眈眈","py":"dān dān","q":"狼不敢前，□□相向","tip":"叠词，凶狠注视的样子；两字均为目字旁，读 dān"},
 {"w":"瞑","py":"míng","q":"目似□，意暇甚","tip":"「瞑」目字旁，闭眼义；勿写「暝」（日落义）、「冥」"},
 {"w":"毙","py":"bì","q":"以刀劈狼首，又数刀□之","tip":"「毙」比字底，杀死义；勿写「弊」「蔽」"},
 {"w":"尻","py":"kāo","q":"身已半入，止露□尾","tip":"「尻」尸字头，屁股义，读 kāo；生僻易错字"},
 {"w":"隧","py":"suì","q":"意将□入以攻其后也","tip":"「隧」左耳旁，从通道进入；勿写「遂」"},
 {"w":"黠","py":"xiá","q":"狼亦□矣，而顷刻两毙","tip":"「黠」犬字旁（反犬旁），狡猾义，读 xiá；勿写「猾」误为全文替字"},
 {"w":"寐","py":"mèi","q":"乃悟前狼假□，盖以诱敌","tip":"「寐」宝盖头，睡觉义；勿写「寤」（醒义）"},
 {"w":"径","py":"jìng","q":"少时，一狼□去","tip":"「径」双人旁（彳），径直义；勿写「经」「轻」"},
]

NOTES = [
 {"w":"屠","a":"宰杀牲畜，这里指屠户，宰杀牲畜卖肉的人","q":"一屠晚归，担中肉尽"},
 {"w":"止有剩骨","a":"只有剩下的骨头。止，仅，只","q":"担中肉尽，止有剩骨"},
 {"w":"缀行甚远","a":"紧跟着走了很远。缀，连接，这里是紧跟的意思","q":"途中两狼，缀行甚远"},
 {"w":"投以骨","a":"把骨头投给狼。以，把","q":"屠惧，投以骨"},
 {"w":"从","a":"跟从","q":"一狼得骨止，一狼仍从"},
 {"w":"复","a":"又","q":"复投之，后狼止而前狼又至"},
 {"w":"并驱如故","a":"像原来一样一起追赶。并，一起；故，旧，原来","q":"骨已尽矣，而两狼之并驱如故"},
 {"w":"窘","a":"处境困迫，为难。读 jiǒng","q":"屠大窘，恐前后受其敌"},
 {"w":"受其敌","a":"遭受它们的攻击。敌，攻击","q":"恐前后受其敌"},
 {"w":"顾","a":"回头看","q":"顾野有麦场"},
 {"w":"积薪","a":"堆积柴草。薪，柴草","q":"场主积薪其中，苫蔽成丘"},
 {"w":"苫蔽","a":"覆盖、遮盖。读 shàn bì","q":"场主积薪其中，苫蔽成丘"},
 {"w":"弛","a":"解除，卸下。读 chí","q":"屠乃奔倚其下，弛担持刀"},
 {"w":"眈眈相向","a":"瞪眼朝着屠户。眈眈，凶狠注视的样子。读 dān dān","q":"狼不敢前，眈眈相向"},
 {"w":"少时","a":"一会儿","q":"少时，一狼径去"},
 {"w":"径去","a":"径直离开。径，径直","q":"少时，一狼径去"},
 {"w":"犬坐于前","a":"像狗一样蹲坐在前面。犬，名词作状语，像狗一样","q":"其一犬坐于前"},
 {"w":"久之","a":"时间长了","q":"久之，目似瞑，意暇甚"},
 {"w":"瞑","a":"闭上眼睛。读 míng","q":"久之，目似瞑，意暇甚"},
 {"w":"意暇甚","a":"神情很悠闲。意，神情；暇，从容、悠闲","q":"久之，目似瞑，意暇甚"},
 {"w":"暴起","a":"突然跳起。暴，突然","q":"屠暴起，以刀劈狼首"},
 {"w":"毙","a":"杀死","q":"以刀劈狼首，又数刀毙之"},
 {"w":"洞其中","a":"在其中（柴草堆中）打洞。洞，名词作动词，打洞","q":"一狼洞其中，意将隧入以攻其后也"},
 {"w":"隧入","a":"从通道进入。隧，名词作状语，从通道","q":"一狼洞其中，意将隧入以攻其后也"},
 {"w":"尻","a":"屁股。读 kāo","q":"身已半入，止露尻尾"},
 {"w":"股","a":"大腿","q":"屠自后断其股，亦毙之"},
 {"w":"假寐","a":"假装睡觉。寐，睡觉","q":"乃悟前狼假寐，盖以诱敌"},
 {"w":"盖","a":"原来是","q":"乃悟前狼假寐，盖以诱敌"},
 {"w":"黠","a":"狡猾。读 xiá","q":"狼亦黠矣，而顷刻两毙"},
 {"w":"顷刻","a":"一会儿","q":"狼亦黠矣，而顷刻两毙"},
 {"w":"变诈","a":"巧变诡诈","q":"禽兽之变诈几何哉？止增笑耳"},
 {"w":"几何","a":"多少，意思是能有多少","q":"禽兽之变诈几何哉？止增笑耳"},
 {"w":"止增笑耳","a":"只是增加笑料罢了。耳，语气词，罢了","q":"禽兽之变诈几何哉？止增笑耳"},
]

BG_LEAD = [
 "《狼》选自《聊斋志异》卷六《狼三则》中的第二则。《狼三则》都以屠户遇狼始、杀狼终，本篇情节最完整、刻画最生动，历来是初中文言文教学的经典篇目。",
 "全文二百余字，却写出了屠户遇狼、惧狼、御狼、杀狼的完整过程，结尾以“狼亦黠矣，而顷刻两毙”点题，借狼喻人，寓意深远。",
]
AUTHOR = [
 "蒲松龄（1640—1715），字留仙，世称聊斋先生，淄川（今山东淄博淄川区）人，清代文学家。早年即有文名，却屡试不第，七十一岁才成岁贡生。一生穷愁潦倒，以教书为业。",
 "蒲松龄数十年间搜集民间奇闻，写成文言短篇小说集《聊斋志异》近五百篇。郭沫若赞其“写鬼写妖高人一等，刺贪刺虐入骨三分”——借花妖狐魅、志怪之谈，写尽人间世相。",
]
STORY = [
 ("科场失意","蒲松龄十九岁应童子试连夺县、府、道三第一，名震一时，此后却屡试屡踬，考到白头仍未中举。科场的黑暗与冷遇，使他对世态炎凉体会极深，讽刺之笔由此练成。"),
 ("聊斋著书","他在乡间设馆教书近四十年，业余摆茶设烟，邀路人谈奇说异，兼采文献，积数十年之功成《聊斋志异》。自序云“集腋成裘，妄续幽冥之录；浮白载笔，仅成孤愤之书”。"),
 ("《狼三则》","《狼三则》皆写屠户与狼，其一写狼随担啖肉，其三写狼穴居入室，本篇为其二。三则均以狼喻恶人，讥其贪诈必败，寄托了作者对世间恶势力的清醒认识。"),
]
VIDEOS = [("《狼》课文朗读（部编七上）","BV1bA411v7jF","【课文朗读】《狼/蒲松龄》古文-部编人教版七年级语文上册"),
          ("蒲松龄《狼》动画演绎","BV16MoNYwEJ5","七年级语文蒲松龄《狼》，动画演绎古诗情节")]

APP_PEOPLE = [
 ("屠户：由怯到勇的强者","屠户的形象有一个清晰的变化轨迹：初遇而“惧”，退让而投骨；骨尽而“大窘”，倚薪持刀对峙；识破诡计而“暴起”，断股毙狼除恶务尽。他不是天生的英雄，而是被贪狼逼出来的战士——恐惧犹在，却终于敢于斗争、善于斗争。这正是全文给读者的启示。"),
 ("两狼：贪婪狡诈的化身","两只狼各有“分工”：一只得骨仍从、并驱如故，写其贪；一只假寐诱敌、打洞袭后，写其诈。它们步步紧逼、机关算尽，却败在最后一口贪念上——作者写狼，实是写人间一切贪而诈的恶人：其行可憎，其败可笑。"),
]
APP_ART = [
 ("情节曲折，张弛有度","遇狼、惧狼、御狼、杀狼、议狼，五段文字层层推进，每一次转折都出人意料：投骨未安、倚薪对峙、假寐诱敌、暴起劈杀——“转视积薪后”一折尤其惊险。二百字小说，有跌宕起伏之妙。"),
 ("动作神态，刻画入神","写屠户，“惧”“投”“顾”“奔倚”“弛”“持”“暴起”“劈”“断”，一连串动词写尽心理与身手；写狼，“缀行”“并驱”“眈眈相向”“目似瞑，意暇甚”，形神毕肖。不重外貌而神态自见，是白描手法的典范。"),
 ("虚实相生，暗藏讽刺","狼之狡计通过屠户“乃悟”才全盘揭晓，读者与屠户同经惊险、同悟真相。“身已半入，止露尻尾”的画面近乎漫画——机关算尽反露破绽，讽刺之意尽在形象之中。"),
 ("卒章显志，画龙点睛","叙事四段不动声色，末段忽然跃出议论：“狼亦黠矣，而顷刻两毙”，以极简之语总束全局；“止增笑耳”冷然一笑，全文题旨和盘托出。叙事与议论的配比，堪称文言短章的教科书。"),
]
APP_FAME = [
 ("其一犬坐于前。久之，目似瞑，意暇甚。","写狼的伪装。“犬坐”状其形，“目似瞑”绘其态，“意暇甚”传其神——三层递进，把一只假寐诱敌的恶狼写活了。越是从容悠闲，越见其险恶用心，为“暴起”一击蓄足张力。"),
 ("屠暴起，以刀劈狼首，又数刀毙之。","全文最见力度的句子。“暴起”写出积蓄已久的爆发，“劈”“毙”斩钉截铁，“又数刀”除恶务尽。短促的节奏与果决的动作相得益彰，屠户性格的转变在此完成。"),
 ("狼亦黠矣，而顷刻两毙，禽兽之变诈几何哉？止增笑耳。","全文警策。“黠”与“毙”对举，狡诈与覆亡只有一步之遥；“几何哉”的反问与“止增笑耳”的冷笑，把对狼的鄙夷推向极处。由狼及人，是一切贪诈之徒的最终判词。"),
]
APP_THEME = [
 "本文讲述屠户路遇两狼、由退让对峙到奋起杀狼的故事，揭示了狼的贪婪、狡诈与凶残，赞颂了屠户的机智勇敢。",
 "故事寄寓深刻：对待像狼一样的恶势力，幻想退让只会助长其气焰；只有敢于斗争、善于斗争，才能取胜。结尾“止增笑耳”的嘲讽，更宣示了这样一个真理——贪诈者纵然机关算尽，终究逃不覆亡的命运。",
]

ACC = [
 ("通假字", [
   ("止","同“只”，仅、只。例：担中肉尽，止有剩骨（教材注：止，仅，只）"),
 ]),
 ("古今异义", [
   ("股","古义：大腿（屠自后断其股）；今义：屁股"),
   ("禽兽","古义：泛指野兽（禽兽之变诈）；今义：鸟兽的统称，多含贬义骂人"),
   ("几何","古义：多少（变诈几何哉）；今义：数学学科名"),
   ("耳","古义：语气词，罢了（止增笑耳）；今义：耳朵"),
 ]),
 ("词类活用", [
   ("洞","名词作动词，打洞。例：一狼洞其中"),
   ("隧","名词作状语，从通道。例：意将隧入以攻其后也"),
   ("犬","名词作状语，像狗一样。例：其一犬坐于前"),
   ("敌","名词作动词，攻击。例：恐前后受其敌"),
 ]),
 ("一词多义", [
   ("止","①仅，只：止有剩骨／止露尻尾；②停止：一狼得骨止"),
   ("意","①神情：意暇甚；②打算：意将隧入以攻其后也"),
   ("前","①上前：狼不敢前；②前面：其一犬坐于前"),
   ("之","①代词，指狼：复投之；②取消句子独立性：两狼之并驱如故／禽兽之变诈几何哉；③音节助词，无实义：久之"),
   ("以","①把：投以骨；②用来：意将隧入以攻其后也"),
 ]),
 ("文化常识", [
   ("《聊斋志异》","蒲松龄著文言短篇小说集，近五百篇。借花妖狐魅故事反映社会现实，被誉为中国文言短篇小说的巅峰。"),
   ("狼三则","《聊斋志异》中三则屠户杀狼故事的合称，本文为第二则。三则均借狼喻恶，结尾皆有“止增笑耳”式的议论。"),
   ("聊斋先生","蒲松龄的世称，因其书斋名“聊斋”而得名。"),
   ("蒲松龄自勉联","“有志者，事竟成，破釜沉舟，百二秦关终属楚；苦心人，天不负，卧薪尝胆，三千越甲可吞吴。”可见其屡败屡试的坚韧。"),
 ]),
]

# ================= 组装 =================
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]
main_js, dict_js = re.findall(r"<script>\n(.*?)</script>", src, re.S)
main_js = main_js.replace("beiying_fs", LS_KEY)
dict_js = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", dict_js, flags=re.S)
dict_js = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", dict_js, flags=re.S)

CN = "一二三四五"
hero = '<header class="hero">\n  <div class="hero-side">清代 · 蒲松龄</div>\n  <h1 class="hero-title">狼</h1>\n</header>'
nav = '<nav class="nav"><div class="nav-in"><a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a><div class="tool"><select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option></select><button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button></div></div></nav>'

def video(i, h4, bvid, atitle):
    return ('<div class="media"><h4>%s</h4>'
            '<iframe id="mediaF%d" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>'
            '<a href="https://www.bilibili.com/video/%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF%d">全屏播放</button></div>'
            % (h4, i, bvid, atitle, bvid, i))

bg = ['<main class="wrap">', '<section id="bg" class="sec">',
      '<div class="sec-head"><h2>背 景</h2><span class="no">作者 · 典籍 · 缘起</span></div>', '<div class="lead">']
for p in BG_LEAD: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>作者简介</h3>')
for p in AUTHOR: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>写作背景</h3>')
for t, p in STORY: bg.append('<p><b>' + t + '：</b>' + p + '</p>')
bg.append('</div><div class="box media-box"><h3>视听</h3><div class="media-grid">')
for i, (h4, bvid, at) in enumerate(VIDEOS): bg.append(video(i + 1, h4, bvid, at))
bg.append('</div></div></section>')

jl = ['<div class="divider"></div>', '<section id="jielu" class="sec">',
      '<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>',
      '<div class="sec-sub">全文按遇狼、惧狼、御狼、杀狼、议狼分五部分。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>',
      '<button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>',
      '<div id="fulltext" class="poem" style="display:none">']
for p in FULLTEXT: jl.append('<div class="pl">' + p + '</div>')
jl.append('</div><div class="verse-list" id="verseList">')
cur = 0
n = 0
for (part, txt, yi, shang, tags) in CARDS:
    if part != cur:
        cur = part
        t, rng, ov = PARTS[part]
        jl.append('<div class="part-head"><span class="p-num">第%s部分</span><h3>%s</h3><span class="range">%s</span></div>' % (CN[part - 1], t, rng))
        jl.append('<div class="part-overview">%s</div>' % ov)
    n += 1
    tag_html = ''.join('<span>%s</span>' % t for t in tags)
    jl.append('<div class="verse" id="l%d" data-i="%d">\n  <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>\n  <details class="v-more">\n    <summary>译文 · 赏析</summary>\n    <div class="d-body">\n      <div class="v-sec"><b class="v-label">译　文</b>\n        <div class="v-trans">%s</div>\n      </div>\n      <div class="v-sec"><b class="v-label">赏　析</b>\n        <div class="d-body"><p>%s</p></div>\n      </div>\n      <div class="tags">%s</div>\n    </div>\n  </details>\n</div>' % (n, n - 1, n, annotate(txt), yi, shang, tag_html))
jl.append('</div></section>')

app = ['<div class="divider"></div>', '<section id="app" class="sec">',
       '<div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>',
       '<div class="box"><h3>形象赏析</h3><p style="margin-bottom:14px;color:var(--ink2)">一怯一勇的屠户与两贪两诈的狼，构成了这篇微型小说的全部戏剧张力。</p><div class="fame">']
for t, p in APP_PEOPLE: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>艺术特色</h3><div class="fame">')
for t, p in APP_ART: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>名句赏析</h3><div class="fame">')
for t, p in APP_FAME: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>主题思想</h3>')
for p in APP_THEME: app.append('<p>' + p + '</p>')
app.append('</div></section>')

acc = ['<div class="divider"></div>', '<section id="acc" class="sec">',
       '<div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 词类活用 · 一词多义 · 文化常识</span></div>']
for cat, items in ACC:
    acc.append('<div class="box"><div class="acc-cat"><h3>%s</h3>' % cat)
    for w, d in items:
        acc.append('<div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>' % (w, d))
    acc.append('</div></div>')
acc.append('</section>')

practice = ['<div class="divider"></div>', '<section id="practice" class="sec">',
            '<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>',
            '<div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>',
            '<div class="ptools"><button data-mode="word" data-rand="5">随机五组字形</button><button data-mode="word" data-all="1">全部字形</button><button data-mode="note" data-rand="5">随机五组注释</button><button data-mode="note" data-all="1">全部注释</button></div></section>']
footer = '<footer>\n  <div class="kai">《狼》</div>\n  <div>蒲松龄 · 清（1640—1715）· 选自《聊斋志异·狼三则》其二</div>\n</footer>'
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

html_doc = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>《狼》蒲松龄</title>\n<style>' + css + '</style>\n</head>\n<body data-fs="100">\n\n'
        + hero + '\n\n' + nav + '\n\n' + "\n".join(bg) + '\n\n' + "\n".join(jl) + '\n\n' + "\n".join(app) + '\n\n' + "\n".join(acc) + '\n\n' + "\n".join(practice) + '\n\n'
        + footer + '\n</main>\n\n' + tail + '\n<script>\n' + main_js + '</script>\n<script>\n' + dict_js + '</script>\n\n</body>\n</html>\n')

# ================= 自检 =================
no_script = re.sub(r"<script>.*?</script>", "", html_doc, flags=re.S)
body_text = re.sub(r"<[^>]+>", "", re.sub(r"<style>.*?</style>", "", no_script, flags=re.S))
assert body_text.count('"') == 0, "straight quotes in visible text"
need = ["verseList", "fulltext", "btnAll", "btnRecite", "btnPrint", "btnShowAll", "fsSel", "annoPopup", "dictate", "topBtn", "mediaF1", "mediaF2"]
missing = [i for i in need if 'id="%s"' % i not in html_doc]
assert not missing, "missing ids: %s" % missing
assert LS_KEY in main_js and "beiying_fs" not in main_js and "beiying" not in dict_js
per_card = re.findall(r'<div class="verse".*?<div class="v-line">(.*?)</div></div>', html_doc, re.S)
empty = [i + 1 for i, o in enumerate(per_card) if "anno-word" not in o]
assert not empty, "cards without annotation: %s" % empty
for it in WORDS:
    assert not any(c in it["q"] for c in it["w"]), "leak: %s" % it["w"]
    assert it["q"].count("□") == len(it["w"]), "box mismatch: %s" % it["w"]
    assert it["py"] and it["tip"] and it["tip"] != it["w"], "tip bad: %s" % it["w"]
import difflib
card_stream = "".join(plain(t) for (_, t, _, _, _) in CARDS).replace("​", "")
full_stream = "".join(FULLTEXT)
norm = lambda s: re.sub(r"\s+", "", s)
if norm(card_stream) != norm(full_stream):
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, norm(card_stream), norm(full_stream)).get_opcodes():
        if op != "equal":
            print("DIFF", op, repr(norm(card_stream)[a1:a2]), "!=", repr(norm(full_stream)[b1:b2]))
    raise SystemExit("fulltext/card stream mismatch")
print("狼 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), html_doc.count('class="anno-word"'), len(WORDS), len(NOTES), len(html_doc.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html_doc)
print("OK ->", OUT)
