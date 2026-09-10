# -*- coding: utf-8 -*-
"""校验：统一 CSS 后，正文内容（去 style 块、去行内 style 属性）应与 HEAD 版本一致。"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STYLE_RE = re.compile(r'<style[^>]*>.*?</style>', re.S)
INLINE = re.compile(r'\sstyle="[^"]*"')

def norm(s):
    s = STYLE_RE.sub('', s)
    s = re.sub(r'<script[^>]*>.*?</script>', '', s, flags=re.S)
    s = INLINE.sub('', s)
    return re.sub(r'\s+', '', s)

files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html'))
bad = []
for f in files:
    old = subprocess.run(['git', 'show', 'HEAD:Apps/'.replace('Apps/', '') + 'yanshi/' + f],
                         cwd=os.path.dirname(ROOT), capture_output=True)
    if old.returncode:
        old = subprocess.run(['git', 'show', 'HEAD:yanshi/' + f],
                             cwd=os.path.dirname(ROOT), capture_output=True)
    if old.returncode:
        print('SKIP(no HEAD version)', f); continue
    o = norm(old.stdout.decode('utf-8'))
    n = norm(open(os.path.join(ROOT, f), encoding='utf-8').read())
    if o != n:
        bad.append((f, len(o), len(n)))

print('正文内容不一致的文件数:', len(bad))
for f, a, b in bad[:10]:
    print('  ', f, 'old', a, 'new', b)
