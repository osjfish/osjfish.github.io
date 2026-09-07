# -*- coding: utf-8 -*-
"""《雁门太守行》课件生成器 —— 复用《琵琶行》课件的 CSS / JS 框架（诗词类）。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = r'D:\App\Apps\yanshi\pipaxing-baijuyi.html'
OUT = r'D:\App\Apps\yanshi\yanmentaishouxing-lihe.html'

src = io.open(SRC, encoding='utf-8').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('pipa_fs', 'yanmen_fs')
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


FULLTEXT = [
    '黑云压城城欲摧，甲光向日金鳞开。',
    '角声满天秋色里，塞上燕脂凝夜紫。',
    '半卷红旗临易水，霜重鼓寒声不起。',
    '报君黄金台上意，提携玉龙为君死。',
]

S = [
("[[黑云|黑色的云，这里比喻敌军攻城的气势]][[压城|压迫城头。压，压迫、逼近]][[城欲摧|城墙将要被摧毁。欲，将要；摧，摧毁、毁坏]][[，|逗号]][[甲光|铠甲在阳光下反射的光芒。甲，铠甲，古代战士穿的护身衣]][[向日|向着太阳。向，朝向、对着]][[金鳞开|像金色的鱼鳞一样张开。金鳞，金色的鱼鳞，比喻铠甲上的金属鳞片；开，张开、展开]]。",
 "敌军如黑云压城，城墙仿佛将要被摧毁；我军铠甲迎着阳光，像金色鱼鳞般闪闪发光。",
 fixq("开篇即写战争的紧张气氛。~L~黑云压城城欲摧~R~以比喻和夸张写敌军人多势众、来势凶猛，一个~L~压~R~字写出敌军的嚣张和城池的危急。~L~甲光向日金鳞开~R~转写我军，在黑云笼罩下，铠甲迎着日光如金鳞绽开，写出我军将士严阵以待、威武不屈的形象。一暗一明，一压一开，对比鲜明，画面感极强。~L~黑云~R~既是写景，又是喻敌，一语双关。"),
 ["比喻夸张", "对比", "名句"]),

("[[角声|号角的声音。角，古代军中乐器，用兽角制成，用于号令军队]][[满天|响彻天空。满，充满、遍布]][[秋色里|在秋天的景色中。秋色，秋天的景象，多指萧瑟凄凉]][[，|逗号]][[塞上|边塞之上。塞（sài），边塞、边境上的险要地方]][[燕脂|即胭脂，红色，这里比喻战场上的血迹。燕（yān），通~L~胭~R~]][[凝夜紫|在夜色中凝结成紫色。凝，凝结；夜紫，夜里呈现紫色，指血迹在夜色中变暗发紫]]。",
 "号角的声音响彻秋天的天空，边塞上战士的血迹在夜色中凝结成暗紫色。",
 fixq("分别从听觉和视觉写战斗的惨烈。~L~角声满天~R~写号角声响彻云霄，战斗激烈；~L~秋色里~R~点明时令，秋的萧瑟与战争的惨烈相映衬。~L~塞上燕脂凝夜紫~R~写战场上的血迹在夜色中凝结成紫色，以~L~燕脂~R~（胭脂）喻血迹，构思奇特，色彩浓艳。李贺诗以~L~奇诡~R~著称，此句可见一斑——不用~L~血流成河~R~的直白，而以~L~燕脂凝夜紫~R~的意象写战争的残酷，视觉冲击力极强。"),
 ["视听结合", "用典比喻", "色彩"]),

("[[半卷红旗|红旗半卷着。半卷，指军队急行军时旗帜不能完全展开，也暗示战事不利或夜行军]][[临易水|抵达易水。临，到、抵达；易水，河名，在今河北易县，荆轲刺秦王出发处，~L~风萧萧兮易水寒~R~即此]][[，|逗号]][[霜重|霜很重。重（zhòng），浓、厚]][[鼓寒|战鼓因霜冻而声音沉闷。寒，寒冷，这里指鼓声因霜重而低沉不扬]][[声不起|声音响不起来。起，响起、振作]]。",
 "红旗半卷，援军赶赴易水；夜寒霜重，战鼓声沉闷得响不起来。",
 fixq("写援军夜袭的情景。~L~半卷红旗~R~写出军队急行军的状态——夜色中或风中旗帜不能完全展开，也暗示战事紧张。~L~临易水~R~用荆轲刺秦的典故，~L~风萧萧兮易水寒，壮士一去兮不复还~R~，暗示将士们抱着必死的决心奔赴战场。~L~霜重鼓寒声不起~R~写夜寒霜重，战鼓被冻得敲不响，以环境的恶劣烘托战斗的艰苦和将士的坚韧。~L~不起~R~二字，既写鼓声，也暗示战局的艰难。"),
 ["用典", "环境烘托", "悲壮"]),

("[[报君|报答君主。报，报答；君，君主、皇帝]][[黄金台上意|黄金台上的心意。黄金台，战国时燕昭王所筑，置千金于台上，招揽天下贤士；意，心意、恩情]][[，|逗号]][[提携|携带、拿起。提，提着；携，带着]][[玉龙|指宝剑。传说晋代雷焕得玉匣，内有双剑，后化龙入水，故以玉龙代指宝剑]][[为君死|为君主而死。为（wèi），替、给；死，牺牲、献身]]。",
 "为了报答君主在黄金台上招贤纳士的恩情，（将士们）手持宝剑甘愿为国血战到死。",
 fixq("尾联点明主旨，抒写将士们誓死报国的决心。~L~黄金台~R~用燕昭王筑台招贤的典故，写出君主对人才的重视和将士知恩图报的心理。~L~提携玉龙为君死~R~以~L~玉龙~R~代指宝剑，~L~为君死~R~直抒胸臆，写出将士们视死如归的英雄气概。全诗以浓墨重彩的战争画面铺垫，最后以~L~为君死~R~的誓言收束，悲壮激昂，感人至深。这是李贺的代表作，也是唐代边塞诗中的名篇。"),
 ["用典", "主旨", "悲壮"]),
]

DICT_WORDS = [
    {"w":"摧","py":"cuī","q":"黑云压城城欲□","tip":"「摧」提手旁，摧毁，音 cuī；与「催」（单人旁）「崔」（山字头）区分"},
    {"w":"鳞","py":"lín","q":"甲光向日金□开","tip":"「鳞」鱼字旁，鱼鳞，音 lín；与「粼」（粼粼）「麟」（麒麟）区分"},
    {"w":"燕","py":"yān","q":"塞上□脂凝夜紫","tip":"「燕」多音字，「燕脂」通「胭脂」读 yān（一声）；燕子读 yàn（四声）"},
    {"w":"凝","py":"níng","q":"塞上燕脂□夜紫","tip":"「凝」两点水，凝结，音 níng；与「疑」（yí，怀疑）区分，左部是「冫」不是「匕」"},
    {"w":"易","py":"yì","q":"半卷红旗临□水","tip":"「易」日字头，音 yì；与「昜」（yáng）区分，下部是「勿」不是「一丿」"},
    {"w":"霜","py":"shuāng","q":"□重鼓寒声不起","tip":"「霜」雨字头，音 shuāng；与「孀」（女字旁）「相」区分"},
    {"w":"携","py":"xié","q":"提□玉龙为君死","tip":"「携」提手旁，携带，音 xié；与「镌」（juān，镌刻）「隽」区分，右部是「隽」"},
    {"w":"鼓","py":"gǔ","q":"霜重□寒声不起","tip":"「鼓」左右结构，音 gǔ；与「豉」（chǐ，豆豉）区分，左部是「壴」不是「豆」"},
]

DICT_NOTES = [
    {"w":"黑云","q":"黑云压城城欲摧","a":"比喻敌军攻城的气势，也指乌云"},
    {"w":"摧","q":"黑云压城城欲摧","a":"摧毁、毁坏"},
    {"w":"甲光","q":"甲光向日金鳞开","a":"铠甲在阳光下反射的光芒。甲，铠甲"},
    {"w":"金鳞","q":"甲光向日金鳞开","a":"金色的鱼鳞，比喻铠甲上的金属鳞片"},
    {"w":"角","q":"角声满天秋色里","a":"古代军中号角，用兽角制成"},
    {"w":"塞","q":"塞上燕脂凝夜紫","a":"边塞、边境，音 sài"},
    {"w":"燕脂","q":"塞上燕脂凝夜紫","a":"即胭脂，红色，比喻战场上的血迹。燕通「胭」"},
    {"w":"凝","q":"塞上燕脂凝夜紫","a":"凝结"},
    {"w":"临","q":"半卷红旗临易水","a":"到、抵达"},
    {"w":"易水","q":"半卷红旗临易水","a":"河名，在今河北易县，荆轲刺秦出发处"},
    {"w":"重","q":"霜重鼓寒声不起","a":"浓、厚，音 zhòng"},
    {"w":"声不起","q":"霜重鼓寒声不起","a":"声音响不起来，指鼓声因霜重而低沉"},
    {"w":"黄金台","q":"报君黄金台上意","a":"战国燕昭王所筑，置千金招贤，后指招贤纳士之地"},
    {"w":"提携","q":"提携玉龙为君死","a":"携带、拿起"},
    {"w":"玉龙","q":"提携玉龙为君死","a":"指宝剑，传说宝剑化龙入水，故以玉龙代指"},
    {"w":"为","q":"提携玉龙为君死","a":"替、给，音 wèi"},
]

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
      中唐时期，藩镇割据，战乱频仍。李贺以浓艳奇诡的笔触，描绘了一场惨烈的边塞保卫战——黑云压城、金鳞向日、角声满天、燕脂凝紫，最后以~L~提携玉龙为君死~R~的誓言收束，悲壮激昂，千古传诵。
    </div>
    <div class="box">
      <h3>作者简介</h3>
      <p><b>李贺</b>（790—816），字长吉，唐代诗人，福昌昌谷（今河南宜阳）人。出身没落贵族，因父名~L~晋肃~R~，~L~晋~R~与~L~进~R~同音，被人排挤不得参加进士考试，只做过奉礼郎的小官。一生困顿，二十七岁即去世。</p>
      <p>李贺诗风奇诡幽冷、色彩浓艳，想象奇特，被称为~L~诗鬼~R~，与李白（诗仙）、李商隐（诗魂）并称~L~三李~R~。代表作品有《雁门太守行》《李凭箜篌引》《马诗》等。</p>
    </div>
    <div class="box">
      <h3>创作背景</h3>
      <p>《雁门太守行》是乐府旧题，属于《相和歌辞·瑟调曲》，内容多写边塞征战。李贺以此题写了这首诗。</p>
      <p>中唐时期，藩镇割据，叛乱不断。元和四年（809），成德军节度使王承宗叛乱，朝廷派兵讨伐。李贺可能以此为背景，或泛写边塞战争，创作了这首诗。全诗没有具体写某次战役，而是以浓墨重彩的画面，塑造了将士们誓死报国的英雄形象。</p>
      <p>据传说，韩愈、皇甫湜来访李贺，李贺即席赋此诗，二人大为惊叹。可见此诗是李贺的精心之作。</p>
      <p class="note">※ 雁门：郡名，在今山西大同东北一带，是唐代北方边防重镇。太守：郡的最高行政长官。</p>
    </div>
    <div class="box media-box">
      <h3>朗诵 · 讲解</h3>
      <div class="media-grid">
        <div class="media">
          <h4>课文朗读《雁门太守行》</h4>
          <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1Ye4y1Y7pK&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读《雁门太守行》"></iframe>
          <a href="https://www.bilibili.com/video/BV1Ye4y1Y7pK" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
        </div>
        <div class="media">
          <h4>动画讲解《雁门太守行》</h4>
          <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1nZ4y1k7Xm&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="动画讲解《雁门太守行》"></iframe>
          <a href="https://www.bilibili.com/video/BV1nZ4y1k7Xm" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
        </div>
      </div>
    </div>
  </section>
''')

APP = fixq(u'''
  <section id="app" class="sec">
    <div class="sec-head"><h2>赏 析</h2><span class="no">画面 · 手法 · 艺术 · 名句</span></div>
    <div class="box">
      <h3>画面层次</h3>
      <p>全诗四句四幅画面，层层递进：</p>
      <p><b>第一幅（首联）</b>：敌军压境，我军待敌。黑云与金鳞对比，写出战争的紧张和我军的威武。</p>
      <p><b>第二幅（颔联）</b>：战斗惨烈，血染边塞。角声满天写听觉，燕脂凝紫写视觉，视听结合。</p>
      <p><b>第三幅（颈联）</b>：援军夜袭，霜重鼓寒。半卷红旗、临易水，用荆轲典故写必死决心。</p>
      <p><b>第四幅（尾联）</b>：誓死报国，为君战死。用黄金台典故点明主旨，悲壮收束。</p>
    </div>
    <div class="box">
      <h3>艺术特色</h3>
      <p><b>① 色彩浓艳，对比鲜明</b>：黑云、金鳞、燕脂、夜紫、红旗，色彩浓烈，画面感极强。黑与金、红与紫对比，视觉冲击力大。</p>
      <p><b>② 视听结合</b>：角声满天（听觉）与燕脂凝紫（视觉）结合，写出战斗的惨烈。</p>
      <p><b>③ 善用典故</b>：易水（荆轲刺秦）、黄金台（燕昭王招贤），两个典故分别写将士的必死决心和报恩心理，含蓄而深刻。</p>
      <p><b>④ 想象奇特</b>：以~L~黑云~R~喻敌军，以~L~金鳞~R~喻铠甲，以~L~燕脂~R~喻血迹，以~L~玉龙~R~喻宝剑，比喻新奇，体现李贺~L~诗鬼~R~的奇诡风格。</p>
    </div>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">黑云压城城欲摧，甲光向日金鳞开。</div>
        <p>千古名句。~L~黑云压城~R~以比喻夸张写敌军人多势众，~L~压~R~字极有力度；~L~甲光向日金鳞开~R~转写我军，在黑云笼罩下铠甲如金鳞绽开，威武不屈。一暗一明，一压一开，对比鲜明，是写战争紧张气氛的典范。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">报君黄金台上意，提携玉龙为君死。</div>
        <p>全诗主旨句。用燕昭王黄金台招贤的典故，写出将士们知恩图报、誓死报国的决心。~L~玉龙~R~代指宝剑，~L~为君死~R~直抒胸臆，悲壮激昂，感人至深。</p>
      </div>
    </div>
  </section>
''')

ACC = fixq(u'''
  <section id="acc" class="sec">
    <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 考点 · 修辞 · 文化常识</span></div>
    <div class="box"><div class="acc-cat">
        <h3>文体与诗体</h3>
        <div class="acc-item"><span class="acc-w">乐府旧题</span><span class="acc-d">《雁门太守行》是乐府《相和歌辞·瑟调曲》旧题，内容多写边塞征战。李贺以此题写边塞战争。</span></div>
        <div class="acc-item"><span class="acc-w">七言歌行</span><span class="acc-d">全诗八句，每句七言，属于古体诗（歌行体），不受近体格律束缚。</span></div>
        <div class="acc-item"><span class="acc-w">用韵</span><span class="acc-d">摧、开押 ai 韵；里、紫押 i 韵；水、起押 i 韵；意、死押 i 韵。中间换韵，与画面转换同步。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>易错字音形</h3>
        <div class="acc-item"><span class="acc-w">摧 cuī</span><span class="acc-d">提手旁，摧毁。勿写成「催」（单人旁，催促）。</span></div>
        <div class="acc-item"><span class="acc-w">鳞 lín</span><span class="acc-d">鱼字旁，鱼鳞。勿写成「粼」（粼粼，水波清澈）「麟」（麒麟）。</span></div>
        <div class="acc-item"><span class="acc-w">燕 yān</span><span class="acc-d">多音字。「燕脂」通「胭脂」读 yān（一声）；燕子读 yàn（四声）。</span></div>
        <div class="acc-item"><span class="acc-w">凝 níng</span><span class="acc-d">两点水，凝结。勿写成「疑」（yí，怀疑）。左部是「冫」不是「匕」。</span></div>
        <div class="acc-item"><span class="acc-w">塞 sài</span><span class="acc-d">多音字。边塞读 sài（本文），堵塞读 sè，瓶塞读 sāi。</span></div>
        <div class="acc-item"><span class="acc-w">重 zhòng</span><span class="acc-d">多音字。霜重读 zhòng（本文），重复读 chóng。</span></div>
        <div class="acc-item"><span class="acc-w">携 xié</span><span class="acc-d">提手旁，携带。勿写成「镌」（juān，镌刻）。右部是「隽」。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文言梳理</h3>
        <div class="acc-sub">通假字</div>
        <div class="acc-item"><span class="acc-w">塞上燕脂凝夜紫</span><span class="acc-d">燕通「胭」，燕脂即胭脂</span></div>
        <div class="acc-sub">古今异义</div>
        <div class="acc-item"><span class="acc-w">黑云压城城欲摧</span><span class="acc-d">摧：古义摧毁、毁坏；今义摧残、折磨（程度较轻）</span></div>
        <div class="acc-item"><span class="acc-w">半卷红旗临易水</span><span class="acc-d">临：古义到、抵达；今义靠近、面对（如「临街」）</span></div>
        <div class="acc-sub">一词多义</div>
        <div class="acc-item"><span class="acc-w">开</span><span class="acc-d">甲光向日金鳞开（张开、展开）／诚开金石（打开）／开花（绽放）</span></div>
        <div class="acc-item"><span class="acc-w">报</span><span class="acc-d">报君黄金台上意（报答）／报之以李（回报）／报告（告知）</span></div>
        <div class="acc-sub">词类活用</div>
        <div class="acc-item"><span class="acc-w">（本文无典型词类活用）</span><span class="acc-d">—</span></div>
        <div class="acc-sub">文言句式</div>
        <div class="acc-item"><span class="acc-w">（本文无特殊句式）</span><span class="acc-d">—</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>核心考点</h3>
        <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">① 临易水——荆轲刺秦，「风萧萧兮易水寒」，暗示必死决心；② 黄金台——燕昭王筑台招贤，写君主重才与将士报恩。</span></div>
        <div class="acc-item"><span class="acc-w">色彩描写</span><span class="acc-d">黑云、金鳞、燕脂、夜紫、红旗，色彩浓烈，对比鲜明，是李贺诗的标志性特色。</span></div>
        <div class="acc-item"><span class="acc-w">视听结合</span><span class="acc-d">角声满天（听觉）＋燕脂凝紫（视觉），写出战斗的惨烈。</span></div>
        <div class="acc-item"><span class="acc-w">名句默写</span><span class="acc-d">黑云压城城欲摧，甲光向日金鳞开。／报君黄金台上意，提携玉龙为君死。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>修辞与手法</h3>
        <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">黑云喻敌军，金鳞喻铠甲，燕脂喻血迹，玉龙喻宝剑。</span></div>
        <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">城欲摧、角声满天，极写敌军凶猛和战斗激烈。</span></div>
        <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">黑云（暗）与金鳞（明）对比，敌军（压）与我军（开）对比。</span></div>
        <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">易水（荆轲）、黄金台（燕昭王），含蓄表达将士的决心与报恩心理。</span></div>
        <div class="acc-item"><span class="acc-w">渲染烘托</span><span class="acc-d">以秋色、霜重、鼓寒等环境描写烘托战争的惨烈和将士的坚韧。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文化常识</h3>
        <div class="acc-item"><span class="acc-w">雁门</span><span class="acc-d">郡名，在今山西大同东北，唐代北方边防重镇，常与北方游牧民族交战。</span></div>
        <div class="acc-item"><span class="acc-w">太守</span><span class="acc-d">郡的最高行政长官，秦置，汉沿设，隋唐时州的长官称刺史或太守。</span></div>
        <div class="acc-item"><span class="acc-w">黄金台</span><span class="acc-d">又称招贤台，战国时燕昭王所筑，置千金于台上，招揽天下贤士。后以「黄金台」指招贤纳士之地。</span></div>
        <div class="acc-item"><span class="acc-w">易水送别</span><span class="acc-d">荆轲刺秦王前，燕太子丹在易水送别，荆轲歌曰：「风萧萧兮易水寒，壮士一去兮不复还。」后以「易水」指悲壮送别。</span></div>
        <div class="acc-item"><span class="acc-w">玉龙</span><span class="acc-d">指宝剑。传说晋代雷焕得玉匣，内有双剑，后双剑化龙入水。故以「玉龙」代指宝剑。</span></div>
        <div class="acc-item"><span class="acc-w">诗鬼</span><span class="acc-d">李贺的称号，因其诗风奇诡幽冷、想象奇特而得名。与「诗仙」李白、「诗圣」杜甫、「诗佛」王维并称。</span></div>
      </div></div>
  </section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《雁门太守行》</title>
<meta name="description" content="李贺《雁门太守行》教学课件：逐句注释译文赏析、文言积累、全屏听写练习。">
<style>
%(css)s
</style>
</head>
<body>

  <header class="hero">
    <div class="hero-inner">
      <div class="hero-side">唐·李贺</div>
      <h1 class="hero-title">雁门太守行</h1>
    </div>
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
  <div class="kai">《雁门太守行》</div>
  <div>李贺 · 唐 · 出自《李长吉歌诗》</div>
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
