# -*- coding: utf-8 -*-
"""《富贵不能淫》课件生成器 —— 复用《鸿门宴》课件的 CSS / JS 框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = r'D:\App\Apps\yanshi\hongmenyan-shiji.html'
OUT = r'D:\App\Apps\yanshi\fuguibunengyin-mengzi.html'

src = io.open(SRC, encoding='utf-8').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('hongmen_fs', 'fugui_fs')
_js_start = JS.index('var DICT_WORDS')
_js_end = JS.index('/* ---------- 听写模式 ---------- */')
JS = JS[:_js_start] + JS[_js_end:]


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)

def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    '景春曰：~L~公孙衍、张仪岂不诚大丈夫哉？一怒而诸侯惧，安居而天下熄。~R~',
    '孟子曰：~L~是焉得为大丈夫乎？子未学礼乎？~R~',
    '~L~丈夫之冠也，父命之；女子之嫁也，母命之，往送之门，戒之曰：~L~往之女家，必敬必戒，无违夫子！~R~以顺为正者，妾妇之道也。~R~',
    '~L~居天下之广居，立天下之正位，行天下之大道。~R~',
    '~L~得志，与民由之；不得志，独行其道。~R~',
    '~L~富贵不能淫，贫贱不能移，威武不能屈。此之谓大丈夫。~R~',
]

# ---------------- 逐句数据 ----------------
S = [
("[[景春|人名，孟子同时代人，纵横家信徒]][[曰|说]]：~L~[[公孙衍|人名，战国时期魏国人，纵横家，曾佩五国相印]][[、|顿号，表并列]][[张仪|人名，战国时期魏国人，纵横家，秦国相，主张连横]][[岂|难道，表反问]][[不|否定副词]][[诚|真正、确实]][[大丈夫|指有大志、有作为、有气节的男子]][[哉|句末语气词，表反问，相当于~L~呢~R~]]？[[一怒|一旦发怒。一，一旦]][[而|表顺承，就]][[诸侯|指各诸侯国的君主]][[惧|害怕、恐惧]]，[[安居|安静地居住，指不出来活动]][[而|表顺承，就]][[天下熄|指战争停息，天下太平。熄，通~L~息~R~，停息]]。~R~",
 "景春说：~L~公孙衍、张仪难道不是真正的大丈夫吗？他们一发怒，诸侯就都害怕；他们安静下来，天下就太平无事。~R~",
 fixq("景春提出辩题，以公孙衍、张仪为~L~大丈夫~R~的标准——位高权重、一怒而天下惧。~L~岂不……哉~R~反问句式，语气强烈，表现出景春对纵横家的推崇。~L~一怒而诸侯惧，安居而天下熄~R~以夸张笔法写纵横家的威势，为下文孟子的反驳树立靶子。"),
 ["景春发难", "反问", "夸张"]),

("[[孟子|名轲，战国时期儒家代表人物]][[曰|说]]：~L~[[是|这、这个，代词]][[焉|怎么、哪里，疑问代词]][[得|能够、可以]][[为|算作、是]][[大丈夫|有大志、有作为、有气节的男子]][[乎|句末语气词，表反问，相当于~L~呢~R~]]？[[子|你，对对方的尊称]][[未|没有]][[学|学习]][[礼|礼仪、礼节]][[乎|句末语气词，表疑问，相当于~L~吗~R~]]？~R~",
 "孟子说：~L~这怎么能算大丈夫呢？你没有学过礼吗？~R~",
 fixq("孟子断然否定，以两个反问句反驳景春。~L~是焉得为大丈夫乎~R~直接否定，语气斩钉截铁；~L~子未学礼乎~R~引出下文以~L~礼~R~论人的论证，从~L~冠礼~R~~L~婚礼~R~说起，指出纵横家的~L~顺~R~不过是~L~妾妇之道~R~。"),
 ["断然否定", "反问", "引出下文"]),

("~L~[[丈夫|成年男子。古时男子二十岁行冠礼，表示成年]][[之冠|行冠礼。之，用在主谓之间，取消句子独立性；冠（guàn），行冠礼，名词作动词]][[也|句中语气词，表停顿]]，[[父命之|父亲训导他。命，教导、训诲；之，代词，指行冠礼的男子]]；[[女子|女儿]][[之嫁|出嫁。之，取消句子独立性；嫁，出嫁]][[也|句中语气词，表停顿]]，[[母命之|母亲训导她]]，[[往送之门|送她到门口。往，到；之，动词，到]][[戒之曰|告诫她说。戒，告诫]][[往之女家|到了你夫家。之，到；女（rǔ），通~L~汝~R~，你]][[必敬必戒|一定要恭敬，一定要谨慎。必，一定；敬，恭敬；戒，谨慎]][[无违夫子|不要违背丈夫。无，通~L~毋~R~，不要；违，违背；夫子，旧时妻称夫为夫子]]！~R~[[以顺为正者|把顺从当作准则的。以……为，把……当作；顺，顺从；正，准则、正道]][[妾妇之道也|是妾妇的行为准则。妾妇，泛指妇女；之，的；道，行为准则、道理。也，表判断]]。~R~",
 "~L~男子行加冠礼时，父亲训导他；女子出嫁时，母亲训导她，送她到门口，告诫她说：~L~到了你夫家，一定要恭敬，一定要谨慎，不要违背你的丈夫！~R~把顺从当作准则，是妾妇的行为准则。~R~",
 fixq("孟子以~L~礼~R~为据，用冠礼、婚礼中~L~父命之~R~~L~母命之~R~的事实，引出~L~以顺为正~R~的妾妇之道。~L~必敬必戒，无违夫子~R~是女子出嫁时的训诫，核心是~L~顺~R~。孟子以此类比纵横家：公孙衍、张仪之流一味顺从君主之意，与妾妇~L~无违夫子~R~并无本质区别，岂能称为大丈夫？比喻精当，讽刺辛辣。注意嵌套引号外双内单。"),
 ["类比论证", "嵌套引号", "妾妇之道"]),

("~L~[[居天下之广居|居住在天下最宽广的住宅里。居，居住；广居，喻指~L~仁~R~，儒家认为仁是天下最宽广的安身之所]][[立天下之正位|站在天下最正确的位置上。立，站立；正位，喻指~L~礼~R~]][[行天下之大道|走在天下最光明的大路上。行，行走；大道，喻指~L~义~R~]]。~R~",
 "~L~（大丈夫应该）住进天下最宽广的住宅——仁，站在天下最正确的位置——礼，走着天下最光明的道路——义。~R~",
 fixq("孟子正面提出大丈夫的立身处世之道。三个排比句，~L~广居~R~~L~正位~R~~L~大道~R~分别喻指~L~仁~R~~L~礼~R~~L~义~R~，是儒家道德理想的形象化表达。句式整齐，气势磅礴，与上文~L~妾妇之道~R~形成鲜明对比。"),
 ["排比", "比喻", "仁礼义"]),

("~L~[[得志|实现志向。得，实现；志，志向]][[与民由之|与百姓一同遵循正道而行。由，遵循、遵从；之，代词，指正道]]；[[不得志|没有实现志向]][[独行其道|独自走自己的道路。独，独自；行，走、坚持；其，自己的；道，道路、原则]]。~R~",
 "~L~得志的时候，与百姓一同遵循正道而行；不得志的时候，独自走自己的道路。~R~",
 fixq("从得志与不得志两种境遇写大丈夫的处世原则。~L~与民由之~R~写得志时兼济天下，~L~独行其道~R~写不得志时独善其身。无论境遇如何，都坚守道义，不改其志。这是对~L~穷则独善其身，达则兼善天下~R~的化用，体现了儒家的处世智慧。"),
 ["对比", "兼济与独善"]),

("~L~[[富贵不能淫|富贵不能使他迷惑。淫，使……迷惑，使动用法]][[贫贱不能移|贫贱不能使他动摇。移，使……动摇、改变，使动用法]][[威武不能屈|威武不能使他屈服。屈，使……屈服，使动用法]]。[[此之谓大丈夫|这才叫作大丈夫。此，这；之，助词，宾语前置的标志；谓，叫作、称作]]。~R~",
 "~L~富贵不能使他迷惑，贫贱不能使他动摇，威武不能使他屈服。这才叫作大丈夫。~R~",
 fixq("全文核心名句，以三个~L~不能~R~排比，从富贵、贫贱、威武三个方面写大丈夫的气节。~L~淫~R~~L~移~R~~L~屈~R~均为使动用法，三字力重千钧。~L~此之谓大丈夫~R~收束全文，与开头景春的~L~岂不诚大丈夫哉~R~遥相呼应，完成了对~L~大丈夫~R~的重新定义。这一名句成为后世无数仁人志士的座右铭。"),
 ["名句", "排比", "使动用法", "主旨"]),
]

# ---------------- 字形题 ----------------
DICT_WORDS = [
    {"w":"衍","py":"yǎn","q":"公孙□、张仪岂不诚大丈夫哉","tip":"「衍」双人旁，音 yǎn；与「演」「衔」区分，右部是「行」中间加「水」"},
    {"w":"仪","py":"yí","q":"公孙衍、张□岂不诚大丈夫哉","tip":"「仪」单人旁，音 yí；与「义」「议」区分"},
    {"w":"冠","py":"guàn","q":"丈夫之□也，父命之","tip":"「冠」多音字，行冠礼读 guàn（四声），帽子读 guān（一声）；与「寇」区分"},
    {"w":"戒","py":"jiè","q":"必敬必□，无违夫子","tip":"「戒」戈字头，音 jiè，谨慎、告诫；与「戎」（róng，兵器）「戌」（xū）区分"},
    {"w":"淫","py":"yín","q":"富贵不能□","tip":"「淫」三点水，音 yín，使迷惑；与「谣」「摇」区分，右部是「𠬶」不是「䍃」"},
    {"w":"贱","py":"jiàn","q":"贫□不能移","tip":"「贱」贝字旁，音 jiàn，地位低下；与「钱」「浅」区分，右部是「戋」"},
    {"w":"屈","py":"qū","q":"威武不能□","tip":"「屈」尸字头，音 qū，屈服；与「曲」「倔」区分，下部是「出」"},
    {"w":"熄","py":"xī","q":"安居而天下□","tip":"「熄」火字旁，音 xī，通「息」，停息；与「息」「媳」区分"},
]

# ---------------- 注释题 ----------------
DICT_NOTES = [
    {"w":"诚","q":"公孙衍、张仪岂不诚大丈夫哉？","a":"真正、确实"},
    {"w":"大丈夫","q":"公孙衍、张仪岂不诚大丈夫哉？","a":"指有大志、有作为、有气节的男子"},
    {"w":"熄","q":"安居而天下熄","a":"通「息」，停息，指战争停息"},
    {"w":"焉","q":"是焉得为大丈夫乎？","a":"怎么、哪里，疑问代词"},
    {"w":"冠","q":"丈夫之冠也，父命之","a":"（guàn）行冠礼，名词作动词"},
    {"w":"命","q":"丈夫之冠也，父命之","a":"教导、训诲"},
    {"w":"女","q":"往之女家，必敬必戒","a":"通「汝」，你"},
    {"w":"夫子","q":"无违夫子","a":"旧时妻称夫为夫子，这里指丈夫"},
    {"w":"以顺为正","q":"以顺为正者，妾妇之道也","a":"把顺从当作准则。以……为，把……当作"},
    {"w":"妾妇之道","q":"以顺为正者，妾妇之道也","a":"妾妇的行为准则，这里指一味顺从的做法"},
    {"w":"广居","q":"居天下之广居","a":"喻指「仁」，天下最宽广的安身之所"},
    {"w":"正位","q":"立天下之正位","a":"喻指「礼」，天下最正确的位置"},
    {"w":"大道","q":"行天下之大道","a":"喻指「义」，天下最光明的道路"},
    {"w":"由","q":"得志，与民由之","a":"遵循、遵从"},
    {"w":"独行其道","q":"不得志，独行其道","a":"独自走自己的道路，指坚守原则"},
    {"w":"淫","q":"富贵不能淫","a":"使……迷惑，使动用法"},
    {"w":"移","q":"贫贱不能移","a":"使……动摇、改变，使动用法"},
    {"w":"屈","q":"威武不能屈","a":"使……屈服，使动用法"},
    {"w":"此之谓","q":"此之谓大丈夫","a":"这才叫作。之，宾语前置标志"},
]

# ---------------- 组装 ----------------
def build_verses():
    out = []
    for idx, (txt, yi, shang, tags) in enumerate(S):
        out.append('      <div class="verse" id="l%d" data-i="%d">' % (idx + 1, idx))
        out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx + 1, annotate(fixq(txt))))
        out.append('        <details class="v-more">')
        out.append('          <summary>译文 · 赏析</summary>')
        out.append('          <div class="d-body">')
        out.append('            <div class="v-sec"><b class="v-label">译　文</b>')
        out.append('              <div class="v-trans">%s</div>' % fixq(yi))
        out.append('            </div>')
        out.append('            <div class="v-sec"><b class="v-label">赏　析</b>')
        out.append('              <div class="d-body"><p>%s</p></div>' % shang)
        if tags:
            out.append('              <div class="tags">%s</div>' % ''.join('<span>%s</span>' % t for t in tags))
        out.append('            </div>')
        out.append('          </div>')
        out.append('        </details>')
        out.append('      </div>')
    return '\n'.join(out)

verses_html = build_verses()
full_html = '\n'.join('      <p class="pl">%s</p>' % fixq(p) for p in FULLTEXT)

BG = fixq(u'''
  <section id="bg" class="sec">
    <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
    <div class="lead">
      战国中期，纵横家横行天下，公孙衍、张仪之流~L~一怒而诸侯惧，安居而天下熄~R~，时人多以为大丈夫。孟子不以为然，以~L~礼~R~为据，以~L~妾妇之道~R~讽之，进而提出~L~富贵不能淫，贫贱不能移，威武不能屈~R~的大丈夫标准——这三句话，成为中华民族精神的千古丰碑。
    </div>
    <div class="box">
      <h3>作者简介</h3>
      <p><b>孟子</b>（约前372—前289），名轲，字子舆，战国时期邹国（今山东邹城）人。儒家学派代表人物，被后世尊为~L~亚圣~R~。他继承并发展了孔子的思想，主张~L~仁政~R~~L~王道~R~，提出~L~民贵君轻~R~的民本思想和~L~性善论~R~。</p>
      <p>《孟子》一书记录孟子及其弟子的言行，共七篇。其文气势充沛，感情强烈，善于雄辩，长于比喻。本文选自《孟子·滕文公下》。</p>
    </div>
    <div class="box">
      <h3>创作背景</h3>
      <p>战国时期，诸侯争霸，纵横家应运而生。他们以口舌之才游说诸侯，左右时局，显赫一时。公孙衍主张~L~合纵~R~（联合六国抗秦），张仪主张~L~连横~R~（事秦攻他国），两人一怒一安，天下随之动荡。景春是纵横家的信徒，认为公孙衍、张仪就是~L~大丈夫~R~。</p>
      <p>孟子反对纵横家~L~朝秦暮楚~R~~L~惟利是图~R~的行事作风，认为他们不过是~L~以顺为正~R~的妾妇之流。本文通过与景春的对话，正面阐述了儒家心目中~L~大丈夫~R~的标准，体现了孟子~L~富贵不淫、贫贱不移、威武不屈~R~的高尚人格。</p>
      <p class="note">※ 纵横家：战国时期从事政治外交活动的谋士，以审察时势、游说君主为能事，代表人物有苏秦、张仪、公孙衍等。</p>
    </div>
    <div class="box media-box">
      <h3>朗诵 · 讲解</h3>
      <div class="media-grid">
        <div class="media">
          <h4>课文朗读《富贵不能淫》</h4>
          <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1rK411A7s8&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读《富贵不能淫》"></iframe>
          <a href="https://www.bilibili.com/video/BV1rK411A7s8" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
        </div>
        <div class="media">
          <h4>动画讲解《富贵不能淫》</h4>
          <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1fJ411A7Ng&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="动画讲解《富贵不能淫》"></iframe>
          <a href="https://www.bilibili.com/video/BV1fJ411A7Ng" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
        </div>
      </div>
    </div>
  </section>
''')

APP = fixq(u'''
  <section id="app" class="sec">
    <div class="sec-head"><h2>赏 析</h2><span class="no">对话 · 论证 · 艺术 · 名句</span></div>
    <div class="box">
      <h3>对话结构</h3>
      <p>全文采用对话体，可分两层：</p>
      <p><b>第一层（景春之问）</b>：景春以公孙衍、张仪为例，认为他们~L~一怒而诸侯惧，安居而天下熄~R~，是真正的大丈夫。这是孟子要反驳的靶子。</p>
      <p><b>第二层（孟子之答）</b>：孟子先以~L~是焉得为大丈夫乎~R~断然否定，再以~L~子未学礼乎~R~引出论证。他先用冠礼、婚礼中~L~以顺为正~R~的妾妇之道类比纵横家，指出其本质是顺从；然后正面提出大丈夫的立身处世之道——居仁、由礼、行义；最后以~L~富贵不能淫，贫贱不能移，威武不能屈~R~收束，完成对~L~大丈夫~R~的定义。</p>
    </div>
    <div class="box">
      <h3>论证方法</h3>
      <p><b>① 类比论证</b>：以~L~妾妇之道~R~类比纵横家的~L~以顺为正~R~，指出公孙衍、张仪之流不过是一味顺从君主的妾妇之辈，辛辣讽刺。</p>
      <p><b>② 对比论证</b>：~L~妾妇之道~R~与~L~大丈夫之道~R~对比，~L~得志~R~与~L~不得志~R~对比，富贵、贫贱、威武三种境遇对比，观点鲜明。</p>
      <p><b>③ 排比论证</b>：~L~居天下之广居，立天下之正位，行天下之大道~R~三句排比，~L~富贵不能淫，贫贱不能移，威武不能屈~R~三句排比，气势充沛，掷地有声。</p>
    </div>
    <div class="box">
      <h3>艺术特色</h3>
      <p><b>① 先破后立，破立结合</b>：先否定景春的~L~大丈夫~R~标准（破），再提出儒家的大丈夫标准（立），论证有力。</p>
      <p><b>② 善用比喻，形象生动</b>：以~L~广居~R~~L~正位~R~~L~大道~R~喻仁、礼、义，以~L~妾妇之道~R~喻纵横家的顺从，化抽象为具体。</p>
      <p><b>③ 语言精炼，气势磅礴</b>：全文仅二百余字，却将~L~大丈夫~R~的内涵阐述得淋漓尽致，体现了孟子散文~L~气盛言宜~R~的特点。</p>
    </div>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line"><b>富贵不能淫，贫贱不能移，威武不能屈。</b></div>
        <p>全文核心名句，也是中华民族精神的写照。三个~L~不能~R~排比，从富贵、贫贱、威武三个维度写大丈夫的气节。~L~淫~R~~L~移~R~~L~屈~R~均为使动用法，三字力重千钧。此句激励了无数仁人志士坚守气节，成为千古座右铭。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">居天下之广居，立天下之<b>正位</b>，行天下之大道。</div>
        <p>以~L~广居~R~~L~正位~R~~L~大道~R~喻仁、礼、义，是儒家道德理想的形象化表达。三句排比，气势恢宏，写出了大丈夫立身处世的根本准则。</p>
      </div>
    </div>
  </section>
''')

ACC = fixq(u'''
  <section id="acc" class="sec">
    <div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 一词多义 · 活用 · 句式 · 文化常识</span></div>
    <div class="box"><div class="acc-cat">
        <h3>通假字</h3>
        <div class="acc-item"><span class="acc-w">往之女家</span><span class="acc-d">女通~L~汝~R~，你</span></div>
        <div class="acc-item"><span class="acc-w">无违夫子</span><span class="acc-d">无通~L~毋~R~，不要</span></div>
        <div class="acc-item"><span class="acc-w">安居而天下熄</span><span class="acc-d">熄通~L~息~R~，停息（一说~L~熄~R~为本字，指战火熄灭）</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>古今异义</h3>
        <div class="acc-item"><span class="acc-w">公孙衍、张仪岂不诚大丈夫哉</span><span class="acc-d">诚：古义真正、确实；今义诚实、真诚</span></div>
        <div class="acc-item"><span class="acc-w">丈夫之冠也</span><span class="acc-d">丈夫：古义成年男子；今义女子的配偶</span></div>
        <div class="acc-item"><span class="acc-w">以顺为正者</span><span class="acc-d">正：古义准则、正道；今义正确、端正</span></div>
        <div class="acc-item"><span class="acc-w">富贵不能淫</span><span class="acc-d">淫：古义使……迷惑（使动）；今义淫乱、过度</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>一词多义</h3>
        <div class="acc-item"><span class="acc-w">之</span><span class="acc-d">丈夫之冠也（取消句子独立性）／父命之（代词，他）／妾妇之道也（结构助词，的）／此之谓大丈夫（宾语前置标志）</span></div>
        <div class="acc-item"><span class="acc-w">命</span><span class="acc-d">父命之（教导、训诲）／奉命于危难之间（命令、使命）</span></div>
        <div class="acc-item"><span class="acc-w">道</span><span class="acc-d">妾妇之道也（行为准则）／行天下之大道（道路，喻指义）／独行其道（道路、原则）</span></div>
        <div class="acc-item"><span class="acc-w">居</span><span class="acc-d">居天下之广居（前一个：居住，动词；后一个：住宅，名词，喻指仁）／居十日（过了）</span></div>
        <div class="acc-item"><span class="acc-w">得</span><span class="acc-d">是焉得为大丈夫乎（能够）／得志（实现）／得道者多助（得到、施行）</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>词类活用</h3>
        <div class="acc-item"><span class="acc-w">丈夫之冠也</span><span class="acc-d">冠：名词作动词，行冠礼（guàn）</span></div>
        <div class="acc-item"><span class="acc-w">富贵不能淫</span><span class="acc-d">淫：使动用法，使……迷惑</span></div>
        <div class="acc-item"><span class="acc-w">贫贱不能移</span><span class="acc-d">移：使动用法，使……动摇、改变</span></div>
        <div class="acc-item"><span class="acc-w">威武不能屈</span><span class="acc-d">屈：使动用法，使……屈服</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文言句式</h3>
        <div class="acc-item"><span class="acc-w">判断句</span><span class="acc-d">以顺为正者，妾妇之道也（~L~……者，……也~R~表判断）</span></div>
        <div class="acc-item"><span class="acc-w">宾语前置</span><span class="acc-d">此之谓大丈夫（~L~之~R~是宾语前置的标志，正常语序为~L~谓此大丈夫~R~）</span></div>
        <div class="acc-item"><span class="acc-w">反问句</span><span class="acc-d">岂不诚大丈夫哉？／是焉得为大丈夫乎？（~L~岂……哉~R~~L~焉得……乎~R~表反问）</span></div>
        <div class="acc-item"><span class="acc-w">省略句</span><span class="acc-d">（大丈夫）居天下之广居……（承前省略主语）</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文化常识</h3>
        <div class="acc-item"><span class="acc-w">冠礼</span><span class="acc-d">古代男子二十岁举行的成人礼，束发加冠，表示成年，可以娶妻生子、参与社会活动。行冠礼时由父亲主持并训导。</span></div>
        <div class="acc-item"><span class="acc-w">纵横家</span><span class="acc-d">战国时期从事政治外交活动的谋士流派，以审察时势、游说君主为能事。~L~合纵~R~派联合六国抗秦（代表公孙衍、苏秦），~L~连横~R~派事秦攻他国（代表张仪）。</span></div>
        <div class="acc-item"><span class="acc-w">公孙衍</span><span class="acc-d">战国时期魏国人，纵横家，号~L~犀首~R~。曾佩五国相印，主张合纵抗秦，与张仪同时代，是连横的主要对手。</span></div>
        <div class="acc-item"><span class="acc-w">张仪</span><span class="acc-d">战国时期魏国人，纵横家，秦国相。主张~L~连横~R~，游说各国事秦，以口舌之才瓦解合纵，对秦统一六国起到重要作用。</span></div>
        <div class="acc-item"><span class="acc-w">大丈夫精神</span><span class="acc-d">孟子提出的理想人格：居仁由礼行义，得志兼济天下，不得志独善其身，富贵不淫、贫贱不移、威武不屈。这一精神塑造了中华民族的气节传统，影响深远。</span></div>
      </div></div>
  </section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《富贵不能淫》</title>
<meta name="description" content="《孟子》之《富贵不能淫》教学课件：逐句注释译文赏析、文言积累、全屏听写练习。">
<style>
%(css)s
</style>
</head>
<body>

  <!-- 卷首 -->
  <header class="hero">
    <div class="hero-inner">
      <div class="hero-side">战国·孟子</div>
      <h1 class="hero-title">富贵不能淫</h1>
    </div>
  </header>

  <!-- 导航 -->
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

  <!-- 逐句解读 -->
  <section id="jielu" class="sec">
    <div class="sec-head"><h2>解 读</h2><span class="no">逐句注释 · 译文 · 赏析</span></div>
    <div class="sec-sub">原文中带下划线的词可点击查看注释。可切换<b>背诵模式</b>（仅显示每句首字，点击任意句可显示/隐藏该句）。</div>
    <div class="texttools">
      <button id="btnShowAll" class="tbtn" style="display:none">显示全部</button>
    </div>
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

  <!-- 练习 -->
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
  <div class="kai">《富贵不能淫》</div>
  <div>孟子 · 战国 · 出自《孟子·滕文公下》</div>
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

with io.open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print('Generated:', OUT)
print('Size:', os.path.getsize(OUT), 'bytes')
