# -*- coding: utf-8 -*-
"""生成《祖国啊，我亲爱的祖国》课件 HTML（现代诗歌，琵琶行框架）"""
import re, json, html, sys
sys.path.insert(0, r"D:\App\Apps")
from data_zuguoawoqinaidezuguoo import PARTS, DICT_WORDS, DICT_NOTES

OUT = r"D:\App\Apps\zuguoawoqinaidezuguo-shuting.html"
TEMPLATE = r"D:\App\Apps\kongyiji-luxun.html"

with open(TEMPLATE, encoding="utf-8") as f:
    tpl = f.read()

style_block = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
style_block += """
  .acc-sub{font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:10px 0 6px;color:var(--teal-deep)}
"""
script_block = re.search(r"<script>(.*?)</script>", tpl, re.S).group(1)
script_block = script_block.replace("kongyiji_fs", "zuguoawoqinaidezuguo_fs")

def fix_quotes(text):
    """将文本中的ASCII " 替换为交替的中文引号"""
    result = []
    is_left = True
    for ch in text:
        if ch == '"':
            result.append('\u201c' if is_left else '\u201d')
            is_left = not is_left
        else:
            result.append(ch)
    return ''.join(result)

# 修复所有正文中的引号
for part in PARTS:
    for i, verse in enumerate(part["verses"]):
        orig, trans, analysis, notes = verse
        orig = fix_quotes(orig)
        trans = fix_quotes(trans)
        analysis = fix_quotes(analysis)
        part["verses"][i] = (orig, trans, analysis, notes)

def annotate(text, notes):
    notes_sorted = sorted(notes, key=lambda x: len(x[0]), reverse=True)
    result = text
    used = set()
    for word, note in notes_sorted:
        if word in used:
            continue
        idx = 0
        while True:
            pos = result.find(word, idx)
            if pos == -1:
                break
            before = result[:pos]
            if before.count('<span class="anno-word"') > before.count('</span>'):
                idx = pos + len(word)
                continue
            span = '<span class="anno-word" data-note="' + html.escape(note, quote=True) + '">' + word + '</span>'
            result = result[:pos] + span + result[pos+len(word):]
            idx = pos + len(span)
            used.add(word)
    return result

def build_verses():
    parts = []
    gidx = 0
    cn_nums = ["一", "二", "三", "四", "五", "六"]
    for pi, part in enumerate(PARTS):
        parts.append('      <div class="part-head"><span class="p-num">第' + cn_nums[pi] + '部分</span><h3>' + part["title"] + '</h3><span class="range">' + part["range"] + '</span></div>')
        parts.append('      <div class="part-overview">' + part["overview"] + '</div>')
        for orig, trans, analysis, notes in part["verses"]:
            gidx += 1
            annotated = annotate(orig, notes)
            parts.append('      <div class="verse" id="l' + str(gidx) + '" data-i="' + str(gidx-1) + '">')
            parts.append('        <div class="v-top"><span class="v-no">' + str(gidx) + '</span><div class="v-line">' + annotated + '</div></div>')
            parts.append('        <details class="v-more">')
            parts.append('          <summary>\u8bd1\u6587 \u00b7 \u8d4f\u6790</summary>')
            parts.append('          <div class="d-body">')
            parts.append('            <div class="v-sec"><b class="v-label">\u8bd1\u6587</b>')
            parts.append('              <div class="v-trans">' + trans + '</div>')
            parts.append('            </div>')
            parts.append('            <div class="v-sec"><b class="v-label">\u8d4f\u6790</b>')
            parts.append('              <div class="d-body"><p>' + analysis + '</p></div>')
            parts.append('            </div>')
            parts.append('          </div>')
            parts.append('        </details>')
            parts.append('      </div>')
    return "\n".join(parts)

def build_fulltext():
    """诗歌全文：按诗节分组，行之间用<br>"""
    lines = []
    for part in PARTS:
        stanza_lines = []
        for orig, _, _, _ in part["verses"]:
            stanza_lines.append(orig)
        # 每个诗节一个pl div，行之间<br>
        lines.append('    <div class="pl">' + "<br>".join(stanza_lines) + '</div>')
    return "\n".join(lines)

