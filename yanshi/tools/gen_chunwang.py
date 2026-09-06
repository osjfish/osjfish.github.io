# -*- coding: utf-8 -*-
"""《春望》课件生成器 —— 复用《背影》CSS/JS框架。"""
import json, re, html, io, os

LQ = '\u201c'; RQ = '\u201d'
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chunwang-dufu.html')
src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>'); JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'chunwang_fs')

def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)
def fixq(s): return s.replace('~L~', LQ).replace('~R~', RQ)

FULLTEXT = [
    "国破山河在，城春草木深。",
    "感时花溅泪，恨别鸟惊心。",
    "烽火连三月，家书抵万金。",
    "白头搔更短，浑欲不胜簪。",
]

PARTS = [
    ("第一部分", "春城败象 · 感时恨别", "第 1–4 句",
     fixq("首联~L~国破山河在，城春草木深~R~，写春望所见：国都沦陷，山河依旧；春天来到长安，城中却草木丛生、人烟稀少。~L~破~R~~L~深~R~二字，炼字精绝，写出了战乱后的荒凉。颔联~L~感时花溅泪，恨别鸟惊心~R~，移情于物，以乐景写哀情——花鸟本是美好之物，但在感时恨别的诗人眼中，花也溅泪，鸟也惊心。这两句是千古传诵的名句。")),
    ("第二部分", "烽火家书 · 白头不胜簪", "第 5–8 句",
     fixq("颈联~L~烽火连三月，家书抵万金~R~，写战乱持续已久，家书弥足珍贵。~L~抵万金~R~用夸张手法，写出了战乱中家书的难得和诗人对家人的深切思念。尾联~L~白头搔更短，浑欲不胜簪~R~，以诗人的自我形象收束全诗——白发越搔越短，简直连簪子都插不住了。一个~L~搔~R~字，写出了诗人的焦虑愁苦；~L~不胜簪~R~的细节，将忧国思家的深情化为可感的形象，余味无穷。")),
]

