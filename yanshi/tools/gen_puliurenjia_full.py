# -*- coding: utf-8 -*-
"""补充脚本：读取gen_puliurenjia.py的VERSES数据，生成完整HTML"""
import json, re, html as htmlmod, io, os, sys

# 执行原脚本获取VERSES数据
exec(open(r'D:\App\Apps\yanshi\tools\gen_puliurenjia.py', encoding='utf-8').read())

LQ = "\u201c"
RQ = "\u201d"
def Q(s):
    return s.replace("_LQ_", LQ).replace("_RQ_", RQ)

TEMPLATE = r"D:\App\Apps\yanshi\kongyiji-luxun.html"
OUT = r"D:\App\Apps\yanshi\puliurenjia-liushaotang.html"

# ---------- 字形题库 ----------
DICT_WORDS = [
    {"w":"晌","py":"shǎng","q":"中伏大□午","tip":"「晌」日字旁，中午，音 shǎng；与「响」（口字旁）区分"},
    {"w":"囱","py":"cōng","q":"刚从烟□里爬出来","tip":"「囱」独体字，烟囱，音 cōng；与「窗」（穴宝盖）区分"},
    {"w":"兜","py":"dōu","q":"大红□肚","tip":"「兜」儿字底，口袋，音 dōu；与「篼」（竹字头）区分"},
    {"w":"痱","py":"fèi","q":"起大半身□子","tip":"「痱」病字旁，痱子，音 fèi；与「诽」（言字旁）「绯」（绞丝旁）区分"},
    {"w":"臊","py":"sào","q":"□得他找个田鼠窝","tip":"「臊」月字旁，害羞，音 sào；与「操」（提手旁）「燥」（火字旁）区分"},
    {"w":"擀","py":"gǎn","q":"手握着□面杖","tip":"「擀」提手旁，碾压，音 gǎn；与「赶」（走之旁）区分"},
    {"w":"梆","py":"bāng","q":"要□他","tip":"「梆」木字旁，用棍子打，音 bāng；与「帮」（巾字旁）区分"},
    {"w":"阎","py":"yán","q":"□王爷","tip":"「阎」门字旁，姓氏，音 yán；与「闫」（三字旁）「谚」（言字旁）区分"},
    {"w":"呵","py":"hē","q":"一气□成","tip":"「呵」口字旁，呼气，音 hē；与「何」（单人旁）「河」（三点水）区分"},
    {"w":"纤","py":"qiàn","q":"几个□夫","tip":"「纤」绞丝旁，拉船绳，音 qiàn；又读 xiān（纤维）。与「阡」（左耳旁）区分"},
    {"w":"戳","py":"chuō","q":"手□着他们的鼻子","tip":"「戳」戈字旁，用尖端触，音 chuō；与「戮」（lù，杀戮）区分"},
    {"w":"楞","py":"léng","q":"是个生□儿","tip":"「楞」木字旁，鲁莽，音 léng；与「愣」（竖心旁）区分"},
    {"w":"抡","py":"lūn","q":"□圆了扇过去","tip":"「抡」提手旁，用力挥动，音 lūn；又读 lún（选择）。与「抢」（qiǎng）区分"},
    {"w":"捯","py":"dáo","q":"紧一口慢一口□气","tip":"「捯」提手旁，急促呼吸，音 dáo；与「倒」（dǎo/dào）区分"},
    {"w":"绽","py":"zhàn","q":"□裂了虎口","tip":"「绽」绞丝旁，裂开，音 zhàn；与「淀」（diàn，淀粉）「锭」（dìng）区分"},
    {"w":"驭","py":"yù","q":"驾□不住","tip":"「驭」马字旁，驾驶，音 yù；与「御」（彳旁）区分"},
    {"w":"茧","py":"jiǎn","q":"长满老□","tip":"「茧」草字头，硬皮，音 jiǎn；与「简」（竹字头）「俭」（单人旁）区分"},
    {"w":"呱呱","py":"gū gū","q":"□□坠地","tip":"「呱」口字旁，婴儿哭声，音 gū；又读 guā（呱呱叫）。与「瓜」区分"},
    {"w":"熏","py":"xūn","q":"□陶得一身书香","tip":"「熏」四点底，长期影响，音 xūn；与「薰」（草字头）「醺」（酉字旁）区分"},
    {"w":"匿","py":"nì","q":"□隐在柳棵子地里","tip":"「匿」半包围结构，隐藏，音 nì；与「溺」（三点水，nì）区分"},
    {"w":"苇","py":"wěi","q":"芦□丛中","tip":"「苇」草字头，芦苇，音 wěi；与「伟」（单人旁）「纬」（绞丝旁）区分"},
    {"w":"潜","py":"qián","q":"□伏在青纱帐内","tip":"「潜」三点水，隐藏，音 qián；与「浅」（qiǎn）「惨」（cǎn）区分"},
    {"w":"嘟","py":"dū","q":"□哝那个","tip":"「嘟」口字旁，嘟囔，音 dū；与「都」（dōu/dū）区分"},
    {"w":"勒","py":"lè","q":"□令他写一百个字","tip":"「勒」力字旁，强制，音 lè；又读 lēi（勒紧）。与「勤」（qín）区分"},
    {"w":"谑","py":"xuè","q":"一半是戏□","tip":"「谑」言字旁，开玩笑，音 xuè；与「虐」（nüè，虐待）区分"},
    {"w":"膺","py":"yīng","q":"荣□这个尊称","tip":"「膺」月字旁，承受，音 yīng；与「鹰」（鸟字旁）「赝」（yàn，赝品）区分"},
    {"w":"坍","py":"tān","q":"□塌破败","tip":"「坍」提土旁，倒塌，音 tān；与「贪」（贝字旁）「摊」（提手旁）区分"},
    {"w":"垣","py":"yuán","q":"断壁残□","tip":"「垣」提土旁，墙，音 yuán；与「恒」（héng）「桓」（huán，盘桓）区分"},
    {"w":"蒿","py":"hāo","q":"蓬□荆棘","tip":"「蒿」草字头，野草，音 hāo；与「篙」（gāo，竹篙）「嵩」（sōng，嵩山）区分"},
    {"w":"棘","py":"jí","q":"荆□之中","tip":"「棘」左右结构，带刺灌木，音 jí；与「刺」（cì，刺刀）区分"},
    {"w":"掂","py":"diān","q":"□量一下自己","tip":"「掂」提手旁，斟酌，音 diān；与「惦」（竖心旁，diàn）「踮」（足字旁，diǎn）区分"},
    {"w":"塾","py":"shú","q":"念了三年私□","tip":"「塾」土字底，私人学校，音 shú；与「熟」（shú，熟悉）区分"},
    {"w":"毡","py":"zhān","q":"如坐针□","tip":"「毡」毛字旁，毡子，音 zhān；与「毯」（tǎn）「粘」（zhān）区分"},
    {"w":"啭","py":"zhuàn","q":"莺啼燕□","tip":"「啭」口字旁，婉转鸣叫，音 zhuàn；与「转」（zhuǎn/zhuàn）区分"},
    {"w":"嘬","py":"zuō","q":"□着嘴唇学鸟叫","tip":"「嘬」口字旁，撅起，音 zuō；又读 chuài（咬）。与「撮」（cuō）区分"},
    {"w":"剜","py":"wān","q":"一块一块□肉","tip":"「剜」立刀旁，用刀挖，音 wān；与「婉」（wǎn）「腕」（wàn）区分"},
    {"w":"腻","py":"nì","q":"□歪了老秀才","tip":"「腻」月字旁，厌烦，音 nì；与「贰」（èr）区分"},
    {"w":"忿忿","py":"fèn fèn","q":"□□而去","tip":"「忿」心字底，愤怒，音 fèn；与「愤」（竖心旁）「纷」（绞丝旁）区分"},
    {"w":"檎","py":"qín","q":"周□","tip":"「檎」木字旁，人名用字，音 qín；与「禽」（qín）「擒」（提手旁）区分"},
    {"w":"茬","py":"chá","q":"满脸胡□","tip":"「茬」草字头，胡子茬，音 chá；与「在」（zài）「荐」（jiàn）区分"},
    {"w":"噘","py":"juē","q":"小嘴□得能挂个油瓶儿","tip":"「噘」口字旁，翘起，音 juē；与「撅」（提手旁）区分"},
    {"w":"殷","py":"yīn","q":"□汝耕","tip":"「殷」左右结构，姓氏，音 yīn；又读 yān（殷红）。右部是「殳」"},
]

