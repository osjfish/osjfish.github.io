# -*- coding: utf-8 -*-
"""文言「常见词纯同义注」收口：只读列出候选，供逐条判。
范围：detect_classical 为真 且 anno-word 词 w 属常见词表(TRIVIAL_EXT)。
分类：KEEP = note 含词类活用/古今异义/通假/虚词用法等学习必需标记；
      REMOVE = note 仅为现代汉语同义对译（X=Y，词性不变），属「纯同义注」。
输出：候选全表 + KEEP/REMOVE 自动标记，便于人工复核。
"""
import os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}
ANNO_RE = re.compile(r'(<span class="anno-word"[^>]*data-note="([^"]*)"[^>]*>)(.*?)(</span>)', re.S)
TAG_STRIP = re.compile(r'<[^>]+>')
CLASSICAL = '之其而以乃遂故曰乎者矣焉哉尔汝吾予'

TRIVIAL = set("""
的 了 是 在 有 我 你 他 她 它 们 这 那 上 下 里 中 个 得 着 过 和 与 把 被 对 从 到
就 都 很 也 要 会 说 来 去 大 小 多 少 好 不 没 一 二 三 四 五 十 什么 怎么 因为 所以
但是 然后 如果 可以 已经 还是 而且 我们 你们 他们 自己 东西 时候 地方 知道 看见 听见
觉得 认为 喜欢 高兴 美丽 漂亮 非常 十分 马上 立刻 忽然 突然 慢慢 悄悄 仔细 认真 努力
帮助 朋友 老师 学生 学校 家里 父亲 母亲 孩子 人们 生活 工作 学习 时间 问题 事情 世界
国家 社会 历史 文化 艺术 科学 自然 环境 今天 明天 昨天 现在 开始 结束 声音 眼睛 心里
太阳 月亮 天空 大地 春天 秋天 冬天 夏天 花 草 树 鸟 鱼 马 牛 羊 家 门 路 山 水 风 雨
肥胖 安静 明白 清楚 简单 容易 困难 重要 主要 完全 全部 一切 许多 各种
""".split())
AA_COMMON = set('处处 天天 人人 年年 时时 个个 家家 户户 步步 声声 阵阵 缓缓 渐渐 往往 常常 刚刚 统统 满满 紧紧 高高 低低 长长 远远 近近 真真 好好 红红 白白 黑黑'.split())
TRIVIAL_EXT = TRIVIAL | AA_COMMON

# 这些标记出现 → 注释是学习必需的（词类活用/古今异义/通假/虚词/代词/特殊句式），KEEP
KEEP_MARK = re.compile(
    r'词类活用|名词作|动词作|形容词作|数量词作|意动|使动|为动|活用'
    r'|作动词|作名词|作状语|作形容词|名作|动作名|形作|方位名词作'
    r'|古今|古义|今义|古指|今指|文中|这里指'
    r'|通[「“\'"]|同[「“\']|通假|读\s*[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]'
    r'|语气词|句末|句首|助词|介词|连词|副词|代词|指示|疑问|一词多义|多义'
    r'|宾语前置|倒装|省略|被动|提宾|谓语前置|定语后置|状语后置'
    r'|比喻义|象征|借代|拟人|双关|修辞|叠词|文化常识|方言|反语|炼字|呼应'
)

SYNONYM_HINT = re.compile(r'[=＝：:]')  # note 形如「X=Y」


def strip_tags(s):
    return TAG_STRIP.sub('', s).strip()


def detect_classical(text):
    n = sum(text.count(c) for c in CLASSICAL)
    return n / max(1, len(text)) > 0.012


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    cands = []
    for fn in files:
        src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
        body = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
        body = re.sub(r'<style\b[^>]*>.*?</style>', '', body, flags=re.S | re.I)
        text = strip_tags(body)
        if not detect_classical(text):
            continue
        for m in ANNO_RE.finditer(src):
            note, wtag = m.group(2), m.group(3)
            w = strip_tags(wtag)
            n = (note or '').strip()
            if w in TRIVIAL_EXT:
                cands.append((fn, w, n))
    print('文言常见词 anno-word 候选：%d 条' % len(cands))
    print('=' * 78)
    keep, rem = [], []
    for fn, w, n in cands:
        tag = 'KEEP' if KEEP_MARK.search(n) else 'REMOVE'
        (keep if tag == 'KEEP' else rem).append((fn, w, n))
    print('\n【KEEP 标记命中 %d 条 — 学习必需，保留】' % len(keep))
    for fn, w, n in keep:
        print('  %-44s %s = %s' % (fn, w, n[:46]))
    print('\n【REMOVE 候选 %d 条 — 疑似纯同义注，待复核】' % len(rem))
    for fn, w, n in rem:
        print('  %-44s %s = %s' % (fn, w, n[:46]))
    # 导出 REMOVE 明细供复核
    if '--dump' in sys.argv:
        with open(os.path.join(ROOT, 'tools', '_classical_remove_cands.txt'), 'w', encoding='utf-8') as f:
            for fn, w, n in rem:
                f.write('%s\t%s\t%s\n' % (fn, w, n))
        print('\n已导出 %d 条 REMOVE 候选到 _classical_remove_cands.txt' % len(rem))


if __name__ == '__main__':
    main()
