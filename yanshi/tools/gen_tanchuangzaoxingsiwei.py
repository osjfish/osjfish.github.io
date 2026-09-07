# -*- coding: utf-8 -*-
"""生成《谈创造性思维》罗迦·费·因格 课件"""
import re, json

OUT = r"D:\App\Apps\yanshi\tanchuangzaoxingsiwei-luojiafeiyinge.html"
TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"

with open(TEMPLATE, 'r', encoding='utf-8') as f:
    tpl = f.read()

style_m = re.search(r'<style>(.*?)</style>', tpl, re.DOTALL)
CSS = style_m.group(1)
CSS += '\n  .acc-sub{font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:14px 0 6px;font-size:calc(16px*var(--fs));color:var(--teal-deep)}\n'

script_m = re.search(r'(<script>\s*\(function\(\)\{.*?</script>)', tpl, re.DOTALL)
JS_IIFE = script_m.group(1)
JS_IIFE = JS_IIFE.replace('beiying_fs', 'tancz_fs')

# ============ 课文数据 ============
PARAS = [
    (
        '对于上面这个问题，你是怎么回答的呢？你若选择的是B，那就恭喜你答对了。因为图形B是唯一一个仅由直线构成的图形。',
        '以图形选择题开篇，指出选B是正确答案，因为B是唯一仅由直线构成的图形。',
        '设置悬念，以问题引入，激发读者思考。用\u201c恭喜你答对了\u201d的口语化表达，拉近与读者的距离，为下文\u201c答案不止一个\u201d的论述做铺垫。',
        [
            ('仅由', '只由、仅仅由'),
            ('构成', '组成、造成'),
        ]
    ),
    (
        '不过，也许有人会选择图形C。因为非对称性图形只有C一个，所以C会被认为与其他图形不同。确实如此，这也是正确答案。答A也是可以的。因为A是唯一没有角的图形，所以A也是正确答案。那么，D又怎样呢？这是唯一一个由直线与曲线构成的图形，因此D也是正确答案。换句话说，由于看图形的角度不同，四种答案全都正确。',
        '逐一分析C、A、D也都是正确答案，得出结论：看图形的角度不同，四种答案全都正确。',
        '层层推进，分别从非对称性、没有角、直线与曲线构成三个角度论证C、A、D的正确性。以设问句\u201c那么，D又怎样呢？\u201d过渡，节奏明快。结尾\u201c换句话说\u201d总结点题，水到渠成地引出\u201c答案不止一个\u201d的核心观点。',
        [
            ('非对称性', '不具有对称的性质，即左右或上下不能重合'),
            ('确实如此', '的确是这样'),
            ('曲线', '弯曲的线，与直线相对'),
            ('换句话说', '用另一种说法来表达，换个说法'),
            ('角度', '看问题的出发点、立场'),
        ]
    ),
    (
        '\u201c正确答案只有一个\u201d这种思维模式，在我们头脑中已不知不觉地根深蒂固。事实上，若是某种数学问题的话，说正确答案只有一个是对的。麻烦的是，生活中大部分事物并不像某种数学问题那样。生活中解决问题的方法并非只有一个，而是多种多样。由于情况的变化，原来行之有效的方法，到了现在往往不灵了。正因为如此，如果你认为正确答案只有一个的话，当你找到某个答案以后，就会止步不前。因此，不满足于一个答案，不放弃探求，这一点非常重要。',
        '指出\u201c正确答案只有一个\u201d的思维模式根深蒂固，但生活中解决问题的方法多种多样，因此不满足于一个答案、不放弃探求非常重要。',
        '先让步承认数学问题中答案唯一，再以\u201c麻烦的是\u201d转折，指出生活中事物的复杂性。因果论证：情况变化→旧方法不灵→认为答案唯一会止步不前→因此要不满足于一个答案。逻辑链条清晰，层层递进。\u201c根深蒂固\u201d\u201c行之有效\u201d\u201c止步不前\u201d等成语准确凝练。',
        [
            ('思维模式', '思维的固定方式、范式'),
            ('不知不觉', '没有意识到、无意中'),
            ('根深蒂固', '比喻基础深厚，不容易动摇'),
            ('若是', '如果是、假如是'),
            ('多种多样', '各种各样、种类繁多'),
            ('行之有效', '实行起来有成效，指某种方法或措施已经实行过，证明很有效用'),
            ('不灵了', '不起作用了、失效了'),
            ('止步不前', '停止脚步，不再前进，比喻安于现状'),
            ('探求', '探索追求'),
        ]
    ),
    (
        '可以说，寻求第二种答案，或是解决问题的其他路径和新的方法，有赖于创造性的思维。那么，创造性的思维必须具备哪些条件呢？',
        '承上启下，指出寻求第二种答案有赖于创造性思维，并以设问引出下文对创造性思维条件的论述。',
        '过渡段，\u201c可以说\u201d承接上文结论，\u201c有赖于\u201d引出创造性思维的重要性。以设问句\u201c创造性的思维必须具备哪些条件呢？\u201d结尾，既引发读者思考，又自然引出下文的论述，起到纲举目张的作用。',
        [
            ('有赖于', '要依靠、取决于'),
            ('创造性的思维', '能产生新思想、新发现的思维方式'),
            ('必须具备', '一定要拥有、不可缺少'),
        ]
    ),
    (
        '有人是这样回答的：富有创造性的人总是孜孜不倦地汲取知识，使自己学识渊博。从古代史到现代技术，从数学到插花，不精通各种知识就一事无成。因为这些知识随时都可能进行组合，形成新的创意。这种情况可能出现在六分钟之后，也可能在六个月之后，六年之后。但当事人坚信它一定会出现。',
        '引用他人观点，指出富有创造性的人总是孜孜不倦地汲取知识，因为知识随时可能组合形成新创意。',
        '道理论证（引用），以\u201c有人是这样回答的\u201d引出他人观点。\u201c从古代史到现代技术，从数学到插花\u201d以夸张的范围列举，强调知识广博的重要性。\u201c六分钟之后\u201d\u201c六个月之后\u201d\u201d六年之后\u201c三个时间短语构成排比，说明创意出现的时间不确定，但\u201d坚信它一定会出现\u201c强调信念的重要性。',
        [
            ('孜孜不倦', '勤奋努力，不知疲倦。孜孜，勤勉'),
            ('汲取', '吸取、吸收'),
            ('学识渊博', '学识深而且广'),
            ('精通', '对学问、技术或业务有透彻的了解并熟练地掌握'),
            ('一事无成', '连一样事情也没做成，形容毫无成就'),
            ('组合', '将不同的事物组织、搭配在一起'),
            ('创意', '有创造性的想法、构思'),
            ('当事人', '这里指产生创意的那个人'),
            ('坚信', '坚决相信'),
        ]
    ),
    (
        '我对此完全赞同。知识是形成新创意的素材。但这并不是说，光凭知识就能拥有创造力。发挥创造力的真正关键，在于如何运用知识。创造性的思维，必须有探求新事物，并为此而活用知识的态度和意识，在此基础上，持之以恒地进行各种尝试。',
        '作者表明赞同上述观点，但进一步指出：光凭知识不够，发挥创造力的关键在于运用知识，要有活用知识的态度和持之以恒的尝试。',
        '先肯定（\u201c完全赞同\u201d），再以\u201c但\u201d转折，推进一层，指出知识只是素材，运用才是关键。\u201c必须有\u2026\u2026在此基础上\u2026\u2026\u201d的句式，层层递进地阐明创造性思维的条件：态度意识→持之以恒的尝试。\u201c素材\u201d一词比喻精当，说明知识是原料而非成品。',
        [
            ('对此', '对于这个（观点）'),
            ('素材', '文学、艺术创作的原始材料，这里比喻知识是创造的基础材料'),
            ('光凭', '只依靠、仅仅凭借'),
            ('关键', '比喻事物最关紧要的部分，对情况起决定作用的因素'),
            ('活用', '灵活运用'),
            ('态度和意识', '对事物的看法和觉察能力'),
            ('持之以恒', '长久地坚持下去。恒，恒心'),
        ]
    ),
    (
        '这方面的典型代表，首推谷登堡。他将原来毫不相关的两种机械\u2014\u2014葡萄压榨机和硬币打制器组合起来，开发了一种新机械。因为葡萄压榨机用来从葡萄中榨出汁，所以它在大面积上均等加力。而硬币打制器的功能则是在金币之类的小平面上打出印花来。有一天，古登堡半开玩笑地自言自语道：是不是可以在几个硬币打制器上加上葡萄压榨机的压力，使它在纸上打印出印花来呢？由此发明了印刷机和排版术。',
        '举谷登堡将葡萄压榨机和硬币打制器组合，发明印刷机和排版术的事例，论证创造性思维在于活用知识、组合创新。',
        '举例论证，以谷登堡发明印刷机的典型事例具体展示创造性思维的过程。先介绍两种机械的各自功能（葡萄压榨机大面积加力、硬币打制器小平面印花），再以\u201c半开玩笑地自言自语\u201d再现灵感闪现的瞬间，最后点明成果。事例叙述生动，逻辑清晰，有力地证明了\u201c组合知识→产生创意\u201d的观点。',
        [
            ('典型代表', '具有代表性的人物或事例'),
            ('首推', '首先推举、第一位要数'),
            ('谷登堡', '约翰·谷登堡，德国发明家，活字印刷术的发明者'),
            ('毫不相关', '一点关系也没有'),
            ('葡萄压榨机', '用来压榨葡萄取汁的机械'),
            ('硬币打制器', '用来在金属币上压制图案的工具'),
            ('开发', '研制、创造'),
            ('均等加力', '均匀地施加压力'),
            ('功能', '事物或方法所发挥的有利作用'),
            ('印花', '印出花纹图案'),
            ('半开玩笑', '有一半是开玩笑的，形容不完全认真'),
            ('自言自语', '自己跟自己说话'),
            ('排版术', '将文字、图片等按一定格式排列的技术'),
        ]
    ),
    (
        '另一个例子是罗兰·布歇内尔。1971年的一天，布歇内尔边看电视边这么想：光看太没意思了。把电视接收器作为试验对象，看它产生什么反应。此后不久，他就发明了交互式的乒乓球电子游戏，从此开始了游戏机的革命。',
        '举罗兰·布歇内尔发明交互式乒乓球电子游戏的事例，进一步论证创造性思维在于探求新事物、活用知识。',
        '举例论证，\u201c另一个例子\u201d与上一段谷登堡的事例构成并列，两个事例一古一今、一重一轻，从不同角度论证同一观点，增强说服力。以\u201c边看电视边这么想\u201d再现灵感产生的日常情境，说明创意往往源于对平凡事物的思考。\u201c从此开始了游戏机的革命\u201d点明发明的深远影响。',
        [
            ('罗兰·布歇内尔', '美国发明家，交互式电子游戏的先驱'),
            ('电视接收器', '接收电视信号的装置，即电视机'),
            ('试验对象', '用来进行实验的对象'),
            ('反应', '事物受到刺激后引起的相应活动或变化'),
            ('交互式', '人与机器之间可以相互交流、相互作用的'),
            ('乒乓球电子游戏', '模拟乒乓球运动的电子游戏'),
            ('革命', '根本改革，这里指游戏机领域的重大变革'),
        ]
    ),
    (
        '不过，这种创造性的思维是否任何人都具备呢？是否存在富有创造力的人和缺乏创造力的人的区别呢？',
        '以两个设问句过渡，从\u201c创造性思维需要什么条件\u201d转入\u201c创造性思维是否人人都有\u201d的论述。',
        '过渡段，连用两个设问句，层层递进地提出新问题，既引发读者思考，又自然引出下文的论述。第一个设问问\u201c是否任何人都具备\u201d，第二个设问进一步问\u201c是否存在区别\u201d，问题逐步深入，体现论证的严密性。',
        [
            ('任何人', '所有的人、不论什么人'),
            ('具备', '具有、拥有'),
            ('富有', '大量具有、丰富地拥有'),
            ('缺乏', '缺少、不足'),
            ('区别', '彼此不同的地方'),
        ]
    ),
    (
        '某心理学专家小组以实际从事创造性工作的人与不从事此类工作的人为对象进行了调查研究，并得出如下结论：富于创造力的人，认为自己具有创造力；缺乏创造力的人，不认为自己具有创造力。',
        '引用心理学专家小组的调查结论，指出富于创造力的人自信具有创造力，缺乏创造力的人则不自信。',
        '举例论证（引用调查结论），以权威的心理学研究为依据，增强论证的科学性和说服力。调查对象的对比（从事创造性工作vs不从事）使结论更具可信度。结论本身采用对比句式（富于vs缺乏，认为vs不认为），鲜明地突出自信与创造力的关系。',
        [
            ('心理学专家小组', '由心理学专业人员组成的研究团队'),
            ('从事', '做、投身于'),
            ('此类工作', '这类工作，指创造性工作'),
            ('调查研究', '为了了解情况进行考察、分析'),
            ('如下结论', '下面这样的结论'),
            ('富于', '丰富地具有、大量拥有'),
        ]
    ),
    (
        '认为\u201c我不具备创造力\u201d的人当中，有的觉得创造力仅仅是贝多芬、爱因斯坦以及莎士比亚他们的，从而进行自我压制。不言而喻，在创造的宇宙里，这些人是光辉灿烂的明星，然而在大多数情况下，即便是他们，也并非轻而易举就能获得如此非凡的灵感。相反，这种非凡的灵感，往往产生于这样的过程：关注极其普通、甚至一闪念的想法，并对它反复推敲，逐渐充实。',
        '分析缺乏自信者的心理误区，指出即使是贝多芬、爱因斯坦等伟人，灵感也非轻而易举获得，而是源于对普通想法的反复推敲和充实。',
        '先破后立：先指出\u201c自我压制\u201d的错误心理（认为创造力只属于伟人），再以\u201c然而\u201d转折，指出伟人的灵感也非轻而易举。\u201c相反\u201d进一步揭示灵感产生的真实过程：关注普通想法→反复推敲→逐渐充实。比喻论证：\u201c创造的宇宙\u201d\u201c光辉灿烂的明星\u201d比喻创造领域和杰出人物，形象生动。\u201c不言而喻\u201d\u201c轻而易举\u201d等成语凝练准确。',
        [
            ('仅仅', '只、只不过'),
            ('贝多芬', '德国作曲家，维也纳古典乐派代表人物'),
            ('爱因斯坦', '美籍德国物理学家，相对论的创立者'),
            ('莎士比亚', '英国文艺复兴时期戏剧家、诗人'),
            ('自我压制', '自己压抑、限制自己'),
            ('不言而喻', '不用说就可以明白，形容道理很明显'),
            ('宇宙', '这里比喻创造的广阔领域'),
            ('光辉灿烂', '光彩耀眼，比喻成就卓越'),
            ('即便', '即使、就算是'),
            ('轻而易举', '形容事情很容易做，不费力气'),
            ('非凡', '超过一般、不寻常'),
            ('灵感', '在文学、艺术、科学等活动中，由于勤奋学习、不断实践、积累经验而突然产生的富有创造性的思路'),
            ('一闪念', '瞬间出现的念头、想法'),
            ('推敲', '比喻斟酌字句、反复琢磨'),
            ('充实', '使丰富、使充足'),
        ]
    ),
    (
        '由此看来，区分一个人是否拥有创造力，主要根据之一是，拥有创造力的人留意自己细小的想法。即使他们不知道将来会产生怎样的结果，但他们很清楚，小的创意会打开大的突破口，并坚信自己一定能使之变为现实。',
        '得出结论：区分是否拥有创造力的主要根据之一是是否留意自己细小的想法，小创意能打开大突破口。',
        '总结段，\u201c由此看来\u201d承接上文的分析，得出结论。\u201c主要根据之一\u201d表述严谨，不绝对化。\u201c小的创意会打开大的突破口\u201d以对比（小vs大）强调细小想法的重要价值。\u201c坚信自己一定能使之变为现实\u201d再次强调自信的重要性，与前文心理学调查结论呼应。',
        [
            ('由此看来', '从这里可以看出、据此看来'),
            ('区分', '辨别、划分'),
            ('主要根据之一', '最重要的依据中的一个'),
            ('留意', '注意、留心'),
            ('细小', '很小、细微'),
            ('突破口', '打破僵局的关键地方、进攻的突破口'),
            ('变为现实', '成为真实存在的事物、实现'),
        ]
    ),
    (
        '任何人都拥有创造力，首先要坚信这一点。关键是要经常保持好奇心，不断积累知识；不满足于一个答案，而去探求新思路，去运用所得的知识；一旦产生小的灵感，相信它的价值，并锲而不舍地把它发展下去。如果能做到这些，你一定会成为一个富有创造力的人。',
        '总结全文，指出任何人都拥有创造力，关键是要坚信、保持好奇心、积累知识、探求新思路、发展灵感，并以此勉励读者。',
        '全文结论段，以\u201c任何人都拥有创造力\u201d回应开篇的问题，首尾呼应。用三个分句（保持好奇心积累知识→不满足一个答案探求新思路→产生灵感锲而不舍发展）系统总结培养创造力的方法，条理清晰。\u201c锲而不舍\u201d与前文\u201c持之以恒\u201d呼应，强调坚持的重要性。结尾\u201c你一定会成为一个富有创造力的人\u201d以肯定的语气勉励读者，富有感召力。',
        [
            ('首先', '第一、最先'),
            ('坚信', '坚决相信'),
            ('好奇心', '对自己所不了解的事物觉得新奇而感兴趣的心理'),
            ('积累', '逐渐聚集'),
            ('一旦', '如果有一天、要是'),
            ('价值', '事物的积极作用、意义'),
            ('锲而不舍', '雕刻一件东西，一直刻下去不放手，比喻有恒心、有毅力。锲，雕刻'),
            ('发展下去', '继续推进、使不断成长'),
            ('富有', '大量具有'),
        ]
    ),
]

