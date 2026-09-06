# -*- coding: utf-8 -*-
"""《饮酒·其五》课件生成器 —— 复用《背影》CSS/JS框架。"""
import json, re, html, io, os
LQ='\u201c';RQ='\u201d'
SRC=os.path.join(os.path.dirname(os.path.abspath(__file__)),'beiying-zhuziqing.html')
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'yinjiu-taoyuanming.html')
src=io.open(SRC,encoding='utf-8-sig').read()
CSS=src[src.index('<style>')+7:src.index('</style>')]
CSS+='\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0=src.index('<script>');JS=src[s0+8:src.index('</script>',s0)]
JS=JS.replace('beiying_fs','yinjiu_fs')
def annotate(text):
    def rep(m):
        w,n=m.group(1),m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>'%(html.escape(n,quote=True),w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]',rep,text)
def fixq(s):return s.replace('~L~',LQ).replace('~R~',RQ)

FULLTEXT=[
    "结庐在人境，而无车马喧。",
    "问君何能尔？心远地自偏。",
    "采菊东篱下，悠然见南山。",
    "山气日夕佳，飞鸟相与还。",
    "此中有真意，欲辨已忘言。",
]
PARTS=[
    ("第一部分","心远地偏 · 采菊见山","第 1–4 句",
     fixq("首四句写诗人归隐后的生活状态和精神境界。~L~结庐在人境，而无车马喧~R~，写诗人虽然住在人群聚居的地方，却没有车马的喧嚣——为什么能这样？~L~心远地自偏~R~，因为心远离了世俗，自然觉得住的地方偏僻了。~L~采菊东篱下，悠然见南山~R~，写诗人在东篱下采菊，悠然自得，无意中抬头看见了南山。~L~悠然~R~二字，写出了诗人的闲适自在，是千古传诵的名句。")),
    ("第二部分","山气飞鸟 · 真意忘言","第 5–10 句",
     fixq("~L~山气日夕佳，飞鸟相与还~R~，写傍晚的山间景色：山间的云气在黄昏时分格外美好，飞鸟结伴而归。这两句既是写景，也是象征——飞鸟归林，象征诗人归隐田园。~L~此中有真意，欲辨已忘言~R~，写诗人从自然中领悟到了人生的真谛，但想要说出来，却忘了该怎样用语言表达。~L~忘言~R~是道家的最高境界，意思是真正的道理是无法用语言表达的，只能用心去体会。这两句是全诗的点睛之笔，蕴含着深刻的哲理。")),
]
S=[
(0,"[[结庐|（jié lú）建造房屋。结，建造、构筑；庐，简陋的房屋]]在[[人境|人间、人群聚居的地方。人，人群；境，地方]]，而无[[车马喧|（chē mǎ xuān）车马的喧嚣声。车马，指世俗的交往；喧，喧嚣]]。",
 "我把房屋建在人群聚居的地方，却没有车马的喧嚣。",
 fixq("开篇即提出一个看似矛盾的现象：住在人境，却无车马喧。~L~结庐~R~是建造房屋的意思，~L~庐~R~指简陋的房屋，暗示诗人的生活简朴。~L~人境~R~是人群聚居的地方，说明诗人并没有隐居到深山老林，而是住在人间。~L~而无车马喧~R~的~L~而~R~字表示转折，住在人境却没有车马的喧嚣，这是为什么呢？这一句为下文~L~心远地自偏~R~的回答做了铺垫，也引发了读者的思考。"),
 ["起笔","铺垫","对比"]),
(0,"问[[君|你，这里是诗人自问]]何能[[尔|（ěr）这样、如此]]？[[心远|心灵远离世俗。心，心灵；远，远离]]地[[自偏|自然偏僻。自，自然；偏，偏僻]]。",
 "请问你为什么能这样呢？因为心灵远离了世俗，住的地方自然就显得偏僻了。",
 fixq("这一联是全诗的主旨所在。~L~问君何能尔~R~以设问起笔，~L~君~R~是诗人自问，~L~尔~R~是~L~这样~R~的意思，指代上一句~L~结庐在人境，而无车马喧~R~。~L~心远地自偏~R~是回答，也是全诗的核心——~L~心远~R~是心灵远离世俗，~L~地自偏~R~是住的地方自然就显得偏僻了。这一句蕴含着深刻的哲理：环境的安静与否，不在于地点，而在于心境。只要心远离了世俗的功名利禄，即使住在人来人往的地方，也能保持内心的宁静。~L~心远~R~二字，是全诗的诗眼，统领全篇。"),
 ["设问","主旨","哲理","诗眼"]),
(0,"采菊东篱下，[[悠然|（yōu rán）闲适自得的样子。悠，闲适；然，……的样子]][[见|（jiàn）看见、望见，这里是无意中看见]]南山。",
 "在东篱下采摘菊花，悠然自得，无意中抬头望见了南山。",
 fixq("这是千古传诵的名句，也是陶渊明诗歌的代表作。~L~采菊东篱下~R~，写诗人在东篱下采摘菊花，动作简单而闲适。~L~悠然见南山~R~，写诗人悠然自得，无意中抬头看见了南山。~L~悠然~R~二字，写出了诗人的闲适自在、心无挂碍；~L~见~R~字用得极妙——是~L~见~R~（无意中看见），而不是~L~望~R~（有意地眺望），说明诗人是在采菊时无意中看到了南山，人与自然融为一体，达到了~L~物我两忘~R~的境界。苏轼曾说：~L~因采菊而见山，境与意会，此句最有妙处。~R~这两句写出了归隐生活的闲适和人与自然的和谐，是中国古典诗歌中最著名的名句之一。"),
 ["炼字","名句","物我两忘","闲适"]),
(1,"[[山气|山间的云气。山，山中；气，云气、雾气]][[日夕|（rì xī）傍晚、黄昏。日，太阳；夕，傍晚]]佳，飞鸟[[相与还|（xiāng yǔ huán）结伴而归。相与，一起、结伴；还，返回]]。",
 "山间的云气在黄昏时分格外美好，飞鸟结伴而归。",
 fixq("这两句写傍晚的山间景色。~L~山气日夕佳~R~，山间的云气在黄昏时分格外美好——~L~日夕~R~是傍晚的意思，~L~佳~R~是美好的意思。~L~飞鸟相与还~R~，飞鸟结伴而归——~L~相与~R~是一起、结伴的意思，~L~还~R~是返回的意思。这两句既是写景，也是象征：飞鸟归林，象征诗人归隐田园，找到了精神的归宿。飞鸟在黄昏时结伴归巢，诗人也在归隐后找到了内心的安宁。~L~还~R~字一语双关，既写飞鸟归林，也写诗人归隐。这两句与上一句~L~悠然见南山~R~衔接自然，由远及近，由山到鸟，画面完整而和谐。"),
 ["写景","象征","一语双关"]),
(1,"[[此中|这里面，指南山的景物和归隐的生活]]有[[真意|真正的意趣、人生的真谛。真，真正；意，意趣、道理]]，[[欲辨|想要辨别、想要说出来。欲，想要；辨，辨别、说明]]已[[忘言|忘记了用语言表达。忘，忘记；言，语言]]。",
 "这里面蕴含着人生的真正意趣，想要说出来，却忘了该怎样用语言表达。",
 fixq("末二句是全诗的点睛之笔，蕴含着深刻的哲理。~L~此中有真意~R~，~L~此中~R~指前面所写的南山景物和归隐生活，~L~真意~R~指人生的真正意趣和真谛。诗人从自然中领悟到了人生的真谛——那就是顺应自然、返璞归真、远离世俗、保持内心的宁静。~L~欲辨已忘言~R~，想要把这个真谛说出来，却忘了该怎样用语言表达。这是道家~L~得意忘言~R~的思想——真正的道理是无法用语言表达的，只能用心去体会。~L~忘言~R~不是真的忘了怎么说话，而是说最高的真理是超越语言的，语言无法完全表达内心的感悟。这两句将全诗的哲理推向极致，余味无穷，是陶渊明~L~平淡中见深醇~R~风格的典范。"),
 ["哲理","用典","点睛之笔","名句"]),
]
DICT_WORDS=[
    {"w":"庐","py":"lú","q":"结□在人境，而无车马喧","tip":fixq("「庐」广字头，音 lú，简陋的房屋，~L~结庐~R~即建造房屋，勿写~L~芦~R~（芦苇，草字头）~L~炉~R~（火炉，火字旁）")},
    {"w":"喧","py":"xuān","q":"结庐在人境，而无车马□","tip":fixq("「喧」口字旁，音 xuān，喧嚣、声音大，~L~车马喧~R~即车马的喧嚣声，勿写~L~暄~R~（寒暄，日字旁）~L~宣~R~（宣传）")},
    {"w":"尔","py":"ěr","q":"问君何能□？心远地自偏","tip":fixq("「尔」小字头，音 ěr，这样、如此，~L~何能尔~R~即怎么能这样，勿写~L~而~R~（而且）~L~耳~R~（耳朵）")},
    {"w":"悠","py":"yōu","q":"采菊东篱下，□然见南山","tip":fixq("「悠」心字底，音 yōu，闲适、闲散，~L~悠然~R~即闲适自得的样子，勿写~L~忧~R~（忧愁，竖心旁）")},
    {"w":"菊","py":"jú","q":"采□东篱下，悠然见南山","tip":fixq("「菊」草字头，音 jú，菊花，~L~采菊~R~即采摘菊花，勿写~L~鞠~R~（鞠躬，革字旁）")},
    {"w":"篱","py":"lí","q":"采菊东□下，悠然见南山","tip":fixq("「篱」竹字头，音 lí，篱笆，~L~东篱~R~即东边的篱笆，勿写~L~离~R~（离开）~L~璃~R~（玻璃，王字旁）")},
    {"w":"辨","py":"biàn","q":"此中有真意，欲□已忘言","tip":fixq("「辨」辛字旁，音 biàn，辨别、分辨，~L~欲辨~R~即想要辨别说明，勿写~L~辩~R~（辩论，言字旁）~L~辫~R~（辫子，绞丝旁）")},
    {"w":"夕","py":"xī","q":"山气日□佳，飞鸟相与还","tip":fixq("「夕」夕字旁，音 xī，傍晚、黄昏，~L~日夕~R~即傍晚，勿写~L~西~R~（西方）~L~汐~R~（潮汐，三点水）")},
]
DICT_NOTES=[
    {"w":"结庐","q":"结庐在人境","a":"（jié lú）建造房屋。结，建造、构筑；庐，简陋的房屋"},
    {"w":"人境","q":"结庐在人境","a":"人间、人群聚居的地方。人，人群；境，地方"},
    {"w":"车马喧","q":"而无车马喧","a":"（chē mǎ xuān）车马的喧嚣声，这里指世俗的交往。喧，喧嚣"},
    {"w":"君","q":"问君何能尔","a":"你，这里是诗人自问"},
    {"w":"尔","q":"问君何能尔","a":"（ěr）这样、如此"},
    {"w":"心远","q":"心远地自偏","a":"心灵远离世俗。心，心灵；远，远离"},
    {"w":"自偏","q":"心远地自偏","a":"自然偏僻。自，自然；偏，偏僻"},
    {"w":"悠然","q":"悠然见南山","a":"（yōu rán）闲适自得的样子。悠，闲适；然，……的样子"},
    {"w":"见","q":"悠然见南山","a":"（jiàn）看见、望见，这里是无意中看见（非有意眺望）"},
    {"w":"山气","q":"山气日夕佳","a":"山间的云气。山，山中；气，云气、雾气"},
    {"w":"日夕","q":"山气日夕佳","a":"（rì xī）傍晚、黄昏。日，太阳；夕，傍晚"},
    {"w":"相与还","q":"飞鸟相与还","a":"（xiāng yǔ huán）结伴而归。相与，一起、结伴；还，返回"},
    {"w":"此中","q":"此中有真意","a":"这里面，指南山的景物和归隐的生活"},
    {"w":"真意","q":"此中有真意","a":"真正的意趣、人生的真谛。真，真正；意，意趣、道理"},
    {"w":"欲辨","q":"欲辨已忘言","a":"想要辨别、想要说出来。欲，想要；辨，辨别、说明"},
    {"w":"忘言","q":"欲辨已忘言","a":"忘记了用语言表达。忘，忘记；言，语言。道家~L~得意忘言~R~的思想"},
]
def build_verses():
    out,idx=[],0
    for pi,part in enumerate(PARTS):
        out.append('      <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>'%(part[0],part[1],part[2]))
        out.append('      <div class="part-overview">%s</div>'%fixq(part[3]))
        for(p,txt,yi,shang,tags)in S:
            if p!=pi:continue
            idx+=1
            out.append('      <div class="verse" id="l%d" data-i="%d">'%(idx,idx-1))
            out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>'%(idx,annotate(txt)))
            out.append('        <details class="v-more"><summary>译文 · 赏析</summary><div class="d-body">')
            out.append('            <div class="v-sec"><b class="v-label">译　文</b><div class="v-trans">%s</div></div>'%yi)
            out.append('            <div class="v-sec"><b class="v-label">赏　析</b><div class="d-body"><p>%s</p></div>'%shang)
            if tags:out.append('              <div class="tags">%s</div>'%''.join('<span>%s</span>'%t for t in tags))
            out.append('            </div></div></details></div>')
    return '\n'.join(out),idx
