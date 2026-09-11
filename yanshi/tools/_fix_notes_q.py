# -*- coding: utf-8 -*-
"""修复注释题 q：§4.3 要求"显示所在句（不是章节名）"。
对 q 形如「第X段 · 标题」的条目，从课文原文中找出包含被考词的真实句子替换。
"""
import os, re, io, sys, json

ROOT = r'D:\App\Apps\yanshi'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PAIR = re.compile(r"(\w+):\s*'([^']*)'")

SEC = re.compile(r'^\s*第[一二三四五六七八九十百\d]+段')
TAG = re.compile(r'<[^>]+>')


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
        lines.append("%s{w:'%s', q:'%s', a:'%s'}," % (indent, it['w'], it['q'], it['a']))
    lines.append(close + ']')
    return '\n'.join(lines)


def body_text(src):
    """抽取课文原文（去掉 script/style/标签）"""
    t = re.sub(r'<script[^>]*>.*?</script>', ' ', src, flags=re.S)
    t = re.sub(r'<style[^>]*>.*?</style>', ' ', t, flags=re.S)
    parts = []
    for m in re.finditer(r'<(?:div|p)[^>]*class="[^"]*(?:v-line|pl)[^"]*"[^>]*>(.*?)</(?:div|p)>', t, re.S):
        parts.append(TAG.sub('', m.group(1)))
    if not parts:
        m = re.search(r'id="fulltext"[^>]*>(.*?)</div>', t, re.S)
        if m:
            parts.append(TAG.sub('', m.group(1)))
    txt = ' '.join(parts)
    txt = txt.replace('&nbsp;', ' ').replace('&amp;', '&')
    return re.sub(r'\s+', '', txt)


def sentences(txt):
    ss = re.split(r'(?<=[。！？；])', txt)
    return [s for s in ss if len(s) >= 4]


changed = []
for fn in sorted(os.listdir(ROOT)):
    if not fn.endswith('.html'):
        continue
    p = os.path.join(ROOT, fn)
    src = open(p, encoding='utf-8').read()
    m = re.search(r'(var\s+DICT_NOTES\s*=\s*)(\[.*?\])(\s*;)', src, re.S)
    if not m:
        continue
    items, fmt = parse(m.group(2))
    if not items:
        continue
    bad = [it for it in items if SEC.match(it.get('q', '')) or ('段' in it.get('q', '')[:6] and '·' in it.get('q', '')[:12])]
    if not bad:
        continue
    txt = body_text(src)
    sents = sentences(txt)
    first = [l for l in m.group(2).splitlines() if l.strip().startswith('{')]
    indent = re.match(r'\s*', first[0]).group(0) if first else '    '
    cm = re.search(r'\n(\s*)\]\s*$', m.group(2))
    close = cm.group(1) if cm else '  '
    nfix = 0
    for it in items:
        q = it.get('q', '')
        if not (SEC.match(q) or ('段' in q[:6] and '·' in q[:12])):
            continue
        wbase = re.sub(r'\(.*?\)', '', it.get('w', '')).replace('…', '').replace('.', '')
        wbase = wbase.split('……')[0].strip()
        if not wbase:
            continue
        hit = None
        for s in sents:
            if wbase in s:
                hit = s
                break
        if hit:
            it['q'] = hit
            nfix += 1
    if nfix:
        new = m.group(1) + dump(items, fmt, indent, close) + m.group(3)
        src = src[:m.start()] + new + src[m.end():]
        open(p, 'w', encoding='utf-8').write(src)
        changed.append((fn, len(bad), nfix))

print('修复文件:')
for c in changed:
    print('   %-40s 章节名条目=%d 已换为所在句=%d' % c)
