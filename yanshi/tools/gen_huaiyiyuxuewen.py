# -*- coding: utf-8 -*-
"""生成《怀疑与学问》顾颉刚 课件"""
import re, json

OUT = r"D:\App\Apps\yanshi\huaiyiyuxuewen-gujiegang.html"
TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"

# 读取模板
with open(TEMPLATE, 'r', encoding='utf-8') as f:
    tpl = f.read()

# 提取 style 块
style_m = re.search(r'<style>(.*?)</style>', tpl, re.DOTALL)
CSS = style_m.group(1)
# 补充 acc-sub 样式
CSS += '\n  .acc-sub{font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:14px 0 6px;font-size:calc(16px*var(--fs));color:var(--teal-deep)}\n'

# 提取第一个 script 块 (IIFE)
script_m = re.search(r'(<script>\s*\(function\(\)\{.*?</script>)', tpl, re.DOTALL)
JS_IIFE = script_m.group(1)
# 替换 localStorage key
JS_IIFE = JS_IIFE.replace('beiying_fs', 'huaiyi_fs')

# ============ 课文数据 ============
# 每段: (原文, 内容概括, 手法分析, [(词,注释),...])
PARAS = [
    (
        '\u201c学者先要会疑。\u201d\u2014\u2014程颐',
        '引用程颐名言，开门见山提出\u201c学则须疑\u201d的中心论点。',
        '道理论证（引用论证）：以北宋理学家程颐的名言开篇，既点明题旨，又增强权威性。独立成段，醒目有力。',
        [('学者', '做学问的人'), ('先要', '首先必须'), ('会疑', '善于质疑、提出疑问')]
    ),
    (
        '\u201c在可疑而不疑者，不曾学；学则须疑。\u201d\u2014\u2014张载',
        '再引张载名言，进一步强调怀疑是治学的必要条件。',
        '引用论证：张载与程颐同为北宋理学大家，两人名言互相印证，使论点更具说服力。两句引文构成排比式的开篇，气势充沛。',
        [('可疑', '值得怀疑的地方'), ('不曾学', '等于没有学习'), ('学则须疑', '学习就必须要有怀疑精神')]
    ),
    (
        '学问的基础是事实和证据。事实和证据的来源有两种：一种是自己亲眼看见的，一种是听别人传说的。譬如在国难危急的时候，各地一定有许多口头的消息，说得如何凶险，那便是别人的传说，不一定可靠；要知道实际的情形，只有靠自己亲身视察。做学问也是这样，最要紧最可靠的材料是自己亲见的事实根据；但这种证据有时候不能亲自看到，便只能靠别人的传说了。',
        '指出学问的基础是事实和证据，而证据来源有亲见和传说两种，引出下文对传说应持怀疑态度的论述。',
        '举例论证：以\u201c国难危急时口头消息不可靠\u201d为例，说明传说未必可信，论证严密。逻辑层次清晰：先下定义，再分类，再举例，最后得出结论。',
        [
            ('事实和证据', '真实的情况和证明事实的依据'),
            ('亲眼看见', '亲身观察、目睹'),
            ('听别人传说', '从他人口中听到的传闻'),
            ('国难危急', '国家危难、形势紧迫'),
            ('口头的消息', '口耳相传的信息'),
            ('凶险', '（情势）危险可怕'),
            ('亲身视察', '亲自到现场察看'),
            ('事实根据', '作为依据的真实事实'),
        ]
    ),
    (
        '我们对于传说的话，不论信不信，都应当经过一番思考，不应当随随便便就信了。我们信它，因为它\u201c是\u201d；不信它，因为它\u201c非\u201d。这一番事前的思索，不随便轻信的态度，便是怀疑的精神，也是做一切学问的基本条件。我们听说古代有三皇、五帝，便要问问：这是谁说的话？最先见于何书？所见的书是何时何人著的？著者何以知道？我们又听说\u201c腐草为萤\u201d，也要问问：死了的植物如何会变成飞动的甲虫？有什么科学根据？我们若能这样追问，一切虚妄的学说便不攻自破了。',
        '提出对传说应持怀疑态度，以\u201c三皇五帝\u201d和\u201c腐草为萤\u201d为例，说明追问能使虚妄学说不攻自破。',
        '举例论证：连用两个事例（三皇五帝、腐草为萤），每个事例都以连续追问的方式展开，具体展示怀疑精神的运用。排比问句增强语势。\u201c不攻自破\u201d点明怀疑的威力。',
        [
            ('不论信不信', '不管是相信还是不相信'),
            ('一番思考', '一番深入的思索'),
            ('随随便便', '轻率、不认真'),
            ('事前的思索', '在相信之前进行的思考'),
            ('轻信', '轻易相信'),
            ('怀疑的精神', '不轻信、善于追问的治学态度'),
            ('基本条件', '根本的、必不可少的前提'),
            ('三皇、五帝', '传说中远古时代的帝王'),
            ('最先见于何书', '最早在哪本书中记载'),
            ('著者何以知道', '作者凭什么知道这些事'),
            ('腐草为萤', '古人认为萤火虫是由腐烂的草变成的，一种不科学的说法'),
            ('虚妄的学说', '没有事实根据的荒谬学说'),
            ('不攻自破', '不用攻击，自己就破灭了'),
        ]
    ),
    (
        '我们对于不论哪一本书，哪一种学问，都要经过自己的怀疑：因怀疑而思索，因思索而辨别是非；经过\u201c怀疑\u201d\u201c思索\u201d\u201c辨别\u201d三步以后，那本书才是自己的书，那种学问才是自己的学问。否则便是盲从，便是迷信。孟子所谓\u201c尽信书则不如无书\u201d，也就是教我们有一点怀疑的精神，不要随便盲从或迷信。',
        '从对传说的怀疑扩展到对书本和学问的怀疑，提出\u201c怀疑\u2192思索\u2192辨别\u201d三步法，并引孟子名言佐证。',
        '道理论证与引用论证相结合：先阐述怀疑\u2014思索\u2014辨别的递进逻辑，再以孟子\u201c尽信书则不如无书\u201d的名言作结，古今印证。\u201c自己的书\u201d\u201c自己的学问\u201d强调经过怀疑消化后的知识才真正属于自己。',
        [
            ('辨别是非', '分辨正确与错误'),
            ('盲从', '不问是非地附和别人，盲目跟从'),
            ('迷信', '盲目地信仰崇拜，不辨真伪'),
            ('尽信书则不如无书', '完全相信书本还不如没有书本，强调读书要有怀疑精神'),
        ]
    ),
    (
        '怀疑不仅是消极方面辨伪去妄的必须步骤，也是积极方面建设新学说、启迪新发明的基本条件。对于别人的话，都不打折扣地承认，那是思想上的懒惰。这样的脑筋永远是被动的，永远不能治学。只有常常怀疑、常常发问的脑筋才有问题，有问题才想求解答。在不断的发问和求解中，一切学问才会发展起来。许多大学问家、大哲学家都是从怀疑中锻炼出来的。清代的一位大学问家\u2014\u2014戴震，幼时读朱子的《大学章句》，便问《大学》是何时的书，朱子是何时的人。塾师告诉他《大学》是周代的书，朱子是宋代的大儒；他便问宋代的人如何能知道一千多年前的著者的意思。法国的大哲学家笛卡儿也说：\u201c我怀疑，所以我存在。\u201d他的哲学就建立在对于万事万物的怀疑和明辨上。一切学问家，不但对于流俗传说，就是对于过去学者的学说也常常要抱怀疑的态度，常常和书中的学说辩论，常常评判书中的学说，常常修正书中的学说：要这样才能有更新更善的学说产生。古今科学上新的发明，哲学上新的理论，美术上新的作风，都是这样起来的。若使后之学者都墨守前人的旧说，那就没有新问题，没有新发明，一切学术停滞，人类的文化也就不会进步了。',
        '承上启下，论述怀疑在积极方面的作用：建设新学说、启迪新发明。以戴震善疑和笛卡儿名言为例，论证怀疑推动学术进步；最后从反面指出墨守旧说的危害。',
        '承上启下的过渡句（\u201c不仅\u2026\u2026也是\u2026\u2026\u201d）使论证从消极方面转入积极方面。举例论证与道理论证结合：戴震幼时善疑的事例具体生动，笛卡儿名言增强权威性。四个\u201c常常\u201d构成排比，语势充沛。结尾从反面假设（\u201c若使\u2026\u2026那就\u2026\u2026\u201d），与正面论证形成对比，强化论点。',
        [
            ('辨伪去妄', '辨别虚假、去除荒谬'),
            ('必须步骤', '必不可少的环节'),
            ('建设新学说', '创立新的学术理论'),
            ('启迪新发明', '启发、导致新的创造发明'),
            ('不打折扣地承认', '毫无保留地全部接受'),
            ('思想上的懒惰', '不愿动脑思考的惰性'),
            ('被动', '受外力推动而行动，不能主动'),
            ('治学', '研究学问'),
            ('戴震', '清代著名思想家、学者，皖派经学创始人'),
            ('朱子', '朱熹，南宋理学家'),
            ('《大学章句》', '朱熹对《大学》的注释著作'),
            ('塾师', '私塾里的老师'),
            ('周代', '中国古代朝代名，约公元前1046年\u2014前256年'),
            ('大儒', '学识渊博的儒者'),
            ('笛卡儿', '法国哲学家、数学家，解析几何创始人'),
            ('我怀疑，所以我存在', '笛卡儿哲学的核心命题，意为通过怀疑一切而确证自我的存在'),
            ('万事万物', '宇宙间一切事物'),
            ('明辨', '清楚地辨别'),
            ('流俗传说', '社会上流行的世俗传闻'),
            ('辩论', '彼此用一定的理由来说明自己对事物的见解，揭露对方的矛盾'),
            ('评判', '判定是非、优劣'),
            ('修正', '修改使正确'),
            ('更新更善', '更新颖、更完善'),
            ('作风', '这里指艺术创作的风格、风气'),
            ('墨守前人的旧说', '固守前人的旧学说，不肯改变。墨守，源于战国时墨子善于守城，后指固执保守'),
            ('学术停滞', '学术停止发展，不再前进'),
        ]
    ),
]

