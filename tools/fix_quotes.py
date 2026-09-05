# -*- coding: utf-8 -*-
"""Fix gen_caogui.py: convert internal ASCII double quotes to Chinese quotes.
Strategy: for each line, if it looks like a Python string literal (starts with optional whitespace + "),
the first and last " are delimiters; all " in between become alternating \u201c / \u201d.
Also handle tuple/list lines with multiple strings.
"""
import re

LQ = '\u201c'
RQ = '\u201d'

with open(r'D:\App\Apps\tools\gen_caogui.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed = []
for line in lines:
    # Skip lines that are clearly code (not data strings)
    stripped = line.strip()
    # Data string lines start with " and end with ", or ", 
    # We need to handle lines like:  "text with "quotes" inside",
    # or:  ("key", [ "item1", "item2" ]),
    
    # Simple approach: find all " in the line. The outermost ones are delimiters.
    # But tuples have multiple strings. Let's use a state machine.
    
    # Actually, let's just replace pairs of " that are NOT at string boundaries.
    # A " is at a string boundary if: it's the first " on the line (after whitespace),
    # or it's immediately followed by , ) ] : or end of line, or it's immediately preceded by , ( [ :
    
    result = []
    i = 0
    in_string = False
    expect_left = True  # next internal quote should be left
    
    while i < len(line):
        ch = line[i]
        if ch == '"':
            if not in_string:
                # This is an opening delimiter
                in_string = True
                result.append('"')
            else:
                # Check if this is a closing delimiter
                # Look ahead: next non-space char should be , ) ] : or newline
                j = i + 1
                while j < len(line) and line[j] == ' ':
                    j += 1
                next_char = line[j] if j < len(line) else '\n'
                if next_char in ',)]:\n' or j >= len(line):
                    # This is a closing delimiter
                    in_string = False
                    result.append('"')
                    expect_left = True
                else:
                    # This is an internal quote - convert to Chinese
                    if expect_left:
                        result.append(LQ)
                        expect_left = False
                    else:
                        result.append(RQ)
                        expect_left = True
        else:
            result.append(ch)
        i += 1
    
    fixed.append(''.join(result))

with open(r'D:\App\Apps\tools\gen_caogui.py', 'w', encoding='utf-8') as f:
    f.writelines(fixed)

# Verify
with open(r'D:\App\Apps\tools\gen_caogui.py', 'r', encoding='utf-8') as f:
    content = f.read()
print(f'Chinese left quotes: {content.count(LQ)}')
print(f'Chinese right quotes: {content.count(RQ)}')
print('Fix applied.')
