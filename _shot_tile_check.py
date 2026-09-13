# -*- coding: utf-8 -*-
# 查找系统浏览器并用无头模式给 _tile_check.html 截图
import os, subprocess, sys

candidates = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
]
exe = next((p for p in candidates if os.path.exists(p)), None)
print("browser:", exe)
if not exe:
    sys.exit(1)

url = "http://127.0.0.1:61556/static-html/bfa96d0048ee0953/_tile_check.html"
out = os.path.abspath("_tile_check.png")
cmd = [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars",
       "--window-size=780,780", "--screenshot=" + out,
       "--virtual-time-budget=6000", url]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
print("exit:", r.returncode)
print("png exists:", os.path.exists(out), os.path.getsize(out) if os.path.exists(out) else 0)
