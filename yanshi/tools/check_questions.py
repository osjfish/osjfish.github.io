# -*- coding: utf-8 -*-
import re, json, sys

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    h = f.read()

# Extract DICT_WORDS
m = re.search(r'var DICT_WORDS = (\[.*?\]);', h, re.DOTALL)
words = json.loads(m.group(1))
m2 = re.search(r'var DICT_NOTES = (\[.*?\]);', h, re.DOTALL)
notes = json.loads(m2.group(1))

print('Word questions:', len(words))
print('Note questions:', len(notes))

# 字形题四条硬规则
leak = [x for x in words if any(c in x['q'] for c in x['w'])]
nbox = [x for x in words if x['q'].count('\u25a1') != len(x['w'])]
npy  = [x for x in words if len(x['py'].split()) != len(x['w']) and len(x['py'].split()) != 1]
ntip = [x for x in words if not x.get('tip') or x['tip'] == x['w']]

print('Leak (answer char in question):', len(leak), leak if leak else '')
print('Box count mismatch:', len(nbox), nbox if nbox else '')
print('Pinyin count mismatch:', len(npy), npy if npy else '')
print('Tip missing/equal:', len(ntip), ntip if ntip else '')

# Check notes format
bad_notes = [n for n in notes if not all(k in n for k in ['w','a','q'])]
print('Bad note format:', len(bad_notes))
