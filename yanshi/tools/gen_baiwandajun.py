# -*- coding: utf-8 -*-
"""生成毛泽东《人民解放军百万大军横渡长江》课件 HTML（消息类）"""
import json, re, html as htmlmod

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\renminjiefangjunbaiwandajunhengduchangjiang-maozedong.html"

src = open(TEMPLATE, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
mains = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = mains[0].replace("beiying_fs", "baiwandajun_fs")

H = "现代 · 毛泽东"
TITLE = "人民解放军百万大军横渡长江"

LEAD = [
    "1949年4月20日，国民党政府拒绝签订国内和平协定，和平谈判宣告破裂。4月21日，毛泽东主席和朱德总司令发布《向全国进军的命令》，人民解放军第二、第三野战军及第四野战军一部，在西起湖口、东至江阴的千里战线上强渡长江，发起了震惊中外的渡江战役。",
    "4月22日，毛泽东为新华社撰写了这则消息，全面报道百万大军横渡长江的战况。文章以磅礴的气势、精确的数字、清晰的层次，展现了人民解放军三路大军渡江作战的壮阔图景，宣告了国民党长江防线的彻底崩溃，是中国新闻史上的经典之作。",
]

AUTHOR = [
    "毛泽东（1893—1976），字润之，湖南湘潭人。中国共产党、中国人民解放军和中华人民共和国的主要缔造者和领导人，伟大的马克思主义者、无产阶级革命家、战略家和理论家。同时也是杰出的诗人和文章大家。",
    "毛泽东长期重视新闻宣传工作，曾亲自为新华社撰写和修改大量消息、评论。这则消息写于1949年4月22日22时，是渡江战役打响后最全面的一篇战况报道，与《我三十万大军胜利南渡长江》并称\u201c消息二则\u201d，充分体现了消息文体准确、及时、简洁的特点。",
]

BG = [
    ("写作背景", [
        "和谈破裂：1949年4月，国共双方在北平举行和平谈判。4月20日，国民党政府拒绝在《国内和平协定》上签字，和谈宣告破裂，人民解放军随即发起渡江战役。",
        "三路大军：渡江战役中，人民解放军分为中、西、东三路大军。中路军首先在安庆、芜湖间突破，西路军在九江、安庆段渡江，东路军在南京、江阴段作战，三路大军协同推进，形成千里渡江的壮阔局面。",
        "江阴要塞：江阴是长江下游的重要门户，国民党军在此设有要塞炮台，控制长江航道。人民解放军突破江阴要塞，封锁长江，切断了国民党军的退路和物资运输线。",
    ]),
    ("文体知识", [
        "消息的倒金字塔结构：把最重要的事实放在导语中，次要信息依次展开。本文导语概括百万大军渡江的总体战况，主体按中、西、东三路分别叙述，层次分明。",
        "消息的语言特点：准确、简洁、客观。用精确的数字（三十万、三十五万、三分之二）和具体的时间（二十日夜、二十一日下午五时）展现战况，不夸大不缩小。",
        "消息的倾向性：消息虽以客观叙述为主，但通过选词（英勇善战、锐不可当、纷纷溃退、毫无斗志）自然流露立场和爱憎，做到\u201c用事实说话\u201d。",
    ]),
]

VIDEOS = [
    ("课文朗读《人民解放军百万大军横渡长江》",
     "BV16Z4y1u7zT",
     "https://www.bilibili.com/video/BV16Z4y1u7zT",
     "mediaF1"),
    ("1949年纪录片《百万雄师下江南》",
     "BV1uK411X7ZH",
     "https://www.bilibili.com/video/BV1uK411X7ZH",
     "mediaF2"),
]

VERSES = [
(1, "新华社长江前线二十二日二十二时电",
 "电头：交代通讯社、发报地点和精确到小时的时间，体现消息的权威性和时效性。",
 "\u201c二十二日二十二时\u201d精确到小时，渡江战役二十一日发起，二十二日晚即发全面报道，发稿速度惊人。电头是消息的标志，也是新闻真实性的保证。",
 [("新华社","新华通讯社的简称，中国国家通讯社"),("长江前线","渡江战役前线指挥部"),("电","电讯稿件")]),

(2, "人民解放军百万大军，从一千余华里的战线上，冲破敌阵，横渡长江。西起九江（不含），东至江阴，均是人民解放军的渡江区域。",
 "导语：概括核心事实——百万大军在千里战线上横渡长江，点明战线的东西起止点。",
 "导语气势磅礴，\u201c百万大军\u201d\u201c一千余华里\u201d两个数字写出规模之大；\u201c冲破\u201d\u201c横渡\u201d两个动词写出攻势之猛。\u201c九江（不含）\u201d用括号精确说明战线起点，体现新闻语言的严谨。",
 [("华里","市里，1华里=500米"),("冲破","突破、冲垮"),("横渡","从江河的这一边渡到那一边"),("九江","江西九江市，长江南岸重要城市"),("不含","不包括，这里指战线西起九江以东地区"),("江阴","江苏江阴市，长江下游重要门户")]),

(3, "二十日夜起，长江北岸人民解放军中路军首先突破安庆、芜湖线，渡至繁昌、铜陵、青阳、荻港、鲁港地区，二十四小时内即已渡过三十万人。",
 "主体第一层（中路军）：交代中路军首先突破的时间、地点和战果——二十四小时内渡过三十万人。",
 "按时间顺序叙述，\u201c首先\u201d点明中路军是三路中最先突破的；\u201c二十四小时内即已\u201d强调速度之快；连用五个地名写出渡江范围之广。数字精确，事实清楚。",
 [("中路军","渡江战役中在安庆、芜湖间作战的部队"),("安庆","安徽安庆市，长江北岸重镇"),("芜湖","安徽芜湖市，长江南岸重要港口"),("渡至","渡江到达"),("繁昌","安徽繁昌区，长江南岸"),("铜陵","安徽铜陵市，长江南岸"),("青阳","安徽青阳县，长江南岸"),("荻港","安徽繁昌荻港镇，长江渡口"),("鲁港","安徽芜湖鲁港镇，长江南岸港口")]),

(4, "二十一日下午五时起，我西路军开始渡江，地点在九江、安庆段。至发电时止，该路三十五万人民解放军已渡过三分之二，余部二十三日可渡完。这一路现已占领贵池、殷家汇、东流、至德、彭泽之线的广大南岸阵地，正向南扩展中。",
 "主体第二层（西路军）：交代西路军渡江的时间、地点、进展和占领区域——三十五万已渡三分之二，正向南扩展。",
 "\u201c至发电时止\u201d是新闻语言的典型表达，说明数据截止到发稿时刻，体现准确性和时效性。\u201c三分之二\u201d用分数精确说明进度，\u201c余部二十三日可渡完\u201d给出预期，信息完整。连用五个地名写出占领区域之广。",
 [("西路军","渡江战役中在九江、安庆段作战的部队"),("至发电时止","到发这封电报的时候为止，新闻用语"),("该路","这一路（指西路军）"),("余部","剩余的部队"),("贵池","安徽贵池区，长江南岸"),("殷家汇","安徽池州殷汇镇，长江南岸"),("东流","安徽东至县东流镇，长江南岸"),("至德","安徽东至县，长江南岸"),("彭泽","江西彭泽县，长江南岸"),("阵地","军队为进行战斗而占据的位置")]),

(5, "和中路军所遇敌情一样，我西路军当面之敌亦纷纷溃退，毫无斗志，我军所遇之抵抗，甚为微弱。此种情况，一方面由于人民解放军英勇善战，锐不可当；另一方面，这和国民党反动派拒绝签订和平协定，有很大关系。国民党的广大官兵一致希望和平，不想再打了，听见南京拒绝和平，都很泄气。战犯汤恩伯二十一日到芜湖督战，不起丝毫作用。",
 "主体第三层（敌情分析）：分析西路军当面之敌溃退的原因——我军英勇善战，敌军厌战反战，和谈破裂动摇军心。",
 "这一段是消息中的议论和分析，从叙述转向原因剖析。\u201c一方面……另一方面……\u201d逻辑清晰，既写我军的英勇，又写敌军的厌战，还点出和谈破裂的政治原因。\u201c不起丝毫作用\u201d以讽刺笔法写汤恩伯督战的无效，见敌军败局已定。",
 [("当面之敌","正面对着的敌人"),("纷纷溃退","接二连三地被打垮后退"),("毫无斗志","丝毫没有战斗的意志"),("甚为微弱","非常微弱。甚，很、非常"),("英勇善战","勇敢出众，善于作战"),("锐不可当","勇往直前，不可抵挡。当，阻挡"),("和平协定","指1949年国共北平和谈拟定的《国内和平协定》"),("泄气","失去信心和劲头"),("战犯","发动非正义战争或在战争中犯严重罪行的人"),("汤恩伯","国民党军将领，时任京沪杭警备总司令"),("督战","在前线监督作战"),("丝毫","极其微小、一点点")]),

(6, "汤恩伯认为南京、江阴段防线是很巩固的，弱点只存在于南京、九江一线。不料正是汤恩伯到芜湖的那一天，东面防线又被我军突破了。我东路三十五万大军与西路同日同时发起渡江作战。所有预定计划，都已实现。至发电时止，我东路各军已大部渡过南岸，余部二十三日可以渡完。",
 "主体第四层（东路军）：写东路军突破东面防线的战况——与西路同日同时发起，预定计划全部实现，大部已渡南岸。",
 "\u201c不料\u201d一词带有讽刺意味，汤恩伯判断失误，恰恰在他督战的当天东路军突破了他认为\u201c很巩固\u201d的防线。\u201c所有预定计划，都已实现\u201d短句有力，见我军指挥正确、作战顺利。与西路军一样用\u201c至发电时止\u201d保证数据准确。",
 [("南京","江苏省会，当时国民党政府所在地"),("巩固","坚固、稳固"),("不料","没想到、出乎意料"),("东面防线","指南京、江阴段的国民党军防线"),("东路军","渡江战役中在南京、江阴段作战的部队"),("预定","预先决定或制定"),("大部","大部分")]),

(7, "此处敌军抵抗较为顽强，然在二十一日下午至二十二日下午的整天激战中，我已歼灭及击溃一切抵抗之敌，占领扬中、镇江、江阴诸县的广大地区，并控制江阴要塞，封锁长江。我军前锋，业已切断镇江、无锡段铁路线。",
 "主体第五层（东路军激战）：写东路军在激战中歼灭击溃敌军，占领广大地区，控制江阴要塞，封锁长江，切断铁路线。",
 "\u201c较为顽强\u201d与西路军\u201c甚为微弱\u201d形成对比，说明东路军遇到的抵抗更强，但结果仍是\u201c歼灭及击溃一切抵抗之敌\u201d，更见我军的英勇。\u201c控制\u201d\u201c封锁\u201d\u201c切断\u201d三个动词层层递进，写出我军的战略成果。结尾以切断铁路线收束，暗示敌军已无路可逃。",
 [("顽强","坚强、强硬"),("然","然而、但是（文言转折词）"),("歼灭","消灭（敌人）"),("击溃","打垮、打散"),("扬中","江苏扬中市，长江南岸"),("镇江","江苏镇江市，长江南岸重要城市"),("诸县","各县。诸，众、各"),("江阴要塞","江阴长江口的军事要塞，炮台控制长江航道"),("封锁","用强制力量使与外界断绝联系"),("前锋","先头部队、先锋"),("业已","已经（文言词）"),("切断","截断、断绝"),("无锡","江苏无锡市，京沪铁路重要城市")]),
]

APP = [
("新闻文体特点", [
    ("准确性：数字精确，事实确凿",
     "全文用精确的数字和时间展现战况：\u201c百万大军\u201d\u201c一千余华里\u201d\u201c三十万人\u201d\u201c三十五万\u201d\u201c三分之二\u201d，时间精确到\u201c二十一日下午五时\u201d\u201c二十二日二十二时\u201d。\u201c至发电时止\u201d两次出现，确保数据的时效性和准确性。\u201c九江（不含）\u201d用括号精确说明，不模糊不含糊。"),
    ("时效性：边战边报，同步更新",
     "渡江战役二十一日发起，二十二日晚即发全面报道，间隔不到两天。电头精确到\u201c二十二时\u201d，文中两次用\u201c至发电时止\u201d说明数据截止时刻，还给出\u201c余部二十三日可渡完\u201d的预期，真正做到了边战边报、同步更新。"),
    ("简洁性：不足六百字报道千里战线",
     "全文约580字，却报道了百万大军在千里战线上三路渡江的全面战况。没有一句多余的话，每一个数字、每一个地名都承载信息。导语一句概括全局，主体按三路分别叙述，层次分明，惜墨如金。"),
    ("倾向性：客观叙述中立场鲜明",
     "写我军用\u201c英勇善战\u201d\u201c锐不可当\u201d\u201c冲破敌阵\u201d，褒扬之情溢于言表；写敌军用\u201c纷纷溃退\u201d\u201c毫无斗志\u201d\u201c泄气\u201d，贬斥之意鲜明。\u201c不料\u201d\u201c不起丝毫作用\u201d带有讽刺意味。消息以客观叙述为主，但立场和倾向通过选词自然流露。"),
]),
("艺术特色", [
    ("层次清晰，三路并进",
     "主体按中、西、东三路大军的顺序分别叙述，每路都交代时间、地点、进展、战果，条理分明。中路军\u201c首先突破\u201d，西路军\u201c正向南扩展\u201d，东路军\u201c控制要塞、封锁长江\u201d，三路并进，形成千里渡江的壮阔图景。"),
    ("对比鲜明，突出我军英勇",
     "西路军\u201c所遇之抵抗，甚为微弱\u201d与东路军\u201c抵抗较为顽强\u201d对比，说明东路战况更激烈，但结果仍是\u201c歼灭及击溃一切抵抗之敌\u201d，更见我军英勇。敌军\u201c纷纷溃退\u201d与我军\u201c锐不可当\u201d对比，胜败之势一目了然。"),
    ("议论精当，深化主题",
     "在叙述西路军战况后，插入一段议论分析敌军溃退的原因：\u201c一方面由于人民解放军英勇善战，锐不可当；另一方面，这和国民党反动派拒绝签订和平协定，有很大关系。\u201d这段议论从军事和政治两个层面分析原因，深化了主题，也体现了消息\u201c用事实说话\u201d的特点。"),
    ("语言凝练，节奏有力",
     "多用短句和四字短语：\u201c冲破敌阵\u201d\u201c横渡长江\u201d\u201c纷纷溃退\u201d\u201c毫无斗志\u201d\u201c锐不可当\u201d，读来铿锵有力。\u201c所有预定计划，都已实现\u201d短句斩截，见我军指挥若定。"),
]),
("主题思想", [
    ("",
     "这则消息通过全面报道人民解放军百万大军横渡长江的战况，歌颂了人民解放军英勇善战、锐不可当的革命英雄主义精神，宣告了国民党长江防线的彻底崩溃和国民党反动统治的即将覆灭，展示了革命战争胜利进军的磅礴气势，极大地鼓舞了全国人民夺取最后胜利的信心和决心。"),
]),
]

ACC = [
("重点词语", [
    ("锐不可当","勇往直前，不可抵挡。当，阻挡。"),
    ("溃退","（军队）被打垮而后退。溃，散乱、垮台。"),
    ("毫无斗志","丝毫没有战斗的意志。毫，细长而尖的毛，比喻极小的量。"),
    ("泄气","失去信心和劲头。"),
    ("督战","在前线监督作战。督，监督、指挥。"),
    ("歼灭","消灭（敌人）。歼，消灭。"),
    ("击溃","打垮、打散。"),
    ("要塞","军事上有重要意义的、有巩固防御设备的据点。"),
    ("封锁","用强制力量使与外界断绝联系。"),
    ("业已","已经（文言词）。"),
    ("预定","预先决定或制定。"),
    ("正面","这里指面对面的、直接的。"),
]),
("用字与读音", [
    ("荻港","（dí gǎng）地名，在安徽繁昌。荻，多年生草本植物，生在水边。"),
    ("殷家汇","（yīn）地名，在安徽池州。殷，富裕、深厚。"),
    ("彭泽","（péng zé）江西彭泽县。泽，水积聚的地方。"),
    ("歼灭","（jiān）消灭。不要读成\u201c千\u201d。"),
    ("击溃","（kuì）打垮。不要读成\u201c贵\u201d。"),
    ("锐不可当","（dāng）阻挡。不要读成\u201c档\u201d（dàng）。"),
    ("要塞","（sài）边界上的险要地方。不要读成\u201c塞子\u201d的sāi。"),
    ("江阴","（yīn）水的南面、山的北面。江阴在长江南岸。"),
]),
("修辞方法", [
    ("对比","西路军\u201c抵抗甚为微弱\u201d与东路军\u201c抵抗较为顽强\u201d对比；我军\u201c锐不可当\u201d与敌军\u201c纷纷溃退\u201d对比，突出我军的英勇和敌军的溃败。"),
    ("四字短语","\u201c冲破敌阵\u201d\u201c横渡长江\u201d\u201c纷纷溃退\u201d\u201c毫无斗志\u201d\u201c英勇善战\u201d\u201c锐不可当\u201d，大量四字短语使语言凝练有力，节奏明快。"),
    ("褒贬色彩","写我军用褒义词（英勇善战、锐不可当），写敌军用贬义词（纷纷溃退、毫无斗志、泄气），通过选词表达鲜明的立场和倾向。"),
    ("讽刺","\u201c不料正是汤恩伯到芜湖的那一天，东面防线又被我军突破了\u201d\u201c不起丝毫作用\u201d，以讽刺笔法写汤恩伯的判断失误和督战无效。"),
]),
("写作借鉴", [
    ("倒金字塔结构","把最重要的信息放在导语中（百万大军横渡长江），次要信息按中、西、东三路依次展开，让读者在最短时间内获取核心内容。"),
    ("用数字和事实说话","不空谈胜利，而是用\u201c三十万\u201d\u201c三十五万\u201d\u201c三分之二\u201d\u201c二十四小时\u201d等精确数字和具体地名展现战果，真实可信。"),
    ("记叙中穿插议论","在叙述西路军战况后，插入一段议论分析敌军溃退的原因，从军事和政治两个层面深化主题，避免了纯记叙的单调。"),
    ("语言准确简洁","全文不足六百字，没有一句多余的话。\u201c至发电时止\u201d\u201c九江（不含）\u201d等表达体现了新闻语言的严谨和精确。"),
]),
("文化常识", [
    ("渡江战役","1949年4月21日至6月2日，人民解放军在西起湖口、东至江阴的千里战线上强渡长江，解放南京、上海、武汉等大城市，推翻了国民党反动统治。"),
    ("消息六要素","时间（When）、地点（Where）、人物（Who）、事件（What）、原因（Why）、经过（How），合称\u201c五W+H\u201d。"),
    ("江阴要塞","江阴位于长江下游南岸，江面较窄，国民党军在此设有要塞炮台，控制长江航道，是长江下游的重要军事门户。"),
    ("汤恩伯","（1900—1954）国民党军将领，浙江金华人。解放战争时期任京沪杭警备总司令，指挥国民党军在长江下游的防御。"),
]),
]

DICT_WORDS = [
    {"w":"荻","py":"dí","q":"渡至繁昌、铜陵、青阳、□港、鲁港地区","tip":"「荻」草字头，水生植物；与「狄」（反犬旁）区分"},
    {"w":"殷","py":"yīn","q":"这一路现已占领贵池、□家汇、东流、至德、彭泽之线","tip":"「殷」殳字旁，富裕深厚；与「烟」（火字旁）区分"},
    {"w":"彭","py":"péng","q":"占领贵池、殷家汇、东流、至德、□泽之线的广大南岸阵地","tip":"「彭」右耳旁，姓氏地名；与「澎」（三点水）区分"},
    {"w":"泽","py":"zé","q":"占领贵池、殷家汇、东流、至德、彭□之线的广大南岸阵地","tip":"「泽」三点水，水积聚处；与「择」（提手旁）区分"},
    {"w":"歼","py":"jiān","q":"我已□灭及击溃一切抵抗之敌","tip":"「歼」歹字旁，消灭；不要读成「千」"},
    {"w":"溃","py":"kuì","q":"我西路军当面之敌亦纷纷□退，毫无斗志","tip":"「溃」三点水，散乱垮台；与「馈」（食字旁）区分"},
    {"w":"当","py":"dāng","q":"一方面由于人民解放军英勇善战，锐不可□","tip":"「当」阻挡义读dāng；不要读成dàng（恰当）"},
    {"w":"塞","py":"sài","q":"并控制江阴要□，封锁长江","tip":"「塞」边界险要处读sài；不要读成sāi（塞子）"},
    {"w":"阴","py":"yīn","q":"并控制江□要塞，封锁长江","tip":"「阴」左耳旁，水南山北；江阴在长江南岸；与「荫」（草字头）区分"},
    {"w":"锐不可当","py":"ruì bù kě dāng","q":"一方面由于人民解放军英勇善战，□□□□","tip":"「锐」金字旁，锋利；「当」阻挡，读dāng"},
]

DICT_NOTES = [
    {"w":"锐不可当","a":"勇往直前，不可抵挡","q":"一方面由于人民解放军英勇善战，锐不可当"},
    {"w":"溃退","a":"（军队）被打垮而后退","q":"我西路军当面之敌亦纷纷溃退"},
    {"w":"毫无斗志","a":"丝毫没有战斗的意志","q":"我西路军当面之敌亦纷纷溃退，毫无斗志"},
    {"w":"泄气","a":"失去信心和劲头","q":"听见南京拒绝和平，都很泄气"},
    {"w":"督战","a":"在前线监督作战","q":"战犯汤恩伯二十一日到芜湖督战"},
    {"w":"歼灭","a":"消灭（敌人）","q":"我已歼灭及击溃一切抵抗之敌"},
    {"w":"击溃","a":"打垮、打散","q":"我已歼灭及击溃一切抵抗之敌"},
    {"w":"要塞","a":"军事上有重要意义的、有巩固防御设备的据点","q":"并控制江阴要塞，封锁长江"},
    {"w":"封锁","a":"用强制力量使与外界断绝联系","q":"并控制江阴要塞，封锁长江"},
    {"w":"业已","a":"已经（文言词）","q":"我军前锋，业已切断镇江、无锡段铁路线"},
    {"w":"至发电时止","a":"到发这封电报的时候为止，新闻用语","q":"至发电时止，该路三十五万人民解放军已渡过三分之二"},
    {"w":"预定","a":"预先决定或制定","q":"所有预定计划，都已实现"},
    {"w":"英勇善战","a":"勇敢出众，善于作战","q":"一方面由于人民解放军英勇善战"},
    {"w":"丝毫","a":"极其微小、一点点","q":"不起丝毫作用"},
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
            w0 = m.group(1); py = m.group(2)
            note = "\uff08" + py + "\uff09" + note
        else:
            w0 = word
        terms.append((w0, note))
    for w0, note in sorted(terms, key=lambda x: -len(x[0])):
        if w0 not in text: continue
        start = 0
        while True:
            i = text.find(w0, start)
            if i == -1: break
            if not any(occ[i:i + len(w0)]):
                spans.append((i, i + len(w0), w0, note))
                for k in range(i, i + len(w0)): occ[k] = True
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

jielu = []
fulltext = []
for (no, text, gk, sf, notes) in VERSES:
    fulltext.append('    <div class="pl">%s</div>' % esc(text))
    jielu.append('      <div class="verse" id="l%d" data-i="%d">' % (no, no - 1))
    jielu.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (no, annotate(text, notes)))
    jielu.append('        <details class="v-more"><summary>内容 · 手法</summary><div class="d-body">')
    jielu.append('            <div class="v-sec"><b class="v-label">内容概括</b><div class="v-trans">%s</div></div>' % esc(gk))
    jielu.append('            <div class="v-sec"><b class="v-label">手法分析</b><div class="d-body"><p>%s</p></div></div>' % esc(sf))
    jielu.append('          </div></details></div>')

jielu = "\n".join(jielu)
fulltext = "\n".join(fulltext)

lead_html = "\n".join('    <p>%s</p>' % esc(p) for p in LEAD)
author_html = "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px;color:var(--ink2)\"" if i else "", esc(p)) for i, p in enumerate(AUTHOR))
bg_html = "".join('  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' % (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:8px\"" if i else "", esc(par)) for i, par in enumerate(paras))) for (title, paras) in BG)
media_html = "".join('      <div class="media">\n        <h4>%s</h4>\n        <iframe id="%s" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>\n        <a href="%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="%s">全屏播放</button>\n      </div>' % (esc(title), fid, bvid, esc(title), url, fid) for (title, bvid, url, fid) in VIDEOS)

