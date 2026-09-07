# -*- coding: utf-8 -*-
"""生成《风雨吟》芦荻课件（短篇现代诗，逐句解读）。"""
import io, json, re

SRC = r"D:\App\Apps\yanshi\zuguoawoqinaidezuguo-shuting.html"
OUT = r"D:\App\Apps\yanshi\fengyuyin-ludi.html"
LS_KEY = "fengyuyin_fs"

LQ = "\u201c"
RQ = "\u201d"

def A(word, note):
    return '<span class="anno-word" data-note="%s">%s</span>' % (note, word)

CARDS = [
("风从大地" + A("卷","席卷，写出风的磅礴气势与裹挟一切的力量") + "来，",
 "首句写风：大风从大地上席卷而来，气势磅礴，不可阻挡。",
 LQ + "卷" + RQ + "是全诗的关键字——它不仅写出了风的形态，更写出了风的力量：席卷一切、裹挟一切、摧枯拉朽。" + LQ + "从大地" + RQ + "点明风的来源——不是从天空吹来，而是从大地上卷起，暗示这场风雨与大地、与人民息息相关。"),
("雨从大地" + A("奔","奔腾，写出雨的迅猛、急促与不可阻挡") + "来。",
 "次句写雨：暴雨从大地上奔腾而来，迅猛急促，不可阻挡。",
 LQ + "奔" + RQ + "与上句的" + LQ + "卷" + RQ + "对仗，写出了雨的迅猛和不可阻挡；两句" + LQ + "风从大地卷来，雨从大地奔来" + RQ + "构成对偶，句式整齐，气势磅礴，极力渲染了风雨的猛烈和大地的动荡。这两句不仅是写自然风雨，更是象征抗战时期动荡的社会现实。"),
(A("郊原","郊外的原野") + "如" + A("海","大海，比喻广阔无边") + "，",
 "第三句由风雨转向大地：郊外的原野在风雨中广阔无边，如同大海一般。",
 LQ + "郊原如海" + RQ + "是一个精妙的比喻——将风雨中的郊原比作波涛汹涌的大海，既写出了郊原的广阔无边，也写出了风雨中大地的动荡不安。这一句为下一句" + LQ + "房舍如舟" + RQ + "做了铺垫：既然郊原是海，那么房舍自然就是海中的舟了。"),
(A("房舍","房屋、住宅") + "如" + A("舟","小船") + "。",
 "第四句继续比喻：大地上的房屋在风雨中如同大海上的小船，飘摇不定。",
 LQ + "房舍如舟" + RQ + "与上句" + LQ + "郊原如海" + RQ + "构成对偶和递进——郊原是海，房舍是舟，那么人呢？人自然就是舟上的舵手了。这两句比喻不仅写出了风雨中大地的动荡和人民的飘摇，更为下文" + LQ + "年轻舵手" + RQ + "的出场做了完美的铺垫。"),
("我有" + A("年轻","年纪不大，这里指充满朝气和力量") + A("舵手","掌舵的人，比喻把握方向的领导者") + "的心，",
 "第五句由景入人：" + LQ + "我" + RQ + "有一颗年轻舵手的心——在风雨如晦的时代，" + LQ + "我" + RQ + "愿做把握方向的舵手。",
 LQ + "年轻舵手" + RQ + "是全诗的核心意象——" + LQ + "年轻" + RQ + "代表朝气、力量和希望，" + LQ + "舵手" + RQ + "代表责任、担当和方向。" + LQ + "我有年轻舵手的心" + RQ + "意味着" + LQ + "我" + RQ + "虽然可能还不是真正的舵手，但" + LQ + "我" + RQ + "有一颗舵手的心——有担当的勇气和把握方向的信念。这是一代青年在抗战时期发出的铮铮誓言。"),
("在大地风雨的海上。",
 "末句收束全诗：" + LQ + "我" + RQ + "在大地风雨的海上——在动荡的时代中，" + LQ + "我" + RQ + "愿做乘风破浪的舵手。",
 LQ + "大地风雨的海上" + RQ + "将前面的意象全部收拢——" + LQ + "大地" + RQ + "是首句的" + LQ + "大地" + RQ + "，" + LQ + "风雨" + RQ + "是题目和前两句的" + LQ + "风雨" + RQ + "，" + LQ + "海" + RQ + "是第三句的" + LQ + "海" + RQ + "。三个意象叠加在一起，构成了全诗的核心意境：在风雨如晦的大地上，在动荡不安的时代中，" + LQ + "我" + RQ + "愿做年轻的舵手，乘风破浪，把握方向。这一句将个人的担当与时代的命运紧密联系在一起，使全诗的主题得到升华。"),
]

