# -*- coding: utf-8 -*-
"""《黄鹤楼》崔颢 课件生成器 —— 复用《背影》CSS/JS框架。
古诗版式：逐句解读，卡片summary用"译文 · 赏析"。
短篇不分part直接逐句。积累区用古诗骨架。"""
import json, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'huanghelou-cuihao.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'huanghelou_fs')


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


def annotate_text(text, word_list):
    items = sorted(word_list, key=lambda x: -len(x[0]))
    used = set()
    for w, n in items:
        if w in used:
            continue
        idx = text.find(w)
        while idx != -1:
            before = text[:idx]
            open_count = before.count('<span class="anno-word"')
            close_count = before.count('</span>')
            if open_count > close_count:
                idx = text.find(w, idx + 1)
                continue
            replacement = '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
            text = text[:idx] + replacement + text[idx + len(w):]
            used.add(w)
            break
    return text


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "昔人已乘黄鹤去，此地空余黄鹤楼。",
    "黄鹤一去不复返，白云千载空悠悠。",
    "晴川历历汉阳树，芳草萋萋鹦鹉洲。",
    "日暮乡关何处是？烟波江上使人愁。",
]

# 每句注释词表（文言字词：读音+释义+用法）
ANNO = [
    [("昔人", "前人，这里指传说中乘鹤登仙的费祎（yī）。昔，从前。"), ("已", "已经。副词。"), ("乘", "驾着、乘坐。"), ("黄鹤", "黄色的鹤，传说中仙人的坐骑。"), ("去", "离开。"), ("此地", "这个地方，指黄鹤楼。"), ("空余", "只剩下。空，只、仅仅。余，剩下。"), ("黄鹤楼", "楼名，在今湖北武汉武昌蛇山，下临长江。")],
    [("一去", "一旦离开。一，一旦。"), ("不复返", "不再回来。复，再。返，返回。"), ("白云", "白色的云。"), ("千载", "（zǎi）千年。载，年。形容时间久远。"), ("空", "徒然、白白地。副词。"), ("悠悠", "（yōu yōu）悠闲自在的样子，这里形容白云飘荡。")],
    [("晴川", "晴朗的江面。川，河流、平地。"), ("历历", "（lì lì）分明可数的样子。"), ("汉阳", "地名，在今湖北武汉，与黄鹤楼隔江相望。"), ("树", "树木。"), ("芳草", "芬芳的青草。"), ("萋萋", "（qī qī）草木茂盛的样子。"), ("鹦鹉洲", "长江中的沙洲，在今湖北武汉西南，因东汉末年祢衡曾作《鹦鹉赋》而得名。")],
    [("日暮", "傍晚。暮，傍晚。"), ("乡关", "故乡。关，这里指家乡。"), ("何处是", "在哪里。何处，哪里。"), ("烟波", "烟雾笼罩的江面。"), ("江上", "长江之上。"), ("使人愁", "让人感到忧愁。使，让。愁，忧愁、乡愁。")],
]

# 每句: (译文, 赏析)
YISHANG = [
    ("传说中的仙人早已乘着黄鹤飞去，这里只留下一座空荡荡的黄鹤楼。",
     "首联从神话传说落笔，写黄鹤楼的由来。~L~昔人已乘黄鹤去~R~，仙人乘鹤而去，一去不返；~L~此地空余黄鹤楼~R~，只留下一座空楼。~L~空~R~字奠定全诗怅惘的基调，虚实结合，引出下文。"),
    ("黄鹤飞去以后再也没有回来，千百年来只有白云在天空中飘飘荡荡。",
     "颔联紧承首联，进一步写岁月流逝、世事苍茫。~L~不复返~R~写仙人一去不回，~L~空悠悠~R~写白云千载依旧。以白云的~L~悠悠~R~反衬人生的短暂，意境开阔，感慨深沉。"),
    ("晴朗的江面，汉阳的树木清晰可见；芬芳的芳草，长得十分茂盛，那是鹦鹉洲。",
     "颈联转写登楼所见的明丽景色。~L~历历~R~写树木清晰可数，~L~萋萋~R~写芳草茂盛。对仗工整，画面明丽，与上联的苍茫形成对比，为尾联的乡愁做铺垫。"),
    ("天色已晚，眺望远方，故乡在哪儿呢？眼前只见一片雾霭笼罩的江面，给人带来深深的愁绪。",
     "尾联由景入情，点明主旨。~L~日暮~R~呼应首联的仙人乘鹤，~L~乡关何处是~R~以设问写乡愁，~L~烟波江上使人愁~R~以景结情，将乡愁融入浩渺的烟波之中，余味无穷。"),
]

