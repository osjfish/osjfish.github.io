# -*- coding: utf-8 -*-
"""生成《蝉》法布尔 课件（说明文）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\chan-fabuer.html"
FS_KEY = "chan_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

paragraphs = [
    (
        "我有很好的环境可以研究蝉的习性。一到七月初，蝉就占据了我门前的树。我是屋里的主人，它却是门外的统治者。有了它的统治，无论怎样总是不很安静的。",
        "开篇交代研究蝉的有利环境，以“门外的统治者”的幽默说法，引出说明对象——蝉。",
        "说明对象：蝉。说明语言：“统治者”用拟人手法，语言幽默生动，体现了《昆虫记》科学与文学结合的特点。",
        [
            ("习性", "长期在某种自然条件或社会环境下养成的特性"),
            ("占据", "用强力取得或保持"),
            ("统治者", "行使统治权力的人，文中指蝉在门外树上的主导地位"),
        ],
    ),
    (
        "每年蝉的初次出现是在夏至。在阳光曝晒的道路上有好些小圆孔，孔口与地面相平。蝉的幼虫就从这些圆孔爬出，在地面上变成完全的蝉。蝉喜欢干燥、阳光多的地方。幼虫有一种有力的工具，能够刺透晒干的泥土和沙石。我要考察它们遗弃下的储藏室，必须用刀子来挖掘。",
        "说明蝉初次出现的时间（夏至）、幼虫出土的地点（阳光曝晒的道路上的小圆孔）和习性（喜欢干燥阳光多的地方）。",
        "说明方法：列数字（夏至、小圆孔）、作诠释（解释幼虫如何出土）。说明语言：“初次”“相平”等词准确；“有力的工具”指幼虫的前足，表述留有余地。",
        [
            ("夏至", "二十四节气之一，在6月21日或22日，这一天北半球白天最长"),
            ("曝晒", "在阳光下晒"),
            ("孔口", "洞孔的开口处"),
            ("相平", "一样平、高度相同"),
            ("幼虫", "昆虫的胚胎发育后孵化出来的幼体"),
            ("刺透", "刺穿、穿透"),
            ("考察", "实地观察调查"),
            ("遗弃", "抛弃、丢弃"),
            ("储藏室", "存放东西的房间，文中指蝉的地穴"),
        ],
    ),
    (
        "这小圆孔约一英寸口径，周围一点土都没有。大多数掘地昆虫，例如金蜣，窠外面总有一座土堆。这种区别是由于它们工作方法的不同。金蜣的工作是由洞口开始，所以把掘出来的废料堆积在地面。蝉的幼虫是从地下上来的，最后的工作才是开辟大门口。因为门还未做，所以不可能在门口堆积泥土。",
        "说明蝉的小圆孔的特点（周围无土），并通过与金蜣的比较解释原因——工作方法不同。",
        "说明方法：列数字（一英寸口径）、作比较（蝉与金蜣的比较）、举例子（金蜣）、作诠释（解释周围无土的原因）。说明语言：“约”“大多数”“总有”等词准确严密。",
        [
            ("英寸", "英美制长度单位，1英寸约合2.54厘米"),
            ("口径", "器物圆口的直径"),
            ("金蜣", "（qiāng）一种昆虫，即屎壳郎，以动物粪便为食"),
            ("窠", "（kē）昆虫、鸟兽的巢穴"),
            ("废料", "生产过程中剩下的材料"),
            ("开辟", "打开、创立"),
        ],
    ),
    (
        "蝉的隧道大都是深十五六英寸，下面较宽大，底部却完全关闭起来。做隧道的时候，泥土搬到哪里去了呢？为什么墙壁不会塌下来呢？谁都以为蝉的幼虫用有爪的腿爬上爬下，会将泥土弄塌了，把自己的房子塞住。其实，它干起活来简直像矿工或铁路工程师。矿工用支柱支撑隧道，铁路工程师利用砖墙使地道坚固。蝉同他们一样聪明，在隧道的墙上涂上灰泥。它身子里藏有一种极黏的液体，可以用来做灰泥。地穴常常建筑在含有汁液的植物根须上，是为了从这些根须取得汁液。",
        "说明蝉的隧道的结构和建造方法：深十五六英寸，下面宽大底部关闭；幼虫用体内的黏液做灰泥涂墙，使隧道坚固；地穴建在植物根须上以获取汁液。",
        "说明方法：列数字（十五六英寸）、打比方（像矿工或铁路工程师）、作比较（与矿工、铁路工程师比较）、作诠释（解释墙壁不塌的原因）。说明语言：设问句引起读者注意；“简直像”“极黏”等词生动准确。",
        [
            ("隧道", "在山中或地下凿成的通道"),
            ("宽大", "面积或容积大"),
            ("塌", "倒下、陷下"),
            ("有爪的腿", "带爪子的腿"),
            ("塞住", "堵住、填满"),
            ("矿工", "开采矿物的工人"),
            ("支柱", "支撑的柱子"),
            ("灰泥", "用来涂抹墙壁的泥"),
            ("极黏", "非常有黏性"),
            ("汁液", "含有某种物质的液体"),
            ("根须", "植物的细根"),
        ],
    ),
    (
        "能够很随便地在穴道内爬上爬下，对于它是很重要的，因为当它爬出去到日光下的时候，它必须知道外面的气候如何。所以它要工作好几个星期，甚至一个月，才做成一道坚固的墙壁，使它上下爬行都没有阻碍。它常常在隧道的顶端留一个手指厚的一层土，用来抵御外面的恶劣气候，直到最后一刹那。只要有一些好天气的消息，它就爬上来，利用顶上的薄盖考察气候的情况。",
        "说明蝉的幼虫在隧道内爬上爬下的重要性，以及它如何用坚固的墙壁和顶端的薄土层来适应气候、选择出土时机。",
        "说明方法：列数字（好几个星期、一个月、手指厚）、作诠释（解释为什么要能爬上爬下）。说明语言：“必须”“常常”“只要……就……”等词准确说明蝉的行为逻辑；“最后一刹那”生动写出出土前的紧张时刻。",
        [
            ("随便", "不受拘束、不受限制"),
            ("气候", "一定地区里经过多年观察所得到的概括性的气象情况"),
            ("阻碍", "使不能顺利通过或发展"),
            ("抵御", "抵抗、防御"),
            ("恶劣", "很坏、非常差"),
            ("一刹那", "极短的时间"),
            ("薄盖", "薄薄的一层覆盖物"),
        ],
    ),
    (
        "如果它估计到外面有雨或风暴，它就谨慎地溜到隧道底下。如果气候看来很温暖，它就用爪击碎天花板，爬到地面上来。",
        "说明蝉的幼虫如何根据气候决定是否出土：有雨或风暴就退回，温暖就击碎顶层出土。",
        "说明方法：分类别（分两种情况说明）。说明语言：“估计”“谨慎”“击碎”等词生动准确，用拟人手法写蝉的行为，体现了说明文语言的生动性。",
        [
            ("估计", "根据某些情况，对事物的性质、数量、变化等做大概的推断"),
            ("风暴", "刮大风而且往往同时有大雨的天气现象"),
            ("谨慎", "对外界事物或自己的言行密切注意，以免发生不利或不幸的事情"),
            ("击碎", "敲碎、打碎"),
        ],
    ),
    (
        "普通的蝉喜欢在干的细枝上产卵。它选择最小的枝，像枯草或铅笔那样粗细，而且往往是向上翘起，差不多已经枯死的小枝。它找到适当的细树枝，就用胸部的尖利工具刺成一排小孔。这些小孔的形成，好像用针斜刺下去，把纤维撕裂，并微微挑起。如果它不受干扰，一根枯枝上常常刺出三四十个孔。卵就产在这些孔里。小孔成为狭窄的小径，一个个斜下去，每个小孔内通常约有十个卵。所以一个蝉在一根枯枝上产卵的总数，大约有三四百个。",
        "说明蝉产卵的地点（干的细枝）、方式（用胸部工具刺孔）和数量（一根枝上约三四百个卵）。",
        "说明方法：打比方（像枯草或铅笔那样粗细、好像用针斜刺）、列数字（三四十个孔、十个卵、三四百个）。说明语言：“普通”“往往”“差不多”“通常”“大约”等词准确严密，体现说明文语言的准确性。",
        [
            ("产卵", "鸟类、昆虫等生产卵"),
            ("枯草", "干枯的草"),
            ("翘起", "一头向上仰起"),
            ("枯死", "干枯而死"),
            ("胸部", "躯干的一部分，在颈和腹之间"),
            ("尖利", "尖锐、锋利"),
            ("纤维", "天然的或人工合成的细丝状物质"),
            ("撕裂", "撕开、扯裂"),
            ("微微", "稍微、表示数量不多或程度不深"),
            ("干扰", "扰乱、打扰"),
            ("狭窄", "宽度小"),
            ("小径", "小路"),
        ],
    ),
    (
        "这是一个蝉的卵的故事。我从放大镜里见过蝉卵的孵化。开始很像极小的鱼，眼睛大而黑，身体下面有一种鳍状物，由两个前腿连结而成。这种鳍状物有些运动力，能够帮助幼虫走出壳外，并且帮助它走出有纤维的树枝——这是比较困难的事情。",
        "说明蝉卵孵化后的形态：像极小的鱼，有鳍状物帮助幼虫走出壳外和树枝。",
        "说明方法：打比方（很像极小的鱼）、作诠释（解释鳍状物的作用）。说明语言：“这是一个蝉的卵的故事”用文学化的语言过渡，体现《昆虫记》的文学性；“比较困难”准确说明幼虫出壳的难度。",
        [
            ("放大镜", "用来观察微小物体的光学仪器"),
            ("孵化", "昆虫的卵在一定条件下发育成幼虫"),
            ("鳍状物", "（qí）像鱼鳍一样的东西"),
            ("连结", "连接、结合在一起"),
            ("运动力", "运动的能力"),
        ],
    ),
    (
        "鱼形幼虫一到孔外，皮即刻脱去。但脱下的皮自动形成一种线，幼虫靠它能够附着在树枝上。幼虫落地之前，在这里行日光浴，踢踢腿，试试筋力，有时却又懒洋洋地在绳端摇摆着。",
        "说明鱼形幼虫出壳后的行为：脱皮形成线附着在树枝上，在落地前进行日光浴和活动。",
        "说明方法：摹状貌（踢踢腿、试试筋力、懒洋洋地摇摆）。说明语言：“即刻”“自动”等词准确；“日光浴”“踢踢腿”“懒洋洋”等拟人化描写生动有趣，体现了科学小品文的特点。",
        [
            ("即刻", "立刻、马上"),
            ("附着", "较小的物体沾在较大的物体上"),
            ("日光浴", "让日光照射身体，文中指幼虫在阳光下活动"),
            ("筋力", "体力、力气"),
            ("懒洋洋", "没精打采的样子"),
            ("绳端", "绳子的末端"),
        ],
    ),
    (
        "它的触须现在自由了，左右挥动；腿可以伸缩；前面的爪能够张合自如。身体悬挂着，只要有一点微风就动摇不定。它在这里为将来的出世做准备。我看到的昆虫再没有比这个更奇妙的了。",
        "说明幼虫在树枝上的活动：触须挥动、腿伸缩、爪张合，身体悬挂着为出世做准备。",
        "说明方法：摹状貌（触须挥动、腿伸缩、爪张合）。说明语言：“张合自如”“动摇不定”等词准确生动；“再没有比这个更奇妙的了”直接表达赞叹，体现作者对昆虫的热爱。",
        [
            ("触须", "昆虫头上的须，有触觉和嗅觉作用"),
            ("伸缩", "伸出和缩入"),
            ("张合自如", "张开和闭合都很灵活"),
            ("悬挂", "借助于绳子、钩子等使物体附着于高处"),
            ("动摇不定", "摇摆不停，不稳定"),
            ("奇妙", "稀奇巧妙"),
        ],
    ),
    (
        "不久，它落到地上来了。这危险的一刻到了。面前的危险是多种多样的。只要有一点风，它就被吹到坚硬的岩石上、车辙的污水中、不毛的黄沙里、或是那软得根本无法钻下去的黏土上。",
        "说明幼虫落地后面临的多种危险：被风吹到岩石、污水、黄沙、黏土等不利于生存的地方。",
        "说明方法：分类别（列举四种危险）、举例子（岩石、污水、黄沙、黏土）。说明语言：“危险的一刻”“多种多样”等词渲染紧张气氛；排比列举危险，增强感染力。",
        [
            ("多种多样", "各种各样、品类多"),
            ("车辙", "车辆经过后车轮压在道路上凹下去的痕迹"),
            ("污水", "不清洁的水"),
            ("不毛", "（土地）不长庄稼，形容荒凉"),
            ("黏土", "含沙粒很少、有黏性的土壤"),
        ],
    ),
    (
        "它的身体逐渐变重，因为它体内充满了一种液体。它必须立刻到地下寻觅藏身的地方，否则就有死去的危险。寒冷的冬天就要来了，迟缓就有死亡的危险。它不得不各处寻找软土。没有疑问，许多是在没有找到以前就死去了。",
        "说明幼虫落地后必须立刻钻入地下的原因：身体变重、冬天将至，许多幼虫在找到软土前就死去了。",
        "说明方法：作诠释（解释为什么必须立刻钻入地下）。说明语言：“必须”“否则”“不得不”等词强调紧迫性；“没有疑问”准确说明死亡率之高，体现了对生命的悲悯。",
        [
            ("逐渐", "渐渐、逐步"),
            ("寻觅", "寻找"),
            ("藏身", "躲藏、安身"),
            ("迟缓", "缓慢、不迅速"),
            ("软土", "松软的泥土"),
        ],
    ),
    (
        "最后，它找到适当的地点，用前足的钩扒掘地面。我从放大镜里见它挥动锄头，将泥土掘出抛在地面。几分钟以后，一个土穴就挖成了。这小生物钻下去，隐藏了自己，此后就不再出现了。",
        "说明幼虫找到地点后挖掘土穴、钻入地下的过程，从此开始地下生活。",
        "说明方法：摹状貌（挥动锄头、掘出抛在地面）、列数字（几分钟）。说明语言：“锄头”比喻前足的钩，生动形象；“此后就不再出现了”以简洁的语言收束，暗示漫长的地下生活的开始。",
        [
            ("扒掘", "刨挖"),
            ("锄头", "松土和除草的农具，文中比喻幼虫的前足"),
            ("土穴", "土洞"),
            ("隐藏", "藏起来不让发现"),
        ],
    ),
    (
        "未长成的蝉的地下生活，至今还是个秘密。不过在它来到地面以前，地下生活所经过的时间我们是知道的，大概是四年。以后，在阳光中的生活只有五个星期。",
        "说明蝉的生命周期：地下生活约四年，地上生活只有五个星期。",
        "说明方法：列数字（四年、五个星期）、作比较（地下四年与地上五星期对比）。说明语言：“至今还是个秘密”“大概”“只有”等词准确而有分寸；数字对比突出了蝉生命的反差。",
        [
            ("未长成", "还没有发育成熟"),
            ("秘密", "有所隐蔽、不让人知道的事情"),
            ("大概", "大致、大约"),
        ],
    ),
    (
        "四年黑暗中的苦工，一个月阳光下的享乐，这就是蝉的生活。我们不应当讨厌它那喧嚣的歌声，因为它是在歌颂它的快乐，难得如此短暂的生命里的快乐。",
        "总结全文：蝉的一生是四年地下苦工换一个月阳光下的享乐，因此不应讨厌它的歌声，那是它对短暂生命的歌颂。",
        "说明方法：作比较（四年苦工与一个月享乐）。说明语言：“苦工”“享乐”对比鲜明，“喧嚣”准确写出蝉声的特点；结尾以议论抒情收束，表达对蝉的理解和赞美，体现了科学小品文的人文关怀。",
        [
            ("苦工", "艰苦的劳动"),
            ("享乐", "享受安乐"),
            ("喧嚣", "（xuān xiāo）声音杂乱、不清静"),
            ("歌颂", "用诗歌颂扬，泛指用言语文字等赞美"),
            ("短暂", "时间短"),
        ],
    ),
]

parts = [
    ("第一部分", "蝉的地穴", "1–6 段", "说明蝉的幼虫如何建造地穴、适应气候、选择时机出土，展现了蝉的生存智慧。"),
    ("第二部分", "蝉的卵", "7–15 段", "说明蝉如何产卵、卵如何孵化、幼虫如何落地入土，以及蝉的生命周期。"),
]

para_part = [0,0,0,0,0,0, 1,1,1,1,1,1,1,1,1]

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
    {"w":"曝","py":"pù","q":"在阳光□晒的道路上有好些小圆孔","tip":"「曝」日字旁，晒；多音字，此处读pù不读bào"},
    {"w":"蜣","py":"qiāng","q":"大多数掘地昆虫，例如金□","tip":"「蜣」虫字旁，昆虫名；生僻字，注意右边是「羌」"},
    {"w":"窠","py":"kē","q":"□外面总有一座土堆","tip":"「窠」穴宝盖，巢穴；与「巢」（巛字头）区分"},
    {"w":"黏","py":"nián","q":"它身子里藏有一种极□的液体","tip":"「黏」黍字旁，有黏性；不要写成「粘」（米字旁，读zhān）"},
    {"w":"刹","py":"chà","q":"直到最后一□那","tip":"「刹」立刀旁，极短时间；多音字，此处读chà不读shā"},
    {"w":"翘","py":"qiào","q":"而且往往是向上□起","tip":"「翘」羽字旁，一头向上仰起；多音字，此处读qiào不读qiáo"},
    {"w":"纤","py":"xiān","q":"把□维撕裂，并微微挑起","tip":"「纤」绞丝旁，细丝；多音字，此处读xiān不读qiàn"},
    {"w":"鳍","py":"qí","q":"身体下面有一种□状物","tip":"「鳍」鱼字旁，鱼类的运动器官；生僻字"},
    {"w":"懒","py":"lǎn","q":"有时却又□洋洋地在绳端摇摆着","tip":"「懒」竖心旁，懒惰；不要写成「赖」（贝字旁）"},
    {"w":"辙","py":"zhé","q":"车□的污水中","tip":"「辙」车字旁，车轮压的痕迹；不要写成「撤」（提手旁）"},
    {"w":"黏","py":"nián","q":"或是那软得根本无法钻下去的□土","tip":"此处应为「黏」但题中是「黏土」，注意「黏」与「粘」的区分"},
    {"w":"掘","py":"jué","q":"用前足的钩扒□地面","tip":"「掘」提手旁，挖；不要写成「崛」（山字旁）"},
    {"w":"喧","py":"xuān","q":"我们不应当讨厌它那□嚣的歌声","tip":"「喧」口字旁，声音大；不要写成「暄」（日字旁）"},
    {"w":"嚣","py":"xiāo","q":"我们不应当讨厌它那喧□的歌声","tip":"「嚣」页字旁，吵闹；笔画多，注意中间是「页」"},
]

# Fix the duplicate 黏 entry - the second one should be 黏 but for 黏土, the answer is 黏
# Actually 黏土 is often written 粘土 in simplified Chinese. Let me use a different word.
dict_words = [
    {"w":"曝","py":"pù","q":"在阳光□晒的道路上有好些小圆孔","tip":"「曝」日字旁，晒；多音字，此处读pù不读bào"},
    {"w":"蜣","py":"qiāng","q":"大多数掘地昆虫，例如金□","tip":"「蜣」虫字旁，昆虫名；生僻字，注意右边是「羌」"},
    {"w":"窠","py":"kē","q":"□外面总有一座土堆","tip":"「窠」穴宝盖，巢穴；与「巢」（巛字头）区分"},
    {"w":"黏","py":"nián","q":"它身子里藏有一种极□的液体","tip":"「黏」黍字旁，有黏性；不要写成「粘」（米字旁，读zhān）"},
    {"w":"刹","py":"chà","q":"直到最后一□那","tip":"「刹」立刀旁，极短时间；多音字，此处读chà不读shā"},
    {"w":"翘","py":"qiào","q":"而且往往是向上□起","tip":"「翘」羽字旁，一头向上仰起；多音字，此处读qiào不读qiáo"},
    {"w":"纤","py":"xiān","q":"把□维撕裂，并微微挑起","tip":"「纤」绞丝旁，细丝；多音字，此处读xiān不读qiàn"},
    {"w":"鳍","py":"qí","q":"身体下面有一种□状物","tip":"「鳍」鱼字旁，鱼类的运动器官；生僻字"},
    {"w":"懒","py":"lǎn","q":"有时却又□洋洋地在绳端摇摆着","tip":"「懒」竖心旁，懒惰；不要写成「赖」（贝字旁）"},
    {"w":"辙","py":"zhé","q":"车□的污水中","tip":"「辙」车字旁，车轮压的痕迹；不要写成「撤」（提手旁）"},
    {"w":"掘","py":"jué","q":"用前足的钩扒□地面","tip":"「掘」提手旁，挖；不要写成「崛」（山字旁）"},
    {"w":"喧","py":"xuān","q":"我们不应当讨厌它那□嚣的歌声","tip":"「喧」口字旁，声音大；不要写成「暄」（日字旁）"},
    {"w":"嚣","py":"xiāo","q":"我们不应当讨厌它那喧□的歌声","tip":"「嚣」页字旁，吵闹；笔画多，注意中间是「页」"},
]

dict_notes = [
    {"w":"习性","a":"长期养成的特性","q":"研究蝉的习性"},
    {"w":"夏至","a":"二十四节气之一，6月21或22日","q":"每年蝉的初次出现是在夏至"},
    {"w":"金蜣","a":"一种昆虫，即屎壳郎","q":"例如金蜣"},
    {"w":"窠","a":"昆虫、鸟兽的巢穴","q":"窠外面总有一座土堆"},
    {"w":"隧道","a":"在地下凿成的通道","q":"蝉的隧道大都是深十五六英寸"},
    {"w":"灰泥","a":"用来涂抹墙壁的泥","q":"在隧道的墙上涂上灰泥"},
    {"w":"抵御","a":"抵抗、防御","q":"用来抵御外面的恶劣气候"},
    {"w":"一刹那","a":"极短的时间","q":"直到最后一刹那"},
    {"w":"纤维","a":"细丝状物质","q":"把纤维撕裂"},
    {"w":"孵化","a":"卵发育成幼虫","q":"见过蝉卵的孵化"},
    {"w":"鳍状物","a":"像鱼鳍一样的东西","q":"身体下面有一种鳍状物"},
    {"w":"懒洋洋","a":"没精打采的样子","q":"懒洋洋地在绳端摇摆着"},
    {"w":"张合自如","a":"张开和闭合都很灵活","q":"前面的爪能够张合自如"},
    {"w":"车辙","a":"车轮压在道路上的痕迹","q":"车辙的污水中"},
    {"w":"不毛","a":"（土地）不长庄稼，形容荒凉","q":"不毛的黄沙里"},
    {"w":"寻觅","a":"寻找","q":"到地下寻觅藏身的地方"},
    {"w":"喧嚣","a":"声音杂乱、不清静","q":"它那喧嚣的歌声"},
    {"w":"举例子","a":"说明方法之一，举出实际事例","q":"例如金蜣"},
    {"w":"作比较","a":"说明方法之一，通过对比突出特点","q":"地下生活约四年，地上只有五个星期"},
    {"w":"列数字","a":"说明方法之一，用具体数字说明","q":"深十五六英寸"},
    {"w":"打比方","a":"说明方法之一，通过比喻介绍事物","q":"简直像矿工或铁路工程师"},
    {"w":"摹状貌","a":"说明方法之一，对事物形态进行描写","q":"踢踢腿，试试筋力"},
    {"w":"科学小品文","a":"用文学笔调介绍科学知识的说明文","q":"《蝉》是科学小品文的典范"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《蝉》法布尔</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">法国 · 法布尔</div>
  <h1 class="hero-title">蝉</h1>
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
    <p>《蝉》是法国昆虫学家法布尔的一篇科学小品文，选自《昆虫记》。文章用生动活泼的文笔，介绍了蝉的地穴建造和卵的孵化过程，展现了蝉从卵到幼虫、从地下到地上的完整生命周期，表达了作者对昆虫世界的热爱和对生命的尊重。</p>
    <p>本文是科学小品文的典范：既有说明文的准确严谨，又有散文的生动优美。作者以第一人称的观察视角，将科学知识融入文学描写之中，语言幽默风趣，充满人文关怀。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>法布尔（1823—1915），法国昆虫学家、文学家，被称为“昆虫世界的荷马”。出身于农民家庭，自幼热爱自然，靠自学获得数学和自然科学学士学位。他用毕生精力观察研究昆虫，写下了十卷本巨著《昆虫记》（又译《昆虫的故事》），详细记录了各种昆虫的生活习性。</p>
    <p style="margin-top:10px;color:var(--ink2)">《昆虫记》不仅是一部科学著作，也是一部文学经典。法布尔用拟人化的手法描写昆虫，语言生动幽默，充满对生命的关爱和尊重。1910年，他因此书获得诺贝尔文学奖提名。</p>
  </div>
  <div class="box">
    <h3>《昆虫记》简介</h3>
    <p>《昆虫记》是法布尔以毕生精力撰写的昆虫学巨著，共十卷，约二百余万字。书中详细介绍了多种昆虫的生活习性、繁殖方式、生存智慧等，被誉为“昆虫的史诗”。</p>
    <p style="margin-top:8px">与一般的科普作品不同，《昆虫记》将科学知识与文学描写完美结合，用散文的笔调介绍昆虫，语言生动优美，充满人文关怀。鲁迅曾评价《昆虫记》是“讲昆虫故事”“讲昆虫生活”的楷模。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文朗读《蝉》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1MD4y1D7N5&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读蝉"></iframe>
        <a href="https://www.bilibili.com/video/BV1MD4y1D7N5" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>《昆虫记》科普动画</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1iNxezMEoS&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="昆虫记科普动画"></iframe>
        <a href="https://www.bilibili.com/video/BV1iNxezMEoS" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 说明方法 · 语言</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{fulltext_html}  </div>
  <div class="verse-list" id="verseList">
{verse_html}  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">说明对象 · 方法 · 顺序 · 语言</span></div>

  <div class="box">
    <h3>说明对象与特征</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">说明对象：蝉的生活习性</div>
        <p>本文的说明对象是蝉，具体介绍了蝉的地穴建造和卵的孵化两个方面。文章从蝉的幼虫出土写起，到地穴结构、出土时机、产卵方式、卵的孵化、幼虫入土，最后总结蝉的生命周期，完整展现了蝉的一生。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">核心特征：四年苦工换一月享乐</div>
        <p>文章结尾点明蝉的生命特征：“四年黑暗中的苦工，一个月阳光下的享乐”。地下生活约四年，地上生活只有五个星期，这种巨大的反差是全文最震撼的发现，也引发了作者对生命的深刻思考。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">作比较与列数字：准确而有说服力</div>
        <p>作比较：蝉与金蜣的工作方法比较，地下四年与地上五星期的比较；列数字：“一英寸口径”“十五六英寸”“三四十个孔”“三四百个卵”“四年”“五个星期”。数字精确，比较鲜明，使说明更有说服力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">打比方与摹状貌：生动而形象</div>
        <p>打比方：“它干起活来简直像矿工或铁路工程师”“像枯草或铅笔那样粗细”“好像用针斜刺下去”；摹状貌：“踢踢腿，试试筋力，有时却又懒洋洋地在绳端摇摆着”“触须左右挥动，腿可以伸缩”。打比方和摹状貌使说明生动形象，如在目前。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">举例子与作诠释：具体而清晰</div>
        <p>举例子：以金蜣为例说明掘地昆虫的一般特点；作诠释：解释蝉的地穴周围为什么没有土、墙壁为什么不会塌、幼虫为什么要能爬上爬下等。举例子和作诠释使说明内容具体清晰，易于理解。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明顺序</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">整体：逻辑顺序（从地穴到卵）</div>
        <p>文章分为两大部分：第一部分写蝉的地穴（幼虫如何建造地穴、选择时机出土），第二部分写蝉的卵（如何产卵、卵如何孵化、幼虫如何入土）。从地穴到卵，从幼虫到成虫再到卵，按照蝉的生命过程安排说明顺序，逻辑清晰。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">局部：时间顺序与观察顺序</div>
        <p>写地穴时，按照从外到内的观察顺序（小圆孔→隧道→内部结构）；写卵的孵化时，按照时间顺序（卵→鱼形幼虫→脱皮→落地→入土）。多种说明顺序综合运用，使文章条理清晰。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明语言的特点</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">准确严谨：科学的态度</div>
        <p>“约一英寸”“大约有三四百个”“大概是四年”“至今还是个秘密”——“约”“大约”“大概”等修饰词，以及对未知领域的坦诚，体现了科学的严谨态度。数字精确，表述留有余地，是说明文语言准确性的典范。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">生动幽默：文学的笔法</div>
        <p>“门外的统治者”“日光浴”“踢踢腿，试试筋力”“懒洋洋地在绳端摇摆着”——拟人化的描写使昆虫形象生动可爱；“简直像矿工或铁路工程师”的比喻幽默风趣。科学与文学的完美结合，正是《昆虫记》的独特魅力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">人文关怀：生命的尊重</div>
        <p>“许多是在没有找到以前就死去了”“我们不应当讨厌它那喧嚣的歌声，因为它是在歌颂它的快乐”——作者对昆虫的生命充满悲悯和尊重，不是冷冰冰的科学观察，而是带着温度的生命礼赞。这种人文关怀使文章超越了一般的科普作品。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《蝉》通过介绍蝉的地穴建造和卵的孵化过程，展现了蝉从卵到成虫的完整生命周期，揭示了“四年黑暗中的苦工，一个月阳光下的享乐”这一生命特征，表达了作者对昆虫世界的热爱、对生命的尊重和赞美。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 说明术语 · 用字 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">曝晒</span><span class="acc-d">（pù）在阳光下晒。</span></div>
      <div class="acc-item"><span class="acc-w">金蜣</span><span class="acc-d">（qiāng）一种昆虫，即屎壳郎。</span></div>
      <div class="acc-item"><span class="acc-w">窠</span><span class="acc-d">（kē）昆虫、鸟兽的巢穴。</span></div>
      <div class="acc-item"><span class="acc-w">隧道</span><span class="acc-d">在地下凿成的通道。</span></div>
      <div class="acc-item"><span class="acc-w">抵御</span><span class="acc-d">抵抗、防御。</span></div>
      <div class="acc-item"><span class="acc-w">一刹那</span><span class="acc-d">（chà）极短的时间。</span></div>
      <div class="acc-item"><span class="acc-w">纤维</span><span class="acc-d">（xiān）细丝状物质。</span></div>
      <div class="acc-item"><span class="acc-w">孵化</span><span class="acc-d">卵在一定条件下发育成幼虫。</span></div>
      <div class="acc-item"><span class="acc-w">鳍状物</span><span class="acc-d">（qí）像鱼鳍一样的东西。</span></div>
      <div class="acc-item"><span class="acc-w">张合自如</span><span class="acc-d">张开和闭合都很灵活。</span></div>
      <div class="acc-item"><span class="acc-w">车辙</span><span class="acc-d">（zhé）车轮压在道路上的痕迹。</span></div>
      <div class="acc-item"><span class="acc-w">不毛</span><span class="acc-d">（土地）不长庄稼，形容荒凉。</span></div>
      <div class="acc-item"><span class="acc-w">寻觅</span><span class="acc-d">寻找。</span></div>
      <div class="acc-item"><span class="acc-w">喧嚣</span><span class="acc-d">（xuān xiāo）声音杂乱、不清静。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>说明文术语</h3>
      <div class="acc-item"><span class="acc-w">科学小品文</span><span class="acc-d">用文学笔调介绍科学知识的说明文，兼具科学性和文学性。本文是科学小品文的典范。</span></div>
      <div class="acc-item"><span class="acc-w">说明对象</span><span class="acc-d">文章要说明的事物。本文的说明对象是蝉的生活习性。</span></div>
      <div class="acc-item"><span class="acc-w">作比较</span><span class="acc-d">说明方法之一，通过对比突出事物特征。如蝉与金蜣比较、地下四年与地上五星期比较。</span></div>
      <div class="acc-item"><span class="acc-w">列数字</span><span class="acc-d">说明方法之一，用具体数字说明。如“四年”“五个星期”。</span></div>
      <div class="acc-item"><span class="acc-w">打比方</span><span class="acc-d">说明方法之一，通过比喻介绍事物。如“像矿工或铁路工程师”。</span></div>
      <div class="acc-item"><span class="acc-w">举例子</span><span class="acc-d">说明方法之一，举出实际事例。如以金蜣为例。</span></div>
      <div class="acc-item"><span class="acc-w">作诠释</span><span class="acc-d">说明方法之一，解释事物的原因或原理。如解释地穴周围无土的原因。</span></div>
      <div class="acc-item"><span class="acc-w">摹状貌</span><span class="acc-d">说明方法之一，对事物的形态进行描写。如幼虫“踢踢腿，试试筋力”。</span></div>
      <div class="acc-item"><span class="acc-w">逻辑顺序</span><span class="acc-d">按照事物的内在逻辑关系安排说明顺序。本文从地穴到卵，按生命过程说明。</span></div>
      <div class="acc-item"><span class="acc-w">时间顺序</span><span class="acc-d">按照时间先后安排说明顺序。写卵的孵化时用时间顺序。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">曝晒</span><span class="acc-d">（pù）日字旁；多音字，此处读pù，不读bào。</span></div>
      <div class="acc-item"><span class="acc-w">金蜣</span><span class="acc-d">（qiāng）虫字旁；生僻字。</span></div>
      <div class="acc-item"><span class="acc-w">窠</span><span class="acc-d">（kē）穴宝盖；与「巢」（巛字头）区分。</span></div>
      <div class="acc-item"><span class="acc-w">极黏</span><span class="acc-d">（nián）黍字旁；与「粘」（zhān，米字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">一刹那</span><span class="acc-d">（chà）立刀旁；多音字，此处读chà，不读shā。</span></div>
      <div class="acc-item"><span class="acc-w">纤维</span><span class="acc-d">（xiān）绞丝旁；多音字，此处读xiān，不读qiàn。</span></div>
      <div class="acc-item"><span class="acc-w">鳍状物</span><span class="acc-d">（qí）鱼字旁；生僻字。</span></div>
      <div class="acc-item"><span class="acc-w">车辙</span><span class="acc-d">（zhé）车字旁；与「撤」（提手旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">喧嚣</span><span class="acc-d">（xuān xiāo）「喧」口字旁，「嚣」页字旁；注意「嚣」的笔画。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">科学与文学结合</span><span class="acc-d">既有准确的科学知识，又有生动的文学描写，是科学小品文的典范。</span></div>
      <div class="acc-item"><span class="acc-w">第一人称观察</span><span class="acc-d">以“我”的观察视角展开，亲切自然，增强了文章的真实性和可读性。</span></div>
      <div class="acc-item"><span class="acc-w">拟人化描写</span><span class="acc-d">用拟人手法描写昆虫，如“统治者”“日光浴”“懒洋洋”，使昆虫形象生动可爱。</span></div>
      <div class="acc-item"><span class="acc-w">人文关怀</span><span class="acc-d">在科学说明中融入对生命的悲悯和尊重，使文章具有温度和深度。</span></div>
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
  <div class="kai">《蝉》</div>
  <div>法布尔 · 法国 · 出自《昆虫记》</div>
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
