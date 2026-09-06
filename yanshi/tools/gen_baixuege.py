# -*- coding: utf-8 -*-
"""《白雪歌送武判官归京》课件生成器 —— 复用《背影》CSS/JS框架。"""
import json, re, html, io, os
LQ='\u201c';RQ='\u201d'
SRC=os.path.join(os.path.dirname(os.path.abspath(__file__)),'beiying-zhuziqing.html')
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'baixuegesongwupanguanguijing-censhen.html')
src=io.open(SRC,encoding='utf-8-sig').read()
CSS=src[src.index('<style>')+7:src.index('</style>')]
CSS+='\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0=src.index('<script>');JS=src[s0+8:src.index('</script>',s0)]
JS=JS.replace('beiying_fs','baixuege_fs')
def annotate(text):
    def rep(m):
        w,n=m.group(1),m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>'%(html.escape(n,quote=True),w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]',rep,text)
def fixq(s):return s.replace('~L~',LQ).replace('~R~',RQ)

FULLTEXT=[
    "北风卷地白草折，胡天八月即飞雪。",
    "忽如一夜春风来，千树万树梨花开。",
    "散入珠帘湿罗幕，狐裘不暖锦衾薄。",
    "将军角弓不得控，都护铁衣冷难着。",
    "瀚海阑干百丈冰，愁云惨淡万里凝。",
    "中军置酒饮归客，胡琴琵琶与羌笛。",
    "纷纷暮雪下辕门，风掣红旗冻不翻。",
    "轮台东门送君去，去时雪满天山路。",
    "山回路转不见君，雪上空留马行处。",
]
PARTS=[
    ("第一部分","咏雪 · 胡天飞雪","第 1–10 句",
     fixq("前十句写边塞雪景。~L~北风卷地白草折，胡天八月即飞雪~R~，写北风席卷大地，白草被吹折，胡地八月就下起了大雪。~L~忽如一夜春风来，千树万树梨花开~R~，以梨花喻雪，是千古传诵的名句。~L~散入珠帘湿罗幕~R~四句写军营中的苦寒，狐裘不暖，锦衾嫌薄，将军角弓拉不开，都护铁衣难穿上。~L~瀚海阑干百丈冰，愁云惨淡万里凝~R~，写大漠上坚冰纵横，万里愁云凝聚，为下文送别渲染了悲凉的气氛。")),
    ("第二部分","饯别 · 中军置酒","第 11–14 句",
     fixq("~L~中军置酒饮归客，胡琴琵琶与羌笛~R~，写在中军帐中摆酒为归客饯行，胡琴琵琶羌笛合奏，以乐助兴。~L~纷纷暮雪下辕门，风掣红旗冻不翻~R~，写傍晚时分大雪纷纷扬扬落在辕门，红旗被冻住了，风也吹不动它。~L~冻不翻~R~三字，写出了边塞的奇寒，是炼字的经典。")),
    ("第三部分","送别 · 雪空留马","第 15–18 句",
     fixq("~L~轮台东门送君去，去时雪满天山路~R~，写在轮台东门外送友人归去，离去时大雪铺满了天山的道路。~L~山回路转不见君，雪上空留马行处~R~，写山路曲折，友人的身影渐渐消失，雪地上只留下马蹄的痕迹。~L~空留~R~二字，写出了诗人对友人的依依惜别之情和送别后的怅惘，余味无穷。")),
]
S=[
(0,"[[北风|寒冷的北方大风。北，北方；风，大风]][[卷地|席卷大地。卷，席卷；地，大地]][[白草|（bái cǎo）西北边塞一种草名，干枯后变白，性坚韧。白，白色；草，草类]]折，[[胡天|胡人的天空，指西北地区。胡，古代对北方少数民族的称呼]]八月即[[飞雪|下雪。飞，飞舞；雪，雪花]]。",
 "北风席卷大地，白草被吹折了；胡地的八月，就已经下起了大雪。",
 fixq("开篇即写边塞的奇寒。~L~北风卷地~R~写北风的猛烈，~L~卷地~R~二字写出了北风席卷大地的气势。~L~白草折~R~写白草被吹折，白草是西北边塞的一种草，干枯后变白，性坚韧，连坚韧的白草都被吹折了，可见北风的猛烈。~L~胡天八月即飞雪~R~，~L~即~R~字用得极妙——中原八月还是秋天，胡地八月就已经下雪了，一个~L~即~R~字写出了边塞气候的反常和寒冷。这两句为下文~L~忽如一夜春风来~R~的奇喻做了铺垫，也为全诗奠定了苦寒的基调。"),
 ["起笔","苦寒","铺垫"]),
(0,"[[忽如|忽然好像。忽，忽然；如，好像]]一夜春风来，千树万树[[梨花|梨树的花，春天开放，白色。这里以梨花喻雪]]开。",
 "忽然好像一夜春风吹来，千树万树的梨花都盛开了。",
 fixq("这是千古传诵的名句，以梨花喻雪，想象奇特，意境优美。~L~忽如一夜春风来~R~，写大雪来得突然，好像一夜之间春风吹来了。~L~千树万树梨花开~R~，写大雪覆盖了千树万树，好像梨花盛开一样。以梨花喻雪，既写出了雪的洁白，又写出了雪的繁盛，更写出了诗人的惊喜之情——在苦寒的边塞，大雪居然带来了春天般的美好想象。这个比喻将萧瑟的冬景写成了烂漫的春景，将寒冷的雪景写成了温暖的花景，体现了诗人乐观豪迈的精神。~L~忽如~R~二字写出了大雪来得突然，~L~千树万树~R~写出了雪的繁盛，~L~梨花~R~写出了雪的洁白。这一句是中国古典诗歌中最著名的咏雪名句。"),
 ["比喻","名句","奇喻","乐观豪迈"]),
(0,"[[散入|飘入、洒入。散，飘散；入，进入]][[珠帘|用珍珠装饰的帘子。珠，珍珠；帘，帘子]][[湿|打湿、沾湿]][[罗幕|（luó mù）用丝织品做的帷幕。罗，丝织品；幕，帷幕]]，[[狐裘|（hú qiú）用狐狸皮做的皮衣。狐，狐狸；裘，皮衣]]不暖[[锦衾|（jǐn qīn）用锦缎做的被子。锦，锦缎；衾，被子]]薄。",
 "雪花飘入珠帘，沾湿了罗幕；狐裘不够暖和，锦被也显得单薄。",
 fixq("这两句写军营中的苦寒。~L~散入珠帘湿罗幕~R~，写雪花飘入珠帘，沾湿了罗幕——~L~散入~R~写雪花轻盈地飘入，~L~湿~R~写雪花融化后沾湿了罗幕，连帐篷里都进了雪，可见雪之大。~L~狐裘不暖锦衾薄~R~，写狐裘不够暖和，锦被也显得单薄——狐裘是用狐狸皮做的皮衣，非常保暖；锦衾是用锦缎做的被子，非常厚实。连狐裘和锦衾都觉得不暖和、单薄，可见边塞的寒冷。这两句从人的感受写寒冷，比直接写~L~天冷~R~更有感染力。"),
 ["苦寒","侧面描写","感受"]),
(0,"将军[[角弓|（jiǎo gōng）用兽角装饰的弓。角，兽角；弓，弓箭]]不得[[控|（kòng）拉开、拉弓。控，拉弓]]，[[都护|（dū hù）唐代边疆最高军事长官]][[铁衣|用铁片做的铠甲。铁，铁片；衣，衣服、铠甲]]冷难[[着|（zhuó）穿、穿上。着，穿]]。",
 "将军的角弓冻得拉不开，都护的铁衣冷得难以穿上。",
 fixq("这两句继续写边塞的苦寒，从将军和都护的角度写寒冷。~L~将军角弓不得控~R~，写将军的角弓冻得拉不开——角弓是用兽角装饰的弓，是将军的武器，连武器都用不了了，可见寒冷之甚。~L~都护铁衣冷难着~R~，写都护的铁衣冷得难以穿上——铁衣是用铁片做的铠甲，在寒冷的天气里，铁片冰凉刺骨，难以穿上。这两句与上两句~L~狐裘不暖锦衾薄~R~形成对仗，从衣被到武器，从士兵到将军，全方位地写出了边塞的苦寒。~L~不得控~R~~L~冷难着~R~，语言朴素，但感染力极强。"),
 ["对仗","苦寒","夸张"]),
(0,"[[瀚海|（hàn hǎi）大沙漠。瀚，广大；海，这里指沙漠如大海般广阔]][[阑干|（lán gān）纵横交错的样子。阑，残、尽；干，纵横]][[百丈|极言其高，虚指。百，数词；丈，长度单位]]冰，[[愁云|使人发愁的云。愁，忧愁；云，云彩]][[惨淡|（cǎn dàn）阴暗、昏暗。惨，凄凉；淡，暗淡]]万里[[凝|凝聚、凝结]]。",
 "大沙漠上坚冰纵横交错，有百丈之厚；万里长空，愁云暗淡，凝聚不散。",
 fixq("这两句写大漠雪景，为下文送别渲染了悲凉的气氛。~L~瀚海阑干百丈冰~R~，写大沙漠上坚冰纵横交错，有百丈之厚——~L~瀚海~R~是大沙漠，~L~阑干~R~是纵横交错的样子，~L~百丈~R~是虚指，极言冰之厚。~L~愁云惨淡万里凝~R~，写万里长空，愁云暗淡，凝聚不散——~L~愁云~R~是使人发愁的云，~L~惨淡~R~是阴暗的样子，~L~万里凝~R~是万里长空都凝聚着愁云。这两句既是写景，也是抒情——~L~愁云~R~二字，将诗人的离愁别绪融入了景物之中，为下文~L~中军置酒饮归客~R~的送别渲染了悲凉的气氛。~L~百丈冰~R~与~L~万里凝~R~对仗工整，气势雄浑。"),
 ["写景","渲染","对仗","情景交融"]),
(1,"[[中军|古代军队的中军营帐，是主帅所在的地方。中，中间；军，军营]][[置酒|摆酒、设酒宴。置，设置、摆放；酒，酒宴]][[饮归客|（yìn guī kè）让归客饮酒。饮，使……饮酒，使动用法；归客，归去的客人，指武判官]]，[[胡琴|（hú qín）古代北方少数民族的弦乐器]]琵琶与[[羌笛|（qiāng dí）古代羌族的管乐器。羌，古代少数民族；笛，笛子]]。",
 "在中军帐中摆酒，为归客饯行；胡琴、琵琶、羌笛合奏，以乐助兴。",
 fixq("这两句写饯别场面。~L~中军置酒饮归客~R~，写在中军帐中摆酒为归客饯行——~L~中军~R~是主帅所在的中军营帐，~L~置酒~R~是摆酒，~L~饮归客~R~是让归客饮酒，~L~饮~R~是使动用法，~L~使……饮酒~R~的意思。~L~胡琴琵琶与羌笛~R~，写宴会上演奏的乐器——胡琴、琵琶、羌笛都是西域少数民族的乐器，在边塞的中军帐中，用这些乐器演奏，既有边塞特色，也增添了饯别的悲凉气氛。这两句由写景转入叙事，由咏雪转入送别，过渡自然。"),
 ["叙事","饯别","使动用法","过渡"]),
(1,"[[纷纷|（fēn fēn）多而杂乱的样子，形容雪下得大。纷，多、杂乱]][[暮雪|傍晚的雪。暮，傍晚；雪，雪花]]下[[辕门|（yuán mén）军营的大门。辕，车前驾牲畜的木杆；古代军营前以两车之辕相向为门，故称辕门]]，[[风掣|（fēng chè）风拉扯、风吹。掣，拉、拽]]红旗[[冻不翻|（dòng bù fān）冻住了不能翻动。冻，结冰；不翻，不能翻动]]。",
 "傍晚时分，大雪纷纷扬扬落在辕门；红旗被冻住了，风也吹不动它。",
 fixq("这两句写辕门外的雪景，是炼字的经典。~L~纷纷暮雪下辕门~R~，写傍晚时分大雪纷纷扬扬落在辕门——~L~纷纷~R~写雪下得大，~L~暮雪~R~点明时间是傍晚，~L~辕门~R~是军营的大门。~L~风掣红旗冻不翻~R~，写红旗被冻住了，风也吹不动它——~L~掣~R~是拉、拽的意思，~L~风掣~R~是风拉扯着红旗，~L~冻不翻~R~是红旗被冻住了不能翻动。~L~冻不翻~R~三字用得极妙：在大风中，红旗本来应该随风翻卷，但因为天气太冷，红旗被冻住了，连风都吹不动。这三个字以动写静，将边塞的奇寒写到了极致。在一片白雪之中，一面红旗被冻住，色彩鲜明，画面感极强。"),
 ["炼字","名句","以动写静","色彩"]),
(2,"[[轮台|（lún tái）古地名，在今新疆米泉一带，唐代北庭都护府所在地]]东门送[[君|你，这里指武判官]]去，去时[[雪满|大雪铺满。雪，大雪；满，铺满]]天山路。",
 "在轮台的东门外送你归去；离去的时候，大雪铺满了天山的道路。",
 fixq("这两句写送别的地点和场景。~L~轮台东门送君去~R~，写在轮台的东门外送友人归去——~L~轮台~R~是古地名，在今新疆米泉一带，是唐代北庭都护府所在地，岑参当时在此任职。~L~东门~R~点明送别的地点，~L~送君去~R~点明送别的主题。~L~去时雪满天山路~R~，写离去的时候大雪铺满了天山的道路——~L~雪满~R~写雪之大，~L~天山路~R~写友人归去的道路。大雪铺满了天山的道路，既写出了边塞的奇寒，也暗示了友人归去的艰难，更写出了诗人对友人的担忧和不舍。这两句由饯别转入送别，过渡自然。"),
 ["送别","叙事","过渡"]),
(2,"[[山回路转|（shān huí lù zhuǎn）山势回环，道路曲折。山回，山势回环；路转，道路曲折]]不见君，雪上[[空留|白白地留下。空，白白地、徒然；留，留下]][[马行处|（mǎ xíng chù）马蹄走过的痕迹。马行，马走过；处，地方、痕迹]]。",
 "山势回环，道路曲折，再也看不见你的身影；雪地上只留下了马蹄走过的痕迹。",
 fixq("末二句是全诗的点睛之笔，写送别后的怅惘。~L~山回路转不见君~R~，写山路曲折，友人的身影渐渐消失，再也看不见了——~L~山回路转~R~写山势回环、道路曲折，~L~不见君~R~写友人的身影消失了。~L~雪上空留马行处~R~，写雪地上只留下了马蹄走过的痕迹——~L~空留~R~二字用得极妙，~L~空~R~是白白地、徒然的意思，~L~空留~R~写出了诗人目送友人远去，友人消失后，雪地上只留下马蹄印的怅惘和失落。这两句以景结情，不直接写离愁，而离愁自见——友人已经远去，诗人还伫立在雪中，望着雪地上的马蹄印发呆。~L~空留~R~二字，将依依惜别之情和送别后的怅惘写得淋漓尽致，余味无穷。"),
 ["以景结情","炼字","名句","余味无穷"]),
]
DICT_WORDS=[
    {"w":"折","py":"zhé","q":"北风卷地白草□，胡天八月即飞雪","tip":fixq("「折」提手旁，音 zhé，折断、弯曲，~L~白草折~R~即白草被吹折，勿读 shé（折本）~L~拆~R~（拆开）")},
    {"w":"即","py":"jí","q":"胡天八月□飞雪","tip":fixq("「即」卩字旁，音 jí，就、便，~L~即飞雪~R~即就下起了大雪，勿写~L~既~R~（既然，右边不同）")},
    {"w":"裘","py":"qiú","q":"散入珠帘湿罗幕，狐□不暖锦衾薄","tip":fixq("「裘」衣字旁，音 qiú，皮衣，~L~狐裘~R~即狐狸皮做的皮衣，勿写~L~袭~R~（袭击，龙字头）")},
    {"w":"衾","py":"qīn","q":"狐裘不暖锦□薄","tip":fixq("「衾」衣字旁，音 qīn，被子，~L~锦衾~R~即锦缎做的被子，勿写~L~裘~R~（皮衣）~L~枕~R~（枕头，木字旁）")},
    {"w":"掣","py":"chè","q":"纷纷暮雪下辕门，风□红旗冻不翻","tip":fixq("「掣」手字旁，音 chè，拉、拽，~L~风掣~R~即风拉扯着，勿写~L~制~R~（制造）~L~挚~R~（真挚，手字旁）")},
    {"w":"辕","py":"yuán","q":"纷纷暮雪下□门，风掣红旗冻不翻","tip":fixq("「辕」车字旁，音 yuán，车前驾牲畜的木杆，~L~辕门~R~即军营大门，勿写~L~园~R~（花园，口字框）")},
    {"w":"瀚","py":"hàn","q":"□海阑干百丈冰，愁云惨淡万里凝","tip":fixq("「瀚」三点水，音 hàn，广大，~L~瀚海~R~即大沙漠，勿写~L~翰~R~（文翰，羽字旁）~L~悍~R~（强悍，竖心旁）")},
    {"w":"阑","py":"lán","q":"瀚海□干百丈冰，愁云惨淡万里凝","tip":fixq("「阑」门字框，音 lán，残、尽，~L~阑干~R~即纵横交错，勿写~L~澜~R~（波澜，三点水）~L~兰~R~（兰花）")},
    {"w":"惨","py":"cǎn","q":"瀚海阑干百丈冰，愁云□淡万里凝","tip":fixq("「惨」竖心旁，音 cǎn，凄凉、暗淡，~L~惨淡~R~即阴暗，勿写~L~渗~R~（渗透，三点水）")},
    {"w":"凝","py":"níng","q":"瀚海阑干百丈冰，愁云惨淡万里□","tip":fixq("「凝」两点水，音 níng，凝聚、凝结，~L~万里凝~R~即万里凝聚，勿写~L~疑~R~（怀疑，匕字头）")},
    {"w":"羌","py":"qiāng","q":"中军置酒饮归客，胡琴琵琶与□笛","tip":fixq("「羌」羊字头，音 qiāng，古代少数民族，~L~羌笛~R~即羌族的笛子，勿写~L~姜~R~（生姜，女字底）")},
]
DICT_NOTES=[
    {"w":"卷地","q":"北风卷地白草折","a":"席卷大地。卷，席卷；地，大地"},
    {"w":"白草","q":"北风卷地白草折","a":"（bái cǎo）西北边塞一种草名，干枯后变白，性坚韧"},
    {"w":"胡天","q":"胡天八月即飞雪","a":"胡人的天空，指西北地区。胡，古代对北方少数民族的称呼"},
    {"w":"即","q":"胡天八月即飞雪","a":"（jí）就、便"},
    {"w":"忽如","q":"忽如一夜春风来","a":"忽然好像。忽，忽然；如，好像"},
    {"w":"梨花","q":"千树万树梨花开","a":"梨树的花，春天开放，白色。这里以梨花喻雪"},
    {"w":"散入","q":"散入珠帘湿罗幕","a":"飘入、洒入。散，飘散；入，进入"},
    {"w":"珠帘","q":"散入珠帘湿罗幕","a":"用珍珠装饰的帘子。珠，珍珠；帘，帘子"},
    {"w":"罗幕","q":"散入珠帘湿罗幕","a":"（luó mù）用丝织品做的帷幕。罗，丝织品；幕，帷幕"},
    {"w":"狐裘","q":"狐裘不暖锦衾薄","a":"（hú qiú）用狐狸皮做的皮衣。狐，狐狸；裘，皮衣"},
    {"w":"锦衾","q":"狐裘不暖锦衾薄","a":"（jǐn qīn）用锦缎做的被子。锦，锦缎；衾，被子"},
    {"w":"角弓","q":"将军角弓不得控","a":"（jiǎo gōng）用兽角装饰的弓。角，兽角；弓，弓箭"},
    {"w":"控","q":"将军角弓不得控","a":"（kòng）拉开、拉弓"},
    {"w":"都护","q":"都护铁衣冷难着","a":"（dū hù）唐代边疆最高军事长官"},
    {"w":"铁衣","q":"都护铁衣冷难着","a":"用铁片做的铠甲。铁，铁片；衣，铠甲"},
    {"w":"着","q":"都护铁衣冷难着","a":"（zhuó）穿、穿上"},
    {"w":"瀚海","q":"瀚海阑干百丈冰","a":"（hàn hǎi）大沙漠。瀚，广大；海，指沙漠如大海般广阔"},
    {"w":"阑干","q":"瀚海阑干百丈冰","a":"（lán gān）纵横交错的样子"},
    {"w":"惨淡","q":"愁云惨淡万里凝","a":"（cǎn dàn）阴暗、昏暗。惨，凄凉；淡，暗淡"},
    {"w":"凝","q":"愁云惨淡万里凝","a":"（níng）凝聚、凝结"},
    {"w":"中军","q":"中军置酒饮归客","a":"古代军队的中军营帐，主帅所在的地方"},
    {"w":"置酒","q":"中军置酒饮归客","a":"摆酒、设酒宴。置，设置、摆放；酒，酒宴"},
    {"w":"饮归客","q":"中军置酒饮归客","a":"（yìn guī kè）让归客饮酒。饮，使……饮酒，使动用法；归客，归去的客人"},
    {"w":"胡琴","q":"胡琴琵琶与羌笛","a":"（hú qín）古代北方少数民族的弦乐器"},
    {"w":"羌笛","q":"胡琴琵琶与羌笛","a":"（qiāng dí）古代羌族的管乐器。羌，古代少数民族；笛，笛子"},
    {"w":"纷纷","q":"纷纷暮雪下辕门","a":"（fēn fēn）多而杂乱的样子，形容雪下得大"},
    {"w":"辕门","q":"纷纷暮雪下辕门","a":"（yuán mén）军营的大门。古代军营前以两车之辕相向为门"},
    {"w":"风掣","q":"风掣红旗冻不翻","a":"（fēng chè）风拉扯、风吹。掣，拉、拽"},
    {"w":"冻不翻","q":"风掣红旗冻不翻","a":"（dòng bù fān）冻住了不能翻动。冻，结冰；不翻，不能翻动"},
    {"w":"轮台","q":"轮台东门送君去","a":"（lún tái）古地名，在今新疆米泉一带，唐代北庭都护府所在地"},
    {"w":"君","q":"轮台东门送君去","a":"你，这里指武判官"},
    {"w":"雪满","q":"去时雪满天山路","a":"大雪铺满。雪，大雪；满，铺满"},
    {"w":"山回路转","q":"山回路转不见君","a":"（shān huí lù zhuǎn）山势回环，道路曲折"},
    {"w":"空留","q":"雪上空留马行处","a":"白白地留下。空，白白地、徒然；留，留下"},
    {"w":"马行处","q":"雪上空留马行处","a":"（mǎ xíng chù）马蹄走过的痕迹。马行，马走过；处，地方、痕迹"},
]
def build_verses():
    out,idx=[],0
    for pi,part in enumerate(PARTS):
        out.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>'%(part[0],part[1],part[2]))
        out.append('      <div class="part-overview">%s</div>'%fixq(part[3]))
        for(p,txt,yi,shang,tags)in S:
            if p!=pi:continue
            idx+=1
            out.append('      <div class="verse" id="l%d" data-i="%d">'%(idx,idx-1))
            out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>'%(idx,annotate(txt)))
            out.append('        <details class="v-more"><summary>译文 · 赏析</summary><div class="d-body">')
            out.append('            <div class="v-sec"><b class="v-label">译　文</b><div class="v-trans">%s</div></div>'%yi)
            out.append('            <div class="v-sec"><b class="v-label">赏　析</b><div class="d-body"><p>%s</p></div>'%shang)
            if tags:out.append('              <div class="tags">%s</div>'%''.join('<span>%s</span>'%t for t in tags))
            out.append('            </div></div></details></div>')
    return '\n'.join(out),idx
