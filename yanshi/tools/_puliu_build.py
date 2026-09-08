# -*- coding: utf-8 -*-
"""蒲柳人家构建：背景三盒+视频、解读35卡+part2、fulltext35pl、acc区、kai、题库"""
import re, sys
sys.path.insert(0, r'D:\App\Apps\yanshi\tools')
from _puliu_data import PARAS, PARTS, ACC, BG_NEW

F = 'puliurenjia-liushaotang.html'
raw = open(F, 'rb').read()
s = raw.decode('utf-8')
crlf = '\r\n' if '\r\n' in s else '\n'
AMAP = {}
for _, _, _, annos in PARAS:
    for w, n in annos:
        AMAP.setdefault(w, n)
WORDS = sorted(AMAP.keys(), key=len, reverse=True)
ESCAPE = lambda t: t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def annotate(plain):
    out, i, miss = [], 0, 0
    while i < len(plain):
        hit = None
        for w in WORDS:
            if plain.startswith(w, i):
                hit = w
                break
        if hit:
            out.append('<span class="anno-word" data-note="%s">%s</span>' % (AMAP[hit], hit))
            i += len(hit)
        else:
            out.append(ESCAPE(plain[i]))
            i += 1
    return ''.join(out)

assert len(PARAS) == 35, '段数异常 %d' % len(PARAS)

# ---------- 卡片 HTML ----------
cards = []
for k, (txt, gai, shoufa, _) in enumerate(PARAS):
    card = (
        '      <div class="verse" id="p{n}" data-i="{i}">' + crlf +
        '        <div class="v-top"><span class="v-no">{n}</span><div class="v-line" style="font-size:17px;line-height:2">{txt}</div></div>' + crlf +
        '        <details class="v-more">' + crlf +
        '          <summary>内容 · 手法</summary>' + crlf +
        '          <div class="d-body">' + crlf +
        '            <div class="v-sec"><b class="v-label">内容概括</b>' + crlf +
        '              <div class="v-trans">{gai}</div>' + crlf +
        '            </div>' + crlf +
        '            <div class="v-sec"><b class="v-label">手法分析</b>' + crlf +
        '              <div class="d-body"><p>{shoufa}</p></div>' + crlf +
        '            </div>' + crlf +
        '          </div>' + crlf +
        '        </details>' + crlf +
        '      </div>'
    ).format(n=k + 1, i=k, txt=annotate(txt), gai=gai, shoufa=shoufa)
    cards.append(card)

def part_html(p):
    num, title, rng, over = p
    return '  <div class="part-head"><span class="p-num">%s</span><h3>%s</h3><span class="range">%s</span></div>%s  <div class="part-overview">%s</div>%s' % (num, title, rng, crlf, over, crlf)

verse_inner = part_html(PARTS[0]) + '\n'.join(cards[:14]) + '\n\n' + part_html(PARTS[1]) + '\n'.join(cards[14:])

# ---------- 定位替换 ----------
mj = re.search(r'<section[^>]*id="jielu"[^>]*>', s)
ma = re.search(r'<section[^>]*id="app"[^>]*>', s)
j = s[mj.end():ma.start()]
vl_s = j.find('<div class="verse-list" id="verseList">')
assert vl_s >= 0
vl_e = j.find('</section>')
j_new = j[:vl_s] + '<div class="verse-list" id="verseList">' + crlf + verse_inner + crlf + j[vl_e:]
s = s[:mj.end()] + j_new + s[ma.start():]

# ---------- fulltext 35 pl ----------
mf = re.search(r'<div[^>]*id="fulltext"[^>]*>', s)
ft_end = s.find('</div>', s.find('class="pl"', mf.end()))
# fulltext 的结束 </div>：找最后一个 pl 之后
last_pl = s.rfind('class="pl"', mf.end())
ft_close = s.find('</div>', last_pl)
old_ft_inner = s[mf.end():ft_close]
pls = crlf.join('      <p class="pl">%s</p>' % annotate(t) for t, _, _, _ in PARAS)
s = s[:mf.end()] + crlf + pls + crlf + '    ' + s[ft_close:]

