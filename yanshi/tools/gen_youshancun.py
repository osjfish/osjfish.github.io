# -*- coding: utf-8 -*-
"""生成《游山西村》课件（中国古诗，七言律诗，逐句解读+译文+赏析）。"""
import io, json, re

SRC = r"D:\App\Apps\yanshi\chibi-dumu.html"
OUT = r"D:\App\Apps\yanshi\youshanxicun-luyou.html"
LS_KEY = "youshancun_fs"

LQ = "\u201c"
RQ = "\u201d"

def A(word, note):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)

# 逐句数据：(原文带注释标记, 译文, 赏析, [标签])
CARDS = [
("莫笑农家" + A("腊酒","腊月（农历十二月）酿造的酒") + A("浑(hún)","浑浊。指酒质不清，味薄") + "，",
 "不要笑话农家腊月酿的酒浑浊味薄。",
 "首联起句，以" + LQ + "莫笑" + RQ + "二字直接入题，告诉读者不要笑话农家的酒浑浊。" + LQ + "腊酒浑" + RQ + "写出了农家酒的质朴——不是什么名酒佳酿，只是自家腊月酿的浊酒。一个" + LQ + "莫笑" + RQ + "，既写出了农家的淳朴，也表达了诗人对农家生活的尊重与喜爱。",
 ["首联","农家热情"]),
("丰年留客" + A("足鸡豚(tún)","备足了鸡肉和猪肉。豚，小猪，这里指猪肉") + "。",
 "丰收之年，农家留客吃饭，备足了鸡肉和猪肉。",
 "次句承接上句，写农家的热情好客。" + LQ + "丰年" + RQ + "点明这是一个丰收之年，" + LQ + "留客" + RQ + "写农家主动挽留客人，" + LQ + "足鸡豚" + RQ + "写菜肴丰盛——虽然酒是浊酒，但菜却备足了鸡和肉。" + LQ + "足" + RQ + "字用得极好，写出了农家的倾其所有、热情款待。首联两句，写出了农家的淳朴与热情，为全诗奠定了温馨的基调。",
 ["首联","热情好客"]),
(A("山重水复","山峦重叠，水流盘曲。形容山水曲折幽深") + "疑无路，",
 "山峦重叠，水流盘曲，正怀疑前面没有路可走。",
 "颔联起句，写山村的山水之景。" + LQ + "山重水复" + RQ + "四个字，写出了山峦重叠、水流盘曲的幽深景象——走过一座山又一座山，绕过一道水又一道水，仿佛前面已经没有路了。" + LQ + "疑无路" + RQ + "的" + LQ + "疑" + RQ + "字，写出了诗人的主观感受——不是真的没有路，而是走在曲折幽深的山水间，怀疑没有路了。这一句为下一句的转折蓄势。",
 ["颔联","名句","哲理"]),
(A("柳暗花明","柳色深绿，花色红艳。形容绿柳成荫、繁花似锦的景象") + "又一村。",
 "忽然柳色深绿、花色红艳，眼前又出现了一个村庄。",
 "次句急转，是全诗的名句。" + LQ + "柳暗花明" + RQ + "写绿柳成荫、繁花似锦的明媚景象，与上一句" + LQ + "山重水复" + RQ + "的幽深形成鲜明对比；" + LQ + "又一村" + RQ + "写在以为无路可走的时候，忽然出现了一个村庄。这两句不仅写出了山村的自然美景，更蕴含着深刻的哲理：在困境中坚持前行，往往会迎来新的希望。" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "因此成为千古传诵的名句，常用来比喻在困境中出现转机。",
 ["颔联","名句","哲理","对比"]),
(A("箫(xiāo)鼓","吹箫打鼓。箫，古代的管乐器") + A("追随","紧跟着、伴随") + A("春社","古代立春后祭祀土地神的日子，祈求丰收") + "近，",
 "吹箫打鼓的声音此起彼伏，春社的日子越来越近了。",
 "颈联起句，写山村的风俗。" + LQ + "箫鼓追随" + RQ + "写吹箫打鼓的声音此起彼伏，人们在为春社做准备；" + LQ + "春社近" + RQ + "点明时间——春社（立春后祭祀土地神的日子）将近。这一句从视觉（山水）转入听觉（箫鼓），写出了山村热闹的节日气氛，也表现了乡村淳朴的民俗风情。",
 ["颈联","乡村风俗"]),
(A("衣冠(guān)","衣服和帽子，指服饰穿戴。冠，读 guān，帽子") + A("简朴","简单朴素") + A("古风","古代的风尚、传统") + "存。",
 "村民们的服饰穿戴简单朴素，古老的风尚依然保存着。",
 "次句承接上句，写村民的淳朴。" + LQ + "衣冠简朴" + RQ + "写村民的穿着简单朴素，没有华丽的装饰；" + LQ + "古风存" + RQ + "写古老的风尚依然保存在这里。颈联两句，从节日风俗到日常穿戴，写出了山西村的淳朴民风——这里没有世俗的浮华，只有古老的传统和淳朴的人情。这正是诗人所向往的。",
 ["颈联","淳朴民风"]),
("从今若许" + A("闲乘月","趁着月明来闲游。乘月，趁着月光") + "，",
 "从今以后，如果允许我趁着月明来闲游，",
 "尾联起句，诗人从写景转入抒情，表达了对山西村的向往。" + LQ + "从今若许" + RQ + "是一个假设——从今以后，如果允许的话；" + LQ + "闲乘月" + RQ + "写趁着月明之夜来闲游。这一句写出了诗人对山西村的留恋——游了一天还不够，还想以后再来。" + LQ + "若许" + RQ + "二字，语气委婉，表达了一种美好的愿望。",
 ["尾联","向往之情"]),
("拄杖无时夜" + A("叩(kòu)","敲") + "门。",
 "我会拄着拐杖，随时在夜里来敲门拜访。",
 "末句收束全诗，将向往之情推向高潮。" + LQ + "拄杖" + RQ + "写出了诗人的年老（陆游写此诗时已42岁，在古代已不算年轻），" + LQ + "无时" + RQ + "是" + LQ + "随时" + RQ + "的意思，" + LQ + "夜叩门" + RQ + "写在夜里来敲门拜访。一个" + LQ + "无时" + RQ + "，写出了诗人与农家之间的亲密无间——不需要事先约定，随时都可以来敲门。尾联两句，表达了诗人对乡村生活的真挚向往，也写出了诗人与村民之间深厚的情谊。",
 ["尾联","真挚向往"]),
]

