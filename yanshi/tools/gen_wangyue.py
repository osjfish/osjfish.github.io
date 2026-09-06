# -*- coding: utf-8 -*-
"""《望岳》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。
中文引号用 ~L~ / ~R~ 占位，生成前替换为 \u201c / \u201d。
注释格式：[[词|（拼音）释义]]，原文纯净，拼音在 data-note 里。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wangyue-dufu.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'wangyue_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "岱宗夫如何？齐鲁青未了。",
    "造化钟神秀，阴阳割昏晓。",
    "荡胸生曾云，决眦入归鸟。",
    "会当凌绝顶，一览众山小。",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "远望泰山 · 神秀昏晓", "第 1–4 句",
     fixq("首联以设问起笔，~L~岱宗夫如何~R~，一个~L~夫~R~字，写出初见泰山时的惊叹与揣摩。~L~齐鲁青未了~R~，以齐鲁大地的青翠不尽来烘托泰山的绵延辽阔。颔联~L~造化钟神秀，阴阳割昏晓~R~，上句写泰山的神奇秀丽是天地造化的钟爱，下句写泰山的高大巍峨使山南山北判若昏晓。~L~钟~R~~L~割~R~二字，炼字精绝，是全诗的名句。")),
    ("第二部分", "近望细观 · 绝顶展望", "第 5–8 句",
     fixq("颈联由远望转入近望细观。~L~荡胸生曾云~R~，山上云气层生，涤荡心胸；~L~决眦入归鸟~R~，极目远眺，归鸟入林，一个~L~入~R~字写出视野的辽远。尾联~L~会当凌绝顶，一览众山小~R~，由~L~望岳~R~转为~L~登岳~R~的展望，抒发了诗人不怕困难、敢于攀登绝顶、俯视一切的雄心壮志，是千古传诵的名句，蕴含深刻的人生哲理。")),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
# ===== 第一部分：远望泰山 =====
(0, "[[岱宗|（dài）对泰山的尊称。岱，泰山的别名；宗，首、大，泰山为五岳之首，故称岱宗]][[夫|（fú）句首发语词，无实义，表惊叹或揣摩的语气]]如何？",
 "泰山到底怎么样呢？",
 fixq("以设问开篇，~L~岱宗夫如何~R~，一个~L~夫~R~字是句首发语词，虽无实义，却写出了诗人初见泰山时那种惊叹、揣摩、不知如何形容的语气。~L~岱宗~R~是对泰山的尊称，泰山为五岳之首，故称~L~宗~R~。以设问起笔，既引人入胜，又为下文描写泰山的高大巍峨蓄势。这种以问句开篇的手法，在杜甫诗中颇为常见，显得自然而有力。"),
 ["设问", "起笔", "炼字"]),

(0, "[[齐鲁|春秋时的两个诸侯国名，在今山东一带，泰山以北为齐，以南为鲁]]青[[了|（liǎo）尽、完结。~L~未了~R~即不尽、没有边际]]。",
 "在齐鲁大地上，泰山的青翠山色连绵不断，没有尽头。",
 fixq("~L~齐鲁青未了~R~是写泰山的千古名句。诗人不直接说泰山有多高多大，而是说在齐鲁两国的大地上，泰山的青翠山色绵延不尽、望不到头。~L~青~R~字写山色，~L~未了~R~写绵延，以距离之远来烘托泰山之高大——走出了齐鲁国境，还能望见泰山的青翠，泰山该有多么巍峨！这种以距离写高度的侧面烘托手法，比直接说~L~泰山很高~R~更有力量，也更有诗意。"),
 ["侧面烘托", "炼字", "名句"]),

(0, "[[造化|指天地、大自然。造，创造；化，化育]][[钟|聚集、钟爱。这里用拟人手法，写大自然把神奇秀丽都聚集在泰山上]]神秀，",
 "大自然把神奇秀丽的景色都聚集在泰山上，",
 fixq("~L~造化钟神秀~R~，一个~L~钟~R~字是全诗的炼字经典。~L~钟~R~本是聚集的意思，这里用拟人手法，写大自然仿佛有情感、有意志，把天地间所有的神奇秀丽都~L~钟~R~（聚集、钟爱）在了泰山上。一个~L~钟~R~字，将大自然写得有情有义，也将泰山的神秀写到了极致——它不是一般的秀美，而是集天地造化之大成的神秀。这种拟人化的炼字，使诗句生动有力，意境深远。"),
 ["拟人", "炼字", "名句"]),

(0, "[[阴阳|山的北面和南面。古代以山北水南为阴，山南水北为阳]][[割|分割、划分。这里写泰山高大，使山南山北的光线明暗截然不同，如同被刀割开一般]]昏晓。",
 "泰山高大巍峨，山南山北，一昏一晓，判若两个世界。",
 fixq("~L~阴阳割昏晓~R~，一个~L~割~R~字又是全诗的炼字经典。~L~阴阳~R~指山北（阴）和山南（阳），~L~昏晓~R~指昏暗和明亮。泰山太高太大了，以至于山的南面阳光普照（晓），山的北面却阴暗昏沉（昏），同一座山，山南山北如同被一把巨大的刀~L~割~R~开了一样，判若两个世界。一个~L~割~R~字，化静为动，将泰山的巍峨高大写得惊心动魄，仿佛能看到那道明暗交界的锐利线条。~L~钟~R~写柔（神秀），~L~割~R~写刚（高大），一柔一刚，将泰山的形神写尽。"),
 ["炼字", "化静为动", "名句"]),

# ===== 第二部分：近望与展望 =====
(1, "[[荡胸|涤荡心胸。荡，涤荡、激荡；胸，心胸]]生[[曾|（céng）同~L~层~R~，层层叠叠。通假字]]云，",
 "山上云气层生，涤荡着我的心胸，",
 fixq("颈联由远望转入近望细观。~L~荡胸生曾云~R~，~L~曾~R~通~L~层~R~，~L~曾云~R~即层云、层层叠叠的云气。诗人站在泰山脚下仰望，只见山上云气蒸腾、层叠而生，这云气仿佛在涤荡着诗人的心胸，使人心胸开阔、意气风发。~L~荡~R~字写出云气的动态，也写出诗人内心的激荡——见此壮美景象，胸中的豪情也被激发出来。~L~生~R~字写云气从山间生出，灵动而有生机。"),
 ["通假字", "炼字", "近望"]),

(1, "[[决眦|（zì）极力张大眼睛远望。决，裂开；眦，眼角。~L~决眦~R~形容眼睛睁得极大，几乎要裂开眼角]]入归鸟。",
 "我极力张大眼睛，远望那归林的飞鸟，",
 fixq("~L~决眦入归鸟~R~，~L~决眦~R~是极力张大眼睛的意思，~L~眦~R~是眼角，~L~决眦~R~形容眼睛睁得极大，几乎要裂开眼角，极写诗人远望时的专注与投入。~L~入归鸟~R~的~L~入~R~字用得极妙——归鸟飞进了诗人的视野之中，一个~L~入~R~字，写出了视野的辽远和诗人的目不转睛，仿佛鸟儿是主动~L~飞进~R~诗人眼中的。这一句通过~L~决眦~R~的细节和~L~入~R~字的炼字，将诗人对泰山的痴迷与向往写得入木三分，也为下文~L~会当凌绝顶~R~的攀登之志做了铺垫。"),
 ["炼字", "细节", "铺垫"]),

(1, "[[会当|终当、终要，表将来时，含有~L~一定要~R~的决心和期望]][[凌|（líng）登、登上。~L~凌~R~有高出、超越之意]]绝顶，",
 "我终要登上泰山的最高峰，",
 fixq("尾联由~L~望岳~R~转为~L~登岳~R~的展望。~L~会当~R~是终当、终要的意思，表将来时，含有~L~一定要~R~的决心和期望。~L~凌~R~是登的意思，但~L~凌~R~比~L~登~R~更有力量——~L~凌~R~有高出、超越之意，~L~凌绝顶~R~不仅是登上山顶，更是超越一切、俯视一切。~L~会当凌绝顶~R~，一个~L~会当~R~，写出了诗人的坚定信念；一个~L~凌~R~，写出了诗人的凌云壮志。这一句是全诗情感的高潮，也是杜甫青年时期豪情壮志的集中体现。"),
 ["炼字", "壮志", "名句"]),

(1, "一览众山小。",
 "俯瞰群山，它们都显得那么渺小。",
 fixq("~L~一览众山小~R~，是全诗的点睛之笔，也是千古传诵的名句。诗人站在泰山绝顶之上，俯瞰四周的群山，它们都显得那么渺小。这一句化用了《孟子·尽心上》~L~孔子登东山而小鲁，登泰山而小天下~R~的典故，但杜甫用~L~一览众山小~R~五个字，比孟子的话更凝练、更有力。~L~小~R~字是形容词的意动用法，~L~以……为小~R~，写出了站在绝顶俯视群山的感受。这一句不仅写了泰山的高大，更抒发了诗人不怕困难、敢于攀登绝顶、俯视一切的雄心壮志，蕴含着~L~站得高，看得远~R~~L~只有攀登绝顶，才能超越一切~R~的深刻人生哲理。千百年来，这两句诗激励着无数人勇攀高峰、追求卓越。"),
 ["用典", "哲理", "名句", "点睛之笔"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"岱","py":"dài","q":"□宗夫如何？齐鲁青未了。","tip":fixq("「岱」山字旁，音 dài，泰山的别名，勿写~L~代~R~~L~袋~R~")},
    {"w":"宗","py":"zōng","q":"岱□夫如何？齐鲁青未了。","tip":fixq("「宗」宝盖头，音 zōng，首、大，泰山为五岳之首故称岱宗，勿写~L~棕~R~~L~踪~R~")},
    {"w":"夫","py":"fú","q":"岱宗□如何？齐鲁青未了。","tip":fixq("「夫」此处读 fú（阳平），句首发语词无实义，勿读 fū（夫妻）")},
    {"w":"了","py":"liǎo","q":"齐鲁青未□","tip":fixq("「了」此处读 liǎo，尽、完结，~L~未了~R~即不尽，勿读 le（助词）")},
    {"w":"钟","py":"zhōng","q":"造化□神秀，阴阳割昏晓","tip":fixq("「钟」金字旁，音 zhōng，聚集、钟爱，拟人手法，勿写~L~中~R~~L~终~R~")},
    {"w":"割","py":"gē","q":"造化钟神秀，阴阳□昏晓","tip":fixq("「割」立刀旁，音 gē，分割，化静为动写泰山高大，勿写~L~阁~R~~L~格~R~")},
    {"w":"曾","py":"céng","q":"荡胸生□云，决眦入归鸟","tip":fixq("「曾」此处通~L~层~R~，读 céng，层层叠叠，通假字，勿读 zēng（曾经）")},
    {"w":"眦","py":"zì","q":"荡胸生曾云，决□入归鸟","tip":fixq("「眦」目字旁，音 zì，眼角，~L~决眦~R~形容极力张大眼睛，勿写~L~呲~R~~L~龇~R~")},
    {"w":"凌","py":"líng","q":"会当□绝顶，一览众山小","tip":fixq("「凌」两点水，音 líng，登、高出，~L~凌绝顶~R~即登最高峰，勿写~L~陵~R~（山陵）~L~零~R~")},
    {"w":"览","py":"lǎn","q":"会当凌绝顶，一□众山小","tip":fixq("「览」见字底，音 lǎn，看、观赏，~L~一览~R~即放眼观看，勿写~L~揽~R~（采摘）~L~缆~R~（缆绳）")},
    {"w":"晓","py":"xiǎo","q":"阴阳割昏□","tip":fixq("「晓」日字旁，音 xiǎo，明亮、天亮，与~L~昏~R~相对，勿写~L~绕~R~~L~饶~R~")},
    {"w":"胸","py":"xiōng","q":"荡□生曾云，决眦入归鸟","tip":fixq("「胸」月字旁（肉），音 xiōng，心胸，勿写~L~凶~R~~L~汹~R~")},
    {"w":"绝","py":"jué","q":"会当凌□顶，一览众山小","tip":fixq("「绝」绞丝旁，音 jué，极、最，~L~绝顶~R~即最高峰，勿写~L~决~R~（决定）")},
]

DICT_NOTES = [
    {"w":"岱宗","q":"岱宗夫如何","a":"对泰山的尊称。岱，dài，泰山的别名；宗，首、大，泰山为五岳之首"},
    {"w":"夫","q":"岱宗夫如何","a":"句首发语词，无实义，表惊叹或揣摩的语气。读 fú"},
    {"w":"齐鲁","q":"齐鲁青未了","a":"春秋时的两个诸侯国名，在今山东一带，泰山以北为齐，以南为鲁"},
    {"w":"未了","q":"齐鲁青未了","a":"不尽、没有边际。了，liǎo，尽、完结"},
    {"w":"造化","q":"造化钟神秀","a":"指天地、大自然。造，创造；化，化育"},
    {"w":"钟","q":"造化钟神秀","a":"聚集、钟爱。拟人手法，写大自然把神奇秀丽都聚集在泰山上"},
    {"w":"神秀","q":"造化钟神秀","a":"神奇秀丽"},
    {"w":"阴阳","q":"阴阳割昏晓","a":"山的北面和南面。古代以山北水南为阴，山南水北为阳"},
    {"w":"割","q":"阴阳割昏晓","a":"分割、划分。写泰山高大，使山南山北光线明暗截然不同"},
    {"w":"昏晓","q":"阴阳割昏晓","a":"昏暗和明亮。昏，昏暗；晓，明亮"},
    {"w":"荡胸","q":"荡胸生曾云","a":"涤荡心胸。荡，涤荡、激荡"},
    {"w":"曾","q":"荡胸生曾云","a":fixq("同~L~层~R~，层层叠叠。读 céng，通假字")},
    {"w":"决眦","q":"决眦入归鸟","a":"极力张大眼睛远望。决，裂开；眦，zì，眼角。形容眼睛睁得极大"},
    {"w":"入","q":"决眦入归鸟","a":"进入（视野）。写归鸟飞进诗人的视野之中"},
    {"w":"会当","q":"会当凌绝顶","a":"终当、终要，表将来时，含有~L~一定要~R~的决心和期望"},
    {"w":"凌","q":"会当凌绝顶","a":"登、登上。读 líng，有高出、超越之意"},
    {"w":"绝顶","q":"会当凌绝顶","a":"最高峰。绝，极、最"},
    {"w":"一览","q":"一览众山小","a":"放眼观看。览，lǎn，看、观赏"},
    {"w":"小","q":"一览众山小","a":"形容词意动用法，以……为小，觉得……渺小"},
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
    <p>《望岳》是唐代伟大诗人杜甫的名篇，作于开元二十四年（736）前后，是杜甫现存诗中年代最早的一首。当时二十四五岁的杜甫正值青年，漫游齐赵（今山东、河北一带），途经泰山，被泰山的雄伟壮丽所震撼，写下了这首千古传诵的五言律诗。</p>
    <p>全诗以~L~望~R~字统摄，由远望到近望，由细望到展望，层层递进，写出了泰山的高大巍峨和神奇秀丽，更抒发了青年杜甫不怕困难、敢于攀登绝顶、俯视一切的雄心壮志。~L~会当凌绝顶，一览众山小~R~不仅是写泰山，更是杜甫一生精神的写照——积极进取、乐观自信、志存高远。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>杜甫（712—770），字子美，自号少陵野老，祖籍襄阳，生于河南巩县。唐代伟大的现实主义诗人，被后世尊为~L~诗圣~R~，其诗被称为~L~诗史~R~。与李白并称~L~李杜~R~。曾任左拾遗、检校工部员外郎，故世称~L~杜工部~R~。</p>
    <p>杜甫的一生以安史之乱为界，分为前后两个时期。前期（三十五岁前）正值开元盛世，杜甫漫游吴越、齐赵，意气风发，诗歌风格豪放明朗，《望岳》是这一时期的代表作。后期历经安史之乱，杜甫颠沛流离，诗歌转向沉郁顿挫，深刻反映社会现实，代表作有~L~三吏~R~~L~三别~R~、《春望》《登高》《茅屋为秋风所破歌》等。</p>
    <p class="note">※ 《望岳》是杜甫现存诗中最早的一首，也是他少有的豪放明快之作，与后期沉郁顿挫的风格形成鲜明对比，是了解杜甫青年时期精神面貌的重要作品。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>开元盛世：</b>唐玄宗开元年间（713—741），是唐朝的全盛时期，国力强盛、经济繁荣、文化昌盛，史称~L~开元盛世~R~。青年杜甫生长在这样一个时代，充满了积极进取的精神和对未来的美好憧憬。</p>
    <p><b>漫游齐赵：</b>开元二十三年（735），杜甫参加科举考试不中，次年开始漫游齐赵（今山东、河北一带）。这段漫游生活持续了四五年，杜甫登山临水、访古探幽，眼界大开，诗歌创作也进入了第一个高峰期。《望岳》即作于这一时期。</p>
    <p><b>泰山崇拜：</b>泰山为五岳之首，自古以来就是帝王封禅、文人朝拜的圣地。孔子~L~登东山而小鲁，登泰山而小天下~R~的典故，使泰山不仅是一座自然名山，更是一种精神象征——攀登泰山，就是攀登人生的高峰。杜甫望岳，不仅是望一座山，更是在望自己的人生理想。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《望岳》是一首<b>五言律诗</b>，全诗八句，每句五字，共四十字。首联（一二句）设问起笔，颔联（三四句）对仗工整，颈联（五六句）继续对仗，尾联（七八句）抒发壮志。全诗格律严谨，对仗精工，是五言律诗的典范之作。</p>
    <p>值得注意的是，诗题是~L~望岳~R~而非~L~登岳~R~——全诗没有一句写诗人真正登上了泰山，而是从各个角度~L~望~R~泰山，最后以~L~会当凌绝顶~R~的展望收束。这种~L~以望写登~R~的手法，既写出了泰山的高大，也留出了想象的空间，比直接写~L~我登上了泰山~R~更有力量。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>徐涛朗诵杜甫《望岳》（安徽卫视~L~诗中国~R~）</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1bf4y1F7M3&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="徐涛朗诵杜甫《望岳》"></iframe>
        <a href="https://www.bilibili.com/video/BV1bf4y1F7M3" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>《望岳》古诗赏析——~L~望~R~人生路，系家国情</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1PT42127RL&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="《望岳》古诗赏析"></iframe>
        <a href="https://www.bilibili.com/video/BV1PT42127RL" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">青年杜甫——意气风发的攀登者</div>
        <p>《望岳》中的抒情主人公，是一个意气风发、胸怀壮志的青年形象。他站在泰山脚下，仰望这座五岳之首的名山，心中充满了惊叹与向往。</p>
        <p><b>惊叹与揣摩：</b>~L~岱宗夫如何~R~，一个~L~夫~R~字，写出了初见泰山时的那种不知如何形容的惊叹与揣摩——泰山太高大了，太神奇了，诗人一时找不到合适的词语来形容它。</p>
        <p><b>痴迷与投入：</b>~L~荡胸生曾云，决眦入归鸟~R~，诗人被泰山的壮美景象深深吸引，云气涤荡心胸，归鸟飞入视野，他~L~决眦~R~而望，目不转睛，完全沉浸在对泰山的观赏之中。这种痴迷，是对美的追求，也是对崇高的向往。</p>
        <p><b>壮志与豪情：</b>~L~会当凌绝顶，一览众山小~R~，诗人不满足于~L~望~R~岳，他要~L~登~R~岳，要登上泰山的最高峰，俯视一切。这种不怕困难、敢于攀登、俯视一切的雄心壮志，正是青年杜甫最动人的精神面貌。这个形象，与后期~L~艰难苦恨繁霜鬓~R~的杜甫形成了鲜明对比，让我们看到了一个充满青春活力和进取精神的杜甫。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">炼字精当——钟、割、凌、入</div>
        <p>《望岳》是杜甫炼字的典范之作，短短四十字中，多个字用得精妙绝伦：</p>
        <p><b>~L~钟~R~字：</b>~L~造化钟神秀~R~，~L~钟~R~是聚集、钟爱的意思，用拟人手法，写大自然把天地间所有的神奇秀丽都聚集、钟爱在了泰山上。一个~L~钟~R~字，将大自然写得有情有义，也将泰山的神秀写到了极致。</p>
        <p><b>~L~割~R~字：</b>~L~阴阳割昏晓~R~，~L~割~R~是分割的意思，写泰山太高太大，山南山北的光线明暗截然不同，如同被一把巨大的刀割开了一样。一个~L~割~R~字，化静为动，将泰山的巍峨高大写得惊心动魄，仿佛能看到那道明暗交界的锐利线条。</p>
        <p><b>~L~入~R~字：</b>~L~决眦入归鸟~R~，~L~入~R~是进入的意思，写归鸟飞进了诗人的视野之中。一个~L~入~R~字，写出了视野的辽远和诗人的目不转睛，仿佛鸟儿是主动~L~飞进~R~诗人眼中的，生动而有神。</p>
        <p><b>~L~凌~R~字：</b>~L~会当凌绝顶~R~，~L~凌~R~是登的意思，但~L~凌~R~比~L~登~R~更有力量——~L~凌~R~有高出、超越之意，~L~凌绝顶~R~不仅是登上山顶，更是超越一切、俯视一切。一个~L~凌~R~字，写出了诗人的凌云壮志。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">虚实结合，由远及近</div>
        <p><b>由远及近的观察顺序：</b>全诗以~L~望~R~字统摄，观察角度由远及近、层层递进。首联~L~岱宗夫如何？齐鲁青未了~R~是远望，从齐鲁大地的整体印象来写泰山的绵延；颔联~L~造化钟神秀，阴阳割昏晓~R~是近望，从正面描写泰山的神秀与高大；颈联~L~荡胸生曾云，决眦入归鸟~R~是细望，写山上的云气和归鸟，是诗人凝神细观的景象；尾联~L~会当凌绝顶，一览众山小~R~是展望，由~L~望~R~转为~L~登~R~的想象。远望—近望—细望—展望，四个层次，条理分明，将泰山的形神写得淋漓尽致。</p>
        <p><b>虚实结合：</b>首联到颈联是实写，写诗人亲眼所见的泰山景象；尾联是虚写，写诗人想象中登上泰山绝顶后的感受。由实入虚，由眼前之景到心中之志，使诗歌的境界从对泰山的描写拓展到对人生理想的抒发，意境更加深远。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">设问起笔，对仗精工</div>
        <p><b>设问起笔：</b>~L~岱宗夫如何？~R~以设问开篇，既引人入胜，又写出了初见泰山时的惊叹与揣摩。问而不答，答案在下文的描写中自然呈现，比直接说~L~泰山很高~R~更有力量，也更有诗意。</p>
        <p><b>对仗精工：</b>颔联~L~造化钟神秀，阴阳割昏晓~R~和颈联~L~荡胸生曾云，决眦入归鸟~R~都是工整的对仗。~L~造化~R~对~L~阴阳~R~（名词对名词），~L~钟~R~对~L~割~R~（动词对动词），~L~神秀~R~对~L~昏晓~R~（形容词对形容词）；~L~荡胸~R~对~L~决眦~R~（动宾对动宾），~L~生~R~对~L~入~R~（动词对动词），~L~曾云~R~对~L~归鸟~R~（名词对名词）。对仗精工而不呆板，格律严谨而不失灵动，是五言律诗的典范。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">造化钟神秀，阴阳割昏晓。</div>
        <p>这两句是描写泰山的千古名句，上句写泰山的神秀，下句写泰山的高大。~L~钟~R~字用拟人手法，写大自然把神奇秀丽都聚集在泰山上；~L~割~R~字化静为动，写泰山使山南山北判若昏晓。一柔一刚，将泰山的形神写尽。这两句不仅写出了泰山的自然美，更体现了杜甫~L~语不惊人死不休~R~的炼字精神，是中国古典诗歌中炼字的典范。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">会当凌绝顶，一览众山小。</div>
        <p>全诗的点睛之笔，也是千古传诵的名句。化用《孟子·尽心上》~L~孔子登东山而小鲁，登泰山而小天下~R~的典故，但比孟子的话更凝练、更有力。~L~会当~R~写出了诗人的坚定信念，~L~凌~R~写出了凌云壮志，~L~一览众山小~R~写出了站在绝顶俯视一切的感受。这两句不仅写了泰山的高大，更抒发了诗人不怕困难、敢于攀登绝顶、俯视一切的雄心壮志，蕴含着~L~站得高，看得远~R~~L~只有攀登绝顶，才能超越一切~R~的深刻人生哲理。千百年来，这两句诗激励着无数人勇攀高峰、追求卓越，成为中华民族精神的重要象征。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《望岳》通过描写泰山的雄伟壮丽和神奇秀丽，抒发了青年杜甫不怕困难、敢于攀登绝顶、俯视一切的雄心壮志，表达了积极进取、乐观自信的人生态度和志存高远的精神追求。</p>
    <p>这首诗的深刻之处在于，它不仅是一首写景诗，更是一首言志诗。诗人以~L~望岳~R~为题，却不止于写岳——泰山的高大巍峨，正是诗人心中崇高理想的象征；~L~会当凌绝顶~R~的攀登之志，正是诗人对人生理想的追求。~L~一览众山小~R~的感受，既是站在泰山绝顶的真实体验，也是超越一切困难后的精神升华。这首诗写于杜甫的青年时期，是他一生积极进取精神的起点，即使在后来颠沛流离的岁月里，这种精神也从未熄灭。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 词类活用 · 炼字 · 文化常识</span></div>

  <div class="box">
    <h3>通假字</h3>
    <div class="tw"><table>
      <tr><th>字</th><th>通假</th><th>例句</th><th>释义</th></tr>
      <tr><td class="kai">曾</td><td>通~L~层~R~</td><td>荡胸生曾云</td><td>层层叠叠。读 céng</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">夫</td><td>句首发语词，无实义（fú）</td><td>丈夫（fū）</td><td>岱宗夫如何</td></tr>
      <tr><td class="kai">造化</td><td>天地、大自然</td><td>福气、运气（如~L~造化弄人~R~）</td><td>造化钟神秀</td></tr>
      <tr><td class="kai">阴阳</td><td>山北（阴）和山南（阳）</td><td>日月、男女、死生等抽象概念</td><td>阴阳割昏晓</td></tr>
      <tr><td class="kai">会当</td><td>终当、终要，表将来时</td><td>会议、应当（分开使用）</td><td>会当凌绝顶</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>词类活用</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">小</td><td>形容词意动用法</td><td>以……为小，觉得……渺小</td><td>一览众山小</td></tr>
      <tr><td class="kai">钟</td><td>名词作动词（拟人）</td><td>聚集、钟爱</td><td>造化钟神秀</td></tr>
      <tr><td class="kai">割</td><td>名词作动词（化静为动）</td><td>分割、划分</td><td>阴阳割昏晓</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>炼字赏析（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>钟——造化钟神秀</dt><dd>~L~钟~R~是聚集、钟爱的意思，用拟人手法，写大自然把天地间所有的神奇秀丽都聚集、钟爱在了泰山上。一个~L~钟~R~字，将大自然写得有情有义，也将泰山的神秀写到了极致。</dd></div>
      <div class="g-item"><dt>割——阴阳割昏晓</dt><dd>~L~割~R~是分割的意思，写泰山太高太大，山南山北的光线明暗截然不同，如同被一把巨大的刀割开了一样。一个~L~割~R~字，化静为动，将泰山的巍峨高大写得惊心动魄。</dd></div>
      <div class="g-item"><dt>入——决眦入归鸟</dt><dd>~L~入~R~是进入的意思，写归鸟飞进了诗人的视野之中。一个~L~入~R~字，写出了视野的辽远和诗人的目不转睛，仿佛鸟儿是主动~L~飞进~R~诗人眼中的，生动而有神。</dd></div>
      <div class="g-item"><dt>凌——会当凌绝顶</dt><dd>~L~凌~R~是登的意思，但~L~凌~R~比~L~登~R~更有力量——~L~凌~R~有高出、超越之意，~L~凌绝顶~R~不仅是登上山顶，更是超越一切、俯视一切。一个~L~凌~R~字，写出了诗人的凌云壮志。</dd></div>
    </div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">设问句</td><td>岱宗夫如何？齐鲁青未了。</td><td>自问自答，以设问起笔，引人入胜</td></tr>
      <tr><td class="kai">对仗句</td><td>造化钟神秀，阴阳割昏晓。</td><td>颔联对仗，名词对名词、动词对动词、形容词对形容词</td></tr>
      <tr><td class="kai">对仗句</td><td>荡胸生曾云，决眦入归鸟。</td><td>颈联对仗，动宾对动宾、动词对动词、名词对名词</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>岱宗</dt><dd>对泰山的尊称。岱，dài，泰山的别名；宗，首、大。泰山为五岳之首，故称~L~岱宗~R~。古代帝王封禅泰山，泰山在五岳中地位最高。</dd></div>
      <div class="g-item"><dt>五岳</dt><dd>中国五大名山的总称，即东岳泰山（山东泰安）、西岳华山（陕西华阴）、南岳衡山（湖南衡阳）、北岳恒山（山西浑源）、中岳嵩山（河南登封）。泰山为五岳之首。</dd></div>
      <div class="g-item"><dt>齐鲁</dt><dd>春秋时的两个诸侯国名，在今山东省一带。泰山以北为齐国，以南为鲁国。~L~齐鲁青未了~R~意思是在齐鲁两国的大地上，泰山的青翠山色绵延不尽。今山东省别称~L~齐鲁大地~R~。</dd></div>
      <div class="g-item"><dt>阴阳</dt><dd>古代以山北水南为阴，山南水北为阳。~L~阴阳割昏晓~R~中的~L~阴阳~R~指泰山的北面（阴）和南面（阳）。因为泰山高大，山南向阳（明亮），山北背阴（昏暗），所以说~L~割昏晓~R~。</dd></div>
      <div class="g-item"><dt>封禅</dt><dd>古代帝王在泰山举行的祭祀天地的大典。在泰山上筑土为坛以祭天，报天之功，称~L~封~R~；在泰山下的小山上辟场祭地，报地之功，称~L~禅~R~。封禅是古代最隆重的祭祀仪式，只有功业卓著的帝王才有资格举行。</dd></div>
      <div class="g-item"><dt>五言律诗</dt><dd>近体诗的一种，全诗八句，每句五字，共四十字。二、四、六、八句押韵，首句可押可不押。中间两联（颔联、颈联）必须对仗。《望岳》是五言律诗的典范之作。</dd></div>
      <div class="g-item"><dt>用典</dt><dd>~L~会当凌绝顶，一览众山小~R~化用了《孟子·尽心上》~L~孔子登东山而小鲁，登泰山而小天下~R~的典故。杜甫用~L~一览众山小~R~五个字，比孟子的话更凝练、更有力。用典使诗句内涵丰富，也体现了杜甫深厚的文化修养。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《望岳》杜甫</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">唐 · 杜甫</div>
  <h1 class="hero-title">望岳</h1>
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
  <div class="sec-sub">全诗八句，分两部分：远望泰山、近望与展望。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《望岳》</div>
  <div>杜甫 · 唐（712—770）· 开元年间作于漫游齐赵途中 · 五言律诗</div>
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
