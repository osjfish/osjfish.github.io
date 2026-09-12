# -*- coding: utf-8 -*-
"""
按 JSON 清单批量解除注释（unwrap span，保留文字），并可选同步清理 DICT_NOTES。
用法：python _fix_anno_batch.py spec.json [--apply]

spec.json: { "文件名.html": ["词1","词2", ...], ... }
DICT_NOTES 同步：spec 里若给 {"__notes__": {"文件名.html": ["词"]}} 则清理对应默写条目。
"""
import os, re, sys, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANNO_RE = re.compile(r'(<span class="anno-word"[^>]*data-note="([^"]*)"[^>]*>)(.*?)(</span>)', re.S)
TAG_STRIP = re.compile(r'<[^>]+>')


def unwrap(src, words):
    stat = collections.Counter()

    def repl(m):
        w = TAG_STRIP.sub('', m.group(3)).strip()
        if w in words:
            stat['注释'] += 1
            return m.group(3)
        return m.group(0)

    return ANNO_RE.sub(repl, src), stat


def clean_notes(src, words):
    """删除 DICT_NOTES 里 w 等于给定词的条目"""
    n = 0

    def repl(m):
        nonlocal n
        body = m.group(2)
        for w in words:
            new, k = re.subn(r"\{[^{}]*['\"]w['\"]\s*:\s*['\"]%s['\"][^{}]*\}\s*,?\s*" % re.escape(w), '', body)
            if k:
                n += k
                body = new
        body = re.sub(r',\s*(\])', r'\1', body)
        body = re.sub(r'\[\s*,', '[', body)
        return m.group(1) + body + m.group(3)

    return re.sub(r'(DICT_NOTES\s*=\s*)(\[.*?\])(\s*;)', repl, src, flags=re.S), n


def main():
    spec_path = sys.argv[1]
    apply = '--apply' in sys.argv
    spec = json.load(open(spec_path, encoding='utf-8'))
    notes_spec = spec.pop('__notes__', {})
    tot = collections.Counter()
    for fn, words in sorted(spec.items()):
        p = os.path.join(ROOT, fn)
        if not os.path.exists(p):
            print('!! 缺失', fn)
            continue
        src = open(p, encoding='utf-8').read()
        new, st = unwrap(src, set(words))
        nw = notes_spec.get(fn)
        if nw:
            new, n = clean_notes(new, nw)
            st['注释题'] = n
        if new != src and apply:
            open(p, 'w', encoding='utf-8').write(new)
        tot.update(st)
        print('%-52s %s' % (fn[:50], dict(st)))
    print('\n合计:', dict(tot))
    print('（dry-run）' if not apply else '已写入')


if __name__ == '__main__':
    main()