# ============ 注释标注函数 ============
def annotate(text, notes):
    """按词表标注注释，长词优先"""
    # 按词长降序
    sorted_notes = sorted(notes, key=lambda x: len(x[0]), reverse=True)
    result = text
    used = set()
    for word, note in sorted_notes:
        if word in used:
            continue
        # 检查是否已被包含在更长的注释中
        # 简单替换第一个出现
        idx = result.find(word)
        if idx >= 0:
            # 检查是否在已有 span 内
            before = result[:idx]
            if before.count('<span class="anno-word"') > before.count('</span>'):
                continue
            escaped_note = note.replace('"', '&quot;')
            replacement = f'<span class="anno-word" data-note="{escaped_note}">{word}</span>'
            result = result[:idx] + replacement + result[idx+len(word):]
            used.add(word)
    return result

# ============ 生成 fulltext ============
fulltext_lines = []
for orig, _, _, _ in PARAS:
    fulltext_lines.append(f'    <div class="pl">{orig}</div>')
FULLTEXT = '\n'.join(fulltext_lines)

# ============ 生成 verse cards ============
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
    {"w":"颐","py":"yí","q":"\u201c学者先要会疑。\u201d\u2014\u2014程□","tip":"\u300c颐\u300d页字旁，面颊；与\u300c臣\u300d（chén，君主时代的官吏）区分"},
    {"w":"载","py":"zài","q":"\u201c在可疑而不疑者，不曾学；学则须疑。\u201d\u2014\u2014张□","tip":"\u300c载\u300d车字旁，又、且；多音字，zǎi（记载）/ zài（载重）"},
    {"w":"譬","py":"pì","q":"□如在国难危急的时候，各地一定有许多口头的消息","tip":"\u300c譬\u300d言字旁，比喻；不要写成\u300c劈\u300d（刀字旁）"},
    {"w":"察","py":"chá","q":"要知道实际的情形，只有靠自己亲身视□","tip":"\u300c察\u300d宝盖头，仔细看；与\u300c查\u300d（检查）区分，\u300c视察\u300d固定用\u300c察\u300d"},
    {"w":"萤","py":"yíng","q":"我们又听说\u201c腐草为□\u201d，也要问问","tip":"\u300c萤\u300d草字头，萤火虫；与\u300c莹\u300d（玉字旁，光亮）、\u300c荧\u300d（火字旁，微光）区分"},
    {"w":"妄","py":"wàng","q":"一切虚□的学说便不攻自破了","tip":"\u300c妄\u300d女字旁，荒谬、不实；不要写成\u300c忘\u300d（心字底，忘记）"},
    {"w":"辨","py":"biàn","q":"因怀疑而思索，因思索而□别是非","tip":"\u300c辨\u300d辛字旁中间是一点一撇，辨别；与\u300c辩\u300d（言字旁，辩论）、\u300c辫\u300d（绞丝旁，辫子）区分"},
    {"w":"盲","py":"máng","q":"否则便是从□，便是迷信","tip":"\u300c盲\u300d目字旁，眼睛看不见，引申为盲目；不要写成\u300c茫\u300d（草字头，茫然）"},
    {"w":"戴","py":"dài","q":"清代的一位大学问家\u2014\u2014□震，幼时读朱子的《大学章句》","tip":"\u300c戴\u300d戈字旁，姓氏；与\u300c带\u300d（巾字旁，带领）区分，注意上面是\u300c十\u300d+\u300c戈\u300d"},
    {"w":"塾","py":"shú","q":"□师告诉他《大学》是周代的书","tip":"\u300c塾\u300d土字底，旧时私人设立的教学地方；不要写成\u300c熟\u300d（四点底，成熟）"},
    {"w":"儒","py":"rú","q":"朱子是宋代的大□","tip":"\u300c儒\u300d单人旁，儒家、学者；不要写成\u300c孺\u300d（子字旁，孺子）"},
    {"w":"笛","py":"dí","q":"法国的大哲学家□卡儿也说","tip":"\u300c笛\u300d竹字头，笛子；人名用字，不要写成\u300c迪\u300d（走之底，启迪）"},
    {"w":"俗","py":"sú","q":"不但对于流□传说，就是对于过去学者的学说","tip":"\u300c俗\u300d单人旁，世俗、流行的；不要写成\u300c裕\u300d（衣字旁，富裕）"},
    {"w":"墨","py":"mò","q":"若使后之学者都□守前人的旧说","tip":"\u300c墨\u300d黑字头，墨守即固执保守；不要写成\u300c默\u300d（黑字旁，沉默）"},
    {"w":"滞","py":"zhì","q":"一切学术停□，人类的文化也就不会进步了","tip":"\u300c滞\u300d三点水，停滞、不流通；不要写成\u300c带\u300d或\u300c置\u300d（四字头，放置）"},
]