FULLTEXT = [
 "莫笑农家腊酒浑，",
 "丰年留客足鸡豚。",
 "山重水复疑无路，",
 "柳暗花明又一村。",
 "箫鼓追随春社近，",
 "衣冠简朴古风存。",
 "从今若许闲乘月，",
 "拄杖无时夜叩门。",
]

BG_LEAD = [
 "陆游（1125—1210），南宋著名爱国诗人。乾道二年（1166），陆游因支持抗金将领张浚北伐，被罢官闲居，回到故乡山阴（今浙江绍兴）。此后四年，他住在乡下，与农民交往，对农村生活有了深入的了解。《游山西村》就是这一时期写的，描写了诗人游览山西村时的所见所感。",
 "全诗八句，首联写农家的热情好客，颔联" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "是千古传诵的名句（蕴含困境中见转机的哲理），颈联写乡村的淳朴风俗，尾联写诗人对乡村生活的向往。这首诗以明快的笔调描绘了一幅江南农村的风俗画，表达了诗人对淳朴乡村生活的喜爱与向往。",
]

AUTHOR = [
 "陆游（1125—1210），字务观，号放翁，越州山阴（今浙江绍兴）人，南宋著名爱国诗人。他一生创作诗歌近万首，是中国历史上写诗最多的诗人之一。其诗风格多样，以豪放悲壮为主，也有清新自然的田园诗。代表作有《示儿》《书愤》《钗头凤》《游山西村》《十一月四日风雨大作》等。",
 "陆游生逢北宋灭亡之际，少年时即深受家庭爱国思想的熏陶。他一生主张抗金，收复中原，但屡遭主和派排挤。中年入蜀，投身军旅生活，这是他诗歌创作的重要时期。晚年退居家乡，但收复中原的信念始终不渝。临终前写下《示儿》：" + LQ + "王师北定中原日，家祭无忘告乃翁。" + RQ + "成为千古绝唱。",
]

