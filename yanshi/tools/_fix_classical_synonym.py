# -*- coding: utf-8 -*-
"""
文言「常见词纯同义注」收口（第二遍）——精确删除。
原则（用户 2026-09-13）：文言注释是否保留，看「生僻程度 + 重要程度」；
      常见词若只是现代汉语同义对译（X=Y，词性不变、无特殊用法），则删除；
      但保留涉及「词类活用 / 古今异义 / 通假 / 虚词用法 / 代词 / 特殊句式」的条目。

实现：按 (文件, 词, 注释子串) 精确匹配 anno-word span 删除（保留文字），
      同步清理 DICT_NOTES 中对应「纯同义」条目（按 w + a 子串匹配），
      绝不误删同词的其他合法义项（如 鸿门宴 下=下车 活用 保留）。
用法：python _fix_classical_synonym.py [--apply]
"""
import os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANNO_RE = re.compile(r'(<span class="anno-word"[^>]*data-note="([^"]*)"[^>]*>)(.*?)(</span>)', re.S)
TAG_STRIP = re.compile(r'<[^>]+>')

# (词, 注释子串) —— 子串命中即视为该纯同义注
REMOVE = {
    'changhenge-baijuyi.html': [('下', '向下'), ('里', '里面'), ('中', '里面')],
    'dujingmensongbie-libai.html': [('山', '山峦')],
    'pipaxing-baijuyi.html': [('往往', '常常')],
    'yujiaaoqiusi-fanzhongyan.html': [('里', '之中、里面')],
    'hongmenyan-shiji.html': [
        ('下', '脚下、下面'), ('下', '……的下面'), ('上', '上面'),
        ('有', '占有'), ('来', '来'), ('我', '我'),
    ],
    'ailianshuo-zhoudunyi.html': [('不', '表示否定')],
    'zhuangziyuhuiziyouyuhaoliang-zhuangzi.html': [('上', '上面'), ('鱼', '鱼'), ('我', '我')],
    'deduoduozhushidaoguazhu-mengzi.html': [('多', '充足')],
    'loushiming-liuyuxi.html': [('有', '有')],
    'sunquanquanxue-simaguang.html': [('过', '经过')],
}


def process(fn, apply=True):
    p = os.path.join(ROOT, fn)
    if not os.path.exists(p):
        print('!! 缺失', fn)
        return
    src = open(p, encoding='utf-8').read()
    pairs = REMOVE[fn]
    words = {w for w, _ in pairs}
    stat = collections.Counter()

    def repl(m):
        note, wtag = m.group(2), m.group(3)
        w = TAG_STRIP.sub('', wtag).strip()
        n = (note or '').strip()
        if w in words and any(sub in n for _, sub in pairs if _ == w):
            stat['注释'] += 1
            return wtag  # 去掉 span，保留文字
        return m.group(0)

    new = ANNO_RE.sub(repl, src)

    # 同步清理 DICT_NOTES（仅删该词的「纯同义」条目：w 命中 且 a 含对应子串）
    def clean_notes(m):
        head, body, tail = m.group(1), m.group(2), m.group(3)
        for blk in re.finditer(r'\{([^{}]*)\}', body):
            inner = blk.group(1)
            d = {}
            for k in ('w', 'a'):
                mm = re.search(r"""['"]?%s['"]?\s*:\s*['"](.*?)['"]""" % k, inner, re.S)
                if mm:
                    d[k] = mm.group(1)
            w = d.get('w')
            a = d.get('a', '')
            if w and any(sub in a for _, sub in pairs if _ == w):
                stat['注释题'] += 1
                body = body.replace(blk.group(0), '', 1)
        body = re.sub(r',\s*\]', ']', body)
        body = re.sub(r'\[\s*,', '[', body)
        body = re.sub(r',\s*,', ',', body)
        return head + body + tail

    new = re.sub(r'(DICT_NOTES\s*=\s*)(\[.*?\])(;)', clean_notes, new, flags=re.S)

    if new != src and apply:
        open(p, 'w', encoding='utf-8').write(new)
    return stat


def main(apply=False):
    tot = collections.Counter()
    for fn in sorted(REMOVE):
        s = process(fn, apply)
        tot.update(s)
        print('%-52s 注释-%d 注释题-%d' % (fn, s['注释'], s['注释题']))
    print('\n合计:', dict(tot))
    print('（dry-run，未写盘）' if not apply else '已写入')


if __name__ == '__main__':
    main(apply='--apply' in sys.argv)
