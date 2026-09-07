# -*- coding: utf-8 -*-
"""生成《咏雪》交互式教学课件"""
import re, json, os

BENCH = r"D:\App\Apps\yanshi\jichengtiansiyeyou-sushi.html"
OUT = r"D:\App\Apps\yanshi\yongxue-shishuoxinyu.html"
LS_KEY = "yongxue_fs"

with open(BENCH, encoding="utf-8") as f:
    bench = f.read()

# 提取 CSS
css = bench[bench.index("<style>")+7:bench.index("</style>")]
# 提取主 JS (IIFE)
js_start = bench.index("<script>\n(function(){")
js_end = bench.index("</script>\n<script>\nvar DICT_WORDS")
main_js = bench[js_start+8:js_end]

# ========== 数据 ==========
HERO_SIDE = "南朝宋 · 刘义庆"
HERO_TITLE = "咏雪"
PAGE_TITLE = "《咏雪》刘义庆"

BG_LEAD = [
    "《咏雪》选自《世说新语·言语》，是南朝宋刘义庆组织门客编撰的志人小说集。全文仅七十余字，记述了东晋名士谢安一家在寒雪日咏雪联句的雅事，寥寥数笔便勾勒出谢家子弟的才情与风度。",
    "“未若柳絮因风起”一句，以春景喻冬雪，形神兼备，历来被视为咏雪绝唱。谢道韫也因此被称为“咏絮之才”，成为中国文学史上才女的代称。"
]

AUTHOR_BOX = [
    ("作者简介", [
        "刘义庆（403—444），南朝宋彭城（今江苏徐州）人，宋武帝刘裕之侄，袭封临川王。他爱好文学，招聚文学之士，组织编撰了《世说新语》《幽明录》等书。",
        "《世说新语》是我国最早的文言志人小说集，主要记载东汉末年至东晋间士族阶层的言谈轶事，分德行、言语、政事、文学等三十六门。语言精炼含蓄，隽永传神，对后世笔记文学影响深远。"
    ])
]

BG_BOX = [
    ("写作背景", [
        "<b>谢氏家族：</b>谢安（320—385），字安石，东晋政治家、名士，官至太保，死后追赠太傅，故称“谢太傅”。他出身陈郡谢氏，是东晋名门望族的代表人物。",
        "<b>咏絮之才：</b>文中“兄女”即谢道韫，谢安长兄谢无奕之女，后嫁王羲之次子王凝之。她以“柳絮因风起”喻雪，才思敏捷，后世遂以“咏絮才”称女子工于吟咏。",
        "<b>魏晋风度：</b>寒雪日内集、讲论文义、即兴咏雪，正是东晋士族清谈雅集生活的缩影。《世说新语》以极简笔法记录这类言谈轶事，展现了魏晋名士的才情与气度。"
    ])
]

# 视频
MEDIA = [
    ("《咏雪》诵读", "BV1bq4y1572q", "咏雪诵读"),
    ("趣味动画学《咏雪》", "BV1T84y1f7fB", "趣味动画学咏雪"),
]