STORY = [
 ("罢官闲居","乾道二年（1166），陆游因支持抗金将领张浚北伐，被主和派以" + LQ + "交结台谏，鼓唱是非，力说张浚用兵" + RQ + "的罪名罢官，回到故乡山阴。此后四年，他住在乡下的三山别业，与农民交往，对农村生活有了深入的了解。"),
 ("游山西村","山西村是山阴县的一个村庄，在今浙江绍兴境内。陆游罢官闲居期间，常到附近的村庄游览，与农民交往。《游山西村》就是他游览山西村时写下的，描写了农家的热情好客、山村的美丽景色和淳朴的风俗。"),
 ("律诗格律","《游山西村》是一首七言律诗，八句五十六字，二、四、六、八句押韵（浑、豚、村、存、门，平水韵元韵）。颔联" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "和颈联" + LQ + "箫鼓追随春社近，衣冠简朴古风存" + RQ + "对仗工整，是律诗的典范。"),
 ("名句影响","" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "是陆游最著名的诗句之一，也是中国诗歌中最著名的哲理名句。它不仅写出了山村的自然美景，更蕴含着深刻的人生哲理——在困境中坚持前行，往往会迎来新的希望。这两句诗被后人广泛引用，成为鼓励人们在困境中保持希望的名言。"),
]

APP_ART = [
 ("" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "的哲理","这是全诗最突出的艺术特色，也是千古传诵的名句。" + LQ + "山重水复" + RQ + "写山水的曲折幽深，" + LQ + "疑无路" + RQ + "写诗人的主观感受——以为没有路了；" + LQ + "柳暗花明" + RQ + "写景色的明媚变化，" + LQ + "又一村" + RQ + "写忽然出现的村庄。这两句不仅写出了山村的自然美景，更蕴含着深刻的哲理：在困境中坚持前行，往往会迎来新的希望。这种从具体景物中提炼出人生哲理的写法，是宋诗" + LQ + "以理趣见长" + RQ + "的典型代表。"),
 ("田园风光的生动描绘","全诗以明快的笔调描绘了一幅江南农村的风俗画。首联" + LQ + "莫笑农家腊酒浑，丰年留客足鸡豚" + RQ + "写农家的热情好客；颔联" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "写山村的自然美景；颈联" + LQ + "箫鼓追随春社近，衣冠简朴古风存" + RQ + "写乡村的淳朴风俗。从饮食到风景，从节日到日常，全方位地展现了乡村生活的美好。"),
 ("对乡村生活的真挚向往","尾联" + LQ + "从今若许闲乘月，拄杖无时夜叩门" + RQ + "直接表达了诗人对乡村生活的向往。" + LQ + "无时" + RQ + "（随时）二字，写出了诗人与农家之间的亲密无间——不需要事先约定，随时都可以来敲门。这种真挚的向往，不是文人的附庸风雅，而是诗人在罢官闲居期间与农民真诚交往后产生的真实情感。"),
 ("结构严谨，对仗工整","作为一首七言律诗，本诗结构严谨，对仗工整。首联起（写农家热情），颔联承（写山村美景），颈联转（写乡村风俗），尾联合（写向往之情），起承转合，层次分明。颔联和颈联对仗工整，" + LQ + "山重水复" + RQ + "对" + LQ + "柳暗花明" + RQ + "，" + LQ + "疑无路" + RQ + "对" + LQ + "又一村" + RQ + "；" + LQ + "箫鼓追随" + RQ + "对" + LQ + "衣冠简朴" + RQ + "，" + LQ + "春社近" + RQ + "对" + LQ + "古风存" + RQ + "，是律诗对仗的典范。"),
]

