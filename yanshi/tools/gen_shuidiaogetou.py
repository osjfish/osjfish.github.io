# -*- coding: utf-8 -*-
"""生成《水调歌头》课件"""
import json, os, re

OUT = r"D:\App\Apps\yanshi\shuidiaogetou-sushi.html"
LQ = "\u201c"  # "
RQ = "\u201d"  # "

# ========== 逐句数据：(原文, 译文, 赏析, [(词,注释),...]) ==========
VERSES = [
    ("明月几时有？把酒问青天。",
     "明月从什么时候才开始出现的？我端起酒杯遥问苍天。",
     "起笔化用李白《把酒问月》" + LQ + "青天有月来几时？我今停杯一问之" + RQ + "句意，以设问开篇，把酒问月，气势豪迈。" + LQ + "明月几时有" + RQ + "一问，排空而来，将读者引入浩渺宇宙的遐想之中。" + LQ + "把酒问青天" + RQ + "，一个" + LQ + "问" + RQ + "字，写出词人对宇宙人生的终极追问，也为全词定下旷达超逸的基调。",
     [("几时有", "从什么时候才有。几，疑问代词，多少"),
      ("把酒", "端起酒杯。把，持、拿"),
      ("青天", "苍天、蔚蓝的天空")]),
    ("不知天上宫阙，今夕是何年。",
     "不知道在天上的宫殿，今天晚上是何年何月。",
     "承接上句" + LQ + "问青天" + RQ + "，想象天上宫阙的岁月。" + LQ + "不知" + RQ + "二字，将人间与天上对照，写出对天上世界的向往与迷惘。" + LQ + "今夕是何年" + RQ + "，化用唐人传奇《周秦行纪》中" + LQ + "香风引到大罗天，月地云阶拜洞仙。共道人间惆怅事，不知今夕是何年" + RQ + "句意，暗含词人对朝廷政局的关切——此时苏轼外放密州，与朝廷睽违已久，不知" + LQ + "今夕" + RQ + "朝廷是何局面。",
     [("宫阙", "（gōng què）宫殿。阙，皇宫门前两边的望楼，代指宫殿"),
      ("今夕", "今天晚上。夕，夜晚"),
      ("何年", "哪一年、什么年月")]),
    ("我欲乘风归去，又恐琼楼玉宇，高处不胜寒。",
     "我想要凭借风力回到天上去，又担心在美玉砌成的楼宇中，受不住高耸九天的寒冷。",
     "这是全词情感最曲折的一句。" + LQ + "我欲乘风归去" + RQ + "，写词人对天上世界的向往——" + LQ + "归去" + RQ + "二字，暗示词人自认为本是天上之人（" + LQ + "谪仙" + RQ + "意识），此番只是暂谪人间。但" + LQ + "又恐" + RQ + "一转，情感陡生波澜：" + LQ + "琼楼玉宇" + RQ + "虽美，却" + LQ + "高处不胜寒" + RQ + "。这一句含蓄地表达了词人对朝廷的复杂心态：既想重返朝廷，又畏惧党争倾轧的险恶。" + LQ + "不胜寒" + RQ + "三字，语意双关，既写天上之寒，又写朝廷之寒。",
     [("欲", "想要、打算"),
      ("乘风", "凭借风力。乘，凭借、利用"),
      ("归去", "回到天上去。归，返回；去，往、到"),
      ("恐", "担心、害怕"),
      ("琼楼玉宇", "（qióng lóu yù yǔ）美玉砌成的楼宇，指想象中的月中仙宫。琼，美玉；宇，屋檐，代指房屋"),
      ("不胜", "（bù shèng）承受不住、禁受不起。胜，承受、禁受"),
      ("寒", "寒冷")]),
    ("起舞弄清影，何似在人间。",
     "在月光下起舞，赏玩自己清朗的影子，哪里比得上在人间的美好呢。",
     "上阕以" + LQ + "何似在人间" + RQ + "收束，情感由天上回到人间。" + LQ + "起舞弄清影" + RQ + "，化用李白" + LQ + "我歌月徘徊，我舞影零乱" + RQ + "（《月下独酌》）句意，写词人在月光下翩翩起舞，与自己的影子嬉戏。一个" + LQ + "弄" + RQ + "字，写出词人的洒脱与自得。" + LQ + "何似在人间" + RQ + "，以反问作结，表达了对人间生活的热爱与肯定——天上虽美，却高寒难耐；人间虽有缺憾，却有温情与乐趣。这一句完成了上阕由" + LQ + "出世" + RQ + "到" + LQ + "入世" + RQ + "的情感转折。",
     [("起舞", "起身舞蹈。起，起身；舞，舞蹈"),
      ("弄", "赏玩、嬉戏。此处指与影子嬉戏"),
      ("清影", "清朗的影子。清，清朗、清晰"),
      ("何似", "哪里比得上、怎么像。何，哪里、怎么；似，像、如同")]),
    ("转朱阁，低绮户，照无眠。",
     "月光转过朱红的楼阁，低低地照进雕花的窗户，照着心事重重、无法入眠的人。",
     "下阕以写月起笔，" + LQ + "转" + RQ + LQ + "低" + RQ + LQ + "照" + RQ + "三个动词，写出月光的移动轨迹，也暗示时间的流逝。" + LQ + "朱阁" + RQ + LQ + "绮户" + RQ + "，写富贵人家的建筑，与词人" + LQ + "无眠" + RQ + "的清苦形成对照。" + LQ + "照无眠" + RQ + "三字，将月光与人事联系起来——月光本无情，却照着一个因思念而无法入眠的人。此句暗写弟弟苏辙（子由），此时兄弟二人已七年未见，中秋月圆之夜，词人对月怀人，辗转难眠。",
     [("转", "移动、转过。此处指月光移动"),
      ("朱阁", "朱红色的楼阁。朱，大红色；阁，楼阁"),
      ("低", "低低地、低垂。此处指月光低照"),
      ("绮户", "（qǐ hù）雕花的窗户。绮，有花纹的丝织品，引申为雕花、华美"),
      ("照", "照射、照耀"),
      ("无眠", "无法入眠的人。眠，睡眠")]),
    ("不应有恨，何事长向别时圆？",
     "明月不应该对人们有什么怨恨吧，为什么总是在人们离别的时候才圆呢？",
     "这一句是全词情感最浓烈的地方。词人埋怨明月：" + LQ + "不应有恨" + RQ + "——你月亮不该有什么遗憾怨恨啊，" + LQ + "何事长向别时圆" + RQ + "——可为什么偏偏在人们离别的时候圆呢？这一问，看似无理，实则有情：月圆人不圆，最是令人伤感。" + LQ + "长向" + RQ + "二字，写出这种遗憾的经常性与普遍性——不只是今夜，而是每每如此。这一句将个人的离别之苦，升华为对人生缺憾的普遍感慨，为下文" + LQ + "人有悲欢离合" + RQ + "的哲理思考做了铺垫。",
     [("不应", "不应该。应，应该"),
      ("恨", "怨恨、遗憾"),
      ("何事", "为什么、什么缘故。何，什么；事，事情、缘故"),
      ("长向", "总是在、常常偏向。长，总是、经常；向，在、于"),
      ("别时", "离别的时候。别，离别、分别"),
      ("圆", "月圆")]),
    ("人有悲欢离合，月有阴晴圆缺，此事古难全。",
     "人有悲欢离合的变迁，月有阴晴圆缺的转换，这种事情自古以来就难以周全。",
     "这是全词的哲理核心，也是苏轼旷达人生观的集中体现。词人由个人的离别之苦，上升到对宇宙人生规律的理性认识：" + LQ + "人有悲欢离合" + RQ + "，是人生的常态；" + LQ + "月有阴晴圆缺" + RQ + "，是自然的规律。" + LQ + "此事古难全" + RQ + "——自古以来，就没有十全十美的事情。这一句将" + LQ + "人事" + RQ + "与" + LQ + "天道" + RQ + "并提，说明缺憾是宇宙人生的普遍规律，非人力所能改变。认识到这一点，便能从个人的痛苦中超脱出来，达到旷达的境界。此句与刘禹锡" + LQ + "沉舟侧畔千帆过，病树前头万木春" + RQ + "有异曲同工之妙，都是由个人悲慨升华为哲理思考。",
     [("悲欢离合", "悲伤、欢乐、离别、团聚。泛指人生的各种遭遇"),
      ("阴晴圆缺", "（月亮的）阴暗、晴朗、圆满、缺损。泛指自然的变化"),
      ("此事", "这种事情。指悲欢离合、阴晴圆缺"),
      ("古", "自古以来、从古到今"),
      ("难全", "难以周全、难以完美。全，周全、完美")]),
    ("但愿人长久，千里共婵娟。",
     "只希望这世上所有人的亲人都能平安健康，即使相隔千里，也能共享这美好的月光。",
     "全词以这一千古名句作结，情感由哲理思考回到美好祝愿。" + LQ + "但愿" + RQ + "二字，写出词人最真挚的祈愿。" + LQ + "人长久" + RQ + "，不是祈求长生不老，而是祝愿亲人平安健康。" + LQ + "千里共婵娟" + RQ + "，化用谢庄《月赋》" + LQ + "美人迈兮音尘阙，隔千里兮共明月" + RQ + "句意，写即使相隔千里，也能共享这一轮明月。" + LQ + "婵娟" + RQ + "，本指美好的样子，此处代指月亮。这一句将对弟弟苏辙的思念，扩展为对天下所有离人的美好祝愿，境界阔大，情韵悠长。千百年来，每逢中秋，人们便会吟诵此句，以寄相思。",
     [("但愿", "只希望、只愿。但，只、仅仅"),
      ("长久", "平安长久、健康长寿"),
      ("千里", "千里之遥，指相隔遥远"),
      ("共", "共同、一起"),
      ("婵娟", "（chán juān）本指美好的样子，此处代指月亮。一说指美人")]),
]

