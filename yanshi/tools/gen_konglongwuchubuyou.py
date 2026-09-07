# -*- coding: utf-8 -*-
"""生成《恐龙无处不有》阿西莫夫 课件（科普说明文）"""
import re, json

TEMPLATE = r"D:\App\Apps\yanshi\beiying-zhuziqing.html"
OUT = r"D:\App\Apps\yanshi\konglongwuchubuyou-aximofu.html"
FS_KEY = "konglong_fs"

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
        f"不同科学领域之间是紧密相连的。在一个科学领域的新发现肯定会对其他领域产生影响。",
        "开篇点明全文主旨：不同科学领域之间紧密相连，一个领域的发现会对其他领域产生影响。这是全文的逻辑基础。",
        "说明对象：不同科学领域之间的关系。说明方法：无特殊说明方法，以议论开篇。说明语言：{LQ}紧密相连{RQ}{LQ}肯定{RQ}等词准确有力，点明全文中心，为下文的逻辑推理奠定基础。",
        [
            ("领域", "学术思想或社会活动的范围"),
            ("紧密相连", "彼此关系密切，互相关联"),
            ("新发现", "新的科学发现或研究成果"),
            ("产生影响", "对别的事物起作用、引起变化"),
        ],
    ),
    (
        f"例如，在1986年1月，阿根廷南极研究所宣布在詹姆斯罗斯岛发现了一些化石骨骼。该岛是稍微离开南极海岸的一小片冰冻陆地，非常靠近南美的南端。这些骨头毫无疑问属于鸟臀目恐龙。",
        "以1986年南极发现恐龙化石为例，引出说明话题，介绍发现的时间、地点和化石的归属。",
        "说明方法：举例子（南极发现恐龙化石）。说明语言：{LQ}毫无疑问{RQ}强调化石归属的确定性；{LQ}稍微离开{RQ}{LQ}非常靠近{RQ}准确描述岛屿位置，体现说明文语言的准确性。",
        [
            ("阿根廷", "南美洲东南部的国家"),
            ("南极研究所", "研究南极地区科学问题的机构"),
            ("詹姆斯罗斯岛", "南极洲的一个岛屿，位于南极半岛附近"),
            ("化石骨骼", "古代生物的遗体或遗迹埋藏在地下变成的跟石头一样的东西，文中指恐龙的骨骼化石"),
            ("冰冻陆地", "被冰雪覆盖的陆地"),
            ("鸟臀目", "恐龙的一个目，骨盆结构与鸟类相似，多为植食性恐龙"),
        ],
    ),
    (
        f"在地球的其他大陆上也都发现有恐龙化石。这些古老的爬行动物在南极的出现，说明恐龙确实遍布于世界各地。",
        "指出恐龙化石在其他大陆也有发现，结合南极的发现，得出恐龙遍布世界各地的结论。",
        "说明方法：作比较（南极与其他大陆比较）、作诠释（解释恐龙遍布世界）。说明语言：{LQ}确实{RQ}强调结论的可靠性；{LQ}遍布{RQ}准确说明恐龙分布之广。",
        [
            ("大陆", "地球上面积广大的陆地，全球共有六块大陆"),
            ("爬行动物", "一类脊椎动物，体表有角质鳞片或甲，用肺呼吸，体温不恒定，如蛇、蜥蜴、恐龙等"),
            ("遍布", "分布到所有地方、到处都有"),
        ],
    ),
    (
        f"如果把这个发现与南极大陆联系起来，这比仅考虑恐龙来说要重要得多。恐龙如何能在南极地区生存呢？恐龙实际上并不适应寒冷的气候，现代的两栖动物（青蛙和蟾蜍是人人皆知的现代两栖动物）更不适应南极气候。但1986年在南极确实发现了这种古老的两栖动物的化石。",
        "将南极恐龙化石与南极大陆联系起来思考，提出问题：恐龙如何能在南极生存？指出恐龙不适应寒冷气候，但南极确实有其化石，制造悬念，引出下文。",
        "说明方法：作比较（恐龙与现代两栖动物比较）、举例子（青蛙和蟾蜍）。说明语言：括号中的补充说明使读者更容易理解；{LQ}实际上{RQ}{LQ}确实{RQ}准确表述，体现语言的严密性。",
        [
            ("仅考虑", "只考虑、单单考虑"),
            ("适应", "适合（客观条件或需要）"),
            ("两栖动物", "脊椎动物的一纲，通常没有鳞或甲，皮肤裸露，幼体用鳃呼吸生活在水中，成体用肺呼吸生活在陆地，如青蛙、蟾蜍等"),
            ("蟾蜍", "（chán chú）两栖动物，身体表面有许多疙瘩，内有毒腺，俗称癞蛤蟆"),
            ("人人皆知", "所有人都知道，形容非常著名"),
        ],
    ),
    (
        f"恐龙不可能在每一块大陆上独立生存，那么它们是如何越过大洋到另一个大陆上去的呢？",
        "进一步提出核心问题：恐龙不可能独立生存于每块大陆，它们是如何越过大洋的？以设问引出下文的解答。",
        "说明方法：设问。说明语言：独句成段，起承上启下的过渡作用；{LQ}不可能{RQ}否定一种可能，从而引出另一种解释，逻辑严密。",
        [
            ("独立生存", "不依靠其他条件而单独生存"),
            ("越过大洋", "跨过广阔的海洋"),
        ],
    ),
    (
        f"这一问题的答案是：是大陆在漂移而不是恐龙自己在迁移。几十年前，人们发现地壳是由一些紧密拼合在一起但又在缓慢运动的大板块构成的。一些板块被拉开，而另一些则挤压在一起，一个板块也许会缓慢地向另一板块下面俯冲。{LQ}板块构造{RQ}理论很快为地质界几乎所有的问题提供了答案，如火山、地震、岛屿链、海洋深渊等等，这些在以前一直是不解之谜。",
        "给出答案：是大陆在漂移而非恐龙迁移。介绍板块构造理论的基本内容：地壳由大板块构成，板块在运动，这一理论解释了许多地质之谜。",
        "说明方法：作诠释（解释板块构造理论）、举例子（火山、地震等）、下定义（板块构造理论）。说明语言：{LQ}是……而不是……{RQ}明确区分两种可能；{LQ}几乎所有{RQ}{LQ}一直是不解之谜{RQ}准确表述理论的解释力，体现语言的准确性。",
        [
            ("漂移", "在液体表面漂浮移动，文中指大陆在地幔上缓慢移动"),
            ("迁移", "离开原来的所在地而另换地点"),
            ("地壳", "地球固体圈层的最外层，由岩石组成"),
            ("拼合", "合在一起、组合"),
            ("板块", "地球岩石圈分裂成的许多块体，它们在软流层上缓慢运动"),
            ("俯冲", "（飞机等）以高速度和大角度向下飞，文中指一个板块插到另一个板块下面"),
            ("板块构造", "一种现代地质理论，认为地球岩石圈由若干板块组成，板块在软流层上运动，板块边界是地壳活动带"),
            ("地质界", "研究地球的形成和发展的科学领域"),
            ("岛屿链", "一连串排列的岛屿"),
            ("海洋深渊", "海洋中深度极大的地方，如海沟"),
            ("不解之谜", "弄不明白的事情、谜"),
        ],
    ),
    (
        f"可以这样比喻，板块背上驮着许多大陆，当板块向一个或另一个方向运动时，大陆也随之一起运动。每隔一段时期，板块会将所有的大陆汇聚在一起，地球此时仅由一个主要陆地构成，称为{LQ}泛大陆{RQ}。当板块继续运动时，大陆又重新被分离开。",
        "用比喻说明板块运动与大陆运动的关系：板块驮着大陆运动，周期性地汇聚成泛大陆，然后又分离。",
        "说明方法：打比方（板块背上驮着大陆）、下定义（泛大陆）、作诠释（解释泛大陆的形成和分离）。说明语言：{LQ}驮着{RQ}用拟人化的比喻生动形象；{LQ}每隔一段时期{RQ}{LQ}仅由{RQ}准确描述过程，体现科学性与生动性的统一。",
        [
            ("比喻", "打比方，用相似的事物来比拟想要说的事物"),
            ("驮着", "用背部承受物体的重量"),
            ("汇聚", "聚集、会聚"),
            ("泛大陆", "又称联合古陆，是地史上推测存在的超级大陆，由所有大陆连接而成"),
            ("构成", "形成、组成"),
            ("分离", "分开、脱离"),
        ],
    ),
    (
        f"在四十多亿年的地球发展史中，泛大陆形成和分裂过多次，最后一次完整的泛大陆大约是在2.25亿年前形成的。这个泛大陆存在了数百万年以后，又开始显示出破裂的迹象。",
        "说明在地球漫长的发展史中，泛大陆多次形成和分裂，最后一次完整的泛大陆约在2.25亿年前形成，数百万年后开始破裂。",
        "说明方法：列数字（四十多亿年、2.25亿年、数百万年）。说明语言：{LQ}大约{RQ}表示约数，{LQ}最后一次{RQ}{LQ}完整的{RQ}限定准确，体现说明文语言的准确性和严密性。",
        [
            ("地球发展史", "地球从形成到现在的演化历史，约四十六亿年"),
            ("分裂", "整体的事物分开"),
            ("破裂", "（完整的东西）出现裂缝、开裂"),
            ("迹象", "指表露出来的不很显著的情况，可借以推断过去或将来"),
        ],
    ),
    (
        f"早期恐龙在那时已经开始出现，并且有机会分散到泛大陆的各个地方。所有陆地似乎都处在热带和温带环境内，所以恐龙可以在泛大陆的不同地区舒适地生活。",
        "说明早期恐龙出现时泛大陆尚未分裂，恐龙有机会分散到泛大陆各地，且当时陆地都处在热带和温带，恐龙可以舒适生活。",
        "说明方法：作诠释（解释恐龙为何能遍布泛大陆）。说明语言：{LQ}似乎{RQ}表示推测，留有余地；{LQ}舒适地生活{RQ}生动说明当时气候适宜，体现语言的准确性与生动性。",
        [
            ("早期恐龙", "恐龙发展早期的种类，出现于约2.3亿年前"),
            ("分散", "散在各处、不集中"),
            ("热带", "赤道两侧南北回归线之间的地带，气候炎热"),
            ("温带", "南极圈与南回归线之间、北极圈与北回归线之间的地带，气候温和"),
            ("舒适", "舒服安逸"),
        ],
    ),
    (
        f"大约在两亿年前，泛大陆分裂成四部分。北部就是现在的北美、欧洲和亚洲，南部是由现在的南美和非洲构成，南部是现在的南极洲和澳大利亚，印度是剩余的一小部分。",
        "说明约两亿年前泛大陆分裂成四部分，并具体说明各部分对应的现代大陆。",
        "说明方法：列数字（两亿年前）、分类别（分四部分说明）、作诠释（解释各部分对应的现代大陆）。说明语言：{LQ}大约{RQ}表示约数；分条说明各部分，条理清晰；{LQ}剩余的一小部分{RQ}准确描述印度的位置。",
        [
            ("北美", "北美洲的简称，位于西半球北部"),
            ("欧洲", "位于东半球西北部的大洲"),
            ("亚洲", "位于东半球东北部的大洲，是世界上面积最大的洲"),
            ("南美", "南美洲的简称，位于西半球南部"),
            ("非洲", "位于东半球西南部的大洲"),
            ("南极洲", "位于地球最南端的大洲，几乎全在南极圈内，气候严寒"),
            ("澳大利亚", "位于大洋洲的国家和大陆"),
            ("剩余", "从某个数里减去一部分后余下的"),
        ],
    ),
    (
        f"随着时间的流逝，北美又与亚洲和欧洲分开，南美也与非洲相离。（如果看一张地图，并假定把非洲和南美洲拼合在一起，你就会看到它们拼合得多么天衣无缝。）印度向北移动，并且大约在5000万年前与亚洲相碰撞，形成巨大的喜马拉雅山脉。两个陆块在那里聚合并缓慢地褶皱变形。南极和澳大利亚也已相互分离。",
        "说明泛大陆分裂后各大陆的进一步运动：北美与亚欧分开、南美与非洲相离、印度北移碰撞亚洲形成喜马拉雅山、南极与澳大利亚分离。括号中补充说明非洲与南美洲轮廓吻合，作为大陆漂移的证据。",
        "说明方法：举例子（印度碰撞形成喜马拉雅山）、列数字（5000万年前）、作比较（非洲与南美洲拼合）。说明语言：括号中的补充说明提供了直观证据；{LQ}大约{RQ}表示约数；{LQ}天衣无缝{RQ}形容拼合完美，生动形象。",
        [
            ("流逝", "像流水一样消逝，形容时间过去"),
            ("假定", "姑且认定、假设"),
            ("拼合", "合在一起、组合"),
            ("天衣无缝", "比喻事物（多指诗文、话语等）没有一点破绽，文中指两块大陆的海岸线吻合得非常好"),
            ("碰撞", "运动着的物体跟别的物体猛然碰上"),
            ("喜马拉雅山脉", "世界上最高大的山脉，位于中国与尼泊尔等国交界处"),
            ("陆块", "大陆板块"),
            ("褶皱变形", "岩层因受力而发生弯曲变形，是地壳运动的证据"),
        ],
    ),
    (
        f"当大陆相互分离时，每一个大陆都携带着自己的恐龙而去。到6500万年以前，由于这样或那样的原因，所有的恐龙都灭绝了，大陆也已完全分开。现在的每一个大陆都有自己的恐龙化石。",
        "说明大陆分离时各大陆带走了自己的恐龙，6500万年前恐龙灭绝，大陆完全分开，因此现在每块大陆都有恐龙化石。",
        "说明方法：列数字（6500万年）、作诠释（解释每块大陆都有恐龙化石的原因）。说明语言：{LQ}这样或那样的原因{RQ}不确指，留有余地；{LQ}携带{RQ}用拟人手法生动说明大陆与恐龙的关系。",
        [
            ("携带", "随身带着"),
            ("灭绝", "完全灭亡、消失"),
            ("完全分开", "彻底分离、不再相连"),
        ],
    ),
    (
        f"南极也有自己的恐龙、两栖动物和其他在恐龙时代繁盛的植物和动物。然而，这些生物的命运比其他同类要悲惨得多，因为板块把它们向南携带到了极地。大约经历了一亿年，气候逐渐变冷，植物慢慢越来越稀少，动物的种类和数量也大量减少。气候变得越来越寒冷，夏天短而且冷，最后成为冰天雪地。",
        "说明南极生物的悲惨命运：板块将它们带到极地，经过约一亿年气候逐渐变冷，动植物大量减少，最终成为冰天雪地。",
        "说明方法：列数字（一亿年）、作比较（南极生物与其他同类比较）、作诠释（解释南极生物命运悲惨的原因）。说明语言：{LQ}然而{RQ}转折，突出南极生物的特殊性；{LQ}逐渐{RQ}{LQ}慢慢{RQ}{LQ}越来越{RQ}准确描述气候变化的过程，体现语言的准确性。",
        [
            ("繁盛", "繁荣兴盛"),
            ("命运", "指生死、贫富和一切遭遇"),
            ("悲惨", "处境或遭遇极其痛苦、令人伤心"),
            ("同类", "同一种类的生物"),
            ("极地", "地球的南北两极地区"),
            ("稀少", "事物出现得少、不多"),
            ("冰天雪地", "形容冰雪漫天盖地，非常寒冷"),
        ],
    ),
    (
        f"位于南极中心部位的南极洲是全球的大冰箱，地球上所有冰的十分之九都在南极冰盖。那里的冰有数英里厚，覆盖着丰富的化石。如果南极的冰雪层再薄一些的话，我们就可以找到它们。",
        "说明南极洲是全球的大冰箱，冰盖占全球冰的十分之九，冰层下覆盖着丰富的化石，只是因为冰层太厚难以发现。",
        "说明方法：打比方（全球的大冰箱）、列数字（十分之九、数英里厚）。说明语言：{LQ}大冰箱{RQ}生动形象地说明南极洲的寒冷和冰量之大；{LQ}如果……就……{RQ}用假设说明化石存在但难以发现，表述准确。",
        [
            ("南极洲", "围绕南极的大陆，是世界上纬度最高、气候最寒冷的大洲"),
            ("全球", "全世界、整个地球"),
            ("冰盖", "覆盖在大陆上的巨大冰层，南极冰盖是世界上最大的冰盖"),
            ("数英里", "几英里（1英里约1.609公里）"),
            ("覆盖", "遮盖、掩蔽"),
            ("冰雪层", "冰和雪堆积形成的层"),
        ],
    ),
    (
        f"因此，南极洲恐龙化石的发现，为支持地壳在进行缓慢但又不可抗拒的运动这一理论提供了另一个强有力的证据。",
        "总结全文，指出南极洲恐龙化石的发现为地壳运动理论提供了又一个强有力的证据，呼应开头的主旨。",
        "说明方法：无特殊说明方法，以议论作结。说明语言：{LQ}因此{RQ}总结上文；{LQ}缓慢但又不可抗拒{RQ}准确概括地壳运动的特点；{LQ}强有力的证据{RQ}强调发现的科学价值，首尾呼应，结构严谨。",
        [
            ("支持", "给以鼓励或赞助，文中指为理论提供依据"),
            ("地壳运动", "地壳结构的改变和地壳内部物质的位移，包括水平运动和垂直运动"),
            ("不可抗拒", "不能抵抗、无法阻挡"),
            ("强有力", "力量大、有说服力"),
            ("证据", "能够证明事物真实性的有关事实或材料"),
        ],
    ),
]