verses_html,total=build_verses()
full_html='\n'.join('    <div class="pl">%s</div>'%p for p in FULLTEXT)
anno_count=sum(txt.count('[[') for(_,txt,_,_,_)in S)
BG=fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《饮酒·其五》是东晋诗人陶渊明的代表作，是《饮酒》组诗二十首中的第五首。这首诗写于陶渊明归隐田园之后，表达了诗人远离世俗、归隐自然的人生态度和~L~心远地自偏~R~的精神境界。</p>
    <p>全诗以~L~心远~R~统摄，先写归隐后的生活状态——结庐人境而无车马喧；再写归隐后的精神境界——采菊东篱，悠然见山；最后以~L~此中有真意，欲辨已忘言~R~收束，蕴含着深刻的哲理。~L~采菊东篱下，悠然见南山~R~是千古传诵的名句，被誉为中国古典诗歌中最能体现隐逸精神的诗句。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>陶渊明（约365—427），字元亮，又名潜，号五柳先生，私谥靖节，浔阳柴桑（今江西九江）人。东晋伟大的诗人、辞赋家，是中国文学史上第一位田园诗人，被称为~L~古今隐逸诗人之宗~R~。</p>
    <p>陶渊明曾任江州祭酒、镇军参军、彭泽令等职，因不愿~L~为五斗米折腰~R~，辞官归隐，过着~L~躬耕自资~R~的田园生活。他的诗歌多写田园风光和归隐生活，风格平淡自然、质朴真率，代表作有《饮酒》《归园田居》《桃花源记》《五柳先生传》等。</p>
    <p class="note">※ 《饮酒》组诗共二十首，非一时之作，约写于陶渊明归隐之后。诗前有序，说明这些诗是在酒后所写，抒发对人生的感悟。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>东晋末年：</b>陶渊明生活在东晋末年，当时社会动荡，政治黑暗，门阀制度森严，寒门子弟很难有出头之日。陶渊明几次出仕，都因看不惯官场的黑暗而辞官归隐。</p>
    <p><b>归隐田园：</b>义熙元年（405），陶渊明任彭泽令仅八十余日，因不愿~L~为五斗米折腰~R~，辞官归隐，从此不再出仕。他在农村过着~L~躬耕自资~R~的生活，虽然清贫，但精神上获得了自由和安宁。《饮酒》组诗即写于这一时期。</p>
    <p><b>玄学与佛教：</b>魏晋时期玄学盛行，道家~L~自然无为~R~的思想和佛教~L~出世~R~的思想对文人影响很大。陶渊明的诗歌深受道家思想影响，~L~此中有真意，欲辨已忘言~R~就是道家~L~得意忘言~R~思想的体现。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《饮酒·其五》是一首<b>五言古诗</b>（五言古体诗），全诗十句，每句五字，共五十字。不同于五言律诗的严格格律，五言古诗不拘平仄粘对，形式自由，节奏明快。</p>
    <p>《饮酒》是组诗，共二十首，本诗为第五首（~L~结庐在人境~R~）。组诗前有序，说明这些诗是在酒后所写，~L~既醉之后，聊题数句，自娱而已~R~。虽然说是~L~自娱~R~，但实际上蕴含着深刻的人生感悟和哲理思考。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>《千古风流人物》陶渊明《饮酒》其五 朗诵</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1Ya411E7eX&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="饮酒其五朗诵"></iframe>
        <a href="https://www.bilibili.com/video/BV1Ya411E7eX" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>《诗画中国》吴彤演唱《饮酒·其五》</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1e44y1Z7SA&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="饮酒其五歌曲"></iframe>
        <a href="https://www.bilibili.com/video/BV1e44y1Z7SA" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')
