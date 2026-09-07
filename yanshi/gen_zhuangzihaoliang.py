# -*- coding: utf-8 -*-
# 生成《庄子与惠子游于濠梁》交互式教学HTML课件
# 所有Python字符串用单引号，内部用中文引号
import json, re

OUT = r'D:\App\Apps\yanshi\zhuangziyuhuiziyouyuhaoliang-zhuangzi.html'
FS_KEY = 'zhuangzihaoliang_fs'
TITLE = '庄子与惠子游于濠梁'
HERO_SIDE = '先秦 · 庄子'

# 逐句数据: (原文, 译文, 赏析, [(词,注释),...])
VERSES = [
(
'庄子与惠子游于濠梁之上。',
'庄子和惠子在濠水的桥上游玩。',
'开篇交代人物、地点和事件，用笔极简。“庄子与惠子”点出两位论辩主角，“游于濠梁之上”点明闲适的游玩场景——正是在这样轻松的氛围中，一场千古名辩自然展开。“濠梁”即濠水上的桥，后成为典故，代指朋友间的从容论辩。',
[
('庄子', '（约前369—前286）名周，战国时宋国人，道家学派代表人物'),
('与', '和，连词'),
('惠子', '即惠施，战国时宋国人，名家学派代表人物，庄子的好友'),
('游', '游玩，游览'),
('于', '在，介词'),
('濠', '（háo）濠水，水名，在今安徽凤阳'),
('梁', '桥'),
('之', '的，结构助词'),
('上', '上面，这里指桥上'),
]
),
(
'庄子曰：“鲦鱼出游从容，是鱼之乐也。”',
'庄子说：“鲦鱼在河水中游得多么悠闲自得，这是鱼的快乐啊。”',
'庄子首先发起话题，以“鲦鱼出游从容”的直观感受，断言“是鱼之乐也”。这不是逻辑推理，而是一种审美体验——庄子以物我合一的心境，将自己的从容快乐投射到鱼身上。“从容”二字，既写鱼游的自在，也写庄子心境的悠然。这一句是全文论辩的起点，也奠定了庄子“物我合一”的哲学基调。',
[
('曰', '说'),
('鲦鱼', '（tiáo）一种白色小鱼，俗称餐鲦鱼'),
('出游', '出来游动'),
('从容', '悠闲自得的样子'),
('是', '这，指示代词'),
('鱼之乐', '鱼的快乐。之，的，结构助词'),
('也', '句末语气词，表判断'),
]
),
(
'惠子曰：“子非鱼，安知鱼之乐？”',
'惠子说：“你不是鱼，怎么知道鱼的快乐呢？”',
'惠子立刻从逻辑角度反驳。“子非鱼”是前提，“安知鱼之乐”是反问——惠子认为，不同物种之间无法相互理解，你不是鱼，就不可能知道鱼的快乐。“安”是“怎么”的意思，表反问。这一句抓住了庄子断言中的逻辑漏洞，体现了惠子严谨的逻辑思维，也将论辩推向深入。',
[
('子', '你，对对方的尊称'),
('非', '不是'),
('安', '怎么，哪里，疑问代词，表反问'),
('知', '知道，了解'),
('鱼之乐', '鱼的快乐。之，的'),
]
),
(
'庄子曰：“子非我，安知我不知鱼之乐？”',
'庄子说：“你不是我，怎么知道我不知道鱼的快乐呢？”',
'庄子没有正面回答，而是以子之矛攻子之盾——用惠子的逻辑反驳惠子。你说“子非鱼，安知鱼之乐”，那我反问你：“子非我，安知我不知鱼之乐？”这是典型的归谬法：如果不同个体之间不能相互理解，那么你也不能理解我，你凭什么说我不知道鱼的快乐？庄子的机智在此尽显，论辩进入第一个回合的高潮。',
[
('子', '你'),
('非', '不是'),
('我', '我，庄子自称'),
('安', '怎么，哪里，疑问代词'),
('知', '知道'),
('不知', '不知道'),
('鱼之乐', '鱼的快乐'),
]
),
(
'惠子曰：“我非子，固不知子矣；子固非鱼也，子之不知鱼之乐，全矣！”',
'惠子说：“我不是你，固然不知道你；你本来就不是鱼，你不知道鱼的快乐，是完全可以确定的了！”',
'惠子进一步推进逻辑，形成完整的推理链条。“我非子，固不知子矣”——承认不同个体之间不能相互理解；“子固非鱼也，子之不知鱼之乐，全矣”——由此推出你也不知道鱼的快乐。两个“固”字含义不同：第一个“固”是“固然”，第二个“固”是“本来”。“全矣”是“完全确定了”的意思，语气肯定，惠子自以为胜券在握。这一句逻辑严密，是名家思辨的典型体现。',
[
('我', '我，惠子自称'),
('非', '不是'),
('子', '你'),
('固', '固然，承认某个事实'),
('不知', '不知道'),
('矣', '句末语气词，表陈述，了'),
('子', '你'),
('固', '本来，副词'),
('非', '不是'),
('鱼', '鱼'),
('也', '句中语气词，表停顿'),
('子之不知', '你不知道。之，用于主谓之间，取消句子独立性'),
('鱼之乐', '鱼的快乐。之，的'),
('全', '完全，完备，这里指完全确定'),
('矣', '句末语气词，表肯定，了'),
]
),
(
'庄子曰：“请循其本。子曰‘汝安知鱼乐’云者，既已知吾知之而问我，我知之濠上也。”',
'庄子说：“请从我们最初的话题说起。你说‘你哪里知道鱼快乐’的话，说明你已经知道我知道鱼快乐而在问我。我是在濠水的桥上知道的。”',
'这是全文的点睛之笔，庄子以偷换概念的方式巧妙“胜出”。“请循其本”——回到话题的起点。惠子问的“安知鱼之乐”中，“安”可以理解为“怎么”（表反问），也可以理解为“哪里”（表处所）。庄子故意将“安”曲解为“哪里”，把“怎么知道”变成了“在哪里知道”，然后回答“我知之濠上也”——我是在濠桥上知道的。这看似是诡辩，实则体现了庄子的哲学智慧：他不从逻辑上纠缠，而是回到“物我合一”的体验本身——我在濠桥上感受到了鱼的快乐，这就是答案。“既已知吾知之而问我”一句，更点出惠子的提问本身就预设了庄子“知”的可能性。全文以机智的反转收束，余味无穷。',
[
('请', '请允许我，表敬副词'),
('循', '追溯，顺着'),
('其', '那，指示代词，指话题的本源'),
('本', '本源，最初的话题'),
('子曰', '你说。子，你；曰，说'),
('汝', '（rǔ）你，第二人称代词'),
('安', '哪里，疑问代词（庄子故意将“怎么”曲解为“哪里”）'),
('知', '知道'),
('鱼乐', '鱼的快乐'),
('云者', '助词，用于句末，表“如此这般的话”，相当于“……的话”'),
('既已', '已经'),
('知', '知道'),
('吾', '我，庄子自称'),
('知之', '知道它（指鱼之乐）。之，代词，指鱼之乐'),
('而', '连词，表转折，却'),
('问我', '问我'),
('我', '我'),
('知之', '知道它。之，代词，指鱼之乐'),
('濠上', '濠水的桥上。濠，（háo）濠水；上，上面'),
('也', '句末语气词，表陈述'),
]
),
]

