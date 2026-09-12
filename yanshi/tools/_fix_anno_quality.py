# -*- coding: utf-8 -*-
"""
注释清理：移除「不合理注释」——本学段学生已掌握、或注释无信息量的条目。
原则（用户）：注释应注释课文学段的学生不理解或需要掌握的字词。

保留（不删）：
- 多音字/易错音（着 zhuó、没 mò、了 liǎo）
- 古今异义（黄鹤楼「去」=离开）
- 语境义/修辞（黄河颂「你」=拟人、雨的四季「自然」=不勉强、秋天=情感载体）
- 书面语词（寻觅、小径、舟、益、娘子）
删除：
- 注释词本身是标点（、=顿号、，=逗号）
- 注释等于词（有=有、鱼=鱼、鸟=鸟、人=人、姓氏=姓氏）
- 现代文里人人都会的词（喜欢、结束、工作、突然、悄悄、明白、完全、然后、慢慢、母亲=妈妈…）

同时同步清理 DICT_NOTES 中对应条目，避免「注释默写」考到已无注释的词。
用法：python _fix_anno_quality.py [--apply]
"""
import os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANNO_RE = re.compile(r'(<span class="anno-word"[^>]*data-note="([^"]*)"[^>]*>)(.*?)(</span>)', re.S)
TAG_STRIP = re.compile(r'<[^>]+>')

REMOVE = {
    # --- 注释词是标点 ---
    'fuguibunengyin-mengzi.html': {'、'},
    'yanmentaishouxing-lihe.html': {'，'},
    'yujiaao-liqingzhao.html': {'，', '。'},
    # --- 注释等于词（无信息量） ---
    'beimingyouyu-zhuangzi.html': {'有', '鱼', '鸟'},
    'huxintingkanxue-zhangdai.html': {'姓氏'},
    'yugongyishan-liezi.html': {'在', '有'},
    'zhouyafujunxiliu-simaqian.html': {'人'},
    # --- 现代文过度注释（常见词） ---
    'beiying-zhuziqing.html': {'努力', '肥胖'},
    'bianselong-qikefu.html': {'喜欢'},
    'daishangtadeyanjing-liucixin.html': {'花', '结束', '工作', '世界'},
    'dongwuxiaotan-kanglaodelunzi.html': {'工作'},
    'haiyan-gaoerji.html': {'肥胖'},
    'huanghelou-cuihao.html': {'树'},
    'huanghesong-guangweiran.html': {'学习'},
    'jinsehua-taigeer.html': {'突然'},
    'laowang-yangjiang.html': {'悄悄', '明白'},
    'maitanweng-baijuyi.html': {'中'},
    'mao-zhengzhenduo.html': {'肥胖', '立刻'},
    'meilideyanse-aifujuli.html': {'完全'},
    'woaizhetudi-aiqing.html': {'然后'},
    'wokan-mudan.html': {'悄悄', '慢慢'},
    'xiangchou-yuguangzhong.html': {'母亲'},
}


def process(fn, apply=True):
    p = os.path.join(ROOT, fn)
    src = open(p, encoding='utf-8').read()
    words = REMOVE[fn]
    stat = collections.Counter()

    def repl(m):
        w = TAG_STRIP.sub('', m.group(3)).strip()
        if w in words:
            stat['注释'] += 1
            return m.group(3)  # 去掉 span，保留文字
        return m.group(0)

    new = ANNO_RE.sub(repl, src)

    # 同步清理 DICT_NOTES 中对应词条
    def clean_notes(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        n0 = len(body)
        for w in words:
            body = re.sub(r"\{[^{}]*['\"]w['\"]\s*:\s*['\"]%s['\"][^{}]*\}\s*,?" % re.escape(w), '', body)
        stat['注释题'] += (n0 - len(body)) and 1 or 0
        body = re.sub(r',\s*\]', ']', body)
        body = re.sub(r'\[\s*,', '[', body)
        return head + body + tail

    new = re.sub(r'(DICT_NOTES\s*=\s*)(\[.*?\])(;)', clean_notes, new, flags=re.S)

    if new != src and apply:
        open(p, 'w', encoding='utf-8').write(new)
    return stat


def main(apply=False):
    tot = collections.Counter()
    for fn in sorted(REMOVE):
        if not os.path.exists(os.path.join(ROOT, fn)):
            print('!! 缺失', fn)
            continue
        s = process(fn, apply)
        tot.update(s)
        print('%-52s 注释-%d 注释题-%d' % (fn, s['注释'], s['注释题']))
    print('\n合计:', dict(tot))
    print('（dry-run，未写盘）' if not apply else '已写入')


if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