APP=fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>
  <div class="box">
    <h3>抒情主人公形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">陶渊明——归隐田园的精神隐士</div>
        <p>《饮酒·其五》中的抒情主人公，是一位远离世俗、归隐田园的精神隐士形象。他虽然住在人群聚居的地方，但心灵远离了世俗的功名利禄，过着闲适自在、与自然融为一体的生活。</p>
        <p><b>心远的境界：</b>~L~心远地自偏~R~，诗人的归隐不是形式上的隐居深山，而是精神上的远离世俗。只要心远了，即使住在人境，也能保持内心的宁静。这种~L~心远~R~的境界，是隐士的最高境界。</p>
        <p><b>悠然的生活：</b>~L~采菊东篱下，悠然见南山~R~，诗人在东篱下采菊，悠然自得，无意中抬头看见了南山。~L~悠然~R~二字，写出了诗人的闲适自在、心无挂碍，人与自然融为一体，达到了~L~物我两忘~R~的境界。</p>
        <p><b>忘言的哲理：</b>~L~此中有真意，欲辨已忘言~R~，诗人从自然中领悟到了人生的真谛，但最高的真理是超越语言的，只能用心去体会。这个形象，是中国文学中最动人的隐士形象，千百年来成为文人精神的寄托。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">平淡自然，质朴真率</div>
        <p>陶渊明的诗歌风格平淡自然，没有华丽的辞藻，没有夸张的修辞，用最朴素的语言表达最深刻的哲理。~L~采菊东篱下，悠然见南山~R~，语言简单到了极点，但意境却深远到了极点。这种~L~平淡中见深醇~R~的风格，是陶渊明诗歌的最大特色。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">情景理交融</div>
        <p>全诗将写景、抒情、说理融为一体。~L~采菊东篱下，悠然见南山~R~是写景，也是抒情；~L~山气日夕佳，飞鸟相与还~R~是写景，也是象征；~L~此中有真意，欲辨已忘言~R~是说理，也是抒情。景中有情，情中有理，情景理交融，天衣无缝。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">炼字精妙——见、悠然、忘言</div>
        <p>~L~见~R~字用得极妙——是无意中看见，而不是有意眺望，写出了人与自然的和谐。~L~悠然~R~二字写出了诗人的闲适自在。~L~忘言~R~二字蕴含着道家~L~得意忘言~R~的哲理。三字炼字精妙，将归隐的境界写到了极致。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">采菊东篱下，悠然见南山。</div>
        <p>这是千古传诵的名句，也是陶渊明诗歌的代表作。诗人在东篱下采摘菊花，悠然自得，无意中抬头望见了南山。~L~悠然~R~二字写出了诗人的闲适自在、心无挂碍；~L~见~R~字用得极妙——是无意中看见，而不是有意眺望，说明诗人完全沉浸在自然之中，达到了~L~物我两忘~R~的境界。苏轼曾说：~L~因采菊而见山，境与意会，此句最有妙处。~R~这两句写出了归隐生活的闲适和人与自然的和谐，是中国古典诗歌中最著名的名句之一，千百年来成为文人精神的寄托。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">此中有真意，欲辨已忘言。</div>
        <p>这两句是全诗的点睛之笔，蕴含着深刻的哲理。诗人从自然中领悟到了人生的真谛——顺应自然、返璞归真、远离世俗、保持内心的宁静。但最高的真理是超越语言的，~L~欲辨已忘言~R~，想要说出来，却忘了该怎样用语言表达。这是道家~L~得意忘言~R~的思想，也是陶渊明诗歌的最高境界。这两句将全诗的哲理推向极致，余味无穷。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>主题思想</h3>
    <p>《饮酒·其五》通过描写归隐田园后的生活状态和精神境界，表达了诗人远离世俗、归隐自然的人生态度，以及~L~心远地自偏~R~的精神追求和~L~得意忘言~R~的哲理思考。</p>
    <p>这首诗的深刻之处在于，它告诉我们：真正的隐居不是形式上的远离人群，而是精神上的远离世俗。~L~心远地自偏~R~，只要心远了，即使住在人来人往的地方，也能保持内心的宁静。这种精神境界，千百年来影响了无数文人，成为中国文化中隐逸精神的核心。</p>
  </div>
