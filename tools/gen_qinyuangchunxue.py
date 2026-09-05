# -*- coding: utf-8 -*-
"""生成《沁园春·雪》课件（古诗词模式：原文+译文+赏析）。自包含脚本。"""
import io, json, re, html

SRC = r"D:\App\Apps\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\qinyuangchunxue-maozedong.html"
LS_KEY = "qinyuan_fs"

def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", rep, text)

def plain(text):
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\1", text)

CARDS = [
(1, "​[[北国|北方]]​[[风光|景色，景象]]，千里冰封，万里雪飘。",
 "北方的风光，千里江山被冰雪封冻，万里长空雪花纷飞。",
 "开篇总领上阕。“北国”定地域，“风光”定视角，千里冰封写大地之静，万里雪飘写长空之动——起笔便是一幅纵横千里的立体画卷。冰封雪飘互文见义，静者愈静，动者愈动，气象初开。",
 ["总领", "互文", "动静结合"]),
(1, "望长城内外，[[惟余|只剩下]]​[[莽莽|（mǎng mǎng）无边无际]]；大河上下，顿失[[滔滔|（tāo tāo）指黄河波涛滚滚的水势]]。",
 "远望长城内外，只剩下白茫茫的一片；黄河上下，顿时失去了滔滔水势。",
 "一个“望”字统领四句，登高远眺之势全出。长城、大河是民族与山河的象征；“惟余”“顿失”写雪之大——天地皆白，连咆哮的黄河也瞬间凝固。“顿”字尤见笔力，静景之中藏着巨大能量的蓄势。",
 ["领字", "夸张", "炼字"]),
(1, "山舞银蛇，原驰蜡象，欲与​[[天公|天帝，这里指自然界的主宰]]​[[试比高|比一比高下]]。",
 "群山披雪绵延起伏，像银蛇在舞动；高原丘陵白雪皑皑，像白象在奔驰，都想和天公比一比高下。",
 "化静为动的千古妙笔：群山本是静的，披雪而舞便成银蛇；高原本是定的，着雪而驰便成蜡象。一“舞”一“驰”，冰雪山河霎时有了生命与豪气；“欲与天公试比高”更把这份生机推向与上天争胜的高度——人的意气，渗透在雪景之中。",
 ["化静为动", "比喻", "名句"]),
(1, "​[[须|等到]]晴日，看[[红装素裹|形容雪后天晴，红日和白雪交相辉映的壮丽景色。红装，本指妇女的艳装，这里指红日照耀着大地；素裹，本指妇女的淡装，这里指白雪覆盖着大地]]，[[分外|格外]]​[[妖娆|（yāo ráo）娇艳美好]]。",
 "等到天晴的时候，红日和白雪交相辉映，那景色格外娇艳美好。",
 "由实景宕开一笔，悬想雪霁初晴：红日为妆，白雪为裹，山河顿时成了盛装的佳人。“须”“看”二字有如邀客共赏，虚景写得比实景更艳丽——严寒之中始终透着乐观与自信，正是全词的底色。",
 ["虚景", "比喻", "名句"]),
(2, "江山如此多娇，引无数英雄​[[竞折腰|争着弯腰行礼，倾倒。折腰，鞠躬，倾倒]]。",
 "江山是这样地娇美，引得无数英雄竞相倾倒。",
 "过片一转，由景入史，是全词枢纽。“江山如此多娇”总束上阕，“引”字一提，引出千年英雄史——雪景是“因”，英雄竞逐是“果”，写景与怀古经此一句浑然衔接，天衣无缝。",
 ["过渡", "承上启下", "名句"]),
(2, "​[[惜|可惜]]​[[秦皇汉武|秦始皇嬴政和汉武帝刘彻]]，略输[[文采|本指辞藻、才华，这里指文学才能]]；",
 "可惜秦始皇和汉武帝，武功虽盛，文治方面的才华却略有欠缺；",
 "一个“惜”字总领七句评点，惋惜而不贬杀。秦皇汉武是千古一帝的代表作，作者先承认其雄才，再以“略输文采”轻轻一抑——衡量英雄的尺度变了：不仅要有马上之功，更要有文明之略。",
 ["领字", "评价尺度"]),
(2, "​[[唐宗宋祖|唐太宗李世民和宋太祖赵匡胤]]，稍[[逊|差，逊色]]​[[风骚|本指《诗经》里的《国风》和《楚辞》里的《离骚》，后来泛指文章辞藻、文学才华]]。",
 "唐太宗和宋太祖，文学才华也要稍逊一筹。",
 "与上句对举成文，历数开国之君而各下一评。“稍逊”与“略输”程度相当，措辞分寸极精——不是否定他们的历史地位，而是指出其局限。为结尾“数风流人物”蓄势：旧式英雄俱有不足，真正的主人尚在后头。",
 ["对举", "用典"]),
(2, "一代​[[天骄|天之骄子，指天所宠爱的人]]，​[[成吉思汗|（hán）元太祖铁木真]]，只识弯弓射大雕。",
 "称雄一世的人物成吉思汗，只知道拉开弓射大雕。",
 "评点推向极致：“一代天骄”是极口的推崇，“只识弯弓射大雕”却是一笔抹倒——武略有余，文治全无。“只识”二字重如千钧，与秦皇汉武“略输”、唐宗宋祖“稍逊”层层加码，贬抑步步收紧，为下句的翻案作足铺垫。",
 ["层层蓄势", "用典"]),
(2, "​[[俱往矣|都过去了。俱，都]]，数​[[风流人物|建功立业的英雄人物]]，还看今朝。",
 "这些人物都过去了，称得上建功立业的英雄人物的，还要看今天的人们。",
 "收束全词的最强音。“俱往矣”三字挥手作别千年英雄史，“数风流人物，还看今朝”掷地有声——真正主宰历史、创造未来的，是当代人民。景、史、情在此汇成一道洪流，全词境界至此完满。",
 ["卒章显志", "名句"]),
]

