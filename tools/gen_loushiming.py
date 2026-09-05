# -*- coding: utf-8 -*-
"""《陋室铭》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。
中文引号用 ~L~ / ~R~ 占位，生成前替换为 \\u201c / \\u201d。
拼音必须放在注释 data-note 里，原文保持纯净：[[词|（拼音）释义]]"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'loushiming-liuyuxi.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'loushiming_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "山不在高，有仙则名。",
    "水不在深，有龙则灵。",
    "斯是陋室，惟吾德馨。",
    "苔痕上阶绿，草色入帘青。",
    "谈笑有鸿儒，往来无白丁。",
    "可以调素琴，阅金经。",
    "无丝竹之乱耳，无案牍之劳形。",
    "南阳诸葛庐，西蜀子云亭。",
    "孔子云：何陋之有？",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "起兴立意 · 惟吾德馨", "第 1–3 句",
     "以山水起兴，引出陋室。山以仙名，水以龙灵，陋室则以吾德馨——点出全文主旨：陋室不陋，贵在德馨。"),
    ("第二部分", "陋室生活 · 清雅脱俗", "第 4–7 句",
     "从环境、交往、日常生活三个层面，描绘陋室中的清雅生活。苔痕草色见其幽，鸿儒白丁见其雅，素琴金经见其闲，无丝竹案牍见其静。"),
    ("第三部分", "类比收束 · 何陋之有", "第 8–9 句",
     "以诸葛庐、子云亭类比陋室，引孔子之言作结，反问有力，余味悠长，把~L~陋室不陋~R~的主旨推向极致。"),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
(0, "山不[[在|在于，取决于]]高，有[[仙|仙人，神仙]][[则|就，便，连词]][[名|（míng）名词作动词，出名，有名]]。",
 "山不在于高，有了仙人就出名了。",
 fixq("以山水起兴，开篇即破题。~L~山不在高~R~一反常理——山的价值不在高峻，而在有无仙人；为下文~L~陋室不陋~R~蓄势。~L~名~R~字名词作动词，精炼传神。"),
 ["起兴", "词类活用"]),

(0, "水不[[在|在于，取决于]][[深|（shēn）水深]]，有[[龙|传说中能兴云作雨的神异动物]]则[[灵|（líng）形容词作动词，显出灵异，有灵气]]。",
 "水不在于深，有了龙就显出灵异了。",
 fixq("承上句，以水龙对山仙，对仗工整。山因仙而名，水因龙而灵——物的价值不在其形，而在其神。两句排比，为~L~斯是陋室，惟吾德馨~R~作铺垫，陋室因吾德而不陋。"),
 ["对仗", "起兴", "词类活用"]),

(0, "[[斯|（sī）这，这个，指示代词]][[是|判断动词，是]][[陋室|简陋的屋子。陋，简陋]]，[[惟|只，只是]][[吾|（wú）我，第一人称代词]][[德馨|（xīn）品德高尚。馨，香气，这里指品德高尚]]。",
 "这是简陋的屋子，只是我的品德高尚（就不觉得简陋了）。",
 fixq("全文主旨句。前两句山水起兴，此句点题——陋室不陋，全在德馨。~L~斯是陋室~R~先抑，~L~惟吾德馨~R~后扬，一抑一扬之间，把个人品德置于物质条件之上。~L~馨~R~字以香气喻美德，是全文的文眼。"),
 ["主旨句", "判断句", "文眼"]),

(1, "[[苔痕|（tái hén）苔藓的痕迹。苔，苔藓；痕，痕迹]][[上|（shàng）名词作动词，蔓延到，长到]][[阶|台阶]][[绿|（lǜ）形容词作动词，变绿，使台阶染上绿色]]，[[草色|草的颜色，指青草]][[入|映入，进入]][[帘|门帘，窗帘]][[青|（qīng）形容词作动词，青翠，使帘映上青色]]。",
 "苔藓的痕迹蔓延到台阶上，使台阶都绿了；草色映入竹帘，使室内染上了青色。",
 fixq("写陋室环境，一句一景，色彩鲜明。~L~上~R~~L~入~R~二字化静为动，把苔痕草色写得有情有意，仿佛主动来装点陋室。~L~绿~R~~L~青~R~二色，清幽淡雅，见出陋室的生机与雅致，也暗示主人的高洁。"),
 ["写景", "炼字", "词类活用"]),

(1, "[[谈笑|说说笑笑，指交往谈笑]]有[[鸿儒|（rú）博学的人。鸿，大；儒，读书人]]，[[往来|来来往往，指交往的人]]无[[白丁|平民，这里指没有功名的人，即没有学问的人]]。",
 "在这里谈笑的都是博学的人，来来往往的没有无学问的人。",
 fixq("写陋室交往，以~L~有~R~~L~无~R~对举。鸿儒满堂，白丁不至——从交往之人的雅俗，反衬主人的学识与品位。~L~鸿儒~R~与~L~白丁~R~对比鲜明，见出陋室虽陋，往来皆贤，是~L~德馨~R~的又一佐证。"),
 ["对比", "写人"]),

(1, "可以[[调|（tiáo）调弄，这里指弹奏]][[素琴|不加装饰的琴。素，朴素，不加装饰]]，[[阅|阅读，这里指翻阅]][[金经|指佛经（古时用泥金书写的佛经）]]。",
 "可以弹奏不加装饰的琴，翻阅佛经。",
 fixq("写陋室日常生活。~L~调素琴~R~见其高雅，~L~阅金经~R~见其沉静。素琴无华，金经无声——没有世俗的喧嚣，只有内心的安宁。两句极写陋室生活的闲适与超脱，与下文~L~无丝竹之乱耳，无案牍之劳形~R~正反呼应。"),
 ["写生活", "正反呼应"]),

(1, "无[[丝竹|琴瑟箫笛等乐器的总称，这里指奏乐的声音。丝，弦乐器；竹，管乐器]][[之|用于主谓之间，取消句子独立性，无实义]][[乱|（luàn）形容词的使动用法，使……扰乱]][[耳|耳朵，这里指听觉]]，无[[案牍|（dú）官府的公文。案，文书；牍，古代写字用的木片]][[之|用于主谓之间，取消句子独立性，无实义]][[劳|（láo）形容词的使动用法，使……劳累]][[形|形体，身体]]。",
 "没有奏乐的声音扰乱耳朵，没有官府的公文使身体劳累。",
 fixq("从反面写陋室之乐。~L~无丝竹之乱耳~R~写无世俗喧嚣，~L~无案牍之劳形~R~写无公务缠身。两个~L~无~R~字，斩钉截铁，见出主人远离尘嚣、安贫乐道的境界。~L~乱~R~~L~劳~R~皆使动用法，精炼有力。此句与上句~L~可以调素琴，阅金经~R~一正一反，把陋室生活的清雅写足。"),
 ["使动用法", "对比", "反面写"]),

(2, "[[南阳|地名，今河南南阳一带]][[诸葛庐|诸葛亮隐居时的草庐。诸葛亮，字孔明，三国时蜀汉丞相]]，[[西蜀|（shǔ）地名，今四川西部]][[子云亭|扬雄的亭子。扬雄，字子云，西汉文学家]]。",
 "（它好比）南阳诸葛亮的草庐，西蜀扬子云的亭子。",
 fixq("以古人之居类比陋室。诸葛庐、子云亭皆简陋，但其主人皆名垂青史——陋室不陋，全在其人。以古贤自比，既见出作者的自信与抱负，也为下文引孔子之言~L~何陋之有~R~张本。"),
 ["用典", "类比", "自比"]),

(2, "[[孔子|名丘，字仲尼，春秋时鲁国人，儒家学派创始人]][[云|说]]：[[何|什么，疑问代词]][[陋|简陋]][[之|宾语前置的标志，无实义]][[有|有（什么简陋的呢）]]？",
 "孔子说：有什么简陋的呢？",
 fixq("引孔子之言收束全文，反问有力。~L~何陋之有~R~是宾语前置句，正常语序为~L~有何陋~R~。以圣人之言为全文作结，既呼应开头~L~惟吾德馨~R~的主旨，又把陋室不陋的道理提升到儒家安贫乐道的高度，余味无穷。"),
 ["引用", "宾语前置", "收束"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"馨","py":"xīn","q":"惟吾德□","tip":fixq("「馨」香字底，音 xīn，意为香气，喻品德高尚，勿写~L~罄~R~~L~磬~R~")},
    {"w":"苔","py":"tái","q":"□痕上阶绿","tip":fixq("「苔」草字头，音 tái，意为苔藓，勿写~L~台~R~~L~抬~R~")},
    {"w":"痕","py":"hén","q":"苔□上阶绿","tip":fixq("「痕」疒字头，音 hén，意为痕迹，勿写~L~很~R~~L~狠~R~")},
    {"w":"儒","py":"rú","q":"谈笑有鸿□","tip":fixq("「儒」单人旁，音 rú，意为读书人，勿写~L~孺~R~~L~懦~R~")},
    {"w":"牍","py":"dú","q":"无案□之劳形","tip":fixq("「牍」片字旁，音 dú，意为古代写字木片，勿写~L~椟~R~~L~犊~R~")},
    {"w":"蜀","py":"shǔ","q":"西□子云亭","tip":fixq("「蜀」四字头，音 shǔ，四川别称，勿写~L~属~R~")},
    {"w":"陋","py":"lòu","q":"斯是□室","tip":fixq("「陋」左耳旁，音 lòu，意为简陋，勿写~L~漏~R~")},
    {"w":"惟","py":"wéi","q":"□吾德馨","tip":fixq("「惟」竖心旁，音 wéi，意为只，勿写~L~唯~R~~L~维~R~")},
    {"w":"调","py":"tiáo","q":"可以□素琴","tip":fixq("「调」言字旁，此处读 tiáo，意为弹奏，勿读 diào")},
    {"w":"素","py":"sù","q":"可以调□琴","tip":fixq("「素」糸字底，音 sù，意为不加装饰，勿写~L~索~R~")},
    {"w":"阅","py":"yuè","q":"□金经","tip":fixq("「阅」门字框，音 yuè，意为阅读，勿写~L~悦~R~")},
    {"w":"阶","py":"jiē","q":"苔痕上□绿","tip":fixq("「阶」左耳旁，音 jiē，意为台阶，勿写~L~价~R~~L~皆~R~")},
    {"w":"帘","py":"lián","q":"草色入□青","tip":fixq("「帘」穴宝盖，音 lián，意为门帘，勿写~L~连~R~~L~莲~R~")},
    {"w":"鸿","py":"hóng","q":"谈笑有□儒","tip":fixq("「鸿」三点水，音 hóng，意为大，勿写~L~洪~R~~L~宏~R~")},
    {"w":"丁","py":"dīng","q":"往来无白□","tip":fixq("「丁」独体字，音 dīng，白丁指无学问的人，勿写~L~仃~R~")},
    {"w":"斯","py":"sī","q":"□是陋室","tip":fixq("「斯」斤字旁，音 sī，意为这，勿写~L~撕~R~~L~嘶~R~")},
    {"w":"吾","py":"wú","q":"惟□德馨","tip":fixq("「吾」口字底，音 wú，意为我，勿写~L~语~R~~L~梧~R~")},
    {"w":"劳","py":"láo","q":"无案牍之□形","tip":fixq("「劳」力字底，音 láo，使动用法~L~使……劳累~R~，勿写~L~牢~R~")},
    {"w":"乱","py":"luàn","q":"无丝竹之□耳","tip":fixq("「乱」舌字旁，音 luàn，使动用法~L~使……扰乱~R~，勿写~L~敌~R~")},
    {"w":"名","py":"míng","q":"有仙则□","tip":fixq("「名」口字底，音 míng，名词作动词~L~出名~R~，勿写~L~明~R~")},
    {"w":"灵","py":"líng","q":"有龙则□","tip":fixq("「灵」火字底，音 líng，形容词作动词~L~显出灵异~R~，勿写~L~零~R~")},
]

DICT_NOTES = [
    {"w":"在","q":"山不在高","a":"在于，取决于"},
    {"w":"仙","q":"有仙则名","a":"仙人，神仙"},
    {"w":"则","q":"有仙则名","a":"就，便，连词"},
    {"w":"名","q":"有仙则名","a":"（míng）名词作动词，出名，有名"},
    {"w":"深","q":"水不在深","a":"（shēn）水深"},
    {"w":"龙","q":"有龙则灵","a":"传说中能兴云作雨的神异动物"},
    {"w":"灵","q":"有龙则灵","a":"（líng）形容词作动词，显出灵异，有灵气"},
    {"w":"斯","q":"斯是陋室","a":"（sī）这，这个，指示代词"},
    {"w":"是","q":"斯是陋室","a":"判断动词，是"},
    {"w":"陋室","q":"斯是陋室","a":"简陋的屋子。陋，简陋"},
    {"w":"惟","q":"惟吾德馨","a":"只，只是"},
    {"w":"吾","q":"惟吾德馨","a":"（wú）我，第一人称代词"},
    {"w":"德馨","q":"惟吾德馨","a":"（xīn）品德高尚。馨，香气，这里指品德高尚"},
    {"w":"苔痕","q":"苔痕上阶绿","a":"（tái hén）苔藓的痕迹。苔，苔藓；痕，痕迹"},
    {"w":"上","q":"苔痕上阶绿","a":"（shàng）名词作动词，蔓延到，长到"},
    {"w":"阶","q":"苔痕上阶绿","a":"台阶"},
    {"w":"绿","q":"苔痕上阶绿","a":"（lǜ）形容词作动词，变绿，使台阶染上绿色"},
    {"w":"草色","q":"草色入帘青","a":"草的颜色，指青草"},
    {"w":"入","q":"草色入帘青","a":"映入，进入"},
    {"w":"帘","q":"草色入帘青","a":"门帘，窗帘"},
    {"w":"青","q":"草色入帘青","a":"（qīng）形容词作动词，青翠，使帘映上青色"},
    {"w":"谈笑","q":"谈笑有鸿儒","a":"说说笑笑，指交往谈笑"},
    {"w":"鸿儒","q":"谈笑有鸿儒","a":"（rú）博学的人。鸿，大；儒，读书人"},
    {"w":"往来","q":"往来无白丁","a":"来来往往，指交往的人"},
    {"w":"白丁","q":"往来无白丁","a":"平民，这里指没有功名的人，即没有学问的人"},
    {"w":"可以","q":"可以调素琴","a":"可以用来。可，可以；以，用来"},
    {"w":"调","q":"可以调素琴","a":"（tiáo）调弄，这里指弹奏"},
    {"w":"素琴","q":"可以调素琴","a":"不加装饰的琴。素，朴素，不加装饰"},
    {"w":"阅","q":"阅金经","a":"阅读，这里指翻阅"},
    {"w":"金经","q":"阅金经","a":"指佛经（古时用泥金书写的佛经）"},
    {"w":"丝竹","q":"无丝竹之乱耳","a":"琴瑟箫笛等乐器的总称，这里指奏乐的声音。丝，弦乐器；竹，管乐器"},
    {"w":"之","q":"无丝竹之乱耳","a":"用于主谓之间，取消句子独立性，无实义"},
    {"w":"乱","q":"无丝竹之乱耳","a":"（luàn）形容词的使动用法，使……扰乱"},
    {"w":"耳","q":"无丝竹之乱耳","a":"耳朵，这里指听觉"},
    {"w":"案牍","q":"无案牍之劳形","a":"（dú）官府的公文。案，文书；牍，古代写字用的木片"},
    {"w":"劳","q":"无案牍之劳形","a":"（láo）形容词的使动用法，使……劳累"},
    {"w":"形","q":"无案牍之劳形","a":"形体，身体"},
    {"w":"南阳","q":"南阳诸葛庐","a":"地名，今河南南阳一带"},
    {"w":"诸葛庐","q":"南阳诸葛庐","a":"诸葛亮隐居时的草庐。诸葛亮，字孔明，三国时蜀汉丞相"},
    {"w":"西蜀","q":"西蜀子云亭","a":"（shǔ）地名，今四川西部"},
    {"w":"子云亭","q":"西蜀子云亭","a":"扬雄的亭子。扬雄，字子云，西汉文学家"},
    {"w":"孔子","q":"孔子云：何陋之有","a":"名丘，字仲尼，春秋时鲁国人，儒家学派创始人"},
    {"w":"云","q":"孔子云：何陋之有","a":"说"},
    {"w":"何","q":"何陋之有","a":"什么，疑问代词"},
    {"w":"陋","q":"何陋之有","a":"简陋"},
    {"w":"之","q":"何陋之有","a":"宾语前置的标志，无实义"},
    {"w":"有","q":"何陋之有","a":"有（什么简陋的呢）"},
]


# ---------------- 组装 ----------------
def build_verses():
    out, idx = [], 0
    for pi, part in enumerate(PARTS):
        out.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>'
                   % (part[0], part[1], part[2]))
        out.append('      <div class="part-overview">%s</div>' % fixq(part[3]))
        for (p, txt, yi, shang, tags) in S:
            if p != pi:
                continue
            idx += 1
            out.append('      <div class="verse" id="l%d" data-i="%d">' % (idx, idx - 1))
            out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx, annotate(txt)))
            out.append('        <details class="v-more">')
            out.append('          <summary>译文 · 赏析</summary>')
            out.append('          <div class="d-body">')
            out.append('            <div class="v-sec"><b class="v-label">译　文</b>')
            out.append('              <div class="v-trans">%s</div>' % yi)
            out.append('            </div>')
            out.append('            <div class="v-sec"><b class="v-label">赏　析</b>')
            out.append('              <div class="d-body"><p>%s</p></div>' % shang)
            if tags:
                out.append('              <div class="tags">%s</div>' % ''.join('<span>%s</span>' % t for t in tags))
            out.append('            </div>')
            out.append('          </div>')
            out.append('        </details>')
            out.append('      </div>')
    return '\n'.join(out), idx


verses_html, total = build_verses()
full_html = '\n'.join('    <div class="pl">%s</div>' % p for p in FULLTEXT)

anno_count = sum(txt.count('[[') for (_, txt, _, _, _) in S)

BG = fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《陋室铭》是唐代文学家刘禹锡的一篇托物言志的骈体铭文，全文仅八十一字，却以凝练的笔墨、精巧的构思，成为中国文学史上咏物散文的经典。</p>
    <p>文章以陋室为喻，通过对陋室环境、交往和日常生活的描绘，表达了作者不慕名利、安贫乐道的人生态度，也暗含了对世俗追逐富贵的鄙弃。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>刘禹锡（772—842），字梦得，洛阳（今河南洛阳）人，唐代著名文学家、哲学家，有~L~诗豪~R~之称。贞元九年进士，官至监察御史。因参与王叔文政治革新失败，被贬朗州司马，后又历任连州、夔州、和州刺史。</p>
    <p>刘禹锡诗文俱佳，与柳宗元并称~L~刘柳~R~，与白居易并称~L~刘白~R~。其诗风爽朗明快，善用比兴寄托，代表作有《竹枝词》《乌衣巷》《酬乐天扬州初逢席上见赠》等。散文以《陋室铭》最为著名。</p>
    <p class="note">※ 刘禹锡性格刚毅，虽屡遭贬谪而不改其志，白居易赞其~L~诗豪者也，其锋森然，少敢当者~R~。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>写作缘起：</b>刘禹锡被贬和州（今安徽和县）任刺史时，和州知县故意刁难，先安排他住城南临江的三间小屋，后又迁至城北一间半，最后逼他住进县城里一间仅能容一床一桌的斗室。刘禹锡不以为意，反而写下这篇《陋室铭》，请人刻于石碑，立于门前。</p>
    <p><b>中唐文风：</b>中唐时期，古文运动兴起，韩愈、柳宗元倡导文以载道，反对骈文浮华。刘禹锡虽以诗名世，但其散文也深受古文运动影响，《陋室铭》虽用骈句，却内容充实、立意高远，是骈散结合的佳作。</p>
    <p><b>社会风气：</b>中唐以后，社会动荡，士大夫阶层多追求物质享受。刘禹锡以~L~陋室~R~自守，表达了对安贫乐道精神的坚守，也是对当时世风的一种无声批判。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>~L~铭~R~是古代刻在器物上用来警戒自己或称述功德的文字，后来发展为一种文体。铭文一般用韵，篇幅短小，语言精炼，多采用托物言志的手法。《陋室铭》就是铭文的典范之作，全文押~L~ing~R~韵（名、灵、馨、青、丁、经、形、亭），节奏铿锵，朗朗上口。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>任志宏朗诵《陋室铭》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1bt411e7b2&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="任志宏朗诵《陋室铭》"></iframe>
        <a href="https://www.bilibili.com/video/BV1bt411e7b2" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>F.Be.I音乐团队古风歌曲《陋室铭》</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1wx411m7ef&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="F.Be.I音乐团队《陋室铭》"></iframe>
        <a href="https://www.bilibili.com/video/BV1wx411m7ef" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>抒情主人公形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">安贫乐道的高洁之士</div>
        <p>文中的~L~吾~R~，是一位安贫乐道、高洁傲岸的隐士形象。他身居陋室，却不以为陋——因为他有~L~德馨~R~。他的生活是清雅的：苔痕草色装点门庭，鸿儒硕学往来谈笑，素琴金经相伴左右，没有丝竹的喧嚣，没有案牍的劳形。他以诸葛亮、扬雄自比，引孔子之言自励，见出其虽处逆境而不改其志的刚毅品格。这个形象，正是刘禹锡自身的写照——屡遭贬谪，却始终坚守内心的高洁与从容。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">托物言志，物我合一</div>
        <p>全文以陋室为喻，句句写陋室，又句句写人。陋室的~L~苔痕上阶绿~R~即主人的清幽之趣，~L~谈笑有鸿儒~R~即主人的学识之雅，~L~可以调素琴，阅金经~R~即主人的生活之闲，~L~无丝竹之乱耳，无案牍之劳形~R~即主人的心境之静。物与志高度统一，陋室的形象就是作者人格理想的化身。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">起兴类比，层层铺垫</div>
        <p>文章以~L~山不在高，有仙则名。水不在深，有龙则灵~R~起兴，引出~L~斯是陋室，惟吾德馨~R~的主旨——山以仙名，水以龙灵，陋室以吾德馨。结尾又以诸葛庐、子云亭类比陋室，引孔子~L~何陋之有~R~作结。起兴与类比首尾呼应，把~L~陋室不陋~R~的道理层层推进，最后以圣人之言一锤定音。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">骈散结合，音韵铿锵</div>
        <p>文章以骈句为主，对偶工整，如~L~苔痕上阶绿，草色入帘青~R~~L~谈笑有鸿儒，往来无白丁~R~~L~无丝竹之乱耳，无案牍之劳形~R~，节奏整齐，音韵和谐。全文押~L~ing~R~韵（名、灵、馨、青、丁、经、形、亭），读来朗朗上口。结尾~L~何陋之有~R~用散句反问，打破骈句的整齐，使文章既有整饬之美，又有灵动之势。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">虚实相生，正反对照</div>
        <p>文章写陋室，实写环境、交往、日常生活，虚写主人的品德与心境。~L~可以调素琴，阅金经~R~是正面写陋室之乐，~L~无丝竹之乱耳，无案牍之劳形~R~是反面写陋室之幸，一正一反，把陋室生活的清雅与超脱写足。虚实相生，正反对照，使文章内涵丰富，余味悠长。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">斯是陋室，惟吾德馨。</div>
        <p>全文主旨句，也是文眼所在。前两句山水起兴，此句点题——陋室不陋，全在德馨。~L~斯是陋室~R~先承认其陋，~L~惟吾德馨~R~再翻出不陋，一抑一扬之间，把个人品德置于物质条件之上。~L~馨~R~字以香气喻美德，既写出品德的芬芳远播，又与陋室的清幽环境相呼应，是全文最精炼传神的一笔。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">苔痕上阶绿，草色入帘青。</div>
        <p>写陋室环境的名句。~L~上~R~~L~入~R~二字化静为动，把苔痕草色写得有情有意，仿佛主动来装点陋室。~L~绿~R~~L~青~R~二色，清幽淡雅，见出陋室的生机与雅致。这一句不写陋室之陋，反写陋室之美——以自然之美衬主人之雅，是典型的以景写人手法。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">孔子云：何陋之有？</div>
        <p>全文收束句，以孔子之言作结，反问有力。~L~何陋之有~R~是宾语前置句，正常语序为~L~有何陋~R~。引圣人之言，既呼应开头~L~惟吾德馨~R~的主旨，又把陋室不陋的道理提升到儒家安贫乐道的高度。以反问作结，不答而答，余味无穷，使文章的立意达到最高点。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《陋室铭》通过对陋室环境、交往和日常生活的描绘，表达了作者不慕名利、安贫乐道的人生态度，以及对高洁品格的坚守和对世俗追逐富贵的鄙弃。</p>
    <p>文章的深刻之处，在于它不是简单地赞美陋室，而是借陋室的形象寄托了作者的人格理想。在作者看来，居室的价值不在其豪华，而在其主人的品德——山以仙名，水以龙灵，陋室以吾德馨。结尾引孔子~L~何陋之有~R~，把个人的安贫乐道提升到儒家精神的高度，使文章的主题超越了个人志趣，具有普遍的文化意义。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 词类活用 · 句式 · 文化常识</span></div>

  <div class="box">
    <h3>通假字</h3>
    <div class="tw"><table>
      <tr><th>字</th><th>通假</th><th>例句</th><th>释义</th></tr>
      <tr><td class="kai">（本文无通假字）</td><td>—</td><td>—</td><td>《陋室铭》全文无通假字</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">馨</td><td>香气，这里指品德高尚</td><td>芳香（多指气味）</td><td>惟吾德馨</td></tr>
      <tr><td class="kai">可以</td><td>可以用来。可，可以；以，用来</td><td>表示许可或能够</td><td>可以调素琴</td></tr>
      <tr><td class="kai">丝竹</td><td>琴瑟箫笛等乐器，这里指奏乐的声音</td><td>丝绸和竹子</td><td>无丝竹之乱耳</td></tr>
      <tr><td class="kai">白丁</td><td>没有功名的人，即没有学问的人</td><td>平民（中性）</td><td>往来无白丁</td></tr>
      <tr><td class="kai">形</td><td>形体，身体</td><td>形状，样子</td><td>无案牍之劳形</td></tr>
      <tr><td class="kai">调</td><td>调弄，这里指弹奏（读 tiáo）</td><td>调节，调动（读 diào）</td><td>可以调素琴</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>词类活用</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">名</td><td>名词作动词</td><td>出名，有名</td><td>有仙则名</td></tr>
      <tr><td class="kai">灵</td><td>形容词作动词</td><td>显出灵异，有灵气</td><td>有龙则灵</td></tr>
      <tr><td class="kai">馨</td><td>形容词作动词</td><td>品德高尚（以香气喻美德）</td><td>惟吾德馨</td></tr>
      <tr><td class="kai">上</td><td>名词作动词</td><td>蔓延到，长到</td><td>苔痕上阶绿</td></tr>
      <tr><td class="kai">绿</td><td>形容词作动词</td><td>变绿，使台阶染上绿色</td><td>苔痕上阶绿</td></tr>
      <tr><td class="kai">青</td><td>形容词作动词</td><td>青翠，使帘映上青色</td><td>草色入帘青</td></tr>
      <tr><td class="kai">乱</td><td>形容词的使动用法</td><td>使……扰乱</td><td>无丝竹之乱耳</td></tr>
      <tr><td class="kai">劳</td><td>形容词的使动用法</td><td>使……劳累</td><td>无案牍之劳形</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">判断句</td><td>斯是陋室</td><td>~L~是~R~表判断，是文言判断句的一种形式</td></tr>
      <tr><td class="kai">宾语前置</td><td>何陋之有</td><td>~L~之~R~是宾语前置的标志，正常语序为~L~有何陋~R~</td></tr>
      <tr><td class="kai">反问句</td><td>何陋之有？</td><td>以反问加强语气，收束全文</td></tr>
      <tr><td class="kai">省略句</td><td>（予）可以调素琴</td><td>承前省略主语~L~予~R~（我）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>一词多义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="3">之</td><td>用于主谓之间，取消句子独立性</td><td>无丝竹之乱耳</td></tr>
      <tr><td>宾语前置的标志</td><td>何陋之有</td></tr>
      <tr><td>的，结构助词</td><td>水陆草木之花（《爱莲说》）</td></tr>
      <tr><td class="kai" rowspan="2">则</td><td>就，便，连词</td><td>有仙则名</td></tr>
      <tr><td>那么（表假设）</td><td>则汉室之隆（《出师表》）</td></tr>
      <tr><td class="kai" rowspan="2">是</td><td>判断动词，是</td><td>斯是陋室</td></tr>
      <tr><td>这，指示代词</td><td>是马也（《马说》）</td></tr>
      <tr><td class="kai" rowspan="2">名</td><td>名词作动词，出名</td><td>有仙则名</td></tr>
      <tr><td>名字，名称</td><td>名之者谁（《醉翁亭记》）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>~L~铭~R~文体</dt><dd>古代刻在器物上用来警戒自己或称述功德的文字，后来发展为一种文体。铭文一般用韵，篇幅短小，语言精炼。如《陋室铭》《柳子厚墓志铭》等。</dd></div>
      <div class="g-item"><dt>诸葛庐</dt><dd>诸葛亮隐居南阳时的草庐。诸葛亮（181—234），字孔明，三国时蜀汉丞相，杰出的政治家、军事家。隐居时被刘备三顾茅庐，请出山辅佐。</dd></div>
      <div class="g-item"><dt>子云亭</dt><dd>扬雄的亭子。扬雄（前53—18），字子云，西汉著名文学家、哲学家，蜀郡成都人。少好学，长于辞赋，著有《太玄》《法言》等。其故居在成都，后人建亭纪念。</dd></div>
      <div class="g-item"><dt>丝竹</dt><dd>琴瑟箫笛等乐器的总称。丝，指弦乐器（琴、瑟等）；竹，指管乐器（箫、笛等）。文中代指奏乐的声音，引申为世俗的娱乐喧嚣。</dd></div>
      <div class="g-item"><dt>案牍</dt><dd>官府的公文。案，文书；牍，古代写字用的木片。~L~案牍劳形~R~指因处理公务而使身体劳累，后成为成语。</dd></div>
      <div class="g-item"><dt>白丁</dt><dd>平民，没有功名的人。古代平民穿白衣，故称~L~白丁~R~。文中指没有学问的人，与~L~鸿儒~R~对举。</dd></div>
      <div class="g-item"><dt>鸿儒</dt><dd>博学的人。鸿，大；儒，读书人。~L~鸿儒~R~指学识渊博的学者，与~L~白丁~R~形成对比。</dd></div>
      <div class="g-item"><dt>金经</dt><dd>指用泥金书写的佛经。泥金是一种用金箔和胶水制成的金色颜料，古人用以抄写佛经，以示虔诚。也有解释为《金刚经》的简称。</dd></div>
      <div class="g-item"><dt>素琴</dt><dd>不加装饰的琴。素，朴素，不加装饰。陶渊明有~L~但识琴中趣，何劳弦上声~R~的佳话，素琴象征高雅脱俗的情趣。</dd></div>
      <div class="g-item"><dt>托物言志</dt><dd>通过对物品的描写和叙述，表达自己的志向和意愿的写作手法。《陋室铭》是托物言志的典范，借陋室的形象表达作者安贫乐道的人格理想。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《陋室铭》刘禹锡</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">唐 · 刘禹锡</div>
  <h1 class="hero-title">陋室铭</h1>
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
        <option value="100">100%%</option>
        <option value="150">150%%</option>
        <option value="200">200%%</option>
        <option value="250">250%%</option>
        <option value="300">300%%</option>
      </select>
      <button id="btnAll">展开</button>
      <button id="btnRecite">背诵</button>
      <button id="btnPrint">打印</button>
    </div>
  </div>
</nav>

<main class="wrap">
%(bg)s

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>
  <div class="sec-sub">全文八十一字，分三部分：起兴立意、陋室生活、类比收束。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《陋室铭》</div>
  <div>刘禹锡 · 唐（772—842）· 字梦得，世称~L~诗豪~R~</div>
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
''' % {
    'css': CSS,
    'js': JS,
    'bg': BG,
    'app': APP,
    'acc': ACC,
    'fulltext': full_html,
    'verses': verses_html,
    'words': json.dumps(DICT_WORDS, ensure_ascii=False),
    'notes': json.dumps(DICT_NOTES, ensure_ascii=False),
}

# Final pass: replace any remaining ~L~/~R~ placeholders
HTML = fixq(HTML)

io.open(OUT, 'w', encoding='utf-8').write(HTML)
print('OK', OUT, 'verses=', total, 'anno=', anno_count, 'words=', len(DICT_WORDS), 'notes=', len(DICT_NOTES))
