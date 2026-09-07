# -*- coding: utf-8 -*-
# 生成《虽有嘉肴》交互式教学HTML课件
import json, re

OUT = r'D:\App\Apps\yanshi\suiyoujiayao-liji.html'
FS_KEY = 'suiyoujiayao_fs'
TITLE = '虽有嘉肴'
HERO_SIDE = '先秦 · 《礼记》'

VERSES = [
(
'虽有嘉肴，弗食，不知其旨也；虽有至道，弗学，不知其善也。',
'即使有美味的肉食，不去品尝，就不知道它的味美；即使有最好的道理，不去学习，就不知道它的好处。',
'开篇以类比论证引出主题。“虽有嘉肴，弗食，不知其旨也”是喻体，“虽有至道，弗学，不知其善也”是本体——以“嘉肴”喻“至道”，以“食”喻“学”，以“旨”喻“善”。两个“虽……弗……不知……”的句式构成工整的对偶，从反面强调了实践（学习）的重要性：再好的道理，不学就不知道它的好处。这一句是全文的逻辑起点，为下文“教学相长”的论述蓄势。',
[
('虽', '即使，表假设连词（古今异义：今义为“虽然”）'),
('嘉肴', '美味的肉食。嘉，美好；肴（yáo），用鱼肉等做的荤菜'),
('弗', '（fú）不，否定副词'),
('食', '吃，动词'),
('不知', '不知道'),
('其', '它的，代词，指嘉肴'),
('旨', '（zhǐ）味美，形容词（古今异义：今义为“意义、目的”）'),
('也', '句末语气词，表判断'),
('虽', '即使，表假设'),
('至道', '最好的道理。至，达到极点的，最好的；道，道理'),
('弗', '不'),
('学', '学习'),
('不知', '不知道'),
('其', '它的，代词，指至道'),
('善', '好处，形容词作名词'),
('也', '句末语气词，表判断'),
]
),
(
'是故学然后知不足，教然后知困。',
'所以，学习之后才知道自己的不足，教人之后才知道自己有困惑的地方。',
'由类比论证推进到因果论证。“是故”二字承接上文，引出学习和教学的实践效果。“学然后知不足”——学习让人发现自己的欠缺；“教然后知困”——教人让人发现自己的困惑。这一句从正反两面（学与教）说明实践的价值，为下文“自反”“自强”张本。“然后”是“这样以后”的意思，强调了实践先于认知的逻辑顺序。',
[
('是故', '所以，因此，连词。是，这；故，缘故'),
('学', '学习'),
('然后', '这样以后，副词（古今异义：今义为连词，表示接着某种动作或情况之后）'),
('知', '知道'),
('不足', '不够，欠缺的地方'),
('教', '教导，传授知识'),
('然后', '这样以后'),
('知', '知道'),
('困', '困惑，理解不清的地方（古今异义：今义为“困难、疲乏”）'),
]
),
(
'知不足，然后能自反也；知困，然后能自强也。',
'知道自己的不足，然后才能自我反思；知道自己有困惑的地方，然后才能自我勉励。',
'进一步推进论述，说明“知不足”和“知困”之后的行动。“自反”即自我反思，反省自己的不足；“自强”即自我勉励，努力钻研困惑。两个“知……然后能……也”的句式构成对偶，逻辑严密：发现不足→自我反思，发现困惑→自我勉励。“强”读qiǎng，是“勉励”的意思（古今异义：今义为“强大”）。这一句为结尾“教学相长”的结论做了最后的铺垫——学与教都能促进人的成长。',
[
('知', '知道'),
('不足', '不够，欠缺'),
('然后', '这样以后'),
('能', '能够'),
('自反', '自我反思。自，自己；反，反省'),
('也', '句末语气词，表陈述'),
('知', '知道'),
('困', '困惑'),
('然后', '这样以后'),
('能', '能够'),
('自强', '自我勉励。强（qiǎng），勉励（古今异义：今义为“自己努力图强”）'),
('也', '句末语气词，表陈述'),
]
),
(
'故曰：教学相长也。',
'所以说：教与学是互相推动、互相促进的。',
'点明全文中心论点。“教学相长”四字，凝练深刻——教与学不是对立的，而是相辅相成、互相促进的。教别人的过程，也是自己学习和提高的过程；自己学习的过程，也能更好地教别人。这一观点突破了“教就是教，学就是学”的二元对立，揭示了教育的本质规律。“故曰”二字收束上文，语气肯定，是全文的点睛之笔。这一成语至今仍广泛使用，是本文对中国教育思想的重要贡献。',
[
('故', '所以，连词'),
('曰', '说'),
('教学相长', '教与学互相促进。教（jiào），教导；学，学习；相长（zhǎng），互相促进、互相提高（长，促进，动词）'),
('也', '句末语气词，表判断和肯定'),
]
),
(
'《兑命》曰“学学半”，其此之谓乎！',
'《兑命》说：“教别人，占自己学习的一半。”大概说的就是这个道理吧！',
'引用经典作结，增强论证的权威性。《兑命》是《尚书》中的一篇，“兑”通“说”（yuè），指的是商代贤相傅说。“学学半”中，前一个“学”通“敩”（xiào），是“教导”的意思；后一个“学”是“学习”的意思。“学学半”即“教别人，占自己学习的一半”，强调了教对学的促进作用。“其此之谓乎”是反问句，“其”表示推测语气，“此之谓”是“谓此”的倒装，意为“说的就是这个道理吧”。引用经典结尾，既印证了“教学相长”的观点，又使文章余味悠长。',
[
('《兑命》', '《尚书》中的一篇。兑（yuè），通“说”，指傅说（商代贤相）；命，尚书中的一种文体'),
('曰', '说'),
('学学半', '教别人，占自己学习的一半。前一个“学”通“敩”（xiào），教导；后一个“学”，学习'),
('其', '表示推测语气，大概、恐怕，副词'),
('此之谓', '“谓此”的倒装，说的就是这个道理。之，宾语前置的标志'),
('乎', '句末语气词，表反问或推测，吧'),
]
),
]

