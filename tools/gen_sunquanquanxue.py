# -*- coding: utf-8 -*-
"""《孙权劝学》课件生成器 —— 复用《背影》课件的 CSS / JS 框架。"""
import json, re, html, io, os

LQ = '\u201c'
RQ = '\u201d'

SRC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'beiying-zhuziqing.html')
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sunquanquanxue-simaguang.html')

src = io.open(SRC, encoding='utf-8-sig').read()
CSS = src[src.index('<style>') + 7: src.index('</style>')]
s0 = src.index('<script>')
JS = src[s0 + 8: src.index('</script>', s0)]
JS = JS.replace('beiying_fs', 'sunquanquanxue_fs')


def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (html.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)


def fixq(s):
    return s.replace('~L~', LQ).replace('~R~', RQ)


# ---------------- 全文（背诵模式） ----------------
FULLTEXT = [
    "初，权谓吕蒙曰：",
    "~L~卿今当涂掌事，不可不学！~R~",
    "蒙辞以军中多务。",
    "权曰：",
    "~L~孤岂欲卿治经为博士邪！但当涉猎，见往事耳。",
    "卿言多务，孰若孤？孤常读书，自以为大有所益。~R~",
    "蒙乃始就学。",
    "及鲁肃过寻阳，与蒙论议，大惊曰：",
    "~L~卿今者才略，非复吴下阿蒙！~R~",
    "蒙曰：",
    "~L~士别三日，即更刮目相待，大兄何见事之晚乎！~R~",
    "肃遂拜蒙母，结友而别。",
]

# ---------------- 分部分 ----------------
PARTS = [
    ("第一部分", "孙权劝学 · 吕蒙始学", "第 1–7 句",
     "故事开端。孙权以~L~当涂掌事，不可不学~R~劝吕蒙读书，吕蒙以军中多务推辞。孙权现身说法，指出读书只需~L~涉猎，见往事~R~，并以自己常读书大有所益相劝。吕蒙深受触动，~L~乃始就学~R~。"),
    ("第二部分", "鲁肃惊赞 · 结友而别", "第 8–12 句",
     "故事发展与结局。鲁肃过寻阳，与蒙论议，大惊其才略已~L~非复吴下阿蒙~R~。吕蒙以~L~士别三日，即更刮目相待~R~回应，语带自豪。鲁肃遂拜蒙母，结友而别——以鲁肃的反应侧面烘托吕蒙就学后的惊人进步。"),
]