# ---------- 注释题库（从VERSES提取） ----------
DICT_NOTES = []
for part in VERSES:
    for item in part[4]:
        for w, a in item[4]:
            if w and a and len(w) <= 6 and not any(x in a for x in ['逗号','句号','问号','感叹','标点']):
                DICT_NOTES.append({"w": w, "a": a, "q": item[1][:50]})
_seen = set()
_DN = []
for x in DICT_NOTES:
    key = x["w"] + "|" + x["a"][:20]
    if key not in _seen:
        _seen.add(key)
        _DN.append(x)
DICT_NOTES = _DN[:150]

# ---------- 生成函数 ----------
def annotate(text):
    def rep(m):
        w, n = m.group(1), m.group(2)
        return '<span class="anno-word" data-note="%s">%s</span>' % (htmlmod.escape(n, quote=True), w)
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', rep, text)

def build_verses():
    out = []
    idx = 0
    for part_title, part_name, part_range, part_sum, items in VERSES:
        out.append('    <div class="part-head">')
        out.append('      <span class="p-num">%s</span>' % part_title)
        out.append('      <h3>%s</h3>' % part_name)
        out.append('      <span class="range">%s</span>' % part_range)
        out.append('    </div>')
        out.append('    <div class="part-sum">%s</div>' % Q(part_sum))
        for no, txt, yi, shang, zhushi in items:
            idx += 1
            out.append('      <div class="verse" id="l%d" data-i="%d">' % (idx, idx))
            out.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (idx, annotate(Q(txt))))
            out.append('        <details class="v-more">')
            out.append('          <summary>内容 · 手法</summary>')
            out.append('          <div class="d-body">')
            out.append('            <div class="v-sec"><b class="v-label">内容概括</b>')
            out.append('              <div class="v-trans">%s</div>' % Q(yi))
            out.append('            </div>')
            out.append('            <div class="v-sec"><b class="v-label">手法分析</b>')
            out.append('              <div class="d-body"><p>%s</p></div>' % Q(shang))
            out.append('            </div>')
            out.append('          </div>')
            out.append('        </details>')
            out.append('      </div>')
    return '\n'.join(out)

