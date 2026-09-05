# -*- coding: utf-8 -*-
"""《爱莲说》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。
中文引号用 ~L~ / ~R~ 占位，生成前替换为 \u201c / \u201d。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ailianshuo-zhoudunyi.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'ailian_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "水陆草木之花，可爱者甚蕃。",
    "晋陶渊明独爱菊。",
    "自李唐来，世人甚爱牡丹。",
    "予独爱莲之出淤泥而不染，濯清涟而不妖，",
    "中通外直，不蔓不枝，香远益清，亭亭净植，可远观而不可亵玩焉。",
    "予谓菊，花之隐逸者也；",
    "牡丹，花之富贵者也；",
    "莲，花之君子者也。",
    "噫！菊之爱，陶后鲜有闻。",
    "莲之爱，同予者何人？",
    "牡丹之爱，宜乎众矣。",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "提出所爱 · 菊牡莲并提", "第 1–3 句",
     "以~L~水陆草木之花~R~泛起，由花及人，点出陶渊明爱菊、世人爱牡丹，以二者陪衬，为下文写自己独爱莲花蓄势。"),
    ("第二部分", "描绘莲品 · 君子之风", "第 4–10 句",
     "全文核心。从生长环境、体态香气、风度气质三个层面，由表及里地描绘莲花的形象，句句写莲，又句句喻人，莲花即君子的化身。"),
    ("第三部分", "对比评价 · 慨叹知音", "第 11–16 句",
     "以菊、牡丹、莲三种花喻三种人：隐逸者、富贵者、君子。层层对比，点明主旨；结尾三叹，感慨知音稀少，追慕者多，余味悠长。"),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
(0, "[[水陆|水中和陆地上]][[草木之花|草本和木本植物的花]]，[[可爱者|值得喜爱的（花）]][[甚蕃(fán)|很多。甚，很；蕃，多]]。",
 "水中、陆地上各种草本木本的花，值得喜爱的很多。",
 fixq("以~L~水陆草木之花~R~泛起，由花及人，为下文写三种花张本。~L~甚蕃~R~二字，见出花的种类之多，也暗示可供选择的对象之广，为下文~L~独爱~R~作反衬。"),
 ["起笔", "反衬"]),

(0, "[[晋|东晋]][[陶渊明|东晋诗人，名潜，字元亮，性爱菊，有~L~采菊东篱下~R~名句]][[独|只，唯独]]爱菊。",
 "东晋的陶渊明唯独喜爱菊花。",
 fixq("由泛写转入具体。陶渊明爱菊，是因为菊花开在深秋，不与百花争春，象征隐士的高洁。~L~独~R~字见出陶渊明的与众不同，也为下文~L~予独爱莲~R~的~L~独~R~字伏笔。"),
 ["用典", "伏笔"]),

(0, "[[自|自从]][[李唐|指唐朝，因皇帝姓李，故称]]来，[[世人|世俗的人]][[甚|很，非常]]爱牡丹。",
 "自从唐朝以来，世上的人非常喜爱牡丹。",
 fixq("再写世人爱牡丹。牡丹雍容华贵，象征富贵，故为世人所追捧。~L~世人~R~与~L~陶渊明~R~对举，一俗一雅；~L~甚爱~R~见出趋之若鹜的世态，为下文写莲花的高洁作反衬。"),
 ["对比", "反衬"]),

(1, "[[予|我]][[独|唯独]]爱莲[[之|用于主谓之间，取消句子独立性，无实义]]出[[淤(yū)泥|河沟或池塘里积存的污泥]]而[[不|表示否定，没有]][[染|沾染（污秽）]]，",
 "我唯独喜爱莲花——它从淤泥中生长出来，却不被沾染污秽，",
 fixq("由~L~予独爱~R~直入正题，与前文~L~陶渊明独爱菊~R~的~L~独~R~字呼应。~L~出淤泥而不染~R~是全文最著名的句子，写莲花生长环境的污浊与品格的洁净形成强烈对比，象征君子身处污浊社会却能保持高洁的操守。"),
 ["名句", "对比", "托物言志"]),

(1, "[[濯(zhuó)|洗涤]][[清涟(lián)|清澈的水波。涟，水波]]而[[不妖|不显得妖艳。妖，美丽而不端庄]]，",
 "在清澈的水波里洗涤过，却不显得妖艳。",
 fixq("承上句，写莲花的洁净与端庄。~L~濯清涟~R~写其经过清水的洗涤，~L~不妖~R~写其不媚俗、不张扬。前句写~L~不染~R~（不受污染），此句写~L~不妖~R~（不炫耀姿色），一内一外，写出君子既不同流合污，也不孤高自傲的品格。"),
 ["对仗", "炼字"]),

(1, "[[中通|（茎）中间贯通]][[外直|外形挺直]]，",
 "（莲茎）中间贯通，外形挺直，",
 fixq("由花及茎，写莲花的体态。~L~中通~R~写内心通达，~L~外直~R~写品行正直。以莲茎的~L~中通外直~R~喻君子的胸怀豁达、行为方正，是典型的托物言志手法。"),
 ["托物言志", "比喻"]),

(1, "[[不蔓(màn)|不生藤蔓。蔓，名词作动词，生藤蔓]][[不枝|不长枝节。枝，名词作动词，长枝节]]，",
 "不生藤蔓，不长枝节，",
 fixq("继续写莲茎的形态。~L~不蔓不枝~R~写莲茎不旁生枝蔓，喻君子不攀附权贵、不结党营私，行为专一、品格端正。两个~L~不~R~字，斩钉截铁，见出君子的操守坚定。"),
 ["词类活用", "炼字"]),

(1, "香[[远|远播，形容词作动词]][[益|更加]]清，",
 "香气远播，越发清芬，",
 fixq("由视觉转入嗅觉，写莲花的香气。~L~远~R~字名词作动词，写香气传得远；~L~益清~R~写香气越远越清芬。以香气喻君子的美德远扬，声名远播，却依然清雅不俗。"),
 ["词类活用", "多感官"]),

(1, "[[亭亭|耸立的样子]][[净植|洁净地竖立。植，竖立]]，",
 "洁净地挺立在水中，",
 fixq("写莲花的整体姿态。~L~亭亭~R~写其高耸挺拔，~L~净植~R~写其洁净直立。以莲花的亭亭玉立喻君子的卓尔不群、刚正不阿，形象鲜明。"),
 ["炼字", "形象"]),

(1, "可[[远观|远远地观赏]]而不可[[亵(xiè)玩|轻慢地玩弄。亵，亲近而不庄重]][[焉|句末语气词，相当于~L~啊~R~~L~呢~R~]]。",
 "可以远远地观赏，却不可以轻慢地玩弄啊。",
 fixq("收束对莲花的描写，点明对待莲花的态度。~L~可远观而不可亵玩~R~写莲花的庄重可敬，喻君子的人格尊严不可侵犯。~L~焉~R~字收束，余味悠长。这一句是对莲花品格的总评，也是对君子人格的礼赞。"),
 ["总收", "托物言志"]),

(2, "[[予谓|我认为]]菊，花之[[隐逸者|隐居的人。者，……的人]][[也|表判断语气]]；",
 "我认为菊花，是花中的隐士；",
 fixq("由描写转入议论，以花喻人。~L~隐逸者~R~点出菊花的象征意义——菊花不与百花争春，独开于深秋，如隐士避世独居。~L~……者也~R~是文言判断句的典型格式。"),
 ["判断句", "象征"]),

(2, "牡丹，花之[[富贵者|富贵的人]]也；",
 "牡丹，是花中的富贵者；",
 fixq("承上句，写牡丹的象征意义。牡丹雍容华贵，象征富贵。与菊花的~L~隐逸~R~形成对比，一隐一显，一雅一俗，为下文写莲花的~L~君子~R~品格作铺垫。"),
 ["对比", "象征"]),

(2, "莲，花之[[君子|品德高尚的人]]者也。",
 "莲花，是花中的君子。",
 fixq("点明全文主旨。~L~君子~R~二字，是对莲花品格的最高评价，也是作者人格理想的寄托。菊花是~L~隐逸者~R~（逃避现实），牡丹是~L~富贵者~R~（追逐名利），唯有莲花是~L~君子~R~（身处污浊而保持高洁）。三者对比，莲花的品格最为可贵。"),
 ["主旨句", "对比", "托物言志"]),

(2, "[[噫(yī)|叹词，相当于~L~唉~R~]]！菊之爱，[[陶后|陶渊明之后]][[鲜(xiǎn)|少]]有闻。",
 "唉！对于菊花的喜爱，陶渊明之后就很少听到了。",
 fixq("~L~噫~R~一叹，由议论转入抒情。~L~菊之爱，陶后鲜有闻~R~感慨像陶渊明那样的隐士越来越少，暗含对世风日下的忧虑。~L~鲜~R~读 xiǎn，意为~L~少~R~，是易错多音字。"),
 ["叹词", "多音字"]),

(2, "莲之爱，[[同予者|和我一样的人]]何人？",
 "对于莲花的喜爱，像我一样的还有什么人呢？",
 fixq("以反问句抒发知音难觅的感慨。~L~同予者何人~R~既写出作者自视甚高、不与世俗同流合污的孤傲，也流露出曲高和寡的孤独。这一问，问的是同道者何在，也是对世人的呼唤。"),
 ["反问", "抒情"]),

(2, "牡丹之爱，[[宜乎|当然。宜，应当]][[众|多]]矣。",
 "对于牡丹的喜爱，当然人很多了。",
 fixq("以感叹句收束全文。~L~宜乎众矣~R~写追逐富贵的人比比皆是，与前文~L~鲜有闻~R~~L~何人~R~形成鲜明对比。作者没有直接批评世人，却在~L~宜乎~R~二字中暗含讽刺与感慨，余味无穷。"),
 ["对比", "讽刺", "收束"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"蕃","py":"fán","q":"可爱者甚□","tip":fixq("「蕃」草字头，音 fán，意为多，勿写~L~藩~R~~L~番~R~")},
    {"w":"淤","py":"yū","q":"出□泥而不染","tip":fixq("「淤」三点水，音 yū，意为污泥，勿写~L~於~R~")},
    {"w":"濯","py":"zhuó","q":"□清涟而不妖","tip":fixq("「濯」三点水，音 zhuó，意为洗涤，勿写~L~擢~R~~L~濯~R~")},
    {"w":"涟","py":"lián","q":"濯清□而不妖","tip":fixq("「涟」三点水，音 lián，意为水波，勿写~L~莲~R~~L~链~R~")},
    {"w":"亵","py":"xiè","q":"可远观而不可□玩焉","tip":fixq("「亵」衣字底，音 xiè，意为轻慢，勿写~L~泄~R~~L~卸~R~")},
    {"w":"噫","py":"yī","q":"□！菊之爱，陶后鲜有闻","tip":fixq("「噫」口字旁，音 yī，叹词，勿写~L~意~R~~L~臆~R~")},
    {"w":"鲜","py":"xiǎn","q":"陶后□有闻","tip":fixq("「鲜」此处读 xiǎn（上声），意为少，勿读 xiān（新鲜）")},
    {"w":"蔓","py":"màn","q":"不□不枝","tip":fixq("「蔓」草字头，音 màn，名词作动词~L~生藤蔓~R~，勿写~L~漫~R~~L~慢~R~")},
    {"w":"植","py":"zhí","q":"亭亭净□","tip":fixq("「植」木字旁，音 zhí，意为竖立，勿写~L~值~R~~L~直~R~")},
    {"w":"颐","py":"yí","q":"周敦□","tip":fixq("「颐」页字旁，音 yí，作者名，勿写~L~熙~R~~L~臣~R~")},
    {"w":"敦","py":"dūn","q":"周□颐","tip":fixq("「敦」反文旁，音 dūn，作者名，勿写~L~墩~R~~L~惇~R~")},
    {"w":"逸","py":"yì","q":"花之隐□者也","tip":fixq("「逸」走之底，音 yì，意为隐居，勿写~L~意~R~~L~益~R~")},
    {"w":"予","py":"yú","q":"□独爱莲之出淤泥而不染","tip":fixq("「予」此处读 yú，意为~L~我~R~，勿读 yǔ（给予）")},
    {"w":"宜","py":"yí","q":"□乎众矣","tip":fixq("「宜」宝盖头，音 yí，意为应当，勿写~L~谊~R~~L~疑~R~")},
    {"w":"焉","py":"yān","q":"可远观而不可亵玩□","tip":fixq("「焉」四点底，音 yān，句末语气词，勿写~L~鄢~R~")},
    {"w":"妖","py":"yāo","q":"濯清涟而不□","tip":fixq("「妖」女字旁，音 yāo，意为美丽而不端庄，勿写~L~娇~R~")},
    {"w":"亭亭","py":"tíng tíng","q":"□□净植","tip":fixq("「亭亭」亠字头，音 tíng tíng，叠词形容耸立，勿写~L~庭~R~")},
    {"w":"清","py":"qīng","q":"香远益□","tip":fixq("「清」三点水，音 qīng，意为清芬，勿写~L~青~R~")},
]

DICT_NOTES = [
    {"w":"甚蕃","q":"水陆草木之花，可爱者甚蕃","a":"很多。甚，很；蕃，fán，多"},
    {"w":"晋","q":"晋陶渊明独爱菊","a":"东晋"},
    {"w":"陶渊明","q":"晋陶渊明独爱菊","a":"东晋诗人，名潜，字元亮，性爱菊"},
    {"w":"独","q":"晋陶渊明独爱菊","a":"只，唯独"},
    {"w":"李唐","q":"自李唐来，世人甚爱牡丹","a":"指唐朝，因皇帝姓李，故称"},
    {"w":"世人","q":"自李唐来，世人甚爱牡丹","a":"世俗的人"},
    {"w":"予","q":"予独爱莲之出淤泥而不染","a":"我。读 yú"},
    {"w":"之","q":"予独爱莲之出淤泥而不染","a":"用于主谓之间，取消句子独立性，无实义"},
    {"w":"淤泥","q":"予独爱莲之出淤泥而不染","a":"河沟或池塘里积存的污泥。淤，yū"},
    {"w":"染","q":"予独爱莲之出淤泥而不染","a":"沾染（污秽）"},
    {"w":"濯","q":"濯清涟而不妖","a":"洗涤。濯，zhuó"},
    {"w":"清涟","q":"濯清涟而不妖","a":"清澈的水波。涟，lián，水波"},
    {"w":"妖","q":"濯清涟而不妖","a":"美丽而不端庄，妖艳"},
    {"w":"中通","q":"中通外直","a":"（茎）中间贯通"},
    {"w":"外直","q":"中通外直","a":"外形挺直"},
    {"w":"蔓","q":"不蔓不枝","a":"名词作动词，生藤蔓。蔓，màn"},
    {"w":"枝","q":"不蔓不枝","a":"名词作动词，长枝节"},
    {"w":"远","q":"香远益清","a":"远播，形容词作动词"},
    {"w":"益","q":"香远益清","a":"更加"},
    {"w":"亭亭","q":"亭亭净植","a":"耸立的样子"},
    {"w":"净植","q":"亭亭净植","a":"洁净地竖立。植，竖立"},
    {"w":"亵玩","q":"可远观而不可亵玩焉","a":"轻慢地玩弄。亵，xiè，亲近而不庄重"},
    {"w":"焉","q":"可远观而不可亵玩焉","a":"句末语气词，相当于~L~啊~R~~L~呢~R~"},
    {"w":"隐逸者","q":"予谓菊，花之隐逸者也","a":"隐居的人。者，……的人"},
    {"w":"也","q":"予谓菊，花之隐逸者也","a":"句末语气词，表判断"},
    {"w":"富贵者","q":"牡丹，花之富贵者也","a":"富贵的人"},
    {"w":"君子","q":"莲，花之君子者也","a":"品德高尚的人"},
    {"w":"噫","q":"噫！菊之爱，陶后鲜有闻","a":"叹词，相当于~L~唉~R~。噫，yī"},
    {"w":"菊之爱","q":"噫！菊之爱，陶后鲜有闻","a":"对于菊花的喜爱。之，宾语前置的标志（或解释为~L~的~R~）"},
    {"w":"鲜","q":"陶后鲜有闻","a":"少。鲜，xiǎn，易错多音字"},
    {"w":"同予者","q":"莲之爱，同予者何人","a":"和我一样的人"},
    {"w":"宜乎","q":"牡丹之爱，宜乎众矣","a":"当然。宜，应当"},
    {"w":"众","q":"牡丹之爱，宜乎众矣","a":"多"},
    {"w":"矣","q":"牡丹之爱，宜乎众矣","a":"句末语气词，表感叹"},
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
    <p>《爱莲说》是北宋理学家周敦颐的一篇托物言志的小品文，全文仅一百一十九字，却以凝练的笔墨、精巧的构思，成为中国文学史上咏物散文的经典。</p>
    <p>文章以莲花为喻，通过对莲花~L~出淤泥而不染，濯清涟而不妖~R~的品格的赞美，表达了作者不慕名利、洁身自好的人生态度，也暗含了对追逐富贵的世风的批评。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>周敦颐（1017—1073），字茂叔，号濂溪，世称~L~濂溪先生~R~，道州营道（今湖南道县）人。北宋著名哲学家、理学家，是宋明理学的开山鼻祖。曾任分宁主簿、南安军司理参军、虔州通判等职，为官清廉，刚正不阿。</p>
    <p>周敦颐的哲学思想以~L~太极~R~为核心，著有《太极图说》《通书》等，对后世理学发展影响深远。朱熹曾推崇他~L~得孔孟不传之学~R~。其文学作品虽不多，但《爱莲说》一篇足以传世。</p>
    <p class="note">※ 周敦颐晚年在庐山莲花峰下建书堂讲学，堂前有溪，取名~L~濂溪~R~，故世称~L~濂溪先生~R~。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>北宋文风：</b>北宋时期，古文运动深入发展，小品文创作繁荣。文人往往通过咏物来表达个人志趣，托物言志成为常见的写作手法。</p>
    <p><b>社会风气：</b>北宋中期，社会相对安定，但追求富贵、贪图享乐的风气渐盛。周敦颐作为理学家，强调个人品德修养，对世俗风气有所不满。</p>
    <p><b>写作缘起：</b>周敦颐任职虔州（今江西赣州）通判时，在衙署东侧开池种莲，名为~L~莲池~R~。他常于池畔赏花思考，借莲花的品格抒发自己的人生理想，写下这篇《爱莲说》。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>~L~说~R~是古代的一种议论文体，用以陈述作者对某个问题的见解，可以叙事，可以议论，可以抒情，写法较为自由。《爱莲说》就是~L~说~R~体的典范之作，全文托物言志，借莲花的形象表达作者的人格理想。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>雅坤朗诵《爱莲说》（央广播音指导）</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1G14y1A7nU&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="雅坤朗诵《爱莲说》"></iframe>
        <a href="https://www.bilibili.com/video/BV1G14y1A7nU" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>把课文编成歌——《爱莲说》歌曲演唱</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1Hs4y1R7i6&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="《爱莲说》歌曲演唱"></iframe>
        <a href="https://www.bilibili.com/video/BV1Hs4y1R7i6" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>莲花形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">出淤泥而不染的君子</div>
        <p>文中的莲花，是君子的化身。作者从三个层面塑造莲花的形象：一是生长环境——~L~出淤泥而不染，濯清涟而不妖~R~，写其身处污浊而保持高洁；二是体态香气——~L~中通外直，不蔓不枝，香远益清~R~，写其内心通达、行为正直、美德远扬；三是风度气质——~L~亭亭净植，可远观而不可亵玩焉~R~，写其庄重可敬、不可轻慢。三个层面由表及里，由形入神，把莲花的品格写得淋漓尽致，也把君子的形象塑造得光彩照人。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">托物言志，物我合一</div>
        <p>全文以莲花为喻，句句写莲，又句句喻人。莲花的~L~出淤泥而不染~R~即君子的不同流合污，~L~中通外直~R~即君子的胸怀豁达与品行方正，~L~不蔓不枝~R~即君子的不攀附不结党，~L~香远益清~R~即君子的美德远扬。物与志高度统一，莲花的形象就是作者人格理想的化身。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比衬托，三者并写</div>
        <p>文章以菊花、牡丹、莲花三种花并写，形成多重对比。菊花是~L~隐逸者~R~，逃避现实；牡丹是~L~富贵者~R~，追逐名利；莲花是~L~君子~R~，身处污浊而保持高洁。三者对比，既突出了莲花品格的可贵，也暗含了对两种人生态度的评价。以菊作正衬，以牡丹作反衬，莲花的形象更加鲜明。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">骈散结合，节奏铿锵</div>
        <p>文章句式整散结合。写莲花的部分多用骈句（对偶句），如~L~出淤泥而不染，濯清涟而不妖~R~~L~中通外直，不蔓不枝~R~，节奏整齐，音韵和谐；议论抒情部分多用散句，灵活自然。骈散结合，使文章既有整齐之美，又有流动之势，读来朗朗上口。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">以花喻人，层层递进</div>
        <p>文章结构精巧：先以草木之花泛起，再点出菊与牡丹两种花，然后集中笔墨写莲花，最后以三种花喻三种人收束。由花及人，由物及志，层层递进，最后以三句感叹收束全文，余味悠长。全文仅一百一十九字，却包含了描写、议论、抒情三种表达方式，容量极大。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">出淤泥而不染，濯清涟而不妖。</div>
        <p>全文最著名的句子，也是莲花品格的集中写照。~L~出淤泥而不染~R~写莲花从污浊的环境中生长出来却不被污染，象征君子身处黑暗社会却能保持高洁的操守；~L~濯清涟而不妖~R~写莲花经过清水洗涤却不显得妖艳，象征君子不媚俗、不张扬、端庄自重的品格。一前一后，一内一外，把君子的品格写得既坚定又温润，成为千古传颂的名句。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">莲，花之君子者也。</div>
        <p>全文的主旨句。在分别点出菊花是~L~隐逸者~R~、牡丹是~L~富贵者~R~之后，作者以判断句的形式郑重宣告：莲花是~L~花之君子~R~。这一句是对莲花品格的最高评价，也是作者人格理想的宣言。~L~君子~R~二字，统摄全文，把莲花的自然属性升华为道德人格，使文章的立意达到最高点。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《爱莲说》通过对莲花可爱形象的描绘和赞美，表达了作者不慕名利、洁身自好的人生态度，以及对追逐富贵、趋炎附势的世风的鄙弃。</p>
    <p>文章的深刻之处，在于它不是简单地赞美莲花，而是借莲花的形象寄托了作者的人格理想。在作者看来，菊花的~L~隐逸~R~是逃避现实，牡丹的~L~富贵~R~是追逐名利，唯有莲花的~L~君子~R~品格——身处污浊而不同流合污，端庄自重而不媚俗——才是最值得追求的人生境界。结尾三叹，既感慨知音稀少，也暗含对世人的呼唤，使文章的主题超越了个人志趣，具有普遍的社会意义。</p>
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
      <tr><td class="kai">（本文无通假字）</td><td>—</td><td>—</td><td>《爱莲说》全文无通假字</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">植</td><td>竖立</td><td>种植、植物</td><td>亭亭净植</td></tr>
      <tr><td class="kai">君子</td><td>品德高尚的人</td><td>对人的尊称</td><td>莲，花之君子者也</td></tr>
      <tr><td class="kai">隐逸</td><td>隐居避世</td><td>隐藏、逃跑</td><td>花之隐逸者也</td></tr>
      <tr><td class="kai">鲜</td><td>少（读 xiǎn）</td><td>新鲜（读 xiān）</td><td>陶后鲜有闻</td></tr>
      <tr><td class="kai">宜</td><td>应当、当然</td><td>合适</td><td>宜乎众矣</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>词类活用</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">蔓</td><td>名词作动词</td><td>生藤蔓</td><td>不蔓不枝</td></tr>
      <tr><td class="kai">枝</td><td>名词作动词</td><td>长枝节</td><td>不蔓不枝</td></tr>
      <tr><td class="kai">远</td><td>形容词作动词</td><td>远播</td><td>香远益清</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">判断句</td><td>予谓菊，花之隐逸者也</td><td>~L~……者也~R~表判断，是文言判断句的典型格式</td></tr>
      <tr><td class="kai">判断句</td><td>莲，花之君子者也</td><td>~L~……者也~R~表判断</td></tr>
      <tr><td class="kai">反问句</td><td>莲之爱，同予者何人？</td><td>以反问加强语气，抒发感慨</td></tr>
      <tr><td class="kai">省略句</td><td>（予）独爱莲之出淤泥而不染</td><td>承前省略主语~L~予~R~</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>一词多义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="3">之</td><td>的，结构助词</td><td>水陆草木之花</td></tr>
      <tr><td>用于主谓之间，取消句子独立性</td><td>予独爱莲之出淤泥而不染</td></tr>
      <tr><td>宾语前置的标志（或~L~的~R~）</td><td>菊之爱，陶后鲜有闻</td></tr>
      <tr><td class="kai" rowspan="2">者</td><td>……的花</td><td>可爱者甚蕃</td></tr>
      <tr><td>……的人</td><td>花之隐逸者也</td></tr>
      <tr><td class="kai" rowspan="3">而</td><td>表转折，却</td><td>出淤泥而不染</td></tr>
      <tr><td>表转折，却</td><td>可远观而不可亵玩焉</td></tr>
      <tr><td>表并列（不译）</td><td>濯清涟而不妖（与上句对举）</td></tr>
      <tr><td class="kai" rowspan="2">鲜</td><td>少，读 xiǎn</td><td>陶后鲜有闻</td></tr>
      <tr><td>新鲜，读 xiān</td><td>（无，本文仅一义）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>~L~说~R~文体</dt><dd>古代的一种议论文体，用以陈述作者对某个问题的见解，可以叙事、议论、抒情，写法自由。如《爱莲说》《师说》《捕蛇者说》等。</dd></div>
      <div class="g-item"><dt>花中四君子</dt><dd>指梅、兰、竹、菊四种花木，象征君子的四种品格：梅的傲雪、兰的幽香、竹的挺拔、菊的隐逸。莲花虽不在~L~四君子~R~之列，但周敦颐的《爱莲说》使莲花成为君子品格的又一象征。</dd></div>
      <div class="g-item"><dt>陶渊明爱菊</dt><dd>陶渊明（365—427），东晋诗人，性爱菊，有~L~采菊东篱下，悠然见南山~R~的名句。菊花在深秋开放，不与百花争春，象征隐士的高洁，故陶渊明被视为~L~隐逸~R~的代表。</dd></div>
      <div class="g-item"><dt>唐人爱牡丹</dt><dd>唐代社会崇尚牡丹，刘禹锡有~L~唯有牡丹真国色，花开时节动京城~R~的诗句。牡丹雍容华贵，象征富贵，故为世人所追捧。</dd></div>
      <div class="g-item"><dt>濂溪先生</dt><dd>周敦颐的世称。他晚年在庐山莲花峰下建书堂讲学，堂前有溪，取名~L~濂溪~R~，学者称其为~L~濂溪先生~R~。</dd></div>
      <div class="g-item"><dt>托物言志</dt><dd>通过对物品的描写和叙述，表达自己的志向和意愿的写作手法。《爱莲说》是托物言志的典范，借莲花的形象表达作者的人格理想。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《爱莲说》周敦颐</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">北宋 · 周敦颐</div>
  <h1 class="hero-title">爱莲说</h1>
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
  <div class="sec-sub">全文一百一十九字，分三部分：提出所爱、描绘莲品、对比评价。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《爱莲说》</div>
  <div>周敦颐 · 北宋（1017—1073）· 世称濂溪先生</div>
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