# 背景区
BG_LEAD = [
'《庄子与惠子游于濠梁》节选自《庄子·秋水》，是《庄子》二则的第二篇。文章通过庄子与惠子在濠水桥上的一场辩论，展现了两人不同的思维方式和哲学立场。',
'全文仅百余字，却波澜起伏，机锋迭出。庄子以“物我合一”的审美体验断言鱼之乐，惠子以逻辑推理质疑其可能性，最终庄子以偷换概念的方式巧妙收束。这场“濠梁之辩”，是中国哲学史上最著名的辩论之一。',
]

BG_BOXES = [
('作者简介', [
'庄子（约前369—前286），名周，战国时期宋国蒙（今河南商丘东北）人，道家学派的代表人物，与老子并称“老庄”。他曾做过蒙地的漆园吏，后辞官不仕，过着清贫的生活。',
'庄子继承并发展了老子的道家思想，主张“道法自然”“无为而治”，追求精神的绝对自由。其文汪洋恣肆，想象丰富，善用寓言说理，具有浓厚的浪漫主义色彩。《庄子》一书，又名《南华经》，是道家经典之一，共三十三篇，分内篇、外篇、杂篇。',
'※ 庄子的文章，“意出尘外，怪生笔端”，鲁迅赞其“汪洋辟阖，仪态万方，晚周诸子之作，莫能先也”。',
]),
('时代背景', [
'<b>战国乱世：</b>庄子生活在战国中期，诸侯争霸，战乱频仍，社会动荡。面对残酷的现实，庄子不愿同流合污，转而追求精神的超越与自由。',
'<b>百家争鸣：</b>战国时期是中国思想史上最活跃的时代，儒、道、墨、名、法等各家学派纷纷著书立说，互相辩论。惠子是名家学派的代表人物，以逻辑思辨著称；庄子是道家学派的代表人物，以直觉体验见长。两人的辩论，正是不同思维方式的碰撞。',
'<b>庄惠之交：</b>庄子与惠子虽然观点不同，却是挚友。《庄子》一书中多次记载两人的辩论，如“濠梁之辩”“惠子相梁”等。惠子死后，庄子曾感叹“自夫子之死也，吾无以为质矣，吾无与言之矣”——自从惠子死了，我就没有辩论的对手了。',
]),
('文体知识', [
'<b>寓言说理：</b>庄子的文章，“寓言十九”（十句话里九句是寓言）。他不直接讲道理，而是通过寓言故事、人物对话来表达哲学思想。本文就是一篇对话体寓言，通过庄惠二人的辩论，展现了两种不同的认知方式。',
'<b>对话体：</b>全文以对话为主，庄子与惠子你一言我一语，论辩层层推进。对话体的好处是生动形象，能让读者在论辩的过程中自己体会其中的哲理，而不是被动接受说教。',
'<b>《秋水》篇：</b>本文节选自《庄子·秋水》。《秋水》是《庄子》外篇中的名篇，主要讨论价值判断的相对性。“濠梁之辩”是《秋水》篇的最后一个故事，也是最著名的一个。',
]),
]

