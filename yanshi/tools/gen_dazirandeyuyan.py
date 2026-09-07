# -*- coding: utf-8 -*-
"""生成《大自然的语言》竺可桢 课件（说明文）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\dazirandeyuyan-zhukezhen.html"
FS_KEY = "ziranyuyan_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
# 注入 acc-sub CSS（积累区子标题样式）
style += "\n  .acc-sub{font-family:var(--font-kai,serif);font-weight:700;border-left:3px solid #b8934a;padding-left:8px;margin:12px 0 6px;color:var(--red-deep)}\n"
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

LQ = "\u201c"
RQ = "\u201d"

paragraphs = [
    (
        f"立春过后，大地渐渐从沉睡中苏醒过来。冰雪融化，草木萌发，各种花次第开放。再过两个月，燕子翩然归来。不久，布谷鸟也来了。于是转入炎热的夏季，这是植物孕育果实的时期。到了秋天，果实成熟，植物的叶子渐渐变黄，在秋风中簌簌地落下来。北雁南飞，活跃在田间草际的昆虫也都销声匿迹。到处呈现一片衰草连天的景象，准备迎接风雪载途的寒冬。在地球上温带和亚热带区域里，年年如是，周而复始。",
        "以生动的笔触描写地球上温带和亚热带区域四季更迭的自然景象，从立春写到寒冬，展现了周而复始的自然规律。",
        "说明对象：物候现象。说明方法：摹状貌（描写四季物候景象）。说明顺序：时间顺序（从春到冬）。说明语言：运用拟人手法（沉睡、苏醒），语言生动形象，为下文引出物候做铺垫。",
        [
            ("萌发", "种子或孢子发芽，比喻事物发生"),
            ("次第", "一个挨一个地，依次"),
            ("翩然", "动作轻快的样子"),
            ("孕育", "怀胎生育，比喻既存的事物中酝酿着新事物"),
            ("簌簌", "形容风吹叶子等的声音，也形容眼泪等纷纷落下的样子"),
            ("销声匿迹", "不再公开讲话，不再出头露面，形容隐藏起来或不公开出现。文中指昆虫消失了"),
            ("衰草连天", "形容荒草遍地，极其荒凉的样子"),
            ("风雪载途", "一路上都是风雪交加，形容旅途艰难。载，充满"),
            ("年年如是", "每年都像这样。是，这样"),
            ("周而复始", "一次又一次地循环"),
        ],
    ),
    (
        f"几千年来，劳动人民注意了草木荣枯、候鸟去来等自然现象同气候的关系，据以安排农事。杏花开了，就好像大自然在传语要赶快耕地；桃花开了，又好像在暗示要赶快种谷子。布谷鸟开始唱歌，劳动人民懂得它在唱什么：{LQ}阿公阿婆，割麦插禾。{RQ}这样看来，花香鸟语，草长莺飞，都是大自然的语言。",
        "说明劳动人民根据自然现象安排农事，以杏花、桃花、布谷鸟为例，指出花香鸟语、草长莺飞都是大自然的语言，引出说明对象。",
        "说明方法：举例子（杏花、桃花、布谷鸟）、引用（农谚）、打比方（大自然的语言）。说明语言：运用拟人（传语、暗示、唱歌），生动形象地说明物候现象与农业的关系；点题{LQ}大自然的语言{RQ}。",
        [
            ("草木荣枯", "草木的茂盛和枯萎，指植物的生长和凋零"),
            ("候鸟去来", "候鸟的到来和离去，指候鸟的迁徙"),
            ("据以", "根据它来"),
            ("农事", "农业生产中的各项工作"),
            ("传语", "传话、告诉"),
            ("割麦插禾", "收割麦子，插秧种稻。禾，指水稻"),
            ("花香鸟语", "花儿飘香，鸟儿鸣叫，形容春天动人的景象"),
            ("草长莺飞", "形容江南暮春的景色。莺，黄鹂"),
        ],
    ),
    (
        f"这些自然现象，我国古代劳动人民称它为物候。物候知识在我国起源很早。古代流传下来的许多农谚就包含了丰富的物候知识。到了近代，利用物候知识来研究农业生产，已经发展为一门科学，就是物候学。物候学记录植物的生长荣枯，动物的养育往来，如桃花开、燕子来等自然现象，从而了解随着时节推移的气候变化和这种变化对动植物的影响。",
        "明确物候和物候学的定义，介绍物候知识的起源和发展，说明物候学的研究内容和目的。",
        "说明方法：下定义（物候学）、作诠释（解释物候学的研究内容）、举例子（桃花开、燕子来）。说明语言：{LQ}就是物候学{RQ}用下定义的方法准确揭示概念；语言准确严密。",
        [
            ("物候", "生物的周期性现象（如植物的发芽、开花、结实，候鸟的迁徙，某些动物的冬眠等）与季节气候的关系"),
            ("农谚", "有关农业生产的谚语，是农民在长期生产实践里总结出来的经验"),
            ("物候学", "研究生物的生命活动现象与季节变化关系的科学"),
            ("养育往来", "指动物的繁殖、生长和迁徙等活动"),
            ("时节推移", "季节时间的推移、变化"),
        ],
    ),
    (
        f"物候观测使用的是{LQ}活的仪器{RQ}，是活生生的生物。它比气象仪器复杂得多，灵敏得多。物候观测的数据反映气温、湿度等气候条件的综合，也反映气候条件对于生物的影响。应用在农事活动里，比较简便，容易掌握。物候对于农业的重要性就在这里。下面是一个例子。",
        "说明物候观测的特点和优势：使用活生生的生物作为{LQ}活的仪器{RQ}，比气象仪器更复杂、更灵敏，应用简便，引出下文的例子。",
        "说明方法：打比方（活的仪器）、作比较（与气象仪器比较）。说明语言：{LQ}活的仪器{RQ}生动形象地说明物候观测的特点；{LQ}复杂得多，灵敏得多{RQ}用比较突出物候观测的优势。",
        [
            ("观测", "观察并测量（天文、地理、气象、方向等）"),
            ("活生生", "实际生活中的，发生在眼前的"),
            ("气象仪器", "测量大气物理参数的仪器，如温度计、湿度计等"),
            ("灵敏", "反应快，能对极其微弱的刺激迅速反应"),
            ("数据", "进行各种统计、计算、科学研究或技术设计等所依据的数值"),
            ("湿度", "空气中水汽含量的多少"),
        ],
    ),
    (
        f"北京的物候记录，1962年的山桃、杏花、苹果、榆叶梅、西府海棠、丁香、刺槐的花期比1961年迟十天左右，比1960年迟五六天。根据这些物候观测资料，可以判断北京地区1962年农业季节来得较晚。而那年春初种的花生等作物仍然是按照往年日期播种的，结果受到低温的损害。如果能注意到物候延迟，选择适宜的播种日期，这种损失就可能避免。",
        "以北京1962年物候记录为例，具体说明物候观测对农业生产的重要性：物候延迟导致按往年日期播种的作物受损，注意物候可避免损失。",
        "说明方法：举例子（北京物候记录）、列数字（迟十天左右、迟五六天）、作比较（1962年与1961年、1960年比较）。说明语言：{LQ}左右{RQ}{LQ}五六天{RQ}表示约数，{LQ}可能{RQ}表示推测，体现说明文语言的准确性。",
        [
            ("榆叶梅", "落叶灌木或小乔木，叶像榆树叶，花像梅花，供观赏"),
            ("西府海棠", "落叶小乔木，花淡红色，果实球形，是海棠的一个品种"),
            ("丁香", "落叶灌木或小乔木，花紫色或白色，有香气"),
            ("刺槐", "落叶乔木，枝上有刺，花白色，有香气，结荚果"),
            ("花期", "植物开花的时期"),
            ("物候延迟", "物候现象出现的时间比正常年份晚"),
            ("适宜", "合适、相宜"),
        ],
    ),
    (
        f"物候现象的来临决定于哪些因素呢？",
        "以设问句过渡，引出下文对决定物候现象来临因素的说明。",
        "说明方法：设问。说明语言：独句成段，起承上启下的过渡作用，引发读者思考。",
        [
            ("来临", "到来、来到"),
            ("因素", "决定事物成败的原因或条件"),
        ],
    ),
    (
        f"首先是纬度。越往北桃花开得越迟，候鸟也来得越晚。值得指出的是物候现象南北差异的日数因季节的差别而不同。我国大陆性气候显著，冬冷夏热。冬季南北温度悬殊，夏季却相差不大。在春天，早春跟晚春也不相同。如在早春三四月间，南京桃花要比北京早开20天，但是到晚春五月初，南京刺槐开花只比北京早10天。所以在华北常感觉到春季短促，冬天结束，夏天就到了。",
        "说明纬度是决定物候现象来临的首要因素：越往北物候越迟，但南北差异的日数因季节而不同，冬季差异大、夏季差异小，早春差异大、晚春差异小。",
        "说明方法：举例子（南京与北京桃花、刺槐开花比较）、列数字（早开20天、早10天）、作比较（南北、冬夏、早春晚春比较）。说明顺序：逻辑顺序（由主到次，首先）。说明语言：{LQ}越……越……{RQ}准确说明纬度与物候的关系；数字精确。",
        [
            ("纬度", "地球表面南北距离的度数，以赤道为0°，南北各90°"),
            ("候鸟", "随季节变化而迁徙的鸟，如大雁、燕子等"),
            ("南北差异", "南方和北方之间的差别"),
            ("大陆性气候", "受大陆影响显著的气候，特点是冬冷夏热，气温年较差大"),
            ("悬殊", "相差很远"),
            ("短促", "时间极短"),
        ],
    ),
    (
        f"经度的差异是影响物候的第二个因素。凡是近海的地方，比同纬度的内陆，冬天温和，春天反而寒冷。所以沿海地区的春天的来临比内陆要迟若干天。如大连纬度在北京以南约1°，但是在大连，连翘和榆叶梅的盛开都比北京要迟一个星期。又如济南苹果开花在四月中或谷雨节，烟台要到立夏。两地纬度相差无几，但烟台靠海，春天便来得迟了。",
        "说明经度差异是影响物候的第二个因素：近海地区冬天温和、春天寒冷，春天来临比内陆迟，以大连与北京、济南与烟台为例具体说明。",
        "说明方法：举例子（大连/北京、济南/烟台）、列数字（约1°、一个星期）、作比较（沿海与内陆比较）。说明顺序：逻辑顺序（第二个因素）。说明语言：{LQ}凡是{RQ}表示范围，{LQ}约{RQ}表示约数，{LQ}相差无几{RQ}准确说明两地纬度相近，体现语言的准确性。",
        [
            ("经度", "地球表面东西距离的度数，以本初子午线为0°，东西各180°"),
            ("近海", "靠近海洋的地区"),
            ("内陆", "大陆内部，远离海洋的地区"),
            ("温和", "（气候）不冷不热"),
            ("连翘", "落叶灌木，春季开黄花，果实可入药"),
            ("谷雨节", "二十四节气之一，在每年4月20日前后"),
            ("立夏", "二十四节气之一，在每年5月6日前后，表示夏季开始"),
            ("相差无几", "彼此差别不大"),
        ],
    ),
    (
        f"影响物候的第三个因素是高下的差异。植物的抽青、开花等物候现象在春夏两季越往高处越迟，而到秋天乔木的落叶则越往高处越早。不过研究这个因素要考虑到特殊的情况。例如秋冬之交，天气晴朗的空中，在一定高度上气温反比低处高。这叫逆温层。由于冷空气比较重，在无风的夜晚，冷空气便向低处流。这种现象在山地秋冬两季，特别是这两季的早晨，极为显著，常会发现山脚有霜而山腰反无霜。在华南丘陵区把热带作物引种在山腰很成功，在山脚反不适宜，就是这个道理。",
        "说明高下差异是影响物候的第三个因素：春夏越往高处物候越迟，秋天越往高处落叶越早；同时说明特殊情况——逆温层，秋冬之交一定高度上气温反比低处高，并解释其原因和影响。",
        "说明方法：作诠释（解释逆温层的成因和影响）、举例子（山脚有霜山腰无霜、华南丘陵引种热带作物）、下定义（逆温层）。说明顺序：逻辑顺序（第三个因素，从一般到特殊）。说明语言：{LQ}不过{RQ}转折引出特殊情况，说明全面；{LQ}极为显著{RQ}准确描述现象。",
        [
            ("高下", "高低，文中指海拔高度的差异"),
            ("抽青", "植物发芽变绿"),
            ("乔木", "树干高大而有明显主干的树木，如松、柏、杨等"),
            ("逆温层", "在某些天气条件下，地面上空的大气结构出现气温随高度增加而升高的反常现象"),
            ("冷空气", "温度较低的空气团"),
            ("显著", "非常明显"),
            ("华南丘陵区", "我国南方丘陵地区，包括广东、广西、福建等地的丘陵地带"),
            ("热带作物", "适合在热带地区生长的作物，如橡胶、咖啡等"),
            ("引种", "把别的地区的动植物优良品种引入本地区，选择适于本地区条件的加以繁殖推广"),
        ],
    ),
    (
        f"此外，物候现象来临的迟早还有古今的差异。根据英国南部物候的一种长期记录，拿1741到1750年十年平均的春初七种乔木抽青和开花日期同1921到1930年十年的平均值相比较，可以看出后者比前者早九天。就是说，春天提前九天。",
        "说明古今差异是影响物候的第四个因素，以英国南部物候长期记录为例，说明现代春天比18世纪提前了九天。",
        "说明方法：举例子（英国南部物候记录）、列数字（1741到1750年、1921到1930年、早九天）、作比较（两个十年平均值比较）。说明顺序：逻辑顺序（此外，第四个因素）。说明语言：用具体年份和数字，准确严密，有说服力。",
        [
            ("古今", "古代和现代"),
            ("长期记录", "跨越很长时间的观测记录"),
            ("平均值", "几个数相加的和除以个数所得的商"),
            ("后者", "比较的两项中靠后的一项，文中指1921到1930年的平均值"),
            ("前者", "比较的两项中靠前的一项，文中指1741到1750年的平均值"),
        ],
    ),
    (
        f"物候学这门科学接近生物学中的生态学和气象学中的农业气象学。物候学的研究首先是为了预报农时，选择播种日期。此外还有多方面的意义。物候资料对于安排农作物区划，确定造林和采集树木种子的日期，很有参考价值，还可以利用来引种植物到物候条件相同的地区，也可以利用来避免或减轻害虫的侵害。我国有很大面积的山区土地可以耕种，而山区的气候、土壤对农作物的适应情况，有很多地方还有待调查。为了便利山区的农业发展，开展山区物候观测是必要的。",
        "说明物候学的学科定位和多方面研究意义：预报农时、安排农作物区划、确定造林采种日期、引种植物、避免或减轻害虫侵害，并指出开展山区物候观测的必要性。",
        "说明方法：分类别（分条说明物候学的多方面意义）。说明顺序：逻辑顺序（由主到次，首先、此外）。说明语言：{LQ}首先{RQ}{LQ}此外{RQ}{LQ}还可以{RQ}{LQ}也可以{RQ}等词语条理清晰地说明物候学的意义；{LQ}有待调查{RQ}表述留有余地。",
        [
            ("生态学", "研究生物之间及生物与非生物环境之间相互关系的学科"),
            ("农业气象学", "研究农业生产与气象条件之间关系的学科"),
            ("预报农时", "预测和报告适合农业生产的时节"),
            ("农作物区划", "根据自然条件和作物特性，对农作物种植区域进行划分"),
            ("造林", "在无林地上建立新林的生产活动"),
            ("引种", "把别的地区的植物引入本地区栽培"),
            ("侵害", "侵入而损害"),
            ("山区", "多山的地区"),
            ("土壤", "地球陆地表面的一层疏松物质，有肥力，能生长植物"),
        ],
    ),
    (
        f"物候学是关系到农业丰产的科学，我们要进一步加强物候观测，懂得大自然的语言，争取农业更大的丰收。",
        "总结全文，强调物候学对农业丰产的重要意义，号召加强物候观测，呼应标题和开头。",
        "说明方法：无特殊说明方法，以议论作结。说明语言：{LQ}大自然的语言{RQ}呼应标题，首尾圆合；{LQ}进一步{RQ}{LQ}更大的{RQ}表达了对物候学发展的期望。",
        [
            ("丰产", "农业上比一般产量高"),
            ("观测", "观察并测量"),
        ],
    ),
]

parts = [
    ("第一部分", "引出物候与物候学", "1–3 段", "从四季物候景象写起，以劳动人民的农事经验引出物候和物候学的概念。"),
    ("第二部分", "物候观测对农业的重要性", "4–5 段", "说明物候观测使用{LQ}活的仪器{RQ}，比气象仪器更灵敏，并以北京物候记录为例具体说明其对农业的重要性。"),
    ("第三部分", "决定物候来临的因素", "6–10 段", "以设问引出，分别说明纬度、经度、高下、古今四个因素对物候现象来临的影响。"),
    ("第四部分", "物候学的研究意义", "11–12 段", "说明物候学的多方面意义，号召加强物候观测，争取农业更大丰收。"),
]

para_part = [0,0,0, 1,1, 2,2,2,2,2, 3,3]

fulltext_paras = [p[0] for p in paragraphs]

def annotate(text, annos):
    items = sorted(annos, key=lambda x: len(x[0]), reverse=True)
    result = text
    used = set()
    for word, note in items:
        if word in used:
            continue
        idx = result.find(word)
        if idx != -1:
            before = result[:idx]
            if before.count("<span") == before.count("</span>"):
                span = f'<span class="anno-word" data-note="{note}">{word}</span>'
                result = result[:idx] + span + result[idx+len(word):]
                used.add(word)
    return result

verse_html = ""
current_part = -1
for i, (orig, content, method, annos) in enumerate(paragraphs):
    pi = para_part[i]
    if pi != current_part:
        current_part = pi
        pname, ptitle, prange, poverview = parts[pi]
        verse_html += f'''      <div class="part-head"><span class="p-num">{pname}</span><h3>{ptitle}</h3><span class="range">{prange}</span></div>
      <div class="part-overview">{poverview}</div>
'''
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

fulltext_html = ""
for para in fulltext_paras:
    fulltext_html += f'    <div class="pl">{para}</div>\n'

dict_words = [
    {"w":"萌","py":"méng","q":"草木□发，各种花次第开放","tip":"「萌」草字头，发芽；不要写成「盟」（皿字底）"},
    {"w":"翩","py":"piān","q":"燕子□然归来","tip":"「翩」羽字旁，动作轻快；不要写成「篇」（竹字头）"},
    {"w":"孕","py":"yùn","q":"这是植物□育果实的时期","tip":"「孕」子字头，怀胎；不要写成「蕴」（草字头）"},
    {"w":"簌簌","py":"sù sù","q":"在秋风中□□地落下来","tip":"「簌」竹字头，形容风声；叠词整体作答，不要写成「蔌蔌」"},
    {"w":"匿","py":"nì","q":"活跃在田间草际的昆虫也都销声□迹","tip":"「匿」匚字旁，隐藏；不要写成「溺」（三点水）"},
    {"w":"载","py":"zài","q":"准备迎接风雪□途的寒冬","tip":"「载」车字旁，充满；多音字，此处读zài不读zǎi"},
    {"w":"谚","py":"yàn","q":"古代流传下来的许多农□就包含了丰富的物候知识","tip":"「谚」言字旁，谚语；不要写成「颜」（页字旁）"},
    {"w":"榆","py":"yú","q":"1962年的山桃、杏花、苹果、□叶梅","tip":"「榆」木字旁，榆树；不要写成「愉」（竖心旁）"},
    {"w":"槐","py":"huái","q":"西府海棠、丁香、刺□的花期","tip":"「槐」木字旁，槐树；不要写成「愧」（竖心旁）"},
    {"w":"纬","py":"wěi","q":"首先是□度","tip":"「纬」绞丝旁，纬度；不要写成「伟」（单人旁）"},
    {"w":"悬","py":"xuán","q":"冬季南北温度□殊","tip":"「悬」心字底，距离远；不要写成「县」"},
    {"w":"促","py":"cù","q":"所以在华北常感觉到春季短□","tip":"「促」单人旁，时间短；不要写成「捉」（提手旁）"},
    {"w":"经","py":"jīng","q":"□度的差异是影响物候的第二个因素","tip":"「经」绞丝旁，经度；与「纬」（纬度）区分"},
    {"w":"翘","py":"qiáo","q":"连□和榆叶梅的盛开都比北京要迟一个星期","tip":"「翘」羽字旁，抬起；多音字，此处读qiáo不读qiào"},
    {"w":"逆","py":"nì","q":"这叫□温层","tip":"「逆」辶字旁，方向相反；不要写成「朔」（shuò）"},
    {"w":"丘陵","py":"qiū líng","q":"在华南□□区把热带作物引种在山腰很成功","tip":"「丘」撇字头，「陵」左耳旁；双字词整体作答，与「凌」（两点水）区分"},
    {"w":"引种","py":"yǐn zhǒng","q":"还可以利用来□□植物到物候条件相同的地区","tip":"「引」弓字旁，「种」禾字旁；双字词整体作答"},
    {"w":"侵","py":"qīn","q":"也可以利用来避免或减轻害虫□害","tip":"「侵」单人旁，侵入损害；不要写成「浸」（三点水）"},
]

dict_notes = [
    {"w":"翩然","a":"动作轻快的样子","q":"燕子翩然归来"},
    {"w":"孕育","a":"怀胎生育，比喻既存的事物中酝酿着新事物","q":"这是植物孕育果实的时期"},
    {"w":"销声匿迹","a":"形容隐藏起来或不公开出现，文中指昆虫消失了","q":"活跃在田间草际的昆虫也都销声匿迹"},
    {"w":"衰草连天","a":"形容荒草遍地，极其荒凉的样子","q":"到处呈现一片衰草连天的景象"},
    {"w":"风雪载途","a":"一路上都是风雪交加，形容旅途艰难。载，充满","q":"准备迎接风雪载途的寒冬"},
    {"w":"周而复始","a":"一次又一次地循环","q":"年年如是，周而复始"},
    {"w":"物候","a":"生物的周期性现象与季节气候的关系","q":"我国古代劳动人民称它为物候"},
    {"w":"物候学","a":"研究生物的生命活动现象与季节变化关系的科学","q":"已经发展为一门科学，就是物候学"},
    {"w":"农谚","a":"有关农业生产的谚语，是农民长期生产实践总结的经验","q":"古代流传下来的许多农谚"},
    {"w":"纬度","a":"地球表面南北距离的度数，以赤道为0°","q":"首先是纬度"},
    {"w":"经度","a":"地球表面东西距离的度数，以本初子午线为0°","q":"经度的差异是影响物候的第二个因素"},
    {"w":"逆温层","a":"在某些天气条件下，气温随高度增加而升高的反常现象","q":"这叫逆温层"},
    {"w":"生态学","a":"研究生物之间及生物与非生物环境之间相互关系的学科","q":"接近生物学中的生态学"},
    {"w":"说明对象","a":"文章要说明的事物或事理，本文的说明对象是物候和物候学","q":"这些自然现象，我国古代劳动人民称它为物候"},
    {"w":"说明顺序","a":"说明内容的安排次序，本文主要用逻辑顺序","q":"物候现象的来临决定于哪些因素呢"},
    {"w":"逻辑顺序","a":"按照事物或事理的内在逻辑关系安排说明顺序，如由主到次、从现象到本质等","q":"首先是纬度"},
    {"w":"下定义","a":"用简明的语言揭示事物的本质特征的说明方法","q":"已经发展为一门科学，就是物候学"},
    {"w":"作比较","a":"通过对比来突出事物特征的说明方法","q":"它比气象仪器复杂得多，灵敏得多"},
    {"w":"举例子","a":"举出实际事例来说明事物的说明方法","q":"下面是一个例子"},
    {"w":"列数字","a":"用具体数字来说明事物的说明方法","q":"南京桃花要比北京早开20天"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《大自然的语言》竺可桢</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 竺可桢</div>
  <h1 class="hero-title">大自然的语言</h1>
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
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 文体 · 缘起</span></div>
  <div class="lead">
    <p>《大自然的语言》是气象学家竺可桢写的一篇事理说明文，选自《科学大众》。文章以生动通俗的语言介绍了物候和物候学的知识，说明了决定物候现象来临的因素以及物候学研究的意义，是中学语文教材中说明文的经典篇目。</p>
    <p>文章把专业的物候知识写得通俗易懂、生动有趣，综合运用举例子、列数字、作比较、下定义、打比方等多种说明方法，语言准确严密而又生动形象，是学习事理说明文写作的典范。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>竺可桢（1890—1974），字藕舫，浙江绍兴人，中国著名气象学家、地理学家、教育家，中国近代地理学和气象学的奠基者，中国科学院院士。1910年赴美国留学，获哈佛大学博士学位。回国后曾任浙江大学校长、中国科学院副院长等职。</p>
    <p style="margin-top:10px;color:var(--ink2)">竺可桢是中国物候学的开创者，他坚持数十年观测记录物候现象，著有《物候学》《中国近五千年来气候变迁的初步研究》等。他的科普文章深入浅出，《大自然的语言》是其代表作，最初发表于1963年《科学大众》第1期。</p>
  </div>
  <div class="box">
    <h3>文体知识</h3>
    <p><b>事理说明文：</b>以分析事物的因果关系、介绍科学道理为主的说明文。事物说明文说明{LQ}是什么{RQ}，事理说明文说明{LQ}为什么{RQ}。本文说明物候现象及其成因，属于事理说明文。</p>
    <p style="margin-top:8px"><b>说明方法：</b>常见的有举例子、列数字、打比方、作比较、分类别、下定义、作诠释、摹状貌、引用等。本文综合运用多种说明方法，是说明文学习的典范。</p>
    <p style="margin-top:8px"><b>说明顺序：</b>常见的有时间顺序、空间顺序、逻辑顺序。本文整体采用逻辑顺序（从现象到本质、由主到次），开头描写四季景象用时间顺序。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文诵读《大自然的语言》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1ZP4y1776p&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读大自然的语言"></iframe>
        <a href="https://www.bilibili.com/video/BV1ZP4y1776p" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>竺可桢：大自然的记录者</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1r18Q6tE58&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="竺可桢大自然的记录者"></iframe>
        <a href="https://www.bilibili.com/video/BV1r18Q6tE58" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 说明方法 · 语言</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{fulltext_html}  </div>
  <div class="verse-list" id="verseList">
{verse_html}  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">说明对象 · 方法 · 顺序 · 语言</span></div>

  <div class="box">
    <h3>说明对象与特征</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">说明对象：物候与物候学</div>
        <p>本文的说明对象是物候现象和物候学。文章从四季更迭的自然景象写起，引出{LQ}大自然的语言{RQ}即物候，进而介绍物候学的定义、物候观测对农业的重要性、决定物候来临的因素以及物候学的研究意义。说明对象明确，条理清晰。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">说明中心：物候与农业生产的关系</div>
        <p>文章围绕物候与农业生产的关系展开：开头以劳动人民根据物候安排农事引出说明对象，中间以北京物候记录为例说明物候观测对农业的重要性，结尾强调物候学关系到农业丰产。全文紧扣{LQ}物候为农业服务{RQ}这一中心，选材精当。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">举例子：典型而有说服力</div>
        <p>举例子是本文最主要的说明方法。说明物候观测的重要性时举北京1962年物候记录的例子；说明纬度影响时举南京与北京桃花、刺槐开花比较的例子；说明经度影响时举大连与北京、济南与烟台的例子；说明高下影响时举华南丘陵引种热带作物的例子；说明古今影响时举英国南部物候记录的例子。例子典型具体，增强了说服力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">列数字与作比较：精确而突出</div>
        <p>全文使用了大量数字：{LQ}迟十天左右{RQ}{LQ}迟五六天{RQ}{LQ}早开20天{RQ}{LQ}早10天{RQ}{LQ}约1°{RQ}{LQ}早九天{RQ}等，数字精确具体，使说明更有说服力。同时大量运用作比较：物候观测与气象仪器比较、南北物候比较、沿海与内陆比较、两个十年平均值比较等，通过对比突出事物特征。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">下定义与作诠释：准确而通俗</div>
        <p>{LQ}到了近代，利用物候知识来研究农业生产，已经发展为一门科学，就是物候学{RQ}，用下定义的方法准确揭示物候学的本质特征；{LQ}这叫逆温层。由于冷空气比较重，在无风的夜晚，冷空气便向低处流{RQ}，用作诠释的方法通俗解释逆温层的成因。两种方法结合，使科学概念既准确又易懂。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">打比方与摹状貌：生动而形象</div>
        <p>物候观测使用的是{LQ}活的仪器{RQ}，是活生生的生物，打比方生动形象地说明物候观测的特点；开头描写四季物候景象（{LQ}冰雪融化，草木萌发{RQ}{LQ}北雁南飞，活跃在田间草际的昆虫也都销声匿迹{RQ}），用摹状貌的方法使读者如见其景。多种方法综合运用，文章既科学准确又生动有趣。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明顺序</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">整体：逻辑顺序（从现象到本质）</div>
        <p>文章整体采用逻辑顺序：先从四季物候现象写起（现象），引出物候和物候学的概念（本质），再说明物候观测的重要性（应用），然后分析决定物候来临的四个因素（原因），最后说明物候学的研究意义（价值）。从现象到本质、从原因到结果、由主到次，条理清晰，层层深入。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">局部：时间顺序与逻辑顺序结合</div>
        <p>开头第一段按春夏秋冬的时间顺序描写四季物候景象；说明决定物候来临的因素时，按由主到次的逻辑顺序排列（首先纬度、第二经度、第三高下、此外古今），并用{LQ}首先{RQ}{LQ}第二个因素{RQ}{LQ}第三个因素{RQ}{LQ}此外{RQ}等标志词语标明顺序。多种说明顺序综合运用，使文章结构严谨。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明语言的准确性</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">修饰限制词的运用</div>
        <p>{LQ}大约建成于公元282年{RQ}{LQ}可能是有记载的最早的石拱桥{RQ}——本文中类似的修饰限制词比比皆是：{LQ}迟十天左右{RQ}{LQ}约1°{RQ}{LQ}相差无几{RQ}{LQ}可能避免{RQ}{LQ}有待调查{RQ}{LQ}极为显著{RQ}等。{LQ}左右{RQ}{LQ}约{RQ}表示约数，{LQ}可能{RQ}表示推测，{LQ}几乎{RQ}表示程度，这些词语准确地反映了客观实际，体现了说明文语言的准确性和严密性。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">准确与生动的统一</div>
        <p>本文语言既准确严密，又生动形象。数字和术语体现了科学性和准确性，而拟人（{LQ}大地渐渐从沉睡中苏醒过来{RQ}{LQ}大自然在传语{RQ}{LQ}布谷鸟开始唱歌{RQ}）、比喻（{LQ}活的仪器{RQ}{LQ}大自然的语言{RQ}）、描写（四季物候景象）等手法又使文章生动有趣。做到了科学性与文学性的统一，是科普说明文的典范。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《大自然的语言》以生动通俗的语言介绍了物候和物候学的知识，说明了决定物候现象来临的纬度、经度、高下、古今四个因素，阐述了物候学研究对农业生产的重要意义，号召人们加强物候观测，懂得大自然的语言，争取农业更大的丰收。文章既传播了科学知识，又激发了读者探索自然奥秘的兴趣。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 说明术语 · 用字 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">翩然</span><span class="acc-d">动作轻快的样子。</span></div>
      <div class="acc-item"><span class="acc-w">孕育</span><span class="acc-d">怀胎生育，比喻既存的事物中酝酿着新事物。</span></div>
      <div class="acc-item"><span class="acc-w">销声匿迹</span><span class="acc-d">形容隐藏起来或不公开出现。文中指昆虫消失了。</span></div>
      <div class="acc-item"><span class="acc-w">衰草连天</span><span class="acc-d">形容荒草遍地，极其荒凉的样子。</span></div>
      <div class="acc-item"><span class="acc-w">风雪载途</span><span class="acc-d">一路上都是风雪交加，形容旅途艰难。载，充满。</span></div>
      <div class="acc-item"><span class="acc-w">周而复始</span><span class="acc-d">一次又一次地循环。</span></div>
      <div class="acc-item"><span class="acc-w">物候</span><span class="acc-d">生物的周期性现象与季节气候的关系。</span></div>
      <div class="acc-item"><span class="acc-w">物候学</span><span class="acc-d">研究生物的生命活动现象与季节变化关系的科学。</span></div>
      <div class="acc-item"><span class="acc-w">农谚</span><span class="acc-d">有关农业生产的谚语，农民长期生产实践总结的经验。</span></div>
      <div class="acc-item"><span class="acc-w">悬殊</span><span class="acc-d">相差很远。</span></div>
      <div class="acc-item"><span class="acc-w">逆温层</span><span class="acc-d">气温随高度增加而升高的反常现象。</span></div>
      <div class="acc-item"><span class="acc-w">引种</span><span class="acc-d">把别的地区的植物引入本地区栽培。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>说明文术语</h3>
      <div class="acc-item"><span class="acc-w">事理说明文</span><span class="acc-d">以分析事物的因果关系、介绍科学道理为主的说明文。本文属于事理说明文。</span></div>
      <div class="acc-item"><span class="acc-w">说明对象</span><span class="acc-d">文章要说明的事物或事理。本文的说明对象是物候和物候学。</span></div>
      <div class="acc-item"><span class="acc-w">说明方法</span><span class="acc-d">说明事物特征的方法，常见的有举例子、列数字、打比方、作比较、分类别、下定义、作诠释、摹状貌、引用等。</span></div>
      <div class="acc-item"><span class="acc-w">举例子</span><span class="acc-d">举出实际事例来说明事物。本文举了北京物候记录、南京与北京比较等大量例子。</span></div>
      <div class="acc-item"><span class="acc-w">列数字</span><span class="acc-d">用具体数字来说明事物。如{LQ}早开20天{RQ}{LQ}早九天{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">作比较</span><span class="acc-d">通过对比来突出事物的特征。如物候观测与气象仪器比较。</span></div>
      <div class="acc-item"><span class="acc-w">下定义</span><span class="acc-d">用简明的语言揭示事物的本质特征。如{LQ}就是物候学{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">作诠释</span><span class="acc-d">对事物进行解释说明。如解释逆温层的成因。</span></div>
      <div class="acc-item"><span class="acc-w">打比方</span><span class="acc-d">通过比喻来说明事物。如{LQ}活的仪器{RQ}{LQ}大自然的语言{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">摹状貌</span><span class="acc-d">对事物的形状、姿态等进行描写。如开头四季物候景象的描写。</span></div>
      <div class="acc-item"><span class="acc-w">说明顺序</span><span class="acc-d">说明内容的安排次序，常见的有时间顺序、空间顺序、逻辑顺序。本文主要用逻辑顺序。</span></div>
      <div class="acc-item"><span class="acc-w">逻辑顺序</span><span class="acc-d">按照事物或事理的内在逻辑关系安排说明顺序，如从现象到本质、由主到次等。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">萌发</span><span class="acc-d">（méng）草字头；与「盟」（皿字底）区分。</span></div>
      <div class="acc-item"><span class="acc-w">翩然</span><span class="acc-d">（piān）羽字旁；与「篇」（竹字头）区分。</span></div>
      <div class="acc-item"><span class="acc-w">簌簌</span><span class="acc-d">（sù）竹字头，形容风声；叠词，不要写成「蔌蔌」。</span></div>
      <div class="acc-item"><span class="acc-w">销声匿迹</span><span class="acc-d">（nì）「匿」匚字旁，隐藏；与「溺」（三点水）区分。</span></div>
      <div class="acc-item"><span class="acc-w">风雪载途</span><span class="acc-d">（zài）「载」车字旁，充满；多音字，此处读zài不读zǎi。</span></div>
      <div class="acc-item"><span class="acc-w">农谚</span><span class="acc-d">（yàn）言字旁；与「颜」（页字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">纬度</span><span class="acc-d">（wěi）绞丝旁；与「伟」（单人旁）区分；与「经度」的「经」区分。</span></div>
      <div class="acc-item"><span class="acc-w">连翘</span><span class="acc-d">（qiáo）羽字旁；多音字，此处读qiáo不读qiào。</span></div>
      <div class="acc-item"><span class="acc-w">逆温层</span><span class="acc-d">（nì）辶字旁；与「朔」（shuò）区分。</span></div>
      <div class="acc-item"><span class="acc-w">丘陵</span><span class="acc-d">（qiū líng）「陵」左耳旁；与「凌」（两点水）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">从现象到本质</span><span class="acc-d">从四季物候现象写起，引出物候学概念，再分析成因和意义，符合人的认知规律。</span></div>
      <div class="acc-item"><span class="acc-w">由主到次排列</span><span class="acc-d">说明决定物候的因素时，按纬度→经度→高下→古今由主到次排列，用标志词语标明顺序。</span></div>
      <div class="acc-item"><span class="acc-w">例子典型具体</span><span class="acc-d">每个因素都配典型例子，例子中含具体数字和比较，增强说服力。</span></div>
      <div class="acc-item"><span class="acc-w">语言准确生动</span><span class="acc-d">修饰限制词体现准确性，拟人、比喻、描写使文章生动有趣，科学性与文学性统一。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">二十四节气</span><span class="acc-d">中国古代订立的用来指导农事的补充历法，文中提到谷雨、立夏等节气。二十四节气反映了物候与气候的关系，2016年被列入联合国教科文组织人类非物质文化遗产代表作名录。</span></div>
      <div class="acc-item"><span class="acc-w">物候观测史</span><span class="acc-d">中国是世界上物候观测最早的国家之一，古代农谚中包含丰富的物候知识。竺可桢是中国物候学的开创者，他从1921年起坚持观测记录物候，直至逝世。</span></div>
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
  <div class="kai">《大自然的语言》</div>
  <div>竺可桢 · 现代 · 出自《科学大众》</div>
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

# Replace {LS}/{RS} with actual Chinese quotes in the generated HTML
html = html.replace("{LS}", LQ).replace("{RS}", RQ)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Generated: {OUT}")
print(f"Paragraphs: {len(paragraphs)}")
print(f"Anno count: {sum(len(p[3]) for p in paragraphs)}")
print(f"Words: {len(dict_words)}, Notes: {len(dict_notes)}")
