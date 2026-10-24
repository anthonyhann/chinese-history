#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smithsonian Open Access 文物导入器（chinese-history pipeline）。

从 Smithsonian Open Access API 拉取亚洲艺术博物馆（NMAA）的 CC0 中国文物，
过滤出带图片的条目，输出为候选清单供人工策展（中文命名与描述需人工撰写）。

用法：
  # DEMO_KEY 有 30 请求/小时限制，正式使用请申请免费 key: https://api.data.gov/signup/
  SMITHSONIAN_API_KEY=xxx python3 tools/import_smithsonian.py --query "tang dynasty tomb figure" --out /tmp/si.json

流程：search API（rows≤100）→ 过滤 unitCode==NMAA → 过滤 CC0+有图 → 候选 JSON。
本仓库 artifacts/smithsonian/ 下的数据即由此工具的产出经人工策展后入库。
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.parse

API = "https://api.si.edu/openaccess/api/v1.0/search"


def search(query, api_key, rows=60):
    q = urllib.parse.urlencode({"q": query, "api_key": api_key, "rows": rows})
    with urllib.request.urlopen(f"{API}?{q}", timeout=60) as r:
        return json.load(r)["response"]["rows"]


def harvest(rows):
    out = []
    for r in rows:
        if r.get("unitCode") != "NMAA":  # 亚洲艺术博物馆（Freer|Sackler）
            continue
        om = r.get("content", {}).get("descriptiveNonRepeating", {}).get("online_media", {})
        media = (om.get("media") or [{}])[0]
        if not media.get("content") or media.get("usage", {}).get("access") != "CC0":
            continue
        ft = r.get("content", {}).get("freetext", {})
        idents = [x["content"] for x in ft.get("identifier", [])]
        acc = next((i for i in idents if i[0] in "FSR" and "." in i), None)
        if not acc:
            continue
        out.append({
            "accession": acc, "title": r["title"],
            "date": "; ".join(x["content"] for x in ft.get("date", [])[:1]),
            "physical": "; ".join(x["content"] for x in ft.get("physicalDescription", [])[:1]),
            "credit": "; ".join(x["content"] for x in ft.get("creditLine", [])[:1]),
            "image_cc0": media["content"],
            "object_url": f"https://asia.si.edu/object/{acc}",
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rows", type=int, default=60)
    args = ap.parse_args()
    key = os.environ.get("SMITHSONIAN_API_KEY", "DEMO_KEY")
    rows = search(args.query, key, args.rows)
    cand = harvest(rows)
    with open(args.out, "w") as f:
        json.dump(cand, f, ensure_ascii=False, indent=1)
    print(f"rows={len(rows)} harvested={len(cand)} -> {args.out}")
    print("注意：候选需人工撰写中文名称/描述并选择朝代后，才能按 schema 入库")


if __name__ == "__main__":
    main()
