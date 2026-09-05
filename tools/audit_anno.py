# -*- coding: utf-8 -*-
"""扫描所有语文课件，挑出低质量注释（同义反复 / 无用 / 过度）。"""
import io, os, re, glob, json, sys, ast

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = ['pipaxing-baijuyi', 'changhenge-baijuyi', 'hongmenyan-shiji',
         'beiying-zhuziqing', 'hetangyuese-zhuziqing',
         'tengyexiansheng-luxun', 'guxiang-luxun', 'zixinli']

# 常识词：初高中生一眼就懂，不该占注释位
COMMON = set('''的 了 是 在 我 有 和 就 不 人 都 一 一个 上 也 很 到 说 要 去 你 会 着 没有
看 好 自己 这 那 里 来 家 天 下 中 出 年 月 日 时 今 今年 明年 去年 前年 昨日 今日
大 小 多 少 长 短 高 低 上 下 左 右 前 后 东 西 南 北 中 内 外
人 山 水 天 地 风 雨 云 月 日 星 花 草 树 木 江 河 湖 海
父 母 兄 弟 姐 妹 儿 女 子
一 二 三 四 五 六 七 八 九 十 百 千 万
遂 乃 即 则 而 且 若 夫 盖 惟 唯 斯 此 之 其 者 所 以 为 于 乎 哉 矣 焉 耳
'''.split())

# 注释中出现的"同义反复"标志
TAUT = ['同“%s”', '即%s', '就是%s', '%s的意思']


def note_quality(w, n):
    """返回问题列表，空列表表示合格"""
    p = []
    w = w.strip()
    n = n.strip()
    if not w or not n:
        return ['空']
    # 1. 注释 == 词
    if n == w:
        p.append('注释=词')
    # 2. 注释只是给词加了"。" / "，"
    if n.rstrip('。，、；：') == w:
        p.append('注释=词+标点')
    # 3. 注释是"X：X"式空转，如"今年：今年"
    if re.match(r'^%s\s*[:：]\s*%s$' % (re.escape(w), re.escape(w)), n):
        p.append('注释=词：词')
    # 4. 常识词
    if w in COMMON and len(w) <= 2:
        p.append('常识词')
    # 5. 注释极短且未补充新信息（去掉括号注音后与词同长且内容相同）
    bare = re.sub(r'[（(][^)）]*[)）]', '', n).strip()
    if bare and bare == w:
        p.append('去注音后=词')
    # 6. 只写了"XX的样子"但词本身就是这个意思的重复（弱判，单列）
    if re.match(r'^%s的样子$' % re.escape(w), n):
        p.append('「词+的样子」')
    if re.match(r'^%s地?$' % re.escape(w), n):
        p.append('「词+地」')
    return p


def scan(fn):
    path = os.path.join(BASE, fn + '.html')
    src = io.open(path, encoding='utf-8').read()
    # 页内注释
    anno = re.findall(r'<span class="anno-word" data-note="([^"]*)"[^>]*>([^<]*)</span>', src)
    # 题库注释
    m = re.search(r'var DICT_NOTES\s*=\s*(\[.*?\]);', src, re.S)
    notes = []
    if m:
        try:
            notes = json.loads(m.group(1))
        except Exception:
            try:
                notes = ast.literal_eval(m.group(1))
            except Exception as e:
                print('  (DICT_NOTES 解析失败 %s: %s)' % (fn, e))
    return anno, notes


if __name__ == '__main__':
    total = 0
    for fn in NAMES:
        if not os.path.exists(os.path.join(BASE, fn + '.html')):
            print('!! missing', fn)
            continue
        anno, notes = scan(fn)
        bad_anno = [(w, n, note_quality(w, n)) for n, w in anno if note_quality(w, n)]
        bad_note = [(d['w'], d['a'], note_quality(d['w'], d['a'])) for d in notes
                    if note_quality(d['w'], d['a'])]
        # 重复注释（同一词注多次且内容不同）
        dup = {}
        for n, w in anno:
            dup.setdefault(w, set()).add(n)
        dupw = {k: v for k, v in dup.items() if len(v) > 1}
        total += len(bad_anno) + len(bad_note)
        print('=' * 60)
        print('%-28s 页内注释 %d  词语题 %d  低质量 %d  同词异注 %d'
              % (fn, len(anno), len(notes), len(bad_anno) + len(bad_note), len(dupw)))
        for w, n, p in bad_anno[:40]:
            print('   [页内] %s -> %s   << %s' % (w, n, '/'.join(p)))
        for w, a, p in bad_note[:40]:
            print('   [词语] %s -> %s   << %s' % (w, a, '/'.join(p)))
        if dupw:
            for k, v in list(dupw.items())[:10]:
                print('   [异注] %s -> %s' % (k, ' | '.join(sorted(v))))
    print('=' * 60)
    print('TOTAL 低质量注释:', total)