# 逐句数据: (原文, 译文, 赏析, [(词,注释),...])
VERSES = [
    (
        "谢太傅寒雪日内集，与儿女讲论文义。",
        "谢太傅在一个寒冷的雪天把家人聚集在一起，跟子侄辈的人讲解谈论文章的义理。",
        "开篇交代时间、人物、事件，极简而要素俱全。“寒雪日”点出时令，“内集”“讲论文义”勾勒出谢家雅集的文化氛围——一个名门望族的家庭教育场景，如在目前。",
        [
            ("谢太傅", "即谢安，字安石，东晋政治家，死后追赠太傅，故称"),
            ("寒雪日", "寒冷的雪天"),
            ("内集", "把家人聚集在一起。内，家中；集，聚集"),
            ("儿女", "这里泛指子侄辈，不是专指儿子和女儿"),
            ("讲论", "讲解谈论"),
            ("文义", "文章的义理"),
        ]
    ),
    (
        "俄而雪骤，公欣然曰：“白雪纷纷何所似？”",
        "不久雪下得急了，谢太傅高兴地说：“这纷纷扬扬的白雪像什么呢？”",
        "“俄而”承接上文，见时间推移；“雪骤”二字写雪势由缓而急，正是触发咏兴的契机。谢安“欣然”一问，雅兴盎然，为下文两个比喻的出场搭建了舞台。",
        [
            ("俄而", "不久，一会儿"),
            ("骤", "急，紧。这里指雪下得急"),
            ("公", "指谢太傅（谢安）"),
            ("欣然", "高兴的样子"),
            ("何所似", "即“所似何”，像什么。似，像"),
        ]
    ),
    (
        "兄子胡儿曰：“撒盐空中差可拟。”",
        "他哥哥的长子胡儿说：“跟把盐撒在空中差不多可以相比。”",
        "胡儿即谢朗，谢安次兄谢据之子。以“撒盐空中”喻雪，取其色白与下落之态，形似而有神不足——盐粒沉重直落，缺乏雪花轻盈飘舞的意态。这个比喻虽平实，却也真切，为下文谢道韫的佳句做了铺垫与反衬。",
        [
            ("兄子", "哥哥的儿子，指谢朗"),
            ("胡儿", "谢朗的小名。谢朗，字长度，谢安次兄谢据之子"),
            ("差", "大致，差不多"),
            ("可拟", "可以相比。拟，相比"),
        ]
    ),
    (
        "兄女曰：“未若柳絮因风起。”",
        "他哥哥的女儿说：“不如比作柳絮凭借着风漫天飞舞。”",
        "全文点睛之笔。以“柳絮”喻雪，既取其色白轻盈，又取其随风飘舞之态，更兼春景的诗意联想——雪花本是寒冬之物，一经比柳絮，便有了春意与生机。“因风起”三字尤妙，写出雪花随风飘舞、漫天纷飞的动态美。形神兼备，意境悠远，故谢安“大笑乐”。",
        [
            ("兄女", "哥哥的女儿，指谢道韫，谢安长兄谢无奕之女"),
            ("未若", "不如，比不上"),
            ("柳絮", "柳树的种子，上面有白色绒毛，随风飞散如飘絮"),
            ("因", "趁，乘，凭借"),
        ]
    ),
    (
        "公大笑乐。",
        "谢太傅听了高兴得大笑起来。",
        "“大笑乐”三字收束对答，谢安的态度不言自明——他更欣赏“柳絮因风起”的比喻。不直接评判高下，而以“大笑乐”暗示褒贬，含蓄隽永，正是《世说新语》的笔法。",
        [
            ("大笑乐", "高兴得大笑起来。乐，快乐、高兴"),
        ]
    ),
    (
        "即公大兄无奕女，左将军王凝之妻也。",
        "（谢道韫）就是谢太傅大哥谢无奕的女儿，左将军王凝之的妻子。",
        "结尾补叙谢道韫的身份，看似闲笔，实则大有深意：点明她出身名门（谢无奕之女）、嫁入望族（王凝之妻，王羲之儿媳），更以郑重的身份介绍暗示作者对这位才女的推崇。“即……也”的判断句式，是史传笔法，为人物立传。",
        [
            ("即", "就是"),
            ("大兄", "大哥，指谢奕，字无奕"),
            ("无奕", "谢奕的字。谢奕，谢安长兄，官至安西将军、豫州刺史"),
            ("左将军", "武官名。王凝之曾任左将军"),
            ("王凝之", "王羲之次子，谢道韫的丈夫，曾任江州刺史、左将军、会稽内史"),
        ]
    ),
]

