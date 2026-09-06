# -*- coding: utf-8 -*-
"""生成《小石潭记》课件（文言模式：译文+赏析）。自包含脚本。"""
import io, json, re

SRC = r"D:\App\Apps\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\xiaoshitanji-liuzongyuan.html"
LS_KEY = "xiaoshitan_fs"

def A(word, note):
    return '<span class="anno-word" data-note="' + note + '">' + word + '</span>'

CARDS = [
(1, "从小丘" + A("西行","向西走。西，名词作状语，向西") + "百二十步，隔" + A("篁竹","（huáng）竹林") + "，闻水声，" + A("如鸣珮环","好像珮环碰撞的声音。鸣，使……发出声音；珮、环，都是玉饰") + "，" + A("心乐之","心里感到高兴。乐，意动用法，以……为乐") + "。",
 "从小丘向西走一百二十多步，隔着竹林，可以听到流水的声音，好像人身上佩带的珮环相互碰击发出的声音，我心里为之高兴。",
 "未见其潭，先闻其声——以水声之悦耳写潭之可爱，“心乐之”一句为全文奠定了“由乐转凄”的情感基调。"),
(1, "伐竹取道，下见小潭，水" + A("尤","格外、特别") + A("清冽","（liè）清凉。冽，寒冷") + "。",
 "砍倒竹子，开辟出一条道路，往下看见一个小潭，潭水格外清凉。",
 "“伐竹取道”见探寻之切；“清冽”二字直写潭水，清到寒意沁人，暗伏后文“凄神寒骨”。"),
(1, "全石" + A("以为底","“以全石为底”的倒装，潭以整块石头为底") + "，近岸，" + A("卷","（quán）弯曲") + "石底以出，为" + A("坻","（chí）水中高地") + "，为" + A("屿","小岛") + "，为" + A("嵁","（kān）不平的岩石") + "，为岩。",
 "小潭以整块石头为底，靠近岸的地方，石底有些部分翻卷过来露出水面，成为坻、屿、嵁、岩各种不同的形状。",
 "“全石以为底”交代小潭“石潭”之名；坻、屿、嵁、岩四字排布，写尽潭底石头形态之奇。"),
(1, A("青树翠蔓","青葱的树木，翠绿的藤蔓") + "，" + A("蒙络摇缀","覆盖缠绕，摇动下垂、连缀在一起") + "，" + A("参差披拂","（cēn cī pī fú）参差不齐，随风飘荡") + "。",
 "青葱的树木，翠绿的藤蔓，覆盖着、缠绕着、摇动着、连缀着，参差不齐，随风飘荡。",
 "四个动词连用写藤蔓动态，静景活写；掩映成趣的竹林也为下文“伐竹取道”“四面竹树环合”埋下伏笔。"),
(2, "潭中鱼" + A("可","大约") + "百" + A("许","用在数词后表示约数，左右") + "头，皆若" + A("空游","在空中游动") + A("无所依","没有什么依托") + "，日光" + A("下澈","（chè）向下穿透到水底。下，名词作状语") + "，影布石上。",
 "潭中的鱼大约有一百来条，都好像在空中游动，什么依托也没有；阳光向下直照到水底，鱼的影子映在石头上。",
 "写鱼即写水——鱼“空游无所依”、日光下澈、鱼影分明，三笔全是侧面烘托，无一“清”字而潭水之清澈如见，是写水千古名笔。"),
(2, A("佁然","（yǐ）静止不动的样子") + "不动，" + A("俶尔","（chù ěr）忽然") + "远逝，往来" + A("翕忽","（xī）轻快敏捷的样子") + "，似与游者" + A("相乐","互相取乐") + "。",
 "（鱼儿）呆呆地一动不动，忽然向远处游去，来来往往，轻快敏捷，好像和游人一同快乐。",
 "动静相生：静时憨然可掬，动时轻快灵动；“似与游者相乐”物我交融，是柳宗元此刻暂忘贬谪之痛的片刻欢愉。"),
(3, "潭" + A("西南","向西南。名词作状语") + "而望，" + A("斗折蛇行","像北斗七星那样曲折，像蛇爬行那样弯曲。斗、蛇，名词作状语") + "，" + A("明灭可见","（溪流）或隐或现，都能看见") + "。",
 "向小石潭的西南方看去，溪水像北斗星那样曲折，像蛇爬行那样弯曲，一段看得见，一段看不见。",
 "“斗折蛇行”以天上星象、地上蛇行作比，一词一形；“明灭可见”写溪身隐现之光感，比喻贴切、观察入微。"),
(3, "其岸势" + A("犬牙差互","（cī hù）像狗的牙齿那样相互交错") + "，不可知其源。",
 "溪岸的地势像狗的牙齿那样互相交错，不能知道溪水的源头。",
 "再以“犬牙差互”作比，写尽岸势错落；源不可知，境界幽深，也隐约透出前途难测的心绪。"),
(4, "坐潭上，四面竹树环合，" + A("寂寥","寂静寥落") + "无人，" + A("凄神寒骨","（使人感到）心神凄凉，寒气透骨。凄、寒，使动用法") + "，" + A("悄怆幽邃","（qiǎo chuàng yōu suì）静悄悄的，幽深。悄怆，忧伤的样子；邃，深") + "。",
 "我坐在潭边，四面竹林树木环绕合抱，寂静寥落，没有旁人，使人感到心神凄凉，寒气透骨，幽静深远，弥漫着忧伤的气息。",
 "“凄神寒骨”由身之感写到心之寒，景之“清”化为境之“凄”——被贬永州的孤寂悲凉，从竹树环合的幽境中渗出，情景交融至此。"),
(4, A("以","因为") + "其境" + A("过清","过分凄清。清，凄清") + "，不可久" + A("居","停留") + "，乃记之而" + A("去","离开") + "。",
 "因为这里的环境太过凄清，不能长时间停留，于是记下这番景致就离开了。",
 "“过清”二字点破转凄之由，与开篇“心乐之”对照成文；乐是暂时的，凄才是心底的底色——贬谪文人的生命况味尽在其中。"),
(5, "同游者：" + A("吴武陵","作者友人，元和进士，亦被贬永州") + "，龚古，余弟" + A("宗玄","作者的堂弟") + "。" + A("隶而从者","跟着同去的。隶，跟随") + "，崔氏二" + A("小生","年轻人。古今异义，旧注指柳宗元的姐夫崔简的两个儿子") + "，曰" + A("恕己","崔恕己") + "，曰" + A("奉壹","崔奉壹") + "。",
 "一同去游览的人：吴武陵、龚古、我的弟弟宗玄；跟着一同去的，还有姓崔的两个年轻人：一个叫恕己，一个叫奉壹。",
 "补记同游者姓名，游记体例的收束笔法；二小生乃崔简之子——崔简亦柳宗元贬谪途中交往的落难之人，同游者皆“同是天涯沦落人”。"),
]

