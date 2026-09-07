# -*- coding: utf-8 -*-
"""Convert English double quotes in HTML text content to Chinese quotes using regex."""
import re

def convert_text_quotes(text):
    """Convert quotes in a text node, tracking open/close state."""
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

def process_html(html):
    """Process HTML, converting quotes only in text content (between tags)."""
    # Split by tags, process text segments
    # Pattern: match everything between > and < (text content)
    # But we need to be careful not to process script/style content
    
    # First, protect script and style blocks
    script_blocks = []
    def protect_script(m):
        script_blocks.append(m.group(0))
        return f'\x00SCRIPT{len(script_blocks)-1}\x00'
    
    html = re.sub(r'<script[^>]*>.*?</script>', protect_script, html, flags=re.DOTALL|re.IGNORECASE)
    
    style_blocks = []
    def protect_style(m):
        style_blocks.append(m.group(0))
        return f'\x00STYLE{len(style_blocks)-1}\x00'
    
    html = re.sub(r'<style[^>]*>.*?</style>', protect_style, html, flags=re.DOTALL|re.IGNORECASE)
    
    # Now process text content between tags
    # Find all text segments (between > and <) and convert quotes
    def replace_text(m):
        text = m.group(0)
        return convert_text_quotes(text)
    
    # Match text that comes after a > and before a <
    # This is the text content of elements
    html = re.sub(r'>([^<]+)<', lambda m: '>' + convert_text_quotes(m.group(1)) + '<', html)
    
    # Restore script and style blocks
    for i, block in enumerate(script_blocks):
        html = html.replace(f'\x00SCRIPT{i}\x00', block)
    for i, block in enumerate(style_blocks):
        html = html.replace(f'\x00STYLE{i}\x00', block)
    
    return html

# Process the file
p = r'D:\App\Apps\yanshi\chouletianyangzhouchufengxishangjianzeng-liuyuxi.html'
with open(p, 'r', encoding='utf-8') as f:
    html = f.read()

# Count before
text_only = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
text_only = re.sub(r'<style[^>]*>.*?</style>', '', text_only, flags=re.DOTALL)
text_only = re.sub(r'<[^>]+>', '', text_only)
print(f"English quotes in text before: {text_only.count('\"')}")

# Convert
new_html = process_html(html)

# Count after
text_only2 = re.sub(r'<script[^>]*>.*?</script>', '', new_html, flags=re.DOTALL)
text_only2 = re.sub(r'<style[^>]*>.*?</style>', '', text_only2, flags=re.DOTALL)
text_only2 = re.sub(r'<[^>]+>', '', text_only2)
print(f"English quotes in text after: {text_only2.count('\"')}")
print(f"Chinese left quotes: {text_only2.count('\u201c')}")
print(f"Chinese right quotes: {text_only2.count('\u201d')}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Done!")