def annotate(text, notes):
    sorted_notes = sorted(notes, key=lambda x: len(x[0]), reverse=True)
    result = text
    used = set()
    for word, note in sorted_notes:
        if word in used:
            continue
        idx = result.find(word)
        if idx >= 0:
            before = result[:idx]
            if before.count('<span class="anno-word"') > before.count('</span>'):
                continue
            escaped_note = note.replace('"', '&quot;')
            replacement = f'<span class="anno-word" data-note="{escaped_note}">{word}</span>'
            result = result[:idx] + replacement + result[idx+len(word):]
            used.add(word)
    return result

fulltext_lines = []
for orig, _, _, _ in PARAS:
    fulltext_lines.append(f'    <div class="pl">{orig}</div>')
FULLTEXT = '\n'.join(fulltext_lines)

verse_cards = []
for i, (orig, content, technique, notes) in enumerate(PARAS):
    annotated = annotate(orig, notes)
    card = f'''      <div class="verse" id="l{i+1}" data-i="{i}">
        <div class="v-top"><span class="v-no">{i+1}</span><div class="v-line">{annotated}</div></div>
        <details class="v-more">
          <summary>内容 · 手法</summary>
          <div class="d-body">
            <div class="v-sec"><b class="v-label">内容概括</b>
              <div class="v-trans">{content}</div>
            </div>
            <div class="v-sec"><b class="v-label">手法分析</b>
              <div class="d-body"><p>{technique}</p></div>
            </div>
          </div>
        </details>
      </div>'''
    verse_cards.append(card)
