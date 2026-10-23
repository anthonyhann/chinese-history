#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chinese-history 数据校验器（零依赖，仅标准库）。

CI 可执行契约，与 schema/*.json（可读规范）保持一致：
  1. 所有 JSON 可解析
  2. 必填字段 / 字段类型 / 枚举值
  3. id 规则与全局唯一
  4. 出处强制（sources 非空，每条含 title + type）
  5. 引用完整性（person/event/artifact/dynasty/place/museum id 必须可解析）
  6. 文物图片许可规则（url 仅当 license=CC0；否则必须用 link）
  7. 时间结构（year 为整数；start <= end）

用法：python3 tools/validate.py   # 在仓库根目录运行，失败时 exit 1
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ID_PATTERN = re.compile(r"^[a-z]+(\.[a-z0-9-]+)+$")  # entity.domain[.slug...]
UUID_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
)
SOURCE_TYPES = {"primary", "secondary", "reference", "institutional", "archaeological"}
IMG_LICENSES = {"CC0", "CC BY", "CC BY-SA", "CC BY-NC-SA", "copyrighted"}

# 数据目录 -> 实体类型
DATA_DIRS = {
    "persons": "person",
    "events": "event",
    "artifacts": "artifact",
}

errors = []
warnings = []


def err(where, msg):
    errors.append(f"[{where}] {msg}")


def warn(where, msg):
    warnings.append(f"[{where}] {msg}")


def load_json_files():
    """返回 [(filepath, records: list, entity_type)]"""
    datasets = []
    for top, etype in DATA_DIRS.items():
        base = os.path.join(ROOT, top)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            for fn in sorted(files):
                if not fn.endswith(".json"):
                    continue
                fp = os.path.join(dirpath, fn)
                rel = os.path.relpath(fp, ROOT)
                try:
                    with open(fp, encoding="utf-8") as f:
                        data = json.load(f)
                except Exception as e:
                    err(rel, f"JSON 解析失败: {e}")
                    continue
                if not isinstance(data, list):
                    err(rel, f"数据文件必须是 JSON 数组: {rel}")
                    continue
                datasets.append((rel, data, etype))
    # 基础设施表（单对象或数组皆可，字段校验从宽，但仍需 id/name）
    # 基础设施表
    infra = {"dynasties": "dynasty", "reign_eras": "reign_era",
             "places": "place", "museums": "museum"}
    for top, etype in infra.items():
        base = os.path.join(ROOT, top)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            for fn in sorted(files):
                if not fn.endswith(".json"):
                    continue
                fp = os.path.join(dirpath, fn)
                rel = os.path.relpath(fp, ROOT)
                try:
                    with open(fp, encoding="utf-8") as f:
                        data = json.load(f)
                except Exception as e:
                    err(rel, f"JSON 解析失败: {e}")
                    continue
                records = data if isinstance(data, list) else [data]
                datasets.append((rel, records, etype))
    return datasets


def check_time_point(where, field, tp):
    if tp is None:
        return
    if not isinstance(tp, dict) or not isinstance(tp.get("year"), int):
        err(where, f"{field} 必须是含整数 year 的对象")
        return
    for d in tp.get("disputed", []):
        if not isinstance(d, dict) or not isinstance(d.get("year"), int) or not d.get("source"):
            err(where, f"{field}.disputed 每项必须含整数 year 和 source")


def check_time_range(where, field, tr):
    if tr is None:
        return
    if not isinstance(tr, dict):
        err(where, f"{field} 必须是对象")
        return
    s, e = tr.get("start"), tr.get("end")
    if not isinstance(s, int) or not isinstance(e, int):
        err(where, f"{field}.start/end 必须是整数")
    elif s > e:
        err(where, f"{field}.start({s}) 晚于 end({e})")


def check_sources(where, sources):
    if not isinstance(sources, list) or len(sources) == 0:
        err(where, "sources 必须是非空数组（无出处的数据不允许合并）")
        return
    for i, s in enumerate(sources):
        if not isinstance(s, dict) or not s.get("title"):
            err(where, f"sources[{i}] 缺少 title")
        elif s.get("type") not in SOURCE_TYPES:
            err(where, f"sources[{i}].type 必须是 {sorted(SOURCE_TYPES)} 之一")


def check_base(where, rec, infra=False):
    rid = rec.get("id", "<no-id>")
    w = f"{where} {rid}"
    if not isinstance(rec.get("id"), str) or not ID_PATTERN.match(rec["id"]):
        err(w, "id 必须匹配 entity.domain[.slug]（小写字母数字连字符）")
    uuid_v = rec.get("uuid")
    # 基础设施表（dynasty/place/museum/reign_era）不强制 uuid；业务实体强制
    if not infra and (not isinstance(uuid_v, str) or not UUID_PATTERN.match(uuid_v or "")):
        err(w, "uuid 缺失或格式非法")
    if not isinstance(rec.get("name"), str) or not rec["name"]:
        err(w, "name 缺失")
    check_sources(w, rec.get("sources"))
    meta = rec.get("_meta")
    if not isinstance(meta, dict) or meta.get("created_by") not in ("ai-pipeline", "human", "import"):
        err(w, "_meta.created_by 必须是 ai-pipeline/human/import")
    return rid


def refs_of(rec, etype):
    """提取记录中的所有 id 引用 (字段路径, 被引用id)"""
    out = []

    def add(path, v):
        if isinstance(v, str) and v:
            out.append((path, v))
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, str) and x:
                    out.append((path, x))

    if etype == "person":
        add("dynasty", rec.get("dynasty"))
        fam = rec.get("family") or {}
        add("family.father", fam.get("father"))
        add("family.mother", fam.get("mother"))
        add("family.spouses", fam.get("spouses"))
        add("family.children", fam.get("children"))
        add("predecessor", rec.get("predecessor"))
        add("successor", rec.get("successor"))
        add("events", rec.get("events"))
        add("artifacts", rec.get("artifacts"))
    elif etype == "event":
        add("place", rec.get("place"))
        add("related_events", rec.get("related_events"))
        for p in rec.get("participants", []):
            if isinstance(p, dict):
                add("participants[].person", p.get("person"))
    elif etype == "artifact":
        add("dynasty", rec.get("dynasty"))
        holder = rec.get("current_holder") or {}
        add("current_holder.museum", holder.get("museum"))
        add("related_persons", rec.get("related_persons"))
        add("related_events", rec.get("related_events"))
    elif etype in ("reign_era",):
        add("dynasty", rec.get("dynasty"))
        add("emperor", rec.get("emperor"))
    return out


def check_person(where, rec):
    w = f"{where} {rec.get('id')}"
    if not rec.get("category"):
        err(w, "category 必须非空")
    if not rec.get("dynasty"):
        err(w, "dynasty 必填")
    check_time_point(where, f"{rec.get('id')}.birth", rec.get("birth"))
    check_time_point(where, f"{rec.get('id')}.death", rec.get("death"))
    reign = rec.get("reign")
    if reign is not None:
        if not isinstance(reign, dict) or not isinstance(reign.get("start"), int) or not isinstance(reign.get("end"), int):
            err(w, "reign 必须是含整数 start/end 的对象或 null")
        elif reign["start"] > reign["end"]:
            err(w, f"reign.start({reign['start']}) 晚于 reign.end({reign['end']})")
    if "emperor" in (rec.get("category") or []):
        for f in ("reign", "predecessor", "successor"):
            if f not in rec:
                err(w, f"emperor 类人物必须显式声明 {f}（可为 null）")
    wd = rec.get("wikidata")
    if wd is not None and not re.match(r"^Q[0-9]+$", str(wd)):
        err(w, "wikidata 必须是 Q 编号或 null")


def check_event(where, rec):
    w = f"{where} {rec.get('id')}"
    if not rec.get("category"):
        err(w, "category 必须非空")
    check_time_range(where, f"{rec.get('id')}.time", rec.get("time"))
    if not rec.get("description"):
        warn(w, "description 为空")
    for p in rec.get("participants", []):
        if not isinstance(p, dict) or not p.get("person") or not p.get("role"):
            err(w, "participants 每项必须含 person 和 role")


def check_artifact(where, rec):
    w = f"{where} {rec.get('id')}"
    if not rec.get("dynasty"):
        err(w, "dynasty 必填")
    holder = rec.get("current_holder")
    if not isinstance(holder, dict) or not holder.get("museum"):
        err(w, "current_holder.museum 必填")
    if rec.get("data_license") not in ("CC0", "CC BY-SA"):
        err(w, "data_license 必须是 CC0 或 CC BY-SA")
    check_time_range(where, f"{rec.get('id')}.date", rec.get("date"))
    for i, img in enumerate(rec.get("images", [])):
        lic = img.get("license")
        if lic not in IMG_LICENSES:
            err(w, f"images[{i}].license 必须是 {sorted(IMG_LICENSES)} 之一")
        if not img.get("source"):
            err(w, f"images[{i}].source 必填")
        if img.get("url") and lic != "CC0":
            err(w, f"images[{i}] 许可为 {lic}，不得直接放 url，请改用 link")
        if not img.get("url") and not img.get("link"):
            err(w, f"images[{i}] 必须含 url 或 link 之一")


CHECKERS = {"person": check_person, "event": check_event, "artifact": check_artifact}


def main():
    datasets = load_json_files()
    if not datasets:
        err("repo", "未发现任何数据文件")
    all_ids = {}
    fingerprints = {}

    # 第一遍：基础校验 + 收集 id
    infra_types = {"dynasty", "place", "museum", "reign_era"}
    for rel, records, etype in datasets:
        for rec in records:
            if not isinstance(rec, dict):
                err(rel, "记录必须是对象")
                continue
            rid = check_base(rel, rec, infra=etype in infra_types)
            if rid in all_ids:
                err(rel, f"id 重复: {rid}（已存在于 {all_ids[rid]}）")
            else:
                all_ids[rid] = rel
            fp = (rec.get("name"), etype)
            if etype in ("person", "event") and fp in fingerprints:
                warn(rel, f"疑似重复条目: {rec.get('name')}（与 {fingerprints[fp]}）")
            fingerprints[fp] = rel
            if etype in CHECKERS:
                CHECKERS[etype](rel, rec)

    # 第二遍：引用完整性
    for rel, records, etype in datasets:
        for rec in records:
            if not isinstance(rec, dict):
                continue
            for path, ref in refs_of(rec, etype):
                if ref not in all_ids:
                    err(rel, f"{rec.get('id')}: 悬空引用 {path} -> {ref}")

    for w_ in warnings:
        print(f"WARN  {w_}")
    if errors:
        for e in errors:
            print(f"ERROR {e}")
        print(f"\n校验失败：{len(errors)} 个错误，{len(warnings)} 个警告")
        sys.exit(1)
    total = sum(len(r) for _, r, _ in datasets)
    print(f"校验通过：{len(datasets)} 个文件，{total} 条记录，{len(all_ids)} 个实体 id，{len(warnings)} 个警告")


if __name__ == "__main__":
    main()
