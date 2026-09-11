# -*- coding: utf-8 -*-
"""
扫描 app(赏析) 区的层级问题：
A. 编号 box（h3 以 一、二、三 开头）缺父级组标题 —— 分点失去归属
B. 同一 app 区内，编号 h3 与非编号 h3 混排且编号组无归属
C. box 内 ≥2 个 p 且段落带并列引导词（首先/其次/在…方面/其一…）却没拆编号 box
D. app 区 box 顺序是否遵循 名句→艺术特色→人物形象 的标杆次序
"""
import os, re, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN = '一二三四五六七八九十'
NUM_RE = re.compile(r'^\s*(?:<[^>]+>)?\s*([' + CN + r'])、')
# 并列引导词
PARA_MARK = re.compile(r'^\s*(首先|其次|再次|再者|最后|此外|另外|其一|其二|其三|其四|一方面|另一方面|一是|二是|三是|第一|第二|第三|在[^，。]{1,8}方面|从[^，。]{1,8}(?:角度|层面|方面)看)')


def app_region(src):
    a = re.search(r'<style[^>]*>(.*?)</style>', src, re.S)
    s = src[a.end():] if a else src
    s = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)
    i = s.find('id="app"')
    if i < 0:
        return None
    j = s.find('id="acc"', i)
    j = j if j > 0 else s.find('id="practice"', i)
    return s[i:j if j > 0 else len(s)]


def boxes(region):
    """返回 [(h3文本, [p文本...])]，只取 box 直系 h3/p"""
    out = []
    for m in re.finditer(r'<div class="box"[^>]*>(.*?)(?=<div class="box"|\Z)', region, re.S):
        body = m.group(1)
        h = re.search(r'<h3[^>]*>(.*?)</h3>', body, re.S)
        if not h:
            continue
        title = re.sub(r'<[^>]+>', '', h.group(1)).strip()
        ps = [re.sub(r'<[^>]+>', '', p).strip()
              for p in re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)]
        out.append((title, ps))
    return out


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
    A, C, D = [], [], []
    for f in files:
        src = open(os.path.join(ROOT, f), encoding='utf-8').read()
        reg = app_region(src)
        if not reg:
            continue
        bs = boxes(reg)
        if not bs:
            continue
        titles = [t for t, _ in bs]
        num_idx = [i for i, t in enumerate(titles) if NUM_RE.match(t)]
        # A：有编号 box，但编号组没有紧邻的父级标题（前一个是普通标题且不是"艺术特色"类）
        if num_idx:
            first = num_idx[0]
            prev = titles[first - 1] if first > 0 else None
            # 父级归属判定：编号组前一个 box 标题应是"艺术特色/…"且紧邻；或编号 h3 自带组名（如"艺术特色之一"）
            has_parent = prev and prev in ('艺术特色', '艺术手法', '艺术成就', '写作特色', '表现手法')
            self_named = all(re.search(r'(特色|手法|结构|语言|艺术|描写|层次|脉络)', t) for t in
                             [titles[i] for i in num_idx])
            if not has_parent and not self_named:
                A.append((f, len(num_idx), prev, titles[max(0, first - 1):first + 2]))
        # C：非编号 box 内多段并列引导词
        for t, ps in bs:
            if NUM_RE.match(t) or len(ps) < 2:
                continue
            hits = [p[:14] for p in ps if PARA_MARK.match(p)]
            if len(hits) >= 2:
                C.append((f, t, hits))
        # D：order
        kinds = []
        for t in titles:
            if '名句' in t:
                kinds.append('名句')
            elif NUM_RE.match(t):
                kinds.append('编号')
            elif '形象' in t:
                kinds.append('形象')
            else:
                kinds.append('其他')
        if '编号' in kinds:
            pos_num = kinds.index('编号')
            if '形象' in kinds and kinds.index('形象') < pos_num:
                D.append((f, kinds))
    lines = []
    P = lines.append
    P('=== A. 编号 box 缺父级组标题（%d 篇）===' % len(A))
    for f, n, prev, ctx in A:
        P('  %-52s 编号%d个 前一项=%r' % (f, n, prev))
    P('')
    P('=== C. box 内多段「第一/第二/第三…」却未拆编号（%d 处）===' % len(C))
    for f, t, hits in C:
        P('  %-52s h3=%r  %s' % (f, t, ' / '.join(hits)))
    P('')
    P('=== D. 编号块排在人物形象之后（与琵琶行「名句→编号→形象」次序相反，%d 篇）===' % len(D))
    for f, kinds in D:
        P('  %-52s %s' % (f, '>'.join(kinds)))
    P('')
    P('=== 编号组前一项标题分布 ===')
    for k, v in collections.Counter(x[2] for x in A).most_common(20):
        P('  %-20s %d' % (k, v))
    txt = '\n'.join(lines)
    open(os.path.join(ROOT, 'tools', '_scan_out.txt'), 'w', encoding='utf-8').write(txt)
    print('ok')
    json.dump({'A': A, 'C': C, 'D': D},
              open(os.path.join(ROOT, 'tools', '_app_level_scan.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
