# -*- coding: utf-8 -*-
"""生成《范进中举》课件 HTML"""
import re, json, html, sys
sys.path.insert(0, r"D:\App\Apps")
from data_fanjinzhongju import PARTS, DICT_WORDS, DICT_NOTES

OUT = r"D:\App\Apps\fanjinzhongju-wujingzi.html"
TEMPLATE = r"D:\App\Apps\kongyiji-luxun.html"

with open(TEMPLATE, encoding="utf-8") as f:
    tpl = f.read()

style_block = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
# 注入 acc-sub CSS（积累区小标题样式）
style_block += """
  .acc-sub{font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:10px 0 6px;color:var(--teal-deep)}
"""
script_block = re.search(r"<script>(.*?)</script>", tpl, re.S).group(1)
script_block = script_block.replace("kongyiji_fs", "fanjinzhongju_fs")

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

BG = '''  <div class="lead">
    <p>《范进中举》节选自清代吴敬梓的长篇讽刺小说《儒林外史》第三回，是中国古代讽刺文学的经典名篇。小说通过范进中举前后的遭遇，特别是中举后喜极而疯的荒诞情节，深刻揭露了封建科举制度对读书人的精神毒害，以及封建社会的世态炎凉。</p>
    <p>范进从二十岁开始应试，考了三十多年，直到五十四岁才中秀才，随后又中举人。几十年的穷困屈辱与一朝功名到手形成巨大反差，使他精神崩溃。胡屠户前倨后恭的态度变化、邻居们的趋炎附势、张乡绅的攀亲送礼，构成了一幅科举社会的群丑图。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>吴敬梓（1701—1754），字敏轩，号粒民，晚年自号文木老人，安徽全椒人。清代小说家。出身官僚世家，后家道衰落，饱尝世态炎凉。晚年贫困潦倒，卖文度日。耗费近二十年心血创作《儒林外史》，是中国古代最伟大的长篇讽刺小说。</p>
    <p style="margin-top:10px;color:var(--ink2)">《儒林外史》共五十六回，以科举制度为中心，刻画了一群封建知识分子的生活和精神面貌，讽刺了科举制度的腐朽和封建社会的黑暗。鲁迅评价其\u201c戚而能谐，婉而多讽\u201d，是中国讽刺小说的巅峰之作。</p>
  </div>
  <div class="box">
    <h3>时代背景</h3>
    <p>明清两代实行科举制度，读书人通过乡试、会试、殿试逐级考取功名。一旦中举，便跻身统治阶级，享有政治特权和经济利益。科举制度使无数读书人耗尽毕生精力于八股文，精神被严重扭曲。</p>
    <p style="margin-top:8px">范进生活的时代，科举制度已走向腐朽。中举意味着财富、地位和权力的到来，落第则意味着穷困潦倒、受人欺凌。这种巨大的反差，正是范进发疯的社会根源。小说以范进的个人悲剧，折射出整个科举制度的罪恶。</p>
  </div>
  <div class="box">
    <h3>写作缘起</h3>
    <p>吴敬梓出身科举世家，曾祖、祖父都是科举出身的大官。但他自己却在科举路上屡屡受挫，对科举制度的腐朽有切身体会。家道衰落后，他看透了世态炎凉，于是以笔为刀，创作《儒林外史》，对科举制度和封建礼教进行无情的讽刺。</p>
    <p style="margin-top:8px">《范进中举》是《儒林外史》中最精彩的篇章之一。吴敬梓以夸张而真实的笔法，写尽了科举制度下读书人的悲喜剧，至今仍有深刻的现实意义。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>《范进中举》课文朗读</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1254y1S7SH&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="《范进中举》课文朗读"></iframe>
        <a href="https://www.bilibili.com/video/BV1254y1S7SH" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>1985年典藏《儒林外史：范进中举》</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1EecrzNEMZ&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="1985年典藏《儒林外史：范进中举》"></iframe>
        <a href="https://www.bilibili.com/video/BV1EecrzNEMZ" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>'''