# 赏析区
APP_BOXES = [
    ("人物形象", [
        ("雅量高致的谢太傅", "谢安是这场雅集的主持者。他“寒雪日内集”“讲论文义”，见其重视家庭教育；雪骤而“欣然”发问，见其性情雅致、富有生活情趣；听完两个比喻“大笑乐”，不置褒贬而态度自明，见其含蓄深沉的名士风度。"),
        ("才思敏捷的谢道韫", "谢道韫是本文的主角。她以“未若柳絮因风起”七字，超越了堂兄“撒盐空中”的平实比喻，展现出超凡的文学才华与审美感受力。作者在结尾郑重补叙其身份，正是对这位“咏絮之才”的推崇。后世以“咏絮才”代指才女，即源于此。"),
    ]),
    ("艺术特色", [
        ("叙事极简，人物传神", "全文仅七十余字，却完整记述了一次家庭咏雪雅集的全过程。没有冗长的描写，只以“内集”“讲论”“欣然”“大笑乐”等关键词，便把谢安的雅量、胡儿的平实、道韫的才情勾勒得栩栩如生。"),
        ("对比衬托，佳句自显", "两个比喻并置：胡儿“撒盐空中”取形似，道韫“柳絮因风起”取神似。前者平实，后者灵动；前者有 winter 的沉重，后者有 spring 的轻盈。一经对比，高下立判，而作者不著一字评判，全凭读者自悟。"),
        ("以景写人，意在言外", "“柳絮因风起”不仅是咏雪佳句，更是谢道韫人格的写照——柳絮轻盈自由、随风起舞，正象征着她才情飘逸、不受拘束的精神世界。一句之妙，既在写景，更在写人。"),
        ("史传笔法，结尾点人", "结尾“即公大兄无奕女，左将军王凝之妻也”用判断句式补叙人物身份，是《世说新语》常见的史传笔法。看似闲笔，实则为谢道韫立传，暗示她才名之重，值得被郑重记载。"),
    ]),
    ("名句赏析", [
        ("未若柳絮因风起。", "咏雪千古名句。以柳絮喻雪，有三妙：一妙在形似——柳絮色白轻盈，与雪花外形相似；二妙在神似——柳絮随风飘舞，与雪花漫天飞舞的动态一致；三妙在意境——柳絮本是春景，以春景喻冬雪，化寒冷为温暖，化肃杀为生机，给人以无限美好的联想。“因风起”三字尤见功力，写出雪花随风起舞的轻盈姿态。"),
        ("白雪纷纷何所似？", "谢安的即兴一问，雅兴盎然。“纷纷”二字写出雪花漫天飞舞之态，“何所似”以问句激发晚辈才思，是整个咏雪故事的引子。此问本身也颇具诗意——面对纷纷白雪，人生又何尝不是在寻找一个恰当的比喻？"),
    ]),
    ("主题思想", [
        "本文通过记述谢安一家在寒雪日咏雪联句的雅事，展现了东晋士族家庭浓厚的文化氛围和教育方式，赞美了谢道韫超凡的文学才华与敏捷才思。",
        "“未若柳絮因风起”不仅是一句咏雪诗，更是一种审美理想——以轻盈灵动之心，观照世间万物。谢道韫的“咏絮之才”，千百年来激励着无数女性追求文学与智慧，成为中国文化史上一道独特的风景。"
    ]),
]

# 积累区
ACC = [
    ("通假字", [
        ("（本文无通假字）", "《咏雪》全文无通假字。"),
    ]),
    ("古今异义", [
        ("儿女", "古义：子侄辈，泛指家中年轻一代（与儿女讲论文义）；今义：儿子和女儿"),
        ("文义", "古义：文章的义理；今义：文章的意义"),
        ("因", "古义：趁、乘、凭借（未若柳絮因风起）；今义：因为"),
    ]),
    ("一词多义", [
        ("日", "天：寒雪日内集"),
        ("集", "聚集：寒雪日内集"),
        ("骤", "急：俄而雪骤"),
        ("似", "像：白雪纷纷何所似"),
        ("拟", "相比：撒盐空中差可拟"),
        ("若", "如，及：未若柳絮因风起"),
    ]),
    ("词类活用", [
        ("（本文无典型词类活用）", "《咏雪》中无典型的词类活用现象。"),
    ]),
    ("文言句式", [
        ("宾语前置", "“白雪纷纷何所似”即“白雪纷纷所似何”，“何”是“似”的宾语，前置"),
        ("判断句", "“即公大兄无奕女，左将军王凝之妻也”，“即……也”表判断"),
    ]),
    ("文化常识", [
        ("《世说新语》", "南朝宋刘义庆组织编撰的志人小说集，记载东汉末至东晋士族阶层言谈轶事，分三十六门。语言精炼含蓄，是魏晋风度的集中写照。"),
        ("谢太傅", "即谢安（320—385），字安石，东晋政治家，官至太保，死后追赠太傅。陈郡谢氏是东晋名门望族，与琅琊王氏并称“王谢”。"),
        ("咏絮之才", "源于谢道韫“未若柳絮因风起”的典故，后世用以称女子工于吟咏、富有才学。《红楼梦》中“可叹停机德，堪怜咏絮才”即以“咏絮才”指林黛玉。"),
        ("内集", "古人家庭聚会的一种形式，通常在雨雪等不宜外出的日子举行，内容包括讲论文义、吟诗作赋等，是士族家庭教育的重要方式。"),
        ("王凝之", "王羲之次子，谢道韫之夫。王氏家族是东晋另一名门望族，王羲之为“书圣”。王谢联姻，是东晋门阀政治的典型体现。"),
    ]),
]

