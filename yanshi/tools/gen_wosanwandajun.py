# -*- coding: utf-8 -*-
"""生成毛泽东《我三十万大军胜利南渡长江》课件 HTML（消息类，参照《背影》模板）"""
import json, re, html as htmlmod

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\wosanwandajunshenglinanduchangjiang-maozedong.html"

src = open(TEMPLATE, encoding="utf-8").read()

# ---- 提取 CSS ----
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)

# ---- 提取主脚本（第一个 <script> 块，含 IIFE） ----
mains = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = mains[0]
main_js = main_js.replace("beiying_fs", "wosanwan_fs")

# ================= 数据 =================

H = "现代 · 毛泽东"
TITLE = "我三十万大军胜利南渡长江"

# ---------- 背景区 ----------
LEAD = [
    "1949年4月，解放战争进入战略追击阶段。国民党反动派在辽沈、淮海、平津三大战役中惨败后，又玩弄\u201c和谈\u201d阴谋，妄图以长江为界\u201c划江而治\u201d。4月20日，国民党政府拒绝签订国内和平协定，毛泽东、朱德发布《向全国进军的命令》，人民解放军发起渡江战役。",
    "4月21日，人民解放军百万雄师在西起湖口、东至江阴的千里战线上强渡长江。毛泽东亲自为新华社撰写了这则消息，及时报道中路军三十万人胜利渡江的战况，极大地鼓舞了全国人民的斗志。文章篇幅短小，气势磅礴，是新闻消息的典范之作。",
]

AUTHOR = [
    "毛泽东（1893—1976），字润之，湖南湘潭人。中国共产党、中国人民解放军和中华人民共和国的主要缔造者和领导人，伟大的马克思主义者、无产阶级革命家、战略家和理论家。同时也是杰出的诗人和文章大家，其新闻作品以气势雄浑、语言精练著称。",
    "毛泽东长期重视新闻宣传工作，曾亲自为新华社撰写和修改大量消息、评论。这则消息写于1949年4月22日，是渡江战役打响后第一篇公开报道，以极简的篇幅传递了重大的军事胜利信息，体现了消息\u201c短、快、准\u201d的文体特征。",
]

BG = [
    ("写作背景", [
        "三大战役后：1948年9月至1949年1月，人民解放军取得辽沈、淮海、平津三大战役的胜利，国民党主力基本被消灭，解放战争胜利在望。",
        "和谈破裂：1949年4月，国共双方在北平举行和平谈判。4月20日，国民党政府拒绝在《国内和平协定》上签字，和谈宣告破裂。",
        "渡江战役：4月21日，毛泽东、朱德发布《向全国进军的命令》，人民解放军第二、第三野战军及第四野战军一部，在西起湖口、东至江阴的千里战线上强渡长江，彻底摧毁国民党的长江防线。",
    ]),
    ("文体知识", [
        "消息的定义：消息是新闻体裁中最基本、最常用的一种，以简要的文字迅速报道新近发生的事实，具有真实性、时效性和准确性的特点。",
        "消息的结构：一般包括标题、导语、主体、背景和结语五部分。导语是消息的核心，用最简练的语言概括最重要的事实；主体具体展开叙述；背景补充说明；结语收束。",
        "消息的六要素：时间、地点、人物、事件的起因、经过、结果，即\u201c五W+H\u201d（When、Where、Who、What、Why、How）。",
    ]),
]

VIDEOS = [
    ("中小学语文示范诵读库《我三十万大军胜利南渡长江》",
     "BV1mY4y1Y7GH",
     "https://www.bilibili.com/video/BV1mY4y1Y7GH",
     "mediaF1"),
    ("1949年渡江战役真实影像",
     "BV1SY4y1t7mA",
     "https://www.bilibili.com/video/BV1SY4y1t7mA",
     "mediaF2"),
]