BG_LEAD = [
'《虽有嘉肴》节选自《礼记·学记》，是《礼记》二则的第一篇。文章以“嘉肴”喻“至道”，通过类比论证，阐述了“教学相长”的道理，强调了实践和学习的重要性。',
'全文仅七十余字，却逻辑严密，层层递进。从“弗食不知旨”的类比，到“学知不足、教知困”的论述，再到“自反自强”的推进，最后以“教学相长”点明中心，引用《兑命》作结。短小精悍，意蕴深远，是中国古代教育思想的经典名篇。',
]

BG_BOXES = [
('作者简介', [
'《礼记》是儒家经典之一，是战国至秦汉间儒家论著的汇编，相传由西汉经学家戴圣编纂，共四十九篇。内容主要是记载和论述先秦的礼制、礼仪，解释仪礼，记录孔子和弟子等的问答，记述修身做人的准则。',
'《学记》是《礼记》中的一篇，是中国古代最早的一篇专门论述教育、教学问题的论著，被称为“教育学的雏形”。它系统地总结了先秦的教育经验和理论，对教育的作用、目的、制度、原则、方法等都有精辟的论述。本文节选的“虽有嘉肴”一段，是《学记》的开篇部分。',
'※ 《礼记》与《周礼》《仪礼》合称“三礼”，是儒家经典“十三经”的重要组成部分，对中国古代文化和教育产生了深远影响。',
]),
('时代背景', [
'<b>先秦教育：</b>春秋战国时期，私学兴起，教育从官府走向民间。孔子开创私学，提出“有教无类”“因材施教”等教育思想。儒家学者在教育实践中积累了丰富的经验，《学记》就是对这些经验的系统总结。',
'<b>百家争鸣：</b>战国时期，诸子百家纷纷著书立说，互相辩论。儒家重视教育，认为教育是治国安邦的基础。《学记》开篇即说：“建国君民，教学为先。”本文通过“嘉肴”与“至道”的类比，强调了学习和实践的重要性，正是儒家教育思想的体现。',
'<b>《学记》的写作：</b>《学记》大约写于战国末期，作者已不可考，一般认为是孟子的学生乐正克所作。全文一千二百余字，系统阐述了教育的作用、目的、制度、原则和方法，是世界教育史上最早的教育专著。',
]),
('文体知识', [
'<b>议论散文：</b>本文是一篇议论性散文，论点明确，论证严密。文章以类比论证开篇，以因果论证推进，最后点明中心论点，引用经典作结。结构完整，逻辑清晰，是先秦议论文的典范。',
'<b>类比论证：</b>本文最突出的论证方法是类比论证。以“嘉肴”喻“至道”，以“弗食不知旨”喻“弗学不知善”，通过人们熟悉的生活经验，说明抽象的教育道理，生动形象，通俗易懂。',
'<b>对偶与排比：</b>文章大量运用对偶句式，如“虽有嘉肴……虽有至道……”“学然后知不足，教然后知困”“知不足……知困……”，句式整齐，节奏明快，读来朗朗上口，增强了文章的气势和说服力。',
]),
]