# 每句：(所属部分索引, 原文[带 [[词|注]] 标记], 译文, 赏析, [标签])
S = [
(0, "[[初|当初，起初，追述往事时常用的发端词]]，权[[谓|对……说，告诉]]吕蒙曰：",
 "当初，孙权对吕蒙说：",
 fixq("~L~初~R~字领起，点明这是一段往事的追述。~L~谓……曰~R~是文言中常见的对话格式，~L~对……说~R~。文章以孙权的劝拉开序幕，开门见山，直接进入核心事件——劝学。"),
 ["开篇", "对话"]),

(0, "~L~[[卿|（qīng）古代君对臣、上级对下级或朋友间的爱称，相当于~L~你~R~]]今[[当涂|当道，当权。涂，同~L~途~R~，道路]][[掌事|掌管事务。掌，掌管、主持；事，事务]]，不可不学！~R~",
 "~L~你现在当权掌管事务了，不可以不学习！~R~",
 fixq("孙权劝学的第一句话，斩钉截铁。~L~卿~R~是君对臣的爱称，见出孙权对吕蒙的亲近与器重。~L~当涂掌事~R~点明吕蒙身份已变——从单纯的武将变为当权者，这就需要学习。~L~不可不学~R~双重否定，语气强烈，既是要求，也是期望——孙权深知吕蒙勇武有余而学识不足，故以~L~不可不学~R~相劝。"),
 ["双重否定", "劝学"]),

(0, "蒙[[辞|推辞，推托]][[以|用，拿，介词]]军中多[[务|事务，事情]]。",
 "吕蒙用军中事务繁多来推辞。",
 fixq("吕蒙的反应——~L~辞以军中多务~R~。这是状语后置句，正常语序为~L~以军中多务辞~R~。吕蒙的推辞在情理之中：作为武将，他更看重军事，认为读书无用。这一推辞既符合吕蒙的身份性格，也为下文孙权的进一步劝说蓄势——只有先~L~辞~R~，孙权的~L~劝~R~才有针对性和说服力。"),
 ["状语后置", "蓄势"]),

(0, "权曰：",
 "孙权说：",
 fixq("简短的过渡，引出孙权的第二次劝说。面对吕蒙的推辞，孙权没有生气，而是耐心开导——这正是孙权作为君主的高明之处：不以权压人，而以理服人，以情动人。"),
 ["过渡", "以理服人"]),

(0, "~L~[[孤|古代王侯的自称，相当于~L~我~R~]][[岂|难道，怎么，表反问]]欲卿[[治经|研究儒家经典。治，研究；经，指《诗》《书》《礼》《易》《春秋》等经书]]为[[博士|（bó shì）当时专掌经学传授的学官（古今异义，今义：学位的最高一级）]][[邪|（yé）通~L~耶~R~，句末语气词，表反问，相当于~L~吗~R~]]！[[但|只，只是]]当[[涉猎|（shè liè）粗略地阅读，浏览。涉，趟水过河，引申为浏览；猎，打猎，引申为搜寻]]，[[见|了解，知道]][[往事|历史（古今异义，今义：过去的事情）]][[耳|罢了，句末语气词，表限止]]。",
 "~L~我难道想要你研究儒家经典成为专掌经学传授的学官吗！只是应当粗略地阅读，了解历史罢了。",
 fixq("孙权首先消除吕蒙的顾虑：~L~孤岂欲卿治经为博士邪~R~——我不是要你成为书呆子！~L~治经~R~~L~博士~R~都是当时儒生的事，武将不必如此。然后提出真正的要求：~L~但当涉猎，见往事耳~R~——只需泛读，了解历史。~L~但~R~~L~耳~R~两个限止词，把要求降到最低，减轻吕蒙的心理负担。~L~涉猎~R~一词精准，既不是~L~不治~R~，也不是~L~精研~R~，而是~L~粗略浏览~R~，非常适合武将的实际需要。"),
 ["古今异义", "通假字", "限止词"]),

(0, "卿言多务，[[孰若|哪里比得上。孰，谁、哪一个；若，比得上]]孤？孤常读书，自以为大有所益。~R~",
 "你说事务繁多，谁比得上我（事务多）呢？我经常读书，自认为大有益处。~R~",
 fixq("孙权现身说法，以自己为例说服吕蒙。~L~卿言多务，孰若孤~R~——你说忙，能比我还忙吗？这一反问极具说服力：孙权作为一国之君，事务远比吕蒙繁多，却仍~L~常读书~R~，吕蒙还有什么理由推辞？~L~自以为大有所益~R~，以亲身体验说明读书的好处，不是空谈大道理，而是实实在在的经验之谈。孙权劝学，既有要求，又有方法，还有榜样，层层递进，令人无法拒绝。"),
 ["现身说法", "反问", "层层递进"]),

(0, "蒙[[乃|于是，就]][[始|开始]][[就学|从事学习，开始读书。就，从事、接近；学，学习]]。",
 "吕蒙于是开始学习。",
 fixq("~L~乃始就学~R~，仅四字，写出吕蒙的转变。~L~乃~R~表顺承，~L~始~R~表开始，~L~就学~R~即从事学习。没有写吕蒙如何表态、如何刻苦，只用~L~乃始就学~R~一笔带过，语言极简。但正是这极简的一笔，为下文鲁肃的~L~大惊~R~埋下伏笔——吕蒙学了多久、学得怎样，全留给下文侧面烘托。这种~L~留白~R~的写法，是本文的艺术特色之一。"),
 ["留白", "一笔带过"]),

(1, "[[及|到，等到]]鲁肃[[过|经过，路过]]寻阳，与蒙[[论议|讨论商议。论，讨论；议，商议]]，大惊曰：",
 "等到鲁肃经过寻阳的时候，和吕蒙讨论商议，（鲁肃）非常吃惊地说：",
 fixq("时间跳跃，从~L~乃始就学~R~直接到~L~及鲁肃过寻阳~R~——中间吕蒙如何勤学苦读，一字未提，全留给读者想象。~L~大惊~R~二字是关键词：鲁肃是东吴名士，见识广博，能让他~L~大惊~R~，吕蒙的进步该有多大！以鲁肃的反应侧面烘托吕蒙就学的成效，比直接写吕蒙如何勤奋更有说服力。"),
 ["侧面烘托", "时间跳跃"]),

(1, "~L~卿[[今者|现在，如今。者，语气词，无实义]][[才略|才干和谋略。才，才干；略，谋略]]，[[非复|不再是。非，不；复，再]]吴下[[阿蒙|即吕蒙，阿是词头，有亲昵意味。吴下阿蒙，指原来那个才疏学浅的吕蒙]]！~R~",
 "~L~你现在的才干和谋略，不再是原来那个吴下阿蒙了！~R~",
 fixq("鲁肃的惊叹，是全文最精彩的侧面描写。~L~卿今者才略，非复吴下阿蒙~R~——以~L~今者~R~与~L~吴下阿蒙~R~对比，突出吕蒙变化之大。~L~吴下阿蒙~R~后来成为成语，特指原来才疏学浅的人。鲁肃的~L~大惊~R~和这句赞叹，从侧面写出了吕蒙就学后的惊人进步——不需要写吕蒙如何勤奋，只需要写鲁肃的反应，效果便跃然纸上。"),
 ["侧面描写", "成语来源", "对比"]),

(1, "蒙曰：",
 "吕蒙说：",
 fixq("简短过渡，引出吕蒙的回应。面对鲁肃的惊叹，吕蒙没有谦虚，也没有得意忘形，而是说出了一句流传千古的名言——这正是吕蒙自信与豁达的体现。"),
 ["过渡"]),

(1, "~L~[[士别三日|读书人分别几天。士，读书人；三，虚指，几；日，天]]，即[[更|（gēng）重新，另]][[刮目相待|用新的眼光看待。刮目，擦擦眼睛，指另眼相看；相待，看待]]，[[大兄|长兄，这里是对鲁肃的尊称]][[何|为什么]][[见事|认清事物。见，认识、认清；事，事物]]之[[晚|迟，晚]]乎！~R~",
 "~L~读书人分别几天，就应该用新的眼光看待（他），长兄为什么认清事物这么晚呢！~R~",
 fixq("吕蒙的回应，是全文的点睛之笔。~L~士别三日，即更刮目相待~R~，以~L~士~R~自称，见出吕蒙对自己身份的新认知——他已不再是那个只知打仗的~L~吴下阿蒙~R~，而是一个有学识、有见地的~L~士~R~了。~L~刮目相待~R~后来成为成语，指用新的眼光看待人。~L~大兄何见事之晚乎~R~，以反问调侃鲁肃，语带自豪而不失亲切，见出吕蒙性格中坦率幽默的一面。这句话既是对鲁肃惊叹的回应，也是对~L~学习改变人~R~这一主题的升华。"),
 ["点睛之笔", "成语来源", "反问"]),

(1, "肃[[遂|于是，就]][[拜|拜见，拜访]]蒙母，[[结友|结交为朋友。结，结交；友，朋友]]而[[别|告别，离别]]。",
 "鲁肃于是拜见了吕蒙的母亲，（和吕蒙）结交为朋友，然后告别。",
 fixq("故事结局。~L~拜蒙母~R~是古代的一种隆重礼节——拜见朋友的母亲，表示对朋友的尊重和对友谊的郑重。鲁肃本是东吴名士，地位高于吕蒙，却主动~L~拜蒙母，结友而别~R~，这一行动比~L~大惊~R~更有分量：他不仅在口头上赞叹吕蒙的进步，更在行动上认可了吕蒙的才学和地位。以~L~结友而别~R~收束全文，含蓄而有力——学习不仅改变了吕蒙的才略，也改变了他在士大夫心中的地位。"),
 ["结局", "行动描写", "含蓄收束"]),
]