BG = '''  <div class=“lead”>
    <p>《祖国啊，我亲爱的祖国》是朦胧诗派代表诗人舒婷的代表作，发表于1979年《诗刊》。诗歌以“我”与祖国融为一体的独特视角，通过一系列新颖而凝重的意象，描绘了祖国数百年来的苦难、新生和希望，表达了诗人对祖国深沉的挚爱和为之献身的决心。</p>
    <p>全诗共四节，情感层层递进：第一节写祖国的贫穷与苦难，第二节写人民痛苦的希望，第三节写祖国的新生与曙光，第四节写诗人的献身誓言。从“破旧的老水车”到“绯红的黎明”，从“迷惘的我”到“沸腾的我”，诗歌在沉郁与昂扬之间完成了对祖国命运的深情咏叹。</p>
  </div>
  <div class=“box”>
    <h3>作者简介</h3>
    <p>舒婷，1952年生，原名龚佩瑜，福建泉州人，中国当代著名女诗人，朦胧诗派的代表人物。1969年下乡插队，1972年返城当工人，1979年开始发表诗歌作品。主要作品有诗集《双桅船》《会唱歌的鸢尾花》《始祖鸟》等，散文集《心烟》等。</p>
    <p style=“margin-top:10px;color:var(--ink2)”>舒婷的诗歌善于从女性独特的视角出发，以细腻的情感、新颖的意象和含蓄的表达，探索个人与时代、自我与祖国的关系。她的诗既有对苦难的深沉反思，又有对理想的执着追求，是中国当代诗歌史上的重要篇章。</p>
  </div>
  <div class=“box”>
    <h3>时代背景</h3>
    <p>这首诗写于1979年，正值中国改革开放初期。经历了十年“文化大革命”的浩劫，国家百废待兴，人民在迷惘中思索、在痛苦中奋起。诗人以敏锐的感受力，捕捉到了时代转型期的复杂情感——既有对过去苦难的沉痛反思，又有对未来希望的热切憧憬。</p>
    <p style=“margin-top:8px”>诗歌中的“迷惘的我、深思的我、沸腾的我”，正是那一代青年的精神写照：他们经历了文革的迷茫，开始深刻思考国家的前途，最终满怀激情地投身到改革开放的建设洪流中。</p>
  </div>
  <div class=“box”>
    <h3>写作缘起</h3>
    <p>舒婷在谈到这首诗的创作时说，她想表达的是“我”与祖国的关系——“我”既是祖国的一部分，又是祖国的见证者和建设者。诗歌中的“我”不是一个人，而是一代青年的缩影。</p>
    <p style=“margin-top:8px”>诗人选择了“老水车”“矿灯”“稻穗”“路基”“驳船”等朴实而凝重的意象，避免了空洞的口号，以具体可感的形象承载深沉的情感，使这首政治抒情诗具有了打动人心的艺术力量。</p>
  </div>
  <div class=“box media-box”>
    <h3>视听</h3>
    <div class=“media-grid”>
      <div class=“media”>
        <h4>《祖国啊，我亲爱的祖国》朗诵：徐涛</h4>
        <iframe id=“mediaF1” src=“https://player.bilibili.com/player.html?bvid=BV1y24y1R7at&page=1&high_quality=1&danmaku=0&autoplay=0” loading=“lazy” scrolling=“no” frameborder=“0” allowfullscreen=“true” title=“祖国啊我亲爱的祖国朗诵徐涛”></iframe>
        <a href=“https://www.bilibili.com/video/BV1y24y1R7at” target=“_blank” rel=“noopener”>在 B 站打开原视频</a><button class=“fsbtn” data-target=“mediaF1”>全屏播放</button>
      </div>
      <div class=“media”>
        <h4>《祖国啊，我亲爱的祖国》示范课精品微课</h4>
        <iframe id=“mediaF2” src=“https://player.bilibili.com/player.html?bvid=BV1N84y1p77K&page=1&high_quality=1&danmaku=0&autoplay=0” loading=“lazy” scrolling=“no” frameborder=“0” allowfullscreen=“true” title=“祖国啊我亲爱的祖国示范课”></iframe>
        <a href=“https://www.bilibili.com/video/BV1N84y1p77K” target=“_blank” rel=“noopener”>在 B 站打开原视频</a><button class=“fsbtn” data-target=“mediaF2”>全屏播放</button>
      </div>
    </div>
  </div>'''