verses_html,total=build_verses()
full_html='\n'.join('    <div class="pl">%s</div>'%p for p in FULLTEXT)
anno_count=sum(txt.count('[[') for(_,txt,_,_,_)in S)
BG=fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《白雪歌送武判官归京》是唐代边塞诗人岑参的代表作，作于唐玄宗天宝十三载（754）。当时岑参第二次出塞，任安西北庭节度使封常清的判官，在轮台（今新疆米泉）送友人武判官归京，写下了这首千古传诵的七言古诗。</p>
    <p>全诗以~L~白雪歌~R~为题，既是咏雪，也是送别。前十句写边塞雪景——北风飞雪、忽如春风、军营苦寒、瀚海愁云；中间四句写饯别——中军置酒、胡琴琵琶、暮雪辕门、风掣红旗；末四句写送别——轮台东门、雪满天山、山回路转、雪空留马。~L~忽如一夜春风来，千树万树梨花开~R~是千古传诵的咏雪名句，~L~山回路转不见君，雪上空留马行处~R~是千古传诵的送别名句。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>岑参（约715—770），唐代著名边塞诗人，荆州江陵（今湖北荆州）人。官至嘉州刺史，世称~L~岑嘉州~R~。他与高适并称~L~高岑~R~，是盛唐边塞诗派的代表人物。</p>
    <p>岑参曾两次出塞，第一次在天宝八载（749）赴安西，第二次在天宝十三载（754）赴北庭。六年的边塞生活，使他对边塞的风光和战争有了深刻的体验，也为他的诗歌创作提供了丰富的素材。他的边塞诗气势雄浑、想象奇特、色彩瑰丽，代表作有《白雪歌送武判官归京》《走马川行奉送出师西征》《轮台歌奉送封大夫出师西征》等。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>两次出塞：</b>岑参一生曾两次出塞。第一次在天宝八载（749），任安西节度使高仙芝的掌书记；第二次在天宝十三载（754），任安西北庭节度使封常清的判官。《白雪歌送武判官归京》即作于第二次出塞期间，当时岑参在轮台任职。</p>
    <p><b>送别武判官：</b>武判官是岑参的友人，姓名不详，~L~判官~R~是唐代节度使的属官。武判官要归京（回长安），岑参在轮台为他送行，写下了这首诗。诗中既有对边塞雪景的描写，也有对友人的依依惜别之情。</p>
    <p><b>盛唐气象：</b>开元天宝年间是唐朝的全盛时期，国力强盛，疆域辽阔，文人普遍有出塞从戎的热情。岑参的边塞诗虽然写了边塞的苦寒，但诗中充满了乐观豪迈的精神和雄浑壮丽的气象，是盛唐气象的生动写照。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《白雪歌送武判官归京》是一首<b>七言古诗</b>（七言古体诗），全诗十八句，每句七字，共一百二十六字。不同于七言律诗的严格格律，七言古诗不拘平仄粘对，形式自由，节奏明快，适合表现雄浑壮阔的内容。</p>
    <p>诗题~L~白雪歌送武判官归京~R~，~L~白雪歌~R~是歌咏白雪的歌，~L~送武判官归京~R~是送武判官回京城。全诗将咏雪与送别融为一体，是一首边塞送别诗。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>《白雪歌送武判官归京》诵读（诵读客）</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1FV4y1F7N8&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="白雪歌朗诵"></iframe>
        <a href="https://www.bilibili.com/video/BV1FV4y1F7N8" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>《白雪歌送武判官归京》奇然/沈谧仁 演唱</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1Ps4y1g7q6&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="白雪歌歌曲"></iframe>
        <a href="https://www.bilibili.com/video/BV1Ps4y1g7q6" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')
