# -*- coding: utf-8 -*-
"""Fix remaining English quotes in v5 verse"""
p = r'D:\App\Apps\yanshi\shuidiaogetou-sushi.html'
with open(p, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the v5 verse section and fix English quotes in the 赏析 text
# The v5 verse starts at id="v5" and ends before the next part-head
v5_start = html.find('id="v5"')
v5_end = html.find('<div class="part-head">', v5_start)
v5_section = html[v5_start:v5_end]

# Replace English quotes in the 赏析 text (within <p> tags)
# We need to be careful not to replace quotes in HTML attributes
# Simple approach: replace patterns like "汉字" with "汉字"
import re

# Find all text between > and < in the v5 section, replace quotes
def fix_quotes_in_text(m):
    text = m.group(0)
    # Toggle quotes
    result = []
    open_state = False
    for c in text:
        if c == '"':
            if not open_state:
                result.append('\u201c')
                open_state = True
            else:
                result.append('\u201d')
                open_state = False
        else:
            result.append(c)
    return ''.join(result)

# Only fix text within the v5 section, between tags
v5_fixed = re.sub(r'>([^<]+)<', lambda m: '>' + fix_quotes_in_text(m) + '<', v5_section)

html = html[:v5_start] + v5_fixed + html[v5_end:]

# Count remaining
text_only = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text_only = re.sub(r'<style[^>]*>.*?</style>', '', text_only, flags=re.DOTALL)
text_only = re.sub(r'<[^>]+>', '', text_only)
print(f"English quotes in text after: {text_only.count(chr(34))}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")
