# -*- coding: utf-8 -*-
"""统一页面 <title> 为《作品名》作者。只改 <title>，不碰其他内容。"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 文件 -> (作品名或None=用现title清洗, 作者或None=自动)
OVERRIDE = {
    'guanju-shijing.html': (None, '诗经'),
    'jianjia-shijing.html': (None, '诗经'),
    'lunyushierzhang-lunyu.html': (None, '论语'),
    'tangjiburushiming-zhanguoce.html': (None, '战国策'),
    'suiyoujiayao-liji.html': (None, '礼记'),
    'jiarushenghuoqipianleni-puxijin.html': (None, '普希金'),
    'weixuanzedelu-fuluosite.html': (None, '弗罗斯特'),
    'manjianghongxiaozhujinghua-qiujin.html': ('满江红·小住京华', '秋瑾'),
    'yujiaao-liqingzhao.html': ('渔家傲·天接云涛连晓雾', '李清照'),
    'haiyan-gaoerji.html': (None, '高尔基'),
    'tongyi-nieluda.html': (None, '聂鲁达'),
}

def fix_author_dup(s):
    if len(s) >= 4 and s[:len(s)//2] == s[len(s)//2:]:
        return s[:len(s)//2]
    return s

def parse_old(title):
    """返回 (作品名, 已知作者或None)"""
    t = title.strip()
    m = re.fullmatch(r'《([^》]+)》《([^》]+)》', t)
    if m:
        return m.group(1), m.group(2)  # 《关雎》《诗经》
    m = re.fullmatch(r'《([^》]+)》', t)
    if m:
        return m.group(1), None
    m = re.fullmatch(r'[“"]([^”"]+)[”"]', t)
    if m:
        return m.group(1), None
    m = re.fullmatch(r'(.+?)\s*[·]\s*(.+)', t)
    if m:
        return m.group(1), m.group(2)
    m = re.fullmatch(r'(.+)\s+( [\u4e00-\u9fa5A-Za-z·]{2,12})', t)
    if m:
        return m.group(1), m.group(2).strip()
    m = re.fullmatch(r'(.+)\s+([^\s]{2,12})', t)
    if m:
        return m.group(1), m.group(2)
    return t, None

changed = []
import glob
for p in sorted(glob.glob('*.html')):
    t = open(p, encoding='utf-8').read()
    m = re.search(r'<title>(.*?)</title>', t)
    if not m:
        continue
    old = m.group(1).strip()
    if re.fullmatch(r'《[^》]+》[^《》]+', old):
        continue  # 已合规
    w, a = parse_old(old)
    # 页面提取作者兜底
    if a is None:
        am = re.search(r'作者简介</h3>(.{0,300})', t, re.S)
        if am:
            seg = re.sub(r'<[^>]+>', '', am.group(1))
            cm = re.match(r'\s*([\u4e00-\u9fa5·]{2,8})\s*[（(，,]', seg)
            if cm:
                a = fix_author_dup(cm.group(1))
    if p in OVERRIDE:
        ow, oa = OVERRIDE[p]
        w = ow or w
        a = oa or a
    if a:
        a = fix_author_dup(a)
    assert w and a, f'{p}: 作品={w} 作者={a}'
    new_title = f'《{w}》{a}'
    if new_title != old:
        t = t[:m.start(1)] + new_title + t[m.end(1):]
        open(p, 'w', encoding='utf-8').write(t)
        changed.append(f'{p}: {old} -> {new_title}')
print('\n'.join(changed))
print(f'\n共修改 {len(changed)} 个')
