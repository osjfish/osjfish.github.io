# -*- coding: utf-8 -*-
"""生成《最后一次讲演》闻一多 课件（即兴演讲词）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\zuihouyicijiangyan-wenyiduo.html"
FS_KEY = "zuihoujiangyan_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
# 注入 acc-sub CSS（积累区小标题样式）
style += '\n.acc-sub{font-family:var(--font-kai,serif);font-weight:700;border-left:3px solid #b8934a;padding-left:10px;margin:14px 0 6px;color:var(--ink);font-size:calc(16px * var(--fs));}'
scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

paragraphs = [
    (
        "这几天，大家晓得，在昆明出现了历史上最卑劣最无耻的事情！李先生究竟犯了什么罪，竟遭此毒手？他只不过用笔写写文章，用嘴说说话，而他所写的，所说的，都无非是一个没有失掉良心的中国人的话！大家都有一枝笔，有一张嘴，有什么理由拿出来讲啊！有事实拿出来说啊！为什么要打要杀，而且又不敢光明正大的来打来杀，而偷偷摸摸的来暗杀！这成什么话？",
        "开门见山，怒斥反动派暗杀李公朴先生的卑劣无耻行径，指出李先生只是说了一个中国人该说的话，反问反动派有什么理由杀人。",
        "演讲手法：以感叹句开篇，情感激烈，现场感极强。连用反问句（究竟犯了什么罪、有什么理由、这成什么话），排比（用笔写写文章，用嘴说说话），对比（光明正大与偷偷摸摸），爱憎分明。口语化表达（大家晓得、只不过）拉近与听众距离。",
        [
            ("卑劣", "（bēi liè）卑鄙恶劣"),
            ("无耻", "不顾羞耻，不知羞耻"),
            ("毒手", "杀人或伤害人的狠毒手段"),
            ("失掉良心", "丧失了做人的道德良知"),
            ("光明正大", "心怀坦白，言行正派"),
            ("偷偷摸摸", "形容瞒着人做事，不敢让人知道"),
            ("暗杀", "乘人不备而杀害"),
        ],
    ),
    (
        "今天，这里有没有特务？你站出来！是好汉的站出来！你出来讲！凭什么要杀死李先生？杀死了人，又不敢承认，还要诬蔑人，说什么\u201c桃色事件\u201d，说什么共产党杀共产党，无耻啊！无耻啊！这是某集团的无耻，恰是李先生的光荣！李先生在昆明被暗杀是李先生留给昆明的光荣！也是昆明人的光荣！",
        "直面特务，厉声质问，揭露反动派杀人后还造谣诬蔑的丑恶嘴脸，将反动派的无耻与李先生的光荣形成鲜明对比。",
        "演讲手法：呼告（你站出来、你出来讲）直接对特务喊话，现场感极强。反复（无耻啊！无耻啊！）强化愤怒情绪。排比反问（凭什么要杀死李先生）。对比论证（某集团的无耻 vs 李先生的光荣）。短句急促，气势逼人，体现即兴演讲的战斗性。",
        [
            ("诬蔑", "（wū miè）捏造事实败坏别人的名誉"),
            ("桃色事件", "旧时指涉及男女私情的事件，这里是反动派造谣的借口"),
            ("某集团", "指国民党反动派，不直接点名，更加含蓄有力"),
            ("光荣", "由于做了有利于人民的和正义的事情而被公认为值得尊敬的"),
        ],
    ),
    (
        "去年\u201c一二\u00b7一\u201d昆明青年学生为了反对内战，遭受屠杀，那算是青年的一代献出了他们最宝贵的生命！现在李先生为了争取民主和平而遭受了反动派的暗杀，我们骄傲一点说，这算是像我这样大年纪的一代，我们的老战友，献出了最宝贵的生命！这两桩事发生在昆明，这算是昆明无限的光荣！",
        "将李公朴被暗杀与\u201c一二\u00b7一\u201d惨案相提并论，指出两代人都为民主和平献出了生命，这是昆明的光荣。",
        "演讲手法：举例论证（一二·一惨案、李公朴被暗杀），用历史事实增强说服力。反复（最宝贵的生命）强调牺牲之重。将悲痛转化为自豪（昆明无限的光荣），情感升华，激励听众。",
        [
            ("一二\u00b7一", "1945年12月1日，昆明学生为反对内战遭到国民党军警镇压，四人牺牲，史称\u201c一二\u00b7一\u201d惨案"),
            ("内战", "国内发生的战争，这里指抗日战争胜利后国民党发动的反共内战"),
            ("民主和平", "人民享有民主权利、国家和平稳定的局面"),
            ("反动派", "反对进步、反对革命的势力，这里指国民党反动派"),
            ("老战友", "并肩战斗的老朋友"),
            ("两桩事", "指\u201c一二\u00b7一\u201d惨案和李公朴被暗杀两件事"),
        ],
    ),
    (
        "反动派暗杀李先生的消息传出以后，大家听了都悲愤痛恨。我心里想，这些无耻的东西，不知他们是怎么想法，他们的心理是什么状态，他们的心是怎样长的！其实很简单，他们这样疯狂的来制造恐怖，正是他们自己在慌啊！在害怕啊！所以他们制造恐怖，其实是他们自己在恐怖啊！特务们，你们想想，你们还有几天？你们完了，快完了！你们以为打伤几个，杀死几个，就可以了事，就可以把人民吓倒了吗？其实广大的人民是打不尽的，杀不完的！要是这样可以的话，世界上早没有人了。",
        "剖析反动派制造恐怖的本质是自己内心恐慌，预言反动派即将灭亡，指出人民是打不尽杀不完的。",
        "演讲手法：心理分析（他们自己在慌、在害怕）揭示敌人虚弱本质。反复（在慌啊、在害怕啊、在恐怖啊）强化判断。呼告（特务们，你们想想）直接对话。反问（你们还有几天、就可以把人民吓倒了吗）。排比（他们是怎么想法，心理是什么状态，心是怎样长的）。逻辑严密，从敌人心理推导到必然灭亡。",
        [
            ("悲愤痛恨", "悲痛愤怒且深切憎恨"),
            ("恐怖", "（kǒng bù）由于生命受到威胁而恐惧"),
            ("了事", "把事情了结、平息"),
            ("吓倒", "因害怕而屈服"),
            ("广大", "范围大、人数多"),
        ],
    ),
    (
        "你们杀死一个李公朴，会有千百万个李公朴站起来！你们将失去千百万的人民！你们看着我们人少，没有力量？告诉你们，我们的力量大得很，强得很！看今天来的这些人，都是我们的人，都是我们的力量！此外还有广大的市民！我们有这个信心：人民的力量是要胜利的，真理是永远存在的。历史上没有一个反人民的势力不被人民毁灭的！希特勒，墨索里尼，不都在人民面前倒下去了吗？翻开历史看看，你们还站得住几天！你们完了，快完了！我们的光明就要出现了。我们看，光明就在我们眼前，而现在正是黎明之前那个最黑暗的时候。我们有力量打破这个黑暗，争到光明！我们的光明，就是反动派的末日！",
        "预言杀死一个李公朴会有千百万个李公朴站起来，以希特勒、墨索里尼为例证明反人民势力必然灭亡，号召人民打破黑暗争到光明。",
        "演讲手法：对比（一个 vs 千百万）突出革命力量的壮大。举例论证（希特勒、墨索里尼）以历史事实证明反动派必然灭亡。反复（你们完了，快完了）强化预言。比喻（黎明之前最黑暗、光明与黑暗）形象表达革命形势。排比（我们的力量大得很，强得很）。反问（不都在人民面前倒下去了吗）。激情澎湃，号召力极强。",
        [
            ("李公朴", "（1902—1946）爱国民主人士，因反对内战被国民党特务暗杀"),
            ("希特勒", "（1889—1945）德国法西斯头子，第二次世界大战的罪魁祸首"),
            ("墨索里尼", "（1883—1945）意大利法西斯独裁者，二战元凶之一"),
            ("毁灭", "摧毁消灭"),
            ("黎明", "天快要亮或刚亮的时候，比喻胜利即将到来"),
            ("末日", "基督教指世界最后毁灭的一天，泛指灭亡的日子"),
        ],
    ),
    (
        "李先生的血不会白流的！李先生赔上了这条性命，我们要换来一个代价。\u201c一二\u00b7一\u201d四烈士倒下了，年青的战士们的血换来了政治协商会议的召开；现在李先生倒下了，他的血要换取政协会议的重开！我们有这个信心！",
        "指出李先生的血不会白流，以\u201c一二\u00b7一\u201d烈士的血换来政协会议召开为先例，坚信李先生的血会换来政协会议重开。",
        "演讲手法：因果论证（血不会白流→换来代价）。类比论证（一二·一烈士的血换来政协召开→李先生的血换取政协重开）。短句有力，信念坚定。反复（倒下了、换取）形成呼应。",
        [
            ("赔上", "搭上、付出（生命等重大代价）"),
            ("代价", "为达到某种目的所耗费的物质或精力"),
            ("政治协商会议", "1946年1月在重庆召开的各党派协商国是的会议，简称政协会议"),
            ("重开", "重新召开"),
        ],
    ),
    (
        "\u201c一二\u00b7一\u201d是昆明的光荣，是云南人民的光荣。云南有光荣的历史，远的如护国，这不用说了，近的如\u201c一二\u00b7一\u201d，都是属于云南人民的。我们要发扬云南光荣的历史！",
        "回顾云南光荣的革命历史（护国运动、一二·一惨案），号召发扬云南人民的光荣传统。",
        "演讲手法：举例论证（护国运动、一二·一）唤起地方自豪感。反复（光荣）强化情感。由远及近，历史与现实贯通，激励昆明听众。",
        [
            ("护国", "指1915年云南发起的护国运动，反对袁世凯复辟帝制"),
            ("发扬", "发展和提倡（优良作风、传统等）"),
        ],
    ),
    (
        "反动派挑拨离间，卑鄙无耻，你们看见联大走了，学生放暑假了，便以为我们没有力量了吗？特务们！你们错了！你们看见今天到会的一千多青年，又握起手来了，我们昆明的青年决不会让你们这样蛮横下去的！",
        "驳斥反动派以为联大走了、学生放假就没有力量的妄想，指出昆明青年已经重新团结起来，决不让反动派蛮横下去。",
        "演讲手法：反问（便以为我们没有力量了吗）。呼告（特务们！你们错了！）直接怒斥。对比（联大走了 vs 一千多青年握起手来）。短句铿锵，掷地有声。",
        [
            ("挑拨离间", "（tiǎo bō lí jiàn）搬弄是非，使别人不团结"),
            ("卑鄙无耻", "（bēi bǐ wú chǐ）形容品质恶劣，不顾羞耻"),
            ("联大", "西南联合大学的简称，抗战时期由北大、清华、南开在昆明合并组建"),
            ("蛮横", "（mán hèng）态度粗暴而不讲理"),
        ],
    ),
    (
        "反动派，你看见一个倒下去，可也看得见千百个继起的！",
        "警告反动派：杀了一个人，会有千百个人继续战斗。",
        "演讲手法：对比（一个 vs 千百个），呼告（反动派，你看见）。极短句，斩钉截铁，是全文最精炼的警句之一。",
        [
            ("继起", "继续起来、接着跟上来"),
        ],
    ),
    (
        "正义是杀不完的，因为真理永远存在！",
        "点明主旨：正义和真理是扼杀不了的，因为真理永存。",
        "演讲手法：因果复句，简洁有力。因果论证（因为真理永远存在，所以正义杀不完）。是全文的核心警句，掷地有声。",
        [],
    ),
    (
        "历史赋予昆明的任务是争取民主和平，我们昆明的青年必须完成这任务！",
        "指出昆明青年的历史使命是争取民主和平，号召青年必须完成这一任务。",
        "演讲手法：判断句明确任务，祈使句发出号召。庄重有力，将个人情感上升为历史使命。",
        [
            ("赋予", "（fù yǔ）交给（重大任务、使命等）"),
        ],
    ),
    (
        "我们不怕死，我们有牺牲的精神！我们随时像李先生一样，前脚跨出大门，后脚就不准备再跨进大门！",
        "表达不怕牺牲的决心，以李先生为榜样，随时准备为民主和平献出生命。",
        "演讲手法：反复（我们不怕死，我们有牺牲的精神）。以具象动作（前脚跨出大门，后脚就不准备再跨进大门）表达视死如归的决心，画面感极强。结尾高潮，感召力巨大。",
        [
            ("牺牲", "为正义事业舍弃生命"),
        ],
    ),
]

parts = [
    ("第一部分", "怒斥罪行，颂扬光荣", "1–3 段", "开篇怒斥反动派暗杀李先生的卑劣行径，揭露其造谣诬蔑的丑恶嘴脸，将李先生的牺牲与一二·一惨案并提，颂扬昆明的光荣。"),
    ("第二部分", "剖析敌人，预言胜利", "4–5 段", "剖析反动派制造恐怖的虚弱本质，以希特勒、墨索里尼为例预言反人民势力必然灭亡，指出人民力量打不尽杀不完。"),
    ("第三部分", "号召奋斗，誓死抗争", "6–12 段", "坚信烈士鲜血不会白流，回顾云南光荣历史，号召昆明青年继承遗志，表达为民主和平不惜牺牲的决心。"),
]

para_part = [0,0,0, 1,1, 2,2,2,2,2,2,2]

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
    {"w":"劣","py":"liè","q":"在昆明出现了历史上最卑□最无耻的事情","tip":"「劣」力字旁，恶劣；不要写成「掠」（提手旁）"},
    {"w":"耻","py":"chǐ","q":"历史上最卑劣最无□的事情","tip":"「耻」耳字旁，羞耻；不要写成「齿」"},
    {"w":"毒","py":"dú","q":"竟遭此□手","tip":"「毒」母字底，狠毒；不要写成「独」（反犬旁）"},
    {"w":"诬","py":"wū","q":"还要□蔑人","tip":"「诬」言字旁，捏造事实；不要写成「污」（三点水）"},
    {"w":"蔑","py":"miè","q":"还要诬□人","tip":"「蔑」草字头，轻视、毁谤；笔画复杂，注意下面是「戍」的变形"},
    {"w":"屠","py":"tú","q":"为了反对内战，遭受□杀","tip":"「屠」尸字头，宰杀；不要写成「暑」（日字头）"},
    {"w":"愤","py":"fèn","q":"大家听了都悲□痛恨","tip":"「愤」竖心旁，愤怒；不要写成「奋」（大字头）"},
    {"w":"怖","py":"bù","q":"他们这样疯狂的来制造恐□","tip":"「怖」竖心旁，害怕；不要写成「布」（巾字旁）"},
    {"w":"毁","py":"huǐ","q":"没有一个反人民的势力不被人民□灭的","tip":"「毁」殳字旁，破坏；不要写成「悔」（竖心旁）"},
    {"w":"黎","py":"lí","q":"□明之前那个最黑暗的时候","tip":"「黎」黍字头，天将亮；不要写成「犁」（牛字旁）"},
    {"w":"赔","py":"péi","q":"李先生□上了这条性命","tip":"「赔」贝字旁，付出代价；不要写成「陪」（左耳旁）"},
    {"w":"拨","py":"bō","q":"反动派挑□离间","tip":"「拨」提手旁，挑动；不要写成「拔」（提手旁，bá）"},
    {"w":"间","py":"jiàn","q":"反动派挑拨离□","tip":"「间」门字框，隔阂；多音字，此处读jiàn不读jiān"},
    {"w":"鄙","py":"bǐ","q":"反动派挑拨离间，卑□无耻","tip":"「鄙」右耳旁，恶劣；不要写成「痹」（病字旁）"},
    {"w":"蛮","py":"mán","q":"决不会让你们这样□横下去的","tip":"「蛮」虫字底，粗野；不要写成「满」（三点水）"},
    {"w":"横","py":"hèng","q":"决不会让你们这样蛮□下去的","tip":"「横」木字旁，粗暴；多音字，此处读hèng不读héng"},
    {"w":"赋","py":"fù","q":"历史□予昆明的任务","tip":"「赋」贝字旁，交给；不要写成「付」（单人旁）"},
    {"w":"予","py":"yǔ","q":"历史赋□昆明的任务","tip":"「予」独体字，给；不要写成「与」或「于」"},
    {"w":"牺","py":"xī","q":"我们有□牲的精神","tip":"「牺」牛字旁，古代祭祀用的纯色牲畜；不要写成「栖」（木字旁）"},
]

dict_notes = [
    {"w":"卑劣","a":"卑鄙恶劣","q":"历史上最卑劣最无耻的事情"},
    {"w":"毒手","a":"杀人或伤害人的狠毒手段","q":"竟遭此毒手"},
    {"w":"光明正大","a":"心怀坦白，言行正派","q":"不敢光明正大的来打来杀"},
    {"w":"偷偷摸摸","a":"形容瞒着人做事，不敢让人知道","q":"偷偷摸摸的来暗杀"},
    {"w":"诬蔑","a":"捏造事实败坏别人的名誉","q":"还要诬蔑人"},
    {"w":"桃色事件","a":"旧时指涉及男女私情的事件，这里是反动派造谣的借口","q":"说什么桃色事件"},
    {"w":"一二·一","a":"1945年12月1日昆明学生反内战遭镇压的惨案","q":"去年一二·一昆明青年学生"},
    {"w":"悲愤痛恨","a":"悲痛愤怒且深切憎恨","q":"大家听了都悲愤痛恨"},
    {"w":"恐怖","a":"由于生命受到威胁而恐惧","q":"制造恐怖"},
    {"w":"希特勒","a":"德国法西斯头子，二战罪魁祸首","q":"希特勒，墨索里尼"},
    {"w":"墨索里尼","a":"意大利法西斯独裁者，二战元凶之一","q":"希特勒，墨索里尼"},
    {"w":"黎明","a":"天快要亮的时候，比喻胜利即将到来","q":"黎明之前那个最黑暗的时候"},
    {"w":"末日","a":"灭亡的日子","q":"就是反动派的末日"},
    {"w":"政治协商会议","a":"1946年在重庆召开的各党派协商国是的会议","q":"换来了政治协商会议的召开"},
    {"w":"护国","a":"1915年云南发起的反对袁世凯复辟的护国运动","q":"远的如护国"},
    {"w":"挑拨离间","a":"搬弄是非，使别人不团结","q":"反动派挑拨离间"},
    {"w":"卑鄙无耻","a":"形容品质恶劣，不顾羞耻","q":"卑鄙无耻"},
    {"w":"联大","a":"西南联合大学的简称","q":"你们看见联大走了"},
    {"w":"蛮横","a":"态度粗暴而不讲理","q":"不会让你们这样蛮横下去"},
    {"w":"继起","a":"继续起来、接着跟上来","q":"可也看得见千百个继起的"},
    {"w":"赋予","a":"交给（重大任务、使命等）","q":"历史赋予昆明的任务"},
    {"w":"牺牲","a":"为正义事业舍弃生命","q":"我们有牺牲的精神"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《最后一次讲演》闻一多</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">现代 · 闻一多</div>
  <h1 class="hero-title">最后一次讲演</h1>
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
  <div class="sec-head"><h2>背 景</h2><span class="no">作者 · 时代 · 缘起</span></div>
  <div class="lead">
    <p>《最后一次讲演》是闻一多于1946年7月15日在李公朴先生追悼会上发表的即兴演讲。当时，爱国民主人士李公朴因反对内战被国民党特务暗杀，闻一多不顾个人安危，拍案而起，在追悼会上发表了这篇义正词严、慷慨激昂的演讲。当天下午，闻一多在回家途中被特务暗杀，这篇演讲也因此成为他的\u201c最后一次讲演\u201d。</p>
    <p>这是一篇即兴演讲词，没有事先准备讲稿，完全是现场情感的爆发。语言激烈短促，爱憎分明，大量使用反问、反复、呼告、排比等修辞手法，具有极强的战斗性和感染力，是中国现代演讲史上的经典之作。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>闻一多（1899—1946），原名闻家骅，湖北浠水人，现代诗人、学者、民主战士。新月派代表诗人，著有诗集《红烛》《死水》。后从事古典文学研究，在《楚辞》《唐诗》等领域造诣深厚。抗战时期任西南联大教授，1943年后积极参加民主运动，1946年7月15日被国民党特务暗杀。</p>
    <p style="margin-top:10px;color:var(--ink2)">毛泽东在《别了，司徒雷登》中称赞：\u201c闻一多拍案而起，横眉怒对国民党的手枪，宁可倒下去，不愿屈服。\u201d</p>
  </div>
  <div class="box">
    <h3>演讲背景</h3>
    <p><b>李公朴被暗杀：</b>1946年7月11日，爱国民主人士李公朴在昆明被国民党特务暗杀。7月15日，昆明各界举行李公朴追悼大会，闻一多先生拍案而起，发表了这篇著名的演讲。</p>
    <p style="margin-top:8px"><b>一二·一惨案：</b>1945年12月1日，昆明学生为反对内战举行罢课，遭到国民党军警镇压，四名师生牺牲，史称\u201c一二·一\u201d惨案。闻一多在演讲中多次提及此事，将两次牺牲并提。</p>
    <p style="margin-top:8px"><b>即兴演讲：</b>这篇演讲没有事先准备讲稿，是闻一多在追悼会上被现场气氛激发，即席发表的。演讲结束后数小时，闻一多即被特务暗杀，用生命践行了演讲中的誓言。</p>
  </div>
  <div class="box">
    <h3>文体知识</h3>
    <p><b>演讲词：</b>在公众场合就某个问题发表意见、阐述观点的讲话文稿。基本要求：内容有针对性，观点鲜明，感情真挚，语言通俗生动，富有感染力和号召力。</p>
    <p style="margin-top:8px"><b>即兴演讲：</b>事先没有准备讲稿，在特定场合因事因情而发的演讲。特点是情感真实、反应敏捷、语言口语化、现场感强。本文是即兴演讲的典范。</p>
    <p style="margin-top:8px"><b>演讲的语言特点：</b>口语化（大家晓得、只不过）、短句多、节奏快；大量使用感叹句、反问句增强气势；运用反复、排比、呼告等修辞强化情感；爱憎分明，具有强烈的战斗性和号召力。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文诵读《最后一次讲演》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV14u411n7vj&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读最后一次讲演"></iframe>
        <a href="https://www.bilibili.com/video/BV14u411n7vj" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>课本剧《最后一次讲演》舞台演绎</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1dELHzCEpP&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课本剧最后一次讲演"></iframe>
        <a href="https://www.bilibili.com/video/BV1dELHzCEpP" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 内容 · 演讲手法</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{fulltext_html}  </div>
  <div class="verse-list" id="verseList">
{verse_html}  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">演讲特色 · 语言 · 论证 · 情感 · 主题</span></div>

  <div class="box">
    <h3>演讲特色</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">即兴演讲，情感爆发</div>
        <p>本文是闻一多在李公朴追悼会上的即席演讲，没有事先准备讲稿，完全是现场悲愤情感的爆发。正因为是即兴，语言才格外真实、激烈、不加修饰，具有直击人心的力量。演讲者与听众同仇敌忾，现场气氛与演讲内容互相激发。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">战斗性与感染力的统一</div>
        <p>演讲既有犀利的战斗性——直面特务厉声质问、揭露敌人阴谋、预言反动派灭亡；又有深沉的感染力——对李先生的崇敬、对青年的期望、对光明的信念。爱憎分明，刚柔并济，既打击敌人又鼓舞人民。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">现场感极强，呼告频繁</div>
        <p>演讲中大量使用呼告：\u201c你站出来！\u201d\u201c特务们，你们想想！\u201d\u201c反动派，你看见一个倒下去\u201d——直接对特务喊话，也直接对听众号召。这种面对面的对话方式，使演讲具有极强的现场感和互动性。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>语言艺术</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">短句急促，节奏铿锵</div>
        <p>\u201c你站出来！是好汉的站出来！你出来讲！\u201d\u201c正义是杀不完的，因为真理永远存在！\u201d大量使用短句和感叹句，节奏急促，如战鼓擂动，气势逼人。这种语言节奏与演讲者愤怒的情绪完全吻合。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">反复与排比，强化情感</div>
        <p>反复：\u201c无耻啊！无耻啊！\u201d\u201c你们完了，快完了！\u201d\u201c在慌啊！在害怕啊！\u201d——通过重复强化愤怒和判断。排比：\u201c他们是怎么想法，他们的心理是什么状态，他们的心是怎样长的！\u201d——层层推进，气势磅礴。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">反问有力，不容置疑</div>
        <p>\u201c李先生究竟犯了什么罪？\u201d\u201c这成什么话？\u201d\u201c希特勒，墨索里尼，不都在人民面前倒下去了吗？\u201d大量反问句，答案不言自明，比正面陈述更有力量，使听众在反问中自然得出结论。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">口语化表达，亲切自然</div>
        <p>\u201c大家晓得\u201d\u201c只不过\u201d\u201c其实很简单\u201d\u201c告诉你们\u201d——口语化的表达使演讲通俗易懂，拉近与听众的距离，符合即兴演讲的特点，也使激烈的情感有了生活化的出口。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>论证方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">举例论证：历史事实不容辩驳</div>
        <p>以希特勒、墨索里尼的覆灭为例，证明\u201c历史上没有一个反人民的势力不被人民毁灭的\u201d；以\u201c一二·一\u201d烈士的血换来政协会议召开为例，证明李先生的血不会白流。历史事实使论证具有不可辩驳的力量。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对比论证：爱憎分明</div>
        <p>\u201c这是某集团的无耻，恰是李先生的光荣\u201d——反动派的无耻与李先生的光荣对比；\u201c你们杀死一个李公朴，会有千百万个李公朴站起来\u201d——一个与千百万对比。对比使立场鲜明，褒贬自现。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">因果论证：逻辑严密</div>
        <p>\u201c他们制造恐怖，正是他们自己在慌啊\u201d——由果推因，揭示敌人虚弱本质；\u201c正义是杀不完的，因为真理永远存在\u201d——由因推果，点明必然趋势。因果论证使演讲不仅有激情，更有理性的力量。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>情感表达</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">对反动派：愤怒揭露，无情痛斥</div>
        <p>开篇即怒斥\u201c最卑劣最无耻\u201d，直指特务\u201c你站出来\u201d，揭露\u201c桃色事件\u201d的谣言，预言\u201c你们完了，快完了\u201d。对敌人的愤怒贯穿始终，毫不留情。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对李先生：崇敬颂扬，引以为荣</div>
        <p>\u201c这是某集团的无耻，恰是李先生的光荣\u201d\u201c李先生的血不会白流的\u201d——将李先生的牺牲视为光荣，将悲痛转化为自豪和力量，情感深沉而崇高。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">对青年与人民：鼓舞号召，充满信心</div>
        <p>\u201c我们的力量大得很，强得很\u201d\u201c我们昆明的青年决不会让你们这样蛮横下去的\u201d——对人民力量充满信心，对青年寄予厚望，结尾\u201c我们不怕死\u201d更是将情感推向高潮。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《最后一次讲演》痛斥了国民党反动派暗杀李公朴的卑劣罪行，揭露了敌人色厉内荏的虚弱本质，高度颂扬了李公朴及爱国志士为民主和平献身的崇高精神，预言了反人民势力必然灭亡、人民革命必然胜利的历史趋势，表达了闻一多为民主和平不惜牺牲生命的坚定决心和大无畏精神。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 字音形 · 修辞 · 写法 · 常识</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">卑劣</span><span class="acc-d">（bēi liè）卑鄙恶劣。</span></div>
      <div class="acc-item"><span class="acc-w">毒手</span><span class="acc-d">杀人或伤害人的狠毒手段。</span></div>
      <div class="acc-item"><span class="acc-w">诬蔑</span><span class="acc-d">（wū miè）捏造事实败坏别人的名誉。</span></div>
      <div class="acc-item"><span class="acc-w">挑拨离间</span><span class="acc-d">（tiǎo bō lí jiàn）搬弄是非，使别人不团结。</span></div>
      <div class="acc-item"><span class="acc-w">卑鄙无耻</span><span class="acc-d">（bēi bǐ wú chǐ）形容品质恶劣，不顾羞耻。</span></div>
      <div class="acc-item"><span class="acc-w">蛮横</span><span class="acc-d">（mán hèng）态度粗暴而不讲理。</span></div>
      <div class="acc-item"><span class="acc-w">赋予</span><span class="acc-d">（fù yǔ）交给（重大任务、使命等）。</span></div>
      <div class="acc-item"><span class="acc-w">光明正大</span><span class="acc-d">心怀坦白，言行正派。</span></div>
      <div class="acc-item"><span class="acc-w">偷偷摸摸</span><span class="acc-d">形容瞒着人做事，不敢让人知道。</span></div>
      <div class="acc-item"><span class="acc-w">悲愤痛恨</span><span class="acc-d">悲痛愤怒且深切憎恨。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">卑劣</span><span class="acc-d">（liè）力字旁；与「掠」（lüè，提手旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">诬蔑</span><span class="acc-d">（wū miè）「诬」言字旁，与「污」（三点水）区分；「蔑」草字头，笔画复杂。</span></div>
      <div class="acc-item"><span class="acc-w">屠杀</span><span class="acc-d">（tú）尸字头；与「暑」（shǔ，日字头）区分。</span></div>
      <div class="acc-item"><span class="acc-w">悲愤</span><span class="acc-d">（fèn）竖心旁；与「奋」（fèn，大字头）区分。</span></div>
      <div class="acc-item"><span class="acc-w">恐怖</span><span class="acc-d">（bù）竖心旁；与「布」（bù，巾字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">毁灭</span><span class="acc-d">（huǐ）殳字旁；与「悔」（huǐ，竖心旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">赔上</span><span class="acc-d">（péi）贝字旁；与「陪」（péi，左耳旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">挑拨离间</span><span class="acc-d">（bō jiàn）「拨」提手旁，与「拔」（bá）区分；「间」多音字，此处读jiàn。</span></div>
      <div class="acc-item"><span class="acc-w">蛮横</span><span class="acc-d">（mán hèng）「蛮」虫字底，与「满」（三点水）区分；「横」多音字，此处读hèng。</span></div>
      <div class="acc-item"><span class="acc-w">赋予</span><span class="acc-d">（fù yǔ）「赋」贝字旁，与「付」区分；「予」独体字，与「与」「于」区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>修辞方法</h3>
      <div class="acc-item"><span class="acc-w">反问</span><span class="acc-d">用疑问的形式表达确定的意思，答案在问句中。如\u201c这成什么话？\u201d\u201c希特勒，墨索里尼，不都在人民面前倒下去了吗？\u201d增强语势，不容置疑。</span></div>
      <div class="acc-item"><span class="acc-w">反复</span><span class="acc-d">有意重复某些词语或句子。如\u201c无耻啊！无耻啊！\u201d\u201c你们完了，快完了！\u201d强化情感，加深印象。</span></div>
      <div class="acc-item"><span class="acc-w">排比</span><span class="acc-d">三个以上结构相似的句子排列。如\u201c他们是怎么想法，他们的心理是什么状态，他们的心是怎样长的！\u201d增强气势。</span></div>
      <div class="acc-item"><span class="acc-w">呼告</span><span class="acc-d">直接对文中的人或物说话。如\u201c你站出来！\u201d\u201c特务们，你们想想！\u201d增强现场感和感染力。</span></div>
      <div class="acc-item"><span class="acc-w">对比</span><span class="acc-d">把两种对立的事物放在一起比较。如\u201c某集团的无耻，恰是李先生的光荣\u201d，使立场鲜明。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">观点鲜明</span><span class="acc-d">演讲必须立场坚定、爱憎分明。本文对反动派怒斥、对李先生颂扬、对人民鼓舞，态度毫不含糊。</span></div>
      <div class="acc-item"><span class="acc-w">情感真挚</span><span class="acc-d">即兴演讲的力量来自真实情感。本文悲愤与激昂交织，不是空洞的口号，而是用生命发出的呐喊。</span></div>
      <div class="acc-item"><span class="acc-w">短句有力</span><span class="acc-d">演讲语言宜短不宜长。短句节奏快、气势足，适合口头表达和现场鼓动。</span></div>
      <div class="acc-item"><span class="acc-w">善用修辞</span><span class="acc-d">反问、反复、排比、呼告是演讲词最常用的修辞手法，能极大增强语言的感染力和号召力。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">李公朴</span><span class="acc-d">（1902—1946）爱国民主人士，中国民主同盟中央委员，1946年7月11日在昆明被国民党特务暗杀。</span></div>
      <div class="acc-item"><span class="acc-w">一二·一惨案</span><span class="acc-d">1945年12月1日，昆明学生为反对内战遭到国民党军警镇压，四人牺牲，是全国解放战争时期学生运动的先声。</span></div>
      <div class="acc-item"><span class="acc-w">护国运动</span><span class="acc-d">1915年12月，蔡锷等在云南发起反对袁世凯复辟帝制的运动，又称护国战争。</span></div>
      <div class="acc-item"><span class="acc-w">西南联大</span><span class="acc-d">抗战时期由北京大学、清华大学、南开大学在昆明合并组建的大学，1938—1946年存在，培养了大批人才。</span></div>
      <div class="acc-item"><span class="acc-w">政治协商会议</span><span class="acc-d">1946年1月在重庆召开的各党派协商国是的会议，通过了和平建国纲领等决议。</span></div>
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
  <div class="kai">《最后一次讲演》</div>
  <div>闻一多 · 现代 · 1946年7月15日李公朴追悼会即兴演讲</div>
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

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Generated: {OUT}")
print(f"Paragraphs: {len(paragraphs)}")
print(f"Anno count: {sum(len(p[3]) for p in paragraphs)}")
print(f"Words: {len(dict_words)}, Notes: {len(dict_notes)}")