S = [
(0, "[[国破|国都沦陷。国，国都，指长安；破，破败、沦陷]]山河在，城春[[草木深|草木丛生，形容人烟稀少、荒凉。深，茂盛、丛生]]。",
 "国都沦陷，山河依旧；春天来到长安，城中草木丛生，一片荒凉。",
 fixq("首联写春望所见，是千古传诵的名句。~L~国破山河在~R~，国都已经沦陷，但山河依旧存在——一个~L~破~R~字，写出了安史之乱后长安的残破；一个~L~在~R~字，写出了山河的无情，不以人的意志为转移。~L~城春草木深~R~，春天来了，城中草木丛生——一个~L~深~R~字，写出了草木的茂盛，也暗示了人烟的稀少。以往春天的长安是繁华的，但如今只有草木丛生，对比之下，更显出战乱后的荒凉。这一联以~L~破~R~字统摄，写出了国破家亡的悲痛，为全诗奠定了沉郁悲凉的基调。"),
 ["炼字", "对比", "名句", "起笔"]),

(0, "[[感时|感伤时局。感，感伤；时，时局、时事]]花[[溅泪|（jiàn lèi）落泪。溅，洒落、迸射]]，[[恨别|怨恨离别。恨，怨恨、遗憾；别，离别]]鸟[[惊心|使心惊动。惊，使……惊动]]。",
 "感伤时局，见花也不禁落泪；怨恨离别，听鸟鸣也感到心惊。",
 fixq("颔联是千古传诵的名句，用移情于物的手法，将诗人的情感投射到花鸟之上。~L~感时花溅泪~R~，感伤时局，连花也在落泪——花本是无情之物，但在诗人眼中，花也在为国破家亡而落泪。~L~恨别鸟惊心~R~，怨恨离别，连鸟鸣也让人心惊——鸟本是可爱之物，但在诗人耳中，鸟鸣也勾起了离别的痛苦。这两句有两种理解：一是诗人感时恨别，见花溅泪、闻鸟惊心；二是花鸟也在感时恨别，花溅泪、鸟惊心。两种理解都通，都写出了诗人内心的极度悲痛。以乐景写哀情，倍增其哀，是杜诗~L~沉郁顿挫~R~风格的典范。"),
 ["移情于物", "以乐景写哀", "炼字", "名句"]),

(1, "[[烽火|（fēng huǒ）古代边防报警的烟火，这里指安史之乱的战火]]连[[三月|连续三个月，一说指春季的三个月（正月、二月、三月）]]，[[家书|家信。家，家人；书，书信]][[抵|（dǐ）值、相当于]]万金。",
 "战火已经连续燃烧了三个月，一封家信抵得上万两黄金。",
 fixq("颈联由景入情，写战乱中对家人的思念。~L~烽火连三月~R~，安史之乱的战火已经持续了三个月，写出了战乱时间之长、破坏之大。~L~家书抵万金~R~，一封家信抵得上万两黄金——~L~抵万金~R~用夸张手法，写出了战乱中家书的难得和珍贵。在和平时期，家书是平常之物，但在战乱中，交通断绝，生死未卜，一封家书就成了最珍贵的东西。这两句写出了诗人对家人的深切思念，也反映了战乱中人民的共同痛苦，具有普遍的意义。~L~家书抵万金~R~后来成为成语，形容家书的珍贵。"),
 ["夸张", "用典", "名句", "思乡"]),

(1, "[[白头|白头发，指诗人自己。杜甫此时四十五岁，因忧愁而早生白发]][[搔|（sāo）用手指抓挠，这里指挠头]]更[[短|短少、稀少]]，[[浑欲|（hún yù）简直要。浑，简直；欲，将要]][[不胜簪|（shèng zān）插不住簪子。胜，经受住；簪，古人用来束发的首饰]]。",
 "满头白发越搔越短少，简直连簪子都插不住了。",
 fixq("尾联以诗人的自我形象收束全诗，是千古传诵的名句。~L~白头搔更短~R~，诗人因为忧愁焦虑，不断地挠头，结果白头发越挠越短少——一个~L~搔~R~字，写出了诗人焦虑愁苦的动作和神态；一个~L~更~R~字，写出了白发日渐稀少的过程。~L~浑欲不胜簪~R~，简直连簪子都插不住了——古人成年后束发戴冠，用簪子固定，头发短到插不住簪子，说明诗人已经憔悴衰老到了极点。这一联没有直接写忧国思家，但~L~搔~R~的动作和~L~不胜簪~R~的细节，将诗人内心的焦虑和愁苦化为可感的形象，含蓄深沉，余味无穷。这是杜甫~L~沉郁顿挫~R~风格的集中体现。"),
 ["细节描写", "炼字", "名句", "收束"]),
]

DICT_WORDS = [
    {"w":"溅","py":"jiàn","q":"感时花□泪，恨别鸟惊心","tip":fixq("「溅」三点水，音 jiàn，液体迸射、洒落，~L~溅泪~R~即落泪，勿写~L~贱~R~（贫贱，贝字旁）")},
    {"w":"搔","py":"sāo","q":"白头□更短，浑欲不胜簪","tip":fixq("「搔」提手旁，音 sāo，用手指抓挠，~L~搔头~R~即挠头，勿写~L~骚~R~（骚扰，马字旁）~L~瘙~R~（瘙痒，病字旁）")},
    {"w":"簪","py":"zān","q":"白头搔更短，浑欲不胜□","tip":fixq("「簪」竹字头，音 zān，古人束发的首饰，~L~不胜簪~R~即插不住簪子，勿写~L~赞~R~（赞美）")},
    {"w":"烽","py":"fēng","q":"□火连三月，家书抵万金","tip":fixq("「烽」火字旁，音 fēng，烽火，古代边防报警的烟火，勿写~L~锋~R~（锋利，金字旁）~L~峰~R~（山峰，山字旁）")},
    {"w":"抵","py":"dǐ","q":"烽火连三月，家书□万金","tip":fixq("「抵」提手旁，音 dǐ，值、相当于，~L~抵万金~R~即值万两黄金，勿写~L~低~R~（高低，单人旁）")},
    {"w":"浑","py":"hún","q":"白头搔更短，□欲不胜簪","tip":fixq("「浑」三点水，音 hún，简直、几乎，~L~浑欲~R~即简直要，勿写~L~混~R~（混合）")},
    {"w":"胜","py":"shēng","q":"白头搔更短，浑欲不□簪","tip":fixq("「胜」此处读 shēng（旧读 shēng），经受住、承受，~L~不胜~R~即经受不住，勿读 shèng（胜利）")},
    {"w":"深","py":"shēn","q":"国破山河在，城春草木□","tip":fixq("「深」三点水，音 shēn，茂盛、丛生，~L~草木深~R~形容荒凉，勿写~L~探~R~（探索，提手旁）")},
]

