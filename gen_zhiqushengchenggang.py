# -*- coding: utf-8 -*-
"""生成《智取生辰纲》课件 HTML"""
import re, json, html, sys
sys.path.insert(0, r"D:\App\Apps")
from data_zhiqushengchenggang import PARTS, DICT_WORDS, DICT_NOTES

OUT = r"D:\App\Apps\zhiqushengchenggang-shinaian.html"
TEMPLATE = r"D:\App\Apps\kongyiji-luxun.html"

with open(TEMPLATE, encoding="utf-8") as f:
    tpl = f.read()

style_block = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
style_block += """
  .acc-sub{font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:10px 0 6px;color:var(--teal-deep)}
"""
script_block = re.search(r"<script>(.*?)</script>", tpl, re.S).group(1)
script_block = script_block.replace("kongyiji_fs", "zhiqushengchenggang_fs")

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
        for orig, summary, analysis, notes in part["verses"]:
            gidx += 1
            annotated = annotate(orig, notes)
            parts.append('      <div class="verse" id="l' + str(gidx) + '" data-i="' + str(gidx-1) + '">')
            parts.append('        <div class="v-top"><span class="v-no">' + str(gidx) + '</span><div class="v-line">' + annotated + '</div></div>')
            parts.append('        <details class="v-more">')
            parts.append('          <summary>内容 \u00b7 手法</summary>')
            parts.append('          <div class="d-body">')
            parts.append('            <div class="v-sec"><b class="v-label">内容概括</b>')
            parts.append('              <div class="v-trans">' + summary + '</div>')
            parts.append('            </div>')
            parts.append('            <div class="v-sec"><b class="v-label">手法分析</b>')
            parts.append('              <div class="d-body"><p>' + analysis + '</p></div>')
            parts.append('            </div>')
            parts.append('          </div>')
            parts.append('        </details>')
            parts.append('      </div>')
    return "\n".join(parts)

def build_fulltext():
    lines = []
    for part in PARTS:
        for orig, _, _, _ in part["verses"]:
            lines.append('    <div class="pl">' + orig + '</div>')
    return "\n".join(lines)

