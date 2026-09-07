# -*- coding: utf-8 -*-
"""使用tokenize修复gen脚本中字符串内容里的ASCII引号。"""
import io, tokenize, sys

path = r"D:\App\Apps\yanshi\tools\gen_dengjiaxian.py"
src = io.open(path, encoding="utf-8").read()

# 方法：逐行处理，对每一行找到所有"字符串字面量"并修复内部引号
# 字符串字面量以"开头，以"结尾（非转义）
# 但由于内部引号导致解析失败，我们用启发式：
# 对每一行，找到第一个"和最后一个"，中间的"交替替换为中文引号

lines = src.split("\n")
out = []
for line in lines:
    # 跳过注释行和空行
    stripped = line.lstrip()
    if not stripped or stripped.startswith('#'):
        out.append(line)
        continue
    # 统计该行的"数量
    quote_positions = [i for i, c in enumerate(line) if c == '"']
    if len(quote_positions) <= 2:
        out.append(line)
        continue
    # 有多于2个引号：第一个和最后一个是分隔符，中间的需要替换
    # 但要注意：一行可能有多个独立字符串（如 ("a","b")）
    # 简单策略：如果行中有逗号分隔的多个字符串，分别处理
    # 更简单：交替替换所有中间的引号
    first = quote_positions[0]
    last = quote_positions[-1]
    prefix = line[:first+1]
    content = line[first+1:last]
    suffix = line[last:]
    result = []
    toggle = True
    for ch in content:
        if ch == '"':
            if toggle:
                result.append('\u201c')
            else:
                result.append('\u201d')
            toggle = not toggle
        else:
            result.append(ch)
    out.append(prefix + ''.join(result) + suffix)

result = "\n".join(out)
io.open(path, "w", encoding="utf-8").write(result)
print("Fixed. Lines processed:", len(lines))
