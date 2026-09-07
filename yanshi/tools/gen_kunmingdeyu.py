# -*- coding: utf-8 -*-
"""生成《昆明的雨》汪曾祺 课件"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\kunmingdeyu-wangzengqi.html"
FS_KEY = "kunming_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

# 每段: (原文, 内容概括, 手法分析, [(词,注释),...])
paragraphs = [
    # === 第一部分 ===
    (
        "宁坤要我给他画一张画，要有昆明的特点。我想了一些时候，画了一幅：右上角画了一片倒挂着的浓绿的仙人掌，末端开出一朵金黄色的花；左下画了几朵青头菌和牛肝菌。题了这样几行字：",
        "开篇从友人求画写起，画了倒挂的仙人掌和青头菌、牛肝菌，以画面引出昆明的特点。",
        "以画画开篇，别致新颖；“倒挂着的浓绿的仙人掌”“金黄色的花”“青头菌和牛肝菌”，色彩鲜明，极具昆明地域特色；为下文写昆明的雨和雨季物产做铺垫。",
        [
            ("宁坤", "人名，汪曾祺的朋友"),
            ("倒挂", "倒着悬挂"),
            ("仙人掌", "多年生植物，茎肉质，耐旱，花多黄色"),
            ("末端", "最末端、尽头"),
            ("青头菌", "云南特产的一种食用菌，菌盖呈浅绿色"),
            ("牛肝菌", "一种食用菌，菌肉肥厚，色如牛肝"),
        ],
    ),
    (
        "昆明人家常于门头挂仙人掌一片以辟邪，仙人掌悬空倒挂，尚能存活开花。于此可见仙人掌生命之顽强，亦可见昆明雨季空气之湿润。雨季则有青头菌、牛肝菌，味极鲜腴。",
        "画上的题字：解释昆明人家门头挂仙人掌辟邪的习俗，点出仙人掌生命力顽强和昆明雨季空气湿润，以及雨季菌子的鲜美。",
        "题字本身就是一段精炼的说明文字；“辟邪”写民俗，“存活开花”写生命力，“湿润”写气候，“鲜腴”写菌子，寥寥数语涵盖昆明的民俗、气候、物产；“鲜腴”二字准确而有味。",
        [
            ("门头", "门框上方的部位"),
            ("辟邪", "避免或驱除邪祟"),
            ("悬空", "悬在空中，没有着地"),
            ("尚能", "还能够"),
            ("顽强", "坚强、不屈服"),
            ("湿润", "潮湿润泽"),
            ("鲜腴", "新鲜肥美。腴，肥美"),
        ],
    ),
    (
        "我想念昆明的雨。",
        "独句成段，直接抒发对昆明雨的思念，点明题旨。",
        "独句成段，简洁有力；“想念”二字奠定全文的抒情基调；与结尾“我想念昆明的雨”首尾呼应，结构圆合。",
        [
            ("想念", "思念、怀念"),
        ],
    ),
    # === 第二部分 ===
    (
        "我以前不知道有所谓雨季。“雨季”，是到昆明以后才有了具体感受的。",
        "交代“雨季”这一概念是到昆明后才有具体感受的，引出下文对昆明雨季的描写。",
        "“以前不知道”与“到昆明以后才有了具体感受”对比，突出昆明雨季的独特；自然过渡到下文对雨季的具体描写。",
        [
            ("所谓", "所说的、用于复说或引证"),
            ("具体感受", "真切的、实在的体会"),
        ],
    ),
    (
        "我不记得昆明的雨季有多长，从几月到几月，好像是相当长的。但是并不使人厌烦。因为是下下停停、停停下下，不是连绵不断，下起来没完。而且并不使人气闷。我觉得昆明雨季气压不低，人很舒服。",
        "写昆明雨季的特点：时间长但不厌烦，下下停停不连绵，气压不低人舒服。",
        "“不记得……好像是相当长的”，以不确定的语气写雨季之长，反而真实可信；“下下停停、停停下下”，叠词反复，写出雨的节奏；“不是连绵不断，下起来没完”，以否定句式突出昆明雨的可亲；“气压不低，人很舒服”，从身体感受写雨的宜人。",
        [
            ("相当", "表示程度高，比较"),
            ("厌烦", "因不耐烦而讨厌"),
            ("连绵不断", "连续不间断"),
            ("气闷", "空气不流通而使人感到憋闷"),
            ("气压", "大气的压强，气压低时人会感到憋闷"),
        ],
    ),
    (
        "昆明的雨季是明亮的、丰满的，使人动情的。城春草木深，孟夏草木长。昆明的雨季，是浓绿的。草木的枝叶里的水分都到了饱和状态，显示出过分的、近于夸张的旺盛。",
        "总写昆明雨季的特点：明亮、丰满、使人动情，草木浓绿旺盛。",
        "“明亮的、丰满的，使人动情的”，三个形容词排比，概括雨季的总体特征；引用杜甫“城春草木深”和陶渊明“孟夏草木长”的诗句，以古诗写昆明草木，典雅而贴切；“饱和状态”“过分的、近于夸张的旺盛”，以科学术语和夸张手法写草木的蓬勃，语言幽默而准确。",
        [
            ("丰满", "充足、丰富"),
            ("动情", "激起情感、感动"),
            ("城春草木深", "杜甫《春望》诗句，写春天城中草木茂盛"),
            ("孟夏", "夏季的第一个月，即农历四月"),
            ("浓绿", "深绿、很绿"),
            ("饱和", "在一定温度和压力下，溶液所含溶质达到最大限度，文中指水分达到极点"),
            ("夸张", "夸大，言过其实"),
            ("旺盛", "生命力强、茂盛"),
        ],
    ),
    # === 第三部分 ===
    (
        "我的那张画是写实的。我确实亲眼看见过倒挂着还能开花的仙人掌。旧日昆明人家门头上用以辟邪的多是这样一些东西：一面小镜子，周围画着八卦，下面便是一片仙人掌，——在仙人掌上扎一个洞，用麻线穿了，挂在钉子上。昆明仙人掌多，且极肥大。有些人家在菜园的周围种了一圈仙人掌以代替篱笆。——种了仙人掌，猪羊便不敢进园吃菜了。仙人掌有刺，猪和羊怕扎。",
        "印证画是写实的：具体描写昆明人家门头挂仙人掌辟邪的习俗，以及仙人掌的肥大和用途。",
        "“写实的”“确实亲眼看见”，强调真实，增强可信度；详细描写挂仙人掌的方法（扎洞、穿麻线、挂钉子），如在目前；“以代替篱笆”“猪羊怕扎”，写仙人掌的实用价值，充满生活气息；破折号的使用使行文自然，如话家常。",
        [
            ("写实", "真实地描绘事物"),
            ("旧日", "过去、从前"),
            ("八卦", "我国古代的一套有象征意义的符号，常用于占卜和辟邪"),
            ("麻线", "用麻搓成的线"),
            ("肥大", "又大又肥"),
            ("菜园", "种蔬菜的园子"),
            ("篱笆", "用竹子、芦苇、树枝等编成的遮拦物"),
            ("刺", "植物的尖刺"),
        ],
    ),
    (
        "昆明菌子极多。雨季逛菜市场，随时可以看到各种菌子。最多，也最便宜的是牛肝菌。牛肝菌下来的时候，家家饭馆卖炒牛肝菌，连西南联大食堂的桌子上都可以有一碗。牛肝菌色如牛肝，滑，嫩，鲜，香，很好吃。炒牛肝菌须多放蒜，否则容易使人晕倒。青头菌比牛肝菌略贵。这种菌子炒熟了也还是浅绿色的，格调比牛肝菌高。菌中之王是鸡枞，味道鲜浓，无可方比。鸡枞是名贵的山珍，但并不真的贵得惊人。一盘红烧鸡枞的价钱和一碗黄焖鸡不相上下，因为这东西在云南并不难得。有一个笑话：有人从昆明坐火车到呈贡，在车上看到地上有一棵鸡枞，他跳下去把鸡枞捡了，紧赶两步，还能追上火车。这笑话用意在说明昆明到呈贡的火车之慢，但也说明鸡枞随处可见。有一种菌子，中吃不中看，叫做干巴菌。乍一看那样子，真叫人怀疑：这种东西也能吃？！颜色深褐带绿，有点像一堆半干的牛粪或一个被踩破了的马蜂窝。里头还有许多草茎、松毛，乱七八糟！可是下点功夫，把草茎松毛择净，撕成蟹腿肉粗细的丝，和青辣椒同炒，入口便会使你张目结舌：这东西这么好吃？！还有一种菌子，中看不中吃，叫鸡油菌。都是一般大小，有一块银圆那样大，滴溜儿圆，颜色浅黄，恰似鸡油一样。这种菌子只能做菜时配色用，没甚味道。",
        "详写昆明雨季的菌子：牛肝菌、青头菌、鸡枞、干巴菌、鸡油菌，各有特点，写得生动有趣。",
        "这是全文最精彩的段落之一。以“昆明菌子极多”总起，然后分别写五种菌子，有详有略；牛肝菌写其普遍和美味，青头菌写其“格调高”，鸡枞写其名贵却常见（用笑话佐证），干巴菌写其“中吃不中看”（先抑后扬，以“牛粪”“马蜂窝”喻其丑，以“张目结舌”写其味美），鸡油菌写其“中看不中吃”；对比手法（中吃不中看/中看不中吃）、比喻、口语化的语言，使这段文字妙趣横生，充满生活气息。",
        [
            ("菌子", "（jùn）即蘑菇，云南方言称菌子"),
            ("逛", "闲游、游览"),
            ("西南联大", "国立西南联合大学，抗战时期北大、清华、南开在昆明合并成立"),
            ("滑", "口感光滑爽口"),
            ("须", "必须、需要"),
            ("晕倒", "昏迷倒下，指牛肝菌处理不当会中毒"),
            ("格调", "风格、品位"),
            ("鸡枞", "（cōng）一种名贵的食用菌，生长在白蚁窝上"),
            ("无可方比", "没有可以相比的，形容独一无二"),
            ("山珍", "山区出产的珍贵食品"),
            ("不相上下", "分不出高低，形容程度相等"),
            ("呈贡", "地名，在昆明东南"),
            ("干巴菌", "云南特产的一种菌子，味美但外观不好看"),
            ("中吃不中看", "好吃但不好看"),
            ("乍一看", "初一看、猛一看"),
            ("深褐", "深棕色"),
            ("牛粪", "牛的粪便"),
            ("马蜂窝", "马蜂的巢穴"),
            ("草茎", "草的茎"),
            ("松毛", "松针，松树的叶子"),
            ("择净", "挑选干净"),
            ("蟹腿肉", "螃蟹腿里的肉，形容丝的粗细"),
            ("张目结舌", "睁大眼睛说不出话，形容惊讶"),
            ("鸡油菌", "一种菌子，色黄如鸡油，好看但味道一般"),
            ("银圆", "旧时使用的银质硬币"),
            ("滴溜儿圆", "形容非常圆"),
            ("恰似", "恰好像、正好像"),
            ("配色", "配合颜色，增加菜肴的美观"),
            ("没甚", "没有什么"),
        ],
    ),
    (
        "雨季的果子，是杨梅。卖杨梅的都是苗族女孩子，戴一顶小花帽子，穿着扳尖的绣了满帮花的鞋，坐在人家阶石的一角，不时吆唤一声：“卖杨梅——”，声音娇娇的。她们的声音使得昆明雨季的空气更加柔和了。昆明的杨梅很大，有一个乒乓球那样大，颜色黑红黑红的，叫做“火炭梅”。这个名字起得真好，真是像一球烧得炽红的火炭！一点都不酸！我吃过苏州洞庭山的杨梅、井冈山的杨梅，好像都比不上昆明的火炭梅。",
        "写雨季的杨梅：卖杨梅的苗族女孩的形象和声音，以及昆明杨梅的大、红、甜。",
        "苗族女孩的外貌描写（小花帽子、扳尖绣花鞋）和声音（“娇娇的”），充满民族风情；“声音使得空气更加柔和”，以听觉写触觉，通感手法，写出雨季的温柔；“火炭梅”的比喻生动形象；“一点都不酸”“都比不上”，以对比和夸张写杨梅的甜美。",
        [
            ("杨梅", "一种水果，味酸甜，成熟时深红色或紫红色"),
            ("苗族", "我国少数民族之一，主要分布在云南、贵州等地"),
            ("扳尖", "一种鞋头翘起的样式"),
            ("满帮花", "整个鞋帮都绣满花"),
            ("阶石", "台阶前的石头"),
            ("吆唤", "吆喝、呼唤"),
            ("娇娇", "形容声音娇嫩柔美"),
            ("柔和", "温和、温柔"),
            ("乒乓球", "一种球类运动用的球，很小很轻"),
            ("黑红黑红", "形容颜色又黑又红"),
            ("火炭梅", "昆明杨梅的一个品种，色黑红如烧红的火炭"),
            ("炽红", "（chì）火红、通红"),
            ("洞庭山", "在江苏苏州，产杨梅"),
            ("井冈山", "在江西，也产杨梅"),
        ],
    ),
    (
        "雨季的花是缅桂花。缅桂花即白兰花，北京叫做“把儿兰”（这个名字真不好听）。云南把这种花叫做缅桂花，可能最初这种花是从缅甸传入的，而花的香味又有点像桂花，其实这跟桂花实在没有什么关系。——不过话又说回来，别处叫它白兰、把儿兰，它和兰花也挨不上呀，也不过是因为它很香，香得像兰花。我家在若园巷，院子里有一棵大缅桂，一到夏天，满院子都是香的。房东母女俩，时常摘了花，用别针别在衣襟上。有时送来一个七寸盘子，里面摆得满满的缅桂花！带着雨珠的缅桂花使我的心软软的，不是怀人，不是思乡。",
        "写雨季的缅桂花：名字的由来、院子里的缅桂树、房东母女送花，以及带雨珠的缅桂花带给作者的柔软感受。",
        "先考证缅桂花名字的由来，语言幽默（“这个名字真不好听”“也不过是因为它很香”），如话家常；“满院子都是香的”，以夸张写花香之浓；“用别针别在衣襟上”“七寸盘子里摆得满满的”，写昆明人的生活情趣；“带着雨珠的缅桂花使我的心软软的，不是怀人，不是思乡”，含蓄地写出一种难以言说的温柔感动，余味深长。",
        [
            ("缅桂花", "即白兰花，花白色，香气浓郁，云南俗称缅桂花"),
            ("白兰花", "一种常绿乔木，花白色，有浓香"),
            ("把儿兰", "北京对白兰花的俗称"),
            ("缅甸", "东南亚国家，与云南接壤"),
            ("桂花", "一种常绿灌木或小乔木，花小，有浓香"),
            ("若园巷", "昆明的一条巷子名，汪曾祺在昆明时曾住于此"),
            ("别针", "一种用来固定衣服或装饰的针"),
            ("衣襟", "上衣的前幅、胸前部分"),
            ("七寸", "约23厘米，形容盘子大小"),
            ("雨珠", "雨滴、雨的水珠"),
            ("软软的", "形容内心温柔、感动"),
            ("怀人", "思念远方的人"),
            ("思乡", "思念家乡"),
        ],
    ),
    # === 第四部分 ===
    (
        "雨，有时是会引起人一点淡淡的乡愁的。李商隐的《夜雨寄北》是为许多久客的游子而写的。我有一天在积雨少住的早晨和德熙从联大新校舍到莲花池去。看了池里的满池清水，看了着比丘尼装的陈圆圆的石像（传说陈圆圆随吴三桂到云南后出家，暮年投莲花池而死），雨又下起来了。莲花池边有一条小街，有一个小酒店，我们走进去，要了一碟猪头肉，半市斤酒（装在上了绿釉的土瓷杯里），坐了下来。雨下大了。酒店有几只鸡，都把脑袋反插在翅膀下面，一只脚着地，一动也不动地在檐下站着。酒店院子里有一架大木香花。昆明木香花很多。有的小河沿岸都是木香。但是这样大的木香却不多见。一棵木香，爬在架上，把院子遮得严严的。密匝匝的细碎的绿叶，数不清的半开的白花和饱涨的花骨朵，都被雨水淋得湿透了。我们走不了，就这样一直坐到午后。四十年后，我还忘不了那天的情味，写了一首诗：",
        "写雨中与友人游莲花池、在小酒店喝酒的情景，雨中的鸡、木香花，以及四十年后仍难忘的情味。",
        "由雨引出乡愁，自然过渡到回忆；引用李商隐《夜雨寄北》，增添文学韵味；陈圆圆石像的传说，给莲花池增添了历史感；小酒店的细节（猪头肉、绿釉土瓷杯、鸡把脑袋插在翅膀下），写得细致入微，如在目前；木香花的描写（“密匝匝”“饱涨”“湿透”），以植物的旺盛反衬人的孤寂；“四十年后，我还忘不了那天的情味”，以时间的跨度写记忆之深，情感深沉。",
        [
            ("乡愁", "思念家乡的愁绪"),
            ("李商隐", "（约813—约858）唐代诗人，《夜雨寄北》是其名作"),
            ("久客", "长久在外做客"),
            ("游子", "离家在外或久居外乡的人"),
            ("积雨少住", "久雨之后稍微停了一会儿"),
            ("德熙", "人名，朱德熙，汪曾祺的同学、朋友，语言学家"),
            ("联大新校舍", "西南联合大学的新校舍"),
            ("莲花池", "昆明的一个地名，有池塘"),
            ("比丘尼", "佛教指尼姑，女性出家修行者"),
            ("陈圆圆", "明末清初名妓，传说随吴三桂到云南"),
            ("吴三桂", "（1612—1678）明末清初将领，曾引清兵入关"),
            ("暮年", "晚年"),
            ("一碟", "一盘、一小盘"),
            ("猪头肉", "用猪头制作的卤味菜"),
            ("市斤", "重量单位，一市斤等于500克"),
            ("绿釉", "绿色的釉子，涂在陶瓷表面"),
            ("土瓷杯", "粗陶杯子"),
            ("檐下", "屋檐下面"),
            ("木香花", "一种攀援灌木，花白色或黄色，有香气"),
            ("沿岸", "顺着河岸"),
            ("严严的", "形容严密、没有空隙"),
            ("密匝匝", "（zā）形容很稠密的样子"),
            ("细碎", "细小而零碎"),
            ("饱涨", "饱满得像要胀开"),
            ("花骨朵", "没有开放的花"),
            ("湿透", "全部湿透了"),
            ("情味", "情趣、意味"),
        ],
    ),
    (
        "莲花池外少行人，野店苔痕一寸深。浊酒一杯天过午，木香花湿雨沉沉。",
        "作者写的诗，描绘莲花池外雨中的情景：行人稀少、野店苔深、一杯浊酒、木香花湿，意境悠远。",
        "这首诗是对前文情景的诗意概括；“少行人”“苔痕一寸深”写环境的清幽；“浊酒一杯”写生活的简朴；“木香花湿雨沉沉”以景结情，雨中的木香花和沉沉的雨，烘托出淡淡的乡愁和悠远的情味；诗的意境与全文的散文风格相得益彰。",
        [
            ("野店", "郊外的小旅店"),
            ("苔痕", "苔藓的痕迹"),
            ("浊酒", "浑浊的酒，指普通的酒"),
            ("过午", "过了中午"),
            ("沉沉", "形容雨大而密，也形容心情沉重"),
        ],
    ),
    (
        "我想念昆明的雨。",
        "再次独句成段，与开头呼应，收束全文，强化对昆明雨的思念。",
        "与第三段“我想念昆明的雨”首尾呼应，反复咏叹，使文章结构圆合；独句成段，情感深沉，余味无穷；“想念”二字，包含了对昆明的人、事、物、景的全部怀念。",
        [
            ("想念", "思念、怀念"),
        ],
    ),
]

# 分部分
parts = [
    ("第一部分", "画中昆明，引出雨季", "1–3 段", "从友人求画写起，以倒挂仙人掌和菌子的画面引出昆明的雨，独句点题。"),
    ("第二部分", "雨季感受，明亮丰满", "4–6 段", "写昆明雨季的特点：时间长但不厌烦，下下停停，明亮丰满，草木浓绿旺盛。"),
    ("第三部分", "雨季物产，菌果花香", "7–10 段", "写昆明雨季的物产：仙人掌、各种菌子、杨梅、缅桂花，充满生活气息。"),
    ("第四部分", "雨中乡愁，首尾呼应", "11–13 段", "写雨中与友人游莲花池、小酒店喝酒的情景，以诗和反复咏叹收束全文。"),
]

# 每段对应的部分索引 (0-based)
para_part = [0,0,0, 1,1,1, 2,2,2,2, 3,3,3]

fulltext_paras = [p[0] for p in paragraphs]

def annotate(text, annos):
    items = sorted(annos, key=lambda x: len(x[0]), reverse=True)
    result = text
    used = set()
    for word, note in items:
        if word in used:
            continue
        idx = result.find(word)
        if idx != -1:
            before = result[:idx]
            if before.count("<span") == before.count("</span>"):
                span = f'<span class="anno-word" data-note="{note}">{word}</span>'
                result = result[:idx] + span + result[idx+len(word):]
                used.add(word)
    return result

# 构建 verse_html，按部分分组
verse_html = ""
current_part = -1
for i, (orig, content, method, annos) in enumerate(paragraphs):
    pi = para_part[i]
    if pi != current_part:
        current_part = pi
        pname, ptitle, prange, poverview = parts[pi]
        verse_html += f'''      <div class="part-head"><span class="p-num">{pname}</span><h3>{ptitle}</h3><span class="range">{prange}</span></div>
      <div class="part-overview">{poverview}</div>
'''
    orig_ann = annotate(orig, annos)
    verse_html += f'''      <div class="verse" id="l{i+1}" data-i="{i}">
        <div class="v-top"><span class="v-no">{i+1}</span><div class="v-line">{orig_ann}</div></div>
        <details class="v-more">
          <summary>内容 · 手法</summary>
          <div class="d-body">
            <div class="v-sec"><b class="v-label">内容概括</b>
              <div class="v-trans">{content}</div>
            </div>
            <div class="v-sec"><b class="v-label">手法分析</b>
              <div class="d-body"><p>{method}</p></div>
            </div>
          </div>
        </details>
      </div>
'''

fulltext_html = ""
for para in fulltext_paras:
    fulltext_html += f'    <div class="pl">{para}</div>\n'

dict_words = [
    {"w":"腴","py":"yú","q":"雨季则有青头菌、牛肝菌，味极鲜□","tip":"「腴」月字旁，肥美；不要写成「谀」（言字旁，谄媚）"},
    {"w":"厌","py":"yàn","q":"但是并不使人□烦","tip":"「厌」厂字头，嫌恶；不要写成「压」"},
    {"w":"绵","py":"mián","q":"不是连□不断，下起来没完","tip":"「绵」绞丝旁，连续；不要写成「棉」（木字旁）"},
    {"w":"闷","py":"mèn","q":"而且并不使人气□","tip":"「闷」门字旁，憋闷；多音字，此处读mèn"},
    {"w":"饱","py":"bǎo","q":"草木的枝叶里的水分都到了□和状态","tip":"「饱」食字旁，满；不要写成「抱」（提手旁）"},
    {"w":"卦","py":"guà","q":"周围画着八□，下面便是一片仙人掌","tip":"「卦」卜字旁，占卜符号；不要写成「挂」（提手旁）"},
    {"w":"篱","py":"lí","q":"种了一圈仙人掌以代替□笆","tip":"「篱」竹字头，篱笆；不要写成「离」"},
    {"w":"笆","py":"ba","q":"种了一圈仙人掌以代替篱□","tip":"「笆」竹字头，用竹片等编成的遮拦物；不要写成「巴」"},
    {"w":"菌","py":"jùn","q":"昆明□子极多","tip":"「菌」草字头，蘑菇；多音字，此处读jùn不读jūn"},
    {"w":"枞","py":"cōng","q":"菌中之王是鸡□，味道鲜浓","tip":"「枞」木字旁，鸡枞是名贵食用菌；不要写成「从」"},
    {"w":"褐","py":"hè","q":"颜色深□带绿，有点像一堆半干的牛粪","tip":"「褐」衣字旁，粗布衣服，引申为黄黑色；不要写成「喝」"},
    {"w":"粪","py":"fèn","q":"有点像一堆半干的牛□","tip":"「粪」米字头，粪便；笔画较多，注意下面是「共」"},
    {"w":"蜂窝","py":"fēng wō","q":"或一个被踩破了的马□□","tip":"「蜂」虫字旁，昆虫；「窝」穴宝盖，巢穴；两字都要写对"},
    {"w":"择","py":"zhái","q":"把草茎松毛□净，撕成蟹腿肉粗细的丝","tip":"「择」提手旁，挑选；多音字，此处读zhái（口语）不读zé"},
    {"w":"蟹","py":"xiè","q":"撕成□腿肉粗细的丝","tip":"「蟹」虫字旁，螃蟹；笔画多，注意上面是「解」"},
    {"w":"吆","py":"yāo","q":"不时□唤一声：卖杨梅","tip":"「吆」口字旁，大声喊；不要写成「么」"},
    {"w":"炽","py":"chì","q":"真是像一球烧得□红的火炭","tip":"「炽」火字旁，火旺；不要写成「织」（绞丝旁）"},
    {"w":"缅甸","py":"miǎn diàn","q":"可能最初这种花是从□□传入的","tip":"「缅」绞丝旁，遥远；「甸」田字旁，郊外；两字都要写对"},
    {"w":"釉","py":"yòu","q":"装在上了绿□的土瓷杯里","tip":"「釉」采字旁，涂在陶瓷表面的物质；不要写成「油」（三点水）"},
    {"w":"檐","py":"yán","q":"一动也不动地在□下站着","tip":"「檐」木字旁，屋檐；不要写成「瞻」（目字旁）"},
    {"w":"匝匝","py":"zā zā","q":"密□□的细碎的绿叶","tip":"「匝」三框儿，周、圈；叠词「密匝匝」形容稠密，两字都写「匝」"},
    {"w":"浊","py":"zhuó","q":"□酒一杯天过午","tip":"「浊」三点水，浑浊；与「烛」（火字旁）区分"},
    {"w":"苔","py":"tái","q":"野店□痕一寸深","tip":"「苔」草字头，苔藓；不要写成「台」"},
]

dict_notes = [
    {"w":"鲜腴","a":"新鲜肥美。腴，肥美","q":"味极鲜腴"},
    {"w":"辟邪","a":"避免或驱除邪祟","q":"挂仙人掌一片以辟邪"},
    {"w":"连绵不断","a":"连续不间断","q":"不是连绵不断"},
    {"w":"孟夏","a":"夏季的第一个月，即农历四月","q":"孟夏草木长"},
    {"w":"饱和","a":"达到最大限度","q":"水分都到了饱和状态"},
    {"w":"八卦","a":"我国古代有象征意义的符号，常用于占卜","q":"周围画着八卦"},
    {"w":"篱笆","a":"用竹子、树枝等编成的遮拦物","q":"以代替篱笆"},
    {"w":"菌子","a":"即蘑菇，云南方言","q":"昆明菌子极多"},
    {"w":"格调","a":"风格、品位","q":"格调比牛肝菌高"},
    {"w":"鸡枞","a":"一种名贵的食用菌","q":"菌中之王是鸡枞"},
    {"w":"无可方比","a":"没有可以相比的","q":"味道鲜浓，无可方比"},
    {"w":"山珍","a":"山区出产的珍贵食品","q":"鸡枞是名贵的山珍"},
    {"w":"不相上下","a":"分不出高低","q":"价钱和一碗黄焖鸡不相上下"},
    {"w":"干巴菌","a":"云南特产菌子，味美但外观不好看","q":"叫做干巴菌"},
    {"w":"中吃不中看","a":"好吃但不好看","q":"中吃不中看"},
    {"w":"张目结舌","a":"睁大眼睛说不出话，形容惊讶","q":"入口便会使你张目结舌"},
    {"w":"鸡油菌","a":"一种菌子，色黄如鸡油，好看但味一般","q":"叫鸡油菌"},
    {"w":"滴溜儿圆","a":"形容非常圆","q":"滴溜儿圆"},
    {"w":"扳尖","a":"一种鞋头翘起的样式","q":"穿着扳尖的绣了满帮花的鞋"},
    {"w":"吆唤","a":"吆喝、呼唤","q":"不时吆唤一声"},
    {"w":"炽红","a":"火红、通红","q":"烧得炽红的火炭"},
    {"w":"缅桂花","a":"即白兰花，花白色，香气浓郁","q":"雨季的花是缅桂花"},
    {"w":"衣襟","a":"上衣的前幅、胸前部分","q":"用别针别在衣襟上"},
    {"w":"乡愁","a":"思念家乡的愁绪","q":"引起人一点淡淡的乡愁"},
    {"w":"积雨少住","a":"久雨之后稍微停了一会儿","q":"在积雨少住的早晨"},
    {"w":"比丘尼","a":"佛教指尼姑","q":"着比丘尼装的陈圆圆的石像"},
    {"w":"暮年","a":"晚年","q":"暮年投莲花池而死"},
    {"w":"绿釉","a":"绿色的釉子","q":"上了绿釉的土瓷杯"},
    {"w":"密匝匝","a":"形容很稠密的样子","q":"密匝匝的细碎的绿叶"},
    {"w":"饱涨","a":"饱满得像要胀开","q":"数不清的半开的白花和饱涨的花骨朵"},
    {"w":"情味","a":"情趣、意味","q":"我还忘不了那天的情味"},
    {"w":"浊酒","a":"浑浊的酒，指普通的酒","q":"浊酒一杯天过午"},
    {"w":"沉沉","a":"形容雨大而密，也形容心情沉重","q":"木香花湿雨沉沉"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《昆明的雨》汪曾祺</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 汪曾祺</div>
  <h1 class="hero-title">昆明的雨</h1>
</header>

<nav class="nav">
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
</nav>

<main class="wrap">
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《昆明的雨》是汪曾祺写于1984年的一篇回忆性散文，选自《汪曾祺散文》。文章从友人求画写起，以“我想念昆明的雨”独句点题，回忆了抗战时期在西南联大读书时昆明的雨季：明亮丰满的雨季、顽强的仙人掌、各种鲜美的菌子、苗族女孩卖的杨梅、带着雨珠的缅桂花，以及莲花池边小酒店里的一杯浊酒。</p>
    <p>全文以“雨”为线索，将昆明的自然风物、民俗人情、个人记忆融为一体，语言平淡自然，如话家常，却在平淡中蕴含着深情。汪曾祺以其独特的“淡而有味”的散文风格，写出了对昆明的深切怀念，也写出了对生活的热爱。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>汪曾祺（1920—1997），江苏高邮人，现代作家、散文家、戏剧家，京派作家的代表人物。1939年考入西南联合大学中文系，师从沈从文。1940年开始发表作品，代表作有小说《受戒》《大淖记事》，散文《昆明的雨》《葡萄月令》《端午的鸭蛋》等，京剧剧本《沙家浜》（主要改编者之一）。</p>
    <p style="margin-top:10px;color:var(--ink2)">汪曾祺的散文“淡而有味”，善于从日常生活中发现美，语言朴素自然，如话家常，却在平淡中蕴含着深情和文化底蕴。他被誉为“抒情的人道主义者，中国最后一个纯粹的文人，中国最后一个士大夫”。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>西南联大岁月：</b>1939年至1946年，汪曾祺在昆明西南联合大学中文系学习。抗战时期的昆明，虽然物质条件艰苦，但自然风光优美、民风淳朴、学术氛围自由。这段经历成为汪曾祺一生最珍贵的记忆，昆明的雨、菌子、杨梅、缅桂花，都深深印在他的脑海中。</p>
    <p style="margin-top:8px"><b>晚年回忆：</b>1984年，汪曾祺已六十四岁，离开昆明近四十年。友人宁坤求画，他画了昆明的仙人掌和菌子，由此触发了对昆明雨季的回忆，写下此文。文章写的是雨，怀念的却是整个昆明的生活和那段青春岁月。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文诵读《昆明的雨》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV14f4y1n7UU&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读昆明的雨"></iframe>
        <a href="https://www.bilibili.com/video/BV14f4y1n7UU" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>超级语文课：汪曾祺与昆明的雨</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV11idzB4Ej1&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="超级语文课汪曾祺与昆明的雨"></iframe>
        <a href="https://www.bilibili.com/video/BV11idzB4Ej1" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 词语 · 手法</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{fulltext_html}  </div>
  <div class="verse-list" id="verseList">
{verse_html}  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">人物 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>抒情主人公形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">“我”—— 热爱生活、品味生活的文人</div>
        <p>文中的“我”是一个善于从日常生活中发现美的人：逛菜市场看菌子，观察卖杨梅的苗族女孩，品味缅桂花的香气，在小酒店里看鸡、看木香花。他不写宏大的叙事，而是从细微处感受生活的美好。这种“生活家”的姿态，正是汪曾祺散文的独特魅力——在平淡中见深情，在细微处见真味。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">昆明人—— 淳朴热情、热爱生活</div>
        <p>门头挂仙人掌辟邪的人家、卖杨梅的苗族女孩（“声音娇娇的”）、送缅桂花的房东母女、小酒店里的寻常酒菜，构成了昆明人的群像。他们淳朴、热情、热爱生活，在艰苦的抗战岁月里依然保持着生活的情趣。正是这些普通人，让昆明的雨季充满了人情味。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">平淡自然，如话家常</div>
        <p>汪曾祺的散文语言朴素自然，没有华丽的辞藻和刻意的煽情。“我不记得昆明的雨季有多长”“这个名字起得真好”“这个名字真不好听”，如话家常，亲切自然。然而在平淡中蕴含着深情，“带着雨珠的缅桂花使我的心软软的”，平淡的文字里满是温柔。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">形散神聚，以雨为线</div>
        <p>文章取材广泛：画画、仙人掌、菌子、杨梅、缅桂花、莲花池、小酒店，看似散漫，实则以“雨”为线索贯穿全文。开篇点“我想念昆明的雨”，中间写雨季的种种风物，结尾以“我想念昆明的雨”呼应，首尾圆合，形散而神不散。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">细节生动，趣味盎然</div>
        <p>写菌子一段最为精彩：牛肝菌的“滑，嫩，鲜，香”，干巴菌“像一堆半干的牛粪”却“张目结舌”地好吃，鸡油菌“中看不中吃”——对比、比喻、口语化的表达，使这段文字妙趣横生。苗族女孩“声音娇娇的”、鸡“把脑袋反插在翅膀下面”，细节生动，如在目前。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">引用诗文，意境悠远</div>
        <p>引用杜甫“城春草木深”、陶渊明“孟夏草木长”写昆明草木的茂盛；引用李商隐《夜雨寄北》引出乡愁；结尾以自作诗“莲花池外少行人……”收束，诗的意境与散文的叙事相得益彰，增添了文化底蕴和悠远情味。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">我想念昆明的雨。</div>
        <p>独句成段，在文中出现两次（第三段和结尾），首尾呼应，反复咏叹。“想念”二字，包含了对昆明的人、事、物、景的全部怀念，是全文的情感主线。独句成段，简洁有力，情感深沉，余味无穷。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">昆明的雨季是明亮的、丰满的，使人动情的。</div>
        <p>三个形容词排比，概括昆明雨季的总体特征。“明亮”写雨的节奏（下下停停，不连绵），“丰满”写草木的旺盛，“使人动情”写雨的感染力。这句话是对昆明雨季的总评，也是全文的文眼之一。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">带着雨珠的缅桂花使我的心软软的，不是怀人，不是思乡。</div>
        <p>“心软软的”，以触觉写内心的感动，形象而含蓄。“不是怀人，不是思乡”，以否定句式写出一种难以言说的温柔——不是具体的思念某人或家乡，而是对那段美好时光的整体眷恋，对生活本身的感动。余味深长。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">莲花池外少行人，野店苔痕一寸深。浊酒一杯天过午，木香花湿雨沉沉。</div>
        <p>作者自作诗，是对前文情景的诗意概括。“少行人”“苔痕一寸深”写环境的清幽；“浊酒一杯”写生活的简朴；“木香花湿雨沉沉”以景结情，雨中的木香花和沉沉的雨，烘托出淡淡的乡愁和悠远的情味。诗的意境与全文风格相得益彰。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《昆明的雨》通过回忆抗战时期在昆明西南联大读书时的雨季生活，描写了昆明的自然风物（仙人掌、菌子、杨梅、缅桂花、木香花）和民俗人情（门头辟邪、苗族女孩卖花、房东送花、小酒店喝酒），表达了对昆明的深切怀念和对生活的热爱。</p>
    <p style="margin-top:10px">文章写的是雨，怀念的却是整个昆明的生活和那段青春岁月。在艰苦的抗战年代，作者依然能从日常生活中发现美、感受美，这种“生活家”的姿态和乐观豁达的人生态度，正是文章最动人的地方。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 用字 · 修辞 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">鲜腴</span><span class="acc-d">新鲜肥美。腴，肥美。</span></div>
      <div class="acc-item"><span class="acc-w">辟邪</span><span class="acc-d">避免或驱除邪祟。</span></div>
      <div class="acc-item"><span class="acc-w">连绵不断</span><span class="acc-d">连续不间断。</span></div>
      <div class="acc-item"><span class="acc-w">孟夏</span><span class="acc-d">夏季的第一个月，即农历四月。</span></div>
      <div class="acc-item"><span class="acc-w">饱和</span><span class="acc-d">达到最大限度。文中指水分达到极点。</span></div>
      <div class="acc-item"><span class="acc-w">八卦</span><span class="acc-d">我国古代有象征意义的符号，常用于占卜。</span></div>
      <div class="acc-item"><span class="acc-w">篱笆</span><span class="acc-d">用竹子、树枝等编成的遮拦物。</span></div>
      <div class="acc-item"><span class="acc-w">格调</span><span class="acc-d">风格、品位。</span></div>
      <div class="acc-item"><span class="acc-w">无可方比</span><span class="acc-d">没有可以相比的，形容独一无二。</span></div>
      <div class="acc-item"><span class="acc-w">张目结舌</span><span class="acc-d">睁大眼睛说不出话，形容惊讶。</span></div>
      <div class="acc-item"><span class="acc-w">滴溜儿圆</span><span class="acc-d">形容非常圆。</span></div>
      <div class="acc-item"><span class="acc-w">扳尖</span><span class="acc-d">一种鞋头翘起的样式。</span></div>
      <div class="acc-item"><span class="acc-w">炽红</span><span class="acc-d">火红、通红。</span></div>
      <div class="acc-item"><span class="acc-w">乡愁</span><span class="acc-d">思念家乡的愁绪。</span></div>
      <div class="acc-item"><span class="acc-w">积雨少住</span><span class="acc-d">久雨之后稍微停了一会儿。</span></div>
      <div class="acc-item"><span class="acc-w">比丘尼</span><span class="acc-d">佛教指尼姑，女性出家修行者。</span></div>
      <div class="acc-item"><span class="acc-w">暮年</span><span class="acc-d">晚年。</span></div>
      <div class="acc-item"><span class="acc-w">密匝匝</span><span class="acc-d">（zā）形容很稠密的样子。</span></div>
      <div class="acc-item"><span class="acc-w">饱涨</span><span class="acc-d">饱满得像要胀开。</span></div>
      <div class="acc-item"><span class="acc-w">情味</span><span class="acc-d">情趣、意味。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">鲜腴</span><span class="acc-d">（yú）月字旁，肥美；与「谀」（yú，谄媚，言字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">连绵</span><span class="acc-d">（mián）绞丝旁；与「棉」（木字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">菌子</span><span class="acc-d">（jùn）草字头；多音字，此处读jùn，不读jūn。</span></div>
      <div class="acc-item"><span class="acc-w">鸡枞</span><span class="acc-d">（cōng）木字旁；不要写成「鸡从」。</span></div>
      <div class="acc-item"><span class="acc-w">深褐</span><span class="acc-d">（hè）衣字旁；不要写成「喝」（口字旁）。</span></div>
      <div class="acc-item"><span class="acc-w">择净</span><span class="acc-d">（zhái）提手旁；多音字，口语中读zhái，不读zé。</span></div>
      <div class="acc-item"><span class="acc-w">炽红</span><span class="acc-d">（chì）火字旁；不要写成「织」（绞丝旁）。</span></div>
      <div class="acc-item"><span class="acc-w">绿釉</span><span class="acc-d">（yòu）采字旁；与「油」（三点水）区分。</span></div>
      <div class="acc-item"><span class="acc-w">屋檐</span><span class="acc-d">（yán）木字旁；与「瞻」（zhān，目字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">密匝匝</span><span class="acc-d">（zā）三框儿，周、圈；注意笔画。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞方法</h3>
      <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">“这些激情犹如狂风”（非本文）；本文中“颜色深褐带绿，有点像一堆半干的牛粪”“真是像一球烧得炽红的火炭”，比喻生动形象。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">干巴菌“中吃不中看”与鸡油菌“中看不中吃”对比；昆明火炭梅与苏州洞庭山、井冈山杨梅对比。</span></div>
      <div class="acc-item"><span class="acc-w">引用</span><span class="acc-d">引用杜甫“城春草木深”、陶渊明“孟夏草木长”、李商隐《夜雨寄北》，以及自作诗，增添文化底蕴。</span></div>
      <div class="acc-item"><span class="acc-w">通感</span><span class="acc-d">“她们的声音使得昆明雨季的空气更加柔和了”，以听觉写触觉；“使我的心软软的”，以触觉写内心感受。</span></div>
      <div class="acc-item"><span class="acc-w">反复</span><span class="acc-d">“我想念昆明的雨”在文中出现两次，首尾呼应，反复咏叹。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">以小见大</span><span class="acc-d">从仙人掌、菌子、杨梅、缅桂花等小事物入手，写出对昆明的深切怀念和对生活的热爱。</span></div>
      <div class="acc-item"><span class="acc-w">形散神聚</span><span class="acc-d">取材广泛，但以“雨”为线索贯穿全文，首尾呼应，结构圆合。</span></div>
      <div class="acc-item"><span class="acc-w">细节描写</span><span class="acc-d">善于捕捉生动的细节（鸡把脑袋插在翅膀下、苗族女孩的声音、干巴菌的外观和味道），如在目前。</span></div>
      <div class="acc-item"><span class="acc-w">语言平淡有味</span><span class="acc-d">如话家常，不事雕琢，却在平淡中蕴含深情，是汪曾祺散文的独特风格。</span></div>
    </div>
  </div>

</section>

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
  <div class="kai">《昆明的雨》</div>
  <div>汪曾祺 · 现代 · 出自《汪曾祺散文》</div>
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
{main_js}
</script>
<script>
var DICT_WORDS = {json.dumps(dict_words, ensure_ascii=False)};
var DICT_NOTES = {json.dumps(dict_notes, ensure_ascii=False)};
</script>

</body>
</html>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Generated: {OUT}")
print(f"Paragraphs: {len(paragraphs)}")
print(f"Anno count: {sum(len(p[3]) for p in paragraphs)}")
print(f"Words: {len(dict_words)}, Notes: {len(dict_notes)}")
