# -*- coding: utf-8 -*-
"""《得道多助，失道寡助》课件生成器 —— 复用《鸿门宴》课件的 CSS / JS 框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = r'D:\App\Apps\yanshi\hongmenyan-shiji.html'
OUT = r'D:\App\Apps\yanshi\deduoduozhushidaoguazhu-mengzi.html'

src = io.open(SRC, encoding='utf-8').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
# 注入 .acc-sub 样式（古诗词积累区需要，文言文也保留以通过校验）
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('hongmen_fs', 'dedu_fs')
# 移除模板自带的 DICT_WORDS / DICT_NOTES 定义（从 var DICT_WORDS 到听写模式注释前）
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

def strip_anno(text):
    """去掉 [[word|note]] 标记，只保留原文"""
    return re.sub(r'\[\[([^|\]]+)\|[^\]]+\]\]', r'\1', text)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "天时不如地利，地利不如人和。",
    "三里之城，七里之郭，环而攻之而不胜。",
    "夫环而攻之，必有得天时者矣；然而不胜者，是天时不如地利也。",
    "城非不高也，池非不深也，兵革非不坚利也，米粟非不多也；委而去之，是地利不如人和也。",
    "故曰：域民不以封疆之界，固国不以山溪之险，威天下不以兵革之利。",
    "得道者多助，失道者寡助。",
    "寡助之至，亲戚畔之；多助之至，天下顺之。",
    "以天下之所顺，攻亲戚之所畔，故君子有不战，战必胜矣。",
]

# ---------------- 逐句数据 ----------------
# 每句：(原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
("[[天时|指有利于作战的天气、时令等自然条件]][[不如|比不上、不及]][[地利|指有利于作战的地理形势，如城池坚固、山川险要等]]，[[地利|指有利于作战的地理形势]][[不如|比不上]][[人和|指人心所向、内部团结，是作战取胜的根本条件]]。",
 "有利于作战的天气、时令，比不上有利于作战的地理形势；有利于作战的地理形势，比不上作战中的人心所向、内部团结。",
 fixq("开门见山提出中心论点。以两个~L~不如~R~层层递进，由~L~天时~R~到~L~地利~R~再到~L~人和~R~，突出~L~人和~R~是克敌制胜的首要条件。排比句式，气势充沛，观点鲜明。"),
 ["论点", "排比"]),

("[[三里之城|方圆三里的内城。城，内城]]，[[七里之郭|方圆七里的外城。郭，外城，在城的外围加筑的一道城墙]]，[[环|围、包围]][[而|连词，表修饰，可不译]][[攻|攻打]][[之|代词，指城]][[而|连词，表转折，却、但是]][[不胜|不能取胜。胜，取胜、战胜]]。",
 "一座方圆三里的内城，方圆七里的外城，四面包围起来攻打它，却不能取胜。",
 fixq("以小城为例，设喻论证~L~天时不如地利~R~。城小而易攻，围攻者必占~L~天时~R~，然而~L~不胜~R~，说明~L~天时~R~并非决定因素。~L~环而攻之~R~写攻势之盛，~L~而不胜~R~一转，对比鲜明。"),
 ["设喻", "对比"]),

("[[夫|句首发语词，用在句首，表示将发议论，不译]][[环|围]][[而|表修饰]][[攻|攻打]][[之|代词，指城]]，[[必有|一定有。必，一定]][[得|得到]][[天时|有利于作战的天气时令]][[者矣|语气词连用，~L~者~R~表停顿，~L~矣~R~表肯定，相当于~L~了~R~]]；[[然而|这样却、可是。然，这样；而，却]][[不胜|不能取胜]][[者|……的原因]][[是|这、这是，代词]][[天时不如地利也|判断句，~L~是天时不如地利~R~的省略。也，句末语气词，表判断]]。",
 "采用四面包围的方式攻城，一定是得到有利于作战的天气、时令了；可是不能取胜，这是因为有利于作战的天气、时令比不上有利于作战的地理形势呀。",
 fixq("对前句作分析推理。~L~必有得天时者矣~R~退一步承认围攻者占天时，~L~然而~R~一转得出结论，论证严密。~L~是……也~R~判断句收束，明确~L~天时不如地利~R~的分论点。"),
 ["推理", "判断句"]),

("[[城|城墙]][[非不|不是不，双重否定表肯定，意为~L~并非不~R~]][[高|高大]][[也|句末语气词，表肯定]]，[[池|护城河（古今异义，今义：池塘、水池）]][[非不|不是不]][[深|水深，指护城河深广难越]]，[[兵革|泛指武器装备。兵，兵器；革，皮革制成的甲、胄、盾之类]][[非不|不是不]][[坚利|坚固锐利。坚，指甲胄坚固；利，指兵器锋利]]，[[米粟|泛指粮食。米，稻米；粟，谷子，去皮后称小米]][[非不|不是不]][[多|充足]]；[[委|放弃、舍弃]][[而|表顺承，就]][[去|离开、逃离（古今异义，今义：从所在地到别的地方，与~L~来~R~相对）]][[之|代词，指城]]，[[是|这是]][[地利不如人和也|判断句。也，表判断]]。",
 "城墙并不是不高啊，护城河并不是不深啊，武器装备并不是不精良啊，粮食供给并不是不充足啊；但是，守城一方还是弃城而逃，这是因为作战的地理形势再好，也比不上人心所向、内部团结啊。",
 fixq("以四个~L~非不~R~双重否定排比，极言地利之优——城高、池深、兵利、粮足，条件可谓完备。~L~委而去之~R~一转，守者弃城逃跑，在强烈对比中得出~L~地利不如人和~R~的结论。排比铺陈，蓄势充分，转折有力。"),
 ["排比", "双重否定", "对比"]),

("[[故|所以、因此]][[曰|说]]：[[域民|使人民定居下来。域，界限，这里用作动词，限制、使定居]][[不以|不能凭靠。以，凭、靠、用]][[封疆之界|疆域的边界。封疆，疆界、边界]]，[[固国|巩固国防。固，形容词作动词，巩固]][[不以|不能凭靠]][[山溪之险|山河的险要。山溪，山地与河流，泛指山川]]，[[威天下|震慑天下。威，形容词作动词，震慑、威慑]][[不以|不能凭靠]][[兵革之利|武器装备的锐利精良]]。",
 "所以说：使人民定居下来（而不迁到别的地方去），不能靠疆域的边界；巩固国防不能靠山河的险要；震慑天下不能靠武器的锐利。",
 fixq("由战争推演到治国，三个~L~不以~R~排比，从~L~域民~R~~L~固国~R~~L~威天下~R~三个层面否定~L~封疆之界~R~~L~山溪之险~R~~L~兵革之利~R~，为下文~L~得道~R~张本。句式整齐，层层推进，气势磅礴。"),
 ["排比", "词类活用", "过渡"]),

("[[得道|指能够施行治国的正道，即行仁政。道，正道，这里指仁政]][[者|……的人（君主）]][[多助|帮助支持他的人多]]，[[失道|不施行仁政，违背正道]][[者|……的人（君主）]][[寡助|帮助支持他的人少。寡，少]]。",
 "能施行~L~仁政~R~的君主，帮助支持他的人就多；不施行~L~仁政~R~的君主，帮助支持他的人就少。",
 fixq("全文核心名句，点明~L~道~R~即~L~仁政~R~。~L~得道~R~与~L~失道~R~对举，~L~多助~R~与~L~寡助~R~对比，寥寥十字，掷地有声，揭示了人心向背的根本规律。"),
 ["名句", "对比", "主旨"]),

("[[寡助|帮助支持他的人少]][[之至|到了极点。之，到；至，极点、极致]]，[[亲戚|内外亲属，包括父系亲属和母系亲属（古今异义，今义：跟自己家庭有婚姻关系或血统关系的家庭或它的成员，多指旁系亲属）]][[畔|通~L~叛~R~，背叛、叛乱]][[之|代词，指失道者]]；[[多助|帮助支持他的人多]][[之至|到了极点]]，[[天下|天下的人、普天下之人]][[顺|归顺、服从]][[之|代词，指得道者]]。",
 "帮助他的人少到了极点，连内外亲属也会背叛他；帮助他的人多到了极点，天下的人都会归顺他。",
 fixq("以~L~至~R~字推到极致，将~L~寡助~R~与~L~多助~R~的后果推向极端。~L~亲戚畔之~R~与~L~天下顺之~R~形成强烈对比，极言失道之孤、得道之众，论证~L~人和~R~的极端重要性。"),
 ["对比", "通假字", "递进"]),

("[[以|凭、凭借、用]][[天下之所顺|天下人都归顺他的（条件）。所，助词，与动词构成名词性短语。顺，归顺]]，[[攻|攻打]][[亲戚之所畔|连亲属都背叛他的（人）。畔，通~L~叛~R~]]，[[故|所以、因此]][[君子|这里指能行仁政的君主，即上文所说的~L~得道者~R~]][[有不战|不战则已。有，要么、或者（一说~L~有~R~同~L~或~R~）]]，[[战|作战]][[必|一定、必定]][[胜|胜利]][[矣|句末语气词，表肯定，了]]。",
 "凭着天下人都归顺他的条件，去攻打那连亲属都反对背叛的君主，所以能行仁政的君主不战则已，战就一定能胜利。",
 fixq("收束全文。~L~以天下之所顺~R~对~L~亲戚之所畔~R~，力量对比悬殊，结论~L~战必胜~R~水到渠成。~L~君子有不战~R~语含委婉——仁者本不好战，然一旦战则必胜，既肯定武力效果，又回归仁政主旨。"),
 ["收束", "对比", "结论"]),
]

# ---------------- 字形题 ----------------
DICT_WORDS = [
    {"w":"郭","py":"guō","q":"三里之城，七里之□","tip":"「郭」右耳旁（阝），外城；与「廓」区分，音 guō"},
    {"w":"粟","py":"sù","q":"米□非不多也","tip":"「粟」西字头+米，谷子，音 sù；与「栗」（lì，栗子）区分，下部是「米」不是「木」"},
    {"w":"畔","py":"pàn","q":"亲戚□之","tip":"「畔」田字旁，通「叛」，音 pàn；与「判」「叛」区分"},
    {"w":"域","py":"yù","q":"□民不以封疆之界","tip":"「域」土字旁，界限、限制，音 yù；与「或」「城」区分"},
    {"w":"溪","py":"xī","q":"固国不以山□之险","tip":"「溪」三点水，山间小河，音 xī；与「蹊」（足字旁）区分"},
    {"w":"寡","py":"guǎ","q":"失道者□助","tip":"「寡」宀头，少，音 guǎ；上「宀」下「𡧛」，勿写成「宴」"},
    {"w":"委","py":"wěi","q":"□而去之","tip":"「委」禾字旁，放弃，音 wěi；与「萎」（艹字头）区分"},
    {"w":"革","py":"gé","q":"兵□非不坚利也","tip":"「革」独体字，皮革，音 gé；笔顺：横、竖、竖、横、竖、横折、横、横、竖"},
]

# ---------------- 注释题 ----------------
DICT_NOTES = [
    {"w":"天时","q":"天时不如地利，地利不如人和。","a":"有利于作战的天气、时令等自然条件"},
    {"w":"地利","q":"天时不如地利，地利不如人和。","a":"有利于作战的地理形势"},
    {"w":"人和","q":"天时不如地利，地利不如人和。","a":"人心所向、内部团结"},
    {"w":"郭","q":"三里之城，七里之郭，环而攻之而不胜。","a":"外城，在城的外围加筑的一道城墙"},
    {"w":"环","q":"三里之城，七里之郭，环而攻之而不胜。","a":"围、包围"},
    {"w":"夫","q":"夫环而攻之，必有得天时者矣","a":"句首发语词，表示将发议论，不译"},
    {"w":"然而","q":"然而不胜者，是天时不如地利也。","a":"这样却、可是"},
    {"w":"是","q":"然而不胜者，是天时不如地利也。","a":"这、这是，代词"},
    {"w":"池","q":"城非不高也，池非不深也","a":"护城河（古今异义，今义：池塘）"},
    {"w":"兵革","q":"兵革非不坚利也","a":"泛指武器装备。兵，兵器；革，皮革制的甲胄"},
    {"w":"委","q":"委而去之，是地利不如人和也。","a":"放弃、舍弃"},
    {"w":"去","q":"委而去之，是地利不如人和也。","a":"离开、逃离（古今异义）"},
    {"w":"域民","q":"域民不以封疆之界","a":"使人民定居下来。域，名词作动词，限制"},
    {"w":"固国","q":"固国不以山溪之险","a":"巩固国防。固，形容词作动词，巩固"},
    {"w":"威天下","q":"威天下不以兵革之利","a":"震慑天下。威，形容词作动词，震慑"},
    {"w":"得道","q":"得道者多助，失道者寡助。","a":"施行仁政。道，正道，这里指仁政"},
    {"w":"寡","q":"失道者寡助","a":"少"},
    {"w":"之至","q":"寡助之至，亲戚畔之","a":"到了极点。之，到；至，极点"},
    {"w":"亲戚","q":"寡助之至，亲戚畔之","a":"内外亲属（古今异义，今义多指旁系亲属）"},
    {"w":"畔","q":"寡助之至，亲戚畔之","a":"通「叛」，背叛"},
    {"w":"顺","q":"多助之至，天下顺之","a":"归顺、服从"},
    {"w":"君子","q":"故君子有不战，战必胜矣。","a":"这里指能行仁政的君主"},
]

# ---------------- 组装 ----------------
def build_verses():
    out = []
    for idx, (txt, yi, shang, tags) in enumerate(S):
        out.append('      <div class="verse" id="l%d" data-i="%d">' % (idx + 1, idx))
        out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx + 1, annotate(txt)))
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
    return '\n'.join(out)

verses_html = build_verses()
full_html = '\n'.join('      <p class="pl">%s</p>' % p for p in FULLTEXT)

BG = fixq(u'''
  <section id="bg" class="sec">
    <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
    <div class="lead">
      战国中期，诸侯争霸，战乱频仍。孟子周游列国，倡言仁政，主张~L~民为贵，社稷次之，君为轻~R~。《得道多助，失道寡助》以战争为喻，层层推演，得出~L~得道者多助，失道者寡助~R~的千古论断——民心向背，才是决定天下兴亡的根本。
    </div>
    <div class="box">
      <h3>作者简介</h3>
      <p><b>孟子</b>（约前372—前289），名轲，字子舆，战国时期邹国（今山东邹城）人。儒家学派代表人物，被后世尊为~L~亚圣~R~。他继承并发展了孔子的思想，主张~L~仁政~R~~L~王道~R~，提出~L~民贵君轻~R~的民本思想和~L~性善论~R~。</p>
      <p>《孟子》一书记录孟子及其弟子的言行，共七篇，由孟子及其弟子万章、公孙丑等编著。其文气势充沛，感情强烈，善于雄辩，长于比喻，对后世散文影响深远。南宋朱熹将《孟子》与《大学》《中庸》《论语》合编为~L~四书~R~。</p>
    </div>
    <div class="box">
      <h3>创作背景</h3>
      <p>本文选自《孟子·公孙丑下》。战国中期，各国兼并战争愈演愈烈，统治者穷兵黩武，百姓流离失所。孟子反对不义之战，主张以~L~仁政~R~统一天下。</p>
      <p>文章以战争中的攻守为例，论证~L~人和~R~重于~L~天时~R~~L~地利~R~，进而指出治国的根本在于~L~得道~R~——施行仁政、争取民心。这既是对当时好战君主的劝诫，也是孟子政治思想的集中体现。</p>
      <p class="note">※ ~L~得道多助，失道寡助~R~后来成为成语，泛指站在正义一方，会得到多数人的支持帮助；违背正义，必然陷于孤立。</p>
    </div>
    <div class="box media-box">
      <h3>朗诵 · 讲解</h3>
      <div class="media-grid">
        <div class="media">
          <h4>课文朗读《得道多助，失道寡助》</h4>
          <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1uG4y1p7mS&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读《得道多助，失道寡助》"></iframe>
          <a href="https://www.bilibili.com/video/BV1uG4y1p7mS" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
        </div>
        <div class="media">
          <h4>动画讲解《得道多助，失道寡助》</h4>
          <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1QW4y1a72K&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="动画讲解《得道多助，失道寡助》"></iframe>
          <a href="https://www.bilibili.com/video/BV1QW4y1a72K" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
        </div>
      </div>
    </div>
  </section>
''')

APP = fixq(u'''
  <section id="app" class="sec">
    <div class="sec-head"><h2>赏 析</h2><span class="no">论点 · 结构 · 艺术 · 名句</span></div>
    <div class="box">
      <h3>中心论点</h3>
      <p>本文开篇即提出中心论点：<b>天时不如地利，地利不如人和</b>。孟子通过战争中的攻守之例，层层推进，论证了~L~人和~R~——即人心所向、内部团结——是决定战争胜负乃至国家兴亡的根本因素。</p>
      <p>文章由战争而论治国，最终落脚于~L~得道多助，失道寡助~R~，阐明了施行仁政的重要性：得民心者得天下，失民心者失天下。</p>
    </div>
    <div class="box">
      <h3>论证结构</h3>
      <p>全文可分三层：</p>
      <p><b>第一层（第1句）</b>：提出中心论点，以两个~L~不如~R~递进，突出~L~人和~R~最重要。</p>
      <p><b>第二层（第2—4句）</b>：以攻城不胜和守城弃逃两个战例，分别论证~L~天时不如地利~R~和~L~地利不如人和~R~，用事实支撑论点。</p>
      <p><b>第三层（第5—8句）</b>：由战争推演到治国，以三个~L~不以~R~否定武力与地形的作用，推出~L~得道多助，失道寡助~R~的论断，并以~L~战必胜~R~收束，深化主旨。</p>
    </div>
    <div class="box">
      <h3>艺术特色</h3>
      <p><b>① 层层递进，逻辑严密</b>：从~L~天时~R~到~L~地利~R~到~L~人和~R~，从战争到治国，论证环环相扣，无懈可击。</p>
      <p><b>② 排比铺陈，气势充沛</b>：~L~城非不高也……米粟非不多也~R~四句排比，~L~域民不以……固国不以……威天下不以……~R~三句排比，句式整齐，气势磅礴，极具说服力。</p>
      <p><b>③ 对比鲜明，正反论证</b>：~L~得道~R~与~L~失道~R~、~L~多助~R~与~L~寡助~R~、~L~天下顺之~R~与~L~亲戚畔之~R~，处处对比，观点鲜明。</p>
      <p><b>④ 语言精炼，善用短句</b>：全文仅百余字，却将治国安邦的大道理讲得透彻明白，体现了孟子散文~L~气盛言宜~R~的特点。</p>
    </div>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">天时不如地利，<b>地利不如人和</b>。</div>
        <p>全文中心论点。以~L~天时~R~~L~地利~R~~L~人和~R~三者比较，层层递进，突出人心向背的决定意义。后世常引此句说明团结的重要性。</p>
      </div>
      <div class="fame-card">
        <div class="f-line"><b>得道者多助，失道者寡助。</b></div>
        <p>千古名句。将~L~道~R~（仁政）与人心向背直接挂钩，阐明了~L~得民心者得天下~R~的政治规律，成为后世治国理政的重要借鉴。</p>
      </div>
    </div>
  </section>
''')

ACC = fixq(u'''
  <section id="acc" class="sec">
    <div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 一词多义 · 活用 · 句式 · 文化常识</span></div>
    <div class="box"><div class="acc-cat">
        <h3>通假字</h3>
        <div class="acc-item"><span class="acc-w">亲戚畔之</span><span class="acc-d">畔通~L~叛~R~，背叛、叛乱</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>古今异义</h3>
        <div class="acc-item"><span class="acc-w">池非不深也</span><span class="acc-d">池：古义护城河；今义池塘、水池</span></div>
        <div class="acc-item"><span class="acc-w">委而去之</span><span class="acc-d">去：古义离开、逃离；今义从所在地到别的地方</span></div>
        <div class="acc-item"><span class="acc-w">亲戚畔之</span><span class="acc-d">亲戚：古义内外亲属（含父母兄弟）；今义跟自己家庭有婚姻关系的家庭或成员，多指旁系</span></div>
        <div class="acc-item"><span class="acc-w">七里之郭</span><span class="acc-d">郭：古义外城；今义多用于姓氏</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>一词多义</h3>
        <div class="acc-item"><span class="acc-w">而</span><span class="acc-d">环而攻之（表修饰，可不译）／而不胜（表转折，却）／委而去之（表顺承，就）</span></div>
        <div class="acc-item"><span class="acc-w">之</span><span class="acc-d">环而攻之（代词，指城）／三里之城（结构助词，的）／寡助之至（动词，到）／天下之所顺（助词，取消句子独立性）</span></div>
        <div class="acc-item"><span class="acc-w">以</span><span class="acc-d">域民不以封疆之界（凭、靠）／以天下之所顺（凭、凭借）</span></div>
        <div class="acc-item"><span class="acc-w">利</span><span class="acc-d">兵革非不坚利也（锐利、精良）／地利不如人和（有利条件）</span></div>
        <div class="acc-item"><span class="acc-w">道</span><span class="acc-d">得道者多助（正道，指仁政）／伐无道（道义）</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>词类活用</h3>
        <div class="acc-item"><span class="acc-w">域民不以封疆之界</span><span class="acc-d">域：名词作动词，限制、使定居</span></div>
        <div class="acc-item"><span class="acc-w">固国不以山溪之险</span><span class="acc-d">固：形容词作动词，巩固</span></div>
        <div class="acc-item"><span class="acc-w">威天下不以兵革之利</span><span class="acc-d">威：形容词作动词，震慑、威慑</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文言句式</h3>
        <div class="acc-item"><span class="acc-w">判断句</span><span class="acc-d">是天时不如地利也／是地利不如人和也（~L~是……也~R~表判断）</span></div>
        <div class="acc-item"><span class="acc-w">双重否定</span><span class="acc-d">城非不高也，池非不深也，兵革非不坚利也，米粟非不多也（~L~非不~R~双重否定表肯定）</span></div>
        <div class="acc-item"><span class="acc-w">被动句（意念被动）</span><span class="acc-d">委而去之（城被放弃、被离开，意念上的被动）</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文化常识</h3>
        <div class="acc-item"><span class="acc-w">《孟子》</span><span class="acc-d">儒家经典之一，记录孟子及其弟子言行，由孟子及其弟子万章等编著，共七篇。行文气势充沛，善于雄辩，长于比喻。南宋朱熹将其与《大学》《中庸》《论语》合为~L~四书~R~。</span></div>
        <div class="acc-item"><span class="acc-w">孟子</span><span class="acc-d">名轲，字子舆，战国时期邹国人，儒家学派代表人物，被尊为~L~亚圣~R~。主张~L~仁政~R~~L~民贵君轻~R~~L~性善论~R~，继承发展了孔子的思想。</span></div>
        <div class="acc-item"><span class="acc-w">城与郭</span><span class="acc-d">古代都城一般有两重城墙，内为~L~城~R~，外为~L~郭~R~。~L~三里之城，七里之郭~R~形容城池之小。</span></div>
        <div class="acc-item"><span class="acc-w">仁政</span><span class="acc-d">孟子政治思想的核心，主张统治者以德服人、以民为本，反对苛政与战争。~L~得道~R~即行仁政，~L~失道~R~即不行仁政。</span></div>
      </div></div>
  </section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《得道多助，失道寡助》</title>
<meta name="description" content="《孟子》之《得道多助，失道寡助》教学课件：逐句注释译文赏析、文言积累、全屏听写练习。">
<style>
%(css)s
</style>
</head>
<body>

  <!-- 卷首 -->
  <header class="hero">
    <div class="hero-inner">
      <div class="hero-side">战国·孟子</div>
      <h1 class="hero-title">得道多助，失道寡助</h1>
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
  <div class="kai">《得道多助，失道寡助》</div>
  <div>孟子 · 战国 · 出自《孟子·公孙丑下》</div>
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
