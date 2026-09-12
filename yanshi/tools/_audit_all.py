# -*- coding: utf-8 -*-
"""
全库课件综合审计（静态）。只读，不改文件。
要点：先剔除 <style>/<script>/注释 再统计，避免把 CSS/JS 里的文本当标签。
用法：python _audit_all.py
"""
import os, re, collections
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}  # React 交互课件例外

SCRIPT_RE = re.compile(r'<script\b[^>]*>.*?</script>', re.S | re.I)
STYLE_RE = re.compile(r'<style\b[^>]*>.*?</style>', re.S | re.I)
COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
VOID = {'br', 'hr', 'img', 'input', 'meta', 'link', 'source', 'area', 'base',
        'col', 'embed', 'param', 'track', 'wbr'}
SECTION_IDS = ['bg', 'jielu', 'app', 'acc', 'practice']


def strip_noise(src):
    return COMMENT_RE.sub('', STYLE_RE.sub('', SCRIPT_RE.sub('', src)))


def balance(clean):
    """栈式标签平衡，返回 (未闭合栈, 错误列表)"""
    stack, errs = [], []
    for m in re.finditer(r'<(/?)([a-zA-Z][\w-]*)\b([^>]*)>', clean):
        close, tag, rest = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID or rest.rstrip().endswith('/'):
            continue
        if not close:
            stack.append(tag)
        else:
            if not stack:
                errs.append('多余闭合 </%s>' % tag)
                continue
            if stack[-1] == tag:
                stack.pop()
            else:
                found = None
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i] == tag:
                        found = i
                        break
                if found is None:
                    errs.append('孤闭合 </%s>' % tag)
                else:
                    errs.append('错配 </%s> 期望 </%s>' % (tag, stack[-1]))
                    del stack[found:]
    return stack, errs


class FulltextParser(HTMLParser):
    """找出 id=fulltext 元素的直接子标签"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.in_ft = False
        self.ft_depth = 0
        self.kids = []
        self.found = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if not self.in_ft and d.get('id') == 'fulltext':
            self.in_ft = True
            self.ft_depth = 0
            self.found = True
            return
        if self.in_ft:
            if self.ft_depth == 0:
                self.kids.append((tag, d.get('class', '')))
            self.ft_depth += 1

    def handle_endtag(self, tag):
        if self.in_ft:
            if self.ft_depth == 0:
                self.in_ft = False
            else:
                self.ft_depth -= 1


def audit_one(path):
    src = open(path, encoding='utf-8').read()
    clean = strip_noise(src)
    cssm = re.search(r'<style\b[^>]*>(.*?)</style>', src, re.S | re.I)
    css = cssm.group(1) if cssm else ''
    f = collections.defaultdict(list)

    # 1) title
    t = re.search(r'<title>(.*?)</title>', src, re.S)
    title = t.group(1).strip() if t else ''
    if not (title.startswith('《') and '》' in title):
        f['title格式'].append(title or '(空)')

    # 2) 正文行内 font-size（canon 禁止）
    n = len(re.findall(r'style="[^"]*font-size[^"]*"', clean))
    if n:
        f['行内font-size'].append(str(n))

    # 3) CSS content 里的 \uXXXX 转义
    if re.search(r'content:[^;}]*\\u[0-9a-fA-F]{4}', css, re.I):
        f['CSS_u转义'].append('有')

    # 4) style 块内出现尖括号标签文本（会污染解析器）
    if '<' in css:
        bad = re.findall(r'</?[a-zA-Z][\w-]*\s*>', css)
        if bad:
            f['style内含标签文本'].append(','.join(bad[:3]))

    # 5) 标签平衡
    stack, errs = balance(clean)
    if stack:
        f['未闭合标签'].append(','.join(stack[:6]) + ('(%d)' % len(stack)))
    if errs:
        f['标签错配'].append(' | '.join(errs[:3]))

    # 6) 六区存在性与顺序
    pos = {}
    for sid in SECTION_IDS:
        m = re.search(r'<section[^>]*\bid="%s"' % sid, src)
        if m:
            pos[sid] = m.start()
    missing = [s for s in SECTION_IDS if s not in pos]
    if missing:
        f['缺区'].append(','.join(missing))
    order = [s for s in SECTION_IDS if s in pos]
    if order != sorted(order, key=lambda s: pos[s]):
        f['区顺序乱'].append('>'.join(order))

    # 7) 重复 id
    ids = re.findall(r'\sid="([^"]+)"', clean)
    dup = [k for k, v in collections.Counter(ids).items() if v > 1]
    if dup:
        f['重复id'].append(','.join(dup[:5]) + ('(%d)' % len(dup)))

    # 8) 视频残留
    if re.search(r'class="fsbtn"', src):
        f['残留fsbtn'].append(str(len(re.findall(r'class="fsbtn"', src))))
    if re.search(r'在\s*B\s*站打开原视频', src):
        f['残留B站外链'].append(str(len(re.findall(r'在\s*B\s*站打开原视频', src))))

    # 9) media-grid 单列
    mg = re.search(r'\.media-grid\{[^}]*\}', css)
    if mg and 'grid-template-columns:1fr' not in mg.group(0):
        f['media-grid非单列'].append(mg.group(0)[:50])

    # 10) fulltext 直接子元素必须是 div.pl，禁裸 p
    p = FulltextParser()
    try:
        p.feed(clean)
    except Exception:
        pass
    if p.found:
        bad_p = [t for t, c in p.kids if t == 'p']
        if bad_p:
            f['fulltext裸p'].append('%d个' % len(bad_p))
        good = [t for t, c in p.kids if t == 'div' and 'pl' in c]
        if not good and not bad_p:
            f['fulltext无pl行'].append('子元素:%s' % [t for t, _ in p.kids][:5])

    # 11) 内联 onclick（历史上致背诵功能死）
    n = len(re.findall(r'\sonclick=', clean))
    if n:
        f['内联onclick'].append(str(n))

    # 12) 空标题
    if re.search(r'<h3>\s*</h3>', src):
        f['空h3'].append(str(len(re.findall(r'<h3>\s*</h3>', src))))
    if re.search(r'class="app-group"[^>]*>\s*</', src):
        f['空app-group'].append('有')

    return f


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    agg = collections.defaultdict(list)
    for fn in files:
        f = audit_one(os.path.join(ROOT, fn))
        for k, v in f.items():
            agg[k].append('%s: %s' % (fn, ';'.join(v)))
    print('审计文件数:', len(files))
    print('=' * 60)
    if not agg:
        print('未发现问题 ✅')
    for k in sorted(agg, key=lambda x: -len(agg[x])):
        print('\n【%s】 %d 篇' % (k, len(agg[k])))
        for line in agg[k][:15]:
            print('   ', line)
        if len(agg[k]) > 15:
            print('    ... 另 %d 篇' % (len(agg[k]) - 15))


if __name__ == '__main__':
    main()
