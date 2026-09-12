# -*- coding: utf-8 -*-
"""修正 DICT_NOTES 的 q 句，使其与课文原文逐字一致（仅在确有错字/字序时改）。
   spec: {file: {set:[{old:w, q:新句}]}}
用法：python _fix_notes_q2.py spec.json [--apply]
"""
import os, re, sys, json, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARR_RE = re.compile(r'(DICT_NOTES\s*=\s*)(\[.*?\])(\s*;)', re.S)
BLK_RE = re.compile(r'\{[^{}]*\}', re.S)
W_RE = re.compile(r"""['"]?w['"]?\s*:\s*(['"])(.*?)\1""", re.S)


def get_field(blk, k):
    m = re.search(r"""['"]?%s['"]?\s*:\s*(['"])(.*?)\1""" % k, blk, re.S)
    return m.group(2) if m else ''


def main():
    spec = json.load(open(sys.argv[1], encoding='utf-8'))
    apply = '--apply' in sys.argv
    tot = collections.Counter()
    for fn, cfg in sorted(spec.items()):
        p = os.path.join(ROOT, fn)
        if not os.path.exists(p):
            print('!! 缺失', fn); continue
        src = open(p, encoding='utf-8').read()
        sets = {s['old']: s for s in cfg.get('set', [])}
        st = collections.Counter()

        def repl(m):
            arr = m.group(2)
            out = []
            for b in BLK_RE.finditer(arr):
                blk = b.group(0)
                wm = W_RE.search(blk)
                w = wm.group(2) if wm else ''
                if w in sets:
                    s = sets[w]
                    new = {}
                    for k in ('w', 'a', 'q', 'py', 'tip'):
                        new[k] = s.get(k, get_field(blk, k))
                    out.append(json.dumps(new, ensure_ascii=False))
                    st['改'] += 1
                else:
                    out.append(blk)
            return m.group(1) + '[' + ', '.join(out) + ']' + m.group(3)

        new = ARR_RE.sub(repl, src, count=1)
        if new != src and apply:
            open(p, 'w', encoding='utf-8').write(new)
        tot.update(st)
        print('%-52s %s' % (fn[:50], dict(st)))
    print('\n合计:', dict(tot), '已写入' if apply else '（dry-run）')


if __name__ == '__main__':
    main()
