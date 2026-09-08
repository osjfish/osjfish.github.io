# -*- coding: utf-8 -*-
"""修《满江红》v3：kai块 + 注释(卡片v-line+fulltext pl) + 上下阕分层
   逐步断言，避免静默失败"""
import re

F = 'manjianghong-qiujin.html'
raw = open(F, 'rb').read()
s = raw.decode('utf-8')
crlf = '\r\n' if '\r\n' in s else '\n'
assert '中秋佳节' in s

# ---------- 1) kai ----------
old_kai = '秋瑾 · 清（1875—1907）· 淳熙十五年（1188）前后作于带湖'
assert old_kai in s, 'kai未匹配'
s = s.replace(old_kai, '秋瑾 · 清末（1875—1907）· 1903年前后作于北京')

# ---------- 2) 注释 ----------
NOTES = [
    ('小住京华', '短暂寓居北京。京华，北京；1903年秋瑾随夫王廷钧寓居北京'),
    ('中秋佳节', '农历八月十五，团圆之日'),
    ('篱下黄花', '化用陶渊明“采菊东篱下”，指篱笆下的菊花'),
    ('秋容如拭', '秋天的景色明净得如同擦拭过一般。拭，擦'),
    ('四面歌残终破楚', '用项羽垓下被围、四面楚歌的典故，喻八国联军攻破北京、国家危亡'),
    ('八年风味', '1896年秋瑾嫁湘潭王廷钧，居湖南至此已八年'),
    ('徒思浙', '徒然思念浙江家乡。徒，白白地；浙，指秋瑾的故乡浙江'),
    ('苦将侬强派作蛾眉', '硬要把我当作美人看待。苦，执意地；侬，我；强派，硬派；蛾眉，美人的代称，此指闺阁女子身份'),
    ('殊未屑', '很不屑。殊，很、全然；未屑，不值得、不情愿'),
    ('男儿列', '男子的行列'),
    ('男儿烈', '比男儿更刚烈。烈，刚烈、壮烈'),
    ('肝胆', '指真诚的爱国之心'),
    ('因人常热', '常常为他人、为国家而热血沸腾。因，因为'),
    ('俗子胸襟', '平庸俗气之人的胸襟气度'),
    ('英雄末路', '英雄走投无路的境地'),
    ('当磨折', '必然会遭受磨难挫折。磨折，折磨'),
    ('莽红尘', '广大的人世间。莽，广大无边；红尘，人世'),
    ('觅知音', '寻觅知己。知音，用伯牙、子期之典指真正理解自己的人'),
    ('青衫湿', '用白居易《琵琶行》“江州司马青衫湿”之典，为知音难觅而伤心落泪'),
]
NMAP = dict(NOTES)
WORDS = sorted(NMAP.keys(), key=len, reverse=True)
ESCAPE = lambda t: t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def annotate(plain):
    out, i, n = [], 0, 0
    while i < len(plain):
        hit = None
        for w in WORDS:
            if plain.startswith(w, i):
                hit = w
                break
        if hit:
            out.append('<span class="anno-word" data-note="%s">%s</span>' % (NMAP[hit], hit))
            n += 1
            i += len(hit)
        else:
            out.append(ESCAPE(plain[i]))
            i += 1
    return ''.join(out), n

# 8 句原文（硬编码，来自 v-no 提取，已验证）
LINES = [
    '小住京华，早又是中秋佳节。',
    '为篱下黄花开遍，秋容如拭。',
    '四面歌残终破楚，八年风味徒思浙。',
    '苦将侬强派作蛾眉，殊未屑！',
    '身不得，男儿列，心却比，男儿烈。',
    '算平生肝胆，因人常热。',
    '俗子胸襟谁识我？英雄末路当磨折。',
    '莽红尘何处觅知音？青衫湿！',
]
htmls = []
tot = 0
for p in LINES:
    h, n = annotate(p)
    htmls.append(h)
    tot += n
print('8句注释数:', tot)
assert tot >= 18, '注释命中过少'

# ---------- 3) 替换卡片 v-line（按 v-no 分卡，卡内 v-line 精确按句子替换）----------
cnt_vl = 0
for k, line in enumerate(LINES):
    plain_span = re.escape(line)
    pat = re.compile(r'(<div class="v-line">)' + plain_span + r'(</div>)')
    s, c = pat.subn(lambda m, k=k: m.group(1) + htmls[k] + m.group(2), s)
    cnt_vl += c
print('v-line替换:', cnt_vl)
assert cnt_vl == 8

# ---------- 4) fulltext p.pl 替换 ----------
cnt_pl = 0
for k, line in enumerate(LINES):
    pat = re.compile(r'(<p class="pl">)\s*' + re.escape(line) + r'\s*(</p>)')
    s, c = pat.subn(lambda m, k=k: m.group(1) + htmls[k] + m.group(2), s)
    cnt_pl += c
print('fulltext pl替换:', cnt_pl)
assert cnt_pl == 8, 'fulltext pl 替换数异常: %d' % cnt_pl

# ---------- 5) 分层 ----------
o = '<div class="part-head"><span class="p-num">上阕</span><h3>中秋篱下 · 家国之思</h3><span class="range">第 1–4 句</span></div>%s  <div class="part-overview">上阕写中秋佳节的所见所感：篱下菊黄、秋色明净，本是团圆美景，却因国事艰危（四面歌残终破楚）与八年远嫁的苦闷，引出“苦将侬强派作蛾眉”的强烈不满，抒发冲破家庭束缚的决心。</div>' % crlf
d = '<div class="part-head"><span class="p-num">下阕</span><h3>男儿之志 · 知音之叹</h3><span class="range">第 5–8 句</span></div>%s  <div class="part-overview">下阕直抒胸臆：“身不得，男儿列，心却比，男儿烈”以短促的排比写出不让须眉的豪情；“俗子胸襟谁识我”感叹知音难觅，结句“青衫湿”用白居易之典收束，悲愤与孤独交织，把词情推向高潮。</div>' % crlf

vstart = [m.start() for m in re.finditer(r'<div class="verse" id="l\d+"', s)]
assert len(vstart) == 8, 'verse异常:%d' % len(vstart)
s = s[:vstart[4]] + d + s[vstart[4]:]
s = s[:vstart[0]] + o + s[vstart[0]:]

open(F, 'wb').write(s.encode('utf-8'))
final = s.count('class="anno-word"')
print('最终anno处数:', final, '| part-head:', s.count('part-head'))
assert final >= 36
print('OK')
