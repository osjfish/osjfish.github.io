# -*- coding: utf-8 -*-
"""统一各课件"积累"区板块：同一类型同一骨架、同一命名、同一顺序。

三类标准骨架：
  文言文    通假字 → 古今异义 → 一词多义 → 词类活用 → 文言句式 → 文化常识（文件专属块跟在其后）
  古诗词/词 文体与词牌 → 易错字音形 → 文言梳理 → 〔本文核心考点块〕→ 修辞与手法 → 文化常识
  现代文    重点词语 → 用字与读音 → 修辞方法 → 写作借鉴 → 文化常识（有则加）

规则：空缺的标准块补占位（如通假字）；句式块统一叫"文言句式"；读音块统一叫"用字与读音"；
副标题枚举最终板块。只动 <section id="acc"> 内部与副标题，内容零丢失（自检保证）。
"""
import io, re

BASE = r"D:\App\Apps"

def rd(fn):
    return io.open(BASE + "\\" + fn, encoding="utf-8-sig").read()

def wr(fn, s):
    io.open(BASE + "\\" + fn, "w", encoding="utf-8-sig").write(s)

def bal(s, start, open_tag='<div', close_tag='</div>'):
    i, depth = start, 0
    while i < len(s):
        no, nc = s.find(open_tag, i), s.find(close_tag, i)
        if nc == -1:
            return len(s)
        if no != -1 and no < nc:
            depth += 1
            i = no + len(open_tag)
        else:
            depth -= 1
            i = nc + len(close_tag)
            if depth == 0:
                return i
    return len(s)

def parse_acc_span(s):
    m = re.search(r'<section id="acc"', s)
    if not m:
        return None
    return m.start(), s.find('</section>', m.start()) + len('</section>')

def split_boxes(sec):
    """返回 (head, [(box_html, start, end)...], tail)。单盒含多个 acc-cat 时拆为多个虚拟盒。"""
    first = re.search(r'<div class="box[ "]', sec)
    head = sec[:first.start()]
    spans, i = [], first.start()
    while True:
        m = re.search(r'<div class="box[ "]', sec[i:])
        if not m:
            break
        st, en = i + m.start(), bal(sec, i + m.start())
        spans.append((sec[st:en], st, en))
        i = en
    tail = sec[spans[-1][2]:]
    out = []
    for b, st, en in spans:
        cats = list(re.finditer(r'<div class="acc-cat[ "]', b))
        if len(cats) >= 2:  # 单盒多类（如鸿门宴）：按 acc-cat 拆
            for cm in cats:
                ce = bal(b, cm.start())
                out.append(('<div class="box">' + b[cm.start():ce] + '</div>', st, en))
        else:
            out.append((b, st, en))
    return head, out, tail

def box_title(b):
    m = re.search(r'<h3[^>]*>([^<]+)</h3>', b)
    return m.group(1).strip() if m else '??'

def box_inner(b):
    b2 = re.sub(r'^<div class="box[^"]*"[^>]*>', '', b.strip())
    b2 = re.sub(r'<h3[^>]*>[^<]*</h3>', '', b2, count=1)
    b2 = re.sub(r'</div>\s*$', '', b2)
    return b2.strip()

def norm(x):
    return re.sub(r'[\s　]+', '', re.sub(r'<h3[^>]*>[^<]*</h3>', '', x))

ACC_SUB_CSS = '.acc-sub{font-family:var(--font-kai,serif);font-weight:700;font-size:1.05em;color:var(--ink,#2b2b2b);margin:16px 0 8px;padding-left:10px;border-left:3px solid #b8934a}\n'

def ensure_accsub_css(fn):
    s = rd(fn)
    if '.acc-sub{' not in s:
        wr(fn, s.replace('</style>', ACC_SUB_CSS + '</style>', 1))