DICT_NOTES = [
    {"w":"国破","q":"国破山河在","a":"国都沦陷。国，国都，指长安；破，破败、沦陷"},
    {"w":"山河在","q":"国破山河在","a":"山河依旧存在。在，存在、依旧"},
    {"w":"城春","q":"城春草木深","a":"长安城的春天。城，指长安"},
    {"w":"草木深","q":"城春草木深","a":"草木丛生，形容人烟稀少、荒凉。深，茂盛、丛生"},
    {"w":"感时","q":"感时花溅泪","a":"感伤时局。感，感伤；时，时局、时事"},
    {"w":"溅泪","q":"感时花溅泪","a":"（jiàn lèi）落泪。溅，洒落、迸射"},
    {"w":"恨别","q":"恨别鸟惊心","a":"怨恨离别。恨，怨恨、遗憾；别，离别"},
    {"w":"惊心","q":"恨别鸟惊心","a":"使心惊动。惊，使……惊动"},
    {"w":"烽火","q":"烽火连三月","a":"（fēng huǒ）古代边防报警的烟火，这里指安史之乱的战火"},
    {"w":"连三月","q":"烽火连三月","a":"连续三个月。一说指春季的三个月（正月、二月、三月）"},
    {"w":"家书","q":"家书抵万金","a":"家信。家，家人；书，书信"},
    {"w":"抵","q":"家书抵万金","a":"（dǐ）值、相当于"},
    {"w":"白头","q":"白头搔更短","a":"白头发，指诗人自己。杜甫此时四十五岁，因忧愁而早生白发"},
    {"w":"搔","q":"白头搔更短","a":"（sāo）用手指抓挠，这里指挠头"},
    {"w":"浑欲","q":"浑欲不胜簪","a":"（hún yù）简直要。浑，简直；欲，将要"},
    {"w":"不胜簪","q":"浑欲不胜簪","a":"（shèng zān）插不住簪子。胜，经受住；簪，古人束发的首饰"},
]

def build_verses():
    out, idx = [], 0
    for pi, part in enumerate(PARTS):
        out.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>' % (part[0], part[1], part[2]))
        out.append('      <div class="part-overview">%s</div>' % fixq(part[3]))
        for (p, txt, yi, shang, tags) in S:
            if p != pi: continue
            idx += 1
            out.append('      <div class="verse" id="l%d" data-i="%d">' % (idx, idx-1))
            out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx, annotate(txt)))
            out.append('        <details class="v-more"><summary>译文 · 赏析</summary><div class="d-body">')
            out.append('            <div class="v-sec"><b class="v-label">译　文</b><div class="v-trans">%s</div></div>' % yi)
            out.append('            <div class="v-sec"><b class="v-label">赏　析</b><div class="d-body"><p>%s</p></div>' % shang)
            if tags: out.append('              <div class="tags">%s</div>' % ''.join('<span>%s</span>' % t for t in tags))
            out.append('            </div></div></details></div>')
    return '\n'.join(out), idx

