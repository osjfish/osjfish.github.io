# -*- coding: utf-8 -*-
"""生成《记承天寺夜游》课件（文言模式）。自包含脚本。"""
import io, json, re, html

SRC = r"D:\App\Apps\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\jichengtiansiyeyou-sushi.html"
LS_KEY = "chengtian_fs"

def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", rep, text)

def plain(text):
    return re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\1", text)

CARDS = [
(1, "[[元丰六年|公元1083年。元丰，宋神宗赵顼的年号]]十月十二日夜，[[解衣|脱了衣服]]欲睡，[[月色入户|月光照进门里。户，门]]，[[欣然|高兴、愉快的样子]]起行。",
 "元丰六年十月十二日夜晚，我脱了衣服想要睡觉，恰好看见月光照进门里，于是高兴地起身出门。",
 "起笔如日记，看似平铺，实则处处有戏：夜深欲睡，是常人常态；月色入户，是天意相邀。“欣然起行”四字，把作者见月之喜、动身之快一笔写出——一个被贬之人，深夜见月仍能欣然，性情先立。",
 ["记事", "炼字"]),
(1, "[[念|考虑，想到]]​[[无与为乐者|没有可以交谈取乐的人。与，共同，一起]]，[[遂|于是，就]]至承天寺[[寻|寻找]]​[[张怀民|苏轼的朋友。名梦得，字怀民，元丰六年也被贬到黄州，寄居承天寺]]。",
 "想到没有可以交谈取乐的人，就到承天寺去找张怀民。",
 "“念无与为乐者”一念之间，藏着深意：黄州满城之人，竟无一个可与共乐者——贬谪之孤凉，不着一字而尽出。寻张怀民，是同是天涯沦落人的相知；“遂”字见其急切，见月之喜与觅友之诚浑然一体。",
 ["知音", "贬谪"]),
(2, "怀民亦未[[寝|睡觉]]，[[相与|共同，一起]]​[[步|名词用作动词，散步]]于[[中庭|庭院里]]。",
 "张怀民也没有睡觉，（于是）我们一起在庭院中散步。",
 "一个“亦”字最堪玩味：怀民也未寝——他也在等月吗？也正无眠？两位逐客不谋而合，相视一笑，同步中庭。“相与步于中庭”六字平淡至极，却是患难之交才能有的从容，为下文写月铺设了同赏之人。",
 ["知音", "词类活用"]),
(2, "庭下如[[积水空明|形容月色如水般澄澈。空明，形容水的澄澈]]，水中[[藻、荇|（zǎo xìng）均为水生植物。藻，水藻；荇，荇菜，这里泛指水草]]​[[交横|纵横交错]]，[[盖|大概是]]竹柏影也。",
 "庭院中的月光如一泓积水一样清澈透明，水中仿佛有藻、荇纵横交错，原来是竹子和柏树的影子。",
 "全文写月名句。不着一“月”字，而月满庭户：先喻月为积水，再以“藻荇交横”写影，最后“盖竹柏影也”轻轻点破——错觉与恍然之间，月色之澄澈、竹影之摇曳如在目前。以水喻月前人已有，而积水藻荇连喻成境，是苏轼独造。",
 ["比喻", "写月", "名句"]),
(3, "[[何|哪，什么]]夜无月？何处无竹柏？",
 "哪一夜没有月光？哪里没有竹子和柏树？",
 "两个反问连发，由眼前之景宕开一层：月夜到处有，竹柏随处见，为何独此夜此景令人惊喜？言外之意呼之欲出——缺的不是月，不是景，而是赏月的闲人与闲情。承上启下，逼出结句。",
 ["反问", "过渡"]),
(3, "[[但|只是]]少[[闲人|清闲的人。这里含有贬谪的悲凉、人生的感慨、赏月的欣喜、漫步的悠闲等意味]]如吾两人者[[耳|语气词，相当于“罢了”]]。",
 "只是很少有像我们两人这样清闲的人罢了。",
 "全文点睛之笔。“闲人”一词，表层是赏月之悠闲，深层却五味俱陈：贬谪之悲凉，进退之感慨，赏月之欣喜，漫步之自在，尽在“闲”中。以“耳”字轻轻收束，自嘲中有自许，失意中有旷达——苏轼的人格境界，正在这“闲”字里。",
 ["点睛", "词句深味", "名句"]),
]