APP = '''  <div class=“box”>
    <h3>意象赏析</h3>
    <div class=“fame”>
      <div class=“fame-card”>
        <div class=“f-line”>破旧的老水车 \u2014\u2014 古老而疲惫的农业文明</div>
        <p>“老水车”象征中国古老的农业文明，“破旧”写尽沧桑。水车数百年来缓缓转动，纺着“疲惫的歌”，正如祖国在漫长历史中艰难前行。这个意象既写出了历史的悠久，也写出了发展的迟滞。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>熏黑的矿灯 \u2014\u2014 黑暗中摸索的工业文明</div>
        <p>“矿灯”象征工业生产，“熏黑”写尽矿工的艰辛。矿灯照人在“历史的隧洞里蜗行摸索”，将祖国百年探索的艰难历程浓缩在一个意象中——黑暗、缓慢、方向不明。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>干瘪的稻穗 / 失修的路基 / 淤滩上的驳船</div>
        <p>三个意象叠加，从农业到交通再到航运，全面展现祖国的贫穷落后。“干瘪”写歉收，“失修”写破败，“淤滩”写困境。纤绳“勒进肩膊”的画面，将苦难具象化，令人动容。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>飞天袖间未落的花朵 \u2014\u2014 痛苦的希望</div>
        <p>“飞天”是敦煌壁画中的美好形象，“袖间的花朵”象征人民千百年来的美好理想。但花朵“未落到地面”，意味着理想始终未能实现。这个意象美丽而哀伤，是“痛苦的希望”的具象化。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>雪被下古莲的胚芽 \u2014\u2014 顽强的新生</div>
        <p>“古莲”是千年古莲子，有极强的生命力，在冰雪下沉睡千年仍能发芽。这个意象象征祖国虽历经苦难，但生命力从未枯竭，正在萌发新的生机。古老与新生在这个意象中完美统一。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>绯红的黎明 / 雪白的起跑线 \u2014\u2014 光明的前景</div>
        <p>“绯红的黎明”色彩明丽，象征祖国的光明前景；“雪白的起跑线”象征新的开始，一切从零出发。两个意象充满动感和力量，与前两节的灰暗色调形成强烈对比，写出了祖国的新生。</p>
      </div>
    </div>
  </div>
  <div class=“box”>
    <h3>艺术特色</h3>
    <div class=“fame”>
      <div class=“fame-card”>
        <div class=“f-line”>意象群的精心构建</div>
        <p>全诗不以直白的抒情取胜，而以意象群的构建见长。每一节都围绕一个中心，组织一组相关意象：第一节是苦难意象群（老水车、矿灯、稻穗、路基、驳船），第三节是新生意象群（理想、胚芽、笑涡、起跑线、黎明）。意象新颖、凝重、具体可感，避免了空洞的口号。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>“我”与祖国的融合</div>
        <p>全诗以“我是你……”的句式贯穿始终，将“我”与祖国融为一体。“我”既是祖国的一部分（十亿分之一），又是祖国的见证者和建设者（九百六十万平方的总和）。这种独特的视角，使个人的命运与祖国的命运不可分割，增强了诗歌的感染力。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>情感的层层递进</div>
        <p>四节诗的情感呈递进结构：第一节沉郁（苦难），第二节深沉（痛苦的希望），第三节昂扬（新生），第四节热烈（献身）。从“破旧”到“簇新”，从“蜗行”到“喷薄”，从“迷惘”到“沸腾”，情感曲线清晰有力。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>对比手法的运用</div>
        <p>前两节的灰暗意象（破旧、熏黑、干瘪、失修、淤滩）与后两节的明丽意象（簇新、雪白、绯红）形成鲜明对比；“蜗行摸索”与“喷薄”的黎明形成对比；“迷惘的我”与“沸腾的我”形成对比。对比中见出祖国的巨变和诗人的情感转折。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>复沓咏叹的结构</div>
        <p>每一节末尾都以“——祖国啊！”的咏叹句结束，形成回环往复的旋律。前三节的“祖国啊”情感各不相同（悲悯、叹惋、振奋），最后一节升华为“祖国啊，我亲爱的祖国！”，与标题呼应，将情感推向高潮。</p>
      </div>
    </div>
  </div>
  <div class=“box”>
    <h3>主题思想</h3>
    <p>诗歌通过一系列凝重而新颖的意象，描绘了祖国数百年来的贫穷苦难和新时代的新生希望，表达了诗人对祖国深沉的挚爱，以及愿以血肉之躯换取祖国富饶、荣光、自由的献身精神。</p>
    <p style=“margin-top:10px”>这首诗的独特之处在于，它没有回避祖国的苦难和落后，而是以直面现实的勇气，写出了一个真实的、伤痕累累的祖国。但诗人没有停留在苦难的哀叹中，而是从苦难中看到了希望，从伤痕中看到了新生。“我是你簇新的理想”“是绯红的黎明正在喷薄”——诗人对祖国的未来充满信心。最后，诗人将个人与祖国融为一体，发出了“从我的血肉之躯上去取得你的富饶、你的荣光、你的自由”的誓言，使全诗的情感得到升华。</p>
  </div>'''