APP_FAME = [
 ("山重水复疑无路，柳暗花明又一村。",
  "这是全诗的精华，也是千古传诵的名句。" + LQ + "山重水复" + RQ + "写山峦重叠、水流盘曲的幽深景象，" + LQ + "疑无路" + RQ + "写诗人以为前面没有路了；" + LQ + "柳暗花明" + RQ + "写忽然出现的绿柳成荫、繁花似锦的明媚景象，" + LQ + "又一村" + RQ + "写忽然出现了一个村庄。这两句不仅写出了山村的自然美景，更蕴含着深刻的哲理：在困境中坚持前行，往往会迎来新的希望。" + LQ + "疑" + RQ + "字和" + LQ + "又" + RQ + "字用得极妙——" + LQ + "疑" + RQ + "是主观感受，" + LQ + "又" + RQ + "是意外惊喜，在转折中见出哲理。这两句诗被后人广泛引用，成为鼓励人们在困境中保持希望的名言。"),
 ("莫笑农家腊酒浑，丰年留客足鸡豚。",
  "首联两句，写出了农家的淳朴与热情。" + LQ + "莫笑" + RQ + "二字直接入题，告诉读者不要笑话农家的酒浑浊；" + LQ + "腊酒浑" + RQ + "写出了农家酒的质朴——只是自家腊月酿的浊酒。" + LQ + "丰年留客足鸡豚" + RQ + "写丰收之年，农家留客吃饭，备足了鸡肉和猪肉。" + LQ + "足" + RQ + "字用得极好，写出了农家的倾其所有、热情款待。虽然酒是浊酒，但菜却丰盛——这种质朴的热情，比任何山珍海味都更动人。"),
 ("箫鼓追随春社近，衣冠简朴古风存。",
  "颈联两句，写出了山村的淳朴风俗。" + LQ + "箫鼓追随" + RQ + "写吹箫打鼓的声音此起彼伏，人们在为春社做准备；" + LQ + "春社近" + RQ + "点明时间——春社将近。" + LQ + "衣冠简朴古风存" + RQ + "写村民的穿着简单朴素，古老的风尚依然保存着。这两句从节日风俗到日常穿戴，写出了山西村的淳朴民风——这里没有世俗的浮华，只有古老的传统和淳朴的人情。"),
]

APP_THEME = [
 "本诗通过描写诗人游览山西村时的所见所感，描绘了一幅江南农村的风俗画，表达了诗人对淳朴乡村生活的喜爱与向往。首联写农家的热情好客——虽然酒是浊酒，但菜却丰盛，" + LQ + "足鸡豚" + RQ + "写出了农家的倾其所有；颔联写山村的自然美景——" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "，在曲折幽深中忽然出现明媚的村庄，蕴含着困境中见转机的哲理；颈联写乡村的淳朴风俗——箫鼓春社，衣冠简朴，古风犹存；尾联写诗人的向往——" + LQ + "从今若许闲乘月，拄杖无时夜叩门" + RQ + "，希望以后能随时来拜访。",
 "全诗以明快的笔调，将农家的热情、山村的美景、淳朴的风俗和诗人的向往融为一体，构成了一幅完整的江南农村风俗画。" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "更是超越了具体的写景，成为蕴含深刻人生哲理的千古名句。这首诗也反映了陆游在罢官闲居期间与农民真诚交往后产生的真实情感——对淳朴乡村生活的热爱，以及对世俗官场的厌倦。",
]