PARTS = {
 1:("月夜起行 · 欣然寻友","第1–2句","点明时间与缘起：月色入户而欣然起行，无与为乐而独寻怀民。"),
 2:("庭中月色 · 积水空明","第3–4句","正面写月：庭下积水空明、藻荇交横，不着一月字而月色满庭。"),
 3:("闲人慨叹 · 旷达收束","第5–6句","两个反问引出“闲人”之叹，贬谪悲凉与赏月欣喜交织作结。"),
}

FULLTEXT = [
 "元丰六年十月十二日夜，解衣欲睡，月色入户，欣然起行。",
 "念无与为乐者，遂至承天寺寻张怀民。",
 "怀民亦未寝，相与步于中庭。",
 "庭下如积水空明，水中藻、荇交横，盖竹柏影也。",
 "何夜无月？何处无竹柏？",
 "但少闲人如吾两人者耳。",
]

WORDS = [
 {"w":"寝","py":"qǐn","q":"怀民亦未□","tip":"「寝」宝盖头，睡觉义；勿写「寢」缺笔或「浸」"},
 {"w":"遂","py":"suì","q":"□至承天寺寻张怀民","tip":"「遂」走之底，于是、就义；勿写「逐」「隧」"},
 {"w":"户","py":"hù","q":"月色入□","tip":"「户」独体字，此处指门；勿写「尸」「护」"},
 {"w":"藻","py":"zǎo","q":"水中□、荇交横","tip":"「藻」草字头，水草义，读 zǎo；勿写「澡」「燥」"},
 {"w":"荇","py":"xìng","q":"水中藻、□交横","tip":"「荇」草字头，荇菜义，读 xìng；勿写「行」「衍」"},
 {"w":"盖","py":"gài","q":"□竹柏影也","tip":"「盖」此处义为大概是（推测语气）；勿写「盍」"},
 {"w":"庭","py":"tíng","q":"相与步于中□","tip":"「庭」广字头，庭院义；勿写「廷」（朝廷义）"},
 {"w":"柏","py":"bǎi","q":"何处无竹□","tip":"「柏」木字旁，读 bǎi；勿写「泊」「伯」"},
 {"w":"耳","py":"ěr","q":"但少闲人如吾两人者□","tip":"「耳」此处为语气词，相当于“罢了”；勿漏写"},
]

NOTES = [
 {"w":"元丰六年","a":"公元1083年。元丰，宋神宗年号","q":"元丰六年十月十二日夜"},
 {"w":"解衣","a":"脱了衣服","q":"解衣欲睡，月色入户"},
 {"w":"月色入户","a":"月光照进门里。户，门","q":"解衣欲睡，月色入户"},
 {"w":"欣然","a":"高兴、愉快的样子","q":"月色入户，欣然起行"},
 {"w":"念","a":"考虑，想到","q":"念无与为乐者，遂至承天寺寻张怀民"},
 {"w":"无与为乐者","a":"没有可以交谈取乐的人。与，共同、一起","q":"念无与为乐者，遂至承天寺寻张怀民"},
 {"w":"遂","a":"于是，就","q":"念无与为乐者，遂至承天寺寻张怀民"},
 {"w":"寻","a":"寻找","q":"遂至承天寺寻张怀民"},
 {"w":"张怀民","a":"苏轼的朋友。名梦得，字怀民，元丰六年也被贬到黄州，寄居承天寺","q":"遂至承天寺寻张怀民"},
 {"w":"寝","a":"睡觉","q":"怀民亦未寝"},
 {"w":"相与","a":"共同，一起","q":"相与步于中庭"},
 {"w":"步","a":"名词用作动词，散步","q":"相与步于中庭"},
 {"w":"中庭","a":"庭院里","q":"相与步于中庭"},
 {"w":"积水空明","a":"形容月色如水般澄澈。空明，形容水的澄澈","q":"庭下如积水空明，水中藻、荇交横"},
 {"w":"藻、荇","a":"均为水生植物。藻，水藻；荇，荇菜，这里泛指水草。读 zǎo xìng","q":"庭下如积水空明，水中藻、荇交横"},
 {"w":"交横","a":"纵横交错","q":"庭下如积水空明，水中藻、荇交横"},
 {"w":"盖","a":"大概是","q":"盖竹柏影也"},
 {"w":"竹柏","a":"竹子和柏树","q":"盖竹柏影也"},
 {"w":"何","a":"哪，什么","q":"何夜无月？何处无竹柏？"},
 {"w":"但","a":"只是","q":"但少闲人如吾两人者耳"},
 {"w":"闲人","a":"清闲的人。这里含有贬谪的悲凉、人生的感慨、赏月的欣喜、漫步的悠闲等意味","q":"但少闲人如吾两人者耳"},
 {"w":"耳","a":"语气词，相当于“罢了”","q":"但少闲人如吾两人者耳"},
]