DICT_NOTES = [
    {"w":"学者先要会疑","a":"做学问的人首先必须善于提出疑问","q":"\u201c学者先要会疑。\u201d\u2014\u2014程颐"},
    {"w":"学则须疑","a":"学习就必须要有怀疑精神","q":"\u201c在可疑而不疑者，不曾学；学则须疑。\u201d\u2014\u2014张载"},
    {"w":"事实和证据","a":"真实的情况和证明事实的依据","q":"学问的基础是事实和证据"},
    {"w":"国难危急","a":"国家危难、形势紧迫","q":"譬如在国难危急的时候，各地一定有许多口头的消息"},
    {"w":"亲身视察","a":"亲自到现场察看","q":"要知道实际的情形，只有靠自己亲身视察"},
    {"w":"怀疑的精神","a":"不轻信、善于追问的治学态度","q":"这一番事前的思索，不随便轻信的态度，便是怀疑的精神"},
    {"w":"基本条件","a":"根本的、必不可少的前提","q":"也是做一切学问的基本条件"},
    {"w":"三皇、五帝","a":"传说中远古时代的帝王","q":"我们听说古代有三皇、五帝，便要问问"},
    {"w":"腐草为萤","a":"古人认为萤火虫是由腐烂的草变成的，一种不科学的说法","q":"我们又听说\u201c腐草为萤\u201d，也要问问"},
    {"w":"虚妄","a":"没有事实根据的、荒谬的","q":"一切虚妄的学说便不攻自破了"},
    {"w":"不攻自破","a":"不用攻击，自己就破灭了","q":"一切虚妄的学说便不攻自破了"},
    {"w":"辨别是非","a":"分辨正确与错误","q":"因怀疑而思索，因思索而辨别是非"},
    {"w":"盲从","a":"不问是非地附和别人，盲目跟从","q":"否则便是盲从，便是迷信"},
    {"w":"尽信书则不如无书","a":"完全相信书本还不如没有书本，强调读书要有怀疑精神","q":"孟子所谓\u201c尽信书则不如无书\u201d"},
    {"w":"辨伪去妄","a":"辨别虚假、去除荒谬","q":"怀疑不仅是消极方面辨伪去妄的必须步骤"},
    {"w":"不打折扣","a":"毫无保留、完全地","q":"对于别人的话，都不打折扣地承认，那是思想上的懒惰"},
    {"w":"戴震","a":"清代著名思想家、学者，皖派经学创始人","q":"清代的一位大学问家\u2014\u2014戴震"},
    {"w":"朱子","a":"朱熹，南宋理学家","q":"幼时读朱子的《大学章句》"},
    {"w":"塾师","a":"私塾里的老师","q":"塾师告诉他《大学》是周代的书"},
    {"w":"大儒","a":"学识渊博的儒者","q":"朱子是宋代的大儒"},
    {"w":"我怀疑，所以我存在","a":"笛卡儿哲学的核心命题，意为通过怀疑一切而确证自我的存在","q":"法国的大哲学家笛卡儿也说：\u201c我怀疑，所以我存在。\u201d"},
    {"w":"流俗","a":"社会上流行的风俗习惯（含贬义）","q":"不但对于流俗传说"},
    {"w":"墨守","a":"固执保守，不肯改变。源于战国时墨子善于守城","q":"若使后之学者都墨守前人的旧说"},
    {"w":"停滞","a":"停止发展，不再前进","q":"一切学术停滞，人类的文化也就不会进步了"},
]