PARTS = {
 1:("发现小潭 · 竹水相映","第1段","隔竹闻声、伐竹取道——以声写水、以石写潭，见潭之奇。"),
 2:("潭中游鱼 · 空游之清","第2段","鱼若空游、影布石上，侧面写水之清；鱼似与游者相乐，物我交融。"),
 3:("溪身岸势 · 源流神秘","第3段","斗折蛇行、犬牙差互，两个比喻写尽溪流曲折、岸势错落。"),
 4:("潭中气氛 · 凄神寒骨","第4段","竹树环合、寂寥无人，境过清而不可久居，由乐转凄。"),
 5:("同游之人 · 记之而去","第5段","补记同游者姓名，游记体例收束。"),
}

FULLTEXT = [
 "从小丘西行百二十步，隔篁竹，闻水声，如鸣珮环，心乐之。伐竹取道，下见小潭，水尤清冽。全石以为底，近岸，卷石底以出，为坻，为屿，为嵁，为岩。青树翠蔓，蒙络摇缀，参差披拂。",
 "潭中鱼可百许头，皆若空游无所依，日光下澈，影布石上。佁然不动，俶尔远逝，往来翕忽，似与游者相乐。",
 "潭西南而望，斗折蛇行，明灭可见。其岸势犬牙差互，不可知其源。",
 "坐潭上，四面竹树环合，寂寥无人，凄神寒骨，悄怆幽邃。以其境过清，不可久居，乃记之而去。",
 "同游者：吴武陵，龚古，余弟宗玄。隶而从者，崔氏二小生，曰恕己，曰奉壹。",
]