# ========== 字形题库 ==========
DICT_WORDS = [
    {"w":"阙","py":"què","q":"不知天上宫□，今夕是何年","tip":"「宫阙」门字框，音 què，勿写「阕」（已封闭）"},
    {"w":"琼","py":"qióng","q":"又恐□楼玉宇，高处不胜寒","tip":"「琼楼」王字旁，音 qióng（美玉），勿写「穷」"},
    {"w":"胜","py":"shèng","q":"高处不□寒","tip":"「不胜」此处读 shèng（承受），勿读 shēng"},
    {"w":"绮","py":"qǐ","q":"转朱阁，低□户，照无眠","tip":"「绮户」纟旁，音 qǐ（有花纹的丝织品），勿写「倚」「琦」"},
    {"w":"眠","py":"mián","q":"转朱阁，低绮户，照无□","tip":"「无眠」目字旁，音 mián，勿写「眼」"},
    {"w":"事","py":"shì","q":"不应有恨，何□长向别时圆","tip":"「何事」事字，勿写「是」「世」"},
    {"w":"圆","py":"yuán","q":"不应有恨，何事长向别时□","tip":"「圆」囗框（全包围），内「员」，勿写「园」"},
    {"w":"缺","py":"quē","q":"月有阴晴圆□，此事古难全","tip":"「缺」缶字旁，音 quē，勿写「决」「诀」"},
    {"w":"婵","py":"chán","q":"但愿人长久，千里共□娟","tip":"「婵娟」女字旁，音 chán，勿写「蝉」「禅」"},
    {"w":"娟","py":"juān","q":"但愿人长久，千里共婵□","tip":"「婵娟」女字旁，音 juān，勿写「涓」「捐」"},
    {"w":"乘","py":"chéng","q":"我欲□风归去","tip":"「乘风」此处读 chéng（凭借），勿读 shèng"},
    {"w":"阙","py":"què","q":"不知天上宫□","tip":"「阙」门字框，右「欠」，音 què"},
]