# ---------- 解读区 ----------
# 消息按结构分卡片：电头/标题 → 导语 → 主体 → 结语
# 每卡: (no, 原文, 内容概括, 手法分析, [(词, 注), ...])
# 短篇课文不分part，直接逐段解读

VERSES = [
(1, "新华社长江前线二十二日二时电",
 "电头：交代通讯社名称、发报地点和时间，体现消息的时效性和权威性。",
 "电头是消息的标志，\u201c新华社\u201d表明消息来源，\u201c长江前线\u201d点明发报地点，\u201c二十二日二时\u201d精确到小时，凸显新闻的时效性。",
 [("新华社","新华通讯社的简称，是中国国家通讯社"),("长江前线","指渡江战役前线指挥部所在地"),("电","电报、电文，这里指电讯稿件")]),

(2, "英勇的人民解放军二十一日已有大约三十万人渡过长江。",
 "导语：一句话概括核心事实——人民解放军三十万人于二十日胜利渡过长江，包含人物、时间、事件、结果四要素。",
 "导语是消息的灵魂，开门见山，\u201c英勇\u201d定感情基调，\u201c大约三十万人\u201d用确数体现新闻准确性，一句话即把最重要的信息传递给读者。",
 [("英勇","勇敢出众，这里褒扬人民解放军的战斗精神"),("大约","表示估计的数目不十分精确，体现新闻语言的严谨")]),

(3, "渡江战斗于二十日午夜开始，地点在芜湖、安庆之间。国民党反动派经营了三个半月的长江防线，遇着人民解放军好似摧枯拉朽，军无斗志，纷纷溃退。",
 "主体第一层：交代战斗开始的时间、地点，描写国民党防线的崩溃——经营三个半月的防线在解放军面前不堪一击。",
 "对比手法：\u201c经营了三个半月\u201d写敌人准备之久，\u201c摧枯拉朽\u201d写崩溃之速，反差强烈；\u201c军无斗志，纷纷溃退\u201d以四字短语写出敌军溃败的狼狈，语言凝练有力。",
 [("午夜","半夜、夜里十二点前后"),("芜湖","安徽芜湖市，长江南岸重要港口"),("安庆","安徽安庆市，长江北岸重镇"),("经营","这里指筹划、修筑（防线），含贬义"),("摧枯拉朽","摧折枯草朽木，比喻迅速摧毁腐朽势力"),("溃退","（军队）被打垮而后退")]),

(4, "长江风平浪静，我军万船齐放，直取对岸，不到二十四小时，三十万人民解放军即已突破敌阵，占领南岸广大地区，现正向繁昌、铜陵、青阳、荻港、鲁港诸城进击中。",
 "主体第二层：描写我军渡江的壮阔场面和神速进展——万船齐放、突破敌阵、占领南岸、乘胜追击，一气呵成。",
 "场面描写气势磅礴：\u201c风平浪静\u201d反衬我军从容，\u201c万船齐放\u201d写声势浩大；\u201c不到二十四小时\u201d\u201c即已\u201d\u201c现正\u201d三个时间词层层推进，体现进军神速；连用五个地名，写出进军范围之广。",
 [("万船齐放","成千上万条船同时出发，形容声势浩大"),("直取","直接攻取，不含糊"),("突破","集中兵力向一点进攻，打开缺口"),("繁昌","安徽繁昌县（今繁昌区），长江南岸"),("铜陵","安徽铜陵市，长江南岸"),("青阳","安徽青阳县，长江南岸"),("荻港","安徽繁昌县荻港镇，长江重要渡口"),("鲁港","安徽芜湖市鲁港镇，长江南岸港口"),("进击","进攻、攻击")]),

(5, "人民解放军正以自己的英雄式的战斗，坚决地执行毛主席朱总司令的命令。",
 "结语：以议论收束，赞扬人民解放军的英雄战斗精神，点明渡江作战是执行毛泽东、朱德的进军命令。",
 "结语从叙述转向议论，\u201c英雄式的战斗\u201d高度评价，\u201c坚决地执行\u201d表明全军上下令行禁止，与导语\u201c英勇\u201d呼应，使全文气势贯通，收束有力。",
 [("英雄式","像英雄一样的，形容战斗英勇无畏"),("坚决","确定不移、不犹豫"),("执行","依照政策、命令等去做"),("朱总司令","朱德，当时任中国人民解放军总司令")]),
]

