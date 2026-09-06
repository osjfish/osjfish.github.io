# -*- coding: utf-8 -*-
"""《次北固山下》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'cibeigushanxia-wangwan.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'cibeigushanxia_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


FULLTEXT = [
    "客路青山外，行舟绿水前。",
    "潮平两岸阔，风正一帆悬。",
    "海日生残夜，江春入旧年。",
    "乡书何处达？归雁洛阳边。",
]

PARTS = [
    ("第一部分", "旅途中景 · 潮平风正", "第 1–4 句",
     fixq("首联以对偶起笔，~L~客路青山外，行舟绿水前~R~，写诗人旅途中的行踪——客路在青山之外，行舟在绿水之前，暗含人在旅途、漂泊不定之意。颔联~L~潮平两岸阔，风正一帆悬~R~，写船上所见之景：潮水涨平，两岸开阔；风顺帆悬，行舟平稳。~L~平~R~~L~阔~R~~L~正~R~~L~悬~R~四字，炼字精当，写出了江面的开阔与行船的平稳，是千古传诵的名句。")),
    ("第二部分", "海日江春 · 乡思归雁", "第 5–8 句",
     fixq("颈联~L~海日生残夜，江春入旧年~R~，是全诗的千古名句。诗人在行舟中看到：残夜未尽，海上的太阳已经升起；旧年未过，江上的春意已经来临。~L~生~R~~L~入~R~二字，将海日江春拟人化，写出了时序交替、新旧更迭的自然规律，也蕴含着积极乐观的人生哲理。尾联~L~乡书何处达？归雁洛阳边~R~，见归雁而生乡思，托归雁传递家书，与首联~L~客路~R~呼应，点明全诗的思乡主题。")),
]

S = [
(0, "[[客路|旅人前行的路。客，旅人、游子]]青山外，[[行舟|行驶的船。行，行驶]]绿水前。",
 "旅人前行的路在青山之外，我乘坐的船行驶在绿水之前。",
 fixq("首联以对偶起笔，~L~客路~R~对~L~行舟~R~，~L~青山外~R~对~L~绿水前~R~，工整自然。~L~客路~R~点明诗人是游子身份，~L~青山外~R~写路途之远，暗含漂泊之意；~L~行舟~R~写当前的交通方式，~L~绿水前~R~写行舟所处的环境。两句一写来路，一写当前，将人在旅途的情景写得简洁而开阔。~L~青~R~~L~绿~R~二色，明丽清新，为全诗奠定了明快的基调。"),
 ["对偶", "起笔", "旅途"]),

(0, "[[潮平|潮水涨平。潮，潮水；平，涨平、与岸齐]]两岸[[阔|（kuò）开阔、宽阔]]，[[风正|风顺。正，顺、不歪斜]]一[[帆|船帆]][[悬|（xuán）悬挂、吊挂]]。",
 "潮水涨平，两岸之间水面宽阔；顺风行船，一张白帆高高悬挂。",
 fixq("颔联写船上所见之景，是千古传诵的名句。~L~潮平两岸阔~R~，写潮水涨满时，江面与两岸齐平，视野格外开阔——一个~L~平~R~字，写出了潮水的充盈；一个~L~阔~R~字，写出了江面的辽阔。~L~风正一帆悬~R~，写风顺而不猛，船帆端端直直地悬挂着——一个~L~正~R~字，写出了风的和顺；一个~L~悬~R~字，写出了船帆的高挂与行船的平稳。四字炼字精当，将江面的开阔与行船的平稳同时呈现，画面感极强，也暗含诗人旅途顺利、心境开阔的感受。"),
 ["对偶", "炼字", "名句", "写景"]),

(1, "[[海日|海上的太阳。海，这里指长江入海口附近的宽阔水面]]生[[残夜|（cán yè）夜将尽未尽之时。残，残余、将尽]]，[[江春|江上的春意]]入[[旧年|未尽的一年。旧年，过去的一年，这里指腊月]]。",
 "残夜未尽，海上的太阳已经升起；旧年未过，江上的春意已经来临。",
 fixq("颈联是全诗的千古名句，写诗人在行舟中看到的时序交替之景。~L~海日生残夜~R~，夜还没有完全过去，海上的太阳已经升起——一个~L~生~R~字，将海日拟人化，仿佛太阳是从残夜中~L~生~R~出来的，写出了新事物从旧事物中孕育而生的力量。~L~江春入旧年~R~，旧年还没有过去，江上的春意已经闯入——一个~L~入~R~字，将江春拟人化，仿佛春意是主动~L~闯~R~入旧年的，写出了新春的生机与活力。两句不仅写景，更蕴含着深刻的哲理：新事物必将取代旧事物，未来充满希望。这种积极乐观的精神，使这两句成为千古传诵的名句，当时的宰相张说曾亲手题写于政事堂，作为唐诗的典范。"),
 ["拟人", "炼字", "哲理", "名句", "千古传诵"]),

(1, "[[乡书|家信。乡，家乡；书，书信]]何处[[达|送到、到达]]？[[归雁|北归的大雁。归，返回；雁，大雁]]洛阳边。",
 "家信要怎样才能送到呢？希望北归的大雁捎到洛阳那边。",
 fixq("尾联由景入情，见归雁而生乡思。~L~乡书何处达？~R~以设问起笔，写诗人漂泊在外，不知家信如何才能送达；~L~归雁洛阳边~R~，诗人想到北归的大雁，希望托大雁把家信捎到洛阳（诗人的家乡）。~L~归雁~R~是古诗词中常见的意象，古人认为大雁可以传书，~L~鸿雁传书~R~的典故由来已久。这一联与首联~L~客路~R~呼应，~L~客路~R~写漂泊之始，~L~乡书~R~写思乡之情，首尾圆合，点明全诗的思乡主题。虽然全诗写景明丽开阔，但结尾的乡思之情真挚动人，使全诗景中有情、情因景生，余味悠长。"),
 ["设问", "用典", "思乡", "首尾呼应"]),
]


DICT_WORDS = [
    {"w":"潮","py":"cháo","q":"□平两岸阔，风正一帆悬。","tip":fixq("「潮」三点水，音 cháo，潮水、潮汐，~L~潮平~R~即潮水涨平，勿写~L~朝~R~（朝阳）")},
    {"w":"阔","py":"kuò","q":"潮平两岸□，风正一帆悬。","tip":fixq("「阔」门字框，音 kuò，开阔、宽阔，~L~两岸阔~R~即两岸之间水面宽阔，勿写~L~括~R~（括号）")},
    {"w":"悬","py":"xuán","q":"潮平两岸阔，风正一帆□。","tip":fixq("「悬」心字底，音 xuán，悬挂、吊挂，~L~帆悬~R~即船帆高挂，勿写~L~玄~R~（玄妙）")},
    {"w":"残","py":"cán","q":"海日生□夜，江春入旧年。","tip":fixq("「残」歹字旁，音 cán，残余、将尽，~L~残夜~R~即夜将尽未尽之时，勿写~L~惨~R~（悲惨）")},
    {"w":"雁","py":"yàn","q":"乡书何处达？归□洛阳边。","tip":fixq("「雁」厂字头，音 yàn，大雁，候鸟，~L~归雁~R~即北归的大雁，勿写~L~燕~R~（燕子，底部不同）")},
    {"w":"洛","py":"luò","q":"乡书何处达？归雁□阳边。","tip":fixq("「洛」三点水，音 luò，洛阳，地名，~L~洛阳~R~是诗人家乡，勿写~L~落~R~（落下）~L~络~R~（联络）")},
    {"w":"帆","py":"fān","q":"潮平两岸阔，风正一□悬。","tip":fixq("「帆」巾字旁，音 fān，船帆，利用风力使船前进的布篷，勿写~L~凡~R~（平凡）")},
    {"w":"绿","py":"lǜ","q":"客路青山外，行舟□水前。","tip":fixq("「绿」绞丝旁，音 lǜ，绿色，~L~绿水~R~即碧绿的江水，勿写~L~碌~R~（忙碌）")},
]

DICT_NOTES = [
    {"w":"客路","q":"客路青山外","a":"旅人前行的路。客，旅人、游子"},
    {"w":"青山","q":"客路青山外","a":"指北固山，在今江苏镇江北，三面临江"},
    {"w":"行舟","q":"行舟绿水前","a":"行驶的船。行，行驶"},
    {"w":"绿水","q":"行舟绿水前","a":"碧绿的江水，指长江"},
    {"w":"潮平","q":"潮平两岸阔","a":"潮水涨平。潮，潮水；平，涨平、与岸齐"},
    {"w":"阔","q":"潮平两岸阔","a":"（kuò）开阔、宽阔"},
    {"w":"风正","q":"风正一帆悬","a":"风顺。正，顺、不歪斜"},
    {"w":"悬","q":"风正一帆悬","a":"（xuán）悬挂、吊挂，这里指船帆高挂"},
    {"w":"海日","q":"海日生残夜","a":"海上的太阳。海，这里指长江入海口附近的宽阔水面"},
    {"w":"残夜","q":"海日生残夜","a":"（cán yè）夜将尽未尽之时。残，残余、将尽"},
    {"w":"江春","q":"江春入旧年","a":"江上的春意"},
    {"w":"旧年","q":"江春入旧年","a":"未尽的一年，这里指腊月（农历十二月）"},
    {"w":"乡书","q":"乡书何处达","a":"家信。乡，家乡；书，书信"},
    {"w":"达","q":"乡书何处达","a":"送到、到达"},
    {"w":"归雁","q":"归雁洛阳边","a":"北归的大雁。归，返回；雁，大雁。古人有鸿雁传书之说"},
    {"w":"洛阳","q":"归雁洛阳边","a":"地名，今河南洛阳，诗人王湾的家乡"},
    {"w":"生","q":"海日生残夜","a":"升起、孕育而生，拟人手法"},
    {"w":"入","q":"江春入旧年","a":"闯入、进入，拟人手法"},
]


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
    <p>《次北固山下》是唐代诗人王湾的代表作，作于唐玄宗开元年间（713—741）。当时王湾游历江南，舟行至北固山下（今江苏镇江北），被江上的壮丽景色所感染，写下了这首千古传诵的五言律诗。</p>
    <p>全诗以~L~客路~R~起笔，写旅途中的所见所感。颔联~L~潮平两岸阔，风正一帆悬~R~写江面开阔、行船平稳；颈联~L~海日生残夜，江春入旧年~R~写时序交替、新旧更迭，是千古传诵的名句，蕴含着新事物必将取代旧事物的深刻哲理；尾联~L~乡书何处达？归雁洛阳边~R~托归雁传书，抒发思乡之情。全诗写景明丽，哲理深刻，乡情真挚，是盛唐山水诗的典范之作。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>王湾（约693—约751），洛阳（今河南洛阳）人，唐代诗人。玄宗先天年间（712—713）进士，曾任荥阳主簿、洛阳尉等职。王湾是盛唐初年的重要诗人，与綦毋潜、储光羲等交往密切，其诗多写山水田园和羁旅之情，风格清丽自然。</p>
    <p>王湾一生诗作不多，《全唐诗》仅存其诗十首，但《次北固山下》一首足以使他名垂千古。当时的宰相张说曾亲手将~L~海日生残夜，江春入旧年~R~两句题写于政事堂，作为唐诗的典范，供文人学习。这两句诗对后世影响深远，被认为是盛唐气象的先声。</p>
    <p class="note">※ 王湾存诗虽少，但一首《次北固山下》奠定了他在唐诗史上的地位，是~L~以一首诗名垂千古~R~的典型代表。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>开元盛世：</b>唐玄宗开元年间（713—741），是唐朝的全盛时期，国力强盛、经济繁荣、文化昌盛，史称~L~开元盛世~R~。王湾生活在这样一个时代，诗歌中充满了积极乐观的精神和开阔明朗的气象。</p>
    <p><b>漫游之风：</b>唐代文人普遍有漫游的风气，青年士子在科举前后往往游历名山大川，开阔眼界，结交朋友。王湾游历江南，舟行至北固山下，被江上景色所感染，写下了这首诗。</p>
    <p><b>北固山：</b>北固山在今江苏镇江北，三面临江，地势险要，是长江下游的名胜。南朝梁武帝曾题书~L~天下第一江山~R~。历代文人墨客多有题咏，王湾的《次北固山下》是其中最著名的一首。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《次北固山下》是一首<b>五言律诗</b>，全诗八句，每句五字，共四十字。首联（一二句）对偶起笔，颔联（三四句）继续对仗，颈联（五六句）对仗精工，尾联（七八句）设问收束。全诗格律严谨，对仗工整，是五言律诗的典范之作。</p>
    <p>诗题中的~L~次~R~是~L~停泊~R~的意思，~L~北固山~R~是山名，~L~下~R~指山下。~L~次北固山下~R~即停泊在北固山下。这首诗写的是诗人舟行途中停泊北固山下时所见的景色和所感的乡情。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>【爱上古诗】次北固山下——王湾（动画朗诵）</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1vR4y1o7xW&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="次北固山下动画朗诵"></iframe>
        <a href="https://www.bilibili.com/video/BV1vR4y1o7xW" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>C叔聊诗词：《次北固山下》孤篇封神第二人</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1vK4y1B7Nw&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="次北固山下深度解读"></iframe>
        <a href="https://www.bilibili.com/video/BV1vK4y1B7Nw" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">王湾——漂泊中的乐观诗人</div>
        <p>《次北固山下》中的抒情主人公，是一位漂泊在外却积极乐观的游子形象。他舟行江上，面对潮平岸阔、海日江春的壮美景象，心中既有旅途中的乡思，更有对未来的希望。</p>
        <p><b>漂泊中的开阔：</b>~L~客路青山外，行舟绿水前~R~，诗人虽然是在旅途中，但他看到的不是凄风苦雨，而是青山绿水、潮平岸阔的明丽景象。这种开阔的视野，正是诗人开阔胸襟的写照。</p>
        <p><b>困境中的希望：</b>~L~海日生残夜，江春入旧年~R~，在残夜与旧年的困境中，诗人看到的是海日升起、江春来临的希望。这种在黑暗中看到光明、在旧岁中看到新春的眼光，体现了诗人积极乐观的人生态度。</p>
        <p><b>真挚的乡思：</b>~L~乡书何处达？归雁洛阳边~R~，诗人虽然乐观，但漂泊在外的乡思是真挚的。托归雁传书，既写出了乡思的深切，也写出了诗人的浪漫情怀。这个形象，是盛唐诗人的典型代表——即使在旅途中，也充满了积极进取的精神。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">炼字精当——平、阔、正、悬、生、入</div>
        <p>《次北固山下》是唐诗炼字的典范之作：</p>
        <p><b>~L~平~R~字：</b>~L~潮平两岸阔~R~，~L~平~R~字写出潮水涨满、与岸齐平的状态，为~L~阔~R~字做铺垫——正因为潮平，才显得两岸格外开阔。</p>
        <p><b>~L~阔~R~字：</b>~L~潮平两岸阔~R~，~L~阔~R~字写出江面的辽阔，也写出诗人视野的开阔和心境的开阔。</p>
        <p><b>~L~正~R~字：</b>~L~风正一帆悬~R~，~L~正~R~字写出风的和顺——不是狂风，也不是微风，而是恰到好处的顺风，使船帆端端直直地悬挂着。</p>
        <p><b>~L~悬~R~字：</b>~L~风正一帆悬~R~，~L~悬~R~字写出船帆高挂的状态，也写出行船的平稳和江面的开阔。</p>
        <p><b>~L~生~R~字：</b>~L~海日生残夜~R~，~L~生~R~字将海日拟人化，仿佛太阳是从残夜中孕育而生的，写出了新事物从旧事物中诞生的力量。</p>
        <p><b>~L~入~R~字：</b>~L~江春入旧年~R~，~L~入~R~字将江春拟人化，仿佛春意是主动闯入旧年的，写出了新春的生机与活力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">情景交融，景中含理</div>
        <p>全诗写景明丽，抒情真挚，更难得的是景中蕴含哲理。~L~海日生残夜，江春入旧年~R~不仅是写景，更蕴含着新事物必将取代旧事物的深刻哲理——残夜中孕育着海日，旧年中孕育着江春，黑暗终将过去，光明必将到来。这种景中含理的写法，使全诗既有山水诗的审美价值，又有哲理诗的思想深度，是唐诗中情景理交融的典范。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对仗精工，首尾圆合</div>
        <p><b>对仗精工：</b>首联~L~客路青山外，行舟绿水前~R~、颔联~L~潮平两岸阔，风正一帆悬~R~、颈联~L~海日生残夜，江春入旧年~R~，三联皆对，对仗工整而不呆板，格律严谨而不失灵动。</p>
        <p><b>首尾圆合：</b>首联~L~客路~R~写漂泊之始，尾联~L~乡书~R~写思乡之情，首尾呼应，结构完整。全诗以~L~客路~R~起，以~L~归雁~R~结，人在旅途的线索贯穿始终。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">海日生残夜，江春入旧年。</div>
        <p>这是全诗的千古名句，也是唐诗中最著名的诗句之一。诗人在行舟中看到：残夜未尽，海上的太阳已经升起；旧年未过，江上的春意已经来临。~L~生~R~~L~入~R~二字，将海日江春拟人化，写出了时序交替、新旧更迭的自然规律。这两句不仅写景逼真，更蕴含着深刻的哲理：新事物必将取代旧事物，未来充满希望。当时的宰相张说曾亲手将这两句题写于政事堂，作为唐诗的典范。千百年来，这两句诗激励着无数人在困境中看到希望，在黑暗中看到光明。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">潮平两岸阔，风正一帆悬。</div>
        <p>这两句写船上所见之景，画面感极强。潮水涨平，两岸之间水面格外开阔；风顺帆悬，行船平稳前行。~L~平~R~~L~阔~R~~L~正~R~~L~悬~R~四字，炼字精当，将江面的开阔与行船的平稳同时呈现。这两句不仅写出了江上的壮美景象，也暗含诗人旅途顺利、心境开阔的感受，是盛唐气象的生动写照。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《次北固山下》通过描写舟行北固山下时所见的江上壮美景象，抒发了诗人漂泊在外的思乡之情，表达了积极乐观、奋发进取的人生态度和对未来充满希望的精神信念。</p>
    <p>这首诗的深刻之处在于，它不仅是一首写景诗、一首思乡诗，更是一首蕴含哲理的言志诗。~L~海日生残夜，江春入旧年~R~所蕴含的新事物必将取代旧事物的哲理，使全诗超越了一般的山水羁旅之作，具有了普遍的人生意义。这种在困境中看到希望、在黑暗中看到光明的积极精神，正是盛唐气象的体现，也是这首诗千古传诵的根本原因。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 炼字 · 修辞 · 文化常识</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>文体与词牌</h3>
      <div class="acc-item"><span class="acc-w">五言律诗</span><span class="acc-d">《次北固山下》是五言律诗，全诗八句，每句五字，共四十字。二、四、六、八句押韵（前、悬、年、边），中间两联必须对仗。</span></div>
      <div class="acc-item"><span class="acc-w">~L~次~R~的含义</span><span class="acc-d">诗题中的~L~次~R~是~L~停泊~R~的意思，~L~次北固山下~R~即停泊在北固山下。</span></div>
      <div class="acc-item"><span class="acc-w">三联皆对</span><span class="acc-d">本诗首联、颔联、颈联皆对仗，在律诗中较为少见，对仗精工而不呆板。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>易错字音形</h3>
      <div class="acc-item"><span class="acc-w">悬</span><span class="acc-d">（xuán）悬挂，心字底，勿写~L~玄~R~。</span></div>
      <div class="acc-item"><span class="acc-w">残</span><span class="acc-d">（cán）残余，歹字旁，勿写~L~惨~R~。</span></div>
      <div class="acc-item"><span class="acc-w">雁</span><span class="acc-d">（yàn）大雁，厂字头，勿写~L~燕~R~（底部不同）。</span></div>
      <div class="acc-item"><span class="acc-w">洛</span><span class="acc-d">（luò）洛阳，三点水，勿写~L~落~R~~L~络~R~。</span></div>
      <div class="acc-item"><span class="acc-w">潮</span><span class="acc-d">（cháo）潮水，三点水，勿写~L~朝~R~。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文言梳理</h3>
      <div class="acc-sub">古今异义</div>
      <div class="tw"><table>
        <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
        <tr><td class="kai">次</td><td>停泊（动词）</td><td>次序、次等（名词/形容词）</td><td>次北固山下</td></tr>
        <tr><td class="kai">客路</td><td>旅人前行的路</td><td>客人走的路</td><td>客路青山外</td></tr>
        <tr><td class="kai">书</td><td>书信（名词）</td><td>书本、书写</td><td>乡书何处达</td></tr>
        <tr><td class="kai">达</td><td>送到、到达</td><td>到达、通达、表达</td><td>乡书何处达</td></tr>
      </table></div>
      <div class="acc-sub">一词多义</div>
      <div class="tw"><table>
        <tr><th>词</th><th>义项</th><th>例句</th></tr>
        <tr><td class="kai" rowspan="2">正</td><td>顺、不歪斜</td><td>风正一帆悬</td></tr>
        <tr><td>正好、恰好</td><td>正合我意</td></tr>
        <tr><td class="kai" rowspan="2">生</td><td>升起、孕育（拟人）</td><td>海日生残夜</td></tr>
        <tr><td>生长、生存</td><td>树木丛生</td></tr>
      </table></div>
      <div class="acc-sub">词类活用</div>
      <div class="tw"><table>
        <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
        <tr><td class="kai">生</td><td>名词作动词（拟人）</td><td>升起、孕育而生</td><td>海日生残夜</td></tr>
        <tr><td class="kai">入</td><td>名词作动词（拟人）</td><td>闯入、进入</td><td>江春入旧年</td></tr>
      </table></div>
      <div class="acc-sub">文言句式</div>
      <div class="tw"><table>
        <tr><th>句式</th><th>例句</th><th>说明</th></tr>
        <tr><td class="kai">设问句</td><td>乡书何处达？归雁洛阳边。</td><td>自问自答，以设问收束全诗，点明乡思</td></tr>
        <tr><td class="kai">对偶句</td><td>潮平两岸阔，风正一帆悬。</td><td>颔联对仗，名词对名词、形容词对形容词、动词对动词</td></tr>
        <tr><td class="kai">对偶句</td><td>海日生残夜，江春入旧年。</td><td>颈联对仗，名词对名词、动词对动词、名词对名词</td></tr>
      </table></div>
    </div>
  </div>

  <div class="box">
    <h3>炼字赏析（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>平——潮平两岸阔</dt><dd>~L~平~R~字写出潮水涨满、与岸齐平的状态，为~L~阔~R~字做铺垫——正因为潮平，才显得两岸格外开阔。一个~L~平~R~字，将江水的充盈写得恰到好处。</dd></div>
      <div class="g-item"><dt>阔——潮平两岸阔</dt><dd>~L~阔~R~字写出江面的辽阔，也写出诗人视野的开阔和心境的开阔。一个~L~阔~R~字，将江面的宽广和诗人的胸襟同时呈现。</dd></div>
      <div class="g-item"><dt>正——风正一帆悬</dt><dd>~L~正~R~字写出风的和顺——不是狂风，也不是微风，而是恰到好处的顺风。一个~L~正~R~字，将行船的顺利和诗人的顺遂同时写出。</dd></div>
      <div class="g-item"><dt>生——海日生残夜</dt><dd>~L~生~R~字将海日拟人化，仿佛太阳是从残夜中孕育而生的。一个~L~生~R~字，写出了新事物从旧事物中诞生的力量，也蕴含着新事物必将取代旧事物的哲理。</dd></div>
      <div class="g-item"><dt>入——江春入旧年</dt><dd>~L~入~R~字将江春拟人化，仿佛春意是主动闯入旧年的。一个~L~入~R~字，写出了新春的生机与活力，也写出了新旧交替的必然趋势。</dd></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞与手法</h3>
      <div class="acc-item"><span class="acc-w">拟人</span><span class="acc-d">~L~生~R~~L~入~R~二字将海日江春拟人化，写出时序交替的生机。</span></div>
      <div class="acc-item"><span class="acc-w">对偶</span><span class="acc-d">首联、颔联、颈联皆对，三联皆对在律诗中较为少见。</span></div>
      <div class="acc-item"><span class="acc-w">设问</span><span class="acc-d">~L~乡书何处达？归雁洛阳边~R~，自问自答，点明乡思。</span></div>
      <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">~L~归雁~R~暗用鸿雁传书的典故，托大雁传递家书。</span></div>
      <div class="acc-item"><span class="acc-w">情景交融</span><span class="acc-d">写景明丽，乡情真挚，景中含理，情景理交融。</span></div>
    </div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>北固山</dt><dd>在今江苏镇江北，三面临江，地势险要，是长江下游的名胜。南朝梁武帝曾题书~L~天下第一江山~R~。历代文人墨客多有题咏。</dd></div>
      <div class="g-item"><dt>鸿雁传书</dt><dd>古代传说大雁可以传递书信。《汉书·苏武传》载，苏武出使匈奴被扣留，后汉使谎称天子射雁得书，苏武得以归汉。后以~L~鸿雁~R~~L~归雁~R~代指传递书信或书信。</dd></div>
      <div class="g-item"><dt>洛阳</dt><dd>今河南洛阳，唐代东都，是王湾的家乡。洛阳是中国历史文化名城，九朝古都，唐代时是仅次于长安的政治文化中心。</dd></div>
      <div class="g-item"><dt>五言律诗</dt><dd>近体诗的一种，全诗八句，每句五字，共四十字。二、四、六、八句押韵，首句可押可不押。中间两联（颔联、颈联）必须对仗。</dd></div>
      <div class="g-item"><dt>盛唐气象</dt><dd>指唐玄宗开元、天宝年间（713—756）诗歌所体现的积极乐观、开阔明朗、奋发进取的时代精神。《次北固山下》是盛唐气象的先声和典范。</dd></div>
      <div class="g-item"><dt>张说题诗</dt><dd>张说是唐玄宗时期的宰相，也是著名文学家。他曾亲手将~L~海日生残夜，江春入旧年~R~题写于政事堂，作为唐诗的典范，供文人学习，一时传为佳话。</dd></div>
    </div>
  </div>

</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《次北固山下》王湾</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">唐 · 王湾</div>
  <h1 class="hero-title">次北固山下</h1>
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
  <div class="sec-sub">全诗八句，分两部分：旅途中景、海日乡思。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《次北固山下》</div>
  <div>王湾 · 唐（约693—约751）· 开元年间舟行北固山下作 · 五言律诗</div>
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
print('OK', OUT, 'verses=', total, 'anno=', anno_count, 'words=', len(DICT_WORDS), 'notes=', len(DICT_NOTES))
