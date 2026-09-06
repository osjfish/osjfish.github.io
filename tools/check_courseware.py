# -*- coding: utf-8 -*-
"""课件结构自检"""
import sys, re

path = sys.argv[1]
h = open(path, encoding='utf-8').read()

checks = {
    'btnAll': 'id="btnAll"' in h,
    'btnRecite': 'id="btnRecite"' in h,
    'btnPrint': 'id="btnPrint"' in h,
    'verseList': 'id="verseList"' in h,
    'fulltext': 'id="fulltext"' in h,
    'topBtn': 'id="topBtn"' in h,
    'annoPopup': 'id="annoPopup"' in h,
    'dictate': 'id="dictate"' in h,
    'DICT_WORDS': 'var DICT_WORDS' in h,
    'DICT_NOTES': 'var DICT_NOTES' in h,
    'acc-sub CSS': '.acc-sub' in h,
    'mediaF1': 'id="mediaF1"' in h,
    'mediaF2': 'id="mediaF2"' in h,
    'wrap class': 'class="wrap"' in h,
    'nav-in': 'class="nav-in"' in h,
    'hero-title': 'class="hero-title"' in h,
    'part-head h3 line-height': 'line-height:1' in h,
}

# Check for English quotes in content (not in HTML tags/attributes)
# Extract text between tags, check for straight double quotes used as Chinese quotes
text_only = re.sub(r'<[^>]+>', '', h)
# Remove JSON data
text_only = re.sub(r'var DICT.*', '', text_only, flags=re.DOTALL)
straight_quotes_in_text = text_only.count('"')

# Check word dict format
import json
m = re.search(r'var DICT_WORDS = (\[.*?\]);', h, re.DOTALL)
word_ok = False
if m:
    try:
        words = json.loads(m.group(1))
        word_ok = True
        leak = [x for x in words if any(c in x['q'] for c in x['w'])]
        nbox = [x for x in words if x['q'].count('\u25a1') != len(x['w'])]
        npy = [x for x in words if len(x['py'].split()) != len(x['w']) and len(x['py'].split()) != 1]
        ntip = [x for x in words if not x.get('tip') or x['tip'] == x['w']]
        print('  words leak:', leak)
        print('  words nbox:', nbox)
        print('  words npy:', npy)
        print('  words ntip:', ntip)
    except Exception as e:
        print('  JSON parse error:', e)

print('=== %s ===' % path)
for k, v in checks.items():
    print('  %s: %s' % (k, 'OK' if v else 'FAIL'))
print('  straight quotes in text:', straight_quotes_in_text)
print('  part-head count:', h.count('class="part-head"'))
print('  verse count:', h.count('class="verse"'))
print('  file size:', len(h))