# ========== 注释题库 ==========
DICT_NOTES = [
    {"w":"把酒","q":"明月几时有？把酒问青天。","a":"端起酒杯。把，持、拿"},
    {"w":"宫阙","q":"不知天上宫阙，今夕是何年。","a":"（gōng què）宫殿。阙，皇宫门前两边的望楼，代指宫殿"},
    {"w":"今夕","q":"不知天上宫阙，今夕是何年。","a":"今天晚上。夕，夜晚"},
    {"w":"乘风","q":"我欲乘风归去，又恐琼楼玉宇，高处不胜寒。","a":"凭借风力。乘，凭借、利用"},
    {"w":"归去","q":"我欲乘风归去，又恐琼楼玉宇，高处不胜寒。","a":"回到天上去。归，返回；去，往、到"},
    {"w":"琼楼玉宇","q":"我欲乘风归去，又恐琼楼玉宇，高处不胜寒。","a":"（qióng lóu yù yǔ）美玉砌成的楼宇，指想象中的月中仙宫"},
    {"w":"不胜","q":"我欲乘风归去，又恐琼楼玉宇，高处不胜寒。","a":"（bù shèng）承受不住、禁受不起。胜，承受"},
    {"w":"弄","q":"起舞弄清影，何似在人间。","a":"赏玩、嬉戏。此处指与影子嬉戏"},
    {"w":"何似","q":"起舞弄清影，何似在人间。","a":"哪里比得上、怎么像"},
    {"w":"朱阁","q":"转朱阁，低绮户，照无眠。","a":"朱红色的楼阁。朱，大红色"},
    {"w":"绮户","q":"转朱阁，低绮户，照无眠。","a":"（qǐ hù）雕花的窗户。绮，有花纹的丝织品"},
    {"w":"无眠","q":"转朱阁，低绮户，照无眠。","a":"无法入眠的人。眠，睡眠"},
    {"w":"何事","q":"不应有恨，何事长向别时圆？","a":"为什么、什么缘故"},
    {"w":"长向","q":"不应有恨，何事长向别时圆？","a":"总是在、常常偏向。长，总是"},
    {"w":"悲欢离合","q":"人有悲欢离合，月有阴晴圆缺，此事古难全。","a":"悲伤、欢乐、离别、团聚，泛指人生的各种遭遇"},
    {"w":"阴晴圆缺","q":"人有悲欢离合，月有阴晴圆缺，此事古难全。","a":"（月亮的）阴暗、晴朗、圆满、缺损，泛指自然的变化"},
    {"w":"难全","q":"人有悲欢离合，月有阴晴圆缺，此事古难全。","a":"难以周全、难以完美。全，周全"},
    {"w":"但愿","q":"但愿人长久，千里共婵娟。","a":"只希望、只愿。但，只、仅仅"},
    {"w":"婵娟","q":"但愿人长久，千里共婵娟。","a":"（chán juān）本指美好的样子，此处代指月亮"},
]

