# -*- coding: utf-8 -*-
"""生成《三峡》课件（文言模式：原文注释+译文+赏析）。自包含脚本。"""
import io, json, re, html

SRC = r"D:\App\Apps\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\sanxia-lidaoyuan.html"
LS_KEY = "sanxia_fs"

def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", rep, text)

def plain(text):
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\1", text)

CARDS = [
(1, "[[自|在，从]][[三峡|瞿塘峡、巫峡和西陵峡的合称，在长江上游重庆奉节和湖北宜昌之间，七百里约合今二百余里]]七百里中，两岸连山，[[略无|完全没有]]​[[阙|同“缺”，空隙、缺口]]处。",
 "在三峡七百里当中，两岸都是连绵的高山，几乎没有中断的地方。",
 "总写三峡之山。起笔便交代三峡之长，​“两岸连山，略无阙处”八字写尽群山绵延不断、山多崖陡的雄浑气势——不是一座山，而是七百里连成一体的山墙，仰视不见缺口，为下文“隐天蔽日”蓄势。",
 ["总写", "正面描写"]),
(1, "[[重岩叠嶂|（zhàng）重叠的山岩、像屏障一样的山峰。嶂，直立如屏障的山峰]]，[[隐天蔽日|遮蔽了天空和太阳]]，",
 "层层的悬崖，排排的峭壁，把天空和太阳都遮蔽了。",
 "承“连山”而作工笔细描：岩是重岩，嶂是叠嶂，山之多且高不言自明。“隐天蔽日”以天日之失侧写山势之峻，是典型的侧面烘托——山高到什么程度？高到把日月都藏了起来。",
 ["侧面烘托", "炼字"]),
(1, "[[自非|如果不是。自，如果]]​[[亭午|正午]]​[[夜分|半夜]]，不见[[曦|（xī）日光，这里指太阳]]月。",
 "如果不是正午和半夜，连太阳和月亮都看不见。",
 "以“不见”反衬，进一步极写山高谷深。正午与半夜，是阳光月光唯一能射进谷底的两个时刻——只有此时才“见”，其余时刻皆“不见”，数量上的极端吝啬，正与山势的极端高峻相称。亦为下文夏水“沿溯阻绝”埋下地理伏笔。",
 ["反衬", "夸张"]),
(2, "至于[[夏水襄陵|夏天江水漫上丘陵。襄，冲上、漫上；陵，大的土山]]，[[沿溯|（sù）顺流而下为沿，逆流而上为溯]]​[[阻绝|阻断，不能通航]]。",
 "到了夏天江水漫上山陵的时候，上行和下行的航路都被阻断。",
 "由山转水，笔锋陡起。“襄陵”写水势之猛——水能漫上山陵，可见水量之丰、水势之暴涨；“阻绝”从船航行之难反衬水大。夏水之险恶与上一部分山之高峻合成三峡的雄奇底色。",
 ["侧面烘托", "过渡"]),
(2, "[[或|有时]][[王命急宣|皇帝的命令要紧急传达。宣，传达]]，有时[[朝发白帝|早晨从白帝城出发。朝，早晨；白帝，城名，在今重庆奉节东白帝山上]]，[[暮到江陵|傍晚就到了江陵。暮，傍晚；江陵，地名，在今湖北荆州]]，其间千二百里，[[虽|即使]]乘[[奔|动词用作名词，指飞奔的马]]​[[御风|驾着风。御，驾御]]，[[不以疾|不如这样快。以，如、及；疾，快]]也。",
 "有时皇帝的命令要紧急传达，这时只要早晨从白帝城出发，傍晚就到了江陵，中间相距一千二百里，即使骑上飞奔的快马，驾着长风，也不如船快。",
 "“或王命急宣”设一特例，引出三峡水路最动人心魄的一面。“朝发白帝，暮到江陵”以时间之短写流速之疾，数字对照（朝暮、千二百里）历历可感；“虽乘奔御风，不以疾也”再以快马疾风作比，层层加码，把水速写到极处。李白“朝辞白帝彩云间，千里江陵一日还”即化用此意。",
 ["数字对照", "衬托", "名句"]),
(3, "春冬之时，则[[素湍|（tuān）白色的急流。湍，急流的水]]​[[绿潭|碧绿的深水]]，[[回清|回旋的清波]]​[[倒影|倒映着各种景物的影子]]，",
 "在春冬时节，就有白色的急流、碧绿的深潭，回旋着清波，倒映着各种景物的影子。",
 "笔调一转，夏之奔放换作春冬之清幽。“素”“绿”设色素净明快，“回清倒影”一句两景：俯看回旋的清波，仰看山物倒影，动静相映，上下辉映，峡江如镜。写景由平面而立体，最见静美。",
 ["设色", "动静结合", "名句"]),
(3, "[[绝巘|（yǎn）极高的山峰。巘，山峰]]多生[[怪柏|姿态怪异的柏树]]，[[悬泉|从山崖流下的悬挂着的泉水]]瀑布，[[飞漱|（shù）飞速地冲荡]]其间，",
 "极高的山峰上多生长着姿态怪异的柏树，悬泉和瀑布在那里飞速地冲荡。",
 "“怪柏”写静态之奇——悬崖绝壁之上柏树竟能扎根生长，姿态各异，见造化之奇与生命之强；“飞漱”写动态之美——泉瀑自天而落，冲荡其间。一静一动，一坚劲一飞动，山之骨、水之魂俱出。",
 ["动静结合", "炼字"]),
(3, "[[清荣峻茂|水清、树荣、山高、草盛]]，[[良|甚，很]]多趣味。",
 "水清、树荣、山高、草盛，实在有很多趣味。",
 "仅四字便总括春冬景物：分承前文——水“清”（回清）、树“荣”（怪柏）、山“峻”（绝巘）、草“茂”，一字一景，高度浓缩，堪称全文炼字之最。末以“良多趣味”直抒赞叹，情与景合。",
 ["炼字", "总括"]),
(4, "每至[[晴初|天刚放晴]]​[[霜旦|下霜的早晨]]，[[林寒涧肃|树林和山涧显出一片清凉和寂静。肃，肃杀、凄寒]]，",
 "每到天刚放晴的时候或下霜的早晨，树林和山涧显出一片清凉和寂静。",
 "写秋峡先设时间——晴初霜旦，秋意最浓的时刻；“林寒涧肃”四字以寒、肃写秋之清冷萧瑟，与夏之壮、春冬之秀迥然别开一境。水枯涧空，林森气寒，猿声将有处所。",
 ["意境", "炼字"]),
(4, "常有高猿长啸，[[属引|（zhǔ yǐn）声音持续不断。属，连接；引，延长]]​[[凄异|凄凉怪异]]，[[空谷传响|空荡的山谷里传来猿啼的回声。响，回声]]，[[哀转|声音悲凉婉转。转，同“啭”]]​[[久绝|很久才消失]]。",
 "常常有高处的猿猴放声长啸，声音持续不断，异常凄凉，空荡的山谷里传来猿啼的回声，悲哀婉转，很久才消失。",
 "以声写秋，是全文最富情味的一笔。“属引凄异”写啸声之长之哀，“空谷传响，哀转久绝”写余音在山谷间的往复回荡——山愈高谷愈空，声愈久哀愈深。至此，猿声、谷响与秋意融为一体，萧瑟之情弥漫纸面。",
 ["以声写景", "名句"]),
(4, "[[故渔者歌曰|所以打鱼的人唱道。渔者，打鱼的人]]：“[[巴东|地名，今重庆东部云阳、奉节、巫山一带]]三峡巫峡长，猿鸣三声泪[[沾|沾湿]]​[[裳|（cháng）古时下裙，这里泛指衣服]]。”",
 "所以打鱼的人唱歌道：“巴东三峡巫峡长，猿鸣三声泪沾裳。”",
 "引用渔歌作结，将全文收束在一片猿声之中。渔歌质朴苍凉，“泪沾裳”三字把秋峡之哀推向极处，也暗暗透出三峡航路之险、行旅之悲——景语化作情语，山川之美与人间之慨融为一体，余韵悠长。",
 ["引用", "以歌结情"]),
]