FULLTEXT = [
 "风从大地卷来，",
 "雨从大地奔来。",
 "郊原如海，",
 "房舍如舟。",
 "我有年轻舵手的心，",
 "在大地风雨的海上。",
]

BG_LEAD = [
 "《风雨吟》是芦荻的代表作，1941年12月写于抗日战争最艰苦的时期。全诗仅六句，却以磅礴的气势、精妙的比喻和深刻的象征，描绘了风雨中大地的动荡，表达了一代青年在民族危亡之际勇于担当、乘风破浪的誓言。",
 "诗歌以" + LQ + "风从大地卷来，雨从大地奔来" + RQ + "开篇，极力渲染风雨的猛烈；继而以" + LQ + "郊原如海，房舍如舟" + RQ + "两个精妙的比喻，将风雨中的大地比作波涛汹涌的大海，将房舍比作飘摇的小舟；最后以" + LQ + "我有年轻舵手的心，在大地风雨的海上" + RQ + "收束，表达了青年一代在动荡时代中勇于担当的精神。全诗气势磅礴，意境雄浑，是抗战时期最具代表性的诗歌之一。",
]

AUTHOR = [
 "芦荻（1912—1994），原名陈培迪，广东南海人，中国现代诗人。1930年代开始发表诗歌作品，是抗战时期重要的诗人之一。曾任中国作家协会广东分会副主席、广东文学院院长等职。",
 "芦荻的诗歌风格雄浑豪放，善于以磅礴的气势和精妙的意象表达对时代的感受和对民族命运的关切。抗战时期，他积极投身抗日救亡运动，写下了大量反映抗战现实、鼓舞民族精神的诗歌。主要作品有诗集《桑野》《驰驱集》《远讯》《旗下高歌》等。1994年，芦荻在广州逝世，享年82岁。",
]

STORY = [
 ("写作背景","1941年12月，正值抗日战争最艰苦的时期。日军发动了太平洋战争，同时加紧了对中国的进攻。中国大片国土沦陷，人民生活在水深火热之中。芦荻此时在广东等地从事抗日救亡工作，深切感受到了时代的风雨和民族的危亡。在一个风雨交加的夜晚，他望着窗外的狂风暴雨，联想到动荡的祖国和苦难的人民，写下了这首《风雨吟》。"),
 ("风雨的象征","诗中的" + LQ + "风雨" + RQ + "不仅是自然的风雨，更是时代的风雨、民族的风雨。" + LQ + "风从大地卷来，雨从大地奔来" + RQ + "，写出了风雨的猛烈和不可阻挡，也象征着抗战时期社会的动荡和民族的危机。" + LQ + "郊原如海，房舍如舟" + RQ + "，写出了风雨中大地的动荡和人民的飘摇，也象征着在民族危亡之际，每一个人都如同大海上的小舟，随时可能被风浪吞没。"),
 ("舵手的寓意","诗中的" + LQ + "年轻舵手" + RQ + "是全诗的核心意象。" + LQ + "年轻" + RQ + "代表朝气、力量和希望，" + LQ + "舵手" + RQ + "代表责任、担当和方向。" + LQ + "我有年轻舵手的心" + RQ + "意味着诗人虽然可能还不是真正的舵手，但他有一颗舵手的心——有担当的勇气和把握方向的信念。这是一代青年在民族危亡之际发出的铮铮誓言：在风雨如晦的时代，我们愿做乘风破浪的舵手，引领民族的航船走出困境，走向光明。"),
]

