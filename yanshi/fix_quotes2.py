# -*- coding: utf-8 -*-
"""精确修复生成脚本中的引号问题：只处理整行字符串字面量内部的ASCII引号"""
import re

path = r'D:\App\Apps\yanshi\gen_zhuangzihaoliang.py'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

LQ = '\u201c'  # "
RQ = '\u201d'  # "
AQ = '\u0022'  # "

def fix_inner_quotes(s):
    """把字符串内部的ASCII双引号交替替换为中文引号"""
    if AQ not in s:
        return s
    parts = s.split(AQ)
    # parts[0]是开头到第一个"，parts[-1]是最后一个"到结尾
    # 中间的交替为左/右引号
    result = parts[0]
    for i, p in enumerate(parts[1:-1]):
        if i % 2 == 0:
            result += LQ + p
        else:
            result += RQ + p
    result += parts[-1]
    return result

new_lines = []
for line in lines:
    stripped = line.rstrip('\n')
    # 匹配整行是一个字符串字面量的情况：可选空白 + " + 内容 + " + 可选逗号
    # 且内容中包含ASCII双引号
    m = re.match(r'^(\s*)"(.*)"(\s*,?\s*)$', stripped)
    if m and AQ in m.group(2):
        indent = m.group(1)
        inner = m.group(2)
        suffix = m.group(3)
        fixed = fix_inner_quotes('"' + inner + '"')
        new_lines.append(indent + fixed + suffix + '\n')
        continue
    
    # 匹配表格行：列表中的字符串元素包含ASCII引号
    # 如：["判断句", "是鱼之乐也", ""也"表判断，..."]
    # 这种行比较复杂，先检查是否以 [ 开头且包含多个字符串
    if stripped.lstrip().startswith('[') and AQ in stripped:
        # 找到所有被引号包裹的字符串，修复内部引号
        # 简单方法：用正则找到所有 "..." 模式，但内部有引号会导致匹配错误
        # 改用：逐字符扫描，识别字符串边界
        result = []
        i = 0
        in_str = False
        str_start = -1
        while i < len(stripped):
            c = stripped[i]
            if c == AQ:
                if not in_str:
                    # 检查是否是字符串开始：前面不是字母数字（避免匹配到属性选择器等）
                    in_str = True
                    str_start = i
                else:
                    # 可能是字符串结束，也可能是内部引号
                    # 看后面的字符：如果是, ] ) 空白 等，则是结束
                    j = i + 1
                    while j < len(stripped) and stripped[j] == ' ':
                        j += 1
                    if j >= len(stripped) or stripped[j] in ',])':
                        # 字符串结束
                        in_str = False
                        # 修复 str_start+1 到 i-1 之间的引号
                        inner = stripped[str_start+1:i]
                        if AQ in inner:
                            result.append(AQ + fix_inner_quotes(inner) + AQ)
                        else:
                            result.append(stripped[str_start:i+1])
                        i += 1
                        continue
                    # 否则是内部引号，继续扫描
            if not in_str:
                result.append(c)
            i += 1
        # 如果还有未闭合的字符串，直接追加剩余部分
        if in_str:
            result.append(stripped[str_start:])
        new_line = ''.join(result) + '\n'
        new_lines.append(new_line)
        continue
    
    new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('修复完成')
