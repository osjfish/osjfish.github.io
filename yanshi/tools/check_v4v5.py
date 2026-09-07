# -*- coding: utf-8 -*-
"""Check v4/v5 HTML structure"""
p = r'D:\App\Apps\yanshi\shuidiaogetou-sushi.html'
with open(p, 'r', encoding='utf-8') as f:
    h = f.read()

# Find v4 and v5
i4 = h.find('id="v4"')
i5 = h.find('id="v5"')
print(f"v4 position: {i4}")
print(f"v5 position: {i5}")
print(f"Distance: {i5-i4}")

# Show context around v4 end / v5 start
print("\n=== v4 to v5 context ===")
print(h[i4:i5+200])
