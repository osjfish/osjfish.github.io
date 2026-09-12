# -*- coding: utf-8 -*-
"""
按 _audit_all.py 的发现批量修复：
A) fulltext 行 <p class="pl"> → <div class="pl">（SKILL §5.3 铁律）
B) 移除内联 onclick（JS 已绑定时冗余）
C) 补齐未闭合标签 / 删除孤闭合 —— 采用「与浏览器自动纠错一致」的策略，
   即在不匹配的闭合标签前插入缺失的 </x>，删除无匹配的 </x>；
   这样修复后的 DOM 与修复前浏览器渲染出的 DOM 完全一致，零视觉变化。
用法：python _fix_audit_issues.py --apply
"""
import os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}

VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'source', 'area', 'base',
        'col', 'embed', 'param', 'track', 'wbr'}
SCRIPT_STYLE_RE = re.compile(r'<(script|style)\b[^>]*>.*?</\1>', re.S | re.I)
TAG_RE = re.compile(r'<(/?)([a-zA-Z][\w-]*)\b([^>]*)>')


def _opaque(src):
    return [(m.start(), m.end()) for m in SCRIPT_STYLE_RE.finditer(src)]


def _in(pos, ranges):
    return any(a <= pos < b for a, b in ranges)


def repair_tags(src):
    """返回修复后的源码与统计。"""
    ranges = _opaque(src)
    edits = []
    stack = []
    stat = collections.Counter()
    for m in TAG_RE.finditer(src):
        if _in(m.start(), ranges):
            continue
        close, tag, rest = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or rest.rstrip().endswith('/'):
            continue
        if not close:
            stack.append(tag)
        else:
            if stack and stack[-1] == tag:
                stack.pop()
                continue
            idx = None
            for i in range(len(stack) - 1, -1, -1):
                if stack[i] == tag:
                    idx = i
                    break
            if idx is None:
                edits.append(('del', m.start(), m.end(), ''))
                stat['孤闭合删除'] += 1
            else:
                missing = ''.join('</%s>' % stack[j] for j in range(len(stack) - 1, idx, -1))
                edits.append(('ins', m.start(), m.start(), missing))
                stat['补齐闭合'] += len(stack) - 1 - idx
                del stack[idx:]
    if not edits:
        return src, stat
    for kind, a, b, text in sorted(edits, key=lambda e: (e[1], e[0]), reverse=True):
        if kind == 'del':
            src = src[:a] + src[b:]
        else:
            src = src[:a] + text + src[a:]
    return src, stat


def fix_fulltext_p(src):
    """fulltext 区块内 <p class="pl"> → <div class="pl">"""
    i = src.find('id="fulltext"')
    if i < 0:
        return src, 0
    gt = src.find('>', i)
    if gt < 0:
        return src, 0
    div_re = re.compile(r'<(/?)div\b')
    depth, end = 0, None
    for mm in div_re.finditer(src, gt + 1):
        if mm.group(1):
            if depth == 0:
                end = mm.start()
                break
            depth -= 1
        else:
            depth += 1
    if end is None:
        return src, 0
    seg = src[gt + 1:end]
    n = seg.count('<p class="pl">')
    if not n:
        return src, 0
    if seg.count('</p>') != n:
        return src, 0  # 结构不符预期，跳过以免误改
    new = seg.replace('<p class="pl">', '<div class="pl">').replace('</p>', '</div>')
    return src[:gt + 1] + new + src[end:], n


def fix_inline_onclick(src):
    """仅删除 JS 已绑定的冗余 onclick（topBtn 的 scrollTo）"""
    pat = re.compile(r'(\sid="topBtn"[^>]*?)\s+onclick="window\.scrollTo\([^"]*\)"')
    new, n = pat.subn(r'\1', src)
    if n:
        return new, n
    pat2 = re.compile(r'\sonclick="window\.scrollTo\([^"]*\)"')
    return pat2.subn('', src)[0], pat2.subn('', src)[1]


def main(apply=False):
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    total = collections.Counter()
    touched = []
    for fn in files:
        p = os.path.join(ROOT, fn)
        src = open(p, encoding='utf-8').read()
        orig = src
        src, n1 = fix_fulltext_p(src)
        src, n2 = fix_inline_onclick(src)
        src, st = repair_tags(src)
        if src != orig:
            touched.append(fn)
            total['fulltext_p→div'] += n1
            total['去内联onclick'] += n2
            total.update(st)
            if apply:
                open(p, 'w', encoding='utf-8').write(src)
    print('待改文件:', len(touched))
    for k, v in total.items():
        print('  %s: %d' % (k, v))
    if not apply:
        print('（dry-run，未写盘；加 --apply 生效）')


if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