app_html = "".join('  <div class="box">\n    <h3>%s</h3>\n    <div class="fame">\n%s\n    </div>\n  </div>\n' % (esc(title), "\n".join('      <div class="fame-card">\n        <div class="f-line">%s</div>\n        <p>%s</p>\n      </div>' % (esc(ft), esc(pc)) for (ft, pc) in items if title != "主题思想")) for (title, items) in APP if title != "主题思想")
theme_html = "".join('  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' % (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px\"" if i else "", esc(pc)) for i, (ft, pc) in enumerate(items))) for (title, items) in APP if title == "主题思想")
acc_html = "".join('  <div class="box">\n    <div class="acc-cat">\n      <h3>%s</h3>\n%s\n    </div>\n  </div>\n' % (esc(title), "\n".join('      <div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>' % (esc(w), esc(d)) for (w, d) in items)) for (title, items) in ACC)

hero = '<header class="hero">\n  <div class="hero-side">%s</div>\n  <h1 class="hero-title">%s</h1>\n</header>' % (H, TITLE)
nav = '''<nav class="nav"><div class="nav-in">
    <a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a>
    <div class="tool"><select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option></select>
      <button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button></div></div></nav>'''

main = '''<main class="wrap">
<section id="bg" class="sec"><div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">%s</div>
  <div class="box"><h3>作者简介</h3>%s</div>
%s  <div class="box media-box"><h3>视听</h3><div class="media-grid">%s</div></div>
</section>
<div class="divider"></div>
<section id="jielu" class="sec"><div class="sec-head"><h2>解 读</h2><span class="no">消息结构 · 导语 · 三路主体</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">%s</div>
  <div class="verse-list" id="verseList">%s</div>
</section>
<div class="divider"></div>
<section id="app" class="sec"><div class="sec-head"><h2>赏 析</h2><span class="no">文体 · 艺术 · 主题</span></div>
%s%s</section>
<div class="divider"></div>
<section id="acc" class="sec"><div class="sec-head"><h2>积 累</h2><span class="no">词语 · 用字 · 修辞 · 写法 · 常识</span></div>
%s</section>
<div class="divider"></div>
<section id="practice" class="sec"><div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>
  <div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>
  <div class="ptools"><button data-mode="word" data-rand="5">随机五组字形</button><button data-mode="word" data-all="1">全部字形</button><button data-mode="note" data-rand="5">随机五组词语</button><button data-mode="note" data-all="1">全部词语</button></div>
</section>
<footer><div class="kai">人民解放军百万大军横渡长江</div><div>毛泽东 · 消息 · 1949年4月22日</div></footer>
</main>''' % (lead_html, author_html, bg_html, media_html, fulltext, jielu, app_html, theme_html, acc_html)