BG_LEAD = [
 "《记承天寺夜游》写于宋神宗元丰六年（1083），当时苏轼正因“乌台诗案”被贬黄州，已有四年。全文仅八十五字，却记事、写景、抒情俱佳，是宋代小品文中传诵最广的名篇之一。",
 "一篇月夜小记，把贬谪的悲凉、人生的感慨、赏月的欣喜、漫步的悠闲都熔铸在“闲人”二字之中，语淡而味永，历来被视为苏轼随笔小品的最高代表。",
]
AUTHOR = [
 "苏轼（1037—1101），字子瞻，号东坡居士，眉山（今四川眉山）人，北宋文学家、书画家。与父苏洵、弟苏辙合称“三苏”，同列“唐宋八大家”。词开豪放一派，与辛弃疾并称“苏辛”；诗与黄庭坚并称“苏黄”。",
 "苏轼一生宦海浮沉，屡遭贬谪——黄州、惠州、儋州，越贬越远，却始终旷达自适。他在黄州躬耕东坡、两游赤壁，写下《念奴娇·赤壁怀古》《赤壁赋》与本文等千古名作，人生最低谷成了艺术最高峰。",
]
STORY = [
 ("乌台诗案","元丰二年（1079），苏轼因所作诗文被指讥讽新法，被捕入御史台狱百余日，几致死地。获释后责授黄州团练副使，不得签书公事——本篇所记，正是这段戴罪谪居岁月中的一个平常月夜。"),
 ("谪居黄州","贬黄州后俸禄微薄，苏轼率家人开垦城东坡地，躬耕自给，自号“东坡居士”。政治上的失意，反倒成全了他与山水、与百姓、与自我内心的深度相处。"),
 ("张怀民","张怀民名梦得，一字偓佺，元丰六年刚被贬到黄州，寄居城南承天寺。同是谪臣，同住一城，才有了这个月夜的“相与步于中庭”。苏辙《黄州快哉亭记》即为怀民而作。"),
]
VIDEOS = [("《记承天寺夜游》诵读","BV1SR4y1D7Ks","记承天寺夜游诵读"),
          ("都靓深度解读苏轼《记承天寺夜游》","BV17r4y1Q7jw","【都靓】深度解读苏轼《记承天寺夜游》")]