parts = [
    ("第一部分", "提出观点，引出发现", "1–3 段", "开篇点明不同科学领域紧密相连的主旨，以南极发现恐龙化石为例，说明恐龙遍布世界各地。"),
    ("第二部分", "提出问题，引出理论", "4–6 段", "提出恐龙如何能在南极生存的问题，引出大陆漂移和板块构造理论。"),
    ("第三部分", "推理过程：泛大陆的分裂", "7–12 段", "说明板块运动导致泛大陆的形成与分裂，恐龙随大陆漂移，最终每块大陆都有恐龙化石。"),
    ("第四部分", "南极生物命运与总结", "13–15 段", "说明南极生物因板块运动命运悲惨，南极洲冰层下覆盖丰富化石，总结恐龙化石发现为地壳运动理论提供证据。"),
]

para_part = [0,0,0, 1,1,1, 2,2,2,2,2,2, 3,3,3]

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
    {"w":"臀","py":"tún","q":"这些骨头毫无疑问属于鸟□目恐龙","tip":"「臀」月字旁，人体后面两股的上端和腰相连接的部分；不要写成「臂」"},
    {"w":"蟾","py":"chán","q":"青蛙和□蜍是人人皆知的现代两栖动物","tip":"「蟾」虫字旁，蟾蜍；不要写成「檐」（木字旁）"},
    {"w":"蜍","py":"chú","q":"青蛙和蟾□是人人皆知的现代两栖动物","tip":"「蜍」虫字旁，蟾蜍；不要写成「余」"},
    {"w":"漂","py":"piāo","q":"是大陆在□移而不是恐龙自己在迁移","tip":"「漂」三点水，漂浮移动；与「飘」（风字旁，随风飘动）区分"},
    {"w":"壳","py":"qiào","q":"人们发现地□是由一些紧密拼合在一起但又在缓慢运动的大板块构成的","tip":"「壳」士字头，坚硬的外皮；多音字，此处读qiào不读ké"},
    {"w":"拼","py":"pīn","q":"地壳是由一些紧密□合在一起但又在缓慢运动的大板块构成的","tip":"「拼」提手旁，合在一起；不要写成「迸」（bèng）"},
    {"w":"俯冲","py":"fǔ chōng","q":"一个板块也许会缓慢地向另一板块下面□□","tip":"「俯」单人旁，「冲」两点水；双字词整体作答，「俯」不要写成「府」"},
    {"w":"渊","py":"yuān","q":"如火山、地震、岛屿链、海洋深□等等","tip":"「渊」三点水，深水；不要写成「源」（也是三点水，但意思不同）"},
    {"w":"驮","py":"tuó","q":"板块背上□着许多大陆","tip":"「驮」马字旁，用背部承受；不要写成「驼」（马字旁，骆驼）"},
    {"w":"汇","py":"huì","q":"板块会将所有的大陆□聚在一起","tip":"「汇」三点水，聚集；不要写成「会」（人字头）"},
    {"w":"裂","py":"liè","q":"又开始显示出破□的迹象","tip":"「裂」衣字底，破开；不要写成「烈」（四点底）"},
    {"w":"迹","py":"jì","q":"又开始显示出破裂的□象","tip":"「迹」辶字旁，留下的印子；不要写成「际」（左耳旁）"},
    {"w":"剩","py":"shèng","q":"印度是□余的一小部分","tip":"「剩」立刀旁，余下的；不要写成「乘」（禾木旁）"},
    {"w":"褶","py":"zhě","q":"两个陆块在那里聚合并缓慢地□皱变形","tip":"「褶」衣字旁，衣服折叠留下的痕迹；生僻字，不要写成「折」"},
    {"w":"携","py":"xié","q":"每一个大陆都□带着自己的恐龙而去","tip":"「携」提手旁，随身带着；不要写成「镌」（juān，金字旁）"},
    {"w":"灭绝","py":"miè jué","q":"所有的恐龙都□□了","tip":"「灭」火字旁，「绝」绞丝旁；双字词整体作答，「灭」不要写成「灰」"},
    {"w":"稀","py":"xī","q":"植物慢慢越来越□少","tip":"「稀」禾字旁，事物出现得少；不要写成「希」（巾字底）"},
    {"w":"覆","py":"fù","q":"那里的冰有数英里厚，□盖着丰富的化石","tip":"「覆」西字头，遮盖；不要写成「复」（夂字头）"},
]