ACC = [
 ("文体与格律", [
   ("七言律诗","本诗是一首七言律诗，八句五十六字。每句七字，共八句，分首联、颔联、颈联、尾联。"),
   ("押韵","二、四、六、八句押韵：浑、豚、村、存、门（平水韵元韵）。首句" + LQ + "浑" + RQ + "也入韵，是首句入韵式。"),
   ("对仗","颔联" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "和颈联" + LQ + "箫鼓追随春社近，衣冠简朴古风存" + RQ + "对仗工整，是律诗的典范。"),
   ("结构","首联起（农家热情）→颔联承（山村美景）→颈联转（乡村风俗）→尾联合（向往之情），起承转合，层次分明。"),
 ]),
 ("易错字音形", [
   ("浑","hún","三点水，指酒浑浊；勿写「混」（此处不读 hùn）"),
   ("豚","tún","月字旁，指小猪，此处指猪肉；勿写「逐」（走之旁）"),
   ("箫","xiāo","竹字头，管乐器；勿写「萧」（草字头，姓/萧条）"),
   ("冠","guān","此处读 guān（帽子），不读 guàn（冠军）"),
   ("叩","kòu","提手旁，敲的意思；勿写「扣」（提手旁，但义不同）"),
   ("拄","zhǔ","提手旁，拄着；勿写「柱」（木字旁，柱子）"),
 ]),
 ("文言梳理", [
   ("古今异义","无时：文中义为" + LQ + "随时" + RQ + "（拄杖无时夜叩门），今义为" + LQ + "没有时间" + RQ + "。这是本诗最重要的古今异义词。"),
   ("一词多义","足：文中义为" + LQ + "充足、备足" + RQ + "（丰年留客足鸡豚）；其他常见义有" + LQ + "脚" + RQ + LQ + "满足" + RQ + LQ + "值得" + RQ + "。"),
   ("词类活用","本诗无明显词类活用。"),
   ("文言句式","本诗无特殊文言句式。颔联、颈联为对仗句式。"),
 ]),
 ("本文核心考点：哲理名句", [
   ("" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "","全诗核心考点。不仅写出山村美景，更蕴含哲理：在困境中坚持前行，往往会迎来新的希望。常用来比喻困境中出现转机。"),
   ("" + LQ + "疑" + RQ + "字炼字","" + LQ + "疑无路" + RQ + "的" + LQ + "疑" + RQ + "字，写出了诗人的主观感受——不是真的没有路，而是走在曲折幽深的山水间，怀疑没有路了。为下文" + LQ + "又一村" + RQ + "的转折蓄势。"),
   ("" + LQ + "又" + RQ + "字炼字","" + LQ + "又一村" + RQ + "的" + LQ + "又" + RQ + "字，写出了意外惊喜——在以为无路的时候，忽然出现了一个村庄。" + LQ + "又" + RQ + "字是转折的关键。"),
   ("" + LQ + "足" + RQ + "字炼字","" + LQ + "足鸡豚" + RQ + "的" + LQ + "足" + RQ + "字，写出了农家的倾其所有、热情款待——虽然酒是浊酒，但菜却备足了。"),
 ]),
 ("修辞与手法", [
   ("对　偶","颔联" + LQ + "山重水复疑无路，柳暗花明又一村" + RQ + "和颈联" + LQ + "箫鼓追随春社近，衣冠简朴古风存" + RQ + "对仗工整。"),
   ("对　比","" + LQ + "山重水复" + RQ + "的幽深与" + LQ + "柳暗花明" + RQ + "的明媚形成对比，在对比中凸显转折的惊喜。"),
   ("借景抒情","全诗借山村的美景和淳朴的风俗，抒发对乡村生活的喜爱与向往之情。"),
   ("用　典","" + LQ + "春社" + RQ + "用古代祭祀土地神的风俗，" + LQ + "古风存" + RQ + "暗用上古淳朴之风的典故。"),
 ]),
 ("文化常识", [
   ("腊酒","腊月（农历十二月）酿造的酒。农家自酿，往往比较浑浊，但味醇。"),
   ("春社","古代立春后第五个戊日，祭祀土地神（社神）的日子，祈求丰收。这一天民间有吹箫打鼓、集会宴饮的风俗。"),
   ("古风","古代的风尚、传统。诗中指上古时期淳朴的社会风气。"),
   ("山西村","山阴县的一个村庄，在今浙江绍兴境内。陆游罢官闲居期间常来此游览。"),
   ("七言律诗","中国古典诗歌的一种体裁，每首八句，每句七字，中间两联必须对仗，二、四、六、八句押韵。"),
 ]),
]

