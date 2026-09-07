# -*- coding: utf-8 -*-
"""Fix all quote issues and self-referential annotations in 刘姥姥课件"""
import re

p = r'D:\App\Apps\yanshi\liulaolaojindaguanyuan-caoxueqin.html'
with open(p, 'r', encoding='utf-8') as f:
    h = f.read()

# Fix all quote concatenation patterns
# Pattern 1: " + "“" + "  -> "
h = re.sub(r'" \+ "“" \+ "', '\u201c', h)
# Pattern 2: " + "”" + "  -> "
h = re.sub(r'" \+ "”" \+ "', '\u201d', h)
# Pattern 3: "”" + "  -> "
h = re.sub(r'”" \+ "', '\u201d', h)
# Pattern 4: " + "“"  -> "
h = re.sub(r'" \+ "“"', '\u201c', h)
# Pattern 5: LQ + "  -> "
h = re.sub(r'LQ \+ "', '\u201c', h)
# Pattern 6: " + LQ  -> "
h = re.sub(r'" \+ LQ', '\u201c', h)
# Pattern 7: " + "  (between Chinese chars or quotes) -> empty
h = re.sub(r'(?<=[\u4e00-\u9fff\u201c\u201d])" \+ "(?=[\u4e00-\u9fff\u201c\u201d])', '', h)
# Pattern 8: leftover " + " at start/end of strings
h = re.sub(r'(?<=\u201c)" \+ ', '', h)
h = re.sub(r' \+ "(?=\u201d)', '', h)

# Fix self-referential annotations
# "我就明白了" -> "我就明白了" (remove the annotation since it's self-referential)
# Actually, these are in the data as annotations. Let me find and remove them.
# The pattern is: data-note="我就明白了">我就明白了</span>
# We need to remove the span and just keep the text.
h = re.sub(r'<span class="anno-word" data-note="我就明白了">我就明白了</span>', '我就明白了', h)
h = re.sub(r'<span class="anno-word" data-note="鸳鸯便坐下了">鸳鸯便坐下了</span>', '鸳鸯便坐下了', h)

# Check for any remaining " + " patterns
remaining = re.findall(r'" \+ "|\+ "|" \+|LQ \+|\+ LQ', h)
print(f"Remaining quote patterns: {len(remaining)}")
for r in remaining[:10]:
    print(f"  {repr(r)}")

# Check ASCII quotes between Chinese chars
ascii_quotes = len(re.findall(r'[\u4e00-\u9fff]"[\u4e00-\u9fff]', h))
print(f"\nASCII quotes between Chinese chars: {ascii_quotes}")

# Check Chinese quote balance
left = h.count('\u201c')
right = h.count('\u201d')
print(f"Chinese left quotes: {left}")
print(f"Chinese right quotes: {right}")
print(f"Balance: {'OK' if left == right else 'IMBALANCE'}")

# Check self-referential annotations
self_ref = re.findall(r'data-note="([^"]+)">\1</span>', h)
print(f"\nSelf-referential annotations: {len(self_ref)}")
for s in self_ref:
    print(f"  {s}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(h)
print("\nSaved.")