PARTS = {
 1:("上阕 · 北国雪景","上阕","由总貌到细部，由实景到虚景，写尽北国雪原的壮阔与娇美。"),
 2:("下阕 · 评古论今","下阕","由江山之娇引出英雄竞逐，历数帝王而翻出新意，收束于“还看今朝”。"),
}

FULLTEXT = [
 "北国风光，千里冰封，万里雪飘。",
 "望长城内外，惟余莽莽；大河上下，顿失滔滔。",
 "山舞银蛇，原驰蜡象，欲与天公试比高。",
 "须晴日，看红装素裹，分外妖娆。",
 "江山如此多娇，引无数英雄竞折腰。",
 "惜秦皇汉武，略输文采；唐宗宋祖，稍逊风骚。",
 "一代天骄，成吉思汗，只识弯弓射大雕。",
 "俱往矣，数风流人物，还看今朝。",
]

WORDS = [
 {"w":"莽莽","py":"mǎng mǎng","q":"望长城内外，惟余□□","tip":"叠词，无边无际义；两字均为草字头，读 mǎng"},
 {"w":"滔滔","py":"tāo tāo","q":"大河上下，顿失□□","tip":"叠词，波涛滚滚的水势；均为三点水，读 tāo"},
 {"w":"娆","py":"ráo","q":"须晴日，看红装素裹，分外妖□","tip":"「娆」女字旁，娇艳美好义，读 ráo；勿写「绕」「挠」"},
 {"w":"蜡","py":"là","q":"山舞银蛇，原驰□象","tip":"「蜡」虫字旁，白蜡之白喻高原积雪；勿写「腊」（腊肉义）"},
 {"w":"裹","py":"guǒ","q":"须晴日，看红装素□","tip":"「裹」衣字部中包“果”，包裹义；笔画易漏，读 guǒ"},
 {"w":"骚","py":"sāo","q":"唐宗宋祖，稍逊风□","tip":"「骚」马字旁，风骚指《国风》与《离骚》；勿写「搔」"},
 {"w":"雕","py":"diāo","q":"只识弯弓射大□","tip":"「雕」隹字部，猛禽义；勿写「凋」（凋谢义）"},
 {"w":"骄","py":"jiāo","q":"一代天□，成吉思汗","tip":"「骄」马字旁，天之骄子；勿写「娇」（娇艳义）"},
 {"w":"逊","py":"xùn","q":"唐宗宋祖，稍□风骚","tip":"「逊」走之底，逊色义；勿写「孙」「送」"},
 {"w":"竞","py":"jìng","q":"江山如此多娇，引无数英雄□折腰","tip":"「竞」竞争义；勿写「竟」（竟然义），音同义异"},
 {"w":"输","py":"shū","q":"惜秦皇汉武，略□文采","tip":"「输」车字旁，此处义为差、负；勿写「愉」「榆」"},
]

