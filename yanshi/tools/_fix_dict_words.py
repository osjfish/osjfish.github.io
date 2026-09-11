# -*- coding: utf-8 -*-
"""修复 DICT_WORDS：叠词整体作答（□数=字数/音节=字数）、去泄题、去重。
按 SKILL §4.2：AABB 叠词与双字连绵词必须整体作答；不符合的绝不硬凑。
"""
import os, re, io, sys, json

ROOT = r'D:\App\Apps\yanshi'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PAIR = re.compile(r"(\w+):\s*'([^']*)'")

# (文件, 原w, 原q) -> (新w, 新py, 新q, 新tip)   tip 为 None 表示沿用原 tip
MOD = {
 ('changhenge-baijuyi.html','绵','此恨□绵无绝期'):('绵绵','mián mián','此恨□□无绝期','「绵绵」纟旁，音 mián mián，连绵不断'),
 ('changhenge-baijuyi.html','茫','两处□茫皆不见'):('茫茫','máng máng','两处□□皆不见','「茫茫」艹头，音 máng máng，辽远无边'),
 ('guxiang-luxun.html','絮','一面愤愤的回转身，一面□絮的说'):('絮絮','xù xù','一面愤愤的回转身，一面□□的说','「絮絮」下部是「糸」，音 xù xù，形容说话啰嗦；与「恕」（心字底）区分'),
 ('pipaxing-baijuyi.html','嘈','大弦□嘈如急雨'):('嘈嘈','cáo cáo','大弦□□如急雨','「嘈嘈」口字旁，音 cáo cáo，拟声，形容弦声粗重'),
 ('pipaxing-baijuyi.html','切','小弦□切如私语'):('切切','qiè qiè','小弦□□如私语','「切切」此处读 qiè qiè，形容声音轻细急促'),
 ('pipaxing-baijuyi.html','铮','□铮然有京都声'):('铮铮','zhēng zhēng','□□然有京都声','「铮铮」金字旁，音 zhēng zhēng，拟声，金属清脆声'),
 ('pipaxing-baijuyi.html','唧','又闻此语重□唧'):('唧唧','jī jī','又闻此语重□□','「唧唧」口字旁，音 jī jī，叹息声'),
 ('pipaxing-baijuyi.html','瑟','枫叶荻花秋□瑟'):('瑟瑟','sè sè','枫叶荻花秋□□','「瑟瑟」王字旁，音 sè sè，拟声，秋风吹动声'),
 ('pipaxing-baijuyi.html','茫','别时□茫江浸月'):('茫茫','máng máng','别时□□江浸月','「茫茫」艹头，音 máng máng，形容江水辽阔无边'),
 ('pipaxing-baijuyi.html','续','低眉信手续□弹'):('续续','xù xù','低眉信手□□弹','「续续」纟旁，音 xù xù，连续不断'),
 ('shexi-luxun.html','篙','双喜拔前□，阿发拔后篙'):('篙','gāo','双喜拔前□',None),
 ('shexi-luxun.html','潺','夹着□□的船头激水的声音'):('潺潺','chán chán','夹着□□的船头激水的声音','「潺潺」氵旁+孱，音 chán chán，流水声'),
 ('tengyexiansheng-luxun.html','菌','细菌的形状是全用电影来显示的'):('菌','jūn','细□的形状是全用电影来显示的',None),
 ('tengyexiansheng-luxun.html','颤','冬天是一件旧外套，寒□□的'):('颤颤','zhàn zhàn','冬天是一件旧外套，寒□□的','「颤颤」页字旁，发抖义；「寒颤」中读 zhàn，不读 chàn'),
 ('beiying-zhuziqing.html','簌','又想起祖母，不禁□□地流下眼泪'):('簌簌','sù sù','又想起祖母，不禁□□地流下眼泪','「簌簌」竹字头，音 sù sù，形容流泪声；与「嗽」（咳嗽，口字旁）区分'),
 ('laowang-yangjiang.html','僵','那直□□的身体好像不能坐'):('僵僵','jiāng jiāng','那直□□的身体好像不能坐','「僵僵」亻旁+畺，音 jiāng jiāng，僵直；与「疆」（弓字旁）区分'),
}
DEL = {  # 句中同字重复、无法合规的条目（§4.2：不符合的绝不硬凑）
 ('shexi-luxun.html','踱','那老旦当初还只是□来踱去的唱'),
}
DEDUP = [  # 重复条目，保留首次出现
 ('congbaicaoyuandaosanweishuwu-luxun.html','臃','何首乌有□肿的根'),
 ('guduzhilv-caowenxuan.html','朦朦胧胧','除了□□□□的树烟，就什么也没有了'),
 ('guduzhilv-caowenxuan.html','浩浩荡荡','再面对这□□□□的芦苇'),
 ('guduzhilv-caowenxuan.html','重重叠叠','一样的芦苇，一样□□□□无边无际'),
 ('liusuo-acheng.html','兢兢','我战战□□跨过去，近了，才看清那索'),
 ('liusuo-acheng.html','吱吱','那索在他们身下□□地响'),
 ('liusuo-acheng.html','哞哞','那牛□□地叫，四条腿蹬着地'),
 ('zhongguoshigongqiao-maoyisheng.html','肖','千态万状，惟妙惟□'),
]


