# -*- coding: utf-8 -*-
"""
注释 / 练习 质量审计（只读）。
判据：注释应面向「本学段学生不理解或需要掌握的字词」。
重点抓：过度注释（注了人人都会的词）、注释质量问题、练习与注释脱节、题量异常。
用法：python _audit_anno.py [可选文件名关键字]
"""
import os, re, sys, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}

ANNO_RE = re.compile(r'<span class="anno-word"[^>]*data-note="([^"]*)"[^>]*>(.*?)</span>', re.S)
TAG_STRIP = re.compile(r'<[^>]+>')

# 初中生（七~九年级）显然已掌握、不该再注的词（仅用于现代文语境）
TRIVIAL = set("""
的 了 是 在 有 我 你 他 她 它 们 这 那 上 下 里 中 个 得 着 过 和 与 把 被 对 从 到
就 都 很 也 要 会 说 来 去 大 小 多 少 好 不 没 一 二 三 四 五 十 什么 怎么 因为 所以
但是 然后 如果 可以 已经 还是 而且 我们 你们 他们 自己 东西 时候 地方 知道 看见 听见
觉得 认为 喜欢 高兴 美丽 漂亮 非常 十分 马上 立刻 忽然 突然 慢慢 悄悄 仔细 认真 努力
帮助 朋友 老师 学生 学校 家里 父亲 母亲 孩子 人们 生活 工作 学习 时间 问题 事情 世界
国家 社会 历史 文化 艺术 科学 自然 环境 今天 明天 昨天 现在 开始 结束 声音 眼睛 心里
太阳 月亮 天空 大地 春天 秋天 冬天 夏天 风 雨 花 草 树 鸟 鱼 马 牛 羊 家 门 路 山 水
""".split())

# 文言特征字（出现多则判定为文言文，文言文允许注虚词）
CLASSICAL = '之其而以乃遂故曰乎者矣焉哉尔汝吾予'
MIN_NOTE_LEN = 2


def strip_tags(s):
    return TAG_STRIP.sub('', s).strip()


def detect_classical(text):
    if not text:
        return False
    n = sum(text.count(c) for c in CLASSICAL)
    return n / max(1, len(text)) > 0.012