MEDIA = [
('经典诵读《虽有嘉肴》', 'BV1EA411E7EX'),
('高老师讲语文《虽有嘉肴》', 'BV1N7411u7rr'),
]

APP_BOXES = [
('艺术特色', [
('类比论证，生动形象',
'本文最突出的艺术特色是类比论证。开篇以“虽有嘉肴，弗食，不知其旨也”类比“虽有至道，弗学，不知其善也”——以人们熟悉的“品尝美食”的生活经验，说明“学习道理”的重要性。嘉肴再美，不吃不知道味美；至道再好，不学不知道好处。这种类比，把抽象的教育道理具体化、形象化，让读者一目了然，易于接受。'),
('层层递进，逻辑严密',
'文章结构严谨，层层递进。第一步，以类比论证说明学习的重要性（弗学不知善）；第二步，说明学与教的效果（学知不足，教知困）；第三步，说明知不足与知困后的行动（自反、自强）；第四步，点明中心论点（教学相长）；第五步，引用经典印证（《兑命》曰“学学半”）。五步环环相扣，逻辑严密，从具体到抽象，从现象到本质，最后得出结论。'),
('对偶排比，气势充沛',
'文章大量运用对偶和排比句式。“虽有嘉肴……虽有至道……”是对偶；“学然后知不足，教然后知困”是对偶；“知不足，然后能自反也；知困，然后能自强也”是对偶。这些对偶句式，结构整齐，节奏明快，读来朗朗上口，增强了文章的气势和说服力。同时，“然后”一词的反复使用，形成了排比的效果，强调了实践先于认知的逻辑顺序。'),
]),
('名句赏析', [
('虽有嘉肴，弗食，不知其旨也；虽有至道，弗学，不知其善也。',
'全文的起笔之句，也是类比论证的经典范例。以“嘉肴”喻“至道”，以“食”喻“学”，以“旨”喻“善”——通过人们熟悉的生活经验，说明抽象的教育道理。两个“虽……弗……不知……”的句式构成工整的对偶，从反面强调了实践的重要性。这一句不仅是全文的逻辑起点，也成为流传千古的名句，启示人们：任何知识和道理，都必须通过亲身实践才能真正理解。'),
('学然后知不足，教然后知困。',
'这一句揭示了学习和教学的辩证关系。学习让人发现自己的不足，教学让人发现自己的困惑——学与教都是发现问题的过程。“然后”二字强调了实践先于认知的逻辑：只有先去学、先去教，才能知道自己哪里不足、哪里困惑。这一句为下文“自反”“自强”的论述做了铺垫，也为“教学相长”的中心论点提供了论据。'),
('教学相长也。',
'全文的中心论点，四个字，凝练深刻。“教学相长”即教与学互相促进、互相提高——教别人的过程，也是自己学习和提高的过程；自己学习的过程，也能更好地教别人。这一观点突破了“教就是教，学就是学”的二元对立，揭示了教育的本质规律。这一成语至今仍广泛使用，是本文对中国教育思想的重要贡献，也是世界教育史上最早的“教学相长”理论。'),
]),
('主题思想', [
'《虽有嘉肴》通过“嘉肴”与“至道”的类比，阐述了“教学相长”的道理，强调了实践和学习的重要性。文章认为，再好的道理，不学就不知道它的好处；学习之后才能知道自己的不足，教学之后才能知道自己的困惑；知道不足才能自我反思，知道困惑才能自我勉励。教与学是相辅相成、互相促进的。',
'文章的深层主题，是探讨教育的本质和规律。“教学相长”的观点，揭示了教与学的辩证关系——教不是单向的灌输，学也不是被动的接受，而是师生双方在教学过程中共同成长。这一思想，对今天的教育仍有重要的启示意义：教师在教学生的同时，也在不断学习和提高；学生在学习的过程中，也可以通过讨论和交流，促进教师的思考和成长。',
'同时，文章也强调了实践的重要性。“弗食不知旨，弗学不知善”——任何知识和道理，都必须通过亲身实践才能真正理解。这一观点，与儒家“知行合一”的思想一脉相承，对我们今天的学习和生活仍有重要的指导意义。',
]),
]