PARTS = {
 1:("连山无阙 · 雄奇之山","第1段","总写三峡绵延高峻的山势：两岸连山、隐天蔽日，山是三峡的骨架。"),
 2:("襄陵阻绝 · 奔放之水","第2段","写夏季水势之猛、流速之疾：朝发白帝、暮到江陵，水是三峡的血脉。"),
 3:("素湍绿潭 · 清秀之景","第3段","写春冬两季的清幽秀美：回清倒影、清荣峻茂，刚柔相济。"),
 4:("林寒涧肃 · 凄异之秋","第4段","写秋季的萧瑟哀婉：高猿长啸、渔歌沾裳，以声传情作结。"),
}

FULLTEXT = [
 "自三峡七百里中，两岸连山，略无阙处。重岩叠嶂，隐天蔽日，自非亭午夜分，不见曦月。",
 "至于夏水襄陵，沿溯阻绝。或王命急宣，有时朝发白帝，暮到江陵，其间千二百里，虽乘奔御风，不以疾也。",
 "春冬之时，则素湍绿潭，回清倒影，绝巘多生怪柏，悬泉瀑布，飞漱其间，清荣峻茂，良多趣味。",
 "每至晴初霜旦，林寒涧肃，常有高猿长啸，属引凄异，空谷传响，哀转久绝。故渔者歌曰：“巴东三峡巫峡长，猿鸣三声泪沾裳。”",
]