# ========== 注释标注函数 ==========
def annotate(text, zhushi):
    pairs = []
    for word, note in zhushi:
        pure = re.sub(r'\([^)]*\)', '', word)
        pairs.append((pure, note))
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    result = text
    used = set()
    for pure, note in pairs:
        if pure in used: continue
        idx = 0
        while True:
            pos = result.find(pure, idx)
            if pos == -1: break
            before = result[:pos]
            if before.count('<span class="anno-word"') > before.count('</span>'):
                idx = pos + len(pure)
                continue
            span = f'<span class="anno-word" data-note="{note}">{pure}</span>'
            result = result[:pos] + span + result[pos+len(pure):]
            idx = pos + len(span)
            used.add(pure)
            break
    return result

# ========== 生成解读卡片 ==========
def gen_verses():
    html = []
    for i, (orig, trans, app, zhushi) in enumerate(VERSES):
        annotated = annotate(orig, zhushi)
        html.append(f'''      <div class="verse" id="v{i+1}" data-i="{i}">
        <div class="v-top"><span class="v-no">{i+1}</span><div class="v-line">{annotated}</div></div>
        <details class="v-more">
          <summary>译文 · 赏析</summary>
          <div class="d-body">
            <div class="v-sec"><b class="v-label">译　文</b>
              <div class="v-trans">{trans}</div>
            </div>
            <div class="v-sec"><b class="v-label">赏　析</b>
              <div class="d-body"><p>{app}</p></div>
            </div>
          </div>
        </details>
      </div>''')
    return '\n'.join(html)

# ========== 生成fulltext ==========
def gen_fulltext():
    html = []
    for i, (orig, _, _, zhushi) in enumerate(VERSES):
        annotated = annotate(orig, zhushi)
        html.append(f'    <div class="pl"><span class="no">{i+1}</span>{annotated}</div>')
    return '\n'.join(html)

# Read CSS from 酬乐天 file (same framework)
with open(r'D:\App\Apps\yanshi\chouletianyangzhouchufengxishangjianzeng-liuyuxi.html', 'r', encoding='utf-8') as f:
    ref = f.read()
CSS = ref[ref.find('<style>')+7:ref.find('</style>')]

# Read JS from 酬乐天 file, replace localStorage key
JS = ref[ref.find('<script>')+8:ref.find('</script>')]
JS = JS.replace('chouletian_fs', 'shuidiaogetou_fs')

# Replace DICT_WORDS and DICT_NOTES in JS
js_start = JS.find('var DICT_WORDS')
js_before = JS[:js_start]
# Find end of DICT_NOTES (the last ]; before var dictate)
dict_end = JS.find('];', JS.find('var DICT_NOTES')) + 2
js_after = JS[dict_end:]

new_dicts = 'var DICT_WORDS = ' + json.dumps(DICT_WORDS, ensure_ascii=False) + ';\n'
new_dicts += '  var DICT_NOTES = ' + json.dumps(DICT_NOTES, ensure_ascii=False) + ';'

JS = js_before + new_dicts + js_after

# ========== 组装HTML ==========
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《水调歌头》苏轼</title>
<meta name="description" content="苏轼《水调歌头·明月几时有》逐句注释、译文、赏析，生僻字与易错词附注音，含背景、原文（背诵模式）、解读、赏析、积累、练习，风格典雅，适合课堂教学。">
<style>{CSS}
</style>
</head>
<body>

<header class="hero" id="top">
  <div class="hero-inner">
    <div class="hero-side">宋·苏轼</div>
    <h1 class="hero-title">水调歌头</h1>
  </div>
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

