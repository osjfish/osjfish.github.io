# -*- coding: utf-8 -*-
import re, os, json

files = {
    '文言文': r'D:\App\Apps\hezhongshishou-jiyun.html',
    '古诗词(长)': r'D:\App\Apps\baixuegesongwupanguanguijing-censhen.html',
    '现代文(长)': r'D:\App\Apps\guduzhilv-caowenxuan.html',
    '元曲': r'D:\App\Apps\tianjingshaqiusi-mazhiyuan.html',
    '文言文(长)': r'D:\App\Apps\zhouyafujunxiliu-simaqian.html',
    '现代文(鲁迅)': r'D:\App\Apps\congbaicaoyuandaosanweishuwu-luxun.html',
}

checks = ['btnAll', 'btnRecite', 'btnPrint', 'verseList', 'fulltext',
          'annoPopup', 'dictate', 'topBtn', 'mediaF1', 'mediaF2',
          'class="wrap"', 'nav-in', 'hero-title', 'part-head',
          'https://player.bilibili.com']

all_ok = True
for label, path in files.items():
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    print('=== %s (%s) ===' % (label, os.path.basename(path)))
    print('  大小: %d 字符' % len(content))
    missing = [c for c in checks if c not in content]
    if missing:
        print('  缺失: %s' % missing)
        all_ok = False
    else:
        print('  关键元素: 全部OK')
    anno_count = content.count('class="anno-word"')
    print('  注释数: %d' % anno_count)
    dw = re.search(r'var DICT_WORDS = (\[.*?\]);', content, re.DOTALL)
    dn = re.search(r'var DICT_NOTES = (\[.*?\]);', content, re.DOTALL)
    if dw:
        words = json.loads(dw.group(1))
        print('  字形题: %d' % len(words))
    if dn:
        notes = json.loads(dn.group(1))
        print('  注释/词语题: %d' % len(notes))
    # Check part-head h3 line-height
    if 'line-height:1' in content and 'margin:0' in content:
        print('  part-head样式: OK')
    else:
        print('  part-head样式: 检查')
        all_ok = False
    print()

print('=== 总结 ===')
print('全部关键元素检查: %s' % ('通过' if all_ok else '有缺失'))