MEDIA = [
('经典诵读《庄子与惠子游于濠梁》', 'BV15t4y1i7gc'),
('濠梁之辩：古代辩论赛，谁赢了？', 'BV1cW41117sZ'),
]

# 赏析区
APP_BOXES = [
('人物形象', [
('庄子：物我合一，机智超然',
'庄子是道家哲学的化身。他以“物我合一”的心境看待世界，将自己的快乐投射到鱼身上，断言“是鱼之乐也”。面对惠子的逻辑质疑，他不正面交锋，而是以子之矛攻子之盾，最后以偷换概念的方式巧妙收束。庄子的形象，是超然物外、机智幽默的哲学家——他不在逻辑的迷宫里纠缠，而是回到生命体验本身。'),
('惠子：逻辑严谨，求真务实',
'惠子是名家学派的代表，以逻辑思辨著称。他从“子非鱼”的前提出发，一步步推出“子之不知鱼之乐，全矣”的结论，推理严密，无懈可击。惠子的形象，是求真务实、严谨理性的逻辑学家——他代表了人类理性思维的力量，与庄子的直觉体验形成鲜明对照。两人的辩论，正是中国哲学史上“诗性智慧”与“逻辑智慧”的经典碰撞。'),
]),
('艺术特色', [
('对话精妙，机锋迭出',
'全文以对话为主，仅六句话，却波澜起伏。庄子发起→惠子质疑→庄子反问→惠子推进→庄子反转，五个回合层层递进，每一句都紧扣上一句，逻辑链条完整。对话语言简洁有力，如“子非鱼，安知鱼之乐”“子非我，安知我不知鱼之乐”，句式整齐，节奏感强，读来如闻其声。'),
('以小见大，寓哲于辩',
'文章从“鱼之乐”这样一个小话题切入，却引出了深刻的哲学问题：不同个体之间能否相互理解？认知的基础是什么？是逻辑推理还是直觉体验？庄子与惠子的辩论，实际上是两种认知方式的较量——庄子代表审美体验和物我合一，惠子代表逻辑推理和主客二分。文章不给出标准答案，而是让读者在辩论中自己思考。'),
('结尾反转，余味无穷',
'最后一句“我知之濠上也”，是全文的点睛之笔。庄子故意将“安”曲解为“哪里”，把“怎么知道”变成了“在哪里知道”，然后给出一个看似答非所问的回答。这不是简单的诡辩，而是庄子哲学的体现：他不从逻辑上证明“我知道鱼之乐”，而是说“我在濠桥上体验到了鱼之乐”——知识来源于体验，而非推理。这个结尾，既机智又深刻，令人回味无穷。'),
]),
('名句赏析', [
('子非鱼，安知鱼之乐？',
'惠子的经典反问，简洁有力，直击要害。“子非鱼”是前提，“安知鱼之乐”是反问——你不是鱼，怎么可能知道鱼的快乐？这一句话，代表了逻辑思维的基本立场：不同主体之间无法直接相互理解。这句话后来成为常用成语，用来质疑他人对事物的判断。但庄子的回答告诉我们：理解不一定需要逻辑，审美体验本身就是一种理解。'),
('子非我，安知我不知鱼之乐？',
'庄子的经典反击，以子之矛攻子之盾。你说“子非鱼，安知鱼之乐”，那我反问你：“子非我，安知我不知鱼之乐？”如果不同个体之间不能相互理解，那么你也不能理解我，你凭什么说我不知道鱼的快乐？这是典型的归谬法，用对方的逻辑反驳对方，机智无比。句式与惠子的话完全对应，形成工整的对答，读来畅快淋漓。'),
('我知之濠上也。',
'全文的点睛之笔，五个字，意蕴无穷。庄子不说“我通过推理知道鱼之乐”，也不说“我凭直觉知道鱼之乐”，而是说“我知之濠上也”——我是在濠水的桥上知道的。这个回答，把抽象的哲学问题拉回到具体的生活场景：我在濠桥上，看到鱼从容出游，我感受到了鱼的快乐——这就是知识的来源。庄子用这种方式，超越了逻辑的纠缠，回到了“物我合一”的生命体验本身。'),
]),
('主题思想', [
'《庄子与惠子游于濠梁》通过庄惠二人的“濠梁之辩”，展现了两种不同的认知方式和哲学立场。惠子代表逻辑理性，认为不同主体之间无法相互理解；庄子代表审美体验，主张“物我合一”，认为人可以通过直觉体验感受到外物的快乐。',
'文章的深层主题，是探讨认知的本质和人与世界的关系。庄子的“我知之濠上也”，暗示了一种超越主客二分的认知方式：不是主体去认识客体，而是主体在与世界的交融中直接体验到世界的意义。这种“物我合一”的境界，正是庄子哲学的核心——“天地与我并生，而万物与我为一”。',
'同时，文章也展现了庄子与惠子的深厚友谊。两人虽然观点不同，却能在辩论中互相启发，这种“和而不同”的友谊，也是文章的动人之处。',
]),
]