# ---------- 背景三盒替换 ----------
# BG_NEW 按 <div class="box"> 切块，取含对应 h3 的块（含结尾 </div>）
bg_blocks = re.split(r'(?=\n  <div class="box")', BG_NEW)
for h3 in ['作者简介', '时代背景', '写作缘起']:
    bnew = next(b for b in bg_blocks if ('<h3>%s</h3>' % h3) in b)
    pat = re.compile(r'<div class="box">\s*<h3>%s</h3>.*?\n  </div>' % h3, re.S)
    m = pat.search(s)
    assert m, h3
    s = s[:m.start()] + bnew.strip() + s[m.end():]

# ---------- 视频替换 ----------
s = s.replace('BV1k94y1S73S', 'BV1ae411p7LG')
s = s.replace('BV1kx4y1P758', 'BV1yb4y1Q7XS')
s = s.replace('鲁迅蒲柳人家全文朗诵', '《蒲柳人家》课文朗读（部编版九下第8课）')
s = s.replace('【孔乙己】话剧（完整版）', '《蒲柳人家》知识点串讲（刘绍棠）')
s = s.replace('title="《蒲柳人家》诵读"', 'title="《蒲柳人家》知识点串讲"')

# ---------- kai 块 ----------
old_kai = '<div class="kai">蒲柳人家</div>%s  <div>鲁迅 · 现代 · 选自《呐喊》</div>%s  <div>本篇最初发表于 1919 年 4 月《新青年》第六卷第四号</div>' % (crlf, crlf)
new_kai = '<div class="kai">《蒲柳人家》</div>%s  <div>刘绍棠 · 当代 · 节选自《蒲柳人家》，选自《十月》1980年第3期</div>' % crlf
assert old_kai in s, 'kai未匹配'
s = s.replace(old_kai, new_kai)

# ---------- acc 区插入（app 与 practice 之间）----------
mp = re.search(r'<section[^>]*id="practice"[^>]*>', s)
s = s[:mp.start()] + '<section id="acc">' + crlf + ACC + '</section>' + crlf + '<div class="divider"></div>' + crlf + crlf + s[mp.start():]