BG_LEAD = [
 "柳宗元因参加王叔文领导的“永贞革新”，于永贞元年（805年）被贬为永州司马。司马是有职无权的闲官，他在永州一住十年，寄情山水以排遣忧愤，遍游郊野，写成著名的《永州八记》，《小石潭记》为其中第四篇，写于元和年间。",
 "小石潭在永州（今湖南零陵）城西郊外。柳宗元于一次出游中偶然发现这个小石潭，为其水石之美所动；然而潭境过于清幽，又唤起他心底的孤寂悲凉——“乐是暂时的，凄是深沉的”。全文不足二百字，却写出了山水游记中最细腻的情感曲线。",
]
AUTHOR = [
 "柳宗元（773—819），字子厚，河东（今山西运城永济）人，世称“柳河东”。唐代文学家、哲学家，“唐宋八大家”之一。与韩愈共同倡导古文运动，并称“韩柳”。永贞元年革新失败后贬永州司马，后改柳州刺史，卒于柳州任上，故又称“柳柳州”。有《柳河东集》。",
 "柳宗元的山水游记成就最高，《永州八记》开创了以山水寄托身世之感的游记传统。他的诗文幽深清峻，于山水清音中常藏着孤愤与凄怆，《小石潭记》即其代表。",
]
STORY = [
 ("永贞革新","唐顺宗即位后，王叔文、柳宗元等主持政治改革，罢宫市、免欠赋，史称“永贞革新”。改革历时一百余天即告失败，八人被贬为边州司马，史称“八司马事件”。"),
 ("贬谪永州","柳宗元初贬永州时寄居龙兴寺，母亲病故，居所数遭火灾，身心交瘁。为排遣忧愤，他“闷即出游”，遍访永州山水，写下一系列山水游记。"),
 ("永州八记","《始得西山宴游记》《钴鉧潭记》《钴鉧潭西小丘记》《小石潭记》等八篇游记，合称《永州八记》。八记既是一组山水画卷，也是一部贬谪心史。"),
 ("凑巧的地名","柳宗元从西山下来，经钴鉧潭、小丘，伐竹而得小潭，遂有此记。文末所记同游者吴武陵、龚古等，也都是当时被贬或落拓之人。"),
]

