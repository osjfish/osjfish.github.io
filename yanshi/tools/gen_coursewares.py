# -*- coding: utf-8 -*-
"""一次性重新生成全部五篇自选自选课件（文言 + 现代文共用 cwlib 引擎）。"""
import data_taohuayuanji
import data_zuiwengtingji
import data_chun
import data_zitengluopubu
import data_denglong

MODULES = [
    data_taohuayuanji,
    data_zuiwengtingji,
    data_chun,
    data_zitengluopubu,
    data_denglong,
]

if __name__ == '__main__':
    for mod in MODULES:
        t = mod.build()
        print('OK', mod.OUT, 'verses=', t)
