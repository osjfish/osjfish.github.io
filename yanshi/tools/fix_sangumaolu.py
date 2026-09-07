# -*- coding: utf-8 -*-
"""Fix LQ/RQ and check verse count in 三顾茅庐"""
import re

p = r'D:\App\Apps\yanshi\sangumaolu-luoguanzhong.html'
with open(p, 'r', encoding='utf-8') as f:
    h = f.read()

# Fix LQ/RQ literals
h = h.replace('" + LQ + "', '\u201c')
h = h.replace('" + RQ + "', '\u201d')

# Check verse count
verses = re.findall(r'<div class="verse" id="p\d+"', h)
print(f"Verse divs: {len(verses)}")
for v in verses:
    print(f"  {v}")

# Check for corrupted HTML at split points
for pid in ['p3', 'p9', 'p15']:
    pos = h.find(f'id="{pid}"')
    if pos > 0:
        print(f"\n{pid} found at position {pos}")
        print(f"Context: {repr(h[pos-30:pos+80])}")
    else:
        print(f"\n{pid} NOT FOUND!")

with open(p, 'w', encoding='utf-8') as f:
    f.write(h)
print("\nFixed LQ/RQ and saved.")