# 听写字库：符合“句中留空+有区分度”的全部列入，不硬凑
WORDS = [
 {"w":"嶂","py":"zhàng","q":"重岩叠□，隐天蔽日","tip":"「嶂」山字旁，直立如屏障的山峰；勿写「障」「彰」"},
 {"w":"曦","py":"xī","q":"自非亭午夜分，不见□月","tip":"「曦」日字旁，日光义，指太阳；勿写「羲」「燨」"},
 {"w":"襄","py":"xiāng","q":"至于夏水□陵","tip":"「襄」此处义为冲上、漫上，夏水襄陵；勿写「镶」「骧」"},
 {"w":"溯","py":"sù","q":"沿□阻绝","tip":"「溯」三点水，逆流而上；勿写「朔」「搠」"},
 {"w":"湍","py":"tuān","q":"则素□绿潭","tip":"「湍」三点水，急流的水；勿写「端」「瑞」"},
 {"w":"巘","py":"yǎn","q":"绝□多生怪柏","tip":"「巘」山字旁（上山下献），山峰义，读 yǎn；极易写错"},
 {"w":"漱","py":"shù","q":"悬泉瀑布，飞□其间","tip":"「漱」三点水，冲荡义；勿写「嗽」「籁」"},
 {"w":"涧","py":"jiàn","q":"每至晴初霜旦，林寒□肃","tip":"「涧」三点水，夹在山间的水沟；勿写「贱」「间」"},
 {"w":"肃","py":"sù","q":"林寒涧□","tip":"「肃」肃杀、凄寒义，此处读 sù；勿写「萧」「箫」"},
 {"w":"御","py":"yù","q":"虽乘奔□风，不以疾也","tip":"「御」双人旁（彳），驾御义；勿写「驱」「禦」"},
 {"w":"属","py":"zhǔ","q":"常有高猿长啸，□引凄异","tip":"此处「属」读 zhǔ，连接义，勿读 shǔ"},
 {"w":"沾","py":"zhān","q":"猿鸣三声泪□裳","tip":"「沾」三点水，浸湿义；勿写「粘」「占」"},
 {"w":"裳","py":"cháng","q":"故渔者歌曰：巴东三峡巫峡长，猿鸣三声泪沾□","tip":"此处「裳」读 cháng，古时下裙；勿读 shang"},
 {"w":"蔽","py":"bì","q":"重岩叠嶂，隐天□日","tip":"「蔽」草字头，遮蔽义；勿写「敝」「弊」"},
]