ACC = '''  <div class=“box”>
    <div class=“acc-cat”>
      <h3>文体与流派</h3>
      <div class=“acc-item”><span class=“acc-w”>朦胧诗</span><span class=“acc-d”>20世纪70年代末80年代初出现的诗歌流派，代表诗人有舒婷、北岛、顾城、江河等。特点是意象朦胧、含蓄多义、注重内心体验和自我表达。</span></div>
      <div class=“acc-item”><span class=“acc-w”>政治抒情诗</span><span class=“acc-d”>以政治题材和社会生活为内容的抒情诗。本诗以祖国为歌咏对象，但避免了空洞的口号，以具体意象承载情感。</span></div>
      <div class=“acc-item”><span class=“acc-w”>自由诗</span><span class=“acc-d”>不讲究格律和押韵的诗体，形式自由。本诗句式长短不一，节奏随情感变化，是典型的自由诗。</span></div>
      <div class=“acc-item”><span class=“acc-w”>意象群</span><span class=“acc-d”>一组相关意象的集合。本诗每一节都构建一个意象群，如苦难意象群、新生意象群。</span></div>
    </div>
  </div>
  <div class=“box”>
    <div class=“acc-cat”>
      <h3>易错字音形</h3>
      <div class=“acc-item”><span class=“acc-w”>惫</span><span class=“acc-d”>读 b\u00e8i，不读 b\u00ec。疲乏。疲惫。</span></div>
      <div class=“acc-item”><span class=“acc-w”>熏</span><span class=“acc-d”>读 x\u016bn，不读 x\u00f9n。烟气熏染。熏黑。</span></div>
      <div class=“acc-item”><span class=“acc-w”>隧</span><span class=“acc-d”>读 su\u00ec，不读 su\u00ed。隧道。隧洞。</span></div>
      <div class=“acc-item”><span class=“acc-w”>蜗</span><span class=“acc-d”>读 w\u014d，不读 w\u0101。蜗牛。蜗行。</span></div>
      <div class=“acc-item”><span class=“acc-w”>瘪</span><span class=“acc-d”>读 bi\u011b，不读 bi\u0113。不丰满。干瘪。</span></div>
      <div class=“acc-item”><span class=“acc-w”>淤</span><span class=“acc-d”>读 y\u016b，不读 y\u00fa。泥沙沉积。淤滩。</span></div>
      <div class=“acc-item”><span class=“acc-w”>驳</span><span class=“acc-d”>读 b\u00f3，不读 b\u01ceo。驳船。</span></div>
      <div class=“acc-item”><span class=“acc-w”>纤</span><span class=“acc-d”>多音字：纤绳 qi\u00e0n；纤维 xi\u0101n。文中读 qi\u00e0n。</span></div>
      <div class=“acc-item”><span class=“acc-w”>勒</span><span class=“acc-d”>多音字：勒进 l\u0113i（捆紧）；勒索 l\u00e8。文中读 l\u0113i。</span></div>
      <div class=“acc-item”><span class=“acc-w”>簇</span><span class=“acc-d”>读 c\u00f9，不读 z\u00fa。极新。簇新。</span></div>
      <div class=“acc-item”><span class=“acc-w”>胚</span><span class=“acc-d”>读 p\u0113i，不读 p\u012b。幼芽。胚芽。</span></div>
      <div class=“acc-item”><span class=“acc-w”>绯</span><span class=“acc-d”>读 f\u0113i，不读 f\u011bi。鲜红。绯红。</span></div>
      <div class=“acc-item”><span class=“acc-w”>惘</span><span class=“acc-d”>读 w\u01ceng，不读 m\u00e1ng。困惑。迷惘。</span></div>
      <div class=“acc-item”><span class=“acc-w”>饶</span><span class=“acc-d”>读 r\u00e1o，不读 y\u00e1o。富足。富饶。</span></div>
    </div>
  </div>
  <div class=“box”>
    <div class=“acc-cat”>
      <h3>文言梳理</h3>
      <div class=“acc-sub”>古今异义</div>
      <div class=“acc-item”><span class=“acc-w”>疲惫</span><span class=“acc-d”>古今同义，均指非常疲乏。</span></div>
      <div class=“acc-item”><span class=“acc-w”>迷惘</span><span class=“acc-d”>古今同义，均指困惑、不知所措。</span></div>
      <div class=“acc-sub”>一词多义</div>
      <div class=“acc-item”><span class=“acc-w”>薄</span><span class=“acc-d”>喷薄 b\u00f3（壮盛）；薄饼 b\u00e1o（厚度小）；薄荷 b\u00f2（植物名）。</span></div>
      <div class=“acc-item”><span class=“acc-w”>累</span><span class=“acc-d”>伤痕累累 l\u00e9i（接连成串）；劳累 l\u00e8i（疲劳）；积累 l\u011bi（堆积）。</span></div>
      <div class=“acc-sub”>词类活用</div>
      <div class=“acc-item”><span class=“acc-w”>蜗行</span><span class=“acc-d”>名词作状语，像蜗牛一样爬行。“照你在历史的隧洞里蜗行摸索”。</span></div>
    </div>
  </div>
  <div class=“box”>
    <div class=“acc-cat”>
      <h3>核心考点（意象与情感）</h3>
      <div class=“acc-item”><span class=“acc-w”>苦难意象群</span><span class=“acc-d”>老水车、矿灯、稻穗、路基、驳船、纤绳——象征祖国数百年来的贫穷落后和人民的深重苦难。</span></div>
      <div class=“acc-item”><span class=“acc-w”>希望意象</span><span class=“acc-d”>“飞天”袖间未落的花朵——象征人民千百年来的美好理想始终未能实现，是“痛苦的希望”。</span></div>
      <div class=“acc-item”><span class=“acc-w”>新生意象群</span><span class=“acc-d”>簇新的理想、古莲的胚芽、挂着眼泪的笑涡、雪白的起跑线、绯红的黎明——象征祖国在新时代的觉醒和希望。</span></div>
      <div class=“acc-item”><span class=“acc-w”>情感脉络</span><span class=“acc-d”>沉郁（苦难）\u2192深沉（痛苦的希望）\u2192昂扬（新生）\u2192热烈（献身），四节情感层层递进。</span></div>
      <div class=“acc-item”><span class=“acc-w”>“我”的含义</span><span class=“acc-d”>“我”既是诗人自己，也是一代青年的缩影，更是与祖国融为一体的共同体。“十亿分之一”与“九百六十万平方的总和”辩证统一。</span></div>
    </div>
  </div>
  <div class=“box”>
    <div class=“acc-cat”>
      <h3>修辞与手法</h3>
      <div class=“acc-item”><span class=“acc-w”>比喻</span><span class=“acc-d”>“我是你河边上破旧的老水车”等一系列“我是你……”的比喻，将“我”与祖国融为一体。</span></div>
      <div class=“acc-item”><span class=“acc-w”>排比</span><span class=“acc-d”>“我是干瘪的稻穗，是失修的路基，是淤滩上的驳船”；“迷惘的我、深思的我、沸腾的我”；“你的富饶、你的荣光、你的自由”。</span></div>
      <div class=“acc-item”><span class=“acc-w”>拟人</span><span class=“acc-d”>“数百年来纺着疲惫的歌”将水车拟人化；“你以伤痕累累的乳房喂养了”将祖国拟人化为母亲。</span></div>
      <div class=“acc-item”><span class=“acc-w”>对比</span><span class=“acc-d”>前两节的灰暗意象与后两节的明丽意象对比；“蜗行摸索”与“喷薄”对比；“迷惘”与“沸腾”对比。</span></div>
      <div class=“acc-item”><span class=“acc-w”>反复（复沓）</span><span class=“acc-d”>每节末尾“——祖国啊！”反复咏叹，形成回环往复的旋律，最后一节升华为“祖国啊，我亲爱的祖国！”。</span></div>
      <div class=“acc-item”><span class=“acc-w”>通感</span><span class=“acc-d”>“纺着疲惫的歌”——将水车转动的听觉形象与疲惫的触觉/心理感受相通，是通感手法。</span></div>
    </div>
  </div>
  <div class=“box”>
    <div class=“acc-cat”>
      <h3>文化常识</h3>
      <div class=“acc-item”><span class=“acc-w”>飞天</span><span class=“acc-d”>敦煌壁画中在空中飞舞的神仙，是中国古代佛教艺术的经典形象，象征美好、自由和吉祥。甘肃敦煌莫高窟有大量飞天壁画。</span></div>
      <div class=“acc-item”><span class=“acc-w”>古莲子</span><span class=“acc-d”>中国辽宁普兰店等地出土的千年古莲子，经培育仍能发芽开花，证明了植物种子顽强的生命力。诗中用来象征祖国古老而不衰的生命力。</span></div>
      <div class=“acc-item”><span class=“acc-w”>朦胧诗派</span><span class=“acc-d”>20世纪70年代末出现在中国文坛的诗歌流派，因诗意朦胧含蓄而得名。代表诗人：舒婷、北岛、顾城、江河、杨炼等。</span></div>
      <div class=“acc-item”><span class=“acc-w”>双桅船</span><span class=“acc-d”>舒婷的第一部诗集，1982年出版，收录了《致橡树》《祖国啊，我亲爱的祖国》等代表作，获中国作家协会第一届全国优秀新诗（诗集）奖。</span></div>
    </div>
  </div>'''