<section id="bg">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>宋神宗熙宁九年（1076）中秋，苏轼在密州（今山东诸城）任知州。彼时他因与王安石政见不合，自请外放，已在地方任职多年。中秋之夜，词人赏月饮酒，通宵达旦，写下这首《水调歌头》，兼怀弟弟苏辙（子由）。此时兄弟二人已七年未见。全词由望月而生发，从问月到想归，从出世到入世，从个人离别到人生哲理，最终以" + LQ + "但愿人长久，千里共婵娟" + RQ + "的美好祝愿作结，境界阔大，情韵悠长，被誉为中秋词的绝唱。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>苏轼（1037—1101），字子瞻，号东坡居士，眉州眉山（今四川眉山）人，北宋文学家、书画家、美食家，" + LQ + "唐宋八大家" + RQ + "之一。与父苏洵、弟苏辙合称" + LQ + "三苏" + RQ + "。嘉祐二年（1057）进士，曾任翰林学士、礼部尚书等职。因" + LQ + "乌台诗案" + RQ + "被贬黄州，后又被贬惠州、儋州。苏轼是北宋文坛领袖，诗、词、文、书、画皆精，与黄庭坚并称" + LQ + "苏黄" + RQ + "，与辛弃疾并称" + LQ + "苏辛" + RQ + "，与欧阳修并称" + LQ + "欧苏" + RQ + "。词风豪放旷达，开创豪放词派，对后世影响深远。</p>
    <p class="note">※ 名篇有《念奴娇·赤壁怀古》《水调歌头·明月几时有》《江城子·密州出猎》《定风波》《赤壁赋》等。</p>
  </div>
  <div class="box">
    <h3>创作背景</h3>
    <p>宋神宗熙宁四年（1071），苏轼因与王安石政见不合，自请外放，任杭州通判。熙宁七年（1074），改任密州知州。熙宁九年（1076）中秋，苏轼在密州赏月饮酒，写下这首《水调歌头》，词前小序云：" + LQ + "丙辰中秋，欢饮达旦，大醉，作此篇，兼怀子由。" + RQ + "</p>
    <p>此时苏轼与弟弟苏辙已七年未见。苏辙（1039—1112），字子由，号颍滨遗老，" + LQ + "唐宋八大家" + RQ + "之一。兄弟二人感情深厚，早年同科进士，后因政见与仕途原因，长期分离。中秋月圆之夜，词人对月怀人，写下这首千古名篇。</p>
    <p>关于这首词的创作，还有一段佳话：据《坡仙集外纪》记载，苏轼写完此词后，" + LQ + "以此词示客，客皆称善" + RQ + "。南宋胡仔《苕溪渔隐丛话》更是评价：" + LQ + "中秋词，自东坡《水调歌头》一出，余词尽废。" + RQ + "</p>
  </div>
  <div class="box">
    <h3>词牌说明</h3>
    <p>《水调歌头》，词牌名，又名《元会曲》《凯歌》《台城游》等。相传隋炀帝开汴河时制《水调歌》，唐人演为大曲，" + LQ + "歌头" + RQ + "是大曲的第一章（中序开头的一遍）。此调双调九十五字，上阕九句四平韵，下阕十句四平韵。苏轼此词是《水调歌头》最著名的作品，后人多以此为正体。</p>
  </div>
  <div class="box media-box">
    <h3>朗诵 · 演唱</h3>
    <div class="media-grid">
      <div class="media">
        <h4>《水调歌头·明月几时有》名家朗诵——诵读客</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1y14y1e7gD&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="水调歌头朗诵"></iframe>
        <a href="https://www.bilibili.com/video/BV1y14y1e7gD" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>《水调歌头·但愿人长久》歌曲演唱——王菲</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV17w41117gN&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="水调歌头歌曲"></iframe>
        <a href="https://www.bilibili.com/video/BV17w41117gN" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>

<section id="jielu">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 注释 / 译文 / 赏析</span></div>
  <div class="sec-sub">每句含<b>注释</b>（生僻字、易错词均附读音）、译文与赏析，点击可展开。全词分上下两阕：上阕写望月问天、欲归又恐，终以" + LQ + "何似在人间" + RQ + "肯定人间；下阕写对月怀人、由怨转悟，终以" + LQ + "千里共婵娟" + RQ + "寄愿。</div>
  <div class="texttools">
    <button id="btnShowAll" class="off" style="display:none">显示全部</button>
  </div>

  <div id="fulltext" class="poem" style="display:none">
{gen_fulltext()}
  </div>

  <div class="verse-list" id="verseList">

  <div class="part-head"><span class="p-num">上阕</span><h3>望月问天 · 欲归又恐</h3><span class="range">第 1–4 句</span></div>
  <div class="part-overview">上阕由望月起笔，" + LQ + "明月几时有" + RQ + "排空一问，引入宇宙遐想；" + LQ + "我欲乘风归去" + RQ + "写出世之想，" + LQ + "又恐琼楼玉宇" + RQ + "一转，写对朝廷的复杂心态；终以" + LQ + "何似在人间" + RQ + "肯定人间，完成由出世到入世的情感转折。</div>

{gen_verses()[:gen_verses().find('id="v5"')-6]}

  <div class="part-head"><span class="p-num">下阕</span><h3>对月怀人 · 由怨转悟</h3><span class="range">第 5–8 句</span></div>
  <div class="part-overview">下阕由写月过渡到怀人，" + LQ + "转朱阁，低绮户，照无眠" + RQ + "暗写思念弟弟的辗转难眠；" + LQ + "何事长向别时圆" + RQ + "以埋怨明月写离别之苦；" + LQ + "人有悲欢离合" + RQ + "由个人痛苦上升到人生哲理；终以" + LQ + "但愿人长久，千里共婵娟" + RQ + "的美好祝愿收束全词。</div>

{gen_verses()[gen_verses().find('id="v5"')-6:]}
  </div>
</section>

<div class="divider"></div>

