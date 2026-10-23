#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chinese-history SQLite 构建器（零依赖，仅标准库）。

把仓库内全部 JSON 数据构建为单文件 SQLite 数据库：
  dist/chinese-history.sqlite

表结构：
  dynasties / reign_eras / places / museums / persons / events / artifacts
  sources（每个实体 1..n 条出处，entity_id 外键）
  event_participants（事件-人物-角色三元组）
  meta（构建信息）

每个实体表都含 json TEXT 列（完整原始记录），常用字段提升为列便于 SQL 查询。
用法：python3 tools/build_sqlite.py
"""
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(DIST, "chinese-history.sqlite")

SCHEMA = """
CREATE TABLE dynasties (
  id TEXT PRIMARY KEY, name TEXT, name_traditional TEXT,
  start INTEGER, end INTEGER, capital TEXT, json TEXT NOT NULL
);
CREATE TABLE reign_eras (
  id TEXT PRIMARY KEY, name TEXT, dynasty TEXT, emperor TEXT,
  start INTEGER, end INTEGER, json TEXT NOT NULL
);
CREATE TABLE places (
  id TEXT PRIMARY KEY, name TEXT, name_traditional TEXT, type TEXT,
  modern_name TEXT, lat REAL, lng REAL, json TEXT NOT NULL
);
CREATE TABLE museums (
  id TEXT PRIMARY KEY, name TEXT, name_en TEXT, city TEXT, country TEXT,
  open_license TEXT, json TEXT NOT NULL
);
CREATE TABLE persons (
  id TEXT PRIMARY KEY, uuid TEXT, name TEXT, name_traditional TEXT,
  category TEXT, dynasty TEXT, titles TEXT,
  birth_year INTEGER, death_year INTEGER,
  reign_start INTEGER, reign_end INTEGER,
  predecessor TEXT, successor TEXT, wikidata TEXT,
  bio TEXT, verified INTEGER DEFAULT 0, json TEXT NOT NULL
);
CREATE INDEX idx_persons_dynasty ON persons(dynasty);
CREATE INDEX idx_persons_reign ON persons(reign_start);
CREATE TABLE events (
  id TEXT PRIMARY KEY, uuid TEXT, name TEXT, name_traditional TEXT,
  category TEXT, start INTEGER, end INTEGER,
  description TEXT, outcome TEXT, verified INTEGER DEFAULT 0, json TEXT NOT NULL
);
CREATE INDEX idx_events_time ON events(start);
CREATE TABLE artifacts (
  id TEXT PRIMARY KEY, uuid TEXT, name TEXT, name_en TEXT,
  dynasty TEXT, category TEXT, museum TEXT,
  date_start INTEGER, date_end INTEGER, data_license TEXT,
  description TEXT, verified INTEGER DEFAULT 0, json TEXT NOT NULL
);
CREATE TABLE sources (
  entity_id TEXT, title TEXT, type TEXT, ref TEXT, url TEXT,
  FOREIGN KEY(entity_id) REFERENCES persons(id)
);
CREATE INDEX idx_sources_entity ON sources(entity_id);
CREATE TABLE event_participants (
  event_id TEXT, person_id TEXT, role TEXT,
  FOREIGN KEY(event_id) REFERENCES events(id),
  FOREIGN KEY(person_id) REFERENCES persons(id)
);
CREATE INDEX idx_participants_event ON event_participants(event_id);
CREATE INDEX idx_participants_person ON event_participants(person_id);
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
"""


def load_dir(top):
    out = []
    base = os.path.join(ROOT, top)
    if not os.path.isdir(base):
        return out
    for dirpath, _d, files in os.walk(base):
        for fn in sorted(files):
            if fn.endswith(".json"):
                with open(os.path.join(dirpath, fn), encoding="utf-8") as f:
                    out.extend(json.load(f))
    return out


def j(obj):
    return json.dumps(obj, ensure_ascii=False)


def jarr(lst):
    return ",".join(lst) if lst else None


def main():
    os.makedirs(DIST, exist_ok=True)
    if os.path.exists(OUT):
        os.remove(OUT)
    db = sqlite3.connect(OUT)
    db.executescript(SCHEMA)

    counts = {}

    for r in load_dir("dynasties"):
        db.execute("INSERT INTO dynasties VALUES (?,?,?,?,?,?,?)",
                   (r["id"], r["name"], r.get("name_traditional"), r.get("start"),
                    r.get("end"), r.get("capital"), j(r)))
    counts["dynasties"] = db.execute("SELECT COUNT(*) FROM dynasties").fetchone()[0]

    for r in load_dir("reign_eras"):
        db.execute("INSERT INTO reign_eras VALUES (?,?,?,?,?,?,?)",
                   (r["id"], r.get("era_name") or r["name"], r.get("dynasty"),
                    r.get("emperor"), r.get("start"), r.get("end"), j(r)))
    counts["reign_eras"] = db.execute("SELECT COUNT(*) FROM reign_eras").fetchone()[0]

    for r in load_dir("places"):
        c = r.get("coordinates") or {}
        db.execute("INSERT INTO places VALUES (?,?,?,?,?,?,?,?)",
                   (r["id"], r["name"], r.get("name_traditional"), r.get("type"),
                    r.get("modern_name"), c.get("lat"), c.get("lng"), j(r)))
    counts["places"] = db.execute("SELECT COUNT(*) FROM places").fetchone()[0]

    for r in load_dir("museums"):
        od = r.get("open_data") or {}
        db.execute("INSERT INTO museums VALUES (?,?,?,?,?,?,?)",
                   (r["id"], r["name"], r.get("name_en"), r.get("city"),
                    r.get("country"), od.get("license"), j(r)))
    counts["museums"] = db.execute("SELECT COUNT(*) FROM museums").fetchone()[0]

    for r in load_dir("persons"):
        b, d, g = r.get("birth") or {}, r.get("death") or {}, r.get("reign") or {}
        verified = 1 if (r.get("_meta") or {}).get("verified_by") else 0
        db.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (r["id"], r.get("uuid"), r["name"], r.get("name_traditional"),
                    jarr(r.get("category")), r.get("dynasty"), jarr(r.get("titles")),
                    b.get("year"), d.get("year"), g.get("start"), g.get("end"),
                    r.get("predecessor"), r.get("successor"), r.get("wikidata"),
                    r.get("bio"), verified, j(r)))
        for s in r.get("sources", []):
            db.execute("INSERT INTO sources VALUES (?,?,?,?,?)",
                       (r["id"], s.get("title"), s.get("type"), s.get("ref"), s.get("url")))
    counts["persons"] = db.execute("SELECT COUNT(*) FROM persons").fetchone()[0]

    for r in load_dir("events"):
        t = r.get("time") or {}
        verified = 1 if (r.get("_meta") or {}).get("verified_by") else 0
        db.execute("INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                   (r["id"], r.get("uuid"), r["name"], r.get("name_traditional"),
                    jarr(r.get("category")), t.get("start"), t.get("end"),
                    r.get("description"), r.get("outcome"), verified, j(r)))
        for s in r.get("sources", []):
            db.execute("INSERT INTO sources VALUES (?,?,?,?,?)",
                       (r["id"], s.get("title"), s.get("type"), s.get("ref"), s.get("url")))
        for p in r.get("participants", []):
            db.execute("INSERT INTO event_participants VALUES (?,?,?)",
                       (r["id"], p.get("person"), p.get("role")))
    counts["events"] = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    for r in load_dir("artifacts"):
        dt = r.get("date") or {}
        holder = r.get("current_holder") or {}
        verified = 1 if (r.get("_meta") or {}).get("verified_by") else 0
        db.execute("INSERT INTO artifacts VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (r["id"], r.get("uuid"), r["name"], r.get("name_en"), r.get("dynasty"),
                    jarr(r.get("category")), holder.get("museum"), dt.get("start"),
                    dt.get("end"), r.get("data_license"), r.get("description"),
                    verified, j(r)))
        for s in r.get("sources", []):
            db.execute("INSERT INTO sources VALUES (?,?,?,?,?)",
                       (r["id"], s.get("title"), s.get("type"), s.get("ref"), s.get("url")))
    counts["artifacts"] = db.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0]

    db.execute("INSERT INTO meta VALUES ('built_at', ?)",
               (datetime.now(timezone.utc).isoformat(),))
    db.execute("INSERT INTO meta VALUES ('source', 'chinese-history git repo')")
    db.commit()

    total = sum(counts.values())
    detail = ", ".join(f"{k}={v}" for k, v in counts.items())
    print(f"构建完成: {OUT}")
    print(f"共 {total} 条记录（{detail}）")
    print(f"文件大小: {os.path.getsize(OUT) / 1024:.0f} KB")
    db.close()


if __name__ == "__main__":
    main()
