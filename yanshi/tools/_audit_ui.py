# -*- coding: utf-8 -*-
"""按 SKILL §0 自检清单做全库 UI/逻辑静态扫描（机器可判项）。"""
import os, re, io, sys, collections

ROOT = r'D:\App\Apps\yanshi'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

IDS = ['verseList', 'fulltext', 'btnAll', 'btnRecite', 'btnPrint', 'btnShowAll',
       'fsSel', 'annoPopup', 'dictate', 'topBtn', 'mediaF1', 'mediaF2']
SECS = ['hero', 'bg', 'jielu', 'app', 'acc', 'practice']

files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
miss_id = collections.defaultdict(list)
miss_sec = collections.defaultdict(list)
vert, vh, title_brackets = [], [], []
placeholder, straight_quote = [], []
css_escape = []
video_bad = collections.defaultdict(list)
ls_key = []
no_style = []
inline_fs = []
dup_id = collections.defaultdict(list)

for f in files:
    src = open(os.path.join(ROOT, f), encoding='utf-8').read()
    # 1 必需 id
    for i in IDS:
        if ('id="%s"' % i) not in src and ("id='%s'" % i) not in src:
            miss_id[f].append(i)
    # 1b 六区
    for s in SECS:
        if ('id="%s"' % s) not in src:
            miss_sec[f].append(s)
    # 重复 id
    for m in re.finditer(r'\sid="([A-Za-z][\w-]*)"', src):
        dup_id[f].append(m.group(1))
    # 2 卷首
    if re.search(r'writing-mode\s*:\s*vertical', src):
        vert.append(f)
    if re.search(r'min-height\s*:\s*\d+vh', src):
        vh.append(f)
    mt = re.search(r'<title>(.*?)</title>', src, re.S)
    if mt and ('《' in mt.group(1) or '》' in mt.group(1)):
        title_brackets.append((f, mt.group(1)))
    # 3 占位符 / 直引号（只看可见文本：去掉 script/style）
    vis = re.sub(r'<script[^>]*>.*?</script>', ' ', src, flags=re.S)
    vis = re.sub(r'<style[^>]*>.*?</style>', ' ', vis, flags=re.S)
    if '{LQ}' in vis or '{RQ}' in vis:
        placeholder.append(f)
    # 可见文本中的英文直引号（成对计数，允许 HTML 属性里的）
    txt = re.sub(r'<[^>]+>', ' ', vis)
    nq = txt.count('"')
    if nq:
        straight_quote.append((f, nq))
    # 14 CSS 转义
    st = re.search(r'<style[^>]*>(.*?)</style>', src, re.S)
    if not st:
        no_style.append(f)
    else:
        for m in re.finditer(r'content\s*:\s*[^;}]*\\u[0-9a-fA-F]{4}', st.group(1)):
            css_escape.append((f, m.group(0)[:40]))
    # 5 视频
    for m in re.finditer(r'src="(https?://[^"]*bilibili[^"]*)"', src):
        u = m.group(1)
        if 'player.bilibili.com' not in u:
            video_bad[f].append('非 player 域名: ' + u[:60])
        if re.search(r'autoplay=(?!0)', u):
            video_bad[f].append('autoplay≠0: ' + u[:60])
    # 10 localStorage key
    for m in re.finditer(r"localStorage\.(?:get|set)Item\(\s*'([^']*)'", src):
        ls_key.append((f, m.group(1)))
    # 行内 font-size（正文）
    body = re.sub(r'<style[^>]*>.*?</style>', '', src, flags=re.S)
    n = len(re.findall(r'style="[^"]*font-size', body))
    if n:
        inline_fs.append((f, n))

print('文件数:', len(files))
print()
print('【A】缺必需 id 的文件:', len(miss_id))
for f, v in list(miss_id.items())[:12]:
    print('   %-42s 缺 %s' % (f, ','.join(v)))
print('【B】缺六区 id 的文件:', len(miss_sec))
for f, v in list(miss_sec.items())[:12]:
    print('   %-42s 缺 %s' % (f, ','.join(v)))
print()
print('【C】卷首 vertical 竖排:', len(vert), vert[:5])
print('【D】min-height 用 vh:', len(vh), vh[:5])
print('【E】title 含书名号:', len(title_brackets), title_brackets[:5])
print()
print('【F】{LQ}/{RQ} 占位符残留:', len(placeholder), placeholder[:8])
print('【G】可见文本英文直引号:', len(straight_quote), straight_quote[:8])
print('【H】CSS content \\uXXXX 转义:', len(css_escape), css_escape[:5])
print('【I】无 <style> 块:', len(no_style), no_style[:5])
print('【J】正文行内 font-size:', len(inline_fs), inline_fs[:8])
print()
print('【K】视频问题:', len(video_bad))
for f, v in list(video_bad.items())[:10]:
    print('   %-42s %s' % (f, v))
print()
print('【L】localStorage key 异常（非本篇前缀/beiying_fs 残留）:')
badls = [(f, k) for f, k in ls_key if k == 'beiying_fs' or k.endswith('_fs') is False]
for f, k in badls[:10]:
    print('   %-42s %s' % (f, k))
print('   共', len(badls))
print()
print('【M】重复 id:')
nd = 0
for f, ids in dup_id.items():
    c = collections.Counter(ids)
    d = [k for k, v in c.items() if v > 1]
    if d:
        nd += 1
        if nd <= 10:
            print('   %-42s %s' % (f, d[:6]))
print('   共', nd, '个文件')