# ---------- 赏析区 ----------
APP = [
("新闻文体特点", [
    ("准确性：数字精确，事实确凿",
     "全文用数字说话：\u201c大约三十万人\u201d\u201c三个半月\u201d\u201c不到二十四小时\u201d，时间、地点、人数精确到可查。\u201c大约\u201d一词更见严谨——三十万是约数，不夸大不缩小，体现了消息\u201c用事实说话\u201d的基本原则。"),
    ("时效性：电头精确到小时",
     "电头\u201c二十二日二时电\u201d，渡江战斗二十日午夜开始，二十二日凌晨即发稿，间隔不到一天。在无线电报时代，这样的发稿速度极为惊人，充分体现了消息\u201c快\u201d的特点。"),
    ("简洁性：不足二百字报道重大战役",
     "全文仅约180字，却报道了渡江战役这一重大历史事件。没有多余的修饰，每一句都承载信息。导语一句概括核心，主体两句展开战况，结语一句升华，结构紧凑，惜墨如金。"),
    ("倾向性：字里行间的爱憎褒贬",
     "写我军用\u201c英勇\u201d\u201c万船齐放\u201d\u201c英雄式的战斗\u201d，褒扬之情溢于言表；写敌军用\u201c摧枯拉朽\u201d\u201c军无斗志\u201d\u201c纷纷溃退\u201d，贬斥之意鲜明。消息虽以客观叙述为主，但立场和倾向通过选词自然流露。"),
]),
("艺术特色", [
    ("对比鲜明，反差强烈",
     "敌军\u201c经营了三个半月\u201d的防线，在解放军面前\u201c好似摧枯拉朽\u201d；敌人\u201c军无斗志，纷纷溃退\u201d，我军\u201c万船齐放，直取对岸\u201d。敌我对比中，胜败之势一目了然。"),
    ("节奏明快，气势磅礴",
     "多用短句和四字短语：\u201c摧枯拉朽\u201d\u201c军无斗志\u201d\u201c纷纷溃退\u201d\u201c万船齐放\u201d\u201c直取对岸\u201d，读来铿锵有力，如战鼓催征，与渡江战役的壮阔场面相得益彰。"),
    ("结构完整，层次清晰",
     "严格遵循消息\u201c倒金字塔\u201d结构：导语最重要的事实在前，主体按战斗进程展开，结语升华主题。读者即使只读第一句，也能获知核心信息。"),
]),
("主题思想", [
    ("",
     "这则消息通过报道人民解放军三十万人胜利渡过长江的战况，歌颂了人民解放军英勇无畏的战斗精神和革命英雄主义气概，宣告了国民党长江防线的彻底崩溃，展示了解放战争胜利进军的磅礴气势，极大地鼓舞了全国人民夺取最后胜利的信心。"),
]),
]