WORDS = [
 {"w":"浑","py":"hún","q":"莫笑农家腊酒□，","tip":"「浑」三点水，读 hún；指酒浑浊，勿写「混」（此处不读 hùn）"},
 {"w":"豚","py":"tún","q":"丰年留客足鸡□。","tip":"「豚」月字旁，读 tún；指小猪/猪肉，勿写「逐」（走之旁）"},
 {"w":"箫","py":"xiāo","q":"□鼓追随春社近，","tip":"「箫」竹字头，读 xiāo；管乐器，勿写「萧」（草字头）"},
 {"w":"冠","py":"guān","q":"衣□简朴古风存。","tip":"「冠」读 guān（帽子），不读 guàn（冠军）；「衣冠」指服饰"},
 {"w":"叩","py":"kòu","q":"拄杖无时夜□门。","tip":"「叩」提手旁，读 kòu；敲的意思，勿写「扣」"},
 {"w":"拄","py":"zhǔ","q":"□杖无时夜叩门。","tip":"「拄」提手旁，读 zhǔ；拄着，勿写「柱」（木字旁，柱子）"},
]

NOTES = [
 {"w":"腊酒","a":"腊月（农历十二月）酿造的酒","q":"莫笑农家腊酒浑，"},
 {"w":"浑","a":"浑浊。指酒质不清，味薄","q":"莫笑农家腊酒浑，"},
 {"w":"足鸡豚","a":"备足了鸡肉和猪肉。豚，小猪，这里指猪肉","q":"丰年留客足鸡豚。"},
 {"w":"山重水复","a":"山峦重叠，水流盘曲。形容山水曲折幽深","q":"山重水复疑无路，"},
 {"w":"柳暗花明","a":"柳色深绿，花色红艳。形容绿柳成荫、繁花似锦","q":"柳暗花明又一村。"},
 {"w":"箫鼓","a":"吹箫打鼓。箫，古代的管乐器","q":"箫鼓追随春社近，"},
 {"w":"春社","a":"古代立春后祭祀土地神的日子，祈求丰收","q":"箫鼓追随春社近，"},
 {"w":"衣冠","a":"衣服和帽子，指服饰穿戴。冠，读 guān","q":"衣冠简朴古风存。"},
 {"w":"简朴","a":"简单朴素","q":"衣冠简朴古风存。"},
 {"w":"古风","a":"古代的风尚、传统","q":"衣冠简朴古风存。"},
 {"w":"闲乘月","a":"趁着月明来闲游。乘月，趁着月光","q":"从今若许闲乘月，"},
 {"w":"无时","a":"随时（古今异义：今义为没有时间）","q":"拄杖无时夜叩门。"},
 {"w":"叩","a":"敲。读 kòu","q":"拄杖无时夜叩门。"},
]

VIDEOS = [
 ("游山西村 陆游 诵读 潇然","BV1DG411t7WT","游山西村朗诵"),
 ("康震讲《游山西村》","BV1w54y1e7tm","康震讲游山西村"),
]

