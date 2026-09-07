# -*- coding: utf-8 -*-
"""Fix LQ/RQ literal strings in generated HTML and check verse count"""
import re

p = r'D:\App\Apps\yanshi\shuidiaogetou-sushi.html'
with open(p, 'r', encoding='utf-8') as f:
    html = f.read()

# Count before
lq_count = html.count('" + LQ + "')
rq_count = html.count('" + RQ + "')
print(f"LQ literals before: {lq_count}")
print(f"RQ literals before: {rq_count}")

# Replace
html = html.replace('" + LQ + "', '\u201c')
html = html.replace('" + RQ + "', '\u201d')

# Also handle edge cases where LQ/RQ might be at start/end
html = html.replace('LQ + "', '\u201c')
html = html.replace('" + RQ', '\u201d')

# Count verse divs
verses = re.findall(r'<div class="verse" id="v\d+"', html)
print(f"Verse divs found: {len(verses)}")
for v in verses:
    print(f"  {v}")

# Check if there's a part-head between verses
part_heads = re.findall(r'<div class="part-head">', html)
print(f"Part-head divs: {len(part_heads)}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")
