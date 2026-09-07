# -*- coding: utf-8 -*-
"""Fix ASCII quotes inside Python string content in gen_lunjiaoyang.py"""
import io, re

p = r'D:\App\Apps\yanshi\tools\gen_lunjiaoyang.py'
h = io.open(p, encoding='utf-8').read()

# Strategy: process line by line. For lines that are S tuple entries,
# replace ASCII quotes that are between Chinese chars with Chinese quotes.
# We detect S entries by looking for lines starting with (N,"

lines = h.split('\n')
fixed = 0
for i, line in enumerate(lines):
    # Only process S data lines (start with (digit," or have content pattern)
    if re.match(r'^\(\d+,', line) or re.match(r'^"[^"]*",', line):
        # Replace ASCII quotes adjacent to Chinese characters
        # Opening quote: " followed by Chinese
        new_line = re.sub(r'"(?=[\u4e00-\u9fff])', '\u201c', line)
        # Closing quote: Chinese followed by "
        new_line = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef])"', '\u201d', new_line)
        if new_line != line:
            fixed += 1
            lines[i] = new_line

h = '\n'.join(lines)
io.open(p, 'w', encoding='utf-8').write(h)
print('Fixed', fixed, 'lines')