NOTES = [
 {"w":"北国","a":"北方","q":"北国风光，千里冰封"},
 {"w":"千里冰封","a":"千里江山被冰雪封冻。与“万里雪飘”互文见义，千、万里均虚指","q":"北国风光，千里冰封，万里雪飘"},
 {"w":"惟余","a":"只剩下","q":"望长城内外，惟余莽莽"},
 {"w":"莽莽","a":"无边无际。读 mǎng mǎng","q":"望长城内外，惟余莽莽"},
 {"w":"大河上下","a":"黄河的上游和下游。大河，指黄河","q":"大河上下，顿失滔滔"},
 {"w":"顿失滔滔","a":"（黄河）顿时失去了滔滔水势。指严冬冰封","q":"大河上下，顿失滔滔"},
 {"w":"山舞银蛇","a":"群山披雪绵延起伏，像银蛇在舞动","q":"山舞银蛇，原驰蜡象"},
 {"w":"原驰蜡象","a":"高原丘陵白雪皑皑，像白象在奔驰。原，指秦晋高原","q":"山舞银蛇，原驰蜡象"},
 {"w":"天公","a":"天帝，这里指自然界的主宰","q":"欲与天公试比高"},
 {"w":"试比高","a":"比一比高下","q":"欲与天公试比高"},
 {"w":"须","a":"等到","q":"须晴日，看红装素裹"},
 {"w":"红装素裹","a":"形容雪后天晴，红日和白雪交相辉映的壮丽景色。红装，指红日照耀大地；素裹，指白雪覆盖大地","q":"须晴日，看红装素裹，分外妖娆"},
 {"w":"分外","a":"格外","q":"须晴日，看红装素裹，分外妖娆"},
 {"w":"妖娆","a":"娇艳美好。读 yāo ráo","q":"须晴日，看红装素裹，分外妖娆"},
 {"w":"竞折腰","a":"争着弯腰行礼，倾倒。折腰，鞠躬，倾倒","q":"引无数英雄竞折腰"},
 {"w":"惜","a":"可惜。统领下文七句评点","q":"惜秦皇汉武，略输文采"},
 {"w":"秦皇汉武","a":"秦始皇嬴政和汉武帝刘彻","q":"惜秦皇汉武，略输文采"},
 {"w":"略输文采","a":"文治方面的才华略有欠缺。输，差、负","q":"惜秦皇汉武，略输文采"},
 {"w":"唐宗宋祖","a":"唐太宗李世民和宋太祖赵匡胤","q":"唐宗宋祖，稍逊风骚"},
 {"w":"稍逊风骚","a":"文学才华稍差。风骚，本指《诗经·国风》和《楚辞·离骚》，泛指文章辞藻","q":"唐宗宋祖，稍逊风骚"},
 {"w":"天骄","a":"天之骄子，指天所宠爱的人","q":"一代天骄，成吉思汗"},
 {"w":"成吉思汗","a":"元太祖铁木真。汗，读 hán","q":"一代天骄，成吉思汗，只识弯弓射大雕"},
 {"w":"弯弓","a":"拉开弓","q":"只识弯弓射大雕"},
 {"w":"俱往矣","a":"都过去了。俱，都","q":"俱往矣，数风流人物，还看今朝"},
 {"w":"数","a":"数得上，点数","q":"俱往矣，数风流人物，还看今朝"},
 {"w":"风流人物","a":"建功立业的英雄人物","q":"俱往矣，数风流人物，还看今朝"},
 {"w":"今朝","a":"今天，指当代。朝，读 zhāo","q":"俱往矣，数风流人物，还看今朝"},
]