html_out = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>\u300a\u7956\u56fd\u554a\uff0c\u6211\u4eb2\u7231\u7684\u7956\u56fd\u300b\u8212\u5a77</title>
<style>""" + style_block + """</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">\u5f53\u4ee3 \u00b7 \u8212\u5a77</div>
  <h1 class="hero-title">\u7956\u56fd\u554a\uff0c\u6211\u4eb2\u7231\u7684\u7956\u56fd</h1>
</header>

<nav class="nav">
  <div class="nav-in">
    <a href="#bg">\u80cc\u666f</a>
    <a href="#jielu">\u89e3\u8bfb</a>
    <a href="#app">\u8d4f\u6790</a>
    <a href="#acc">\u79ef\u7d2f</a>
    <a href="#practice">\u7ec3\u4e60</a>
    <div class="tool">
      <select id="fsSel" class="fs-sel" title="\u6b63\u6587\u5b57\u4f53\u5927\u5c0f">
        <option value="100">100%</option>
        <option value="150">150%</option>
        <option value="200">200%</option>
        <option value="250">250%</option>
        <option value="300">300%</option>
      </select>
      <button id="btnAll">\u5c55\u5f00</button>
      <button id="btnRecite">\u80cc\u8bf5</button>
      <button id="btnPrint">\u6253\u5370</button>
    </div>
  </div>
