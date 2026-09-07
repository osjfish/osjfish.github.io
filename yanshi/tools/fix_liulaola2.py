# -*- coding: utf-8 -*-
"""Fix remaining consecutive quote patterns in 刘姥姥"""
import re

p = r'D:\App\Apps\yanshi\liulaolaojindaguanyuan-caoxueqin.html'
with open(p, 'r', encoding='utf-8') as f:
    h = f.read()

# Fix: ”" + “ -> ”“
h = h.replace('\u201d" + \u201c', '\u201d\u201c')

# Verify
remaining = re.findall(r'" \+|\+ "', h)
print(f"Remaining quote patterns: {len(remaining)}")

# Check ASCII quotes between Chinese chars
ascii_quotes = len(re.findall(r'[\u4e00-\u9fff]"[\u4e00-\u9fff]', h))
print(f"ASCII quotes between Chinese chars: {ascii_quotes}")

# Check Chinese quote balance
left = h.count('\u201c')
right = h.count('\u201d')
print(f"Chinese left quotes: {left}")
print(f"Chinese right quotes: {right}")
print(f"Balance: {'OK' if left == right else 'IMBALANCE'}")

with open(p, 'w', encoding='utf-8') as f:
    f.write(h)
print("\nSaved.")