APP_PEOPLE = [
 ("柳宗元 —— 寄情山水而难以释怀的贬谪者",
  "他以发现者的惊喜写潭，以画家的眼睛摹鱼，可“四面竹树环合”的幽境一合拢，“凄神寒骨，悄怆幽邃”便涌上心头。乐——凄——去，一条情感曲线，画出改革失败后被贬远州的知识分子精神底色：山水可以暂时安顿他，却治愈不了他。"),
 ("潭中之鱼 —— 空游自在的“自由”意象",
  "“皆若空游无所依”，鱼在柳宗元笔下没有一丝拘束，往来翕忽，似与游者相乐。这位失去自由的逐臣，把对自在的向往寄托给了那一百来条鱼——鱼之乐，正是人求之不得的乐。"),
]
APP_ART = [
 ("移步换景，井然有序",
  "闻声——伐竹——见潭——观鱼——望源——坐潭——记之而去，以游踪为线，所见所闻所感次第展开，是古代山水游记“移步换景”章法的典范。"),
 ("侧面烘托，不著一字",
  "写水之清澈，全不用“清”字正面形容，而以鱼“空游无所依”、日光下澈、影布石上烘托——皆若空游，其清可知，是侧面描写的千古名例。"),
 ("比喻精妙，曲尽其态",
  "“斗折蛇行”写溪身，“犬牙差互”写岸势，一取象于星蛇，一取象于兽牙，状难写之景如在目前；坻、屿、嵁、岩四字排比，写尽石底奇态。"),
 ("情景交融，由乐转凄",
  "开篇“心乐之”，中段“似与游者相乐”，结尾“凄神寒骨”“以其境过清，不可久居”——情感的起伏与潭境的幽邃互为表里，景语即情语，是柳文“清深”风格的代表。"),
]
APP_FAME = [
 ("潭中鱼可百许头，皆若空游无所依，日光下澈，影布石上。",
  "正面不著一字写水清，全借鱼与影来写：鱼如在空中，则水之澄澈可见；日光直透水底，影布石上，则水之净可掬。虚处传神，历来被誉为古代写水第一笔。"),
 ("佁然不动，俶尔远逝，往来翕忽，似与游者相乐。",
  "十二字写尽鱼之神态：静时呆若木雕，动时倏忽远逝，一静一动，节奏如音乐。以“似与游者相乐”收束，鱼通人性，物我两忘，是柳宗元贬谪生活中难得的亮色。"),
 ("潭西南而望，斗折蛇行，明灭可见。",
  "“斗折”状溪身之曲，“蛇行”状溪流之动，“明灭可见”写远处波光忽隐忽现。两个比喻加一个光影描写，把一条看不见源头的小溪写活了。"),
 ("凄神寒骨，悄怆幽邃。",
  "由“心乐之”到“凄神寒骨”，是全文情感的转折点。潭之“清冽”至此化为境之“凄清”，山水之美终于敌不过贬谪之痛——八个字写尽幽境中的孤独，也写透了柳宗元的心。"),
]
APP_THEME = [
 "本文以游踪为序，记叙了发现小石潭、潭中景物、溪流水源、潭中气氛的经过，生动描绘了小石潭水石之美与幽邃之境；同时寓情于景，抒发了作者贬居生活中的孤凄悲凉之情。",
 "文章前半见“乐”，后半见“凄”：乐是山水之乐，凄是身世之凄。乐凄交织，以乐衬凄，正是柳宗元被贬永州期间复杂心绪的真实写照——寄情山水而不能忘怀现实，是《永州八记》共同的精神底色。",
]

ACC = [
 ("古今异义", [
   ("可","古义：大约。潭中鱼可百许头。今义：可以、能够。"),
   ("许","古义：用在数词后表约数。百许头。今义：许诺、或许。"),
   ("居","古义：停留。不可久居。今义：居住。"),
   ("去","古义：离开。乃记之而去。今义：前往。"),
   ("小生","古义：年轻人。崔氏二小生。今义：指戏曲中的青年男子角色。"),
   ("清","古义：凄清、冷清。以其境过清。今义：清澈、干净。"),
 ]),
 ("词类活用", [
   ("乐","意动用法，以……为乐。心乐之。"),
   ("西、西南","名词作状语，向西、向西南。从小丘西行百二十步；潭西南而望。"),
   ("下","名词作状语，向下。日光下澈。"),
   ("斗、蛇","名词作状语，像北斗那样、像蛇那样。斗折蛇行。"),
   ("犬牙","名词作状语，像狗的牙齿那样。犬牙差互。"),
   ("凄、寒","使动用法，使……凄凉，使……寒冷。凄神寒骨。"),
 ]),
 ("一词多义", [
   ("以","因为（以其境过清）；相当于“而”（卷石底以出）。"),
   ("清","清澈（水尤清冽）；凄清（以其境过清）。"),
   ("从","跟随（隶而从者）；自、由（从小丘西行）。"),
   ("见","看见（下见小潭）；显露、呈现（影布石上之“布”义近，另“才美不外见”）。"),
   ("乐","以……为乐（心乐之）；逗乐、嬉戏（似与游者相乐）。"),
 ]),
 ("文言句式", [
   ("宾语前置","全石以为底（即“以全石为底”）。"),
   ("谓语前置","如鸣珮环（即“如珮环鸣”）。"),
   ("省略句","（鱼）影布（于）石上；（余）坐潭上。"),
   ("定语后置","皆若空游无所依（“无所依”修饰“空游”）。"),
 ]),
 ("文化常识", [
   ("永州八记","柳宗元贬永州所作八篇山水游记的合称，《小石潭记》为其第四篇。"),
   ("司马","州郡的佐官，唐中期多为安置贬谪官员的闲职，无实际职权。"),
   ("永贞革新","唐顺宗永贞年间王叔文等主导的政治改革，失败后八人被贬，史称“八司马”。"),
   ("唐宋八大家","韩愈、柳宗元、欧阳修、苏洵、苏轼、苏辙、王安石、曾巩八位散文家的合称。"),
 ]),
]

