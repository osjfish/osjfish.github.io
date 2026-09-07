# -*- coding: utf-8 -*-
"""Fix corrupted verse divs at split points in 三顾茅庐"""
import re

p = r'D:\App\Apps\yanshi\sangumaolu-luoguanzhong.html'
with open(p, 'r', encoding='utf-8') as f:
    h = f.read()

# Fix corrupted divs: erse" id="pX" -> <div class="verse" id="pX"
for pid in ['p3', 'p9', 'p15']:
    old = f'erse" id="{pid}"'
    new = f'<div class="verse" id="{pid}"'
    count = h.count(old)
    print(f"{pid}: found {count} occurrence(s) of '{old}'")
    h = h.replace(old, new)
    print(f"  Replaced with '{new}'")

# Verify
verses = re.findall(r'<div class="verse" id="p\d+"', h)
print(f"\nVerse divs after fix: {len(verses)}")
for v in verses:
    print(f"  {v}")

# Check for any remaining corrupted patterns
corrupted = re.findall(r'erse" id="p\d+"', h)
print(f"\nRemaining corrupted: {len(corrupted)}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(h)
print("\nSaved.")