NOTES = [
 {"w":"自三峡","a":"自：在，从","q":"自三峡七百里中"},
 {"w":"略无","a":"完全没有","q":"两岸连山，略无阙处"},
 {"w":"阙","a":"同“缺”，空隙、缺口","q":"两岸连山，略无阙处"},
 {"w":"重岩叠嶂","a":"重叠的山岩、像屏障一样的山峰。嶂，直立如屏障的山峰","q":"重岩叠嶂，隐天蔽日"},
 {"w":"隐天蔽日","a":"遮蔽了天空和太阳","q":"重岩叠嶂，隐天蔽日"},
 {"w":"自非","a":"如果不是。自，如果","q":"自非亭午夜分，不见曦月"},
 {"w":"亭午","a":"正午","q":"自非亭午夜分，不见曦月"},
 {"w":"夜分","a":"半夜","q":"自非亭午夜分，不见曦月"},
 {"w":"曦","a":"日光，这里指太阳。读 xī","q":"自非亭午夜分，不见曦月"},
 {"w":"夏水襄陵","a":"夏天江水漫上丘陵。襄，冲上、漫上；陵，大的土山","q":"至于夏水襄陵，沿溯阻绝"},
 {"w":"沿溯","a":"顺流而下为沿，逆流而上为溯。溯，读 sù","q":"至于夏水襄陵，沿溯阻绝"},
 {"w":"阻绝","a":"阻断，不能通航","q":"至于夏水襄陵，沿溯阻绝"},
 {"w":"或","a":"有时","q":"或王命急宣，有时朝发白帝"},
 {"w":"王命急宣","a":"皇帝的命令要紧急传达。宣，传达","q":"或王命急宣，有时朝发白帝"},
 {"w":"白帝","a":"城名，在今重庆奉节东白帝山上","q":"有时朝发白帝，暮到江陵"},
 {"w":"江陵","a":"地名，在今湖北荆州","q":"有时朝发白帝，暮到江陵"},
 {"w":"奔","a":"动词用作名词，指飞奔的马","q":"虽乘奔御风，不以疾也"},
 {"w":"御风","a":"驾着风。御，驾御","q":"虽乘奔御风，不以疾也"},
 {"w":"不以疾","a":"不如这样快。以，如、及；疾，快","q":"虽乘奔御风，不以疾也"},
 {"w":"素湍","a":"白色的急流。湍，急流的水，读 tuān","q":"则素湍绿潭，回清倒影"},
 {"w":"绿潭","a":"碧绿的深水","q":"则素湍绿潭，回清倒影"},
 {"w":"回清","a":"回旋的清波","q":"则素湍绿潭，回清倒影"},
 {"w":"倒影","a":"倒映着各种景物的影子","q":"则素湍绿潭，回清倒影"},
 {"w":"绝巘","a":"极高的山峰。巘，山峰，读 yǎn","q":"绝巘多生怪柏，悬泉瀑布"},
 {"w":"怪柏","a":"姿态怪异的柏树","q":"绝巘多生怪柏，悬泉瀑布"},
 {"w":"悬泉","a":"从山崖流下的悬挂着的泉水","q":"绝巘多生怪柏，悬泉瀑布，飞漱其间"},
 {"w":"飞漱","a":"飞速地冲荡。漱，冲荡，读 shù","q":"绝巘多生怪柏，悬泉瀑布，飞漱其间"},
 {"w":"清荣峻茂","a":"水清、树荣、山高、草盛","q":"清荣峻茂，良多趣味"},
 {"w":"良","a":"甚，很","q":"清荣峻茂，良多趣味"},
 {"w":"晴初","a":"天刚放晴","q":"每至晴初霜旦，林寒涧肃"},
 {"w":"霜旦","a":"下霜的早晨","q":"每至晴初霜旦，林寒涧肃"},
 {"w":"林寒涧肃","a":"树林和山涧显出一片清凉和寂静。肃，肃杀、凄寒","q":"每至晴初霜旦，林寒涧肃"},
 {"w":"属引凄异","a":"声音持续不断，异常凄凉。属，连接，读 zhǔ；引，延长","q":"常有高猿长啸，属引凄异"},
 {"w":"空谷传响","a":"空荡的山谷里传来猿啼的回声。响，回声","q":"空谷传响，哀转久绝"},
 {"w":"哀转久绝","a":"声音悲凉婉转，很久才消失。转，同“啭”，声音婉转","q":"空谷传响，哀转久绝"},
 {"w":"巴东","a":"地名，今重庆东部云阳、奉节、巫山一带","q":"巴东三峡巫峡长，猿鸣三声泪沾裳"},
 {"w":"沾","a":"沾湿","q":"巴东三峡巫峡长，猿鸣三声泪沾裳"},
 {"w":"裳","a":"古时下裙，这里泛指衣服。读 cháng","q":"巴东三峡巫峡长，猿鸣三声泪沾裳"},
]

