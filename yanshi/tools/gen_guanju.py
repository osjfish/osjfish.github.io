# -*- coding: utf-8 -*-
"""《关雎》课件生成器 —— 《诗经》首篇，复用《背影》CSS/JS框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'beiying-zhuziqing.html')
SRC = os.path.normpath(SRC)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'guanju-shijing.html')
OUT = os.path.normpath(OUT)

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'guanju_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


FULLTEXT = [
    "关关雎鸠，在河之洲。",
    "窈窕淑女，君子好逑。",
    "参差荇菜，左右流之。",
    "窈窕淑女，寤寐求之。",
    "求之不得，寤寐思服。",
    "悠哉悠哉，辗转反侧。",
    "参差荇菜，左右采之。",
    "窈窕淑女，琴瑟友之。",
    "参差荇菜，左右芼之。",
    "窈窕淑女，钟鼓乐之。",
]

PARTS = [
    ("第一章", "雎鸠起兴 · 君子好逑", "第 1–2 句",
     fixq("首章以~L~关关雎鸠，在河之洲~R~起兴，雎鸠鸟在河洲上和鸣，雌雄相依，引出~L~窈窕淑女，君子好逑~R~——文静美好的女子，是君子的好配偶。这是全诗的纲领，奠定了爱慕追求的基调。比兴手法的运用，使爱情的抒发自然而不突兀，情景交融，和谐优美。")),
    ("第二章", "荇菜流动 · 寤寐求之", "第 3–4 句",
     fixq("第二章以采摘荇菜起兴，~L~左右流之~R~写女子在船的左右两边求取荇菜，忙碌而优美的身影牵动了君子的心。~L~窈窕淑女，寤寐求之~R~，君子日日夜夜都想追求她。~L~寤寐~R~二字，写出思念之深——醒时想，睡时也想，无论白天黑夜，思念从未停止。")),
    ("第三章", "求之不得 · 辗转反侧", "第 5–6 句",
     fixq("第三章写追求的苦闷。~L~求之不得，寤寐思服~R~，追求不到，日日夜夜思念不已。~L~悠哉悠哉，辗转反侧~R~，思念绵绵不断，翻来覆去无法入睡。这一章是全诗情感最浓烈的部分，将单相思的苦闷写到极致，但哀而不伤，始终保持着温柔敦厚的格调。")),
    ("第四、五章", "琴瑟友之 · 钟鼓乐之", "第 7–10 句",
     fixq("第四、五章写幻想中的结合。仍以采摘荇菜起兴，~L~采之~~L~芼之~R~，由~L~流~R~而~L~采~R~而~L~芼~R~，动作递进，暗示感情的深化。~L~琴瑟友之~~L~钟鼓乐之~R~，弹琴鼓瑟亲近她，敲钟击鼓使她快乐——这是君子想象中与淑女结合后的欢乐场景，以热闹的音乐渲染喜庆的氛围，乐而不淫，圆满收束全诗。")),
]

S = [
(0, "[[关关|（guān guān）拟声词，雎鸠鸟的鸣叫声]][[雎鸠|（jū jiū）一种水鸟，传说雌雄情意专一]]，在河之[[洲|水中的陆地]]。",
 "雎鸠鸟关关地鸣叫，在那河中的小洲上。",
 fixq("开篇起兴。~L~关关~R~是拟声词，描摹雎鸠鸟的和鸣；~L~在河之洲~R~点明地点——河中的小洲。雎鸠鸟雌雄相依、和鸣而飞，古人认为这种鸟情意专一，以此起兴，自然引出下文君子对淑女的爱慕。以鸟鸣起兴，是《诗经》常用的手法，使爱情的抒发有了自然的依托，不突兀、不直白，含蓄而优美。"),
 ["起兴", "拟声", "开篇"]),

(0, "[[窈窕|（yǎo tiǎo）文静美好的样子]][[淑女|善良美好的女子。淑，善、美]]，[[君子|古代对贵族男子的通称，这里指青年男子]][[好逑|（hǎo qiú）好的配偶。逑，配偶]]。",
 "那文静美好的女子，正是君子的好配偶。",
 fixq("由兴入赋，点明主旨。~L~窈窕~R~写女子的外表文静美好，~L~淑~R~写女子的品德善良，内外兼修，是理想的配偶形象。~L~君子好逑~R~直接表明君子的心愿——要娶这样的女子为妻。这一句是全诗的纲领，以下各章都围绕~L~求之~R~展开。~L~好逑~R~的~L~好~R~读 hǎo，意为美好的，不是动词~L~喜爱~R~（hào），这是易错读音。"),
 ["主旨", "名句", "纲领"]),

(1, "[[参差|（cēn cī）长短不齐的样子]][[荇菜|（xìng cài）一种水生植物，嫩叶可食用]]，[[左右|向左向右，这里指在船的两边]][[流|求取，这里指采摘]]之。",
 "长短不齐的荇菜，在船的左右两边采摘。",
 fixq("第二章以采摘荇菜起兴。~L~参差~R~写荇菜长短不齐的样子，~L~左右流之~R~写女子在船的左右两边灵活地求取荇菜。一个~L~流~R~字，写出女子采摘动作的轻快优美，也暗示君子目光的追随——他的视线随着女子的身影左右移动。荇菜在水中飘摇不定，正如君子捉摸不定的心思，比兴贴切自然。"),
 ["起兴", "炼字", "重章叠句"]),

(1, "窈窕淑女，[[寤寐|（wù mèi）日日夜夜。寤，醒时；寐，睡时]][[求|追求]]之。",
 "那文静美好的女子，我日日夜夜都想追求她。",
 fixq("由兴入赋，直抒思念。~L~寤寐~R~二字是关键——寤是醒时，寐是睡时，无论白天黑夜，君子都在思念这位女子。~L~求之~R~的~L~求~R~，不是短暂的念头，而是持续的渴望。这一句与第一章~L~君子好逑~R~呼应，由~L~好逑~R~的心愿进入~L~求之~R~的行动，情感递进一层。"),
 ["直抒胸臆", "情感递进", "重章叠句"]),

(2, "求之不得，寤寐[[思服|思念。服，思念]]。",
 "追求却得不到，日日夜夜思念不已。",
 fixq("第三章写追求的苦闷。~L~求之不得~R~是转折——由~L~求之~R~的渴望到~L~不得~R~的失落，情感骤然沉落。~L~寤寐思服~R~与上章~L~寤寐求之~R~呼应，但~L~求~R~变成了~L~思~R~——追求无望，只能在思念中煎熬。~L~思服~R~的~L~服~R~也是思念的意思，二字同义复用，强调思念的深沉。"),
 ["转折", "情感深化", "重章叠句"]),

(2, "[[悠哉|思念绵绵不断的样子。悠，忧思]]悠哉，[[辗转反侧|翻来覆去不能入睡。辗转，转动身体；反侧，翻来覆去]]。",
 "思念绵绵不断啊，翻来覆去无法入睡。",
 fixq("这一句是全诗情感的高潮。~L~悠哉悠哉~R~用叠词，写出思念的绵长不绝——不是一阵一阵的，而是持续不断、无休无止。~L~辗转反侧~R~是动作描写，翻来覆去无法入睡，将无形的思念化为有形的动作，生动地写出了失眠之苦。这一章写相思之苦，但哀而不伤——没有怨恨，没有绝望，只是真挚的思念，保持了《诗经》温柔敦厚的格调。"),
 ["叠词", "动作描写", "名句", "哀而不伤"]),

(3, "参差荇菜，左右[[采|采摘]]之。",
 "长短不齐的荇菜，在船的左右两边采摘。",
 fixq("第四章仍以采摘荇菜起兴。与第二章~L~左右流之~R~相比，~L~流~R~变成了~L~采~R~——由求取到采摘，动作递进，暗示感情的发展。重章叠句是《诗经》的典型手法，通过更换个别字词，在反复咏唱中推进情感，使诗歌富有音乐性和节奏感。"),
 ["起兴", "重章叠句", "动作递进"]),

(3, "窈窕淑女，[[琴瑟|（qín sè）两种弦乐器，古人常以琴瑟比喻夫妻和谐]][[友|亲近，亲爱，这里作动词]]之。",
 "那文静美好的女子，我要弹琴鼓瑟亲近她。",
 fixq("由现实的苦闷转入幻想的欢乐。~L~琴瑟友之~R~写君子想象中与淑女相处的场景——弹琴鼓瑟，以音乐表达爱慕，亲近她。~L~琴瑟~R~在中国文化中象征夫妻和谐，~L~友~R~是亲近、亲爱的意思，作动词用。这一句写的是幻想中的亲密，不是现实的结合，为下一章~L~钟鼓乐之~R~的婚礼场景做铺垫。"),
 ["想象", "用典", "乐而不淫"]),

(3, "参差荇菜，左右[[芼|（mào）挑选]]之。",
 "长短不齐的荇菜，在船的左右两边挑选。",
 fixq("第五章仍以采摘荇菜起兴。~L~芼~R~是挑选的意思，比~L~采~R~更进一步——采摘之后还要精心挑选。~L~流→采→芼~R~三个动词的递进，暗示君子对淑女的感情由追求到亲近到珍视，层层深化。重章叠句的反复咏唱，使诗歌的音乐性达到极致。"),
 ["起兴", "重章叠句", "炼字", "动作递进"]),

(3, "窈窕淑女，[[钟鼓|钟和鼓，古代乐器，常用于喜庆场合]][[乐|（lè）使……快乐，使动用法]]之。",
 "那文静美好的女子，我要敲钟击鼓使她快乐。",
 fixq("末句以热闹的音乐收束全诗。~L~钟鼓乐之~R~写君子想象中婚礼的喜庆场景——敲钟击鼓，让新娘快乐。~L~乐~R~是使动用法，~L~使……快乐~R~。钟鼓是古代喜庆场合的乐器，与上章~L~琴瑟~R~的清雅相比，更加热闹隆重，暗示婚礼的盛大。全诗以~L~钟鼓乐之~R~圆满结束，乐而不淫——写欢乐但不过分，始终保持着庄重典雅的格调，是~L~乐而不淫，哀而不伤~R~的典范。"),
 ["想象", "使动用法", "名句", "乐而不淫", "卒章显志"]),
]


DICT_WORDS = [
    {"w":"雎","py":"jū","q":"关关□鸠，在河之洲","tip":fixq("「雎」隹字部，音 jū，雎鸠是水鸟名；勿写~L~睢~R~（suī，目字旁，恣睢）")},
    {"w":"鸠","py":"jiū","q":"关关雎□，在河之洲","tip":fixq("「鸠」鸟字旁，音 jiū，鸟类；勿写~L~鸩~R~（zhèn，毒酒）")},
    {"w":"窈","py":"yǎo","q":"□窕淑女，君子好逑","tip":fixq("「窈」穴字头，音 yǎo，窈窕形容文静美好；勿写~L~杳~R~（yǎo，杳无音信）")},
    {"w":"窕","py":"tiǎo","q":"窈□淑女，君子好逑","tip":fixq("「窕」穴字头，音 tiǎo，窈窕叠韵词；勿写~L~挑~R~（tiāo，挑选）")},
    {"w":"逑","py":"qiú","q":"窈窕淑女，君子好□","tip":fixq("「逑」走之底，音 qiú，配偶义；勿写~L~求~R~（请求），好逑即好配偶")},
    {"w":"参","py":"cēn","q":"□差荇菜，左右流之","tip":fixq("「参」此处音 cēn，参差形容长短不齐；多音字，又读 cān（参加）、shēn（人参）")},
    {"w":"差","py":"cī","q":"参□荇菜，左右流之","tip":fixq("「差」此处音 cī，参差叠韵词；多音字，又读 chà（差不多）、chā（差别）、chāi（出差）")},
    {"w":"荇","py":"xìng","q":"参差□菜，左右流之","tip":fixq("「荇」草字头，音 xìng，水生植物；勿写~L~行~R~（xíng，行走）")},
    {"w":"寤","py":"wù","q":"□寐求之","tip":fixq("「寤」宀字头，音 wù，睡醒；与~L~寐~R~（mèi，睡着）对举，勿写~L~悟~R~（领悟）")},
    {"w":"寐","py":"mèi","q":"寤□求之","tip":fixq("「寐」宀字头，音 mèi，睡着；勿写~L~味~R~（味道）、~L~魅~R~（魅力）")},
    {"w":"辗","py":"zhǎn","q":"□转反侧","tip":fixq("「辗」车字旁，音 zhǎn，辗转指转动身体；勿写~L~碾~R~（niǎn，碾压）")},
    {"w":"芼","py":"mào","q":"左右□之","tip":fixq("「芼」草字头，音 mào，挑选义；勿写~L~毛~R~（máo，毛发）、~L~笔~R~（bǐ）")},
    {"w":"瑟","py":"sè","q":"琴□友之","tip":fixq("「瑟」王字旁，音 sè，弦乐器；笔画多，上部为双~L~王~R~，勿写~L~琴~R~")},
    {"w":"洲","py":"zhōu","q":"在河之□","tip":fixq("「洲」三点水，音 zhōu，水中陆地；勿写~L~州~R~（zhōu，州县，无水旁）")},
]

DICT_NOTES = [
    {"w":"关关","a":"（guān guān）拟声词，雎鸠鸟的鸣叫声","q":"关关雎鸠，在河之洲"},
    {"w":"雎鸠","a":"（jū jiū）一种水鸟，传说雌雄情意专一","q":"关关雎鸠，在河之洲"},
    {"w":"洲","a":"水中的陆地","q":"在河之洲"},
    {"w":"窈窕","a":"（yǎo tiǎo）文静美好的样子","q":"窈窕淑女，君子好逑"},
    {"w":"淑女","a":"善良美好的女子。淑，善、美","q":"窈窕淑女，君子好逑"},
    {"w":"君子","a":"古代对贵族男子的通称，这里指青年男子","q":"窈窕淑女，君子好逑"},
    {"w":"好逑","a":"（hǎo qiú）好的配偶。逑，配偶","q":"君子好逑"},
    {"w":"参差","a":"（cēn cī）长短不齐的样子","q":"参差荇菜，左右流之"},
    {"w":"荇菜","a":"（xìng cài）一种水生植物，嫩叶可食用","q":"参差荇菜，左右流之"},
    {"w":"流","a":"求取，这里指采摘","q":"左右流之"},
    {"w":"寤寐","a":"（wù mèi）日日夜夜。寤，醒时；寐，睡时","q":"寤寐求之"},
    {"w":"思服","a":"思念。服，思念","q":"寤寐思服"},
    {"w":"悠哉","a":"思念绵绵不断的样子。悠，忧思","q":"悠哉悠哉"},
    {"w":"辗转反侧","a":"翻来覆去不能入睡。辗转，转动身体；反侧，翻来覆去","q":"辗转反侧"},
    {"w":"琴瑟","a":"（qín sè）两种弦乐器，古人常以琴瑟比喻夫妻和谐","q":"琴瑟友之"},
    {"w":"友","a":"亲近，亲爱，这里作动词","q":"琴瑟友之"},
    {"w":"芼","a":"（mào）挑选","q":"左右芼之"},
    {"w":"钟鼓","a":"钟和鼓，古代乐器，常用于喜庆场合","q":"钟鼓乐之"},
    {"w":"乐","a":"（lè）使……快乐，使动用法","q":"钟鼓乐之"},
    {"w":"比兴","a":"《诗经》表现手法。比，比喻；兴，先言他物以引起所咏之词","q":"关关雎鸠，在河之洲"},
    {"w":"重章叠句","a":"《诗经》表现手法，各章字句基本相同，只换少数词语，反复咏唱","q":"参差荇菜，左右流之"},
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
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 文体</span></div>
  <div class="lead">
    <p>《关雎》是《诗经》的第一篇，选自《诗经·周南》，是中国文学史上最著名的爱情诗之一。全诗以雎鸠和鸣起兴，描写一位青年男子对文静美好女子的爱慕、追求和幻想，情感真挚，格调高雅，被孔子誉为~L~乐而不淫，哀而不伤~R~。</p>
    <p>全诗五章二十句，采用《诗经》典型的重章叠句手法，以采摘荇菜为线索，通过~L~流→采→芼~R~三个动词的递进，展现情感的发展变化。比兴手法的运用，使爱情的抒发含蓄自然，是中国古典诗歌的典范之作。</p>
  </div>
  <div class="box">
    <h3>《诗经》简介</h3>
    <p>《诗经》是中国最早的一部诗歌总集，收录了从西周初年到春秋中叶（约公元前11世纪至公元前6世纪）的诗歌305篇，又称~L~诗三百~R~。相传由孔子编订，汉代以后被奉为儒家经典。</p>
    <p>《诗经》分为~L~风、雅、颂~R~三部分：~L~风~R~是各地的民歌，共160篇；~L~雅~R~是宫廷乐歌，分大雅、小雅，共105篇；~L~颂~R~是宗庙祭祀的乐歌，共40篇。《关雎》选自~L~国风·周南~R~，是~L~风~R~的第一篇，也是整部《诗经》的第一篇。</p>
    <p>《诗经》的表现手法有~L~赋、比、兴~R~三种：~L~赋~R~是直接陈述；~L~比~R~是比喻；~L~兴~R~是先言他物以引起所咏之词。《关雎》是比兴手法的典范。</p>
    <p class="note">※ 《诗经》与《尚书》《礼记》《周易》《春秋》并称~L~五经~R~，是中国传统文化的核心经典。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>周代社会：</b>《关雎》产生于西周时期，当时的婚姻制度虽已有~L~父母之命，媒妁之言~R~的规范，但民间自由恋爱的风气仍然存在。《诗经》中的~L~国风~R~部分，保存了大量民间情歌，反映了当时青年男女对美好爱情的追求。</p>
    <p><b>礼乐文化：</b>周代是礼乐文明的鼎盛时期，诗歌与音乐、舞蹈密不可分。《关雎》本是一首可以演唱的乐歌，~L~琴瑟友之~~L~钟鼓乐之~R~反映了当时贵族婚礼用乐的制度。孔子重视《关雎》，不仅因为它写爱情，更因为它体现了~L~乐而不淫，哀而不伤~R~的中庸之美，符合儒家的审美理想。</p>
    <p><b>周南地域：</b>~L~周南~R~指西周王畿以南的南方地区，包括今河南西南部及湖北北部一带。这里的民歌融合了中原文化与南方文化的特色，风格清新优美。</p>
  </div>
  <div class="box">
    <h3>文体知识</h3>
    <p>《关雎》是一首<b>四言诗</b>，每句四字，两句为一联，四句为一章，共五章二十句。四言诗是《诗经》的主要形式，节奏明快，富有音乐性。</p>
    <p><b>重章叠句：</b>全诗第二、四、五章都以~L~参差荇菜~R~开头，只更换~L~流→采→芼~R~和~L~求→友→乐~R~等个别词语，反复咏唱。这种手法使诗歌富有音乐性和节奏感，同时在反复中推进情感。</p>
    <p><b>比兴手法：</b>~L~关关雎鸠，在河之洲~R~是兴——以雎鸠鸟的和鸣引出君子对淑女的爱慕；~L~参差荇菜，左右流之~R~也是兴——以采摘荇菜的动作引出君子对淑女的追求。比兴使爱情的抒发含蓄自然，不直白、不突兀。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>《关雎》中华经典诵读大赛一等奖朗诵</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1CyWEzBEkd&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="关雎朗诵"></iframe>
        <a href="https://www.bilibili.com/video/BV1CyWEzBEkd" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>经典咏流传《关雎》仇海平演唱</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1xE411P7Qs&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="关雎歌曲"></iframe>
        <a href="https://www.bilibili.com/video/BV1xE411P7Qs" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句 · 主题</span></div>

  <div class="box">
    <h3>人物形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">淑女——文静美好的理想配偶</div>
        <p>诗中的~L~淑女~R~是一位内外兼修的理想女性形象。~L~窈窕~R~写她的外表文静美好，~L~淑~R~写她的品德善良。她在河边采摘荇菜，~L~左右流之~~L~左右采之~~L~左右芼之~R~，动作轻快优美，勤劳而质朴。她没有直接出场说话，但通过君子的视角和想象，塑造了一个完美的配偶形象——不仅外表美，更有品德美，是中国文学中~L~窈窕淑女~R~的典范。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">君子——真挚执着的追求者</div>
        <p>诗中的~L~君子~R~是一位真挚、执着、有教养的青年男子。他对淑女一见倾心，~L~寤寐求之~R~，日日夜夜思念；追求不到时~L~辗转反侧~R~，痛苦不堪；但他没有因此而怨恨或放弃，而是在幻想中~L~琴瑟友之~~L~钟鼓乐之~R~，以礼乐的方式表达爱慕。他的感情真挚而克制，热烈而不失分寸，是~L~乐而不淫，哀而不伤~R~的君子形象。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">比兴手法——先言他物，引起所咏</div>
        <p>《关雎》是比兴手法的典范。开篇~L~关关雎鸠，在河之洲~R~以雎鸠鸟的和鸣起兴，雎鸠雌雄相依、情意专一，自然引出君子对淑女的爱慕。第二、四、五章以~L~参差荇菜~R~起兴，采摘荇菜的动作与君子追求淑女的行为形成类比。比兴手法使爱情的抒发含蓄自然，不直白、不突兀，富有诗意和美感。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">重章叠句——反复咏唱，情感递进</div>
        <p>全诗五章，第二、四、五章结构相同，只更换个别词语：~L~流→采→芼~R~写采摘动作的递进，~L~求→友→乐~R~写情感的发展。重章叠句是《诗经》的典型手法，通过反复咏唱增强音乐性和节奏感，同时在词语的变换中推进情感，使诗歌一唱三叹，韵味无穷。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">乐而不淫，哀而不伤——中庸之美</div>
        <p>孔子评价《关雎》~L~乐而不淫，哀而不伤~R~。写欢乐（琴瑟友之、钟鼓乐之）但不过分，始终保持庄重典雅；写哀愁（求之不得、辗转反侧）但不绝望，没有怨恨和沉沦。这种情感的节制，体现了儒家的中庸之道和温柔敦厚的诗教传统，是中国古典诗歌的审美理想。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">关关雎鸠，在河之洲。窈窕淑女，君子好逑。</div>
        <p>这是《诗经》的开篇名句，也是中国文学史上最著名的起兴之一。以雎鸠鸟的和鸣起兴，引出君子对淑女的爱慕，情景交融，自然和谐。~L~窈窕淑女，君子好逑~R~点明全诗主旨，成为后世赞美理想配偶的经典表达。这四句奠定了全诗爱慕追求的基调，也确立了中国爱情诗~L~发乎情，止乎礼~R~的传统。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">求之不得，寤寐思服。悠哉悠哉，辗转反侧。</div>
        <p>这四句是全诗情感的高潮，写单相思的苦闷。~L~求之不得~R~是转折，由渴望到失落；~L~寤寐思服~R~写思念的深沉，日日夜夜；~L~悠哉悠哉~R~用叠词写思念的绵长不绝；~L~辗转反侧~R~以动作写失眠之苦，将无形的情感化为有形的动作。这四句写哀而不伤——没有怨恨，没有绝望，只是真挚的思念，是中国文学中写相思的经典名句。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《关雎》通过描写一位青年男子对文静美好女子的爱慕、追求和幻想，表达了对美好爱情和理想婚姻的向往与追求。</p>
    <p>这首诗的深刻之处在于，它不仅写了爱情的甜蜜与苦闷，更通过~L~乐而不淫，哀而不伤~R~的情感节制，体现了儒家的审美理想和诗教传统。爱情是人类最美好的情感之一，但需要以礼节制，发乎情而止乎礼。《关雎》作为《诗经》的第一篇，确立了中国爱情诗的基本范式——真挚、执着、克制、优雅，对后世文学产生了深远的影响。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 比兴 · 修辞 · 文化常识</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>文体与词牌</h3>
      <div class="acc-item"><span class="acc-w">《诗经》</span><span class="acc-d">中国最早的诗歌总集，收录西周至春秋诗歌305篇，分风、雅、颂三部分，表现手法为赋、比、兴。</span></div>
      <div class="acc-item"><span class="acc-w">国风·周南</span><span class="acc-d">~L~风~R~是各地民歌，共160篇；~L~周南~R~指西周王畿以南地区的民歌。《关雎》是~L~周南~R~的第一篇，也是《诗经》全书第一篇。</span></div>
      <div class="acc-item"><span class="acc-w">四言诗</span><span class="acc-d">每句四字的诗歌形式，是《诗经》的主要句式。两句为一联，四句为一章，节奏明快，富有音乐性。</span></div>
      <div class="acc-item"><span class="acc-w">重章叠句</span><span class="acc-d">《诗经》典型手法，各章字句基本相同，只换少数词语，反复咏唱，增强音乐性并推进情感。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>易错字音形</h3>
      <div class="acc-item"><span class="acc-w">雎鸠</span><span class="acc-d">（jū jiū）水鸟名。~L~雎~R~隹字部，勿写~L~睢~R~（suī）。</span></div>
      <div class="acc-item"><span class="acc-w">窈窕</span><span class="acc-d">（yǎo tiǎo）文静美好。叠韵词，均为穴字头，勿写~L~杳~R~~L~挑~R~。</span></div>
      <div class="acc-item"><span class="acc-w">好逑</span><span class="acc-d">（hǎo qiú）好的配偶。~L~好~R~读 hǎo（美好的），不读 hào；~L~逑~R~走之底，配偶义。</span></div>
      <div class="acc-item"><span class="acc-w">参差</span><span class="acc-d">（cēn cī）长短不齐。多音字：~L~参~R~又读 cān/shēn，~L~差~R~又读 chà/chā/chāi。</span></div>
      <div class="acc-item"><span class="acc-w">荇菜</span><span class="acc-d">（xìng cài）水生植物。~L~荇~R~草字头，勿写~L~行~R~。</span></div>
      <div class="acc-item"><span class="acc-w">寤寐</span><span class="acc-d">（wù mèi）日日夜夜。寤，醒时；寐，睡着。均为宀字头，勿写~L~悟~R~~L~味~R~。</span></div>
      <div class="acc-item"><span class="acc-w">芼</span><span class="acc-d">（mào）挑选。草字头，勿写~L~毛~R~~L~笔~R~。</span></div>
      <div class="acc-item"><span class="acc-w">乐</span><span class="acc-d">~L~钟鼓乐之~R~的~L~乐~R~读 lè，使动用法，使……快乐；不读 yuè（音乐）。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文言梳理</h3>
      <div class="acc-sub">古今异义</div>
      <div class="tw"><table>
        <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
        <tr><td class="kai">君子</td><td>贵族男子通称，这里指青年男子</td><td>品德高尚的人</td><td>君子好逑</td></tr>
        <tr><td class="kai">流</td><td>求取，采摘</td><td>流动、流传</td><td>左右流之</td></tr>
        <tr><td class="kai">友</td><td>亲近，亲爱（动词）</td><td>朋友（名词）</td><td>琴瑟友之</td></tr>
        <tr><td class="kai">服</td><td>思念</td><td>衣服、服从</td><td>寤寐思服</td></tr>
      </table></div>
      <div class="acc-sub">词类活用</div>
      <div class="tw"><table>
        <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
        <tr><td class="kai">友</td><td>名词作动词</td><td>亲近，亲爱</td><td>琴瑟友之</td></tr>
        <tr><td class="kai">乐</td><td>形容词使动用法</td><td>使……快乐</td><td>钟鼓乐之</td></tr>
      </table></div>
      <div class="acc-sub">一词多义</div>
      <div class="tw"><table>
        <tr><th>词</th><th>义项</th><th>例句</th></tr>
        <tr><td class="kai">之</td><td>代词，指荇菜/淑女</td><td>左右流之 / 寤寐求之</td></tr>
        <tr><td class="kai">之</td><td>结构助词，的</td><td>在河之洲</td></tr>
        <tr><td class="kai">好</td><td>hǎo，美好的</td><td>君子好逑</td></tr>
        <tr><td class="kai">乐</td><td>lè，使……快乐（使动）</td><td>钟鼓乐之</td></tr>
      </table></div>
      <div class="acc-sub">文言句式</div>
      <div class="tw"><table>
        <tr><th>句式</th><th>例句</th><th>说明</th></tr>
        <tr><td class="kai">省略句</td><td>（君子）寤寐求之</td><td>承前省略主语~L~君子~R~</td></tr>
        <tr><td class="kai">判断句</td><td>窈窕淑女，君子好逑</td><td>~L~淑女~R~是~L~君子好逑~R~，语义判断</td></tr>
      </table></div>
    </div>
  </div>

  <div class="box">
    <h3>比兴手法（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>兴——先言他物以引起所咏之词</dt><dd>~L~关关雎鸠，在河之洲~R~以雎鸠和鸣起兴，引出君子对淑女的爱慕；~L~参差荇菜，左右流之~R~以采摘荇菜起兴，引出君子对淑女的追求。兴的作用是渲染氛围、引发联想，使情感抒发自然含蓄。</dd></div>
      <div class="g-item"><dt>比——以此物比彼物</dt><dd>雎鸠鸟雌雄相依、情意专一，比喻君子与淑女的美好姻缘；采摘荇菜的动作比喻追求淑女的行为。比的作用是使抽象的情感具体化、形象化。</dd></div>
      <div class="g-item"><dt>比兴的区别与联系</dt><dd>~L~比~R~是比喻，有明确的本体和喻体；~L~兴~R~是起兴，先写他物再引出正题，两者关系较灵活。《关雎》中比兴往往交融使用，雎鸠和鸣既是兴也是比——既引出下文，也比喻美好姻缘。</dd></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞与手法</h3>
      <div class="acc-item"><span class="acc-w">重章叠句</span><span class="acc-d">第二、四、五章结构相同，换~L~流→采→芼~R~、~L~求→友→乐~R~，反复咏唱，推进情感。</span></div>
      <div class="acc-item"><span class="acc-w">叠词</span><span class="acc-d">~L~关关~R~（拟声）、~L~参差~R~（叠韵）、~L~悠哉悠哉~R~（反复），增强音乐性和形象性。</span></div>
      <div class="acc-item"><span class="acc-w">双声叠韵</span><span class="acc-d">~L~雎鸠~R~（jū jiū）叠韵，~L~窈窕~R~（yǎo tiǎo）叠韵，~L~参差~R~（cēn cī）双声，使诗句音韵和谐。</span></div>
      <div class="acc-item"><span class="acc-w">动作描写</span><span class="acc-d">~L~辗转反侧~R~以动作写失眠之苦，将无形的思念化为有形的动作。</span></div>
      <div class="acc-item"><span class="acc-w">虚实结合</span><span class="acc-d">前三章写实（追求与思念），后两章写虚（幻想中的结合），虚实相生。</span></div>
    </div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>诗三百</dt><dd>《诗经》共305篇，举其成数称~L~诗三百~R~。《论语·为政》：~L~诗三百，一言以蔽之，曰思无邪。~R~</dd></div>
      <div class="g-item"><dt>六义</dt><dd>《诗经》有~L~六义~R~：风、雅、颂（内容分类），赋、比、兴（表现手法）。这是研究《诗经》的基本概念。</dd></div>
      <div class="g-item"><dt>四始</dt><dd>《诗经》中~L~四始~R~指：《关雎》为《国风》之始，《鹿鸣》为《小雅》之始，《文王》为《大雅》之始，《清庙》为《颂》之始。《关雎》居首，地位特殊。</dd></div>
      <div class="g-item"><dt>乐而不淫，哀而不伤</dt><dd>孔子对《关雎》的评价，出自《论语·八佾》。意思是快乐而不放荡，哀愁而不悲伤，体现了儒家的中庸之美和温柔敦厚的诗教传统。</dd></div>
      <div class="g-item"><dt>琴瑟与钟鼓</dt><dd>琴瑟是弦乐器，音色清雅，常用于表达亲密之情；钟鼓是打击乐器，音色洪亮，常用于喜庆场合。~L~琴瑟友之~R~写亲密，~L~钟鼓乐之~R~写婚礼，由亲到庆，层层递进。</dd></div>
      <div class="g-item"><dt>荇菜</dt><dd>一种水生植物，嫩叶可食用，古代常用于祭祀。采摘荇菜是古代妇女的常见劳动，诗中以此起兴，富有生活气息。</dd></div>
    </div>
  </div>

</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《关雎》《诗经》</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">《诗经》</div>
  <h1 class="hero-title">关雎</h1>
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
  <div class="sec-sub">全诗五章二十句，分四部分解读。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《关雎》</div>
  <div>《诗经·周南》 · 中国最早诗歌总集第一篇 · 四言诗 · 比兴典范</div>
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