# Build verses
verses_html_parts = []
for i in range(4):
    annotated = annotate_text(FULLTEXT[i], ANNO[i])
    idx = i + 1
    verses_html_parts.append('      <div class="verse" id="l%d" data-i="%d">' % (idx, idx - 1))
    verses_html_parts.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx, fixq(annotated)))
    verses_html_parts.append('        <details class="v-more">')
    verses_html_parts.append('          <summary>译文 · 赏析</summary>')
    verses_html_parts.append('          <div class="d-body">')
    verses_html_parts.append('            <div class="v-sec"><b class="v-label">译文</b>')
    verses_html_parts.append('              <div class="v-trans">%s</div>' % fixq(YISHANG[i][0]))
    verses_html_parts.append('            </div>')
    verses_html_parts.append('            <div class="v-sec"><b class="v-label">赏析</b>')
    verses_html_parts.append('              <div class="d-body"><p>%s</p></div>' % fixq(YISHANG[i][1]))
    verses_html_parts.append('            </div>')
    verses_html_parts.append('          </div>')
    verses_html_parts.append('        </details>')
    verses_html_parts.append('      </div>')
verses_html = '\n'.join(verses_html_parts)
full_html = '\n'.join('    <div class="pl">%s</div>' % fixq(p) for p in FULLTEXT)
anno_count = sum(len(a) for a in ANNO)


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"鹤鹤","py":"hè hè","q":"昔人已乘黄□去，此地空余黄□楼","tip":"「鹤」鸟字旁，音 hè，仙鹤，勿写「鹊」（què）"},
    {"w":"载","py":"zǎi","q":"白云千□空悠悠","tip":"「载」车字旁，音 zǎi，年；又音 zài，装载。此处读 zǎi"},
    {"w":"悠悠","py":"yōu yōu","q":"白云千载空□□","tip":"「悠」心字底，音 yōu，悠闲，「悠悠」形容飘荡，勿写「忧」（竖心旁）"},
    {"w":"历历","py":"lì lì","q":"晴川□□汉阳树，芳草萋萋鹦鹉洲","tip":"「历」厂字头，音 lì，分明，「历历」指清晰可数，勿写「厉」（厂字头，严厉）"},
    {"w":"萋萋","py":"qī qī","q":"晴川历历汉阳树，芳草□□鹦鹉洲","tip":"「萋」草字头，音 qī，茂盛，「萋萋」形容草木茂盛，勿写「凄」（两点水）"},
    {"w":"鹦","py":"yīng","q":"芳草萋萋□鹉洲","tip":"「鹦」鸟字旁，音 yīng，「鹦鹉」，鸟名，勿写「樱」（木字旁）"},
    {"w":"鹉","py":"wǔ","q":"芳草萋萋鹦□洲","tip":"「鹉」鸟字旁，音 wǔ，「鹦鹉」，勿写「武」（止字旁）"},
    {"w":"暮","py":"mù","q":"日□乡关何处是？烟波江上使人愁","tip":"「暮」日字底，音 mù，傍晚，勿写「幕」（巾字底）"},
]