</nav>

<main class="wrap">
<section id="bg" class="sec">
  <div class="sec-head"><h2>\u80cc \u666f</h2><span class="no">\u4f5c\u8005 \u00b7 \u65f6\u4ee3 \u00b7 \u7f18\u8d77</span></div>
""" + BG + """
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>\u89e3 \u8bfb</h2><span class="no">\u9010\u53e5 \u00b7 \u8bd1\u6587 \u00b7 \u8d4f\u6790</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">\u663e\u793a\u5168\u90e8</button>
  <div id="fulltext" class="poem" style="display:none">
""" + build_fulltext() + """
  </div>
  <div class="verse-list" id="verseList">
""" + build_verses() + """
  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>\u8d4f \u6790</h2><span class="no">\u610f\u8c61 \u00b7 \u827a\u672f \u00b7 \u4e3b\u9898</span></div>
""" + APP + """
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>\u79ef \u7d2f</h2><span class="no">\u6587\u4f53 \u00b7 \u5b57\u97f3\u5f62 \u00b7 \u6587\u8a00 \u00b7 \u6838\u5fc3\u8003\u70b9 \u00b7 \u4fee\u8f9e \u00b7 \u6587\u5316</span></div>
""" + ACC + """
</section>

<div class="divider"></div>
<section id="practice" class="sec">
  <div class="sec-head"><h2>\u7ec3 \u4e60</h2><span class="no">\u5168\u5c4f\u542c\u5199</span></div>
  <div class="sec-sub">\u70b9\u51fb\u6309\u94ae\u8fdb\u5165\u5168\u5c4f\u542c\u5199\u6a21\u5f0f\uff0c\u53ef\u6309 A\u2212 / A+ \u8c03\u8282\u5b57\u4f53\u5927\u5c0f\u3002</div>
  <div class="ptools">
    <button data-mode="word" data-rand="5">\u968f\u673a\u4e94\u7ec4\u5b57\u5f62</button>
    <button data-mode="word" data-all="1">\u5168\u90e8\u5b57\u5f62</button>
    <button data-mode="note" data-rand="5">\u968f\u673a\u4e94\u7ec4\u6ce8\u91ca</button>
    <button data-mode="note" data-all="1">\u5168\u90e8\u6ce8\u91ca</button>
  </div>
