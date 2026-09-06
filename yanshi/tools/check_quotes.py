# -*- coding: utf-8 -*-
with open(r'D:\App\Apps\tools\gen_maowu.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
line = lines[44]
print(repr(line[:100]))
for i, c in enumerate(line[:100]):
    if ord(c) == 0x22:
        print('  pos %d: ASCII quote' % i)
    elif ord(c) in (0x201c, 0x201d):
        print('  pos %d: Chinese quote U+%04X' % (i, ord(c)))