DICT_NOTES = [
    {"w":"昔人","a":"前人，这里指传说中乘鹤登仙的费祎","q":"昔人已乘黄鹤去"},
    {"w":"乘","a":"驾着、乘坐","q":"昔人已乘黄鹤去"},
    {"w":"空余","a":"只剩下。空，只、仅仅。余，剩下","q":"此地空余黄鹤楼"},
    {"w":"不复返","a":"不再回来。复，再。返，返回","q":"黄鹤一去不复返"},
    {"w":"千载","a":"（zǎi）千年。载，年。形容时间久远","q":"白云千载空悠悠"},
    {"w":"悠悠","a":"（yōu yōu）悠闲自在的样子，这里形容白云飘荡","q":"白云千载空悠悠"},
    {"w":"晴川","a":"晴朗的江面。川，河流、平地","q":"晴川历历汉阳树"},
    {"w":"历历","a":"（lì lì）分明可数的样子","q":"晴川历历汉阳树"},
    {"w":"萋萋","a":"（qī qī）草木茂盛的样子","q":"芳草萋萋鹦鹉洲"},
    {"w":"鹦鹉洲","a":"长江中的沙洲，因祢衡曾作《鹦鹉赋》而得名","q":"芳草萋萋鹦鹉洲"},
    {"w":"日暮","a":"傍晚。暮，傍晚","q":"日暮乡关何处是"},
    {"w":"乡关","a":"故乡。关，这里指家乡","q":"日暮乡关何处是"},
    {"w":"烟波","a":"烟雾笼罩的江面","q":"烟波江上使人愁"},
    {"w":"使人愁","a":"让人感到忧愁。使，让。愁，忧愁、乡愁","q":"烟波江上使人愁"},
    {"w":"去","a":"离开","q":"昔人已乘黄鹤去"},
    {"w":"此地","a":"这个地方，指黄鹤楼","q":"此地空余黄鹤楼"},
    {"w":"一去","a":"一旦离开。一，一旦","q":"黄鹤一去不复返"},
    {"w":"空","a":"徒然、白白地。副词","q":"白云千载空悠悠"},
    {"w":"汉阳","a":"地名，在今湖北武汉，与黄鹤楼隔江相望","q":"晴川历历汉阳树"},
    {"w":"芳草","a":"芬芳的青草","q":"芳草萋萋鹦鹉洲"},
]