dict_notes = [
    {"w":"鸟臀目","a":"恐龙的一个目，骨盆结构与鸟类相似，多为植食性恐龙","q":"这些骨头毫无疑问属于鸟臀目恐龙"},
    {"w":"两栖动物","a":"脊椎动物的一纲，幼体用鳃呼吸生活在水中，成体用肺呼吸生活在陆地","q":"现代的两栖动物更不适应南极气候"},
    {"w":"漂移","a":"在液体表面漂浮移动，文中指大陆在地幔上缓慢移动","q":"是大陆在漂移而不是恐龙自己在迁移"},
    {"w":"地壳","a":"地球固体圈层的最外层，由岩石组成","q":"人们发现地壳是由一些紧密拼合在一起的大板块构成的"},
    {"w":"板块构造","a":"一种现代地质理论，认为地球岩石圈由若干板块组成，板块在软流层上运动","q":"板块构造理论很快为地质界几乎所有的问题提供了答案"},
    {"w":"俯冲","a":"（飞机等）以高速度和大角度向下飞，文中指一个板块插到另一个板块下面","q":"一个板块也许会缓慢地向另一板块下面俯冲"},
    {"w":"泛大陆","a":"又称联合古陆，是地史上推测存在的超级大陆，由所有大陆连接而成","q":"地球此时仅由一个主要陆地构成，称为泛大陆"},
    {"w":"天衣无缝","a":"比喻事物没有一点破绽，文中指两块大陆的海岸线吻合得非常好","q":"你就会看到它们拼合得多么天衣无缝"},
    {"w":"褶皱变形","a":"岩层因受力而发生弯曲变形，是地壳运动的证据","q":"两个陆块在那里聚合并缓慢地褶皱变形"},
    {"w":"灭绝","a":"完全灭亡、消失","q":"所有的恐龙都灭绝了"},
    {"w":"冰天雪地","a":"形容冰雪漫天盖地，非常寒冷","q":"最后成为冰天雪地"},
    {"w":"冰盖","a":"覆盖在大陆上的巨大冰层","q":"地球上所有冰的十分之九都在南极冰盖"},
    {"w":"不可抗拒","a":"不能抵抗、无法阻挡","q":"地壳在进行缓慢但又不可抗拒的运动"},
    {"w":"说明对象","a":"文章要说明的事物或事理，本文通过南极恐龙化石说明地壳运动理论","q":"不同科学领域之间是紧密相连的"},
    {"w":"逻辑顺序","a":"按照事物或事理的内在逻辑关系安排说明顺序，本文采用从现象到本质的逻辑顺序","q":"恐龙不可能在每一块大陆上独立生存"},
    {"w":"作诠释","a":"对事物进行解释说明的说明方法","q":"这一问题的答案是：是大陆在漂移而不是恐龙自己在迁移"},
    {"w":"打比方","a":"通过比喻来说明事物的说明方法","q":"板块背上驮着许多大陆"},
    {"w":"举例子","a":"举出实际事例来说明事物的说明方法","q":"例如，在1986年1月，阿根廷南极研究所宣布"},
    {"w":"列数字","a":"用具体数字来说明事物的说明方法","q":"大约是在2.25亿年前形成的"},
    {"w":"下定义","a":"用简明的语言揭示事物的本质特征的说明方法","q":"称为泛大陆"},
]

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>《恐龙无处不有》阿西莫夫</title>
<style>{style}</style>
</head>
<body data-fs="100">

