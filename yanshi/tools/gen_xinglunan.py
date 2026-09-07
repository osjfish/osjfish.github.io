# -*- coding: utf-8 -*-
"""《行路难（其一）》课件生成器 —— 复用《琵琶行》课件的 CSS / JS 框架（诗词类）。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = r'D:\App\Apps\yanshi\pipaxing-baijuyi.html'
OUT = r'D:\App\Apps\yanshi\xinglunan-libai.html'

src = io.open(SRC, encoding='utf-8').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('pipa_fs', 'xinglu_fs')
# 移除模板自带的 DICT_WORDS / DICT_NOTES（在 IIFE 末尾，听写题库注释到 IIFE 闭合前）
_dw_start = JS.index('/* ---------- 听写题库')
_iife_end = JS.rindex('})();')
JS = JS[:_dw_start] + JS[_iife_end:]


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)

def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    '金樽清酒斗十千，玉盘珍羞直万钱。',
    '停杯投箸不能食，拔剑四顾心茫然。',
    '欲渡黄河冰塞川，将登太行雪满山。',
    '闲来垂钓碧溪上，忽复乘舟梦日边。',
    '行路难，行路难，多歧路，今安在？',
    '长风破浪会有时，直挂云帆济沧海。',
]

# ---------------- 逐句数据 ----------------
S = [
("[[金樽|金色的酒杯。樽（zūn），古代盛酒的器具]][[清酒|清醇的美酒]][[斗十千|一斗值十千钱，极言酒美价贵。斗，古代酒器；十千，万钱，虚指高价]][[，|逗号]]，[[玉盘|玉制的盘子，极言餐具精美]][[珍羞|珍贵的菜肴。羞，通~L~馐~R~，美味的食品]][[直万钱|值万钱，极言菜贵。直，通~L~值~R~，价值]]。",
 "金杯里的清醇美酒一斗值十千钱，玉盘中的珍贵菜肴值万钱。",
 fixq("开篇写宴席的奢华：~L~金樽~R~~L~清酒~R~~L~玉盘~R~~L~珍羞~R~，一斗十千、一盘万钱，极尽铺陈。然而这不是太平宴饮，而是朋友为诗人设的饯别盛宴。以乐景写哀情，盛宴越奢华，越反衬出诗人内心的苦闷——美酒佳肴在前，却无心享用。~L~羞~R~通~L~馐~R~，~L~直~R~通~L~值~R~，两个通假字需注意。"),
 ["乐景写哀", "通假字", "铺陈"]),

("[[停杯|放下酒杯。停，放下]][[投箸|扔下筷子。投，扔、放下；箸（zhù），筷子]][[不能食|吃不下东西]][[，|逗号]][[拔剑|拔出宝剑]][[四顾|向四周看。顾，看、望]][[心茫然|心中迷惘无措。茫然，迷惘、不知所措的样子]]。",
 "（我）放下酒杯、扔下筷子，吃不下东西；拔出宝剑，环顾四周，心中一片迷惘。",
 fixq("紧承上联，急转直下。~L~停杯投箸~R~与~L~金樽清酒~R~形成强烈反差——美酒佳肴在前，诗人却食不下咽。~L~拔剑四顾~R~写英雄无用武之地的愤懑，~L~心茫然~R~点出内心的迷惘与苦闷。四个连续动作（停、投、拔、顾），生动刻画出诗人内心的激荡与无奈。这是李白被~L~赐金放还~R~离开长安时的真实写照。"),
 ["动作描写", "反衬", "情感转折"]),

("[[欲渡|想要渡过。欲，想要、打算]][[黄河|中国第二长河，这里喻指人生道路上的险阻]][[冰塞川|冰雪堵塞了河道。塞（sè），堵塞、阻塞；川，河流]][[，|逗号]][[将登|将要登上。将，将要、打算]][[太行|太行山，在今山西、河南、河北交界处，这里喻指人生道路上的高山]][[雪满山|大雪覆盖了山岭。满山，遍山]]。",
 "想渡过黄河，冰雪却堵塞了河道；想登上太行山，大雪却覆盖了山岭。",
 fixq("以自然界的险阻比喻人生道路的艰难。~L~冰塞川~R~~L~雪满山~R~，既是实景，又是象征——仕途之路被冰雪封锁，理想难以实现。~L~欲渡~R~~L~将登~R~写出诗人的进取之心，而~L~冰塞~R~~L~雪满~R~则写出现实的冷酷阻挡。两句对仗工整，以景寓情，把抽象的~L~行路难~R~具象化为可感的自然险阻，是千古传诵的名句。"),
 ["比喻象征", "对仗", "名句"]),

("[[闲来|空闲时。闲，空闲、闲来无事]][[垂钓|钓鱼。垂，垂挂；钓，钓鱼]][[碧溪上|碧绿的溪水边。碧，青绿色；溪，小河。这里用姜太公渭水垂钓遇周文王的典故]][[，|逗号]][[忽复|忽然又。忽，忽然；复，又、再]][[乘舟|乘船。乘，坐、驾]][[梦日边|梦见自己乘船经过太阳旁边。这里用伊尹梦见乘舟过日边、后被商汤重用的典故]]。",
 "闲暇时坐在碧绿的溪边钓鱼，忽然又梦见自己乘船经过太阳旁边。",
 fixq("笔锋一转，由现实的苦闷转入对历史人物的追慕。~L~垂钓碧溪~R~用姜太公吕尚渭水垂钓遇周文王的典故，~L~乘舟梦日~R~用伊尹梦见乘舟过日边、后被商汤重用的典故。两位先贤都曾在困顿中遇明主、建功业，诗人借此表达自己虽遭挫折但仍对前途抱有希望。用典含蓄，意境开阔，与上联的~L~冰塞川~R~~L~雪满山~R~形成对比。"),
 ["用典", "对比", "希望"]),

("[[行路难|行路艰难啊，这里比喻人生道路、仕途艰难]][[，|逗号]][[行路难|重复感叹，强化情感]][[，|逗号]][[多歧路|岔路这么多。歧路，岔路，比喻人生道路上的多种选择与困惑]][[，|逗号]][[今安在|如今（我）在哪里呢？安，哪里、何处；在，存在。宾语前置，正常语序为~L~今在安~R~]]？",
 "行路艰难啊，行路艰难啊！岔路这么多，如今我身在何处？",
 fixq("短句急促，反复咏叹，是全诗情感的高潮。~L~行路难，行路难~R~连续重复，如一声声长叹，把内心的苦闷与彷徨推向顶点。~L~多歧路，今安在~R~以问句收束，写出面对人生岔路的迷惘——不知何去何从。四字短句节奏紧凑，与前面的七言长句形成对比，情感跌宕起伏。这是诗人发自内心的呐喊，也是对~L~行路难~R~主题的直接点题。"),
 ["反复咏叹", "短句节奏", "点题"]),

("[[长风破浪|比喻实现政治理想。出自南朝宗悫~L~愿乘长风破万里浪~R~之语。长风，强劲的风；破浪，冲破浪涛]][[会有时|终会有那一天。会，终将、一定；有时，有那一天、有机会]][[，|逗号]][[直挂|高高挂起。直，径直、直接；挂，悬挂]][[云帆|像白云一样的船帆，指高大的船帆]][[济沧海|渡过大海。济，渡、渡过；沧海，大海]]。",
 "终有一天能乘长风破万里浪，高高挂起云帆渡过沧海。",
 fixq("全诗的最强音，千古名句。~L~长风破浪~R~用宗悫~L~愿乘长风破万里浪~R~的典故，表达远大志向；~L~会有时~R~写出坚定的信念；~L~直挂云帆济沧海~R~以壮阔的画面收束全诗，气势磅礴。经过前面的苦闷、迷惘、追问，诗人最终以乐观自信的姿态展望未来——尽管前路艰险，但理想终会实现。这一句是李白精神的写照，激励了后世无数在困境中奋斗的人。"),
 ["名句", "用典", "乐观自信", "主旨"]),
]

# ---------------- 字形题 ----------------
DICT_WORDS = [
    {"w":"樽","py":"zūn","q":"金□清酒斗十千","tip":"「樽」木字旁，古代盛酒器，音 zūn；与「尊」「遵」区分"},
    {"w":"羞","py":"xiū","q":"玉盘珍□直万钱","tip":"「羞」通「馐」，美味食物，音 xiū；与「馐」（食字旁）区分，本文用本字「羞」"},
    {"w":"箸","py":"zhù","q":"停杯投□不能食","tip":"「箸」竹字头，筷子，音 zhù；与「著」「署」区分，下部是「者」"},
    {"w":"茫","py":"máng","q":"拔剑四顾心□然","tip":"「茫」草字头，音 máng，迷惘；与「忙」「芒」区分"},
    {"w":"渡","py":"dù","q":"欲□黄河冰塞川","tip":"「渡」三点水，渡过，音 dù；与「度」（计量、程度）区分，过河用「渡」"},
    {"w":"歧","py":"qí","q":"多□路，今安在","tip":"「歧」止字旁，岔路，音 qí；与「岐」（山字旁，地名）「技」区分"},
    {"w":"沧","py":"cāng","q":"直挂云帆济□海","tip":"「沧」三点水，音 cāng，大海；与「苍」（草字头，青色）「仓」区分"},
    {"w":"帆","py":"fān","q":"直挂云□济沧海","tip":"「帆」巾字旁，船帆，音 fān；与「凡」「矾」区分"},
]

# ---------------- 注释题 ----------------
DICT_NOTES = [
    {"w":"樽","q":"金樽清酒斗十千","a":"古代盛酒的器具，音 zūn"},
    {"w":"斗十千","q":"金樽清酒斗十千","a":"一斗值十千钱，极言酒美价贵。斗，古代酒器"},
    {"w":"羞","q":"玉盘珍羞直万钱","a":"通「馐」，美味的食品"},
    {"w":"直","q":"玉盘珍羞直万钱","a":"通「值」，价值"},
    {"w":"箸","q":"停杯投箸不能食","a":"筷子，音 zhù"},
    {"w":"顾","q":"拔剑四顾心茫然","a":"看、望"},
    {"w":"茫然","q":"拔剑四顾心茫然","a":"迷惘、不知所措的样子"},
    {"w":"塞","q":"欲渡黄河冰塞川","a":"堵塞、阻塞，音 sè"},
    {"w":"川","q":"欲渡黄河冰塞川","a":"河流"},
    {"w":"垂钓碧溪","q":"闲来垂钓碧溪上","a":"用姜太公渭水垂钓遇周文王的典故，指等待明主重用"},
    {"w":"乘舟梦日","q":"忽复乘舟梦日边","a":"用伊尹梦见乘舟过日边、后被商汤重用的典故"},
    {"w":"歧路","q":"多歧路，今安在","a":"岔路，比喻人生道路上的多种选择与困惑"},
    {"w":"安在","q":"今安在","a":"在哪里。安，哪里；宾语前置，正常语序为「在安」"},
    {"w":"长风破浪","q":"长风破浪会有时","a":"比喻实现政治理想。出自宗悫「愿乘长风破万里浪」"},
    {"w":"会","q":"长风破浪会有时","a":"终将、一定"},
    {"w":"济","q":"直挂云帆济沧海","a":"渡、渡过"},
    {"w":"沧海","q":"直挂云帆济沧海","a":"大海"},
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
full_html = '\n'.join('      <p class="pl">%s</p>' % p for p in FULLTEXT)

BG = fixq(u'''
  <section id="bg" class="sec">
    <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
    <div class="lead">
      唐天宝三年（744），李白被唐玄宗~L~赐金放还~R~，离开长安。朋友在洛阳为他设宴饯行。面对美酒佳肴，诗人却食不下咽——一腔报国之志无处施展，理想与现实的冲突在胸中激荡。《行路难》正是此时所作，共三首，本课选的是第一首。
    </div>
    <div class="box">
      <h3>作者简介</h3>
      <p><b>李白</b>（701—762），字太白，号青莲居士，唐代伟大的浪漫主义诗人，被后世尊为~L~诗仙~R~。其诗风豪放飘逸、想象奇特、语言清新，与杜甫并称~L~李杜~R~。代表作品有《望庐山瀑布》《将进酒》《蜀道难》《早发白帝城》等。</p>
      <p>李白一生以~L~济苍生~R~~L~安社稷~R~为己任，但仕途坎坷。天宝元年（742）被召入长安，供奉翰林，却因权贵排挤，不到两年便被~L~赐金放还~R~。《行路难》正写于此时。</p>
    </div>
    <div class="box">
      <h3>创作背景</h3>
      <p>《行路难》是乐府旧题，属于《杂曲歌辞》，内容多写世路艰难和离别悲伤。李白以此为题写了三首，本课选第一首。</p>
      <p>天宝三年（744），李白离开长安后，在洛阳与朋友相聚。朋友为他设盛宴饯行。面对~L~金樽清酒~R~~L~玉盘珍羞~R~，诗人却~L~停杯投箸不能食~R~。他想到自己满怀报国之志，却被权贵排挤出京，仕途之路如~L~冰塞川~R~~L~雪满山~R~般艰难。但诗人并未消沉，最终以~L~长风破浪会有时，直挂云帆济沧海~R~的豪迈信念收束全诗。</p>
      <p class="note">※ 赐金放还：唐玄宗给李白一些钱财，让他离开宫廷。名义上是礼遇，实际上是变相驱逐。</p>
    </div>
    <div class="box media-box">
      <h3>朗诵 · 讲解</h3>
      <div class="media-grid">
        <div class="media">
          <h4>课文朗读《行路难》</h4>
          <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1Nb4y1j7pB&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读《行路难》"></iframe>
          <a href="https://www.bilibili.com/video/BV1Nb4y1j7pB" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
        </div>
        <div class="media">
          <h4>名师讲解《行路难》</h4>
          <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1QP411m7nT&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="名师讲解《行路难》"></iframe>
          <a href="https://www.bilibili.com/video/BV1QP411m7nT" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
        </div>
      </div>
    </div>
  </section>
''')

APP = fixq(u'''
  <section id="app" class="sec">
    <div class="sec-head"><h2>赏 析</h2><span class="no">情感 · 手法 · 艺术 · 名句</span></div>
    <div class="box">
      <h3>情感脉络</h3>
      <p>全诗情感跌宕起伏，一波三折：</p>
      <p><b>① 苦闷抑郁</b>（前四句）：盛宴在前却食不下咽，拔剑四顾心茫然，写出被排挤后的苦闷。</p>
      <p><b>② 迷惘困惑</b>（五、六句）：冰塞黄河、雪满太行，以自然险阻比喻仕途艰难。</p>
      <p><b>③ 希望期盼</b>（七、八句）：用姜尚、伊尹的典故，表达对前途的希望。</p>
      <p><b>④ 彷徨呐喊</b>（九至十二句）：~L~行路难，行路难~R~反复咏叹，~L~今安在~R~追问出路。</p>
      <p><b>⑤ 乐观自信</b>（末两句）：长风破浪、云帆济海，以豪迈信念收束。</p>
    </div>
    <div class="box">
      <h3>艺术特色</h3>
      <p><b>① 跌宕起伏的情感结构</b>：全诗在苦闷与希望、迷惘与自信之间反复跳跃，情感大起大落，正是李白浪漫主义诗风的体现。</p>
      <p><b>② 妙用典故</b>：姜尚垂钓、伊尹梦日、宗悫破浪，三个典故分别表达希望、信念与志向，含蓄而意蕴丰富。</p>
      <p><b>③ 象征手法</b>：~L~冰塞川~R~~L~雪满山~R~象征仕途险阻，~L~长风破浪~R~~L~云帆济海~R~象征理想实现，化抽象为具象。</p>
      <p><b>④ 长短句交错</b>：前八句七言，节奏舒缓；~L~行路难~R~四句转为三字短句，节奏急促；末两句又恢复七言，气势磅礴。句式变化与情感变化同步。</p>
    </div>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">长风破浪会有时，直挂云帆济沧海。</div>
        <p>全诗的最强音，千古名句。用宗悫~L~愿乘长风破万里浪~R~的典故，表达诗人对理想的坚定信念。~L~会有时~R~写出必然的信心，~L~直挂~R~~L~济~R~写出一往无前的气概。画面壮阔，气势磅礴，激励了后世无数在困境中奋斗的人。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">欲渡黄河冰塞川，将登太行雪满山。</div>
        <p>以自然界的险阻比喻人生道路的艰难，是千古传诵的名句。对仗工整，以景寓情，把抽象的~L~行路难~R~具象化为可感的冰雪险阻，既是写实，又是象征。</p>
      </div>
    </div>
  </section>
''')

ACC = fixq(u'''
  <section id="acc" class="sec">
    <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 考点 · 修辞 · 文化常识</span></div>
    <div class="box"><div class="acc-cat">
        <h3>文体与诗体</h3>
        <div class="acc-item"><span class="acc-w">乐府旧题</span><span class="acc-d">《行路难》是乐府《杂曲歌辞》旧题，内容多写世路艰难和离别悲伤。李白以此为题写了三首，本课选第一首。</span></div>
        <div class="acc-item"><span class="acc-w">七言歌行</span><span class="acc-d">全诗以七言为主，中间穿插三字短句，句式灵活，属于古体诗（歌行体），不受近体格律束缚。</span></div>
        <div class="acc-item"><span class="acc-w">用韵</span><span class="acc-d">前八句押 an 韵（钱、然、山、边），九至十二句转韵（难、在），末两句押 ai 韵（时、海为邻韵），换韵与情感变化同步。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>易错字音形</h3>
        <div class="acc-item"><span class="acc-w">樽 zūn</span><span class="acc-d">木字旁，古代盛酒器。勿写成「尊」「遵」。</span></div>
        <div class="acc-item"><span class="acc-w">羞 xiū</span><span class="acc-d">通「馐」，本文用本字「羞」。勿写成「馐」。</span></div>
        <div class="acc-item"><span class="acc-w">直 zhí</span><span class="acc-d">通「值」，价值。本文用本字「直」。</span></div>
        <div class="acc-item"><span class="acc-w">箸 zhù</span><span class="acc-d">竹字头，筷子。勿写成「著」「署」。</span></div>
        <div class="acc-item"><span class="acc-w">塞 sè</span><span class="acc-d">多音字。堵塞读 sè（本文），边塞读 sài，瓶塞读 sāi。</span></div>
        <div class="acc-item"><span class="acc-w">歧 qí</span><span class="acc-d">止字旁，岔路。勿写成「岐」（山字旁，多用于地名）。</span></div>
        <div class="acc-item"><span class="acc-w">沧 cāng</span><span class="acc-d">三点水，大海。勿写成「苍」（草字头，青色）。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文言梳理</h3>
        <div class="acc-sub">通假字</div>
        <div class="acc-item"><span class="acc-w">玉盘珍羞直万钱</span><span class="acc-d">羞通「馐」，美味的食物；直通「值」，价值</span></div>
        <div class="acc-sub">古今异义</div>
        <div class="acc-item"><span class="acc-w">长风破浪会有时</span><span class="acc-d">会：古义终将、一定；今义聚会、会议</span></div>
        <div class="acc-item"><span class="acc-w">直挂云帆济沧海</span><span class="acc-d">济：古义渡、渡过；今义救济、帮助</span></div>
        <div class="acc-sub">一词多义</div>
        <div class="acc-item"><span class="acc-w">安</span><span class="acc-d">今安在（哪里，疑问代词）／风雨不动安如山（安稳，形容词）</span></div>
        <div class="acc-item"><span class="acc-w">直</span><span class="acc-d">直万钱（通「值」，价值）／直挂云帆（径直、直接，副词）</span></div>
        <div class="acc-sub">词类活用</div>
        <div class="acc-item"><span class="acc-w">（本文无典型词类活用）</span><span class="acc-d">—</span></div>
        <div class="acc-sub">文言句式</div>
        <div class="acc-item"><span class="acc-w">宾语前置</span><span class="acc-d">今安在（正常语序：今在安，在哪里）</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>核心考点</h3>
        <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">① 闲来垂钓碧溪上——姜太公渭水垂钓遇周文王；② 忽复乘舟梦日边——伊尹梦见乘舟过日边后被商汤重用；③ 长风破浪——宗悫「愿乘长风破万里浪」。三个典故分别表达希望、期盼与信念。</span></div>
        <div class="acc-item"><span class="acc-w">象征手法</span><span class="acc-d">冰塞川、雪满山象征仕途艰难；长风破浪、云帆济海象征理想实现。</span></div>
        <div class="acc-item"><span class="acc-w">情感变化</span><span class="acc-d">苦闷→迷惘→希望→彷徨→乐观自信，一波三折，跌宕起伏。</span></div>
        <div class="acc-item"><span class="acc-w">名句默写</span><span class="acc-d">长风破浪会有时，直挂云帆济沧海。／欲渡黄河冰塞川，将登太行雪满山。／停杯投箸不能食，拔剑四顾心茫然。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>修辞与手法</h3>
        <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">斗十千、直万钱，极言宴席奢华。</span></div>
        <div class="acc-item"><span class="acc-w">对偶</span><span class="acc-d">欲渡黄河冰塞川，将登太行雪满山。／金樽清酒斗十千，玉盘珍羞直万钱。</span></div>
        <div class="acc-item"><span class="acc-w">反复</span><span class="acc-d">行路难，行路难，连续重复，强化情感。</span></div>
        <div class="acc-item"><span class="acc-w">动作描写</span><span class="acc-d">停、投、拔、顾四个连续动作，刻画内心的激荡与无奈。</span></div>
        <div class="acc-item"><span class="acc-w">乐景写哀</span><span class="acc-d">以盛宴的奢华反衬内心的苦闷。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文化常识</h3>
        <div class="acc-item"><span class="acc-w">姜太公钓鱼</span><span class="acc-d">姜尚（姜子牙）在渭水垂钓，遇周文王，被重用，辅佐武王灭商。后以「垂钓」指等待明主重用。</span></div>
        <div class="acc-item"><span class="acc-w">伊尹梦日</span><span class="acc-d">伊尹在受商汤重用前，梦见自己乘舟经过日月之旁。后以「梦日」指将遇明主、建功业。</span></div>
        <div class="acc-item"><span class="acc-w">宗悫破浪</span><span class="acc-d">南朝宋宗悫少年时，叔父问其志向，答曰：「愿乘长风破万里浪。」后以「乘风破浪」指志向远大、不畏艰险。</span></div>
        <div class="acc-item"><span class="acc-w">赐金放还</span><span class="acc-d">唐玄宗给李白钱财让他离开宫廷，名义上是礼遇，实际上是变相驱逐。此事发生在天宝三年（744）。</span></div>
        <div class="acc-item"><span class="acc-w">乐府</span><span class="acc-d">古代掌管音乐的官署，也指乐府官署采集和创作的诗歌。汉魏六朝乐府诗多为五言，唐代乐府古题则句式自由。</span></div>
      </div></div>
  </section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《行路难（其一）》</title>
<meta name="description" content="李白《行路难（其一）》教学课件：逐句注释译文赏析、文言积累、全屏听写练习。">
<style>
%(css)s
</style>
</head>
<body>

  <!-- 卷首 -->
  <header class="hero">
    <div class="hero-inner">
      <div class="hero-side">唐·李白</div>
      <h1 class="hero-title">行路难（其一）</h1>
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
  <div class="kai">《行路难（其一）》</div>
  <div>李白 · 唐 · 出自《李太白全集》</div>
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
