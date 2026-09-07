# -*- coding: utf-8 -*-
"""收尾脚本：追加题库和生成逻辑到 gen_puliurenjia.py 并执行"""
import os

TAIL = r'''

# ---------- 听写题库 ----------
DICT_WORDS = [
 {"w":"晌","py":"shǎng","q":Q("七月天，中伏大□午"),"tip":Q("「晌」日字旁+向，中午；不读 xiǎng")},
 {"w":"囱","py":"cōng","q":Q("全身上下就像刚从烟□里爬出来"),"tip":Q("「囱」撇+囗+夕，烟囱；不读 tǒng")},
 {"w":"擀","py":"gǎn","q":Q("手握着□面杖要梆他"),"tip":Q("「擀」扌旁+干，碾压；不读 hàn")},
 {"w":"阎","py":"yán","q":Q("奶奶老是怕□王爷打发白无常把他勾走"),"tip":Q("「阎」门字框+臽，阎王；不读 yàn")},
 {"w":"纤","py":"qiàn","q":Q("一见几个□夫赤身露体"),"tip":Q("「纤」纟旁+千，拉船绳；多音字，纤夫读 qiàn，纤维读 xiān")},
 {"w":"腌","py":"ā","q":Q("不能叫你们□臜了我们大姑娘小媳妇的眼睛"),"tip":Q("「腌」月字旁+奄，脏；腌臜读 ā zā，不读 yān")},
 {"w":"臜","py":"zā","q":Q("不能叫你们腌□了我们大姑娘小媳妇的眼睛"),"tip":Q("「臜」月字旁+赞，脏；腌臜读 ā zā")},
 {"w":"捯","py":"dáo","q":Q("紧一口慢一口□气"),"tip":Q("「捯」扌旁+到，喘气；不读 dào")},
 {"w":"唿","py":"hū","q":Q("几个纤夫见他们的伙伴挨了打，□哨而上"),"tip":Q("「唿」口字旁+忽，唿哨读 hū shào")},
 {"w":"绽","py":"zhàn","q":Q("掌舵的□裂了虎口"),"tip":Q("「绽」纟旁+定，裂开；不读 dìng")},
 {"w":"茧","py":"jiǎn","q":Q("一丈青大娘有一双长满老□的大手"),"tip":Q("「茧」草字头+虫，老茧；不读 jiǒng")},
 {"w":"呱","py":"gū","q":Q("一丈青大娘一听见孙子□□坠地的啼声"),"tip":Q("「呱」口字旁+瓜，婴儿哭声读 gū；不读 guā")},
 {"w":"拗","py":"niù","q":Q("可是，她□不过老头子"),"tip":Q("「拗」扌旁+幼，固执；多音字，拗不过读 niù，拗口读 ào")},
 {"w":"匿","py":"nì","q":Q("何满子却隐□在柳棵子地里"),"tip":Q("「匿」匚字旁+若，隐藏；不读 mì")},
 {"w":"苇","py":"wěi","q":Q("深藏到芦□丛中"),"tip":Q("「苇」草字头+韦，芦苇；不读 wéi")},
 {"w":"杠","py":"gàng","q":Q("奶奶抄起顶门□子"),"tip":Q("「杠」木字旁+工，粗棍；不读 gāng")},
 {"w":"讳","py":"huì","q":Q("何满子的爷爷，名□已不可考"),"tip":Q("「讳」讠旁+韦，名字；不读 wěi")},
 {"w":"耍","py":"shuǎ","q":Q("年轻的时候，当过义和团，会□大刀"),"tip":Q("「耍」而字头+女，舞弄；不读 yào")},
 {"w":"膺","py":"yīng","q":Q("在荣□这个尊称之后"),"tip":Q("「膺」广字头+隹+月，承受；不读 yìng")},
 {"w":"揣","py":"chuāi","q":Q("他腰里常常□着个北京老二酉堂出版的唱本"),"tip":Q("「揣」扌旁+耑，藏在怀里；多音字，揣着读 chuāi，揣测读 chuǎi")},
 {"w":"嚼","py":"jiáo","q":Q("说话也咬文□字"),"tip":Q("「嚼」口字旁+爵，斟酌；多音字，咬文嚼字读 jiáo，咀嚼读 jué")},
 {"w":"坍","py":"tān","q":Q("小城镇的文庙十有八九□塌破败"),"tip":Q("「坍」土字旁+丹，倒塌；不读 dān")},
 {"w":"垣","py":"yuán","q":Q("只剩下断壁残□"),"tip":Q("「垣」土字旁+亘，墙；不读 huán")},
 {"w":"蒿","py":"hāo","q":Q("埋没于蓬□荆棘之中"),"tip":Q("「蒿」草字头+高，野草；不读 gāo")},
 {"w":"垄","py":"lǒng","q":Q("穷得房无一间，地无一□"),"tip":Q("「垄」土字旁+龙，田埂；不读 lóng")},
 {"w":"塾","py":"shú","q":Q("也只念了三年私□"),"tip":Q("「塾」土字旁+孰，私塾；不读 shù")},
 {"w":"掂","py":"diān","q":Q("可是，□量一下自己这点财力"),"tip":Q("「掂」扌旁+店，斟酌；不读 diàn")},
 {"w":"砌","py":"qì","q":Q("没有白花花的银洋□台阶"),"tip":Q("「砌」石字旁+切，垒；不读 qiè")},
 {"w":"檎","py":"qín","q":Q("西隔壁那个在通州潞河中学念书的周□"),"tip":Q("「檎」木字旁+禽，人名用字；读 qín")},
 {"w":"聘","py":"pìn","q":Q("何大学问脑瓜子一热，就礼□这位老秀才"),"tip":Q("「聘」耳字旁+甹，聘请；不读 pìng")},
 {"w":"毡","py":"zhān","q":Q("难受得屁股下如坐针□"),"tip":Q("「毡」毛字旁+占，毡子；不读 zhàn")},
 {"w":"啭","py":"zhuàn","q":Q("一听见篱笆外柳树梢上莺啼燕□"),"tip":Q("「啭」口字旁+转，鸟鸣婉转；不读 zhuǎn")},
 {"w":"嘬","py":"zuō","q":Q("就想□着嘴唇学鸟叫"),"tip":Q("「嘬」口字旁+最，撅起；不读 chuài")},
 {"w":"锥","py":"zhuī","q":Q("老秀才的眼睛尖得像□子"),"tip":Q("「锥」钅旁+隹，钻孔工具；不读 zuī")},
 {"w":"剜","py":"wān","q":Q("心疼得就像一块一块□肉"),"tip":Q("「剜」刂旁+宛，用刀挖；不读 wǎn")},
 {"w":"蹚","py":"tāng","q":Q("脚□着露水"),"tip":Q("「蹚」足字旁+堂，从水中走；不读 táng")},
 {"w":"忿","py":"fèn","q":Q("索取了几百个铜板，□□而去"),"tip":Q("「忿」心字底+分，愤怒；不读 fēn")},
 {"w":"茬","py":"chá","q":Q("他满脸胡□，就像根根松针"),"tip":Q("「茬」草字头+在，胡子茬；不读 cá")},
 {"w":"噘","py":"juē","q":Q("小嘴□得能挂个油瓶儿"),"tip":Q("「噘」口字旁+厥，翘起；不读 jué")},
 {"w":"咒","py":"zhòu","q":Q("你还□我"),"tip":Q("「咒」口字旁+几+又，诅咒；不读 zǒu")},
 {"w":"卸","py":"xiè","q":Q("日本鬼子把咱们中国大□八块啦"),"tip":Q("「卸」卩旁+缶+止，搬下；不读 yù")},
 {"w":"捻","py":"niǎn","q":Q("拨动着一支牛拐骨□麻绳"),"tip":Q("「捻」扌旁+念，用手指搓；不读 niē")},
 {"w":"拐","py":"guǎi","q":Q("拨动着一支牛□骨捻麻绳"),"tip":Q("「拐」扌旁+另，膝盖骨；不读 guài")},
]

DICT_NOTES = [
 {"w":"拴贼扣儿","a":Q("用来拴贼的绳结，形容打得结实"),"q":Q("系的是拴贼扣儿")},
 {"w":"一交立夏","a":Q("一到立夏。交，到、进入"),"q":Q("一交立夏就光屁股")},
 {"w":"人配衣裳马配鞍","a":Q("民间俗语，人靠衣服打扮，马靠鞍装装饰"),"q":Q("人配衣裳马配鞍")},
 {"w":"讲究","a":Q("值得注意或考究的地方，这里指有特殊用意"),"q":Q("原来，这条兜肚大有讲究")},
 {"w":"勾魂索命","a":Q("勾取魂魄，索取性命，即致人死亡"),"q":Q("也就起不了勾魂索命的恶念")},
 {"w":"一丈青","a":Q("《水浒传》中扈三娘的绰号，这里形容何满子奶奶泼辣好强"),"q":Q("人人都管她叫一丈青大娘")},
 {"w":"招架","a":Q("抵挡、承受"),"q":Q("敢说找不出能够招架几个回合的敌手")},
 {"w":"一气呵成","a":Q("一口气做成，形容文章或说话紧凑连贯"),"q":Q("鼓点似的骂一天，一气呵成")},
 {"w":"歇晌","a":Q("中午休息、歇午觉"),"q":Q("也正是歇晌时分")},
 {"w":"纤夫","a":Q("用绳子拉船前进的人。纤，qiàn"),"q":Q("一见几个纤夫赤身露体")},
 {"w":"断喝","a":Q("急促地大声喊叫"),"q":Q("便断喝一声")},
 {"w":"歇脚打尖","a":Q("走路途中休息吃饭"),"q":Q("还没有歇脚打尖")},
 {"w":"耳旁风","a":Q("耳边吹过的风，比喻听过后不放在心上的话"),"q":Q("他们只当耳旁风")},
 {"w":"吆喝","a":Q("大声喊叫"),"q":Q("又吆喝了一声")},
 {"w":"腌臜","a":Q("弄脏、玷污。腌臜，ā zā"),"q":Q("不能叫你们腌臜了我们大姑娘小媳妇的眼睛")},
 {"w":"生楞儿","a":Q("鲁莽、愣头青的人"),"q":Q("那个不知好歹的年轻纤夫，是个生楞儿")},
 {"w":"捅了马蜂窝","a":Q("比喻闯了祸、惹了难对付的人"),"q":Q("这一下可捅了马蜂窝")},
 {"w":"勃然大怒","a":Q("突然变脸大发脾气"),"q":Q("一丈青大娘勃然大怒")},
 {"w":"抡圆了","a":Q("手臂抡得圆圆的，形容用力猛。抡，lūn"),"q":Q("老大一个耳刮子抡圆了扇过去")},
 {"w":"风吹乍蓬","a":Q("风吹起刚长出来的蓬草，形容人被打得转圈圈"),"q":Q("那个年轻的纤夫就像风吹乍蓬")},
 {"w":"捯气","a":Q("急促地喘气、呼吸困难。捯，dáo"),"q":Q("紧一口慢一口捯气")},
 {"w":"呻吟","a":Q("因痛苦而发出声音"),"q":Q("高一声低一声呻吟")},
 {"w":"唿哨","a":Q("把手指放在嘴里吹出来的尖锐声音。唿哨，hū shào"),"q":Q("几个纤夫见他们的伙伴挨了打，唿哨而上")},
 {"w":"不依不饶","a":Q("不肯罢休、不肯原谅"),"q":Q("一丈青大娘不依不饶")},
 {"w":"绽裂","a":Q("裂开。绽，zhàn"),"q":Q("掌舵的绽裂了虎口")},
 {"w":"驾驭","a":Q("驾驶、控制"),"q":Q("也驾驭不住")},
 {"w":"说和","a":Q("调解、劝说使和解"),"q":Q("说和了两三个时辰")},
 {"w":"开恩","a":Q("给予宽恕、施以恩惠"),"q":Q("一丈青大娘才算开恩放行")},
 {"w":"老茧","a":Q("手掌或脚掌上因长期摩擦而生的硬皮。茧，jiǎn"),"q":Q("一丈青大娘有一双长满老茧的大手")},
 {"w":"行家","a":Q("内行、对某种事情富有经验的人"),"q":Q("种地、撑船、打鱼都是行家")},
 {"w":"妙手回春","a":Q("称赞医生医术高明，能把垂危的病人治好"),"q":Q("都来找她妙手回春")},
 {"w":"镇八方","a":Q("能震慑、管理周围所有的地方和人"),"q":Q("别看一丈青大娘能镇八方")},
 {"w":"世代单传","a":Q("世世代代都是独生子"),"q":Q("何家世代单传")},
 {"w":"老生儿","a":Q("父母晚年生的儿子"),"q":Q("何满子的爷爷就是老生儿")},
 {"w":"落生","a":Q("出生、降生"),"q":Q("他父亲也是在一丈青大娘将近四十岁时才落生的")},
 {"w":"不同凡响","a":Q("不同于平常，形容人或事物很出色"),"q":Q("偏是何满子不同凡响")},
 {"w":"呱呱坠地","a":Q("形容婴儿出生。呱呱，gū gū"),"q":Q("一丈青大娘一听见孙子呱呱坠地的啼声")},
 {"w":"百家衣","a":Q("旧时为婴儿做的衣服，用从各家讨来的零碎布缝成，认为能保孩子长命百岁"),"q":Q("给何满子缝了一件五光十色的百家衣")},
 {"w":"长命锁","a":Q("挂在儿童脖子上的锁形饰物，迷信认为能锁住生命、保长命百岁"),"q":Q("还打造了一个分量不小的包铜镀金长命锁")},
 {"w":"心尖子","a":Q("心尖上的肉，比喻最疼爱的人"),"q":Q("何满子是一丈青大娘的心尖子")},
 {"w":"命根子","a":Q("生命和根子，比喻最最重要、不可缺少的人或物"),"q":Q("肺叶子，眼珠子，命根子")},
 {"w":"石印","a":Q("用石版印刷的方法，是旧时的一种印刷技术"),"q":Q("学的是石印")},
 {"w":"攀高枝儿","a":Q("比喻与地位比自己高的人结亲或拉关系"),"q":Q("好攀高枝儿")},
 {"w":"拗不过","a":Q("无法改变（别人的坚决意见）。拗，niù"),"q":Q("她拗不过老头子")},
 {"w":"文墨小康之家","a":Q("有一定文化、家境小康的家庭"),"q":Q("她到底是文墨小康之家出身")},
 {"w":"熏陶","a":Q("长期接触的人或事物对人的生活习惯、思想行为等逐渐产生某种影响"),"q":Q("却也熏陶得一身书香")},
 {"w":"识文断字","a":Q("能识字读书"),"q":Q("识文断字")},
 {"w":"中看而无用","a":Q("好看但没有用处"),"q":Q("就是一朵中看而无用的纸花")},
 {"w":"鸡吵鹅斗","a":Q("比喻家庭成员之间争吵不休"),"q":Q("可是一家子鸡吵鹅斗")},
 {"w":"左右为难","a":Q("左也不好，右也不好，形容不管怎么做都有难处"),"q":Q("老人家左右为难")},
 {"w":"千里搭长棚，没有不散的筵席","a":Q("俗语，比喻再好的聚会也有散的时候"),"q":Q("千里搭长棚，没有不散的筵席")},
 {"w":"到了儿","a":Q("到最后、最终"),"q":Q("到了儿点了头")},
 {"w":"野鸟不入笼","a":Q("野鸟不愿意进笼子，比喻人不受约束、自由自在"),"q":Q("就像野鸟不入笼")},
 {"w":"拍花子的","a":Q("旧时用药物迷人后拐走小孩的人"),"q":Q("怕给拍花子的拐走")},
 {"w":"提心吊胆","a":Q("形容十分担心或害怕"),"q":Q("老人家提心吊胆")},
 {"w":"隐匿","a":Q("隐藏、躲起来。匿，nì"),"q":Q("何满子却隐匿在柳棵子地里")},
 {"w":"青纱帐","a":Q("指夏秋间长得高而密的大面积高粱、玉米等，因像青纱做的帐子而得名"),"q":Q("潜伏在青纱帐内的豆棵下")},
 {"w":"顶门杠子","a":Q("顶门用的粗木棍。杠，gàng"),"q":Q("奶奶抄起顶门杠子")},
 {"w":"小祖宗儿","a":Q("对调皮孩子的昵称，含无奈和疼爱的意味"),"q":Q("叫了声：小祖宗儿")},
 {"w":"一脑门子官司","a":Q("形容心里有很多烦心事、脸色不好看"),"q":Q("哼哼哈哈，一脑门子官司")},
 {"w":"气不打一处来","a":Q("形容非常生气"),"q":Q("一丈青大娘气不打一处来")},
 {"w":"风火性儿","a":Q("形容脾气暴躁、像风火一样来得快"),"q":Q("爷爷是个风火性儿")},
 {"w":"勒令","a":Q("用命令方式强制人做某事"),"q":Q("勒令他在这一个歇晌的工夫")},
 {"w":"名讳","a":Q("名字。讳，huì，旧时指死去的帝王或尊长的名字"),"q":Q("名讳已不可考")},
 {"w":"叫得山响","a":Q("叫得像山一样响，形容名声很大、很响亮"),"q":Q("那可真是叫得山响")},
 {"w":"人高马大","a":Q("形容人身材高大魁梧"),"q":Q("何大学问人高马大")},
 {"w":"面如重枣","a":Q("脸色像深暗红色的枣子，形容人脸色红润。重，chóng"),"q":Q("面如重枣")},
 {"w":"关公相貌","a":Q("像关羽一样的相貌"),"q":Q("一副关公相貌")},
 {"w":"义和团","a":Q("清末活跃于北方的民间反帝爱国组织，以拳术和迷信活动为特点"),"q":Q("当过义和团")},
 {"w":"赶车把式","a":Q("赶车的能手。把式，能手、行家"),"q":Q("他给地主家当赶车把式")},
 {"w":"鞭花","a":Q("甩鞭子时发出的响声，也指甩鞭子的动作"),"q":Q("打一手好鞭花")},
 {"w":"打抱不平","a":Q("遇到不公平的事，挺身而出帮助受欺负的人"),"q":Q("爱打抱不平")},
 {"w":"两肋插刀","a":Q("肋骨上插着刀，比喻为朋友敢于冒险、牺牲"),"q":Q("为朋友敢两肋插刀")},
 {"w":"温驯","a":Q("温和顺从"),"q":Q("乖乖地像一群温驯的绵羊")},
 {"w":"保镖","a":Q("会技击的人受雇保护他人或财物安全"),"q":Q("他不但是赶马的，还是保镖的")},
 {"w":"三顾茅庐","a":Q("东汉末年刘备三次到隆中拜访诸葛亮，请他出山辅佐。比喻诚心诚意地邀请人"),"q":Q("不三顾茅庐，他是不出山的")},
 {"w":"礼贤下士","a":Q("对有才有德的人以礼相待，对一般有才能的人不计自己的身份去结交"),"q":Q("要的就是刘皇叔那样的礼贤下士")},
 {"w":"揭不开锅","a":Q("锅里没有米，无法做饭，形容穷得没饭吃"),"q":Q("伙友们有谁家揭不开锅")},
 {"w":"驴打滚儿","a":Q("高利贷的一种，利息越滚越多，像驴打滚一样"),"q":Q("跟牲口贩子借一笔驴打滚儿")},
 {"w":"过五关，斩六将","a":Q("三国关羽的故事，比喻克服重重困难、立下大功"),"q":Q("听他谈讲过五关，斩六将")},
 {"w":"云山雾罩","a":Q("形容说话漫无边际、使人摸不着头脑"),"q":Q("云山雾罩")},
 {"w":"戏谑","a":Q("用诙谐有趣的话开玩笑。戏谑，xì xuè"),"q":Q("人们一半是戏谑，一半是尊敬")},
 {"w":"荣膺","a":Q("光荣地接受或承当。膺，yīng，承受"),"q":Q("在荣膺这个尊称之后")},
 {"w":"不耻下问","a":Q("不以向地位比自己低、知识比自己少的人请教为可耻"),"q":Q("遇上生字儿，不耻下问")},
 {"w":"咬文嚼字","a":Q("过分地斟酌字句，多用来指死抠字眼儿。嚼，jiáo"),"q":Q("说话也咬文嚼字")},
 {"w":"威风凛凛","a":Q("形容声势或气派使人敬畏"),"q":Q("那形象是既威风凛凛又滑稽可笑")},
 {"w":"坍塌破败","a":Q("倒塌破败。坍，tān"),"q":Q("小城镇的文庙十有八九坍塌破败")},
 {"w":"断壁残垣","a":Q("残缺不全的墙壁，形容房屋遭受破坏后的凄凉景象。垣，yuán，墙"),"q":Q("只剩下断壁残垣")},
 {"w":"蓬蒿荆棘","a":Q("蓬草、蒿草、荆棘，泛指野草"),"q":Q("埋没于蓬蒿荆棘之中")},
 {"w":"年过花甲","a":Q("年龄超过六十岁。花甲，指六十岁"),"q":Q("已经年过花甲")},
 {"w":"睁眼瞎","a":Q("比喻不识字的人、文盲"),"q":Q("都是睁眼瞎")},
 {"w":"跳跶","a":Q("蹦跳、活动，比喻为生活奔波"),"q":Q("自个儿跳跶了大半辈子")},
 {"w":"鼓着肚子充胖","a":Q("挺着肚子假装肥胖，比喻没有能力硬撑"),"q":Q("已经是鼓着肚子充胖")},
 {"w":"老迈年高","a":Q("年纪大了"),"q":Q("自己已经老迈年高")},
 {"w":"聪慧灵秀","a":Q("聪明、灵巧、秀气"),"q":Q("何满子也真是聪慧灵秀")},
 {"w":"过耳不忘","a":Q("听过就不会忘记，形容记忆力极强"),"q":Q("爱听故事，过耳不忘")},
 {"w":"过目不忘","a":Q("看过就不会忘记，形容记忆力极强"),"q":Q("好问个字儿，过目不忘")},
 {"w":"假充圣人","a":Q("假装成有学问的圣人"),"q":Q("何大学问在孙子面前假充圣人")},
 {"w":"惊喜过望","a":Q("惊喜超过了期望"),"q":Q("何大学问惊喜过望")},
 {"w":"前清","a":Q("清朝灭亡后，对清朝的称呼"),"q":Q("遇见一位前清的老秀才")},
 {"w":"账房先生","a":Q("旧时店铺中管理钱财和账目人"),"q":Q("在这座骡马大店里当账房先生")},
 {"w":"魏碑","a":Q("北朝碑刻的统称，字体古朴雄健"),"q":Q("写一手魏碑好字")},
 {"w":"穷儒","a":Q("贫穷的读书人"),"q":Q("掌柜的打算辞退这个穷儒")},
 {"w":"脑瓜子一热","a":Q("一时冲动、头脑发热"),"q":Q("何大学问脑瓜子一热")},
 {"w":"礼聘","a":Q("以礼聘请。聘，pìn"),"q":Q("就礼聘这位老秀才到他家教专馆")},
 {"w":"专馆","a":Q("私塾的一种，由教师到学生家中专门教一个或几个学生"),"q":Q("就礼聘这位老秀才到他家教专馆")},
 {"w":"高高在上","a":Q("形容领导者脱离实际、高高在上"),"q":Q("他高高在上")},
 {"w":"太师椅","a":Q("一种旧式的宽大扶手椅"),"q":Q("坐一张太师椅")},
 {"w":"低首俯身","a":Q("低着头、弯着腰，形容恭顺"),"q":Q("何满子低首俯身")},
 {"w":"酸气冲天","a":Q("形容人迂腐、书呆子气十足"),"q":Q("老秀才又酸气冲天")},
 {"w":"诗云子曰","a":Q("《诗经》云、孔子曰，泛指儒家经典，形容人说话文绉绉"),"q":Q("开口诗云子曰")},
 {"w":"枯燥乏味","a":Q("单调、没有趣味"),"q":Q("何满子只觉得枯燥乏味")},
 {"w":"闷闷不乐","a":Q("因有不如意的事而心里不快活"),"q":Q("更加闷闷不乐")},
 {"w":"如坐针毡","a":Q("像坐在插着针的毡子上，形容心神不定、坐立不安。毡，zhān"),"q":Q("难受得屁股下如坐针毡")},
 {"w":"芒刺在背","a":Q("像芒和刺扎在背上，形容内心惶恐、坐立不安"),"q":Q("身上像芒刺在背")},
 {"w":"莺啼燕啭","a":Q("黄莺啼叫、燕子婉转鸣叫，形容春天鸟儿的鸣叫声。啭，zhuàn"),"q":Q("一听见篱笆外柳树梢上莺啼燕啭")},
 {"w":"嘬着嘴唇","a":Q("撅起嘴唇。嘬，zuō"),"q":Q("就想嘬着嘴唇学鸟叫")},
 {"w":"七上八下","a":Q("形容心里慌乱不安"),"q":Q("心里就七上八下")},
 {"w":"走了神儿","a":Q("注意力不集中、分心"),"q":Q("念书走了神儿")},
 {"w":"不打不成材","a":Q("不打骂就不能成才，是旧时的教育观念"),"q":Q("只有何大学问认定不打不成材")},
 {"w":"学规森严","a":Q("学校的规矩非常严厉"),"q":Q("非但不怪罪老秀才学规森严")},
 {"w":"呐喊助威","a":Q("大声喊叫帮助增加威势"),"q":Q("而且还从旁给老秀才呐喊助威")},
 {"w":"闹了饥荒","a":Q("发生了饥荒、经济上出现了困难"),"q":Q("不到一个月，何大学问就闹了饥荒")},
 {"w":"亏空","a":Q("支出超过收入的差额"),"q":Q("拉下了斗大的亏空")},
 {"w":"野马摘了笼头","a":Q("野马摘掉了笼头，比喻摆脱了束缚"),"q":Q("何满子就像野马摘了笼头")},
 {"w":"腻歪了","a":Q("厌恶、厌烦了"),"q":Q("一丈青大娘早就腻歪了老秀才")},
 {"w":"混不下去了","a":Q("无法继续待下去了"),"q":Q("老秀才混不下去了")},
 {"w":"忿忿而去","a":Q("愤怒地离开。忿忿，fèn fèn"),"q":Q("索取了几百个铜板，忿忿而去")},
 {"w":"形影不离","a":Q("像形体和它的影子那样分不开，形容彼此关系亲密、经常在一起"),"q":Q("何满子整天跟这位洋学生形影不离")},
 {"w":"过意不去","a":Q("心中不安、抱歉"),"q":Q("很觉得过意不去")},
 {"w":"埋怨","a":Q("因为事情不如意而对自己认为原因所在的人或事物表示不满"),"q":Q("埋怨一丈青大娘头发长，见识短")},
 {"w":"转怒为喜","a":Q("由愤怒转为高兴"),"q":Q("又不禁转怒为喜了")},
 {"w":"天伦之乐","a":Q("家庭亲人之间团聚的欢乐"),"q":Q("最大的盼头就是享受天伦之乐")},
 {"w":"磨蹭","a":Q("轻轻地摩擦"),"q":Q("最喜欢磨蹭孙子的脸蛋儿")},
 {"w":"梢马子","a":Q("褡裢，一种挂在肩上的口袋，可装东西"),"q":Q("都要给孙子带回一梢马子吃食")},
 {"w":"苍老了几岁","a":Q("看起来老了好几岁"),"q":Q("何大学问好像苍老了几岁")},
 {"w":"愁眉苦脸","a":Q("皱着眉头、哭丧着脸，形容愁苦的神情"),"q":Q("愁眉苦脸，垂头丧气")},
 {"w":"垂头丧气","a":Q("形容因失败或不顺利而情绪低落、萎靡不振的样子"),"q":Q("愁眉苦脸，垂头丧气")},
 {"w":"空空荡荡","a":Q("形容很空、什么也没有"),"q":Q("梢马子空空荡荡只有两层皮")},
 {"w":"心怀不满","a":Q("心里存有不满"),"q":Q("何满子对爷爷心怀不满")},
 {"w":"丧门神似的","a":Q("像丧门神一样，形容人脸色阴沉、带来晦气"),"q":Q("你一进家就丧门神似的")},
 {"w":"低头服软儿","a":Q("低下头认输、服软"),"q":Q("爷爷却不肯向奶奶低头服软儿")},
 {"w":"忍气吞声","a":Q("形容受了气而勉强忍耐、不说什么话"),"q":Q("忍气吞声")},
 {"w":"大卸八块","a":Q("把人切成八块，形容残酷肢解，这里比喻把中国分割得四分五裂"),"q":Q("日本鬼子把咱们中国大卸八块啦")},
 {"w":"满洲国","a":Q("1932年日本在东北建立的伪政权，以清朝末代皇帝溥仪为执政"),"q":Q("先在东三省立了个小宣统的满洲国")},
 {"w":"蒙疆政府","a":Q("1939年日本在内蒙古建立的伪政权，以德王为主席"),"q":Q("又在口外立了个德王的蒙疆政府")},
 {"w":"殷汝耕","a":Q("汉奸，1935年在日本指使下在河北通县成立伪冀东防共自治政府"),"q":Q("往后没有殷汝耕的公文护照")},
 {"w":"蒙疆军","a":Q("伪蒙疆政府的军队"),"q":Q("蒙疆军把我跟掌柜的扣住")},
 {"w":"扣住","a":Q("扣押、扣留"),"q":Q("蒙疆军把我跟掌柜的扣住")},
 {"w":"硬说","a":Q("强行说、无根据地说"),"q":Q("硬说我们是共产党")},
 {"w":"没收","a":Q("把财产等强制收归公有"),"q":Q("不过是为了没收那几百匹马")},
 {"w":"牢房","a":Q("监狱里关押犯人的房间"),"q":Q("掌柜的在牢房里上吊了")},
 {"w":"上吊","a":Q("用绳子吊在高处自杀"),"q":Q("掌柜的在牢房里上吊了")},
 {"w":"榨不出油水","a":Q("比喻榨不出钱财"),"q":Q("他们看我是个榨不出油水的穷光蛋")},
 {"w":"穷光蛋","a":Q("贫穷的人（骂人的话）"),"q":Q("他们看我是个榨不出油水的穷光蛋")},
 {"w":"哄传","a":Q("纷纷传说"),"q":Q("乡下哄传殷汝耕在通州坐了龙庭")},
 {"w":"坐了龙庭","a":Q("当了皇帝。龙庭，皇帝的朝庭"),"q":Q("乡下哄传殷汝耕在通州坐了龙庭")},
 {"w":"另立国号","a":Q("另外建立国家的称号"),"q":Q("另立国号")},
 {"w":"天怒人怨","a":Q("上天发怒、人民怨恨，形容作恶多端引起普遍愤怒"),"q":Q("天怒人怨，大地穿白挂孝")},
 {"w":"儿皇帝","a":Q("投靠外国、受外国支配的傀儡皇帝"),"q":Q("大骂殷汝耕是儿皇帝")},
 {"w":"石敬瑭","a":Q("五代时后晋的建立者，曾割让燕云十六州给契丹，自称儿皇帝，后以此比喻卖国求荣的傀儡"),"q":Q("管殷汝耕叫石敬瑭")},
 {"w":"五代残唐","a":Q("五代十国时期，唐朝灭亡后的混乱时期"),"q":Q("还给何满子讲了一段五代残唐的故事")},
 {"w":"坐了牢","a":Q("被关进了监狱"),"q":Q("原来爷爷坐了牢")},
 {"w":"险些扔了命","a":Q("几乎丢了性命"),"q":Q("还险些扔了命")},
 {"w":"满腔怒火","a":Q("心里充满了愤怒"),"q":Q("谁想爷爷竟把满腔怒火发泄到他身上")},
 {"w":"发泄","a":Q("把情绪等尽量发出"),"q":Q("谁想爷爷竟把满腔怒火发泄到他身上")},
 {"w":"硬逼","a":Q("强行逼迫"),"q":Q("而且还硬逼他在石板上写一百个字")},
 {"w":"手迹","a":Q("亲手写的字"),"q":Q("何满子一看见老秀才留下的这些手迹")},
 {"w":"烦透了","a":Q("厌烦到了极点"),"q":Q("心里烦透了")},
 {"w":"四脚八叉","a":Q("四肢张开、仰面朝天躺着的样子"),"q":Q("四脚八叉躺在北房东屋土炕上")},
 {"w":"打着呼噜","a":Q("打鼾"),"q":Q("打着呼噜睡大觉")},
 {"w":"哭丧着脸","a":Q("脸上带着哭相、不高兴"),"q":Q("奶奶哭丧着脸")},
 {"w":"外屋锅台","a":Q("外屋的灶台"),"q":Q("坐在外屋锅台上")},
 {"w":"拨动","a":Q("用手拨弄使转动"),"q":Q("拨动着一支牛拐骨捻麻绳")},
 {"w":"牛拐骨","a":Q("牛的膝盖骨，可用来捻麻绳"),"q":Q("拨动着一支牛拐骨捻麻绳")},
 {"w":"捻麻绳","a":Q("搓麻绳。捻，niǎn，用手指搓"),"q":Q("拨动着一支牛拐骨捻麻绳")},
 {"w":"怒气不息","a":Q("怒气不消"),"q":Q("依然怒气不息")},
 {"w":"搭救","a":Q("帮助人脱离危险"),"q":Q("只有一个人能搭救何满子")},
 {"w":"望眼欲穿","a":Q("眼睛都要望穿了，形容盼望殷切"),"q":Q("何满子望眼欲穿")},
 {"w":"救命星","a":Q("比喻能救命的人"),"q":Q("这颗救命星却迟迟不从东边闪现出来")},
 {"w":"迟迟","a":Q("长久、缓慢"),"q":Q("这颗救命星却迟迟不从东边闪现出来")},
 {"w":"闪现","a":Q("一瞬间出现"),"q":Q("这颗救命星却迟迟不从东边闪现出来")},
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

acc_html = "".join(
    '  <div class="box"><div class="acc-cat">\n      <h3>%s</h3>\n%s\n    </div></div>\n' %
    (esc(title), "\n".join('      <div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>'
                           % (esc(w), esc(d)) for (w, d) in items))
    for (title, items) in ACC)

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
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 用字 · 修辞 · 写法 · 文化</span></div>
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
  <div class="kai">《蒲柳人家》</div>
  <div>刘绍棠 · 现代 · 选自《蒲柳人家》</div>
  <div>本篇最初发表于 1980 年《十月》第二期</div>
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
<title>《蒲柳人家》刘绍棠</title>
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
'''

# 追加到 gen_puliurenjia.py
with open(r"D:\App\Apps\yanshi\tools\gen_puliurenjia.py", "a", encoding="utf-8") as f:
    f.write(TAIL)

print("Appended tail, total length:", len(open(r"D:\App\Apps\yanshi\tools\gen_puliurenjia.py", encoding="utf-8").read()))