# ---------------- 题库 ----------------
DICT_WORDS = [
    {"w":"卿","py":"qīng","q":"□今当涂掌事","tip":fixq("「卿」卯字旁，音 qīng，君对臣的爱称，勿写~L~乡~R~~L~即~R~")},
    {"w":"涂","py":"tú","q":"当□掌事","tip":fixq("「涂」三点水，音 tú，同~L~途~R~，意为道路，勿写~L~途~R~~L~图~R~")},
    {"w":"辞","py":"cí","q":"蒙□以军中多务","tip":fixq("「辞」辛字旁，音 cí，意为推辞，勿写~L~词~R~~L~祠~R~")},
    {"w":"涉","py":"shè","q":"但当□猎","tip":fixq("「涉」三点水，音 shè，意为浏览，勿写~L~步~R~~L~摄~R~")},
    {"w":"猎","py":"liè","q":"但当涉□","tip":fixq("「猎」反犬旁，音 liè，意为搜寻，勿写~L~腊~R~~L~蜡~R~")},
    {"w":"博","py":"bó","q":"治经为□士","tip":fixq("「博」十字旁，音 bó，意为广博，勿写~L~搏~R~~L~膊~R~")},
    {"w":"邪","py":"yé","q":"为博士□","tip":fixq("「邪」右耳旁，此处读 yé，通~L~耶~R~，语气词，勿读 xié")},
    {"w":"孰","py":"shú","q":"□若孤","tip":fixq("「孰」子字底，音 shú，意为谁、哪一个，勿写~L~熟~R~~L~塾~R~")},
    {"w":"略","py":"lüè","q":"卿今者才□","tip":fixq("「略」田字旁，音 lüè，意为谋略，勿写~L~掠~R~~L~各~R~")},
    {"w":"刮","py":"guā","q":"即更□目相待","tip":fixq("「刮」立刀旁，音 guā，意为擦，勿写~L~乱~R~~L~括~R~")},
    {"w":"更","py":"gēng","q":"即□刮目相待","tip":fixq("「更」曰字底，此处读 gēng，意为重新，勿读 gèng")},
    {"w":"遂","py":"suì","q":"肃□拜蒙母","tip":fixq("「遂」走之底，音 suì，意为于是、就，勿写~L~逐~R~~L~隧~R~")},
    {"w":"蒙","py":"méng","q":"肃拜□母","tip":fixq("「蒙」草字头，音 méng，吕蒙的名，勿写~L~朦~R~~L~濛~R~")},
    {"w":"涉猎","py":"shè liè","q":"但当□□","tip":fixq("「涉」三点水音 shè，「猎」反犬旁音 liè，意为粗略阅读")},
    {"w":"博士","py":"bó shì","q":"治经为□□","tip":fixq("「博」十字旁音 bó，「士」独体字音 shì，古指学官，今指学位")},
    {"w":"往事","py":"wǎng shì","q":"见□□耳","tip":fixq("「往」彳旁音 wǎng，「事」独体字音 shì，古义为历史")},
    {"w":"才略","py":"cái lüè","q":"卿今者□□","tip":fixq("「才」独体字音 cái，「略」田字旁音 lüè，意为才干谋略")},
    {"w":"吴下","py":"wú xià","q":"非复□□阿蒙","tip":fixq("「吴」口字底音 wú，「下」独体字音 xià，指吴地")},
    {"w":"阿蒙","py":"ā méng","q":"非复吴下□□","tip":fixq("「阿」左耳旁音 ā，词头；「蒙」草字头音 méng，指吕蒙")},
    {"w":"刮目","py":"guā mù","q":"即更□□相待","tip":fixq("「刮」立刀旁音 guā，「目」独体字音 mù，意为另眼相看")},
]