<header class="hero">
  <div class="hero-side">美国 · 阿西莫夫</div>
  <h1 class="hero-title">恐龙无处不有</h1>
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
    <p>《恐龙无处不有》是美国科普作家阿西莫夫写的一篇科普说明文，选自《新疆域》。文章从南极发现恐龙化石这一现象出发，通过严密的逻辑推理，证明了地壳板块构造理论，体现了不同科学领域之间紧密相连的科学思想。</p>
    <p>文章以科学发现为切入点，运用举例子、列数字、打比方、作诠释等多种说明方法，逻辑严密，语言准确而又生动幽默，是科普说明文的典范。学习本文重点在于理解作者的逻辑推理过程。</p>
  </div>
  <div class="box">
    <h3>作者简介</h3>
    <p>阿西莫夫（1920—1992），美国著名科普作家、科幻小说家，美国科幻小说黄金时代的代表人物之一。他一生著述近500本，题材涉及自然科学、社会科学和文学艺术等许多领域，曾获代表科幻界最高荣誉的雨果奖和星云终身成就大师奖。</p>
    <p style="margin-top:10px;color:var(--ink2)">阿西莫夫的科普作品以逻辑严密、语言通俗幽默著称，善于将深奥的科学知识写得深入浅出。代表作有科幻小说《基地》系列、《机器人》系列，科普作品《新疆域》等。《恐龙无处不有》和《被压扁的沙子》均选自《新疆域》。</p>
  </div>
  <div class="box">
    <h3>文体知识</h3>
    <p><b>科普说明文：</b>以介绍科学知识、解释科学原理为主要内容的说明文。它既有说明文的科学性和准确性，又讲究通俗易懂、生动有趣，使读者在轻松的阅读中获得科学知识。本文是科普说明文的典范。</p>
    <p style="margin-top:8px"><b>逻辑推理：</b>科普说明文常通过逻辑推理来揭示科学原理。本文的推理链条是：南极发现恐龙化石→恐龙不适应南极气候→恐龙不可能自行越过大洋→是大陆在漂移→板块构造理论。推理严密，环环相扣。</p>
    <p style="margin-top:8px"><b>说明顺序：</b>本文采用从现象到本质的逻辑顺序：先提出科学发现（现象），再分析推理（本质），最后得出结论。这种顺序符合人的认知规律，使文章条理清晰。</p>
  </div>
  <div class="box media-box">
    <h3>视听</h3>
    <div class="media-grid">
      <div class="media">
        <h4>课文诵读《恐龙无处不有》</h4>
        <iframe id="mediaF1" src="https://player.bilibili.com/player.html?bvid=BV1nZ4y1K71S&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="课文诵读恐龙无处不有"></iframe>
        <a href="https://www.bilibili.com/video/BV1nZ4y1K71S" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF1">全屏播放</button>
      </div>
      <div class="media">
        <h4>地球板块漂移科普动画</h4>
        <iframe id="mediaF2" src="https://player.bilibili.com/player.html?bvid=BV19s41177i9&page=1&high_quality=1&danmaku=0&autoplay=0" loading="lazy" scrolling="no" frameborder="0" allowfullscreen="true" title="地球板块漂移科普动画"></iframe>
        <a href="https://www.bilibili.com/video/BV19s41177i9" target="_blank" rel="noopener">在 B 站打开原视频</a><button class="fsbtn" data-target="mediaF2">全屏播放</button>
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
        <div class="f-line">说明对象：地壳板块构造理论</div>
        <p>本文的说明对象不是恐龙本身，而是通过南极恐龙化石的发现来证明地壳板块构造理论。文章以{LQ}不同科学领域之间是紧密相连的{RQ}这一主旨开篇，从古生物学领域的发现（恐龙化石）推导出地质学领域的理论（板块构造），体现了跨学科思维的科学方法。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">说明中心：不同科学领域紧密相连</div>
        <p>全文围绕{LQ}不同科学领域之间是紧密相连的{RQ}这一中心展开：开头提出主旨，中间以南极恐龙化石为例进行推理，结尾指出这一发现为地壳运动理论提供了强有力的证据。古生物学的发现为地质学理论提供了证据，两个领域相互关联、相互印证，中心明确，首尾呼应。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>逻辑推理过程（本文重点）</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">推理链条：从现象到本质</div>
        <p>本文的逻辑推理过程环环相扣，严密有力：<br>①现象：1986年在南极发现鸟臀目恐龙化石，且其他大陆也有恐龙化石。<br>②矛盾：恐龙不适应寒冷的南极气候，不可能在每块大陆上独立生存。<br>③问题：恐龙是如何越过大洋到另一个大陆上去的？<br>④假设：是大陆在漂移而不是恐龙自己在迁移。<br>⑤理论：板块构造理论——地壳由大板块构成，板块驮着大陆缓慢运动。<br>⑥验证：泛大陆的形成与分裂过程解释了恐龙为何遍布各大陆。<br>⑦结论：南极恐龙化石的发现为地壳运动理论提供了强有力的证据。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">推理特点：严密而通俗</div>
        <p>作者的推理有以下特点：一是{LQ}提出问题—分析问题—解决问题{RQ}的结构清晰，用设问句引导读者思考；二是善于用补充说明（括号中的内容）帮助读者理解，如用青蛙和蟾蜍解释两栖动物，用地图拼合说明大陆漂移；三是用具体的时间和数字（2.25亿年、5000万年、6500万年）增强推理的科学性；四是语言通俗幽默，使抽象的地质理论变得生动易懂。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明方法</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">举例子与列数字：科学而具体</div>
        <p>举例子是本文最主要的说明方法：以南极发现恐龙化石为例引出话题，以印度北移碰撞亚洲形成喜马拉雅山为例说明板块运动，以非洲与南美洲轮廓吻合为例说明大陆漂移。列数字贯穿全文：{LQ}2.25亿年前{RQ}{LQ}5000万年前{RQ}{LQ}6500万年以前{RQ}{LQ}一亿年{RQ}{LQ}十分之九{RQ}等，数字精确具体，使说明更有科学性和说服力。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">打比方与作诠释：生动而通俗</div>
        <p>{LQ}板块背上驮着许多大陆{RQ}用打比方（兼拟人）生动形象地说明板块与大陆的关系；{LQ}南极洲是全球的大冰箱{RQ}用打比方说明南极洲的寒冷和冰量之大。作诠释贯穿全文：解释板块构造理论的基本内容、泛大陆的形成与分裂过程、每块大陆都有恐龙化石的原因等，使深奥的科学原理变得通俗易懂。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">作比较与下定义：准确而严密</div>
        <p>{LQ}是大陆在漂移而不是恐龙自己在迁移{RQ}用作比较明确区分两种可能；{LQ}恐龙实际上并不适应寒冷的气候，现代的两栖动物更不适应南极气候{RQ}用比较突出矛盾。下定义用于揭示概念本质：{LQ}称为泛大陆{RQ}{LQ}板块构造理论{RQ}等，用简明的语言揭示事物的本质特征。多种说明方法综合运用，文章既科学准确又生动有趣。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>说明顺序与语言</h3>
    <div class="fame">
      <div class="fame-card">
        <div class="f-line">说明顺序：从现象到本质的逻辑顺序</div>
        <p>本文整体采用从现象到本质的逻辑顺序：先写南极发现恐龙化石的现象（1-3段），再提出恐龙如何能在南极生存的问题（4-5段），然后引出板块构造理论并解释泛大陆的分裂过程（6-12段），最后说明南极生物的命运并总结全文（13-15段）。从现象到本质、从问题到答案，条理清晰，符合人的认知规律。</p>
      </div>
      <div class="fame-card">
        <div class="f-line">说明语言：准确严密而又生动幽默</div>
        <p>本文语言既准确严密，又生动幽默。准确性体现在大量修饰限制词的运用：{LQ}大约{RQ}{LQ}似乎{RQ}{LQ}几乎所有{RQ}{LQ}这样或那样的原因{RQ}等，这些词语准确地反映了科学认识的程度，体现了说明文语言的准确性。生动性体现在比喻和拟人手法的运用：{LQ}板块背上驮着许多大陆{RQ}{LQ}全球的大冰箱{RQ}等，使文章生动有趣。幽默感体现在括号中的补充说明，如{LQ}你也可以在真空中对金刚石加热，但谁愿意这样做呢？{RQ}（见《被压扁的沙子》），体现了阿西莫夫独特的语言风格。</p>
      </div>
    </div>
  </div>

  <div class="box">
    <h3>主题思想</h3>
    <p>《恐龙无处不有》通过南极发现恐龙化石这一科学现象，经过严密的逻辑推理，证明了地壳板块构造理论，说明了不同科学领域之间是紧密相连的，一个科学领域的发现会对其他领域产生影响。文章既传播了科学知识，又展示了科学推理的思维方法，激发了读者探索自然奥秘的兴趣和跨学科思考的科学精神。</p>
  </div>