WORDS = [
 {"w":"篁","py":"huáng","q":"隔□竹，闻水声","tip":"「篁」竹字头，竹林；与「皇」（白字头）区分"},
 {"w":"冽","py":"liè","q":"下见小潭，水尤清□","tip":"「冽」两点水，寒冷义；与「烈」（四点底，火）区分"},
 {"w":"坻","py":"chí","q":"为□，为屿，为嵁，为岩","tip":"「坻」土字旁，水中高地；不要读成 dǐ"},
 {"w":"屿","py":"yǔ","q":"为坻，为□，为嵁，为岩","tip":"「屿」山字旁，小岛；与「与」区分"},
 {"w":"嵁","py":"kān","q":"为坻，为屿，为□，为岩","tip":"「嵁」山字旁，不平的岩石；笔画注意「堪」无山字头"},
 {"w":"蔓","py":"màn","q":"青树翠□，蒙络摇缀","tip":"「蔓」草字头，藤蔓；读 màn 不读 wàn（课文读法按教材注音 màn）"},
 {"w":"缀","py":"zhuì","q":"蒙络摇□，参差披拂","tip":"「缀」绞丝旁，连结；与「辍」（车字旁，中断）区分"},
 {"w":"拂","py":"fú","q":"参差披□","tip":"「拂」提手旁，飘动；不要读成 fó"},
 {"w":"佁","py":"yǐ","q":"□然不动，俶尔远逝","tip":"「佁」单人旁，静止的样子；不要读成 tái"},
 {"w":"俶","py":"chù","q":"佁然不动，□尔远逝","tip":"「俶」单人旁，忽然；与「叔」区分"},
 {"w":"翕","py":"xī","q":"往来□忽，似与游者相乐","tip":"「翕」合字头，聚合、迅疾；与「歙」（xī/shè）区分"},
 {"w":"邃","py":"suì","q":"悄怆幽□","tip":"「邃」辶旁，幽深；与「隧」（左耳旁，隧道）区分"},
 {"w":"怆","py":"chuàng","q":"凄神寒骨，悄□幽邃","tip":"「怆」竖心旁，悲伤；与「沧」（三点水）区分"},
 {"w":"龚","py":"gōng","q":"同游者：吴武陵，□古，余弟宗玄","tip":"「龚」上「龙」下「共」，姓氏；与「供」（单人旁）区分"},
 {"w":"玄","py":"xuán","q":"同游者：吴武陵，龚古，余弟宗□","tip":"「玄」单独成字，黑色、深奥；不要写成「眩」"},
]
NOTES = [
 {"w":"如鸣珮环","a":"好像珮环碰撞的声音。珮、环，都是玉饰","q":"隔篁竹，闻水声，如鸣珮环"},
 {"w":"心乐之","a":"心里感到高兴。乐，以……为乐","q":"隔篁竹，闻水声，如鸣珮环，心乐之"},
 {"w":"清冽","a":"清凉。冽，寒冷","q":"伐竹取道，下见小潭，水尤清冽"},
 {"w":"全石以为底","a":"潭以整块石头为底（宾语前置）","q":"全石以为底，近岸，卷石底以出"},
 {"w":"卷","a":"弯曲。读 quán","q":"全石以为底，近岸，卷石底以出"},
 {"w":"坻","a":"水中高地。读 chí","q":"为坻，为屿，为嵁，为岩"},
 {"w":"嵁","a":"不平的岩石。读 kān","q":"为坻，为屿，为嵁，为岩"},
 {"w":"蒙络摇缀","a":"覆盖缠绕，摇动下垂、连缀在一起","q":"青树翠蔓，蒙络摇缀，参差披拂"},
 {"w":"参差披拂","a":"参差不齐，随风飘荡","q":"青树翠蔓，蒙络摇缀，参差披拂"},
 {"w":"可百许头","a":"大约一百来条。可，大约；许，左右","q":"潭中鱼可百许头"},
 {"w":"空游","a":"在空中游动","q":"皆若空游无所依"},
 {"w":"下澈","a":"向下穿透到水底","q":"日光下澈，影布石上"},
 {"w":"佁然","a":"静止不动的样子。佁，读 yǐ","q":"佁然不动，俶尔远逝"},
 {"w":"俶尔","a":"忽然。读 chù ěr","q":"佁然不动，俶尔远逝"},
 {"w":"翕忽","a":"轻快敏捷的样子。翕，读 xī","q":"往来翕忽，似与游者相乐"},
 {"w":"斗折蛇行","a":"像北斗那样曲折，像蛇那样弯曲","q":"潭西南而望，斗折蛇行，明灭可见"},
 {"w":"明灭可见","a":"或隐或现，都能看见","q":"潭西南而望，斗折蛇行，明灭可见"},
 {"w":"犬牙差互","a":"像狗的牙齿那样相互交错。差互，读 cī hù","q":"其岸势犬牙差互，不可知其源"},
 {"w":"寂寥","a":"寂静寥落","q":"四面竹树环合，寂寥无人"},
 {"w":"凄神寒骨","a":"使人感到心神凄凉，寒气透骨（使动用法）","q":"四面竹树环合，寂寥无人，凄神寒骨"},
 {"w":"悄怆幽邃","a":"忧伤的样子，幽静深远。邃，读 suì","q":"凄神寒骨，悄怆幽邃"},
 {"w":"以其境过清","a":"因为这里的环境太过凄清。以，因为","q":"以其境过清，不可久居"},
 {"w":"久居","a":"长时间停留。居，停留","q":"以其境过清，不可久居"},
 {"w":"乃记之而去","a":"就记下这景致离开了。去，离开","q":"以其境过清，不可久居，乃记之而去"},
 {"w":"隶而从者","a":"跟着同去的人。隶，跟随","q":"隶而从者，崔氏二小生"},
 {"w":"小生","a":"年轻人（古今异义）","q":"隶而从者，崔氏二小生"},
]