DICT_NOTES = [
    {"w":"初","q":"初，权谓吕蒙曰","a":"当初，起初，追述往事的发端词"},
    {"w":"谓","q":"权谓吕蒙曰","a":"对……说，告诉"},
    {"w":"卿","q":"卿今当涂掌事","a":"（qīng）古代君对臣或朋友间的爱称，相当于~L~你~R~"},
    {"w":"当涂","q":"卿今当涂掌事","a":"当道，当权。涂，同~L~途~R~，道路"},
    {"w":"掌事","q":"卿今当涂掌事","a":"掌管事务。掌，掌管、主持"},
    {"w":"辞","q":"蒙辞以军中多务","a":"推辞，推托"},
    {"w":"以","q":"蒙辞以军中多务","a":"用，拿，介词"},
    {"w":"务","q":"蒙辞以军中多务","a":"事务，事情"},
    {"w":"孤","q":"孤岂欲卿治经为博士邪","a":"古代王侯的自称，相当于~L~我~R~"},
    {"w":"岂","q":"孤岂欲卿治经为博士邪","a":"难道，怎么，表反问"},
    {"w":"治经","q":"孤岂欲卿治经为博士邪","a":"研究儒家经典。治，研究；经，经书"},
    {"w":"博士","q":"孤岂欲卿治经为博士邪","a":"（bó shì）当时专掌经学传授的学官（古今异义）"},
    {"w":"邪","q":"孤岂欲卿治经为博士邪","a":"（yé）通~L~耶~R~，句末语气词，表反问"},
    {"w":"但","q":"但当涉猎","a":"只，只是"},
    {"w":"涉猎","q":"但当涉猎","a":"（shè liè）粗略地阅读，浏览"},
    {"w":"见","q":"见往事耳","a":"了解，知道"},
    {"w":"往事","q":"见往事耳","a":"历史（古今异义，今义：过去的事情）"},
    {"w":"耳","q":"见往事耳","a":"罢了，句末语气词，表限止"},
    {"w":"孰若","q":"孰若孤","a":"哪里比得上。孰，谁、哪一个；若，比得上"},
    {"w":"益","q":"自以为大有所益","a":"益处，好处"},
    {"w":"乃","q":"蒙乃始就学","a":"于是，就"},
    {"w":"始","q":"蒙乃始就学","a":"开始"},
    {"w":"就学","q":"蒙乃始就学","a":"从事学习，开始读书。就，从事、接近"},
    {"w":"及","q":"及鲁肃过寻阳","a":"到，等到"},
    {"w":"过","q":"及鲁肃过寻阳","a":"经过，路过"},
    {"w":"论议","q":"与蒙论议","a":"讨论商议。论，讨论；议，商议"},
    {"w":"今者","q":"卿今者才略","a":"现在，如今。者，语气词，无实义"},
    {"w":"才略","q":"卿今者才略","a":"才干和谋略。才，才干；略，谋略"},
    {"w":"非复","q":"非复吴下阿蒙","a":"不再是。非，不；复，再"},
    {"w":"吴下阿蒙","q":"非复吴下阿蒙","a":"指原来才疏学浅的吕蒙。阿，词头，有亲昵意味"},
    {"w":"士别三日","q":"士别三日","a":"读书人分别几天。士，读书人；三，虚指，几"},
    {"w":"更","q":"即更刮目相待","a":"（gēng）重新，另"},
    {"w":"刮目相待","q":"即更刮目相待","a":"用新的眼光看待。刮目，擦擦眼睛，指另眼相看"},
    {"w":"大兄","q":"大兄何见事之晚乎","a":"长兄，对鲁肃的尊称"},
    {"w":"何","q":"大兄何见事之晚乎","a":"为什么"},
    {"w":"见事","q":"大兄何见事之晚乎","a":"认清事物。见，认识、认清"},
    {"w":"晚","q":"大兄何见事之晚乎","a":"迟，晚"},
    {"w":"遂","q":"肃遂拜蒙母","a":"于是，就"},
    {"w":"拜","q":"肃遂拜蒙母","a":"拜见，拜访"},
    {"w":"结友","q":"结友而别","a":"结交为朋友。结，结交"},
    {"w":"别","q":"结友而别","a":"告别，离别"},
]


