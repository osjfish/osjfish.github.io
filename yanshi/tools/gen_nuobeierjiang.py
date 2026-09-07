# -*- coding: utf-8 -*-
"""生成路透社《首届诺贝尔奖颁发》课件 HTML（消息类，外国作者）"""
import json, re, html as htmlmod

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\shojienuobeierjiangbanfa-loutoushe.html"

src = open(TEMPLATE, encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
mains = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = mains[0].replace("beiying_fs", "nuobeier_fs")

H = "英国 · 路透社"
TITLE = "首届诺贝尔奖颁发"

LEAD = [
    "1901年12月10日，是瑞典化学家诺贝尔逝世五周年的日子。这一天，首届诺贝尔奖在瑞典斯德哥尔摩和挪威奥斯陆同时颁发。诺贝尔奖是根据诺贝尔1895年立下的遗嘱设立的，旨在奖励过去一年中在物理学、化学、生理学或医学、文学及和平事业方面为人类做出最大贡献的人。",
    "这则消息由英国路透社发自斯德哥尔摩，及时报道了首届诺贝尔奖颁发的盛况。文章依次介绍了颁奖概况、六位获奖者的成就、颁奖机构与仪式安排，以及诺贝尔基金的来源与管理，结构清晰，信息准确，是一则典型的事件性消息。",
]

AUTHOR = [
    "路透社（Reuters）是世界上最古老、最著名的新闻通讯社之一，1851年由保罗·朱利叶斯·路透在英国伦敦创办。路透社以快速、准确、客观的新闻报道著称，在全球范围内拥有广泛的影响力，是国际新闻传播的重要渠道。",
    "这则消息是路透社1901年12月10日发自瑞典斯德哥尔摩的电讯报道，记录了首届诺贝尔奖颁发这一重大历史事件。消息语言简洁客观，信息丰富准确，体现了路透社一贯的新闻专业风格，也为后人了解诺贝尔奖的起源提供了珍贵的第一手资料。",
]

BG = [
    ("写作背景", [
        "诺贝尔遗嘱：1895年11月27日，瑞典化学家阿尔弗雷德·贝恩哈德·诺贝尔在巴黎立下遗嘱，将其大部分财产（约3100万瑞典克朗）设立基金，每年以利息奖励在物理学、化学、生理学或医学、文学及和平领域为人类做出最大贡献的人。",
        "首届颁奖：1901年12月10日（诺贝尔逝世五周年纪念日），首届诺贝尔奖在瑞典斯德哥尔摩和挪威奥斯陆同时颁发。物理学奖授予德国的伦琴，化学奖授予荷兰的范托夫，生理学或医学奖授予德国的贝林，文学奖授予法国的普吕多姆，和平奖授予瑞士的迪南和经济学家帕西。",
        "诺贝尔奖的影响：百余年来，诺贝尔奖已成为世界上最具影响力和权威性的科学文化奖项，激励着无数科学家、文学家和和平工作者为人类进步事业不懈奋斗。",
    ]),
    ("文体知识", [
        "事件性消息：以报道新近发生的重大事件为主要内容的消息，强调时效性和客观性。本文报道首届诺贝尔奖颁发，是典型的事件性消息。",
        "消息的背景材料：消息中常插入背景材料，帮助读者理解事件的来龙去脉。本文最后一段介绍诺贝尔的生平、基金来源和管理方式，属于背景材料，补充说明了诺贝尔奖的由来。",
        "消息的客观叙述：消息以客观叙述为主，不掺杂作者的主观感情和评价。本文用平实的语言介绍获奖者及其成就，不加褒贬，体现了消息\u201c用事实说话\u201d的特点。",
    ]),
]

VIDEOS = [
    ("课文朗读《首届诺贝尔奖颁发》",
     "BV1FA411Y7hV",
     "https://www.bilibili.com/video/BV1FA411Y7hV",
     "mediaF1"),
    ("天才简史：诺贝尔奖创立者诺贝尔的传奇故事",
     "BV18x41157tu",
     "https://www.bilibili.com/video/BV18x41157tu",
     "mediaF2"),
]

VERSES = [
(1, "斯德哥尔摩1901年12月10日电",
 "电头：交代发报地点和时间，斯德哥尔摩是瑞典首都，也是诺贝尔奖颁奖地。",
 "电头是消息的标志，\u201c斯德哥尔摩\u201d点明发报地点，\u201c1901年12月10日\u201d是诺贝尔逝世五周年纪念日，也是首届诺贝尔奖颁奖日，时间本身就有历史意义。",
 [("斯德哥尔摩","瑞典首都，诺贝尔奖颁奖地"),("电","电报、电讯稿件")]),

(2, "瑞典国王和挪威诺贝尔基金会今天首次颁发了诺贝尔奖。根据诺贝尔的遗嘱，诺贝尔奖每年发给那些在过去的一年里，在物理学、化学、生理学或医学、文学及和平事业方面为人类做出最大贡献的人。",
 "导语：概括核心事件——首届诺贝尔奖今天颁发，并说明诺贝尔奖的评选标准和五个奖项类别。",
 "导语开门见山，\u201c首次\u201d点明这是首届颁奖，具有历史意义。第二句引用诺贝尔遗嘱说明评选标准，\u201c为人类做出最大贡献\u201d是诺贝尔奖的核心宗旨。列举五个奖项类别，信息完整准确。",
 [("挪威","北欧国家，诺贝尔和平奖在挪威奥斯陆颁发"),("遗嘱","死者生前依法处理遗产或其他事务并于死亡时发生效力的法律行为"),("生理学","研究生物机体生命活动规律的科学"),("贡献","对国家或公众所做的有益的事")]),

(3, "今年诺贝尔奖的获得者有：德国的伦琴（物理学奖），他发现了X射线；荷兰的范托夫（化学奖），他发现了化学动力学定律和渗透压定律；德国的贝林（生理学或医学奖），他在血清疗法的研究方面卓有成就；法国的普吕多姆（文学奖），他在诗歌创作方面颇有建树；瑞士的迪南（和平奖），他于1864年建立了红十字会；经济学家帕西，他建立了促进国际仲裁的各国议会联盟。",
 "主体第一层（获奖者名单）：依次介绍六位首届诺贝尔奖获得者的国籍、姓名、奖项和主要成就。",
 "这一段是消息的核心内容，用排比句式依次介绍六位获奖者，每人一句，格式统一（国籍+姓名+奖项+成就），条理清晰。\u201c卓有成就\u201d\u201c颇有建树\u201d等词语客观评价获奖者的贡献，不夸大不缩小。括号注明奖项类别，信息准确。",
 [("伦琴","（1845—1923）德国物理学家，X射线的发现者"),("X射线","也称伦琴射线，一种波长很短的电磁波，有很强的穿透能力"),("范托夫","（1852—1911）荷兰化学家，物理化学的奠基人之一"),("化学动力学","研究化学反应速率和机理的学科"),("渗透压","溶液中的溶质微粒对半透膜产生的压力"),("贝林","（1854—1917）德国细菌学家、免疫学家，血清疗法的创始人"),("血清疗法","用含有抗体的血清治疗疾病的方法"),("卓有成就","有突出的成绩和效果。卓，突出"),("普吕多姆","（1839—1907）法国诗人，首届诺贝尔文学奖获得者"),("建树","建立的功绩、取得的成就"),("迪南","（1828—1910）瑞士人道主义者，红十字会的创始人"),("红十字会","国际性的志愿救护、救济团体"),("帕西","（1822—1912）法国经济学家、和平主义者"),("国际仲裁","通过仲裁方式和平解决国际争端"),("各国议会联盟","各国议会议员的国际组织，旨在促进国际合作与和平")]),

(4, "从即日起，根据诺贝尔的遗嘱，诺贝尔奖由4个机构（瑞典3个，挪威1个）颁发，从按诺贝尔遗嘱建立的基金中拨款。授奖仪式每年于12月10日诺贝尔逝世周年纪念日，在瑞典的斯德哥尔摩和挪威的奥斯陆举行。",
 "主体第二层（颁奖机构与仪式）：说明诺贝尔奖的颁发机构、资金来源和授奖仪式的时间地点。",
 "这一段补充说明诺贝尔奖的运作机制。\u201c4个机构（瑞典3个，挪威1个）\u201d用数字和括号精确说明，体现新闻语言的准确性。\u201c12月10日诺贝尔逝世周年纪念日\u201d点明颁奖日期的特殊意义，斯德哥尔摩和奥斯陆两地同时颁奖，与诺贝尔遗嘱中和平奖在挪威颁发的规定一致。",
 [("拨款","拨付或调出款项。拨，分出、调发"),("授奖仪式","颁发奖品、奖金的典礼"),("逝世","去世、死亡（多用于庄重场合）"),("周年纪念日","满一年的日子，这里指诺贝尔逝世的日子"),("奥斯陆","挪威首都，诺贝尔和平奖颁奖地")]),

(5, "1867年，瑞典化学家诺贝尔发明了黄色炸药，以后又发明了多种炸药，这使他获得巨额收入。1896年诺贝尔逝世，这笔巨款用来设立诺贝尔奖金。他留下来的资金每年的利息将支付这5种诺贝尔奖金。诺贝尔基金会是这笔资金的合法拥有者，并管理这笔资金的投资，但与诺贝尔奖的评定无关。诺贝尔奖的评议权属于瑞典和挪威的诺贝尔奖评委会。",
 "背景（诺贝尔与基金）：介绍诺贝尔的生平、基金来源、管理方式和评定权归属，补充说明诺贝尔奖的由来。",
 "这一段是消息的背景材料，按时间顺序叙述：1867年发明炸药→获得巨额收入→1896年逝世→遗产设立基金→利息支付奖金。最后两句明确区分基金会的管理权（管资金）和评委会的评议权（定获奖者），两者互不干涉，体现了诺贝尔奖运作的独立性和公正性。背景材料帮助读者理解事件的来龙去脉，是消息的重要组成部分。",
 [("黄色炸药","即硝化甘油炸药，诺贝尔1867年发明的安全炸药"),("巨额","数量极大的（钱财）。巨，大"),("巨款","数额巨大的款项"),("设立","成立、建立（组织、机构等）"),("利息","因存款、放款而得到的本金以外的钱"),("合法拥有者","依照法律规定享有所有权的人或机构"),("投资","把资金投入企业或基本建设以获取利润"),("评定","经过评判或审核来决定"),("评议权","经过讨论、评定来决定的权力"),("评委会","负责评审、评议的委员会")]),
]

APP = [
("新闻文体特点", [
    ("准确性：信息精确，事实清楚",
     "全文用精确的数字和事实展现信息：\u201c4个机构（瑞典3个，挪威1个）\u201d\u201c5种诺贝尔奖金\u201d\u201c1867年\u201d\u201c1896年\u201d\u201c12月10日\u201d，时间、数字、地点精确到可查。六位获奖者的国籍、姓名、奖项、成就一一对应，准确无误。括号补充说明奖项类别，信息完整。"),
    ("时效性：事件当天即发报道",
     "电头\u201c斯德哥尔摩1901年12月10日电\u201d，颁奖当天即发稿，在电报通讯时代已是最快速度。消息报道的是当天发生的重大事件，时效性极强。导语中\u201c今天首次颁发\u201d的\u201c今天\u201d一词，更凸显了新闻的即时性。"),
    ("客观性：平实叙述，不加褒贬",
     "全文以客观叙述为主，用平实的语言介绍获奖者及其成就，不掺杂作者的主观感情和评价。\u201c卓有成就\u201d\u201c颇有建树\u201d等词语是对获奖者贡献的客观描述，而非主观赞美。背景材料介绍诺贝尔生平和基金管理，同样客观中立，体现了消息\u201c用事实说话\u201d的特点。"),
    ("结构完整：导语主体背景层次分明",
     "严格遵循消息结构：导语概括颁奖事件和评选标准，主体依次介绍获奖者、颁奖机构与仪式，背景补充诺贝尔生平和基金来源。读者即使只读导语，也能获知核心信息；读完全文，则对诺贝尔奖的起源和运作有全面了解。"),
]),
("艺术特色", [
    ("排比句式，条理清晰",
     "介绍六位获奖者时，用排比句式\u201c德国的伦琴（物理学奖），他……；荷兰的范托夫（化学奖），他……\u201d，每人一句，格式统一，国籍、姓名、奖项、成就一一对应，读来条理清晰，信息密度高而不显杂乱。"),
    ("数字精确，信息丰富",
     "全文大量使用精确数字：\u201c4个机构（瑞典3个，挪威1个）\u201d\u201c5种诺贝尔奖金\u201d\u201c1867年\u201d\u201c1896年\u201d，数字本身就承载了丰富的信息。括号补充说明，使信息更加精确完整，体现了新闻语言\u201c准确\u201d的核心要求。"),
    ("背景巧妙，深化主题",
     "最后一段背景材料不是可有可无的附加内容，而是消息的有机组成部分。它解释了诺贝尔奖的资金来源（诺贝尔发明炸药的收入）、管理机制（基金会管资金、评委会定获奖者），帮助读者理解诺贝尔奖的独立性和公正性，也深化了\u201c为人类做出最大贡献\u201d的主题。"),
    ("语言平实，专业规范",
     "全文语言平实简洁，没有华丽的修辞和主观的抒情，符合消息的文体要求。专业术语（X射线、化学动力学、渗透压、血清疗法等）使用准确，体现了新闻报道的专业性。"),
]),
("主题思想", [
    ("",
     "这则消息通过报道首届诺贝尔奖颁发的盛况，介绍了六位获奖者的杰出成就和诺贝尔奖的评选标准、颁奖机制与基金来源，展现了诺贝尔奖\u201c奖励为人类做出最大贡献的人\u201d的崇高宗旨，也体现了新闻消息准确、及时、客观的文体特征。消息记录了这一重大历史事件，为后人了解诺贝尔奖的起源提供了珍贵的第一手资料。"),
]),
]

ACC = [
("重点词语", [
    ("遗嘱","死者生前依法处理遗产或其他事务并于死亡时发生效力的法律行为。"),
    ("贡献","对国家或公众所做的有益的事。"),
    ("卓有成就","有突出的成绩和效果。卓，突出。"),
    ("建树","建立的功绩、取得的成就。"),
    ("拨款","拨付或调出款项。拨，分出、调发。"),
    ("授奖","颁发奖品、奖金。授，交付、给予。"),
    ("逝世","去世、死亡（多用于庄重场合）。"),
    ("巨额","数量极大的（钱财）。巨，大。"),
    ("设立","成立、建立（组织、机构等）。"),
    ("利息","因存款、放款而得到的本金以外的钱。"),
    ("投资","把资金投入企业或基本建设以获取利润。"),
    ("评定","经过评判或审核来决定。"),
]),
("用字与读音", [
    ("遗嘱","（yí zhǔ）死者生前依法处理遗产的法律行为。遗，yí，不读wèi。"),
    ("渗透","（shèn tòu）液体从物体的细小空隙中透过。渗，shèn，不读cān。"),
    ("仲裁","（zhòng cái）双方争执不决时，由第三者居中调解裁决。仲，zhòng。"),
    ("逝世","（shì）去世。逝，shì，不读shé。"),
    ("巨额","（é）数量极大。额，é，不读è。"),
    ("拨款","（bō）拨付。拨，bō，不读bá。"),
    ("卓有成就","（zhuó）突出。卓，zhuó，不读zhuō。"),
]),
("修辞方法", [
    ("排比","介绍六位获奖者时，用\u201c国籍+姓名（奖项），他……\u201d的排比句式，每人一句，格式统一，条理清晰，信息密度高。"),
    ("列数字","全文大量使用精确数字：\u201c4个机构\u201d\u201c5种奖金\u201d\u201c1867年\u201d\u201c1896年\u201d，用数字准确说明事实，体现新闻语言的精确性。"),
    ("括号补充","\u201c（物理学奖）\u201d\u201c（瑞典3个，挪威1个）\u201d等括号补充说明，使信息更加精确完整，是新闻写作中常用的说明方法。"),
]),
("写作借鉴", [
    ("倒金字塔结构","导语概括核心事件（首届诺贝尔奖颁发），主体依次展开（获奖者、颁奖机构），背景补充说明（诺贝尔与基金），重要信息在前，次要信息在后。"),
    ("用事实和数字说话","不空谈诺贝尔奖的意义，而是用六位获奖者的具体成就、精确的数字和时间来展现事实，真实可信，客观中立。"),
    ("背景材料的运用","在消息末尾插入背景材料，介绍诺贝尔的生平和基金管理，帮助读者理解事件的来龙去脉，深化了主题。"),
    ("语言准确简洁","全文没有多余的修饰，每一个数字、每一个术语都准确无误。专业术语使用规范，体现了新闻报道的专业性。"),
]),
("文化常识", [
    ("诺贝尔奖","根据瑞典化学家诺贝尔的遗嘱设立的国际奖项，分物理学、化学、生理学或医学、文学、和平五个奖项（1968年增设经济学奖），每年12月10日诺贝尔逝世纪念日颁发。"),
    ("诺贝尔","（1833—1896）瑞典化学家、工程师，黄色炸药的发明者。他一生拥有355项专利，积累了巨额财富，逝世前立下遗嘱将大部分财产设立诺贝尔奖基金。"),
    ("伦琴与X射线","伦琴（1845—1923），德国物理学家，1895年发现X射线（伦琴射线），为医学和材料科学的发展做出了巨大贡献，是首届诺贝尔物理学奖获得者。"),
    ("红十字会","国际性的志愿救护、救济团体，1864年由瑞士人迪南发起创立，以白底红十字为标志，旨在战时救护伤兵、平时救济灾民。"),
]),
]

DICT_WORDS = [
    {"w":"遗","py":"yí","q":"根据诺贝尔的□嘱，诺贝尔奖每年发给那些在过去的一年里","tip":"「遗」走之底，遗留；不读wèi；与「遣」（qiǎn）区分"},
    {"w":"渗","py":"shèn","q":"他发现了化学动力学定律和□透压定律","tip":"「渗」三点水，液体透过；不读cān；与「惨」（cǎn）区分"},
    {"w":"仲","py":"zhòng","q":"他建立了促进国际□裁的各国议会联盟","tip":"「仲」单人旁，居中；不读zhōng；与「中」区分"},
    {"w":"逝","py":"shì","q":"1896年诺贝尔□世，这笔巨款用来设立诺贝尔奖金","tip":"「逝」走之底，死亡；不读shé；与「世」区分"},
    {"w":"额","py":"é","q":"这使他获得巨□收入","tip":"「额」页字旁，数额；不读è；与「客」（kè）区分"},
    {"w":"拨","py":"bō","q":"从按诺贝尔遗嘱建立的基金中□款","tip":"「拨」提手旁，分出调发；不读bá；与「拔」（bá）区分"},
    {"w":"卓","py":"zhuó","q":"他在血清疗法的研究方面□有成就","tip":"「卓」卜字旁，突出；不读zhuō；与「桌」区分"},
    {"w":"授","py":"shòu","q":"□奖仪式每年于12月10日诺贝尔逝世周年纪念日举行","tip":"「授」提手旁，交付给予；与「受」（接受）区分"},
]

DICT_NOTES = [
    {"w":"遗嘱","a":"死者生前依法处理遗产或其他事务并于死亡时发生效力的法律行为","q":"根据诺贝尔的遗嘱，诺贝尔奖每年发给那些在过去的一年里"},
    {"w":"贡献","a":"对国家或公众所做的有益的事","q":"在物理学、化学、生理学或医学、文学及和平事业方面为人类做出最大贡献的人"},
    {"w":"卓有成就","a":"有突出的成绩和效果","q":"他在血清疗法的研究方面卓有成就"},
    {"w":"建树","a":"建立的功绩、取得的成就","q":"他在诗歌创作方面颇有建树"},
    {"w":"拨款","a":"拨付或调出款项","q":"从按诺贝尔遗嘱建立的基金中拨款"},
    {"w":"授奖","a":"颁发奖品、奖金","q":"授奖仪式每年于12月10日诺贝尔逝世周年纪念日举行"},
    {"w":"逝世","a":"去世、死亡（多用于庄重场合）","q":"1896年诺贝尔逝世"},
    {"w":"巨额","a":"数量极大的（钱财）","q":"这使他获得巨额收入"},
    {"w":"设立","a":"成立、建立（组织、机构等）","q":"这笔巨款用来设立诺贝尔奖金"},
    {"w":"利息","a":"因存款、放款而得到的本金以外的钱","q":"他留下来的资金每年的利息将支付这5种诺贝尔奖金"},
    {"w":"评定","a":"经过评判或审核来决定","q":"但与诺贝尔奖的评定无关"},
    {"w":"仲裁","a":"双方争执不决时，由第三者居中调解裁决","q":"他建立了促进国际仲裁的各国议会联盟"},
    {"w":"渗透压","a":"溶液中的溶质微粒对半透膜产生的压力","q":"他发现了化学动力学定律和渗透压定律"},
    {"w":"血清疗法","a":"用含有抗体的血清治疗疾病的方法","q":"他在血清疗法的研究方面卓有成就"},
]

# ================= 生成 =================
def annotate(text, notes):
    n = len(text); occ = [False] * n; spans = []; terms = []
    for word, note in notes:
        m = re.match(r"^(.*?)[（(]([^）)]*)[）)]$", word)
        if m: w0 = m.group(1); note = "\uff08" + m.group(2) + "\uff09" + note
        else: w0 = word
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
    spans.sort(); out, pos = [], 0
    for s, e, w, nt in spans:
        out.append(text[pos:s])
        nt_esc = nt.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
        out.append('<span class="anno-word" data-note="%s">%s</span>' % (nt_esc, w))
        pos = e
    out.append(text[pos:])
    return "".join(out)

def esc(t): return htmlmod.escape(t, quote=True)

jielu = []; fulltext = []
for (no, text, gk, sf, notes) in VERSES:
    fulltext.append('    <div class="pl">%s</div>' % esc(text))
    jielu.append('      <div class="verse" id="l%d" data-i="%d">' % (no, no - 1))
    jielu.append('        <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (no, annotate(text, notes)))
    jielu.append('        <details class="v-more"><summary>内容 · 手法</summary><div class="d-body">')
    jielu.append('            <div class="v-sec"><b class="v-label">内容概括</b><div class="v-trans">%s</div></div>' % esc(gk))
    jielu.append('            <div class="v-sec"><b class="v-label">手法分析</b><div class="d-body"><p>%s</p></div></div>' % esc(sf))
    jielu.append('          </div></details></div>')
jielu = "\n".join(jielu); fulltext = "\n".join(fulltext)

lead_html = "\n".join('    <p>%s</p>' % esc(p) for p in LEAD)
author_html = "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px;color:var(--ink2)\"" if i else "", esc(p)) for i, p in enumerate(AUTHOR))
bg_html = "".join('  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' % (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:8px\"" if i else "", esc(par)) for i, par in enumerate(paras))) for (title, paras) in BG)
media_html = "".join('      <div class="media">\n        <h4>%s</h4>\n        <iframe id="%s" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>\n        <a href="%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="%s">全屏播放</button>\n      </div>' % (esc(title), fid, bvid, esc(title), url, fid) for (title, bvid, url, fid) in VIDEOS)
app_html = "".join('  <div class="box">\n    <h3>%s</h3>\n    <div class="fame">\n%s\n    </div>\n  </div>\n' % (esc(title), "\n".join('      <div class="fame-card">\n        <div class="f-line">%s</div>\n        <p>%s</p>\n      </div>' % (esc(ft), esc(pc)) for (ft, pc) in items if title != "主题思想")) for (title, items) in APP if title != "主题思想")
theme_html = "".join('  <div class="box">\n    <h3>%s</h3>\n%s\n  </div>\n' % (esc(title), "\n".join('    <p%s>%s</p>' % (" style=\"margin-top:10px\"" if i else "", esc(pc)) for i, (ft, pc) in enumerate(items))) for (title, items) in APP if title == "主题思想")
acc_html = "".join('  <div class="box">\n    <div class="acc-cat">\n      <h3>%s</h3>\n%s\n    </div>\n  </div>\n' % (esc(title), "\n".join('      <div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>' % (esc(w), esc(d)) for (w, d) in items)) for (title, items) in ACC)