def item_box(title, items):
    rows = ''.join('<div class="acc-item"><span class="acc-w">%s</span><span class="acc-d">%s</span></div>\n' % (w, d) for w, d in items)
    return '<div class="box">\n<div class="acc-cat">\n<h3>%s</h3>\n%s</div>\n</div>' % (title, rows)

def merge_box(title, pairs):
    parts = ''.join('<div class="acc-sub">%s</div>\n%s\n' % (t, box_inner(b)) for t, b in pairs)
    return '<div class="box">\n<div class="acc-cat">\n<h3>%s</h3>\n%s</div>\n</div>' % (title, parts)

SHORT = {
 '通假字': '通假', '通假字（本文核心考点）': '通假', '（本文无通假字）': '通假',
 '古今异义': '古今异义', '古今异义（重点）': '古今异义', '一词多义': '一词多义',
 '词类活用': '活用', '文言句式': '句式', '特殊句式': '句式', '文化常识': '文化常识',
 '文体与词牌': '词牌', '易错字音形': '字音形', '易错用字': '字音形', '文言梳理': '文言',
 '修辞与手法': '修辞', '修辞方法': '修辞', '修辞与句式': '修辞',
 '炼字赏析（本文核心考点）': '炼字', '哲理赏析（本文核心考点）': '哲理', '互文修辞（本文核心考点）': '互文',
 '重点词语': '词语', '用字与读音': '用字', '课文用字与读音': '用字', '重点字词读音': '用字',
 '重点词语理解': '词语', '文言现象': '文言', '写作借鉴': '写法', '写作手法': '写法', '人物形象': '人物',
}

def subtitle(fn, titles):
    s = rd(fn)
    sub = ' · '.join(SHORT.get(t, t) for t in titles)
    new, n = re.subn(r'(<h2[^>]*>\s*积\s*累\s*</h2>\s*<span class="no"[^>]*>)[^<]*(</span>)',
                     lambda m: m.group(1) + sub + m.group(2), s, count=1)
    assert n == 1, 'subtitle not found: ' + fn
    wr(fn, new)

def transform(fn, renames, order, new_boxes, merges=None):
    if merges:
        ensure_accsub_css(fn)
    s = rd(fn)
    span = parse_acc_span(s)
    assert span, 'no acc: ' + fn
    sec = s[span[0]:span[1]]
    head, boxed, tail = split_boxes(sec)
    boxes = [b for b, _, _ in boxed]
    if [box_title(b) for b in boxes] == order and not merges:
        subtitle(fn, order)
        print('SKIP(already) %-30s' % fn)
        return
    if merges and '文言梳理' in [box_title(b) for b in boxes] and all(
            t not in [box_title(b) for b in boxes] for _, srcs in merges for t in srcs):
        subtitle(fn, order)
        print('SKIP(merged)  %-30s' % fn)
        return
    old_titles = [box_title(b) for b in boxes]
    old_norms = [norm(box_inner(b)) for b in boxes]  # 比较内容本体，外壳/h3 不计入
    if merges:
        for new_title, src_titles in merges:
            picked = []
            for t in src_titles:
                idx = [box_title(b) for b in boxes].index(t)
                picked.append((t.replace('（重点）', ''), boxes.pop(idx)))
            boxes.append(merge_box(new_title, picked))
    boxes = [re.sub(r'(<h3[^>]*>)[^<]*(</h3>)', lambda m, b=b: m.group(1) + renames.get(box_title(b), box_title(b)) + m.group(2), b, count=1)
             for b in boxes]
    titles = [box_title(b) for b in boxes]
    bmap = dict(zip(titles, boxes))
    final, used = [], set()
    for t in order:
        if t in bmap:
            final.append(bmap[t]); used.add(t)
        elif t in new_boxes:
            final.append(new_boxes[t])
        else:
            raise SystemExit('%s: missing target %s; have %s' % (fn, t, titles))
    leftovers = [t for t in titles if t not in used]
    if leftovers and len(boxes) > len(re.findall(r'<div class="box[ "]', sec)):
        # 虚拟拆分（内嵌 acc-cat）产生的影子盒被丢弃属预期，内容已由丢失检查兜底
        print('  note: drop shadow boxes', leftovers)
    else:
        assert not leftovers, '%s: boxes not placed: %s' % (fn, leftovers)
    # 内容零丢失：每个原盒子的内部内容必须仍出现在最终盒子集合中
    join = '||'.join(norm(b) for b in final)
    for ot, on in zip(old_titles, old_norms):
        assert on in join, '%s: CONTENT LOST: %s' % (fn, ot)
    new_sec = head + '\n'.join(final) + '\n' + tail
    s2 = s[:span[0]] + new_sec + s[span[1]:]
    assert s2.count('<div') - s2.count('</div>') == s.count('<div') - s.count('</div>'), 'div balance broken: ' + fn
    wr(fn, s2)
    subtitle(fn, order)
    print('OK %-38s -> %s' % (fn, ' | '.join(order)))