# ---------- 积累区 ----------
ACC = [
("重点词语", [
    ("摧枯拉朽","摧折枯草朽木，比喻迅速摧毁腐朽势力。枯，枯草；朽，朽木。"),
    ("溃退","（军队）被打垮而后退。溃，散乱、垮台。"),
    ("经营","这里指筹划、修筑（防线），含贬义。"),
    ("风平浪静","没有风浪，水面很平静，比喻平静无事。"),
    ("万船齐放","成千上万条船同时出发，形容声势浩大。"),
    ("直取","直接攻取，不含糊、不绕弯。"),
    ("突破","集中兵力向一点进攻，打开缺口。"),
    ("进击","进攻、攻击。"),
    ("英雄式","像英雄一样的，形容战斗英勇无畏。"),
    ("坚决","确定不移、不犹豫。"),
]),
("用字与读音", [
    ("荻港","（dí gǎng）地名，在安徽繁昌。荻，多年生草本植物，生在水边。"),
    ("铜陵","（líng）安徽铜陵市。陵，大土山。"),
    ("溃退","（kuì）被打垮而后退。不要读成\u201c贵\u201d。"),
    ("摧枯拉朽","（cuī kū lā xiǔ）摧折枯草朽木。朽，xiǔ，不要读成\u201c巧\u201d。"),
    ("芜湖","（wú）安徽芜湖市。芜，草长得多而乱。"),
    ("安庆","（qìng）安徽安庆市。庆，祝贺、庆祝。"),
]),
("修辞方法", [
    ("对比","敌军\u201c经营三个半月\u201d与我军\u201c摧枯拉朽\u201d对比；敌军\u201c纷纷溃退\u201d与我军\u201c万船齐放\u201d对比，突出我军的英勇和敌军的溃败。"),
    ("四字短语","\u201c摧枯拉朽\u201d\u201c军无斗志\u201d\u201c纷纷溃退\u201d\u201c风平浪静\u201d\u201c万船齐放\u201d，大量四字短语使语言凝练有力，节奏明快。"),
    ("褒贬色彩","写我军用褒义词（英勇、英雄式），写敌军用贬义词（摧枯拉朽、溃退），通过选词表达鲜明的立场和倾向。"),
]),
("写作借鉴", [
    ("倒金字塔结构","把最重要的信息放在最前面（导语），次要信息依次展开，让读者在最短时间内获取核心内容。"),
    ("用事实和数字说话","不空谈胜利，而是用\u201c三十万人\u201d\u201c不到二十四小时\u201d\u201c五个地名\u201d等具体事实和数字展现战果，真实可信。"),
    ("语言精练","全文不足二百字，没有一句多余的话。写新闻要学会删繁就简，每一个词都要有信息价值。"),
    ("立场鲜明","客观叙述中通过选词自然流露倾向，不喊口号，却爱憎分明。"),
]),
("文化常识", [
    ("渡江战役","1949年4月21日至6月2日，人民解放军在西起湖口、东至江阴的千里战线上强渡长江，解放南京、上海、武汉等大城市，推翻了国民党反动统治。"),
    ("消息五要素","时间（When）、地点（Where）、人物（Who）、事件（What）、原因（Why），加上经过（How），合称\u201c五W+H\u201d。"),
    ("电头","消息开头的说明文字，一般包括通讯社名称、发报地点和时间，如\u201c新华社长江前线二十二日二时电\u201d。"),
]),
]

# ---------- 题库 ----------
DICT_WORDS = [
    {"w":"朽","py":"xiǔ","q":"遇着人民解放军好似摧枯拉□，军无斗志","tip":"「朽」木字旁，腐烂；与「巧」（工字旁）区分"},
    {"w":"溃","py":"kuì","q":"军无斗志，纷纷□退","tip":"「溃」三点水，散乱垮台；与「馈」（食字旁）区分"},
    {"w":"荻","py":"dí","q":"现正向繁昌、铜陵、青阳、□港、鲁港诸城进击中","tip":"「荻」草字头，水生植物；与「狄」（反犬旁）区分"},
    {"w":"陵","py":"líng","q":"现正向繁昌、铜□、青阳、荻港、鲁港诸城进击中","tip":"「陵」左耳旁，大土山；与「凌」（两点水）区分"},
    {"w":"芜","py":"wú","q":"地点在□湖、安庆之间","tip":"「芜」草字头，杂草多；与「抚」（提手旁）区分"},
    {"w":"摧","py":"cuī","q":"遇着人民解放军好似□枯拉朽，军无斗志","tip":"「摧」提手旁，折断；与「催」（单人旁）区分"},
    {"w":"经营","py":"jīng yíng","q":"国民党反动派□□了三个半月的长江防线","tip":"「经」绞丝旁，「营」草字头；筹划修筑义"},
    {"w":"铜陵","py":"tóng líng","q":"现正向繁昌、□□、青阳、荻港、鲁港诸城进击中","tip":"「铜」金字旁，「陵」左耳旁；安徽城市名"},
]