VERSE_CARDS = '\n'.join(verse_cards)

# ============ 题库 ============
DICT_WORDS = [
    {"w":"蒂","py":"dì","q":"在我们头脑中已不知不觉地根深□固","tip":"\u300c蒂\u300d草字头，花或瓜果跟枝茎相连的部分；不要写成\u300c缔\u300d（绞丝旁，缔结）"},
    {"w":"孜孜","py":"zī zī","q":"富有创造性的人总是□□不倦地汲取知识","tip":"\u300c孜孜\u300d叠词整体作答，子字旁，勤勉；不要写成\u300c姿姿\u300d（女字旁，姿态）"},
    {"w":"汲","py":"jí","q":"富有创造性的人总是孜孜不倦地□取知识","tip":"\u300c汲\u300d三点水，从下往上打水，引申为吸取；不读 xī，与\u300c吸\u300d（口字旁）区分"},
    {"w":"博","py":"bó","q":"使自己学识渊□","tip":"\u300c博\u300d十字旁，广博；不要写成\u300c搏\u300d（提手旁，搏斗）"},
    {"w":"恒","py":"héng","q":"在此基础上，持之以□地进行各种尝试","tip":"\u300c恒\u300d竖心旁，恒心、持久；不要写成\u300c桓\u300d（木字旁，盘桓）"},
    {"w":"榨","py":"zhà","q":"他将原来毫不相关的两种机械——葡萄压□机和硬币打制器组合起来","tip":"\u300c榨\u300d木字旁，压出物体里的汁液；不要写成\u300c诈\u300d（言字旁，欺诈）"},
    {"w":"币","py":"bì","q":"葡萄压榨机和硬□打制器组合起来","tip":"\u300c币\u300d巾字底，货币；不要写成\u300c帀\u300d（zā，同匝）"},
    {"w":"验","py":"yàn","q":"把电视接收器作为试□对象，看它产生什么反应","tip":"\u300c验\u300d马字旁，检验、试验；不要写成\u300c检\u300d（木字旁，检查）"},
    {"w":"抑","py":"yì","q":"从而进行自我□制","tip":"\u300c抑\u300d提手旁，压制；不读 yǎng，与\u300c仰\u300d（单人旁，仰望）区分"},
    {"w":"喻","py":"yù","q":"不言而□，在创造的宇宙里，这些人是光辉灿烂的明星","tip":"\u300c喻\u300d口字旁，明白、了解；不要写成\u300c谕\u300d（言字旁，上对下的指示）"},
    {"w":"灿","py":"càn","q":"这些人是光辉□烂的明星","tip":"\u300c灿\u300d火字旁，光彩耀眼；不要写成\u300c璨\u300d（王字旁，美玉）"},
    {"w":"凡","py":"fán","q":"想要获得创造力，并非轻而□举","tip":"\u300c凡\u300d几字底，平常、一般；\u300c轻而易举\u300d形容事情容易做；不要写成\u300c烦\u300d（火字旁，烦恼）"},
    {"w":"敲","py":"qiāo","q":"并对它反复推□，逐渐充实","tip":"\u300c敲\u300d高字头，击打；\u300c推敲\u300d比喻斟酌字句；不要写成\u300c锹\u300d（金字旁，铁锹）"},
    {"w":"锲","py":"qiè","q":"相信它的价值，并□而不舍地把它发展下去","tip":"\u300c锲\u300d金字旁，雕刻；不读 qì，与\u300c契\u300d（大字头，契约）区分，\u300c锲而不舍\u300d出自《荀子》"},
    {"w":"破","py":"pò","q":"小的创意会打开大的突□口","tip":"\u300c破\u300d石字旁，打破、突破；不要写成\u300c坡\u300d（提土旁，山坡）"},
]