ACC_BOXES = [
('通假字', [
['字', '通假', '例句', '释义'],
['兑', '通“说”', '《兑命》曰', '读 yuè，指傅说（商代贤相）'],
['学', '通“敩”', '学学半（前一个“学”）', '读 xiào，教导'],
]),
('古今异义', [
['词', '古义', '今义', '例句'],
['虽', '即使', '虽然', '虽有嘉肴'],
['旨', '味美', '意义、目的', '不知其旨也'],
['至道', '最好的道理', '宽阔的路', '虽有至道'],
['困', '困惑，理解不清', '困难、疲乏', '教然后知困'],
['自强', '自我勉励', '自己努力图强', '然后能自强也'],
['长', '促进，提高', '成长、长度', '教学相长'],
['然后', '这样以后', '连词，表接着', '学然后知不足'],
]),
('一词多义', [
['词', '义项', '例句'],
['学', '学习', '弗学，不知其善也 / 学然后知不足'],
['学', '通“敩”，教导', '学学半（前一个“学”）'],
['其', '它的，代词', '不知其旨也 / 不知其善也'],
['其', '表示推测，大概', '其此之谓乎'],
['食', '吃，动词', '弗食，不知其旨也'],
['食', '食物，名词', '衣食所安（《曹刿论战》）'],
['道', '道理', '虽有至道'],
['道', '说，讲', '不足为外人道也（《桃花源记》）'],
['善', '好处，形容词作名词', '不知其善也'],
['善', '好的，善良的', '择其善者而从之（《论语》）'],
]),
('词类活用', [
['词', '活用类型', '释义', '例句'],
['善', '形容词作名词', '好处', '不知其善也'],
['旨', '形容词作名词', '味美的地方', '不知其旨也'],
['长', '形容词作动词', '促进、提高', '教学相长'],
['困', '形容词作名词', '困惑的地方', '教然后知困'],
]),
('文言句式', [
['句式', '例句', '说明'],
['判断句', '不知其旨也', '“也”表判断，“就不知道它的味美”'],
['判断句', '教学相长也', '“也”表判断，“教与学是互相促进的”'],
['倒装句（宾语前置）', '其此之谓乎', '正常语序为“其谓此乎”，“之”是宾语前置的标志，“大概说的就是这个道理吧”'],
['反问句', '其此之谓乎', '“其……乎”表推测反问，“大概……吧”'],
['省略句', '（人）弗食，不知其旨也', '承前省略主语“人”'],
]),
('文化常识', [
('《礼记》', '儒家经典之一，战国至秦汉间儒家论著的汇编，相传由西汉戴圣编纂，共四十九篇。与《周礼》《仪礼》合称“三礼”，是“十三经”之一。内容涉及礼制、礼仪、教育、哲学等，是研究中国古代社会和文化的重要资料。'),
('《学记》', '《礼记》中的一篇，是中国古代最早的专门论述教育、教学问题的论著，被称为“教育学的雏形”。全文一千二百余字，系统阐述了教育的作用、目的、制度、原则和方法，提出了“教学相长”“长善救失”“启发诱导”等重要教育思想，对中国古代教育产生了深远影响。'),
('《兑命》', '《尚书》中的一篇，“兑”通“说”（yuè），指商代贤相傅说。“命”是《尚书》的一种文体，是君王对臣子的命令或告诫。《兑命》记载了商王武丁与傅说的对话，其中“学学半”一句，强调了教对学的促进作用，是“教学相长”思想的经典出处。'),
('教学相长', '本文的中心论点，也是中国古代教育思想的重要命题。指教与学是相辅相成、互相促进的——教别人的过程，也是自己学习和提高的过程。这一思想最早见于《学记》，至今仍是教育的基本原则之一，启示教师在教学过程中不断学习和提高，也启示学生在学习过程中通过讨论和交流促进理解。'),
('类比论证', '本文最突出的论证方法。以“嘉肴”喻“至道”，以“弗食不知旨”喻“弗学不知善”，通过人们熟悉的生活经验说明抽象的教育道理。类比论证是先秦议论文常用的论证方法，如《孟子》的“五十步笑百步”、《庄子》的“庖丁解牛”等，都是类比论证的经典范例。'),
]),
]

