# -*- coding: utf-8 -*-
"""生成《永久的生命》严文井 课件"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\yongjiudeshengming-yanwenjing.html"
FS_KEY = "yongjiu_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

# 提取 <style>...</style>
style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
# 提取主 IIFE script (第一个 <script> 不含 DICT)
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]  # IIFE
main_js = main_js.replace("beiying_fs", FS_KEY)

# ===== 数据 =====
# 每段: (原文, 内容概括, 手法分析, [(词,注释),...])
paragraphs = [
    (
        "过去了的时间永不再回来。一个人到了三十岁的边头就会发现自己丢失了一些什么：一颗臼齿，一段盲肠，一些头发，一点点和人开玩笑的兴味，这意味着他已经失去了大半个青春。有限的岁月只能一度为你所有，它们既然离开，就永远不会再返回。智者对此也无能为力！个人生命不像一件衬衣，当你发现它脏了、破了的时候，就可以脱下它来洗涤，把它再补好。那存在过的忧愁，也许你能忘却，但却不能取消它遗留下的印迹。我们都非常可怜！",
        "以时间一去不返开篇，列举人到三十丢失的种种，感叹个人生命的有限与不可挽回，以“我们都非常可怜”收束，基调低沉。",
        "开门见山点出时间不可逆；用“臼齿、盲肠、头发、兴味”四个具体意象将抽象的青春流逝具象化；“衬衣”的比喻通俗而贴切，写生命不可修补；结尾感叹为下文转折蓄势。",
        [
            ("永不再回来", "永远不会再回来，强调时间的不可逆"),
            ("边头", "边缘、临近（指接近三十岁）"),
            ("臼齿", "（jiù chǐ）磨牙，在口腔后方，用于研磨食物"),
            ("盲肠", "（máng cháng）大肠的起始段，阑尾所在处"),
            ("兴味", "兴趣、兴致"),
            ("一度", "一次、一回"),
            ("智者", "有智慧的人"),
            ("无能为力", "用不上力量，指没有办法"),
            ("洗涤", "（xǐ dí）清洗"),
            ("印迹", "痕迹、印记"),
        ],
    ),
    (
        "人们却不应该为此感到悲观。我们没有时间悲观。我们应该看到生命自身的神奇，生命流动着，永远不朽。地面上的小草，它们是那样卑微，那样柔弱，每一个严寒的冬天过去后，它们依然一根根从土壤里钻出来，欢乐地迎着春天的风，好像那刚刚过去的寒冷从未存在。一万年前是这样，一万年以后也是这样！在春天，我们以同样感动的眼光看着山坡上那些小牛犊，它们跳跳蹦蹦，炫耀它们遍身金黄的茸毛。永远的小牛犊，永远的金黄色茸毛！",
        "笔锋一转，主张不应悲观。以小草经冬犹生、小牛犊年年欢跃为例，展现生命流动不息、永远不朽的神奇。",
        "“却”字转折，由低沉转向昂扬；小草“钻出来”“迎着春天的风”，拟人化写生命的顽强；“一万年前……一万年以后”以时间的跨度写生命的永恒；小牛犊的画面充满生机，与首段的衰老形成对比。",
        [
            ("悲观", "对世事失去信心和希望"),
            ("神奇", "非常奇妙"),
            ("不朽", "永不磨灭、永存"),
            ("卑微", "地位低下、渺小"),
            ("柔弱", "软弱、不刚强"),
            ("严寒", "极度寒冷"),
            ("土壤", "泥土、土地"),
            ("小牛犊", "（dú）小牛"),
            ("跳跳蹦蹦", "形容欢快跳跃的样子"),
            ("炫耀", "夸耀、展示"),
            ("茸毛", "（róng）细软的毛"),
        ],
    ),
    (
        "感谢生命的奇迹，它分开来是暂时，合起来却是永久。它是一个不懂疲倦的旅客，总是只暂时在哪一个个体内住一会儿，便又离开前去。那些个体消逝了，它却永远存在。它充满了希望，永不休止地繁殖着，蔓延着，随处宣示它的快乐和威势。",
        "揭示生命的哲理：个体生命短暂，而生命整体永恒。生命如不知疲倦的旅客，在个体间传递，永远充满希望与力量。",
        "“分开来是暂时，合起来却是永久”是全文的核心哲思；“不懂疲倦的旅客”比喻生命在个体间的流转，生动形象；“繁殖、蔓延、宣示”三个动词层层递进，写生命的蓬勃与不可阻挡。",
        [
            ("奇迹", "想象不到的不平凡的事情"),
            ("暂时", "短时间之内"),
            ("永久", "永远、长久"),
            ("疲倦", "疲乏、困倦"),
            ("旅客", "旅行的人"),
            ("消逝", "消失、逝去"),
            ("永不休止", "永远不停止"),
            ("繁殖", "生物产生新的个体"),
            ("蔓延", "像蔓草一样向周围扩展"),
            ("宣示", "公开表示、显示"),
            ("威势", "威力和气势"),
        ],
    ),
    (
        "我的伙伴们，我们的心应该感到舒畅。那些暴君们能够杀害许多许多人，但是他们消灭不了生命。让我们赞美生命，赞美那毁灭不掉的生命吧！我们将要以不声不响的爱情来赞美它。生命在那些终于要凋谢的花朵里永存，不断给世界以色彩，不断给世界以芬芳。",
        "呼吁伙伴们保持乐观，指出暴君可以杀人却消灭不了生命；以不声不响的爱赞美生命，生命在凋谢的花朵中永存，持续给世界带来色彩与芬芳。",
        "“伙伴们”的呼告拉近与读者的距离；“暴君消灭不了生命”将生命的主题提升到社会与历史的高度；“不声不响的爱情”含蓄而深沉；“凋谢的花朵里永存”以对比写生命的永恒，色彩与芬芳诉诸视觉与嗅觉，富有感染力。",
        [
            ("舒畅", "开朗愉快、舒服痛快"),
            ("暴君", "暴虐的君主"),
            ("消灭", "使消灭、除掉"),
            ("赞美", "称赞、颂扬"),
            ("毁灭", "摧毁消灭"),
            ("不声不响", "不说话、不出声，形容默默"),
            ("凋谢", "（草木花叶）脱落"),
            ("永存", "永远存在"),
            ("芬芳", "香气、香味"),
        ],
    ),
    (
        "凋谢和不朽混为一体，这就是奇迹。",
        "以一句话收束全文：凋谢（个体的死亡）与不朽（生命的永恒）融为一体，正是生命的奇迹。",
        "独句成段，简洁有力；“凋谢”与“不朽”看似矛盾，实则统一——个体消亡而生命永存，这正是全文的核心感悟，余味无穷。",
        [
            ("混为一体", "融合在一起，不可分割"),
            ("奇迹", "想象不到的不平凡的事情"),
        ],
    ),
]

# 全文流（背诵区）
fulltext_paras = [p[0] for p in paragraphs]

# ===== 构建解读区 =====
verse_html = ""
for i, (orig, content, method, annos) in enumerate(paragraphs):
    # 标注注释
    def annotate(text, annos):
        # 按词长降序匹配
        items = sorted(annos, key=lambda x: len(x[0]), reverse=True)
        result = text
        used = set()
        for word, note in items:
            if word in used:
                continue
            # 避免重复标注
            idx = result.find(word)
            if idx != -1:
                # 检查是否已在span内
                before = result[:idx]
                if before.count("<span") == before.count("</span>"):
                    span = f'<span class="anno-word" data-note="{note}">{word}</span>'
                    result = result[:idx] + span + result[idx+len(word):]
                    used.add(word)
        return result

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

# 全文流
fulltext_html = ""
for para in fulltext_paras:
    fulltext_html += f'    <div class="pl">{para}</div>\n'

# ===== 字形题 =====
dict_words = [
    {"w":"臼","py":"jiù","q":"一颗□齿，一段盲肠，一些头发","tip":"「臼」臼字头，舂米器具；笔画：撇、竖、横、横折、横、横"},
    {"w":"盲","py":"máng","q":"一颗臼齿，一段□肠，一些头发","tip":"「盲」目字旁，眼睛看不见；与「肓」（病入膏肓，月字旁）区分"},
    {"w":"涤","py":"dí","q":"就可以脱下它来洗□，把它再补好","tip":"「涤」三点水，清洗；不要写成「条」"},
    {"w":"朽","py":"xiǔ","q":"生命流动着，永远不□","tip":"「朽」木字旁，腐烂；不要写成「巧」"},
    {"w":"卑","py":"bēi","q":"它们是那样□微，那样柔弱","tip":"「卑」十字头，低下；不要写成「俾」"},
    {"w":"犊","py":"dú","q":"看着山坡上那些小牛□","tip":"「犊」牛字旁，小牛；与「渎」（三点水）、「牍」（片字旁）区分"},
    {"w":"耀","py":"yào","q":"它们跳跳蹦蹦，炫□它们遍身金黄的茸毛","tip":"「耀」光字旁，光线照射；笔画多，注意右边是「翟」"},
    {"w":"茸","py":"róng","q":"炫耀它们遍身金黄的□毛","tip":"「茸」草字头，细软的毛；与「葺」（qì，修补）区分"},
    {"w":"倦","py":"juàn","q":"它是一个不懂疲□的旅客","tip":"「倦」单人旁，疲乏；与「蜷」（虫字旁）区分"},
    {"w":"逝","py":"shì","q":"那些个体消□了，它却永远存在","tip":"「逝」走之底，消失；不要写成「世」"},
    {"w":"殖","py":"zhí","q":"永不休止地繁□着，蔓延着","tip":"「殖」歹字旁，生育；与「值」（单人旁）区分"},
    {"w":"蔓","py":"màn","q":"永不休止地繁殖着，□延着","tip":"「蔓」草字头，蔓草；不要写成「漫」（三点水）"},
    {"w":"虐","py":"nüè","q":"那些暴□们能够杀害许多许多人","tip":"「虐」虎字头，残暴；注意下面是「虍」的变形"},
    {"w":"凋","py":"diāo","q":"生命在那些终于要□谢的花朵里永存","tip":"「凋」两点水，草木衰落；与「雕」（隹字旁）区分"},
    {"w":"芬","py":"fēn","q":"不断给世界以色彩，不断给世界以□芳","tip":"「芬」草字头，香气；不要写成「纷」（绞丝旁）"},
]

# ===== 注释题 =====
dict_notes = [
    {"w":"臼齿","a":"磨牙，在口腔后方，用于研磨食物","q":"一颗臼齿，一段盲肠"},
    {"w":"兴味","a":"兴趣、兴致","q":"一点点和人开玩笑的兴味"},
    {"w":"一度","a":"一次、一回","q":"有限的岁月只能一度为你所有"},
    {"w":"无能为力","a":"用不上力量，指没有办法","q":"智者对此也无能为力"},
    {"w":"洗涤","a":"清洗","q":"就可以脱下它来洗涤"},
    {"w":"不朽","a":"永不磨灭、永存","q":"生命流动着，永远不朽"},
    {"w":"卑微","a":"地位低下、渺小","q":"它们是那样卑微"},
    {"w":"小牛犊","a":"小牛","q":"山坡上那些小牛犊"},
    {"w":"炫耀","a":"夸耀、展示","q":"炫耀它们遍身金黄的茸毛"},
    {"w":"茸毛","a":"细软的毛","q":"遍身金黄的茸毛"},
    {"w":"暂时","a":"短时间之内","q":"它分开来是暂时"},
    {"w":"疲倦","a":"疲乏、困倦","q":"它是一个不懂疲倦的旅客"},
    {"w":"消逝","a":"消失、逝去","q":"那些个体消逝了"},
    {"w":"永不休止","a":"永远不停止","q":"永不休止地繁殖着"},
    {"w":"蔓延","a":"像蔓草一样向周围扩展","q":"蔓延着"},
    {"w":"宣示","a":"公开表示、显示","q":"随处宣示它的快乐和威势"},
    {"w":"威势","a":"威力和气势","q":"随处宣示它的快乐和威势"},
    {"w":"舒畅","a":"开朗愉快、舒服痛快","q":"我们的心应该感到舒畅"},
    {"w":"暴君","a":"暴虐的君主","q":"那些暴君们能够杀害许多许多人"},
    {"w":"凋谢","a":"（草木花叶）脱落","q":"那些终于要凋谢的花朵里永存"},
    {"w":"芬芳","a":"香气、香味","q":"不断给世界以芬芳"},
]

# ===== 构建完整 HTML =====
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《永久的生命》严文井</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 严文井</div>
  <h1 class="hero-title">永久的生命</h1>
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
    <p>《永久的生命》是严文井写于1942年的一篇哲理散文，选自《严文井散文选》。文章以时间一去不返起笔，在感叹个人生命有限之后，笔锋一转，从小草、小牛犊等寻常物象中发现生命流动不息、永远不朽的奇迹，最终以“凋谢和不朽混为一体，这就是奇迹”收束，表达了对生命的礼赞与乐观信念。</p>
    <p>全文仅五百余字，却熔哲理、抒情、描写于一炉。语言朴素而富有诗意，议论中饱含情感，是中国现代哲理散文的名篇，与罗素《我为什么而活着》同编为统编版八年级上册第四单元“散文二篇”。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>严文井（1915—2005），原名严文锦，湖北武昌人，现代作家、儿童文学家。1935年开始发表作品，曾任《人民文学》主编、人民文学出版社社长等职。其散文以哲理深邃、语言清丽著称，代表作有《永久的生命》《论友情》《一个人的烦恼》等，童话有《唐小西在“下一次开船港”》《“下次开船”港》等。</p>
    <p style="margin-top:10px;color:var(--ink2)">严文井的散文善于从日常生活中提炼哲理，以小见大，在朴素的叙述中寄寓深刻的人生感悟。《永久的生命》写于抗战时期，在民族危亡的背景下，作者对生命的思考更显深沉与坚定。</p>
  </div>
  <div class="box">
    <h3>写作背景</h3>
    <p><b>抗战岁月：</b>1942年，抗日战争正处于艰苦的相持阶段。国土沦丧、生灵涂炭，个人生命在战争中显得格外脆弱。严文井此时思考生命的意义，既是对个体命运的感悟，也是对民族未来的信念。</p>
    <p style="margin-top:8px"><b>哲理思考：</b>文章从“过去了的时间永不再回来”的感叹出发，没有停留在悲观，而是从中外哲人的思考中汲取力量，看到生命整体的永恒。“那些暴君们能够杀害许多许多人，但是他们消灭不了生命”，正是对侵略者的有力回应。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>雅坤朗读《永久的生命》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1vv4y1v7K8&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="雅坤朗读《永久的生命》"></iframe>
        <a href="https://www.bilibili.com/video/BV1vv4y1v7K8" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>《散文二篇》之永久的生命 讲解</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1ZG4y1473e&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="散文二篇之永久的生命讲解"></iframe>
        <a href="https://www.bilibili.com/video/BV1ZG4y1473e" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 词语 · 手法</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{fulltext_html}  </div>
  <div class="verse-list" id="verseList">
{verse_html}  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">哲理 · 艺术 · 名句</span></div>

  <div class="box">
    <h3>哲理意蕴</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">个体有限，生命永恒</div>
        <p>文章的核心哲理是：个体的生命是短暂的、不可挽回的，“过去了的时间永不再回来”；但生命整体是流动的、不朽的，“它分开来是暂时，合起来却是永久”。小草经冬犹生、小牛犊年年欢跃，都是生命永恒的见证。个体如花朵终将凋谢，而生命在凋谢中永存——这就是“凋谢和不朽混为一体”的奇迹。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">反对悲观，赞美生命</div>
        <p>作者没有停留在对生命短暂的感叹上，而是明确提出“人们却不应该为此感到悲观。我们没有时间悲观”。在抗战的艰苦岁月里，这种乐观不是盲目的，而是建立在对生命本质的深刻认识之上——暴君可以杀人，却消灭不了生命。对生命的赞美，也是对民族生命力的信念。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">欲扬先抑，层层推进</div>
        <p>首段极写生命的有限与可悲，“我们都非常可怜”，基调低沉；第二段以“却”字转折，从悲观转向对生命神奇的发现；第三段揭示生命永恒的哲理；第四段呼吁赞美生命；第五段以一句话收束。情感由抑到扬，哲理由浅入深，结构精巧。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">以小见大，意象鲜活</div>
        <p>小草“从土壤里钻出来”、小牛犊“跳跳蹦蹦，炫耀它们遍身金黄的茸毛”，都是极寻常的物象，作者却从中发现了生命永恒的哲理。“钻”“迎”“跳跳蹦蹦”“炫耀”等动词和拟人手法，让画面充满生机，哲理不再抽象。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">比喻生动，语言诗化</div>
        <p>“个人生命不像一件衬衣”，通俗的比喻写生命不可修补；“它是一个不懂疲倦的旅客”，将抽象的生命人格化，写其在个体间流转不息。语言朴素而富有诗意，议论中饱含情感，读来如散文诗。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">首尾圆合，警句收束</div>
        <p>首段感叹时间不返，末段“凋谢和不朽混为一体，这就是奇迹”，以独句成段收束，简洁有力，余味无穷。“奇迹”一词与第三段“感谢生命的奇迹”呼应，全文结构圆合。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">它分开来是暂时，合起来却是永久。</div>
        <p>全文的核心哲思。“分开来”指个体生命，“合起来”指生命整体。个体有生有死，是暂时的；而生命如河流般在个体间传递，永不停息，是永久的。这句话以极简的语言道出了生命的辩证法，是理解全文的钥匙。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">它是一个不懂疲倦的旅客，总是只暂时在哪一个个体内住一会儿，便又离开前去。</div>
        <p>将生命比作“不懂疲倦的旅客”，生动地写出了生命在个体间流转不息的特点。“住一会儿”“离开前去”，拟人化的描写让抽象的哲理变得可感，也暗示了个体生命的短暂与生命整体的永恒。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">生命在那些终于要凋谢的花朵里永存，不断给世界以色彩，不断给世界以芬芳。</div>
        <p>“凋谢”与“永存”形成对比：花朵终将凋谢，但生命在凋谢中延续，持续给世界带来色彩与芬芳。色彩诉诸视觉，芬芳诉诸嗅觉，意象优美，情感深沉。这是对生命最深情的赞美。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">凋谢和不朽混为一体，这就是奇迹。</div>
        <p>独句成段，收束全文。“凋谢”是个体的死亡，“不朽”是生命的永恒，二者看似矛盾，实则统一——正是个体的不断凋谢，才成就了生命的不朽。这句话以悖论的形式道出了生命的本质，简洁而深刻，余味无穷。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《永久的生命》通过对时间流逝与生命有限的感叹，以及对小草、小牛犊等生命现象的观察，揭示了“个体生命短暂，生命整体永恒”的哲理，表达了对生命的礼赞和乐观坚定的人生信念。</p>
    <p style="margin-top:10px">文章写于抗战艰苦岁月，“那些暴君们能够杀害许多许多人，但是他们消灭不了生命”，将对生命的思考与民族命运联系在一起，使文章超越了一般的哲理散文，具有了深沉的时代意义。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 用字 · 修辞 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">臼齿</span><span class="acc-d">（jiù chǐ）磨牙，在口腔后方，用于研磨食物。</span></div>
      <div class="acc-item"><span class="acc-w">兴味</span><span class="acc-d">兴趣、兴致。</span></div>
      <div class="acc-item"><span class="acc-w">一度</span><span class="acc-d">一次、一回。文中指岁月只能拥有一次。</span></div>
      <div class="acc-item"><span class="acc-w">无能为力</span><span class="acc-d">用不上力量，指没有办法。</span></div>
      <div class="acc-item"><span class="acc-w">洗涤</span><span class="acc-d">（xǐ dí）清洗。</span></div>
      <div class="acc-item"><span class="acc-w">不朽</span><span class="acc-d">永不磨灭、永存。</span></div>
      <div class="acc-item"><span class="acc-w">卑微</span><span class="acc-d">地位低下、渺小。</span></div>
      <div class="acc-item"><span class="acc-w">小牛犊</span><span class="acc-d">（dú）小牛。</span></div>
      <div class="acc-item"><span class="acc-w">炫耀</span><span class="acc-d">夸耀、展示。</span></div>
      <div class="acc-item"><span class="acc-w">茸毛</span><span class="acc-d">（róng）细软的毛。</span></div>
      <div class="acc-item"><span class="acc-w">疲倦</span><span class="acc-d">疲乏、困倦。</span></div>
      <div class="acc-item"><span class="acc-w">消逝</span><span class="acc-d">消失、逝去。</span></div>
      <div class="acc-item"><span class="acc-w">蔓延</span><span class="acc-d">像蔓草一样向周围扩展。</span></div>
      <div class="acc-item"><span class="acc-w">宣示</span><span class="acc-d">公开表示、显示。</span></div>
      <div class="acc-item"><span class="acc-w">威势</span><span class="acc-d">威力和气势。</span></div>
      <div class="acc-item"><span class="acc-w">舒畅</span><span class="acc-d">开朗愉快、舒服痛快。</span></div>
      <div class="acc-item"><span class="acc-w">凋谢</span><span class="acc-d">（diāo）（草木花叶）脱落。</span></div>
      <div class="acc-item"><span class="acc-w">芬芳</span><span class="acc-d">香气、香味。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">臼齿</span><span class="acc-d">（jiù）不要读成“jiù”以外的音；注意与“舅”区分。</span></div>
      <div class="acc-item"><span class="acc-w">盲肠</span><span class="acc-d">（máng）目字旁；与“肓”（huāng，病入膏肓，月字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">洗涤</span><span class="acc-d">（dí）三点水，清洗；不要写成“条”。</span></div>
      <div class="acc-item"><span class="acc-w">不朽</span><span class="acc-d">（xiǔ）木字旁，腐烂；不要写成“巧”。</span></div>
      <div class="acc-item"><span class="acc-w">卑微</span><span class="acc-d">（bēi）十字头，低下。</span></div>
      <div class="acc-item"><span class="acc-w">牛犊</span><span class="acc-d">（dú）牛字旁，小牛；与“渎”“牍”区分。</span></div>
      <div class="acc-item"><span class="acc-w">茸毛</span><span class="acc-d">（róng）草字头；与“葺”（qì，修补）区分。</span></div>
      <div class="acc-item"><span class="acc-w">凋谢</span><span class="acc-d">（diāo）两点水；与“雕”（隹字旁）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞方法</h3>
      <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">“个人生命不像一件衬衣”，以衬衣可洗可补反衬生命不可修补；“它是一个不懂疲倦的旅客”，将生命比作旅客，写其流转不息。</span></div>
      <div class="acc-item"><span class="acc-w">拟人</span><span class="acc-d">小草“欢乐地迎着春天的风”，小牛犊“炫耀它们遍身金黄的茸毛”，赋予自然物以人的情态，写生命的蓬勃。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">首段的衰老可悲与第二段的生机盎然对比；“凋谢”与“不朽”对比，在对比中揭示生命的哲理。</span></div>
      <div class="acc-item"><span class="acc-w">反复</span><span class="acc-d">“永远的小牛犊，永远的金黄色茸毛”，两个“永远的”反复，强调生命的永恒；“不断给世界以色彩，不断给世界以芬芳”，两个“不断”反复，写生命的持续奉献。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">欲扬先抑</span><span class="acc-d">先写生命的有限可悲，再写生命的永恒可敬，情感由抑到扬，哲理在转折中显现。</span></div>
      <div class="acc-item"><span class="acc-w">以小见大</span><span class="acc-d">从小草、小牛犊等寻常物象中发现生命永恒的哲理，选材小而开掘深。</span></div>
      <div class="acc-item"><span class="acc-w">哲理与抒情结合</span><span class="acc-d">议论中饱含情感，不是空洞的说教，而是以形象和情感承载哲理，读来如散文诗。</span></div>
      <div class="acc-item"><span class="acc-w">警句收束</span><span class="acc-d">以“凋谢和不朽混为一体，这就是奇迹”独句成段收束，简洁有力，余味无穷。</span></div>
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
  <div class="kai">《永久的生命》</div>
  <div>严文井 · 现代 · 出自《严文井散文选》</div>
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