BG_LEAD = [
 "《三峡》节选自《水经注》卷三十四《江水》，题目是编者加的。全文以不到二百字的篇幅，描摹了长江三峡雄奇险拔、清幽秀丽的景色，是山水小品文中的千古名篇。",
 "《水经注》名为注释《水经》，实则以《水经》为纲，广泛记载了一千多条大小河流及相关的历史遗迹、人物掌故、神话传说，是我国古代地理名著，也是散文佳作，对后世山水游记影响深远。",
]
AUTHOR = [
 "郦道元（约470—527），字善长，范阳涿县（今河北涿州）人，北魏地理学家。曾任冀州镇东府长史、鲁阳太守、东荆州刺史、河南尹等职，为政严猛，执法清刻。后奉命出使关中，遭雍州刺史萧宝夤杀害。",
 "郦道元好学博览，遍历北方各地，留心观察水道风物。《水经注》四十卷即为毕生心血所聚，文笔绚烂，山水传神，兼具科学与文学双重价值，被誉为“宇宙未有之奇书”。",
]
STORY = [
 ("为《水经》作注","《水经》是三国时人桑钦所著的一部记录全国水道的简略地理书，仅一万三千余字。郦道元有感于其“粗缀津绪，阙略不全”，遂以之为纲，亲历考察、广搜文献，写成四十卷《水经注》，字数三十倍于原书。"),
 ("未至三峡之憾","学者多认为郦道元一生足迹未至江南，写三峡主要依据前人记载与传闻。正因如此，《三峡》才更见匠心——以想象与文献重构山河，为一片他到不了的山河，写下了最深情的注脚。"),
 ("北魏时代","郦道元所处的北魏，南北分裂、南北互市不通。他写南方山水，寄托的实是对天下一统、江山入画的向往；文中四季三峡的壮美与深情，也由此超越了单纯的地理记录。"),
]
VIDEOS = [("郦道元《三峡》朗读（八上语文）","BV1YB4y1f76j","郦道元《三峡》朗读，山水散文名篇，八年级语文上册"),
          ("《三峡》课文第一人称沉浸式体验","BV1YeVxeXE1Y","《三峡》课文第一人称沉浸式体验")]