APP = '''  <div class="box">
    <h3>人物形象</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">范进 \u2014\u2014 科举制度的殉道者</div>
        <p>范进是一个被科举制度扭曲了灵魂的下层知识分子。他从二十岁考到五十四岁，三十四年间屡试不第，穷困潦倒，受尽屈辱。中举前，他逆来顺受、猥琐卑微，被胡屠户骂得狗血喷头也唯唯连声；中举后，他喜极而疯，清醒后立刻学会了官场的那一套应酬\u2014\u2014与张乡绅称兄道弟、收银子收房子。他的悲剧不在于疯，而在于他把全部人生价值寄托于科举功名，一旦实现，人格便彻底异化。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">胡屠户 \u2014\u2014 前倨后恭的市侩典型</div>
        <p>胡屠户是小说中最生动的喜剧人物。中举前，他对范进一口啐在脸上，骂其现世宝、癞虾蟆、尖嘴猴腮；中举后，他改口叫贤婿老爷，吹嘘范进才学又高，品貌又好，打了范进一嘴巴后手打疼了，竟以为是文曲星在惩罚他。横披了衣服，腆着肚子去了与低着头，笑迷迷的去了前后对照，一个市侩小人的势利嘴脸跃然纸上。他的变化不是个人品质问题，而是科举社会价值观的集中体现。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">张乡绅 \u2014\u2014 老于世故的官场掮客</div>
        <p>张乡绅是举人出身、做过知县的地方豪绅。范进中举前，他根本不认识范进；中举后，他主动登门，送五十两银子和一所空房，还硬攀世弟兄的关系。他的慷慨不是出于友情，而是一种政治投资\u2014\u2014结交新举人，扩大自己的势力网络。世先生果是清贫一句，看似关心，实则居高临下的施舍。他是科举制度的既得利益者，也是这个制度的维护者。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">众邻居 \u2014\u2014 趋炎附势的群像</div>
        <p>范进中举前，家里饿了两三天，邻居们无人过问；中举后，有拿鸡蛋来的，有拿白酒来的，也有背了斗米来的，也有捉两只鸡来的。范进发疯后，他们出主意、找胡屠户、帮忙按摩，热情得不得了。他们的态度变化与胡屠户如出一辙，构成了科举社会的群丑图\u2014\u2014不是某一个人坏，而是整个社会的价值取向出了问题。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>艺术特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">夸张变形，讽刺入骨</div>
        <p>范进中举后喜极而疯是全文最夸张的情节：拍手大笑、昏倒、飞跑、踹进塘里、浑身泥水、跑到集市上\u2014\u2014一个五十四岁的老读书人，在功名到手的瞬间精神崩溃。这种夸张并非凭空捏造，而是对科举制度真实危害的艺术放大。正如鲁迅所说，讽刺的生命是真实，范进的疯是无数读书人精神悲剧的集中缩影。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比手法，前倨后恭</div>
        <p>小说通篇运用对比：胡屠户中举前啐脸辱骂与中举后谄媚的对比；范进中举前家里饿了两三天与中举后送银送房的对比；邻居中举前无人过问与中举后挤满一屋的对比；胡屠户横披衣服腆肚子与低头笑迷迷的对比。多重对比使讽刺效果层层叠加，科举制度对人心的腐蚀力不言自明。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">细节描写，传神写照</div>
        <p>把银子攥在手里紧紧的，把拳头舒过来\u2014\u2014胡屠户收银的细节，嘴上推辞手却攥紧，等范进一坚持就连忙把拳头缩了回去，往腰里揣。油晃晃的衣袖是屠夫的标志。散着头发，满脸污泥，鞋都跑掉了一只是范进的疯态。细节虽小，却字字传神，人物性格在细节中自然流露。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">语言个性化，人物即语言</div>
        <p>胡屠户的语言粗俗刻薄（癞虾蟆想吃起天鹅肉、尖嘴猴腮、撒抛尿自己照照），范进的语言迂腐刻板（岳父见教的是、晚生侥幸，实是有愧），张乡绅的语言圆滑世故（世先生同在桑梓、年谊世好，就如至亲骨肉一般）。什么人说什么话，语言即人物，这是中国古典小说的优秀传统。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">白描手法，客观冷峻</div>
        <p>吴敬梓继承了中国史传文学的白描传统，不加主观评论，让人物和事实自己说话。范进发疯的全过程，作者只是客观描写动作和语言，不置一词褒贬，但讽刺意味已力透纸背。这种婉而多讽的笔法，比直接批判更有力量。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>名句赏析</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">噫！好了！我中了！</div>
        <p>范进看了报帖后的呼喊，只有六个字，却是几十年压抑的总爆发。噫是感叹词，包含了不敢相信、狂喜、激动等复杂情感；好了是苦尽甘来的释然；我中了是梦想成真的确认。这句话反复出现，成为范进疯态的标志，也是科举制度对读书人精神摧残的最凝练表达。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">把银子攥在手里紧紧的，把拳头舒过来</div>
        <p>胡屠户收银的经典细节。嘴上说这个，你且收着。我原是贺你的，怎好又拿了回去？，手却攥在手里紧紧的\u2014\u2014口是心非的虚伪跃然纸上。等范进说若用完了，再来问老爹讨来用，他连忙把拳头缩了回去，往腰里揣\u2014\u2014动作之快，与之前的推辞形成滑稽对比。一个攥一个揣，写尽市侩小人的贪财与虚伪。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">有我这贤婿，还怕后半世靠不着也怎的？</div>
        <p>胡屠户在范进中举后的得意之言。此前他还在骂范进现世宝、烂忠厚没用，现在却把范进当作后半世的靠山。这句话赤裸裸地暴露了胡屠户的势利本质：他对范进的态度完全取决于范进的功名地位，亲情在利益面前一文不值。</p>
      </div>
    </div>
  </div>
  <div class="box">
    <h3>主题思想</h3>
    <p>小说通过范进中举前后的遭遇，深刻揭露了封建科举制度对读书人的精神毒害\u2014\u2014它使读书人把全部人生价值寄托于功名，一旦中举便人格异化，一旦落第则穷困潦倒。范进的疯不是个人的偶然，而是科举制度的必然产物。</p>
    <p style="margin-top:10px">同时，小说通过胡屠户、众邻居、张乡绅等人的态度变化，描绘了一幅科举社会的世态炎凉图。在这个社会里，一个人的价值完全由科举功名决定：中举前是现世宝，中举后是贤婿老爷。吴敬梓以冷峻的白描和夸张的讽刺，对科举制度和封建礼教进行了无情的批判，使《范进中举》成为中国古代讽刺文学的不朽名篇。</p>
  </div>'''