</section>

<div class="divider"></div>
<section id="acc" class="sec">
  <div class="sec-head"><h2>积 累</h2><span class="no">词语 · 说明术语 · 用字 · 写法</span></div>

  <div class="box">
    <div class="acc-cat">
      <h3>重点词语</h3>
      <div class="acc-item"><span class="acc-w">鸟臀目</span><span class="acc-d">恐龙的一个目，骨盆结构与鸟类相似，多为植食性恐龙。</span></div>
      <div class="acc-item"><span class="acc-w">两栖动物</span><span class="acc-d">脊椎动物的一纲，幼体用鳃呼吸生活在水中，成体用肺呼吸生活在陆地。</span></div>
      <div class="acc-item"><span class="acc-w">漂移</span><span class="acc-d">在液体表面漂浮移动，文中指大陆在地幔上缓慢移动。</span></div>
      <div class="acc-item"><span class="acc-w">地壳</span><span class="acc-d">地球固体圈层的最外层，由岩石组成。</span></div>
      <div class="acc-item"><span class="acc-w">板块构造</span><span class="acc-d">一种现代地质理论，认为地球岩石圈由若干板块组成，板块在软流层上运动。</span></div>
      <div class="acc-item"><span class="acc-w">俯冲</span><span class="acc-d">（飞机等）以高速度和大角度向下飞，文中指一个板块插到另一个板块下面。</span></div>
      <div class="acc-item"><span class="acc-w">泛大陆</span><span class="acc-d">又称联合古陆，是地史上推测存在的超级大陆，由所有大陆连接而成。</span></div>
      <div class="acc-item"><span class="acc-w">天衣无缝</span><span class="acc-d">比喻事物没有一点破绽，文中指两块大陆的海岸线吻合得非常好。</span></div>
      <div class="acc-item"><span class="acc-w">褶皱变形</span><span class="acc-d">岩层因受力而发生弯曲变形，是地壳运动的证据。</span></div>
      <div class="acc-item"><span class="acc-w">灭绝</span><span class="acc-d">完全灭亡、消失。</span></div>
      <div class="acc-item"><span class="acc-w">冰天雪地</span><span class="acc-d">形容冰雪漫天盖地，非常寒冷。</span></div>
      <div class="acc-item"><span class="acc-w">不可抗拒</span><span class="acc-d">不能抵抗、无法阻挡。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>说明文术语</h3>
      <div class="acc-item"><span class="acc-w">科普说明文</span><span class="acc-d">以介绍科学知识、解释科学原理为主要内容的说明文，既有科学性又通俗易懂。</span></div>
      <div class="acc-item"><span class="acc-w">说明对象</span><span class="acc-d">文章要说明的事物或事理。本文通过南极恐龙化石说明地壳板块构造理论。</span></div>
      <div class="acc-item"><span class="acc-w">逻辑顺序</span><span class="acc-d">按照事物或事理的内在逻辑关系安排说明顺序。本文采用从现象到本质的逻辑顺序。</span></div>
      <div class="acc-item"><span class="acc-w">举例子</span><span class="acc-d">举出实际事例来说明事物。本文举了南极恐龙化石、印度碰撞形成喜马拉雅山等例子。</span></div>
      <div class="acc-item"><span class="acc-w">列数字</span><span class="acc-d">用具体数字来说明事物。如{LQ}2.25亿年前{RQ}{LQ}6500万年以前{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">打比方</span><span class="acc-d">通过比喻来说明事物。如{LQ}板块背上驮着许多大陆{RQ}{LQ}全球的大冰箱{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">作比较</span><span class="acc-d">通过对比来突出事物的特征。如{LQ}是大陆在漂移而不是恐龙自己在迁移{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">作诠释</span><span class="acc-d">对事物进行解释说明。本文大量运用作诠释来解释科学原理。</span></div>
      <div class="acc-item"><span class="acc-w">下定义</span><span class="acc-d">用简明的语言揭示事物的本质特征。如{LQ}称为泛大陆{RQ}。</span></div>
      <div class="acc-item"><span class="acc-w">逻辑推理</span><span class="acc-d">从已知的判断推出新判断的思维过程。本文的推理链条是本文学习的重点。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>用字与读音</h3>
      <div class="acc-item"><span class="acc-w">鸟臀目</span><span class="acc-d">（tún）「臀」月字旁；不要写成「臂」（bì，月字旁但意思不同）。</span></div>
      <div class="acc-item"><span class="acc-w">蟾蜍</span><span class="acc-d">（chán chú）都是虫字旁；「蟾」不要写成「檐」，「蜍」不要写成「余」。</span></div>
      <div class="acc-item"><span class="acc-w">漂移</span><span class="acc-d">（piāo yí）「漂」三点水；与「飘移」（风字旁，指随风移动）区分。</span></div>
      <div class="acc-item"><span class="acc-w">地壳</span><span class="acc-d">（qiào）「壳」士字头；多音字，此处读qiào不读ké（蛋壳）。</span></div>
      <div class="acc-item"><span class="acc-w">俯冲</span><span class="acc-d">（fǔ chōng）「俯」单人旁；不要写成「府」（广字头）。</span></div>
      <div class="acc-item"><span class="acc-w">褶皱</span><span class="acc-d">（zhě）「褶」衣字旁；生僻字，不要写成「折」（提手旁）。</span></div>
      <div class="acc-item"><span class="acc-w">携带</span><span class="acc-d">（xié）「携」提手旁；不要写成「镌」（juān，金字旁）。</span></div>
      <div class="acc-item"><span class="acc-w">覆盖</span><span class="acc-d">（fù）「覆」西字头；不要写成「复」（夂字头）。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>写作借鉴</h3>
      <div class="acc-item"><span class="acc-w">逻辑推理结构</span><span class="acc-d">采用{LQ}提出问题—分析问题—解决问题{RQ}的结构，用设问句引导读者，推理环环相扣。</span></div>
      <div class="acc-item"><span class="acc-w">跨学科思维</span><span class="acc-d">从古生物学发现推导出地质学理论，体现不同科学领域之间的紧密联系。</span></div>
      <div class="acc-item"><span class="acc-w">补充说明手法</span><span class="acc-d">善用括号中的补充说明帮助读者理解，如用青蛙和蟾蜍解释两栖动物。</span></div>
      <div class="acc-item"><span class="acc-w">准确与幽默统一</span><span class="acc-d">修饰限制词体现准确性，比喻和拟人使文章生动，幽默的笔调使科普文更有趣。</span></div>
    </div>
  </div>

  <div class="box">
    <div class="acc-cat">
      <h3>文化常识</h3>
      <div class="acc-item"><span class="acc-w">板块构造理论</span><span class="acc-d">20世纪60年代发展起来的地球科学理论，是大陆漂移学说和海底扩张学说的发展。该理论认为地球岩石圈由六大板块组成，板块在软流层上运动，板块边界是地震、火山等地质活动的集中带。</span></div>
      <div class="acc-item"><span class="acc-w">恐龙灭绝</span><span class="acc-d">约6500万年前，包括恐龙在内的大量生物灭绝，称为白垩纪末大灭绝。目前主流观点认为是小行星撞击地球所致（详见《被压扁的沙子》）。</span></div>
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
  <div class="kai">《恐龙无处不有》</div>
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
