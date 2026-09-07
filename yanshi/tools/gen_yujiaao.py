# -*- coding: utf-8 -*-
"""《渔家傲（天接云涛连晓雾）》课件生成器 —— 复用《琵琶行》课件的 CSS / JS 框架（诗词类）。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = r'D:\App\Apps\yanshi\pipaxing-baijuyi.html'
OUT = r'D:\App\Apps\yanshi\yujiaao-liqingzhao.html'

src = io.open(SRC, encoding='utf-8').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('pipa_fs', 'yjiao_fs')
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
    '天接云涛连晓雾，星河欲转千帆舞。',
    '仿佛梦魂归帝所，闻天语，殷勤问我归何处。',
    '我报路长嗟日暮，学诗谩有惊人句。',
    '九万里风鹏正举。风休住，蓬舟吹取三山去！',
]

S = [
("[[天接|天空连接着。接，连接、衔接]][[云涛|如波涛般的云彩。云涛，云层翻涌如波涛]][[连晓雾|与拂晓的雾气连成一片。连，连接；晓雾，拂晓的雾气]][[，|逗号]][[星河|银河、天河。星，星辰；河，天河]][[欲转|将要转动。欲，将要；转，转动、旋转，指银河在天空中移动]][[千帆舞|无数船帆在风中起舞。千帆，极言船多；舞，舞动、飘动]]。",
 "天空连接着如波涛般的云彩，与拂晓的雾气连成一片；银河将要转动，无数船帆在风中起舞。",
 fixq("开篇描绘了一幅辽阔壮美的海天拂晓图。~L~天接云涛连晓雾~R~写天际云涛翻涌、晓雾弥漫，境界开阔；~L~星河欲转千帆舞~R~写银河西移、千帆竞舞，想象奇特。这是词人梦中所见，虚实结合——既有真实的海天景色，又有梦幻般的瑰丽想象。~L~接~R~~L~连~R~二字写出天地相连的壮阔，~L~舞~R~字赋予千帆以生命，画面动感十足。李清照词以婉约著称，此词却境界开阔、气势磅礴，被评家誉为~L~无一毫钗粉气~R~。"),
 ["虚实结合", "开阔境界", "梦魂"]),

("[[仿佛|好像、似乎。仿（fǎng）佛（fú），模模糊糊的样子]][[梦魂|梦中的灵魂。古人认为人做梦时灵魂会离开身体]][[归帝所|回到天帝的居所。归，回到；帝所，天帝居住的地方，即天宫]][[，|逗号]][[闻天语|听到天帝说话。闻，听到；天语，天帝的话语]][[，|逗号]][[殷勤|情意恳切、热情周到。殷（yīn）勤，恳切的样子]][[问我归何处|问我要回到哪里去。归，回去、归宿；何处，哪里]]。",
 "恍惚间梦魂回到了天帝的居所，听到天帝说话，情意恳切地问我要回到哪里去。",
 fixq("承上启下，由景入情。~L~仿佛梦魂归帝所~R~写词人在梦中魂飞天外，来到天帝居所，想象奇瑰。~L~闻天语，殷勤问我归何处~R~写天帝亲切发问，一个~L~殷勤~R~写出天帝的温和与关切。这一问，引出下片词人的回答——~L~我报路长嗟日暮~R~。天帝的~L~问~R~与词人的~L~报~R~构成对话，结构巧妙。此词题为~L~记梦~R~，全词以梦境贯穿，天帝的出现是梦境的核心。"),
 ["承上启下", "对话结构", "记梦"]),

("[[我报|我回答。报，回答、禀报]][[路长|路途漫长。路，道路，这里比喻人生道路、理想之路；长，漫长]][[嗟日暮|叹息天色已晚。嗟（jiē），叹息、慨叹；日暮，天色已晚，比喻年华已逝、前途渺茫]][[，|逗号]][[学诗|学习写诗。学，学习；诗，诗歌创作]][[谩有|空有、徒有。谩（màn），通~L~漫~R~，徒然、空自；有，拥有]][[惊人句|惊人的诗句。惊人，使人惊讶；句，诗句]]。",
 "我回答说：路途漫长啊，又叹息天色已晚；学诗空有惊人的诗句。",
 fixq("词人回答天帝之问，抒发内心的苦闷。~L~路长嗟日暮~R~化用屈原《离骚》~L~路漫漫其修远兮~R~和~L~日忽忽其将暮~R~，写人生道路漫长而天色已晚，比喻理想未实现而年华已逝。~L~学诗谩有惊人句~R~写自己虽有诗才，却~L~谩有~R~（空有）——在乱世中，才华无处施展，诗句再惊人也无济于事。一个~L~谩~R~字，含无限感慨与愤懑。李清照南渡后，国破家亡，丈夫去世，孤身漂泊，此句正是她晚年心境的真实写照。"),
 ["用典", "苦闷", "谩有"]),

("[[九万里风鹏正举|九万里高空的大风中，大鹏正展翅高飞。九万里，极言高远，出自《庄子·逍遥游》~L~鹏之徙于南冥也，水击三千里，抟扶摇而上者九万里~R~；鹏，大鹏鸟；正举，正展翅高飞。举，飞起、高飞]][[。|句号]][[风休住|风啊不要停止。休，不要、别；住，停止]][[，|逗号]][[蓬舟|像蓬草一样轻快的小船。蓬，蓬草，枯后根断，随风飘转，比喻小船轻快]][[吹取三山去|把我吹到三山去。吹取，吹到、吹向；三山，指传说中的蓬莱、方丈、瀛洲三座仙山，在东海中]]！",
 "九万里高空的大风中，大鹏正展翅高飞。风啊不要停止，把我这轻快的小船吹到三座仙山去吧！",
 fixq("结尾振起，由苦闷转向豪迈。~L~九万里风鹏正举~R~用《庄子·逍遥游》大鹏展翅的典故，境界骤开，气势磅礴。~L~风休住，蓬舟吹取三山去~R~以呼告的语气，祈求大风把自己吹向仙山，表达对自由、理想境界的向往。全词从梦境的壮阔，到天帝的发问，到词人的苦闷，最后以大鹏展翅、乘风赴仙山的豪迈收束——在现实中无法实现的理想，只能寄托于梦境与仙境。这是李清照词中少见的豪放之作，梁启超评曰：~L~此绝似苏辛派，不类《漱玉词》中语。~R~"),
 ["用典", "豪放", "主旨", "呼告"]),
]

DICT_WORDS = [
    {"w":"涛","py":"tāo","q":"天接云□连晓雾","tip":"「涛」三点水，波涛，音 tāo；与「滔」（滔滔不绝）「韬」区分"},
    {"w":"晓","py":"xiǎo","q":"天接云涛连□雾","tip":"「晓」日字旁，拂晓，音 xiǎo；与「饶」「绕」「烧」区分，右部是「尧」"},
    {"w":"帆","py":"fān","q":"星河欲转千□舞","tip":"「帆」巾字旁，船帆，音 fān；与「凡」「矾」区分"},
    {"w":"殷","py":"yīn","q":"□勤问我归何处","tip":"「殷」多音字，殷勤读 yīn（一声）；殷红读 yān；殷切读 yǐn。右部是「殳」不是「攵」"},
    {"w":"嗟","py":"jiē","q":"我报路长□日暮","tip":"「嗟」口字旁，叹息，音 jiē；与「蹉」（cuō，蹉跎）「搓」区分"},
    {"w":"谩","py":"màn","q":"学诗□有惊人句","tip":"「谩」言字旁，通「漫」，徒然，音 màn；与「慢」（竖心旁）「漫」（三点水）区分"},
    {"w":"鹏","py":"péng","q":"九万里风□正举","tip":"「鹏」鸟字旁，大鹏鸟，音 péng；与「朋」「棚」「绷」区分"},
    {"w":"蓬","py":"péng","q":"□舟吹取三山去","tip":"「蓬」草字头，蓬草，音 péng；与「篷」（竹字头，船篷）「逢」区分"},
]

DICT_NOTES = [
    {"w":"云涛","q":"天接云涛连晓雾","a":"如波涛般的云彩，云层翻涌如波涛"},
    {"w":"晓雾","q":"天接云涛连晓雾","a":"拂晓的雾气。晓，天刚亮"},
    {"w":"星河","q":"星河欲转千帆舞","a":"银河、天河"},
    {"w":"欲转","q":"星河欲转千帆舞","a":"将要转动。欲，将要；转，旋转"},
    {"w":"仿佛","q":"仿佛梦魂归帝所","a":"好像、似乎，模模糊糊的样子"},
    {"w":"帝所","q":"仿佛梦魂归帝所","a":"天帝居住的地方，即天宫"},
    {"w":"天语","q":"闻天语","a":"天帝的话语"},
    {"w":"殷勤","q":"殷勤问我归何处","a":"情意恳切、热情周到"},
    {"w":"报","q":"我报路长嗟日暮","a":"回答、禀报"},
    {"w":"嗟","q":"我报路长嗟日暮","a":"叹息、慨叹，音 jiē"},
    {"w":"日暮","q":"我报路长嗟日暮","a":"天色已晚，比喻年华已逝、前途渺茫"},
    {"w":"谩","q":"学诗谩有惊人句","a":"通「漫」，徒然、空自，音 màn"},
    {"w":"惊人句","q":"学诗谩有惊人句","a":"惊人的诗句，指才华出众的作品"},
    {"w":"鹏正举","q":"九万里风鹏正举","a":"大鹏正展翅高飞。举，飞起、高飞"},
    {"w":"休","q":"风休住","a":"不要、别"},
    {"w":"蓬舟","q":"蓬舟吹取三山去","a":"像蓬草一样轻快的小船"},
    {"w":"三山","q":"蓬舟吹取三山去","a":"传说中的蓬莱、方丈、瀛洲三座仙山"},
    {"w":"吹取","q":"蓬舟吹取三山去","a":"吹到、吹向。取，语助词，无实义"},
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
      李清照南渡后，国破家亡，丈夫赵明诚去世，孤身漂泊江南。一个拂晓，她乘船航行于海上，见云涛翻涌、星河欲转，梦魂飞天，天帝发问——于是写下这首境界开阔、想象奇瑰的《渔家傲》，被评家誉为~L~无一毫钗粉气~R~。
    </div>
    <div class="box">
      <h3>作者简介</h3>
      <p><b>李清照</b>（1084—约1155），号易安居士，宋代女词人，婉约词派代表，有~L~千古第一才女~R~之称。早年生活优裕，与丈夫赵明诚共同致力于书画金石的搜集整理。金兵入据中原后，流寓南方，丈夫病逝，境遇孤苦。</p>
      <p>其词以南渡为界，前期多写悠闲生活和闺阁相思，清丽明快；后期多写国破家亡之痛和身世飘零之苦，沉哀凄苦。代表作品有《声声慢·寻寻觅觅》《如梦令·常记溪亭日暮》《一剪梅·红藕香残玉簟秋》等，词集名《漱玉词》。</p>
    </div>
    <div class="box">
      <h3>创作背景</h3>
      <p>此词写于李清照南渡之后。建炎四年（1130），李清照曾乘船航行于海上，经历了风浪颠簸。词中~L~云涛~R~~L~晓雾~R~~L~星河~R~~L~千帆~R~等意象，可能与这段海上经历有关。</p>
      <p>此时的李清照，国破家亡，丈夫去世，孤身一人，漂泊无依。她在现实中找不到出路，便在梦境中寻求慰藉——梦魂飞天，天帝发问，大鹏展翅，乘风赴仙山。全词以记梦的形式，将现实的苦闷与对理想的向往交织在一起，境界开阔，气势磅礴，在李清照词中别具一格。</p>
      <p class="note">※ 渔家傲：词牌名，双调六十二字，上下片各五句、五仄韵。此词一题作「记梦」。</p>
    </div>
    <div class="box media-box">
      <h3>朗诵 · 讲解</h3>
      <div class="media-grid">
        <div class="media">
          <h4>课文朗读《渔家傲》</h4>
          <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV15d4y1V7eW&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读《渔家傲》"></iframe>
          <a href="https://www.bilibili.com/video/BV15d4y1V7eW" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
        </div>
        <div class="media">
          <h4>动画讲解《渔家傲》</h4>
          <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1Yz4y1R7mf&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="动画讲解《渔家傲》"></iframe>
          <a href="https://www.bilibili.com/video/BV1Yz4y1R7mf" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
        </div>
      </div>
    </div>
  </section>
''')

APP = fixq(u'''
  <section id="app" class="sec">
    <div class="sec-head"><h2>赏 析</h2><span class="no">记梦 · 手法 · 艺术 · 名句</span></div>
    <div class="box">
      <h3>记梦结构</h3>
      <p>全词以~L~记梦~R~贯穿，可分三层：</p>
      <p><b>第一层（开头两句）</b>：写梦中所见的壮阔景象——天接云涛、星河欲转、千帆竞舞，为梦境铺设瑰丽的背景。</p>
      <p><b>第二层（中间三句）</b>：写梦魂飞天，天帝发问——~L~殷勤问我归何处~R~，引出词人的倾诉。</p>
      <p><b>第三层（结尾四句）</b>：写词人的回答与向往——路长日暮、谩有诗才，最后以大鹏展翅、乘风赴仙山收束，在梦境中寻求理想的归宿。</p>
    </div>
    <div class="box">
      <h3>艺术特色</h3>
      <p><b>① 想象奇瑰，境界开阔</b>：云涛、星河、千帆、帝所、大鹏、三山，意象宏大，想象奇特，完全突破了婉约词的闺阁境界。</p>
      <p><b>② 虚实结合，梦幻交融</b>：海上航行的实景与梦中飞天的幻境交织，亦真亦幻，朦胧瑰丽。</p>
      <p><b>③ 善用典故</b>：~L~路长嗟日暮~R~化用屈原《离骚》，~L~九万里风鹏正举~R~用《庄子·逍遥游》大鹏典故，~L~三山~R~用海上仙山传说，典故丰富而贴切。</p>
      <p><b>④ 豪放与婉约并存</b>：既有~L~九万里风鹏正举~R~的豪放，又有~L~我报路长嗟日暮~R~的婉约，刚柔相济，是李清照词中少见的~L~豪放~R~之作。</p>
    </div>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">九万里风鹏正举。风休住，蓬舟吹取三山去！</div>
        <p>全词最强音。用《庄子·逍遥游》大鹏展翅的典故，境界骤开，气势磅礴。~L~风休住~R~以呼告语气祈求大风不停，~L~蓬舟吹取三山去~R~表达对自由、理想境界的向往。在现实中无法实现的理想，只能寄托于梦境与仙境，豪迈中含悲凉。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">我报路长嗟日暮，学诗谩有惊人句。</div>
        <p>化用屈原《离骚》~L~路漫漫其修远兮~R~~L~日忽忽其将暮~R~，写人生道路漫长而年华已逝。~L~谩有~R~（空有）二字，含无限感慨——虽有惊世诗才，在乱世中却无处施展。这是李清照晚年心境的真实写照。</p>
      </div>
    </div>
  </section>
''')

ACC = fixq(u'''
  <section id="acc" class="sec">
    <div class="sec-head"><h2>积 累</h2><span class="no">词牌 · 字音形 · 文言 · 考点 · 修辞 · 文化常识</span></div>
    <div class="box"><div class="acc-cat">
        <h3>文体与词牌</h3>
        <div class="acc-item"><span class="acc-w">渔家傲</span><span class="acc-d">词牌名，双调六十二字，上下片各五句、五仄韵。此词一题作「记梦」。</span></div>
        <div class="acc-item"><span class="acc-w">词的特点</span><span class="acc-d">词又称长短句，句式长短不齐，有固定的词牌、字数、平仄和用韵。此词上下片各五句，句式为七、七、七、三、四。</span></div>
        <div class="acc-item"><span class="acc-w">用韵</span><span class="acc-d">全词押仄韵：雾、舞、所、处、暮、句、举、住、去，均为去声或入声，韵脚密集，节奏急促。</span></div>
        <div class="acc-item"><span class="acc-w">婉约与豪放</span><span class="acc-d">李清照为婉约派代表，但此词境界开阔、气势磅礴，被评家誉为「无一毫钗粉气」，是其词中少见的豪放之作。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>易错字音形</h3>
        <div class="acc-item"><span class="acc-w">涛 tāo</span><span class="acc-d">三点水，波涛。勿写成「滔」（滔滔不绝）。</span></div>
        <div class="acc-item"><span class="acc-w">晓 xiǎo</span><span class="acc-d">日字旁，拂晓。勿写成「饶」「绕」。右部是「尧」。</span></div>
        <div class="acc-item"><span class="acc-w">殷 yīn</span><span class="acc-d">多音字。殷勤读 yīn（一声）；殷红读 yān；殷切读 yǐn。右部是「殳」不是「攵」。</span></div>
        <div class="acc-item"><span class="acc-w">嗟 jiē</span><span class="acc-d">口字旁，叹息。勿写成「蹉」（cuō，蹉跎）。</span></div>
        <div class="acc-item"><span class="acc-w">谩 màn</span><span class="acc-d">言字旁，通「漫」，徒然。勿写成「慢」（竖心旁）「漫」（三点水）。</span></div>
        <div class="acc-item"><span class="acc-w">鹏 péng</span><span class="acc-d">鸟字旁，大鹏鸟。勿写成「朋」「棚」。</span></div>
        <div class="acc-item"><span class="acc-w">蓬 péng</span><span class="acc-d">草字头，蓬草。勿写成「篷」（竹字头，船篷）。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文言梳理</h3>
        <div class="acc-sub">通假字</div>
        <div class="acc-item"><span class="acc-w">学诗谩有惊人句</span><span class="acc-d">谩通「漫」，徒然、空自</span></div>
        <div class="acc-sub">古今异义</div>
        <div class="acc-item"><span class="acc-w">殷勤问我归何处</span><span class="acc-d">殷勤：古义情意恳切；今义热情周到（含义基本相同，但古义更重「恳切」）</span></div>
        <div class="acc-item"><span class="acc-w">九万里风鹏正举</span><span class="acc-d">举：古义飞起、高飞；今义举起、推荐</span></div>
        <div class="acc-sub">一词多义</div>
        <div class="acc-item"><span class="acc-w">报</span><span class="acc-d">我报路长嗟日暮（回答、禀报）／报君黄金台上意（报答）／报告（告知）</span></div>
        <div class="acc-item"><span class="acc-w">归</span><span class="acc-d">归帝所（回到）／归何处（归宿、回去）／完璧归赵（归还）</span></div>
        <div class="acc-sub">词类活用</div>
        <div class="acc-item"><span class="acc-w">（本文无典型词类活用）</span><span class="acc-d">—</span></div>
        <div class="acc-sub">文言句式</div>
        <div class="acc-item"><span class="acc-w">（本文无特殊句式）</span><span class="acc-d">—</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>核心考点</h3>
        <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">① 路长嗟日暮——化用屈原《离骚》「路漫漫其修远兮」「日忽忽其将暮」；② 九万里风鹏正举——用《庄子·逍遥游》大鹏展翅典故；③ 三山——传说中的蓬莱、方丈、瀛洲三座仙山。</span></div>
        <div class="acc-item"><span class="acc-w">记梦手法</span><span class="acc-d">全词以梦境贯穿，梦魂飞天、天帝发问、大鹏展翅，虚实结合，亦真亦幻。</span></div>
        <div class="acc-item"><span class="acc-w">豪放风格</span><span class="acc-d">此词境界开阔、气势磅礴，与李清照婉约词风不同，被称为「无一毫钗粉气」。</span></div>
        <div class="acc-item"><span class="acc-w">名句默写</span><span class="acc-d">九万里风鹏正举。风休住，蓬舟吹取三山去！／我报路长嗟日暮，学诗谩有惊人句。／天接云涛连晓雾，星河欲转千帆舞。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>修辞与手法</h3>
        <div class="acc-item"><span class="acc-w">想象</span><span class="acc-d">梦魂飞天、天帝发问、大鹏展翅、三山仙境，想象奇瑰，是全词最突出的特色。</span></div>
        <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">屈原《离骚》、庄子《逍遥游》、海上仙山传说，典故丰富而贴切。</span></div>
        <div class="acc-item"><span class="acc-w">虚实结合</span><span class="acc-d">海上实景与梦中幻境交织，亦真亦幻。</span></div>
        <div class="acc-item"><span class="acc-w">呼告</span><span class="acc-d">风休住——直接对风呼唤，语气强烈。</span></div>
        <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">九万里、千帆，极言高远与众多。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文化常识</h3>
        <div class="acc-item"><span class="acc-w">星河</span><span class="acc-d">即银河、天河。古人认为银河是天上的河流，由无数星辰组成。</span></div>
        <div class="acc-item"><span class="acc-w">帝所</span><span class="acc-d">天帝居住的地方，即天宫、天庭。中国古代神话中，天帝是最高天神。</span></div>
        <div class="acc-item"><span class="acc-w">大鹏</span><span class="acc-d">出自《庄子·逍遥游》：「鹏之徙于南冥也，水击三千里，抟扶摇而上者九万里。」后以大鹏比喻志向远大、气概非凡。</span></div>
        <div class="acc-item"><span class="acc-w">三山</span><span class="acc-d">传说中东海中的三座仙山：蓬莱、方丈、瀛洲，山上有仙人与不死之药。后以「三山」指仙境或理想之地。</span></div>
        <div class="acc-item"><span class="acc-w">蓬舟</span><span class="acc-d">像蓬草一样轻快的小船。蓬草枯后根断，随风飘转，故称「飘蓬」，比喻行踪不定。</span></div>
        <div class="acc-item"><span class="acc-w">南渡</span><span class="acc-d">1127年「靖康之变」后，宋室南迁，史称「南渡」。李清照随难民南下，从此国破家亡，漂泊江南。</span></div>
      </div></div>
  </section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《渔家傲》</title>
<meta name="description" content="李清照《渔家傲（天接云涛连晓雾）》教学课件：逐句注释译文赏析、文言积累、全屏听写练习。">
<style>
%(css)s
</style>
</head>
<body>

  <header class="hero">
    <div class="hero-inner">
      <div class="hero-side">宋·李清照</div>
      <h1 class="hero-title">渔家傲</h1>
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
  <div class="kai">《渔家傲》</div>
  <div>李清照 · 宋 · 出自《漱玉词》</div>
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