DICT_WORDS = [
{'w':'肴','py':'yáo','q':'虽有嘉□','tip':'「肴」肉字旁，音 yáo，意为荤菜，勿写“尧”“淆”'},
{'w':'弗','py':'fú','q':'□食，不知其旨也','tip':'「弗」弓字旁，音 fú，意为不，勿写“佛”“拂”'},
{'w':'旨','py':'zhǐ','q':'不知其□也','tip':'「旨」日字旁，音 zhǐ，意为味美，勿写“指”“脂”'},
{'w':'强','py':'qiǎng','q':'然后能自□也','tip':'「强」弓字旁，音 qiǎng，意为勉励，勿读 qiáng，勿写“墙”“蔷”'},
{'w':'兑','py':'yuè','q':'《□命》曰','tip':'「兑」儿字旁，通“说”读 yuè，勿读 duì，勿写“说”“锐”'},
{'w':'敩','py':'xiào','q':'□学半','tip':'「敩」反文旁，音 xiào，意为教导，通“学”，勿写“学”“觉”'},
{'w':'嘉','py':'jiā','q':'虽有□肴','tip':'「嘉」士字底，音 jiā，意为美好，勿写“佳”“加”'},
{'w':'反','py':'fǎn','q':'然后能自□也','tip':'「反」又字旁，音 fǎn，意为反省，勿写“返”“饭”'},
{'w':'困','py':'kùn','q':'教然后知□','tip':'「困」口字框，音 kùn，意为困惑，勿写“因”“捆”'},
{'w':'长','py':'zhǎng','q':'教学相□','tip':'「长」独体字，音 zhǎng，意为促进，勿读 cháng，勿写“常”“涨”'},
]