# 积累区
ACC_BOXES = [
('通假字', [
['字', '通假', '例句', '释义'],
['（本文无通假字）', '', '', ''],
]),
('古今异义', [
['词', '古义', '今义', '例句'],
['从容', '悠闲自得的样子', '不慌不忙，镇静', '鲦鱼出游从容'],
['安', '怎么，哪里（疑问代词）', '安全，安定', '安知鱼之乐'],
['全', '完全，确定', '全部，整个', '子之不知鱼之乐，全矣'],
['循', '追溯，顺着', '遵循，依照', '请循其本'],
['本', '本源，最初的话题', '本来，根本', '请循其本'],
]),
('一词多义', [
['词', '义项', '例句'],
['固', '固然（承认事实）', '我非子，固不知子矣'],
['固', '本来（副词）', '子固非鱼也'],
['之', '的，结构助词', '是鱼之乐也 / 濠梁之上'],
['之', '用于主谓之间，取消句子独立性', '子之不知鱼之乐'],
['之', '代词，指鱼之乐', '既已知吾知之而问我 / 我知之濠上也'],
['安', '怎么，哪里（表反问）', '安知鱼之乐 / 安知我不知鱼之乐'],
['安', '哪里（表处所，庄子曲解义）', '汝安知鱼乐'],
['也', '句末语气词，表判断', '是鱼之乐也'],
['也', '句中语气词，表停顿', '子固非鱼也'],
['也', '句末语气词，表陈述', '我知之濠上也'],
['子', '你（尊称）', '子非鱼 / 子非我'],
['子', '先生，指惠子', '子曰‘汝安知鱼乐’'],
]),
('词类活用', [
['词', '活用类型', '释义', '例句'],
['（本文无明显词类活用）', '', '', ''],
]),
('文言句式', [
['句式', '例句', '说明'],
['判断句', '是鱼之乐也', '“也”表判断，“这是鱼的快乐”'],
['反问句', '子非鱼，安知鱼之乐？', '“安”表反问，“怎么……呢？”'],
['反问句', '子非我，安知我不知鱼之乐？', '“安”表反问'],
['倒装句（状语后置）', '庄子与惠子游于濠梁之上', '正常语序为“庄子与惠子于濠梁之上游”，“在濠梁之上游玩”'],
['省略句', '（庄子）曰：“鲦鱼出游从容……”', '承前省略主语“庄子”'],
['固定句式', '……云者', '“……的话”，表引用，如“子曰‘汝安知鱼乐’云者”'],
]),
('文化常识', [
('庄子与《庄子》', '庄子（约前369—前286），名周，战国时宋国人，道家学派代表人物，与老子并称“老庄”。《庄子》又名《南华经》，道家经典之一，共三十三篇，分内篇、外篇、杂篇。其文汪洋恣肆，想象丰富，善用寓言说理。'),
('惠子与名家', '惠子（约前370—前310），名施，战国时宋国人，名家学派代表人物，曾任魏相。名家以逻辑思辨和概念分析著称，惠子提出“合同异”等命题，与公孙龙的“离坚白”并称。惠子是庄子的挚友，《庄子》中多次记载两人的辩论。'),
('濠梁之辩', '指庄子与惠子在濠水桥上关于“鱼之乐”的辩论，是中国哲学史上最著名的辩论之一。“濠梁”后来成为典故，代指朋友间的从容论辩和物我合一的审美境界。如辛弃疾词“濠梁上，观鱼胜，濠梁上，观鱼乐”。'),
('物我合一', '庄子哲学的核心概念之一，指主体与客体融为一体，不分物我。庄子认为，人可以通过直觉体验，超越主客二分，达到“天地与我并生，而万物与我为一”的境界。“鲦鱼出游从容，是鱼之乐也”正是物我合一的体现——庄子将自己的快乐投射到鱼身上。'),
('《秋水》篇', '《庄子》外篇中的名篇，主要讨论价值判断的相对性。篇中通过“河伯与北海若”的对话，说明人的认知受限于时空和视角；“濠梁之辩”是篇末的故事，进一步探讨认知的本质。'),
('寓言十九', '出自《庄子·寓言》：“寓言十九，重言十七，卮言日出。”意思是庄子的文章，十句话里九句是寓言。庄子不直接讲道理，而是通过寓言故事、人物对话来表达哲学思想，本文就是典型的对话体寓言。'),
]),
]