APP_PEOPLE = [
 ("山河的深情注脚人","郦道元写三峡，笔下有科学家的精确，更有诗人的深情。“素湍绿潭，回清倒影”是精确的水文记录，“猿鸣三声泪沾裳”是人间行旅的喟叹。他把地理书写写成了文学，把一条江写成了四季有魂的生灵——这不是猎奇的风物志，而是一位北魏学者对万里江山最温柔的凝视。"),
]
APP_ART = [
 ("抓住特征，善用笔墨","全文按季节分写山、夏水、春冬、秋景，各抓其最突出之点：山写连绵高峻，夏水写奔放疾速，春冬写清幽秀美，秋景写凄婉哀转。四个部分既相对独立，又以三峡整体气质贯通，笔墨极其俭省而面貌全出。"),
 ("正侧结合，层层烘托","写山，先正面写“两岸连山，略无阙处”，再以“隐天蔽日”“不见曦月”侧面烘托其高峻；写水，先以“沿溯阻绝”从航路断绝反衬水势，再正面写“朝发白帝，暮到江陵”。正笔立其形，侧笔传其神，虚实相生。"),
 ("动静相衬，声色兼备","“素湍绿潭”中急流为动、深潭为静，“回清倒影”里清波回旋是动、影子沉静是静；“怪柏”静而“飞漱”动。春冬以色彩取胜（素、绿），秋景以声音动人（长啸、传响），三峡的四季因此有形有声有色。"),
 ("骈散相间，音节谐美","全文以四字句为主干，间以散句调节，如“重岩叠嶂，隐天蔽日”“清荣峻茂，良多趣味”，节奏整齐而绝不呆板；渔歌引文入文，更添古朴苍凉之韵。读来朗朗上口，宜于成诵。"),
]
APP_FAME = [
 ("重岩叠嶂，隐天蔽日。","八字写山，字字如刻。“重”“叠”言岩嶂之多，“隐”“蔽”言其高峻——连日月都藏得住的山，才配称三峡。以失天日写山之高，是典型的侧面烘托，比直说山高百仞更有力。"),
 ("虽乘奔御风，不以疾也。","快马与疾风是人间速度的极致，而作者说船比它们更快——不直接写水速，而借两项“不可能被超越”的参照物作比，夏水之疾遂成千古定评。李白“千里江陵一日还”正从此句化出。"),
 ("素湍绿潭，回清倒影。","一句之中俯仰两层：俯看白色急流卷起回旋的清波，仰看绝壁怪柏倒映在碧绿深潭里。素、绿二字设色明净，动静互映，把春冬三峡写成了工笔小品，是全文最清丽的一笔。"),
 ("巴东三峡巫峡长，猿鸣三声泪沾裳。","引渔歌作结，以歌传情。猿声本哀，三峡山高谷深，回声往复，哀音更久；渔人行舟其上，闻声堕泪。景之凄异与人之情悲在此合而为一，全文的秋峡因此不止是景，更是人间。"),
]
APP_THEME = [
 "《三峡》以凝练生动的笔墨，描写了长江三峡雄奇险拔、清幽秀丽的景色：山之连绵高峻、夏水之奔放疾速、春冬之清幽秀美、秋景之凄婉哀转，四季各异而气象万千，展现了祖国河山的壮美。",
 "文章在写景之外，亦暗含对三峡航路艰险、行旅悲辛的关注——夏水阻绝、猿鸣沾裳，既是自然之景，也是人间之情。郦道元以地理学家的严谨与文学家的深情，为三峡立传，为中国山水散文树立了典范。",
]