# ===== 读取框架 =====
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]
js_main = src[src.index("<script>") + 8 : src.index("var DICT_WORDS")]
js_main = js_main.replace("chibi_fs", LS_KEY)
js_dict = src[src.index("var DICT_WORDS") : src.index("</script>", src.index("var DICT_WORDS"))]
js_dict = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", js_dict, flags=re.S)
js_dict = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", js_dict, flags=re.S)

def video(i, h4, bvid, atitle):
    return ('<div class="media"><h4>%s</h4>'
            '<iframe id="mediaF%d" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>'
            '<a href="https://www.bilibili.com/video/%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF%d">全屏播放</button></div>'
            % (h4, i, bvid, atitle, bvid, i))

hero = '<header class="hero" id="top">\n  <div class="hero-inner">\n    <div class="hero-side">宋·陆游</div>\n    <h1 class="hero-title">游山西村</h1>\n  </div>\n</header>'

nav = ('<nav class="nav"><div class="nav-in">'
       '<a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a>'
       '<div class="tool">'
       '<select id="fsSel" class="fs-sel" title="正文字体大小">'
       '<option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option>'
       '</select>'
       '<button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button>'
       '</div></div></nav>')

bg = ['<section id="bg">',
      '<div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>',
      '<div class="lead">']
for p in BG_LEAD: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>作者简介</h3>')
for p in AUTHOR: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>创作背景</h3>')
for t, p in STORY: bg.append('<p><b>' + t + '：</b>' + p + '</p>')
bg.append('</div></section>')

jl = ['<section id="jielu">',
      '<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>',
      '<div class="sec-sub">全诗八句，首联写农家热情，颔联' + LQ + '山重水复疑无路，柳暗花明又一村' + RQ + '是名句（哲理），颈联写乡村风俗，尾联写向往。每句含<b>注释</b>（生僻字、易错词均附读音）、译文与赏析，点击可展开。</div>',
      '<div class="texttools">',
      '<button id="btnShowAll" class="off" style="display:none">显示全部</button>',
      '</div>',
      '<div class="box media-box">',
      '<h3>朗诵 · 拓展</h3>',
      '<div class="media-grid">']
for i, (h4, bvid, at) in enumerate(VIDEOS):
    jl.append(video(i + 1, h4, bvid, at))
jl.append('</div></div>')

jl.append('<div class="fulltext poem" id="fulltext" style="display:none">')
for idx, line in enumerate(FULLTEXT, 1):
    jl.append('<div class="pl"><span class="no">%d</span>%s</div>' % (idx, line))
jl.append('</div>')