# 题库
DICT_WORDS = [
    {"w":"骤","py":"zhòu","q":"俄而雪□","tip":"「骤」马字旁，急、紧义，读 zhòu；勿写「聚」「揍」"},
    {"w":"拟","py":"nǐ","q":"撒盐空中差可□","tip":"「拟」提手旁，相比义，读 nǐ；勿写「似」「疑」"},
    {"w":"絮","py":"xù","q":"未若柳□因风起","tip":"「絮」糸字旁（绞丝底），柳絮义，读 xù；勿写「恕」「紧」"},
    {"w":"奕","py":"yì","q":"即公大兄无□女","tip":"「奕」大字底，盛大义，用于人名，读 yì；勿写「弈」（下棋义）"},
    {"w":"凝","py":"níng","q":"左将军王□之妻也","tip":"「凝」两点水，凝结义，读 níng；勿写「疑」「疑」"},
    {"w":"傅","py":"fù","q":"谢太□寒雪日内集","tip":"「傅」单人旁，辅佐义，用于官名太傅，读 fù；勿写「博」「缚」"},
    {"w":"撒","py":"sǎ","q":"□盐空中差可拟","tip":"「撒」提手旁，散布义，读 sǎ；勿写「散」「撤」"},
]

DICT_NOTES = [
    {"w":"谢太傅","a":"即谢安，字安石，东晋政治家，死后追赠太傅","q":"谢太傅寒雪日内集"},
    {"w":"内集","a":"把家人聚集在一起","q":"谢太傅寒雪日内集"},
    {"w":"儿女","a":"这里泛指子侄辈，不是专指儿子和女儿","q":"与儿女讲论文义"},
    {"w":"文义","a":"文章的义理","q":"与儿女讲论文义"},
    {"w":"俄而","a":"不久，一会儿","q":"俄而雪骤"},
    {"w":"骤","a":"急，紧","q":"俄而雪骤"},
    {"w":"欣然","a":"高兴的样子","q":"公欣然曰"},
    {"w":"何所似","a":"即“所似何”，像什么","q":"白雪纷纷何所似"},
    {"w":"兄子","a":"哥哥的儿子","q":"兄子胡儿曰"},
    {"w":"胡儿","a":"谢朗的小名","q":"兄子胡儿曰"},
    {"w":"差","a":"大致，差不多","q":"撒盐空中差可拟"},
    {"w":"可拟","a":"可以相比。拟，相比","q":"撒盐空中差可拟"},
    {"w":"兄女","a":"哥哥的女儿，指谢道韫","q":"兄女曰"},
    {"w":"未若","a":"不如，比不上","q":"未若柳絮因风起"},
    {"w":"柳絮","a":"柳树的种子，上面有白色绒毛，随风飞散如飘絮","q":"未若柳絮因风起"},
    {"w":"因","a":"趁，乘，凭借","q":"未若柳絮因风起"},
    {"w":"大笑乐","a":"高兴得大笑起来","q":"公大笑乐"},
    {"w":"即","a":"就是","q":"即公大兄无奕女"},
    {"w":"大兄","a":"大哥","q":"即公大兄无奕女"},
    {"w":"无奕","a":"谢奕的字，谢安长兄","q":"即公大兄无奕女"},
    {"w":"王凝之","a":"王羲之次子，谢道韫的丈夫","q":"左将军王凝之妻也"},
]

# ========== 生成 HTML ==========
def make_media():
    items = []
    for i, (title, bv, t) in enumerate(MEDIA):
        fid = f"mediaF{i+1}"
        items.append(f'''<div class="media"><h4>{title}</h4><iframe id="{fid}" src="https://player.bilibili.com/player.html?bvid={bv}&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="{t}"></iframe><a href="https://www.bilibili.com/video/{bv}" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="{fid}">全屏播放</button></div>''')
    return "\n".join(items)

def make_bg():
    parts = ['<div class="lead">']
    for p in BG_LEAD:
        parts.append(f"<p>{p}</p>")
    parts.append("</div>")
    for title, paras in AUTHOR_BOX:
        parts.append(f'<div class="box"><h3>{title}</h3>')
        for p in paras:
            parts.append(f"<p>{p}</p>")
        parts.append("</div>")
    for title, paras in BG_BOX:
        parts.append(f'<div class="box"><h3>{title}</h3>')
        for p in paras:
            parts.append(f"<p>{p}</p>")
        parts.append("</div>")
    parts.append(f'<div class="box media-box"><h3>视听</h3><div class="media-grid">{make_media()}</div></div>')
    return "\n".join(parts)

