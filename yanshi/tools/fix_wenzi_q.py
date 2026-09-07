# -*- coding: utf-8 -*-
path = r'D:\App\Apps\yanshi\tools\data_wenzi.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_next = False
for i, line in enumerate(lines):
    if skip_next:
        skip_next = False
        continue
    if '"w":"较"' in line and 'jiào' in line:
        new_lines.append(' {"w":"较量较量","py":"jiào liàng jiào liàng","q":"我们来□□□□吧！","tip":"「较」车字旁读jiào；「量」日字底读liàng；叠词整体作答"},\n')
        skip_next = True  # skip the 量 line
        continue
    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Done. Lines:', len(new_lines))
