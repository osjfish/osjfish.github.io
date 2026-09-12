# -*- coding: utf-8 -*-
"""严格校验全部课件 DICT_WORDS / DICT_NOTES 是否为合法 JSON（非法则浏览器会 SyntaxError）。"""
import os, re, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}


def parse_strict(src, name):
    m = re.search(r'(?:var|let|const)?\s*%s\s*=\s*(\[.*?\])\s*;' % name, src, re.S)
    if not m:
        return None, '无数组'
    raw = m.group(1)
    try:
        json.loads(raw)
        return True, ''
    except Exception as e:
        return False, str(e)


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    bad = collections.defaultdict(list)
    for fn in files:
        src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
        for name in ('DICT_WORDS', 'DICT_NOTES'):
            ok, msg = parse_strict(src, name)
            if ok is not True:
                bad[name].append('%s: %s' % (fn, msg[:80]))
    print('文件数:', len(files))
    if not bad:
        print('全部 DICT_WORDS / DICT_NOTES 均为合法 JSON，0 问题')
    else:
        for k, v in bad.items():
            print('\n【%s 非法】 %d 篇' % (k, len(v)))
            for line in v[:50]:
                print('   ', line)


if __name__ == '__main__':
    main()
