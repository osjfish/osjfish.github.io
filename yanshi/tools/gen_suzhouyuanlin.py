# -*- coding: utf-8 -*-
"""生成《苏州园林》叶圣陶 课件（说明文）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\suzhouyuanlin-yetaotao.html"
FS_KEY = "suzhou_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

paragraphs = [
    (
        "苏州园林据说有一百多处，我到过的不过十多处。其他地方的园林我也到过一些。倘若要我说说总的印象，我觉得苏州园林是我国各地园林的标本，各地园林或多或少都受到苏州园林的影响。因此，谁如果要鉴赏我国的园林，苏州园林就不该错过。",
        "总说苏州园林在我国园林中的地位——各地园林的标本，引出下文对苏州园林特点的具体说明。",
        "说明对象：苏州园林。说明方法：列数字（一百多处、十多处）、作比较（苏州园林与其他地方园林比较）。说明语言：“据说”“不过”“或多或少”等词准确留有余地，体现说明文语言的准确性。",
        [
            ("据说", "听别人说，表示信息来源不是亲自确认"),
            ("标本", "这里指典范、代表"),
            ("或多或少", "或者多或者少，表示数量不一定"),
            ("鉴赏", "鉴定和欣赏（艺术品、文物等）"),
            ("错过", "失去机会、没有赶上"),
        ],
    ),
    (
        "设计者和匠师们因地制宜，自出心裁，修建成功的园林当然各个不同。可是苏州各个园林在不同之中有个共同点，似乎设计者和匠师们一致追求的是：务必使游览者无论站在哪个点上，眼前总是一幅完美的图画。为了达到这个目的，他们讲究亭台轩榭的布局，讲究假山池沼的配合，讲究花草树木的映衬，讲究近景远景的层次。总之，一切都要为构成完美的图画而存在，决不容许有欠美伤美的败笔。他们唯愿游览者得到“如在画图中”的美感，而他们的成绩实现了他们的愿望，游览者来到园里，没有一个不心里想着口头说着“如在画图中”的。",
        "点明苏州园林的总体特征：务必使游览者无论站在哪个点上，眼前总是一幅完美的图画。并从四个方面概括下文的说明内容。",
        "说明方法：作比较（各个不同与共同点）、引用（“如在画图中”）。说明结构：总分结构，本段是总说，下文从四个“讲究”分项说明。说明语言：“务必”“总是”“决不容许”等词强调追求的严格，“似乎”表示推测，准确严密。",
        [
            ("因地制宜", "根据不同地区的具体情况规定适宜的办法"),
            ("自出心裁", "出于自己的创造，指不抄袭、模仿别人"),
            ("匠师", "有专门技艺的工匠"),
            ("务必", "必须、一定要"),
            ("游览者", "游览的人"),
            ("亭台轩榭", "（xuān xiè）泛指园林中的各种建筑物。轩，有窗的廊子或小屋；榭，建筑在台上的房屋"),
            ("布局", "全面安排、布置"),
            ("池沼", "（zhǎo）比较大的水坑"),
            ("映衬", "映照、衬托"),
            ("层次", "事物的次序、阶段"),
            ("欠美伤美", "破坏美感、有损于美"),
            ("败笔", "写字写得不好的一笔，引申为事情中做得不好的部分"),
            ("唯愿", "只希望"),
            ("美感", "对于美的感受或体会"),
        ],
    ),
    (
        "我国的建筑，从古代的宫殿到近代的一般住房，绝大部分是对称的，左边怎么样，右边也怎么样。苏州园林可绝不讲究对称，好像故意避免似的。东边有了一个亭子或者一道回廊，西边决不会来一个同样的亭子或者一道同样的回廊。这是为什么？我想，用图画来比方，对称的建筑是图案画，不是美术画，而园林是美术画，美术画要求自然之趣，是不讲究对称的。",
        "说明苏州园林不讲究对称的特点，以图案画和美术画的区别解释原因。",
        "说明方法：作比较（我国一般建筑的对称与苏州园林的不对称比较）、打比方（对称的建筑是图案画，园林是美术画）、举例子（东边有亭子西边不会有同样的亭子）。说明语言：“绝大部分”“可绝不”“好像”等词准确严密；设问句引起读者注意。",
        [
            ("对称", "图形或物体相对的两边各部分，在大小、形状和排列上一一对应"),
            ("回廊", "曲折环绕的走廊"),
            ("图案画", "强调对称、整齐的装饰性绘画"),
            ("美术画", "强调自然、生动的艺术性绘画"),
            ("自然之趣", "自然的趣味、情趣"),
        ],
    ),
    (
        "苏州园林里都有假山和池沼。假山的堆叠，可以说是一项艺术而不仅是技术。或者是重峦叠嶂，或者是几座小山配合着竹子花木，全在乎设计者和匠师们生平多阅历，胸中有丘壑，才能使游览者攀登的时候忘却苏州城市，只觉得身在山间。至于池沼，大多引用活水。有些园林池沼宽敞，就把池沼作为全园的中心，其他景物配合着布置。水面假如成河道模样，往往安排桥梁。假如安排两座以上的桥梁，那就一座一个样，决不雷同。池沼或河道的边沿很少砌齐整的石岸，总是高低屈曲任其自然。还在那儿布置几块玲珑的石头，或者种些花草：这也是为了取得从各个角度看都成一幅画的效果。池沼里养着金鱼或各色鲤鱼，夏秋季节荷花或睡莲开放，游览者看“鱼戏莲叶间”，又是入画的一景。",
        "说明苏州园林中假山和池沼的配合：假山堆叠是艺术，池沼引用活水、布置自然，处处追求入画的效果。",
        "说明方法：分类别（假山和池沼分别说明）、引用（“鱼戏莲叶间”出自汉乐府《江南》）、举例子（桥梁一座一个样、石岸高低屈曲）。说明语言：“大多”“往往”“很少”“总是”等词准确说明情况，留有余地；“艺术而不仅是技术”强调假山堆叠的审美价值。",
        [
            ("堆叠", "一层一层地堆起来"),
            ("重峦叠嶂", "（zhàng）重重叠叠的山峰。峦，连绵的山；嶂，像屏障的山峰"),
            ("阅历", "由经历得来的知识和经验"),
            ("胸中有丘壑", "（hè）心中有山水风景的形象，指有深远的构思和意境"),
            ("攀登", "抓着东西向上爬"),
            ("活水", "流动的水"),
            ("宽敞", "宽阔、宽大"),
            ("雷同", "不该相同而相同"),
            ("砌", "用和好的灰泥把砖石等一层层地垒起"),
            ("齐整", "整齐"),
            ("屈曲", "弯曲、曲折"),
            ("任其自然", "听任它自然发展，不加约束"),
            ("玲珑", "（东西）精巧细致"),
            ("入画", "进入画中，形容景物优美"),
        ],
    ),
    (
        "苏州园林栽种和修剪树木也着眼在画意。高树与低树俯仰生姿。落叶树与常绿树相间，花时不同的多种花树相间，这就一年四季不感到寂寞。没有修剪得像宝塔那样的松柏，没有阅兵式似的道旁树：因为依据中国画的审美观点看，这是不足取的。有几个园里有古老的藤萝，盘曲嶙峋的枝干就是一幅好画。开花的时候满眼的珠光宝气，使游览者感到无限的繁华和欢悦，可是没法说出来。",
        "说明苏州园林花草树木的映衬：高低错落、四季有景，不讲究整齐划一，追求自然画意。",
        "说明方法：作比较（苏州园林的树木与宝塔式松柏、阅兵式道旁树比较）、打比方（修剪得像宝塔那样、阅兵式似的）、举例子（古老的藤萝）、摹状貌（盘曲嶙峋的枝干、珠光宝气）。说明语言：“也着眼在画意”紧扣总体特征；“不感到寂寞”用拟人手法写园林的生机。",
        [
            ("栽种", "种植"),
            ("修剪", "用剪子修枝叶等使整齐美观"),
            ("着眼", "（从某方面）观察、考虑"),
            ("俯仰生姿", "高树好像低着头，低树好像抬着头，形成一种相互呼应的优美姿态"),
            ("落叶树", "秋冬季节叶子脱落的树"),
            ("常绿树", "全年都有绿叶的树"),
            ("相间", "一个隔着一个"),
            ("寂寞", "孤单冷清，文中指单调、没有变化"),
            ("审美观点", "对美的看法和标准"),
            ("不足取", "不值得采取、不值得效法"),
            ("藤萝", "紫藤的通称，一种攀援植物"),
            ("盘曲", "曲折环绕"),
            ("嶙峋", "（lín xún）形容山石等突兀、重叠，文中形容枝干瘦削有力"),
            ("珠光宝气", "形容服饰、陈设等非常华丽，文中形容藤萝花的繁盛艳丽"),
            ("繁华", "繁荣热闹"),
            ("欢悦", "欢乐喜悦"),
        ],
    ),
    (
        "游览苏州园林必然会注意到花墙和廊子。有墙壁隔着，有廊子界着，层次多了，景致就见得深了。可是墙壁上有砖砌的各式镂空图案，廊子大多是两边无所依傍的，实际是隔而不隔，界而未界，因而更增加了景致的深度。有几个园林还在适当的位置装上一面大镜子，层次就更多了，几乎可以说把整个园林翻了一番。",
        "说明苏州园林花墙和廊子的设计：通过“隔而不隔，界而未界”增加景致的层次和深度。",
        "说明方法：作诠释（解释花墙和廊子如何增加层次）、举例子（装大镜子）。说明语言：“必然”“大多”“几乎”等词准确严密；“隔而不隔，界而未界”用语精炼，准确概括了花墙廊子的设计妙处。",
        [
            ("花墙", "墙上有镂空图案的墙"),
            ("廊子", "屋檐下的过道或独立的有顶的过道"),
            ("界", "划分、隔开"),
            ("景致", "风景、景物"),
            ("砖砌", "用砖砌筑"),
            ("镂空", "在物体上雕刻出穿透物体的花纹或文字"),
            ("依傍", "依靠"),
            ("隔而不隔", "看似隔开了，实际上没有完全隔开"),
            ("界而未界", "看似划分了界限，实际上没有完全划清"),
            ("深度", "深浅的程度，文中指景致的纵深感"),
            ("翻了一番", "增加了一倍"),
        ],
    ),
    (
        "游览者必然也不会忽略另外一点，就是苏州园林在每一个角落都注意图画美。阶砌旁边栽几丛书带草。墙上蔓延着爬山虎或者蔷薇木香。如果开窗正对着白色墙壁，太单调了，给补上几竿竹子或几棵芭蕉。诸如此类，无非要游览者即使就极小范围的局部看，也能得到美的享受。",
        "说明苏州园林在每一个角落都注意图画美，以阶砌旁的草、墙上的藤蔓、窗前的竹蕉为例。",
        "说明方法：举例子（阶砌旁栽草、墙上爬山虎、窗前补竹蕉）。说明语言：“必然也不会忽略”承接上文；“诸如此类”“无非”等词口语化，亲切自然；“极小范围的局部”与“美的享受”对比，突出苏州园林处处皆画。",
        [
            ("忽略", "没有注意到、疏忽"),
            ("阶砌", "台阶"),
            ("书带草", "一种多年生草本植物，叶细长"),
            ("蔓延", "像蔓草一样向周围扩展"),
            ("爬山虎", "一种藤本植物，常攀附在墙壁上"),
            ("蔷薇", "一种落叶灌木，花有芳香"),
            ("木香", "一种攀援灌木，花白色或黄色，有香气"),
            ("单调", "简单重复，没有变化"),
            ("芭蕉", "一种多年生草本植物，叶子大而宽"),
            ("诸如此类", "与此相似的种种事物"),
            ("无非", "只、不外乎"),
            ("局部", "整体中的一部分"),
        ],
    ),
    (
        "苏州园林里的门和窗，图案设计和雕镂琢磨功夫都是工艺美术的上品。大致说来，那些门和窗尽量工细而决不庸俗，即使简朴而别具匠心。四扇，八扇，十二扇，综合起来看，谁都要赞叹这是高度的图案美。摄影家挺喜欢这些门和窗，他们斟酌着光和影，摄成称心满意的照片。",
        "说明苏州园林的门和窗：图案设计精美，雕镂功夫深厚，是工艺美术的上品。",
        "说明方法：列数字（四扇、八扇、十二扇）、举例子（摄影家喜欢拍门窗）。说明语言：“大致说来”“尽量”“即使”等词准确严密；“工细而决不庸俗”“简朴而别具匠心”用对比写出门窗的审美追求。",
        [
            ("雕镂", "（lòu）雕刻"),
            ("琢磨", "（zhuó mó）雕刻和打磨，也指思考考虑"),
            ("工艺美术", "指工艺品的制作艺术"),
            ("上品", "上等、最好的品级"),
            ("工细", "精巧细致"),
            ("庸俗", "平庸鄙俗，不高尚"),
            ("简朴", "简单朴素"),
            ("别具匠心", "另有一种巧妙的心思（多指文学、艺术方面创造性的构思）"),
            ("赞叹", "称赞、感叹"),
            ("斟酌", "考虑事情、文字等是否可行或是否适当"),
            ("称心满意", "形容心满意足，事情的发展完全符合心意"),
        ],
    ),
    (
        "苏州园林与北京的园林不同，极少使用彩绘。梁和柱子以及门窗栏杆大多漆广漆，那是不刺眼的颜色。墙壁白色。有些室内墙壁下半截铺水磨方砖，淡灰色和白色对衬。屋瓦和檐漏一律淡灰色。这些颜色与草木的绿色配合，引起人们安静闲适的感觉。花开时节，更显得各种花明艳照眼。",
        "说明苏州园林的色彩特点：极少使用彩绘，以淡灰色和白色为主，与草木绿色配合，给人安静闲适之感。",
        "说明方法：作比较（苏州园林与北京园林比较）、分类别（梁柱、墙壁、屋瓦分别说明）。说明语言：“极少”“大多”“有些”“一律”等词准确说明使用情况；“不刺眼”“安静闲适”从人的感受写色彩的效果。",
        [
            ("彩绘", "用彩色绘画装饰"),
            ("梁", "架在墙上或柱子上支撑屋顶的横木"),
            ("广漆", "一种天然漆，颜色深沉不刺眼"),
            ("刺眼", "光线过强，使眼睛不舒服"),
            ("下半截", "下半部分"),
            ("水磨方砖", "经过打磨的方形砖，表面光滑"),
            ("对衬", "互相映衬"),
            ("屋瓦", "屋顶上的瓦"),
            ("檐漏", "屋檐处滴水的瓦"),
            ("一律", "全部、一个样子"),
            ("闲适", "清闲安逸"),
            ("明艳照眼", "鲜明美丽，耀眼夺目"),
        ],
    ),
    (
        "可以说的当然不止以上这些，这里不再多写了。",
        "以简洁的收尾结束全文，暗示苏州园林的美还有很多，留有余味。",
        "说明方法：无特殊说明方法，以简洁的语言收束全文。说明语言：“当然不止”“不再多写”，留有余地，引发读者进一步探索的兴趣。",
        [
            ("不止", "不仅、超过"),
        ],
    ),
]

parts = [
    ("第一部分", "总说地位与特征", "1–2 段", "总说苏州园林是我国园林的标本，点明总体特征——务必使游览者眼前总是一幅完美的图画。"),
    ("第二部分", "分项说明特点", "3–9 段", "从布局、假山池沼、树木、花墙廊子、角落、门窗、色彩七个方面，具体说明苏州园林的特点。"),
    ("第三部分", "收尾留余味", "10 段", "以简洁的语言收尾，暗示苏州园林之美还有更多。"),
]

para_part = [0,0, 1,1,1,1,1,1,1, 2]

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
    {"w":"鉴","py":"jiàn","q":"谁如果要□赏我国的园林","tip":"「鉴」金字旁，仔细看；不要写成「签」（竹字头）"},
    {"w":"裁","py":"cái","q":"因地制宜，自出心□","tip":"「裁」衣字旁，安排取舍；不要写成「栽」（木字旁）"},
    {"w":"榭","py":"xiè","q":"讲究亭台轩□的布局","tip":"「榭」木字旁，建筑在台上的房屋；生僻字"},
    {"w":"沼","py":"zhǎo","q":"讲究假山池□的配合","tip":"「沼」三点水，水池；不要写成「诏」（言字旁）"},
    {"w":"嶂","py":"zhàng","q":"或者是重峦叠□","tip":"「嶂」山字旁，像屏障的山峰；与「障」（左耳旁）区分"},
    {"w":"壑","py":"hè","q":"胸中有丘□","tip":"「壑」土字头，山沟；生僻字，笔画较多"},
    {"w":"砌","py":"qì","q":"池沼或河道的边沿很少□齐整的石岸","tip":"「砌」石字旁，用砖石垒筑；不要写成「彻」（双人旁）"},
    {"w":"嶙","py":"lín","q":"盘曲□峋的枝干就是一幅好画","tip":"「嶙」山字旁，形容山石突兀；与「鳞」（鱼字旁）区分"},
    {"w":"峋","py":"xún","q":"盘曲嶙□的枝干就是一幅好画","tip":"「峋」山字旁，形容山石重叠；不要写成「询」（言字旁）"},
    {"w":"镂","py":"lòu","q":"图案设计和雕□琢磨功夫都是工艺美术的上品","tip":"「镂」金字旁，雕刻；不要写成「楼」（木字旁）"},
    {"w":"酌","py":"zhuó","q":"他们斟□着光和影，摄成称心满意的照片","tip":"「酌」酉字旁，考虑；不要写成「酌」以外的写法"},
    {"w":"漆","py":"qī","q":"梁和柱子以及门窗栏杆大多广□，那是不刺眼的颜色","tip":"「漆」三点水，涂料；不要写成「膝」（月字旁）"},
    {"w":"檐","py":"yán","q":"屋瓦和□漏一律淡灰色","tip":"「檐」木字旁，屋檐；不要写成「瞻」（目字旁）"},
    {"w":"蔓","py":"màn","q":"墙上□延着爬山虎或者蔷薇木香","tip":"「蔓」草字头，蔓草；不要写成「漫」（三点水）"},
    {"w":"芭","py":"bā","q":"给补上几竿竹子或几棵□蕉","tip":"「芭」草字头，芭蕉；不要写成「笆」（竹字头）"},
]

dict_notes = [
    {"w":"标本","a":"这里指典范、代表","q":"苏州园林是我国各地园林的标本"},
    {"w":"鉴赏","a":"鉴定和欣赏","q":"谁如果要鉴赏我国的园林"},
    {"w":"因地制宜","a":"根据不同地区的具体情况规定适宜的办法","q":"设计者和匠师们因地制宜"},
    {"w":"自出心裁","a":"出于自己的创造，指不抄袭、模仿别人","q":"自出心裁"},
    {"w":"亭台轩榭","a":"泛指园林中的各种建筑物","q":"讲究亭台轩榭的布局"},
    {"w":"败笔","a":"事情中做得不好的部分","q":"决不容许有欠美伤美的败笔"},
    {"w":"重峦叠嶂","a":"重重叠叠的山峰","q":"或者是重峦叠嶂"},
    {"w":"胸中有丘壑","a":"心中有山水风景的形象，指有深远的构思","q":"胸中有丘壑"},
    {"w":"雷同","a":"不该相同而相同","q":"那就一座一个样，决不雷同"},
    {"w":"玲珑","a":"精巧细致","q":"布置几块玲珑的石头"},
    {"w":"俯仰生姿","a":"高树低树相互呼应，形成优美姿态","q":"高树与低树俯仰生姿"},
    {"w":"嶙峋","a":"形容山石等突兀、重叠","q":"盘曲嶙峋的枝干"},
    {"w":"珠光宝气","a":"形容非常华丽，文中形容藤萝花繁盛艳丽","q":"满眼的珠光宝气"},
    {"w":"镂空","a":"在物体上雕刻出穿透物体的花纹","q":"墙壁上有砖砌的各式镂空图案"},
    {"w":"隔而不隔","a":"看似隔开了，实际上没有完全隔开","q":"实际是隔而不隔"},
    {"w":"界而未界","a":"看似划分了界限，实际上没有完全划清","q":"界而未界"},
    {"w":"雕镂","a":"雕刻","q":"图案设计和雕镂琢磨功夫"},
    {"w":"别具匠心","a":"另有一种巧妙的心思","q":"即使简朴而别具匠心"},
    {"w":"斟酌","a":"考虑是否适当","q":"他们斟酌着光和影"},
    {"w":"闲适","a":"清闲安逸","q":"引起人们安静闲适的感觉"},
    {"w":"明艳照眼","a":"鲜明美丽，耀眼夺目","q":"更显得各种花明艳照眼"},
    {"w":"作比较","a":"说明方法之一，通过对比突出事物特征","q":"苏州园林可绝不讲究对称"},
    {"w":"打比方","a":"说明方法之一，通过比喻介绍事物","q":"对称的建筑是图案画"},
    {"w":"分类别","a":"说明方法之一，按类别分别说明","q":"苏州园林里都有假山和池沼"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《苏州园林》叶圣陶</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 叶圣陶</div>
  <h1 class="hero-title">苏州园林</h1>
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
    <p>《苏州园林》是叶圣陶写的一篇事物说明文，选自《百科知识》。文章从游览者的角度，概括出苏州园林的共同特征——“务必使游览者无论站在哪个点上，眼前总是一幅完美的图画”，然后从布局、假山池沼、树木、花墙廊子、角落、门窗、色彩等方面具体说明，是中学说明文教学的经典篇目。</p>
    <p>全文采用总分结构，条理清晰，综合运用作比较、打比方、举例子、引用、摹状貌等多种说明方法，语言准确严密而又生动形象，体现了叶圣陶先生严谨而优美的文风。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>叶圣陶（1894—1988），原名叶绍钧，字秉臣，江苏苏州人，现代作家、教育家、出版家。1921年与沈雁冰、郑振铎等发起成立文学研究会。代表作有长篇小说《倪焕之》，童话集《稻草人》《古代英雄的石像》，散文集《脚步集》等。他也是语文教育的一代宗师，曾任人民教育出版社社长、教育部副部长等职。</p>
    <p style="margin-top:10px;color:var(--ink2)">叶圣陶的散文语言朴素自然、准确严密，善于用平实的文字说明复杂的事物。《苏州园林》写于1979年，是他为一本苏州园林摄影集写的序文，后被选入中学语文教材。</p>
  </div>
  <div class="box">
    <h3>苏州园林简介</h3>
    <p>苏州是中国著名的历史文化名城，有“园林之城”的美誉。苏州园林始于春秋时期，发展于唐宋，鼎盛于明清，现存有六十余处。其中拙政园、留园、网师园、环秀山庄等九座古典园林被联合国教科文组织列入《世界遗产名录》。</p>
    <p style="margin-top:8px">苏州园林以写意山水的高超艺术手法，蕴含浓厚的中国传统思想和文化内涵，是东方文明的造园艺术典范。其最大特点是“虽由人作，宛自天开”，在有限的空间里模拟自然山水，达到“一步一景”“移步换景”的效果。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文诵读《苏州园林》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1hQ4y1r7ox&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读苏州园林"></iframe>
        <a href="https://www.bilibili.com/video/BV1hQ4y1r7ox" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>花一年时间拍苏州园林</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1kMVz67Erh&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="花一年时间拍苏州园林"></iframe>
        <a href="https://www.bilibili.com/video/BV1kMVz67Erh" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">说明对象：苏州园林</div>
        <p>本文的说明对象是苏州园林。文章先总说苏州园林是我国园林的“标本”，然后点明其总体特征，再从七个方面分项说明，最后以简洁的语言收尾。说明对象明确，特征突出。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">总体特征：完美的图画</div>
        <p>文章第二段明确指出苏州园林的共同特征：“务必使游览者无论站在哪个点上，眼前总是一幅完美的图画。”下文的七个方面（布局、假山池沼、树木、花墙廊子、角落、门窗、色彩）都围绕这一特征展开，做到了“一切都要为构成完美的图画而存在”。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">作比较：突出苏州园林的独特</div>
        <p>“我国的建筑……绝大部分是对称的……苏州园林可绝不讲究对称”，以一般建筑的对称与苏州园林的不对称比较；“苏州园林与北京的园林不同，极少使用彩绘”，以北京园林的彩绘与苏州园林的淡雅比较。作比较使苏州园林的特点更加鲜明突出。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">打比方与引用：生动而典雅</div>
        <p>“对称的建筑是图案画，不是美术画，而园林是美术画”，以打比方说明园林追求自然之趣；“鱼戏莲叶间”引用汉乐府诗句，增添文学色彩；“胸中有丘壑”引用古语，说明设计者的修养。打比方和引用使说明生动而富有文化底蕴。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">举例子与摹状貌：具体而生动</div>
        <p>举例子：“东边有了一个亭子或者一道回廊，西边决不会来一个同样的亭子”“阶砌旁边栽几丛书带草”等，使说明具体可感；摹状貌：“盘曲嶙峋的枝干”“满眼的珠光宝气”“高低屈曲任其自然”，生动地写出了园林景物的形态和美感。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">分类别与列数字：条理清晰</div>
        <p>分类别：将苏州园林的特点分为布局、假山池沼、树木、花墙廊子、角落、门窗、色彩七个方面，条理清晰；列数字：“一百多处”“十多处”“四扇，八扇，十二扇”，用数字使说明更精确。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明顺序</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">整体：逻辑顺序（总分结构）</div>
        <p>文章采用总分结构：第一、二段总说苏州园林的地位和总体特征，第三至九段从七个方面分项说明，第十段收尾。分项说明时按由主到次的逻辑顺序（从整体布局到局部细节，从大处到小处），条理清晰，层次分明。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">局部：从概括到具体</div>
        <p>每个分项内部也遵循从概括到具体的逻辑顺序。如写假山池沼，先总说“假山的堆叠，可以说是一项艺术而不仅是技术”，再具体说明假山的形态和池沼的布置；写花草树木，先总说“也着眼在画意”，再具体说明高低错落、四季有景等特点。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明语言的准确性</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">修饰限制词的运用</div>
        <p>“据说有一百多处”“不过十多处”“绝大部分是对称的”“大多引用活水”“往往安排桥梁”“极少使用彩绘”“大多漆广漆”——“据说”“不过”“绝大部分”“大多”“往往”“极少”等修饰限制词，准确地反映了客观实际，体现了说明文语言的准确性和严密性。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">准确与生动的统一</div>
        <p>本文语言既准确严密，又生动形象。“隔而不隔，界而未界”用语精炼，准确概括了花墙廊子的设计妙处；“俯仰生姿”“珠光宝气”“明艳照眼”等词语生动优美，使说明文具有了文学色彩。叶圣陶的语言风格正是“平实中见功力，准确中见生动”。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《苏州园林》通过介绍苏州园林的总体特征和各方面特点，展现了苏州园林的建筑艺术美，歌颂了我国劳动人民的智慧和创造力，表达了对苏州园林的赞美和对中国传统园林艺术的自豪。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 说明术语 · 用字 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">标本</span><span class="acc-d">这里指典范、代表。</span></div>
      <div class="acc-item"><span class="acc-w">鉴赏</span><span class="acc-d">鉴定和欣赏（艺术品、文物等）。</span></div>
      <div class="acc-item"><span class="acc-w">因地制宜</span><span class="acc-d">根据不同地区的具体情况规定适宜的办法。</span></div>
      <div class="acc-item"><span class="acc-w">自出心裁</span><span class="acc-d">出于自己的创造，指不抄袭、模仿别人。</span></div>
      <div class="acc-item"><span class="acc-w">亭台轩榭</span><span class="acc-d">（xuān xiè）泛指园林中的各种建筑物。</span></div>
      <div class="acc-item"><span class="acc-w">败笔</span><span class="acc-d">写字写得不好的一笔，引申为事情中做得不好的部分。</span></div>
      <div class="acc-item"><span class="acc-w">重峦叠嶂</span><span class="acc-d">（zhàng）重重叠叠的山峰。</span></div>
      <div class="acc-item"><span class="acc-w">胸中有丘壑</span><span class="acc-d">（hè）心中有山水风景的形象，指有深远的构思。</span></div>
      <div class="acc-item"><span class="acc-w">雷同</span><span class="acc-d">不该相同而相同。</span></div>
      <div class="acc-item"><span class="acc-w">俯仰生姿</span><span class="acc-d">高树低树相互呼应，形成优美姿态。</span></div>
      <div class="acc-item"><span class="acc-w">嶙峋</span><span class="acc-d">（lín xún）形容山石等突兀、重叠。</span></div>
      <div class="acc-item"><span class="acc-w">珠光宝气</span><span class="acc-d">形容非常华丽，文中形容藤萝花繁盛艳丽。</span></div>
      <div class="acc-item"><span class="acc-w">镂空</span><span class="acc-d">在物体上雕刻出穿透物体的花纹或文字。</span></div>
      <div class="acc-item"><span class="acc-w">隔而不隔</span><span class="acc-d">看似隔开了，实际上没有完全隔开。</span></div>
      <div class="acc-item"><span class="acc-w">别具匠心</span><span class="acc-d">另有一种巧妙的心思。</span></div>
      <div class="acc-item"><span class="acc-w">闲适</span><span class="acc-d">清闲安逸。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>说明文术语</h3>
      <div class="acc-item"><span class="acc-w">说明对象</span><span class="acc-d">文章要说明的事物。本文的说明对象是苏州园林。</span></div>
      <div class="acc-item"><span class="acc-w">说明特征</span><span class="acc-d">说明对象区别于其他事物的标志。本文的特征是“务必使游览者眼前总是一幅完美的图画”。</span></div>
      <div class="acc-item"><span class="acc-w">作比较</span><span class="acc-d">说明方法之一，通过对比突出事物特征。如苏州园林与一般建筑、北京园林的比较。</span></div>
      <div class="acc-item"><span class="acc-w">打比方</span><span class="acc-d">说明方法之一，通过比喻介绍事物。如“对称的建筑是图案画，园林是美术画”。</span></div>
      <div class="acc-item"><span class="acc-w">分类别</span><span class="acc-d">说明方法之一，按类别分别说明。本文从七个方面分类说明苏州园林。</span></div>
      <div class="acc-item"><span class="acc-w">举例子</span><span class="acc-d">说明方法之一，举出实际事例使说明更具体。如阶砌旁栽草、窗前补竹蕉。</span></div>
      <div class="acc-item"><span class="acc-w">摹状貌</span><span class="acc-d">说明方法之一，对事物的形态进行描写。如“盘曲嶙峋的枝干”。</span></div>
      <div class="acc-item"><span class="acc-w">引用</span><span class="acc-d">说明方法之一，引用资料、诗句等。如“鱼戏莲叶间”。</span></div>
      <div class="acc-item"><span class="acc-w">总分结构</span><span class="acc-d">先总说特征，再分项说明的结构方式。本文采用总分结构。</span></div>
      <div class="acc-item"><span class="acc-w">逻辑顺序</span><span class="acc-d">按照事物的内在逻辑关系安排说明顺序。本文按由主到次的逻辑顺序说明。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">鉴赏</span><span class="acc-d">（jiàn）金字旁；与「签」（竹字头）区分。</span></div>
      <div class="acc-item"><span class="acc-w">轩榭</span><span class="acc-d">（xiè）木字旁，建筑在台上的房屋；生僻字。</span></div>
      <div class="acc-item"><span class="acc-w">池沼</span><span class="acc-d">（zhǎo）三点水，水池；与「诏」（言字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">重峦叠嶂</span><span class="acc-d">（zhàng）山字旁；与「障」（左耳旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">丘壑</span><span class="acc-d">（hè）土字头，山沟；生僻字。</span></div>
      <div class="acc-item"><span class="acc-w">嶙峋</span><span class="acc-d">（lín xún）山字旁；与「鳞」「询」区分。</span></div>
      <div class="acc-item"><span class="acc-w">雕镂</span><span class="acc-d">（lòu）金字旁，雕刻；与「楼」（木字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">斟酌</span><span class="acc-d">（zhuó）酉字旁，考虑；注意右边是「酉」不是「西」。</span></div>
      <div class="acc-item"><span class="acc-w">广漆</span><span class="acc-d">（qī）三点水，涂料；与「膝」（xī，月字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">屋檐</span><span class="acc-d">（yán）木字旁；与「瞻」（zhān，目字旁）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">抓住特征</span><span class="acc-d">全文围绕“完美的图画”这一总体特征展开，七个方面都紧扣特征，中心明确。</span></div>
      <div class="acc-item"><span class="acc-w">总分结构</span><span class="acc-d">先总说特征，再从七个方面分项说明，条理清晰，层次分明。</span></div>
      <div class="acc-item"><span class="acc-w">方法多样</span><span class="acc-d">综合运用作比较、打比方、举例子、分类别、引用、摹状貌等多种说明方法。</span></div>
      <div class="acc-item"><span class="acc-w">语言准确生动</span><span class="acc-d">大量使用修饰限制词体现准确性，同时运用生动的描写和典雅的引用，做到准确与生动的统一。</span></div>
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
  <div class="kai">《苏州园林》</div>
  <div>叶圣陶 · 现代 · 出自《百科知识》</div>
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
