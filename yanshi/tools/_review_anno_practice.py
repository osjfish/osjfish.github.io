# -*- coding: utf-8 -*-
"""复查：①文言里是否还有该删的「常见词纯同义注」（结构化初筛+待议清单）
        ②练习题（DICT_NOTES 注释题 / DICT_WORDS 字形题）里有无同类「常见词过度考查」问题。
仅做只读分析，供人工讨论，不落盘。
判定：结构化 KEEP 标记（词类活用/通假/多音/虚数/修辞/文化/显式古今异义/虚词）命中→学习必需；
      其余「X=Y 简单对译」为待议候选。待议候选再按语义粗分：纯净同义 / 疑似文言必需。
"""
import os, re, collections

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

# 结构化 KEEP 标记：命中即「学习必需」，不列入待议
KEEP_MARK = re.compile(
    r'词类活用|名词作|动词作|形容词作|数量词作|意动|使动|为动|活用'
    r'|作动词|作名词|作状语|作形容词|名作|动作名|形作|方位名词作'
    r'|古今异义|古义|今义|古指|今指|文中|这里指'
    r'|通[「"\'xX]|同[「"\'xX]|通假'
    r'|读\s*[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]|（[a-zāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]'
    r'|语气词|句末|句首|句中|助词|介词|连词|副词|代词|指示|疑问|一词多义|多义'
    r'|宾语前置|倒装|省略|被动|提宾|谓语前置|定语后置|状语后置|判断句|被动句'
    r'|比喻义|象征|借代|拟人|双关|修辞|叠词|文化常识|方言|反语|炼字|呼应'
    r'|虚数|非确数|多次（非确数）|表确数'
)

# 已删除的 27 条（用于交叉核对「还有没有漏网」）
REMOVED = {
 'changhenge-baijuyi.html': [('下','向下'),('里','里面'),('中','里面')],
 'dujingmensongbie-libai.html': [('山','山峦')],
 'pipaxing-baijuyi.html': [('往往','常常')],
 'yujiaaoqiusi-fanzhongyan.html': [('里','之中、里面')],
 'hongmenyan-shiji.html': [('下','脚下、下面'),('下','……的下面'),('上','上面'),('有','占有'),('来','来'),('我','我')],
 'ailianshuo-zhoudunyi.html': [('不','表示否定')],
 'zhuangziyuhuiziyouyuhaoliang-zhuangzi.html': [('上','上面'),('鱼','鱼'),('我','我')],
 'deduoduozhushidaoguazhu-mengzi.html': [('多','充足')],
 'loushiming-liuyuxi.html': [('有','有')],
 'sunquanquanxue-simaguang.html': [('过','经过')],
}


def strip_tags(s):
    return TAG_STRIP.sub('', s).strip()


def detect_classical(text):
    n = sum(text.count(c) for c in CLASSICAL)
    return n / max(1, len(text)) > 0.012


def parse_dict(src, name):
    m = re.search(r'(?:var|let|const)?\s*%s\s*=\s*(\[.*?\])\s*;' % name, src, re.S)
    if not m:
        return None
    out = []
    for blk in re.finditer(r'\{([^{}]*)\}', m.group(1)):
        d = {}
        for k in ('w', 'a', 'q'):
            mm = re.search(r"""['"]?%s['"]?\s*:\s*['"](.*?)['"]""" % k, blk.group(1), re.S)
            if mm:
                d[k] = mm.group(1)
        if d:
            out.append(d)
    return out


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    # ---- ① 文言注释待议清单 ----
    pending = []
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
            if w in TRIVIAL_EXT and not KEEP_MARK.search(n):
                removed = any(sub in n for _, sub in REMOVED.get(fn, []) if _ == w)
                pending.append((fn, w, n, removed))
    print('【① 文言常见词 简单对译注（结构化初筛待议）共 %d 条】' % len(pending))
    still = [p for p in pending if not p[3]]
    done = [p for p in pending if p[3]]
    print('  - 已删 %d 条；仍待议 %d 条（即「可能漏网/边界」）' % (len(done), len(still)))
    print('\n--- 仍待议（按文件）---')
    for fn, w, n, _ in still:
        print('  %-46s %s = %s' % (fn, w, n[:50]))

    # ---- ② 练习题：文言 DICT_NOTES 注释题里常见词纯同义考查 ----
    print('\n\n【② 练习题·注释题（DICT_NOTES）文言常见词纯同义考查候选】')
    for fn in files:
        src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
        body = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
        body = re.sub(r'<style\b[^>]*>.*?</style>', '', body, flags=re.S | re.I)
        text = strip_tags(body)
        if not detect_classical(text):
            continue
        dn = parse_dict(src, 'DICT_NOTES')
        if not dn:
            continue
        for d in dn:
            w = d.get('w', '')
            a = d.get('a', '')
            if w in TRIVIAL_EXT and not KEEP_MARK.search(a):
                print('  %-46s 注释题 w=%s a=%s' % (fn, w, a[:40]))

    # ---- ③ 练习题：文言 DICT_WORDS 字形题里常见字 ----
    print('\n【③ 练习题·字形题（DICT_WORDS）文言常见字候选】')
    for fn in files:
        src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
        body = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
        body = re.sub(r'<style\b[^>]*>.*?</style>', '', body, flags=re.S | re.I)
        text = strip_tags(body)
        if not detect_classical(text):
            continue
        dw = parse_dict(src, 'DICT_WORDS')
        if not dw:
            continue
        for d in dw:
            w = d.get('w', '')
            if w in TRIVIAL_EXT:
                print('  %-46s 字形题 w=%s q=%s' % (fn, w, (d.get('q', '')[:30])))


if __name__ == '__main__':
    main()