APP=fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>
  <div class="box">
    <h3>抒情主人公形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">岑参——乐观豪迈的边塞诗人</div>
        <p>《白雪歌送武判官归京》中的抒情主人公，是一位乐观豪迈、重情重义的边塞诗人形象。他虽然身处苦寒的边塞，但面对壮丽的雪景，充满了惊喜和赞叹；送别友人时，又充满了依依惜别之情。</p>
        <p><b>乐观豪迈：</b>~L~忽如一夜春风来，千树万树梨花开~R~，在苦寒的边塞，大雪居然带来了春天般的美好想象。诗人以梨花喻雪，将萧瑟的冬景写成了烂漫的春景，体现了乐观豪迈的精神。</p>
        <p><b>重情重义：</b>~L~山回路转不见君，雪上空留马行处~R~，友人已经远去，诗人还伫立在雪中，望着雪地上的马蹄印发呆。~L~空留~R~二字，写出了诗人对友人的依依惜别之情和送别后的怅惘。</p>
        <p>这个形象，既有边塞诗人的雄浑豪迈，又有送别人的深情厚谊，是盛唐边塞诗人的典型写照。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">想象奇特——忽如一夜春风来</div>
        <p>以梨花喻雪，是中国古典诗歌中最著名的比喻之一。大雪覆盖千树万树，好像梨花盛开，既写出了雪的洁白，又写出了雪的繁盛，更写出了诗人的惊喜之情。将萧瑟的冬景写成烂漫的春景，将寒冷的雪景写成温暖的花景，想象奇特，意境优美。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">炼字精妙——冻不翻、空留</div>
        <p>~L~风掣红旗冻不翻~R~的~L~冻不翻~R~三字，以动写静，将边塞的奇寒写到了极致。~L~雪上空留马行处~R~的~L~空留~R~二字，将依依惜别之情和送别后的怅惘写得淋漓尽致。炼字精妙，言简意丰。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">情景交融——咏雪与送别</div>
        <p>全诗将咏雪与送别融为一体。前十句咏雪，为送别渲染了苦寒悲凉的气氛；中间四句饯别，在雪景中摆酒奏乐；末四句送别，在雪景中目送友人远去。雪贯穿全诗，既是写景的对象，也是抒情的载体，情景交融，天衣无缝。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">色彩鲜明——白雪与红旗</div>
        <p>~L~纷纷暮雪下辕门，风掣红旗冻不翻~R~，在一片白雪之中，一面红旗被冻住，色彩鲜明，画面感极强。白雪的洁白与红旗的鲜红形成强烈对比，构成了一幅奇特壮丽的边塞雪景图。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">忽如一夜春风来，千树万树梨花开。</div>
        <p>这是千古传诵的咏雪名句。以梨花喻雪，想象奇特，意境优美。~L~忽如~R~二字写出了大雪来得突然，~L~千树万树~R~写出了雪的繁盛，~L~梨花~R~写出了雪的洁白。在苦寒的边塞，大雪居然带来了春天般的美好想象——将萧瑟的冬景写成了烂漫的春景，将寒冷的雪景写成了温暖的花景，体现了诗人乐观豪迈的精神。这一句是中国古典诗歌中最著名的咏雪名句，千百年来传诵不衰。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">山回路转不见君，雪上空留马行处。</div>
        <p>这是千古传诵的送别名句。山路曲折，友人的身影渐渐消失，雪地上只留下马蹄的痕迹。~L~空留~R~二字用得极妙——~L~空~R~是白白地、徒然的意思，~L~空留~R~写出了诗人目送友人远去，友人消失后，雪地上只留下马蹄印的怅惘和失落。这两句以景结情，不直接写离愁，而离愁自见。友人已经远去，诗人还伫立在雪中，望着雪地上的马蹄印发呆，余味无穷。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>主题思想</h3>
    <p>《白雪歌送武判官归京》通过描写边塞的壮丽雪景和送别友人的场景，抒发了诗人对边塞风光的赞美和对友人的依依惜别之情，体现了盛唐边塞诗人乐观豪迈的精神面貌。</p>
    <p>这首诗的深刻之处在于，它将咏雪与送别融为一体——雪既是写景的对象，也是抒情的载体。前十句的咏雪，为送别渲染了苦寒悲凉的气氛；末四句的送别，在雪景中目送友人远去，~L~雪上空留马行处~R~，将离愁别绪融入了雪景之中。全诗气势雄浑，想象奇特，色彩瑰丽，是盛唐边塞诗的代表作。</p>
  </div>
