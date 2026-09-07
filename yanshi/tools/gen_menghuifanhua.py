# -*- coding: utf-8 -*-
"""生成《梦回繁华》毛宁 课件（说明文）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\menghuifanhua-maoning.html"
FS_KEY = "menghui_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

paragraphs = [
    (
        "北宋时期，商业手工业迅速发展，城市布局打破了坊与市的严格界限，出现空前的繁荣局面。北宋汴京商业繁盛，除了商业中心之外，还有定期集市。城中有沿街叫卖的小贩，有说书的、演杂剧的、耍杂技的，还有卖花的、卖卦的、卖酸文的，真是热闹非凡。",
        "介绍《清明上河图》产生的时代背景：北宋商业手工业繁荣，城市布局打破坊市界限，汴京商业繁盛、市井生活丰富。",
        "说明对象：《清明上河图》及其时代背景。说明方法：举例子（说书的、演杂剧的、耍杂技的等）。说明语言：“空前”“繁盛”“热闹非凡”等词写出北宋的繁荣，为下文介绍画作铺垫。",
        [
            ("坊", "古代城市中的住宅区"),
            ("市", "古代城市中的商业区"),
            ("界限", "不同事物的分界"),
            ("空前", "以前所没有的"),
            ("汴京", "北宋都城，即今河南开封"),
            ("繁盛", "繁荣兴盛"),
            ("集市", "定期聚集进行商品交易的市场"),
            ("小贩", "做小买卖的人"),
            ("杂剧", "宋代的一种戏曲形式"),
            ("耍杂技", "表演杂技"),
            ("卖卦", "以占卜为业"),
            ("酸文", "指迂腐的文章，这里指卖文为生的人"),
            ("热闹非凡", "形容热闹的程度超过一般"),
        ],
    ),
    (
        "张择端的《清明上河图》便是北宋风俗画的代表作，也是中国十大传世名画之一。它是一幅绢本设色长卷，长约528厘米，高约24.8厘米。全卷以全景式构图和长卷的形式，描绘了北宋都城汴京从城郊、汴河到城内街市的繁华景象。",
        "总体介绍《清明上河图》：作者、地位、形制（绢本设色长卷）、尺寸、构图形式和描绘内容。",
        "说明方法：列数字（长约528厘米，高约24.8厘米）、下定义（绢本设色长卷）、分类别（从城郊、汴河到城内街市三部分）。说明语言：“约”表示约数，准确严密；“全景式构图”专业术语准确。",
        [
            ("张择端", "北宋末年画家，《清明上河图》的作者"),
            ("风俗画", "以社会生活风俗为题材的绘画"),
            ("传世名画", "流传于世的著名画作"),
            ("绢本", "以绢为底本的书画"),
            ("设色", "涂色、着色"),
            ("长卷", "中国书画的一种装裱形式，横幅长幅"),
            ("全景式构图", "将广阔的场景全部纳入画面的构图方式"),
            ("汴河", "河流名，流经北宋都城汴京"),
            ("街市", "商店较多的街道"),
        ],
    ),
    (
        "《清明上河图》采用了中国传统绘画特有的手卷形式，以移动的视点摄取对象。全图内容庞大，却繁而不乱，长而不冗，段落清晰，结构严谨。画中人物有五百多个，形态各异，个个传神。采用兼工带写的手法，线条遒劲，笔法灵动，有别于一般的界画。",
        "说明《清明上河图》的艺术特点：手卷形式、移动视点、繁而不乱的结构、众多传神的人物、兼工带写的笔法。",
        "说明方法：列数字（五百多个人物）、作比较（有别于一般的界画）、作诠释（解释手卷形式和兼工带写手法）。说明语言：“繁而不乱，长而不冗”四字短语精练准确；“遒劲”“灵动”等词专业而生动。",
        [
            ("手卷", "中国书画的一种横幅长卷，可从右至左展开观赏"),
            ("视点", "观察或描绘事物的角度"),
            ("摄取", "吸收、捕捉"),
            ("繁而不乱", "内容繁多但条理清晰，不杂乱"),
            ("长而不冗", "篇幅长但不冗长累赘"),
            ("形态各异", "形状姿态各不相同"),
            ("传神", "描绘人或物，给人生动逼真的印象"),
            ("兼工带写", "中国画的一种技法，兼用工笔和写意"),
            ("遒劲", "（qiú jìng）雄健有力"),
            ("灵动", "活泼不呆板、富于变化"),
            ("界画", "中国画的一种，以宫室、楼台、屋宇等为题材，用界笔划线"),
        ],
    ),
    (
        "画面开卷处描绘的是汴京近郊的风光。疏林薄雾，掩映着几家农舍；一片杨柳，嫩枝舒展，似乎刚从寒冬中苏醒过来。路上有一顶轿子，轿内坐着一个妇人，轿后跟着几个随从。远处有一行人，正匆匆向城内走去。这是一幅宁静而充满生机的早春图。",
        "介绍画面开卷处（近郊风光）：疏林薄雾、农舍杨柳、轿子随从、行人赶路，构成宁静而充满生机的早春图。",
        "说明方法：摹状貌（疏林薄雾、嫩枝舒展、轿子随从等）、打比方（早春图）。说明顺序：空间顺序（从远到近，从景物到人物）。说明语言：“掩映”“舒展”“苏醒”等词生动优美，有文学色彩；“宁静而充满生机”准确概括画面氛围。",
        [
            ("开卷", "展开画卷，指画卷的开头部分"),
            ("近郊", "城市周围附近的地方"),
            ("疏林", "稀疏的树林"),
            ("薄雾", "淡淡的雾气"),
            ("掩映", "彼此遮掩而互相衬托"),
            ("农舍", "农家的房屋"),
            ("嫩枝", "娇嫩的树枝"),
            ("舒展", "不卷缩、展开"),
            ("苏醒", "从昏迷或沉睡中醒过来，文中指春天到来"),
            ("轿子", "旧时的交通工具，由人抬着走"),
            ("随从", "跟随在身边的人"),
            ("匆匆", "急急忙忙的样子"),
            ("生机", "生存的机会、生命力"),
        ],
    ),
    (
        "画面中段是汴河两岸的繁华情景。汴河是当时南北交通的要道，也是汴京的生命线。巨大的漕船，往来穿梭，有的停在码头，有的正在行驶。最引人注目的是那艘准备驶过拱桥的大船。船工们有的站在船篷顶上，有的在船舷边，有的在船头，有的在船尾，各就各位，紧张地忙碌着。桥上桥下，行人如织，车水马龙，一片繁忙景象。",
        "介绍画面中段（汴河两岸）：汴河的重要地位、漕船往来、大船过拱桥的紧张场面、桥上桥下的繁忙景象。",
        "说明方法：摹状貌（船工们的各种姿态、行人如织）、打比方（生命线）、分类别（分船工的不同位置说明）。说明语言：“生命线”比喻汴河的重要性；“各就各位”“紧张地忙碌”写出船工的分工合作；“行人如织，车水马龙”用成语写繁华，生动形象。",
        [
            ("中段", "中间的部分"),
            ("要道", "重要的道路"),
            ("生命线", "比喻维持生存和发展的最重要的因素"),
            ("漕船", "（cáo）运输粮食的船"),
            ("往来穿梭", "来来往往，像织布的梭子一样频繁"),
            ("码头", "在江河沿岸及港湾内，供停船时装卸货物和乘客上下的建筑"),
            ("引人注目", "引起人们的注意"),
            ("拱桥", "中部高起、桥洞呈弧形的桥"),
            ("船篷", "船上遮蔽日光和风雨的设备"),
            ("船舷", "（xián）船两侧的边"),
            ("各就各位", "各自到各自的位置上"),
            ("行人如织", "行人多得像织布的线一样，密密麻麻"),
            ("车水马龙", "车像流水，马像游龙，形容车马或车辆很多，来往不绝"),
        ],
    ),
    (
        "画面后段描写的是市区街道的景象。街上行人摩肩接踵，络绎不绝。士农工商，男女老幼，无所不有。有骑马的，有坐轿的，有挑担的，有推车的，有赶驴的，有步行的。街道两旁，店铺林立，酒楼、茶坊、当铺、诊所、香铺、肉铺，应有尽有。招牌上写着“王家纸马”“孙羊店”“正店”等字样。最有趣的是那座“孙羊店”，门前搭着彩楼，招徕顾客。这一切，生动地再现了北宋都城的繁华和市井生活的丰富。",
        "介绍画面后段（市区街道）：行人摩肩接踵、各行各业无所不有、店铺林立、招牌彩楼，生动再现北宋都城的繁华和市井生活。",
        "说明方法：摹状貌（各种行人、店铺、招牌）、分类别（士农工商、各种店铺）、举例子（“王家纸马”“孙羊店”“正店”）。说明语言：“摩肩接踵”“络绎不绝”“应有尽有”等成语准确写出繁华；“最有趣的是”用口语化表达，亲切自然。",
        [
            ("后段", "后面的部分"),
            ("摩肩接踵", "（zhǒng）肩碰肩，脚碰脚，形容人很多，很拥挤"),
            ("络绎不绝", "（yì）形容行人车马来来往往，接连不断"),
            ("士农工商", "古代指读书的、种田的、做工的、经商的四种人"),
            ("无所不有", "什么都有"),
            ("挑担", "用肩膀挑着担子"),
            ("店铺", "各种商店、铺子"),
            ("林立", "像树林一样密集地竖立着，形容很多"),
            ("酒楼", "卖酒和饭菜的店铺"),
            ("茶坊", "茶馆、卖茶的店铺"),
            ("当铺", "用衣物等作抵押借钱的店铺"),
            ("诊所", "医生给病人看病的地方"),
            ("香铺", "卖香的店铺"),
            ("纸马", "旧时祭祀用的纸糊的马"),
            ("正店", "宋代有酿酒权的大酒店"),
            ("彩楼", "用彩帛装饰的门楼，店铺的广告装饰"),
            ("招徕", "（lái）招揽、招引"),
            ("市井", "街市、市场"),
        ],
    ),
    (
        "《清明上河图》不仅是一幅艺术珍品，更是研究北宋社会生活的珍贵史料。它以写实的手法，记录了当时的城市面貌、市井风情、交通运输、建筑风格等，为我们了解北宋历史提供了生动的图像资料。",
        "说明《清明上河图》的双重价值：艺术珍品和珍贵史料，以写实手法记录了北宋社会生活的多个方面。",
        "说明方法：分类别（城市面貌、市井风情、交通运输、建筑风格）、作比较（不仅是……更是……，递进关系突出史料价值）。说明语言：“不仅……更是……”递进关联词，强调后者；“珍贵史料”“生动的图像资料”准确概括其价值。",
        [
            ("艺术珍品", "珍贵的艺术作品"),
            ("史料", "研究历史的资料"),
            ("写实", "真实地描绘事物"),
            ("城市面貌", "城市的外观和景象"),
            ("市井风情", "街市上的风俗习惯"),
            ("交通运输", "各种运输和交通事业"),
            ("建筑风格", "建筑的艺术特色和风格"),
            ("图像资料", "以图像形式保存的资料"),
        ],
    ),
    (
        "这幅画的作者张择端，是北宋末年的画家。他擅长画舟车、市桥、郭径，自成一家。《清明上河图》是他唯一的传世作品，也是中国绘画史上的不朽杰作。",
        "介绍作者张择端：北宋末年画家，擅长画舟车市桥，《清明上河图》是其唯一传世作品和不朽杰作。",
        "说明方法：下定义（对张择端的身份和特长进行说明）。说明语言：“擅长”“自成一家”“唯一”“不朽杰作”等词准确评价作者和作品，简洁有力。",
        [
            ("北宋末年", "北宋王朝的末期"),
            ("擅长", "在某方面有特长"),
            ("舟车", "船和车，泛指交通工具"),
            ("市桥", "城市中的桥梁"),
            ("郭径", "城外的道路。郭，外城；径，小路"),
            ("自成一家", "在某种学问或技艺上有独创的风格或方法，能自成体系"),
            ("传世作品", "流传到后世的作品"),
            ("不朽杰作", "永不磨灭的优秀作品"),
        ],
    ),
]

parts = [
    ("第一部分", "时代背景与画作总览", "1–3 段", "介绍北宋商业繁荣的时代背景，总体说明《清明上河图》的形制、尺寸和艺术特点。"),
    ("第二部分", "画面内容详解", "4–6 段", "按空间顺序分别介绍画面开卷处（近郊）、中段（汴河）、后段（市区）的内容。"),
    ("第三部分", "价值与作者", "7–8 段", "说明《清明上河图》的艺术价值和史料价值，介绍作者张择端。"),
]

para_part = [0,0,0, 1,1,1, 2,2]

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
    {"w":"汴","py":"biàn","q":"北宋□京商业繁盛","tip":"「汴」三点水，汴京（开封）；生僻字，注意右边是「卞」"},
    {"w":"绢","py":"juàn","q":"它是一幅□本设色长卷","tip":"「绢」绞丝旁，丝织品；不要写成「娟」（女字旁）"},
    {"w":"冗","py":"rǒng","q":"全图内容庞大，却繁而不乱，长而不□","tip":"「冗」秃宝盖，多余；不要写成「沉」（三点水）"},
    {"w":"遒","py":"qiú","q":"线条□劲，笔法灵动","tip":"「遒」走之底，雄健；生僻字，注意里面是「酋」"},
    {"w":"掩","py":"yǎn","q":"疏林薄雾，□映着几家农舍","tip":"「掩」提手旁，遮蔽；不要写成「淹」（三点水）"},
    {"w":"轿","py":"jiào","q":"路上有一顶□子，内坐着一个妇人","tip":"「轿」车字旁，轿子；不要写成「桥」（木字旁）"},
    {"w":"漕","py":"cáo","q":"巨大的□船，往来穿梭","tip":"「漕」三点水，运输粮食；生僻字，注意右边是「曹」"},
    {"w":"舷","py":"xián","q":"有的在船□边，有的在船头","tip":"「舷」舟字旁，船两侧的边；不要写成「弦」（弓字旁）"},
    {"w":"踵","py":"zhǒng","q":"街上行人摩肩接□，络绎不绝","tip":"「踵」足字旁，脚后跟；生僻字，注意右边是「重」"},
    {"w":"绎","py":"yì","q":"街上行人摩肩接踵，络□不绝","tip":"「绎」绞丝旁，连续；不要写成「译」（言字旁）"},
    {"w":"铺","py":"pù","q":"街道两旁，店□林立","tip":"「铺」金字旁，商店；多音字，此处读pù不读pū"},
    {"w":"档","py":"dàng","q":"当□","tip":"「档」木字旁，用衣物抵押借钱的店铺；不要写成「挡」（提手旁）"},
    {"w":"徕","py":"lái","q":"门前搭着彩楼，招□顾客","tip":"「徕」双人旁，招引；生僻字，与「来」区分"},
    {"w":"择","py":"zé","q":"这幅画的作者张□端，是北宋末年的画家","tip":"「择」提手旁，挑选；不要写成「泽」（三点水）"},
]

dict_notes = [
    {"w":"坊市","a":"古代城市中的住宅区（坊）和商业区（市）","q":"打破了坊与市的严格界限"},
    {"w":"汴京","a":"北宋都城，即今河南开封","q":"北宋汴京商业繁盛"},
    {"w":"风俗画","a":"以社会生活风俗为题材的绘画","q":"北宋风俗画的代表作"},
    {"w":"绢本设色","a":"以绢为底本、涂色的书画","q":"绢本设色长卷"},
    {"w":"长卷","a":"中国书画的一种横幅长幅装裱形式","q":"长约528厘米，高约24.8厘米"},
    {"w":"全景式构图","a":"将广阔场景全部纳入画面的构图方式","q":"以全景式构图和长卷的形式"},
    {"w":"手卷","a":"中国书画的横幅长卷，可从右至左展开观赏","q":"中国传统绘画特有的手卷形式"},
    {"w":"繁而不乱","a":"内容繁多但条理清晰","q":"却繁而不乱"},
    {"w":"长而不冗","a":"篇幅长但不冗长累赘","q":"长而不冗"},
    {"w":"兼工带写","a":"中国画技法，兼用工笔和写意","q":"采用兼工带写的手法"},
    {"w":"遒劲","a":"雄健有力","q":"线条遒劲"},
    {"w":"界画","a":"以宫室楼台为题材、用界笔划线的中国画","q":"有别于一般的界画"},
    {"w":"漕船","a":"运输粮食的船","q":"巨大的漕船"},
    {"w":"摩肩接踵","a":"肩碰肩脚碰脚，形容人很多很拥挤","q":"行人摩肩接踵"},
    {"w":"络绎不绝","a":"形容行人车马来来往往接连不断","q":"络绎不绝"},
    {"w":"招徕","a":"招揽、招引","q":"招徕顾客"},
    {"w":"写实","a":"真实地描绘事物","q":"以写实的手法"},
    {"w":"史料","a":"研究历史的资料","q":"研究北宋社会生活的珍贵史料"},
    {"w":"自成一家","a":"在学问或技艺上有独创风格，自成体系","q":"自成一家"},
    {"w":"列数字","a":"说明方法之一，用具体数字说明","q":"长约528厘米，高约24.8厘米"},
    {"w":"摹状貌","a":"说明方法之一，对事物形态进行描写","q":"疏林薄雾，掩映着几家农舍"},
    {"w":"空间顺序","a":"按照空间方位安排说明顺序","q":"从城郊、汴河到城内街市"},
    {"w":"举例子","a":"说明方法之一，举出实际事例","q":"招牌上写着王家纸马、孙羊店"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《梦回繁华》毛宁</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 毛宁</div>
  <h1 class="hero-title">梦回繁华</h1>
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
    <p>《梦回繁华》是毛宁写的一篇事物说明文，介绍了北宋画家张择端的传世名画《清明上河图》。文章从北宋商业繁荣的时代背景写起，总体介绍了画作的形制、尺寸和艺术特点，然后按空间顺序详细描绘了画面的三个部分（近郊、汴河、市区），最后说明了画作的艺术价值和史料价值。</p>
    <p>文章语言准确而生动，在说明中融入描写，使读者仿佛穿越时空，梦回北宋繁华的汴京。本文是学习说明文写作和了解中国古代绘画艺术的优秀篇目。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>毛宁，当代作家，长期从事中国古代艺术史的研究和普及工作。其文章以准确的说明和生动的描写见长，善于将专业的艺术知识用通俗易懂的语言介绍给大众。《梦回繁华》是其介绍中国古代绘画的代表作之一。</p>
  </div>
  <div class="box">
    <h3>《清明上河图》简介</h3>
    <p>《清明上河图》是北宋画家张择端的传世名作，中国十大传世名画之一。画作以长卷形式，描绘了北宋都城汴京（今河南开封）的城市面貌和社会各阶层人民的生活状况，是北宋时期都城繁荣的见证，也是北宋城市经济情况的写照。</p>
    <p style="margin-top:8px">画作现藏于北京故宫博物院，全长528厘米，高24.8厘米，画中人物多达五百余人，另有牛、马、骡、驴等牲畜六十多匹，木船二十多只，房屋楼阁三十多栋，推车乘轿也有二十多件，具有极高的艺术价值和史料价值。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文朗读《梦回繁华》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1kD4y1m75s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读梦回繁华"></iframe>
        <a href="https://www.bilibili.com/video/BV1kD4y1m75s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>画中人醒来了：清明上河图</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1wDta6iE41&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="画中人醒来了清明上河图"></iframe>
        <a href="https://www.bilibili.com/video/BV1wDta6iE41" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">说明对象：《清明上河图》</div>
        <p>本文的说明对象是北宋画家张择端的《清明上河图》。文章从时代背景写起，然后介绍画作的总体情况和艺术特点，再按空间顺序详细描绘画面内容，最后说明画作的价值和作者。说明对象明确，内容全面。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">核心特征：繁华与写实</div>
        <p>文章以“繁华”为文眼，贯穿全文。时代背景是“空前的繁荣”，画面内容是“繁华景象”“繁忙景象”，历史价值是“生动地再现了北宋都城的繁华”。同时，画作的“写实”手法是其成为珍贵史料的关键，也是文章反复强调的特征。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">列数字与下定义：准确而专业</div>
        <p>列数字：“长约528厘米，高约24.8厘米”“人物有五百多个”，用精确的数字说明画作的规模；下定义：“绢本设色长卷”“全景式构图”“兼工带写”等专业术语，准确说明画作的形制和技法。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">摹状貌与打比方：生动而形象</div>
        <p>摹状貌是本文最主要的说明方法：“疏林薄雾，掩映着几家农舍”“船工们有的站在船篷顶上……各就各位”“行人摩肩接踵，络绎不绝”，生动地再现了画面内容；打比方：“汴京的生命线”“早春图”，使说明更形象。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">分类别与举例子：条理清晰</div>
        <p>分类别：将画面分为城郊、汴河、市区三部分分别说明；将行人分为“骑马的、坐轿的、挑担的”等；将店铺分为“酒楼、茶坊、当铺”等。举例子：“王家纸马”“孙羊店”“正店”等具体招牌，使说明更具体。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明顺序</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">整体：逻辑顺序（从背景到内容到价值）</div>
        <p>文章整体采用逻辑顺序：先写时代背景（为什么会有这样的画），再写画作总体情况（是什么样的画），然后详细介绍画面内容（画了什么），最后说明价值和作者（有什么意义、谁画的）。由因到果，由整体到局部，由介绍到评价，逻辑清晰。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">局部：空间顺序（从城郊到汴河到市区）</div>
        <p>介绍画面内容时，严格按照画卷的空间顺序：开卷处（近郊风光）→中段（汴河两岸）→后段（市区街道）。由远及近，由城外到城内，与手卷展开的顺序一致，使读者仿佛跟随画卷徐徐展开，身临其境。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明语言的特点</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">准确严密：科学的态度</div>
        <p>“长约528厘米，高约24.8厘米”“约”表示约数；“人物有五百多个”“多”表示概数；“不仅是……更是……”递进关系准确。数字精确，表述留有余地，体现了说明文语言的准确性。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">生动优美：文学的笔法</div>
        <p>“疏林薄雾，掩映着几家农舍”“嫩枝舒展，似乎刚从寒冬中苏醒过来”“行人如织，车水马龙”——文章在说明中大量运用描写，语言优美生动，富有文学色彩，使读者在了解知识的同时获得美的享受。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">标题含蓄：梦回繁华</div>
        <p>“梦回繁华”这一标题含蓄而富有诗意：“梦”字点出《清明上河图》是对逝去繁华的追忆，“繁华”概括了画作的核心内容和北宋的时代特征。标题既点明了说明对象的内涵，又营造了悠远的意境。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《梦回繁华》通过介绍北宋画家张择端的《清明上河图》，展现了北宋都城汴京的繁华景象和社会生活，说明了这幅画作的艺术价值和史料价值，表达了对中国古代绘画艺术的赞美和对北宋繁华文明的追忆。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 说明术语 · 用字 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">坊市</span><span class="acc-d">古代城市中的住宅区（坊）和商业区（市）。</span></div>
      <div class="acc-item"><span class="acc-w">汴京</span><span class="acc-d">北宋都城，即今河南开封。</span></div>
      <div class="acc-item"><span class="acc-w">风俗画</span><span class="acc-d">以社会生活风俗为题材的绘画。</span></div>
      <div class="acc-item"><span class="acc-w">绢本设色</span><span class="acc-d">以绢为底本、涂色的书画。</span></div>
      <div class="acc-item"><span class="acc-w">长卷</span><span class="acc-d">中国书画的一种横幅长幅装裱形式。</span></div>
      <div class="acc-item"><span class="acc-w">繁而不乱</span><span class="acc-d">内容繁多但条理清晰，不杂乱。</span></div>
      <div class="acc-item"><span class="acc-w">长而不冗</span><span class="acc-d">篇幅长但不冗长累赘。</span></div>
      <div class="acc-item"><span class="acc-w">兼工带写</span><span class="acc-d">中国画技法，兼用工笔和写意。</span></div>
      <div class="acc-item"><span class="acc-w">遒劲</span><span class="acc-d">（qiú jìng）雄健有力。</span></div>
      <div class="acc-item"><span class="acc-w">界画</span><span class="acc-d">以宫室楼台为题材、用界笔划线的中国画。</span></div>
      <div class="acc-item"><span class="acc-w">漕船</span><span class="acc-d">（cáo）运输粮食的船。</span></div>
      <div class="acc-item"><span class="acc-w">摩肩接踵</span><span class="acc-d">（zhǒng）肩碰肩脚碰脚，形容人很多很拥挤。</span></div>
      <div class="acc-item"><span class="acc-w">络绎不绝</span><span class="acc-d">（yì）形容行人车马来来往往接连不断。</span></div>
      <div class="acc-item"><span class="acc-w">招徕</span><span class="acc-d">（lái）招揽、招引。</span></div>
      <div class="acc-item"><span class="acc-w">自成一家</span><span class="acc-d">在学问或技艺上有独创风格，自成体系。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>说明文术语</h3>
      <div class="acc-item"><span class="acc-w">说明对象</span><span class="acc-d">文章要说明的事物。本文的说明对象是《清明上河图》。</span></div>
      <div class="acc-item"><span class="acc-w">列数字</span><span class="acc-d">说明方法之一，用具体数字说明。如“长约528厘米”。</span></div>
      <div class="acc-item"><span class="acc-w">下定义</span><span class="acc-d">说明方法之一，用简明语言揭示事物本质。如“绢本设色长卷”。</span></div>
      <div class="acc-item"><span class="acc-w">摹状貌</span><span class="acc-d">说明方法之一，对事物形态进行描写。本文大量运用。</span></div>
      <div class="acc-item"><span class="acc-w">打比方</span><span class="acc-d">说明方法之一，通过比喻介绍事物。如“汴京的生命线”。</span></div>
      <div class="acc-item"><span class="acc-w">分类别</span><span class="acc-d">说明方法之一，按类别分别说明。如画面分三部分。</span></div>
      <div class="acc-item"><span class="acc-w">举例子</span><span class="acc-d">说明方法之一，举出实际事例。如具体的店铺招牌。</span></div>
      <div class="acc-item"><span class="acc-w">空间顺序</span><span class="acc-d">按照空间方位安排说明顺序。本文按城郊→汴河→市区的顺序。</span></div>
      <div class="acc-item"><span class="acc-w">逻辑顺序</span><span class="acc-d">按照事物的内在逻辑关系安排说明顺序。本文整体采用逻辑顺序。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">汴京</span><span class="acc-d">（biàn）三点水；生僻字，注意右边是「卞」。</span></div>
      <div class="acc-item"><span class="acc-w">绢本</span><span class="acc-d">（juàn）绞丝旁，丝织品；与「娟」（女字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">长而不冗</span><span class="acc-d">（rǒng）秃宝盖，多余；与「沉」（三点水）区分。</span></div>
      <div class="acc-item"><span class="acc-w">遒劲</span><span class="acc-d">（qiú）走之底，雄健；生僻字。</span></div>
      <div class="acc-item"><span class="acc-w">漕船</span><span class="acc-d">（cáo）三点水，运输粮食；生僻字。</span></div>
      <div class="acc-item"><span class="acc-w">船舷</span><span class="acc-d">（xián）舟字旁，船两侧的边；与「弦」（弓字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">摩肩接踵</span><span class="acc-d">（zhǒng）足字旁，脚后跟；生僻字。</span></div>
      <div class="acc-item"><span class="acc-w">络绎不绝</span><span class="acc-d">（yì）绞丝旁，连续；与「译」（言字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">招徕</span><span class="acc-d">（lái）双人旁，招引；与「来」区分。</span></div>
      <div class="acc-item"><span class="acc-w">张择端</span><span class="acc-d">（zé）提手旁，挑选；与「泽」（三点水）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">说明与描写结合</span><span class="acc-d">在准确说明的同时融入生动的描写，使说明文既有科学性又有文学性。</span></div>
      <div class="acc-item"><span class="acc-w">空间顺序清晰</span><span class="acc-d">按照画面展开的空间顺序介绍内容，由远及近，由城外到城内，条理清晰。</span></div>
      <div class="acc-item"><span class="acc-w">方法多样</span><span class="acc-d">综合运用列数字、下定义、摹状貌、打比方、分类别、举例子等多种说明方法。</span></div>
      <div class="acc-item"><span class="acc-w">语言准确生动</span><span class="acc-d">数字精确、术语专业，同时描写优美、成语丰富，做到准确与生动的统一。</span></div>
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
  <div class="kai">《梦回繁华》</div>
  <div>毛宁 · 现代 · 介绍《清明上河图》</div>
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