# ---------------- 组装 ----------------
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
full_html = '\n'.join('    <div class="pl">%s</div>' % fixq(p) for p in FULLTEXT)

anno_count = sum(txt.count('[[') for (_, txt, _, _, _) in S)

BG = fixq(u'''
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《孙权劝学》选自北宋司马光主持编纂的编年体通史《资治通鉴》，文章通过孙权劝吕蒙读书、吕蒙就学后才略大进的故事，说明了~L~学习可以改变人~R~的道理，也展现了孙权善于劝学、吕蒙虚心受教的品格。</p>
    <p>全文仅一百一十九字，却叙事完整、对话生动、人物鲜明，是中国古代笔记散文中的精品，也是初中语文的经典篇目。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>司马光（1019—1086），字君实，号迂叟，陕州夏县（今山西夏县）人，北宋著名政治家、史学家、文学家。宝元元年进士，官至尚书左仆射兼门下侍郎。死后追封温国公，谥文正，世称司马温公。</p>
    <p>司马光最大的贡献是主持编纂了中国历史上第一部编年体通史《资治通鉴》。该书历时十九年完成，共二百九十四卷，记载了从战国到五代共一千三百六十二年的历史，以~L~鉴于往事，有资于治道~R~为宗旨，是中国古代史学的不朽巨著。</p>
    <p class="note">※ 司马光为人温良谦恭、刚正不阿，其人格堪称儒学教化下的典范，历来受人景仰。他与王安石政见不同，是旧党领袖。</p>
  </div>
  <div class="box">
    <h3>创作背景</h3>
    <p><b>《资治通鉴》：</b>宋神宗认为此书~L~鉴于往事，有资于治道~R~，赐名《资治通鉴》。全书以时间为纲、事件为目，体例严谨，脉络清晰，是与《史记》并列的史学双璧。《孙权劝学》即选自《资治通鉴·汉纪》，记载的是东汉建安年间的事。</p>
    <p><b>历史背景：</b>吕蒙（178—219），字子明，汝南富陂（今安徽阜南）人，三国时吴国名将。他早年从军，以勇猛著称，但文化水平不高。孙权劝他读书后，他笃志不倦，终成一代儒将，后来设计袭取荆州，击败关羽，是吴国的重要将领。</p>
    <p><b>写作意图：</b>司马光选取这段史料，意在说明学习的重要性——即使是已成名的武将，通过学习也能获得巨大进步。同时也展现了孙权作为君主的知人善任和善于劝学。</p>
  </div>
  <div class="box">
    <h3>体裁说明</h3>
    <p>本文是一篇史传散文，选自编年体通史《资治通鉴》。史传散文以叙事为主，通过人物的言行来展现人物性格和历史事件。本文篇幅极短，却完整地叙述了~L~劝学—就学—赞学~R~的全过程，以对话推动情节，以侧面描写烘托人物，是史传散文中~L~以小见大~R~的典范。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>诵读经典：《孙权劝学》司马光</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1WW4y167Fw&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="诵读经典《孙权劝学》"></iframe>
        <a href="https://www.bilibili.com/video/BV1WW4y167Fw" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>《孙权劝学》小动画：吕蒙就学的来龙去脉</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1aY411v7pE&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="孙权劝学小动画"></iframe>
        <a href="https://www.bilibili.com/video/BV1aY411v7pE" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>
''')