ACC = [
 ("通假字", [
   ("阙","同“缺”，空隙、缺口。例：两岸连山，略无阙处"),
   ("转","同“啭”，声音婉转。例：空谷传响，哀转久绝"),
 ]),
 ("古今异义", [
   ("或","古义：有时（或王命急宣）；今义：或许，表选择"),
   ("虽","古义：即使（虽乘奔御风）；今义：虽然"),
   ("良","古义：甚，很（良多趣味）；今义：良好，善良"),
   ("疾","古义：快（不以疾也）；今义：疾病"),
   ("夜分","古义：半夜（自非亭午夜分）；今义：不单独使用"),
 ]),
 ("词类活用", [
   ("奔","动词用作名词，指飞奔的马。例：虽乘奔御风"),
 ]),
 ("一词多义", [
   ("自","①在，从：自三峡七百里中；②如果：自非亭午夜分"),
   ("绝","①阻断：沿溯阻绝；②极高：绝巘多生怪柏；③消失：哀转久绝"),
   ("清","①回旋的清波：回清倒影；②水清：清荣峻茂"),
   ("属","连接：属引凄异（读 zhǔ）"),
 ]),
 ("文化常识", [
   ("《水经注》","北魏郦道元撰，四十卷，为三国时《水经》作注。记载河流一千余条及沿岸风物掌故，是我国古代地理名著，也是山水散文杰作。"),
   ("三峡","瞿塘峡、巫峡、西陵峡的合称，西起重庆奉节白帝城，东至湖北宜昌南津关，全长约二百公里，两岸高山对峙，江流湍急。文中“七百里”为古代计程，约合今二百余里。"),
   ("白帝城","在今重庆奉节东白帝山上。东汉公孙述筑城，自号白帝。三国刘备伐吴败退于此。李白“朝辞白帝彩云间”即咏此地。"),
   ("渔者歌","巴东一带渔民行船所唱之歌谣。文中所引渔歌又见于《水经注》他篇及《宜都山川记》，是古代三峡行旅生活的真实写照。"),
 ]),
]

# ================= 组装 =================
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]
main_js, dict_js = re.findall(r"<script>\n(.*?)</script>", src, re.S)
main_js = main_js.replace("beiying_fs", LS_KEY)
dict_js = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", dict_js, flags=re.S)
dict_js = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", dict_js, flags=re.S)

CN = "一二三四"
hero = '<header class="hero">\n  <div class="hero-side">北魏 · 郦道元</div>\n  <h1 class="hero-title">三峡</h1>\n</header>'
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
      '<div class="sec-sub">全文分四部分：山、夏水、春冬、秋景。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>',
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
       '<div class="sec-head"><h2>赏 析</h2><span class="no">笔法 · 艺术 · 名句</span></div>',
       '<div class="box"><h3>形象赏析</h3><p style="margin-bottom:14px;color:var(--ink2)">文中的“形象”是四季面目各异的三峡，与它背后那位深情凝视山河的记录者。</p><div class="fame">']
for t, p in APP_PEOPLE: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>艺术特色</h3><div class="fame">')
for t, p in APP_ART: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>名句赏析</h3><div class="fame">')
for t, p in APP_FAME: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>主题思想</h3>')
for p in APP_THEME: app.append('<p>' + p + '</p>')
app.append('</div></section>')

acc = ['<div class="divider"></div>', '<section id="acc" class="sec">',
       '<div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 词类活用 · 文化常识</span></div>']
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
footer = '<footer>\n  <div class="kai">《三峡》</div>\n  <div>郦道元 · 北魏 · 节选自《水经注·江水》</div>\n</footer>'
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

html_doc = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>《三峡》郦道元</title>\n<style>' + css + '</style>\n</head>\n<body data-fs="100">\n\n'
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
# 全文与卡片流一致性
card_stream = "".join(plain(t) for (_, t, _, _, _) in CARDS).replace("​", "")
full_stream = "".join(FULLTEXT)
norm = lambda s: re.sub(r"\s+", "", s)
import difflib
if norm(card_stream) != norm(full_stream):
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, norm(card_stream), norm(full_stream)).get_opcodes():
        if op != "equal":
            print("DIFF", op, repr(norm(card_stream)[a1:a2]), "!=", repr(norm(full_stream)[b1:b2]))
    raise SystemExit("fulltext/card stream mismatch")
print("三峡 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), html_doc.count('class="anno-word"'), len(WORDS), len(NOTES), len(html_doc.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html_doc)
print("OK ->", OUT)
