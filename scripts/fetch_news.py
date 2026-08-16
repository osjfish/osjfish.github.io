#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""热点聚合数据抓取脚本。

在服务器端(GitHub Actions)定时运行，从多个公开来源抓取热点新闻，
归一化后写入仓库根目录 news_data.json，随站点自动部署。

仅使用 Python 标准库，无需安装任何依赖。

来源分类：
  综合热搜：百度、头条、微博、知乎、抖音
  财经资讯：东方财富、财联社、新浪
  科技媒体：差评、IT之家、cnBeta、少数派、爱范儿
  社区论坛：B站、吾爱破解
"""
import hashlib
import html
import json
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
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

# 各来源配置：url / 解析方式(kind) / 分类 / best_effort(云端IP可能被风控，失败仅跳过)
SOURCES = {
    "baidu":     {"name": "百度热搜", "color": "#DE2910", "category": "综合",
                  "url": "https://top.baidu.com/api/board?platform=wise&tab=realtime"},
    "toutiao":   {"name": "头条热榜", "color": "#D94E2E", "category": "综合",
                  "url": "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"},
    "weibo":     {"name": "微博热搜", "color": "#E6162D", "category": "综合",
                  "url": "https://weibo.com/ajax/side/hotSearch", "best_effort": True},
    "zhihu":     {"name": "知乎热榜", "color": "#0084FF", "category": "综合",
                  "url": "https://uapis.cn/api/v1/misc/hotboard?type=zhihu", "kind": "uapis", "best_effort": True},
    "douyin":    {"name": "抖音热榜", "color": "#FE2C55", "category": "综合",
                  "url": "https://uapis.cn/api/v1/misc/hotboard?type=douyin", "kind": "uapis", "best_effort": True},
    "bilibili":  {"name": "B站热榜", "color": "#FB7299", "category": "社区",
                  "url": "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all", "best_effort": True},
    "52pojie":   {"name": "吾爱破解", "color": "#E68A00", "category": "社区",
                  "url": "https://www.52pojie.cn/forum.php?mod=rss", "kind": "rss", "best_effort": True},
    "sina":      {"name": "新浪新闻", "color": "#E60012", "category": "财经",
                  "url": "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&num=30&page=1"},
    "eastmoney": {"name": "东方财富", "color": "#C7000B", "category": "财经",
                  "url": "https://np-listapi.eastmoney.com/comm/web/getFastNewsList?client=web&biz=web_724&fastColumn=102&sortEnd=&pageSize=30&req_trace=1&fields=&order=1&beginTime=&endTime=",
                  "kind": "eastmoney", "best_effort": True},
    "cls":       {"name": "财联社", "color": "#1E4B8F", "category": "财经",
                  "url": "https://www.cls.cn/v1/roll/get_roll_list", "kind": "cls", "best_effort": True},
    "chaping":   {"name": "差评", "color": "#7C3AED", "category": "科技",
                  "url": "https://www.thexpin.com/feed", "kind": "rss", "best_effort": True},
    "ithome":    {"name": "IT之家", "color": "#FF7C00", "category": "科技",
                  "url": "https://www.ithome.com/rss/", "kind": "rss"},
    "cnbeta":    {"name": "cnBeta", "color": "#1F6AA5", "category": "科技",
                  "url": "https://www.cnbeta.com.tw/backend.php", "kind": "rss", "best_effort": True},
    "sspai":     {"name": "少数派", "color": "#B8860B", "category": "科技",
                  "url": "https://sspai.com/feed", "kind": "rss", "best_effort": True},
    "ifanr":     {"name": "爱范儿", "color": "#07C160", "category": "科技",
                  "url": "https://www.ifanr.com/feed", "kind": "rss"},
}

# 分类展示顺序
CATEGORY_ORDER = ["综合", "财经", "科技", "社区"]

BJ_TZ = timezone(timedelta(hours=8))


def fetch_bytes(url, timeout=20):
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_text(url, timeout=20):
    raw = fetch_bytes(url, timeout)
    return raw.decode("utf-8", "replace")


def to_int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def clean(s):
    if not s:
        return ""
    return html.unescape(re.sub(r"[\s\u3000]+", " ", str(s))).strip()


def parse_hot(v):
    """把热度转成数字。支持 '275 万热度'、'1.2亿'、纯数字等格式。"""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).strip()
    if not s:
        return None
    m = re.search(r"([\d.]+)\s*(万|亿|w|W|k)?", s)
    if not m:
        return to_int(s)
    try:
        n = float(m.group(1))
    except ValueError:
        return None
    mult = {"万": 1e4, "亿": 1e8, "w": 1e4, "W": 1e4, "k": 1e3}.get(m.group(2) or "", 1)
    return int(n * mult)


def _rss_to_str(raw):
    """把 RSS 原始字节解码为字符串并重写 XML 声明，兼容 gbk/utf-8 等编码。"""
    head = raw[:200].decode("ascii", "ignore")
    m = re.search(r"encoding\s*=\s*[\"']([\w-]+)[\"']", head)
    enc = m.group(1) if m else "utf-8"
    try:
        text = raw.decode(enc, "replace")
    except LookupError:
        text = raw.decode("utf-8", "replace")
    return re.sub(r"<\?xml[^>]*\?>", '<?xml version="1.0" encoding="utf-8"?>', text, count=1)


def parse_rss(raw, max_items=MAX_PER_RSS):
    """解析 RSS 2.0 或 Atom，返回 [{title,url,time}]。raw 为原始字节。"""
    items = []
    try:
        root = ET.fromstring(_rss_to_str(raw))
    except ET.ParseError:
        return items
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
                if e.findtext("pubDate") or e.findtext("dc:date"):
                    dt = parsedate_to_datetime(date_raw.strip())
                else:
                    dt = datetime.fromisoformat(date_raw.replace("Z", "+00:00"))
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

    if kind == "rss":
        raw = fetch_bytes(conf["url"])
        out = []
        for it in parse_rss(raw):
            out.append({"title": it["title"], "url": it["url"], "hot": None, "time": it["time"]})
        return out

    if kind == "cls":
        # 财联社 v1 接口需本地计算 sign，零 key：sign = md5(sha1(字典序 query))
        params = {"app": "CailianpressWeb", "category": "", "last_time": "",
                  "os": "web", "refresh_type": "1", "rn": "30", "sv": "8.4.6"}
        qs = "&".join("{}={}".format(k, params[k]) for k in sorted(params))
        sign = hashlib.md5(hashlib.sha1(qs.encode()).hexdigest().encode()).hexdigest()
        url = conf["url"] + "?" + qs + "&sign=" + sign
        data = json.loads(fetch_text(url))
        out = []
        for item in data.get("data", {}).get("roll_data", []) or []:
            title = clean(item.get("title")) or clean(item.get("brief")) or clean(item.get("content"))
            if not title:
                continue
            ts = to_int(item.get("ctime"))
            out.append({"title": title,
                        "url": "https://www.cls.cn/detail/{}".format(item.get("id")) if item.get("id") else "",
                        "hot": parse_hot(item.get("reading_num")),
                        "time": datetime.fromtimestamp(ts, timezone.utc).isoformat() if ts else None})
            if len(out) >= MAX_PER_SOURCE:
                break
        return out

    text = fetch_text(conf["url"])
    data = json.loads(text)
    out = []

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

    elif key == "bilibili":
        for item in data.get("data", {}).get("list", []):
            title = clean(item.get("title"))
            url = item.get("short_link_v2") or item.get("url") or item.get("short_link") or ""
            if not title:
                continue
            out.append({"title": title, "url": url, "hot": to_int(item.get("score")), "time": None})
            if len(out) >= MAX_PER_SOURCE:
                break

    elif key in ("zhihu", "douyin"):
        # 官方接口风控严格，改用公开聚合接口 uapis.cn
        for item in data.get("list", []):
            title = clean(item.get("title"))
            url = item.get("url") or ""
            if not title:
                continue
            out.append({"title": title, "url": url, "hot": parse_hot(item.get("hot_value")),
                        "time": item.get("update_time") or item.get("updatetime")})
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

    elif key == "eastmoney":
        for item in data.get("data", {}).get("fastNewsList", []) or []:
            title = clean(item.get("title")) or clean(item.get("summary"))
            if not title:
                continue
            code = item.get("code")
            url = "https://finance.eastmoney.com/a/{}.html".format(code) if code else ""
            show = clean(item.get("showTime"))
            t = None
            if show:
                try:
                    dt = datetime.strptime(show, "%Y-%m-%d %H:%M:%S").replace(tzinfo=BJ_TZ)
                    t = dt.astimezone(timezone.utc).isoformat()
                except ValueError:
                    t = None
            out.append({"title": title, "url": url, "hot": None, "time": t})
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
            "category": conf.get("category", "综合"),
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
    return 0 if items else 1


if __name__ == "__main__":
    sys.exit(main())