APP = fixq(u'''
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>人物形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">孙权：善于劝学的明君</div>
        <p>孙权是一位慧眼识人、善于劝学的明君。他看到吕蒙~L~当涂掌事~R~却学识不足，便主动劝其学习。他的劝学不是简单的命令，而是有步骤、有方法的：先指出~L~不可不学~R~的必要性，再消除吕蒙~L~治经为博士~R~的顾虑，提出~L~涉猎，见往事~R~的具体方法，最后现身说法~L~孤常读书，自以为大有所益~R~。既有要求，又有方法，还有榜样，层层递进，令人无法拒绝。他不以权压人，而以理服人、以情动人，是一位高明的领导者。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">吕蒙：虚心受教的将才</div>
        <p>吕蒙是一位知错能改、虚心受教的将才。他起初以~L~军中多务~R~推辞读书，但在孙权的耐心劝说下，~L~乃始就学~R~，而且一旦开始便笃志不倦。他的进步是惊人的——鲁肃的~L~大惊~R~和~L~非复吴下阿蒙~R~的赞叹，从侧面写出了他就学后的巨大变化。面对鲁肃的惊叹，他以~L~士别三日，即更刮目相待~R~回应，语带自豪而不失豁达，见出他性格中坦率自信的一面。从~L~吴下阿蒙~R~到令人~L~刮目相待~R~，吕蒙的转变正是学习力量的最好证明。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">鲁肃：敬才爱才的名士</div>
        <p>鲁肃是一位敬才爱才的东吴名士。他过寻阳时与蒙论议，~L~大惊~R~于吕蒙的进步，脱口而出~L~非复吴下阿蒙~R~——这份惊叹出自真心，毫无虚饰。更难得的是，他不仅在口头上赞叹，更在行动上~L~拜蒙母，结友而别~R~，以隆重的礼节表达对吕蒙才学的认可和尊重。鲁肃在文中既是陪衬人物，又是吕蒙变化的~L~见证人~R~——他的反应比任何直接描写都更有说服力。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">以对话推动情节，言简意丰</div>
        <p>全文以对话为主，孙权的两次劝说、吕蒙的一句回应、鲁肃的一句惊叹，构成了完整的叙事链条。每个人的话都符合其身份性格：孙权的话循循善诱、层层递进；吕蒙的话坦率自信、语带幽默；鲁肃的话直抒胸臆、惊叹由衷。对话不仅推动了情节发展，更塑造了鲜明的人物形象，可谓~L~言简意丰~R~。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">侧面描写，以小见大</div>
        <p>文章写吕蒙就学，没有正面描写他如何勤奋苦读，而是通过鲁肃的~L~大惊~R~和~L~非复吴下阿蒙~R~的赞叹来侧面烘托。这种~L~不写之写~R~的手法，给读者留下了广阔的想象空间，效果比直接描写更好。~L~乃始就学~R~一笔带过，~L~及鲁肃过寻阳~R~时间跳跃，中间的勤学过程全留给读者想象——以极简的笔墨写出极丰富的内容，是本文最突出的艺术特色。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比鲜明，主题突出</div>
        <p>文章多处运用对比：孙权的~L~不可不学~R~与吕蒙的~L~辞以军中多务~R~对比，见出劝学与拒学的矛盾；吕蒙~L~乃始就学~R~前后的变化对比，以~L~吴下阿蒙~R~与~L~今者才略~R~对举，见出学习的巨大力量；鲁肃的~L~大惊~R~与吕蒙的~L~自信~R~对比，见出人物性格的差异。对比之中，~L~学习改变人~R~的主题自然凸显。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">详略得当，结构紧凑</div>
        <p>全文仅一百一十九字，却完整地叙述了~L~劝学—就学—赞学~R~三个阶段。劝学部分详写孙权的两次劝说，因为这是故事的核心；就学部分仅~L~乃始就学~R~四字，因为过程可以省略；赞学部分详写鲁肃的惊叹和吕蒙的回应，因为这是主题的升华。详略得当，结构紧凑，无一字多余，是短篇叙事的典范。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">士别三日，即更刮目相待。</div>
        <p>吕蒙的名言，也是全文的点睛之笔。~L~士别三日~R~极言时间之短，~L~即更刮目相待~R~极言变化之大——分别才几天，就应该用新的眼光看待。这句话以~L~士~R~自称，见出吕蒙对自己身份的新认知；以~L~刮目~R~为喻，生动形象地写出了~L~另眼相看~R~的含义。后来~L~士别三日，当刮目相待~R~和~L~刮目相看~R~都成为成语，广泛流传。这句话既是吕蒙对鲁肃惊叹的回应，也是对~L~学习改变人~R~这一主题的升华。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">卿今者才略，非复吴下阿蒙！</div>
        <p>鲁肃的惊叹，是全文最精彩的侧面描写。~L~今者才略~R~与~L~吴下阿蒙~R~形成鲜明对比，突出吕蒙变化之大。~L~吴下阿蒙~R~后来成为成语，特指原来才疏学浅的人。鲁肃的这句话出自真心，毫无虚饰——作为东吴名士，他的评价具有权威性。以鲁肃的~L~大惊~R~和这句赞叹来写吕蒙的进步，比直接写吕蒙如何勤奋更有说服力，是~L~不写之写~R~的典范。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">但当涉猎，见往事耳。</div>
        <p>孙权劝学的核心方法论。~L~但~R~~L~耳~R~两个限止词，把读书的要求降到最低——不需要~L~治经为博士~R~，只需要~L~涉猎~R~（泛读），目的是~L~见往事~R~（了解历史）。这一要求非常务实，既消除了吕蒙的畏难情绪，又指明了读书的方向。~L~涉猎~R~一词精准，既不是~L~不治~R~，也不是~L~精研~R~，而是适合武将的~L~粗略浏览~R~。孙权劝学，不是要吕蒙成为学者，而是要他成为有见识的当权者——这正是孙权的高明之处。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《孙权劝学》通过孙权劝吕蒙读书、吕蒙就学后才略大进、鲁肃惊叹结友的故事，说明了~L~学习可以改变人~R~的深刻道理，同时也展现了孙权善于劝学、吕蒙虚心受教、鲁肃敬才爱才的美好品格。</p>
    <p>文章的深刻之处，在于它不是空洞地说教~L~要好好学习~R~，而是通过具体的人物和事件，让读者自己感受到学习的力量。吕蒙从~L~吴下阿蒙~R~到令人~L~刮目相待~R~，变化是惊人的，而这变化的根源就是~L~乃始就学~R~。同时，文章也告诉我们：学习不在于时间多少，而在于是否开始；不在于学历高低，而在于是否用心。孙权的劝学方法——提出要求、消除顾虑、指明方法、现身说法——也值得今天的教育者借鉴。</p>
  </div>
</section>
''')