APP_ART = [
 ("磅礴的气势","全诗开篇" + LQ + "风从大地卷来，雨从大地奔来" + RQ + "，以" + LQ + "卷" + RQ + LQ + "奔" + RQ + "两个动词，写出了风雨的磅礴气势和不可阻挡的力量。两句对偶工整，节奏急促，如风雨扑面而来，使读者如临其境、如闻其声。这种磅礴的气势，正是抗战时期民族精神的写照。"),
 ("精妙的比喻","" + LQ + "郊原如海，房舍如舟" + RQ + "是全诗最精妙的比喻。将风雨中的郊原比作波涛汹涌的大海，将房舍比作飘摇的小舟，既写出了风雨中大地的广阔和动荡，也为下文" + LQ + "年轻舵手" + RQ + "的出场做了完美的铺垫。这两个比喻层层递进，由大到小，由景到人，构思极为精巧。"),
 ("深刻的象征","全诗的意象都具有深刻的象征意义：" + LQ + "风雨" + RQ + "象征动荡的时代和民族的危机，" + LQ + "大地" + RQ + "象征祖国和人民，" + LQ + "海" + RQ + "象征动荡不安的社会，" + LQ + "舟" + RQ + "象征飘摇中的个体，" + LQ + "年轻舵手" + RQ + "象征勇于担当的青年一代。这些象征意象交织在一起，使全诗的意境雄浑而深远。"),
 ("层层递进的结构","全诗六句，结构极为精巧：前两句写风雨，极力渲染气势；中间两句写大地，以比喻营造意境；后两句写人，以" + LQ + "年轻舵手" + RQ + "点明主旨。由风雨到大地，由大地到人，层层递进，步步深入，最后以" + LQ + "在大地风雨的海上" + RQ + "收束，将前面的意象全部收拢，使全诗浑然一体。"),
 ("对偶的运用","全诗多处运用对偶：" + LQ + "风从大地卷来" + RQ + "对" + LQ + "雨从大地奔来" + RQ + "，" + LQ + "郊原如海" + RQ + "对" + LQ + "房舍如舟" + RQ + "。对偶句式整齐，节奏明快，增强了诗歌的音乐美和气势感。同时，对偶也使意象之间形成对照和呼应，强化了诗歌的意境。"),
]

APP_FAME = [
 ("风从大地卷来，雨从大地奔来。",
  "开篇两句以磅礴的气势写出了风雨的猛烈。" + LQ + "卷" + RQ + "写出了风的形态和力量——席卷一切、裹挟一切；" + LQ + "奔" + RQ + "写出了雨的迅猛和急促——奔腾而来、不可阻挡。两句对偶工整，节奏急促，如风雨扑面而来。这两句不仅是写自然风雨，更是象征抗战时期动荡的社会现实和民族危机。" + LQ + "从大地" + RQ + "点明风雨的来源——不是从天空吹来，而是从大地上卷起，暗示这场风雨与大地、与人民息息相关。"),
 ("郊原如海，房舍如舟。",
  "中间两句是全诗最精妙的比喻。" + LQ + "郊原如海" + RQ + "将风雨中的郊原比作波涛汹涌的大海，既写出了郊原的广阔无边，也写出了风雨中大地的动荡不安；" + LQ + "房舍如舟" + RQ + "将大地上的房屋比作大海上的小船，写出了风雨中人民的飘摇不定。这两个比喻层层递进，由大到小，由景到人，为下文" + LQ + "年轻舵手" + RQ + "的出场做了完美的铺垫——既然郊原是海，房舍是舟，那么人自然就是舟上的舵手了。"),
 ("我有年轻舵手的心，在大地风雨的海上。",
  "后两句是全诗的主旨所在。" + LQ + "年轻舵手" + RQ + "是全诗的核心意象——" + LQ + "年轻" + RQ + "代表朝气、力量和希望，" + LQ + "舵手" + RQ + "代表责任、担当和方向。" + LQ + "我有年轻舵手的心" + RQ + "意味着诗人有担当的勇气和把握方向的信念，这是一代青年在民族危亡之际发出的铮铮誓言。末句" + LQ + "在大地风雨的海上" + RQ + "将前面的意象全部收拢——" + LQ + "大地" + RQ + LQ + "风雨" + RQ + LQ + "海" + RQ + "三个意象叠加，构成了全诗的核心意境，将个人的担当与时代的命运紧密联系在一起，使全诗的主题得到升华。"),
]