# 题库
DICT_WORDS = [
{'w':'濠','py':'háo','q':'□梁之上','tip':'「濠」三点水，音 háo，水名，勿写“豪”“毫”'},
{'w':'鲦','py':'tiáo','q':'□鱼出游从容','tip':'「鲦」鱼字旁，音 tiáo，小鱼名，勿写“条”“绦”'},
{'w':'汝','py':'rǔ','q':'子非□','tip':'「汝」三点水，音 rǔ，意为你，勿写“女”“如”'},
{'w':'循','py':'xún','q':'请□其本','tip':'「循」彳旁，音 xún，意为追溯，勿写“寻”“巡”'},
{'w':'惠','py':'huì','q':'庄子与□子游','tip':'「惠」心字底，音 huì，人名，勿写“慧”“穗”'},
{'w':'梁','py':'liáng','q':'濠□之上','tip':'「梁」木字旁，音 liáng，意为桥，勿写“粱”（米字旁）'},
{'w':'从容','py':'cóng róng','q':'出游□□','tip':'「从容」叠词整体作答案，“从”双人旁，“容”宝盖头，勿写“从荣”'},
{'w':'固','py':'gù','q':'□不知子矣','tip':'「固」口字框，音 gù，意为固然/本来，勿写“故”“顾”'},
{'w':'矣','py':'yǐ','q':'全□','tip':'「矣」矢字旁，音 yǐ，句末语气词，勿写“已”“以”'},
{'w':'濠上','py':'háo shàng','q':'我知之□□','tip':'「濠上」指濠水桥上，“濠”三点水，叠词整体作答案'},
]