</section>

<footer>
  <div class="kai">\u300a\u7956\u56fd\u554a\uff0c\u6211\u4eb2\u7231\u7684\u7956\u56fd\u300b</div>
  <div>\u8212\u5a77 \u00b7 \u5f53\u4ee3 \u00b7 \u8499\u80e7\u8bd7\u6d3e\u4ee3\u8868\u4f5c</div>
  <div>\u4eba\u6559\u7248\u4e5d\u5e74\u7ea7\u8bed\u6587\u4e0b\u518c\u8bfe\u6587</div>
</footer>
</main>

<button class="top-btn" id="topBtn" title="\u56de\u5230\u9876\u90e8">\u2191</button>
<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>
<div class="dictate" id="dictate" hidden>
  <div class="dictate-top">
    <span class="dictate-mode" id="dictMode">\u5b57\u5f62\u542c\u5199</span>
    <span class="dictate-progress" id="dictProgress">\u7b2c 1 / 5 \u9898</span>
    <button class="dictate-fs" id="dictFsMinus">A\u2212</button>
    <button class="dictate-fs" id="dictFsPlus">A+</button>
    <button class="dictate-exit" id="dictExit">\u9000\u51fa</button>
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
    <button id="dictPrev">\u4e0a\u4e00\u9898</button>
    <button class="primary" id="dictShow">\u663e\u793a\u7b54\u6848</button>
    <button id="dictNext">\u4e0b\u4e00\u9898</button>
  </div>
</div>

<script>""" + script_block + """</script>
<script>
var DICT_WORDS = """ + json.dumps(DICT_WORDS, ensure_ascii=False) + """;
var DICT_NOTES = """ + json.dumps(DICT_NOTES, ensure_ascii=False) + """;
</script>

</body>
</html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html_out)

total_verses = sum(len(p["verses"]) for p in PARTS)
total_anno = sum(len(v[3]) for p in PARTS for v in p["verses"])
print("Generated:", OUT)
print("Total verses:", total_verses)
print("Total annotations:", total_anno)
print("Dict words:", len(DICT_WORDS), "Dict notes:", len(DICT_NOTES))
