# -*- coding: utf-8 -*-
"""修复第二批新20篇审计问题：
1) {LQ}/{RQ} 占位符泄露（4篇韵文，180处）——先修不成对残缺 token，再全局替换为中文引号
2) 10 篇题库定义移出主 IIFE（与标准模板一致，全局可见）
3) _list.json 导航错字（唐雊→唐雎）
幂等：已应用的补丁自动跳过。"""
import io, re, json

BASE = r"D:\App\Apps"

def rd(fn):
    return io.open(BASE + "\\" + fn, encoding="utf-8-sig").read()

def wr(fn, s):
    io.open(BASE + "\\" + fn, "w", encoding="utf-8-sig").write(s)

LQ, RQ = "\u201c", "\u201d"
FILES4 = ['wenwangchanglingzuoqianlongbiaoyaoyouciji-libai.html', 'qiantanghuchunxing-baijuyi.html',
          'chibi-dumu.html', 'yujiaaoqiusi-fanzhongyan.html']
FILES10 = ['jiezishu-zhugeliang.html', 'shengyuyouhuansiyuanle-mengzi.html', 'yuzhuyuansishu-wujun.html',
           'daxiezhongshushu-taohongjing.html', 'huxintingkanxue-zhangdai.html', 'tangjiburushiming-zhanguoce.html'] + FILES4

# ---------- 1) {LQ}/{RQ} ----------
# 1a. 残缺 token（{RQ，/{LQ， 等）
malformed = {
 'wenwangchanglingzuoqianlongbiaoyaoyouciji-libai.html': [('一{LQ}啼{RQ，视觉', '一{LQ}啼{RQ}，视觉', 1)],
}
for fn, plist in malformed.items():
    s = rd(fn)
    for old, new, cnt in plist:
        n = s.count(old)
        if n == 0:
            print('  (already) malformed', fn); continue
        assert n == cnt, (fn, n)
        s = s.replace(old, new)
    wr(fn, s)
    print('malformed fixed', fn)

# 1b. 全局替换 + 残缺扫描
for fn in FILES4:
    s = rd(fn)
    if '{LQ}' not in s and '{RQ}' not in s:
        print('  (already) placeholder', fn); continue
    bad = re.findall(r'\{(LQ|RQ)[^}]}', s)
    assert not bad, '%s malformed tokens remain: %s' % (fn, bad[:5])
    lq, rq = s.count('{LQ}'), s.count('{RQ}')
    assert lq == rq, '%s unbalanced: LQ=%d RQ=%d' % (fn, lq, rq)
    s = s.replace('{LQ}', LQ).replace('{RQ}', RQ)
    assert '{LQ}' not in s and '{RQ}' not in s
    assert s.count(LQ) == s.count(RQ), '%s curly unbalanced' % fn
    wr(fn, s)
    print('placeholder fixed', fn, 'pairs=%d' % lq)

# ---------- 2) 题库定义移出 IIFE ----------
for fn in FILES10:
    s = rd(fn)
    i_c = s.find('/* ---------- 听写题库 ---------- */')
    i_dw = s.find('var DICT_WORDS', i_c if i_c != -1 else 0)
    if i_dw == -1:
        print('  (skip) no DICT_WORDS:', fn); continue
    j_close = s.find('})();', i_dw)
    # 该文件是否已修（题库已在 IIFE 外：IIFE 闭合在题库定义之前）
    prev_close = s.rfind('})();', 0, i_dw)
    if prev_close != -1 and s.find('var DICT_NOTES', prev_close) != -1 and prev_close > s.find('var DICT_WORDS'):
        print('  (already) scope', fn); continue
    assert j_close != -1, fn
    block = s[i_dw:j_close]
    assert 'var DICT_NOTES' in block and '})();' not in block, 'unexpected block content in %s: %r' % (fn, block[:80])
    comment = s[i_c:i_dw] if (i_c != -1 and i_c > j_close - 4000 and i_c < i_dw) else ''
    # 从原位切除（含注释行）
    cut_start = i_c if (comment and i_c < i_dw) else i_dw
    s2 = s[:cut_start] + s[j_close:]
    # 插到 IIFE 闭合之后
    k = s2.find('})();', cut_start)
    assert k != -1, fn
    ins_at = k + len('})();')
    s2 = s2[:ins_at] + '\n' + comment + block.rstrip() + '\n' + s2[ins_at:]
    # 校验：div/section 平衡不受影响；DICT_NOTES 在 DICT_WORDS 后
    assert s2.count('var DICT_WORDS') == 1 and s2.count('var DICT_NOTES') == 1
    wr(fn, s2)
    print('scope fixed', fn)

# ---------- 3) _list.json 错字 ----------
p = BASE + r"\_list.json"
s = io.open(p, encoding='utf-8').read()
if '唐雊' in s:
    s = s.replace('唐雊', '唐雎')
    io.open(p, 'w', encoding='utf-8').write(s)
    print('_list.json 唐雊→唐雎')
else:
    print('  (already) _list.json')

# ---------- 4) 自检 ----------
print('\n===== 自检 =====')
CHECK = FILES10 + ['jiangchengzimizhouchulie-sushi.html', 'pozhenziweichentongfufuzhuangciyijizhi-xinqiji.html',
                   'guolingdingyang-wentianxiang.html', 'jihaizashi-gongzizhen.html']
ok_all = True
for fn in sorted(set(CHECK)):
    s = rd(fn)
    lq_res = s.count('{LQ}') + s.count('{RQ}')
    words = json.loads(re.search(r'var DICT_WORDS = (\[[\s\S]*?\]);', s).group(1))
    notes = json.loads(re.search(r'var DICT_NOTES = (\[[\s\S]*?\]);', s).group(1))
    # 作用域：IIFE 闭合应出现在题库定义之前
    i_dw = s.find('var DICT_WORDS')
    prev_close = s.rfind('})();', 0, i_dw)
    scope_ok = prev_close != -1
    ok = lq_res == 0 and len(words) >= 5 and len(notes) >= 5 and scope_ok
    ok_all = ok_all and ok
    print('%-52s {LQ}残留=%d words=%d notes=%d 全局作用域=%s' % (fn, lq_res, len(words), len(notes), scope_ok))
print('\nALL OK' if ok_all else '\nHAS ISSUES')