APP_THEME = [
 "《风雨吟》通过描绘风雨中大地的动荡和人民的飘摇，表达了诗人在民族危亡之际勇于担当、乘风破浪的誓言，展现了一代青年在抗战时期的责任感和使命感。",
 "全诗以" + LQ + "风雨" + RQ + "为核心意象，象征动荡的时代和民族的危机；以" + LQ + "郊原如海，房舍如舟" + RQ + "两个精妙的比喻，营造出风雨中大地动荡、人民飘摇的意境；最后以" + LQ + "年轻舵手" + RQ + "的形象，表达了青年一代在民族危亡之际勇于担当、把握方向的信念。全诗气势磅礴，意境雄浑，是抗战时期最具代表性的诗歌之一，也是中国现代诗歌中以自然风雨象征时代风雨的经典之作。",
]

ACC = [
 ("重点词语", [
   ("卷","席卷，写出风的磅礴气势与裹挟一切的力量。"),
   ("奔","奔腾，写出雨的迅猛、急促与不可阻挡。"),
   ("郊原","郊外的原野。"),
   ("房舍","房屋、住宅。"),
   ("年轻","年纪不大，这里指充满朝气和力量。"),
   ("舵手","掌舵的人，比喻把握方向的领导者。"),
 ]),
 ("用字与读音", [
   ("卷","读 juǎn，三声；多音字，此处读 juǎn（席卷），不读 juàn（试卷）。"),
   ("奔","读 bēn，一声；多音字，此处读 bēn（奔腾），不读 bèn（投奔）。"),
   ("郊","读 jiāo，一声；" + LQ + "郊原" + RQ + "不要写成" + LQ + "郊原" + RQ + "（" + LQ + "效" + RQ + "反文旁，读 xiào）。"),
   ("原","读 yuán，二声；" + LQ + "郊原" + RQ + "指郊外的原野，不要写成" + LQ + "郊源" + RQ + "（" + LQ + "源" + RQ + "三点水，指水源）。"),
   ("舍","读 shè，四声；多音字，此处读 shè（房屋），不读 shě（舍弃）。"),
   ("舵","读 duò，四声；舟字旁+它，" + LQ + "舵手" + RQ + "不要写成" + LQ + "舵手" + RQ + "（" + LQ + "驼" + RQ + "马字旁，读 tuó）。"),
 ]),
 ("修辞方法", [
   ("比　喻", LQ + "郊原如海，房舍如舟" + RQ + "——将风雨中的郊原比作大海，将房舍比作小舟，既写出了大地的广阔和动荡，也为" + LQ + "年轻舵手" + RQ + "的出场做了铺垫。"),
   ("对　偶", LQ + "风从大地卷来，雨从大地奔来" + RQ + "——两句对偶工整，" + LQ + "风" + RQ + "对" + LQ + "雨" + RQ + "，" + LQ + "卷" + RQ + "对" + LQ + "奔" + RQ + "，增强了诗歌的气势和音乐美；" + LQ + "郊原如海，房舍如舟" + RQ + "同样对偶工整。"),
   ("象　征", LQ + "风雨" + RQ + "——象征动荡的时代和民族的危机；" + LQ + "大地" + RQ + "——象征祖国和人民；" + LQ + "年轻舵手" + RQ + "——象征勇于担当的青年一代。"),
   ("炼　字", LQ + "卷" + RQ + LQ + "奔" + RQ + "——两个动词极为精当，" + LQ + "卷" + RQ + "写出风的磅礴气势，" + LQ + "奔" + RQ + "写出雨的迅猛急促，使风雨的形象跃然纸上。"),
 ]),
 ("写作借鉴", [
   ("以自然风雨象征时代风雨","全诗以自然风雨为核心意象，通过描绘风雨中大地的动荡，象征抗战时期动荡的社会现实和民族危机。这种以自然现象象征社会现实的手法，使诗歌的意境更加雄浑深远。"),
   ("层层递进的结构","由风雨到大地，由大地到人，层层递进，步步深入。前两句渲染气势，中间两句营造意境，后两句点明主旨。这种结构使全诗浑然一体，主题逐步升华。"),
   ("精妙的比喻铺垫","" + LQ + "郊原如海，房舍如舟" + RQ + "两个比喻不仅写出了风雨中大地的动荡，更为下文" + LQ + "年轻舵手" + RQ + "的出场做了完美的铺垫。这种前后呼应的构思，使诗歌的结构极为精巧。"),
   ("磅礴的气势","全诗以" + LQ + "卷" + RQ + LQ + "奔" + RQ + "等有力的动词和对偶工整的句式，营造出磅礴的气势。这种气势与抗战时期的民族精神相呼应，使诗歌具有强烈的感染力和鼓舞力量。"),
 ]),
 ("文化常识", [
   ("芦荻","（1912—1994）原名陈培迪，广东南海人，中国现代诗人。抗战时期重要诗人之一，曾任中国作家协会广东分会副主席。代表作有《风雨吟》《桑野》《驰驱集》等。"),
   ("吟","诗歌的一种体裁，这里指抒情诗。" + LQ + "吟" + RQ + "原本是古代诗歌的一种形式，如《梁甫吟》《白头吟》等，后来泛指抒情性的诗歌。"),
   ("抗日战争","1931年至1945年中国人民抵抗日本帝国主义侵略的民族解放战争。1941年12月正值抗战最艰苦的时期，日军发动太平洋战争，同时加紧对中国的进攻。"),
   ("舵手","掌舵的人，比喻把握方向的领导者。在诗歌中，" + LQ + "舵手" + RQ + "常用来象征在动荡时代中把握方向、引领人民前进的人。"),
 ]),
]