DICT_NOTES = [
    {"w":"摧枯拉朽","a":"摧折枯草朽木，比喻迅速摧毁腐朽势力","q":"遇着人民解放军好似摧枯拉朽"},
    {"w":"溃退","a":"（军队）被打垮而后退","q":"军无斗志，纷纷溃退"},
    {"w":"经营","a":"这里指筹划、修筑（防线），含贬义","q":"国民党反动派经营了三个半月的长江防线"},
    {"w":"风平浪静","a":"没有风浪，水面很平静","q":"长江风平浪静"},
    {"w":"万船齐放","a":"成千上万条船同时出发，形容声势浩大","q":"我军万船齐放，直取对岸"},
    {"w":"直取","a":"直接攻取，不含糊","q":"我军万船齐放，直取对岸"},
    {"w":"突破","a":"集中兵力向一点进攻，打开缺口","q":"三十万人民解放军即已突破敌阵"},
    {"w":"进击","a":"进攻、攻击","q":"现正向繁昌、铜陵、青阳、荻港、鲁港诸城进击中"},
    {"w":"坚决","a":"确定不移、不犹豫","q":"坚决地执行毛主席朱总司令的命令"},
    {"w":"电头","a":"消息开头的说明文字，包括通讯社名称、发报地点和时间","q":"新华社长江前线二十二日二时电"},
    {"w":"导语","a":"消息的开头部分，用最简练的语言概括最重要的事实","q":"英勇的人民解放军二十一日已有大约三十万人渡过长江"},
    {"w":"英雄式","a":"像英雄一样的，形容战斗英勇无畏","q":"人民解放军正以自己的英雄式的战斗"},
]

# ================= 生成 =================

def annotate(text, notes):
    n = len(text)
    occ = [False] * n
    spans = []
    terms = []
    for word, note in notes:
        m = re.match(r"^(.*?)[（(]([^）)]*)[）)]$", word)
        if m:
            w0 = m.group(1)
            py = m.group(2)
            note = "\uff08" + py + "\uff09" + note
        else:
            w0 = word
        terms.append((w0, note))
    for w0, note in sorted(terms, key=lambda x: -len(x[0])):
        if w0 not in text:
            continue
        start = 0
        while True:
            i = text.find(w0, start)
            if i == -1:
                break
            if not any(occ[i:i + len(w0)]):
                spans.append((i, i + len(w0), w0, note))
                for k in range(i, i + len(w0)):
                    occ[k] = True
            start = i + len(w0)
    spans.sort()
    out, pos = [], 0
    for s, e, w, nt in spans:
        out.append(text[pos:s])
        nt_esc = nt.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
        out.append('<span class="anno-word" data-note="%s">%s</span>' % (nt_esc, w))
        pos = e
    out.append(text[pos:])
    return "".join(out)

def esc(t):
    return htmlmod.escape(t, quote=True)

# 解读区（短篇不分part）
jielu = []
fulltext = []
for (no, text, gk, sf, notes) in VERSES:
    fulltext.append('    <div class="pl">%s</div>' % esc(text))
    jielu.append('      <div class="verse" id="l%d" data-i="%d">' % (no, no - 1))
    jielu.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>'
                 % (no, annotate(text, notes)))
    jielu.append('        <details class="v-more">')
    jielu.append('          <summary>内容 · 手法</summary>')
    jielu.append('          <div class="d-body">')
    jielu.append('            <div class="v-sec"><b class="v-label">内容概括</b>')
    jielu.append('              <div class="v-trans">%s</div>' % esc(gk))
    jielu.append('            </div>')
    jielu.append('            <div class="v-sec"><b class="v-label">手法分析</b>')
    jielu.append('              <div class="d-body"><p>%s</p></div>' % esc(sf))
    jielu.append('            </div>')
    jielu.append('          </div>')
    jielu.append('        </details>')
    jielu.append('      </div>')

