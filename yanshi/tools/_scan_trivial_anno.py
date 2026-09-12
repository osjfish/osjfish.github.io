# -*- coding: utf-8 -*-
"""全库扫描「既不生僻也不重要的常见词 anno-word」候选（只读，供逐条判）。
判定：词在 常见词表(扩展=原 TRIVIAL + 常用 AA 叠词) 且 注释非「合法注释类型」。
合法注释类型（VALID_MARK）：多音字注音/古今异义/文中·这里指/方言/通假/修辞(拟人·比喻义·象征·借代·叠词·双关)/语境义/文化常识。
"""
import os, re, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}
ANNO_RE = re.compile(r'<span class="anno-word"[^>]*data-note="([^"]*)"[^>]*>(.*?)</span>', re.S)
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
# 常用 AA 叠词（日常通用，非文言叠词）：处/天/人/年/时/个/家/户/步/声/阵/缓/渐/往/常/刚/统/满/紧/高/低/长/远/近/真/好/红/白/黑
AA_COMMON = set('处处 天天 人人 年年 时时 个个 家家 户户 步步 声声 阵阵 缓缓 渐渐 往往 常常 刚刚 统统 满满 紧紧 高高 低低 长长 远远 近近 真真 好好 红红 白白 黑黑'.split())
TRIVIAL_EXT = TRIVIAL | AA_COMMON

VALID_MARK = re.compile(
    r'读\s*[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]|[（(][a-zāáǎà].{0,12}[)）]'
    r'|文中|这里指|古今|方言|通[「“]|反语|拟人|比喻义|象征|借代|词类活用|意动|使动'
    r'|呼应|全文|情感载体|炼字|修辞|双关|叠词')


def strip_tags(s):
    return TAG_STRIP.sub('', s).strip()


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    cands = []
    for fn in files:
        src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
        body = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
        body = re.sub(r'<style\b[^>]*>.*?</style>', '', body, flags=re.S | re.I)
        text = strip_tags(body)
        classical = sum(text.count(c) for c in CLASSICAL) / max(1, len(text)) > 0.012
        for m in ANNO_RE.finditer(src):
            note, wtag = m.group(1), m.group(2)
            w = strip_tags(wtag)
            n = (note or '').strip()
            if w in TRIVIAL_EXT and not VALID_MARK.search(n):
                cands.append((fn, w, n, classical))
    print('候选（词在常见词表 且 非合法注释类型）：%d 条' % len(cands))
    print('=' * 70)
    # 先列非文言（直接可删），再列文言（需逐条判）
    for label, cl in (('非文言', False), ('文言', True)):
        grp = [c for c in cands if c[3] == cl]
        print('\n--- %s篇章 %d 条 ---' % (label, len(grp)))
        for fn, w, n, _ in grp:
            print('  %-46s %s = %s' % (fn, w, n[:40]))
    # 汇总待删文件数
    files_to_fix = sorted(set(c[0] for c in cands if not c[3]))
    print('\n非文言待处理文件：%d 篇' % len(files_to_fix))


if __name__ == '__main__':
    main()
