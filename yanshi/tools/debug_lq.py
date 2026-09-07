# -*- coding: utf-8 -*-
import io, re, json, html as htmlmod
exec(open(r"D:\App\Apps\yanshi\tools\gen_daishangtadeyanjing.py", encoding="utf-8").read().split("# ==================== 组装 HTML ====================")[0])

# Now check all data structures for _LQ_
def check_obj(obj, path=""):
    if isinstance(obj, str):
        if "_LQ_" in obj or "_RQ_" in obj:
            print(f"FOUND at {path}: {obj[:80]}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            check_obj(v, f"{path}[{i}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            check_obj(v, f"{path}.{k}")

check_obj(CARDS, "CARDS")
check_obj(FULLTEXT, "FULLTEXT")
check_obj(BG_LEAD, "BG_LEAD")
check_obj(AUTHOR, "AUTHOR")
check_obj(STORY, "STORY")
check_obj(APP_PEOPLE, "APP_PEOPLE")
check_obj(APP_ART, "APP_ART")
check_obj(APP_FAME, "APP_FAME")
check_obj(APP_THEME, "APP_THEME")
check_obj(ACC, "ACC")
check_obj(DICT_WORDS, "DICT_WORDS")
check_obj(DICT_NOTES, "DICT_NOTES")
print("done checking")
