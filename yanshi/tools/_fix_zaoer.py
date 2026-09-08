# -*- coding: utf-8 -*-
"""修《枣儿》：删背影残留题库script、kai块改正、按钮改标准data-mode"""
import re

F = 'zaoer-sunhong.html'
raw = open(F, 'rb').read()
s = raw.decode('utf-8')
crlf = '\r\n' if '\r\n' in s else '\n'

# 1) 删除《背影》残留题库 script 块（含特征句"父亲的差使也交卸"）
m3 = re.search(r'<script>\s*var DICT_WORDS = \[[^"]*"w": "卸".*?</script>', s, re.S)
assert m3, '未找到背影残留块'
s = s.replace(m3.group(0), '<script>/* 已删除《背影》残留题库 */</script>')

# 2) kai 块改正
old_kai = '<div class="kai">《背影》</div>%s  <div>朱自清 · 现代 · 出自《背影》</div>' % crlf
new_kai = '<div class="kai">《枣儿》</div>%s  <div>孙鸿 · 当代 · 选自《剧本》1999年第1期</div>' % crlf
assert old_kai in s, 'kai块未匹配'
s = s.replace(old_kai, new_kai)

# 3) 按钮 onclick → 标准 data-mode
pairs = [
    ('<button class="p-btn" onclick="startDict(\'words\',5)">', '<button data-mode="word" data-rand="5">'),
    ('<button class="p-btn" onclick="startDict(\'words\',0)">', '<button data-mode="word" data-all="1">'),
    ('<button class="p-btn" onclick="startDict(\'notes\',5)">', '<button data-mode="note" data-rand="5">'),
    ('<button class="p-btn" onclick="startDict(\'notes\',0)">', '<button data-mode="note" data-all="1">'),
]
for old, new in pairs:
    assert old in s, '按钮未匹配: ' + old
    s = s.replace(old, new)

open(F, 'wb').write(s.encode('utf-8'))
print('枣儿修复完成')

# 验证
s2 = open(F, 'rb').read().decode('utf-8')
print('data-mode数:', len(re.findall(r'data-mode="(word|note)"', s2)))
print('startDict残留:', s2.count('startDict'))
print('背影残留:', s2.count('交卸'))
print('kai:', re.search(r'<div class="kai">([^<]*)</div>\s*<div>([^<]*)</div>', s2).groups())