APP_PEOPLE = [
 ("失意中的旷达者","文中的苏轼，是深夜见月便“欣然起行”的性情中人，也是自称“闲人”的失意逐客。他没有哀哀切切地写贬谪之苦，只淡淡记一夜之游；而“但少闲人如吾两人者耳”一句，把悲凉与旷达、自嘲与自许全部收进一个“闲”字。能在人生低谷里把月光过成风景的，正是这份超然。"),
 ("相知相惜的张怀民","“怀民亦未寝”，一个“亦”字写出两位贬客的心照不宣。怀民同样刚遭贬谪，同样寓居寺中无眠——不必敲门寒暄，邀即同行。这段月下同游，是中国文学里“知音”最简练也最动人的一次记载。"),
]
APP_ART = [
 ("不着一字，尽得风流","全文正面写月仅一句，且通篇无一“月”字：以“积水”喻月光之澄澈，以“藻荇”写竹影之横斜，月色无形无质，一经比喻便可见可感。这是中国古典写月文字中公认的绝唱。"),
 ("一线串珠，尺水兴波","八十余字起承转合俱全：起于“欲睡”，一转“起行”，再转“寻友”，落于“步庭”；由事入景，由景入理，“何夜无月”一问荡开，“闲人”一叹收束。尺幅之间有起伏波澜，故读来毫无促狭之感。"),
 ("情感深藏，意味层出","记事写景的表面之下，情感层层叠叠：见月之欣喜、无友之孤凉、同游之默契、被贬之悲凉、自我宽解之旷达——都不明说，全藏在“欣然”“遂”“亦”“但”“耳”这些虚字的缝隙里，耐人反复咀嚼。"),
 ("语淡味永的小品笔法","不用奇字险韵，不作大声疾呼，全以家常口吻出之。正因语淡，情感才显得真切；正因短小，“闲人”二字才有千钧之力。南宋以来选家公认，此篇是苏轼小品的压卷之作。"),
]
APP_FAME = [
 ("庭下如积水空明，水中藻、荇交横，盖竹柏影也。","写月名句。先总喻月色为“积水空明”，再虚构“藻、荇交横”的错觉，末以“盖竹柏影也”点破缘由——一喻到底，虚实两转，月之澄澈、影之横斜、人之恍惚俱出。十八字写尽月光，无一月字。"),
 ("何夜无月？何处无竹柏？","两个反问把眼前之景推向普遍之理：月夜寻常，竹柏寻常，而不寻常的是赏景之心与同游之人。以问蓄势，为“闲人”之叹张本，是全文由景入情的枢纽。"),
 ("但少闲人如吾两人者耳。","全文点睛。“闲人”二字有表里两层：表面写拥有闲暇的赏月人，内里包含贬谪的悲凉、人生的感慨、赏月的欣喜、漫步的悠闲。一个“但”字轻轻拨转，“耳”字缓缓收束，自嘲与自适俱在其中，余味无穷。"),
]
APP_THEME = [
 "本文以胗胗八十五字，记一次月夜闲游：由“欣然起行”到“相与步于中庭”，再到庭下月色的绝妙描摹，最后归结于“闲人”之叹，表达了作者微妙而复杂的心境。",
 "文中的“闲人”意蕴丰厚：既有赏月的欣喜、漫步的悠闲，也有遭贬的悲凉、人生的感慨，更有身处逆境而超然自适的旷达。一庭月色，两颗闲心，苏轼以他特有的方式告诉后人：境遇可以困人，心境却能自由。",
]

ACC = [
 ("古今异义", [
   ("但","古义：只是（但少闲人）；今义：表转折的连词"),
   ("户","古义：门（月色入户）；今义：人家、住户"),
   ("念","古义：考虑，想到（念无与为乐者）；今义：想念，读书"),
   ("盖","古义：大概是（盖竹柏影也）；今义：器物上的遮盖物"),
 ]),
 ("词类活用", [
   ("步","名词用作动词，散步。例：相与步于中庭"),
 ]),
 ("一词多义", [
   ("与","共同，一起：无与为乐者"),
   ("寻","寻找：遂至承天寺寻张怀民"),
   ("遂","于是，就：遂至承天寺"),
   ("耳","语气词，罢了：但少闲人如吾两人者耳"),
 ]),
 ("文化常识", [
   ("元丰","宋神宗赵顼的年号（1078—1085）。文中“元丰六年”即公元1083年。"),
   ("承天寺","在今湖北黄冈城南。张怀民贬黄州时寓居于此。一说寺名承天，取“承奉天命”之意。"),
   ("乌台诗案","元丰二年苏轼因诗文获罪下狱的案件。御史台又称乌台，故称。此案后苏轼贬黄州，《记承天寺夜游》《赤壁赋》皆作于谪居期间。"),
   ("闲人","本文点睛之词。既指有闲情逸趣之人，也暗含贬官“不得签书公事”的清闲身份，悲凉与旷达兼而有之。"),
   ("记","古代散文文体，可叙事、写景、状物、抒怀。本文是“记”中的月夜小记，不施藻绘而情味隽永。"),
 ]),
]

