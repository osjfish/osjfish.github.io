# -*- coding: utf-8 -*-
with open(r'D:\App\Apps\tools\gen_hetangyuese.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
line = lines[29]  # line 30, has Chinese quotes
print(repr(line[:80]))
for i, c in enumerate(line[:80]):
    if ord(c) == 0x22:
        print('  pos %d: ASCII quote' % i)
    elif ord(c) in (0x201c, 0x201d):
        print('  pos %d: Chinese quote U+%04X' % (i, ord(c)))