DICT_NOTES = [
    {"w":"根深蒂固","a":"比喻基础深厚，不容易动摇","q":"在我们头脑中已不知不觉地根深蒂固"},
    {"w":"行之有效","a":"实行起来有成效，指某种方法或措施已经实行过，证明很有效用","q":"原来行之有效的方法，到了现在往往不灵了"},
    {"w":"止步不前","a":"停止脚步，不再前进，比喻安于现状","q":"当你找到某个答案以后，就会止步不前"},
    {"w":"探求","a":"探索追求","q":"不满足于一个答案，不放弃探求"},
    {"w":"孜孜不倦","a":"勤奋努力，不知疲倦。孜孜，勤勉","q":"富有创造性的人总是孜孜不倦地汲取知识"},
    {"w":"汲取","a":"吸取、吸收","q":"富有创造性的人总是孜孜不倦地汲取知识"},
    {"w":"学识渊博","a":"学识深而且广","q":"使自己学识渊博"},
    {"w":"一事无成","a":"连一样事情也没做成，形容毫无成就","q":"不精通各种知识就一事无成"},
    {"w":"创意","a":"有创造性的想法、构思","q":"这些知识随时都可能进行组合，形成新的创意"},
    {"w":"素材","a":"文学、艺术创作的原始材料，这里比喻知识是创造的基础材料","q":"知识是形成新创意的素材"},
    {"w":"持之以恒","a":"长久地坚持下去。恒，恒心","q":"在此基础上，持之以恒地进行各种尝试"},
    {"w":"谷登堡","a":"约翰·谷登堡，德国发明家，活字印刷术的发明者","q":"这方面的典型代表，首推谷登堡"},
    {"w":"葡萄压榨机","a":"用来压榨葡萄取汁的机械","q":"他将原来毫不相关的两种机械——葡萄压榨机和硬币打制器组合起来"},
    {"w":"排版术","a":"将文字、图片等按一定格式排列的技术","q":"由此发明了印刷机和排版术"},
    {"w":"罗兰·布歇内尔","a":"美国发明家，交互式电子游戏的先驱","q":"另一个例子是罗兰·布歇内尔"},
    {"w":"交互式","a":"人与机器之间可以相互交流、相互作用的","q":"他就发明了交互式的乒乓球电子游戏"},
    {"w":"自我压制","a":"自己压抑、限制自己","q":"从而进行自我压制"},
    {"w":"不言而喻","a":"不用说就可以明白，形容道理很明显","q":"不言而喻，在创造的宇宙里，这些人是光辉灿烂的明星"},
    {"w":"轻而易举","a":"形容事情很容易做，不费力气","q":"也并非轻而易举就能获得如此非凡的灵感"},
    {"w":"灵感","a":"在文学、艺术、科学等活动中突然产生的富有创造性的思路","q":"也并非轻而易举就能获得如此非凡的灵感"},
    {"w":"推敲","a":"比喻斟酌字句、反复琢磨","q":"并对它反复推敲，逐渐充实"},
    {"w":"突破口","a":"打破僵局的关键地方、进攻的突破口","q":"小的创意会打开大的突破口"},
    {"w":"好奇心","a":"对自己所不了解的事物觉得新奇而感兴趣的心理","q":"关键是要经常保持好奇心"},
    {"w":"锲而不舍","a":"雕刻一件东西一直刻下去不放手，比喻有恒心、有毅力。锲，雕刻","q":"并锲而不舍地把它发展下去"},
]