def audit(path):
    src = open(path, encoding='utf-8').read()
    body = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
    body = re.sub(r'<style\b[^>]*>.*?</style>', '', body, flags=re.S | re.I)
    text = strip_tags(body)
    classical = detect_classical(text)

    annos = []
    for m in ANNO_RE.finditer(src):
        annos.append((strip_tags(m.group(2)), m.group(1)))

    def grab(name):
        m = re.search(r'(?:var|let|const)?\s*%s\s*=\s*(\[.*?\])\s*;' % name, src, re.S)
        if not m:
            return None
        raw = m.group(1)
        try:
            return json.loads(raw)
        except Exception:
            return 'UNPARSED:' + raw[:80]

    dw, dn = grab('DICT_WORDS'), grab('DICT_NOTES')
    f = collections.defaultdict(list)
    anno_words = [w for w, _ in annos]

    # ---- 注释质量 ----
    for w, note in annos:
        n = (note or '').strip()
        if not n:
            f['注释空'].append(w)
        elif n in {'，', '。', '、', '？', '！', '；', '：', '逗号', '句号', '、'}:
            f['注释是标点'].append('%s=%s' % (w, n))
        elif n == w:
            f['注释等于词'].append(w)
        elif len(n) < MIN_NOTE_LEN:
            f['注释过短'].append('%s=%s' % (w, n))
        elif re.search(r'<[a-zA-Z/]', n):
            f['注释含标签'].append('%s=%s' % (w, n[:30]))
        elif '{LQ}' in n or '{RQ}' in n or '\\u' in n:
            f['注释含占位/转义'].append('%s=%s' % (w, n[:30]))
        if not classical and w in TRIVIAL:
            f['过度注释(常见词)'].append('%s=%s' % (w, n[:20]))

    # 重复注释（同一词注多次且释义不同）
    byw = collections.defaultdict(set)
    for w, note in annos:
        byw[w].add(note)
    for w, ns in byw.items():
        if len(ns) > 1:
            f['同词异释'].append('%s(%d种)' % (w, len(ns)))

    # ---- 练习 ----
    if dw is None:
        f['缺DICT_WORDS'].append('无')
    elif isinstance(dw, str):
        f['DICT_WORDS解析失败'].append(dw[:60])
    else:
        if len(dw) < 8:
            f['字形题过少'].append(str(len(dw)))
        ws = [d.get('w', '') for d in dw if isinstance(d, dict)]
        dup = [w for w, c in collections.Counter(ws).items() if c > 1]
        if dup:
            f['字形题重复'].append(','.join(dup[:5]))
        for d in dw:
            if not isinstance(d, dict):
                continue
            if not d.get('py'):
                f['字形题缺拼音'].append(d.get('w', '?'))
            if not d.get('q') or '□' not in str(d.get('q', '')):
                f['字形题缺挖空句'].append(d.get('w', '?'))
            if d.get('w') and d['w'] not in text:
                f['字形题字不在课文'].append(d.get('w', '?'))
        # 字形题字应是被注释过的重点字
        notanno = [d.get('w') for d in dw if isinstance(d, dict)
                   and d.get('w') and d['w'] not in anno_words]
        if notanno:
            f['字形题字未注释'].append(','.join(notanno[:8]) + ('(%d)' % len(notanno)))

    if dn is None:
        f['缺DICT_NOTES'].append('无')
    elif isinstance(dn, str):
        f['DICT_NOTES解析失败'].append(dn[:60])
    else:
        if len(dn) < 8:
            f['注释题过少'].append(str(len(dn)))
        ws = [d.get('w', '') for d in dn if isinstance(d, dict)]
        dup = [w for w, c in collections.Counter(ws).items() if c > 1]
        if dup:
            f['注释题重复'].append(','.join(dup[:5]))
        for d in dn:
            if not isinstance(d, dict):
                continue
            w = d.get('w', '')
            if not w:
                f['注释题缺词'].append('?')
                continue
            if w not in anno_words:
                f['注释题词未注释'].append(w)
            if not d.get('a'):
                f['注释题缺答案'].append(w)
            elif w in byw and d['a'] not in byw[w]:
                f['注释题答案与注释不符'].append('%s:%s' % (w, str(d['a'])[:20]))

    return f, len(annos), (len(dw) if isinstance(dw, list) else 0), \
        (len(dn) if isinstance(dn, list) else 0), classical, annos


def main():
    kw = sys.argv[1] if len(sys.argv) > 1 else None
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    if kw:
        files = [f for f in files if kw in f]
    agg = collections.defaultdict(list)
    stats = {}
    all_annos = []
    for fn in files:
        f, na, nw, nn, cl, annos = audit(os.path.join(ROOT, fn))
        stats[fn] = (na, nw, nn, cl)
        all_annos.extend(annos)
        for k, v in f.items():
            agg[k].append('%s: %s' % (fn, ';'.join(v)))
    print('文件数:', len(files))
    print('=' * 60)
    for k in sorted(agg, key=lambda x: -len(agg[x])):
        print('\n【%s】 %d 篇' % (k, len(agg[k])))
        for line in agg[k][:10]:
            print('   ', line[:200])
        if len(agg[k]) > 10:
            print('    ... 另 %d 篇' % (len(agg[k]) - 10))
    # 全局：被反复注释的词（可能过浅）
    c = collections.Counter(w for w, _ in all_annos)
    print('\n' + '=' * 60)
    print('被注释次数最多的词 TOP25（跨全库，可能过浅/过频）:')
    for w, n in c.most_common(25):
        print('   %s x%d' % (w, n))
    # 密度
    ds = sorted(((v[0], k, v[1], v[2], v[3]) for k, v in stats.items()))
    print('\n注释数最少 8 篇:')
    for na, k, nw, nn, cl in ds[:8]:
        print('   %s anno=%d 字形=%d 注释题=%d 文言=%s' % (k, na, nw, nn, cl))
    print('注释数最多 8 篇:')
    for na, k, nw, nn, cl in ds[-8:]:
        print('   %s anno=%d 字形=%d 注释题=%d 文言=%s' % (k, na, nw, nn, cl))


if __name__ == '__main__':
    main()
