# -*- coding: utf-8 -*-
"""定点诊断 8 篇：注释题 w 是否真在正文、q 是否真非原文（意引豁免之外）。"""
import os, re, html, difflib

ROOT = r'D:\App\Apps\yanshi'
FILES = ['chuangzaoxuanyan-taoxingzhi.html', 'liulaolaojindaguanyuan-caoxueqin.html',
         'lunjiaoyang-lihachiaofu.html', 'tianxiadiyilou-hejiping.html',
         'yuwosuoyuye-mengzi.html', 'baiyanglizan-maodun.html',
         'pipaxing-baijuyi.html', 'zaoer-sunhong.html']

TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')
NO = re.compile(r'<span class="no">.*?</span>', re.S)
PUNC = re.compile(r'[，。、；：！？“”‘’＇\'…—·＜＞《》「」『』\s（）()0-9]')
PAREN = re.compile(r'[（(][^（()）]{0,24}[)）]')


def plain(src):
    src = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
    src = re.sub(r'<style\b[^>]*>.*?</style>', '', src, flags=re.S | re.I)
    src = re.sub(r'<div class="d-body".*?</div>', '', src, flags=re.S)
    return WS.sub('', html.unescape(TAG.sub('', NO.sub('', src))))


def bare(s):
    return PUNC.sub('', PAREN.sub('', s))


def parse_dict(src, name):
    m = re.search(r'%s\s*=\s*(\[.*?\])\s*;' % name, src, re.S)
    if not m:
        return []
    out = []
    for blk in re.finditer(r'\{([^{}]*)\}', m.group(1)):
        d = {}
        for k in ('w', 'a', 'q', 'py', 'tip'):
            mm = re.search(r"""['"]?%s['"]?\s*:\s*(['"])(.*?)\1""" % k, blk.group(1), re.S)
            if mm:
                d[k] = mm.group(2)
        if d:
            out.append(d)
    return out


for fn in FILES:
    src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
    body = plain(src)
    bare_body = bare(body)
    dn = parse_dict(src, 'DICT_NOTES')
    print('=' * 70)
    print(fn)
    print('-' * 70)
    for d in dn:
        w = d.get('w', '')
        q = d.get('q', '')
        if not w or not q:
            continue
        qc = re.sub(r'[（(][^）)]*[)）]', '', q)
        wb = bare(re.sub(r'[（(][^）)]*[)）]', '', w))
        qb = bare(qc)
        qhit = q in body or qc in body or qb in bare_body
        whit = (wb in bare_body) if wb else True
        flag = ''
        if not qhit:
            sm = difflib.SequenceMatcher(None, qb, bare_body, autojunk=False)
            longest = max((b.size for b in sm.get_matching_blocks()), default=0)
            if longest < max(4, int(len(qb) * 0.6)):
                flag += ' [句非原文]'
        if not whit and '/' not in w and '…' not in w and '...' not in w:
            flag += ' [词不在课文]'
        if flag:
            print('  w=%r q=%r%s' % (w, q, flag))
            print('    qhit=%s  whit=%s  wb=%r' % (qhit, whit, wb))
            if wb:
                idx = bare_body.find(wb)
                if idx >= 0:
                    print('    词在正文@%d: …%s…' % (idx, bare_body[max(0, idx - 12):idx + len(wb) + 12]))
                else:
                    print('    词确不在正文(bare_body)')
            # 句的最长连续匹配
            sm = difflib.SequenceMatcher(None, qb, bare_body, autojunk=False)
            longest = max((b.size for b in sm.get_matching_blocks()), default=0)
            print('    句最长连续匹配=%d / 句长=%d (阈值%d)' % (longest, len(qb), max(4, int(len(qb) * 0.6))))