WORDS = [
 {"w":"卷","py":"juǎn","q":"风从大地□来，","tip":"「卷」多音字，此处读 juǎn（席卷），不读 juàn（试卷）"},
 {"w":"奔","py":"bēn","q":"雨从大地□来。","tip":"「奔」多音字，此处读 bēn（奔腾），不读 bèn（投奔）"},
 {"w":"郊","py":"jiāo","q":"□原如海，","tip":"「郊」阝旁+交，读 jiāo 一声；勿写「效」（反文旁，读 xiào）"},
 {"w":"原","py":"yuán","q":"郊□如海，","tip":"「原」读 yuán 二声；「郊原」指郊外原野，勿写「郊源」（三点水，指水源）"},
 {"w":"舍","py":"shè","q":"房□如舟。","tip":"「舍」多音字，此处读 shè（房屋），不读 shě（舍弃）"},
 {"w":"舵","py":"duò","q":"我有年轻□手的心，","tip":"「舵」舟字旁+它，读 duò 四声；勿写「驼」（马字旁，读 tuó）"},
]

NOTES = [
 {"w":"卷","a":"席卷，写出风的磅礴气势与裹挟一切的力量","q":"风从大地卷来，"},
 {"w":"奔","a":"奔腾，写出雨的迅猛、急促与不可阻挡","q":"雨从大地奔来。"},
 {"w":"郊原","a":"郊外的原野","q":"郊原如海，"},
 {"w":"房舍","a":"房屋、住宅","q":"房舍如舟。"},
 {"w":"年轻","a":"年纪不大，这里指充满朝气和力量","q":"我有年轻舵手的心，"},
 {"w":"舵手","a":"掌舵的人，比喻把握方向的领导者","q":"我有年轻舵手的心，"},
]

VIDEOS = [
 ("情景朗读《风雨吟》芦荻","BV1NJ411w7s4","风雨吟情景朗读"),
 ("芦荻《风雨吟》朗读","BV1Ro4y1h7VK","风雨吟朗读"),
]

# ===== 读取框架 =====
src = io.open(SRC, encoding="utf-8-sig").read()
css = src.split("<style>", 1)[1].split("</style>", 1)[0]
js_main = src[src.index("<script>") + 8 : src.index("var DICT_WORDS")]
js_main = js_main.replace("zuguoawoqinaidezuguo_fs", LS_KEY)
js_dict = src[src.index("var DICT_WORDS") : src.index("</script>", src.index("var DICT_WORDS"))]
js_dict = re.sub(r"var DICT_WORDS = .*?;\n", "var DICT_WORDS = " + json.dumps(WORDS, ensure_ascii=False) + ";\n", js_dict, flags=re.S)
js_dict = re.sub(r"var DICT_NOTES = .*?;\n", "var DICT_NOTES = " + json.dumps(NOTES, ensure_ascii=False) + ";\n", js_dict, flags=re.S)

def video(i, h4, bvid, atitle):
    return ('<div class="media"><h4>%s</h4>'
            '<iframe id="mediaF%d" src="https://player.bilibili.com/player.html?bvid=%s&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="%s"></iframe>'
            '<a href="https://www.bilibili.com/video/%s" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF%d">全屏播放</button></div>'
            % (h4, i, bvid, atitle, bvid, i))