DICT_NOTES = [
{'w':'虽','q':'虽有嘉肴','a':'即使，表假设连词（古今异义：今义为“虽然”）'},
{'w':'嘉肴','q':'虽有嘉肴','a':'美味的肉食。嘉，美好；肴（yáo），荤菜'},
{'w':'弗','q':'弗食，不知其旨也','a':'（fú）不，否定副词'},
{'w':'旨','q':'不知其旨也','a':'（zhǐ）味美（古今异义：今义为“意义、目的”）'},
{'w':'至道','q':'虽有至道','a':'最好的道理。至，达到极点的；道，道理'},
{'w':'善','q':'不知其善也','a':'好处，形容词作名词'},
{'w':'是故','q':'是故学然后知不足','a':'所以，因此。是，这；故，缘故'},
{'w':'困','q':'教然后知困','a':'困惑，理解不清的地方（古今异义：今义为“困难”）'},
{'w':'自反','q':'然后能自反也','a':'自我反思。自，自己；反，反省'},
{'w':'自强','q':'然后能自强也','a':'自我勉励。强（qiǎng），勉励'},
{'w':'教学相长','q':'教学相长也','a':'教与学互相促进。长（zhǎng），促进'},
{'w':'兑','q':'《兑命》曰','a':'通“说”（yuè），指傅说'},
{'w':'学学半','q':'学学半','a':'教别人，占自己学习的一半。前一个“学”通“敩”（xiào），教导'},
{'w':'其','q':'其此之谓乎','a':'表示推测语气，大概、恐怕'},
{'w':'此之谓','q':'其此之谓乎','a':'“谓此”的倒装，说的就是这个道理。之，宾语前置标志'},
]

with open(r'D:\App\Apps\yanshi\beimingyouyu-zhuangzi.html', 'r', encoding='utf-8') as f:
    tpl = f.read()
css = re.search(r'<style>(.*?)</style>', tpl, re.S).group(1)
js_main = re.search(r"<script>\s*\(function\(\)\{(.*?)\}\)\(\);\s*</script>", tpl, re.S).group(1)
js_main = js_main.replace('beimingyouyu_fs', FS_KEY)

def annotate(text, zhushi):
    result = text
    items = sorted(zhushi, key=lambda x: len(x[0]), reverse=True)
    used = set()
    for word, note in items:
        if word in used:
            continue
        idx = result.find(word)
        if idx >= 0:
            before = result[:idx]
            if before.count('<span class="anno-word"') > before.count('</span>'):
                continue
            span = '<span class="anno-word" data-note="' + note + '">' + word + '</span>'
            result = result[:idx] + span + result[idx+len(word):]
            used.add(word)
    return result

def build_verse(i, v):
    orig, trans, app, zhushi = v
    annotated = annotate(orig, zhushi)
    return '''      <div class="verse" id="l''' + str(i+1) + '''" data-i="''' + str(i) + '''">
        <div class="v-top"><span class="v-no">''' + str(i+1) + '''</span><div class="v-line">''' + annotated + '''</div></div>
        <details class="v-more">
          <summary>译文 · 赏析</summary>
          <div class="d-body">
            <div class="v-sec"><b class="v-label">译　文</b>
              <div class="v-trans">''' + trans + '''</div>
            </div>
            <div class="v-sec"><b class="v-label">赏　析</b>
              <div class="d-body"><p>''' + app + '''</p></div>
              <div class="tags"><span>教学相长</span><span>类比论证</span></div>
            </div>
          </div>
        </details>
      </div>'''

verses_html = '\n'.join(build_verse(i, v) for i, v in enumerate(VERSES))
fulltext_lines = '\n'.join('    <div class="pl">' + v[0] + '</div>' for v in VERSES)

bg_boxes_html = ''
for title, paras in BG_BOXES:
    ps = '\n'.join('<p>' + p + '</p>' for p in paras)
    bg_boxes_html += '  <div class="box">\n    <h3>' + title + '</h3>\n' + ps + '\n  </div>\n'

lead_html = '\n'.join('<p>' + p + '</p>' for p in BG_LEAD)