ACC = fixq(u'''
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 一词多义 · 活用 · 句式 · 文化常识</span></div>

  <div class="box">
    <h3>通假字</h3>
    <div class="tw"><table>
      <tr><th>字</th><th>通假</th><th>例句</th><th>释义</th></tr>
      <tr><td class="kai">邪</td><td>通~L~耶~R~</td><td>孤岂欲卿治经为博士邪</td><td>句末语气词，表反问，相当于~L~吗~R~</td></tr>
      <tr><td class="kai">涂</td><td>同~L~途~R~</td><td>卿今当涂掌事</td><td>道路。当涂，当道、当权</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>古今异义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>古义</th><th>今义</th><th>例句</th></tr>
      <tr><td class="kai">博士</td><td>当时专掌经学传授的学官</td><td>学位的最高一级</td><td>孤岂欲卿治经为博士邪</td></tr>
      <tr><td class="kai">往事</td><td>历史</td><td>过去的事情</td><td>见往事耳</td></tr>
      <tr><td class="kai">但</td><td>只，只是</td><td>但是（表转折）</td><td>但当涉猎</td></tr>
      <tr><td class="kai">孤</td><td>古代王侯的自称</td><td>孤单，孤独</td><td>孤岂欲卿治经为博士邪</td></tr>
      <tr><td class="kai">治</td><td>研究</td><td>治理，医治</td><td>孤岂欲卿治经为博士邪</td></tr>
      <tr><td class="kai">过</td><td>经过，路过</td><td>经过（时间）；超过</td><td>及鲁肃过寻阳</td></tr>
      <tr><td class="kai">更</td><td>重新，另（读 gēng）</td><td>更加（读 gèng）</td><td>即更刮目相待</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>一词多义</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="3">以</td><td>用，拿，介词</td><td>蒙辞以军中多务</td></tr>
      <tr><td>认为，动词</td><td>自以为大有所益</td></tr>
      <tr><td>来，表目的，连词</td><td>以光先帝遗德（《出师表》）</td></tr>
      <tr><td class="kai" rowspan="2">当</td><td>应当，应该</td><td>但当涉猎</td></tr>
      <tr><td>掌管，主持</td><td>卿今当涂掌事</td></tr>
      <tr><td class="kai" rowspan="2">见</td><td>了解，知道</td><td>见往事耳</td></tr>
      <tr><td>认清，识别</td><td>大兄何见事之晚乎</td></tr>
      <tr><td class="kai" rowspan="2">就</td><td>从事，接近</td><td>蒙乃始就学</td></tr>
      <tr><td>完成，达到</td><td>自是指物作诗立就（《伤仲永》）</td></tr>
      <tr><td class="kai" rowspan="2">乃</td><td>于是，就</td><td>蒙乃始就学</td></tr>
      <tr><td>才，这才</td><td>乃悟前狼假寐（《狼》）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>词类活用</h3>
    <div class="tw"><table>
      <tr><th>词</th><th>活用类型</th><th>释义</th><th>例句</th></tr>
      <tr><td colspan="4" class="kai">（本文无典型词类活用）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文言句式</h3>
    <div class="tw"><table>
      <tr><th>句式</th><th>例句</th><th>说明</th></tr>
      <tr><td class="kai">状语后置</td><td>蒙辞以军中多务</td><td>正常语序为~L~蒙以军中多务辞~R~，~L~以军中多务~R~是状语</td></tr>
      <tr><td class="kai">反问句</td><td>孤岂欲卿治经为博士邪</td><td>~L~岂……邪~R~表反问，~L~难道……吗~R~</td></tr>
      <tr><td class="kai">反问句</td><td>大兄何见事之晚乎</td><td>~L~何……乎~R~表反问，~L~为什么……呢~R~</td></tr>
      <tr><td class="kai">省略句</td><td>（肃）与蒙论议</td><td>承前省略主语~L~肃~R~</td></tr>
      <tr><td class="kai">省略句</td><td>（蒙）结友而别</td><td>承前省略主语~L~蒙~R~（肃与蒙结友）</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <div class="glossary">
      <div class="g-item"><dt>《资治通鉴》</dt><dd>北宋司马光主持编纂的中国第一部编年体通史，共二百九十四卷，记载从战国到五代一千三百六十二年的历史。宋神宗以~L~鉴于往事，有资于治道~R~赐名。与《史记》并称~L~史学双璧~R~。</dd></div>
      <div class="g-item"><dt>编年体</dt><dd>中国传统史书的一种体裁，以时间为中心，按年、月、日顺序记述史事。《春秋》是中国最早的编年体史书，《资治通鉴》是编年体通史的巅峰之作。</dd></div>
      <div class="g-item"><dt>卿</dt><dd>古代高级官名，也是君对臣、上级对下级或朋友间的爱称，相当于~L~你~R~。文中孙权称吕蒙为~L~卿~R~，见出君臣之间的亲近关系。</dd></div>
      <div class="g-item"><dt>孤</dt><dd>古代王侯的自称，相当于~L~我~R~。春秋战国时期诸侯自称~L~孤~R~或~L~寡人~R~，三国时孙权仍沿用此称。</dd></div>
      <div class="g-item"><dt>治经</dt><dd>研究儒家经典。~L~经~R~指《诗》《书》《礼》《易》《春秋》等儒家经书。汉代以来，治经是儒生的主要学业，~L~博士~R~则是专掌经学传授的学官。</dd></div>
      <div class="g-item"><dt>吴下阿蒙</dt><dd>成语，指原来才疏学浅的人。吴下，指吴地；阿蒙，指吕蒙（阿是词头，有亲昵意味）。鲁肃以~L~非复吴下阿蒙~R~赞叹吕蒙的进步，后遂用为典故。</dd></div>
      <div class="g-item"><dt>刮目相待</dt><dd>成语，也作~L~刮目相看~R~，指用新的眼光看待人。刮目，擦擦眼睛，指去掉旧印象，另眼相看。吕蒙以~L~士别三日，即更刮目相待~R~回应鲁肃的惊叹，后遂用为成语。</dd></div>
      <div class="g-item"><dt>拜蒙母</dt><dd>古代拜见朋友母亲的礼节，表示对朋友的尊重和对友谊的郑重。鲁肃本是东吴名士，地位高于吕蒙，却主动拜蒙母、结友而别，见出他对吕蒙才学的高度认可。</dd></div>
      <div class="g-item"><dt>吕蒙</dt><dd>（178—219）字子明，汝南富陂人，三国时吴国名将。早年以勇猛著称，经孙权劝学后笃志不倦，终成儒将。后设计袭取荆州，击败关羽，是吴国的重要将领。~L~白衣渡江~R~即其经典战例。</dd></div>
    </div>
  </div>
</section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《孙权劝学》司马光</title>
<style>
%(css)s
</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">宋 · 司马光</div>
  <h1 class="hero-title">孙权劝学</h1>
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
  <div class="sec-sub">全文分两部分：孙权劝学吕蒙始学、鲁肃惊赞结友而别。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="kai">《孙权劝学》</div>
  <div>司马光 · 北宋（1019—1086）· 字君实，《资治通鉴》</div>
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