# ---------- 题库替换（第二 script 块）----------
DW = [
    {"w":"痱","py":"fèi","q":"就得起大半身□子","tip":"「痱子」病字旁，音 fèi，勿写「排子」"},
    {"w":"擀","py":"gǎn","q":"手握着□面杖要梆他","tip":"「擀面杖」提手旁，音 gǎn，勿写「杆」"},
    {"w":"梆","py":"bāng","q":"擀面杖要□他","tip":"「梆」木字旁，敲打义，勿写「绑」"},
    {"w":"腌臜","py":"ā zā","q":"不能叫你们□□了我们大姑娘小媳妇儿的眼睛","tip":"「腌臜」皆为月（肉）字旁，脏、不干净，勿写「腌砸」"},
    {"w":"捯","py":"dáo","q":"紧一口慢一口□气","tip":"「捯气」提手旁，音 dáo，喘息，勿写「倒气」"},
    {"w":"讳","py":"huì","q":"何满子的爷爷，名□已不可考","tip":"「名讳」言字旁，音 huì，勿写「伟」「违」"},
    {"w":"嗓","py":"sǎng","q":"青铜肤色，□门也亮堂","tip":"「嗓」口字旁，音 sǎng，勿写「搡」「桑」"},
    {"w":"蕉","py":"jiāo","q":"就像雨打芭□","tip":"「芭蕉」草字头，音 jiāo，勿写「焦」"},
    {"w":"谑","py":"xuè","q":"一半是戏□，一半是尊敬","tip":"「戏谑」言字旁，音 xuè，开玩笑，勿写「虐」"},
    {"w":"膺","py":"yīng","q":"在荣□这个尊称之后","tip":"「荣膺」月（肉）字旁，音 yīng，承受，勿写「荣鹰」"},
    {"w":"匿","py":"nì","q":"何满子却隐□在柳棵子地里","tip":"「隐匿」匚部，音 nì，隐藏，勿写「隐慝」"},
    {"w":"垣","py":"yuán","q":"只剩下断壁残□","tip":"「残垣」土字旁，音 yuán，墙，勿写「恒」「桓」"},
    {"w":"毡","py":"zhān","q":"难受得屁股下如坐针□","tip":"「针毡」毛字旁，音 zhān，毡子，勿写「沾」「毡」混用"},
    {"w":"啭","py":"zhuàn","q":"柳树梢上莺啼燕□","tip":"「燕啭」口字旁，音 zhuàn，鸟婉转鸣叫，勿写「转」"},
    {"w":"嘬","py":"zuō","q":"就想□着嘴唇学鸟叫","tip":"「嘬」口字旁，音 zuō，吸吮，勿写「撮」"},
    {"w":"剜","py":"wān","q":"心疼得就像一块一块□肉","tip":"「剜肉」刀字底，音 wān，挖，勿写「腕」"},
    {"w":"绽","py":"zhàn","q":"掌舵的□裂了虎口","tip":"「绽裂」绞丝旁，音 zhàn，裂开，勿写「锭」「淀」"},
    {"w":"捻","py":"niǎn","q":"拨动着一支牛拐骨□麻绳","tip":"「捻麻绳」提手旁，音 niǎn，搓，勿写「撵」「捻」混用"},
]
DN = [
    {"w":"一气呵成","q":"鼓点似的骂一天，一气呵成，也不倒嗓子。","a":"不间断地完成，形容骂人酣畅连贯"},
    {"w":"断壁残垣","q":"只剩下断壁残垣，埋没于蓬蒿荆棘之中。","a":"（yuán）形容建筑物倒塌残破的景象"},
    {"w":"如坐针毡","q":"难受得屁股下如坐针毡，身上像芒刺在背。","a":"（zhān）形容心神不宁、坐立不安"},
    {"w":"影影绰绰","q":"从大人们的只言片语里，影影绰绰听说爷爷在口外还有一个相好的女人。","a":"模模糊糊，不真切"},
    {"w":"望眼欲穿","q":"但是，何满子望眼欲穿，这颗救命星却迟迟不从东边闪现出来。","a":"形容盼望殷切"},
    {"w":"天伦之乐","q":"最大的盼头就是享天伦之乐。","a":"家庭中亲人团聚的欢乐"},
    {"w":"礼贤下士","q":"要的就是刘皇叔那样的礼贤下士。","a":"恭敬地对待有才能的人"},
    {"w":"不耻下问","q":"遇上生字儿，不耻下问，而且舍得掏学费。","a":"向学问不如自己的人请教不觉得丢脸"},
    {"w":"云山雾罩","q":"听他谈讲过五关，斩六将，云山雾罩。","a":"说话漫无边际、不着边际"},
    {"w":"腰缠万贯","q":"但是回到村来，却要装得好像腰缠万贯。","a":"形容非常有钱"},
    {"w":"妙手回春","q":"都来找她妙手回春。","a":"称赞医生医术高明，能把重病治好"},
    {"w":"呱呱坠地","q":"一丈青大娘一听见孙子呱呱坠地的啼声，喜泪如雨。","a":"（gū gū）婴儿出生"},
    {"w":"两肋插刀","q":"爱打抱不平，为朋友敢两肋插刀。","a":"为朋友不怕牺牲，形容重义气"},
    {"w":"咬牙切齿","q":"奶奶气得咬牙切齿地骂他。","a":"形容愤恨到极点"},
    {"w":"不依不饶","q":"一丈青大娘不依不饶，站在河边大骂不住声。","a":"纠缠不休，不肯罢休"},
]
import json
dict_js = 'var DICT_WORDS = %s;%svar DICT_NOTES = %s;' % (
    json.dumps(DW, ensure_ascii=False), crlf, json.dumps(DN, ensure_ascii=False))
m2 = re.search(r'<script>\s*var DICT_WORDS.*?</script>', s, re.S)
assert m2, '题库块未找到'
s = s[:m2.start()] + '<script>' + crlf + dict_js + crlf + '</script>' + s[m2.end():]

open(F, 'wb').write(s.encode('utf-8'))
print('构建完成')
print('anno:', s.count('class="anno-word"'), '| verse卡:', s.count('<div class="verse" id='), '| part-head:', len(re.findall(r'class="part-head"', s)),
      '| pl:', s.count('class="pl"'), '| acc区:', 'id="acc"' in s, '| kai:', re.search(r'<div class="kai">([^<]*)</div>\s*<div>([^<]*)</div>', s).groups())