# ---------------- 组装 ----------------
BG = fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《黄鹤楼》是唐代诗人崔颢的代表作，被誉为唐人七律第一。诗人登临黄鹤楼，由楼名联想到仙人乘鹤的传说，又由眼前的明丽秋景生发出浓浓的乡愁，写下了这首意境开阔、情景交融的千古名篇。</p>
    <p>传说李白登黄鹤楼时，见到崔颢此诗，赞叹道：~L~眼前有景道不得，崔颢题诗在上头。~R~可见此诗的艺术成就之高。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>崔颢（hào）（？—754），汴州（今河南开封）人，唐代诗人。开元十一年（723）进士，官至司勋员外郎。他早年诗风浮艳，后经历边塞生活，诗风变为雄浑奔放。</p>
    <p>崔颢的诗现存四十余首，《黄鹤楼》是其最著名的作品。严羽《沧浪诗话》评：~L~唐人七言律诗，当以崔颢《黄鹤楼》为第一。~R~有《崔颢集》。</p>
  </div>
  <div class="box">
    <h3>黄鹤楼与神话传说</h3>
    <p><b>黄鹤楼：</b>位于今湖北武汉武昌蛇山，下临长江，是江南三大名楼之一（另两座为岳阳楼、滕王阁）。始建于三国吴黄武二年（223），历代屡毁屡建。</p>
    <p><b>乘鹤传说：</b>传说古代有一位名叫费祎（yī）的仙人，曾在黄鹤楼乘鹤登仙。又有传说称，有一位辛姓妇人在黄鹤楼卖酒，有道士为感谢她的千杯之赠，在墙上画了一只黄鹤，告知拍手即舞。后道士乘鹤而去，辛氏遂建此楼纪念。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p>崔颢一生仕途不得意，曾漫游四方。《黄鹤楼》写于他漫游江汉、登临黄鹤楼之时。诗人由楼名联想到仙人乘鹤的传说，又由眼前的景色生发出乡愁，写下了这首名篇。</p>
    <p>此诗虽题为~L~黄鹤楼~R~，但并不局限于写楼，而是由楼及人、由景及情，将神话传说、眼前景色和个人乡愁融为一体，意境开阔，感慨深沉。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>古诗朗读《黄鹤楼》崔颢</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1qA14YREeL&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="古诗朗读《黄鹤楼》"></iframe>
        <a href="https://www.bilibili.com/video/BV1qA14YREeL" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>古诗赏析《黄鹤楼》崔颢</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1pR4y1o7MT&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="古诗赏析《黄鹤楼》"></iframe>
        <a href="https://www.bilibili.com/video/BV1pR4y1o7MT" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">艺术 · 主题 · 名句</span></div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">虚实结合，意境开阔</div>
        <p>首联从神话传说落笔（虚写），写仙人乘鹤而去；颔联紧承，写白云千载依旧（实中含虚）；颈联转写登楼所见的明丽景色（实写）；尾联由景入情，抒发乡愁（虚实相生）。全诗虚实结合，意境开阔，将神话、历史、现实融为一体。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">气势奔腾，一气呵成</div>
        <p>首联~L~昔人已乘黄鹤去，此地空余黄鹤楼~R~，颔联~L~黄鹤一去不复返，白云千载空悠悠~R~，两联连用三个~L~黄鹤~R~，气势奔腾，一气呵成。虽不完全符合律诗的平仄对仗要求，但意脉贯通，自然流畅，被称为~L~七律第一~R~。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">情景交融，以景结情</div>
        <p>颈联写~L~晴川历历汉阳树，芳草萋萋鹦鹉洲~R~的明丽景色，反衬尾联的乡愁；~L~日暮乡关何处是？烟波江上使人愁~R~以设问引出乡愁，以浩渺的烟波作结，将抽象的乡愁融入具体的景物之中，情景交融，余味无穷。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">叠词传神，音韵优美</div>
        <p>~L~悠悠~R~写白云飘荡，~L~历历~R~写树木清晰，~L~萋萋~R~写芳草茂盛。三组叠词，既增强了诗歌的节奏感和音韵美，又生动地描绘了景物的特征，使画面更加鲜明可感。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《黄鹤楼》通过描写登临黄鹤楼所见的景色，抒发了诗人漂泊异乡的孤独寂寞和对故乡的深切思念，同时也表达了对世事苍茫、岁月流逝的感慨。</p>
    <p>诗人由楼名联想到仙人乘鹤的传说，感叹仙人一去不返、白云千载依旧；又由眼前的明丽秋景，在日暮时分生发出浓浓的乡愁。全诗将神话传说、眼前景色和个人情感融为一体，意境开阔，感情真挚，是唐代七言律诗的巅峰之作。</p>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">~L~黄鹤一去不复返，白云千载空悠悠~R~</div>
        <p>这两句是全诗的名句。仙人乘鹤一去不返，只留下白云在天空中悠悠飘荡，千年不变。~L~不复返~R~写时间的一去不回，~L~空悠悠~R~写空间的辽阔永恒。以白云的~L~悠悠~R~反衬人生的短暂，以自然的永恒反衬世事的变迁，意境开阔，感慨深沉。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">~L~晴川历历汉阳树，芳草萋萋鹦鹉洲~R~</div>
        <p>这两句对仗工整，画面明丽。~L~历历~R~写汉阳树木清晰可数，~L~萋萋~R~写鹦鹉洲芳草茂盛。诗人登楼远眺，所见景色明丽如画，但这明丽的景色反而勾起了他的乡愁——以乐景写哀情，为尾联的抒情做了有力的铺垫。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">~L~日暮乡关何处是？烟波江上使人愁~R~</div>
        <p>尾联以设问开篇，~L~乡关何处是~R~问得急切而茫然；~L~烟波江上使人愁~R~以景结情，将乡愁融入浩渺的烟波之中。~L~愁~R~字点明主旨，却不直说愁什么，留给读者无限的想象空间，余味悠长。</p>
      </div>
    </div>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 考点 · 修辞 · 文化</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>文体与格律</h3>
      <div class="acc-item"><span class="acc-w">七言律诗</span><span class="acc-d">简称~L~七律~R~，近体诗的一种，每首八句，每句七字，共五十六字。要求颔联、颈联对仗，平仄协调，押韵严格。</span></div>
      <div class="acc-item"><span class="acc-w">押韵</span><span class="acc-d">本诗押~L~尤~R~韵：楼（lóu）、悠（yōu）、洲（zhōu）、愁（chóu），韵脚在二、四、六、八句。</span></div>
      <div class="acc-item"><span class="acc-w">对仗</span><span class="acc-d">颈联~L~晴川历历汉阳树，芳草萋萋鹦鹉洲~R~对仗工整。首联、颔联不完全对仗，是此诗的特点。</span></div>
      <div class="acc-item"><span class="acc-w">变格</span><span class="acc-d">此诗前两联不完全符合律诗平仄，被称为~L~变格~R~，但意脉贯通，自然流畅，被誉为~L~七律第一~R~。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>易错字音形</h3>
      <div class="acc-item"><span class="acc-w">鹤</span><span class="acc-d">（hè）鸟字旁，仙鹤。不读 hé，不写~L~鹊~R~（què）。</span></div>
      <div class="acc-item"><span class="acc-w">载</span><span class="acc-d">（zǎi）年。~L~千载~R~即千年。又音 zài（装载）。此处读 zǎi。</span></div>
      <div class="acc-item"><span class="acc-w">悠</span><span class="acc-d">（yōu）心字底，悠闲。与~L~忧~R~（竖心旁，忧愁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">历</span><span class="acc-d">（lì）厂字头，分明。~L~历历~R~指清晰可数。与~L~厉~R~（严厉）区分。</span></div>
      <div class="acc-item"><span class="acc-w">萋</span><span class="acc-d">（qī）草字头，茂盛。~L~萋萋~R~形容草木茂盛。与~L~凄~R~（两点水，凄凉）区分。</span></div>
      <div class="acc-item"><span class="acc-w">鹦</span><span class="acc-d">（yīng）鸟字旁，~L~鹦鹉~R~。与~L~樱~R~（木字旁，樱桃）区分。</span></div>
      <div class="acc-item"><span class="acc-w">暮</span><span class="acc-d">（mù）日字底，傍晚。与~L~幕~R~（巾字底，帷幕）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文言梳理</h3>
      <div class="acc-sub">一词多义</div>
      <div class="acc-item"><span class="acc-w">空</span><span class="acc-d">①只、仅仅（空余）；②徒然、白白地（空悠悠）；③天空（晴空）。</span></div>
      <div class="acc-item"><span class="acc-w">去</span><span class="acc-d">①离开（乘鹤去）；②距离（相去甚远）；③除掉（去粗取精）。</span></div>
      <div class="acc-item"><span class="acc-w">使</span><span class="acc-d">①让（使人愁）；②出使（出使匈奴）；③使者（使者）。</span></div>
      <div class="acc-sub">古今异义</div>
      <div class="acc-item"><span class="acc-w">乡关</span><span class="acc-d">古义：故乡。今义：乡里的关口。</span></div>
      <div class="acc-item"><span class="acc-w">历历</span><span class="acc-d">古义：分明可数的样子。今义：（物体或景象）一个一个清清楚楚。</span></div>
      <div class="acc-sub">词类活用</div>
      <div class="acc-item"><span class="acc-w">烟波</span><span class="acc-d">名词作状语，在烟波之上（烟波江上使人愁）。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>核心考点</h3>
      <div class="acc-item"><span class="acc-w">用典/神话</span><span class="acc-d">首联化用仙人乘鹤的传说，需掌握其含义和作用——以神话起笔，增添黄鹤楼的神秘色彩，引出世事苍茫之感。</span></div>
      <div class="acc-item"><span class="acc-w">~L~空~R~字赏析</span><span class="acc-d">~L~空余~R~的~L~空~R~是~L~只~R~，~L~空悠悠~R~的~L~空~R~是~L~徒然~R~，两个~L~空~R~字分别写空间的空荡和时间的徒劳，是全诗的诗眼。</span></div>
      <div class="acc-item"><span class="acc-w">以乐景写哀情</span><span class="acc-d">颈联明丽的景色反衬尾联的乡愁，需掌握这种反衬手法的表达效果。</span></div>
      <div class="acc-item"><span class="acc-w">叠词作用</span><span class="acc-d">~L~悠悠~R~~L~历历~R~~L~萋萋~R~三组叠词的表达效果：增强节奏感，描绘景物特征。</span></div>
      <div class="acc-item"><span class="acc-w">以景结情</span><span class="acc-d">尾联~L~烟波江上使人愁~R~以景结情，将乡愁融入烟波之中，含蓄不尽。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞与手法</h3>
      <div class="acc-item"><span class="acc-w">对偶（对仗）</span><span class="acc-d">颈联对仗工整，是律诗的基本要求。</span></div>
      <div class="acc-item"><span class="acc-w">叠词</span><span class="acc-d">~L~悠悠~R~~L~历历~R~~L~萋萋~R~，增强节奏感和音韵美。</span></div>
      <div class="acc-item"><span class="acc-w">设问</span><span class="acc-d">~L~日暮乡关何处是？~R~以设问引出乡愁，增强抒情效果。</span></div>
      <div class="acc-item"><span class="acc-w">反衬</span><span class="acc-d">以明丽的秋景反衬乡愁，以乐景写哀情。</span></div>
      <div class="acc-item"><span class="acc-w">虚实结合</span><span class="acc-d">神话传说（虚）与眼前景色（实）结合，意境开阔。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">江南三大名楼</span><span class="acc-d">黄鹤楼（湖北武汉）、岳阳楼（湖南岳阳）、滕王阁（江西南昌）。</span></div>
      <div class="acc-item"><span class="acc-w">乘鹤传说</span><span class="acc-d">传说费祎在黄鹤楼乘鹤登仙；又有辛氏卖酒、道士画鹤的故事。黄鹤楼因此得名。</span></div>
      <div class="acc-item"><span class="acc-w">鹦鹉洲</span><span class="acc-d">长江中的沙洲，因东汉末年祢衡曾作《鹦鹉赋》而得名。祢衡后被黄祖所杀，葬于此洲。</span></div>
      <div class="acc-item"><span class="acc-w">李白与黄鹤楼</span><span class="acc-d">传说李白登黄鹤楼见崔颢诗，叹~L~眼前有景道不得，崔颢题诗在上头~R~，后作《登金陵凤凰台》仿效。</span></div>
      <div class="acc-item"><span class="acc-w">唐人七律第一</span><span class="acc-d">严羽《沧浪诗话》评~L~唐人七言律诗，当以崔颢《黄鹤楼》为第一~R~。</span></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《黄鹤楼》崔颢</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">唐 · 崔颢</div>
  <h1 class="hero-title">黄鹤楼</h1>
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
  <div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 译文 · 赏析</span></div>
  <div class="sec-sub">七言律诗，八句四联。每句含译文与赏析，点击可展开。</div>
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
  <div class="kai">《黄鹤楼》</div>
  <div>崔颢 · 唐 · 七言律诗 · 登临抒怀</div>
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

HTML = fixq(HTML)
io.open(OUT, 'w', encoding='utf-8').write(HTML)
print('OK', OUT, 'verses=4', 'anno=', anno_count, 'words=', len(DICT_WORDS), 'notes=', len(DICT_NOTES))
