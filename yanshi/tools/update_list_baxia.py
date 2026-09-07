# -*- coding: utf-8 -*-
"""更新 _list.json，添加八下19篇新课件"""
import json

LIST_PATH = r"D:\App\Apps\_list.json"

# 八下19篇（说明文5篇已由说明文组添加，这里添加剩余14篇）
NEW_ITEMS = [
    {"name": "《回延安》", "path": "./yanshi/huiyanan-hejingzhi.html", "category": "演示"},
    {"name": "《关雎》", "path": "./yanshi/guanju-shijing.html", "category": "演示"},
    {"name": "《蒹葭》", "path": "./yanshi/jianjia-shijing.html", "category": "演示"},
    {"name": "《最后一次讲演》", "path": "./yanshi/zuihouyicijiangyan-wenyiduo.html", "category": "演示"},
    {"name": "《应有格物致知精神》", "path": "./yanshi/yingyougewuzhizhijingshen-dingzhaozhong.html", "category": "演示"},
    {"name": "《我一生中的重要抉择》", "path": "./yanshi/woyishengzhongdezhongyaojueze-wangxuan.html", "category": "演示"},
    {"name": "《庆祝奥林匹克运动复兴25周年》", "path": "./yanshi/qingzhuaolinpikeyundongfuxing25zhounian-gubaidan.html", "category": "演示"},
    {"name": "《壶口瀑布》", "path": "./yanshi/hukoupubu-liangheng.html", "category": "演示"},
    {"name": "《在长江源头各拉丹东》", "path": "./yanshi/zaichangjiangyuantougeladandong-malihua.html", "category": "演示"},
    {"name": "《登勃朗峰》", "path": "./yanshi/dengbolangfeng-maketuweng.html", "category": "演示"},
    {"name": "《一滴水经过丽江》", "path": "./yanshi/yidishuijingguolijiang-alai.html", "category": "演示"},
    {"name": "《庄子与惠子游于濠梁》", "path": "./yanshi/zhuangziyuhuiziyouyuhaoliang-zhuangzi.html", "category": "演示"},
    {"name": "《虽有嘉肴》", "path": "./yanshi/suiyoujiayao-liji.html", "category": "演示"},
    {"name": "《卖炭翁》", "path": "./yanshi/maitanweng-baijuyi.html", "category": "演示"},
]

with open(LIST_PATH, encoding="utf-8") as f:
    data = json.load(f)

existing_paths = {item["path"] for item in data["apps"]}
added = 0
for item in NEW_ITEMS:
    if item["path"] not in existing_paths:
        data["apps"].append(item)
        added += 1
        print(f"Added: {item['name']}")
    else:
        print(f"Already exists: {item['name']}")

with open(LIST_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

print(f"\nTotal added: {added}")
print(f"Total apps: {len(data['apps'])}")
