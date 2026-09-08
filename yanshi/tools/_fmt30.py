# -*- coding: utf-8 -*-
"""最近批次版式量化：part分组/注释/题库/背景区盒子"""
import re

FILES = ['manjianghong-qiujin.html', 'puliurenjia-liushaotang.html', 'zaoer-sunhong.html',
         'tongyi-nieluda.html', 'haiyan-gaoerji.html', 'tianxiadiyilou-hejiping.html',
         'tandushu-peigen.html', 'buqiushenjie-manancun.html', 'shanshuihuadeyijing-likeran.html',
         'wuyanzhimei-zhuguangqian.html', 'quqianwomendexiangxiang-yetaotao.html',
         'fengyuyin-ludi.html', 'duanzhang-bianzhilin.html', 'quyuan-guomoruo.html',
         'taikongyiri-yangliwei.html', 'taijie-lisenxiang.html',
         'zaichangjiangyuantougeladandong-malihua.html', 'dengbolangfeng-maketuweng.html',
         'weixuanzedelu-fuluosite.html', 'jiarushenghuoqipianleni-puxijin.html',
         'huiyanan-hejingzhi.html', 'shuohezuo-zangkejia.html',
         'liefutuoersitai-ciweige.html', 'weidadebeiju-ciweige.html',
         'meilideyanse-aifujuli.html', 'zuihouyicijiangyan-wenyiduo.html',
         'yingyougewuzhizhijingshen-dingzhaozhong.html', 'woyishengzhongdezhongyaojueze-wangxuan.html',
         'woweishimeerhuozhe-luosu.html']
REF = ['pipaxing-baijuyi.html', 'changhenge-baijuyi.html', 'hongmenyan-shiji.html', 'beiying-zhuziqing.html']

def stats(f):
    s = open(f, 'rb').read().decode('utf-8', errors='ignore')
    d = {
        'part': len(re.findall(r'class="part-head"', s)),
        'over': len(re.findall(r'part-overview', s)),
        'anno': len(re.findall(r'class="anno-word"', s)),
        'verse': len(re.findall(r'class="verse"', s)),
        'h3': len(re.findall(r'<h3', s)),
        'dict_w': len(re.findall(r'"w":\s*"', s)) or len(re.findall(r"w:\s*'", s)),
        'fame': len(re.findall(r'fame-card', s)),
        'box': len(re.findall(r'class="box"', s)),
        'databody': 'data-body' in s,
    }
    return d

print('%-46s %5s %5s %5s %5s %5s %6s %5s %5s' % ('文件', 'part', 'over', 'anno', 'verse', 'h3', 'dict', 'fame', 'box'))
for f in REF + FILES:
    d = stats(f)
    print('%-46s %5d %5d %5d %5d %5d %6d %5d %5d' % (f[:44], d['part'], d['over'], d['anno'],
          d['verse'], d['h3'], d['dict_w'], d['fame'], d['box']))