jielu = "\n".join(jielu)
fulltext = "\n".join(fulltext)

# 背景区
lead_html = "\n".join('    <p>%s</p>' % esc(p) for p in LEAD)
author_html = "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px;color:var(--ink2)\"" if i else "", esc(p))
                        for i, p in enumerate(AUTHOR))
bg_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' %
    (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:8px\"" if i else "", esc(par))
                           for i, par in enumerate(paras)))
    for (title, paras) in BG)
media_html = "".join(
    '      <div class="media">\n        <h4>%s</h4>\n        <iframe id="%s" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>\n        <a href="%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="%s">全屏播放</button>\n      </div>'
    % (esc(title), fid, bvid, esc(title), url, fid)
    for (title, bvid, url, fid) in VIDEOS)

# 赏析区
app_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n    <div class="fame">\n%s\n    </div>\n  </div>\n' %
    (esc(title), "\n".join(
        '      <div class="fame-card">\n        <div class="f-line">%s</div>\n        <p>%s</p>\n      </div>' %
        (esc(ft), esc(pc)) for (ft, pc) in items if title != "主题思想"))
    for (title, items) in APP if title != "主题思想")

theme_html = "".join(
    '  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' %
    (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px\"" if i else "", esc(pc))
                           for i, (ft, pc) in enumerate(items)))
    for (title, items) in APP if title == "主题思想")

# 积累区
acc_html = "".join(
    '  <div class="box">\n    <div class="acc-cat">\n      <h3>%s</h3>\n%s\n    </div>\n  </div>\n' %
    (esc(title), "\n".join('      <div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>'
                           % (esc(w), esc(d)) for (w, d) in items))
    for (title, items) in ACC)

hero = ('<header class="hero">\n  <div class="hero-side">%s</div>\n  <h1 class="hero-title">%s</h1>\n</header>' % (H, TITLE))

nav = '''<nav class="nav">
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
</nav>'''

main = '''<main class="wrap">
<section id="bg" class="sec">
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
%s
  </div>
  <div class="box">
    <h3>作者简介</h3>
%s
  </div>
%s  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
%s
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">消息结构 · 导语 · 主体</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
%s
  </div>
  <div class="verse-list" id="verseList">
%s
  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">文体 · 艺术 · 主题</span></div>
%s
%s</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 用字 · 修辞 · 写法 · 常识</span></div>
%s</section>

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
  <div class="kai">我三十万大军胜利南渡长江</div>
  <div>毛泽东 · 消息 · 1949年4月22日</div>
</footer>
</main>''' % (lead_html, author_html, bg_html, media_html, fulltext, jielu, app_html, theme_html, acc_html)

tail = '''<button class="top-btn" id="topBtn" title="回到顶部">↑</button>
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
</div>'''

dict_js = ("var DICT_WORDS = %s;\nvar DICT_NOTES = %s;\n"
           % (json.dumps(DICT_WORDS, ensure_ascii=False),
              json.dumps(DICT_NOTES, ensure_ascii=False)))

html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>我三十万大军胜利南渡长江 毛泽东</title>
<style>%s</style>
</head>
<body data-fs="100">

%s

%s

%s

%s

<script>
%s
</script>
<script>
%s</script>

</body>
</html>''' % (css, hero, nav, main, tail, main_js, dict_js)

open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, len(html), "chars")
print("verses:", len(VERSES))
print("word dict:", len(DICT_WORDS), "note dict:", len(DICT_NOTES))
