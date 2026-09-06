# -*- coding: utf-8 -*-
"""修复数据文件中的引号：将三引号字符串内的ASCII " 替换为中文引号"""
import re

def fix_quotes_in_triple_strings(content):
    """找到所有 '''...''' 字符串，将其中的 " 替换为交替的中文引号"""
    def replace_in_string(match):
        s = match.group(0)
        # 只处理字符串内容（不含前后的 '''）
        inner = s[3:-3]
        # 交替替换 " 为中文左右引号
        result = []
        is_left = True
        for ch in inner:
            if ch == '"':
                result.append('\u201c' if is_left else '\u201d')
                is_left = not is_left
            else:
                result.append(ch)
        return "'''" + ''.join(result) + "'''"
    
    # 匹配三引号字符串（非贪婪）
    pattern = re.compile(r"'''(.*?)'''", re.S)
    return pattern.sub(replace_in_string, content)

# 修复智取生辰纲数据文件
for fpath in [
    r"D:\App\Apps\data_zuguoawoqinaidezuguo.py",
    r"D:\App\Apps\gen_zuguoawoqinaidezuguo.py",
]:
    with open(fpath, encoding="utf-8") as f:
        content = f.read()
    fixed = fix_quotes_in_triple_strings(content)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(fixed)
    ascii_count = fixed.count('"')
    left_count = fixed.count('\u201c')
    right_count = fixed.count('\u201d')
    print(f"{fpath}: ASCII={ascii_count}, ChineseLeft={left_count}, ChineseRight={right_count}")