verses_html, total = build_verses()
full_html = '\n'.join('    <div class="pl">%s</div>' % p for p in FULLTEXT)
anno_count = sum(txt.count('[[') for (_, txt, _, _, _) in S)

BG = fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《春望》是唐代伟大诗人杜甫的代表作，作于唐肃宗至德二载（757）三月。当时安史之乱已经爆发，长安沦陷，杜甫被困在长安城中，目睹了国都残破、民不聊生的景象，写下了这首千古传诵的五言律诗。</p>
    <p>全诗以~L~望~R~字统摄，由远及近，由景入情。首联写春望所见——国破家亡，草木丛生；颔联移情于物——花溅泪，鸟惊心；颈联写战乱中家书的珍贵；尾联以诗人自我形象收束——白头搔短，不胜簪。全诗沉郁顿挫，感人至深，是杜甫爱国主义精神的集中体现，也是中国古典诗歌中最著名的忧国忧民之作。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>杜甫（712—770），字子美，自号少陵野老，祖籍襄阳，生于河南巩县。唐代伟大的现实主义诗人，被后世尊为~L~诗圣~R~，其诗被称为~L~诗史~R~。与李白并称~L~李杜~R~。曾任左拾遗、检校工部员外郎，故世称~L~杜工部~R~。</p>
    <p>杜甫的一生以安史之乱为界，分为前后两个时期。前期正值开元盛世，漫游吴越、齐赵，意气风发；后期历经安史之乱，颠沛流离，诗歌转向沉郁顿挫，深刻反映社会现实。《春望》作于安史之乱中，是杜甫后期的代表作，体现了他~L~沉郁顿挫~R~的艺术风格和忧国忧民的崇高精神。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>安史之乱：</b>天宝十四载（755），安禄山、史思明以~L~讨杨国忠~R~为名，在范阳起兵叛乱，史称~L~安史之乱~R~。叛军很快攻陷洛阳、长安，唐玄宗仓皇出逃四川。这场叛乱持续了八年（755—763），是唐朝由盛转衰的转折点。</p>
    <p><b>杜甫被困长安：</b>至德元载（756），杜甫在投奔唐肃宗的途中被叛军俘虏，押回长安。他在长安被困了近一年，目睹了国都残破、人民流离的惨状。《春望》即作于至德二载（757）三月，是杜甫被困长安时的作品。</p>
    <p><b>春天的反差：</b>春天本是万物复苏、生机盎然的季节，但在沦陷后的长安，春天带来的不是希望，而是更深的悲痛——~L~国破山河在，城春草木深~R~，以春景写哀情，倍增其哀。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《春望》是一首<b>五言律诗</b>，全诗八句，每句五字，共四十字。首联（一二句）写春望所见，颔联（三四句）移情于物，颈联（五六句）写战乱家书，尾联（七八句）以自我形象收束。全诗格律严谨，对仗精工，是五言律诗的典范之作。</p>
    <p>诗题~L~春望~R~，即春天远望。全诗围绕~L~望~R~字展开，由远望到近望，由望景到望情，层层递进，将忧国思家的深情写得淋漓尽致。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>杜甫《春望》朗诵</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV13a4y1d7kF&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="春望朗诵"></iframe>
        <a href="https://www.bilibili.com/video/BV13a4y1d7kF" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>经典咏流传《春望》徐均朔、张会芳演唱</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1ec411G7xi&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="春望经典咏流传"></iframe>
        <a href="https://www.bilibili.com/video/BV1ec411G7xi" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">杜甫——忧国忧民的爱国诗人</div>
        <p>《春望》中的抒情主人公，是一位忧国忧民、思念家人的爱国诗人形象。他被困在沦陷后的长安，面对春日的荒凉景象，心中充满了国破家亡的悲痛和对家人的深切思念。</p>
        <p><b>忧国之痛：</b>~L~国破山河在，城春草木深~R~，诗人目睹国都沦陷、人民流离，心中充满了对国家命运的忧虑。~L~感时花溅泪~R~，连花都在为国破家亡而落泪，何况是人？</p>
        <p><b>思家之苦：</b>~L~烽火连三月，家书抵万金~R~，战乱持续已久，家书弥足珍贵。诗人被困长安，与家人音信断绝，对家人的思念日益深切。</p>
        <p><b>憔悴之态：</b>~L~白头搔更短，浑欲不胜簪~R~，诗人因为忧愁焦虑，白发越搔越短，简直连簪子都插不住了。这个形象，将忧国思家的深情化为可感的细节，感人至深。这个形象，是杜甫一生忧国忧民精神的缩影，也是中国文学中最动人的爱国诗人形象之一。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">移情于物，以乐景写哀</div>
        <p>~L~感时花溅泪，恨别鸟惊心~R~是移情于物的典范。花鸟本是美好之物，但在感时恨别的诗人眼中，花也溅泪，鸟也惊心。诗人将自己的情感投射到花鸟之上，使无情之物也带上了人的情感。以乐景写哀情，倍增其哀，是杜诗~L~沉郁顿挫~R~风格的集中体现。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">炼字精当——破、深、溅、惊、抵、搔</div>
        <p>~L~破~R~字写出长安的残破，~L~深~R~字写出草木的丛生和人烟的稀少，~L~溅~R~字写出泪落的力度，~L~惊~R~字写岀心惊的程度，~L~抵~R~字写出家书的珍贵，~L~搔~R~字写出焦虑的动作。六字炼字精当，将诗人的悲痛和焦虑写得入木三分。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">情景交融，层层递进</div>
        <p>全诗以~L~望~R~字统摄，由远及近，由景入情，层层递进。首联写远望之景，颔联写近望之情，颈联写望中所思，尾联写望中自我形象。景中有情，情因景生，情景交融，天衣无缝。全诗沉郁顿挫，感人至深。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">感时花溅泪，恨别鸟惊心。</div>
        <p>这是千古传诵的名句，用移情于物的手法，将诗人的情感投射到花鸟之上。感伤时局，见花也不禁落泪；怨恨离别，听鸟鸣也感到心惊。这两句有两种理解：一是诗人感时恨别，见花溅泪、闻鸟惊心；二是花鸟也在感时恨别，花溅泪、鸟惊心。两种理解都通，都写出了诗人内心的极度悲痛。以乐景写哀情，倍增其哀，是杜诗~L~沉郁顿挫~R~风格的典范。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">烽火连三月，家书抵万金。</div>
        <p>这两句写出了战乱中家书的珍贵。~L~烽火连三月~R~写战乱时间之长，~L~家书抵万金~R~用夸张手法写家书的价值。在和平时期，家书是平常之物，但在战乱中，交通断绝，生死未卜，一封家书就成了最珍贵的东西。这两句写出了诗人对家人的深切思念，也反映了战乱中人民的共同痛苦，具有普遍的意义。~L~家书抵万金~R~后来成为成语。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>主题思想</h3>
    <p>《春望》通过描写安史之乱中长安的荒凉景象，抒发了诗人忧国忧民、思念家人的深切悲痛，表达了对国家命运的忧虑和对和平生活的渴望。</p>
    <p>这首诗的深刻之处在于，它将个人的命运与国家的命运紧密联系在一起——国破则家亡，家亡则人愁。诗人的忧国与思家不是分离的，而是融为一体的。~L~白头搔更短，浑欲不胜簪~R~的形象，既是个人忧愁的写照，也是时代苦难的缩影。千百年来，这首诗以其沉郁顿挫的风格和忧国忧民的精神，感动了无数读者，成为中国古典诗歌中最著名的爱国诗篇之一。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 炼字 · 修辞 · 文化常识</span></div>
  <div class="box"><div class="acc-cat"><h3>文体与词牌</h3>
    <div class="acc-item"><span class="acc-w">五言律诗</span><span class="acc-d">《春望》是五言律诗，全诗八句，每句五字，共四十字。二、四、六、八句押韵（深、心、金、簪），中间两联对仗。</span></div>
    <div class="acc-item"><span class="acc-w">~L~望~R~的统摄</span><span class="acc-d">诗题~L~春望~R~即春天远望，全诗以~L~望~R~字统摄，由远望到近望，由望景到望情，层层递进。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>易错字音形</h3>
    <div class="acc-item"><span class="acc-w">溅</span><span class="acc-d">（jiàn）洒落，三点水，勿写~L~贱~R~。</span></div>
    <div class="acc-item"><span class="acc-w">搔</span><span class="acc-d">（sāo）抓挠，提手旁，勿写~L~骚~R~~L~瘙~R~。</span></div>
    <div class="acc-item"><span class="acc-w">簪</span><span class="acc-d">（zān）束发首饰，竹字头，勿写~L~赞~R~。</span></div>
    <div class="acc-item"><span class="acc-w">烽</span><span class="acc-d">（fēng）烽火，火字旁，勿写~L~锋~R~~L~峰~R~。</span></div>
    <div class="acc-item"><span class="acc-w">胜</span><span class="acc-d">（shēng）经受住，~L~不胜簪~R~，勿读 shèng。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>文言梳理</h3>
    <div class="acc-sub">古今异义</div>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">国</td><td>国都（指长安）</td><td>国家</td><td>国破山河在</td></tr>
      <tr><td class="kai">城</td><td>长安城</td><td>城市（泛指）</td><td>城春草木深</td></tr>
      <tr><td class="kai">书</td><td>书信</td><td>书本、书写</td><td>家书抵万金</td></tr>
      <tr><td class="kai">浑</td><td>简直、几乎</td><td>浑浊、糊涂</td><td>浑欲不胜簪</td></tr>
      <tr><td class="kai">胜</td><td>经受住（读 shēng）</td><td>胜利（读 shèng）</td><td>浑欲不胜簪</td></tr>
    </table></div>
    <div class="acc-sub">词类活用</div>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td class="kai">惊</td><td>形容词使动用法</td><td>使……惊动</td><td>恨别鸟惊心</td></tr>
    </table></div>
    <div class="acc-sub">文言句式</div>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">对偶句</td><td>感时花溅泪，恨别鸟惊心。</td><td>颔联对仗，动宾对动宾、名词对名词、动词对动词</td></tr>
      <tr><td class="kai">对偶句</td><td>烽火连三月，家书抵万金。</td><td>颈联对仗，名词对名词、动词对动词、数量对数量</td></tr>
      <tr><td class="kai">夸张</td><td>家书抵万金</td><td>~L~抵万金~R~夸张家书的珍贵</td></tr>
    </table></div>
  </div></div>
  <div class="box">
    <h3>炼字赏析（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>破——国破山河在</dt><dd>~L~破~R~字写出安史之乱后长安的残破，一字传神，将国都沦陷的惨状概括无遗。与~L~在~R~字形成对比——国已破，山河仍在，物是人非，更添悲痛。</dd></div>
      <div class="g-item"><dt>深——城春草木深</dt><dd>~L~深~R~字写出草木的茂盛丛生，也暗示了人烟的稀少。以往繁华的长安，如今只有草木丛生，一个~L~深~R~字，将战乱后的荒凉写得淋漓尽致。</dd></div>
      <div class="g-item"><dt>溅——感时花溅泪</dt><dd>~L~溅~R~字写出泪落的力度，仿佛泪是迸射而出的，将诗人悲痛的程度写得惊心动魄。移情于物，花也在溅泪。</dd></div>
      <div class="g-item"><dt>抵——家书抵万金</dt><dd>~L~抵~R~字写出家书的价值，~L~抵万金~R~用夸张手法，将战乱中家书的珍贵写到极致。后来~L~家书抵万金~R~成为成语。</dd></div>
      <div class="g-item"><dt>搔——白头搔更短</dt><dd>~L~搔~R~字写出诗人焦虑愁苦的动作，一个~L~搔~R~字，将内心的忧愁外化为可感的细节，含蓄深沉，余味无穷。</dd></div>
    </div>
  </div>
  <div class="box"><div class="acc-cat"><h3>修辞与手法</h3>
    <div class="acc-item"><span class="acc-w">移情于物</span><span class="acc-d">~L~感时花溅泪，恨别鸟惊心~R~，将人的情感投射到花鸟之上。</span></div>
    <div class="acc-item"><span class="acc-w">以乐景写哀</span><span class="acc-d">花鸟本是美好之物，在诗人眼中却带悲情，倍增其哀。</span></div>
    <div class="acc-item"><span class="acc-w">对偶</span><span class="acc-d">颔联、颈联皆对，对仗精工。</span></div>
    <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">~L~家书抵万金~R~，极言家书之珍贵。</span></div>
    <div class="acc-item"><span class="acc-w">细节描写</span><span class="acc-d">~L~白头搔更短，浑欲不胜簪~R~，以~L~搔~R~的动作和~L~不胜簪~R~的细节写忧愁。</span></div>
  </div></div>
  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>安史之乱</dt><dd>天宝十四载（755）至广德元年（763），安禄山、史思明发动的叛乱，是唐朝由盛转衰的转折点。叛军攻陷洛阳、长安，唐玄宗出逃四川。</dd></div>
      <div class="g-item"><dt>烽火</dt><dd>古代边防报警的烟火。敌人入侵时，守边将士在高台上点燃柴草，以烟火传递警报。诗中代指安史之乱的战火。</dd></div>
      <div class="g-item"><dt>簪</dt><dd>古人用来束发的首饰，男子成年后束发戴冠，用簪子固定。~L~不胜簪~R~指头发短少到插不住簪子，形容人憔悴衰老。</dd></div>
      <div class="g-item"><dt>诗史</dt><dd>后人对杜甫诗歌的美誉，认为其诗真实反映了安史之乱前后的社会现实，具有历史价值。~L~诗史~R~之称最早见于晚唐孟棨《本事诗》。</dd></div>
      <div class="g-item"><dt>沉郁顿挫</dt><dd>杜甫诗歌的艺术风格。~L~沉郁~R~指内容深沉博大，~L~顿挫~R~指表达抑扬曲折。《春望》是这一风格的典范之作。</dd></div>
      <div class="g-item"><dt>五言律诗</dt><dd>近体诗的一种，全诗八句，每句五字，共四十字。二、四、六、八句押韵，中间两联必须对仗。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《春望》杜甫</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">
