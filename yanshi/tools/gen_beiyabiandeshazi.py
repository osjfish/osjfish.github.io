# -*- coding: utf-8 -*-
"""生成《被压扁的沙子》阿西莫夫 课件（科普说明文）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\beiyabiandeshazi-aximofu.html"
FS_KEY = "beiyasha_fs"

with open(TEMPLATE, encoding="utf-8") as f:
    src = f.read()

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
style += "\n  .acc-sub{font-family:var(--font-kai,serif);font-weight:700;border-left:3px solid #b8934a;padding-left:8px;margin:12px 0 6px;color:var(--red-deep)}\n"

scripts = re.findall(r"<script>(.*?)</script>", src, re.S)
main_js = scripts[0]
main_js = main_js.replace("beiying_fs", FS_KEY)

LQ = "\u201c"
RQ = "\u201d"

paragraphs = [
    (
        f"在过去的9年里，科学家们一直对6500万年前恐龙灭绝的一个新观点争论不休，这个问题最终也许会得到解决。",
        "开篇点明说明话题：科学家们对6500万年前恐龙灭绝的新观点争论不休，引出下文。",
        "说明对象：恐龙灭绝的原因。说明方法：无特殊说明方法，以议论开篇。说明语言：{LQ}一直{RQ}{LQ}争论不休{RQ}说明问题的复杂性和科学家的探索精神；{LQ}也许{RQ}表示推测，留有余地，体现说明文语言的准确性。",
        [
            ("灭绝", "完全灭亡、消失"),
            ("争论不休", "争论不停、各执己见"),
            ("新观点", "新的看法或理论"),
        ],
    ),
    (
        f"1980年，曾经有报道说，在一个6500万年前形成的沉积物薄层中，发现了稀有金属铱，它的含量异常丰富。一些人认为，这可能是由于一个巨大的小行星或彗星撞击地球的结果。这种撞击也许深入到了地壳内部，引起火山喷发，造成大火和潮汐大浪。许多尘埃进入了平流层中，结果造成在很长一段时间内阳光无法抵达地球表面。这也许是导致包括所有恐龙在内的许多地球生物灭绝的原因。",
        "介绍1980年的科学发现：6500万年前的沉积物中铱含量异常丰富，一些人认为这是小行星或彗星撞击地球的结果，并推测撞击导致恐龙灭绝的过程。",
        "说明方法：举例子（1980年的发现）、列数字（6500万年前）、作诠释（解释撞击导致灭绝的过程）。说明语言：{LQ}可能{RQ}{LQ}也许{RQ}多次出现，表示推测，体现说明文语言的准确性和严密性；描述撞击后果的过程条理清晰。",
        [
            ("沉积物", "沉积在水底或地下的物质，如泥沙、矿物质等"),
            ("薄层", "薄薄的一层"),
            ("稀有金属", "自然界中储量稀少、分布分散的金属，如铱、铂等"),
            ("铱", "（yī）一种稀有金属元素，银白色，质硬而脆，在陨石中含量较高"),
            ("异常丰富", "不同寻常地多、含量特别高"),
            ("小行星", "太阳系中绕太阳运行的小天体，比行星小得多"),
            ("彗星", "绕太阳运行的一种天体，通常有云雾状的尾巴"),
            ("撞击", "运动着的物体跟别的物体猛然碰上"),
            ("地壳", "地球固体圈层的最外层，由岩石组成"),
            ("火山喷发", "地球内部的岩浆等物质喷出地表的现象"),
            ("潮汐大浪", "由潮汐引起的巨大波浪"),
            ("尘埃", "尘土"),
            ("平流层", "地球大气的一层，位于对流层之上，气流平稳"),
            ("抵达", "到达"),
        ],
    ),
    (
        f"毫无疑问，6500万年前地球上曾有过一次{LQ}大灭绝{RQ}，发生过一次{LQ}大劫难{RQ}。然而，并不是所有的科学家都认为这是由巨大撞击引起的。例如，1987年就有人指出，如果地球突然经历了一个火山爆发期，许多火山大致同时喷发，那么也能造成一个足以使生物大量灭绝的巨大灾难。",
        "肯定6500万年前曾发生大灭绝和大劫难，但指出并非所有科学家都认为是撞击引起的，并以1987年有人提出的火山爆发说为例，说明存在另一种理论。",
        "说明方法：举例子（1987年火山爆发说）、作比较（撞击说与火山说比较）。说明语言：{LQ}毫无疑问{RQ}强调大灭绝的确定性；{LQ}然而{RQ}转折，引出不同观点；{LQ}大致同时{RQ}准确描述火山喷发的情况，体现语言的准确性。",
        [
            ("毫无疑问", "没有什么可以怀疑的，形容非常肯定"),
            ("大灭绝", "大规模的生物灭绝事件"),
            ("大劫难", "大灾难、大灾祸"),
            ("火山爆发期", "火山活动频繁、大量火山喷发的时期"),
            ("大致", "大概、基本上"),
            ("喷发", "（岩浆、气体等）突然猛烈地射出"),
            ("足以", "完全可以、够得上"),
            ("巨大灾难", "极大的灾祸"),
        ],
    ),
    (
        f"因此，目前存在两种对立的理论，即{LQ}撞击说{RQ}和{LQ}火山说{RQ}。",
        "总结上文，明确指出目前存在两种对立的理论：撞击说和火山说，为下文的验证做铺垫。",
        "说明方法：分类别（分两种理论）、下定义（撞击说和火山说）。说明语言：{LQ}因此{RQ}总结上文；{LQ}对立{RQ}准确说明两种理论的关系；独句成段，起承上启下的过渡作用。",
        [
            ("对立", "两种事物或一种事物中的两个方面之间的相互排斥、矛盾"),
            ("撞击说", "认为恐龙灭绝是由小行星或彗星撞击地球引起的理论"),
            ("火山说", "认为恐龙灭绝是由火山大规模喷发引起的理论"),
        ],
    ),
    (
        f"这不仅仅是一个学术问题，因为我们将来也许还会遇到这样或那样的大灾难（万一哪天某个星体要撞击地球，我们也许会知道如何来避免这种撞击）。我们需要尽可能多地了解这种事件所产生的影响，希望将来一旦面临这种事件，我们可以采取某种应急措施。",
        "说明研究恐龙灭绝原因的现实意义：不仅仅是学术问题，还关系到人类未来如何应对类似的大灾难，括号中补充说明研究的实用价值。",
        "说明方法：作诠释（解释研究的现实意义）。说明语言：括号中的补充说明体现了作者的科学远见和人文关怀；{LQ}也许{RQ}{LQ}尽可能多{RQ}{LQ}某种{RQ}等词准确表述，体现语言的严密性。",
        [
            ("学术问题", "属于学术研究范畴的问题"),
            ("星体", "天体，如恒星、行星、小行星、彗星等"),
            ("避免", "设法不使某种情形发生、防止"),
            ("事件", "历史上或社会上发生的不平常的大事情"),
            ("面临", "面前遇到（问题、形势等）"),
            ("应急措施", "应对紧急情况的办法和行动"),
        ],
    ),
    (
        f"为此，科学家们一直都在努力寻找证据来验证这两种理论。",
        "过渡段，说明科学家们一直在努力寻找证据来验证撞击说和火山说，引出下文对斯石英的介绍。",
        "说明方法：无特殊说明方法，以叙述过渡。说明语言：{LQ}为此{RQ}承接上文；{LQ}一直{RQ}{LQ}努力{RQ}体现科学家的探索精神；独句成段，起承上启下的过渡作用。",
        [
            ("为此", "为了这个目的"),
            ("验证", "通过实验或检验来证实"),
            ("证据", "能够证明事物真实性的有关事实或材料"),
        ],
    ),
    (
        f"1961年，一位名叫S.M.斯季绍夫的原苏联科学家发现，如果二氧化硅（即非常纯的沙子）处于超高压的状态，那么它的原子相距很近，从而变得极为致密。一立方英寸被压扁的沙子比一立方英寸普通的沙子要重得多。这种被压扁的沙子因此被称为{LQ}斯石英{RQ}。",
        "介绍1961年苏联科学家斯季绍夫的发现：二氧化硅在超高压下变得极为致密，形成被压扁的沙子，即斯石英，并解释斯石英的命名由来。",
        "说明方法：举例子（斯季绍夫的发现）、列数字（一立方英寸）、作比较（斯石英与普通沙子比较）、下定义（斯石英）、作诠释（解释斯石英的形成）。说明语言：括号中补充说明二氧化硅即非常纯的沙子，通俗易懂；{LQ}极为致密{RQ}{LQ}重得多{RQ}准确描述斯石英的特点。",
        [
            ("二氧化硅", "（guī）一种化合物，是沙子、石英等的主要成分，化学式SiO₂"),
            ("超高压", "超过正常压强很多的极高压力"),
            ("原子", "构成化学元素的最小粒子，由原子核和核外电子组成"),
            ("致密", "细而密、细致精密"),
            ("立方英寸", "英美制体积单位，1立方英寸约16.39立方厘米"),
            ("斯石英", "（sī shí yīng）一种在超高压下形成的二氧化硅变体，比普通沙子致密得多"),
        ],
    ),
    (
        f"斯石英并不十分稳定，原子之间靠得太近以至于它们又出现相互排斥的趋势，最后又变为普通沙子。然而，由于原子之间结合得极为致密，所以这种反弹变化进行得非常缓慢，从而使斯石英可保持数百万年。",
        "说明斯石英的不稳定性：原子之间相互排斥，最终会变为普通沙子，但由于结合极为致密，反弹变化非常缓慢，斯石英可保持数百万年。",
        "说明方法：作诠释（解释斯石英不稳定但变化缓慢的原因）、列数字（数百万年）。说明语言：{LQ}并不十分稳定{RQ}准确表述斯石英的性质；{LQ}然而{RQ}转折，说明变化缓慢；{LQ}极为致密{RQ}{LQ}非常缓慢{RQ}准确描述，体现语言的准确性。",
        [
            ("稳定", "稳固安定、不易变化"),
            ("相互排斥", "彼此之间互相推开、不相容"),
            ("趋势", "事物发展的动向"),
            ("反弹", "压紧的物体恢复原状的运动"),
            ("缓慢", "不迅速、慢"),
            ("保持", "维持（原状），使不消失或减弱"),
        ],
    ),
    (
        f"金刚石的形成与此相同。金刚石中的碳原子被挤压得异常紧密，它们同样存在一个向外扩散并且恢复为普通碳的趋势。在通常条件下，这也需要数百万年。",
        "以金刚石的形成类比斯石英：金刚石中的碳原子也被挤压得异常紧密，也有恢复为普通碳的趋势，在通常条件下也需要数百万年，进一步说明斯石英的性质。",
        "说明方法：作比较（金刚石与斯石英类比）、作诠释（解释金刚石的形成和性质）、列数字（数百万年）。说明语言：{LQ}与此相同{RQ}明确类比关系；用读者熟悉的金刚石来解释斯石英，通俗易懂；{LQ}异常紧密{RQ}{LQ}通常条件下{RQ}准确表述。",
        [
            ("金刚石", "一种极硬的宝石，是碳的结晶体，由碳在高温高压下形成"),
            ("碳原子", "碳元素的原子"),
            ("挤压", "挤和压、压迫"),
            ("异常紧密", "不同寻常地紧密"),
            ("扩散", "扩大分散出去"),
            ("普通碳", "一般状态的碳，如石墨、木炭等"),
            ("通常条件", "一般的、正常的条件"),
        ],
    ),
    (
        f"如果你把温度升得足够高，就可使这种变化加快。增温可以增加原子的能量，使它们之间能够相互分离，返回到原始状态。因此，如果在850℃的温度下把斯石英加热30分钟，它将变为普通沙子。（你也可以在真空中对金刚石加热，从而把它恢复到原始碳的状态，但谁愿意这样做呢？）",
        "说明高温可以加快斯石英变为普通沙子的过程：增温增加原子能量，使原子分离，在850℃下加热30分钟斯石英就变为普通沙子。括号中以金刚石类比，并用幽默的笔调说明同样的道理。",
        "说明方法：列数字（850℃、30分钟）、作诠释（解释高温加速变化的原理）、作比较（金刚石与斯石英类比）。说明语言：{LQ}足够高{RQ}{LQ}相互分离{RQ}准确描述原理；括号中的幽默笔调体现了阿西莫夫的语言风格；数字精确具体。",
        [
            ("增温", "增加温度、升温"),
            ("能量", "物质做功的能力，如热能、电能等"),
            ("相互分离", "彼此分开"),
            ("原始状态", "最初的、本来的状态"),
            ("真空", "没有空气或空气极少的空间"),
            ("恢复", "变成原来的样子"),
        ],
    ),
    (
        f"斯石英可以在实验室里制造，但它们在自然界中存在吗？回答是肯定的。然而它们只出现在沙子被强烈挤压的地方。",
        "说明斯石英在自然界中确实存在，但只出现在沙子被强烈挤压的地方，为下文推断撞击说埋下伏笔。",
        "说明方法：设问、作诠释（解释斯石英在自然界存在的条件）。说明语言：{LQ}回答是肯定的{RQ}明确回答；{LQ}然而{RQ}转折，强调存在条件的特殊性；{LQ}只出现在{RQ}准确限定范围，体现语言的严密性。",
        [
            ("实验室", "进行科学实验的场所"),
            ("制造", "用人工使原材料成为可供使用的物品"),
            ("自然界", "自然存在的物质世界，与人类社会相对"),
            ("强烈挤压", "强有力地挤和压"),
        ],
    ),
    (
        f"在一些地方已经发现了斯石英，而且有证据显示，这些地区曾经受到巨大陨石的撞击。撞击所产生的巨大压力形成了斯石英。另外，在进行过原子弹爆炸实验的场地也发现了斯石英，它是由膨胀火球的巨大压力形成的。",
        "说明自然界中斯石英的发现：一些地区曾受到巨大陨石撞击，撞击的巨大压力形成斯石英；原子弹爆炸实验场地也因膨胀火球的巨大压力形成斯石英，证明斯石英只在巨大压力下形成。",
        "说明方法：举例子（陨石撞击地区、原子弹爆炸场地）、作诠释（解释斯石英形成的原因）。说明语言：{LQ}有证据显示{RQ}强调结论的科学性；{LQ}另外{RQ}补充另一个例子；两个例子都证明巨大压力形成斯石英，增强说服力。",
        [
            ("陨石", "含石质较多或全部为石质的陨星，是从宇宙空间落到地球表面的固体块"),
            ("撞击", "运动着的物体跟别的物体猛然碰上"),
            ("巨大压力", "极大的挤压力"),
            ("原子弹", "利用核裂变释放巨大能量的核武器"),
            ("爆炸实验", "为测试武器性能而进行的爆炸试验"),
            ("场地", "进行某种活动的地方"),
            ("膨胀火球", "爆炸时形成的迅速扩大的火球"),
        ],
    ),
    (
        f"似乎可以肯定地说，斯石英也应该出现在压力极高的地壳深处。在这种情况下，它可通过火山喷发被携带到地表。然而，喷发温度极高，岩石会被熔化，所以任何由火山携带而来的斯石英都被转化为普通的二氧化硅。事实上，在火山活动地区至今没有发现过斯石英。",
        "推断斯石英也可能出现在地壳深处，但通过火山喷发带到地表时，由于喷发温度极高，斯石英会被转化为普通二氧化硅，因此火山活动地区至今没有发现过斯石英，从而排除了火山说。",
        "说明方法：作诠释（解释火山喷发不能带来斯石英的原因）、作比较（撞击与火山活动比较）、作假设（假设斯石英出现在地壳深处）。说明语言：{LQ}似乎可以肯定地说{RQ}看似矛盾实则严密——{LQ}似乎{RQ}表示推测，{LQ}肯定{RQ}表示依据充分；{LQ}事实上{RQ}用事实佐证推断，体现语言的准确性和严密性。",
        [
            ("地壳深处", "地球固体圈层最外层的深部"),
            ("火山喷发", "地球内部的岩浆等物质喷出地表的现象"),
            ("携带", "随身带着"),
            ("地表", "地球的表面"),
            ("喷发温度", "火山喷发时的温度"),
            ("熔化", "固体加热到一定程度变成液体"),
            ("转化", "转变、改变"),
            ("二氧化硅", "沙子、石英等的主要成分"),
            ("火山活动地区", "有火山活动的地区"),
            ("至今", "到现在"),
        ],
    ),
    (
        f"那么，你可能会说在斯石英出现的地方肯定发生过撞击，而且肯定没有发生过火山活动。",
        "总结上文的推理：斯石英出现的地方肯定发生过撞击，而且肯定没有发生过火山活动，为下文用斯石英验证恐龙灭绝原因奠定基础。",
        "说明方法：作诠释（总结推理结论）。说明语言：{LQ}那么{RQ}承接上文；两个{LQ}肯定{RQ}强调结论的确定性；独句成段，突出推理结论的重要性。",
        [
            ("撞击", "运动着的物体跟别的物体猛然碰上"),
            ("火山活动", "火山的喷发等活动"),
        ],
    ),
    (
        f"亚里桑那大学的麦克霍恩和几位合作者研究了新墨西哥州拉顿地区的岩层。岩层的年龄为6500万年，因此可以追溯到恐龙灭绝的年代。",
        "介绍科学家的研究：麦克霍恩等人研究了新墨西哥州拉顿地区6500万年前的岩层，这一年代可以追溯到恐龙灭绝的年代，为验证撞击说提供了研究对象。",
        "说明方法：举例子（麦克霍恩的研究）、列数字（6500万年）。说明语言：{LQ}因此{RQ}说明因果关系；{LQ}追溯{RQ}准确说明岩层年代与恐龙灭绝年代的对应关系；介绍研究的时间和地点，具体明确。",
        [
            ("亚里桑那大学", "美国亚利桑那州的一所大学"),
            ("麦克霍恩", "美国科学家，研究斯石英的专家"),
            ("合作者", "一起工作的人"),
            ("新墨西哥州", "美国西南部的一个州"),
            ("拉顿地区", "新墨西哥州的一个地区"),
            ("岩层", "地壳中成层的岩石"),
            ("追溯", "逆流而上，向江河发源处走，比喻探索事物的由来"),
            ("年代", "时代、时期"),
        ],
    ),
    (
        f"他们在1989年3月1日宣布，利用测试固体物质中的原子排列的现代技术，即核磁共振和X光衍射，他们确实检测到了在斯石英中存在的一种原子排列。",
        "说明科学家的研究成果：1989年3月1日，麦克霍恩等人利用核磁共振和X光衍射技术，在6500万年前的岩层中检测到了斯石英的原子排列，为撞击说提供了关键证据。",
        "说明方法：举例子（检测到斯石英）、作诠释（解释核磁共振和X光衍射技术）、列数字（1989年3月1日）。说明语言：{LQ}确实{RQ}强调检测结果的可靠性；{LQ}即{RQ}解释现代技术的具体内容，使读者更容易理解；日期精确，体现科学研究的严谨性。",
        [
            ("宣布", "公开正式告诉大家"),
            ("固体物质", "有一定体积和形状的物质"),
            ("原子排列", "原子在物质中的排列方式"),
            ("现代技术", "当代先进的科学技术"),
            ("核磁共振", "利用原子核在磁场中的共振现象来探测物质结构的技术"),
            ("X光衍射", "利用X光通过晶体时产生的衍射现象来分析物质结构的技术"),
            ("检测", "检验测定"),
            ("原子排列", "原子在物质中的排列方式"),
        ],
    ),
    (
        f"这种情况显示，在6500万年以前曾有巨大的撞击并形成了数吨重的斯石英。这些斯石英在沉降之前曾被溅到了平流层中。那么，造成恐龙灭绝的原因不是火山活动，而应该是撞击。",
        "总结全文，得出结论：6500万年前曾有巨大撞击形成斯石英，这些斯石英被溅到平流层中，因此造成恐龙灭绝的原因不是火山活动，而是撞击，验证了撞击说。",
        "说明方法：作诠释（解释斯石英的沉降过程）、作比较（撞击说与火山说比较）、列数字（6500万年、数吨）。说明语言：{LQ}这种情况显示{RQ}总结研究结果；{LQ}不是……而应该是……{RQ}明确排除火山说，肯定撞击说；{LQ}应该{RQ}留有余地，体现说明文语言的准确性；首尾呼应，结构严谨。",
        [
            ("显示", "明显地表现"),
            ("巨大撞击", "极大的撞击事件"),
            ("数吨", "几吨（1吨=1000千克）"),
            ("沉降", "下沉、降落"),
            ("溅到", "液体受冲击向四外射出，文中指斯石英被抛射到"),
            ("平流层", "地球大气的一层，位于对流层之上"),
            ("火山活动", "火山的喷发等活动"),
            ("撞击", "运动着的物体跟别的物体猛然碰上"),
        ],
    ),
]

parts = [
    ("第一部分", "提出问题，引出两种理论", "1–6 段", "从恐龙灭绝的争论写起，介绍撞击说和火山说两种对立理论，说明研究的现实意义，引出科学家寻找证据验证理论。"),
    ("第二部分", "介绍斯石英的形成和性质", "7–10 段", "介绍斯石英的发现、形成条件、不稳定性和高温加速变化的性质，以金刚石类比说明。"),
    ("第三部分", "斯石英与撞击说的推理", "11–14 段", "说明斯石英在自然界只出现在巨大压力下，火山活动地区没有斯石英，从而推断斯石英出现的地方肯定发生过撞击且没有火山活动。"),
    ("第四部分", "科学验证与结论", "15–17 段", "介绍麦克霍恩等人在6500万年前岩层中检测到斯石英的研究成果，得出恐龙灭绝的原因是撞击而非火山活动的结论。"),
]

para_part = [0,0,0,0,0,0, 1,1,1,1, 2,2,2,2, 3,3,3]

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
    {"w":"铱","py":"yī","q":"发现了稀有金属□，它的含量异常丰富","tip":"「铱」金字旁，稀有金属；生僻字，注意右边是「衣」"},
    {"w":"陨","py":"yǔn","q":"这些地区曾经受到巨大□石的撞击","tip":"「陨」左耳旁，坠落；不要写成「殒」（歹字旁，死亡）"},
    {"w":"劫","py":"jié","q":"发生过一次“大□难”","tip":"「劫」力字旁，灾难；不要写成「却」（卩字旁）"},
    {"w":"硅","py":"guī","q":"如果二氧化□处于超高压的状态","tip":"「硅」石字旁，非金属元素；不要写成「圭」（土字旁）"},
    {"w":"致","py":"zhì","q":"从而变得极为□密","tip":"「致」反文旁，精密；不要写成「至」（土字底）"},
    {"w":"斥","py":"chì","q":"它们又出现相互排□的趋势","tip":"「斥」斤字旁，排斥；不要写成「斤」"},
    {"w":"缓","py":"huǎn","q":"所以这种反弹变化进行得非常□慢","tip":"「缓」绞丝旁，慢；不要写成「暖」（日字旁）"},
    {"w":"碳","py":"tàn","q":"金刚石中的□原子被挤压得异常紧密","tip":"「碳」石字旁，非金属元素；与「炭」（山字头，木炭）区分"},
    {"w":"扩","py":"kuò","q":"它们同样存在一个向外□散并且恢复为普通碳的趋势","tip":"「扩」提手旁，扩大；不要写成「阔」（门字旁）"},
    {"w":"熔","py":"róng","q":"喷发温度极高，岩石会被□化","tip":"「熔」火字旁，固体加热变液体；与「溶」（三点水，溶解）、「融」（虫字旁，融化）区分"},
    {"w":"溯","py":"sù","q":"因此可以追□到恐龙灭绝的年代","tip":"「溯」三点水，逆流而上；不要写成「朔」（shuò，月字旁）"},
    {"w":"衍","py":"yǎn","q":"利用测试固体物质中的原子排□的现代技术","tip":"「衍」双人旁，展开；生僻字，不要写成「行」"},
    {"w":"磁","py":"cí","q":"即核□共振和X光衍射","tip":"「磁」石字旁，磁性；不要写成「慈」（心字底）"},
    {"w":"溅","py":"jiàn","q":"这些斯石英在沉降之前曾被□到了平流层中","tip":"「溅」三点水，液体受冲击射出；不要写成「贱」（贝字旁）"},
    {"w":"潮汐","py":"cháo xī","q":"造成大火和□□大浪","tip":"「潮」三点水，「汐」三点水；双字词整体作答，汐指夜间的潮"},
    {"w":"尘埃","py":"chén āi","q":"许多□□进入了平流层中","tip":"「尘」小字头，「埃」土字旁；双字词整体作答，「埃」不要写成「挨」"},
    {"w":"劫难","py":"jié nàn","q":"发生过一次“大□□”","tip":"「劫」力字旁，「难」又字旁；双字词整体作答，与「灾难」区分"},
    {"w":"致密","py":"zhì mì","q":"由于原子之间结合得极为□□","tip":"「致」反文旁，「密」宝盖头；双字词整体作答，与「精密」「细密」区分"},
]

dict_notes = [
    {"w":"铱","a":"一种稀有金属元素，在陨石中含量较高","q":"发现了稀有金属铱"},
    {"w":"撞击说","a":"认为恐龙灭绝是由小行星或彗星撞击地球引起的理论","q":"目前存在两种对立的理论，即撞击说和火山说"},
    {"w":"火山说","a":"认为恐龙灭绝是由火山大规模喷发引起的理论","q":"目前存在两种对立的理论，即撞击说和火山说"},
    {"w":"二氧化硅","a":"沙子、石英等的主要成分，化学式SiO₂","q":"如果二氧化硅处于超高压的状态"},
    {"w":"斯石英","a":"一种在超高压下形成的二氧化硅变体，比普通沙子致密得多","q":"这种被压扁的沙子因此被称为斯石英"},
    {"w":"致密","a":"细而密、细致精密","q":"从而变得极为致密"},
    {"w":"金刚石","a":"一种极硬的宝石，是碳的结晶体，由碳在高温高压下形成","q":"金刚石的形成与此相同"},
    {"w":"平流层","a":"地球大气的一层，位于对流层之上，气流平稳","q":"许多尘埃进入了平流层中"},
    {"w":"陨石","a":"从宇宙空间落到地球表面的固体块，含石质较多","q":"这些地区曾经受到巨大陨石的撞击"},
    {"w":"追溯","a":"逆流而上，比喻探索事物的由来","q":"因此可以追溯到恐龙灭绝的年代"},
    {"w":"核磁共振","a":"利用原子核在磁场中的共振现象来探测物质结构的技术","q":"即核磁共振和X光衍射"},
    {"w":"X光衍射","a":"利用X光通过晶体时产生的衍射现象来分析物质结构的技术","q":"即核磁共振和X光衍射"},
    {"w":"沉降","a":"下沉、降落","q":"这些斯石英在沉降之前曾被溅到了平流层中"},
    {"w":"说明对象","a":"文章要说明的事物或事理，本文说明恐龙灭绝的原因","q":"科学家们一直对6500万年前恐龙灭绝的一个新观点争论不休"},
    {"w":"逻辑顺序","a":"按照事物或事理的内在逻辑关系安排说明顺序，本文采用从问题到答案的逻辑顺序","q":"为此，科学家们一直都在努力寻找证据来验证这两种理论"},
    {"w":"作诠释","a":"对事物进行解释说明的说明方法，本文大量运用作诠释来解释科学原理","q":"斯石英并不十分稳定"},
    {"w":"举例子","a":"举出实际事例来说明事物的说明方法","q":"例如，1987年就有人指出"},
    {"w":"列数字","a":"用具体数字来说明事物的说明方法","q":"如果在850℃的温度下把斯石英加热30分钟"},
    {"w":"下定义","a":"用简明的语言揭示事物的本质特征的说明方法","q":"这种被压扁的沙子因此被称为斯石英"},
    {"w":"作比较","a":"通过对比来突出事物特征的说明方法","q":"造成恐龙灭绝的原因不是火山活动，而应该是撞击"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《被压扁的沙子》阿西莫夫</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">美国 · 阿西莫夫</div>
  <h1 class="hero-title">被压扁的沙子</h1>
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
    <p>《被压扁的沙子》是美国科普作家阿西莫夫写的一篇科普说明文，选自《新疆域》。文章围绕6500万年前恐龙灭绝的原因，通过介绍{LQ}斯石英{RQ}（被压扁的沙子）的形成和性质，经过严密的逻辑推理，证明了恐龙灭绝的原因是撞击而非火山活动。</p>
    <p>文章以科学问题为切入点，运用举例子、列数字、作比较、作诠释、下定义等多种说明方法，逻辑严密，语言准确而又生动幽默。学习本文重点在于理解作者从斯石英到撞击说的逻辑推理过程。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>阿西莫夫（1920—1992），美国著名科普作家、科幻小说家，美国科幻小说黄金时代的代表人物之一。他一生著述近500本，题材涉及自然科学、社会科学和文学艺术等许多领域，曾获代表科幻界最高荣誉的雨果奖和星云终身成就大师奖。</p>
    <p style="margin-top:10px;color:var(--ink2)">阿西莫夫的科普作品以逻辑严密、语言通俗幽默著称，善于将深奥的科学知识写得深入浅出。代表作有科幻小说《基地》系列、《机器人》系列，科普作品《新疆域》等。《恐龙无处不有》和《被压扁的沙子》均选自《新疆域》。</p>
  </div>
  <div class="box">
    <h3>文体知识</h3>
    <p><b>科普说明文：</b>以介绍科学知识、解释科学原理为主要内容的说明文。它既有说明文的科学性和准确性，又讲究通俗易懂、生动有趣。本文是科普说明文的典范，以{LQ}被压扁的沙子{RQ}这一形象化的题目引发读者兴趣。</p>
    <p style="margin-top:8px"><b>逻辑推理：</b>本文的推理链条是：恐龙灭绝有撞击说和火山说两种理论→斯石英只在巨大压力下形成→火山喷发的高温会使斯石英变为普通沙子→火山活动地区没有斯石英→6500万年前岩层中发现斯石英→恐龙灭绝的原因是撞击。推理严密，环环相扣。</p>
    <p style="margin-top:8px"><b>说明顺序：</b>本文采用从问题到答案的逻辑顺序：先提出恐龙灭绝的问题和两种理论，再介绍斯石英的知识作为推理工具，然后通过推理排除火山说，最后用科学发现验证撞击说。这种顺序符合科学探究的思维过程。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文诵读《被压扁的沙子》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1ju411q7yo&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读被压扁的沙子"></iframe>
        <a href="https://www.bilibili.com/video/BV1ju411q7yo" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>6500万年前恐龙的最后一天</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV1cf8qzYEcq&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="6500万年前恐龙的最后一天"></iframe>
        <a href="https://www.bilibili.com/video/BV1cf8qzYEcq" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
      </div>
    </div>
  </div>
</section>

<div class="divider"></div>
<section id="jielu" class="sec">
  <div class="sec-head"><h2>解 读</h2><span class="no">逐段 · 逻辑推理 · 说明方法</span></div>
  <button id="btnShowAll" class="tbtn" style="display:none;margin-bottom:12px">显示全部</button>
  <div id="fulltext" class="poem" style="display:none">
{fulltext_html}  </div>
  <div class="verse-list" id="verseList">
{verse_html}  </div>
</section>

<div class="divider"></div>
<section id="app" class="sec">
  <div class="sec-head"><h2>赏 析</h2><span class="no">说明对象 · 逻辑推理 · 方法 · 语言</span></div>

  <div class="box">
    <h3>说明对象与特征</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">说明对象：恐龙灭绝的原因</div>
        <p>本文的说明对象是6500万年前恐龙灭绝的原因。文章并不直接说明恐龙灭绝的过程，而是通过{LQ}被压扁的沙子{RQ}（斯石英）这一科学证据，经过严密的逻辑推理，证明恐龙灭绝的原因是撞击而非火山活动。说明对象明确，推理过程是本文的核心。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">题目妙处：形象化引发兴趣</div>
        <p>题目{LQ}被压扁的沙子{RQ}十分巧妙：一是形象化，将抽象的科学概念（斯石英）转化为读者容易理解的{LQ}被压扁的沙子{RQ}，引发阅读兴趣；二是设置悬念，沙子为什么会被压扁？被压扁的沙子与恐龙灭绝有什么关系？引导读者带着问题阅读；三是作为全文的推理线索，斯石英的性质和发现是证明撞击说的关键证据。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>逻辑推理过程（本文重点）</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">推理链条：从两种理论到撞击说</div>
        <p>本文的逻辑推理过程环环相扣，严密有力：<br>①提出问题：6500万年前恐龙灭绝的原因是什么？<br>②两种理论：撞击说（小行星或彗星撞击地球）和火山说（火山大规模喷发）。<br>③引入证据：斯石英（被压扁的沙子）只在超高压下形成。<br>④关键推理：斯石英不稳定，高温下会变为普通沙子；火山喷发温度极高，会将斯石英转化为普通沙子，因此火山活动地区没有斯石英。<br>⑤排除火山说：斯石英出现的地方肯定发生过撞击，且肯定没有发生过火山活动。<br>⑥科学验证：1989年在6500万年前的岩层中检测到斯石英的原子排列。<br>⑦得出结论：恐龙灭绝的原因不是火山活动，而应该是撞击。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">推理特点：科学严密而通俗</div>
        <p>作者的推理有以下特点：一是{LQ}提出问题—分析问题—解决问题{RQ}的结构清晰，符合科学探究的思维过程；二是善于用类比帮助读者理解，如用金刚石的形成类比斯石英，用读者熟悉的事物解释陌生的科学概念；三是用具体的实验数据（850℃、30分钟）和科学发现（1989年检测到斯石英）增强推理的科学性；四是语言通俗幽默，如括号中{LQ}但谁愿意这样做呢？{RQ}的幽默笔调，使抽象的科学推理变得生动有趣。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">举例子与列数字：科学而具体</div>
        <p>举例子贯穿全文：1980年发现铱含量异常、1987年有人提出火山说、1961年斯季绍夫发现斯石英、陨石撞击地区和原子弹爆炸场地发现斯石英、1989年麦克霍恩检测到斯石英等，每个例子都服务于推理过程。列数字精确具体：{LQ}6500万年前{RQ}{LQ}850℃{RQ}{LQ}30分钟{RQ}{LQ}数百万年{RQ}{LQ}1989年3月1日{RQ}等，数字精确，使说明更有科学性和说服力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">作诠释与下定义：准确而通俗</div>
        <p>作诠释是本文最主要的说明方法之一：解释撞击导致灭绝的过程、斯石英的形成和性质、高温加速变化的原理、火山喷发不能带来斯石英的原因、斯石英的沉降过程等，使深奥的科学原理变得通俗易懂。下定义用于揭示概念本质：{LQ}这种被压扁的沙子因此被称为斯石英{RQ}{LQ}撞击说{RQ}{LQ}火山说{RQ}等，用简明的语言揭示事物的本质特征。两种方法结合，文章既科学准确又通俗易懂。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">作比较与分类别：突出而清晰</div>
        <p>作比较贯穿推理过程：斯石英与普通沙子比较（更重、更致密）、金刚石与斯石英类比（形成原理相同）、撞击说与火山说比较（两种对立理论）、撞击地区与火山活动地区比较（有无斯石英），通过比较突出事物特征，推动推理进程。分类别用于梳理理论：{LQ}目前存在两种对立的理论，即撞击说和火山说{RQ}，分类说明使文章条理清晰。多种说明方法综合运用，文章既科学严密又生动有趣。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明顺序与语言</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">说明顺序：从问题到答案的逻辑顺序</div>
        <p>本文整体采用从问题到答案的逻辑顺序：先提出恐龙灭绝的问题和两种对立理论（1-6段），再介绍斯石英的形成和性质作为推理工具（7-10段），然后通过斯石英的性质推理排除火山说（11-14段），最后用科学发现验证撞击说并得出结论（15-17段）。从问题到答案、从理论到验证，符合科学探究的思维过程，条理清晰，逻辑严密。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">说明语言：准确严密而又生动幽默</div>
        <p>本文语言既准确严密，又生动幽默。准确性体现在大量修饰限制词和推测性词语的运用：{LQ}可能{RQ}{LQ}也许{RQ}{LQ}似乎{RQ}{LQ}大约{RQ}{LQ}几乎{RQ}等，这些词语准确地反映了科学认识的程度，体现了说明文语言的准确性和严密性。特别是{LQ}似乎可以肯定地说{RQ}——{LQ}似乎{RQ}表示推测，{LQ}肯定{RQ}表示依据充分，看似矛盾实则非常妥帖。生动性体现在比喻和拟人手法的运用，幽默感体现在括号中的补充说明，如{LQ}但谁愿意这样做呢？{RQ}，体现了阿西莫夫独特的语言风格。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《被压扁的沙子》围绕6500万年前恐龙灭绝的原因，通过介绍斯石英的形成和性质，经过严密的逻辑推理，证明了恐龙灭绝的原因是小行星或彗星撞击地球而非火山活动。文章既传播了科学知识，又展示了科学推理的思维方法，体现了不同科学领域之间紧密相连的科学思想，激发了读者探索自然奥秘的兴趣和严谨求实的科学精神。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 说明术语 · 用字 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">铱</span><span class="acc-d">（yī）一种稀有金属元素，在陨石中含量较高。</span></div>
      <div class="acc-item"><span class="acc-w">潮汐</span><span class="acc-d">（cháo xī）由于月亮和太阳的引力而产生的水位定时涨落的现象。</span></div>
      <div class="acc-item"><span class="acc-w">尘埃</span><span class="acc-d">（chén āi）尘土。</span></div>
      <div class="acc-item"><span class="acc-w">劫难</span><span class="acc-d">（jié nàn）灾难、灾祸。</span></div>
      <div class="acc-item"><span class="acc-w">致密</span><span class="acc-d">（zhì mì）细而密、细致精密。</span></div>
      <div class="acc-item"><span class="acc-w">二氧化硅</span><span class="acc-d">（guī）沙子、石英等的主要成分，化学式SiO₂。</span></div>
      <div class="acc-item"><span class="acc-w">斯石英</span><span class="acc-d">（sī shí yīng）一种在超高压下形成的二氧化硅变体，比普通沙子致密得多。</span></div>
      <div class="acc-item"><span class="acc-w">追溯</span><span class="acc-d">（sù）逆流而上，比喻探索事物的由来。</span></div>
      <div class="acc-item"><span class="acc-w">核磁共振</span><span class="acc-d">利用原子核在磁场中的共振现象来探测物质结构的技术。</span></div>
      <div class="acc-item"><span class="acc-w">X光衍射</span><span class="acc-d">利用X光通过晶体时产生的衍射现象来分析物质结构的技术。</span></div>
      <div class="acc-item"><span class="acc-w">撞击说</span><span class="acc-d">认为恐龙灭绝是由小行星或彗星撞击地球引起的理论。</span></div>
      <div class="acc-item"><span class="acc-w">火山说</span><span class="acc-d">认为恐龙灭绝是由火山大规模喷发引起的理论。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>说明文术语</h3>
      <div class="acc-item"><span class="acc-w">科普说明文</span><span class="acc-d">以介绍科学知识、解释科学原理为主要内容的说明文，既有科学性又通俗易懂。</span></div>
      <div class="acc-item"><span class="acc-w">说明对象</span><span class="acc-d">文章要说明的事物或事理。本文说明恐龙灭绝的原因。</span></div>
      <div class="acc-item"><span class="acc-w">逻辑顺序</span><span class="acc-d">按照事物或事理的内在逻辑关系安排说明顺序。本文采用从问题到答案的逻辑顺序。</span></div>
      <div class="acc-item"><span class="acc-w">逻辑推理</span><span class="acc-d">从已知的判断推出新判断的思维过程。本文从斯石英的性质推理出撞击说，是本文学习的重点。</span></div>
      <div class="acc-item"><span class="acc-w">举例子</span><span class="acc-d">举出实际事例来说明事物。本文举了斯季绍夫的发现、麦克霍恩的研究等大量例子。</span></div>
      <div class="acc-item"><span class="acc-w">列数字</span><span class="acc-d">用具体数字来说明事物。如{LQ}850℃{RQ}{LQ}30分钟{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">作比较</span><span class="acc-d">通过对比来突出事物的特征。如撞击说与火山说比较、斯石英与普通沙子比较。</span></div>
      <div class="acc-item"><span class="acc-w">作诠释</span><span class="acc-d">对事物进行解释说明。本文大量运用作诠释来解释科学原理。</span></div>
      <div class="acc-item"><span class="acc-w">下定义</span><span class="acc-d">用简明的语言揭示事物的本质特征。如{LQ}这种被压扁的沙子因此被称为斯石英{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">分类别</span><span class="acc-d">按照一定标准把事物分成若干类别来说明。如将恐龙灭绝的理论分为撞击说和火山说。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">铱</span><span class="acc-d">（yī）金字旁，稀有金属；生僻字，右边是「衣」。</span></div>
      <div class="acc-item"><span class="acc-w">陨石</span><span class="acc-d">（yǔn）「陨」左耳旁，坠落；与「殒」（歹字旁，死亡）区分。</span></div>
      <div class="acc-item"><span class="acc-w">劫难</span><span class="acc-d">（jié）「劫」力字旁，灾难；不要写成「却」（卩字旁）。</span></div>
      <div class="acc-item"><span class="acc-w">二氧化硅</span><span class="acc-d">（guī）「硅」石字旁，非金属元素；不要写成「圭」（土字旁）。</span></div>
      <div class="acc-item"><span class="acc-w">致密</span><span class="acc-d">（zhì）「致」反文旁，精密；与「至」（土字底）区分。</span></div>
      <div class="acc-item"><span class="acc-w">熔化</span><span class="acc-d">（róng）「熔」火字旁，固体加热变液体；与「溶」（三点水，溶解）、「融」（虫字旁，融化）区分。</span></div>
      <div class="acc-item"><span class="acc-w">追溯</span><span class="acc-d">（sù）「溯」三点水，逆流而上；与「朔」（shuò，月字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">衍射</span><span class="acc-d">（yǎn）「衍」双人旁，展开；生僻字，不要写成「行」。</span></div>
      <div class="acc-item"><span class="acc-w">溅到</span><span class="acc-d">（jiàn）「溅」三点水，液体受冲击射出；与「贱」（贝字旁）区分。</span></div>
      <div class="acc-item"><span class="acc-w">潮汐</span><span class="acc-d">（cháo xī）都是三点水；汐指夜间的潮，与「潮」（白天的潮）区分。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">逻辑推理结构</span><span class="acc-d">采用{LQ}提出问题—介绍证据—推理排除—科学验证—得出结论{RQ}的结构，推理环环相扣。</span></div>
      <div class="acc-item"><span class="acc-w">形象化题目</span><span class="acc-d">用{LQ}被压扁的沙子{RQ}这一形象化题目，将抽象的科学概念转化为读者容易理解的表达，引发兴趣。</span></div>
      <div class="acc-item"><span class="acc-w">类比说明法</span><span class="acc-d">用读者熟悉的金刚石类比斯石英，用通俗的例子解释深奥的科学原理，化难为易。</span></div>
      <div class="acc-item"><span class="acc-w">准确与幽默统一</span><span class="acc-d">修饰限制词和推测性词语体现准确性，括号中的幽默笔调（如{LQ}但谁愿意这样做呢？{RQ}）使文章生动有趣。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">恐龙灭绝</span><span class="acc-d">约6500万年前的白垩纪末，包括恐龙在内的约75%的物种灭绝，是地球历史上第五次生物大灭绝。目前主流观点认为是墨西哥尤卡坦半岛的希克苏鲁伯陨石撞击所致，撞击产生的陨石坑直径约180公里。</span></div>
      <div class="acc-item"><span class="acc-w">斯石英与柯石英</span><span class="acc-d">斯石英和柯石英都是二氧化硅在高压下形成的变体，是判断陨石撞击的重要标志矿物。斯石英由苏联科学家斯季绍夫于1961年发现，以他的名字命名。在地球上，斯石英只在陨石撞击坑和核爆炸场地被发现。</span></div>
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
  <div class="kai">《被压扁的沙子》</div>
  <div>阿西莫夫 · 美国 · 出自《新疆域》</div>
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