# ================= 组装 =================
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]
main_js, dict_js = re.findall(r"<script>\n(.*?)</script>", src, re.S)
main_js = main_js.replace("beiying_fs", LS_KEY)
dict_js = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", dict_js, flags=re.S)
dict_js = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", dict_js, flags=re.S)

CN = "一二三"
hero = '<header class="hero">\n  <div class="hero-side">北宋 · 苏轼</div>\n  <h1 class="hero-title">记承天寺夜游</h1>\n</header>'
nav = '<nav class="nav"><div class="nav-in"><a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a><div class="tool"><select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option></select><button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button></div></div></nav>'

def video(i, h4, bvid, atitle):
    return ('<div class="media"><h4>%s</h4>'
            '<iframe id="mediaF%d" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>'
            '<a href="https://www.bilibili.com/video/%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF%d">全屏播放</button></div>'
            % (h4, i, bvid, atitle, bvid, i))

bg = ['<main class="wrap">', '<section id="bg" class="sec">',
      '<div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>', '<div class="lead">']
for p in BG_LEAD: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>作者简介</h3>')
for p in AUTHOR: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>写作背景</h3>')
for t, p in STORY: bg.append('<p><b>' + t + '：</b>' + p + '</p>')
bg.append('</div><div class="box media-box"><h3>视听</h3><div class="media-grid">')
for i, (h4, bvid, at) in enumerate(VIDEOS): bg.append(video(i + 1, h4, bvid, at))
bg.append('</div></div></section>')

jl = ['<div class="divider"></div>', '<section id="jielu" class="sec">',
      '<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>',
      '<div class="sec-sub">全文八十五字，分三部分：月夜起行、庭中月色、闲人慨叹。每句含注释、译文与赏析，点击可展开。</div>',
      '<button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>',
      '<div id="fulltext" class="poem" style="display:none">']
for p in FULLTEXT: jl.append('<div class="pl">' + p + '</div>')
jl.append('</div><div class="verse-list" id="verseList">')
cur = 0
n = 0
for (part, txt, yi, shang, tags) in CARDS:
    if part != cur:
        cur = part
        t, rng, ov = PARTS[part]
        jl.append('<div class="part-head"><span class="p-num">第%s部分</span><h3>%s</h3><span class="range">%s</span></div>' % (CN[part - 1], t, rng))
        jl.append('<div class="part-overview">%s</div>' % ov)
    n += 1
    tag_html = ''.join('<span>%s</span>' % t for t in tags)
    jl.append('<div class="verse" id="l%d" data-i="%d">\n  <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>\n  <details class="v-more">\n    <summary>译文 · 赏析</summary>\n    <div class="d-body">\n      <div class="v-sec"><b class="v-label">译　文</b>\n        <div class="v-trans">%s</div>\n      </div>\n      <div class="v-sec"><b class="v-label">赏　析</b>\n        <div class="d-body"><p>%s</p></div>\n      </div>\n      <div class="tags">%s</div>\n    </div>\n  </details>\n</div>' % (n, n - 1, n, annotate(txt), yi, shang, tag_html))
jl.append('</div></section>')

app = ['<div class="divider"></div>', '<section id="app" class="sec">',
       '<div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>',
       '<div class="box"><h3>形象赏析</h3><p style="margin-bottom:14px;color:var(--ink2)">文中的“形象”是月下同游的两位“闲人”，尤其是那位在失意中依然欣然的苏轼。</p><div class="fame">']