<header class="hero">
  <div class="hero-side">唐 · 杜甫</div>
  <h1 class="hero-title">春望</h1>
</header>
<nav class="nav"><div class="nav-in">
    <a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a>
    <div class="tool">
      <select id="fsSel" class="fs-sel" title="正文字体大小">
        <option value="100">100%%</option><option value="150">150%%</option><option value="200">200%%</option><option value="250">250%%</option><option value="300">300%%</option>
      </select>
      <button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button>
    </div>
</div></nav>
<main class="wrap">
%(bg)s
<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>
  <div class="sec-sub">全诗八句，分两部分：春城败象、烽火家书。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《春望》</div>
  <div>杜甫 · 唐（712—770）· 至德二载被困长安作 · 五言律诗</div>
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
''' % {'css':CSS,'js':JS,'bg':BG,'app':APP,'acc':ACC,'fulltext':full_html,'verses':verses_html,'words':json.dumps(DICT_WORDS,ensure_ascii=False),'notes':json.dumps(DICT_NOTES,ensure_ascii=False)}
HTML = fixq(HTML)
io.open(OUT, 'w', encoding='utf-8').write(HTML)
print('OK', OUT, 'verses=', total, 'anno=', anno_count, 'words=', len(DICT_WORDS), 'notes=', len(DICT_NOTES))
