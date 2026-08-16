#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""热点聚合数据抓取脚本。

在服务器端(GitHub Actions)定时运行，从多个公开来源抓取热点新闻，
归一化后写入仓库根目录 news_data.json，随站点自动部署。

仅使用 Python 标准库，无需安装任何依赖。
"""
import html
import json
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree as ET

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

OUT_FILE = Path(__file__).resolve().parent.parent / "news_data.json"

# 每个来源最多保留条数
MAX_PER_SOURCE = 30
# RSS 源最多保留条数
MAX_PER_RSS = 20

# 各来源配置：url / 解析方式 / 可选 best_effort(云端IP可能被风控，失败仅跳过)
SOURCES = {
    "baidu":   {"name": "百度热搜", "color": "#A93226", "url": "https://top.baidu.com/api/board?platform=wise&tab=realtime"},
    "toutiao": {"name": "头条热榜", "color": "#D94E2E", "url": "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"},
    "weibo":   {"name": "微博热搜", "color": "#E81123", "url": "https://weibo.com/ajax/side/hotSearch", "best_effort": True},
    "zhihu":   {"name": "知乎热榜", "color": "#0084FF", "url": "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50", "best_effort": True},
    "bilibili": {"name": "B站热榜", "color": "#FB7299", "url": "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all", "best_effort": True},
    "douyin":  {"name": "抖音热榜", "color": "#FE2C55", "url": "https://www.douyin.com/aweme/v1/web/hot/search/list/", "best_effort": True},
    "sina":    {"name": "新浪新闻", "color": "#E60012", "url": "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&num=30&page=1"},
    "ithome":  {"name": "IT之家", "color": "#FF7C00", "url": "https://www.ithome.com/rss/", "kind": "rss"},
    "cnbeta":  {"name": "cnBeta", "color": "#1F6AA5", "url": "https://www.cnbeta.com.tw/backend.php", "kind": "rss"},
    "sspai":   {"name": "少数派", "color": "#B8860B", "url": "https://sspai.com/feed", "kind": "rss"},
    "ifanr":   {"name": "爱范儿", "color": "#07C160", "url": "https://www.ifanr.com/feed", "kind": "rss"},
}


def fetch_text(url, timeout=20):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
        return raw.decode(charset, "replace")


def to_int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def clean(s):
    if not s:
        return ""
    return html.unescape(re.sub(r"[\s\u3000]+", " ", str(s))).strip()


def parse_rss(text, max_items=MAX_PER_RSS):
    """解析 RSS 2.0 或 Atom，返回 [{title,url,time}]。"""
    items = []
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return items
    # 兼容 RSS / Atom 两种命名空间
    ns_rss = "{http://www.w3.org/2005/Atom}"
    entries = root.findall("./channel/item") or root.findall("./item") or root.findall(ns_rss + "entry")
    for e in entries:
        if len(items) >= max_items:
            break
        if e.find("title") is None:
            continue
        title = clean(e.findtext("title"))
        link = e.findtext("link") or ""
        if not title or not link:
            continue
        date_raw = e.findtext("pubDate") or e.findtext("dc:date") or e.findtext(ns_rss + "updated")
        t = None
        if date_raw:
            try:
                dt = parsedate_to_datetime(date_raw.strip()) if e.findtext("pubDate") else datetime.fromisoformat(
                    date_raw.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                t = dt.astimezone(timezone.utc).isoformat()
            except (ValueError, TypeError):
                t = None
        items.append({"title": title, "url": link, "time": t})
    return items


def get_json_items(key):
    """根据来源类型解析，返回 [{title,url,hot,time}]。"""
    conf = SOURCES[key]
    kind = conf.get("kind", "json")
    text = fetch_text(conf["url"])
    out = []
    if kind == "rss":
        for it in parse_rss(text):
            out.append({"title": it["title"], "url": it["url"], "hot": None, "time": it["time"]})
        return out
    data = json.loads(text)

    if key == "baidu":
        for card in data.get("data", {}).get("cards", []):
            for block in card.get("content", []):
                for item in block.get("content", []):
                    title = clean(item.get("word"))
                    url = item.get("url") or ""
                    if not title:
                        continue
                    out.append({"title": title, "url": url,
                                "hot": to_int(item.get("hotScore")) or (100 - int(item.get("index", 50))),
                                "time": None})
                    if len(out) >= MAX_PER_SOURCE:
                        break

    elif key == "toutiao":
        for item in data.get("data", []):
            title = clean(item.get("Title"))
            url = item.get("Url") or ""
            if not title:
                continue
            out.append({"title": title, "url": url, "hot": to_int(item.get("HotValue")), "time": None})
            if len(out) >= MAX_PER_SOURCE:
                break

    elif key == "weibo":
        for item in data.get("data", {}).get("realtime", []):
            title = clean(item.get("word"))
            url = item.get("url") or ""
            if not title:
                continue
            hot = to_int(item.get("num"))
            if hot is None:
                hot = to_int(item.get("raw_hot"))
            out.append({"title": title, "url": url, "hot": hot, "time": None})
            if len(out) >= MAX_PER_SOURCE:
                break

    elif key == "zhihu":
        for item in data.get("data", []):
            target = item.get("target", {})
            title = clean(target.get("title"))
            url = target.get("url") or ""
            if not title:
                continue
            out.append({"title": title, "url": url, "hot": to_int(item.get("detail_text")),
                        "time": target.get("created", None)})
            if len(out) >= MAX_PER_SOURCE:
                break

    elif key == "bilibili":
        for item in data.get("data", {}).get("list", []):
            title = clean(item.get("title"))
            url = item.get("short_link_v2") or item.get("url") or item.get("short_link") or ""
            if not title:
                continue
            out.append({"title": title, "url": url, "hot": to_int(item.get("score")), "time": None})
            if len(out) >= MAX_PER_SOURCE:
                break

    elif key == "douyin":
        for item in data.get("data", {}).get("word_list", []):
            title = clean(item.get("word"))
            url = item.get("link") or ""
            if not title:
                continue
            out.append({"title": title, "url": url, "hot": to_int(item.get("hot_value")),
                        "time": item.get("event_time", None)})
            if len(out) >= MAX_PER_SOURCE:
                break

    elif key == "sina":
        for item in data.get("result", {}).get("data", []):
            title = clean(item.get("title"))
            url = item.get("url") or ""
            if not title:
                continue
            ts = to_int(item.get("ctime"))
            out.append({"title": title, "url": url, "hot": None,
                        "time": datetime.fromtimestamp(ts, timezone.utc).isoformat() if ts else None})
            if len(out) >= MAX_PER_SOURCE:
                break

    return out


def main():
    results = {}
    items = []
    errors = []
    for key, conf in SOURCES.items():
        try:
            got = get_json_items(key)
        except Exception as exc:  # noqa: BLE001
            msg = "{}: {}".format(type(exc).__name__, exc)
            errors.append("{} -> {}".format(key, msg))
            if not conf.get("best_effort"):
                print("[FAIL] " + key + " -> " + msg, file=sys.stderr)
            else:
                print("[SKIP] " + key + " -> " + msg, file=sys.stderr)
            continue
        for it in got:
            it["source"] = key
            items.append(it)
        results[key] = {
            "name": conf["name"],
            "color": conf.get("color", "#888888"),
            "count": len(got),
        }
        print("[OK] {:<10} {} 条".format(key, len(got)))

    now = datetime.now(timezone.utc).isoformat()
    payload = {
        "updated_at": now,
        "total": len(items),
        "sources": results,
        "items": items,
    }
    OUT_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print("共 {} 条，已写入 {}".format(len(items), OUT_FILE))
    if errors:
        print("部分来源失败: {}".format("; ".join(errors)), file=sys.stderr)
    # 供工作流判断是否有可用数据
    return 0 if items else 1


if __name__ == "__main__":
    sys.exit(main())
