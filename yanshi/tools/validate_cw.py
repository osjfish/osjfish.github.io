# -*- coding: utf-8 -*-
"""统一校验五篇自选自选课件：听写库不泄题 + HTML 结构完整 + 注释三不。"""
import io, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data_taohuayuanji, data_zuiwengtingji, data_chun, data_zitengluopubu, data_denglong

MODS = {
    '桃花源记': (data_taohuayuanji, r'D:\App\Apps\taohuayuanji-taoyuanming.html'),
    '醉翁亭记': (data_zuiwengtingji, r'D:\App\Apps\zuiwengtingji-ouyangxiu.html'),
    '春':       (data_chun, r'D:\App\Apps\chun-zhuziqing.html'),
    '紫藤萝瀑布': (data_zitengluopubu, r'D:\App\Apps\zitengluopubu-zongpu.html'),
    '灯笼':     (data_denglong, r'D:\App\Apps\denglong-wubojie.html'),
}

REQ_IDS = ['bg', 'jielu', 'app', 'acc', 'practice', 'dictate', 'fulltext']
all_ok = True

def check_words(words):
    leak = []
    box = []
    pin = []
    for d in words:
        w, py, q = d.get('w', ''), d.get('py', ''), d.get('q', '')
        if w and w in q:
            leak.append(w)
        if q.count('□') != len(w):
            box.append((w, q.count('□')))
        if len(py.split()) != len(w):
            pin.append((w, py))
    return leak, box, pin

for name, (mod, html_path) in MODS.items():
    print('=' * 64)
    print('【%s】' % name)
    leak, box, pin = check_words(mod.DICT_WORDS)
    print('  WORDS=%d  NOTES=%d' % (len(mod.DICT_WORDS), len(mod.DICT_NOTES)))
    print('  LEAK  =', leak)
    print('  BOX   =', box)
    print('  PINYIN=', pin)

    # 附加：DICT_NOTES 为「词语」库，答项是释义 a，例句 q 必含原词 w；
    # 真正的泄题是「释义 a 出现在例句 q 中」。
    n_leak = [n['w'] for n in mod.DICT_NOTES if n.get('a') and n.get('a') in n.get('q', '')]
    if n_leak:
        print('  NOTES_LEAK =', n_leak)

    h = io.open(html_path, encoding='utf-8').read()
    missing = [i for i in REQ_IDS if 'id="%s"' % i not in h]
    leftover = h.count('[[')
    anno = len(re.findall(r'class="anno-word"', h))
    empty_note = len(re.findall(r'data-note=""', h))
    rot = []
    for m in re.finditer(r'<span class="anno-word" data-note="([^"]*)">([^<]*)</span>', h):
        note, word = m.group(1), m.group(2)
        if note == word:
            rot.append(word)
    print('  MISSING_IDS=%s  LEFT_BRACKET=%d  anno=%d  empty_note=%d  rotate=%d'
          % (missing, leftover, anno, empty_note, len(rot)))
    if rot:
        print('    rotate_words =', rot)

    ok = not (leak or box or pin or n_leak or missing or leftover or empty_note or rot)
    all_ok = all_ok and ok
    print('  RESULT:', 'OK' if ok else 'FAIL')

print('=' * 64)
print('ALL_OK =', all_ok)