verses_html = build_verses()
full_lines = []
for part in VERSES:
    for item in part[4]:
        full_lines.append(item[1])
full_html = '\n'.join('      <p class="pl">%s</p>' % Q(p) for p in full_lines)

# 提取CSS和JS
src = open(TEMPLATE, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
# 注入acc-sub样式（积累区小标题）
css += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:16px 0 8px;color:#8b6914;font-size:1.05em;}\n'
mains = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = mains[0]
main_js = main_js.replace("kongyiji_fs", "puliurenjia_fs")

BG = Q(u'''
  <section id="bg" class="sec">
    <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
    <div class="lead">
      _LQ_蒲柳人家_RQ_即普通穷苦农家。小说以二十世纪三十年代京东北运河畔的农村为背景，通过六岁孩童何满子的视角，刻画了一丈青大娘、何大学问等淳朴豪爽的农民形象，展现了浓郁的乡土气息和淳厚的人情美。
    </div>
    <div class="box">
      <h3>作者简介</h3>
      <p><b>刘绍棠</b>（1936—1997），北京通州人，当代著名乡土文学作家，被誉为_LQ_神童作家_RQ_。他十三岁开始发表作品，二十岁加入中国作家协会。他一生致力于_LQ_中国气派，民族风格，地方特色，乡土题材_RQ_的创作，是_LQ_大运河乡土文学体系_RQ_的创立者。</p>
      <p>代表作有中篇小说《蒲柳人家》《运河的桨声》《瓜棚柳巷》，长篇小说《春草》《地火》《狼烟》等。</p>
    </div>
    <div class="box">
      <h3>创作背景</h3>
      <p>二十世纪三十年代，日本帝国主义加紧侵华。1931年_LQ_九一八_RQ_事变后东三省沦陷，1935年_LQ_华北事变_RQ_后，殷汝耕在通州成立伪_LQ_冀东防共自治政府_RQ_。何大学问赶马出入古北口，正处在这一动荡的前沿。</p>
      <p>课文节选的故事发生在1936年的北运河畔。刘绍棠生于京东北运河畔的农村，他说：_LQ_我一直把我的创作看作是对故乡土地和人民的回报。_RQ_</p>
    </div>
    <div class="box media-box">
      <h3>朗诵 · 讲解</h3>
      <div class="media-grid">
        <div class="media">
          <h4>课文朗读《蒲柳人家》</h4>
          <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1ae411p7LG&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文朗读"></iframe>
          <a href="https://www.bilibili.com/video/BV1ae411p7LG" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
        </div>
        <div class="media">
          <h4>课文讲解《蒲柳人家》</h4>
          <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1Vb4y1J7i8&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文讲解"></iframe>
          <a href="https://www.bilibili.com/video/BV1Vb4y1J7i8" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
        </div>
      </div>
    </div>
  </section>
''')

APP = Q(u'''
  <section id="app" class="sec">
    <div class="sec-head"><h2>赏 析</h2><span class="no">人物 · 手法 · 艺术 · 主题</span></div>
    <div class="box">
      <h3>人物形象</h3>
      <p><b>一丈青大娘</b>：泼辣豪爽、能干勤劳、溺爱孙子。她大高个儿、大脚、青铜肤色，骂人方圆二三十里无敌手，打架三五个小伙子不够她打一锅的。她种地、撑船、打鱼都是行家，还会扎针、接生、接骨。</p>
      <p><b>何大学问</b>：仗义疏财、慷慨大方、虚荣心强、期望孙子成才。他外号_LQ_何大学问_RQ_，不是真有学问，而是阅历丰富、好说大话。被尊称后真的看起书来，穿长衫、咬文嚼字，既威风凛凛又滑稽可笑。</p>
      <p><b>何满子</b>：顽皮聪明、天真可爱、热爱自由。他六岁，剃光葫芦头，整天在运河滩野跑，跟奶奶捉迷藏。他聪慧灵秀，过耳不忘、过目不忘。</p>
    </div>
    <div class="box">
      <h3>艺术特色</h3>
      <p><b>① 儿童视角</b>：以六岁孩童何满子的视角展开叙事，既写出乡土生活的淳朴美好，又通过孩子的眼睛观察成人世界，生动有趣。</p>
      <p><b>② 倒叙结构</b>：以_LQ_何满子被爷爷拴在葡萄架上_RQ_开篇，设置悬念，然后追述原因，最后揭示真相，结构精巧。</p>
      <p><b>③ 语言乡土气息浓郁</b>：大量使用北方农村的口语、俗语、歇后语，生动形象，富有地方特色。</p>
      <p><b>④ 夸张与幽默</b>：一丈青大娘打纤夫_LQ_像正月十五煮元宵，纷纷落水_RQ_，夸张中见幽默，人物形象鲜明。</p>
      <p><b>⑤ 风俗画般的描写</b>：花红兜肚、洗三、满月、百家衣、长命锁等民俗描写，展现浓郁的乡土风情。</p>
    </div>
    <div class="box">
      <h3>主题思想</h3>
      <p>小说通过刻画一丈青大娘、何大学问等普通农民形象，歌颂了北运河畔农民的淳朴豪爽、多情重义的美好品质，展现了浓郁的乡土气息和淳厚的人情美。同时通过何大学问被蒙疆军扣押坐牢的情节，将个人命运与民族危机联系起来，暗含对日寇侵华的控诉。</p>
    </div>
  </section>
''')

ACC = Q(u'''
  <section id="acc" class="sec">
    <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 字音形 · 修辞 · 写作 · 文化常识</span></div>
    <div class="box"><div class="acc-cat">
        <h3>重点词语</h3>
        <div class="acc-item"><span class="acc-w">一丈青大娘</span><span class="acc-d">何满子奶奶的外号。一丈青本是《水浒传》中扈三娘的绰号，形容女子泼辣好强。</span></div>
        <div class="acc-item"><span class="acc-w">何大学问</span><span class="acc-d">何满子爷爷的外号，带有戏谑和尊敬的意味。</span></div>
        <div class="acc-item"><span class="acc-w">蒲柳人家</span><span class="acc-d">普通穷苦农家。蒲草柔弱，比喻底层寻常百姓。</span></div>
        <div class="acc-item"><span class="acc-w">一气呵成</span><span class="acc-d">一口气做成，形容文章或说话紧凑连贯。</span></div>
        <div class="acc-item"><span class="acc-w">妙手回春</span><span class="acc-d">称赞医生医术高明，能把垂危的病人治好。</span></div>
        <div class="acc-item"><span class="acc-w">如坐针毡</span><span class="acc-d">像坐在插着针的毡子上，形容心神不定、坐立不安。</span></div>
        <div class="acc-item"><span class="acc-w">芒刺在背</span><span class="acc-d">像芒和刺扎在背上，形容内心惶恐、坐立不安。</span></div>
        <div class="acc-item"><span class="acc-w">望眼欲穿</span><span class="acc-d">眼睛都要望穿了，形容盼望殷切。</span></div>
        <div class="acc-item"><span class="acc-w">天怒人怨</span><span class="acc-d">上天发怒、人民怨恨，形容作恶多端引起普遍愤怒。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>用字与读音</h3>
        <div class="acc-item"><span class="acc-w">晌 shǎng</span><span class="acc-d">日字旁，中午。勿写成「响」。</span></div>
        <div class="acc-item"><span class="acc-w">纤 qiàn</span><span class="acc-d">绞丝旁，拉船绳。又读 xiān（纤维）。</span></div>
        <div class="acc-item"><span class="acc-w">戳 chuō</span><span class="acc-d">戈字旁，用尖端触。与「戮」（lù）区分。</span></div>
        <div class="acc-item"><span class="acc-w">绽 zhàn</span><span class="acc-d">绞丝旁，裂开。与「淀」（diàn）区分。</span></div>
        <div class="acc-item"><span class="acc-w">匿 nì</span><span class="acc-d">半包围结构，隐藏。与「溺」（nì）区分。</span></div>
        <div class="acc-item"><span class="acc-w">膺 yīng</span><span class="acc-d">月字旁，承受。与「鹰」「赝」（yàn）区分。</span></div>
        <div class="acc-item"><span class="acc-w">垣 yuán</span><span class="acc-d">提土旁，墙。与「恒」（héng）「桓」（huán）区分。</span></div>
        <div class="acc-item"><span class="acc-w">毡 zhān</span><span class="acc-d">毛字旁，毡子。与「毯」「粘」区分。</span></div>
        <div class="acc-item"><span class="acc-w">剜 wān</span><span class="acc-d">立刀旁，用刀挖。与「婉」「腕」区分。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>修辞方法</h3>
        <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">骂人像雨打芭蕉、被打像风吹乍蓬、纤夫落水像正月十五煮元宵。</span></div>
        <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">三五个大小伙子不够她打一锅的、全村三十岁以下的人都是她接生的。</span></div>
        <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">心尖子，肺叶子，眼珠子，命根子／怕让狗咬了，怕让鹰抓了……</span></div>
        <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">一丈青大娘的泼辣与对孙子的溺爱、何大学问的威风与滑稽。</span></div>
        <div class="acc-item"><span class="acc-w">用典</span><span class="acc-d">一丈青（水浒扈三娘）、三顾茅庐（刘备请诸葛亮）。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>写作借鉴</h3>
        <div class="acc-sub">人物形象刻画</div>
        <div class="acc-item"><span class="acc-w">外貌描写</span><span class="acc-d">一丈青大娘「大高个儿，一双大脚，青铜肤色」，白描手法勾勒人物。</span></div>
        <div class="acc-item"><span class="acc-w">动作描写</span><span class="acc-d">「挽了挽袖口」「手戳着鼻子」「抡圆了扇过去」，动作连贯写性格。</span></div>
        <div class="acc-item"><span class="acc-w">语言描写</span><span class="acc-d">一丈青大娘的骂人话、何大学问的吹牛话，人物语言个性化。</span></div>
        <div class="acc-sub">叙事技巧</div>
        <div class="acc-item"><span class="acc-w">倒叙开篇</span><span class="acc-d">以何满子被拴开篇，设置悬念，追述原因，揭示真相。</span></div>
        <div class="acc-item"><span class="acc-w">儿童视角</span><span class="acc-d">以六岁孩童视角叙事，生动有趣，充满童真。</span></div>
        <div class="acc-item"><span class="acc-w">插叙手法</span><span class="acc-d">插叙何家的家事，交代人物关系和背景。</span></div>
      </div></div>
    <div class="box"><div class="acc-cat">
        <h3>文化常识</h3>
        <div class="acc-item"><span class="acc-w">北运河</span><span class="acc-d">京杭大运河的北段，在今北京、天津一带。</span></div>
        <div class="acc-item"><span class="acc-w">古北口</span><span class="acc-d">长城上的重要关口，在今北京市密云区。</span></div>
        <div class="acc-item"><span class="acc-w">洗三</span><span class="acc-d">婴儿出生第三天洗澡的习俗。</span></div>
        <div class="acc-item"><span class="acc-w">百家衣</span><span class="acc-d">用从各家讨来的零碎布缝成的婴儿衣服，认为能保长命百岁。</span></div>
        <div class="acc-item"><span class="acc-w">长命锁</span><span class="acc-d">挂在儿童脖子上的锁形饰物，迷信认为能保长命百岁。</span></div>
        <div class="acc-item"><span class="acc-w">义和团</span><span class="acc-d">清末活跃于北方的民间反帝爱国组织。</span></div>
      </div></div>
  </section>
''')

HTML = u'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《蒲柳人家》</title>
<meta name="description" content="刘绍棠《蒲柳人家》教学课件：逐段解读、词语积累、全屏听写练习。">
<style>
%(css)s
</style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <div class="hero-side">现代 · 刘绍棠</div>
      <h1 class="hero-title">蒲柳人家</h1>
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
    <div class="sec-head"><h2>解 读</h2><span class="no">逐段解读 · 内容 · 手法</span></div>
    <div class="sec-sub">原文中带下划线的词可点击查看注释。可切换<b>背诵模式</b>（仅显示每句首字，点击任意句可显示/隐藏该句）。</div>
    <div class="texttools">
      <button id="btnShowAll" class="tbtn" style="display:none">显示全部</button>
    </div>
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
      <button data-mode="note" data-rand="5">随机五组词语</button>
      <button data-mode="note" data-all="1">全部词语</button>
    </div>
  </section>
<footer>
  <div class="kai">《蒲柳人家》</div>
  <div>刘绍棠 · 现代 · 出自《十月》1980年第2期</div>
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
%(js)s
</script>
<script>
var DICT_WORDS = %(words)s;
var DICT_NOTES = %(notes)s;
</script>
</body>
</html>
''' % {
    'css': css,
    'js': main_js,
    'bg': BG,
    'app': APP,
    'acc': ACC,
    'fulltext': full_html,
    'verses': verses_html,
    'words': json.dumps(DICT_WORDS, ensure_ascii=False),
    'notes': json.dumps(DICT_NOTES, ensure_ascii=False),
}

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(HTML)
print('Generated:', OUT)
print('Size:', os.path.getsize(OUT), 'bytes')
print('Verse count:', len(full_lines))
print('Dict words:', len(DICT_WORDS))
print('Dict notes:', len(DICT_NOTES))