src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]
main_js, dict_js = re.findall(r"<script>\n(.*?)</script>", src, re.S)
main_js = main_js.replace("beiying_fs", LS_KEY)
dict_js = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", dict_js, flags=re.S)
dict_js = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", dict_js, flags=re.S)

CN = "一二三四五"
hero = '<header class="hero">\n  <div class="hero-side">唐 · 柳宗元</div>\n  <h1 class="hero-title">小石潭记</h1>\n</header>'
nav = '<nav class="nav"><div class="nav-in"><a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a><div class="tool"><select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option></select><button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button></div></div></nav>'

def video(i, h4, bvid, atitle):
    return ('<div class="media"><h4>%s</h4>'
            '<iframe id="mediaF%d" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>'
            '<a href="https://www.bilibili.com/video/%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF%d">全屏播放</button></div>'
            % (h4, i, bvid, atitle, bvid, i))

VIDEOS = [("《小石潭记》朗诵","BV1t65bzUEMu","《小石潭记》朗诵版"),
          ("国宝版《小石潭记》创意演绎","BV1vj41117Py","国宝版《小石潭记》")]

bg = ['<main class="wrap">', '<section id="bg" class="sec">',
      '<div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>', '<div class="lead">']
for p in BG_LEAD: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>作者简介</h3>')
for p in AUTHOR: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>写作背景</h3>')
for t, p in STORY: bg.append('<p><b>' + t + '：</b>' + p + '</p>')
bg.append('</div><div class="box media-box"><h3>视听</h3><div class="media-grid">')
for i, (h4, bvid, at) in enumerate(VIDEOS): bg.append(video(i + 1, h4, bvid, at))
bg.append('</div></div></section>')

jl = ['<div class="divider"></div>', '<section id="jielu" class="sec">',
      '<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 · 译文</span></div>',
      '<button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>',
      '<div id="fulltext" class="poem" style="display:none">']
