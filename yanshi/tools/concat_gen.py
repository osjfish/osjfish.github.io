# -*- coding: utf-8 -*-
"""拼接数据区和代码区，生成完整的gen脚本"""
gen_path = r"D:\App\Apps\yanshi\tools\gen_huangdindexinzhuang.py"
code_path = r"D:\App\Apps\yanshi\tools\code_huangdi.py"

with open(gen_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find marker
marker_idx = None
for i, line in enumerate(lines):
    if '================= 生成' in line:
        marker_idx = i
        break

data_section = ''.join(lines[:marker_idx])
# Ensure data section ends with newline
if not data_section.endswith('\n'):
    data_section += '\n'

with open(code_path, 'r', encoding='utf-8') as f:
    code_section = f.read()

with open(gen_path, 'w', encoding='utf-8') as f:
    f.write(data_section + code_section)

print("Concatenated. Data lines:", marker_idx, "Total length:", len(data_section) + len(code_section))