<section id="app">
  <div class="sec-head"><h2>赏 析</h2><span class="no">名句 · 艺术 · 主题</span></div>

  <div class="box">
    <h3>千古名句</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">但愿人长久，千里共婵娟。</div>
        <p>全词以这一千古名句作结，将对弟弟苏辙的思念，扩展为对天下所有离人的美好祝愿。" + LQ + "但愿" + RQ + "二字，写出最真挚的祈愿；" + LQ + "人长久" + RQ + "，祝愿亲人平安健康；" + LQ + "千里共婵娟" + RQ + "，写即使相隔千里，也能共享这一轮明月。此句化用谢庄《月赋》" + LQ + "隔千里兮共明月" + RQ + "句意，而境界更阔大，情韵更悠长。千百年来，每逢中秋，人们便吟诵此句以寄相思，它已成为中华民族共同的文化记忆。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">人有悲欢离合，月有阴晴圆缺，此事古难全。</div>
        <p>这是全词的哲理核心。词人由个人的离别之苦，上升到对宇宙人生规律的理性认识：人生有悲欢离合，自然有阴晴圆缺，自古以来就没有十全十美的事情。这一句将" + LQ + "人事" + RQ + "与" + LQ + "天道" + RQ + "并提，说明缺憾是宇宙人生的普遍规律。认识到这一点，便能从个人的痛苦中超脱出来，达到旷达的境界。此句体现了苏轼独特的人生智慧——不是否认痛苦，而是在承认痛苦的基础上超越痛苦。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <p><b>一、构思奇崛，想象丰富。</b>全词由望月生发，" + LQ + "明月几时有" + RQ + "一问排空而来，" + LQ + "不知天上宫阙" + RQ + "引入想象，" + LQ + "我欲乘风归去" + RQ + "更是奇想天外。词人将神话传说（琼楼玉宇）与个人情感融为一体，创造出浩渺空灵的艺术境界。</p>
    <p><b>二、情感跌宕，一波三折。</b>全词情感经历了多次转折：上阕由问月（豪迈）→想归（向往）→又恐（忧虑）→何似在人间（肯定）；下阕由照无眠（思念）→埋怨明月（痛苦）→哲理感悟（超脱）→美好祝愿（旷达）。情感起伏跌宕，层层深入。</p>
    <p><b>三、虚实相生，意境空灵。</b>词中既有实写（把酒问月、起舞弄影、转朱阁低绮户），又有虚写（天上宫阙、琼楼玉宇、乘风归去），虚实相生，创造出空灵澄澈的意境。月光作为贯穿全词的意象，将天上与人间、现实与想象、个人与天下联结在一起。</p>
    <p><b>四、以议论入词，理趣盎然。</b>" + LQ + "人有悲欢离合，月有阴晴圆缺，此事古难全" + RQ + "是议论，但不是抽象的说教，而是从个人体验中提炼出的人生哲理，情理交融，理趣盎然。这是苏轼豪放词的重要特征——以诗的笔法、文的气格入词，扩大了词的表现功能。</p>
    <p><b>五、语言清丽，化用无痕。</b>全词多处化用前人诗句（李白《把酒问月》《月下独酌》、谢庄《月赋》、唐人传奇《周秦行纪》），但化用无痕，如从己出，体现了苏轼深厚的学养和高超的语言功力。</p>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>这首词是苏轼中秋望月怀人之作，表达了对弟弟苏辙的深切思念，也展现了词人旷达超脱的人生态度。全词由望月而生发，从问月到想归，从出世到入世，从个人离别到人生哲理，最终以" + LQ + "但愿人长久，千里共婵娟" + RQ + "的美好祝愿作结。词人没有沉溺于个人的离别之苦，而是由个人的痛苦上升到对宇宙人生规律的理性认识，在承认缺憾的基础上超越缺憾，达到了旷达的境界。这首词之所以成为千古绝唱，不仅因为它写出了人类共同的离别之思，更因为它提供了一种面对人生缺憾的积极态度——不是否认痛苦，而是在痛苦中寻找超越，在缺憾中发现美好。</p>
  </div>
</section>

<div class="divider"></div>

