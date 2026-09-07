# -*- coding: utf-8 -*-
"""八上 24 篇体检·第一批修复（小缺陷五处）"""
import io, sys

BASE = r'D:\App\Apps\yanshi'

def rw(fn, pairs):
    p = BASE + '\\' + fn
    h = open(p, 'rb').read().decode('utf-8')
    for old, new, cnt in pairs:
        n = h.count(old)
        assert n == cnt, 'ASSERT %s: count=%d expect=%d for %r...' % (fn, n, cnt, old[:60])
        h = h.replace(old, new)
    open(p, 'wb').write(h.encode('utf-8'))
    print('OK', fn, '(%d rules)' % len(pairs))

# 1) 得道多助：卡片补逗号与「也」（已在上一轮应用成功）

# 2) 富贵不能淫：卡片补 11 处标点（用 anno-word 锚定，避开 acc 积累区）
rw('fuguibunengyin-mengzi.html', [
    ('>往送之门</span><span class="anno-word"', '>往送之门</span>，<span class="anno-word"', 1),
    ('>戒之曰</span><span class="anno-word"', '>戒之曰</span>：“<span class="anno-word"', 1),
    ('>往之女家</span><span class="anno-word"', '>往之女家</span>，<span class="anno-word"', 1),
    ('>必敬必戒</span><span class="anno-word"', '>必敬必戒</span>，<span class="anno-word"', 1),
    ('>以顺为正者</span><span class="anno-word"', '>以顺为正者</span>，<span class="anno-word"', 1),
    ('>居天下之广居</span><span class="anno-word"', '>居天下之广居</span>，<span class="anno-word"', 1),
    ('>立天下之正位</span><span class="anno-word"', '>立天下之正位</span>，<span class="anno-word"', 1),
    ('>得志</span><span class="anno-word"', '>得志</span>，<span class="anno-word"', 1),
    ('>不得志</span><span class="anno-word"', '>不得志</span>，<span class="anno-word"', 1),
    ('>富贵不能淫</span><span class="anno-word"', '>富贵不能淫</span>，<span class="anno-word"', 1),
    ('>贫贱不能移</span><span class="anno-word"', '>贫贱不能移</span>，<span class="anno-word"', 1),
])

# 3) 行路难：逗号注解 span 清理
rw('xinglunan-libai.html', [
    # 第 1 处：span + 字面逗号 叠用 → 只留字面逗号
    ('<span class="anno-word" data-note="逗号">，</span>，', '，', 1),
    # 其余 7 处：span 换回字面逗号
    ('<span class="anno-word" data-note="逗号">，</span>', '，', 7),
])

# 4) 永久的生命：小牛犊释义泄漏修复
rw('yongjiudeshengming-yanwenjing.html', [
    ('{"w": "小牛犊", "a": "小牛", "q": "山坡上那些小牛犊"}',
     '{"w": "小牛犊", "a": "幼小的牛。犊（dú），小牛", "q": "山坡上那些小牛犊"}', 1),
])

# 5) 回忆我的母亲：data-note 嵌套 span 拍平
rw('huiyiwodemuqin-zhude.html', [
    ('data-note="习惯了劳动，不劳动就<span class="anno-word" data-note="这里指不适应、不习惯">不舒服</span>"',
     'data-note="习惯了劳动，不劳动就不舒服"', 1),
])

print('ALL DONE')