ACC = '''  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">进学</span><span class="acc-d">科举时代童生考取秀才叫进学。范进进学回家。</span></div>
      <div class="acc-item"><span class="acc-w">现世宝</span><span class="acc-d">丢脸的家伙、不成器的人（骂人话）。把个女儿嫁与你这现世宝。</span></div>
      <div class="acc-item"><span class="acc-w">带挈</span><span class="acc-d">提携、提拔，让别人沾光。挈，qi\u00e8。带挈你中了个相公。</span></div>
      <div class="acc-item"><span class="acc-w">唯唯连声</span><span class="acc-d">连声答应，表现顺从。唯，w\u01cei。范进唯唯连声。</span></div>
      <div class="acc-item"><span class="acc-w">体统</span><span class="acc-d">规矩、体制、身分。凡事要立起个体统来。</span></div>
      <div class="acc-item"><span class="acc-w">狗血喷头</span><span class="acc-d">形容骂得很凶。骂了一个狗血喷头。</span></div>
      <div class="acc-item"><span class="acc-w">火候</span><span class="acc-d">这里指文章的功力、水平。宗师说我火候已到。</span></div>
      <div class="acc-item"><span class="acc-w">不省人事</span><span class="acc-d">昏迷过去，失去知觉。省，x\u01d0ng。牙关咬紧，不省人事。</span></div>
      <div class="acc-item"><span class="acc-w">拙病</span><span class="acc-d">倒霉的病、奇怪的病。拙，zhu\u014d。就得了这个拙病。</span></div>
      <div class="acc-item"><span class="acc-w">商酌</span><span class="acc-d">商量、斟酌。酌，zhu\u00f3。再为商酌。</span></div>
      <div class="acc-item"><span class="acc-w">星宿</span><span class="acc-d">星辰，迷信认为中举者是天上星宿下凡。宿，xi\u00f9。就是天上的星宿。</span></div>
      <div class="acc-item"><span class="acc-w">权变</span><span class="acc-d">随机应变、变通处理。你没奈何，权变一权变。</span></div>
      <div class="acc-item"><span class="acc-w">兀自</span><span class="acc-d">还、仍然（早期白话）。兀，w\u00f9。兀自拍着掌。</span></div>
      <div class="acc-item"><span class="acc-w">桑梓</span><span class="acc-d">家乡，古时住宅旁种桑梓，后代指故乡。梓，z\u01d0。世先生同在桑梓。</span></div>
      <div class="acc-item"><span class="acc-w">轩敞</span><span class="acc-d">高大宽敞。轩，xu\u0101n。虽不轩敞，也还干净。</span></div>
      <div class="acc-item"><span class="acc-w">年谊</span><span class="acc-d">科举时代同年考中者之间的关系。你我年谊世好。</span></div>
      <div class="acc-item"><span class="acc-w">见外</span><span class="acc-d">当外人看待、疏远。若要如此，就是见外了。</span></div>
      <div class="acc-item"><span class="acc-w">今非昔比</span><span class="acc-d">现在不是过去能比的，形容变化很大。姑老爷今非昔比。</span></div>
    </div>
  </div>
  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">腆</span><span class="acc-d">读 ti\u01cen，不读 di\u01cen。挺着。腆着肚子。</span></div>
      <div class="acc-item"><span class="acc-w">啐</span><span class="acc-d">读 cu\u00ec，不读 cu\u014d。用力吐唾沫。一口啐在脸上。</span></div>
      <div class="acc-item"><span class="acc-w">攥</span><span class="acc-d">读 zu\u00e0n，不读 zhu\u00e0n。紧握。攥在手里紧紧的。</span></div>
      <div class="acc-item"><span class="acc-w">踹</span><span class="acc-d">读 chu\u00e0i，不读 chu\u0101n。踩踏。一脚踹在塘里。</span></div>
      <div class="acc-item"><span class="acc-w">掼</span><span class="acc-d">读 gu\u00e0n，不读 gu\u0101n。扔、摔。掼在地下。</span></div>
      <div class="acc-item"><span class="acc-w">绾</span><span class="acc-d">读 w\u01cen，不读 gu\u01cen。盘结。自绾了头发。</span></div>
      <div class="acc-item"><span class="acc-w">宿</span><span class="acc-d">多音字：星宿 xi\u00f9；住宿 s\u00f9。文中星宿读 xi\u00f9。</span></div>
      <div class="acc-item"><span class="acc-w">省</span><span class="acc-d">多音字：不省人事 x\u01d0ng；省份 sh\u01d0ng。文中读 x\u01d0ng。</span></div>
      <div class="acc-item"><span class="acc-w">中</span><span class="acc-d">多音字：中举 zh\u00f2ng；中间 zh\u014dng。文中中举读 zh\u00f2ng。</span></div>
      <div class="acc-item"><span class="acc-w">醺</span><span class="acc-d">读 x\u016bn，不读 x\u00f9n。酒醉。吃的醺醺的。</span></div>
      <div class="acc-item"><span class="acc-w">锭</span><span class="acc-d">读 d\u00ecng，不读 d\u00ecn。银元宝。细丝锭子。</span></div>
    </div>
  </div>
  <div class="box">
    <div class="acc-cat">
      <h3>修辞方法</h3>
      <div class="acc-item"><span class="acc-w">夸张</span><span class="acc-d">范进中举后喜极而疯是全文最夸张的情节，通过放大人物的失常行为，揭露科举制度对读书人的精神摧残。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">胡屠户中举前辱骂与中举后谄媚的对比；范进中举前穷困与中举后富贵的对比；邻居中举前冷漠与中举后热情的对比。</span></div>
      <div class="acc-item"><span class="acc-w">细节描写</span><span class="acc-d">把银子攥在手里紧紧的，把拳头舒过来\u2014\u2014胡屠户收银的细节，写尽市侩小人的虚伪贪财。</span></div>
      <div class="acc-item"><span class="acc-w">白描</span><span class="acc-d">作者不加主观评论，客观描写人物的言行，让讽刺意味自然流露，婉而多讽。</span></div>
      <div class="acc-item"><span class="acc-w">语言描写</span><span class="acc-d">胡屠户的粗俗刻薄、范进的迂腐刻板、张乡绅的圆滑世故，人物语言即人物性格。</span></div>
      <div class="acc-item"><span class="acc-w">反复</span><span class="acc-d">噫！好了！我中了！反复出现，成为范进疯态的标志，强化了科举制度对人的精神控制。</span></div>
    </div>
  </div>
  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-sub" style="font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:10px 0 6px;color:var(--teal-deep)">人物形象</div>
      <div class="acc-item"><span class="acc-w">范进</span><span class="acc-d">科举制度的殉道者：三十四年应试，中举前逆来顺受，中举后喜极而疯，清醒后立刻学会官场应酬。</span></div>
      <div class="acc-item"><span class="acc-w">胡屠户</span><span class="acc-d">前倨后恭的市侩典型：中举前啐脸辱骂，中举后贤婿老爷，态度变化本身就是对科举社会的讽刺。</span></div>
      <div class="acc-sub" style="font-family:var(--font-kai);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:10px 0 6px;color:var(--teal-deep)">写作手法</div>
      <div class="acc-item"><span class="acc-w">以小见大</span><span class="acc-d">通过范进一个人的中举事件，折射整个科举制度的腐朽和封建社会的世态炎凉。</span></div>
      <div class="acc-item"><span class="acc-w">夸张与真实结合</span><span class="acc-d">范进发疯是夸张的，但背后是科举制度真实的精神危害。讽刺的生命是真实。</span></div>
      <div class="acc-item"><span class="acc-w">前后对照</span><span class="acc-d">胡屠户横披衣服腆肚子与低头笑迷迷前后对照，人物态度变化一目了然。</span></div>
      <div class="acc-item"><span class="acc-w">细节传神</span><span class="acc-d">攥、揣、油晃晃的衣袖等细节，用最少的笔墨写出最丰富的人物性格。</span></div>
    </div>
  </div>
  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">科举制度</span><span class="acc-d">明清科举分四级：院试（考秀才）\u2192乡试（考举人，三年一次，在省城）\u2192会试（考贡士，在京城）\u2192殿试（考进士，皇帝亲考）。范进先中秀才（进学），后中举人（乡试第七名亚元）。</span></div>
      <div class="acc-item"><span class="acc-w">相公 / 老爷</span><span class="acc-d">明清时称秀才为相公，称举人为老爷。范进中秀才后胡屠户称他相公，中举后报录人称范老爷。</span></div>
      <div class="acc-item"><span class="acc-w">亚元</span><span class="acc-d">乡试第一名称解元，第二名至第十名称亚元。范进中第七名，故称第七名亚元。</span></div>
      <div class="acc-item"><span class="acc-w">报录人</span><span class="acc-d">把考中消息送到家中的差役，也叫报子。他们向考中者家庭索取喜钱作为报酬。</span></div>
      <div class="acc-item"><span class="acc-w">文曲星</span><span class="acc-d">中国神话中主管文运的星官。迷信认为科举考中者都是文曲星下凡，所以胡屠户说中老爷的都是天上的文曲星。</span></div>
      <div class="acc-item"><span class="acc-w">房师 / 门生</span><span class="acc-d">乡试时，同考官分房阅卷，称房师；考中的人对房师自称门生。张乡绅攀亲时说范进的房师是他先祖的门生。</span></div>
      <div class="acc-item"><span class="acc-w">桑梓</span><span class="acc-d">古代住宅旁常种桑树（养蚕）和梓树（做家具），后用桑梓代指故乡。世先生同在桑梓即我们是同乡。</span></div>
    </div>
  </div>'''

html_out = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>\u300a\u8303\u8fdb\u4e2d\u4e3e\u300b\u5434\u656c\u6893</title>
<style>""" + style_block + """</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">\u6e05 \u00b7 \u5434\u656c\u6893</div>
  <h1 class="hero-title">\u8303\u8fdb\u4e2d\u4e3e</h1>
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
  <div class="kai">\u300a\u8303\u8fdb\u4e2d\u4e3e\u300b</div>
  <div>\u5434\u656c\u6893 \u00b7 \u6e05 \u00b7 \u8282\u9009\u81ea\u300a\u5112\u6797\u5916\u53f2\u300b\u7b2c\u4e09\u56de</div>
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
