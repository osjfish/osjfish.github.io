# -*- coding: utf-8 -*-
"""生成《中国石拱桥》茅以升 课件（说明文）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\zhongguoshigongqiao-maoyisheng.html"
FS_KEY = "shigongqiao_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

paragraphs = [
    (
        "石拱桥的桥洞成弧形，就像虹。古代神话里说，雨后彩虹是“人间天上的桥”，通过彩虹就能上天。我国的诗人爱把拱桥比作虹，说拱桥是“卧虹”“飞虹”，把水上拱桥形容为“长虹卧波”。",
        "以打比方开篇，将石拱桥的桥洞比作虹，引用神话和诗人的说法，说明石拱桥形式优美的特点。",
        "说明对象：石拱桥。说明方法：打比方（桥洞成弧形，就像虹）、引用（古代神话、诗人说法）。说明语言：“就像虹”形象生动，引出说明对象。",
        [
            ("弧形", "圆周的一部分的形状，即弯曲如弓的形状"),
            ("虹", "雨后天空中出现的彩色圆弧"),
            ("卧虹", "横卧的彩虹，形容拱桥如彩虹横卧水面"),
            ("飞虹", "飞架的彩虹，形容拱桥如虹飞跨两岸"),
            ("长虹卧波", "长长的彩虹横卧在水波上，形容水上拱桥的优美姿态"),
        ],
    ),
    (
        "石拱桥在世界桥梁史上出现得比较早。这种桥不但形式优美，而且结构坚固，能几十年几百年甚至上千年雄跨在江河之上，在交通方面发挥作用。",
        "总说石拱桥的两个特点：形式优美、结构坚固，以及在世界桥梁史上的地位和作用。",
        "说明方法：作比较（与其他桥梁比较出现时间）、列数字（几十年几百年甚至上千年）。说明语言：“比较早”“不但……而且……”准确概括石拱桥的特点，“雄跨”一词写出石拱桥的气势和坚固。",
        [
            ("桥梁史", "桥梁发展的历史"),
            ("形式优美", "外形好看、美观"),
            ("结构坚固", "构造结实、牢固"),
            ("雄跨", "气势雄伟地跨越"),
            ("交通", "各种运输和邮电事业的总称，文中指渡河运输"),
        ],
    ),
    (
        "我国的石拱桥有悠久的历史。《水经注》里提到的“旅人桥”，大约建成于公元282年，可能是有记载的最早的石拱桥了。我国的石拱桥几乎到处都有。这些桥大小不一，形式多样，有许多是惊人的杰作。其中最著名的当推河北省赵县的赵州桥，还有北京丰台区的卢沟桥。",
        "说明我国石拱桥历史悠久、分布广泛、形式多样，并以赵州桥和卢沟桥为例引出下文。",
        "说明方法：举例子（旅人桥、赵州桥、卢沟桥）、列数字（公元282年）、引用（《水经注》）。说明语言：“大约”“可能”“几乎”等修饰词体现了说明文语言的准确性；“当推”表示推测，留有余地。",
        [
            ("悠久", "年代久远"),
            ("《水经注》", "北魏郦道元所著的古代地理名著"),
            ("旅人桥", "古代石拱桥名，相传建于西晋"),
            ("记载", "用文字记录下来"),
            ("杰作", "超出一般水平的优秀作品"),
            ("当推", "应当推选、算是"),
        ],
    ),
    (
        "赵州桥横跨在洨河上，是世界著名的古代石拱桥，也是造成后一直使用到现在的最古的石桥。这座桥修建于公元605年左右，到现在已经一千三百多年了，还保持着原来的雄姿。到解放的时候，桥身有些残损了，在人民政府的领导下，经过彻底整修，这座古桥又恢复了青春。",
        "介绍赵州桥的位置、地位、建造时间和历史，以及解放后的整修。",
        "说明方法：列数字（公元605年、一千三百多年）。说明语言：“左右”表示约数，“最古”以“造成后一直使用到现在”限定，表述准确；“恢复了青春”用拟人手法，生动形象。",
        [
            ("横跨", "两脚分跨在物体两边站立支撑着，文中指桥跨越河流"),
            ("洨河", "（xiáo）河名，在河北省赵县"),
            ("雄姿", "威武雄壮的姿态"),
            ("残损", "残缺破损"),
            ("彻底", "一直到底、深入而透彻"),
            ("整修", "整治修理"),
        ],
    ),
    (
        "赵州桥非常雄伟，全长50.82米，两端宽9.6米，中部略窄，宽9米。桥的设计完全合乎科学原理，施工技术更是巧妙绝伦。唐朝的张嘉贞说它“制造奇特，人不知其所以为”。这座桥的特点是：（一）全桥只有一个大拱，长达37.4米，在当时可算是世界上最长的石拱。桥洞不是普通半圆形，而是像一张弓，因而大拱上面的道路没有陡坡，便于车马上下。（二）大拱的两肩上，各有两个小拱。这个创造性的设计，不但节约了石料，减轻了桥身的重量，而且在河水暴涨的时候，还可以增加桥洞的过水量，减轻洪水对桥身的冲击。同时，拱上加拱，桥身也更美观。（三）大拱由28道拱圈拼成，就像这么多同样形状的弓合拢在一起，做成一个弧形的桥洞。每道拱圈都能独立支撑上面的重量，一道坏了，其他各道不致受到影响。（四）全桥结构匀称，和四周景色配合得十分和谐；桥上的石栏石板也雕刻得古朴美观。唐朝的张鷟说，远望这座桥就像“初月出云，长虹饮涧”。赵州桥高度的技术水平和不朽的艺术价值，充分显示了我国劳动人民的智慧和力量。桥的主要设计者李春就是一位杰出的工匠，在桥头的碑文里刻着他的名字。",
        "详细说明赵州桥的四个特点：大拱的设计、拱上加拱的设计、拱圈的构造、结构与雕刻的美观，高度评价其技术水平和艺术价值。",
        "说明方法：列数字（50.82米、9.6米、37.4米、28道）、打比方（像一张弓、像这么多同样形状的弓、初月出云长虹饮涧）、分类别（分四点说明）、引用（张嘉贞、张鷟的话）、作诠释（解释每个特点的原理和好处）。说明顺序：逻辑顺序（从整体到局部，从主到次）。说明语言：“在当时可算是”限定时间和程度，“完全”“更是”强调程度，准确严密。",
        [
            ("雄伟", "雄壮而伟大"),
            ("合乎", "符合、合于"),
            ("科学原理", "科学上的基本规律"),
            ("巧妙绝伦", "灵巧高明，没有能比得上的。伦，同类、同等"),
            ("张嘉贞", "（666—729）唐代大臣，此文引用其《石桥铭序》"),
            ("人不知其所以为", "人们不知道它是怎么建造的，形容建造技术高超"),
            ("陡坡", "很大的坡度"),
            ("暴涨", "（水位）急剧上升"),
            ("过水量", "能够通过的水的流量"),
            ("拱圈", "拱桥中弧形的承重构件"),
            ("合拢", "合到一起、闭合"),
            ("独立支撑", "单独承受重量"),
            ("匀称", "（chèn）均匀、比例和谐"),
            ("和谐", "配合得适当、协调"),
            ("古朴", "朴素而有古代的风格"),
            ("张鷟", "（zhuó）（约660—740）唐代文学家，此文引用其《朝野佥载》"),
            ("初月出云", "初升的月亮从云中出来，形容桥的优美"),
            ("长虹饮涧", "长长的彩虹在山涧饮水，形容桥如长虹横卧"),
            ("不朽", "永不磨灭"),
            ("李春", "隋代工匠，赵州桥的主要设计者"),
            ("碑文", "刻在石碑上的文字"),
        ],
    ),
    (
        "永定河上的卢沟桥，修建于公元1189到1192年间。桥长265米，由11个半圆形的石拱组成，每个石拱长度不一，自16米到21.6米。桥宽约8米，路面平坦，几乎与河面平行。每两个石拱之间有石砌桥墩，把11个石拱联成一个整体。由于各拱相联，所以这种桥叫做联拱石桥。永定河发水时，来势很猛，以前两岸河堤常被冲毁，但是这座桥极少出事，足见它的坚固。桥面用石板铺砌，两旁有石栏石柱。每个柱头上都雕刻着不同姿态的狮子。这些石刻狮子，有的母子相抱，有的交头接耳，有的像倾听水声，有的像注视行人，千态万状，惟妙惟肖。",
        "介绍卢沟桥的建造时间、规模、结构特点（联拱石桥）、坚固程度，以及柱头上石刻狮子的精美。",
        "说明方法：列数字（1189到1192年、265米、11个、16米到21.6米、8米）、作比较（以前两岸河堤常被冲毁，但是这座桥极少出事）、摹状貌（石刻狮子的各种姿态）、下定义（联拱石桥）。说明语言：“约”“几乎”“极少”等词准确严密；“千态万状，惟妙惟肖”写出石刻狮子的精美。",
        [
            ("永定河", "河名，在北京市西南部"),
            ("石砌桥墩", "用石头砌成的桥墩"),
            ("联拱石桥", "由多个石拱相连而成的石桥"),
            ("发水", "发生洪水、涨水"),
            ("来势很猛", "到来的气势很猛烈"),
            ("河堤", "沿河道两岸修筑的挡水建筑物"),
            ("冲毁", "被水冲击毁坏"),
            ("足见", "完全可以看出"),
            ("铺砌", "用砖石等铺盖"),
            ("石柱", "石头柱子"),
            ("柱头", "柱子的顶端"),
            ("交头接耳", "彼此在耳朵边低声说话"),
            ("倾听", "细心地听"),
            ("千态万状", "形容姿态多种多样"),
            ("惟妙惟肖", "（xiào）形容描写或模仿得非常逼真、传神"),
        ],
    ),
    (
        "早在13世纪，卢沟桥就闻名世界。那时候有个意大利人马可·波罗来过中国，他的游记里，十分推崇这座桥，说它“是世界上独一无二的”，并且特别欣赏桥栏柱上刻的狮子，说它们“共同构成美丽的奇观”。在国内，这座桥也是历来为人们所称赞的。它地处入都要道，而且建筑优美，“卢沟晓月”很早就成为北京的胜景之一。",
        "说明卢沟桥的世界声誉和国内影响，以马可·波罗的评价和“卢沟晓月”胜景佐证。",
        "说明方法：举例子（马可·波罗的游记）、引用（“是世界上独一无二的”“共同构成美丽的奇观”）。说明语言：“十分推崇”“特别欣赏”写出评价之高；“之一”说明北京胜景很多，卢沟桥只是其中之一，表述准确。",
        [
            ("闻名世界", "在世界上都很有名"),
            ("马可·波罗", "（1254—1324）意大利旅行家，曾来中国游历，著有《马可·波罗行纪》"),
            ("推崇", "十分推重、崇敬"),
            ("独一无二", "没有相同的，没有可以相比的"),
            ("奇观", "雄伟美丽而又罕见的景象"),
            ("入都要道", "进入都城的重要道路"),
            ("卢沟晓月", "卢沟桥的晓月，为旧时北京八景之一"),
            ("胜景", "优美的风景"),
        ],
    ),
    (
        "为什么我国的石拱桥会有这样光辉的成就呢？首先，在于我国劳动人民的勤劳和智慧。他们制作石料的工艺极其精巧，能把石料切成整块大石碑，又能把石块雕刻成各种形象。在建筑技术上有很多创造，在起重吊装方面更有意想不到的办法。如福建漳州的江东桥，修建于八百年前，有的石梁一块就有二百来吨重，究竟是怎样安装上去的，至今还不完全知道。其次，我国石拱桥的设计施工有优良传统，建成的桥，用料省，结构巧，强度高。再其次，我国富有建筑用的各种石料，便于就地取材，这也为修造石桥提供了有利条件。",
        "分析我国石拱桥取得光辉成就的三个原因：劳动人民的勤劳智慧、设计施工的优良传统、石料资源丰富。",
        "说明方法：分类别（首先、其次、再其次，分三点说明）、举例子（福建漳州江东桥）、列数字（八百年前、二百来吨）。说明顺序：逻辑顺序（由主到次）。说明语言：“极其”“更有”强调程度，“不完全知道”表述留有余地，准确严密。",
        [
            ("光辉", "光明、灿烂，比喻卓越"),
            ("成就", "事业上的成绩"),
            ("勤劳", "努力劳动，不怕辛苦"),
            ("智慧", "辨析判断、发明创造的能力"),
            ("工艺", "将原材料或半成品加工成产品的方法、技术"),
            ("精巧", "精细巧妙"),
            ("石碑", "刻着文字或图画的竖石"),
            ("起重吊装", "用起重设备把重物吊起并安装到位"),
            ("漳州", "地名，在福建省"),
            ("江东桥", "古代石桥名，在福建漳州"),
            ("石梁", "石桥上的石制横梁"),
            ("究竟", "到底、毕竟"),
            ("优良传统", "优秀的、代代相传的做法"),
            ("就地取材", "在本地选取需要的材料"),
        ],
    ),
    (
        "两千年来，我国修建了无数的石拱桥。解放后，全国大规模兴建起各种型式的公路桥与铁路桥，其中就有许多钢筋混凝土拱桥。近几年来，全国造了总长二十余万米的这种拱桥，其中最大的一孔，长达150米。我国桥梁事业的飞跃发展，表明了我国社会主义制度的无比优越。",
        "总结全文，从古代石拱桥写到现代桥梁事业的飞跃发展，歌颂社会主义制度的优越性。",
        "说明方法：列数字（两千年来、二十余万米、150米）、作比较（古代石拱桥与现代钢筋混凝土拱桥）。说明顺序：时间顺序（从古代到解放后到近几年来）。说明语言：“无数”“大规模”“飞跃”等词写出发展之大，“无比优越”点明主旨。",
        [
            ("无数", "数不清、形容极多"),
            ("大规模", "范围大、规模大"),
            ("兴建", "开始建筑、建设"),
            ("型式", "类型、样式"),
            ("钢筋混凝土", "用钢筋加固的混凝土，是现代建筑的重要材料"),
            ("总长", "总长度"),
            ("一孔", "一个桥洞"),
            ("飞跃发展", "形容发展速度极快"),
            ("表明", "表示清楚、说明"),
            ("无比优越", "没有什么能比得上的优胜"),
        ],
    ),
]

parts = [
    ("第一部分", "石拱桥的总体特征", "1–3 段", "从石拱桥的外形、特点和我国石拱桥的历史地位写起，引出赵州桥和卢沟桥两个例子。"),
    ("第二部分", "赵州桥详解", "4–5 段", "介绍赵州桥的位置、历史、规模和四个结构特点，高度评价其技术水平和艺术价值。"),
    ("第三部分", "卢沟桥详解", "6–7 段", "介绍卢沟桥的建造时间、规模、联拱结构、石刻狮子的精美，以及其世界声誉。"),
    ("第四部分", "成就原因与现代发展", "8–9 段", "分析我国石拱桥取得光辉成就的原因，并从古代写到现代桥梁事业的飞跃发展。"),
]

para_part = [0,0,0, 1,1, 2,2, 3,3]

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
    {"w":"弧","py":"hú","q":"石拱桥的桥洞成□形，就像虹","tip":"「弧」弓字旁，圆周的一部分；不要写成「狐」（反犬旁）"},
    {"w":"卧","py":"wò","q":"说拱桥是“□虹”“飞虹”","tip":"「卧」卜字旁，横躺；不要写成「卧」以外的写法"},
    {"w":"悠","py":"yōu","q":"我国的石拱桥有□久的历史","tip":"「悠」心字底，长久；不要写成「忧」（竖心旁）"},
    {"w":"洨","py":"xiáo","q":"赵州桥横跨在□河上","tip":"「洨」三点水，河名；生僻字，注意右边是「交」"},
    {"w":"残","py":"cán","q":"桥身有些□损了","tip":"「残」歹字旁，残缺；不要写成「惨」（竖心旁）"},
    {"w":"伦","py":"lún","q":"施工技术更是巧妙绝□","tip":"「伦」单人旁，同类；不要写成「论」（言字旁）"},
    {"w":"陡","py":"dǒu","q":"大拱上面的道路没有□坡","tip":"「陡」左耳旁，坡度很大；不要写成「徒」（双人旁）"},
    {"w":"涨","py":"zhǎng","q":"在河水暴□的时候","tip":"「涨」三点水，水位升高；多音字，此处读zhǎng不读zhàng"},
    {"w":"拱","py":"gǒng","q":"28道□圈拼成，就像这么多同样形状的弓合拢在一起","tip":"「拱」提手旁，弧形的建筑结构；不要写成「共」"},
    {"w":"称","py":"chèn","q":"全桥结构匀□，和四周景色配合得十分和谐","tip":"「称」禾字旁，适合；多音字，此处读chèn不读chēng"},
    {"w":"鷟","py":"zhuó","q":"唐朝的张□说，远望这座桥就像","tip":"「鷟」鸟字旁，人名用字；生僻字，注意上面是「族」的省略"},
    {"w":"涧","py":"jiàn","q":"初月出云，长虹饮□","tip":"「涧」三点水，山间水沟；不要写成「间」（门字旁）"},
    {"w":"砌","py":"qì","q":"每两个石拱之间有石□桥墩","tip":"「砌」石字旁，用砖石垒筑；不要写成「彻」（双人旁）"},
    {"w":"堤","py":"dī","q":"以前两岸河□常被冲毁","tip":"「堤」土字旁，挡水建筑物；不要写成「提」（提手旁）"},
    {"w":"肖","py":"xiào","q":"千态万状，惟妙惟□","tip":"「肖」月字旁，相似；多音字，此处读xiào不读xiāo；成语「惟妙惟肖」"},
    {"w":"肖","py":"xiào","q":"千态万状，惟妙惟□","tip":"「肖」月字旁，相似；多音字，此处读xiào不读xiāo"},
    {"w":"崇","py":"chóng","q":"他的游记里，十分推□这座桥","tip":"「崇」山字头，尊敬；不要写成「祟」（suì，鬼怪）"},
    {"w":"漳","py":"zhāng","q":"如福建□州的江东桥","tip":"「漳」三点水，地名；不要写成「章」"},
    {"w":"吨","py":"dūn","q":"有的石梁一块就有二百来□重","tip":"「吨」口字旁，重量单位；不要写成「顿」（页字旁）"},
    {"w":"筋","py":"jīn","q":"其中就有许多钢□混凝土拱桥","tip":"「筋」竹字头，肌腱或像筋的东西；不要写成「斤」"},
]

dict_notes = [
    {"w":"弧形","a":"圆周的一部分的形状，即弯曲如弓的形状","q":"石拱桥的桥洞成弧形"},
    {"w":"长虹卧波","a":"长长的彩虹横卧在水波上，形容水上拱桥的优美姿态","q":"把水上拱桥形容为长虹卧波"},
    {"w":"雄跨","a":"气势雄伟地跨越","q":"能几十年几百年甚至上千年雄跨在江河之上"},
    {"w":"悠久","a":"年代久远","q":"我国的石拱桥有悠久的历史"},
    {"w":"杰作","a":"超出一般水平的优秀作品","q":"有许多是惊人的杰作"},
    {"w":"巧妙绝伦","a":"灵巧高明，没有能比得上的","q":"施工技术更是巧妙绝伦"},
    {"w":"暴涨","a":"（水位）急剧上升","q":"在河水暴涨的时候"},
    {"w":"拱圈","a":"拱桥中弧形的承重构件","q":"大拱由28道拱圈拼成"},
    {"w":"匀称","a":"均匀、比例和谐","q":"全桥结构匀称"},
    {"w":"古朴","a":"朴素而有古代的风格","q":"桥上的石栏石板也雕刻得古朴美观"},
    {"w":"联拱石桥","a":"由多个石拱相连而成的石桥","q":"所以这种桥叫做联拱石桥"},
    {"w":"惟妙惟肖","a":"形容描写或模仿得非常逼真、传神","q":"千态万状，惟妙惟肖"},
    {"w":"推崇","a":"十分推重、崇敬","q":"十分推崇这座桥"},
    {"w":"独一无二","a":"没有相同的，没有可以相比的","q":"是世界上独一无二的"},
    {"w":"奇观","a":"雄伟美丽而又罕见的景象","q":"共同构成美丽的奇观"},
    {"w":"就地取材","a":"在本地选取需要的材料","q":"便于就地取材"},
    {"w":"钢筋混凝土","a":"用钢筋加固的混凝土，现代建筑的重要材料","q":"许多钢筋混凝土拱桥"},
    {"w":"飞跃发展","a":"形容发展速度极快","q":"我国桥梁事业的飞跃发展"},
    {"w":"打比方","a":"说明方法之一，通过比喻来介绍事物","q":"石拱桥的桥洞成弧形，就像虹"},
    {"w":"列数字","a":"说明方法之一，用具体数字来说明事物","q":"全长50.82米"},
    {"w":"举例子","a":"说明方法之一，举出实际事例来说明事物","q":"如福建漳州的江东桥"},
    {"w":"作比较","a":"说明方法之一，通过对比来突出事物特点","q":"以前两岸河堤常被冲毁，但是这座桥极少出事"},
    {"w":"摹状貌","a":"说明方法之一，对事物的形状、姿态等进行描写","q":"这些石刻狮子，有的母子相抱"},
    {"w":"下定义","a":"说明方法之一，用简明的语言揭示事物的本质特征","q":"由于各拱相联，所以这种桥叫做联拱石桥"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《中国石拱桥》茅以升</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 茅以升</div>
  <h1 class="hero-title">中国石拱桥</h1>
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
    <p>《中国石拱桥》是桥梁专家茅以升写的一篇事物说明文，选自《人民日报》。文章以赵州桥和卢沟桥为例，介绍了中国石拱桥的特点、历史成就和现代发展，是中学语文教材中说明文的经典篇目。</p>
    <p>文章抓住石拱桥“形式优美、结构坚固”的特征，以赵州桥和卢沟桥为典型例子，综合运用举例子、列数字、打比方、作比较、引用、摹状貌等多种说明方法，语言准确严密而又生动形象，是学习说明文写作的典范。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>茅以升（1896—1989），字唐臣，江苏镇江人，中国著名桥梁专家、教育家，中国科学院院士。1916年毕业于唐山工业专门学校，后赴美留学，获卡内基理工学院博士学位。1933年至1937年，主持设计并建造了钱塘江大桥，这是中国人自己设计和建造的第一座现代化大型桥梁。</p>
    <p style="margin-top:10px;color:var(--ink2)">茅以升毕生致力于桥梁科学研究和工程教育，曾任中国交通大学、北方交通大学校长，中国科协副主席等职。他的科普文章深入浅出，将专业的桥梁知识写得通俗易懂，《中国石拱桥》是其代表作。</p>
  </div>
  <div class="box">
    <h3>文体知识</h3>
    <p><b>说明文：</b>以说明为主要表达方式，用来介绍或解释事物的状态、性质、构造、功能、制作方法、发展过程等的一种文体。说明文的语言要求准确、简明、周密。</p>
    <p style="margin-top:8px"><b>说明方法：</b>常见的有举例子、列数字、打比方、作比较、分类别、下定义、作诠释、摹状貌、引用等。本文综合运用了多种说明方法，是说明文学习的典范。</p>
    <p style="margin-top:8px"><b>说明顺序：</b>常见的有时间顺序、空间顺序、逻辑顺序。本文整体采用逻辑顺序（从一般到个别、从概括到具体），局部也有时间顺序。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文诵读《中国石拱桥》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1ob4y127mb&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读中国石拱桥"></iframe>
        <a href="https://www.bilibili.com/video/BV1ob4y127mb" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>天才简史：茅以升与中国大桥</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV19J411N7uK&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="天才简史茅以升"></iframe>
        <a href="https://www.bilibili.com/video/BV19J411N7uK" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">说明对象：中国石拱桥</div>
        <p>本文的说明对象是中国石拱桥。文章从石拱桥的一般特征写起，然后以赵州桥和卢沟桥为典型例子，具体说明中国石拱桥的特点，最后分析成就原因并介绍现代发展。说明对象明确，特征突出。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">总体特征：形式优美，结构坚固</div>
        <p>文章第二段明确指出石拱桥“不但形式优美，而且结构坚固”，这是全文的说明中心。赵州桥的“初月出云，长虹饮涧”写形式优美，“一千三百多年了，还保持着原来的雄姿”写结构坚固；卢沟桥的“联拱”结构和“极少出事”写坚固，石刻狮子的“千态万状，惟妙惟肖”写优美。两个例子都紧扣特征。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">举例子：赵州桥与卢沟桥</div>
        <p>举例子是本文最主要的说明方法。赵州桥是独拱石桥的代表，卢沟桥是联拱石桥的代表，两个例子各有侧重，互为补充，全面说明了中国石拱桥的特点。例子典型、有代表性，增强了说明的说服力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">列数字：精确而有说服力</div>
        <p>全文使用了大量数字：赵州桥“全长50.82米”“大拱长达37.4米”“28道拱圈”，卢沟桥“桥长265米”“由11个半圆形的石拱组成”“自16米到21.6米”。数字精确具体，使说明更有说服力，体现了说明文的科学性。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">打比方与引用：生动而典雅</div>
        <p>“石拱桥的桥洞成弧形，就像虹”“桥洞不是普通半圆形，而是像一张弓”，打比方使说明生动形象；引用张嘉贞“制造奇特，人不知其所以为”和张鷟“初月出云，长虹饮涧”，既说明了桥的特点，又增添了文章的文化底蕴和文学色彩。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">作比较与摹状貌：突出特征</div>
        <p>“以前两岸河堤常被冲毁，但是这座桥极少出事”，以河堤与卢沟桥作比较，突出卢沟桥的坚固；“这些石刻狮子，有的母子相抱，有的交头接耳……千态万状，惟妙惟肖”，摹状貌生动地写出了石狮的精美，使读者如见其形。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明顺序</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">整体：逻辑顺序（从一般到个别）</div>
        <p>文章先写石拱桥的一般特征（形式优美、结构坚固），再写中国石拱桥的总体情况，然后以赵州桥和卢沟桥为例具体说明，最后分析成就原因和现代发展。这是从一般到个别、从概括到具体的逻辑顺序，条理清晰，层层深入。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">局部：时间顺序与空间顺序</div>
        <p>介绍赵州桥和卢沟桥时，按从整体到局部的空间顺序（先写桥的整体规模，再写结构特点）；分析成就原因时，按由主到次的逻辑顺序（首先、其次、再其次）；结尾从古代写到现代，用时间顺序。多种说明顺序综合运用，使文章结构严谨。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明语言的准确性</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">修饰限制词的运用</div>
        <p>“大约建成于公元282年”“可能是有记载的最早的石拱桥”“几乎到处都有”“在当时可算是世界上最长的石拱”“桥宽约8米”“几乎与河面平行”“极少出事”——“大约”“可能”“几乎”“在当时”“约”“极少”等修饰限制词，准确地反映了客观实际，体现了说明文语言的准确性和严密性。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">准确与生动的统一</div>
        <p>本文语言既准确严密，又生动形象。数字和术语体现了准确性，而打比方、引用、摹状貌等手法又使文章生动有趣。如“长虹卧波”“初月出云，长虹饮涧”等描写，既准确地说明了桥的形态，又富有文学色彩，做到了科学性与文学性的统一。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《中国石拱桥》以赵州桥和卢沟桥为例，介绍了中国石拱桥的特点和光辉成就，分析了取得成就的原因，介绍了解放后桥梁事业的飞跃发展，歌颂了我国劳动人民的智慧和力量，以及社会主义制度的优越性。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 说明术语 · 用字 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">弧形</span><span class="acc-d">圆周的一部分的形状，即弯曲如弓的形状。</span></div>
      <div class="acc-item"><span class="acc-w">长虹卧波</span><span class="acc-d">长长的彩虹横卧在水波上，形容水上拱桥的优美姿态。</span></div>
      <div class="acc-item"><span class="acc-w">雄跨</span><span class="acc-d">气势雄伟地跨越。</span></div>
      <div class="acc-item"><span class="acc-w">悠久</span><span class="acc-d">年代久远。</span></div>
      <div class="acc-item"><span class="acc-w">杰作</span><span class="acc-d">超出一般水平的优秀作品。</span></div>
      <div class="acc-item"><span class="acc-w">巧妙绝伦</span><span class="acc-d">灵巧高明，没有能比得上的。伦，同类、同等。</span></div>
      <div class="acc-item"><span class="acc-w">匀称</span><span class="acc-d">（chèn）均匀、比例和谐。</span></div>
      <div class="acc-item"><span class="acc-w">古朴</span><span class="acc-d">朴素而有古代的风格。</span></div>
      <div class="acc-item"><span class="acc-w">联拱石桥</span><span class="acc-d">由多个石拱相连而成的石桥。</span></div>
      <div class="acc-item"><span class="acc-w">惟妙惟肖</span><span class="acc-d">（xiào）形容描写或模仿得非常逼真、传神。</span></div>
      <div class="acc-item"><span class="acc-w">推崇</span><span class="acc-d">十分推重、崇敬。</span></div>
      <div class="acc-item"><span class="acc-w">独一无二</span><span class="acc-d">没有相同的，没有可以相比的。</span></div>
      <div class="acc-item"><span class="acc-w">就地取材</span><span class="acc-d">在本地选取需要的材料。</span></div>
      <div class="acc-item"><span class="acc-w">飞跃发展</span><span class="acc-d">形容发展速度极快。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>说明文术语</h3>
      <div class="acc-item"><span class="acc-w">说明对象</span><span class="acc-d">文章要说明的事物或事理。本文的说明对象是中国石拱桥。</span></div>
      <div class="acc-item"><span class="acc-w">说明方法</span><span class="acc-d">说明事物特征的方法，常见的有举例子、列数字、打比方、作比较、分类别、下定义、作诠释、摹状貌、引用等。</span></div>
      <div class="acc-item"><span class="acc-w">举例子</span><span class="acc-d">举出实际事例来说明事物，使说明更具体、更有说服力。本文举了赵州桥和卢沟桥。</span></div>
      <div class="acc-item"><span class="acc-w">列数字</span><span class="acc-d">用具体数字来说明事物，使说明更精确、更有说服力。如“全长50.82米”。</span></div>
      <div class="acc-item"><span class="acc-w">打比方</span><span class="acc-d">通过比喻来说明事物，使说明更生动形象。如“桥洞成弧形，就像虹”。</span></div>
      <div class="acc-item"><span class="acc-w">作比较</span><span class="acc-d">通过对比来突出事物的特征。如河堤常被冲毁而卢沟桥极少出事。</span></div>
      <div class="acc-item"><span class="acc-w">摹状貌</span><span class="acc-d">对事物的形状、姿态等进行描写，使说明更生动。如石刻狮子的各种姿态。</span></div>
      <div class="acc-item"><span class="acc-w">下定义</span><span class="acc-d">用简明的语言揭示事物的本质特征。如“这种桥叫做联拱石桥”。</span></div>
      <div class="acc-item"><span class="acc-w">说明顺序</span><span class="acc-d">说明内容的安排次序，常见的有时间顺序、空间顺序、逻辑顺序。本文主要用逻辑顺序。</span></div>
      <div class="acc-item"><span class="acc-w">逻辑顺序</span><span class="acc-d">按照事物或事理的内在逻辑关系来安排说明顺序，如从一般到个别、从概括到具体、由主到次等。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">弧形</span><span class="acc-d">（hú）弓字旁；与「狐」（反犬旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">洨河</span><span class="acc-d">（xiáo）三点水，河名；生僻字。</span></div>
      <div class="acc-item"><span class="acc-w">巧妙绝伦</span><span class="acc-d">（lún）单人旁；与「论」（言字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">匀称</span><span class="acc-d">（chèn）禾字旁；多音字，此处读chèn，不读chēng。</span></div>
      <div class="acc-item"><span class="acc-w">张鷟</span><span class="acc-d">（zhuó）鸟字旁，人名用字；生僻字。</span></div>
      <div class="acc-item"><span class="acc-w">惟妙惟肖</span><span class="acc-d">（wéi xiào）「惟」竖心旁，「肖」月字旁；成语固定写法。</span></div>
      <div class="acc-item"><span class="acc-w">推崇</span><span class="acc-d">（chóng）山字头；与「祟」（suì，鬼怪）区分。</span></div>
      <div class="acc-item"><span class="acc-w">河堤</span><span class="acc-d">（dī）土字旁；与「提」（tí，提手旁）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">抓住特征</span><span class="acc-d">全文围绕“形式优美、结构坚固”的特征展开，两个例子都紧扣特征，中心明确。</span></div>
      <div class="acc-item"><span class="acc-w">典型举例</span><span class="acc-d">以赵州桥（独拱）和卢沟桥（联拱）两个典型例子，全面说明中国石拱桥的特点。</span></div>
      <div class="acc-item"><span class="acc-w">方法多样</span><span class="acc-d">综合运用举例子、列数字、打比方、作比较、引用、摹状貌等多种说明方法。</span></div>
      <div class="acc-item"><span class="acc-w">语言准确</span><span class="acc-d">大量使用修饰限制词（大约、可能、几乎、约等），体现说明文语言的准确性和严密性。</span></div>
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
  <div class="kai">《中国石拱桥》</div>
  <div>茅以升 · 现代 · 出自《人民日报》</div>
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