<section id="acc">
  <div class="sec-head"><h2>积 累</h2><span class="no">词牌 / 字音形 / 文言 / 炼字 / 修辞 / 文化</span></div>

  <div class="box">
    <h3>文体与词牌</h3>
    <div class="tw"><table>
      <tr><th style="width:120px">项目</th><th>说明</th></tr>
      <tr><td class="kai">词牌</td><td>《水调歌头》，又名《元会曲》《凯歌》《台城游》</td></tr>
      <tr><td class="kai">来源</td><td>相传隋炀帝开汴河时制《水调歌》，唐人演为大曲，" + LQ + "歌头" + RQ + "是大曲第一章</td></tr>
      <tr><td class="kai">格律</td><td>双调九十五字，上阕九句四平韵，下阕十句四平韵</td></tr>
      <tr><td class="kai">结构</td><td>上下两阕。上阕写望月问天、欲归又恐；下阕写对月怀人、由怨转悟</td></tr>
      <tr><td class="kai">小序</td><td>" + LQ + "丙辰中秋，欢饮达旦，大醉，作此篇，兼怀子由。" + RQ + "——交代时间、缘由、写作目的</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>易错字音形</h3>
    <div class="glossary">
      <div class="g-item"><dt>阙（què）</dt><dd>宫殿。门字框，勿写「阕」（已封闭、止息）</dd></div>
      <div class="g-item"><dt>琼（qióng）</dt><dd>美玉。王字旁，勿写「穷」</dd></div>
      <div class="g-item"><dt>胜（shèng）</dt><dd>承受。「不胜寒」读 shèng，勿读 shēng</dd></div>
      <div class="g-item"><dt>绮（qǐ）</dt><dd>有花纹的丝织品。纟旁，勿写「倚」「琦」</dd></div>
      <div class="g-item"><dt>眠（mián）</dt><dd>睡眠。目字旁，勿写「眼」</dd></div>
      <div class="g-item"><dt>缺（quē）</dt><dd>缺损。缶字旁，勿写「决」「诀」</dd></div>
      <div class="g-item"><dt>婵（chán）</dt><dd>「婵娟」女字旁，勿写「蝉」「禅」</dd></div>
      <div class="g-item"><dt>娟（juān）</dt><dd>「婵娟」女字旁，勿写「涓」「捐」</dd></div>
      <div class="g-item"><dt>乘（chéng）</dt><dd>凭借。「乘风」读 chéng，勿读 shèng</dd></div>
      <div class="g-item"><dt>长（cháng）</dt><dd>总是。「长向」读 cháng，不读 zhǎng</dd></div>
    </div>
  </div>

  <div class="box">
    <h3>文言梳理</h3>
    <div class="acc-sub">古今异义</div>
    <div class="tw"><table>
      <tr><th style="width:100px">词语</th><th style="width:200px">古义</th><th>今义</th></tr>
      <tr><td class="kai">归去</td><td>回到天上去（词人自认为谪仙）</td><td>返回、回去</td></tr>
      <tr><td class="kai">不胜</td><td>承受不住（胜，shèng，承受）</td><td>不能取胜、不能战胜</td></tr>
      <tr><td class="kai">何事</td><td>为什么、什么缘故</td><td>什么事情</td></tr>
      <tr><td class="kai">长向</td><td>总是在、常常偏向（长，cháng，总是）</td><td>长久地朝向</td></tr>
      <tr><td class="kai">婵娟</td><td>本指美好的样子，此处代指月亮</td><td>多用来形容女子姿态美好</td></tr>
    </table></div>
    <div class="acc-sub">一词多义</div>
    <div class="tw"><table>
      <tr><th style="width:80px">字</th><th style="width:160px">义项</th><th>例句</th></tr>
      <tr><td class="kai" rowspan="2">胜</td><td>承受、禁受（shèng）</td><td>高处不胜寒</td></tr>
      <tr><td>胜利、取胜</td><td>此所谓战胜于朝廷（《邹忌讽齐王纳谏》）</td></tr>
      <tr><td class="kai" rowspan="2">长</td><td>总是、经常（cháng）</td><td>何事长向别时圆</td></tr>
      <tr><td>长度大（cháng）/ 增长（zhǎng）</td><td>暂凭杯酒长精神（《酬乐天扬州初逢席上见赠》）</td></tr>
      <tr><td class="kai" rowspan="2">乘</td><td>凭借、利用（chéng）</td><td>我欲乘风归去</td></tr>
      <tr><td>辆（shèng，量词）</td><td>车六七百乘（《陈涉世家》）</td></tr>
    </table></div>
    <div class="acc-sub">词类活用</div>
    <p>（本词无典型词类活用现象）</p>
    <div class="acc-sub">文言句式</div>
    <p>（本词无特殊文言句式）</p>
  </div>

  <div class="box">
    <h3>炼字与意象（本文核心考点）</h3>
    <p><b>" + LQ + "问" + RQ + "字：</b>" + LQ + "把酒问青天" + RQ + "，一个" + LQ + "问" + RQ + "字，写出词人对宇宙人生的终极追问，气势豪迈，为全词定下旷达超逸的基调。</p>
    <p><b>" + LQ + "恐" + RQ + "字：</b>" + LQ + "又恐琼楼玉宇" + RQ + "，一个" + LQ + "恐" + RQ + "字，写出词人情感的转折——由向往天上转为忧虑高寒，含蓄地表达了对朝廷的复杂心态。</p>
    <p><b>" + LQ + "弄" + RQ + "字：</b>" + LQ + "起舞弄清影" + RQ + "，一个" + LQ + "弄" + RQ + "字，写出词人在月光下与影子嬉戏的洒脱与自得，化用李白" + LQ + "我舞影零乱" + RQ + "句意而更显灵动。</p>
    <p><b>" + LQ + "转" + RQ + LQ + "低" + RQ + LQ + "照" + RQ + "：</b>" + LQ + "转朱阁，低绮户，照无眠" + RQ + "，三个动词写出月光的移动轨迹，也暗示时间的流逝，将无情的月光写得有情有态。</p>
    <p><b>" + LQ + "月" + RQ + "的意象：</b>全词以月贯穿始终，月是词人情感的载体——问月、想归、恐寒、弄影、照无眠、怨月、悟月、愿月。月亮在词中既是自然景物，又是宇宙永恒的象征，更是寄托相思的媒介。</p>
  </div>

  <div class="box">
    <h3>修辞与手法</h3>
    <div class="tw"><table>
      <tr><th style="width:100px">手法</th><th>例句</th><th>分析</th></tr>
      <tr><td class="kai">设问</td><td>明月几时有？把酒问青天。</td><td>以设问开篇，排空而来，引入宇宙遐想</td></tr>
      <tr><td class="kai">想象</td><td>不知天上宫阙……我欲乘风归去</td><td>想象天上宫阙、乘风归去，创造浩渺空灵的境界</td></tr>
      <tr><td class="kai">对比</td><td>我欲乘风归去，又恐琼楼玉宇</td><td>" + LQ + "欲" + RQ + "与" + LQ + "恐" + RQ + "对比，写出情感的曲折</td></tr>
      <tr><td class="kai">拟人</td><td>转朱阁，低绮户，照无眠</td><td>将月光拟人化，写出月光的移动与情态</td></tr>
      <tr><td class="kai">反问</td><td>不应有恨，何事长向别时圆？</td><td>埋怨明月，看似无理，实则有情</td></tr>
      <tr><td class="kai">对偶</td><td>人有悲欢离合，月有阴晴圆缺</td><td>人事与天道并提，工整而富有哲理</td></tr>
      <tr><td class="kai">用典</td><td>千里共婵娟</td><td>化用谢庄《月赋》" + LQ + "隔千里兮共明月" + RQ + "句意</td></tr>
    </table></div>
  </div>

  <div class="box">
    <h3>文化常识</h3>
    <p><b>中秋节：</b>农历八月十五，是中国传统节日，又称团圆节、八月节。中秋节自古便有祭月、赏月、拜月、吃月饼、赏桂花、饮桂花酒等习俗，流传至今，经久不息。中秋节以月之圆兆人之团圆，为寄托思念故乡、思念亲人之情，祈盼丰收、幸福，成为丰富多彩、弥足珍贵的文化遗产。</p>
    <p><b>婵娟：</b>本指美好的样子，可用来形容女子、花木、月色等。在" + LQ + "千里共婵娟" + RQ + "中，" + LQ + "婵娟" + RQ + "代指月亮。这一用法始于苏轼此词，此后" + LQ + "婵娟" + RQ + "便成为月亮的雅称之一。</p>
    <p><b>琼楼玉宇：</b>指美玉砌成的楼宇，是中国古代神话中月中仙宫的别称。《大业拾遗记》载：" + LQ + "瞿乾祐于江岸玩月，或问此中何有？瞿笑曰：可随我指观之。俄见月规半天，琼楼玉宇烂然。" + RQ + "后以" + LQ + "琼楼玉宇" + RQ + "指月中宫殿，也泛指华美的楼宇。</p>
    <p><b>水调歌：</b>相传为隋炀帝杨广开汴河（大运河）时所制的乐曲。唐代演为大曲，入" + LQ + "商调" + RQ + "。" + LQ + "歌头" + RQ + "是大曲的第一章（中序开头的一遍），声调高亢悠扬。《水调歌头》作为词牌，即取大曲" + LQ + "水调歌" + RQ + "的开头一段填词而成。</p>
    <p><b>乌台诗案：</b>北宋元丰二年（1079），苏轼因作诗讽刺新法，被御史台弹劾入狱，史称" + LQ + "乌台诗案" + RQ + "（御史台别称" + LQ + "乌台" + RQ + "）。苏轼入狱一百三十日，几乎丧命，后被贬为黄州团练副使。此案是苏轼人生的重要转折点，也是他文学创作的重要分水岭——此后苏轼的词风更加旷达超脱。</p>
  </div>
