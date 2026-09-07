# -*- coding: utf-8 -*-
"""生成《我为什么而活着》罗素 课件"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\woweishimeerhuozhe-luosu.html"
FS_KEY = "weishenme_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

paragraphs = [
    (
        "三种单纯然而极其强烈的激情支配着我的一生。那就是对于爱情的渴望，对于知识的追求，以及对于人类苦难痛彻肺腑的怜悯。这些激情犹如狂风，把我伸展到绝望边缘的深深的苦海上东抛西掷，使我的生活没有定向。",
        "开篇点明支配一生的三种激情：对爱情的渴望、对知识的追求、对人类苦难的怜悯。以狂风中的苦海为喻，写这三种激情给人生带来的动荡与不安。",
        "开门见山，总领全文；“三种……激情”构成全文的纲领；“犹如狂风”“东抛西掷”的比喻，将抽象的情感化为可感的画面，写出激情的强烈与不可控；“绝望边缘”“深深的苦海”渲染人生的痛苦，为下文张本。",
        [
            ("支配", "对人或事物起引导和控制的作用"),
            ("单纯", "简单、不复杂"),
            ("极其", "非常、极端"),
            ("渴望", "迫切地希望"),
            ("追求", "用积极的行动来争取达到某种目的"),
            ("痛彻肺腑", "形容极度痛苦，好像穿透了肺腑"),
            ("怜悯", "对遭遇不幸的人表示同情"),
            ("犹如", "好像、如同"),
            ("绝望", "希望断绝、毫无希望"),
            ("东抛西掷", "形容被风吹得左右摇摆、没有定向"),
            ("定向", "确定的方向"),
        ],
    ),
    (
        "我追求爱情，首先因为它叫我销魂，爱情的魔力往往让我愿意为了几小时的欢愉而牺牲生命中的其他一切。我追求爱情，其次是因为它能减轻孤独——一颗颤抖的灵魂在世界的边缘，俯瞰那冰冷死寂、深不可测的深渊。我追求爱情，最后是因为在爱情的结合中，我看到了圣徒和诗人们所想象的天堂景象的神秘缩影。这就是我所追求的，虽然这对人生似乎过于美好，然而最终我还是得到了它。",
        "阐述追求爱情的三个原因：叫人销魂、减轻孤独、看到天堂的缩影。爱情是人生最美好的体验，作者最终得到了它。",
        "“首先……其次……最后……”层层递进，条理清晰；“销魂”写爱情的狂喜；“颤抖的灵魂”“冰冷死寂、深不可测的深渊”写孤独的可怕，以反衬爱情的可贵；“天堂景象的神秘缩影”将爱情神圣化；“过于美好”“最终还是得到了它”，先抑后扬，见爱情的珍贵。",
        [
            ("销魂", "灵魂离开肉体，形容极度快乐、陶醉"),
            ("魔力", "神奇的、使人迷惑的力量"),
            ("欢愉", "欢乐愉快"),
            ("牺牲", "为了正义的目的舍弃自己的利益或生命"),
            ("减轻", "使程度减少、变轻"),
            ("孤独", "独自一个、孤单"),
            ("颤抖", "哆嗦、发抖"),
            ("俯瞰", "（fǔ kàn）从高处往下看"),
            ("死寂", "没有一丝生气，形容极其安静"),
            ("深不可测", "深得无法测量，比喻情况捉摸不透"),
            ("深渊", "很深的水，比喻险境或痛苦的境地"),
            ("圣徒", "虔诚而有德行的宗教徒"),
            ("缩影", "可以代表同一类型的具体而微的人或事物"),
        ],
    ),
    (
        "我以同样的热情寻求知识。我希望了解人的心灵。我希望知道星星为什么闪闪发光，我试图理解毕达哥拉斯的思想威力，即数字支配着万物流转。这方面我获得一些成就，然而并不多。",
        "阐述对知识的追求：了解人的心灵、探索自然奥秘、理解哲学思想。虽然有所成就，但并不多，体现了学者的谦逊。",
        "“同样的热情”承接上文，将知识与爱情并提；“了解人的心灵”“知道星星为什么闪闪发光”“理解毕达哥拉斯的思想威力”，从人到自然到哲学，三个层次展现知识追求的广度；“获得一些成就，然而并不多”，谦逊中见对知识的无止境追求。",
        [
            ("寻求", "寻找追求"),
            ("心灵", "指内心、精神世界"),
            ("闪闪发光", "形容光亮闪烁"),
            ("试图", "打算、尝试"),
            ("毕达哥拉斯", "（约前580—约前500）古希腊哲学家、数学家，认为数是万物的本原"),
            ("思想威力", "思想的力量和影响"),
            ("支配", "对人或事物起引导和控制的作用"),
            ("万物", "宇宙间的一切事物"),
            ("流转", "流动转移、循环变化"),
            ("成就", "事业上的成绩"),
        ],
    ),
    (
        "爱情和知识，尽其可能地把我引上天堂，但是同情心总把我带回尘世。痛苦的呼号的回声在我心中回荡。饥饿的儿童，被压迫者折磨的受害者，被儿女视为负担的无助的老人，以及充满孤寂、贫穷和痛苦的整个世界，都是对人类应有生活的嘲讽。我渴望减轻这些不幸，但是我无能为力，而且我自己也深受其害。",
        "写同情心将作者从天堂拉回尘世：饥饿的儿童、受压迫的受害者、无助的老人、充满苦难的世界，都让作者痛苦。渴望减轻不幸却无能为力，自己也深受其害。",
        "“天堂”与“尘世”对比，写理想与现实的落差；“痛苦的呼号的回声”诉诸听觉，写苦难的震撼；“饥饿的儿童……无助的老人……整个世界”，排比列举苦难的种种，触目惊心；“嘲讽”一词尖锐，写现实对人类理想的嘲弄；“无能为力”“深受其害”，写作者的痛苦与无力，情感深沉。",
        [
            ("尽其可能", "尽自己最大的可能"),
            ("同情心", "对别人的遭遇在感情上发生共鸣"),
            ("尘世", "佛教徒或道教徒指现实世界，与他们所幻想的理想世界相对"),
            ("呼号", "因极端痛苦而呼喊"),
            ("回声", "声波遇到障碍物反射回来再度被听到的声音"),
            ("回荡", "（声音等）来回飘荡"),
            ("压迫者", "用权力或势力强制别人服从的人"),
            ("折磨", "使在肉体上、精神上受痛苦"),
            ("受害者", "遭受损害的人"),
            ("视为", "看作、当作"),
            ("负担", "承受的压力或担当的责任、费用等"),
            ("无助", "没有帮助、孤立无援"),
            ("孤寂", "孤独寂寞"),
            ("嘲讽", "嘲笑讽刺"),
            ("不幸", "不幸运、使人失望、痛苦的事"),
            ("无能为力", "用不上力量，指没有办法"),
            ("深受其害", "深深地受到它的损害"),
        ],
    ),
    (
        "这就是我的一生，我发现人是值得活的。如果有谁再给我一次生活的机会，我将欣然接受这难得的赐予。",
        "总结全文：这一生被三种激情支配，虽然痛苦，但值得活。如果有机会，愿意再活一次。",
        "“这就是我的一生”收束全文，呼应开头；“人是值得活的”是全文的核心感悟，在经历了爱情的狂喜、知识的追求和苦难的痛苦之后，作者依然肯定人生的价值；“欣然接受”“难得的赐予”，以积极乐观的态度收束，余味深长。",
        [
            ("值得", "有价值、有意义"),
            ("欣然", "愉快地"),
            ("赐予", "赏赐、给予（多指上对下或长辈对晚辈）"),
        ],
    ),
]

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
for i, (orig, content, method, annos) in enumerate(paragraphs):
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
    {"w":"彻","py":"chè","q":"以及对于人类苦难痛□肺腑的怜悯","tip":"「彻」双人旁，穿透；不要写成「撤」（提手旁）"},
    {"w":"腑","py":"fǔ","q":"以及对于人类苦难痛彻肺□的怜悯","tip":"「腑」月字旁，内脏；与「俯」（单人旁）区分"},
    {"w":"悯","py":"mǐn","q":"以及对于人类苦难痛彻肺腑的怜□","tip":"「悯」竖心旁，忧愁；不要写成「闵」（门字旁）"},
    {"w":"掷","py":"zhì","q":"把我伸展到绝望边缘的深深的苦海上东抛西□","tip":"「掷」提手旁，扔、投；不要写成「郑」"},
    {"w":"魂","py":"hún","q":"首先因为它叫我销□，爱情的魔力","tip":"「魂」云字旁，灵魂；不要写成「魄」（白字旁）"},
    {"w":"颤","py":"chàn","q":"一颗□抖的灵魂在世界的边缘","tip":"「颤」页字旁，发抖；多音字，此处读chàn不读zhàn"},
    {"w":"瞰","py":"kàn","q":"俯□那冰冷死寂、深不可测的深渊","tip":"「瞰」目字旁，从高处往下看；不要写成「敢」"},
    {"w":"寂","py":"jì","q":"俯瞰那冰冷死□、深不可测的深渊","tip":"「寂」宝盖头，安静；不要写成「叔」"},
    {"w":"渊","py":"yuān","q":"俯瞰那冰冷死寂、深不可测的深□","tip":"「渊」三点水，深水；不要写成「渊」以外的写法"},
    {"w":"圣","py":"shèng","q":"我看到了□徒和诗人们所想象的天堂景象","tip":"「圣」又字头，最崇高的；不要写成「怪」"},
    {"w":"缩","py":"suō","q":"天堂景象的神秘□影","tip":"「缩」绞丝旁，收缩；不要写成「宿」"},
    {"w":"耀","py":"yào","q":"我希望知道星星为什么闪闪发□","tip":"「耀」光字旁，光线照射；笔画多，注意右边是「翟」"},
    {"w":"哥","py":"gē","q":"我试图理解毕达□拉斯的思想威力","tip":"「哥」可字头，兄长；毕达哥拉斯是古希腊哲学家"},
    {"w":"转","py":"zhuǎn","q":"即数字支配着万物流□","tip":"「转」车字旁，流动变化；多音字，此处读zhuǎn"},
    {"w":"荡","py":"dàng","q":"痛苦的呼号的回声在我心中回□","tip":"「荡」草字头，来回飘荡；不要写成「汤」（三点水）"},
    {"w":"迫","py":"pò","q":"被压□者折磨的受害者","tip":"「迫」走之底，强迫；不要写成「破」（石字旁）"},
    {"w":"嘲","py":"cháo","q":"都是对人类应有生活的□讽","tip":"「嘲」口字旁，嘲笑；不要写成「朝」"},
    {"w":"赐","py":"cì","q":"我将欣然接受这难得的□予","tip":"「赐」贝字旁，赏赐；不要写成「踢」（足字旁）"},
]

dict_notes = [
    {"w":"支配","a":"对人或事物起引导和控制的作用","q":"三种单纯然而极其强烈的激情支配着我的一生"},
    {"w":"痛彻肺腑","a":"形容极度痛苦，好像穿透了肺腑","q":"对于人类苦难痛彻肺腑的怜悯"},
    {"w":"怜悯","a":"对遭遇不幸的人表示同情","q":"对于人类苦难痛彻肺腑的怜悯"},
    {"w":"犹如","a":"好像、如同","q":"这些激情犹如狂风"},
    {"w":"东抛西掷","a":"形容被风吹得左右摇摆、没有定向","q":"把我……东抛西掷"},
    {"w":"销魂","a":"灵魂离开肉体，形容极度快乐、陶醉","q":"首先因为它叫我销魂"},
    {"w":"魔力","a":"神奇的、使人迷惑的力量","q":"爱情的魔力往往让我愿意"},
    {"w":"俯瞰","a":"从高处往下看","q":"俯瞰那冰冷死寂、深不可测的深渊"},
    {"w":"死寂","a":"没有一丝生气，形容极其安静","q":"俯瞰那冰冷死寂"},
    {"w":"深不可测","a":"深得无法测量，比喻情况捉摸不透","q":"深不可测的深渊"},
    {"w":"深渊","a":"很深的水，比喻险境或痛苦的境地","q":"深不可测的深渊"},
    {"w":"缩影","a":"可以代表同一类型的具体而微的人或事物","q":"天堂景象的神秘缩影"},
    {"w":"毕达哥拉斯","a":"古希腊哲学家、数学家，认为数是万物的本原","q":"我试图理解毕达哥拉斯的思想威力"},
    {"w":"流转","a":"流动转移、循环变化","q":"数字支配着万物流转"},
    {"w":"尘世","a":"指现实世界，与理想世界相对","q":"同情心总把我带回尘世"},
    {"w":"呼号","a":"因极端痛苦而呼喊","q":"痛苦的呼号的回声"},
    {"w":"回荡","a":"（声音等）来回飘荡","q":"在我心中回荡"},
    {"w":"嘲讽","a":"嘲笑讽刺","q":"都是对人类应有生活的嘲讽"},
    {"w":"无能为力","a":"用不上力量，指没有办法","q":"但是我无能为力"},
    {"w":"深受其害","a":"深深地受到它的损害","q":"而且我自己也深受其害"},
    {"w":"欣然","a":"愉快地","q":"我将欣然接受这难得的赐予"},
    {"w":"赐予","a":"赏赐、给予","q":"这难得的赐予"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《我为什么而活着》罗素</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">英国 · 罗素</div>
  <h1 class="hero-title">我为什么而活着</h1>
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
    <p>《我为什么而活着》是英国哲学家、数学家伯特兰·罗素的一篇哲理散文，是其自传《罗素自传》的序言。文章以“三种单纯然而极其强烈的激情”总领全文：对爱情的渴望、对知识的追求、对人类苦难的怜悯。这三种激情如狂风般支配着他的一生，使他在天堂与尘世之间往返，最终得出“人是值得活的”这一坚定结论。</p>
    <p>全文仅五百余字，却浓缩了一位伟大哲人的一生思考。语言凝练、气势磅礴、情感真挚，是世界散文史上的经典名篇，与严文井《永久的生命》同编为统编版八年级上册第四单元“散文二篇”。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>伯特兰·罗素（1872—1970），英国哲学家、数学家、逻辑学家、社会活动家，1950年诺贝尔文学奖获得者。出身于英国贵族家庭，早年在剑桥大学学习数学和哲学，后成为分析哲学的主要创始人之一。他一生著述宏富，涉及哲学、数学、历史、政治、教育等诸多领域，代表作有《西方哲学史》《数学原理》《幸福之路》《罗素自传》等。</p>
    <p style="margin-top:10px;color:var(--ink2)">罗素不仅是书斋里的学者，更是积极的社会活动家。他反对战争、呼吁和平、关注人类苦难，曾因反战活动入狱。1955年，他与爱因斯坦联合发表《罗素—爱因斯坦宣言》，呼吁警惕核战争的危险。《我为什么而活着》正是他一生追求与关怀的自我写照。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>自传序言：</b>本文是《罗素自传》的序言，写于罗素晚年。在回顾一生时，他以三种激情概括自己的人生动力：爱情给了他狂喜与慰藉，知识让他探索人与宇宙的奥秘，而对人类苦难的怜悯则让他无法安于象牙塔。</p>
    <p style="margin-top:8px"><b>时代印记：</b>罗素一生经历了两次世界大战、核军备竞赛等重大历史事件。“饥饿的儿童，被压迫者折磨的受害者……充满孤寂、贫穷和痛苦的整个世界”，正是20世纪上半叶人类苦难的真实写照。对苦难的怜悯，不是抽象的同情，而是他亲身参与和平运动、社会改革的动力。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文朗读《我为什么而活着》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1PA411v7w9&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读我为什么而活着"></iframe>
        <a href="https://www.bilibili.com/video/BV1PA411v7w9" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>罗素：我们为何而活？</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1wbCeBCEYn&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="罗素我们为何而活"></iframe>
        <a href="https://www.bilibili.com/video/BV1wbCeBCEYn" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 词语 · 手法</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{fulltext_html}  </div>
  <div class="verse-list" id="verseList">
{verse_html}  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">哲理 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>哲理意蕴</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">三种激情，一生坐标</div>
        <p>罗素以三种激情概括一生：对爱情的渴望、对知识的追求、对人类苦难的怜悯。爱情是个人情感的极致体验，知识是对世界的理性探索，怜悯是对他人的道德关怀。三者分别对应情感、理性、道德三个维度，构成了完整的人生坐标。这三种激情“犹如狂风”，既带来了痛苦，也赋予了人生意义。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">天堂与尘世之间</div>
        <p>“爱情和知识，尽其可能地把我引上天堂，但是同情心总把我带回尘世。”爱情与知识是美好的，引人向上；而对苦难的怜悯让人无法回避现实的痛苦。罗素没有选择逃避到象牙塔中，而是选择直面苦难——虽然“无能为力”，虽然“深受其害”，但正是这种担当，让他的人生超越了个人的悲欢。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">总分结构，纲举目张</div>
        <p>首段提出三种激情，总领全文；第二、三、四段分别阐述爱情、知识、怜悯；第五段总结全文。结构严谨，条理清晰，如议论文般层层展开，却又饱含情感，是哲理散文的典范。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">比喻生动，形象鲜明</div>
        <p>“这些激情犹如狂风，把我伸展到绝望边缘的深深的苦海上东抛西掷”，以狂风、苦海写激情的强烈与人生的动荡；“冰冷死寂、深不可测的深渊”写孤独的可怕；“天堂景象的神秘缩影”写爱情的美好。比喻让抽象的哲理变得可感可触。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">排比铺陈，气势磅礴</div>
        <p>“我追求爱情，首先因为……其次是因为……最后是因为……”，排比写追求爱情的三个原因；“饥饿的儿童，被压迫者折磨的受害者，被儿女视为负担的无助的老人，以及充满孤寂、贫穷和痛苦的整个世界”，排比列举苦难的种种。排比增强了文章的气势和感染力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比鲜明，情感深沉</div>
        <p>“天堂”与“尘世”对比，写理想与现实的落差；爱情的狂喜与孤独的深渊对比，写爱情的可贵；“获得一些成就，然而并不多”，在自谦中见对知识的无止境追求。对比中见思考的深度，情感的真挚。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">三种单纯然而极其强烈的激情支配着我的一生。</div>
        <p>全文的总纲。“单纯”写激情的纯粹，“极其强烈”写激情的力量，“支配”写激情对人生的决定性影响。这句话开门见山，奠定了全文的基调，也引出了下文对三种激情的分别阐述。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">这些激情犹如狂风，把我伸展到绝望边缘的深深的苦海上东抛西掷，使我的生活没有定向。</div>
        <p>以狂风、苦海为喻，写三种激情给人生带来的动荡。“绝望边缘”“深深的苦海”渲染痛苦，“东抛西掷”“没有定向”写身不由己。这个比喻既写出了激情的力量，也暗示了人生的痛苦与不安。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">爱情和知识，尽其可能地把我引上天堂，但是同情心总把我带回尘世。</div>
        <p>全文的关键转折。“天堂”象征美好与超越，“尘世”象征苦难与现实。爱情和知识引人向上，而同情心让人无法回避苦难。这句话写出了罗素内心的张力：既追求美好，又担当苦难，正是这种张力让他的人生有了厚度。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">这就是我的一生，我发现人是值得活的。</div>
        <p>全文的核心结论。在经历了爱情的狂喜、知识的追求和苦难的痛苦之后，罗素依然肯定人生的价值。“人是值得活的”，不是因为人生没有痛苦，而是因为在痛苦中依然有爱、有知、有怜悯——这正是人生的意义所在。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《我为什么而活着》以三种激情——对爱情的渴望、对知识的追求、对人类苦难的怜悯——概括了罗素的一生，表达了他对人生意义的思考：人生虽然充满痛苦，但爱情、知识和同情心赋予了人生价值，因此“人是值得活的”。</p>
    <p style="margin-top:10px">文章的深刻之处在于：它没有回避人生的苦难，而是在直面苦难的基础上肯定人生。“同情心总把我带回尘世”，这种对人类苦难的担当，让罗素的人生超越了个人的悲欢，具有了崇高的道德力量。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 用字 · 修辞 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">支配</span><span class="acc-d">对人或事物起引导和控制的作用。</span></div>
      <div class="acc-item"><span class="acc-w">痛彻肺腑</span><span class="acc-d">形容极度痛苦，好像穿透了肺腑。</span></div>
      <div class="acc-item"><span class="acc-w">怜悯</span><span class="acc-d">对遭遇不幸的人表示同情。</span></div>
      <div class="acc-item"><span class="acc-w">犹如</span><span class="acc-d">好像、如同。</span></div>
      <div class="acc-item"><span class="acc-w">销魂</span><span class="acc-d">灵魂离开肉体，形容极度快乐、陶醉。</span></div>
      <div class="acc-item"><span class="acc-w">魔力</span><span class="acc-d">神奇的、使人迷惑的力量。</span></div>
      <div class="acc-item"><span class="acc-w">俯瞰</span><span class="acc-d">（fǔ kàn）从高处往下看。</span></div>
      <div class="acc-item"><span class="acc-w">死寂</span><span class="acc-d">没有一丝生气，形容极其安静。</span></div>
      <div class="acc-item"><span class="acc-w">深不可测</span><span class="acc-d">深得无法测量，比喻情况捉摸不透。</span></div>
      <div class="acc-item"><span class="acc-w">深渊</span><span class="acc-d">很深的水，比喻险境或痛苦的境地。</span></div>
      <div class="acc-item"><span class="acc-w">缩影</span><span class="acc-d">可以代表同一类型的具体而微的人或事物。</span></div>
      <div class="acc-item"><span class="acc-w">毕达哥拉斯</span><span class="acc-d">古希腊哲学家、数学家，认为数是万物的本原。</span></div>
      <div class="acc-item"><span class="acc-w">流转</span><span class="acc-d">流动转移、循环变化。</span></div>
      <div class="acc-item"><span class="acc-w">尘世</span><span class="acc-d">指现实世界，与理想世界相对。</span></div>
      <div class="acc-item"><span class="acc-w">呼号</span><span class="acc-d">因极端痛苦而呼喊。</span></div>
      <div class="acc-item"><span class="acc-w">回荡</span><span class="acc-d">（声音等）来回飘荡。</span></div>
      <div class="acc-item"><span class="acc-w">嘲讽</span><span class="acc-d">嘲笑讽刺。</span></div>
      <div class="acc-item"><span class="acc-w">无能为力</span><span class="acc-d">用不上力量，指没有办法。</span></div>
      <div class="acc-item"><span class="acc-w">欣然</span><span class="acc-d">愉快地。</span></div>
      <div class="acc-item"><span class="acc-w">赐予</span><span class="acc-d">赏赐、给予。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">痛彻肺腑</span><span class="acc-d">（chè fǔ）彻，穿透；腑，内脏。不要写成“痛撤肺腹”。</span></div>
      <div class="acc-item"><span class="acc-w">怜悯</span><span class="acc-d">（mǐn）竖心旁；不要写成“闵”。</span></div>
      <div class="acc-item"><span class="acc-w">东抛西掷</span><span class="acc-d">（zhì）掷，提手旁，扔；不要写成“郑”。</span></div>
      <div class="acc-item"><span class="acc-w">销魂</span><span class="acc-d">（hún）云字旁；与“魄”（pò，白字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">颤抖</span><span class="acc-d">（chàn）页字旁；多音字，此处读chàn，不读zhàn。</span></div>
      <div class="acc-item"><span class="acc-w">俯瞰</span><span class="acc-d">（kàn）目字旁，从高处往下看；不要写成“敢”。</span></div>
      <div class="acc-item"><span class="acc-w">死寂</span><span class="acc-d">（jì）宝盖头；不要写成“叔”。</span></div>
      <div class="acc-item"><span class="acc-w">赐予</span><span class="acc-d">（cì）贝字旁，赏赐；与“踢”（tī，足字旁）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞方法</h3>
      <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">“这些激情犹如狂风”，以狂风写激情的强烈；“深深的苦海”写人生的痛苦；“冰冷死寂、深不可测的深渊”写孤独的可怕；“天堂景象的神秘缩影”写爱情的美好。</span></div>
      <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">“我追求爱情，首先因为……其次是因为……最后是因为……”；“饥饿的儿童，被压迫者折磨的受害者，被儿女视为负担的无助的老人……”排比增强气势和感染力。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">“天堂”与“尘世”对比；爱情的狂喜与孤独的深渊对比；“获得一些成就，然而并不多”的自谦。</span></div>
      <div class="acc-item"><span class="acc-w">反复</span><span class="acc-d">“我追求爱情”三次反复，强调对爱情的执着追求；“我希望”两次反复，写对知识的渴望。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">总分总结构</span><span class="acc-d">首段总领，中间分述，末段总结，结构严谨，条理清晰。</span></div>
      <div class="acc-item"><span class="acc-w">哲理与抒情结合</span><span class="acc-d">以哲学家的理性思考人生，又以诗人的激情表达情感，议论中饱含深情。</span></div>
      <div class="acc-item"><span class="acc-w">以小见大</span><span class="acc-d">从个人的三种激情出发，写出对整个人生意义的思考，以个人体验承载普遍哲理。</span></div>
      <div class="acc-item"><span class="acc-w">语言凝练</span><span class="acc-d">全文仅五百余字，却浓缩了一生的思考，字字千钧，气势磅礴。</span></div>
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
  <div class="kai">《我为什么而活着》</div>
  <div>罗素 · 英国 · 出自《罗素自传》</div>
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
