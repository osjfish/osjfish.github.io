# -*- coding: utf-8 -*-
"""Convert English double quotes in HTML text content to Chinese quotes.
Only converts quotes in visible text (not in HTML attributes or JS strings)."""
import re

def convert_quotes_in_html(html):
    result = []
    i = 0
    n = len(html)
    in_tag = False
    in_script = False
    in_style = False
    quote_open = False  # track open/close state per text run
    
    while i < n:
        c = html[i]
        
        # Detect tag start/end
        if c == '<' and not in_script and not in_style:
            # Check if it's a script/style tag
            rest = html[i:i+10].lower()
            if rest.startswith('<script'):
                in_script = True
            elif rest.startswith('<style'):
                in_style = True
            elif rest.startswith('</script'):
                in_script = False
            elif rest.startswith('</style'):
                in_style = False
            in_tag = True
            result.append(c)
            i += 1
            continue
        
        if c == '>' and in_tag:
            in_tag = False
            result.append(c)
            i += 1
            continue
        
        # If in tag, script, or style, keep as-is
        if in_tag or in_script or in_style:
            result.append(c)
            i += 1
            continue
        
        # We're in text content - convert quotes
        if c == '"':
            # Determine if this is opening or closing
            # Look at previous non-space char
            prev_char = ''
            for j in range(len(result)-1, -1, -1):
                if result[j] not in ' \t\n\r':
                    prev_char = result[j]
                    break
            
            # Opening quote if: prev char is not a Chinese char/word char,
            # or prev char is punctuation that typically precedes opening quote
            # Simple heuristic: toggle, but reset at block boundaries
            if not quote_open:
                result.append('\u201c')  # "
                quote_open = True
            else:
                result.append('\u201d')  # "
                quote_open = False
            i += 1
            continue
        
        # Reset quote state at block-level punctuation
        if c in '\n':
            quote_open = False
        
        result.append(c)
        i += 1
    
    return ''.join(result)

# Process the file
p = r'D:\App\Apps\yanshi\chouletianyangzhouchufengxishangjianzeng-liuyuxi.html'
with open(p, 'r', encoding='utf-8') as f:
    html = f.read()

# First, let's check how many quotes are in text content vs attributes
# Simple approach: remove all tags and script/style, count quotes
text_only = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text_only = re.sub(r'<style[^>]*>.*?</style>', '', text_only, flags=re.DOTALL)
text_only = re.sub(r'<[^>]+>', '', text_only)
print(f"Quotes in text content before: {text_only.count('\"')}")

# Convert
new_html = convert_quotes_in_html(html)

# Verify
text_only2 = re.sub(r'<script[^>]*>.*?</script>', '', new_html, flags=re.DOTALL)
text_only2 = re.sub(r'<style[^>]*>.*?</style>', '', text_only2, flags=re.DOTALL)
text_only2 = re.sub(r'<[^>]+>', '', text_only2)
print(f"Quotes in text content after: {text_only2.count('\"')}")
print(f"Chinese left quotes: {text_only2.count('\u201c')}")
print(f"Chinese right quotes: {text_only2.count('\u201d')}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Done!")
