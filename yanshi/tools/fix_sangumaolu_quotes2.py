# -*- coding: utf-8 -*-
"""Fix remaining LQ/RQ patterns in 三顾茅庐"""
import re

p = r'D:\App\Apps\yanshi\sangumaolu-luoguanzhong.html'
with open(p, 'r', encoding='utf-8') as f:
    h = f.read()

# Fix combined patterns
patterns = [
    ('" + RQ + LQ + "', '\u201d\u201c'),
    ('" + LQ + RQ + "', '\u201c\u201d'),
    ('+ RQ +', '\u201d'),
    ('+ LQ +', '\u201c'),
    ('" + RQ', '\u201d'),
    ('" + LQ', '\u201c'),
    ('RQ + "', '\u201d'),
    ('LQ + "', '\u201c'),
]

for old, new in patterns:
    count = h.count(old)
    if count > 0:
        print(f"Replacing {count}x: {repr(old)} -> {repr(new)}")
        h = h.replace(old, new)

# Check for any remaining LQ/RQ references
remaining = re.findall(r'[LQ RQ]+ \+|" \+ [LQ RQ]+', h)
print(f"\nRemaining LQ/RQ patterns: {len(remaining)}")
for r in remaining[:10]:
    print(f"  {repr(r)}")

# Count ASCII quotes in visible text
# Simple check: find " between Chinese characters
ascii_quotes = len(re.findall(r'[\u4e00-\u9fff]"[\u4e00-\u9fff]', h))
print(f"\nASCII quotes between Chinese chars: {ascii_quotes}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(h)
print("\nSaved.")