BG_LEAD = [
 "《沁园春·雪》作于1936年2月。当时毛泽东率红军抗日先锋军东征，行至陕北清涧袁家沟一带，恰逢大雪，登高远眺，面对苍茫雪原，写下这首气吞山河的词作。",
 "1945年重庆谈判期间，毛泽东将此词书赠柳亚子，经《新民报晚刊》刊出后轰动山城，一时和作、评论蜂起，被视为现代诗词史上的重大事件。",
]
AUTHOR = [
 "毛泽东（1893—1976），字润之，湖南湘潭韶山冲人。伟大的无产阶级革命家、战略家、理论家，中国共产党、中国人民解放军和中华人民共和国的主要缔造者和领导人；同时也是独树一帜的诗人、书法家。",
 "他的诗词气势磅礴、意境雄浑，熔历史、现实与理想于一炉，代表作有《沁园春·长沙》《沁园春·雪》《七律·长征》《水调歌头·游泳》等。本篇是其中传播最广、影响最大的作品之一。",
]
STORY = [
 ("东征遇雪","1936年2月，红军东征抗日，毛泽东驻足陕北清涧，一场大雪覆盖秦晋高原。他登上海拔千米、白雪覆盖的塬上视察地形，面对“千里冰封”的北国山河，豪情激荡，遂成此词。"),
 ("重庆轰传","1945年8月，毛泽东赴重庆谈判。柳亚子索诗，毛泽东手书此词相赠。11月《新民报晚刊》刊出后，山城纸贵——人们从词中看到一个政党领袖的胸襟与文采，民心向背自此可见。"),
 ("柳亚子盛赞","柳亚子读后和词一阕，推为“千古绝唱”：“展读之余，叹为中国有词以来第一作手，虽苏、辛未能抗手。”此评虽属过誉，却道出了此词在词史上的冲击力。"),
]
VIDEOS = [("《沁园春·雪》方明朗诵","BV1dW411B7Wc","视频欣赏：《沁园春·雪》朗诵 方明"),
          ("康辉等诗朗诵《沁园春·雪》","BV1Tx42127mH","康辉等诗朗诵《沁园春·雪》")]

APP_PEOPLE = [
 ("顶天立地的历史主人","词中的抒情主人公，立于千里雪原之巅：他“望”长城大河，“看”红装素裹，与天公“试比高”，历数千古帝王而从容评点，最后一句“还看今朝”把历史的笔递给了当代人民。这是一位自信、豪迈、以天下为己任的时代巨人的形象——景之壮与人之豪互为表里。"),
]
APP_ART = [
 ("写景、议论、抒情熔于一炉","上阕纯是写景，末句已伏赞叹之情；下阕借“江山多娇”过渡，转入议论人物，而“惜”字“数”字无不带着感情。景为情设，史为情用，三者在“风流人物”处汇合，浑然一体。"),
 ("化静为动，虚实相生","“山舞银蛇，原驰蜡象”把静景写活；“须晴日，看红装素裹”由眼前实景宕开，悬想放晴之艳。实景壮，虚景艳，一动一静、一实一虚之间，雪原有了完整的生命。"),
 ("以“望”“惜”“数”领起，章法谨严","“望”字统领上阕四句写景，“惜”字统领下阕七句评点，“数”字收束全篇——领字如纲，提挈全词。上阕写空间之广，下阕写时间之远，一纵一横，格局宏大。"),
 ("用词精当，分寸极严","评点帝王，“略输”“稍逊”“只识”层层加码而各有分寸：对秦皇汉武是惋惜，对成吉思汗是近乎否定。褒不虚美，贬不抹杀，大笔墨中见大手笔。"),
]
APP_FAME = [
 ("山舞银蛇，原驰蜡象，欲与天公试比高。","写静景的千古名句。群山高原披雪而“舞”而“驰”，一静物世界霎时奔腾起来；“欲与天公试比高”再翻一层，把山河的生机写成与天争胜的豪气。景中有人，物我交融，是毛泽东诗词雄浑风格的典型代表。"),
 ("江山如此多娇，引无数英雄竞折腰。","承上启下的枢纽句。上半收束上阕雪景，下半开启下阕议论——一个“引”字，把江山之美与英雄之逐绾合为一：正因为江山如此可爱，才值得无数英雄为之倾倒、为之奋斗。过片毫不着力而天堑变通途。"),
 ("俱往矣，数风流人物，还看今朝。","全词的最强音。三字“俱往矣”挥别千年帝王史，“还看今朝”掷地有声地宣告：历史的真正创造者是当代人民。此句一出，全词境界顿升——它超越了个人咏怀，成为对时代主人的礼赞。"),
]
APP_THEME = [
 "上阕描绘北国壮丽雪景，展示山河之壮美；下阕纵论历代英雄，抒发对当代革命人民的赞美——全词以宏大的气魄，唱出了对祖国江山的无限热爱和对改造世界的历史主人的坚定自信。",
 "这首词最动人处，在于景、史、情的高度统一：雪景之壮是山河之壮，评点之豪是自信之豪，“还看今朝”的宣告，把对祖国山河的爱升华为对时代与人民的信念。读此词，当读出那份立于天地之间的浩然之气。",
]