</section>
''')
ACC=fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 哲理 · 修辞 · 文化常识</span></div>
  <div class="box"><div class="acc-cat"><h3>文体与词牌</h3>
    <div class="acc-item"><span class="acc-w">五言古诗</span><span class="acc-d">《饮酒·其五》是五言古诗（古体诗），全诗十句，每句五字，不拘平仄粘对，形式自由。</span></div>
    <div class="acc-item"><span class="acc-w">《饮酒》组诗</span><span class="acc-d">共二十首，非一时之作，约写于陶渊明归隐之后。诗前有序，说明是酒后所写，抒发人生感悟。本诗为第五首。</span></div>
    <div class="acc-item"><span class="acc-w">田园诗</span><span class="acc-d">以田园风光和归隐生活为题材的诗歌。陶渊明是中国文学史上第一位田园诗人，被誉为~L~古今隐逸诗人之宗~R~。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>易错字音形</h3>
    <div class="acc-item"><span class="acc-w">庐</span><span class="acc-d">（lú）房屋，广字头，勿写~L~芦~R~~L~炉~R~。</span></div>
    <div class="acc-item"><span class="acc-w">喧</span><span class="acc-d">（xuān）喧嚣，口字旁，勿写~L~暄~R~（日字旁）。</span></div>
    <div class="acc-item"><span class="acc-w">尔</span><span class="acc-d">（ěr）这样，小字头，勿写~L~而~R~~L~耳~R~。</span></div>
    <div class="acc-item"><span class="acc-w">悠</span><span class="acc-d">（yōu）闲适，心字底，勿写~L~忧~R~（竖心旁）。</span></div>
    <div class="acc-item"><span class="acc-w">辨</span><span class="acc-d">（biàn）辨别，辛字旁，勿写~L~辩~R~（言字旁）~L~辫~R~（绞丝旁）。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>文言梳理</h3>
    <div class="acc-sub">古今异义</div>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">结庐</td><td>建造房屋</td><td>搭建茅屋（狭义）</td><td>结庐在人境</td></tr>
      <tr><td class="kai">人境</td><td>人间、人群聚居的地方</td><td>人类的环境</td><td>结庐在人境</td></tr>
      <tr><td class="kai">尔</td><td>这样、如此</td><td>你（代词）</td><td>问君何能尔</td></tr>
      <tr><td class="kai">相与</td><td>一起、结伴</td><td>彼此、互相</td><td>飞鸟相与还</td></tr>
      <tr><td class="kai">真意</td><td>人生的真谛、真正的意趣</td><td>真实的意思</td><td>此中有真意</td></tr>
    </table></div>
    <div class="acc-sub">一词多义</div>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="2">见</td><td>看见（无意中）</td><td>悠然见南山</td></tr>
      <tr><td>被（被动）</td><td>风吹草低见牛羊</td></tr>
      <tr><td class="kai" rowspan="2">还</td><td>返回</td><td>飞鸟相与还</td></tr>
      <tr><td>还是（副词）</td><td>还是要去</td></tr>
    </table></div>
    <div class="acc-sub">文言句式</div>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">设问句</td><td>问君何能尔？心远地自偏。</td><td>自问自答，以设问点明主旨</td></tr>
      <tr><td class="kai">省略句</td><td>（予）采菊东篱下</td><td>承前省略主语~L~予~R~（我）</td></tr>
    </table></div>
  </div></div>
  <div class="box">
    <h3>哲理赏析（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>心远地自偏</dt><dd>环境的安静与否，不在于地点，而在于心境。只要心远离了世俗的功名利禄，即使住在人来人往的地方，也能保持内心的宁静。~L~心远~R~是全诗的诗眼，统领全篇。</dd></div>
      <div class="g-item"><dt>悠然见南山</dt><dd>~L~见~R~是无意中看见，而不是有意眺望。诗人完全沉浸在自然之中，达到了~L~物我两忘~R~的境界。人与自然融为一体，是归隐的最高境界。</dd></div>
      <div class="g-item"><dt>飞鸟相与还</dt><dd>飞鸟归林，象征诗人归隐田园，找到了精神的归宿。~L~还~R~字一语双关，既写飞鸟归林，也写诗人归隐。</dd></div>
      <div class="g-item"><dt>欲辨已忘言</dt><dd>道家~L~得意忘言~R~的思想——最高的真理是超越语言的，只能用心去体会。~L~忘言~R~不是真的忘了怎么说话，而是说语言无法完全表达内心的感悟。</dd></div>
    </div>
  </div>
  <div class="box"><div class="acc-cat"><h3>修辞与手法</h3>
    <div class="acc-item"><span class="acc-w">设问</span><span class="acc-d">~L~问君何能尔？心远地自偏~R~，自问自答，点明主旨。</span></div>
    <div class="acc-item"><span class="acc-w">象征</span><span class="acc-d">~L~飞鸟相与还~R~象征诗人归隐田园，找到精神归宿。</span></div>
    <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">~L~欲辨已忘言~R~用《庄子》~L~得意忘言~R~的典故。</span></div>
    <div class="acc-item"><span class="acc-w">情景理交融</span><span class="acc-d">写景、抒情、说理融为一体，景中有情，情中有理。</span></div>
    <div class="acc-item"><span class="acc-w">白描</span><span class="acc-d">用朴素的语言描写景物，不加修饰，平淡自然。</span></div>
  </div></div>
  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>五柳先生</dt><dd>陶渊明的号。他在《五柳先生传》中说：~L~宅边有五柳树，因以为号焉。~R~五柳先生是陶渊明的自我写照。</dd></div>
      <div class="g-item"><dt>靖节先生</dt><dd>陶渊明的私谥。陶渊明去世后，友人私谥其为~L~靖节先生~R~。~L~靖~R~是安静，~L~节~R~是节操，~L~靖节~R~即安于贫贱、坚守节操。</dd></div>
      <div class="g-item"><dt>不为五斗米折腰</dt><dd>陶渊明任彭泽令时，郡督邮来视察，县吏说应束带见之。陶渊明叹道：~L~我岂能为五斗米折腰向乡里小儿！~R~即日辞官归隐。</dd></div>
      <div class="g-item"><dt>得意忘言</dt><dd>出自《庄子·外物》：~L~言者所以在意，得意而忘言。~R~意思是语言是用来表达意义的，领会了意义就忘了语言。指最高的真理超越语言。</dd></div>
      <div class="g-item"><dt>菊花</dt><dd>陶渊明爱菊，~L~采菊东篱下~R~使菊花成为隐逸的象征。菊花在秋季开放，不畏严寒，象征高洁的品格。后人称菊花为~L~花中隐士~R~。</dd></div>
      <div class="g-item"><dt>南山</dt><dd>指庐山，在陶渊明家乡附近。~L~悠然见南山~R~的南山即庐山。庐山是中国名山，以云雾和瀑布闻名。</dd></div>
      <div class="g-item"><dt>田园诗派</dt><dd>以描写田园风光和归隐生活为主要内容的诗歌流派。陶渊明是田园诗派的开创者，对后世王维、孟浩然、韦应物等诗人影响深远。</dd></div>
    </div>
  </div>
</section>
''')
HTML=u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《饮酒》陶渊明</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">
<header class="hero"><div class="hero-side">东晋 · 陶渊明</div><h1 class="hero-title">饮酒</h1></header>
<nav class="nav"><div class="nav-in">
<a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a>
<div class="tool">
<select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%%</option><option value="150">150%%</option><option value="200">200%%</option><option value="250">250%%</option><option value="300">300%%</option></select>
<button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button>
</div></div></nav>
<main class="wrap">
%(bg)s
<div class="divider"></div>
<section id="jielu" class="sec">
<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>
<div class="sec-sub">全诗十句（《饮酒》组诗其五），分两部分：心远采菊、真意忘言。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
<div class="kai">《饮酒·其五》</div>
<div>陶渊明 · 东晋（约365—427）· 号五柳先生，私谥靖节 · 五言古诗</div>
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
'''%{'css':CSS,'js':JS,'bg':BG,'app':APP,'acc':ACC,'fulltext':full_html,'verses':verses_html,'words':json.dumps(DICT_WORDS,ensure_ascii=False),'notes':json.dumps(DICT_NOTES,ensure_ascii=False)}
HTML=fixq(HTML)
io.open(OUT,'w',encoding='utf-8').write(HTML)
print('OK',OUT,'verses=',total,'anno=',anno_count,'words=',len(DICT_WORDS),'notes=',len(DICT_NOTES))