media_html = ''
for i, (title, bv) in enumerate(MEDIA):
    mid = 'mediaF' + str(i+1)
    media_html += '''      <div class="media">
        <h4>''' + title + '''</h4>
        <iframe id="''' + mid + '''" src="https://player.bilibili.com/player.html?bvid=''' + bv + '''&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="''' + title + '''"></iframe>
        <a href="https://www.bilibili.com/video/''' + bv + '''" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="''' + mid + '''">全屏播放</button>
      </div>'''

app_html = ''
for title, items in APP_BOXES:
    if isinstance(items[0], tuple):
        cards = ''
        for line, p in items:
            cards += '      <div class="fame-card">\n        <div class="f-line">' + line + '</div>\n        <p>' + p + '</p>\n      </div>\n'
        app_html += '  <div class="box">\n    <h3>' + title + '</h3>\n    <div class="fame">\n' + cards + '    </div>\n  </div>\n'
    else:
        ps = '\n'.join('<p>' + p + '</p>' for p in items)
        app_html += '  <div class="box">\n    <h3>' + title + '</h3>\n' + ps + '\n  </div>\n'

acc_html = ''
for title, data in ACC_BOXES:
    if isinstance(data, list) and isinstance(data[0], list):
        header = data[0]
        rows = data[1:]
        th = ''.join('<th>' + h + '</th>' for h in header)
        trs = ''
        for row in rows:
            tds = ''
            for j, cell in enumerate(row):
                if j == 0 and cell and '（本文无' not in cell:
                    tds += '<td class="kai">' + cell + '</td>'
                else:
                    tds += '<td>' + cell + '</td>'
            trs += '<tr>' + tds + '</tr>\n'
        acc_html += '  <div class="box">\n    <h3>' + title + '</h3>\n    <div class="tw"><table>\n      <tr>' + th + '</tr>\n' + trs + '    </table></div>\n  </div>\n'
    else:
        items_html = ''
        for dt, dd in data:
            items_html += '      <div class="g-item"><dt>' + dt + '</dt><dd>' + dd + '</dd></div>\n'
        acc_html += '  <div class="box">\n    <h3>' + title + '</h3>\n    <div class="glossary">\n' + items_html + '    </div>\n  </div>\n'

words_json = json.dumps(DICT_WORDS, ensure_ascii=False)
notes_json = json.dumps(DICT_NOTES, ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《''' + TITLE + '''》</title>
<meta name="description" content="《礼记》之《虽有嘉肴》教学课件：逐句注释译文赏析、文言积累、教学相长、全屏听写练习。">
<style>''' + css + '''</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">''' + HERO_SIDE + '''</div>
  <h1 class="hero-title">''' + TITLE + '''</h1>
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
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 文体</span></div>
  <div class="lead">
''' + lead_html + '''
  </div>
''' + bg_boxes_html + '''  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
''' + media_html + '''
    </div>
  </div>
</section>


<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>
  <div class="sec-sub">全文五句，短篇不分部分。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
''' + fulltext_lines + '''
  </div>
  <div class="verse-list" id="verseList">
''' + verses_html + '''
  </div>
</section>

<div class="divider"></div>

<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">艺术 · 名句 · 主题</span></div>

''' + app_html + '''
</section>


<div class="divider"></div>

<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">通假 · 古今异义 · 一词多义 · 活用 · 句式 · 文化常识</span></div>

''' + acc_html + '''
</section>


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
  <div class="kai">《''' + TITLE + '''》</div>
  <div>《礼记》 · 先秦 · 选自《学记》，《礼记》二则之一</div>
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

(function(){
''' + js_main + '''
})();

</script>
<script>
var DICT_WORDS = ''' + words_json + ''';
var DICT_NOTES = ''' + notes_json + ''';
</script>

</body>
</html>'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)

print('已生成:', OUT)
print('句子数:', len(VERSES))
print('字形题:', len(DICT_WORDS))
print('注释题:', len(DICT_NOTES))
