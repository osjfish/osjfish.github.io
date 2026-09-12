# -*- coding: utf-8 -*-
"""
精确结构体检：先把 <script>...</script> 与 HTML 注释剔除，再统计标签平衡，
避免 JS 里的 '<div ...>' 字符串造成误报。
"""
import os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}

SCRIPT_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.S | re.I)
COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
TAG_RE = re.compile(r'<(/?)([a-zA-Z][\w-]*)\b[^>]*?(/?)>', re.S)
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'source', 'area', 'base',
        'col', 'embed', 'param', 'track', 'wbr'}


def balance(html):
    """返回 (stack剩余未闭合, 错误列表)"""
    stack, errs = [], []
    for m in re.finditer(r'<(/?)([a-zA-Z][\w-]*)\b([^>]*)>', html):
        close, tag, rest = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or rest.rstrip().endswith('/'):
            continue
        if tag in ('script', 'style'):
            continue
        if not close:
            stack.append((tag, m.start()))
        else:
            if not stack:
                errs.append('多余闭合 </%s>' % tag)
                continue
            if stack[-1][0] == tag:
                stack.pop()
            else:
                # 找最近的同类
                found = None
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][0] == tag:
                        found = i
                        break
                if found is None:
                    errs.append('孤闭合 </%s>' % tag)
                else:
                    errs.append('错配 </%s> 期望 </%s>' % (tag, stack[-1][0]))
                    del stack[found:]
    return stack, errs


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    bad = []
    for fn in files:
        src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
        clean = SCRIPT_RE.sub('', src)
        clean = COMMENT_RE.sub('', clean)
        stack, errs = balance(clean)
        if stack or errs:
            bad.append((fn, [t for t, _ in stack][:8], errs[:4]))
    print('体检文件:', len(files), '| 结构异常:', len(bad))
    for fn, st, errs in bad[:40]:
        print('\n-', fn)
        if st:
            print('    未闭合:', ','.join(st))
        if errs:
            print('    错误:', ' | '.join(errs))


if __name__ == '__main__':
    main()
