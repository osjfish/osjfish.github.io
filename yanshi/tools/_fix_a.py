# -*- coding: utf-8 -*-
import io
p = r'D:\App\Apps\yanshi\tools\gen_weidadebeiju.py'
s = io.open(p, encoding='utf-8-sig').read()
old = "return '' + word + ''"
new = 'return \'<span class="anno-word" data-note="\' + note + \'">\' + word + \'</span>\''
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8-sig').write(s)
print('fixed A()')
