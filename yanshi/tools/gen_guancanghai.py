# -*- coding: utf-8 -*-
"""《观沧海》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guancanghai-caocao.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'guancanghai_fs')
# Inject .acc-sub style (古诗词积累区文言梳理子表标题)
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


FULLTEXT = [
    "东临碣石，以观沧海。",
    "水何澹澹，山岛竦峙。",
    "树木丛生，百草丰茂。",
    "秋风萧瑟，洪波涌起。",
    "日月之行，若出其中；",
    "星汉灿烂，若出其里。",
    "幸甚至哉，歌以咏志。",
]

PARTS = [
    ("第一部分", "登临碣石 · 俯瞰沧海", "第 1–4 句",
     fixq("首二句点明登临的地点与目的——~L~东临碣石，以观沧海~R~，总领全篇。以下六句从全景到局部，从静到动，层层铺写沧海景象：~L~水何澹澹~R~写海面浩渺，~L~山岛竦峙~R~写岛屿挺拔，~L~树木丛生，百草丰茂~R~写岛上生机，~L~秋风萧瑟，洪波涌起~R~写海上波涛。四句由远及近、由静入动，写出了沧海的辽阔与壮美。")),
    ("第二部分", "吞吐日月 · 歌咏壮志", "第 5–7 句",
     fixq("~L~日月之行，若出其中；星汉灿烂，若出其里~R~，诗人以奇特的想象，写日月星辰仿佛都从沧海中升起运行，将沧海的广阔写到极致，也暗含诗人包容天地、一统天下的雄心壮志。末二句~L~幸甚至哉，歌以咏志~R~是乐府诗的合乐套语，直抒胸臆，点明全诗以歌咏志的主旨。")),
]

S = [
(0, "[[东|向东，名词作状语]]临[[碣石|（jié shí）山名，在今河北昌黎西北，秦始皇、汉武帝曾东巡至此刻石]]，以[[观|观看，观赏]]沧海。",
 "向东登上碣石山，来观赏苍茫的大海。",
 fixq("开篇点明登临的地点与目的。~L~东~R~字名词作状语，点明方向；~L~临~R~字写出登高俯瞰之势；~L~碣石~R~是历史名山，秦始皇、汉武帝都曾东巡至此刻石颂功，曹操登临此山，暗含追慕帝王功业之意。~L~以观沧海~R~的~L~观~R~字统摄全篇，以下所见之景皆由此~L~观~R~字展开。全诗以叙事起笔，平实而有力，为下文写景蓄势。"),
 ["起笔", "名词作状语", "统摄全篇"]),

(0, "水[[何|多么，副词]][[澹澹|（dàn dàn）水波荡漾的样子]]，[[山岛|海中的山岛]][[竦峙|（sǒng zhì）高高地挺立。竦，通~L~耸~R~，高；峙，挺立]]。",
 "海水多么宽阔浩荡，海中的山岛高高地挺立着。",
 fixq("写全景，先写海面，再写山岛。~L~何~R~字是~L~多么~R~的意思，表达诗人初见沧海时的惊叹之情。~L~澹澹~R~写水波荡漾、浩渺无边的样子，叠词增强了画面的动感。~L~竦峙~R~写山岛高高挺立，~L~竦~R~通~L~耸~R~，是高的意思；~L~峙~R~是挺立的意思。一动一静，一远一近，将沧海的辽阔与山岛的挺拔同时呈现，构图开阔而有层次。"),
 ["叠词", "通假字", "动静结合"]),

(0, "树木[[丛生|（cóng）密集地生长。丛，聚集]]，百草[[丰茂|（fēng mào）丰盛繁茂。丰，丰盛；茂，茂盛]]。",
 "树木密集地生长着，各种草儿长得丰盛繁茂。",
 fixq("镜头从海面拉到山岛，写岛上的近景。~L~树木丛生，百草丰茂~R~，虽然是秋天，但诗人看到的不是凋零衰败，而是草木繁茂、生机盎然。这与一般文人~L~悲秋~R~的传统不同，体现了曹操积极乐观的精神面貌。~L~丛生~R~写树木之密，~L~丰茂~R~写草木之盛，四字一顿，节奏明快，充满了生命的力量。"),
 ["近景", "反悲秋", "生机"]),

(0, "[[秋风|秋天的风]][[萧瑟|（xiāo sè）形容风吹树木的声音，也形容冷落凄凉]]，[[洪波|巨大的波涛。洪，大]]涌[[起|涌起，翻腾起来]]。",
 "秋风吹动树木发出萧瑟的声响，海上巨大的波涛汹涌翻腾。",
 fixq("由静转动，写海上的动态景象。~L~秋风萧瑟~R~写听觉，秋风穿过树林发出萧瑟之声；~L~洪波涌起~R~写视觉，巨大的波涛汹涌翻腾。虽然秋风萧瑟，但诗人笔下的沧海不是衰飒的，而是~L~洪波涌起~R~的壮阔——风越大，浪越高，沧海越显出它的雄浑力量。~L~涌~R~字写出波涛的力量感，仿佛能看到海浪冲天而起的景象。这一句将沧海的壮美写到了极致。"),
 ["动静结合", "炼字", "壮美"]),

(1, "[[日月|太阳和月亮]]之[[行|运行，运转]]，[[若|好像，如同]]出[[其中|它（沧海）的里面]]；",
 "太阳和月亮的运行，好像是从这沧海之中升起的；",
 fixq("由实写转入虚写，以奇特的想象写沧海的广阔。~L~日月之行，若出其中~R~，诗人不说沧海有多大，而是说连日月的运行都好像是从沧海之中出发的——沧海之大，竟能包容日月！~L~若~R~字是~L~好像~R~的意思，表明这是诗人的想象，而非实景，但正是这种想象，将沧海的广阔写到了极致。这一句不仅是写景，更是诗人胸襟的写照——能包容日月的沧海，正是诗人包容天下的雄心的象征。"),
 ["想象", "虚写", "胸襟"]),

(1, "[[星汉|（xīng hàn）银河，天河。星，星辰；汉，天河]]灿烂，若出[[其里|它（沧海）的里面。里，里面、内部]]。",
 "银河星光灿烂，好像是从这沧海之中涌现出来的。",
 fixq("承上句，继续以想象写沧海之大。~L~星汉~R~即银河，~L~灿烂~R~写星光闪烁耀眼的样子。如果说~L~日月之行~R~写的是白昼，那么~L~星汉灿烂~R~写的就是夜晚——无论白昼还是黑夜，无论日月还是星辰，仿佛都从沧海中生出。四句~L~日月之行，若出其中；星汉灿烂，若出其里~R~，以互文见义的手法，将沧海的广阔无垠写到了极致，也暗含了诗人吞吐天地、囊括宇宙的雄心壮志。这是全诗的高潮，也是千古传诵的名句。"),
 ["互文", "想象", "名句", "壮志"]),

(1, "[[幸甚至哉|（xìng shèn zhì zāi）庆幸得很，好极了。幸，庆幸；甚，很、极；至，到了极点；哉，语气词，表感叹]]，[[歌以咏志|用诗歌来抒发志向。歌，写诗、歌唱；以，用来；咏，抒发；志，志向]]。",
 "庆幸得很，好极了，让我用诗歌来抒发心中的志向吧。",
 fixq("末二句是乐府诗的合乐套语，在《步出夏门行》各章末尾都有，但在此处并非可有可无。~L~幸甚至哉~R~直抒诗人登临碣石、俯瞰沧海后的欣喜与豪迈；~L~歌以咏志~R~点明全诗以歌咏志的主旨——曹操歌咏的不是沧海本身，而是借沧海的辽阔壮美，抒发自己一统天下、建功立业的雄心壮志。这一句与全诗的写景浑然一体，景中有志，志因景显，余味悠长。"),
 ["合乐套语", "直抒胸臆", "咏志"]),
]


DICT_WORDS = [
    {"w":"碣","py":"jié","q":"东临□石，以观沧海。","tip":fixq("「碣」石字旁，音 jié，碣石山，勿写~L~竭~R~（竭力）~L~揭~R~（揭开）")},
    {"w":"澹澹","py":"dàn dàn","q":"水何□□，山岛竦峙。","tip":fixq("「澹」三点水，音 dàn，~L~澹澹~R~形容水波荡漾，叠词，勿写~L~淡~R~（冷淡）")},
    {"w":"竦","py":"sǒng","q":"水何澹澹，山岛□峙。","tip":fixq("「竦」立字旁，音 sǒng，通~L~耸~R~，高，~L~竦峙~R~即高高挺立，勿写~L~耸~R~~L~悚~R~（害怕）")},
    {"w":"峙","py":"zhì","q":"水何澹澹，山岛竦□。","tip":fixq("「峙」山字旁，音 zhì，挺立、屹立，~L~竦峙~R~即高高挺立，勿写~L~侍~R~（侍奉）~L~待~R~")},
    {"w":"萧","py":"xiāo","q":"秋风□瑟，洪波涌起。","tip":fixq("「萧」草字头，音 xiāo，~L~萧瑟~R~形容风声，勿写~L~箫~R~（竹箫，竹字头）~L~啸~R~")},
    {"w":"瑟","py":"sè","q":"秋风萧□，洪波涌起。","tip":fixq("「瑟」王字旁（玉），音 sè，~L~萧瑟~R~形容风吹树木声，勿写~L~琵~R~~L~琴~R~")},
    {"w":"涌","py":"yǒng","q":"秋风萧瑟，洪波□起。","tip":fixq("「涌」三点水，音 yǒng，水或云气冒出、翻腾，~L~涌起~R~即汹涌而起，勿写~L~勇~R~（勇敢）")},
    {"w":"灿","py":"càn","q":"星汉□烂，若出其里。","tip":fixq("「灿」火字旁，音 càn，光彩鲜明耀眼，~L~灿烂~R~，勿写~L~璨~R~（美玉，王字旁）")},
    {"w":"烂","py":"làn","q":"星汉灿□，若出其里。","tip":fixq("「烂」火字旁，音 làn，光彩鲜明，~L~灿烂~R~，勿写~L~栏~R~（栏杆）~L~拦~R~")},
    {"w":"哉","py":"zāi","q":"幸甚至□，歌以咏志。","tip":fixq("「哉」口字旁，音 zāi，语气词表感叹，~L~幸甚至哉~R~，勿写~L~栽~R~（栽种）~L~裁~R~（裁剪）")},
    {"w":"咏","py":"yǒng","q":"幸甚至哉，歌以□志。","tip":fixq("「咏」口字旁，音 yǒng，用诗词等来叙述、抒发，~L~咏志~R~即抒发志向，勿写~L~泳~R~（游泳，三点水）")},
    {"w":"茂","py":"mào","q":"树木丛生，百草丰□。","tip":fixq("「茂」草字头，音 mào，茂盛、繁盛，~L~丰茂~R~即丰盛繁茂，勿写~L~贸~R~（贸易）")},
    {"w":"丛","py":"cóng","q":"树木□生，百草丰茂。","tip":fixq("「丛」一字底，音 cóng，聚集、许多事物凑在一起，~L~丛生~R~即密集生长，勿写~L~从~R~（从前）")},
]

DICT_NOTES = [
    {"w":"东","q":"东临碣石","a":"向东，名词作状语"},
    {"w":"临","q":"东临碣石","a":"登上，到达（高处）"},
    {"w":"碣石","q":"东临碣石","a":"山名，在今河北昌黎西北，秦始皇、汉武帝曾东巡至此刻石"},
    {"w":"以","q":"以观沧海","a":"连词，来，用来"},
    {"w":"何","q":"水何澹澹","a":"多么，副词，表感叹"},
    {"w":"澹澹","q":"水何澹澹","a":"（dàn dàn）水波荡漾的样子"},
    {"w":"竦峙","q":"山岛竦峙","a":"（sǒng zhì）高高地挺立。竦，通~L~耸~R~，高；峙，挺立"},
    {"w":"丛生","q":"树木丛生","a":"密集地生长。丛，聚集"},
    {"w":"丰茂","q":"百草丰茂","a":"（fēng mào）丰盛繁茂。丰，丰盛；茂，茂盛"},
    {"w":"萧瑟","q":"秋风萧瑟","a":"（xiāo sè）形容风吹树木的声音"},
    {"w":"洪波","q":"洪波涌起","a":"巨大的波涛。洪，大"},
    {"w":"涌","q":"洪波涌起","a":"水或云气冒出、翻腾"},
    {"w":"行","q":"日月之行","a":"运行，运转"},
    {"w":"若","q":"若出其中","a":"好像，如同，表比喻或想象"},
    {"w":"其中","q":"若出其中","a":"它（沧海）的里面。其，代词，指沧海"},
    {"w":"星汉","q":"星汉灿烂","a":"（xīng hàn）银河，天河。星，星辰；汉，天河"},
    {"w":"灿烂","q":"星汉灿烂","a":"光彩鲜明耀眼的样子"},
    {"w":"其里","q":"若出其里","a":"它（沧海）的里面。里，里面、内部"},
    {"w":"幸甚至哉","q":"幸甚至哉","a":"庆幸得很，好极了。幸，庆幸；甚，很；至，极点；哉，语气词"},
    {"w":"歌以咏志","q":"歌以咏志","a":"用诗歌来抒发志向。歌，写诗；以，用来；咏，抒发；志，志向"},
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
    <p>《观沧海》是东汉末年政治家、军事家、文学家曹操的名篇，作于建安十二年（207）北征乌桓凯旋途中。当时曹操大破乌桓，统一了北方，回师途经碣石山，登高望海，被沧海的辽阔壮美所震撼，写下了这首中国文学史上第一首完整的山水诗。</p>
    <p>全诗以~L~观~R~字统摄，由近及远、由实入虚，先写沧海全景与山岛草木，再写秋风洪波，最后以~L~日月之行，若出其中；星汉灿烂，若出其里~R~的奇特想象，将沧海的广阔写到极致，也抒发了诗人包容天地、一统天下的雄心壮志。这首诗是建安文学的代表作，也是曹操诗歌~L~苍凉慷慨、气势雄浑~R~风格的集中体现。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>曹操（155—220），字孟德，沛国谯县（今安徽亳州）人。东汉末年杰出的政治家、军事家、文学家，三国中曹魏政权的奠基人。曾任丞相，封魏王，其子曹丕称帝后追尊为魏武帝。</p>
    <p>曹操是建安文学的开创者和领袖，与其子曹丕、曹植并称~L~三曹~R~。他的诗歌继承了汉乐府民歌的现实主义传统，内容充实，感情真挚，风格苍凉慷慨、气势雄浑，代表作有《观沧海》《龟虽寿》《短歌行》《蒿里行》等。鲁迅称曹操为~L~改造文章的祖师~R~。</p>
    <p class="note">※ 曹操不仅是政治军事领袖，更是建安文学的核心人物。他的诗歌以乐府旧题写时事，开创了建安文学~L~建安风骨~R~的新局面。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>北征乌桓：</b>建安十二年（207），曹操为消灭袁绍残余势力、统一北方，亲率大军北征乌桓（当时北方的少数民族政权）。大军出卢龙塞，大破乌桓于白狼山，斩蹋顿单于，取得决定性胜利。回师途中，曹操登临碣石山，写下了《观沧海》。</p>
    <p><b>建安风骨：</b>建安是汉献帝的年号（196—220），这一时期的文学作品反映了社会动乱和人民疾苦，表达了建功立业的理想，风格慷慨悲凉、刚健有力，被后世称为~L~建安风骨~R~。曹操是建安文学的领袖，《观沧海》正是建安风骨的典范之作。</p>
    <p><b>碣石情结：</b>碣石山是历史名山，秦始皇、汉武帝都曾东巡至此刻石颂功。曹操登临碣石，不仅是观赏海景，更是在追慕前代帝王的功业，表达自己一统天下的抱负。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《观沧海》是一首<b>四言乐府诗</b>，选自《步出夏门行》组诗的第一章。《步出夏门行》是汉乐府旧题，曹操用旧题写新内容，共四章：《观沧海》《冬十月》《土不同》《龟虽寿》。全诗每句四字，两句一韵，节奏明快，气势雄浑。</p>
    <p>《观沧海》是中国文学史上第一首完整的山水诗。在此之前，《诗经》《楚辞》中的写景多为比兴的附庸，而曹操第一次把山水作为独立的审美对象来描写，开创了山水诗的先河。末二句~L~幸甚至哉，歌以咏志~R~是乐府诗的合乐套语，在组诗各章末尾都有。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>赵岭朗诵曹操《观沧海》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1BV411d7Lw&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="赵岭朗诵曹操《观沧海》"></iframe>
        <a href="https://www.bilibili.com/video/BV1BV411d7Lw" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>经典咏流传《观沧海》吉克隽逸演唱</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1JE411P7a8&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="经典咏流传《观沧海》"></iframe>
        <a href="https://www.bilibili.com/video/BV1JE411P7a8" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">曹操——吞吐天地的政治家与诗人</div>
        <p>《观沧海》中的抒情主人公，是一位胸怀天下、气势雄浑的政治家兼诗人形象。他站在碣石山顶，俯瞰苍茫大海，心中充满了胜利的喜悦和一统天下的豪情。</p>
        <p><b>登高望远的视野：</b>~L~东临碣石，以观沧海~R~，诗人登高临海，视野开阔。他看到的不是一池一丘，而是整个沧海——水何澹澹、山岛竦峙、洪波涌起，这种宏大的视野，正是政治家的视野。</p>
        <p><b>包容宇宙的胸襟：</b>~L~日月之行，若出其中；星汉灿烂，若出其里~R~，诗人想象日月星辰都从沧海中升起运行，这种吞吐天地的想象，正是诗人包容宇宙的胸襟的写照。沧海有多大，诗人的胸襟就有多大。</p>
        <p><b>积极乐观的精神：</b>面对~L~秋风萧瑟~R~，诗人没有悲秋伤怀，而是看到~L~洪波涌起~R~的壮美和~L~百草丰茂~R~的生机。这种积极乐观的精神，与曹操作为政治家的自信和进取密不可分。这个形象，是建安风骨的人格化身。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">虚实结合，由实入虚</div>
        <p>全诗前六句（~L~水何澹澹~R~到~L~洪波涌起~R~）是实写，写诗人亲眼所见的沧海景象：海面浩渺、山岛挺拔、草木繁茂、波涛汹涌。后四句（~L~日月之行~R~到~L~若出其里~R~）是虚写，写诗人的想象——日月星辰仿佛都从沧海中升起运行。由实入虚，由眼前之景到心中之境，使诗歌的境界从对沧海的描写拓展到对宇宙的包容，意境更加深远。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">动静结合，由静入动</div>
        <p>~L~水何澹澹，山岛竦峙~R~是静景，写海面的浩渺和山岛的挺拔；~L~树木丛生，百草丰茂~R~也是静景，写岛上的生机；~L~秋风萧瑟，洪波涌起~R~则转为动景，写海上的波涛汹涌。由静入动，先写沧海的宁静辽阔，再写沧海的雄浑力量，动静相生，将沧海的形神写尽。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">情景交融，景中有志</div>
        <p>全诗没有一句直接抒情，但句句都含情言志。沧海的辽阔壮美，正是诗人胸襟的写照；~L~日月之行，若出其中~R~的想象，正是诗人一统天下的雄心的象征。这种~L~景中有志，志因景显~R~的手法，使全诗既具有山水诗的审美价值，又具有言志诗的思想深度，是中国古典诗歌情景交融的典范。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">日月之行，若出其中；星汉灿烂，若出其里。</div>
        <p>这是全诗的高潮，也是千古传诵的名句。诗人以奇特的想象，写日月的运行好像从沧海之中出发，银河的灿烂好像从沧海之中涌现。四句互文见义，无论白昼还是黑夜，无论日月还是星辰，仿佛都从沧海中生出。这不仅写出了沧海的广阔无垠，更暗含了诗人吞吐天地、囊括宇宙的雄心壮志。~L~若~R~字表明这是想象而非实景，但正是这种想象，将沧海的大写到了极致，也将诗人的胸襟写到了极致。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">秋风萧瑟，洪波涌起。</div>
        <p>这两句写沧海的动态美。~L~秋风萧瑟~R~写听觉，秋风穿过树林发出萧瑟之声；~L~洪波涌起~R~写视觉，巨大的波涛汹涌翻腾。一般文人面对秋风多生悲秋之情，但曹操笔下的秋风却带来了~L~洪波涌起~R~的壮美——风越大，浪越高，沧海越显出它的雄浑力量。~L~涌~R~字写出波涛的力量感，仿佛能看到海浪冲天而起的景象。这两句体现了曹操积极乐观的精神和建安文学~L~苍凉慷慨~R~的风格。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《观沧海》通过描写沧海的辽阔壮美，抒发了诗人包容天地、一统天下的雄心壮志，表达了积极进取、乐观自信的人生态度和建功立业的政治抱负。</p>
    <p>这首诗的深刻之处在于，它不仅是一首山水诗，更是一首言志诗。诗人以~L~观沧海~R~为题，却不止于写海——沧海的辽阔壮美，正是诗人心中崇高理想的象征；~L~日月之行，若出其中~R~的想象，正是诗人对一统天下的追求。这首诗写于曹操北征乌桓凯旋途中，是他一生政治军事生涯的高光时刻，诗中的豪情壮志，正是胜利者的自信和政治家的抱负的真实流露。千百年来，这首诗以其雄浑的气势和开阔的意境，激励着无数人胸怀天下、锐意进取。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 炼字 · 修辞 · 文化常识</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>文体与词牌</h3>
      <div class="acc-item"><span class="acc-w">四言乐府诗</span><span class="acc-d">《观沧海》是四言乐府诗，选自《步出夏门行》组诗第一章。每句四字，两句一韵，节奏明快，气势雄浑。</span></div>
      <div class="acc-item"><span class="acc-w">《步出夏门行》</span><span class="acc-d">汉乐府旧题，曹操用旧题写新内容，共四章：《观沧海》《冬十月》《土不同》《龟虽寿》。末二句~L~幸甚至哉，歌以咏志~R~是合乐套语，各章末尾都有。</span></div>
      <div class="acc-item"><span class="acc-w">山水诗先河</span><span class="acc-d">《观沧海》是中国文学史上第一首完整的山水诗，第一次把山水作为独立的审美对象来描写，开创了山水诗的先河。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>易错字音形</h3>
      <div class="acc-item"><span class="acc-w">碣石</span><span class="acc-d">（jié shí）山名，~L~碣~R~石字旁，勿写~L~竭~R~~L~揭~R~。</span></div>
      <div class="acc-item"><span class="acc-w">澹澹</span><span class="acc-d">（dàn dàn）水波荡漾，~L~澹~R~三点水，勿写~L~淡~R~。</span></div>
      <div class="acc-item"><span class="acc-w">竦峙</span><span class="acc-d">（sǒng zhì）高高挺立，~L~竦~R~通~L~耸~R~，~L~峙~R~山字旁，勿写~L~侍~R~。</span></div>
      <div class="acc-item"><span class="acc-w">萧瑟</span><span class="acc-d">（xiāo sè）风声，~L~萧~R~草字头，~L~瑟~R~王字旁，勿写~L~箫~R~（竹字头）。</span></div>
      <div class="acc-item"><span class="acc-w">哉</span><span class="acc-d">（zāi）语气词，口字旁，勿写~L~栽~R~~L~裁~R~。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文言梳理</h3>
      <div class="acc-sub">通假字</div>
      <div class="tw"><table>
        <tr><th>字</th><th>通假</th><th>例句</th><th>释义</th></tr>
        <tr><td class="kai">竦</td><td>通~L~耸~R~</td><td>山岛竦峙</td><td>高。读 sǒng</td></tr>
      </table></div>
      <div class="acc-sub">古今异义</div>
      <div class="tw"><table>
        <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
        <tr><td class="kai">何</td><td>多么，副词，表感叹</td><td>什么，疑问代词</td><td>水何澹澹</td></tr>
        <tr><td class="kai">若</td><td>好像，如同</td><td>如果（连词）、你（代词）</td><td>若出其中</td></tr>
        <tr><td class="kai">歌</td><td>写诗、歌唱（动词）</td><td>歌曲（名词）</td><td>歌以咏志</td></tr>
        <tr><td class="kai">志</td><td>志向、抱负</td><td>志向、记号（多义）</td><td>歌以咏志</td></tr>
      </table></div>
      <div class="acc-sub">词类活用</div>
      <div class="tw"><table>
        <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
        <tr><td class="kai">东</td><td>名词作状语</td><td>向东</td><td>东临碣石</td></tr>
      </table></div>
      <div class="acc-sub">文言句式</div>
      <div class="tw"><table>
        <tr><th>句式</th><th>例句</th><th>说明</th></tr>
        <tr><td class="kai">省略句</td><td>（吾）东临碣石</td><td>承前省略主语~L~吾~R~（我）</td></tr>
        <tr><td class="kai">互文</td><td>日月之行，若出其中；星汉灿烂，若出其里</td><td>日月星汉的运行灿烂，都若出其中/其里</td></tr>
      </table></div>
    </div>
  </div>

  <div class="box">
    <h3>炼字赏析（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>观——以观沧海</dt><dd>~L~观~R~字统摄全篇，以下所见之景皆由此~L~观~R~字展开。一个~L~观~R~字，既写出了诗人登高俯瞰的姿态，也奠定了全诗宏大的叙事视角。</dd></div>
      <div class="g-item"><dt>何——水何澹澹</dt><dd>~L~何~R~是~L~多么~R~的意思，副词，表感叹。一个~L~何~R~字，写出了诗人初见沧海时的惊叹之情，使平淡的叙述带上了强烈的感情色彩。</dd></div>
      <div class="g-item"><dt>涌——洪波涌起</dt><dd>~L~涌~R~字写出波涛的力量感，仿佛能看到海浪冲天而起的景象。一个~L~涌~R~字，将沧海的雄浑力量写得惊心动魄，化静为动，气势磅礴。</dd></div>
      <div class="g-item"><dt>若——若出其中</dt><dd>~L~若~R~是~L~好像~R~的意思，表明这是诗人的想象而非实景。一个~L~若~R~字，将实写与虚写连接起来，使想象显得真实可信，也留出了审美的空间。</dd></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞与手法</h3>
      <div class="acc-item"><span class="acc-w">互文</span><span class="acc-d">~L~日月之行，若出其中；星汉灿烂，若出其里~R~——日月星汉的运行灿烂，都仿佛从沧海中生出。</span></div>
      <div class="acc-item"><span class="acc-w">想象（虚写）</span><span class="acc-d">日月星辰从沧海中升起，以奇特想象写沧海之大。</span></div>
      <div class="acc-item"><span class="acc-w">动静结合</span><span class="acc-d">~L~水何澹澹，山岛竦峙~R~静景，~L~秋风萧瑟，洪波涌起~R~动景。</span></div>
      <div class="acc-item"><span class="acc-w">情景交融</span><span class="acc-d">沧海的辽阔壮美正是诗人胸襟的写照，景中有志，志因景显。</span></div>
      <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">~L~日月之行，若出其中~R~，极言沧海之大，能包容日月星辰。</span></div>
    </div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>碣石</dt><dd>山名，在今河北昌黎西北。秦始皇、汉武帝都曾东巡至此刻石颂功。曹操登临碣石，暗含追慕帝王功业之意。</dd></div>
      <div class="g-item"><dt>乌桓</dt><dd>中国古代北方少数民族之一，亦作~L~乌丸~R~。建安十二年（207），曹操北征乌桓，大破之于白狼山，统一了北方。</dd></div>
      <div class="g-item"><dt>建安风骨</dt><dd>建安时期（196—220）的文学风格，作品反映社会动乱和人民疾苦，表达建功立业的理想，风格慷慨悲凉、刚健有力。曹操是建安文学的领袖。</dd></div>
      <div class="g-item"><dt>三曹</dt><dd>指曹操与其子曹丕、曹植，他们是建安文学的核心人物，文学史上并称~L~三曹~R~。曹操诗风苍凉雄浑，曹丕诗风清丽婉约，曹植诗风骨气奇高。</dd></div>
      <div class="g-item"><dt>乐府诗</dt><dd>汉武帝时设立的音乐机构~L~乐府~R~所采集的诗歌，后来成为一种诗歌体裁。乐府诗可以配乐歌唱，句式灵活，多反映社会现实。曹操用乐府旧题写新内容，是建安文学的重要特色。</dd></div>
      <div class="g-item"><dt>四言诗</dt><dd>每句四字的诗歌体裁，是中国古代最早的诗歌形式之一，《诗经》即为四言诗的代表。汉代以后四言诗渐衰，曹操的四言诗是四言诗的最后一座高峰。</dd></div>
      <div class="g-item"><dt>星汉</dt><dd>指银河、天河。~L~星~R~是星辰，~L~汉~R~是天河。~L~星汉灿烂~R~即银河星光灿烂。古人认为银河是天上的河流，与地上的沧海相对应。</dd></div>
    </div>
  </div>

</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《观沧海》曹操</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">东汉 · 曹操</div>
  <h1 class="hero-title">观沧海</h1>
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
  <div class="sec-sub">全诗七句（含合乐套语），分两部分：登临写景、想象咏志。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《观沧海》</div>
  <div>曹操 · 东汉（155—220）· 建安十二年北征乌桓凯旋途中作 · 四言乐府诗</div>
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
