# -*- coding: utf-8 -*-
import io
p = r'D:\App\Apps\yanshi\tools\gen_weidadebeiju.py'
s = io.open(p, encoding='utf-8-sig').read()
s = s.replace('{"w":"怏","py":"yàng","q":"他们□□不乐地', '{"w":"怏怏","py":"yàng yàng","q":"他们□□不乐地')
s = s.replace('{"w":"姗","py":"shān","q":"一面□□来迟的', '{"w":"姗姗","py":"shān shān","q":"一面□□来迟的')
s = s.replace('{"w":"忡","py":"chōng","q":"使他们每走一步都忧心□□"', '{"w":"忡忡","py":"chōng chōng","q":"使他们每走一步都忧心□□"')
s = s.replace('{"w":"踉","py":"liàng","q":"于是病人只好用冻伤了的双腿□□跄跄地', '{"w":"踉踉","py":"liàng liàng","q":"于是病人只好用冻伤了的双腿□□跄跄地')
io.open(p, 'w', encoding='utf-8-sig').write(s)
print('fixed')
