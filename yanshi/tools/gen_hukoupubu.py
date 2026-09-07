# -*- coding: utf-8 -*-
"""生成《壶口瀑布》梁衡 课件（游记散文）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\hukoupubu-liangheng.html"
FS_KEY = "hukou_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

paragraphs = [
    (
        "壶口在晋陕两省的边境上，我曾两次到过那里。",
        "交代壶口的地理位置和作者两次到访的经历，总起全文，为下文两次观瀑的不同感受做铺垫。",
        "开门见山，简洁利落。“晋陕两省的边境”点明地理位置；“曾两次到过那里”设置悬念，引出下文雨季与枯水季两次观瀑的对比，“两次”是全文的叙事线索。",
        [
            ("晋陕", "山西和陕西两省，壶口瀑布位于两省交界处"),
            ("边境", "交界地带、边界附近"),
        ],
    ),
    (
        "第一次是雨季，临出发时有人告诫：“这个时节看壶口最危险，千万不要到河滩里去，赶巧上游下雨，一个洪峰下来，根本来不及上岸。”果然，车还在半山腰就听见涛声隐隐如雷，河谷里雾气弥漫，我们大着胆子下到滩里，那河就像一锅正沸着的水。壶口瀑布不是从高处落下，让人们仰视垂空的水幕，而是由平地向更低的沟里跌去，人们只能俯视被急急吸去的水流。其时，正是雨季，那沟已被灌得浪沫横溢，但上面的水还是一股劲地冲进去，冲进去……我在雾中想寻找想象中的飞瀑，但水浸沟岸，雾罩乱石，除了扑面而来的水汽，震耳欲聋的涛声，什么也看不见，什么也听不见，只有一个可怕的警觉：仿佛突然就要出现一个洪峰将我吞没。于是，只急慌慌地扫了几眼，我便匆匆逃离，到了岸上回望那团白烟，心还在不住地跳……",
        "写第一次雨季观瀑的经历。以涛声、雾气、水汽等侧面烘托壶口瀑布的壮观与危险，作者因恐惧匆匆逃离，与下文枯水季的从容观瀑形成鲜明对比。",
        "侧面描写：未见瀑布先闻其声（涛声隐隐如雷），以声写势。比喻：那河就像一锅正沸着的水，写出河水的翻滚沸腾。对比：“不是……而是……”否定常见瀑布的仰视角度，突出壶口由平地向深沟跌去的独特形态。反复：冲进去，冲进去，写水势之急之猛。多感官：听觉（涛声如雷、震耳欲聋）、视觉（雾气弥漫、浪沫横溢、白烟）、触觉（扑面而来的水汽）。心理描写：可怕的警觉、心还在不住地跳，以作者的恐惧侧面写瀑布的威力。",
        [
            ("告诫", "警告劝诫，提醒别人注意"),
            ("洪峰", "河流在涨水期间达到最高点的水位，也指涨到最高水位的洪水"),
            ("半山腰", "山坡的中部、半腰"),
            ("弥漫", "（mí màn）（烟尘、雾气、水等）充满、布满"),
            ("大着胆子", "鼓起勇气、壮着胆子"),
            ("仰视", "抬头向上看"),
            ("俯视", "从高处往下看"),
            ("浪沫横溢", "波浪的泡沫四处流淌、漫溢"),
            ("震耳欲聋", "耳朵都快震聋了，形容声音很大"),
            ("警觉", "对危险或情况变化的敏锐感觉"),
            ("吞没", "把公共的或代管的财物据为己有；文中指淹没、吞噬"),
            ("急慌慌", "急忙慌张的样子"),
            ("匆匆逃离", "急急忙忙地逃跑离开"),
        ],
    ),
    (
        "第二次看黄河，我专选了个枯水季节。春寒刚过，山还未青，谷底显得异常开阔。我们从从容容地下到沟底，这时的黄河像是一张极大的石床，上面铺了一层软软的细沙，踏上去坚实而又松软。我一直走到河心，原来河心还有一条河，是突然凹下去的一条深沟，当地人叫“龙槽”，槽头入水处深不可测，这便是“壶口”。我倚在一块大石头上向上游看去，这龙槽顶着宽宽的河面，正好形成一个丁字。河水从五百米宽的河道上排排涌来，其势如千军万马，互相挤着、撞着，推推搡搡，前呼后拥，撞向石壁，排排黄浪霎时碎成堆堆白雪。山是青冷的灰，天是寂寂的蓝，宇宙间仿佛只有这水的存在。当河水正这般畅畅快快地驰骋着时，突然脚下出现一条四十多米宽的深沟，它们还来不及想一下，便一齐跌了进去，更涌、更挤、更急。沟底飞转着一个个漩涡，当地人说，曾有一头黑猪掉进去，再漂上来时，浑身的毛竟被拔得一根不剩。我听了不觉打了一个寒噤。",
        "写第二次枯水季观瀑的上半部分。先写谷底的开阔和黄河的石床，再写河心龙槽的形态和壶口的成因，最后浓墨重彩地描写河水从五百米宽河道涌入龙槽的壮观景象，以黑猪被拔毛的传说侧面写漩涡威力。",
        "对比：与雨季的“急慌慌”“匆匆逃离”对比，这次“从从容容”，为细致描写提供条件。比喻：黄河像是一张极大的石床；其势如千军万马；排排黄浪霎时碎成堆堆白雪。拟人：互相挤着、撞着，推推搡搡，前呼后拥；它们还来不及想一下，便一齐跌了进去，赋予河水以人的动作和情态。多角度写景：远观（五百米宽的河道上排排涌来）、近看（龙槽顶着宽宽的河面）、仰视（山是青冷的灰，天是寂寂的蓝）、俯视（沟底飞转着一个个漩涡）。侧面烘托：黑猪掉进去毛被拔光，以传说写漩涡威力之大，比直接描写更有冲击力。炼字：涌、挤、撞、推、搡、跌，一系列动词精准写出水的动态和力量。",
        [
            ("枯水季节", "河流处于最低水位的时期，通常在冬春"),
            ("春寒", "春季的寒冷，倒春寒"),
            ("谷底", "山谷的底部"),
            ("石床", "像床一样平坦的岩石河床"),
            ("细沙", "细小的沙粒"),
            ("坚实", "结实、牢固"),
            ("河心", "河流的中心"),
            ("凹下去", "中间向下陷进去"),
            ("龙槽", "壶口瀑布处黄河河床被水冲刷形成的深槽，当地人称为龙槽"),
            ("深不可测", "深得无法测量，形容极深"),
            ("倚", "靠着"),
            ("丁字", "像“丁”字的形状"),
            ("河道", "河水流经的路线"),
            ("千军万马", "形容雄壮的队伍或浩大的声势"),
            ("推推搡搡", "（sǎng）粗暴地、接连不断地猛推"),
            ("前呼后拥", "前面有人吆喝开道，后面有人簇拥护卫，多形容随从多、排场大；文中形容水势拥挤"),
            ("霎时", "极短的时间、片刻"),
            ("驰骋", "（chí chěng）（骑马）奔驰；文中形容河水自由自在地奔流"),
            ("漩涡", "（xuán wō）水流旋转时形成的螺旋形水涡"),
            ("寒噤", "（hán jìn）寒战，因寒冷或害怕而身体颤动"),
        ],
    ),
    (
        "黄河在这里由宽而窄，由高到低，只见那平坦如席的大水像是被一个无形的大洞吸着，顿然拢成一束，向龙槽里隆隆冲去，先跌在石上，翻个身再跌下去，三跌、四跌，一川大水硬是这样被跌得粉碎，碎成点，碎成雾。从沟底升起一道彩虹，横跨龙槽，穿过雾霭，消失在远山青色的背景中。当然这么窄的壶口一时容不下这么多的水，于是洪流便向两边涌去，沿着龙槽的边沿轰然而下，平平的，大大的，浑厚庄重如一卷飞毯从空抖落。不，简直如一卷钢板出轧，的确有那种凝重，那种猛烈。尽管这样，壶口还是不能尽收这一川黄浪，于是又有一些各自夺路而走的，乘隙而进的，折返迂回的，它们在龙槽两边的滩壁上散开来，或钻石觅缝，汩汩如泉；或淌过石板，潺潺成溪；或被夹在石间，哀哀打漩。还有那顺壁挂下的，亮晶晶的如丝如缕……而这一切都隐在湿漉漉的水雾中，罩在七色彩虹中，像一曲交响乐，一幅写意画。我突然陷入沉思，眼前这个小小的壶口，怎么一下子集纳了海、河、瀑、泉、雾所有水的形态，兼容了喜、怒、哀、怨、愁，人的各种感情。造物者难道是要在这壶口中浓缩一个世界吗？",
        "详细描写黄河水在壶口的各种形态：主流跌入龙槽被跌得粉碎，洪流沿边沿轰然而下如飞毯如钢板，余水在滩壁上散开成泉、溪、雾、丝缕。最后作者陷入沉思，感悟壶口集纳了水的所有形态和人的各种感情，浓缩了一个世界。",
        "动词精准：拢、冲、跌、翻、碎、涌、轰、夺、钻、淌、夹、挂，一连串动词写出水在不同位置的不同动态。比喻：浑厚庄重如一卷飞毯从空抖落；简直如一卷钢板出轧（以“不”否定前喻，递进为更有力度的后喻）；像一曲交响乐，一幅写意画（通感，将视觉形象转化为听觉和艺术感受）。排比：或钻石觅缝，汩汩如泉；或淌过石板，潺潺成溪；或被夹在石间，哀哀打漩，写余水的三种形态。动静结合：动写水的各种流动，静写彩虹横跨、远山青色背景。虚实结合：实写水的形态，虚写人的各种感情、浓缩一个世界。拟人：各自夺路而走的，乘隙而进的，折返迂回的，赋予水以人的意志。反问：造物者难道是要在这壶口中浓缩一个世界吗？引发读者思考，升华意境。",
        [
            ("由宽而窄", "从宽阔变得狭窄"),
            ("平坦如席", "平坦得像席子一样"),
            ("拢成一束", "收拢聚集成一股"),
            ("隆隆", "拟声词，形容剧烈震动的声音"),
            ("粉碎", "破碎得像粉末一样"),
            ("雾霭", "（ǎi）雾气、云雾"),
            ("浑厚庄重", "厚重有力、庄严端正"),
            ("飞毯", "神话中能飞行的毯子"),
            ("钢板出轧", "（zhá）钢板从轧钢机中轧制出来，形容厚重猛烈"),
            ("凝重", "厚重、沉重"),
            ("猛烈", "气势大、力量大"),
            ("夺路而走", "争抢道路而走，形容水势急迫"),
            ("乘隙而进", "趁着空隙而进入"),
            ("折返迂回", "返回、绕弯前行"),
            ("滩壁", "河滩两边的岩壁"),
            ("钻石觅缝", "钻进石头寻找缝隙"),
            ("汩汩", "（gǔ gǔ）拟声词，形容水流动的声音"),
            ("潺潺", "（chán chán）拟声词，形容溪水、泉水等流动的声音"),
            ("哀哀打漩", "悲伤地打着漩涡，拟人写水被夹在石间的情态"),
            ("如丝如缕", "像丝一样细，像线一样连绵"),
            ("湿漉漉", "（shī lù lù）形容物体潮湿的样子"),
            ("集纳", "收集、容纳"),
            ("兼容", "同时容纳、包容"),
            ("造物者", "指创造万物的上天、大自然"),
            ("浓缩", "用加热等方法使溶液中的溶剂蒸发而提高浓度；文中指高度概括、凝聚"),
        ],
    ),
    (
        "看罢水，我再细观察脚下的石。这些如钢似铁的顽物竟被水凿得窟窟窍窍，如蜂窝杂陈，更有一些地方被旋出一个个光溜溜的大坑，而整个龙槽就是这样被水齐齐地切下去，切出一道深沟。人常以柔情比水，但至柔至和的水一旦被压迫竟会这样怒不可遏。原来这柔和之中只有宽厚绝无软弱，当她忍耐到一定程度时就会以力相较，奋力抗争。据《元和郡县图志》中所载，当年壶口的位置还在这下游一千五百米处。你看，日夜不止，这柔和的水硬将铁硬的石一寸寸地剁去。",
        "写作者观察脚下的石头，描写石头被水凿出的各种痕迹（窟窟窍窍、光溜溜的大坑、深沟），由此感悟至柔至和的水一旦被压迫竟会怒不可遏，以柔克刚的力量，并引用古籍记载佐证水的侵蚀力量。",
        "比喻：如钢似铁的顽物、如蜂窝杂陈，写石头的坚硬和被凿后的形态。拟人：至柔至和的水一旦被压迫竟会这样怒不可遏；这柔和之中只有宽厚绝无软弱，赋予水以人的性格和情感。对比：柔情比水 vs 怒不可遏；柔和的水 vs 铁硬的石，在对比中突出水以柔克刚的力量。引用：《元和郡县图志》所载壶口位置在下游一千五百米处，以历史记载佐证水日夜侵蚀的力量，增强说服力。炼字：凿、旋、切、剁，四个动词力度递增，写出水侵蚀石头的过程和力量。以小见大：从脚下石头被水侵蚀的细微痕迹，感悟水的性格和力量，为下文写黄河的伟大性格做铺垫。",
        [
            ("顽物", "顽固坚硬的东西，文中指石头"),
            ("窟窟窍窍", "形容石头上有许多孔洞的样子"),
            ("蜂窝杂陈", "像蜂窝一样杂乱地排列着"),
            ("旋出", "旋转着冲刷出来"),
            ("光溜溜", "形容光滑的样子"),
            ("齐齐地", "整齐、一致地"),
            ("至柔至和", "最柔和、最温和"),
            ("压迫", "用权势或势力强制别人服从；文中指水被地形约束"),
            ("怒不可遏", "愤怒得不能抑制，形容愤怒到了极点"),
            ("宽厚", "宽大厚道"),
            ("软弱", "缺乏力气、不坚强"),
            ("忍耐", "把痛苦的感觉或某种情绪抑制住不使表现出来"),
            ("以力相较", "用力量来较量、对抗"),
            ("奋力抗争", "竭尽全力抵抗、斗争"),
            ("《元和郡县图志》", "唐代李吉甫编撰的地理名著，是我国现存最早的地理总志"),
            ("所载", "所记载的内容"),
            ("剁去", "用刀向下砍，文中形容水侵蚀石头的力量"),
        ],
    ),
    (
        "黄河博大宽厚，柔中有刚；挟而不服，压而不弯；不平则呼，遇强则抗，死地必生，勇往直前。正像一个人，经了许多磨难便有了自己的个性；黄河被两岸的山，地下的石逼得忽上忽下，忽左忽右时，也就铸成了自己伟大的性格。这伟大只在冲过壶口的一刹那才闪现出来被我们看见。",
        "总结黄河的性格：博大宽厚、柔中有刚、挟而不服、压而不弯、不平则呼、遇强则抗、死地必生、勇往直前。由黄河的性格联想到人经磨难形成个性，点明主旨——黄河的伟大性格正是中华民族精神的象征。",
        "排比：博大宽厚，柔中有刚；挟而不服，压而不弯；不平则呼，遇强则抗，死地必生，勇往直前，四字短语排比，节奏铿锵，气势磅礴，概括黄河的性格。拟人：黄河被两岸的山，地下的石逼得……铸成了自己伟大的性格，赋予黄河以人的意志和性格。托物言志：由黄河的性格联想到人经磨难形成个性，进而象征中华民族压而不弯、勇往直前的精神，卒章显志。长短句结合：四字短语排比短促有力，长句“正像一个人……”舒缓深沉，节奏富于变化。炼字：挟、压、呼、抗、生、冲、铸、闪，动词精准有力。",
        [
            ("博大宽厚", "宽广宏大、宽大厚道"),
            ("柔中有刚", "柔和之中蕴含着刚强"),
            ("挟而不服", "被挟持却不屈服"),
            ("压而不弯", "被压迫却不弯曲"),
            ("不平则呼", "遇到不公平就呼喊、抗争"),
            ("遇强则抗", "遇到强者就抵抗"),
            ("死地必生", "在绝境中必定寻求生机"),
            ("勇往直前", "勇敢地一直向前进"),
            ("磨难", "在艰难困苦的境遇中遭受的折磨"),
            ("个性", "一个人比较固定的特性"),
            ("铸成", "铸造形成，比喻造就"),
            ("一刹那", "极短的时间"),
            ("闪现", "一瞬间出现、呈现"),
        ],
    ),
]

parts = [
    ("第一部分", "总起：两次到访", "第1段", "交代壶口的地理位置和作者两次到访的经历，总起全文，为下文两次观瀑的对比做铺垫。"),
    ("第二部分", "雨季观瀑：惊险匆匆", "第2段", "写第一次雨季观瀑，以声、雾、水汽侧面烘托瀑布的壮观与危险，作者匆匆逃离，与下文枯水季形成对比。"),
    ("第三部分", "枯水观瀑：壮美沉思", "第3–4段", "详写第二次枯水季观瀑，先写龙槽形态和河水涌入的壮观，再写水在壶口的各种形态，最后作者陷入沉思，感悟壶口浓缩了一个世界。"),
    ("第四部分", "观石悟理：黄河性格", "第5–6段", "由脚下的石头被水侵蚀的痕迹，感悟水以柔克刚的力量，进而总结黄河博大宽厚、柔中有刚的伟大性格，点明主旨。"),
]

para_part = [0, 1, 2, 2, 3, 3]

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
                span = '<span class="anno-word" data-note="' + note + '">' + word + '</span>'
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
        verse_html += '      <div class="part-head"><span class="p-num">' + pname + '</span><h3>' + ptitle + '</h3><span class="range">' + prange + '</span></div>\n'
        verse_html += '      <div class="part-overview">' + poverview + '</div>\n'
    orig_ann = annotate(orig, annos)
    verse_html += '      <div class="verse" id="l' + str(i+1) + '" data-i="' + str(i) + '">\n'
    verse_html += '        <div class="v-top"><span class="v-no">' + str(i+1) + '</span><div class="v-line">' + orig_ann + '</div></div>\n'
    verse_html += '        <details class="v-more">\n'
    verse_html += '          <summary>内容 · 手法</summary>\n'
    verse_html += '          <div class="d-body">\n'
    verse_html += '            <div class="v-sec"><b class="v-label">内容概括</b>\n'
    verse_html += '              <div class="v-trans">' + content + '</div>\n'
    verse_html += '            </div>\n'
    verse_html += '            <div class="v-sec"><b class="v-label">手法分析</b>\n'
    verse_html += '              <div class="d-body"><p>' + method + '</p></div>\n'
    verse_html += '            </div>\n'
    verse_html += '          </div>\n'
    verse_html += '        </details>\n'
    verse_html += '      </div>\n'

fulltext_html = ""
for para in fulltext_paras:
    fulltext_html += '    <div class="pl">' + para + '</div>\n'

dict_words = [
    {"w":"诫","py":"jiè","q":"临出发时有人告□：这个时节看壶口最危险","tip":"「诫」言字旁，警告劝诫；不要写成「戒」（戈字旁）"},
    {"w":"峰","py":"fēng","q":"一个洪□下来，根本来不及上岸","tip":"「峰」山字旁，山峰；与「锋」（金字旁）区分"},
    {"w":"漫","py":"màn","q":"河谷里雾气弥□","tip":"「漫」三点水，充满；与「慢」（竖心旁）区分"},
    {"w":"仰","py":"yǎng","q":"让人们□视垂空的水幕","tip":"「仰」单人旁，抬头；与「抑」（yì，压制）区分"},
    {"w":"溢","py":"yì","q":"那沟已被灌得浪沫横□","tip":"「溢」三点水，满而流出；不要写成「益"},
    {"w":"聋","py":"lóng","q":"震耳欲□的涛声","tip":"「聋」耳字旁，听不见；不要写成「笼」（竹字头）"},
    {"w":"慌慌","py":"huāng huāng","q":"只急□□地扫了几眼","tip":"叠词「慌慌」整体作答；「慌」竖心旁，急忙；与「荒」（草字头）区分"},
    {"w":"匆匆","py":"cōng cōng","q":"我便□□逃离","tip":"叠词「匆匆」整体作答；「匆」撇加点，急忙；与「勿」（wù，不要）区分"},
    {"w":"槽","py":"cáo","q":"当地人叫龙□","tip":"「槽」木字旁，两边高起中间凹下的器具；与「糟」（米字旁）区分"},
    {"w":"测","py":"cè","q":"槽头入水处深不可□","tip":"「测」三点水，测量；与「侧」（单人旁）区分"},
    {"w":"倚","py":"yǐ","q":"我□在一块大石头上向上游看去","tip":"「倚」单人旁，靠着；与「椅」（木字旁）区分"},
    {"w":"搡搡","py":"sǎng sǎng","q":"互相挤着、撞着，推推□□","tip":"叠词「搡搡」整体作答；「搡」提手旁，猛推；生僻字"},
    {"w":"拥","py":"yōng","q":"前呼后□，撞向石壁","tip":"「拥」提手旁，簇拥；与「佣」（单人旁）区分"},
    {"w":"霎","py":"shà","q":"排排黄浪□时碎成堆堆白雪","tip":"「霎」雨字头，极短时间；与「刹」（chà，单人旁）区分"},
    {"w":"骋","py":"chěng","q":"当河水正这般畅畅快快地驰□着时","tip":"「骋」马字旁，奔驰；与「聘」（pìn，耳字旁）区分"},
    {"w":"漩","py":"xuán","q":"沟底飞转着一个个□涡","tip":"「漩」三点水，旋转的水流；与「旋」（方字旁）区分"},
    {"w":"噤","py":"jìn","q":"我听了不觉打了一个寒□","tip":"「噤」口字旁，寒战；生僻字，注意是口字旁不是竖心旁"},
    {"w":"拢","py":"lǒng","q":"顿然□成一束，向龙槽里隆隆冲去","tip":"「拢」提手旁，收拢；与「笼」（竹字头）区分"},
    {"w":"隆隆","py":"lóng lóng","q":"向龙槽里□□冲去","tip":"叠词「隆隆」整体作答；「隆」左耳旁，盛大；与「窿」（穴宝盖）区分"},
    {"w":"霭","py":"ǎi","q":"穿过雾□，消失在远山青色的背景中","tip":"「霭」雨字头，云雾；与「蔼」（ǎi，草字头，和蔼）区分"},
    {"w":"轧","py":"zhá","q":"简直如一卷钢板出□","tip":"「轧」车字旁，碾压；多音字，此处读zhá不读yà"},
    {"w":"迂","py":"yū","q":"折返□回的","tip":"「迂」走之底，绕弯；与「遇」（yù）区分"},
    {"w":"汩汩","py":"gǔ gǔ","q":"或钻石觅缝，□□如泉","tip":"叠词「汩汩」整体作答；「汩」三点水，水流声；与「汨」（mì，汨罗江）区分"},
    {"w":"潺潺","py":"chán chán","q":"或淌过石板，□□成溪","tip":"叠词「潺潺」整体作答；「潺」三点水，溪水流动声；生僻字"},
    {"w":"漉漉","py":"lù lù","q":"而这一切都隐在湿□□的水雾中","tip":"叠词「漉漉」整体作答；「漉」三点水，液体慢慢渗出；生僻字"},
    {"w":"纳","py":"nà","q":"怎么一下子集□了海、河、瀑、泉、雾所有水的形态","tip":"「纳」绞丝旁，收进来；与「呐」（口字旁）区分"},
    {"w":"窟窟","py":"kū kū","q":"竟被水凿得□□窍窍","tip":"叠词「窟窟」整体作答；「窟」穴宝盖，孔洞；与「崫」区分"},
    {"w":"窍窍","py":"qiào qiào","q":"竟被水凿得窟窟□□","tip":"叠词「窍窍」整体作答；「窍」穴宝盖，孔洞；与「窃」（qiè，盗窃）区分"},
    {"w":"遏","py":"è","q":"但至柔至和的水一旦被压迫竟会这样怒不可□","tip":"「遏」走之底，阻止；生僻字，成语「怒不可遏」"},
    {"w":"剁","py":"duò","q":"这柔和的水硬将铁硬的石一寸寸地□去","tip":"「剁」立刀旁，用刀向下砍；与「跺」（duò，足字旁，跺脚）区分"},
    {"w":"挟","py":"xié","q":"黄河博大宽厚，柔中有刚；□而不服，压而不弯","tip":"「挟」提手旁，用胳膊夹住；多音字，此处读xié不读jiā"},
    {"w":"铸","py":"zhù","q":"也就□成了自己伟大的性格","tip":"「铸」金字旁，铸造；与「祷」（dǎo，示字旁，祈祷）区分"},
    {"w":"刹","py":"chà","q":"这伟大只在冲过壶口的一□那才闪现出来","tip":"「刹」立刀旁，极短时间；多音字，此处读chà不读shā；与「霎」（shà）区分"},
]

dict_notes = [
    {"w":"弥漫","a":"（烟尘、雾气、水等）充满、布满","q":"河谷里雾气弥漫"},
    {"w":"震耳欲聋","a":"耳朵都快震聋了，形容声音很大","q":"震耳欲聋的涛声"},
    {"w":"深不可测","a":"深得无法测量，形容极深","q":"槽头入水处深不可测"},
    {"w":"千军万马","a":"形容雄壮的队伍或浩大的声势","q":"其势如千军万马"},
    {"w":"推推搡搡","a":"粗暴地、接连不断地猛推","q":"互相挤着、撞着，推推搡搡"},
    {"w":"前呼后拥","a":"前面有人吆喝开道，后面有人簇拥护卫，多形容随从多排场大","q":"前呼后拥，撞向石壁"},
    {"w":"驰骋","a":"（骑马）奔驰；文中形容河水自由自在地奔流","q":"当河水正这般畅畅快快地驰骋着时"},
    {"w":"寒噤","a":"寒战，因寒冷或害怕而身体颤动","q":"我听了不觉打了一个寒噤"},
    {"w":"雾霭","a":"雾气、云雾","q":"穿过雾霭，消失在远山青色的背景中"},
    {"w":"浑厚庄重","a":"厚重有力、庄严端正","q":"浑厚庄重如一卷飞毯从空抖落"},
    {"w":"凝重","a":"厚重、沉重","q":"的确有那种凝重，那种猛烈"},
    {"w":"夺路而走","a":"争抢道路而走，形容水势急迫","q":"于是又有一些各自夺路而走的"},
    {"w":"乘隙而进","a":"趁着空隙而进入","q":"乘隙而进的"},
    {"w":"折返迂回","a":"返回、绕弯前行","q":"折返迂回的"},
    {"w":"钻石觅缝","a":"钻进石头寻找缝隙","q":"或钻石觅缝，汩汩如泉"},
    {"w":"汩汩","a":"拟声词，形容水流动的声音","q":"或钻石觅缝，汩汩如泉"},
    {"w":"潺潺","a":"拟声词，形容溪水、泉水等流动的声音","q":"或淌过石板，潺潺成溪"},
    {"w":"如丝如缕","a":"像丝一样细，像线一样连绵","q":"还有那顺壁挂下的，亮晶晶的如丝如缕"},
    {"w":"集纳","a":"收集、容纳","q":"怎么一下子集纳了海、河、瀑、泉、雾所有水的形态"},
    {"w":"兼容","a":"同时容纳、包容","q":"兼容了喜、怒、哀、怨、愁，人的各种感情"},
    {"w":"浓缩","a":"用加热等方法使溶液浓度提高；文中指高度概括、凝聚","q":"造物者难道是要在这壶口中浓缩一个世界吗"},
    {"w":"窟窟窍窍","a":"形容石头上有许多孔洞的样子","q":"竟被水凿得窟窟窍窍"},
    {"w":"蜂窝杂陈","a":"像蜂窝一样杂乱地排列着","q":"如蜂窝杂陈"},
    {"w":"怒不可遏","a":"愤怒得不能抑制，形容愤怒到了极点","q":"但至柔至和的水一旦被压迫竟会这样怒不可遏"},
    {"w":"以力相较","a":"用力量来较量、对抗","q":"当她忍耐到一定程度时就会以力相较"},
    {"w":"奋力抗争","a":"竭尽全力抵抗、斗争","q":"奋力抗争"},
    {"w":"博大宽厚","a":"宽广宏大、宽大厚道","q":"黄河博大宽厚，柔中有刚"},
    {"w":"柔中有刚","a":"柔和之中蕴含着刚强","q":"黄河博大宽厚，柔中有刚"},
    {"w":"勇往直前","a":"勇敢地一直向前进","q":"死地必生，勇往直前"},
    {"w":"铸成","a":"铸造形成，比喻造就","q":"也就铸成了自己伟大的性格"},
    {"w":"一刹那","a":"极短的时间","q":"这伟大只在冲过壶口的一刹那才闪现出来"},
]

html = '<!DOCTYPE html>\n'
html += '<html lang="zh-CN">\n'
html += '<head>\n'
html += '<meta charset="UTF-8">\n'
html += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
html += '<title>《壶口瀑布》梁衡</title>\n'
html += '<style>' + style + '</style>\n'
html += '</head>\n'
html += '<body data-fs="100">\n\n'

html += '<header class="hero">\n'
html += '  <div class="hero-side">现代 · 梁衡</div>\n'
html += '  <h1 class="hero-title">壶口瀑布</h1>\n'
html += '</header>\n\n'

html += '<nav class="nav">\n'
html += '  <div class="nav-in">\n'
html += '    <a href="#bg">背景</a>\n'
html += '    <a href="#jielu">解读</a>\n'
html += '    <a href="#app">赏析</a>\n'
html += '    <a href="#acc">积累</a>\n'
html += '    <a href="#practice">练习</a>\n'
html += '    <div class="tool">\n'
html += '      <select id="fsSel" class="fs-sel" title="正文字体大小">\n'
html += '        <option value="100">100%</option>\n'
html += '        <option value="150">150%</option>\n'
html += '        <option value="200">200%</option>\n'
html += '        <option value="250">250%</option>\n'
html += '        <option value="300">300%</option>\n'
html += '      </select>\n'
html += '      <button id="btnAll">展开</button>\n'
html += '      <button id="btnRecite">背诵</button>\n'
html += '      <button id="btnPrint">打印</button>\n'
html += '    </div>\n'
html += '  </div>\n'
html += '</nav>\n\n'

html += '<main class="wrap">\n'

# 背景区
html += '<section id="bg" class="sec">\n'
html += '  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 游记背景 · 文体知识</span></div>\n'
html += '  <div class="lead">\n'
html += '    <p>《壶口瀑布》是梁衡写的一篇游记散文，选自《梁衡文集》。文章记述了作者两次到壶口瀑布观瀑的经历，通过对黄河水在壶口的各种形态的细腻描写，感悟黄河博大宽厚、柔中有刚的伟大性格，进而赞美中华民族压而不弯、勇往直前的精神。</p>\n'
html += '    <p>文章以游踪为线索，先略写雨季观瀑的惊险，再详写枯水季观瀑的壮美，最后由水及石、由石及理，卒章显志。写景细腻生动，用词准确精妙，融情于景，托物言志，是游记散文的典范之作。</p>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <h3>作者简介</h3>\n'
html += '    <p>梁衡，1946年生，山西霍州人，著名学者、新闻理论家、作家。曾任国家新闻出版署副署长、《人民日报》副总编辑。长期从事散文创作和新闻理论研究，作品多次入选中学语文教材。</p>\n'
html += '    <p style="margin-top:10px;color:var(--ink2)">梁衡的散文以理性见长，善于在对自然山水的描写中融入对历史、人生和民族精神的思考。代表作有《晋祠》《觅渡，觅渡，渡何处？》《把栏杆拍遍》等，《壶口瀑布》是其游记散文的代表作品。</p>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <h3>游记背景</h3>\n'
html += '    <p>壶口瀑布位于黄河中游，地处山西吉县与陕西宜川县交界处，是黄河上唯一的黄色大瀑布，也是中国第二大瀑布。黄河流至壶口一带，两岸苍山夹峙，河床由宽骤然收窄，河水从二十多米高的陡崖上倾注而泻，形成“千里黄河一壶收”的气概。</p>\n'
html += '    <p style="margin-top:8px">作者梁衡曾两次到访壶口：第一次在雨季，瀑布水势浩大但危险，作者匆匆一瞥；第二次在枯水季节，作者从容细致地观察了瀑布的各种形态，由此产生深刻感悟，写下了这篇散文。文章发表于1993年8月23日《人民日报》，后被收入多种版本的中学语文教材。</p>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <h3>文体知识：游记散文</h3>\n'
html += '    <p><b>游记：</b>游记是描写旅行见闻的一种散文体裁，以轻快的笔调和生动的描写，记叙旅途中的见闻（如某地的政治生活、社会风情、山川景物、名胜古迹等），并表达作者的思想感情。</p>\n'
html += '    <p style="margin-top:8px"><b>游记的三要素：</b>所至（游踪线索，即作者的行踪）、所见（景物描写，即作者看到的景象）、所感（思想感情，即作者的感悟和思考）。本文以两次观瀑的游踪为线索，以壶口瀑布的各种形态为描写对象，以对黄河性格和民族精神的感悟为旨归，三要素兼备。</p>\n'
html += '    <p style="margin-top:8px"><b>游记的常见写法：</b>移步换景（随游踪变化描写不同景物）、定点观景（在一个观察点多角度描写）、情景交融（写景与抒情结合）、托物言志（借景物表达志向和感悟）。本文综合运用了多种写法。</p>\n'
html += '  </div>\n'

html += '  <div class="box media-box">\n'
html += '    <h3>视听</h3>\n'
html += '    <div class="media-grid">\n'
html += '      <div class="media">\n'
html += '        <h4>课文诵读《壶口瀑布》</h4>\n'
html += '        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV16E411L7AH&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读壶口瀑布"></iframe>\n'
html += '        <a href="https://www.bilibili.com/video/BV16E411L7AH" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>\n'
html += '      </div>\n'
html += '      <div class="media">\n'
html += '        <h4>壶口瀑布风光：黄河在此怒吼</h4>\n'
html += '        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV14T3k6ZEVZ&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="壶口瀑布风光纪录片"></iframe>\n'
html += '        <a href="https://www.bilibili.com/video/BV14T3k6ZEVZ" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>\n'
html += '      </div>\n'
html += '    </div>\n'
html += '  </div>\n'
html += '</section>\n\n'

html += '<div class="divider"></div>\n'

# 解读区
html += '<section id="jielu" class="sec">\n'
html += '  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 内容概括 · 手法分析</span></div>\n'
html += '  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>\n'
html += '  <div id="fulltext" class="poem" style="display:none">\n'
html += fulltext_html
html += '  </div>\n'
html += '  <div class="verse-list" id="verseList">\n'
html += verse_html
html += '  </div>\n'
html += '</section>\n\n'

html += '<div class="divider"></div>\n'

# 赏析区
html += '<section id="app" class="sec">\n'
html += '  <div class="sec-head"><h2>赏 析</h2><span class="no">游踪线索 · 写景艺术 · 语言特色 · 情感表达 · 主题思想</span></div>\n'

html += '  <div class="box">\n'
html += '    <h3>游踪线索</h3>\n'
html += '    <div class="fame">\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">两次观瀑，一略一详</div>\n'
html += '        <p>文章以作者两次到壶口观瀑的游踪为线索。第一次是雨季，作者在他人告诫后下到河滩，但因水势危险、雾气弥漫，只“急慌慌地扫了几眼”便“匆匆逃离”，这是略写，为下文做铺垫和对比。第二次是枯水季节，作者“从从容容地下到沟底”，走到河心观察龙槽，再看河水涌入龙槽的各种形态，最后观察脚下的石头，这是详写，是文章的主体。</p>\n'
html += '      </div>\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">观察点的变化：由远及近，由上到下</div>\n'
html += '        <p>枯水季观瀑部分，作者的观察点不断变化：先在沟底远望（黄河像是一张极大的石床），再走到河心近看（龙槽顶着宽宽的河面，正好形成一个丁字），然后向上游看去（河水从五百米宽的河道上排排涌来），再俯视沟底（飞转着一个个漩涡），接着看水在龙槽的各种形态，最后看脚下的石头。观察点由远及近、由上到下、由水到石，层次分明，条理清晰。</p>\n'
html += '      </div>\n'
html += '    </div>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <h3>写景艺术</h3>\n'
html += '    <div class="fame">\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">多角度写景：远近高低俯仰</div>\n'
html += '        <p>文章善于从不同角度描写壶口瀑布。远观：“河水从五百米宽的河道上排排涌来，其势如千军万马”，写水势的浩大和气势；近看：“这龙槽顶着宽宽的河面，正好形成一个丁字”，写壶口的形态；仰视：“山是青冷的灰，天是寂寂的蓝，宇宙间仿佛只有这水的存在”，以远山蓝天衬托水的主体地位；俯视：“沟底飞转着一个个漩涡”，写水跌入深沟后的状态。多角度描写使壶口瀑布的形象立体丰满。</p>\n'
html += '      </div>\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">多感官描写：视听触结合</div>\n'
html += '        <p>文章调动多种感官描写瀑布。听觉：“涛声隐隐如雷”“震耳欲聋的涛声”“隆隆冲去”“轰然而下”“汩汩如泉”“潺潺成溪”，从远到近、从大到小写出水的各种声音；视觉：“雾气弥漫”“浪沫横溢”“排排黄浪霎时碎成堆堆白雪”“一道彩虹，横跨龙槽”“亮晶晶的如丝如缕”，写出水的各种色彩和形态；触觉：“扑面而来的水汽”“踏上去坚实而又松软”，写出水汽和细沙的触感。多感官描写使读者如临其境。</p>\n'
html += '      </div>\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">动静结合与虚实结合</div>\n'
html += '        <p>动静结合：文章既写水的动态（涌、挤、撞、跌、冲、淌），又写静景（彩虹横跨龙槽、远山青色背景、如钢似铁的顽石），以静衬动，更显水的生命力。虚实结合：实写水的各种具体形态（海、河、瀑、泉、雾），虚写人的各种感情（喜、怒、哀、怨、愁）和“浓缩一个世界”的哲理思考，由实入虚，意境深远。</p>\n'
html += '      </div>\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">比喻、拟人、排比的综合运用</div>\n'
html += '        <p>比喻：“那河就像一锅正沸着的水”“其势如千军万马”“排排黄浪霎时碎成堆堆白雪”“浑厚庄重如一卷飞毯从空抖落”“简直如一卷钢板出轧”“像一曲交响乐，一幅写意画”，比喻新奇贴切，形象生动。拟人：“互相挤着、撞着，推推搡搡，前呼后拥”“各自夺路而走的，乘隙而进的，折返迂回的”“至柔至和的水一旦被压迫竟会这样怒不可遏”，赋予水以人的动作、意志和情感。排比：“或钻石觅缝，汩汩如泉；或淌过石板，潺潺成溪；或被夹在石间，哀哀打漩”，写余水的三种形态，节奏明快。</p>\n'
html += '      </div>\n'
html += '    </div>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <h3>语言特色：炼字精准，富有画面感</h3>\n'
html += '    <div class="fame">\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">动词的精准运用：“铸”“拢”“冲”“轰”</div>\n'
html += '        <p>文章的动词运用极为精准。“拢”字写黄河水由宽而窄聚集成束的形态，准确而有力；“冲”字写水向龙槽奔去的力度和速度；“轰”字（轰然而下）从听觉角度写洪流沿龙槽边沿落下的巨大声响；“铸”字（铸成了自己伟大的性格）将黄河的性格形成比作金属铸造，既有力度又有历史厚重感。此外，“跌”字写水从高处落入深沟的状态，“碎”字写水被撞后的形态，“凿”“旋”“切”“剁”写水侵蚀石头的过程，个个精准传神。</p>\n'
html += '      </div>\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">叠词与拟声词的运用</div>\n'
html += '        <p>文章大量运用叠词和拟声词，增强了语言的音乐美和画面感。叠词：“排排涌来”“推推搡搡”“排排黄浪”“堆堆白雪”“畅畅快快”“窟窟窍窍”“光溜溜”“齐齐地”“一寸寸”，或写形态，或写动作，或写程度，节奏明快，形象生动。拟声词：“隐隐如雷”“隆隆冲去”“轰然而下”“汩汩如泉”“潺潺成溪”“哀哀打漩”，从声音角度写出水在不同位置、不同状态下的声响，如闻其声。</p>\n'
html += '      </div>\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">长短句结合，节奏富于变化</div>\n'
html += '        <p>文章句式灵活多变。描写水势时多用短句，如“更涌、更挤、更急”“碎成点，碎成雾”“平平的，大大的”，节奏急促，与水的湍急相呼应；抒情议论时多用长句，如“正像一个人，经了许多磨难便有了自己的个性；黄河被两岸的山，地下的石逼得忽上忽下，忽左忽右时，也就铸成了自己伟大的性格”，节奏舒缓，深沉有力。结尾的四字短语排比（博大宽厚，柔中有刚；挟而不服，压而不弯……）更是节奏铿锵，气势磅礴。</p>\n'
html += '      </div>\n'
html += '    </div>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <h3>情感表达：融情于景，托物言志</h3>\n'
html += '    <div class="fame">\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">融情于景：在描写中自然流露赞美之情</div>\n'
html += '        <p>文章对壶口瀑布的描写中自然融入了作者的赞美和惊叹之情。雨季观瀑时，“可怕的警觉”“心还在不住地跳”，以作者的恐惧侧面写瀑布的威力，暗含对自然伟力的敬畏；枯水季观瀑时，“其势如千军万马”“浑厚庄重如一卷飞毯从空抖落”“简直如一卷钢板出轧”，比喻中饱含对黄河壮美的赞叹；“像一曲交响乐，一幅写意画”，更是直接以艺术美来赞美瀑布。作者的情感不是直白地喊出来，而是融在具体的描写之中，情景交融。</p>\n'
html += '      </div>\n'
html += '      <div class="fame-card">\n'
html += '        <div class="f-line">托物言志：由黄河性格到民族精神</div>\n'
html += '        <p>文章由写景到悟理，由黄河的性格联想到人的个性，进而象征中华民族的精神。第五段写水以柔克刚，“至柔至和的水一旦被压迫竟会这样怒不可遏”“这柔和之中只有宽厚绝无软弱”，已经在写水的性格；第六段直接总结黄河的性格：“博大宽厚，柔中有刚；挟而不服，压而不弯；不平则呼，遇强则抗，死地必生，勇往直前”，并说“正像一个人，经了许多磨难便有了自己的个性”。这里的黄河性格，正是中华民族历经磨难而不屈不挠、勇往直前的民族精神的象征。文章托物言志，卒章显志，意蕴深厚。</p>\n'
html += '      </div>\n'
html += '    </div>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <h3>主题思想</h3>\n'
html += '    <p>《壶口瀑布》通过记述作者两次到壶口瀑布观瀑的经历，细致描写了黄河水在壶口的各种壮美形态，由水及石、由石及理，感悟到黄河博大宽厚、柔中有刚、挟而不服、压而不弯、勇往直前的伟大性格，进而赞美中华民族历经磨难而不屈不挠、压而不弯、勇往直前的民族精神。文章融情于景，托物言志，既是对自然伟力的礼赞，也是对民族精神的讴歌。</p>\n'
html += '  </div>\n'
html += '</section>\n\n'

html += '<div class="divider"></div>\n'

# 积累区
html += '<section id="acc" class="sec">\n'
html += '  <div class="sec-head"><h2>积 累</h2><span class="no">重点词语 · 用字与读音 · 修辞方法 · 写作借鉴 · 文化常识</span></div>\n'

html += '  <div class="box">\n'
html += '    <div class="acc-cat">\n'
html += '      <h3>重点词语</h3>\n'
html += '      <div class="acc-item"><span class="acc-w">弥漫</span><span class="acc-d">（mí màn）（烟尘、雾气、水等）充满、布满。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">震耳欲聋</span><span class="acc-d">耳朵都快震聋了，形容声音很大。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">深不可测</span><span class="acc-d">深得无法测量，形容极深。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">千军万马</span><span class="acc-d">形容雄壮的队伍或浩大的声势。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">推推搡搡</span><span class="acc-d">（sǎng）粗暴地、接连不断地猛推。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">前呼后拥</span><span class="acc-d">前面有人吆喝开道，后面有人簇拥护卫，多形容随从多、排场大。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">霎时</span><span class="acc-d">（shà）极短的时间、片刻。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">驰骋</span><span class="acc-d">（chí chěng）（骑马）奔驰；文中形容河水自由自在地奔流。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">寒噤</span><span class="acc-d">（hán jìn）寒战，因寒冷或害怕而身体颤动。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">雾霭</span><span class="acc-d">（ǎi）雾气、云雾。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">浑厚庄重</span><span class="acc-d">厚重有力、庄严端正。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">凝重</span><span class="acc-d">厚重、沉重。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">汩汩</span><span class="acc-d">（gǔ gǔ）拟声词，形容水流动的声音。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">潺潺</span><span class="acc-d">（chán chán）拟声词，形容溪水、泉水等流动的声音。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">怒不可遏</span><span class="acc-d">（è）愤怒得不能抑制，形容愤怒到了极点。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">勇往直前</span><span class="acc-d">勇敢地一直向前进。</span></div>\n'
html += '    </div>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <div class="acc-cat">\n'
html += '      <h3>用字与读音</h3>\n'
html += '      <div class="acc-item"><span class="acc-w">弥漫</span><span class="acc-d">（mí màn）「弥」弓字旁，「漫」三点水；不要写成「迷漫」。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">告诫</span><span class="acc-d">（jiè）「诫」言字旁；与「戒」（jiè，戈字旁）区分。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">推推搡搡</span><span class="acc-d">（sǎng）「搡」提手旁，猛推；生僻字，不要写成「嗓」（口字旁）。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">霎时</span><span class="acc-d">（shà）「霎」雨字头；与「刹」（chà，立刀旁）区分，二者都可表示时间短。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">驰骋</span><span class="acc-d">（chí chěng）「骋」马字旁；与「聘」（pìn，耳字旁，聘请）区分。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">寒噤</span><span class="acc-d">（hán jìn）「噤」口字旁；生僻字，不要写成「禁」（示字旁）。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">雾霭</span><span class="acc-d">（ǎi）「霭」雨字头，云雾；与「蔼」（ǎi，草字头，和蔼）区分。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">出轧</span><span class="acc-d">（zhá）「轧」车字旁，碾压；多音字，此处读zhá，不读yà（倾轧）。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">汩汩</span><span class="acc-d">（gǔ gǔ）「汩」三点水，水流声；与「汨」（mì，汨罗江）区分，右边是「曰」不是「日」。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">潺潺</span><span class="acc-d">（chán chán）「潺」三点水，溪水流动声；生僻字，右边是「孱」。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">怒不可遏</span><span class="acc-d">（è）「遏」走之底，阻止；生僻字，成语固定写法。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">铸成</span><span class="acc-d">（zhù）「铸」金字旁，铸造；与「祷」（dǎo，示字旁，祈祷）区分。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">挟而不服</span><span class="acc-d">（xié）「挟」提手旁，用胳膊夹住；多音字，此处读xié，不读jiā。</span></div>\n'
html += '    </div>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <div class="acc-cat">\n'
html += '      <h3>修辞方法</h3>\n'
html += '      <div class="acc-item"><span class="acc-w">比喻</span><span class="acc-d">本文比喻新奇贴切。如“那河就像一锅正沸着的水”写雨季河水的翻滚；“其势如千军万马”写河水的浩大声势；“浑厚庄重如一卷飞毯从空抖落”“简直如一卷钢板出轧”以递进比喻写洪流的厚重猛烈；“像一曲交响乐，一幅写意画”以通感比喻写瀑布的整体美。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">拟人</span><span class="acc-d">赋予水以人的动作、意志和情感。如“互相挤着、撞着，推推搡搡，前呼后拥”写河水的拥挤；“各自夺路而走的，乘隙而进的，折返迂回的”写余水的不同走向；“至柔至和的水一旦被压迫竟会这样怒不可遏”写水的性格。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">“或钻石觅缝，汩汩如泉；或淌过石板，潺潺成溪；或被夹在石间，哀哀打漩”，写余水的三种形态，节奏明快。结尾“博大宽厚，柔中有刚；挟而不服，压而不弯；不平则呼，遇强则抗，死地必生，勇往直前”，四字短语排比，气势磅礴。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">反复</span><span class="acc-d">“冲进去，冲进去”写雨季水势之急之猛；“什么也看不见，什么也听不见”强调雨季雾大、水声大，作者什么也看不清。反复手法增强了语势和表达效果。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">通感</span><span class="acc-d">“像一曲交响乐，一幅写意画”，将视觉形象（瀑布的形态和色彩）转化为听觉感受（交响乐）和艺术感受（写意画），打通了视觉与听觉、视觉与艺术的界限，是通感手法。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">反问</span><span class="acc-d">“造物者难道是要在这壶口中浓缩一个世界吗？”以反问句式引发读者思考，壶口不仅集纳了水的各种形态，也兼容了人的各种感情，浓缩了一个世界，升华了文章的意境。</span></div>\n'
html += '    </div>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <div class="acc-cat">\n'
html += '      <h3>写作借鉴</h3>\n'
html += '      <div class="acc-item"><span class="acc-w">移步换景与定点观景结合</span><span class="acc-d">文章既随游踪变化描写不同景物（从沟底到河心，从上游到沟底，从水到石），又在固定观察点多角度描写（在河心向上游看、俯视沟底、看龙槽边沿），两种写法结合，条理清晰，描写全面。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">多角度多感官写景</span><span class="acc-d">从远近高低俯仰不同角度描写，调动视觉、听觉、触觉等多种感官，使景物形象立体丰满，读者如临其境。这是游记散文写景的基本方法，值得学习借鉴。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">动静结合与虚实结合</span><span class="acc-d">以静衬动（远山、蓝天、彩虹衬托水的动态），由实入虚（由水的具体形态联想到人的感情和世界哲理），使文章既有画面感又有思想深度。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">融情于景，托物言志</span><span class="acc-d">在写景中自然融入情感，不直白抒情；由景物的特征引申出哲理思考，卒章显志。本文由黄河的性格联想到民族精神，是托物言志的典范。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">详略得当，对比鲜明</span><span class="acc-d">雨季观瀑略写，枯水季观瀑详写，一略一详，重点突出；雨季的惊险慌乱与枯水季的从容细致形成对比，在对比中突出壶口瀑布在不同季节的不同面貌。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">炼字精准，富有画面感</span><span class="acc-d">动词（拢、冲、跌、碎、凿、旋、切、剁、铸）精准传神，叠词和拟声词（排排、堆堆、隆隆、汩汩、潺潺）增强音乐美和画面感，长短句结合使节奏富于变化。</span></div>\n'
html += '    </div>\n'
html += '  </div>\n'

html += '  <div class="box">\n'
html += '    <div class="acc-cat">\n'
html += '      <h3>文化常识</h3>\n'
html += '      <div class="acc-item"><span class="acc-w">壶口瀑布</span><span class="acc-d">位于黄河中游，山西吉县与陕西宜川县交界处，是黄河上唯一的黄色大瀑布，中国第二大瀑布。黄河流至壶口，河床由宽骤然收窄，河水从二十多米高的陡崖上倾注而泻，形成“千里黄河一壶收”的奇观。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">龙槽</span><span class="acc-d">壶口瀑布处黄河河床被水长期冲刷形成的深槽，因传说为巨龙穿山留下的痕迹而得名。龙槽是壶口瀑布的核心景观，河水跌入龙槽后形成壮观的瀑布。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">《元和郡县图志》</span><span class="acc-d">唐代李吉甫编撰的地理名著，共四十卷，是我国现存最早的地理总志。记载了唐代全国各郡县的沿革、户口、山川、古迹等，是研究唐代地理的重要文献。</span></div>\n'
html += '      <div class="acc-item"><span class="acc-w">黄河与民族精神</span><span class="acc-d">黄河是中华民族的母亲河，孕育了华夏文明。黄河奔腾不息、百折不挠的形象，常被用来象征中华民族的精神。本文以黄河“博大宽厚，柔中有刚；挟而不服，压而不弯；勇往直前”的性格，象征中华民族历经磨难而不屈不挠的精神。</span></div>\n'
html += '    </div>\n'
html += '  </div>\n'

html += '</section>\n\n'

html += '<div class="divider"></div>\n'

# 练习区
html += '<section id="practice" class="sec">\n'
html += '    <div class="sec-head"><h2>练 习</h2><span class="no">全屏听写</span></div>\n'
html += '    <div class="sec-sub">点击按钮进入全屏听写模式，可按 A− / A+ 调节字体大小。</div>\n'
html += '    <div class="ptools">\n'
html += '      <button data-mode="word" data-rand="5">随机五组字形</button>\n'
html += '      <button data-mode="word" data-all="1">全部字形</button>\n'
html += '      <button data-mode="note" data-rand="5">随机五组词语</button>\n'
html += '      <button data-mode="note" data-all="1">全部词语</button>\n'
html += '    </div>\n'
html += '  </section>\n\n'

html += '<footer>\n'
html += '  <div class="kai">《壶口瀑布》</div>\n'
html += '  <div>梁衡 · 现代 · 出自《梁衡文集》</div>\n'
html += '</footer>\n'
html += '</main>\n\n'

html += '<button class="top-btn" id="topBtn" title="回到顶部">↑</button>\n'
html += '<div class="anno-popup" id="annoPopup"><div class="aw" id="annoW"></div><div class="an" id="annoN"></div></div>\n'
html += '<div class="dictate" id="dictate" hidden>\n'
html += '  <div class="dictate-top">\n'
html += '    <span class="dictate-mode" id="dictMode">字形听写</span>\n'
html += '    <span class="dictate-progress" id="dictProgress">第 1 / 5 题</span>\n'
html += '    <button class="dictate-fs" id="dictFsMinus">A−</button>\n'
html += '    <button class="dictate-fs" id="dictFsPlus">A+</button>\n'
html += '    <button class="dictate-exit" id="dictExit">退出</button>\n'
html += '  </div>\n'
html += '  <div class="dictate-card">\n'
html += '    <div class="dictate-py" id="dictPy"></div>\n'
html += '    <div class="dictate-line" id="dictLine"></div>\n'
html += '    <div class="dictate-hint" id="dictHint"></div>\n'
html += '    <div class="dictate-ans" id="dictAnsBox" hidden>\n'
html += '      <div class="dictate-word" id="dictWord"></div>\n'
html += '      <div class="dictate-tip" id="dictTip"></div>\n'
html += '    </div>\n'
html += '  </div>\n'
html += '  <div class="dictate-actions">\n'
html += '    <button id="dictPrev">上一题</button>\n'
html += '    <button class="primary" id="dictShow">显示答案</button>\n'
html += '    <button id="dictNext">下一题</button>\n'
html += '  </div>\n'
html += '</div>\n'

html += '<script>\n' + main_js + '\n</script>\n'
html += '<script>\n'
html += 'var DICT_WORDS = ' + json.dumps(dict_words, ensure_ascii=False) + ';\n'
html += 'var DICT_NOTES = ' + json.dumps(dict_notes, ensure_ascii=False) + ';\n'
html += '</script>\n\n'

html += '</body>\n'
html += '</html>'

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("Generated: " + OUT)
print("Paragraphs: " + str(len(paragraphs)))
print("Anno count: " + str(sum(len(p[3]) for p in paragraphs)))
print("Words: " + str(len(dict_words)) + ", Notes: " + str(len(dict_notes)))