jl.append('<div class="verse-list" id="verseList">')
for n, (orig, yi, shang, tags) in enumerate(CARDS, 1):
    jl.append('<div class="verse" id="v%d">' % n)
    jl.append('  <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (n, orig))
    jl.append('  <details class="v-more">')
    jl.append('    <summary>译文 · 赏析</summary>')
    jl.append('    <div class="d-body">')
    jl.append('      <div class="v-sec"><b class="v-label">译　文</b>')
    jl.append('        <div class="v-trans">%s</div>' % yi)
    jl.append('      </div>')
    jl.append('      <div class="v-sec"><b class="v-label">赏　析</b>')
    jl.append('        <div class="d-body"><p>%s</p></div>' % shang)
    if tags:
        jl.append('        <div class="tags">%s</div>' % ''.join('<span>%s</span>' % t for t in tags))
    jl.append('      </div>')
    jl.append('    </div>')
    jl.append('  </details>')
    jl.append('</div>')
jl.append('</div></section>')

app = ['<section id="app">',
       '<div class="sec-head"><h2>赏 析</h2><span class="no">艺术特色 · 名句 · 主题</span></div>']
app.append('<div class="fame-card"><h3>艺术特色</h3>')
for t, p in APP_ART:
    app.append('<p><b>%s</b>：%s</p>' % (t, p))
app.append('</div>')
app.append('<div class="fame-card"><h3>名句赏析</h3><div class="fame">')
for t, p in APP_FAME:
    app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div>')
app.append('<div class="fame-card"><h3>主题思想</h3>')
for p in APP_THEME: app.append('<p>' + p + '</p>')
app.append('</div></section>')

acc = ['<section id="acc">',
       '<div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 哲理 · 修辞 · 文化常识</span></div>']
for cat, items in ACC:
    acc.append('<div class="box"><h3>%s</h3>' % cat)
    if cat == "易错字音形":
        acc.append('<div class="tw"><table>')
        acc.append('<tr><th>字词</th><th>注音</th><th>易错提示</th></tr>')
        for w, py, tip in items:
            acc.append('<tr><td class="kai">%s</td><td>%s</td><td>%s</td></tr>' % (w, py, tip))
        acc.append('</table></div>')
    else:
        for w, d in items:
            acc.append('<p><b class="term">%s</b>%s</p>' % (w, d))
    acc.append('</div>')
acc.append('</section>')

practice = ['<section id="practice">',
            '<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写 · 字词 / 注释</span></div>',
            '<div class="sec-sub">以全篇<b>易错字词</b>与<b>重点注释</b>为题库，点击按钮进入<b>全屏听写</b>：先看提示在纸上默写，再核对答案。随机五组适合随堂小测，全部适合系统复习。</div>',
            '<div class="ptools">',
            '<button data-mode="word" data-rand="5">随机五组字形</button>',
            '<button data-mode="word" data-all="1">全部字形</button>',
            '<button data-mode="note" data-rand="5">随机五组注释</button>',
            '<button data-mode="note" data-all="1">全部注释</button>',
            '</div></section>']

footer = '<footer>\n  <div class="kai">游山西村</div>\n  <div>陆游 · 宋</div>\n</footer>'

dictate_html = '''<div class="dictate" id="dictate" hidden>
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
</div>'''

html = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>游山西村</title>\n'
        '<meta name="description" content="宋陆游《游山西村》逐句注释、译文、赏析，生僻字与易错词附注音，含背景、原文（背诵模式）、解读、赏析、积累、练习，适合课堂教学。">\n'
        '<style>' + css + '</style>\n</head>\n<body>\n\n'
        + hero + '\n\n' + nav + '\n\n<main class="wrap">\n\n'
        + "\n".join(bg) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(jl) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(app) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(acc) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(practice) + '\n\n'
        + footer + '\n</main>\n\n'
        + '<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>\n'
        + '<button class="top-btn" id="topBtn" title="回到顶部">↑</button>\n\n'
        + dictate_html + '\n\n'
        + '<script>\n' + js_main + '\n' + js_dict + '\n</script>\n\n'
        + '</body>\n</html>\n')

no_script = re.sub(r"<script>.*?</script>", "", html, flags=re.S)
body_text = re.sub(r"<[^>]+>", "", re.sub(r"<style>.*?</style>", "", no_script, flags=re.S))
assert body_text.count('"') == 0, "straight quotes in visible text: %d" % body_text.count('"')
assert "{LQ}" not in html and "{RQ}" not in html, "placeholder残留"
need = ["verseList", "fulltext", "btnAll", "btnRecite", "btnPrint", "btnShowAll", "fsSel", "annoPopup", "dictate", "topBtn", "mediaF1", "mediaF2"]
missing = [i for i in need if 'id="%s"' % i not in html]
assert not missing, "missing ids: %s" % missing
assert LS_KEY in js_main and "chibi_fs" not in js_main
for it in WORDS:
    assert not any(c in it["q"] for c in it["w"]), "leak: %s" % it["w"]
    assert it["q"].count("\u25a1") == len(it["w"]), "box mismatch: %s" % it["w"]
    assert it["tip"] and it["tip"] != it["w"], "tip bad: %s" % it["w"]

anno_count = html.count('class="anno-word"')
print("游山西村 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), anno_count, len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