hero = '<header class="hero">\n  <div class="hero-side">%s</div>\n  <h1 class="hero-title">%s</h1>\n</header>' % (H, TITLE)
nav = '''<nav class="nav"><div class="nav-in"><a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a><div class="tool"><select id="fsSel" class="fs-sel" title="正文字体大小"><option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option></select><button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button></div></div></nav>'''

main = '''<main class="wrap">
<section id="bg" class="sec"><div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div><div class="lead">%s</div><div class="box"><h3>作者简介</h3>%s</div>%s<div class="box media-box"><h3>视听</h3><div class="media-grid">%s</div></div></section>
<div class="divider"></div>
<section id="jielu" class="sec"><div class="sec-head"><h2>解 读</h2><span class="no">消息结构 · 导语 · 主体 · 背景</span></div><button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button><div id="fulltext" class="poem" style="display:none">%s</div><div class="verse-list" id="verseList">%s</div></section>
<div class="divider"></div>
<section id="app" class="sec"><div class="sec-head"><h2>赏 析</h2><span class="no">文体 · 艺术 · 主题</span></div>%s%s</section>
<div class="divider"></div>
<section id="acc" class="sec"><div class="sec-head"><h2>积 累</h2><span class="no">词语 · 用字 · 修辞 · 写法 · 常识</span></div>%s</section>
<div class="divider"></div>
<section id="practice" class="sec"><div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div><div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div><div class="ptools"><button data-mode="word" data-rand="5">随机五组字形</button><button data-mode="word" data-all="1">全部字形</button><button data-mode="note" data-rand="5">随机五组词语</button><button data-mode="note" data-all="1">全部词语</button></div></section>
<footer><div class="kai">首届诺贝尔奖颁发</div><div>路透社 · 消息 · 1901年12月10日</div></footer>
</main>''' % (lead_html, author_html, bg_html, media_html, fulltext, jielu, app_html, theme_html, acc_html)