hero = '<header class="hero" id="top">\n  <div class="hero-inner">\n    <div class="hero-side">现代 · 芦荻</div>\n    <h1 class="hero-title">风雨吟</h1>\n  </div>\n</header>'

nav = ('<nav class="nav"><div class="nav-in">'
       '<a href="#bg">背景</a><a href="#jielu">解读</a><a href="#app">赏析</a><a href="#acc">积累</a><a href="#practice">练习</a>'
       '<div class="tool">'
       '<select id="fsSel" class="fs-sel" title="正文字体大小">'
       '<option value="100">100%</option><option value="150">150%</option><option value="200">200%</option><option value="250">250%</option><option value="300">300%</option>'
       '</select>'
       '<button id="btnAll">展开</button><button id="btnRecite">背诵</button><button id="btnPrint">打印</button>'
       '</div></div></nav>')

bg = ['<section id="bg">',
      '<div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>',
      '<div class="lead">']
for p in BG_LEAD: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>作者简介</h3>')
for p in AUTHOR: bg.append("<p>" + p + "</p>")
bg.append('</div><div class="box"><h3>创作背景</h3>')
for t, p in STORY: bg.append('<p><b>' + t + '：</b>' + p + '</p>')
bg.append('</div></section>')

jl = ['<section id="jielu">',
      '<div class="sec-head"><h2>解 读</h2><span class="no">逐句 · 内容 / 手法</span></div>',
      '<div class="sec-sub">全诗六句，以磅礴的气势和精妙的比喻，描绘了风雨中大地的动荡，表达了一代青年在民族危亡之际勇于担当的誓言。每句含<b>注释</b>（点击可查看）、内容概括与手法分析。短篇诗歌不分部分，直接逐句解读。</div>',
      '<div class="texttools">',
      '<button id="btnShowAll" class="off" style="display:none">显示全部</button>',
      '</div>',
      '<div class="box media-box">',
      '<h3>朗诵 · 拓展</h3>',
      '<div class="media-grid">']
for i, (h4, bvid, at) in enumerate(VIDEOS):
    jl.append(video(i + 1, h4, bvid, at))
jl.append('</div></div>')

jl.append('<div class="fulltext poem" id="fulltext" style="display:none">')
for idx, line in enumerate(FULLTEXT, 1):
    jl.append('<div class="pl"><span class="no">%d</span>%s</div>' % (idx, line))
jl.append('</div>')

jl.append('<div class="verse-list" id="verseList">')
for n, (orig, gai, shou) in enumerate(CARDS, 1):
    jl.append('<div class="verse" id="v%d">' % n)
    jl.append('  <div class="v-top"><span class="v-no">%d</span><div class="v-line">%s</div></div>' % (n, orig))
    jl.append('  <details class="v-more">')
    jl.append('    <summary>内容 · 手法</summary>')
    jl.append('    <div class="d-body">')
    jl.append('      <div class="v-sec"><b class="v-label">内容概括</b>')
    jl.append('        <div class="v-trans">%s</div>' % gai)
    jl.append('      </div>')
    jl.append('      <div class="v-sec"><b class="v-label">手法分析</b>')
    jl.append('        <div class="d-body"><p>%s</p></div>' % shou)
    jl.append('      </div>')
    jl.append('    </div>')
    jl.append('  </details>')
    jl.append('</div>')
jl.append('</div></section>')

app = ['<section id="app">',
       '<div class="sec-head"><h2>赏 析</h2><span class="no">艺术特色 · 名句 · 主题</span></div>']
app.append('<div class="fame-card"><h3>艺术特色</h3>')
for t, p in APP_ART:
    app.append('<p><b>%s</b>：%s</p>' % (t, p))
app.append('</div>')
app.append('<div class="fame-card"><h3>名句赏析</h3><div class="fame">')
for t, p in APP_FAME:
    app.append('<div class="fame-card"><div class="f-line">%s</div><p>%s</p></div>' % (t, p))
app.append('</div></div>')
app.append('<div class="fame-card"><h3>主题思想</h3>')
for p in APP_THEME: app.append('<p>' + p + '</p>')
app.append('</div></section>')

acc = ['<section id="acc">',
       '<div class="sec-head"><h2>积 累</h2><span class="no">词语 · 读音 · 修辞 · 写作 · 文化</span></div>']