</section>

<div class="divider"></div>

<section id="practice">
  <div class="sec-head"><h2>练 习</h2><span class="no">字形 · 注释 全屏听写</span></div>
  <div class="sec-sub">点击下方按钮进入全屏听写模式，适合课堂投影使用。可随机抽五组练习，也可练习全部题目。按 Esc 退出。</div>
  <div class="ptools">
    <button data-mode="word" data-rand="1">随机五组字形</button>
    <button data-mode="word" data-rand="0">全部字形</button>
    <button data-mode="note" data-rand="1">随机五组注释</button>
    <button data-mode="note" data-rand="0">全部注释</button>
  </div>
</section>

</main>

<footer>
  <div class="kai">《水调歌头·明月几时有》· 宋·苏轼</div>
  <div>但愿人长久，千里共婵娟。</div>
</footer>

<button class="top-btn" id="topBtn" title="回到顶部">↑</button>

<div class="anno-popup" id="annoPopup">
  <div class="aw" id="annoW"></div>
  <div class="an" id="annoN"></div>
</div>

<div class="dictate" id="dictate" hidden>
  <div class="dictate-top">
    <div class="dictate-mode" id="dictMode">字形听写</div>
    <div class="dictate-progress" id="dictProgress">第 1 / 1 题</div>
    <div>
      <button class="dictate-fs" id="dictFsMinus">A−</button>
      <button class="dictate-fs" id="dictFsPlus">A+</button>
      <button class="dictate-exit" id="dictExit">退出</button>
    </div>
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
    <button id="dictShow">显示答案</button>
    <button id="dictPrev">上一题</button>
    <button class="primary" id="dictNext">下一题</button>
  </div>
</div>

<script>
{JS}
</script>
</body>
</html>'''

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Generated: {OUT}")
print(f"Size: {os.path.getsize(OUT)} bytes")
