# -*- coding: utf-8 -*-
import re, sys

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    h = f.read()

# Extract body content between <body...> and </body>, excluding <style> and <script>
body_match = re.search(r'<body[^>]*>(.*?)</body>', h, re.DOTALL)
if body_match:
    body = body_match.group(1)
    # Remove style and script blocks
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', body)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    ascii_quotes = text.count('"')
    print('ASCII quotes in body text:', ascii_quotes)
    if ascii_quotes > 0:
        # Find contexts
        for m in re.finditer(r'.{20}".{20}', text):
            print('  context:', repr(m.group()))
    print('Chinese left quotes:', text.count('\u201c'))
    print('Chinese right quotes:', text.count('\u201d'))