DICT_NOTES = [
{'w':'濠梁','q':'庄子与惠子游于濠梁之上','a':'（háo）濠水上的桥。濠，濠水；梁，桥'},
{'w':'是','q':'是鱼之乐也','a':'这，指示代词'},
{'w':'安','q':'安知鱼之乐','a':'怎么，哪里，疑问代词，表反问'},
{'w':'固','q':'固不知子矣','a':'固然，承认某个事实'},
{'w':'固','q':'子固非鱼也','a':'本来，副词'},
{'w':'全','q':'子之不知鱼之乐，全矣','a':'完全，完备，这里指完全确定'},
{'w':'循','q':'请循其本','a':'追溯，顺着'},
{'w':'本','q':'请循其本','a':'本源，最初的话题'},
{'w':'云者','q':'子曰‘汝安知鱼乐’云者','a':'助词，用于句末，表“……的话”'},
{'w':'既已','q':'既已知吾知之而问我','a':'已经'},
{'w':'之','q':'子之不知鱼之乐','a':'用于主谓之间，取消句子独立性'},
{'w':'之','q':'我知之濠上也','a':'代词，指鱼之乐'},
{'w':'从容','q':'鲦鱼出游从容','a':'悠闲自得的样子'},
{'w':'子','q':'子非鱼','a':'你，对对方的尊称'},
{'w':'非','q':'子非鱼','a':'不是'},
]

# 读取CSS和JS模板
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
              <div class="tags"><span>濠梁之辩</span><span>对话体</span></div>
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
<meta name="description" content="《庄子》之《庄子与惠子游于濠梁》教学课件：逐句注释译文赏析、文言积累、人物赏析、全屏听写练习。">
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
  <div class="sec-sub">全文六句，对话合并为完整一句。每句含注释（生僻字附读音）、译文与赏析，点击可展开。</div>
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
  <div class="sec-head"><h2>赏 析</h2><span class="no">形象 · 艺术 · 名句 · 主题</span></div>

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
  <div>庄子 · 先秦（约前369—前286）· 名周，道家代表，《庄子》二则之二</div>
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