def parse(raw):
    if '"w"' in raw:
        try:
            return json.loads(raw), 'json'
        except Exception:
            return json.loads(re.sub(r',\s*\]', ']', raw)), 'json'
    items = []
    for line in raw.splitlines():
        s = line.strip().rstrip(',')
        if s.startswith('{'):
            d = dict(PAIR.findall(s))
            if 'w' in d:
                items.append(d)
    return items, 'sq'


def dump(items, fmt, indent='    ', close='  '):
    if fmt == 'json':
        return json.dumps(items, ensure_ascii=False)
    lines = ['[']
    for it in items:
        lines.append("%s{w:'%s', py:'%s', q:'%s', tip:'%s'}," %
                     (indent, it['w'], it['py'], it['q'], it['tip']))
    lines.append(close + ']')
    return '\n'.join(lines)


changed = []
for fn in sorted(os.listdir(ROOT)):
    if not fn.endswith('.html'):
        continue
    p = os.path.join(ROOT, fn)
    src = open(p, encoding='utf-8').read()
    m = re.search(r'(var\s+DICT_WORDS\s*=\s*)(\[.*?\])(\s*;)', src, re.S)
    if not m:
        continue
    items, fmt = parse(m.group(2))
    if not items:
        continue
    # 原缩进（sq 形态）
    first = [l for l in m.group(2).splitlines() if l.strip().startswith('{')]
    indent = re.match(r'\s*', first[0]).group(0) if first else '    '
    closem = re.search(r'\n(\s*)\]\s*$', m.group(2))
    close = closem.group(1) if closem else '  '
    out, seen, nmod, ndel, nded = [], set(), 0, 0, 0
    for it in items:
        key = (fn, it.get('w'), it.get('q'))
        if key in DEL:
            ndel += 1
            continue
        if key in MOD:
            nw, npy, nq, ntip = MOD[key]
            it = dict(it)
            it['w'], it['py'], it['q'] = nw, npy, nq
            if ntip is not None:
                it['tip'] = ntip
            nmod += 1
        k2 = (it.get('w'), it.get('q'))
        if k2 in seen and k2 in [(d[1], d[2]) for d in DEDUP if d[0] == fn]:
            nded += 1
            continue
        seen.add(k2)
        out.append(it)
    if nmod or ndel or nded:
        new = m.group(1) + dump(out, fmt, indent, close) + m.group(3)
        src = src[:m.start()] + new + src[m.end():]
        open(p, 'w', encoding='utf-8').write(src)
        changed.append((fn, nmod, ndel, nded))

print('修改文件数:', len(changed))
for c in changed:
    print('   %-42s 改=%d 删=%d 去重=%d' % c)