tail = '''<button class="top-btn" id="topBtn" title="回到顶部">↑</button>
<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>
<div class="dictate" id="dictate" hidden><div class="dictate-top">
  <span class="dictate-mode" id="dictMode">字形听写</span><span class="dictate-progress" id="dictProgress">第 1 / 5 题</span>
  <button class="dictate-fs" id="dictFsMinus">A−</button><button class="dictate-fs" id="dictFsPlus">A+</button>
  <button class="dictate-exit" id="dictExit">退出</button></div>
  <div class="dictate-card"><div class="dictate-py" id="dictPy"></div><div class="dictate-line" id="dictLine"></div>
  <div class="dictate-hint" id="dictHint"></div>
  <div class="dictate-ans" id="dictAnsBox" hidden><div class="dictate-word" id="dictWord"></div><div class="dictate-tip" id="dictTip"></div></div></div>
  <div class="dictate-actions"><button id="dictPrev">上一题</button><button class="primary" id="dictShow">显示答案</button><button id="dictNext">下一题</button></div></div>'''

dict_js = "var DICT_WORDS = %s;\nvar DICT_NOTES = %s;\n" % (json.dumps(DICT_WORDS, ensure_ascii=False), json.dumps(DICT_NOTES, ensure_ascii=False))

html = '''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>人民解放军百万大军横渡长江 毛泽东</title><style>%s</style></head><body data-fs="100">
%s%s%s%s<script>%s</script><script>%s</script></body></html>''' % (css, hero, nav, main, tail, main_js, dict_js)

open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, len(html), "chars")
print("verses:", len(VERSES), "word dict:", len(DICT_WORDS), "note dict:", len(DICT_NOTES))