# ============ 组装 HTML ============
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《怀疑与学问》顾颉刚</title>
<style>{CSS}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 顾颉刚</div>
  <h1 class="hero-title">怀疑与学问</h1>
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
    <p>顾颉刚是中国现代著名历史学家、民俗学家，\u201c古史辨\u201d派的创始人。他一生治学以\u201c怀疑\u201d为精神核心，认为研究历史必须对古书古史进行严格的考辨，不能盲从前人旧说。</p>
    <p>《怀疑与学问》正是这一治学精神的集中体现。文章开篇引用程颐、张载两句名言，提出\u201c学则须疑\u201d的中心论点，然后从消极方面（辨伪去妄）和积极方面（建设新学说）层层深入地论证怀疑在治学中的重要作用，是一篇典型的立论型议论文。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>顾颉刚（1893\u20141980），原名诵坤，字铭坚，江苏苏州人。现代著名历史学家、民俗学家，\u201c古史辨\u201d派的创始人。1920年毕业于北京大学哲学系，历任厦门大学、中山大学、燕京大学、北京大学等校教授。他提出\u201c层累地造成的中国古史\u201d学说，在史学界产生了深远影响。代表作有《古史辨》《秦汉的方士与儒生》《史林杂识初编》等。</p>
    <p style="margin-top:10px;color:var(--ink2)">顾颉刚的治学以怀疑和考辨著称，他认为\u201c吾们处于现在，只有应用了考古学的方法，去真实地寻出古代的事实，才可算是研究古史的正当方法\u201d。《怀疑与学问》写于20世纪30年代，是其治学经验的总结。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>治学理念：</b>顾颉刚一生倡导\u201c疑古\u201d精神，认为对古书古史必须进行严格考辨。他在北京大学读书时，受章太炎、胡适等人影响，开始用科学方法审视传统古史体系。</p>
    <p style="margin-top:8px"><b>古史辨运动：</b>1923年，顾颉刚提出\u201c层累地造成的中国古史\u201d观点，认为古史是历代不断叠加编造而成的，引发了中国史学界著名的\u201c古史辨\u201d大讨论。</p>
    <p style="margin-top:8px"><b>写作意图：</b>本文正是在这样的学术背景下写成，旨在向青年学生阐述怀疑精神在治学中的根本意义，鼓励学生不盲从、不迷信，以科学的态度对待学问。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文朗读《怀疑与学问》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1tA411Y7Cw&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读《怀疑与学问》"></iframe>
        <a href="https://www.bilibili.com/video/BV1tA411Y7Cw" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>公开课《怀疑与学问》</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1cN411B7nD&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="公开课《怀疑与学问》"></iframe>
        <a href="https://www.bilibili.com/video/BV1cN411B7nD" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
    <p>本文的中心论点是：治学必须有怀疑精神（或\u201c学则须疑\u201d）。文章开篇引用程颐\u201c学者先要会疑\u201d和张载\u201c在可疑而不疑者，不曾学；学则须疑\u201d两句名言，既引出论点，又作为道理论据，开门见山，醒人耳目。</p>
  </div>
  <div class="box">
    <h3>论证思路</h3>
    <p>全文按照\u201c提出论点\u2014\u2014论证论点\u201d的思路展开，可分为三个部分：</p>
    <p style="margin-top:8px"><b>第一部分（第1\u20142段）：</b>引用程颐、张载名言，提出\u201c学则须疑\u201d的中心论点。</p>
    <p style="margin-top:8px"><b>第二部分（第3\u20145段）：</b>论证怀疑在消极方面的作用\u2014\u2014辨伪去妄。先指出学问的基础是事实和证据，而证据有亲见和传说两种；再论证对传说必须经过思考（怀疑精神），以三皇五帝、腐草为萤为例；最后扩展到对书本和学问也要怀疑，引孟子名言佐证。</p>
    <p style="margin-top:8px"><b>第三部分（第6段）：</b>论证怀疑在积极方面的作用\u2014\u2014建设新学说、启迪新发明。以承上启下的过渡句领起，先从反面指出不怀疑就是思想懒惰，再从正面论证怀疑推动学问发展，以戴震善疑和笛卡儿名言为例，最后从反面假设墨守旧说的危害，强化论点。</p>
  </div>
  <div class="box">
    <h3>论证方法</h3>
    <div class="tw">
    <table>
      <tr><th>论证方法</th><th>文中体现</th><th>作用</th></tr>
      <tr><td>引用论证（道理论证）</td><td>开篇引程颐、张载名言；第5段引孟子\u201c尽信书则不如无书\u201d；第6段引笛卡儿\u201c我怀疑，所以我存在\u201d</td><td>以古今中外学者名言佐证论点，增强权威性和说服力</td></tr>
      <tr><td>举例论证</td><td>第4段举\u201c三皇五帝\u201d\u201c腐草为萤\u201d两例；第6段举戴震幼时善疑的事例</td><td>以具体事例展示怀疑精神的运用，使论证生动可感</td></tr>
      <tr><td>对比论证</td><td>第6段先从反面指出\u201c不打折扣地承认\u201d是思想懒惰，再从正面论证怀疑推动发展；结尾\u201c若使后之学者都墨守前人的旧说\u201d从反面假设</td><td>正反对照，使论点更加鲜明突出</td></tr>
    </table>
    </div>
  </div>
  <div class="box">
    <h3>语言特点</h3>
    <p><b>逻辑严密，层层深入：</b>文章从\u201c学问的基础是事实和证据\u201d起笔，到\u201c对传说要怀疑\u201d，再到\u201c对书本学问要怀疑\u201d，最后到\u201c怀疑能建设新学说\u201d，论证环环相扣，步步推进。</p>
    <p style="margin-top:8px"><b>排比与反复，语势充沛：</b>第4段连用四个问句追问三皇五帝的来源；第6段四个\u201c常常\u201d构成排比（\u201c常常要抱怀疑的态度，常常和书中的学说辩论，常常评判书中的学说，常常修正书中的学说\u201d），语势充沛，强调怀疑精神贯穿治学始终。</p>
    <p style="margin-top:8px"><b>过渡自然，衔接紧密：</b>第6段开头\u201c怀疑不仅是消极方面辨伪去妄的必须步骤，也是积极方面建设新学说、启迪新发明的基本条件\u201d是典型的承上启下过渡句，使文章从消极论证自然转入积极论证。</p>
  </div>
  <div class="fame">
    <div class="fame-card">
      <div class="f-line">\u201c学者先要会疑。\u201d\u2014\u2014程颐</div>
      <p>开篇引用，点明题旨。程颐是北宋理学大家，其言具有权威性，为全文奠定立论基础。</p>
    </div>
    <div class="fame-card">
      <div class="f-line">怀疑不仅是消极方面辨伪去妄的必须步骤，也是积极方面建设新学说、启迪新发明的基本条件。</div>
      <p>承上启下的关键句，用\u201c不仅\u2026\u2026也是\u2026\u2026\u201d的递进句式，将论证从消极方面推向积极方面，是全文论证的枢纽。</p>
    </div>
    <div class="fame-card">
      <div class="f-line">若使后之学者都墨守前人的旧说，那就没有新问题，没有新发明，一切学术停滞，人类的文化也就不会进步了。</div>
      <p>结尾从反面假设，以三个\u201c没有\u201d和\u201c停滞\u201d\u201c不会进步\u201d层层递进，指出墨守旧说的严重危害，与正面论证形成强烈对比，发人深省。</p>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 字音 · 修辞 · 借鉴 · 常识</span></div>

  <div class="acc-cat">
    <h3>重点词语</h3>
    <div class="acc-item"><span class="acc-w">虚妄</span><span class="acc-d">没有事实根据的、荒谬的。如\u201c一切虚妄的学说便不攻自破了\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">不攻自破</span><span class="acc-d">不用攻击，自己就破灭了。形容观点、学说等站不住脚。</span></div>
    <div class="acc-item"><span class="acc-w">盲从</span><span class="acc-d">不问是非地附和别人，盲目跟从。如\u201c否则便是盲从，便是迷信\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">辨伪去妄</span><span class="acc-d">辨别虚假、去除荒谬。指对所学内容进行甄别，剔除不实之说。</span></div>
    <div class="acc-item"><span class="acc-w">墨守</span><span class="acc-d">固执保守，不肯改变。源于战国时墨子善于守城，后以\u201c墨守成规\u201d形容因循守旧。</span></div>
    <div class="acc-item"><span class="acc-w">停滞</span><span class="acc-d">因为受到阻碍，不能顺利地运动或发展。如\u201c一切学术停滞\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">流俗</span><span class="acc-d">指社会上流行的风俗习惯（含贬义）。如\u201c不但对于流俗传说\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">启迪</span><span class="acc-d">开导、启发。如\u201c启迪新发明的基本条件\u201d。</span></div>
  </div>

  <div class="acc-cat">
    <h3>用字与读音</h3>
    <div class="acc-item"><span class="acc-w">颐（yí）</span><span class="acc-d">程颐，北宋理学家。\u300c颐\u300d页字旁，面颊、保养。不读 yǐ。</span></div>
    <div class="acc-item"><span class="acc-w">载（zài）</span><span class="acc-d">张载，北宋理学家。多音字：zǎi（记载、一年半载）/ zài（载重、载歌载舞）。人名中读 zài。</span></div>
    <div class="acc-item"><span class="acc-w">譬（pì）</span><span class="acc-d">譬如。不读 bì。\u300c譬\u300d言字旁。</span></div>
    <div class="acc-item"><span class="acc-w">萤（yíng）</span><span class="acc-d">腐草为萤。\u300c萤\u300d草字头，萤火虫。与\u300c莹\u300d（玉字旁，光亮）、\u300c荧\u300d（火字旁，微光）区分。</span></div>
    <div class="acc-item"><span class="acc-w">妄（wàng）</span><span class="acc-d">虚妄。\u300c妄\u300d女字头，荒谬。不读 wǎng。与\u300c忘\u300d（心字底）区分。</span></div>
    <div class="acc-item"><span class="acc-w">辨（biàn）</span><span class="acc-d">辨别。\u300c辨\u300d辛字旁中间是一点一撇。与\u300c辩\u300d（言字旁，辩论）、\u300c辫\u300d（绞丝旁，辫子）区分。</span></div>
    <div class="acc-item"><span class="acc-w">塾（shú）</span><span class="acc-d">塾师。\u300c塾\u300d土字底，旧时私人设立的教学地方。不读 shǔ。与\u300c熟\u300d（四点底）区分。</span></div>
    <div class="acc-item"><span class="acc-w">滞（zhì）</span><span class="acc-d">停滞。\u300c滞\u300d三点水，不流通。不读 dài。与\u300c置\u300d（四字头，放置）区分。</span></div>
  </div>

  <div class="acc-cat">
    <h3>修辞方法</h3>
    <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">第6段\u201c常常要抱怀疑的态度，常常和书中的学说辩论，常常评判书中的学说，常常修正书中的学说\u201d，四个\u201c常常\u201d构成排比，语势充沛，强调怀疑精神贯穿治学全过程。</span></div>
    <div class="acc-item"><span class="acc-w">反问/连续追问</span><span class="acc-d">第4段对三皇五帝连用四个问句（\u201c这是谁说的话？最先见于何书？所见的书是何时何人著的？著者何以知道？\u201d），以连续追问的方式具体展示怀疑精神的运用，增强语势。</span></div>
    <div class="acc-item"><span class="acc-w">引用</span><span class="acc-d">全文多处引用古今中外学者名言：程颐、张载（开篇）、孟子（第5段）、笛卡儿（第6段），以权威言论佐证论点，增强说服力。</span></div>
    <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">第6段正面论证怀疑推动学问发展与反面假设墨守旧说导致学术停滞形成对比；\u201c不打折扣地承认\u201d的思想懒惰与\u201c常常怀疑、常常发问\u201d的主动治学形成对比。</span></div>
  </div>

  <div class="acc-cat">
    <h3>写作借鉴</h3>
    <div class="acc-item"><span class="acc-w">引用名言开篇</span><span class="acc-d">文章以程颐、张载两句名言独立成段开篇，既引出中心论点，又作为道理论据，醒目有力。写作议论文时可借鉴这种\u201c引文开篇\u201d的写法。</span></div>
    <div class="acc-item"><span class="acc-w">承上启下的过渡句</span><span class="acc-d">第6段开头\u201c怀疑不仅是消极方面\u2026\u2026也是积极方面\u2026\u2026\u201d用递进复句作过渡，将论证从一个层面推进到另一个层面，使文章结构严谨、层次分明。</span></div>
    <div class="acc-item"><span class="acc-w">正反对比论证</span><span class="acc-d">文章在正面论证怀疑的积极作用后，又从反面假设墨守旧说的危害，正反对照，使论点更加鲜明。这种\u201c正面立论+反面假设\u201d的写法值得借鉴。</span></div>
    <div class="acc-item"><span class="acc-w">举例与引用结合</span><span class="acc-d">第6段既有戴震善疑的具体事例，又有笛卡儿的哲学名言，事例与名言相得益彰，使论证既有事实支撑又有理论高度。</span></div>
  </div>

  <div class="acc-cat">
    <h3>文化常识</h3>
    <div class="acc-item"><span class="acc-w">程颐</span><span class="acc-d">（1033\u20141107），字正叔，世称伊川先生，北宋理学家、教育家。与其兄程颢合称\u201c二程\u201d，同为理学奠基者，其学说后为朱熹继承发展，世称\u201c程朱理学\u201d。</span></div>
    <div class="acc-item"><span class="acc-w">张载</span><span class="acc-d">（1020\u20141077），字子厚，世称横渠先生，北宋理学家。\u201c关学\u201d创始人。其名言\u201c为天地立心，为生民立命，为往圣继绝学，为万世开太平\u201d广为传诵。</span></div>
    <div class="acc-item"><span class="acc-w">三皇五帝</span><span class="acc-d">传说中远古时代的帝王。\u201c三皇\u201d一般指伏羲、神农、女娲（或燧人、伏羲、神农）；\u201c五帝\u201d一般指黄帝、颛顼、帝喾、尧、舜。因是传说，史料记载不一，正是怀疑考辨的对象。</span></div>
    <div class="acc-item"><span class="acc-w">腐草为萤</span><span class="acc-d">出自《礼记·月令》：\u201c季夏之月\u2026\u2026腐草为萤。\u201d古人误认为萤火虫是由腐烂的草变化而成，是一种不科学的说法。文中以此为例说明对传说应追问科学根据。</span></div>
    <div class="acc-item"><span class="acc-w">戴震</span><span class="acc-d">（1724\u20141777），字东原，安徽休宁人，清代著名思想家、学者，皖派经学创始人。他治学精于考证，对天文、数学、历史、地理均有深入研究，著有《孟子字义疏证》等。</span></div>
    <div class="acc-item"><span class="acc-w">笛卡儿</span><span class="acc-d">（1596\u20141650），法国哲学家、物理学家、数学家，解析几何的创始人。他提出\u201c我思故我在\u201d（文中作\u201c我怀疑，所以我存在\u201d）的哲学命题，主张以怀疑的方法审视一切，是西方近代哲学的奠基人之一。</span></div>
    <div class="acc-item"><span class="acc-w">古史辨派</span><span class="acc-d">中国现代史学流派，以顾颉刚为代表，因编辑出版《古史辨》而得名。该派以怀疑精神考辨中国古史，提出\u201c层累地造成的中国古史\u201d学说，对中国现代史学发展产生了深远影响。</span></div>
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
  <div class="kai">《怀疑与学问》</div>
  <div>顾颉刚 · 现代 · 出自《宝树园文存》</div>
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
