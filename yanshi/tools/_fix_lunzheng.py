# -*- coding: utf-8 -*-
"""
把「论证思路 / 论证结构 / 对话结构」box 内已成型的分点
（「第一部分（第1段），摆靶子。…」）拆成 app-group + 编号 box，
与「艺术特色」的一、二、三、四 形态统一。
标题规则：优先用括号后的短句（≤12字），否则用括号内容本身。
"""
import os, re, io, sys, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = r'D:\App\Apps\yanshi'
CN = '一二三四五六七八九十'
GROUP_TITLES = ('论证思路', '论证结构', '对话结构', '论证方法', '论证过程', '逻辑推理过程')

PREFIX = re.compile(r'^(第[一二三四五六七八九十]+(?:部分|层|步|间小屋))[（(]([^）)]+)[）)][，,：:]?\s*(.*)$', re.S)
PREFIX2 = re.compile(r'^(第[一二三四五六七八九十]+间小屋)([^。！？]{0,20})[。！？]\s*(.*)$', re.S)
FIRST = re.compile(r'^([^。！？；]{2,12})[。！？](.*)$', re.S)


def app_span(src):
    a = re.search(r'<style[^>]*>(.*?)</style>', src, re.S).end()
    i = src.find('id="app"', a)
    j = src.find('id="acc"', i)
    return i, (j if j > 0 else len(src))


def main(apply=True):
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
    stat = collections.Counter()
    rep = []
    for f in files:
        p = os.path.join(ROOT, f)
        src = open(p, encoding='utf-8').read()
        i0, j0 = app_span(src)
        reg = src[i0:j0]
        # 找目标 box
        for m in re.finditer(r'<div class="box"[^>]*>(.*?)(?=<div class="box"|\Z)', reg, re.S):
            body = m.group(1)
            h = re.search(r'<h3[^>]*>(.*?)</h3>', body, re.S)
            if not h:
                continue
            title = re.sub(r'<[^>]+>', '', h.group(1)).strip()
            if not any(title.startswith(g) for g in GROUP_TITLES):
                continue
            ps = list(re.finditer(r'<p[^>]*>(.*?)</p>', body, re.S))
            if len(ps) < 2:
                continue
            intro, pts = [], []
            for pm in ps:
                txt = re.sub(r'<[^>]+>', '', pm.group(1)).strip()
                raw = pm.group(0)
                mm = PREFIX.match(txt)
                if mm:
                    grp, bracket, rest = mm.groups()
                    fm = FIRST.match(rest)
                    if fm and len(fm.group(1)) <= 12:
                        t, b = fm.group(1), fm.group(2)
                    else:
                        t, b = bracket, rest
                    pts.append(('（%s）' % bracket, t, b, raw))
                    continue
                mm = PREFIX2.match(txt)
                if mm:
                    pts.append(('', mm.group(2), mm.group(3), raw))
                    continue
                intro.append(raw)
            if len(pts) < 2:
                stat['skip'] += 1
                rep.append(('SKIP', f, title, len(pts)))
                continue
            # 生成新结构
            blocks = ['  <div class="app-group">%s</div>' % title]
            for n, (br, t, b, raw) in enumerate(pts):
                head = '%s、%s' % (CN[n], t)
                if br and bracket not in t:
                    head += br
                inner = '<h3>%s</h3>\n    <p>%s</p>' % (head, b)
                if n == 0 and intro:
                    inner = '\n    '.join(intro) + '\n    ' + inner
                blocks.append('  <div class="box">\n    %s\n  </div>' % inner)
            new = '\n'.join(blocks)
            out = src[:i0] + reg[:m.start()] + new + reg[m.end():] + src[j0:]
            if apply:
                open(p, 'w', encoding='utf-8').write(out)
            stat['patched'] += 1
            rep.append(('OK', f, title, [(CN[n] + '、' + t) for n, (br, t, b, r) in enumerate(pts)]))
            break   # 每篇只处理一个论证类 box
    print('修补', stat['patched'], '跳过', stat['skip'])
    L = []
    for r in rep:
        L.append('%-6s %-50s %s' % (r[0], r[1], r[2]))
        if r[0] == 'OK':
            L.append('        新增: %s' % r[3])
        else:
            L.append('        仅 %s 个可识别分点，未拆' % r[2])
    open(os.path.join(ROOT, 'tools', '_fix_lunzheng_out.txt'), 'w', encoding='utf-8').write('\n'.join(L))


if __name__ == '__main__':
    main('--apply' in sys.argv)