for cat, items in ACC:
    acc.append('<div class="box"><h3>%s</h3>' % cat)
    acc.append('<div class="tw"><table>')
    acc.append('<tr><th>词语</th><th>释义</th></tr>')
    for w, d in items:
        acc.append('<tr><td class="kai">%s</td><td>%s</td></tr>' % (w, d))
    acc.append('</table></div></div>')
acc.append('</section>')

practice = ['<section id="practice">',
            '<div class="sec-head"><h2>练 习</h2><span class="no">全屏听写 · 字形 / 词语</span></div>',
            '<div class="sec-sub">以全篇<b>易错字词</b>与<b>重点词语</b>为题库，点击按钮进入<b>全屏听写</b>：先看提示在纸上默写，再核对答案。随机五组适合随堂小测，全部适合系统复习。</div>',
            '<div class="ptools">',
            '<button data-mode="word" data-rand="5">随机五组字形</button>',
            '<button data-mode="word" data-all="1">全部字形</button>',
            '<button data-mode="note" data-rand="5">随机五组词语</button>',
            '<button data-mode="note" data-all="1">全部词语</button>',
            '</div></section>']

footer = '<footer>\n  <div class="kai">风雨吟</div>\n  <div>芦荻 · 现代 · 抗战时期青年担当的誓言</div>\n  <div>人教版九年级语文下册课文</div>\n</footer>'

dictate_html = '''<div class="dictate" id="dictate" hidden>
  <div class="dictate-top">
    <span class="dictate-mode" id="dictMode">字形听写</span>
    <span class="dictate-progress" id="dictProgress">第 1 / 5 题</span>
    <button class="dictate-fs" id="dictFsMinus">A−</button><button class="dictate-fs" id="dictFsPlus">A+</button><button class="dictate-exit" id="dictExit">退出</button>
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

html = ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<title>风雨吟 · 芦荻</title>\n'
        '<meta name="description" content="现代芦荻《风雨吟》逐句解读、注释、赏析，含背景、原文（背诵模式）、解读、赏析、积累、练习，适合课堂教学。">\n'
        '<style>' + css + '</style>\n</head>\n<body data-fs="100">\n\n'
        + hero + '\n\n' + nav + '\n\n<main class="wrap">\n\n'
        + "\n".join(bg) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(jl) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(app) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(acc) + '\n\n<div class="divider"></div>\n\n'
        + "\n".join(practice) + '\n\n'
        + footer + '\n</main>\n\n'
        + '<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>\n'
        + '<button class="top-btn" id="topBtn" title="回到顶部">↑</button>\n\n'
        + dictate_html + '\n\n'
        + '<script>\n' + js_main + '\n' + js_dict + '\n</script>\n\n'
        + '</body>\n</html>\n')

# ===== 自检 =====
no_script = re.sub(r"<script>.*?</script>", "", html, flags=re.S)
body_text = re.sub(r"<[^>]+>", "", re.sub(r"<style>.*?</style>", "", no_script, flags=re.S))
assert body_text.count('"') == 0, "straight quotes in visible text: %d" % body_text.count('"')
assert "{LQ}" not in html and "{RQ}" not in html, "placeholder残留"
need = ["verseList", "fulltext", "btnAll", "btnRecite", "btnPrint", "btnShowAll", "fsSel", "annoPopup", "dictate", "topBtn", "mediaF1", "mediaF2"]
missing = [i for i in need if 'id="%s"' % i not in html]
assert not missing, "missing ids: %s" % missing
assert LS_KEY in js_main and "zuguoawoqinaidezuguo_fs" not in js_main
for it in WORDS:
    assert not any(c in it["q"] for c in it["w"]), "leak: %s" % it["w"]
    assert it["q"].count("\u25a1") == len(it["w"]), "box mismatch: %s" % it["w"]
    assert it["tip"] and it["tip"] != it["w"], "tip bad: %s" % it["w"]

anno_count = html.count('class="anno-word"')
print("风雨吟 | cards=%d fulltext=%d anno=%d words=%d notes=%d bytes=%d" % (len(CARDS), len(FULLTEXT), anno_count, len(WORDS), len(NOTES), len(html.encode("utf-8"))))
with io.open(OUT, "w", encoding="utf-8-sig") as f:
    f.write(html)
print("OK ->", OUT)