BG = '''  <div class=“lead”>
    <p>《智取生辰纲》节选自元末明初施耐庵的长篇小说《水浒传》第十六回（原题“杨志押送金银担，吴用智取生辰纲”），是《水浒传》中最精彩的篇章之一。小说通过杨志押送生辰纲失败的经过，生动展现了吴用等人的智谋，以及官逼民反的社会现实。</p>
    <p>生辰纲是北京大名府留守梁中书为岳父蔡京祝寿而搜刮的十万贯金珠宝贝。杨志奉命押送，一路上小心谨慎、严加防范，却最终在黄泥冈被晁盖、吴用等七人用蒙汗药麻翻，生辰纲被尽数劫走。杨志的失败，不仅在于吴用的计策高明，更在于他自身性格的缺陷和押送队伍内部的矛盾。</p>
  </div>
  <div class=“box”>
    <h3>作者简介</h3>
    <p>施耐庵（约1296—约1370），原名彦端，字肇瑞，号子安，别号耐庵，江苏兴化人（一说浙江钱塘人）。元末明初小说家。曾参加元末张士诚起义，后隐居著书。他在民间传说、话本、杂剧的基础上，创作了中国第一部以农民起义为题材的长篇章回体小说《水浒传》。</p>
    <p style=“margin-top:10px;color:var(--ink2)”>《水浒传》是中国古典四大名著之一，描写了北宋末年以宋江为首的一百零八位好汉在梁山聚义的故事，深刻反映了封建社会的黑暗和“官逼民反”的现实。小说塑造了林冲、鲁智深、武松、杨志等众多栩栩如生的英雄形象。</p>
  </div>
  <div class=“box”>
    <h3>时代背景</h3>
    <p>北宋末年，政治腐败，民不聊生。宋徽宗宠信蔡京、童贯等奸臣，搜刮民脂民膏。生辰纲就是这种社会现实的产物——梁中书为讨好岳父蔡京，从民间搜刮十万贯金珠宝贝作为寿礼。</p>
    <p style=“margin-top:8px”>《水浒传》的故事虽以北宋为背景，但反映的却是元末明初的社会现实。施耐庵亲身经历了元末农民大起义，对社会的黑暗和人民的苦难有深切体会，因此能写出如此深刻的作品。</p>
  </div>
  <div class=“box”>
    <h3>写作缘起</h3>
    <p>《水浒传》的故事在民间流传已久，宋元时期已有许多关于水浒英雄的话本和杂剧。施耐庵在这些民间文学的基础上，进行了艺术再创作，将零散的故事串联成一部完整的长篇小说。</p>
    <p style=“margin-top:8px”>“智取生辰纲”是梁山好汉聚义的开端——晁盖、吴用等人劫取生辰纲后，被迫投奔梁山，拉开了水浒英雄大聚义的序幕。这一事件充分展示了吴用的智慧和梁山好汉的反抗精神。</p>
  </div>
  <div class=“box media-box”>
    <h3>视听</h3>
    <div class=“media-grid”>
      <div class=“media”>
        <h4>《智取生辰纲》课文朗读</h4>
        <iframe id=“mediaF1” src=“https://player.bilibili.com/player.html?bvid=BV18A41177Rn&page=1&high_quality=1&danmaku=0&autoplay=0” loading=“lazy” scrolling=“no” frameborder=“0” allowfullscreen=“true” title=“《智取生辰纲》课文朗读”></iframe>
        <a href=“https://www.bilibili.com/video/BV18A41177Rn” target=“_blank” rel=“noopener”>在 B 站打开原视频</a><button class=“fsbtn” data-target=“mediaF1”>全屏播放</button>
      </div>
      <div class=“media”>
        <h4>98版《水浒传》智取生辰纲</h4>
        <iframe id=“mediaF2” src=“https://player.bilibili.com/player.html?bvid=BV1Mu411U7tZ&page=1&high_quality=1&danmaku=0&autoplay=0” loading=“lazy” scrolling=“no” frameborder=“0” allowfullscreen=“true” title=“98版水浒传智取生辰纲”></iframe>
        <a href=“https://www.bilibili.com/video/BV1Mu411U7tZ” target=“_blank” rel=“noopener”>在 B 站打开原视频</a><button class=“fsbtn” data-target=“mediaF2”>全屏播放</button>
      </div>
    </div>
  </div>'''

