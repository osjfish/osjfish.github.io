# -*- coding: utf-8 -*-
"""清除纯空转注释：data-note 去掉标点/空白后与词完全相同的，删除标注保留原词。
有括号补充信息的（如「三千人（虚指，形容多）」「那边（指北京）」）一律保留。"""
import io, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
FILES = ['pipaxing-baijuyi', 'changhenge-baijuyi', 'hongmenyan-shiji',
         'beiying-zhuziqing', 'hetangyuese-zhuziqing',
         'tengyexiansheng-luxun', 'guxiang-luxun', 'zixinli']

PUNCT = '。，、；：！？！?.,;: \u3000\t\r\n'
PAT = re.compile(r'<span class="anno-word" data-note="([^"]*)">([^<]*)</span>')


def core(s):
    return ''.join(c for c in s if c not in PUNCT)


def clean(fn):
    path = os.path.join(BASE, fn + '.html')
    if not os.path.exists(path):
        return
    src = io.open(path, encoding='utf-8').read()
    removed, kept = [], []

    def rep(m):
        note, word = m.group(1), m.group(2)
        if core(note) == core(word):          # 纯空转
            removed.append((word, note))
            return word
        kept.append((word, note))
        return m.group(0)

    out = PAT.sub(rep, src)
    if removed:
        io.open(path, 'w', encoding='utf-8', newline='').write(out)
    print('%-24s 删 %d 处空转，其余 %d 条保留' % (fn, len(removed), len(kept)))
    for w, n in removed:
        print('    - %s -> %s' % (w, n if n != w else '(与词相同)'))


for f in FILES:
    clean(f)
