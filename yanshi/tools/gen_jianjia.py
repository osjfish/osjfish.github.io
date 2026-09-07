# -*- coding: utf-8 -*-
"""《蒹葭》课件生成器 —— 《诗经·秦风》，复用《背影》CSS/JS框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'beiying-zhuziqing.html'))
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'jianjia-shijing.html'))

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
CSS += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'jianjia_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


FULLTEXT = [
    "蒹葭苍苍，白露为霜。",
    "所谓伊人，在水一方。",
    "溯洄从之，道阻且长。",
    "溯游从之，宛在水中央。",
    "蒹葭萋萋，白露未晞。",
    "所谓伊人，在水之湄。",
    "溯洄从之，道阻且跻。",
    "溯游从之，宛在水中坻。",
    "蒹葭采采，白露未已。",
    "所谓伊人，在水之涘。",
    "溯洄从之，道阻且右。",
    "溯游从之，宛在水中沚。",
]

PARTS = [
    ("第一章", "苍苍为霜 · 宛在中央", "第 1–4 句",
     fixq("首章以~L~蒹葭苍苍，白露为霜~R~起兴，深秋清晨，芦苇苍苍，白露凝霜，营造出朦胧凄清的氛围。~L~所谓伊人，在水一方~R~点出所思念的人在水的那一方，可望而不可即。逆流而上，道路险阻又漫长；顺流而下，仿佛又在水的中央。全诗的朦胧意境和执着追求，在首章中已经奠定。")),
    ("第二章", "萋萋未晞 · 宛在中坻", "第 5–8 句",
     fixq("第二章与首章结构相同，只换少数词语：~L~苍苍~R~变~L~萋萋~R~，~L~为霜~R~变~L~未晞~R~，~L~一方~R~变~L~之湄~R~，~L~且长~R~变~L~且跻~R~，~L~中央~R~变~L~中坻~R~。露水由~L~为霜~R~到~L~未晞~R~，时间在推移；道路由~L~长~R~到~L~跻~R~（险峻），追寻越来越艰难。重章叠句中，情感在递进。")),
    ("第三章", "采采未已 · 宛在中沚", "第 9–12 句",
     fixq("第三章继续重章叠句：~L~萋萋~R~变~L~采采~R~，~L~未晞~R~变~L~未已~R~，~L~之湄~R~变~L~之涘~R~，~L~且跻~R~变~L~且右~R~（迂回），~L~中坻~R~变~L~中沚~R~。三章反复咏叹，伊人始终在水一方，若隐若现，可望而不可即。这种朦胧的意境和执着的追求，使《蒹葭》成为中国文学中最著名的朦胧诗，~L~秋水伊人~R~也成为千古流传的美好意象。")),
]

S = [
(0, "[[蒹葭|（jiān jiā）芦苇。蒹，荻；葭，芦苇]][[苍苍|茂盛的样子]]，[[白露|清晨的露水]][[为霜|凝结成霜。为，成为]]。",
 "芦苇苍苍茂盛，清晨的露水凝结成霜。",
 fixq("开篇起兴，营造朦胧凄清的意境。~L~蒹葭苍苍~R~写芦苇的茂盛，~L~白露为霜~R~写露水凝霜，点明时节是深秋，时间是清晨。芦苇、白露、秋霜，三个意象构成了一幅苍茫凄清的秋水图。~L~苍苍~R~是叠词，不仅写芦苇的茂盛，也渲染出苍茫辽远的氛围。深秋清晨的萧瑟景象，为下文~L~伊人~R~的可望不可即做了充分的氛围铺垫。"),
 ["起兴", "叠词", "意境", "开篇"]),

(0, "[[所谓|所说的，这里指所怀念的]][[伊人|那个人，指所爱的人。伊，那]]，在水[[一方|那一边。方，边、旁]]。",
 "我所思念的那个人，在水的那一边。",
 fixq("由景入情，点出全诗核心。~L~所谓伊人~R~的~L~所谓~R~，是~L~所说的~R~之意，这里指心中所怀念的；~L~伊人~R~即~L~那个人~R~，是诗人思念追寻的对象。~L~在水一方~R~写伊人在水的另一边，被河水阻隔，可望而不可即。一个~L~在~R~字，写出了距离的遥远和追寻的艰难。伊人是谁？是恋人、是友人、还是理想？诗人没有明说，这种模糊性正是本诗朦胧美的来源。"),
 ["点题", "朦胧美", "名句", "伊人形象"]),

(0, "[[溯洄|（sù huí）逆流而上。溯，逆流；洄，曲折的水道]][[从|追寻、跟随]]之，道[[阻|险阻]]且[[长|漫长]]。",
 "逆流而上去追寻她，道路险阻又漫长。",
 fixq("写追寻的艰难。~L~溯洄从之~R~是逆流而上追寻伊人，~L~道阻且长~R~写道路的险阻和漫长。~L~阻~R~写道路的艰难，~L~长~R~写距离的遥远。一个~L~且~R~字，将~L~阻~R~和~L~长~R~连接起来，强调追寻的双重困难。但诗人没有因为道路艰难而放弃，逆流而上的行动本身，就体现了执着的追求精神。"),
 ["动作描写", "执着追求", "重章叠句"]),

(0, "[[溯游|顺流而下。溯，沿着；游，水流]][[从|追寻、跟随]]之，[[宛|仿佛、好像]]在水[[中央|中间]]。",
 "顺流而下去追寻她，仿佛又在水的中央。",
 fixq("~L~溯游从之~R~是顺流而下追寻，~L~宛在水中央~R~写伊人仿佛在水的中央。~L~宛~R~字是关键——~L~仿佛~R~~L~好像~R~，伊人若隐若现，似有似无。逆流而上找不到，顺流而下也只是~L~宛在~R~，伊人始终是朦胧的、不可触及的。这种~L~宛在~R~的写法，营造出如梦如幻的朦胧意境，也是~L~秋水伊人~R~意象的核心。"),
 ["朦胧美", "炼字", "名句", "重章叠句"]),

(1, "蒹葭[[萋萋|（qī qī）茂盛的样子]]，白露[[未晞|未干。晞（xī），干]]。",
 "芦苇萋萋茂盛，清晨的露水还未干。",
 fixq("第二章起兴，与首章~L~蒹葭苍苍，白露为霜~R~形成重章叠句。~L~苍苍~R~变~L~萋萋~R~，同样写芦苇茂盛，但词语的变换避免了单调；~L~为霜~R~变~L~未晞~R~，露水由凝结成霜到还未干，暗示时间在推移——从霜重的清晨到露水渐干的时分，诗人已经追寻了很久。时间的推移，突出了追寻的执着和漫长。"),
 ["起兴", "重章叠句", "时间推移"]),

(1, "所谓伊人，在水之[[湄|（méi）水边，河岸]]。",
 "我所思念的那个人，在水的岸边。",
 fixq("~L~在水之湄~R~与首章~L~在水一方~R~对应，~L~一方~R~变~L~之湄~R~，伊人的位置从~L~水的那一边~R~具体到~L~水的岸边~R~。但无论是~L~一方~R~还是~L~之湄~R~，伊人始终被水阻隔，可望而不可即。位置的细微变化，暗示诗人在不断追寻中不断接近，却始终无法触及。"),
 ["重章叠句", "伊人形象", "朦胧美"]),

(1, "溯洄从之，道阻且[[跻|（jī）升高，这里指道路险峻，难以攀登]]。",
 "逆流而上去追寻她，道路险阻又高峻。",
 fixq("~L~道阻且跻~R~与首章~L~道阻且长~R~对应，~L~长~R~变~L~跻~R~。~L~跻~R~是升高的意思，这里指道路险峻、难以攀登。道路从~L~漫长~R~到~L~高峻~R~，追寻的难度在增加——不仅远，而且险。但诗人依然逆流而上，执着追求的精神在重章叠句中不断强化。"),
 ["重章叠句", "执着追求", "炼字"]),

(1, "溯游从之，宛在水中[[坻|（chí）水中的高地]]。",
 "顺流而下去追寻她，仿佛又在水中的高地上。",
 fixq("~L~宛在水中坻~R~与首章~L~宛在水中央~R~对应，~L~中央~R~变~L~中坻~R~，伊人的位置从~L~水的中央~R~到~L~水中的高地~R~。但~L~宛~R~字不变——伊人始终是~L~仿佛~R~在那里，若隐若现，不可触及。三章中~L~宛~R~字的反复出现，强化了全诗的朦胧意境。"),
 ["重章叠句", "朦胧美", "炼字"]),

(2, "蒹葭[[采采|茂盛、众多的样子]]，白露[[未已|未止，未干。已，止]]。",
 "芦苇采采茂盛，清晨的露水还没有干。",
 fixq("第三章起兴，~L~萋萋~R~变~L~采采~R~，~L~未晞~R~变~L~未已~R~。~L~采采~R~与~L~苍苍~~L~萋萋~R~一样，都是写芦苇茂盛，但三个不同的叠词使诗歌在反复中富有变化。~L~未已~R~是~L~未止~R~的意思，露水还没有干，时间仍在推移。从~L~为霜~R~到~L~未晞~R~到~L~未已~R~，诗人追寻的时间越来越长，执着的精神也越来越突出。"),
 ["起兴", "重章叠句", "叠词", "时间推移"]),

(2, "所谓伊人，在水之[[涘|（sì）水边]]。",
 "我所思念的那个人，在水的边上。",
 fixq("~L~在水之涘~R~与前两章~L~在水一方~~L~在水之湄~R~对应，~L~涘~R~也是水边的意思。三个不同的词（一方、之湄、之涘）都指水边，伊人始终在水的那一边，从未改变。这种~L~变中不变~R~的写法，既通过词语变换避免了单调，又通过伊人位置的不变，强化了可望不可即的主题。"),
 ["重章叠句", "伊人形象", "变中不变"]),

(2, "溯洄从之，道阻且[[右|弯曲，迂回]]。",
 "逆流而上去追寻她，道路险阻又迂回曲折。",
 fixq("~L~道阻且右~R~与前两章~L~道阻且长~~L~道阻且跻~R~对应，~L~长~R~（漫长）→~L~跻~R~（高峻）→~L~右~R~（迂回），道路的困难层层递进：先是远，再是险，最后是曲折迂回。三个不同的形容词，写出了追寻道路的各种艰难，但诗人始终逆流而上，从未放弃。这种在困难中执着追求的精神，是全诗的核心主题。"),
 ["重章叠句", "执着追求", "层层递进", "炼字"]),

(2, "溯游从之，宛在水中[[沚|（zhǐ）水中的小块陆地]]。",
 "顺流而下去追寻她，仿佛又在水中的小块陆地上。",
 fixq("末句与前两章~L~宛在水中央~~L~宛在水中坻~R~对应，~L~中央~R~→~L~中坻~R~→~L~中沚~R~，伊人的位置在变化，但~L~宛~R~字始终不变——伊人永远是~L~仿佛~R~在那里，若隐若现，可望而不可即。全诗在~L~宛在水中沚~R~中结束，没有交代追寻的结果，伊人依然在水一方。这种没有结局的结尾，留下了无限的想象空间，也使~L~秋水伊人~R~的朦胧意境达到了极致。三章重章叠句，反复咏叹，写尽了追寻的执着和理想的朦胧，被誉为中国第一首朦胧诗。"),
 ["重章叠句", "朦胧美", "名句", "卒章显志", "秋水伊人"]),
]


DICT_WORDS = [
    {"w":"蒹","py":"jiān","q":"□葭苍苍，白露为霜","tip":fixq("「蒹」草字头，音 jiān，荻类植物；与~L~葭~R~（jiā）组成蒹葭，即芦苇")},
    {"w":"葭","py":"jiā","q":"蒹□苍苍，白露为霜","tip":fixq("「葭」草字头，音 jiā，芦苇；勿写~L~霞~R~（xiá，彩霞）、~L~暇~R~（xiá，空暇）")},
    {"w":"溯","py":"sù","q":"□洄从之，道阻且长","tip":fixq("「溯」三点水，音 sù，逆流而上；勿写~L~朔~R~（shuò，朔方）、~L~塑~R~（sù，塑料）")},
    {"w":"洄","py":"huí","q":"溯□从之，道阻且长","tip":fixq("「洄」三点水，音 huí，曲折的水道、逆流；勿写~L~回~R~（huí，回来）")},
    {"w":"晞","py":"xī","q":"白露未□","tip":fixq("「晞」日字旁，音 xī，晒干、干；勿写~L~稀~R~（xī，稀少）、~L~希~R~（xī，希望）")},
    {"w":"湄","py":"méi","q":"在水之□","tip":fixq("「湄」三点水，音 méi，水边、河岸；勿写~L~眉~R~（méi，眉毛）、~L~楣~R~（méi，门楣）")},
    {"w":"跻","py":"jī","q":"道阻且□","tip":fixq("「跻」足字旁，音 jī，升高、攀登；勿写~L~挤~R~（jǐ，拥挤）、~L~齐~R~（qí，整齐）")},
    {"w":"坻","py":"chí","q":"宛在水中□","tip":fixq("「坻」提土旁，音 chí，水中高地；多音字，又读 dǐ（宝坻）；勿写~L~低~R~（dī）")},
    {"w":"涘","py":"sì","q":"在水之□","tip":fixq("「涘」三点水，音 sì，水边；勿写~L~矣~R~（yǐ，语助词）、~L~挨~R~（āi）")},
    {"w":"沚","py":"zhǐ","q":"宛在水中□","tip":fixq("「沚」三点水，音 zhǐ，水中的小块陆地；勿写~L~止~R~（zhǐ，停止）、~L~址~R~（zhǐ，地址）")},
    {"w":"萋萋","py":"qī qī","q":"蒹葭□□，白露未晞","tip":fixq("叠词，草木茂盛义；两字均为草字头，读 qī qī，勿写~L~凄凄~R~（两点水，凄凉）")},
    {"w":"宛","py":"wǎn","q":"□在水中央","tip":fixq("「宛」宝盖头，音 wǎn，仿佛、好像；勿写~L~婉~R~（wǎn，婉转）、~L~苑~R~（yuàn，苑囿）")},
]

DICT_NOTES = [
    {"w":"蒹葭","a":"（jiān jiā）芦苇。蒹，荻；葭，芦苇","q":"蒹葭苍苍，白露为霜"},
    {"w":"苍苍","a":"茂盛的样子","q":"蒹葭苍苍，白露为霜"},
    {"w":"为霜","a":"凝结成霜。为，成为","q":"白露为霜"},
    {"w":"所谓","a":"所说的，这里指所怀念的","q":"所谓伊人"},
    {"w":"伊人","a":"那个人，指所爱的人。伊，那","q":"所谓伊人，在水一方"},
    {"w":"一方","a":"那一边。方，边、旁","q":"在水一方"},
    {"w":"溯洄","a":"（sù huí）逆流而上。溯，逆流；洄，曲折的水道","q":"溯洄从之"},
    {"w":"从","a":"追寻、跟随","q":"溯洄从之"},
    {"w":"阻","a":"险阻","q":"道阻且长"},
    {"w":"溯游","a":"顺流而下。溯，沿着；游，水流","q":"溯游从之"},
    {"w":"宛","a":"仿佛、好像","q":"宛在水中央"},
    {"w":"萋萋","a":"（qī qī）茂盛的样子","q":"蒹葭萋萋，白露未晞"},
    {"w":"未晞","a":"未干。晞（xī），干","q":"白露未晞"},
    {"w":"湄","a":"（méi）水边，河岸","q":"在水之湄"},
    {"w":"跻","a":"（jī）升高，这里指道路险峻，难以攀登","q":"道阻且跻"},
    {"w":"坻","a":"（chí）水中的高地","q":"宛在水中坻"},
    {"w":"采采","a":"茂盛、众多的样子","q":"蒹葭采采，白露未已"},
    {"w":"未已","a":"未止，未干。已，止","q":"白露未已"},
    {"w":"涘","a":"（sì）水边","q":"在水之涘"},
    {"w":"右","a":"弯曲，迂回","q":"道阻且右"},
    {"w":"沚","a":"（zhǐ）水中的小块陆地","q":"宛在水中沚"},
    {"w":"重章叠句","a":"《诗经》表现手法，各章字句基本相同，只换少数词语，反复咏唱","q":"蒹葭苍苍，白露为霜"},
    {"w":"秋水伊人","a":"出自《蒹葭》，指思念的人在远方，可望而不可即","q":"所谓伊人，在水一方"},
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
    <p>《蒹葭》选自《诗经·秦风》，是中国文学史上最著名的朦胧诗。全诗三章二十四句，以深秋清晨的芦苇、白露、秋水为背景，描写诗人对~L~伊人~R~的执着追寻，营造出朦胧缥缈、可望不可即的意境，被誉为~L~中国第一首朦胧诗~R~。</p>
    <p>全诗采用重章叠句的手法，三章结构相同，只换少数词语：~L~苍苍→萋萋→采采~R~写芦苇的茂盛，~L~为霜→未晞→未已~R~写时间的推移，~L~一方→之湄→之涘~R~写伊人的位置，~L~长→跻→右~R~写道路的艰难。在反复咏唱中，情感层层递进，意境越来越朦胧深远。</p>
  </div>
  <div class="box">
    <h3>《诗经》与秦风</h3>
    <p>《蒹葭》选自《诗经·秦风》。~L~秦~R~是西周时期的一个诸侯国，位于今陕西、甘肃一带，地处西陲，民风质朴而略带苍凉。秦地的秋景——苍茫的芦苇、萧瑟的秋风、清寒的秋水——与诗中朦胧凄清的意境高度契合。</p>
    <p>《诗经》是中国最早的诗歌总集，收录西周至春秋诗歌305篇，分风、雅、颂三部分。~L~风~R~是各地民歌，共160篇，包括十五国风。《秦风》是十五国风之一，共10篇，以雄浑苍凉著称。《蒹葭》是《秦风》中最著名的一篇，也是《诗经》中意境最美的作品之一。</p>
    <p class="note">※ 《诗经》~L~六义~R~：风、雅、颂（内容分类），赋、比、兴（表现手法）。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>秦地风貌：</b>秦地位于西北，秋天气候寒冷，芦苇丛生，秋水苍茫。这种自然环境为《蒹葭》提供了独特的背景——苍茫的芦苇、清寒的露水、辽阔的秋水，共同营造出朦胧凄清的氛围。</p>
    <p><b>爱情与理想：</b>关于《蒹葭》的主题，历来有不同解读。有人认为是爱情诗，写对恋人的追寻；有人认为是招贤诗，写对贤人的渴求；还有人认为是政治诗，写对理想的追求。正是这种主题的多义性，使《蒹葭》具有了永恒的艺术魅力——每个人都能在~L~秋水伊人~R~中看到自己的追寻。</p>
    <p><b>周代礼乐：</b>《蒹葭》本是一首可以演唱的乐歌，重章叠句的结构正是为了适应音乐的需要。三章反复咏唱，一唱三叹，富有音乐性和节奏感。</p>
  </div>
  <div class="box">
    <h3>文体知识</h3>
    <p>《蒹葭》是一首<b>四言诗</b>，每句四字，两句为一联，四句为一章，共三章十二句（按八言分行则为二十四句）。四言诗是《诗经》的主要形式。</p>
    <p><b>重章叠句：</b>全诗三章结构完全相同，只更换~L~苍苍→萋萋→采采~~L~为霜→未晞→未已~~L~一方→之湄→之涘~~L~长→跻→右~~L~中央→中坻→中沚~R~等词语。这种手法使诗歌富有音乐性，同时在反复中推进情感。</p>
    <p><b>起兴与意境：</b>~L~蒹葭苍苍，白露为霜~R~以秋景起兴，渲染朦胧凄清的氛围。全诗没有直接抒情，但景中含情，情景交融，营造出中国文学中最著名的朦胧意境。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>《蒹葭》八年级语文课文朗诵（一等奖）</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1ER62BYEoh&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="蒹葭朗诵"></iframe>
        <a href="https://www.bilibili.com/video/BV1ER62BYEoh" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>国风水墨MV《诗经·蒹葭》</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1bLZAYkEU5&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="蒹葭水墨MV"></iframe>
        <a href="https://www.bilibili.com/video/BV1bLZAYkEU5" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">伊人——朦胧缥缈的理想化身</div>
        <p>~L~伊人~R~是《蒹葭》的核心形象，但全诗从未直接描写伊人的外貌、性格，甚至没有交代伊人的身份。伊人始终~L~在水一方~~L~在水之湄~~L~在水之涘~R~，被秋水阻隔，若隐若现，可望而不可即。~L~宛在~R~二字，更写出伊人的缥缈——仿佛在那里，又仿佛不在。这种朦胧的写法，使伊人超越了具体的人物，成为一切美好理想的象征：可以是恋人，可以是贤人，可以是理想，可以是真理。伊人越是朦胧，追寻的意义就越丰富。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">抒情主人公——执着坚定的追寻者</div>
        <p>诗中的抒情主人公是一位执着的追寻者。面对秋水的阻隔和道路的艰难（~L~阻且长~~L~阻且跻~~L~阻且右~R~），他始终没有放弃——逆流而上（溯洄从之），顺流而下（溯游从之），上下求索。时间在推移（~L~为霜→未晞→未已~R~），道路越来越艰难，但追寻的脚步从未停止。这种明知不可为而为之的执着，使主人公的形象具有了感人的力量。他追寻的不仅是伊人，更是一切美好的理想。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">朦胧意境——秋水伊人，可望不可即</div>
        <p>《蒹葭》最突出的艺术特色是朦胧美。深秋清晨的芦苇、白露、秋水，本身就带有朦胧凄清的色彩；伊人始终~L~在水一方~R~，被秋水阻隔，~L~宛在~R~二字更写出若隐若现的缥缈。全诗没有直接抒情，也没有交代结果，一切都在朦胧之中。这种朦胧不是模糊，而是一种艺术的留白——给读者留下了无限的想象空间。《蒹葭》因此被誉为~L~中国第一首朦胧诗~R~。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">重章叠句——反复咏唱，层层递进</div>
        <p>全诗三章结构相同，只换少数词语。但这些变换不是简单的重复，而是有意义的递进：~L~苍苍→萋萋→采采~R~写芦苇的茂盛，~L~为霜→未晞→未已~R~写时间的推移，~L~长→跻→右~R~写道路的艰难层层加深。在反复咏唱中，追寻的执着和伊人的朦胧都得到了强化。一唱三叹，韵味无穷。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">情景交融——景中含情，情因景生</div>
        <p>全诗没有一句直接抒情，但处处含情。蒹葭的苍茫、白露的清寒、秋水的辽阔，都是诗人心境的外化——苍茫凄清的秋景，正是追寻者孤独执着心境的写照。景中有情，情因景生，情景交融，天衣无缝。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">蒹葭苍苍，白露为霜。所谓伊人，在水一方。</div>
        <p>这是《蒹葭》的开篇名句，也是中国文学中最著名的起兴之一。以深秋清晨的芦苇、白露起兴，营造出苍茫凄清的氛围；~L~所谓伊人，在水一方~R~点出所思念的人在水的那一边，可望而不可即。短短十六字，景、情、人、事俱全，朦胧优美，意境深远。~L~秋水伊人~R~由此成为千古流传的美好意象，象征着一切可望而不可即的美好事物。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">溯洄从之，道阻且长。溯游从之，宛在水中央。</div>
        <p>这四句写追寻的艰难和伊人的缥缈。~L~溯洄从之~R~是逆流而上，~L~道阻且长~R~写道路的险阻漫长；~L~溯游从之~R~是顺流而下，~L~宛在水中央~R~写伊人仿佛在水的中央。逆流、顺流，上下求索，却始终无法触及伊人。~L~宛~R~字是点睛之笔——仿佛在那里，又仿佛不在，将朦胧美写到极致。这四句是全诗的核心，写出了人类对美好理想执着追寻而又难以企及的普遍体验。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《蒹葭》通过描写诗人在深秋清晨对~L~伊人~R~的执着追寻，表达了对美好事物的向往和追求，以及追求过程中的惆怅与执着。</p>
    <p>这首诗的深刻之处在于它的多义性和普遍性。~L~伊人~R~是谁？是恋人、是贤人、还是理想？诗人没有明说。正是这种模糊性，使《蒹葭》超越了具体的时空，成为人类对一切美好事物执着追寻的象征。每个人都有自己的~L~伊人~R~，每个人都经历过~L~在水一方~R~的惆怅和~L~溯洄从之~R~的执着。~L~秋水伊人~R~的意象，因此具有了永恒的艺术魅力，千百年来感动了无数读者。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 意象 · 修辞 · 文化常识</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>文体与词牌</h3>
      <div class="acc-item"><span class="acc-w">《诗经》</span><span class="acc-d">中国最早的诗歌总集，收录西周至春秋诗歌305篇，分风、雅、颂三部分，表现手法为赋、比、兴。</span></div>
      <div class="acc-item"><span class="acc-w">国风·秦风</span><span class="acc-d">~L~风~R~是各地民歌，共160篇；~L~秦风~R~是十五国风之一，秦地民歌，风格雄浑苍凉。《蒹葭》是《秦风》名篇。</span></div>
      <div class="acc-item"><span class="acc-w">四言诗</span><span class="acc-d">每句四字的诗歌形式，《诗经》主要句式。两句为一联，四句为一章，节奏明快，富有音乐性。</span></div>
      <div class="acc-item"><span class="acc-w">重章叠句</span><span class="acc-d">《诗经》典型手法，各章字句基本相同，只换少数词语，反复咏唱，增强音乐性并推进情感。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>易错字音形</h3>
      <div class="acc-item"><span class="acc-w">蒹葭</span><span class="acc-d">（jiān jiā）芦苇。均为草字头，~L~蒹~R~音 jiān，~L~葭~R~音 jiā；勿写~L~霞~~L~暇~R~。</span></div>
      <div class="acc-item"><span class="acc-w">溯洄</span><span class="acc-d">（sù huí）逆流而上。均为三点水，~L~溯~R~音 sù，~L~洄~R~音 huí；勿写~L~朔~~L~回~R~。</span></div>
      <div class="acc-item"><span class="acc-w">晞</span><span class="acc-d">（xī）干。日字旁，勿写~L~稀~R~（禾木旁）、~L~希~R~。</span></div>
      <div class="acc-item"><span class="acc-w">湄</span><span class="acc-d">（méi）水边。三点水，勿写~L~眉~R~（目字旁）、~L~楣~R~（木字旁）。</span></div>
      <div class="acc-item"><span class="acc-w">跻</span><span class="acc-d">（jī）升高、攀登。足字旁，勿写~L~挤~R~（提手旁）、~L~齐~R~。</span></div>
      <div class="acc-item"><span class="acc-w">坻</span><span class="acc-d">（chí）水中高地。提土旁，多音字又读 dǐ；勿写~L~低~R~（单人旁）。</span></div>
      <div class="acc-item"><span class="acc-w">涘</span><span class="acc-d">（sì）水边。三点水，勿写~L~矣~R~（yǐ）、~L~挨~R~（āi）。</span></div>
      <div class="acc-item"><span class="acc-w">沚</span><span class="acc-d">（zhǐ）水中的小块陆地。三点水，勿写~L~止~R~、~L~址~R~（提土旁）。</span></div>
      <div class="acc-item"><span class="acc-w">萋萋</span><span class="acc-d">（qī qī）草木茂盛。草字头，勿写~L~凄~R~（两点水，凄凉）。</span></div>
      <div class="acc-item"><span class="acc-w">宛</span><span class="acc-d">（wǎn）仿佛、好像。宝盖头，勿写~L~婉~R~（女字旁）、~L~苑~R~（yuàn）。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文言梳理</h3>
      <div class="acc-sub">古今异义</div>
      <div class="tw"><table>
        <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
        <tr><td class="kai">所谓</td><td>所说的，这里指所怀念的</td><td>所说的（多用于引用）</td><td>所谓伊人</td></tr>
        <tr><td class="kai">伊人</td><td>那个人，指所爱的人</td><td>意中人（多指女性）</td><td>所谓伊人</td></tr>
        <tr><td class="kai">右</td><td>弯曲，迂回</td><td>右边，方位词</td><td>道阻且右</td></tr>
        <tr><td class="kai">已</td><td>止，停止</td><td>已经</td><td>白露未已</td></tr>
      </table></div>
      <div class="acc-sub">一词多义</div>
      <div class="tw"><table>
        <tr><th>词</th><th>义项</th><th>例句</th></tr>
        <tr><td class="kai">之</td><td>代词，指伊人</td><td>溯洄从之 / 溯游从之</td></tr>
        <tr><td class="kai">之</td><td>结构助词，的</td><td>在水之湄 / 在水之涘</td></tr>
        <tr><td class="kai">且</td><td>又、并且</td><td>道阻且长 / 道阻且跻</td></tr>
        <tr><td class="kai">从</td><td>追寻、跟随</td><td>溯洄从之</td></tr>
      </table></div>
      <div class="acc-sub">文言句式</div>
      <div class="tw"><table>
        <tr><th>句式</th><th>例句</th><th>说明</th></tr>
        <tr><td class="kai">省略句</td><td>（诗人）溯洄从之</td><td>承前省略主语~L~诗人~R~</td></tr>
        <tr><td class="kai">状语后置</td><td>所谓伊人，在水一方</td><td>~L~在水一方~R~即~L~在一方之水~R~，伊人在水的另一边</td></tr>
      </table></div>
    </div>
  </div>

  <div class="box">
    <h3>意象赏析（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>蒹葭·白露</dt><dd>深秋清晨的芦苇和露水，营造出苍茫凄清的氛围。~L~苍苍→萋萋→采采~R~写芦苇的茂盛，~L~为霜→未晞→未已~R~写时间的推移。蒹葭白露不仅是背景，更是诗人心境的外化——苍茫凄清的秋景，正是追寻者孤独执着心境的写照。</dd></div>
      <div class="g-item"><dt>秋水</dt><dd>阻隔诗人与伊人的河水，是距离和障碍的象征。秋水苍茫，伊人在水一方，可望而不可即。秋水的阻隔，使追寻变得艰难，也使伊人更加朦胧缥缈。~L~秋水伊人~R~由此成为千古流传的意象。</dd></div>
      <div class="g-item"><dt>伊人</dt><dd>全诗的核心形象，始终朦胧缥缈，若隐若现。~L~在水一方→在水之湄→在水之涘~R~，位置在变，但始终被水阻隔；~L~宛在水中央→宛在水中坻→宛在水中沚~R~，~L~宛~R~字不变，始终仿佛在那里。伊人是一切美好理想的象征。</dd></div>
      <div class="g-item"><dt>道路</dt><dd>~L~道阻且长→道阻且跻→道阻且右~R~，道路的艰难层层递进：漫长→高峻→迂回。道路象征追寻过程中的困难和挫折，但诗人始终逆流而上，从未放弃。</dd></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞与手法</h3>
      <div class="acc-item"><span class="acc-w">起兴</span><span class="acc-d">~L~蒹葭苍苍，白露为霜~R~以秋景起兴，渲染氛围，引出下文对伊人的追寻。</span></div>
      <div class="acc-item"><span class="acc-w">重章叠句</span><span class="acc-d">三章结构相同，换少数词语反复咏唱，在反复中推进情感，增强音乐性。</span></div>
      <div class="acc-item"><span class="acc-w">叠词</span><span class="acc-d">~L~苍苍~~L~萋萋~~L~采采~R~三个叠词，写芦苇茂盛，渲染苍茫氛围，增强音乐性。</span></div>
      <div class="acc-item"><span class="acc-w">双声叠韵</span><span class="acc-d">~L~蒹葭~R~（jiān jiā）双声，~L~苍苍~R~（cāng cāng）叠音，使诗句音韵和谐。</span></div>
      <div class="acc-item"><span class="acc-w">情景交融</span><span class="acc-d">秋景的苍茫凄清与诗人的孤独执着融为一体，景中含情，情因景生。</span></div>
      <div class="acc-item"><span class="acc-w">留白</span><span class="acc-d">全诗不直接抒情，不交代结果，伊人身份不明，给读者留下无限想象空间。</span></div>
    </div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>秦风</dt><dd>《诗经》十五国风之一，秦地民歌，共10篇。秦地位于西北，民风质朴苍凉，秦风多写征战、狩猎、爱情，风格雄浑。《蒹葭》是秦风中最柔美的一篇。</dd></div>
      <div class="g-item"><dt>秋水伊人</dt><dd>出自《蒹葭》~L~所谓伊人，在水一方~R~，指思念的人在远方，可望而不可即。后成为成语，象征一切美好而难以企及的事物。</dd></div>
      <div class="g-item"><dt>在水一方</dt><dd>出自《蒹葭》，后成为常用表达，指相隔遥远、难以相见。琼瑶小说《在水一方》及同名歌曲即典出于此。</dd></div>
      <div class="g-item"><dt>六义</dt><dd>《诗经》~L~六义~R~：风、雅、颂（内容分类），赋、比、兴（表现手法）。《蒹葭》以~L~兴~R~为主，兼有~L~赋~R~的叙述。</dd></div>
      <div class="g-item"><dt>朦胧诗</dt><dd>《蒹葭》被誉为~L~中国第一首朦胧诗~R~。其朦胧不是晦涩，而是通过意象的模糊和主题的多义，营造出悠远的意境，给读者留下广阔的想象空间。</dd></div>
      <div class="g-item"><dt>芦苇文化</dt><dd>芦苇在古代文学中常与秋天、离别、思念联系在一起。《蒹葭》开创了以芦苇写思念的传统，后世诗词中~L~芦苇~R~~L~芦荻~R~常作为凄凉、思念的意象。</dd></div>
    </div>
  </div>

</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《蒹葭》《诗经》</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">《诗经》</div>
  <h1 class="hero-title">蒹葭</h1>
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
  <div class="sec-sub">全诗三章十二句，分三部分解读。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《蒹葭》</div>
  <div>《诗经·秦风》 · 中国第一首朦胧诗 · 四言诗 · 秋水伊人</div>
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
