# -*- coding: utf-8 -*-
"""将 DICT_WORDS / DICT_NOTES 的单引号无引号 key 写法规范为合法 JSON（双引号 key+值）。
仅改引号/空白，不改任何字段值；浏览器显示文本不变（JS 双引号串内 \" 即 "）。
用法：python _normalize_dict_json.py            # dry-run
      python _normalize_dict_json.py --apply     # 落地
"""
import os, re, sys, json

ROOT = r'D:\App\Apps\yanshi'
APPLY = '--apply' in sys.argv
FILES = ['changhenge-baijuyi.html', 'hongmenyan-shiji.html', 'pipaxing-baijuyi.html']
PAIR = re.compile(r"(\w+)\s*:\s*'([^']*)'")            # key:'value'
ARR = re.compile(r"var\s+(DICT_\w+)\s*=\s*(\[.*?\])\s*;", re.S)


def parse_block(b):
    b = b.strip()
    try:
        return json.loads(b)                      # 已是合法 JSON（双引号）
    except Exception:
        pass
    d = PAIR.findall(b)                            # 单引号无引号 key 写法
    if d:
        return {k: v for k, v in d}
    raise ValueError('无法解析对象: ' + b[:60])


def normalize_array(raw):
    objs = []
    for blk in re.finditer(r'\{[^{}]*\}', raw):
        objs.append(parse_block(blk.group(0)))
    return '[' + ', '.join(
        '{' + ', '.join('"%s": %s' % (k, json.dumps(v, ensure_ascii=False)) for k, v in o.items()) + '}'
        for o in objs
    ) + ']'


def objs_equal(a, b):
    """逐对象、逐字段比对，确保规范化零值漂移（忽略 key 顺序）。"""
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if set(x.keys()) != set(y.keys()):
            return False
        for k in x:
            if x[k] != y[k]:
                return False
    return True


def fix_file(f):
    p = os.path.join(ROOT, f)
    src = open(p, encoding='utf-8').read()
    # 一次性取全部匹配；从右向左替换，避免前次替换改变 src 长度导致后续偏移失效
    matches = list(ARR.finditer(src))
    total = 0
    for m in sorted(matches, key=lambda mm: mm.start(2), reverse=True):
        name, raw = m.group(1), m.group(2)
        try:
            json.loads(raw)
            continue  # 已是合法 JSON，跳过
        except Exception:
            pass
        before_objs = [parse_block(b.group(0)) for b in re.finditer(r'\{[^{}]*\}', raw)]
        new = normalize_array(raw)
        after_objs = json.loads(new)
        assert objs_equal(before_objs, after_objs), '%s %s 规范化前后字段不一致' % (f, name)
        # 二次校验：new 必为合法 JSON 且条目数一致
        assert len(before_objs) == len(after_objs), '%s %s 条目数 %d→%d' % (f, name, len(before_objs), len(after_objs))
        src = src[:m.start(2)] + new + src[m.end(2):]
        total += 1
        print('  %s %s: %d 对象已规范化' % (name, f, len(after_objs)))
    if total == 0:
        print('  %s: 无需改动' % f)
        return 0
    if APPLY:
        open(p, 'w', encoding='utf-8').write(src)
    return total


if __name__ == '__main__':
    t = 0
    for f in FILES:
        print('==', f)
        t += fix_file(f)
    print('合计规范化数组:', t, '(APPLY=%s)' % APPLY)
