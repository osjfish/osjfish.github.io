# -*- coding: utf-8 -*-
"""生成《应有格物致知精神》丁肇中 课件（议论文式演讲词）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\yingyougewuzhizhijingshen-dingzhaozhong.html"
FS_KEY = "gewuzhizhi_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
style += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:14px 0 6px;color:var(--ink);font-size:calc(16px * var(--fs));}'
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

LQ = "\u201c"
RQ = "\u201d"

paragraphs = [
    (
        f"我非常荣幸地接受《瞭望》周刊授予我的{LQ}情系中华{RQ}征文特别荣誉奖。我父亲是受中国传统教育长大的，我受的教育的一部分是传统教育，一部分是西方教育。缅怀我的父亲，我写了《怀念》这篇文章。多年来，我在学校里接触到不少中国学生，因此，我想借这个机会向大家谈谈学习自然科学的中国学生应该怎样了解自然科学。",
        "从获奖谈起，交代演讲缘由，提出全文论题：学习自然科学的中国学生应该怎样了解自然科学。",
        "演讲手法：以个人经历切入，亲切自然。交代中西教育背景，为下文对比传统教育与西方教育埋下伏笔。结尾提出论题，明确演讲中心，体现议论文式演讲提出问题的思路。",
        [
            ("瞭望", "这里指《瞭望》周刊，中国的新闻周刊"),
            ("情系中华", "情感牵挂着中国，表达对祖国的深情"),
            ("缅怀", "追念、怀念（已往的人或事）"),
            ("自然科学", "研究自然界物质形态、结构、性质和运动规律的科学"),
        ],
    ),
    (
        f"在中国传统教育里，最重要的书是{LQ}四书{RQ}。{LQ}四书{RQ}之一的《大学》里这样说：一个人教育的出发点是{LQ}格物{RQ}和{LQ}致知{RQ}。就是说，从探察物体而得到知识。用这两个词语描写现代学术发展是再恰当也没有的了。现代学术的基础就是实地的探察，就是我们现在所谓的实验。",
        "引用《大学》解释格物致知的含义，指出现代学术的基础就是实地探察即实验，将传统概念与现代科学对接。",
        "演讲手法：引用论证（《大学》中的格物致知），从经典中引出话题。下定义（格物致知=从探察物体而得到知识），概念清晰。将传统概念与现代实验对接，为下文论证铺垫。",
        [
            ("四书", "儒家经典《大学》《中庸》《论语》《孟子》的合称"),
            ("格物", "推究事物的道理"),
            ("致知", "获得知识"),
            ("探察", "探听侦察，这里指实地观察研究"),
            ("实地", "在现场、在实际中"),
        ],
    ),
    (
        f"但是传统的中国教育并不重视真正的格物和致知。这可能是因为传统教育的目的并不是寻求新知识，而是适应一个固定的社会制度。《大学》本身就说，格物致知的目的，是使人能达到诚意、正心、修身、齐家、治国的田地，从而追求儒家的最高理想——平天下。因为这样，格物致知的真正意义便被埋没了。",
        "指出传统教育并不重视真正的格物致知，分析其原因是传统教育的目的在于适应社会制度而非寻求新知识，导致格物致知的真正意义被埋没。",
        "演讲手法：转折（但是）引出问题，因果论证分析传统教育不重视格物致知的原因。引用《大学》八条目（诚意、正心、修身、齐家、治国、平天下）说明传统教育的目的。逻辑清晰，层层递进。",
        [
            ("诚意", "使自己的心意真诚"),
            ("正心", "使自己的心思端正"),
            ("修身", "修养自身的品德"),
            ("齐家", "整治好家庭"),
            ("治国", "治理国家"),
            ("平天下", "使天下太平，儒家的最高政治理想"),
            ("埋没", "使显不出来，使不发挥作用"),
        ],
    ),
    (
        f"大家都知道明朝的大理论家王阳明，他的思想可以代表传统儒家对实验的态度。有一天王阳明要依照《大学》的指示，先从{LQ}格物{RQ}做起。他决定要{LQ}格{RQ}院子里的竹子。于是他搬了一条凳子坐在院子里，面对着竹子硬想了七天，结果因为头痛而宣告失败。这位先生明明是把探察外界误认为探讨自己。",
        "以王阳明格竹子为例，说明传统儒家把格物理解为内心探讨而非实地探察，结果必然失败。",
        "演讲手法：举例论证（王阳明格竹子），用典型事例说明传统格物的错误。细节描写（搬凳子、硬想七天、头痛失败）生动具体，增强说服力。对比（探察外界 vs 探讨自己）点明错误实质。语言幽默，暗含讽刺。",
        [
            ("王阳明", "（1472—1529）明代哲学家、教育家，心学集大成者"),
            ("依照", "按照、依从"),
            ("硬想", "费力地、不切实际地空想"),
            ("宣告失败", "公开表明失败"),
            ("探察外界", "观察研究外部客观事物"),
            ("探讨自己", "反省探究内心世界"),
        ],
    ),
    (
        f"王阳明的观点，在当时的社会环境里是可以理解的。因为儒家传统的看法认为天下有不变的真理，而真理是{LQ}圣人{RQ}从内心领悟的。圣人知道真理以后，就传给一般人。所以经书上的道理是可{LQ}推之于四海，传之于万世{RQ}的。经验告诉我们，这种观点是不适用于现在的世界的。",
        "分析王阳明观点产生的社会根源——儒家认为真理由圣人内心领悟并传之后世，指出这种观点已不适用于现代世界。",
        "演讲手法：因果论证分析王阳明观点的历史根源。引用（推之于四海，传之于万世）说明儒家真理观。辩证看待（在当时可以理解，但不适用于现在），体现客观理性的态度。",
        [
            ("领悟", "领会、理解"),
            ("推之于四海，传之于万世", "推广到天下，流传到后世，形容真理放之四海而皆准"),
            ("经书", "儒家经典著作"),
        ],
    ),
    (
        "我是研究科学的人，所以重视实验精神在科学上的重要性。",
        "过渡段，由对传统教育的批判转入对实验精神的正面论述。",
        "演讲手法：独句成段，承上启下。以研究者身份强调实验精神的重要性，增强权威性。简短有力，标志论证方向的转换。",
        [],
    ),
    (
        "科学发展的历史告诉我们，新的知识只能通过实地实验而得到，不是由自我检讨或哲理的清谈就可求到的。",
        "提出核心观点：新知识只能通过实地实验得到，不能靠自我检讨或哲理清谈。",
        "演讲手法：道理论证，从科学发展史的角度提出论点。对比（实地实验 vs 自我检讨/哲理清谈），旗帜鲜明。判断句斩钉截铁，体现科学家的理性精神。",
        [
            ("自我检讨", "反省自己的言行思想"),
            ("清谈", "不切实际的谈论"),
        ],
    ),
    (
        "实验的过程不是消极的观察，而是积极的探测。比如，我们要知道竹子的性质，就要特地栽种竹子，以研究它生长的过程，要把叶子切下来拿到显微镜下去观察，绝不是袖手旁观就可以得到知识的。",
        "阐述实验的第一个特点：不是消极观察而是积极探测，以研究竹子为例具体说明。",
        "演讲手法：对比论证（消极观察 vs 积极探测）。举例论证（研究竹子的性质），与前文王阳明格竹子形成鲜明对照，前后呼应。列举具体实验步骤（栽种、研究生长、切叶子显微镜观察），使抽象道理具体化。",
        [
            ("消极", "不求进取的，跟积极相对"),
            ("探测", "对不能直接观察的事物或现象用仪器进行考察和测量"),
            ("特地", "专门、特意"),
            ("显微镜", "观察微小物体的光学仪器"),
            ("袖手旁观", "比喻置身事外或不协助别人"),
        ],
    ),
    (
        "实验不是毫无选择的测量，它需要有细致具体的计划。特别重要的，是要有一个适当的目标，以作为整个探索过程的向导。至于这目标怎样选定，就要靠实验者的判断力和灵感。一个成功的实验需要的是眼光、勇气和毅力。",
        "阐述实验的第二个特点：需要细致具体的计划和适当的目标，成功的实验需要眼光、勇气和毅力。",
        "演讲手法：道理论证，层层深入（计划→目标→判断力和灵感→眼光勇气毅力）。否定句式（不是毫无选择的测量）先破后立。排比收尾（眼光、勇气和毅力），简洁有力。",
        [
            ("细致", "精细周密"),
            ("向导", "带路的人，这里指引导方向的东西"),
            ("判断力", "分析决断的能力"),
            ("灵感", "在文学、艺术、科学等活动中突然产生的富有创造性的思路"),
            ("毅力", "坚强持久的意志"),
        ],
    ),
    (
        "由此我们可以了解，为什么基本知识上的突破是不常有的事情。我们也可以了解，为什么历史上学术的进展只靠少数人关键性的发现。",
        "由实验的要求推知：知识突破和学术进展之所以稀少，正是因为成功的实验需要眼光、勇气和毅力。",
        "演讲手法：因果论证（由此我们可以了解），由实验的困难推知学术突破的稀少。两个并列的{LQ}我们也可以了解{RQ}形成反复，强化结论。承上启下，从实验的一般论述转向对中国学生现状的分析。",
        [
            ("突破", "打破困难、限制等，取得新进展"),
            ("关键性", "对事物发展起决定作用的"),
        ],
    ),
    (
        f"时至今天，王阳明的思想还在继续地支配着一些中国读书人的头脑。因为这个文化背景，中国学生大部偏向于理论而轻视实验，偏向于抽象的思维而不愿动手。中国学生往往念功课成绩很好，考试都得近100分，但是在研究工作中需要拿主意时，就常常不知所措了。",
        "指出王阳明思想至今仍影响中国学生，导致他们偏重理论轻视实验、高分低能，在实际研究中不知所措。",
        "演讲手法：因果论证（因为这个文化背景）分析中国学生问题的根源。对比（成绩很好 vs 不知所措）揭示高分低能的现实。反复（偏向于……偏向于……）强化问题。客观指出问题，语重心长。",
        [
            ("支配", "对人或事物起引导和控制的作用"),
            ("偏向", "倾向于、偏重某一方面"),
            ("抽象", "不能具体经验到的，笼统的"),
            ("不知所措", "不知道怎么办才好，形容受窘或发急"),
        ],
    ),
    (
        f"在这方面，我有个人的经验为证。我是受传统教育长大的。到美国大学念物理的时候，起先以为只要很{LQ}用功{RQ}，什么都遵照老师的指导，就可以一帆风顺了，但是事实并不是这样。一开始做研究便马上发现不能光靠教师，需要自己做主张、出主意。当时因为事先没有准备，不知吃了多少苦。最使我彷徨恐慌的，是当时的唯一办法——以埋头读书应付一切，对于实际的需要毫无帮助。",
        "以个人留学经历为例，证明传统教育的弊端：埋头读书应付一切对实际需要毫无帮助，做研究需要自己拿主意。",
        "演讲手法：举例论证（个人经验），现身说法更有说服力。对比（以为可以一帆风顺 vs 事实并不是这样）。心理描写（彷徨恐慌）真实感人。破折号解释唯一办法的无效，点明传统教育的根本问题。",
        [
            ("一帆风顺", "船挂满帆顺风行驶，比喻非常顺利，没有阻碍"),
            ("做主张", "出主意、做决定"),
            ("彷徨", "（páng huáng）走来走去，犹豫不决，不知往哪个方向去"),
            ("恐慌", "因担忧害怕而慌张"),
            ("埋头读书", "专心致志地读书"),
        ],
    ),
    (
        f"我觉得真正的格物致知精神，不但研究学术不可缺少，而且对应付今天的世界环境也是不可少的。我们需要培养实验的精神。就是说，不论是研究自然科学，研究人文科学，还是在个人行动上，我们都要保留一个怀疑求真的态度，要靠实践来发现事物的真相。现在世界和社会的环境变化得很快。世界上不同文化的交流也越来越密切。我们不能盲目地接受过去认定的真理，也不能等待{LQ}学术权威{RQ}的指示。我们要自己有判断力。在环境激变的今天，我们应该重新体会几千年前经书里说的格物致知真正的意义。这意义有两个方面：第一，寻求真理的唯一途径是对事物客观的探索；第二，探索应该有想象力、有计划，不能消极地袖手旁观。希望我们这一代对于格物和致知有新的认识和思考，使得实验精神真正变成中国文化的一部分。",
        "总结全文，强调格物致知精神在研究学术和应付世界环境中的重要性，重新阐释格物致知的真正意义，发出号召使实验精神成为中国文化的一部分。",
        "演讲手法：递进复句（不但……而且……）扩展格物致知的适用范围。排比（研究自然科学，研究人文科学，还是在个人行动上）。分两点阐述格物致知的真正意义，条理清晰。结尾发出号召，呼应开头，结构完整。",
        [
            ("人文科学", "研究社会现象和文化艺术的科学，如文学、历史、哲学等"),
            ("怀疑求真", "抱着怀疑的态度去寻求真理"),
            ("盲目", "眼睛看不见东西，比喻认识不清、没有主见"),
            ("学术权威", "在学术上最有地位和影响力的人或学说"),
            ("激变", "剧烈变化"),
            ("唯一途径", "唯一的道路、方法"),
            ("客观", "按照事物的本来面目去考察，不加个人偏见"),
        ],
    ),
]

parts = [
    ("第一部分", "提出论题，解释概念", "1–2 段", "从获奖谈起提出论题，引用《大学》解释格物致知的含义，指出现代学术的基础是实验。"),
    ("第二部分", "批判传统教育", "3–5 段", "指出传统教育不重视真正的格物致知，以王阳明格竹子为例说明传统格物的错误，分析其历史根源。"),
    ("第三部分", "论述实验精神", "6–10 段", "正面论述实验精神在科学上的重要性，阐述实验的两个特点（积极探测、有计划有目标），推知学术突破的稀少。"),
    ("第四部分", "针砭现实，发出号召", "11–13 段", "指出中国学生偏重理论轻视实验的现状，以个人经历为证，重新阐释格物致知的真正意义，号召培养实验精神。"),
]

para_part = [0,0, 1,1,1, 2,2,2,2,2, 3,3,3]

fulltext_paras = [p[0] for p in paragraphs]

def annotate(text, annos):
    items = sorted(annos, key=lambda x: len(x[0]), reverse=True)
    result = text
    used = set()
    for word, note in items:
        if word in used:
            continue
        idx = result.find(word)
        if idx != -1:
            before = result[:idx]
            if before.count("<span") == before.count("</span>"):
                span = f'<span class="anno-word" data-note="{note}">{word}</span>'
                result = result[:idx] + span + result[idx+len(word):]
                used.add(word)
    return result

verse_html = ""
current_part = -1
for i, (orig, content, method, annos) in enumerate(paragraphs):
    pi = para_part[i]
    if pi != current_part:
        current_part = pi
        pname, ptitle, prange, poverview = parts[pi]
        verse_html += f'''      <div class="part-head"><span class="p-num">{pname}</span><h3>{ptitle}</h3><span class="range">{prange}</span></div>
      <div class="part-overview">{poverview}</div>
'''
    orig_ann = annotate(orig, annos)
    verse_html += f'''      <div class="verse" id="l{i+1}" data-i="{i}">
        <div class="v-top"><span class="v-no">{i+1}</span><div class="v-line">{orig_ann}</div></div>
        <details class="v-more">
          <summary>内容 · 手法</summary>
          <div class="d-body">
            <div class="v-sec"><b class="v-label">内容概括</b>
              <div class="v-trans">{content}</div>
            </div>
            <div class="v-sec"><b class="v-label">手法分析</b>
              <div class="d-body"><p>{method}</p></div>
            </div>
          </div>
        </details>
      </div>
'''

fulltext_html = ""
for para in fulltext_paras:
    fulltext_html += f'    <div class="pl">{para}</div>\n'

dict_words = [
    {"w":"瞭","py":"liào","q":"接受《□望》周刊授予我的","tip":"「瞭」目字旁，远望；不要写成「了」或「廖」"},
    {"w":"缅","py":"miǎn","q":"□怀我的父亲","tip":"「缅」绞丝旁，遥远；不要写成「湎」（三点水）"},
    {"w":"察","py":"chá","q":"从探□物体而得到知识","tip":"「察」宝盖头，仔细看；不要写成「查」"},
    {"w":"埋","py":"mái","q":"格物致知的真正意义便被□没了","tip":"「埋」土字旁，藏；多音字，此处读mái不读mán"},
    {"w":"阳明","py":"yáng míng","q":"有一天，王□□要依照《大学》的指示，先从格物做起","tip":"「阳明」是号，「阳」左耳旁，「明」日字旁；人名固定写法"},
    {"w":"凳","py":"dèng","q":"搬了一条□子坐在院子里","tip":"「凳」几字底，坐具；不要写成「登」"},
    {"w":"悟","py":"wù","q":"真理是圣人从内心领□的","tip":"「悟」竖心旁，领会；不要写成「吾」或「误」"},
    {"w":"测","py":"cè","q":"而是积极的探□","tip":"「测」三点水，测量；不要写成「侧」（单人旁）"},
    {"w":"栽","py":"zāi","q":"就要特地□种竹子","tip":"「栽」木字旁，种植；不要写成「裁」（衣字旁）或「载」（车字旁）"},
    {"w":"袖","py":"xiù","q":"绝不是□手旁观就可以得到知识的","tip":"「袖」衣字旁，衣袖；不要写成「袖」以外的写法"},
    {"w":"韧","py":"rèn","q":"一个成功的实验需要的是眼光、勇气和□力","tip":"「韧」韦字旁，柔软而坚固；不要写成「刃」"},
    {"w":"徨","py":"huáng","q":"最使我彷□恐慌的","tip":"「徨」双人旁，徘徊；与「惶」（竖心旁）区分，「彷徨」固定写法"},
    {"w":"恐","py":"kǒng","q":"最使我彷徨□慌的","tip":"「恐」心字底，害怕；不要写成「巩」"},
    {"w":"途","py":"tú","q":"寻求真理的唯一□径是对事物客观的探索","tip":"「途」走之底，道路；不要写成「图」"},
]

dict_notes = [
    {"w":"格物致知","a":"推究事物的原理而获得知识","q":"一个人教育的出发点是格物和致知"},
    {"w":"四书","a":"《大学》《中庸》《论语》《孟子》的合称","q":"最重要的书是四书"},
    {"w":"诚意","a":"使自己的心意真诚","q":"使人能达到诚意、正心、修身"},
    {"w":"正心","a":"使自己的心思端正","q":"使人能达到诚意、正心、修身"},
    {"w":"修身","a":"修养自身的品德","q":"使人能达到诚意、正心、修身"},
    {"w":"齐家","a":"整治好家庭","q":"齐家、治国的田地"},
    {"w":"平天下","a":"使天下太平，儒家最高政治理想","q":"追求儒家的最高理想——平天下"},
    {"w":"王阳明","a":"明代哲学家、教育家，心学集大成者","q":"明朝的大理论家王阳明"},
    {"w":"清谈","a":"不切实际的谈论","q":"不是由自我检讨或哲理的清谈就可求到的"},
    {"w":"袖手旁观","a":"比喻置身事外或不协助别人","q":"绝不是袖手旁观就可以得到知识的"},
    {"w":"不知所措","a":"不知道怎么办才好，形容受窘或发急","q":"就常常不知所措了"},
    {"w":"一帆风顺","a":"比喻非常顺利，没有阻碍","q":"就可以一帆风顺了"},
    {"w":"彷徨","a":"走来走去，犹豫不决","q":"最使我彷徨恐慌的"},
    {"w":"人文科学","a":"研究社会现象和文化艺术的科学","q":"研究人文科学"},
    {"w":"怀疑求真","a":"抱着怀疑的态度去寻求真理","q":"保留一个怀疑求真的态度"},
    {"w":"激变","a":"剧烈变化","q":"在环境激变的今天"},
    {"w":"唯一途径","a":"唯一的道路、方法","q":"寻求真理的唯一途径"},
    {"w":"客观","a":"按照事物本来面目考察，不加个人偏见","q":"对事物客观的探索"},
    {"w":"缅怀","a":"追念、怀念","q":"缅怀我的父亲"},
    {"w":"埋没","a":"使显不出来，使不发挥作用","q":"格物致知的真正意义便被埋没了"},
    {"w":"探测","a":"用仪器考察测量","q":"而是积极的探测"},
    {"w":"毅力","a":"坚强持久的意志","q":"需要的是眼光、勇气和毅力"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《应有格物致知精神》丁肇中</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 丁肇中</div>
  <h1 class="hero-title">应有格物致知精神</h1>
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
    <p>《应有格物致知精神》是美籍华裔物理学家丁肇中于1991年10月18日在北京人民大会堂举行的{LQ}情系中华{RQ}征文颁奖大会上发表的演讲。作者从中国传统教育中的{LQ}格物致知{RQ}概念切入，结合现代科学精神，深刻指出中国学生偏重理论、轻视实验的弊端，呼吁培养真正的格物致知精神即实验精神。</p>
    <p>这是一篇议论文式的演讲词，观点鲜明，论证严密。作者综合运用引用论证、举例论证、道理论证、对比论证等方法，层层深入地阐明了格物致知精神的真正意义及其在当代的重要价值。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>丁肇中（zhào）（1936— ），美籍华裔物理学家，祖籍山东日照。1962年获密歇根大学物理学博士学位，现任麻省理工学院教授。1974年领导研究小组发现J粒子，1976年获诺贝尔物理学奖。他领导的阿尔法磁谱仪实验旨在探索宇宙中的反物质和暗物质。</p>
    <p style="margin-top:10px;color:var(--ink2)">丁肇中始终关注中国科技发展，多次来华讲学，培养中国科研人才。他在诺贝尔奖颁奖仪式上坚持用中文演讲，表达对祖国的深情。</p>
  </div>
  <div class="box">
    <h3>演讲背景</h3>
    <p><b>演讲场合：</b>1991年10月18日，北京人民大会堂，《瞭望》周刊{LQ}情系中华{RQ}征文特别荣誉奖颁奖大会。丁肇中因《怀念》一文获奖，在颁奖会上发表了这篇演讲。</p>
    <p style="margin-top:8px"><b>现实针对性：</b>作者多年接触中国学生，发现他们{LQ}偏向于理论而轻视实验{RQ}，考试成绩好但实际研究能力弱。这篇演讲正是针对这一现实问题，呼吁重视实验精神。</p>
    <p style="margin-top:8px"><b>格物致知的渊源：</b>{LQ}格物致知{RQ}出自《礼记·大学》，是儒家八条目（格物、致知、诚意、正心、修身、齐家、治国、平天下）的基础。作者赋予这一传统概念以现代科学的内涵。</p>
  </div>
  <div class="box">
    <h3>文体知识</h3>
    <p><b>议论文式演讲：</b>以议论为主要表达方式的演讲，具备议论文的三要素——论点、论据、论证。特点是观点鲜明、论据充分、论证严密，同时具有演讲的感染力和号召力。</p>
    <p style="margin-top:8px"><b>论证方法：</b>常见的有举例论证、道理论证、对比论证、引用论证、比喻论证等。本文综合运用了多种论证方法，是学习议论文写作的典范。</p>
    <p style="margin-top:8px"><b>演讲的思路：</b>提出问题（中国学生应该怎样了解自然科学）→ 分析问题（传统教育的弊端、实验精神的重要性、中国学生的现状）→ 解决问题（培养格物致知精神）。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文诵读《应有格物致知精神》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1FE411g7iZ&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读应有格物致知精神"></iframe>
        <a href="https://www.bilibili.com/video/BV1FE411g7iZ" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>丁肇中：获诺奖后坚持用中文演讲</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1W84y1z7pA&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="丁肇中中文演讲"></iframe>
        <a href="https://www.bilibili.com/video/BV1W84y1z7pA" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 内容 · 论证思路</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{fulltext_html}  </div>
  <div class="verse-list" id="verseList">
{verse_html}  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">论证思路 · 方法 · 语言 · 主题</span></div>

  <div class="box">
    <h3>论证思路</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">提出问题：中国学生应怎样了解自然科学</div>
        <p>文章从获奖谈起，自然引出论题。然后引用《大学》解释格物致知的含义，将传统概念与现代实验对接，为下文论证奠定基础。论题明确，切入点巧妙。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">分析问题：传统教育的弊端与实验精神的重要</div>
        <p>先指出传统教育不重视真正的格物致知，以王阳明格竹子为例说明传统格物的错误；再正面论述实验精神的重要性，阐述实验的两个特点；最后指出中国学生偏重理论轻视实验的现状，以个人经历为证。反面批判与正面论证结合，层层深入。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">解决问题：培养格物致知精神</div>
        <p>结尾强调格物致知精神在研究学术和应付世界环境中的重要性，重新阐释格物致知的真正意义（客观探索、有想象力有计划），发出号召使实验精神成为中国文化的一部分。结构完整，首尾呼应。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>论证方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">举例论证：典型事例，说服力强</div>
        <p>王阳明格竹子（说明传统格物的错误）、研究竹子的性质（说明实验是积极探测）、个人留学经历（证明传统教育的弊端）。三个例子各有侧重，从历史到科学到个人，全面支撑论点。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">道理论证：逻辑严密，层层深入</div>
        <p>从科学发展史的角度提出{LQ}新知识只能通过实地实验得到{RQ}；由实验的要求推知学术突破的稀少；由文化背景分析中国学生的问题。道理论证使文章具有理论深度。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比论证：正误分明，观点突出</div>
        <p>传统教育（重理论轻实验）与现代科学（重实验）对比；王阳明格竹子（空想）与科学研究竹子（实地实验）对比；中国学生考试成绩好与研究能力弱对比。对比使正误分明，论点突出。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">引用论证：经典支撑，文化底蕴</div>
        <p>引用《大学》中的格物致知、诚意正心修身齐家治国平天下；引用{LQ}推之于四海，传之于万世{RQ}说明儒家真理观。引用经典既增添了文化底蕴，又为批判传统教育提供了依据。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>语言艺术</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">准确严密，逻辑性强</div>
        <p>{LQ}可能是因为{RQ}{LQ}大都偏向于{RQ}{LQ}往往{RQ}等修饰词，准确反映客观实际，体现了科学家严谨的语言风格。判断句斩钉截铁（新知识只能通过实地实验而得到），不容置疑。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">通俗生动，如话家常</div>
        <p>作为演讲词，语言通俗易懂。{LQ}硬想了七天{RQ}{LQ}搬了一条凳子{RQ}{LQ}吃了多少苦{RQ}等口语化表达，使抽象的道理变得生动亲切。王阳明格竹子的故事更是如话家常，引人入胜。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">情感真挚，语重心长</div>
        <p>作者对中国学生的问题不是简单批评，而是{LQ}彷徨恐慌{RQ}的切身之痛和殷切期望。结尾{LQ}希望我们这一代……使得实验精神真正变成中国文化的一部分{RQ}，语重心长，感人至深。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《应有格物致知精神》由古代文化典籍引出观点，以王阳明和作者自身的实例为论据，论证了格物致知精神的真正意义，揭露了传统教育的弊病，阐明了实验精神在科学研究和应对世界环境中的重要性，呼吁中国学生培养真正的格物致知精神，使实验精神成为中国文化的一部分。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 字音形 · 修辞 · 写法 · 常识</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">格物致知</span><span class="acc-d">推究事物的原理而获得知识。格，推究；致，获得。</span></div>
      <div class="acc-item"><span class="acc-w">缅怀</span><span class="acc-d">（miǎn）追念、怀念（已往的人或事）。</span></div>
      <div class="acc-item"><span class="acc-w">探察</span><span class="acc-d">探听侦察，文中指实地观察研究。</span></div>
      <div class="acc-item"><span class="acc-w">埋没</span><span class="acc-d">（mái）使显不出来，使不发挥作用。</span></div>
      <div class="acc-item"><span class="acc-w">清谈</span><span class="acc-d">不切实际的谈论。</span></div>
      <div class="acc-item"><span class="acc-w">袖手旁观</span><span class="acc-d">比喻置身事外或不协助别人。</span></div>
      <div class="acc-item"><span class="acc-w">不知所措</span><span class="acc-d">不知道怎么办才好，形容受窘或发急。措，安置、处理。</span></div>
      <div class="acc-item"><span class="acc-w">一帆风顺</span><span class="acc-d">比喻非常顺利，没有阻碍。</span></div>
      <div class="acc-item"><span class="acc-w">彷徨</span><span class="acc-d">（páng huáng）走来走去，犹豫不决，不知往哪个方向去。</span></div>
      <div class="acc-item"><span class="acc-w">激变</span><span class="acc-d">剧烈变化。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">瞭望</span><span class="acc-d">（liào）目字旁；与「撩」（liāo，提手旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">缅怀</span><span class="acc-d">（miǎn）绞丝旁；与「湎」（miǎn，三点水，沉湎）区分。</span></div>
      <div class="acc-item"><span class="acc-w">埋没</span><span class="acc-d">（mái）土字旁；多音字，此处读mái，不读mán（埋怨）。</span></div>
      <div class="acc-item"><span class="acc-w">栽种</span><span class="acc-d">（zāi）木字旁；与「裁」（cái，衣字旁）、「载」（zài，车字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">彷徨</span><span class="acc-d">（páng huáng）均为双人旁；「徨」与「惶」（huáng，竖心旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">探测</span><span class="acc-d">（cè）三点水；与「侧」（cè，单人旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">毅力</span><span class="acc-d">（yì）韦字旁；与「刃」（rèn）区分。</span></div>
      <div class="acc-item"><span class="acc-w">丁肇中</span><span class="acc-d">（zhào）「肇」户字头，开始、发生；人名用字，不要读成zú。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞方法</h3>
      <div class="acc-item"><span class="acc-w">引用</span><span class="acc-d">引用《大学》中的格物致知、八条目等，既增添文化底蕴，又为论证提供依据。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">传统教育与现代科学对比、王阳明格竹与科学实验对比、高分与低能对比，使观点鲜明突出。</span></div>
      <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">{LQ}研究自然科学，研究人文科学，还是在个人行动上{RQ}，扩展格物致知的适用范围。</span></div>
      <div class="acc-item"><span class="acc-w">设问</span><span class="acc-d">文章以{LQ}中国学生应该怎样了解自然科学{RQ}的问题引领全文，引发思考。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">提出—分析—解决</span><span class="acc-d">典型的议论文结构：提出问题→分析问题→解决问题，条理清晰，逻辑严密。</span></div>
      <div class="acc-item"><span class="acc-w">正反结合</span><span class="acc-d">反面批判传统教育的弊端，正面论述实验精神的重要，正反对比使论证更有力。</span></div>
      <div class="acc-item"><span class="acc-w">事例典型</span><span class="acc-d">王阳明格竹、科学研究竹子、个人留学经历，三个事例各有侧重，典型且有说服力。</span></div>
      <div class="acc-item"><span class="acc-w">语言准确</span><span class="acc-d">大量使用修饰限制词（可能、大都、往往），体现议论文语言的准确性和严密性。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">四书</span><span class="acc-d">《大学》《中庸》《论语》《孟子》的合称，儒家经典。南宋朱熹编注。</span></div>
      <div class="acc-item"><span class="acc-w">八条目</span><span class="acc-d">《大学》提出的个人修养到治国的八个步骤：格物、致知、诚意、正心、修身、齐家、治国、平天下。</span></div>
      <div class="acc-item"><span class="acc-w">王阳明</span><span class="acc-d">（1472—1529）名守仁，字伯安，号阳明，明代哲学家、教育家，心学集大成者，提出{LQ}致良知{RQ}{LQ}知行合一{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">J粒子</span><span class="acc-d">1974年丁肇中领导的小组发现的新粒子，因丁肇中姓丁（拼音Ding），以类似的英文字母J命名。</span></div>
      <div class="acc-item"><span class="acc-w">诺贝尔物理学奖</span><span class="acc-d">根据诺贝尔遗嘱设立的物理学奖项，每年颁发。丁肇中1976年与里克特同获此奖。</span></div>
    </div>
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
  <div class="kai">《应有格物致知精神》</div>
  <div>丁肇中 · 现代 · 1991年北京人民大会堂演讲</div>
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
<script>
{main_js}
</script>
<script>
var DICT_WORDS = {json.dumps(dict_words, ensure_ascii=False)};
var DICT_NOTES = {json.dumps(dict_notes, ensure_ascii=False)};
</script>

</body>
</html>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Generated: {OUT}")
print(f"Paragraphs: {len(paragraphs)}")
print(f"Anno count: {sum(len(p[3]) for p in paragraphs)}")
print(f"Words: {len(dict_words)}, Notes: {len(dict_notes)}")