APP = '''  <div class=“box”>
    <h3>人物形象</h3>
    <div class=“fame”>
      <div class=“fame-card”>
        <div class=“f-line”>杨志 \u2014\u2014 精明能干却粗暴蛮横的失意英雄</div>
        <p>杨志是杨家将后人，武举出身，曾任殿司制使。他一心想封妻荫子、光宗耀祖，却时运不济：先失花石纲，后杀牛二被发配，好不容易得到梁中书赏识负责押送生辰纲，又在黄泥冈功亏一篑。杨志精明能干（选择辰牌起身、申时歇息，警惕强人），但性格粗暴蛮横（打骂军汉、不体恤下属），导致内部矛盾激化，最终失败。他是一个有能力却不得志的悲剧英雄。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>吴用 \u2014\u2014 足智多谋的“智多星”</div>
        <p>吴用是智取生辰纲的策划者和执行者。他的计策环环相扣、天衣无缝：第一步，七人扮作枣贩子现身，消除杨志疑虑；第二步，白胜卖酒，杨志阻止，制造矛盾；第三步，枣贩子买酒喝光一桶，证明无毒；第四步，在第二桶酒中用椰瓢下药；第五步，军汉们买酒喝下，全部被麻翻。整个过程利用了天气炎热、内部矛盾和人的心理，不费一刀一枪就劫走了生辰纲，充分展示了“智多星”的智慧。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>白胜 \u2014\u2014 演技精湛的“白日鼠”</div>
        <p>白胜扮作卖酒的汉子，是计策成功的关键人物。他的表演自然真实：冷笑反驳杨志（你这客官好不晓事）、故意说不卖（不卖！不卖！）、被客人多舀一瓢时的愤怒（劈手夺住、好不君子相）、最后收了钱唱着山歌下冈——每一个动作、每一句话都恰到好处，完全是一个普通卖酒人的样子，连精明的杨志都被蒙骗了。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>老都管 \u2014\u2014 倚老卖老的官场老手</div>
        <p>老都管是梁中书的亲信，在押送队伍中地位特殊。他起初还能忍耐（权且耐他），但随着矛盾激化，终于出面与杨志对抗。他搬出在东京太师府的资历（我在东京太师府里做奶公时），以身份压人，大骂杨志官职微小（比得芥菜子大小的官职）。他的出面求情，是杨志同意买酒的直接原因，也是押送失败的重要因素。他代表了官场中那种倚老卖老、不切实际的官僚作风。</p>
      </div>
    </div>
  </div>
  <div class=“box”>
    <h3>艺术特色</h3>
    <div class=“fame”>
      <div class=“fame-card”>
        <div class=“f-line”>双线结构，明暗交织</div>
        <p>小说有两条线索：明线是杨志押送生辰纲（小心谨慎、处处防范），暗线是吴用智取生辰纲（精心策划、步步设局）。两条线索在黄泥冈交汇，最终暗线战胜明线。这种结构使故事悬念迭起、引人入胜——读者知道吴用的计策，但不知道杨志何时会中计，紧张感贯穿始终。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>环境描写，烘托气氛</div>
        <p>天气炎热是贯穿全文的重要环境因素。“一轮红日当天，没半点云彩”“石头上热了，脚疼走不得”——酷热的天气不仅是军汉们怨声载道的原因，更是他们买酒解渴的动机，也是吴用计策成功的客观条件。环境描写与情节发展紧密结合，推动了故事的发展。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>细节描写，精妙入微</div>
        <p>下药的过程是全文最精彩的细节描写：第一个客人兜一瓢往松林走（吸引注意），第二个客人从松林出来舀酒（瓢里藏药），白胜劈手夺住望桶里一倾（药下入桶中）——三个动作一气呵成，在读者和杨志眼中都只是客人贪小便宜，毫无破绽。这种细节描写，使吴用的智慧具体可感。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>对比手法，人物鲜明</div>
        <p>杨志的谨慎与军汉的麻木对比；杨志的粗暴与老都管的圆滑对比；吴用的智慧与杨志的失算对比；押送队伍的内部矛盾与七星聚义的团结对比——多重对比使人物形象更加鲜明，主题更加突出。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>语言个性化，生动传神</div>
        <p>杨志的语言简短严厉（快走！教你早歇！），军汉的语言充满抱怨（你便剁做我七八段，其实去不得了），老都管的语言官气十足（我在东京太师府里做奶公时），白胜的语言市井气浓（不卖！不卖！）——什么人说什么话，语言即人物。</p>
      </div>
    </div>
  </div>
  <div class=“box”>
    <h3>名句赏析</h3>
    <div class=“fame”>
      <div class=“fame-card”>
        <div class=“f-line”>倒也！倒也！</div>
        <p>七个枣贩子指着十五人喊出的话，是全文的点睛之笔。简短的四个字，既是蒙汗药发作的信号，也是对杨志等人的嘲讽。“倒也”重复两次，节奏感强，画面感十足——十五个人头重脚轻、面面厮觑、纷纷软倒的场景如在目前。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>你便剁做我七八段，其实去不得了。</div>
        <p>军汉对杨志的反抗之语。“剁做我七八段”是极端的说法，意思是就算你把我砍成七八段，我也走不动了。这句话既写出了天气的酷热和军汉们的疲惫，也写出了他们对杨志的怨恨——宁可被砍死也不愿再走，矛盾已经到了不可调和的地步。</p>
      </div>
      <div class=“fame-card”>
        <div class=“f-line”>不卖了！不卖了！这酒里有蒙汗药在里头。</div>
        <p>白胜的经典台词。越是说有蒙汗药，众人越不相信——这是典型的“反话正说”。白胜故意用这种方式打消众人的疑虑，同时也表现出一个普通卖酒人被冤枉后的愤怒。这句话是吴用计策中最精彩的心理战术。</p>
      </div>
    </div>
  </div>
  <div class=“box”>
    <h3>主题思想</h3>
    <p>小说通过杨志押送生辰纲失败的故事，歌颂了梁山好汉的智慧和反抗精神，揭露了封建统治阶级的腐朽和社会的黑暗。生辰纲是梁中书从民间搜刮来的民脂民膏，晁盖、吴用等人劫取它，是“劫富济贫”的正义行为。</p>
    <p style=“margin-top:10px”>同时，小说也深刻揭示了杨志失败的原因：外部有吴用的妙计，内部有队伍的矛盾，而根本原因在于杨志自身的性格缺陷——他精明但不智慧，能干但不团结人，一心想靠押送成功来恢复功名，却忽视了人的因素。杨志的悲剧，是个人性格的悲剧，也是时代的悲剧——在那个“官逼民反”的时代，任何想在体制内有所作为的人，最终都只能走向反抗的道路。</p>
  </div>'''

