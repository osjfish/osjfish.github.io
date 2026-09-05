# -*- coding: utf-8 -*-
import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else r'D:\App\Apps\maowu-dufu.html'
with open(path, 'r', encoding='utf-8') as f:
    h = f.read()

text = re.sub(r'<[^>]+>', '', h)
text = re.sub(r'https?://\S+', '', text)
ascii_quotes = text.count('"')
print('ASCII quotes in text content:', ascii_quotes)
print('Chinese left quotes:', text.count('\u201c'))
print('Chinese right quotes:', text.count('\u201d'))

for eid in ['btnAll','btnRecite','btnPrint','verseList','fulltext']:
    found = ('id="%s"' % eid) in h
    print('id=%s: %s' % (eid, 'found' if found else 'MISSING'))

print('main.wrap:', 'class="wrap"' in h)
print('nav.nav-in:', 'class="nav-in"' in h)
print(':root --fs:', '--fs:1' in h)

# Check video iframes
iframes = re.findall(r'src="https://player\.bilibili\.com/player\.html\?bvid=([^&]+)', h)
print('Video BVs:', iframes)

# Check practice buttons
print('Practice note buttons:', '随机五组注释' in h, '全部注释' in h)
print('No 词语 buttons:', '随机五组词语' not in h)

# Count verses
verses = re.findall(r'class="verse"', h)
print('Verse cards:', len(verses))

# Count annotations
annos = re.findall(r'class="anno-word"', h)
print('Annotation words:', len(annos))

# Check part-head h3 line-height
print('part-head h3 line-height:1:', 'line-height:1' in h)