# ================= 各文件规格 =================
WY_NO = '（本文无通假字）'

def run():
    # ---------- 文言文 ----------
    six = ['通假字', '古今异义', '一词多义', '词类活用', '文言句式', '文化常识']
    transform('ailianshuo-zhoudunyi.html', {}, six, {})
    transform('caoguilunzhan-zuoqiuming.html', {}, six, {})
    transform('chushibiao-zhugeliang.html', {},
              ['通假字', '古今异义', '词类活用', '文言句式', '文化常识'], {})
    transform('hongmenyan-shiji.html', {'特殊句式': '文言句式'},
              ['通假字', '古今异义', '一词多义', '词类活用', '文言句式'], {})
    transform('jichengtiansiyeyou-sushi.html', {},
              ['通假字', '古今异义', '一词多义', '词类活用', '文化常识'],
              {'通假字': item_box('通假字', [(WY_NO, '《记承天寺夜游》全文无通假字。')])})
    transform('lang-pusongling.html', {},
              ['通假字', '古今异义', '一词多义', '词类活用', '文化常识'], {})
    transform('loushiming-liuyuxi.html', {}, six, {})
    transform('mashuo-hanyu.html', {},
              ['通假字（本文核心考点）', '古今异义', '一词多义', '词类活用', '文言句式', '文化常识'], {})
    transform('sanxia-lidaoyuan.html', {},
              ['通假字', '古今异义', '一词多义', '词类活用', '文化常识'], {})
    transform('songdongyangmashengxu-songlian.html', {}, six, {})
    transform('xiaoshitanji-liuzongyuan.html', {},
              ['通假字', '古今异义', '一词多义', '词类活用', '文言句式', '文化常识'],
              {'通假字': item_box('通假字', [(WY_NO, '《小石潭记》全文无通假字；一说“下见小潭”之“见”同“现”，教材未按通假处理。')])})
    transform('yueyanglouji-fanzhongyan.html', {}, six, {})
    transform('yuwosuoyuye-mengzi.html', {}, six, {})

    # ---------- 古诗词 / 词 ----------
    transform('mulanshi-beichaominge.html', {},
              ['文体与词牌', '易错字音形', '文言梳理', '互文修辞（本文核心考点）', '修辞与手法', '文化常识'],
              {
               '文体与词牌': item_box('文体与词牌', [
                   ('乐府诗', '北朝民歌，收入郭茂倩《乐府诗集·横吹曲辞》。乐府本是汉代音乐机关，后指其采制或后人拟作的乐府诗。'),
                   ('乐府双璧', '《木兰诗》与《孔雀东南飞》并称，是古乐府民歌的两大代表作。'),
                   ('体式', '长篇叙事诗，以五言为主，间用排比、对偶、互文，节奏明快，便于传唱。'),
               ]),
               '易错字音形': item_box('易错字音形', [
                   ('机杼', '（zhù）织布机。勿读 shù，勿写“抒”。'),
                   ('可汗', '（kè hán）古代西北少数民族君主称号，勿读 kě hàn。'),
                   ('鞍鞯', '（ān jiān）马鞍和马鞍下的垫子。'),
                   ('辔头', '（pèi）驾驭牲口的嚼子和缰绳。'),
                   ('燕山', '（yān）指北方边塞，勿读 yàn。'),
                   ('胡骑', '（jì）战马，名词，勿读 qí。'),
                   ('著', '（zhuó）“著我旧时裳”，穿、穿戴。'),
                   ('裳', '（cháng）古时下裙，勿读 shang。'),
               ]),
               '修辞与手法': item_box('修辞与手法', [
                   ('排比', '“爷娘闻女来，出郭相扶将……”三段排比铺陈全家迎归，喜气扑面。'),
                   ('顶真', '“军书十二卷，卷卷有爷名”“归来见天子，天子坐明堂”，上递下接，音韵回环。'),
                   ('对偶', '“万里赴戎机，关山度若飞”“朔气传金柝，寒光照铁衣”，工整凝练。'),
                   ('夸张', '“策勋十二转，赏赐百千强”，极言木兰功勋之隆、辞官之决。'),
               ]),
              },
              merges=[('文言梳理', ['通假字', '古今异义', '一词多义', '词类活用', '文言句式'])])

    transform('wangyue-dufu.html', {},
              ['文体与词牌', '易错字音形', '文言梳理', '炼字赏析（本文核心考点）', '修辞与手法', '文化常识'],
              {
               '文体与词牌': item_box('文体与词牌', [
                   ('五言古诗', '《望岳》虽中间两联对仗工整，但不拘平仄粘对，属五言古体诗，而非律诗。'),
                   ('三首《望岳》', '杜甫《望岳》共三首，分咏东岳泰山、西岳华山、南岳衡山，课文所选为咏泰山之作。'),
                   ('岱宗', '泰山别名“岱”，居五岳之首，故尊称“岱宗”。'),
               ]),
               '易错字音形': item_box('易错字音形', [
                   ('岱宗', '（dài）泰山尊称，勿写“贷”。'),
                   ('决眦', '（zì）眼眶，勿写“疵”。'),
                   ('曾云', '（céng）“曾”同“层”，重叠，勿读 zēng。'),
                   ('未了', '（liǎo）不尽，勿读 le。'),
               ]),
               '修辞与手法': item_box('修辞与手法', [
                   ('设问', '“岱宗夫如何？齐鲁青未了”——自问自答，以青色不尽写泰山之广远。'),
                   ('对偶', '“造化钟神秀，阴阳割昏晓”，工整雄健。'),
                   ('拟人', '“钟”字把大自然写得有情，将神秀汇聚于泰山。'),
                   ('夸张', '“会当凌绝顶，一览众山小”，极言俯视一切的气概与抱负。'),
               ]),
              },
              merges=[('文言梳理', ['通假字', '古今异义', '词类活用', '文言句式'])])

    transform('maowu-dufu.html', {},
              ['文体与词牌', '易错字音形', '文言梳理', '修辞与手法', '文化常识'],
              {
               '文体与词牌': item_box('文体与词牌', [
                   ('歌行体', '“歌”是古体诗的一种体裁，句式自由、可换韵、宜于叙事抒情，本诗为歌行体名篇。'),
                   ('写作缘起', '作于唐肃宗上元二年（761）秋，成都草堂刚建成不久，安史之乱尚未平定。'),
               ]),
               '易错字音形': item_box('易错字音形', [
                   ('挂罥', '（juàn）挂着、缠绕，勿写“绢”。'),
                   ('长林梢', '（cháng）高高的树梢，勿读 zhǎng。'),
                   ('塘坳', '（ào）低洼积水处，勿写“拗”。'),
                   ('布衾', '（qīn）被子，勿写“琴”。'),
                   ('丧乱', '（sāng）战乱，指安史之乱，勿读 sàng。'),
                   ('大庇', '（bì）全部遮盖、庇护，勿读 pì。'),
                   ('突兀', '（wù）高耸的样子，勿写“冗”。'),
                   ('见此屋', '（xiàn）“见”同“现”，出现。'),
               ]),
               '修辞与手法': item_box('修辞与手法', [
                   ('夸张', '“卷我屋上三重茅”“安得广厦千万间”，前者极写风势，后者极写宏愿。'),
                   ('对比', '由“床头屋漏无干处”的身寒，翻出“大庇天下寒士”的心热，冷暖相激。'),
                   ('章法', '叙事—抒情—议论层层推进，由一屋之破推及天下寒士，境界节节拔高。'),
                   ('烘托', '“雨脚如麻未断绝”以苦雨长夜烘托难眠之痛，为末段呼号蓄势。'),
               ]),
              },
              merges=[('文言梳理', ['通假字', '古今异义', '词类活用', '文言句式'])])

    for fn in ['changhenge-baijuyi.html', 'pipaxing-baijuyi.html']:
        s = rd(fn)
        span = parse_acc_span(s)
        sec = s[span[0]:span[1]]
        m = re.search(r'<div class="g-item"[^>]*>\s*<dt[^>]*>\s*歌行体.*?</div>', sec, re.S)
        assert m, 'gelongeti g-item not found: ' + fn
        gex = m.group(0)
        head, boxed, tail = split_boxes(sec)
        nb = [b.replace(gex, '', 1) if box_title(b) == '文化常识' else b for b, _, _ in boxed]
        wr(fn, s[:span[0]] + head + '\n'.join(nb) + '\n' + tail + s[span[1]:])
        transform(fn, {'修辞与句式': '修辞与手法'},
                  ['文体与词牌', '易错字音形', '文言梳理', '修辞与手法', '文化常识'],
                  {'文体与词牌': '<div class="box">\n<div class="acc-cat">\n<h3>文体与词牌</h3>\n' + gex + '\n</div>\n</div>'},
                  merges=[('文言梳理', ['古今异义（重点）', '词类活用'])])

    transform('dengfeilaifeng-wanganshi.html', {'修辞方法': '修辞与手法'},
              ['文体与词牌', '易错字音形', '文言梳理', '哲理赏析（本文核心考点）', '修辞与手法', '文化常识'],
              {
               '文体与词牌': item_box('文体与词牌', [
                   ('七言绝句', '四句二十八字，一、二、四句押韵，本诗为王安石早期言志名作。'),
                   ('写作缘起', '宋仁宗皇祐二年（1050）夏，王安石知鄞县任满返乡，途经越州登飞来峰而作，时年三十。'),
                   ('飞来峰', '教材注：在今浙江绍兴城外宝林山，一说在杭州灵隐寺前。'),
               ]),
               '易错字音形': item_box('易错字音形', [
                   ('千寻', '（xún）古以八尺为寻，千寻极言塔高。'),
                   ('自缘', '（yuán）因为，勿误作“绿”。'),
                   ('闻说', '（wén）听说。'),
               ]),
              },
              merges=[('文言梳理', ['古今异义', '一词多义', '文言句式'])])

    transform('qinyuangchunxue-maozedong.html', {'易错用字': '易错字音形'},
              ['文体与词牌', '易错字音形', '文言梳理', '修辞与手法', '文化常识'],
              {
               '文言梳理': item_box('文言梳理', [
                   ('大河', '古义：指黄河；今义：泛指大的河流。“大河上下，顿失滔滔”。'),
                   ('风骚', '古义：本指《诗经·国风》与《楚辞·离骚》，泛指文学才华；今义：多含贬义。'),
                   ('风流人物', '古义：建功立业的英雄人物；今义：有才学而不拘礼法的人。'),
                   ('须', '古义：等到，“须晴日”；今义：必须、胡须。'),
               ]),
              })

    # ---------- 现代文 ----------
    transform('beiying-zhuziqing.html', {},
              ['重点词语', '用字与读音', '修辞方法', '写作借鉴'],
              {'用字与读音': item_box('用字与读音', [
                  ('差使', '（chāi）旧时职务、官职。“谋差使”。'),
                  ('奔丧', '（sāng）从外地急忙赶回去料理长辈亲属的丧事。'),
                  ('狼藉', '（jí）乱七八糟的样子。'),
                  ('簌簌', '（sù）形容眼泪纷纷落下的样子。'),
                  ('举箸', '（zhù）筷子。'),
                  ('颓唐', '（tuí）衰颓败落。'),
                  ('琐屑', '（xiè）细小而繁多（的事务）。'),
              ])})
    transform('chun-zhuziqing.html', {},
              ['重点词语', '用字与读音', '修辞方法', '写作借鉴'],
              {'用字与读音': item_box('用字与读音', [
                  ('朗润', '（rùn）明亮滋润。'),
                  ('酝酿', '（yùn niàng）原指造酒发酵，文中指各种气息在空气里越来越浓。'),
                  ('黄晕', '（yùn）昏黄不明亮的光圈，勿读 hūn。'),
                  ('应和', '（hè）呼应、唱和，勿读 hé。'),
                  ('抖擞', '（sǒu）振作。'),
                  ('蓑衣', '（suō）用草或棕编成的雨衣。'),
                  ('嘹亮', '（liáo）声音清脆响亮。'),
              ])})
    transform('hetangyuese-zhuziqing.html', {},
              ['重点词语', '用字与读音', '修辞方法', '写作借鉴'],
              {'用字与读音': item_box('用字与读音', [
                  ('蓊蓊郁郁', '（wěng wěng yù yù）树木茂盛的样子。'),
                  ('袅娜', '（niǎo nuó）柔美的样子，形容荷花姿态。'),
                  ('脉脉', '（mò）形容水没有声音、好像饱含感情，勿读 mài。'),
                  ('霎时', '（shà）极短的时间。'),
                  ('敛裾', '（liǎn jū）收拢衣襟。裾，衣襟。'),
                  ('梵婀玲', '（fàn ē líng）英语 violin 的音译，小提琴。'),
              ])})
    transform('guxiang-luxun.html', {},
              ['重点词语', '用字与读音', '修辞方法', '写作借鉴'],
              {'用字与读音': item_box('用字与读音', [
                  ('阴晦', '（huì）阴沉昏暗。'),
                  ('五行缺土', '（xíng）旧时迷信用天干地支推算的五行，勿读 háng。'),
                  ('伶仃', '（líng dīng）孤独，没有依靠。'),
                  ('獾猪', '（huān）一种野兽。'),
                  ('潮汛', '（xùn）定期上涨的潮水。'),
                  ('惘然', '（wǎng）心里好像失去了什么的样子。'),
                  ('恣睢', '（zì suī）放纵、凶暴。'),
              ])})
    transform('denglong-wubojie.html', {},
              ['重点词语', '用字与读音', '修辞方法', '写作借鉴'],
              {'用字与读音': item_box('用字与读音', [
                  ('斡旋', '（wò xuán）调停、调解；文中指灯彩穿行回转。'),
                  ('幽悄', '（qiǎo）幽深寂静，勿读 qiāo。'),
                  ('神龛', '（kān）供奉神位的小阁子。'),
                  ('犬吠', '（fèi）狗叫。'),
                  ('汲', '（jí）从下往上打水。'),
              ])})
    transform('zitengluopubu-zongpu.html', {},
              ['重点词语', '用字与读音', '修辞方法', '写作借鉴'],
              {'用字与读音': item_box('用字与读音', [
                  ('迸溅', '（bèng jiàn）向外溅出、喷射。'),
                  ('伫立', '（zhù）长时间地站着。'),
                  ('仙露琼浆', '（qióng）比喻美酒，文中形容花朵晶莹如仙酒。'),
                  ('盘虬卧龙', '（qiú）盘绕弯曲如卧龙，形容枝干。虬，传说中的一种龙。'),
                  ('酒酿', '（niàng）甜米酒，文中形容花香。'),
                  ('绽开', '（zhàn）裂开、开放。'),
              ])})
    for fn in ['kongyiji-luxun.html', 'laowang-yangjiang.html', 'shexi-luxun.html']:
        transform(fn, {'课文用字与读音': '用字与读音'},
                  ['重点词语', '用字与读音', '修辞方法', '写作借鉴'], {})
    transform('bianselong-qikefu.html', {'课文用字与读音': '用字与读音'},
              ['重点词语', '用字与读音', '修辞方法', '写作借鉴', '文化常识'], {})

    # 我的叔叔于勒：并回现代文骨架，"人物形象"并入"写作借鉴"
    fn = 'wodeshushuyule-mobosang.html'
    ensure_accsub_css(fn)
    s = rd(fn)
    span = parse_acc_span(s)
    sec = s[span[0]:span[1]]
    head, boxed, tail = split_boxes(sec)
    bmap = {box_title(b): b for b, _, _ in boxed}
    if '人物形象' not in bmap:
        nb = None  # 已并入写作借鉴，直接重排
    else:
        rw = bmap['写作手法']
        rw_items = ''.join(re.findall(r'<div class="acc-item">.*?</div>', box_inner(bmap['人物形象']), re.S))
        assert 'acc-item' in rw_items, 'yule: no items found'
        borrow = '<div class="acc-sub">人物形象</div>\n' + rw_items + '\n'
        new_rw = re.sub(r'</div>\s*</div>\s*$', borrow + '</div>\n</div>', rw.strip())
        assert new_rw != rw, 'yule merge failed'
        nb = [new_rw if box_title(b) == '写作手法' else b for b, _, _ in boxed if box_title(b) != '人物形象']
        wr(fn, s[:span[0]] + head + '\n'.join(nb) + '\n' + tail + s[span[1]:])
    transform(fn, {'重点词语理解': '重点词语', '重点字词读音': '用字与读音', '写作手法': '写作借鉴'},
              ['重点词语', '用字与读音', '修辞方法', '写作借鉴'],
              {'修辞方法': item_box('修辞方法', [
                  ('比喻', '“在一片平静得好似绿色大理石桌面的海上驶向远处”——以镜面海写平静，反衬后文人心的波澜。'),
                  ('反复', '“唉！如果于勒竟在这只船上，那会叫人多么惊喜呀！”两度出现，盼富心理的定格与反讽。'),
                  ('夸张', '“拟定了上千种计划”，极言全家发财幻想之炽。'),
              ])})

    # 桃花源记 / 醉翁亭记：文言现象盒拆分归位，迁移到文言六块
    migrate_th('taohuayuanji-taoyuanming.html', {
        '通假字': item_box('通假字', [
            ('要', '同“邀”，邀请。“便要还家”。'),
            ('具', '通“俱”，全、详细。“具答之”“具言所闻”。'),
        ]),
        '古今异义': item_box('古今异义', [
            ('妻子', '古义：妻与子女；今义：仅指配偶。'),
            ('绝境', '古义：与世隔绝之地；今义：绝望处境。'),
            ('无论', '古义：更不必说；今义：表条件关系的连词。'),
            ('交通', '古义：交错相通；今义：运输事业。'),
        ]),
        '一词多义': item_box('一词多义', [
            ('乃', '“见渔人，乃大惊”意为“于是、就”；“乃不知有汉”意为“竟然”，须据语境分辨。'),
            ('遂', '“遂与外人间隔”意为“于是”；“遂迷，不复得路”“后遂无问津者”意为“终于”，暗含转折。'),
        ]),
        '词类活用': item_box('词类活用', [
            ('异', '意动用法，以……为异。“渔人甚异之”。'),
            ('志', '名词作动词，做标记。“处处志之”。'),
        ]),
        '文言句式': item_box('文言句式', [
            ('省略句', '“（渔人）便舍船，从口入”“（村人）见渔人，乃大惊，问所从来”“（渔人）具答之”——多处承前省略主语。'),
            ('判断句', '“南阳刘子骥，高尚士也”——“也”表判断。'),
        ]),
        '文化常识': item_box('文化常识', [
            ('诗序', '《桃花源记》原是《桃花源诗》前的序文，约作于南朝宋永初二年（421），后独立成篇。'),
            ('武陵', '郡名，今湖南常德一带。'),
            ('朝代链', '“乃不知有汉，无论魏晋”暗写桃源人避世之久：秦—汉—魏—晋。'),
            ('成语出处', '世外桃源、豁然开朗、无人问津、怡然自乐、鸡犬相闻等成语皆出此文。'),
        ]),
    }, ['重点词语', '写作借鉴'])
    migrate_th('zuiwengtingji-ouyangxiu.html', {
        '通假字': item_box('通假字', [('（本文无通假字）', '《醉翁亭记》全文无通假字。')]),
        '古今异义': item_box('古今异义', [
            ('意', '古义：情趣，“意不在酒”；今义：意思、心意。'),
            ('提携', '古义：指被搀扶的小孩，“伛偻提携”；今义：搀扶、提拔。'),
            ('时', '古义：季节，“山间之四时”；今义：时间。'),
            ('发', '古义：开放，“野芳发而幽香”；今义：出发、发生。'),
        ]),
        '一词多义': item_box('一词多义', [
            ('归', '“云归而岩穴暝”意为“聚拢”；“太守归而宾客从”意为“回去”，须据语境分辨。'),
            ('谓', '“太守自谓也”意为“称呼、称作”；“太守谓谁”意为“为、是”。'),
            ('乐', '“山水之乐”是名词“乐趣”；“乐亦无穷”是动词“感到快乐”；“乐其乐”前一个“乐”是意动“以……为乐”。'),
        ]),
        '词类活用': item_box('词类活用', [
            ('名', '名词作动词，命名。“名之者谁”。'),
            ('号', '名词作动词，取别号。“故自号曰醉翁”。'),
            ('山', '名词作状语，沿山路。“山行六七里”。'),
        ]),
        '文言句式': item_box('文言句式', [
            ('判断句', '“……者，……也”表判断，如“琅琊也”“醉翁亭也”“太守宴也”，是本文标志性句式，舒缓从容。'),
        ]),
        '文化常识': item_box('文化常识', [
            ('醉翁亭', '在今安徽滁州琅琊山，为僧智仙所建，因欧阳修此记而名扬天下。'),
            ('贬滁', '庆历新政失败后，欧阳修于庆历五年（1045）贬知滁州，本文作于庆历六年前后。'),
            ('成语出处', '醉翁之意不在酒、水落石出、觥筹交错、峰回路转、前呼后拥皆出本文。'),
            ('地位', '欧阳修为北宋诗文革新运动领袖，唐宋八大家之一。'),
        ]),
    }, ['重点词语', '写作借鉴'])

def migrate_th(fn, newb, extras):
    """弹掉"文言现象"盒（内容已手工拆入 newb），其余原样保留后统一重排。"""
    s = rd(fn)
    span = parse_acc_span(s)
    sec = s[span[0]:span[1]]
    head, boxed, tail = split_boxes(sec)
    if box_title(boxed[0][0]) != '文言现象' and '文言现象' not in sec:
        transform(fn, {}, ['通假字', '古今异义', '一词多义', '词类活用', '文言句式', '文化常识'] + extras, newb)
        return
    nb = [b for b, _, _ in boxed if box_title(b) != '文言现象']
    wr(fn, s[:span[0]] + head + '\n'.join(nb) + '\n' + tail + s[span[1]:])
    transform(fn, {}, ['通假字', '古今异义', '一词多义', '词类活用', '文言句式', '文化常识'] + extras, newb)


if __name__ == '__main__':
    run()
    print('ALL DONE')
