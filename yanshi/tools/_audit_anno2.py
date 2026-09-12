# -*- coding: utf-8 -*-
"""
注释/练习 质量审计 v2（只读）。修正 v1 的误判：
- 文言文的虚词一词多义、单字短注属正常，不再报警
- DICT 兼容单引号写法
- 覆盖判定改用包含匹配（注释词常多/少一个虚字）
输出：可直接执行的「待清理注释」清单
用法：python _audit_anno2.py [--json out.json]
"""
import os, re, sys, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}
ANNO_RE = re.compile(r'(<span class="anno-word"[^>]*data-note="([^"]*)"[^>]*>)(.*?)(</span>)', re.S)
TAG_STRIP = re.compile(r'<[^>]+>')

# 积累区词条有多种模板：acc-w 词条卡 / g-item 的 dt / 表格 td.kai / b.term 术语
ACC_PATTERNS = [
    re.compile(r'<span class="acc-w(?:ord)?">(.*?)</span>', re.S),
    re.compile(r'<dt>(.*?)</dt>', re.S),
    re.compile(r'<td class="kai">(.*?)</td>', re.S),
    re.compile(r'<b class="term">(.*?)</b>', re.S),
]


def acc_words(src):
    out = []
    for p in ACC_PATTERNS:
        out += [strip_tags(m.group(1)) for m in p.finditer(src)]
    return out

# 初中生显然已掌握、不该注的词（仅用于现代文）
TRIVIAL = set("""
的 了 是 在 有 我 你 他 她 它 们 这 那 上 下 里 中 个 得 着 过 和 与 把 被 对 从 到
就 都 很 也 要 会 说 来 去 大 小 多 少 好 不 没 一 二 三 四 五 十 什么 怎么 因为 所以
但是 然后 如果 可以 已经 还是 而且 我们 你们 他们 自己 东西 时候 地方 知道 看见 听见
觉得 认为 喜欢 高兴 美丽 漂亮 非常 十分 马上 立刻 忽然 突然 慢慢 悄悄 仔细 认真 努力
帮助 朋友 老师 学生 学校 家里 父亲 母亲 孩子 人们 生活 工作 学习 时间 问题 事情 世界
国家 社会 历史 文化 艺术 科学 自然 环境 今天 明天 昨天 现在 开始 结束 声音 眼睛 心里
太阳 月亮 天空 大地 春天 秋天 冬天 夏天 花 草 树 鸟 鱼 马 牛 羊 家 门 路 山 水 风 雨
肥胖 安静 明白 清楚 清楚 简单 容易 困难 重要 主要 完全 全部 一切 一切 许多 各种
""".split())

CLASSICAL = '之其而以乃遂故曰乎者矣焉哉尔汝吾予'


def strip_tags(s):
    return TAG_STRIP.sub('', s).strip()


def detect_classical(text):
    n = sum(text.count(c) for c in CLASSICAL)
    return n / max(1, len(text)) > 0.012


def parse_dict(src, name):
    """兼容单/双引号，返回 list[dict]"""
    m = re.search(r'(?:var|let|const)?\s*%s\s*=\s*(\[.*?\])\s*;' % name, src, re.S)
    if not m:
        return None
    raw = m.group(1)
    try:
        return json.loads(raw)
    except Exception:
        pass
    out = []
    for blk in re.finditer(r'\{([^{}]*)\}', raw):
        d = {}
        for k in ('w', 'a', 'q', 'py', 'tip'):
            mm = re.search(r"""['"]?%s['"]?\s*:\s*(['"])(.*?)\1""" % k, blk.group(1), re.S)
            if mm:
                d[k] = mm.group(2)
        if d:
            out.append(d)
    return out


def covered(word, anno_words):
    """包含匹配：注释词常多/少一个虚字"""
    if word in anno_words:
        return True
    for a in anno_words:
        if word and a and (word in a or a in word):
            return True
    return False


def audit(path):
    src = open(path, encoding='utf-8').read()
    body = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
    body = re.sub(r'<style\b[^>]*>.*?</style>', '', body, flags=re.S | re.I)
    text = strip_tags(body)
    classical = detect_classical(text)

    annos = [(strip_tags(m.group(3)), m.group(2)) for m in ANNO_RE.finditer(src)]
    anno_words = [w for w, _ in annos]
    dw, dn = parse_dict(src, 'DICT_WORDS'), parse_dict(src, 'DICT_NOTES')

    issues = collections.defaultdict(list)
    remove = []  # 建议移除的注释 (word, note)

    for w, note in annos:
        n = (note or '').strip()
        # 1) 注释词本身是标点
        if w and not re.search(r'[\u4e00-\u9fff A-Za-z]', w):
            issues['注释词是标点'].append('%s=%s' % (w, n))
            remove.append((w, n, '注释词是标点'))
        # 2) 注释等于词 / 空
        elif not n or n == w:
            issues['无效注释(空/等于词)'].append(w or '(空)')
            remove.append((w, n, '无效注释'))
        # 3) 现代文注了人人都会的词
        elif not classical and w in TRIVIAL:
            issues['现代文过度注释'].append('%s=%s' % (w, n[:24]))
            remove.append((w, n, '常见词'))
        # 4) 现代文注释过短（<3字）多半没信息量
        elif not classical and len(n) < 3 and w not in ('曰',):
            issues['现代文注释过短'].append('%s=%s' % (w, n))

    # DICT_NOTES 覆盖（注释默写应考「课文注释过」或「积累区收过」的词）
    if dn:
        pool = anno_words + acc_words(src)
        miss = [d.get('w') for d in dn if isinstance(d, dict)
                and d.get('w') and not covered(d['w'], pool)]
        if miss:
            issues['注释默写词无出处'].append(','.join(miss[:6]) + ('(%d)' % len(miss)))
    # DICT_WORDS 字应出现在课文中
    if dw:
        out = [d.get('w') for d in dw if isinstance(d, dict)
               and d.get('w') and d['w'] not in text]
        if out:
            issues['字形题字不在课文'].append(','.join(out[:6]) + ('(%d)' % len(out)))

    return issues, remove, len(annos), len(dw or []), len(dn or []), classical


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    agg = collections.defaultdict(list)
    all_remove = {}
    rows = []
    for fn in files:
        issues, remove, na, nw, nn, cl = audit(os.path.join(ROOT, fn))
        rows.append((fn, na, nw, nn, cl))
        if remove:
            all_remove[fn] = remove
        for k, v in issues.items():
            agg[k].append('%s: %s' % (fn, ';'.join(v)))
    print('文件数:', len(files))
    print('=' * 60)
    for k in sorted(agg, key=lambda x: -len(agg[x])):
        print('\n【%s】 %d 篇' % (k, len(agg[k])))
        for line in agg[k][:20]:
            print('   ', line[:180])
        if len(agg[k]) > 20:
            print('    ... 另 %d 篇' % (len(agg[k]) - 20))
    print('\n' + '=' * 60)
    tot = sum(len(v) for v in all_remove.values())
    print('建议移除的注释：%d 篇 / %d 条' % (len(all_remove), tot))
    if '--json' in sys.argv:
        json.dump(all_remove, open(sys.argv[sys.argv.index('--json') + 1], 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('已导出 JSON')


if __name__ == '__main__':
    main()
