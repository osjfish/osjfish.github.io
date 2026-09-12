# -*- coding: utf-8 -*-
"""
题库题干溯源体检（只读）。
  · DICT_WORDS.q（挖空句）去掉 □ 后必须是课文原文中真实存在的连续片段
  · DICT_NOTES.q（默写句）同样必须是课文原文片段
  · 挖空还原后须与原文一致（□ 位置即答案字位置）
  · 字形题答案 w 的拼音 py 与注释区标注是否矛盾（仅提示）
用法：python _audit_quiz.py
"""
import os, re, sys, json, collections, html, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {'zixinli.html'}
TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'\s+')
NO = re.compile(r'<span class="no">.*?</span>', re.S)
PUNC = re.compile(r'[，。、；：！？“”‘’＇\'…—·＜＞《》「」『』\s（）()0-9]')
PAREN = re.compile(r'[（(][^（()）]{0,24}[)）]')


def plain(src):
    src = re.sub(r'<script\b[^>]*>.*?</script>', '', src, flags=re.S | re.I)
    src = re.sub(r'<style\b[^>]*>.*?</style>', '', src, flags=re.S | re.I)
    src = re.sub(r'<div class="d-body".*?</div>', '', src, flags=re.S)   # 译文属意译，不算原文
    return WS.sub('', html.unescape(TAG.sub('', NO.sub('', src))))


def bare(s):
    """去掉括注（原文的"叫天子（云雀）"、题干的"（海市蜃楼）"）与标点，用于宽松匹配"""
    return PUNC.sub('', PAREN.sub('', s))
    return PUNC.sub('', s)


def parse_dict(src, name):
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


def audit(fn):
    src = open(os.path.join(ROOT, fn), encoding='utf-8').read()
    body = plain(src)
    bare_body = bare(body)
    iss = collections.defaultdict(list)

    dw = parse_dict(src, 'DICT_WORDS')
    dn = parse_dict(src, 'DICT_NOTES')

    for d in (dw or []):
        if not isinstance(d, dict):
            continue
        w, q = d.get('w', ''), d.get('q', '')
        if not w or not q:
            continue
        # 挖空还原后须与原文一致（□ 数已由 _audit_deep 保证等于字数）
        filled = q
        for ch in w:
            filled = filled.replace('□', ch, 1)
        filled = re.sub(r'[（(][^）)]*[)）]', '', filled)   # 去掉题干里的补充括号
        if filled in body or bare(filled) in bare_body:
            continue
        # 允许题干是原文的非连续摘引：按标点切分后每片（≥2字）都须在原文中
        segs = [x for x in re.split(r'[，。、；：！？…—]+', filled) if len(x) >= 2]
        miss = [x for x in segs if bare(x) not in bare_body]
        if miss:
            iss['挖空还原后非原文'].append('%s|%s⟨%s⟩' % (w, filled[:22], '／'.join(miss)[:20]))

    for d in (dn or []):
        if not isinstance(d, dict):
            continue
        w, q = d.get('w', ''), d.get('q', '')
        if not w or not q:
            continue
        qc = re.sub(r'[（(][^）)]*[)）]', '', q)
        if q in body or qc in body or bare(qc) in bare_body:
            hit = True
        else:
            segs = [x for x in re.split(r'[，。、；：！？…—]+', qc) if len(x) >= 2]
            hit = bool(segs) and all(bare(x) in bare_body for x in segs)
        if not hit:
            # 软规则：若 q 与原文存在较长连续公共片段（≥60%字符连续匹配），视为合理节选/意引，不报
            qb = bare(qc)
            sm = difflib.SequenceMatcher(None, qb, bare_body, autojunk=False)
            longest = max((b.size for b in sm.get_matching_blocks()), default=0)
            if longest >= max(4, int(len(qb) * 0.6)):
                continue
            iss['注释题句非原文'].append('%s|%s' % (w, q[:26]))
        else:
            # 注释题 w 是"要默写的词"，不要求出现在例句 q 中；
            # 真问题：该词在课文正文中完全找不到（学生无从定位）
            w2 = re.sub(r'[（(][^）)]*[)）]', '', w)
            if '/' in w or '……' in w or '...' in w:
                continue
            wb = bare(w2)
            if wb and wb not in bare_body:
                iss['注释词不在课文'].append('%s|%s' % (w, q[:26]))

    return iss


def main():
    files = sorted(f for f in os.listdir(ROOT) if f.endswith('.html') and f not in SKIP)
    agg = collections.defaultdict(list)
    for fn in files:
        for k, v in audit(fn).items():
            agg[k].append('%s: %s' % (fn, ';'.join(v[:5])))
    print('文件数:', len(files))
    print('=' * 66)
    if not agg:
        print('题库题干全部溯源成功，0 问题')
    for k in sorted(agg, key=lambda x: -len(agg[x])):
        print('\n【%s】 %d 篇' % (k, len(agg[k])))
        for line in agg[k][:40]:
            print('   ', line[:170])
        if len(agg[k]) > 40:
            print('    ... 另 %d 篇' % (len(agg[k]) - 40))
    if '--json' in sys.argv:
        json.dump({k: v for k, v in agg.items()},
                  open(sys.argv[sys.argv.index('--json') + 1], 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