</section>
''')
ACC=fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 炼字 · 修辞 · 文化常识</span></div>
  <div class="box"><div class="acc-cat"><h3>文体与词牌</h3>
    <div class="acc-item"><span class="acc-w">七言古诗</span><span class="acc-d">《白雪歌送武判官归京》是七言古诗（古体诗），全诗十八句，每句七字，不拘平仄粘对，形式自由。</span></div>
    <div class="acc-item"><span class="acc-w">边塞诗</span><span class="acc-d">以边塞风光、战争生活为题材的诗歌。盛唐边塞诗派代表有高适、岑参、王维、王昌龄等。</span></div>
    <div class="acc-item"><span class="acc-w">送别诗</span><span class="acc-d">以送别友人为题材的诗歌。本诗将咏雪与送别融为一体，是边塞送别诗的代表作。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>易错字音形</h3>
    <div class="acc-item"><span class="acc-w">折</span><span class="acc-d">（zhé）折断，勿读 shé（折本）。</span></div>
    <div class="acc-item"><span class="acc-w">即</span><span class="acc-d">（jí）就，勿写~L~既~R~（jì）。</span></div>
    <div class="acc-item"><span class="acc-w">裘</span><span class="acc-d">（qiú）皮衣，衣字旁，勿写~L~袭~R~。</span></div>
    <div class="acc-item"><span class="acc-w">衾</span><span class="acc-d">（qīn）被子，衣字旁，勿写~L~裘~R~~L~枕~R~。</span></div>
    <div class="acc-item"><span class="acc-w">掣</span><span class="acc-d">（chè）拉、拽，手字旁，勿写~L~制~R~~L~挚~R~。</span></div>
    <div class="acc-item"><span class="acc-w">辕</span><span class="acc-d">（yuán）车字旁，~L~辕门~R~即军营大门，勿写~L~园~R~。</span></div>
    <div class="acc-item"><span class="acc-w">瀚</span><span class="acc-d">（hàn）三点水，~L~瀚海~R~即大沙漠，勿写~L~翰~R~（羽字旁）。</span></div>
    <div class="acc-item"><span class="acc-w">羌</span><span class="acc-d">（qiāng）羊字头，古代少数民族，勿写~L~姜~R~。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>文言梳理</h3>
    <div class="acc-sub">古今异义</div>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">白草</td><td>西北边塞一种草名</td><td>白色的草（泛指）</td><td>北风卷地白草折</td></tr>
      <tr><td class="kai">胡天</td><td>胡人的天空，指西北地区</td><td>胡人的天空（狭义）</td><td>胡天八月即飞雪</td></tr>
      <tr><td class="kai">瀚海</td><td>大沙漠</td><td>浩瀚的海洋</td><td>瀚海阑干百丈冰</td></tr>
      <tr><td class="kai">中军</td><td>中军营帐，主帅所在</td><td>军队的中间部分</td><td>中军置酒饮归客</td></tr>
      <tr><td class="kai">辕门</td><td>军营的大门</td><td>官署的外门</td><td>纷纷暮雪下辕门</td></tr>
    </table></div>
    <div class="acc-sub">词类活用</div>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">饮</td><td>使动用法</td><td>使……饮酒</td><td>中军置酒饮归客</td></tr>
    </table></div>
    <div class="acc-sub">一词多义</div>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="2">着</td><td>穿（zhuó）</td><td>都护铁衣冷难着</td></tr>
      <tr><td>接触（zhe）</td><td>看着</td></tr>
      <tr><td class="kai" rowspan="2">空</td><td>白白地、徒然</td><td>雪上空留马行处</td></tr>
      <tr><td>天空</td><td>空谷传响</td></tr>
      <tr><td class="kai" rowspan="2">即</td><td>就、便</td><td>胡天八月即飞雪</td></tr>
      <tr><td>立即</td><td>即刻出发</td></tr>
    </table></div>
    <div class="acc-sub">文言句式</div>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">对偶句</td><td>将军角弓不得控，都护铁衣冷难着。</td><td>对仗工整，名词对名词、动词对动词</td></tr>
      <tr><td class="kai">对偶句</td><td>瀚海阑干百丈冰，愁云惨淡万里凝。</td><td>对仗工整，数量词对数量词</td></tr>
      <tr><td class="kai">比喻</td><td>忽如一夜春风来，千树万树梨花开。</td><td>以梨花喻雪，想象奇特</td></tr>
      <tr><td class="kai">夸张</td><td>瀚海阑干百丈冰</td><td>~L~百丈~R~虚指，极言冰之厚</td></tr>
    </table></div>
  </div></div>
  <div class="box">
    <h3>炼字与边塞诗特色（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>即——胡天八月即飞雪</dt><dd>~L~即~R~字写出了边塞气候的反常——中原八月还是秋天，胡地八月就已经下雪了。一个~L~即~R~字，将边塞的奇寒和气候的反常写得淋漓尽致。</dd></div>
      <div class="g-item"><dt>忽如——忽如一夜春风来</dt><dd>~L~忽如~R~二字写出了大雪来得突然，好像一夜之间春风吹来了。以~L~忽如~R~领起奇喻，将萧瑟的冬景写成了烂漫的春景，体现了诗人的惊喜和乐观。</dd></div>
      <div class="g-item"><dt>冻不翻——风掣红旗冻不翻</dt><dd>~L~冻不翻~R~三字以动写静——在大风中，红旗本来应该随风翻卷，但因为天气太冷，红旗被冻住了，连风都吹不动。这三个字将边塞的奇寒写到了极致，是炼字的经典。</dd></div>
      <div class="g-item"><dt>空留——雪上空留马行处</dt><dd>~L~空留~R~二字写出了诗人目送友人远去后的怅惘——友人已经消失，雪地上只留下马蹄印。~L~空~R~是白白地、徒然的意思，将依依惜别之情写得淋漓尽致。</dd></div>
      <div class="g-item"><dt>边塞诗特色</dt><dd>①奇寒：白草折、狐裘不暖、角弓不得控、铁衣冷难着、红旗冻不翻；②奇景：千树万树梨花开、瀚海百丈冰、愁云万里凝；③奇情：乐观豪迈的精神、依依惜别的深情。奇寒、奇景、奇情，构成了岑参边塞诗的独特风貌。</dd></div>
    </div>
  </div>
  <div class="box"><div class="acc-cat"><h3>修辞与手法</h3>
    <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">~L~忽如一夜春风来，千树万树梨花开~R~，以梨花喻雪。</span></div>
    <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">~L~瀚海阑干百丈冰~R~，~L~百丈~R~虚指，极言冰之厚。</span></div>
    <div class="acc-item"><span class="acc-w">对偶</span><span class="acc-d">~L~将军角弓不得控，都护铁衣冷难着~R~等，对仗工整。</span></div>
    <div class="acc-item"><span class="acc-w">以动写静</span><span class="acc-d">~L~风掣红旗冻不翻~R~，以风的动写旗的静。</span></div>
    <div class="acc-item"><span class="acc-w">以景结情</span><span class="acc-d">~L~山回路转不见君，雪上空留马行处~R~，以雪景结送别之情。</span></div>
    <div class="acc-item"><span class="acc-w">情景交融</span><span class="acc-d">咏雪与送别融为一体，雪既是写景对象，也是抒情载体。</span></div>
  </div></div>
  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>白草</dt><dd>西北边塞的一种草名，干枯后变白，性坚韧。《汉书·西域传》：~L~鄯善国，地沙卤，多白草。~R~颜师古注：~L~白草，草之白者，似莠而细，无芒，其干熟时正白色，牛马所嗜也。~R~</dd></div>
      <div class="g-item"><dt>胡天</dt><dd>胡人的天空，指西北地区。~L~胡~R~是古代对北方和西方少数民族的称呼。唐代边塞诗中常用~L~胡天~R~指代边塞地区。</dd></div>
      <div class="g-item"><dt>狐裘</dt><dd>用狐狸皮做的皮衣，是古代非常贵重的保暖衣物。~L~裘~R~是皮衣的总称，~L~狐裘~R~是用狐狸皮做的皮衣，最为贵重。</dd></div>
      <div class="g-item"><dt>锦衾</dt><dd>用锦缎做的被子。~L~锦~R~是有彩色花纹的丝织品，~L~衾~R~是被子。锦衾是非常厚实的被子，连锦衾都觉得薄，可见边塞之寒。</dd></div>
      <div class="g-item"><dt>角弓</dt><dd>用兽角装饰的弓。古代良弓多用兽角（如牛角）装饰，既美观又增强弓的弹性。~L~角弓~R~是将军使用的精良武器。</dd></div>
      <div class="g-item"><dt>都护</dt><dd>唐代边疆最高军事长官，统辖边防军政。唐太宗时设安西都护府，武则天时设北庭都护府。岑参第二次出塞即在北庭都护府任职。</dd></div>
      <div class="g-item"><dt>瀚海</dt><dd>大沙漠。~L~瀚~R~是广大的意思，~L~海~R~指沙漠如大海般广阔。唐代边塞诗中常用~L~瀚海~R~指代西北大沙漠。</dd></div>
      <div class="g-item"><dt>中军</dt><dd>古代军队的中军营帐，是主帅所在的地方。古代军队分左、中、右三军，中军是主帅所在的主力部队。</dd></div>
      <div class="g-item"><dt>判官</dt><dd>唐代节度使的属官，负责处理文书事务。岑参本人也曾任判官，~L~武判官~R~是他的友人，姓名不详。</dd></div>
      <div class="g-item"><dt>辕门</dt><dd>军营的大门。古代军营前以两车之辕（车前驾牲畜的木杆）相向为门，故称~L~辕门~R~。后来~L~辕门~R~泛指军营的大门。</dd></div>
      <div class="g-item"><dt>轮台</dt><dd>古地名，在今新疆米泉一带，唐代北庭都护府所在地。岑参第二次出塞时在此任职，写下了多首以轮台为背景的边塞诗。</dd></div>
      <div class="g-item"><dt>天山</dt><dd>亚洲中部的大山系，横贯新疆中部，将新疆分为南疆和北疆。唐代边塞诗中常提到天山，是边塞的象征。</dd></div>
      <div class="g-item"><dt>胡琴琵琶羌笛</dt><dd>都是西域少数民族的乐器。胡琴是弦乐器，琵琶是弹拨乐器，羌笛是管乐器。在边塞的中军帐中，用这些乐器演奏，既有边塞特色，也增添了饯别的悲凉气氛。</dd></div>
      <div class="g-item"><dt>边塞诗派</dt><dd>盛唐诗歌流派，以描写边塞风光、战争生活、将士情感为主要内容。代表诗人有高适、岑参、王维、王昌龄、李颀等。岑参的边塞诗以想象奇特、色彩瑰丽、气势雄浑著称。</dd></div>
    </div>
  </div>
</section>
''')
HTML=u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《白雪歌送武判官归京》岑参</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">
<header class="hero"><div class="hero-side">唐 · 岑参</div><h1 class="hero-title">白雪歌送武判官归京</h1></header>
<nav class="nav"><div class="nav-in">
<a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a>
<div class="tool">
<select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%%</option><option value="150">150%%</option><option value="200">200%%</option><option value="250">250%%</option><option value="300">300%%</option></select>
<button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button>
</div></div></nav>
<main class="wrap">
%(bg)s
<div class="divider"></div>
<section id="jielu" class="sec">
<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>
<div class="sec-sub">全诗十八句（七言古诗），分三部分：咏雪、饯别、送别。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
<button data-mode="note" data-rand="5">随机五组注释</button>
<button data-mode="note" data-all="1">全部注释</button>
</div>
</section>
<footer>
<div class="kai">《白雪歌送武判官归京》</div>
<div>岑参 · 唐（约715—770）· 天宝十三载轮台作 · 七言古诗 · 边塞诗</div>
</footer>
</main>
<button class="top-btn" id="topBtn" title="回到顶部">↑</button>
<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>
<div class="dictate" id="dictate" hidden>
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
'''%{'css':CSS,'js':JS,'bg':BG,'app':APP,'acc':ACC,'fulltext':full_html,'verses':verses_html,'words':json.dumps(DICT_WORDS,ensure_ascii=False),'notes':json.dumps(DICT_NOTES,ensure_ascii=False)}
HTML=fixq(HTML)
io.open(OUT,'w',encoding='utf-8').write(HTML)
print('OK',OUT,'verses=',total,'anno=',anno_count,'words=',len(DICT_WORDS),'notes=',len(DICT_NOTES))
