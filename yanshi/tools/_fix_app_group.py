# -*- coding: utf-8 -*-
"""
给赏析区「一、二、三、四」分点 box 补回归属组标题（.app-group）。
组名来源：0faf483^ 旧版被删掉的 h3（已恢复在 _group_titles.json）。
归属判定：新版编号 h3 去掉编号后，与旧版各组 box 内的 f-line / 分点标题做文本匹配。
特例：编号块去编号后为「主题思想/主旨/中心思想」等 → 去编号并移出编号组。
"""
import os, re, io, sys, json, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\App\Apps\yanshi'
OLD = r'D:\App\Apps\yanshi\tools\_oldapp\yanshi'
CN = '一二三四五六七八九十'
NUM_RE = re.compile(r'^\s*(?:<[^>]+>)?\s*([' + CN + r'])、')
# 不该归属到「艺术特色」组的编号块（去编号后命中即移出）
THEME = re.compile(r'^(主题思想|主旨|中心思想|主题|思想主旨|中心论点)$')


def region(src):
    a = re.search(r'<style[^>]*>(.*?)</style>', src, re.S)
    s = src[a.end():] if a else src
    s = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)
    i = s.find('id="app"')
    if i < 0:
        return None, 0, 0
    j = s.find('id="acc"', i)
    j = j if j > 0 else len(s)
    return s[i:j], i + (a.end() if a else 0), j + (a.end() if a else 0)


def clean(t):
    return re.sub(r'<[^>]+>', '', t).strip()


def old_groups(src):
    """旧版：{组标题: [分点标题...]}，只取含 fame-card 或分点的具名 box"""
    reg, _, _ = region(src)
    if not reg:
        return {}
    out = collections.OrderedDict()
    for m in re.finditer(r'<div class="box"[^>]*>(.*?)(?=<div class="box"|\Z)', reg, re.S):
        body = m.group(1)
        h = re.search(r'<h3[^>]*>(.*?)</h3>', body, re.S)
        if not h:
            continue
        t = clean(h.group(1))
        if NUM_RE.match(t):
            continue
        pts = [clean(x) for x in re.findall(r'<div class="f-line"[^>]*>(.*?)</div>', body, re.S)]
        if not pts:
            pts = [clean(x) for x in re.findall(r'<b[^>]*>(.*?)</b>', body, re.S)]
        out[t] = pts
    return out


def norm_key(s):
    return re.sub(r'[\s，。、：:；;（）()《》“”"\'·—\-]', '', s)


def main(apply=True):
    gt = json.load(open(os.path.join(ROOT, 'tools', '_group_titles.json'), encoding='utf-8'))
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
    stat = collections.Counter()
    report = []
    for f in files:
        p = os.path.join(ROOT, f)
        src = open(p, encoding='utf-8').read()
        reg, off, _ = region(src)
        if not reg:
            continue
        boxes = list(re.finditer(r'<div class="box"[^>]*>(?=.*?<h3)', reg, re.S))
        # 收集 (start_in_region, title, is_num)
        info = []
        for m in re.finditer(r'<div class="box"[^>]*>(.*?)(?=<div class="box"|\Z)', reg, re.S):
            h = re.search(r'<h3[^>]*>(.*?)</h3>', m.group(1), re.S)
            if not h:
                continue
            t = clean(h.group(1))
            mm = NUM_RE.match(t)
            info.append({'start': m.start(), 'end': m.end(), 'title': t,
                         'num': bool(mm), 'body': NUM_RE.sub('', t) if mm else t})
        if not any(x['num'] for x in info):
            continue
        # 组名候选
        op = os.path.join(OLD, f)
        groups = old_groups(open(op, encoding='utf-8', errors='replace').read()) if os.path.exists(op) else {}
        names = gt.get(f)
        if not names:
            names = ['艺术特色']
        # 判定每个编号块归属：
        # 1) 主题思想类不归组（去编号、移出）
        # 2) 编号序号回退（如 三 → 一）即视为新一组开始
        # 3) 组名按 _group_titles.json 的顺序取（旧版出现顺序）
        seq = {c: i + 1 for i, c in enumerate(CN)}
        last = 0
        gi = 0
        for x in info:
            if not x['num']:
                last = 0
                continue
            if THEME.match(x['body']):
                x['grp'] = None
                last = 0
                continue
            mm = NUM_RE.match(x['title'])
            cur = seq.get(mm.group(1), 0) if mm else 0
            if cur <= last:          # 编号回退 → 新组
                gi += 1
            last = cur
            x['grp'] = names[gi] if gi < len(names) else names[-1]
        # 生成插入点
        inserts = []   # (region_pos, html)
        prev = None
        for x in info:
            if x['num'] and x.get('grp') and x['grp'] != prev:
                inserts.append((x['start'], '  <div class="app-group">%s</div>\n' % x['grp'], x['grp']))
            if x['num']:
                prev = x.get('grp')
            elif THEME.match(x['body']):
                prev = None
        if not inserts:
            stat['skip'] += 1
            continue
        # 改写：插入组标题 + 主题思想类编号块去编号
        new = reg
        for pos, html, _g in sorted(inserts, reverse=True):
            new = new[:pos] + html + new[pos:]
        # 主题思想编号块去编号（h3 文本层）
        def de_num(m):
            t = clean(m.group(2))
            if NUM_RE.match(t) and THEME.match(NUM_RE.sub('', t)):
                return m.group(1) + NUM_RE.sub('', t) + m.group(3)
            return m.group(0)
        new = re.sub(r'(<h3[^>]*>)(.*?)(</h3>)', de_num, new, flags=re.S)
        if new != reg:
            out = src[:off] + new + src[off + len(reg):]
            if apply:
                open(p, 'w', encoding='utf-8').write(out)
            stat['patched'] += 1
            report.append((f, [x[2] for x in inserts], [x['title'] for x in info]))
    print('修补篇数', stat['patched'], '跳过', stat['skip'])
    L = []
    for f, gs, ts in report:
        L.append('%-50s 组=%s' % (f, gs))
    L.append('')
    L.append('=== 多组篇复核（应含 4 篇双组）===')
    for f, gs, ts in report:
        if len(gs) > 1:
            L.append('%-50s 组=%s  标题=%s' % (f, gs, ts))
    L.append('')
    L.append('=== 未插入组标题但存在编号块的篇 ===')
    L.append('（空即全部覆盖）')
    open(os.path.join(ROOT, 'tools', '_fix_group_out.txt'), 'w', encoding='utf-8').write('\n'.join(L))


if __name__ == '__main__':
    main('--apply' in sys.argv)