# ============ 组装 HTML ============
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《谈创造性思维》罗迦·费·因格</title>
<style>{CSS}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">美国 · 罗迦·费·因格</div>
  <h1 class="hero-title">谈创造性思维</h1>
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
        <option value="100">100%</option>
        <option value="150">150%</option>
        <option value="200">200%</option>
        <option value="250">250%</option>
        <option value="300">300%</option>
      </select>
      <button id="btnAll">展开</button>
      <button id="btnRecite">背诵</button>
      <button id="btnPrint">打印</button>
    </div>
  </div>
</nav>

<main class="wrap">
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>罗迦·费·因格是美国实业家、学者，曾任创意顾问公司的总裁，长期从事创意思维的研究与培训。他认为创造力不是少数人的天赋，而是每个人都可以培养的能力。</p>
    <p>《谈创造性思维》从一道图形选择题切入，提出\u201c事物的正确答案不止一个\u201d的观点，进而层层深入地论述创造性思维的必备条件、创造力的区分依据以及培养创造力的方法，是一篇深入浅出、富有启发性的议论文。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>罗迦·费·因格（Roger von Oech），美国实业家、学者、创意顾问。曾任美国创意顾问公司的总裁，长期致力于创意思维的研究与培训，为众多知名企业提供创新咨询服务。代表作有《当头棒喝》《在屁股上踢一脚》《创意大惊奇》等。他的作品以生动有趣的方式阐释创新思维，深受读者欢迎。</p>
    <p style="margin-top:10px;color:var(--ink2)">本文是作者为《中外母语教材选粹》撰写的一篇议论文，原题为《事物的正确答案不止一个》，选入教材时改题为《谈创造性思维》。文章语言通俗、逻辑严密，是培养学生创新思维的优秀读物。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>创新时代的呼唤：</b>20世纪后期，随着科技革命的深入，创新能力成为个人和企业竞争力的核心。美国教育界开始反思传统教育中\u201c标准答案唯一\u201d的思维模式对创造力的压抑。</p>
    <p style="margin-top:8px"><b>创意思维研究：</b>罗迦·费·因格长期从事创意思维的研究和培训，他通过大量案例和实践，总结出创造性思维的规律和培养方法，认为创造力是可以通过训练获得的。</p>
    <p style="margin-top:8px"><b>写作意图：</b>本文旨在打破\u201c正确答案只有一个\u201d的思维定式，引导读者认识到创造性思维的重要性，并掌握培养创造力的方法，鼓励每个人都成为富有创造力的人。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文朗读《谈创造性思维》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1ba4y1j79c&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读《谈创造性思维》"></iframe>
        <a href="https://www.bilibili.com/video/BV1ba4y1j79c" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>公开课《谈创造性思维》</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV13u4y147Dw&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="公开课《谈创造性思维》"></iframe>
        <a href="https://www.bilibili.com/video/BV13u4y147Dw" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 词语 · 手法</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{FULLTEXT}
  </div>
  <div class="verse-list" id="verseList">
{VERSE_CARDS}
  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">论点 · 论证 · 语言</span></div>
  <div class="box">
    <h3>中心论点</h3>
    <p>本文的中心论点是：任何人都拥有创造力，关键是要保持好奇心、积累知识、探求新思路、发展灵感，做一个富有创造力的人。文章从\u201c事物的正确答案不止一个\u201d的现象切入，逐层深入地论述创造性思维的条件和创造力的培养，最终得出结论。</p>
  </div>
  <div class="box">
    <h3>论证思路</h3>
    <p>全文按照\u201c提出问题\u2014\u2014分析问题\u2014\u2014解决问题\u201d的思路展开，可分为四个部分：</p>
    <p style="margin-top:8px"><b>第一部分（第1\u20143段）：</b>以图形选择题引出\u201c事物的正确答案不止一个\u201d的观点，指出\u201c正确答案只有一个\u201d的思维模式的危害，强调不满足于一个答案、不放弃探求的重要性。</p>
    <p style="margin-top:8px"><b>第二部分（第4\u20148段）：</b>论述创造性思维必须具备的条件。先以设问引出问题，再引用他人观点指出知识的重要性，然后作者推进一层指出运用知识才是关键，最后以谷登堡和布歇内尔两个事例具体论证。</p>
    <p style="margin-top:8px"><b>第三部分（第9\u201412段）：</b>论述创造性思维是否人人都有。以两个设问过渡，引用心理学调查结论，分析缺乏自信者的心理误区，指出灵感源于对普通想法的反复推敲，得出\u201c留意细小想法\u201d是区分创造力的主要根据之一。</p>
    <p style="margin-top:8px"><b>第四部分（第13段）：</b>总结全文，指出任何人都拥有创造力，系统总结培养创造力的方法，勉励读者成为富有创造力的人。</p>
  </div>
  <div class="box">
    <h3>论证方法</h3>
    <div class="tw">
    <table>
      <tr><th>论证方法</th><th>文中体现</th><th>作用</th></tr>
      <tr><td>举例论证</td><td>第7段举谷登堡组合两种机械发明印刷机；第8段举布歇内尔发明交互式乒乓球电子游戏</td><td>以两个典型事例具体展示创造性思维的过程，使论证生动可感，增强说服力</td></tr>
      <tr><td>道理论证（引用）</td><td>第5段引用\u201c有人\u201d关于知识重要性的观点；第10段引用心理学专家小组的调查结论</td><td>以权威观点和科学研究为依据，增强论证的理论深度和可信度</td></tr>
      <tr><td>对比论证</td><td>第3段数学问题答案唯一vs生活中方法多样；第10段富于创造力的人自信vs缺乏创造力的人不自信；第11段伟人灵感也非轻而易举vs普通人认为灵感只属于伟人</td><td>正反对照，使论点更加鲜明，突出创造性思维的本质和培养路径</td></tr>
      <tr><td>比喻论证</td><td>\u201c知识是形成新创意的素材\u201d；\u201c在创造的宇宙里，这些人是光辉灿烂的明星\u201d；\u201c小的创意会打开大的突破口\u201d</td><td>以生动的比喻将抽象的道理形象化，使读者易于理解</td></tr>
    </table>
    </div>
  </div>
  <div class="box">
    <h3>语言特点</h3>
    <p><b>通俗浅显，平易近人：</b>文章以一道图形选择题开篇，用口语化的表达（\u201c恭喜你答对了\u201d\u201c麻烦的是\u201d）拉近与读者的距离，将抽象的创意思维讲得深入浅出，适合中学生阅读。</p>
    <p style="margin-top:8px"><b>逻辑严密，层层递进：</b>全文从现象到本质，从条件到方法，环环相扣。设问句的运用（\u201c创造性的思维必须具备哪些条件呢？\u201d\u201c是否任何人都具备呢？\u201d）既推动论证深入，又引发读者思考。</p>
    <p style="margin-top:8px"><b>排比与反复，语势充沛：</b>\u201c六分钟之后\u201d\u201c六个月之后\u201d\u201c六年之后\u201d构成时间排比；结尾三个分句（保持好奇心→不满足一个答案→产生灵感锲而不舍）构成方法排比，语势充沛，条理清晰。</p>
    <p style="margin-top:8px"><b>成语丰富，凝练准确：</b>全文运用了\u201c根深蒂固\u201d\u201c孜孜不倦\u201d\u201c行之有效\u201d\u201c止步不前\u201d\u201c一事无成\u201d\u201c持之以恒\u201d\u201c不言而喻\u201d\u201c轻而易举\u201d\u201c锲而不舍\u201d等大量成语，语言凝练，表达准确。</p>
  </div>
  <div class="fame">
    <div class="fame-card">
      <div class="f-line">不满足于一个答案，不放弃探求，这一点非常重要。</div>
      <p>全文的核心观点之一。在指出\u201c正确答案只有一个\u201d思维模式的危害后得出此结论，\u201c不满足\u201d\u201c不放弃\u201d两个否定短语强调态度的坚定，为下文论述创造性思维张本。</p>
    </div>
    <div class="fame-card">
      <div class="f-line">发挥创造力的真正关键，在于如何运用知识。</div>
      <p>承上启下的关键句。先肯定知识的重要性，再以\u201c但\u201d转折推进一层，指出运用才是关键。\u201c真正关键\u201d强调核心，与下文两个事例形成论点与论据的关系。</p>
    </div>
    <div class="fame-card">
      <div class="f-line">任何人都拥有创造力，首先要坚信这一点。</div>
      <p>全文结论的核心句。以\u201c任何人\u201d打破创造力属于少数人的迷思，以\u201c首先要坚信\u201d强调自信是前提，与前文心理学调查结论呼应，富有感召力。</p>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 字音 · 修辞 · 借鉴 · 常识</span></div>

  <div class="acc-cat">
    <h3>重点词语</h3>
    <div class="acc-item"><span class="acc-w">根深蒂固</span><span class="acc-d">比喻基础深厚，不容易动摇。如\u201c在我们头脑中已不知不觉地根深蒂固\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">孜孜不倦</span><span class="acc-d">勤奋努力，不知疲倦。孜孜，勤勉。如\u201c富有创造性的人总是孜孜不倦地汲取知识\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">汲取</span><span class="acc-d">吸取、吸收。如\u201c孜孜不倦地汲取知识\u201d。不读 xī。</span></div>
    <div class="acc-item"><span class="acc-w">行之有效</span><span class="acc-d">实行起来有成效。如\u201c原来行之有效的方法，到了现在往往不灵了\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">止步不前</span><span class="acc-d">停止脚步，不再前进，比喻安于现状。如\u201c当你找到某个答案以后，就会止步不前\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">持之以恒</span><span class="acc-d">长久地坚持下去。恒，恒心。如\u201c持之以恒地进行各种尝试\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">不言而喻</span><span class="acc-d">不用说就可以明白，形容道理很明显。如\u201c不言而喻，在创造的宇宙里\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">轻而易举</span><span class="acc-d">形容事情很容易做，不费力气。如\u201c并非轻而易举就能获得如此非凡的灵感\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">锲而不舍</span><span class="acc-d">雕刻一件东西一直刻下去不放手，比喻有恒心、有毅力。锲，雕刻。不读 qì。如\u201c并锲而不舍地把它发展下去\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">探求</span><span class="acc-d">探索追求。如\u201c不满足于一个答案，不放弃探求\u201d。</span></div>
  </div>

  <div class="acc-cat">
    <h3>用字与读音</h3>
    <div class="acc-item"><span class="acc-w">蒂（dì）</span><span class="acc-d">根深蒂固。\u300c蒂\u300d草字头，花或瓜果跟枝茎相连的部分。与\u300c缔\u300d（绞丝旁，缔结）区分。</span></div>
    <div class="acc-item"><span class="acc-w">孜（zī）</span><span class="acc-d">孜孜不倦。\u300c孜\u300d子字旁，勤勉。不读 zǐ。叠词\u300c孜孜\u300d整体作答。</span></div>
    <div class="acc-item"><span class="acc-w">汲（jí）</span><span class="acc-d">汲取。\u300c汲\u300d三点水，从下往上打水。不读 xī。与\u300c吸\u300d（口字旁）区分。</span></div>
    <div class="acc-item"><span class="acc-w">博（bó）</span><span class="acc-d">渊博。\u300c博\u300d十字旁，广博。与\u300c搏\u300d（提手旁，搏斗）区分。</span></div>
    <div class="acc-item"><span class="acc-w">恒（héng）</span><span class="acc-d">持之以恒。\u300c恒\u300d竖心旁，恒心。不读 huán。与\u300c桓\u300d（木字旁，盘桓）区分。</span></div>
    <div class="acc-item"><span class="acc-w">榨（zhà）</span><span class="acc-d">压榨机。\u300c榨\u300d木字旁，压出汁液。不读 zhá。与\u300c诈\u300d（言字旁，欺诈）区分。</span></div>
    <div class="acc-item"><span class="acc-w">抑（yì）</span><span class="acc-d">自我压制。\u300c抑\u300d提手旁，压制。不读 yǎng。与\u300c仰\u300d（单人旁）区分。</span></div>
    <div class="acc-item"><span class="acc-w">喻（yù）</span><span class="acc-d">不言而喻。\u300c喻\u300d口字旁，明白。不读 yú。与\u300c谕\u300d（言字旁）区分。</span></div>
    <div class="acc-item"><span class="acc-w">锲（qiè）</span><span class="acc-d">锲而不舍。\u300c锲\u300d金字旁，雕刻。不读 qì。与\u300c契\u300d（大字头，契约）区分。</span></div>
  </div>

  <div class="acc-cat">
    <h3>修辞方法</h3>
    <div class="acc-item"><span class="acc-w">设问</span><span class="acc-d">全文多处运用设问：\u201c创造性的思维必须具备哪些条件呢？\u201d\u201c这种创造性的思维是否任何人都具备呢？是否存在富有创造力的人和缺乏创造力的人的区别呢？\u201d设问既引发读者思考，又推动论证层层深入。</span></div>
    <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">\u201c六分钟之后\u201d\u201c六个月之后\u201d\u201c六年之后\u201d构成时间排比；结尾\u201c经常保持好奇心，不断积累知识；不满足于一个答案，而去探求新思路；一旦产生小的灵感\u2026\u2026\u201d构成方法排比，语势充沛，条理清晰。</span></div>
    <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">\u201c知识是形成新创意的素材\u201d将知识比作创作原料；\u201c在创造的宇宙里，这些人是光辉灿烂的明星\u201d将创造领域比作宇宙、杰出人物比作明星；\u201c小的创意会打开大的突破口\u201d以军事术语比喻创新，形象生动。</span></div>
    <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">数学问题答案唯一与生活中方法多样对比；富于创造力的人自信与缺乏创造力的人不自信对比；伟人灵感也非轻而易举与普通人认为灵感只属于伟人对比，正反对照使论点鲜明。</span></div>
  </div>

  <div class="acc-cat">
    <h3>写作借鉴</h3>
    <div class="acc-item"><span class="acc-w">从生活现象切入</span><span class="acc-d">文章以一道图形选择题开篇，从学生熟悉的生活现象切入，自然引出\u201c答案不止一个\u201d的观点，避免了议论文常见的枯燥说教，值得借鉴。</span></div>
    <div class="acc-item"><span class="acc-w">设问推动论证</span><span class="acc-d">全文以设问句作为段落之间的过渡（\u201c创造性的思维必须具备哪些条件呢？\u201d\u201c是否任何人都具备呢？\u201d），既引发读者思考，又使论证层次分明、层层深入。</span></div>
    <div class="acc-item"><span class="acc-w">事例典型、叙述生动</span><span class="acc-d">谷登堡和布歇内尔两个事例一古一今、一重一轻，从不同角度论证同一观点。事例叙述中再现灵感闪现的瞬间（\u201c半开玩笑地自言自语\u201d\u201c边看电视边这么想\u201d），生动具体，避免了举例论证的干巴巴。</span></div>
    <div class="acc-item"><span class="acc-w">先肯定再推进</span><span class="acc-d">第6段\u201c我对此完全赞同\u2026\u2026但这并不是说\u2026\u2026发挥创造力的真正关键，在于如何运用知识\u201d，先肯定对方观点，再以\u201c但\u201d转折推进一层，使论证更加严密、全面，避免了绝对化。</span></div>
  </div>

  <div class="acc-cat">
    <h3>文化常识</h3>
    <div class="acc-item"><span class="acc-w">谷登堡</span><span class="acc-d">约翰·谷登堡（约1400\u20141468），德国发明家，活字印刷术的发明者。他将葡萄压榨机和硬币打制器的原理结合，发明了金属活字印刷机和排版术，对欧洲文艺复兴和知识传播产生了深远影响。</span></div>
    <div class="acc-item"><span class="acc-w">罗兰·布歇内尔</span><span class="acc-d">美国发明家，交互式电子游戏的先驱。1971年发明了世界上第一个交互式电子游戏《乒乓》（Pong），开创了电子游戏产业，被誉为\u201c电子游戏之父\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">贝多芬</span><span class="acc-d">（1770\u20141827），德国作曲家，维也纳古典乐派代表人物之一。一生创作了9部交响曲、32首钢琴奏鸣曲等大量作品，被称为\u201c乐圣\u201d。即使在失聪后仍坚持创作，其灵感源于对音乐的执着追求。</span></div>
    <div class="acc-item"><span class="acc-w">爱因斯坦</span><span class="acc-d">（1879\u20141955），美籍德国物理学家，相对论的创立者。他提出的狭义相对论和广义相对论彻底改变了人类对时空和引力的认识，被认为是继牛顿以来最伟大的物理学家。</span></div>
    <div class="acc-item"><span class="acc-w">莎士比亚</span><span class="acc-d">（1564\u201616），英国文艺复兴时期戏剧家、诗人。代表作有《哈姆雷特》《罗密欧与朱丽叶》《威尼斯商人》等37部戏剧，被马克思称为\u201c人类最伟大的戏剧天才\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">创造性思维</span><span class="acc-d">一种具有开创意义的思维活动，即开拓人类认识新领域、开创人类认识新成果的思维活动。它以感知、记忆、思考、联想、理解等能力为基础，具有综合性、探索性和求新性等特征。</span></div>
  </div>
</section>

<div class="divider"></div>
<section id="practice" class="sec">
    <div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>
    <div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>
    <div class="ptools">
      <button data-mode="word" data-rand="5">随机五组字形</button>
      <button data-mode="word" data-all="1">全部字形</button>
      <button data-mode="note" data-rand="5">随机五组词语</button>
      <button data-mode="note" data-all="1">全部词语</button>
    </div>
  </section>

<footer>
  <div class="kai">《谈创造性思维》</div>
  <div>罗迦·费·因格 · 美国 · 出自《中外母语教材选粹》</div>
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

{JS_IIFE}
<script>
var DICT_WORDS = {json.dumps(DICT_WORDS, ensure_ascii=False)};
var DICT_NOTES = {json.dumps(DICT_NOTES, ensure_ascii=False)};
</script>

</body>
</html>'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated: {OUT}")
print(f"File size: {len(html)} bytes")