ACC = '''  <div class=“box”>
    <div class=“acc-cat”>
      <h3>重点词语</h3>
      <div class=“acc-item”><span class=“acc-w”>趱行</span><span class=“acc-d”>赶路、快走。趱，z\u01cen。只得在路上趱行。</span></div>
      <div class=“acc-item”><span class=“acc-w”>端的</span><span class=“acc-d”>确实、果然（早期白话）。端的只是起五更。</span></div>
      <div class=“acc-item”><span class=“acc-w”>嗔</span><span class=“acc-d”>发怒、生气。嗔，ch\u0113n。杨志也嗔道。</span></div>
      <div class=“acc-item”><span class=“acc-w”>干系</span><span class=“acc-d”>责任、关系。这干系须是俺的。</span></div>
      <div class=“acc-item”><span class=“acc-w”>尴尬去处</span><span class=“acc-d”>危险的地方、容易出问题的路段。尴尬，g\u0101n g\u00e0。如今正是尴尬去处。</span></div>
      <div class=“acc-item”><span class=“acc-w”>这厮</span><span class=“acc-d”>这家伙、这小子（骂人话）。厮，s\u012b。这厮不直得便骂人。</span></div>
      <div class=“acc-item”><span class=“acc-w”>提辖</span><span class=“acc-d”>宋代武官名，负责地方军队训练和治安。强杀只是我相公门下一个提辖。</span></div>
      <div class=“acc-item”><span class=“acc-w”>做大</span><span class=“acc-d”>摆架子、妄自尊大。直这般会做大。</span></div>
      <div class=“acc-item”><span class=“acc-w”>吹嘘</span><span class=“acc-d”>这里指喘气、嘘气（不是吹牛）。都叹气吹嘘。</span></div>
      <div class=“acc-item”><span class=“acc-w”>恁地</span><span class=“acc-d”>这样、如此。恁，n\u00e8n。我们直恁地苦。</span></div>
      <div class=“acc-item”><span class=“acc-w”>怨怅</span><span class=“acc-d”>怨恨、埋怨。怅，ch\u00e0ng。你们不要怨怅。</span></div>
      <div class=“acc-item”><span class=“acc-w”>省得</span><span class=“acc-d”>懂得、知道。省，x\u01d0ng。你们省得甚么。</span></div>
      <div class=“acc-item”><span class=“acc-w”>絮絮聒聒</span><span class=“acc-d”>唠叨不停、说个没完。聒，gu\u014d。絮絮聒聒地搬口。</span></div>
      <div class=“acc-item”><span class=“acc-w”>强人</span><span class=“acc-d”>强盗、劫匪。这里正是强人出没的去处。</span></div>
      <div class=“acc-item”><span class=“acc-w”>兀自</span><span class=“acc-d”>还、仍然（早期白话）。兀，w\u00f9。白日里兀自出来劫人。</span></div>
      <div class=“acc-item”><span class=“acc-w”>朱砂记</span><span class=“acc-d”>红色的胎记。鬓边老大一搭朱砂记。</span></div>
      <div class=“acc-item”><span class=“acc-w”>小本经纪</span><span class=“acc-d”>小本生意、小买卖。我等是小本经纪。</span></div>
      <div class=“acc-item”><span class=“acc-w”>蒙汗药</span><span class=“acc-d”>一种麻醉药，吃了会昏迷。这酒里有甚么蒙汗药。</span></div>
      <div class=“acc-item”><span class=“acc-w”>面面厮觑</span><span class=“acc-d”>面面相觑，你看我我看你。觑，q\u00f9。一个个面面厮觑。</span></div>
      <div class=“acc-item”><span class=“acc-w”>聒噪</span><span class=“acc-d”>打扰了、麻烦了（早期白话告别语）。聒，gu\u014d。叫声：聒噪！</span></div>
    </div>
  </div>
  <div class=“box”>
    <div class=“acc-cat”>
      <h3>用字与读音</h3>
      <div class=“acc-item”><span class=“acc-w”>趱</span><span class=“acc-d”>读 z\u01cen，不读 z\u00e0n。快走。趱行。</span></div>
      <div class=“acc-item”><span class=“acc-w”>嗔</span><span class=“acc-d”>读 ch\u0113n，不读 ti\u00e1n。发怒。嗔道。</span></div>
      <div class=“acc-item”><span class=“acc-w”>朴</span><span class=“acc-d”>多音字：朴刀 p\u014d；朴素 p\u01d2。文中朴刀读 p\u014d。</span></div>
      <div class=“acc-item”><span class=“acc-w”>恁</span><span class=“acc-d”>读 n\u00e8n，不读 r\u00e8n。这样。恁地。</span></div>
      <div class=“acc-item”><span class=“acc-w”>怅</span><span class=“acc-d”>读 ch\u00e0ng，不读 zh\u00e0ng。埋怨。怨怅。</span></div>
      <div class=“acc-item”><span class=“acc-w”>省</span><span class=“acc-d”>多音字：省得 x\u01d0ng；省份 sh\u01d0ng。文中省得读 x\u01d0ng。</span></div>
      <div class=“acc-item”><span class=“acc-w”>讷</span><span class=“acc-d”>读 n\u00e8，不读 n\u00e0。言语迟钝。喃喃讷讷。</span></div>
      <div class=“acc-item”><span class=“acc-w”>聒</span><span class=“acc-d”>读 gu\u014d，不读 sh\u00e9。吵闹。絮絮聒聒。</span></div>
      <div class=“acc-item”><span class=“acc-w”>兀</span><span class=“acc-d”>读 w\u00f9，不读 w\u016b。仍然。兀自。</span></div>
      <div class=“acc-item”><span class=“acc-w”>剜</span><span class=“acc-d”>读 w\u0101n，不读 w\u01cen。挖。剜口割舌。</span></div>
      <div class=“acc-item”><span class=“acc-w”>觑</span><span class=“acc-d”>读 q\u00f9，不读 x\u016b。看。面面厮觑。</span></div>
    </div>
  </div>
  <div class=“box”>
    <div class=“acc-cat”>
      <h3>修辞方法</h3>
      <div class=“acc-item”><span class=“acc-w”>双线结构</span><span class=“acc-d”>明线杨志押送（谨慎防范），暗线吴用智取（步步设局），两线在黄泥冈交汇，悬念迭起。</span></div>
      <div class=“acc-item”><span class=“acc-w”>环境烘托</span><span class=“acc-d”>酷热天气贯穿全文，既是军汉抱怨的原因，也是买酒的动机，更是计策成功的客观条件。</span></div>
      <div class=“acc-item”><span class=“acc-w”>细节描写</span><span class=“acc-d”>下药过程（兜瓢、走松林、舀酒、夺住、倾入桶）一气呵成，在读者眼中只是贪小便宜，毫无破绽。</span></div>
      <div class=“acc-item”><span class=“acc-w”>对比</span><span class=“acc-d”>杨志的谨慎与军汉的麻木；杨志的粗暴与老都管的圆滑；吴用的智慧与杨志的失算。</span></div>
      <div class=“acc-item”><span class=“acc-w”>语言描写</span><span class=“acc-d”>杨志简短严厉，军汉抱怨无奈，老都管官气十足，白胜市井气浓——语言即人物。</span></div>
      <div class=“acc-item”><span class=“acc-w”>反复</span><span class=“acc-d”>倒也！倒也！不卖！不卖！的反复，增强节奏感和画面感。</span></div>
    </div>
  </div>
  <div class=“box”>
    <div class=“acc-cat”>
      <h3>写作借鉴</h3>
      <div class=“acc-sub”>人物形象</div>
      <div class=“acc-item”><span class=“acc-w”>杨志</span><span class=“acc-d”>精明能干却粗暴蛮横的失意英雄：小心押送却因内部矛盾失败，是个人性格悲剧也是时代悲剧。</span></div>
      <div class=“acc-item”><span class=“acc-w”>吴用</span><span class=“acc-d”>足智多谋的智多星：计策环环相扣，利用天气、矛盾和心理，不费一刀一枪劫走生辰纲。</span></div>
      <div class=“acc-sub”>写作手法</div>
      <div class=“acc-item”><span class=“acc-w”>悬念设置</span><span class=“acc-d”>读者知道吴用的计策，但不知道杨志何时中计，紧张感贯穿始终。</span></div>
      <div class=“acc-item”><span class=“acc-w”>伏笔与照应</span><span class=“acc-d”>椰瓢的出现（我们自有椰瓢在这里）为下文下药埋下伏笔；枣子丢弃照应了枣贩子的身份。</span></div>
      <div class=“acc-item”><span class=“acc-w”>心理刻画</span><span class=“acc-d”>杨志从坚决反对到勉强同意的心理转变，写得细腻真实（想是好的、胡乱容他买碗吃罢）。</span></div>
      <div class=“acc-item”><span class=“acc-w”>以小见大</span><span class=“acc-d”>一次押送事件，折射出封建社会的黑暗和官逼民反的现实。</span></div>
    </div>
  </div>
  <div class=“box”>
    <div class=“acc-cat”>
      <h3>文化常识</h3>
      <div class=“acc-item”><span class=“acc-w”>生辰纲</span><span class=“acc-d”>纲，旧时成批运输货物的组织。生辰纲是为祝寿而押送的大批礼物。梁中书为岳父蔡京送的十万贯金珠宝贝。</span></div>
      <div class=“acc-item”><span class=“acc-w”>提辖</span><span class=“acc-d”>宋代武官名，负责地方军队的训练、督捕盗贼等事务。杨志曾任殿司制使，后被梁中书提拔为提辖。</span></div>
      <div class=“acc-item”><span class=“acc-w”>虞候 / 都管</span><span class=“acc-d”>虞候是宋代低级武官，都管是官府中的管家。在押送队伍中，老都管地位最高，虞候次之，杨志虽是负责人但地位不如老都管。</span></div>
      <div class=“acc-item”><span class=“acc-w”>辰牌 / 申时</span><span class=“acc-d”>古代用十二时辰计时，辰时为上午7-9时，申时为下午3-5时。牌，时报的牌子。</span></div>
      <div class=“acc-item”><span class=“acc-w”>蒙汗药</span><span class=“acc-d”>相传是一种用曼陀罗花等制成的麻醉药，混入酒中饮用后会使人昏迷不醒。是古代小说中常见的作案工具。</span></div>
      <div class=“acc-item”><span class=“acc-w”>江州车</span><span class=“acc-d”>江州（今江西九江）一带的独轮小车，适合在山路运输。晁盖等人用它伪装成枣贩子，实际上用来运财宝。</span></div>
      <div class=“acc-item”><span class=“acc-w”>七星聚义</span><span class=“acc-d”>劫取生辰纲的共七人：晁盖、吴用、公孙胜、刘唐、三阮（阮小二、阮小五、阮小七），加上白胜共八人。七人扮枣贩子，白胜扮卖酒人。</span></div>
    </div>
  </div>'''