def annotate(text, zhushi):
    """给原文加注释 span"""
    result = text
    # 按词长降序排列，避免短词先匹配
    for word, note in sorted(zhushi, key=lambda x: -len(x[0])):
        if word in result:
            # 只替换第一次出现（每句独立）
            idx = result.index(word)
            # 检查是否已在 span 中
            before = result[:idx]
            if before.count('<span class="anno-word"') > before.count('</span>'):
                continue  # 已在 span 内
            escaped_note = note.replace('"', '&quot;')
            replacement = f'<span class="anno-word" data-note="{escaped_note}">{word}</span>'
            result = result[:idx] + replacement + result[idx+len(word):]
    return result

def make_verses():
    parts = []
    for i, (orig, trans, appr, zhushi) in enumerate(VERSES):
        annotated = annotate(orig, zhushi)
        parts.append(f'''<div class="verse" id="l{i+1}" data-i="{i}">
  <div class="v-top"><span class="v-no">{i+1}</span><div class="v-line">{annotated}</div></div>
  <details class="v-more">
    <summary>译文 · 赏析</summary>
    <div class="d-body">
      <div class="v-sec"><b class="v-label">译　文</b>
        <div class="v-trans">{trans}</div>
      </div>
      <div class="v-sec"><b class="v-label">赏　析</b>
        <div class="d-body"><p>{appr}</p></div>
      </div>
    </div>
  </details>
</div>''')
    return "\n".join(parts)

def make_fulltext():
    parts = ['<div id="fulltext" class="poem" style="display:none">']
    for orig, _, _, _ in VERSES:
        parts.append(f'<div class="pl">{orig}</div>')
    parts.append("</div>")
    return "\n".join(parts)

def make_app():
    parts = []
    for title, items in APP_BOXES:
        parts.append(f'<div class="box"><h3>{title}</h3>')
        if title in ("人物形象", "艺术特色", "名句赏析"):
            parts.append('<div class="fame">')
            for sub, content in items:
                parts.append(f'<div class="fame-card"><div class="f-line">{sub}</div><p>{content}</p></div>')
            parts.append("</div>")
        else:
            for p in items:
                parts.append(f"<p>{p}</p>")
        parts.append("</div>")
    return "\n".join(parts)

def make_acc():
    parts = []
    for cat, items in ACC:
        parts.append(f'<div class="box"><div class="acc-cat"><h3>{cat}</h3>')
        for w, d in items:
            parts.append(f'<div class="acc-item"><span class="acc-w">{w}</span><span class="acc-d">{d}</span></div>')
        parts.append("</div></div>")
    return "\n".join(parts)

# 替换 localStorage key
main_js = main_js.replace("chengtian_fs", LS_KEY)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{PAGE_TITLE}</title>
<style>
{css}
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">{HERO_SIDE}</div>
  <h1 class="hero-title">{HERO_TITLE}</h1>
</header>

<nav class="nav"><div class="nav-in"><a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a><div class="tool"><select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option></select><button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button></div></div></nav>

<main class="wrap">
<section id="bg" class="sec">
<div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
{make_bg()}
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>
<div class="sec-sub">全文七十余字，分六句逐句解读。每句含注释、译文与赏析，点击可展开。</div>
<button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
{make_fulltext()}
<div class="verse-list" id="verseList">
{make_verses()}
</div></section>

<div class="divider"></div>
<section id="app" class="sec">
<div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>
{make_app()}
</section>

<div class="divider"></div>
<section id="acc" class="sec">
<div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 一词多义 · 活用 · 句式 · 文化常识</span></div>
{make_acc()}
</section>

<div class="divider"></div>
<section id="practice" class="sec">
<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>
<div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>
<div class="ptools"><button data-mode="word" data-rand="5">随机五组字形</button><button data-mode="word" data-all="1">全部字形</button><button data-mode="note" data-rand="5">随机五组注释</button><button data-mode="note" data-all="1">全部注释</button></div></section>

<footer>
  <div class="kai">《咏雪》</div>
  <div>刘义庆 · 南朝宋（403—444）· 选自《世说新语·言语》</div>
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
var DICT_WORDS = {json.dumps(DICT_WORDS, ensure_ascii=False)};
var DICT_NOTES = {json.dumps(DICT_NOTES, ensure_ascii=False)};
</script>

</body>
</html>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated: {OUT}")
print(f"Size: {os.path.getsize(OUT)} bytes")