ACC = [
 ("文体与词牌", [
   ("词","兴起于唐代、盛行于宋代的一种诗体，句式长短不一，依词牌填写。又称“长短句”。"),
   ("沁园春","词牌名。相传东汉窦宪仗势夺取沁水公主园林，后人作诗以咏其事，遂有此调。双调，一百十四字。上阕十三句，下阕十二句。"),
   ("上下阕","词的一段叫一阕（或一片）。上阕多写景，下阕多抒情议论；上下阕交接处的句子称“过片”，本词过片即“江山如此多娇”一句。"),
 ]),
 ("易错用字", [
   ("惟余莽莽","教材用“惟余”，不作“唯余”。惟，只、仅。"),
   ("原驰蜡象","教材用“蜡象”（白蜡之白），不作“腊象”。"),
   ("红装素裹","教材用“装”，不作“妆”；“分外妖娆”不作“纷外”。"),
   ("成吉思汗","“汗”读 hán，不读 hàn；“朝”在“今朝”中读 zhāo。"),
 ]),
 ("修辞与手法", [
   ("互文","“千里冰封，万里雪飘”上下文义互相交错补充：千万里江山或冰封或雪飘。"),
   ("化静为动","“山舞银蛇，原驰蜡象”，把静止的群山高原写成舞动的银蛇、奔驰的蜡象。"),
   ("比喻","以银蛇、蜡象喻披雪之山原，以红装素裹喻雪霁红日。"),
   ("对偶","“长城内外”对“大河上下”，“惟余莽莽”对“顿失滔滔”，“山舞银蛇”对“原驰蜡象”。"),
 ]),
 ("文化常识", [
   ("秦皇汉武","秦始皇嬴政统一六国，汉武帝刘彻开疆拓土，皆为武功盖世的君主。"),
   ("唐宗宋祖","唐太宗李世民开创贞观之治，宋太祖赵匡胤结束五代分裂。"),
   ("成吉思汗","元太祖铁木真，统一蒙古各部，建立蒙古汗国，曾远征欧亚。“汗”意为君主，读 hán。"),
   ("风骚","本指《诗经》中的《国风》与《楚辞》中的《离骚》，后代指文学才华。"),
   ("风流人物","建功立业的英雄人物。此处特指能主宰历史、创造新时代的当代人民。"),
 ]),
]

# ================= 组装 =================
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]
main_js, dict_js = re.findall(r"<script>\n(.*?)</script>", src, re.S)
main_js = main_js.replace("beiying_fs", LS_KEY)
dict_js = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", dict_js, flags=re.S)
dict_js = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", dict_js, flags=re.S)

CN = "一二"
hero = '<header class="hero">\n  <div class="hero-side">现代 · 毛泽东</div>\n  <h1 class="hero-title">沁园春·雪</h1>\n</header>'
nav = '<nav class="nav"><div class="nav-in"><a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a><div class="tool"><select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option></select><button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button></div></div></nav>'

def video(i, h4, bvid, atitle):
    return ('<div class="media"><h4>%s</h4>'
            '<iframe id="mediaF%d" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>'
            '<a href="https://www.bilibili.com/video/%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF%d">全屏播放</button></div>'
            % (h4, i, bvid, atitle, bvid, i))

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
      '<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>',
      '<div class="sec-sub">上阕写北国雪景，下阕评古论今。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>',
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
       '<div class="box"><h3>形象赏析</h3><p style="margin-bottom:14px;color:var(--ink2)">词中的“形象”是立于千里雪原之巅、俯仰古今的抒情主人公。</p><div class="fame">']
for t, p in APP_PEOPLE: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>艺术特色</h3><div class="fame">')
for t, p in APP_ART: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>名句赏析</h3><div class="fame">')
for t, p in APP_FAME: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>主题思想</h3>')
for p in APP_THEME: app.append('<p>' + p + '</p>')
app.append('</div></section>')

acc = ['<div class="divider"></div>', '<section id="acc" class="sec">',
       '<div class="sec-head"><h2>积 累</h2><span class="no">词牌 · 易错用字 · 修辞 · 文化常识</span></div>']
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
footer = '<footer>\n  <div class="kai">《沁园春·雪》</div>\n  <div>毛泽东 · 1936年2月作于陕北 · 1945年发表于重庆</div>\n</footer>'
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

html_doc = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>《沁园春·雪》毛泽东</title>\n<style>' + css + '</style>\n</head>\n<body data-fs="100">\n\n'
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
print("沁园春·雪 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), html_doc.count('class="anno-word"'), len(WORDS), len(NOTES), len(html_doc.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html_doc)
print("OK ->", OUT)