html_out = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>\u300a\u667a\u53d6\u751f\u8fb0\u7eb2\u300b\u65bd\u8010\u5eb5</title>
<style>""" + style_block + """</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">\u5143\u672b\u660e\u521d \u00b7 \u65bd\u8010\u5eb5</div>
  <h1 class="hero-title">\u667a\u53d6\u751f\u8fb0\u7eb2</h1>
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
  <div class="sec-head"><h2>\u89e3 \u8bfb</h2><span class="no">\u9010\u6bb5 \u00b7 \u8bcd\u8bed \u00b7 \u624b\u6cd5</span></div>
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
  <div class="sec-head"><h2>\u8d4f \u6790</h2><span class="no">\u4eba\u7269 \u00b7 \u827a\u672f \u00b7 \u540d\u53e5</span></div>
""" + APP + """
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>\u79ef \u7d2f</h2><span class="no">\u8bcd\u8bed \u00b7 \u7528\u5b57 \u00b7 \u4fee\u8f9e \u00b7 \u5199\u6cd5 \u00b7 \u6587\u5316</span></div>
""" + ACC + """
</section>

<div class="divider"></div>
<section id="practice" class="sec">
  <div class="sec-head"><h2>\u7ec3 \u4e60</h2><span class="no">\u5168\u5c4f\u542c\u5199</span></div>
  <div class="sec-sub">\u70b9\u51fb\u6309\u94ae\u8fdb\u5165\u5168\u5c4f\u542c\u5199\u6a21\u5f0f\uff0c\u53ef\u6309 A\u2212 / A+ \u8c03\u8282\u5b57\u4f53\u5927\u5c0f\u3002</div>
  <div class="ptools">
    <button data-mode="word" data-rand="5">\u968f\u673a\u4e94\u7ec4\u5b57\u5f62</button>
    <button data-mode="word" data-all="1">\u5168\u90e8\u5b57\u5f62</button>
    <button data-mode="note" data-rand="5">\u968f\u673a\u4e94\u7ec4\u8bcd\u8bed</button>
    <button data-mode="note" data-all="1">\u5168\u90e8\u8bcd\u8bed</button>
  </div>
</section>

<footer>
  <div class="kai">\u300a\u667a\u53d6\u751f\u8fb0\u7eb2\u300b</div>
  <div>\u65bd\u8010\u5eb5 \u00b7 \u5143\u672b\u660e\u521d \u00b7 \u8282\u9009\u81ea\u300a\u6c34\u6d52\u4f20\u300b\u7b2c\u5341\u516d\u56de</div>
  <div>\u4eba\u6559\u7248\u4e5d\u5e74\u7ea7\u8bed\u6587\u4e0a\u518c\u8bfe\u6587</div>
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