tail = '''<button class="top-btn" id="topBtn" title="回到顶部">↑</button><div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div><div class="dictate" id="dictate" hidden><div class="dictate-top"><span class="dictate-mode" id="dictMode">字形听写</span><span class="dictate-progress" id="dictProgress">第 1 / 5 题</span><button class="dictate-fs" id="dictFsMinus">A−</button><button class="dictate-fs" id="dictFsPlus">A+</button><button class="dictate-exit" id="dictExit">退出</button></div><div class="dictate-card"><div class="dictate-py" id="dictPy"></div><div class="dictate-line" id="dictLine"></div><div class="dictate-hint" id="dictHint"></div><div class="dictate-ans" id="dictAnsBox" hidden><div class="dictate-word" id="dictWord"></div><div class="dictate-tip" id="dictTip"></div></div></div><div class="dictate-actions"><button id="dictPrev">上一题</button><button class="primary" id="dictShow">显示答案</button><button id="dictNext">下一题</button></div></div>'''

dict_js = "var DICT_WORDS = %s;\nvar DICT_NOTES = %s;\n" % (json.dumps(DICT_WORDS, ensure_ascii=False), json.dumps(DICT_NOTES, ensure_ascii=False))
html = '''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>首届诺贝尔奖颁发 路透社</title><style>%s</style></head><body data-fs="100">%s%s%s%s<script>%s</script><script>%s</script></body></html>''' % (css, hero, nav, main, tail, main_js, dict_js)

open(OUT, "w", encoding="utf-8").write(html)
print("written:", OUT, len(html), "chars")
print("verses:", len(VERSES), "word dict:", len(DICT_WORDS), "note dict:", len(DICT_NOTES))
