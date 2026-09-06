# -*- coding: utf-8 -*-
"""《使至塞上》课件生成器 —— 复用《背影》CSS/JS框架。"""
import json, re, html, io, os
LQ='\u201c';RQ='\u201d'
SRC=os.path.join(os.path.dirname(os.path.abspath(__file__)),'beiying-zhuziqing.html')
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'shizhisaishang-wangwei.html')
src=io.open(SRC,encoding='utf-8-sig').read()
CSS=src[src.index('<style>')+7:src.index('</style>')]
CSS+='\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'
s0=src.index('<script>');JS=src[s0+8:src.index('</script>',s0)]
JS=JS.replace('beiying_fs','shizhisaishang_fs')
def annotate(text):
    def rep(m):
        w,n=m.group(1),m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>'%(html.escape(n,quote=True),w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]',rep,text)
def fixq(s):return s.replace('~L~',LQ).replace('~R~',RQ)

FULLTEXT=[
    "单车欲问边，属国过居延。",
    "征蓬出汉塞，归雁入胡天。",
    "大漠孤烟直，长河落日圆。",
    "萧关逢候骑，都护在燕然。",
]
PARTS=[
    ("第一部分","出使边塞 · 征蓬归雁","第 1–4 句",
     fixq("首联~L~单车欲问边，属国过居延~R~，点明出使的目的和经过的地点。~L~单车~R~写随从之少，暗含诗人被排挤出朝廷的孤寂。颔联~L~征蓬出汉塞，归雁入胡天~R~，以~L~征蓬~R~~L~归雁~R~自比，写自己像飘飞的蓬草一样出了汉塞，像北归的大雁一样进入胡天，既写景又抒情，暗含诗人内心的激愤和抑郁。")),
    ("第二部分","大漠长河 · 都护在燕然","第 5–8 句",
     fixq("颈联~L~大漠孤烟直，长河落日圆~R~，是千古传诵的名句，写边塞奇特壮丽的风光。~L~直~R~~L~圆~R~二字，炼字精绝，将大漠的辽阔和落日的壮美写得淋漓尽致。尾联~L~萧关逢候骑，都护在燕然~R~，写在萧关遇到侦察骑兵，得知都护正在燕然前线，以实写结尾，与首联~L~问边~R~呼应，使全诗结构完整。")),
]
S=[
(0,"[[单车|一辆车，形容随从少。单，一辆；车，车辆]][[欲|将要、想要]][[问边|到边塞去察看、慰问。问，慰问；边，边塞]]，[[属国|（shǔ guó）典属国的简称，汉代官名，这里指诗人自己出使边塞的身份]]过[[居延|（jū yán）古地名，在今内蒙古额济纳旗一带]]。",
 "我轻车简从，将要去慰问边塞；作为使者，经过了居延这个地方。",
 fixq("首联点明出使的目的和经过的地点。~L~单车~R~写随从之少，轻车简从，暗含诗人被排挤出朝廷的孤寂和失落。~L~欲问边~R~点明出使的目的是慰问边塞将士。~L~属国~R~是典属国的简称，汉代官名，掌管少数民族事务，这里指诗人自己出使边塞的身份。~L~过居延~R~写经过的地点，居延在今内蒙古额济纳旗一带，是边塞要地。这一联叙事平实，但~L~单车~R~二字已暗含诗人的孤寂和抑郁，为下文抒情做了铺垫。"),
 ["叙事","起笔","孤寂"]),
(0,"[[征蓬|（zhēng péng）飘飞的蓬草。征，远行；蓬，蓬草，枯后根断，随风飘飞]]出[[汉塞|汉朝的边塞，这里指唐朝的边塞。汉，以汉代唐]]，[[归雁|北归的大雁。归，返回；雁，大雁]]入[[胡天|胡人的天空，指西北地区。胡，古代对北方少数民族的称呼]]。",
 "像飘飞的蓬草一样出了汉塞，像北归的大雁一样进入了胡天。",
 fixq("颔联以~L~征蓬~R~~L~归雁~R~自比，是千古传诵的名句。~L~征蓬~R~是飘飞的蓬草，蓬草枯后根断，随风飘飞，古人常用以比喻漂泊不定的旅人；~L~归雁~R~是北归的大雁，大雁春天北归，秋天南飞。诗人以~L~征蓬~R~自比，写自己像飘飞的蓬草一样被排挤出朝廷，漂泊到边塞；以~L~归雁~R~自比，写自己像北归的大雁一样进入胡天。这两句既写景又抒情，~L~出汉塞~R~~L~入胡天~R~对仗工整，将诗人内心的激愤和抑郁含蓄地表达出来。以物喻人，情景交融，是王维~L~诗中有画~R~的典范。"),
 ["比喻","自比","对偶","名句"]),
(1,"[[大漠|广阔的沙漠。大，广阔；漠，沙漠]][[孤烟|（gū yān）烽火台升起的狼烟。孤，单独；烟，狼烟]]直，[[长河|长长的河流，这里指黄河]]落日圆。",
 "广阔的沙漠中，一缕狼烟笔直升起；长长的黄河上，一轮落日又大又圆。",
 fixq("颈联是千古传诵的名句，写边塞奇特壮丽的风光，被誉为~L~千古壮观~R~。~L~大漠孤烟直~R~，写广阔的沙漠中，一缕狼烟笔直升起——~L~大~R~字写沙漠的辽阔，~L~孤~R~字写人烟的稀少，~L~直~R~字写狼烟的挺拔。~L~长河落日圆~R~，写长长的黄河上，一轮落日又大又圆——~L~长~R~字写黄河的绵延，~L~落~R~字写时间的黄昏，~L~圆~R~字写落日的形状。~L~直~R~~L~圆~R~二字，炼字精绝：~L~直~R~字写出了狼烟的挺拔有力，~L~圆~R~字写出了落日的温暖壮美。在广阔的沙漠背景下，一缕直烟、一轮圆日，构成了一幅奇特壮丽的边塞图。这两句不仅写景逼真，更体现了诗人开阔的胸襟和积极乐观的精神，是王维~L~诗中有画，画中有诗~R~的典范。"),
 ["炼字","写景","名句","诗中有画","千古壮观"]),
(1,"[[萧关|（xiāo guān）古关名，在今宁夏固原东南，是关中通向塞北的要道]]逢[[候骑|（hòu jì）骑马的侦察兵。候，侦察、巡逻；骑，骑兵]]，[[都护|（dū hù）唐代边疆最高军事长官，这里指河西节度使]]在[[燕然|（yān rán）山名，即今蒙古国杭爱山，东汉窦宪大破匈奴，刻石纪功于此]]。",
 "在萧关遇到了侦察骑兵，得知都护正在燕然前线。",
 fixq("尾联以实写结尾，写诗人在萧关遇到侦察骑兵，得知都护正在燕然前线。~L~萧关~R~是古关名，在今宁夏固原东南，是关中通向塞北的要道。~L~候骑~R~是骑马的侦察兵。~L~都护~R~是唐代边疆最高军事长官，这里指河西节度使。~L~燕然~R~是山名，东汉窦宪大破匈奴后，在燕然山刻石纪功，后来~L~燕然~R~就成为战功的代称。这一联与首联~L~问边~R~呼应——诗人出使问边，在萧关遇到候骑，得知都护正在前线作战，使全诗结构完整。~L~都护在燕然~R~暗用窦宪刻石燕然的典故，既写出了边塞将士的战功，也表达了诗人对他们的敬意。"),
 ["用典","呼应","收束"]),
]
DICT_WORDS=[
    {"w":"蓬","py":"péng","q":"征□出汉塞，归雁入胡天","tip":fixq("「蓬」草字头，音 péng，蓬草，枯后根断随风飘飞，~L~征蓬~R~比喻漂泊，勿写~L~篷~R~（船篷，竹字头）")},
    {"w":"雁","py":"yàn","q":"征蓬出汉塞，归□入胡天","tip":fixq("「雁」厂字头，音 yàn，大雁，候鸟，~L~归雁~R~即北归的大雁，勿写~L~燕~R~（燕子，底部不同）")},
    {"w":"漠","py":"mò","q":"大□孤烟直，长河落日圆","tip":fixq("「漠」三点水，音 mò，沙漠，~L~大漠~R~即广阔的沙漠，勿写~L~莫~R~（莫非）~L~摸~R~（抚摸）")},
    {"w":"圆","py":"yuán","q":"大漠孤烟直，长河落日□","tip":fixq("「圆」口字框，音 yuán，圆形，~L~落日圆~R~即落日又大又圆，勿写~L~园~R~（花园，里面是元）")},
    {"w":"萧","py":"xiāo","q":"□关逢候骑，都护在燕然","tip":fixq("「萧」草字头，音 xiāo，萧关，古关名，勿写~L~箫~R~（竹箫，竹字头）~L~啸~R~")},
    {"w":"骑","py":"jì","q":"萧关逢候□，都护在燕然","tip":fixq("「骑」此处读 jì（旧读），骑兵，~L~候骑~R~即骑马的侦察兵，勿读 qí（骑马）")},
    {"w":"燕","py":"yān","q":"萧关逢候骑，都护在□然","tip":fixq("「燕」此处读 yān（阴平），燕然山，地名，勿读 yàn（燕子）")},
    {"w":"延","py":"yán","q":"单车欲问边，属国过居□","tip":fixq("「延」半包围，音 yán，居延，古地名，勿写~L~廷~R~（朝廷）~L~庭~R~（庭院）")},
]
DICT_NOTES=[
    {"w":"单车","q":"单车欲问边","a":"一辆车，形容随从少。单，一辆"},
    {"w":"问边","q":"单车欲问边","a":"到边塞去察看、慰问。问，慰问；边，边塞"},
    {"w":"属国","q":"属国过居延","a":"（shǔ guó）典属国的简称，汉代官名，这里指诗人出使边塞的身份"},
    {"w":"居延","q":"属国过居延","a":"（jū yán）古地名，在今内蒙古额济纳旗一带"},
    {"w":"征蓬","q":"征蓬出汉塞","a":"（zhēng péng）飘飞的蓬草，比喻漂泊不定的旅人"},
    {"w":"汉塞","q":"征蓬出汉塞","a":"汉朝的边塞，这里指唐朝的边塞（以汉代唐）"},
    {"w":"归雁","q":"归雁入胡天","a":"北归的大雁。归，返回"},
    {"w":"胡天","q":"归雁入胡天","a":"胡人的天空，指西北地区。胡，古代对北方少数民族的称呼"},
    {"w":"大漠","q":"大漠孤烟直","a":"广阔的沙漠。大，广阔；漠，沙漠"},
    {"w":"孤烟","q":"大漠孤烟直","a":"（gū yān）烽火台升起的狼烟。孤，单独；烟，狼烟"},
    {"w":"长河","q":"长河落日圆","a":"长长的河流，这里指黄河"},
    {"w":"萧关","q":"萧关逢候骑","a":"（xiāo guān）古关名，在今宁夏固原东南"},
    {"w":"候骑","q":"萧关逢候骑","a":"（hòu jì）骑马的侦察兵。候，侦察；骑，骑兵"},
    {"w":"都护","q":"都护在燕然","a":"（dū hù）唐代边疆最高军事长官，这里指河西节度使"},
    {"w":"燕然","q":"都护在燕然","a":"（yān rán）山名，即今蒙古国杭爱山，东汉窦宪刻石纪功于此"},
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
    <p>《使至塞上》是唐代诗人王维的代表作，作于唐玄宗开元二十五年（737）。当时王维以监察御史的身份出使凉州（今甘肃武威），慰问边塞将士，实际上是被排挤出朝廷。在赴边途中，他写下了这首千古传诵的五言律诗。</p>
    <p>全诗以~L~使至塞上~R~为题，写出使边塞的所见所感。首联叙事，颔联以征蓬归雁自比，颈联~L~大漠孤烟直，长河落日圆~R~写边塞奇特壮丽的风光，是千古传诵的名句，被誉为~L~千古壮观~R~。尾联以实写结尾，与首联呼应。全诗意境开阔，气势雄浑，是王维边塞诗的代表作，也是~L~诗中有画~R~的典范。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>王维（701—761），字摩诘，号摩诘居士，蒲州（今山西永济）人。唐代著名诗人、画家，官至尚书右丞，世称~L~王右丞~R~。他是盛唐山水田园诗派的代表人物，与孟浩然并称~L~王孟~R~。</p>
    <p>王维的诗歌风格清新淡远，意境优美，被誉为~L~诗中有画，画中有诗~R~（苏轼语）。他的边塞诗也写得气势雄浑、意境开阔，《使至塞上》是其边塞诗的代表作。晚年王维隐居辋川，吃斋奉佛，诗风更加恬淡空灵。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p><b>出使边塞：</b>开元二十五年（737），河西节度使崔希逸大破吐蕃，唐玄宗命王维以监察御史的身份出使凉州，慰问边塞将士。实际上，王维因张九龄罢相而受到牵连，被排挤出朝廷，这次出使是明升暗降。</p>
    <p><b>边塞风光：</b>王维在赴边途中，目睹了边塞奇特壮丽的风光——广阔的沙漠、笔直的狼烟、长长的黄河、圆圆的落日。这些景象与中原的秀丽山水截然不同，给诗人带来了强烈的视觉冲击，也激发了他的创作灵感。</p>
    <p><b>盛唐气象：</b>开元年间是唐朝的全盛时期，国力强盛，疆域辽阔，文人普遍有出塞从戎的热情。王维的《使至塞上》虽然写于被排挤之后，但诗中仍然充满了积极乐观的精神和开阔雄浑的气象，是盛唐气象的生动写照。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>《使至塞上》是一首<b>五言律诗</b>，全诗八句，每句五字，共四十字。首联叙事，颔联对仗，颈联对仗，尾联叙事。全诗格律严谨，对仗精工，是五言律诗的典范之作。</p>
    <p>诗题~L~使至塞上~R~，~L~使~R~是出使，~L~至~R~是到，~L~塞上~R~是边塞。全诗写诗人出使边塞途中的所见所感，是一首记行诗。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>《使至塞上》王维 诵读 潇然</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV18B4y1G7KB&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="使至塞上朗诵"></iframe>
        <a href="https://www.bilibili.com/video/BV18B4y1G7KB" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>《使至塞上》王维 名师讲解（央视出品）</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1Kk4y1J7cW&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="使至塞上名师讲解"></iframe>
        <a href="https://www.bilibili.com/video/BV1Kk4y1J7cW" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">王维——孤寂中见开阔的使者</div>
        <p>《使至塞上》中的抒情主人公，是一位被排挤出朝廷、出使边塞的使者形象。他虽然内心有孤寂和抑郁，但面对边塞的壮丽风光，胸襟变得开阔，精神变得昂扬。</p>
        <p><b>孤寂的使者：</b>~L~单车欲问边~R~，轻车简从，随从稀少，写出了诗人被排挤出朝廷的孤寂。~L~征蓬出汉塞，归雁入胡天~R~，以飘飞的蓬草和北归的大雁自比，写出了漂泊无依的感受。</p>
        <p><b>开阔的胸襟：</b>~L~大漠孤烟直，长河落日圆~R~，面对边塞奇特壮丽的风光，诗人的孤寂被壮美的景象所取代，胸襟变得开阔。~L~直~R~~L~圆~R~二字，写出了边塞的雄浑和壮美，也写出了诗人积极乐观的精神。</p>
        <p>这个形象，从孤寂到开阔，从抑郁到昂扬，体现了盛唐诗人即使在逆境中也能保持积极乐观的精神面貌，是盛唐气象的生动写照。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">诗中有画——大漠孤烟直，长河落日圆</div>
        <p>这两句是~L~诗中有画~R~的典范。广阔的沙漠是背景，一缕直烟是竖线，长长的黄河是横线，一轮圆日是圆点——点、线、面结合，构成了一幅奇特壮丽的边塞图。构图简洁，色彩鲜明，意境开阔，被誉为~L~千古壮观~R~。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">比喻自比——征蓬归雁</div>
        <p>~L~征蓬出汉塞，归雁入胡天~R~，以飘飞的蓬草和北归的大雁自比，既写了诗人出使边塞的行程，又含蓄地表达了被排挤出朝廷的孤寂和抑郁。以物喻人，情景交融，是王维诗歌的经典手法。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">首尾呼应，结构完整</div>
        <p>首联~L~单车欲问边~R~写出使的目的，尾联~L~都护在燕然~R~写出使的结果，首尾呼应，结构完整。全诗由叙事到抒情到写景再到叙事，层次分明，过渡自然。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">大漠孤烟直，长河落日圆。</div>
        <p>这是千古传诵的名句，被誉为~L~千古壮观~R~。~L~大漠~R~写环境的辽阔，~L~孤烟~R~写人烟的稀少，~L~直~R~字写出狼烟的挺拔有力；~L~长河~R~写黄河的绵延，~L~落日~R~写时间的黄昏，~L~圆~R~字写出落日的温暖壮美。在广阔的沙漠背景下，一缕直烟、一轮圆日，构成了一幅奇特壮丽的边塞图。~L~直~R~~L~圆~R~二字，炼字精绝，将边塞的雄浑和壮美写得淋漓尽致。这两句不仅写景逼真，更体现了诗人开阔的胸襟和积极乐观的精神，是王维~L~诗中有画，画中有诗~R~的典范。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>主题思想</h3>
    <p>《使至塞上》通过描写出使边塞途中的所见所感，抒发了诗人被排挤出朝廷的孤寂和抑郁，同时也表达了对边塞壮丽风光的赞美和对戍边将士的敬意，体现了盛唐诗人积极乐观的精神面貌。</p>
    <p>这首诗的深刻之处在于，它将个人的失意与国家的强盛融为一体——虽然诗人被排挤出朝廷，但面对边塞的壮丽风光和将士的赫赫战功，个人的失意被冲淡了，取而代之的是开阔的胸襟和昂扬的精神。这种在逆境中保持积极乐观的态度，正是盛唐气象的体现。</p>
  </div>
</section>
''')
ACC=fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">文体 · 字音形 · 文言 · 炼字 · 修辞 · 文化常识</span></div>
  <div class="box"><div class="acc-cat"><h3>文体与词牌</h3>
    <div class="acc-item"><span class="acc-w">五言律诗</span><span class="acc-d">《使至塞上》是五言律诗，全诗八句，每句五字，共四十字。颔联、颈联对仗。</span></div>
    <div class="acc-item"><span class="acc-w">边塞诗</span><span class="acc-d">以边塞风光、战争生活为题材的诗歌。盛唐边塞诗派代表有高适、岑参、王维、王昌龄等。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>易错字音形</h3>
    <div class="acc-item"><span class="acc-w">蓬</span><span class="acc-d">（péng）蓬草，草字头，勿写~L~篷~R~（竹字头）。</span></div>
    <div class="acc-item"><span class="acc-w">雁</span><span class="acc-d">（yàn）大雁，厂字头，勿写~L~燕~R~。</span></div>
    <div class="acc-item"><span class="acc-w">骑</span><span class="acc-d">（jì）骑兵，~L~候骑~R~，勿读 qí。</span></div>
    <div class="acc-item"><span class="acc-w">燕</span><span class="acc-d">（yān）燕然山，地名，勿读 yàn。</span></div>
    <div class="acc-item"><span class="acc-w">萧</span><span class="acc-d">（xiāo）萧关，草字头，勿写~L~箫~R~（竹字头）。</span></div>
  </div></div>
  <div class="box"><div class="acc-cat"><h3>文言梳理</h3>
    <div class="acc-sub">古今异义</div>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">属国</td><td>典属国（官名），指使者身份</td><td>附属国</td><td>属国过居延</td></tr>
      <tr><td class="kai">长河</td><td>黄河</td><td>长长的河流（泛指）</td><td>长河落日圆</td></tr>
      <tr><td class="kai">骑</td><td>骑兵（读 jì）</td><td>骑马（读 qí）</td><td>萧关逢候骑</td></tr>
    </table></div>
    <div class="acc-sub">一词多义</div>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="2">直</td><td>笔直（形容词）</td><td>大漠孤烟直</td></tr>
      <tr><td>一直、径直（副词）</td><td>直挂云帆济沧海</td></tr>
      <tr><td class="kai" rowspan="2">圆</td><td>圆形（形容词）</td><td>长河落日圆</td></tr>
      <tr><td>圆满（形容词）</td><td>花好月圆</td></tr>
    </table></div>
    <div class="acc-sub">文言句式</div>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">对偶句</td><td>征蓬出汉塞，归雁入胡天。</td><td>颔联对仗，名词对名词、动词对动词、名词对名词</td></tr>
      <tr><td class="kai">对偶句</td><td>大漠孤烟直，长河落日圆。</td><td>颈联对仗，名词对名词、形容词对形容词</td></tr>
      <tr><td class="kai">用典</td><td>都护在燕然</td><td>暗用东汉窦宪刻石燕然的典故</td></tr>
    </table></div>
  </div></div>
  <div class="box">
    <h3>炼字赏析（本文核心考点）</h3>
    <div class="glossary">
      <div class="g-item"><dt>直——大漠孤烟直</dt><dd>~L~直~R~字写出狼烟的挺拔有力，在广阔的沙漠背景下，一缕直烟显得格外醒目。一个~L~直~R~字，将边塞的雄浑和苍凉同时呈现，是全诗的炼字经典。</dd></div>
      <div class="g-item"><dt>圆——长河落日圆</dt><dd>~L~圆~R~字写出落日的形状，又大又圆，给人温暖壮美的感觉。一个~L~圆~R~字，将黄昏落日的壮美写得淋漓尽致，与~L~直~R~字形成对比，一直一圆，构图完美。</dd></div>
      <div class="g-item"><dt>孤——大漠孤烟直</dt><dd>~L~孤~R~字写出人烟的稀少，在广阔的沙漠中，只有一缕狼烟，更显边塞的辽阔和荒凉。~L~孤~R~字也暗含诗人的孤寂之感。</dd></div>
      <div class="g-item"><dt>大——大漠孤烟直</dt><dd>~L~大~R~字写出沙漠的辽阔无边，为~L~孤烟~R~和~L~落日~R~提供了广阔的背景，使画面更加雄浑壮观。</dd></div>
    </div>
  </div>
  <div class="box"><div class="acc-cat"><h3>修辞与手法</h3>
    <div class="acc-item"><span class="acc-w">比喻（自比）</span><span class="acc-d">~L~征蓬~R~~L~归雁~R~自比，写漂泊之感。</span></div>
    <div class="acc-item"><span class="acc-w">对偶</span><span class="acc-d">颔联、颈联皆对，对仗精工。</span></div>
    <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">~L~都护在燕然~R~暗用窦宪刻石燕然的典故。</span></div>
    <div class="acc-item"><span class="acc-w">诗中有画</span><span class="acc-d">~L~大漠孤烟直，长河落日圆~R~，点线面结合，构图完美。</span></div>
  </div></div>
  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>居延</dt><dd>古地名，在今内蒙古额济纳旗一带，是边塞要地。汉代在此设居延都尉，唐代为军事重镇。</dd></div>
      <div class="g-item"><dt>萧关</dt><dd>古关名，在今宁夏固原东南，是关中通向塞北的要道，为古代关中四大关之一。</dd></div>
      <div class="g-item"><dt>燕然</dt><dd>山名，即今蒙古国杭爱山。东汉窦宪大破匈奴后，在此刻石纪功（~L~燕然勒石~R~），后以~L~燕然~R~代指战功。</dd></div>
      <div class="g-item"><dt>都护</dt><dd>唐代边疆最高军事长官，统辖边防军政。唐太宗时设安西都护府，武则天时设北庭都护府。</dd></div>
      <div class="g-item"><dt>候骑</dt><dd>骑马的侦察兵。~L~候~R~是侦察、巡逻，~L~骑~R~读 jì，指骑兵。古代边塞设有候骑，负责侦察敌情。</dd></div>
      <div class="g-item"><dt>狼烟</dt><dd>古代边防报警时点燃的烟火。传说用狼粪燃烧，烟直而聚，风吹不斜，故称~L~狼烟~R~。诗中~L~孤烟~R~即指狼烟。</dd></div>
      <div class="g-item"><dt>边塞诗派</dt><dd>盛唐诗歌流派，以描写边塞风光、战争生活、将士情感为主要内容。代表诗人有高适、岑参、王维、王昌龄、李颀等。</dd></div>
    </div>
  </div>
</section>
''')
HTML=u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《使至塞上》王维</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">
<header class="hero"><div class="hero-side">唐 · 王维</div><h1 class="hero-title">使至塞上</h1></header>
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
<div class="sec-sub">全诗八句，分两部分：出使叙事、大漠风光。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
<div class="kai">《使至塞上》</div>
<div>王维 · 唐（701—761）· 开元二十五年出使凉州途中作 · 五言律诗</div>
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