for p in FULLTEXT: jl.append('<div class="pl">' + p + '</div>')
jl.append('</div><div class="verse-list" id="verseList">')
cur = 0
for n, (part, orig, gk, sf) in enumerate(CARDS, 1):
    if part != cur:
        cur = part
        t, rng, ov = PARTS[part]
        jl.append('<div class="part-head"><span class="p-num">第%s部分</span><h3>%s</h3><span class="range">%s</span></div>' % (CN[part - 1], t, rng))
        jl.append('<div class="part-overview">%s</div>' % ov)
    jl.append('<div class="verse" id="l%d" data-i="%d">\n  <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>\n  <details class="v-more">\n    <summary>译文 · 赏析</summary>\n    <div class="d-body">\n      <div class="v-sec"><b class="v-label">译文</b>\n        <div class="v-trans">%s</div>\n      </div>\n      <div class="v-sec"><b class="v-label">赏析</b>\n        <div class="d-body"><p>%s</p></div>\n      </div>\n    </div>\n  </details>\n</div>' % (n, n - 1, n, orig, gk, sf))
jl.append('</div></section>')

app = ['<div class="divider"></div>', '<section id="app" class="sec">',
       '<div class="sec-head"><h2>赏 析</h2><span class="no">人物 · 艺术 · 名句</span></div>',
       '<div class="box"><h3>人物形象</h3><p style="margin-bottom:14px;color:var(--ink2)">本文的“人物”，一位是执笔的柳宗元，一位是他笔下通人性的游鱼——一悲一乐，互为镜像。</p><div class="fame">']
for t, p in APP_PEOPLE: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>艺术特色</h3><div class="fame">')
for t, p in APP_ART: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>名句赏析</h3><div class="fame">')
for t, p in APP_FAME: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>主题思想</h3>')
for p in APP_THEME: app.append('<p>' + p + '</p>')
app.append('</div></section>')

acc = ['<div class="divider"></div>', '<section id="acc" class="sec">',
       '<div class="sec-head"><h2>积 累</h2><span class="no">活用 · 句式 · 常识</span></div>']
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
footer = '<footer>\n  <div class="kai">《小石潭记》</div>\n  <div>柳宗元 · 唐 · 出自《柳河东集》（永州八记）</div>\n</footer>'
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

html = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>《小石潭记》柳宗元</title>\n<style>' + css + '</style>\n</head>\n<body data-fs="100">\n\n'
        + hero + '\n\n' + nav + '\n\n' + "\n".join(bg) + '\n\n' + "\n".join(jl) + '\n\n' + "\n".join(app) + '\n\n' + "\n".join(acc) + '\n\n' + "\n".join(practice) + '\n\n'
        + footer + '\n</main>\n\n' + tail + '\n<script>\n' + main_js + '</script>\n<script>\n' + dict_js + '</script>\n\n</body>\n</html>\n')

no_script = re.sub(r"<script>.*?</script>", "", html, flags=re.S)
body_text = re.sub(r"<[^>]+>", "", re.sub(r"<style>.*?</style>", "", no_script, flags=re.S))
assert body_text.count('"') == 0, "straight quotes in visible text"
need = ["verseList", "fulltext", "btnAll", "btnRecite", "btnPrint", "btnShowAll", "fsSel", "annoPopup", "dictate", "topBtn", "mediaF1", "mediaF2"]
missing = [i for i in need if 'id="%s"' % i not in html]
assert not missing, "missing ids: %s" % missing
assert LS_KEY in main_js and "beiying_fs" not in main_js and "beiying" not in dict_js
per_card = re.findall(r'<div class="verse".*?<div class="v-line">(.*?)</div></div>', html, re.S)
empty = [i + 1 for i, o in enumerate(per_card) if "anno-word" not in o]
assert not empty, "cards without annotation: %s" % empty
for it in WORDS:
    assert not any(c in it["q"] for c in it["w"]), "leak: %s" % it["w"]
    assert it["q"].count("□") == len(it["w"]), "box mismatch: %s" % it["w"]
    assert it["tip"] and it["tip"] != it["w"], "tip bad: %s" % it["w"]
print("小石潭记 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), html.count('class="anno-word"'), len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