for t, p in APP_PEOPLE: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>艺术特色</h3><div class="fame">')
for t, p in APP_ART: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>名句赏析</h3><div class="fame">')
for t, p in APP_FAME: app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div><div class="box"><h3>主题思想</h3>')
for p in APP_THEME: app.append('<p>' + p + '</p>')
app.append('</div></section>')

acc = ['<div class="divider"></div>', '<section id="acc" class="sec">',
       '<div class="sec-head"><h2>积 累</h2><span class="no">古今异义 · 词类活用 · 一词多义 · 文化常识</span></div>']
for cat, items in ACC:
    acc.append('<div class="box"><div class="acc-cat"><h3>%s</h3>' % cat)
    for w, d in items:
        acc.append('<div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>' % (w, d))
    acc.append('</div></div>')
acc.append('</section>')

practice = ['<div class="divider"></div>', '<section id="practice" class="sec">',
            '<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>',
            '<div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>',
            '<div class="ptools"><button data-mode="word" data-rand="5">随机五组字形</button><button data-mode="word" data-all="1">全部字形</button><button data-mode="note" data-rand="5">随机五组注释</button><button data-mode="note" data-all="1">全部注释</button></div></section>']
footer = '<footer>\n  <div class="kai">《记承天寺夜游》</div>\n  <div>苏轼 · 北宋（1037—1101）· 元丰六年黄州所作</div>\n</footer>'
tail = '''<button class="top-btn" id="topBtn" title="回到顶部">↑</button>
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
</div>'''

html_doc = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>《记承天寺夜游》苏轼</title>\n<style>' + css + '</style>\n</head>\n<body data-fs="100">\n\n'
        + hero + '\n\n' + nav + '\n\n' + "\n".join(bg) + '\n\n' + "\n".join(jl) + '\n\n' + "\n".join(app) + '\n\n' + "\n".join(acc) + '\n\n' + "\n".join(practice) + '\n\n'
        + footer + '\n</main>\n\n' + tail + '\n<script>\n' + main_js + '</script>\n<script>\n' + dict_js + '</script>\n\n</body>\n</html>\n')

# ================= 自检 =================
no_script = re.sub(r"<script>.*?</script>", "", html_doc, flags=re.S)
body_text = re.sub(r"<[^>]+>", "", re.sub(r"<style>.*?</style>", "", no_script, flags=re.S))
assert body_text.count('"') == 0, "straight quotes in visible text"
need = ["verseList", "fulltext", "btnAll", "btnRecite", "btnPrint", "btnShowAll", "fsSel", "annoPopup", "dictate", "topBtn", "mediaF1", "mediaF2"]
missing = [i for i in need if 'id="%s"' % i not in html_doc]
assert not missing, "missing ids: %s" % missing
assert LS_KEY in main_js and "beiying_fs" not in main_js and "beiying" not in dict_js
per_card = re.findall(r'<div class="verse".*?<div class="v-line">(.*?)</div></div>', html_doc, re.S)
empty = [i + 1 for i, o in enumerate(per_card) if "anno-word" not in o]
assert not empty, "cards without annotation: %s" % empty
for it in WORDS:
    assert not any(c in it["q"] for c in it["w"]), "leak: %s" % it["w"]
    assert it["q"].count("□") == len(it["w"]), "box mismatch: %s" % it["w"]
    assert it["py"] and it["tip"] and it["tip"] != it["w"], "tip bad: %s" % it["w"]
import difflib
card_stream = "".join(plain(t) for (_, t, _, _, _) in CARDS).replace("​", "")
full_stream = "".join(FULLTEXT)
norm = lambda s: re.sub(r"\s+", "", s)
if norm(card_stream) != norm(full_stream):
    for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, norm(card_stream), norm(full_stream)).get_opcodes():
        if op != "equal":
            print("DIFF", op, repr(norm(card_stream)[a1:a2]), "!=", repr(norm(full_stream)[b1:b2]))
    raise SystemExit("fulltext/card stream mismatch")
print("记承天寺夜游 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), html_doc.count('class="anno-word"'), len(WORDS), len(NOTES), len(html_doc.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html_doc)
print("OK ->", OUT)
