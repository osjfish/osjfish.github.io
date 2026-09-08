# -*- coding: utf-8 -*-
"""修《满江红》：kai块改正 + 8卡补注释(双份同步) + 上下阕分层"""
import re

F = 'manjianghong-qiujin.html'
raw = open(F, 'rb').read()
s = raw.decode('utf-8')
crlf = '\r\n' if '\r\n' in s else '\n'

# ---------- 1) kai 块改正 ----------
old_kai = '秋瑾 · 清（1875—1907）· 淳熙十五年（1188）前后作于带湖'
new_kai = '秋瑾 · 清末（1875—1907）· 1903年前后作于北京'
assert old_kai in s, 'kai未匹配'
s = s.replace(old_kai, new_kai)

# ---------- 2) 注释表（词 → 释义）----------
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
    out, i = [], 0
    while i < len(plain):
        hit = None
        for w in WORDS:
            if plain.startswith(w, i):
                hit = w
                break
        if hit:
            out.append('<span class="anno-word" data-note="%s">%s</span>' % (NMAP[hit], hit))
            i += len(hit)
        else:
            out.append(ESCAPE(plain[i]))
            i += 1
    return ''.join(out)

mj = re.search(r'<section[^>]*id="jielu"[^>]*>', s)
ma = re.search(r'<section[^>]*id="app"[^>]*>', s)
j = s[mj.end():ma.start()]

# 每卡的 v-line 与 pl 文本
plains, htmls = [], []
for m in re.finditer(r'<span class="v-no">(\d+)</span>', j):
    seg = j[m.end():m.end() + 1500]
    vl = re.search(r'<div class="v-line"[^>]*>(.*?)</div>', seg, re.S)
    plains.append(re.sub(r'<[^>]+>', '', vl.group(1)).strip())
    htmls.append(annotate(plains[-1]))
print('卡片数:', len(plains))

# 替换 v-line（逐卡定位）：重建 jielu 内全部 v-line 与 pl
# v-line: 与 v-no 同卡；pl: 文本与卡相同
new_j = j
idx = 0

def repl_vl(m):
    global idx
    html = htmls[idx]
    idx += 1
    return m.group(1) + html + '</div>'

new_j = re.sub(r'(<div class="v-line"[^>]*>)(.*?)</div>', repl_vl, new_j, flags=re.S)
print('v-line替换:', idx)

pi = 0

def repl_pl(m):
    global pi
    plain = re.sub(r'<[^>]+>', '', m.group(2))
    # 找到内容匹配的卡
    for k in range(len(plains)):
        if plain.strip() == plains[k].strip():
            pi += 1
            return m.group(1) + htmls[k] + '</div>'
    return m.group(0)

new_j = re.sub(r'(<div class="pl"[^>]*>)(.*?)</div>', repl_pl, new_j, flags=re.S)
print('pl替换:', pi)

# ---------- 3) 上下阕分层 ----------
parts = []
o = '<div class="part-head"><span class="p-num">上阕</span><h3>中秋篱下 · 家国之思</h3><span class="range">第 1–4 句</span></div>%s  <div class="part-overview">上阕写中秋佳节的所见所感：篱下菊黄、秋色明净，本是团圆美景，却因国事艰危（四面歌残终破楚）与八年远嫁的苦闷，引出“苦将侬强派作蛾眉”的强烈不满，抒发冲破家庭束缚的决心。</div>' % crlf
d = '<div class="part-head"><span class="p-num">下阕</span><h3>男儿之志 · 知音之叹</h3><span class="range">第 5–8 句</span></div>%s  <div class="part-overview">下阕直抒胸臆：“身不得，男儿列，心却比，男儿烈”以短促的自问自答写出不让须眉的豪情；“俗子胸襟谁识我”感叹知音难觅，结句“青衫湿”用白居易之典收束，悲愤与孤独交织，把词情推向高潮。</div>' % crlf

# 在 verseList 内第一个卡片(第一个 v-no 卡的 verse div)前插上阕；第5卡前插下阕
# 找 verse div 起点
vstart = [m.start() for m in re.finditer(r'<div class="verse" id="p\d+"', new_j)]
print('verse起点:', len(vstart))
assert len(vstart) == 8
# 从后往前插
new_j = new_j[:vstart[4]] + d + new_j[vstart[4]:]
new_j = new_j[:vstart[0]] + o + new_j[vstart[0]:]

s2 = s[:mj.end()] + new_j + s[ma.start():]
open(F, 'wb').write(s2.encode('utf-8'))

tot = len(re.findall(r'class="anno-word"', new_j))
print('注释处数:', tot, '| 词数:', len(NMAP), '| part数:', len(re.findall(r'part-head', new_j)))
