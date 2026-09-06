# -*- coding: utf-8 -*-
"""后处理：将HTML标签内属性的中文引号恢复为ASCII引号"""
import re

def fix_html_attr_quotes(html):
    """在HTML标签内（<...>），将中文引号替换为ASCII引号"""
    def fix_tag(match):
        tag = match.group(0)
        tag = tag.replace('\u201c', '"').replace('\u201d', '"')
        return tag
    # 匹配HTML标签（包括自闭合）
    return re.sub(r'<[^>]+>', fix_tag, html)

fpath = r"D:\App\Apps\zuguoawoqinaidezugu-shuting.html"
with open(fpath, encoding="utf-8") as f:
    html = f.read()

fixed = fix_html_attr_quotes(html)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(fixed)

# 验证
print("id=\"mediaF1\" found:", 'id="mediaF1"' in fixed)
print("id=\"mediaF2\" found:", 'id="mediaF2"' in fixed)
print("Chinese left in tags:", len(re.findall(r'<[^>]*\u201c[^>]*>', fixed)))
print("Chinese right in tags:", len(re.findall(r'<[^>]*\u201d[^>]*>', fixed)))
