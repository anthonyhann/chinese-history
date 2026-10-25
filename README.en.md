<div align="center">

# chinese-history 📜

### Persons · Events · Artifacts: the open structured database of Chinese history

370 historical figures (94% linked to Wikidata QIDs) · 154 events · 551 era names · 49 dynasties/regimes — all in JSON, clone and build

[![Code license: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![Facts: CC0](https://img.shields.io/badge/facts-CC0-green.svg)](LICENSE-DATA)
[![Texts: CC BY-SA 4.0](https://img.shields.io/badge/text-CC%20BY--SA%204.0-orange.svg)](LICENSE-DATA)
[![Entities: 179](https://img.shields.io/badge/entities-1224-red.svg)](#-datasets)
[![Validation: passing](https://img.shields.io/badge/validation-passing-brightgreen.svg)](tools/validate.py)

[🚀 Quickstart](#-quickstart) · [📦 Datasets](#-datasets) · [📐 Schema](schema/) · [🤝 Contributing](CONTRIBUTING.md) · [中文](README.md) · [llms.txt](llms.txt)

</div>

---

> Inspired by [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) — the de-facto open database of classical Chinese poetry (53k+ stars). Chinese history deserves the same.
> The key difference: historical data carries academic disputes, so **provenance and disputed-value markup are first-class citizens** in this schema.

## 📖 What it looks like

```json
{
  "id": "person.qin.yingzheng",
  "name": "嬴政",
  "titles": ["秦始皇", "始皇帝"],
  "birth": {"year": -259, "original": "秦昭襄王四十八年正月"},
  "reign": {"start": -247, "end": -210},
  "successor": "person.qin.huhai",
  "sources": [{"title": "史记·秦始皇本纪", "type": "primary", "ref": "卷六"}]
}
```

Query it in one line:

```bash
jq '.[] | select(.titles[]? | contains("秦始皇"))' persons/qin/person.qin.0.json
```

## 🚀 Quickstart

**3 steps, zero dependencies (Python stdlib only):**

```bash
git clone https://github.com/anthonyhann/chinese-history.git  # ① get the data
cd chinese-history
python3 tools/validate.py                                     # ② verify integrity (1224 records)
jq '.[] | .name' persons/han/person.han.0.json                # ③ use it (or any JSON lib)
```

**For AI agents** (paste this to yours):

> Read https://github.com/anthonyhann/chinese-history/blob/master/llms.txt to learn the structure and schema of chinese-history, then help me build an app on top of it.

## 📦 Datasets

Every record must carry `sources` — records without provenance fail CI. That is the line between this repo and an AI content farm.

| Dataset | Records | Status |
|---|---:|---|
| [Persons · Qin](persons/qin/) | 18 | ✅ M1 seed |
| [Persons · Han](persons/han/) | 31 | ✅ M2 (complete imperial lines of both Han) |
| [Persons · Wei-Jin & N/S Dynasties](persons/) | 86 | ✅ v0.2.0 |
| [Persons · Sui-Tang & Five Dynasties](persons/) | 39 | ✅ v0.3.0 (incl. Wu Zetian) |
| [Persons · Song-Liao-Jin](persons/) | 37 | ✅ v0.4.0 |
| [Persons · Yuan-Ming-Qing](persons/) | 43 | ✅ v1.0.0 (imperial line complete through 1912) |
| [Persons · Ten Kingdoms/W. Xia/Dali](persons/) | 34 | ✅ v1.1.0 |
| [Persons · Ministers & Generals](persons/) | 82 | ✅ two batches |
| [Events · Qin](events/qin/) | 20 | ✅ M1 seed |
| [Events · Han](events/han/) | 19 | ✅ M2 (new) |
| [Events · Wei-Jin & N/S Dynasties](events/) | 12 | ✅ v0.2.0 (Guandu, Chibi, Feishui…) |
| [Events · Sui-Tang](events/) | 15 | ✅ v0.3.0 (Grand Canal, Xuanwu Gate, An Lushan…) |
| [Events · Song-Liao-Jin](events/) | 12 | ✅ v0.4.0 (Chenqiao, Chanyuan, Jingkang, Yashan…) |
| [Events · Yuan-Ming-Qing](events/) | 15 | ✅ v1.0.0 |
| [Events · density pass](events/) | 61 | ✅ v1.2.0 (Canhepi, Baijiangkou, Sarhū, Self-Strengthening…) |
| [Artifacts · Qin](artifacts/qin/) | 1 | 🔬 schema sample |
| [Artifacts · Met](artifacts/met/) | 24 | ✅ v1.1.0 (CC0) |
| [Artifacts · Smithsonian NMAA](artifacts/smithsonian/) | 15 | ✅ v1.2.0 (CC0) |
| [Artifacts · British Museum](artifacts/british-museum/) | 3 | ✅ v1.3.0 (NC = link only) |
| [Artifacts · Cleveland](artifacts/cleveland/) | 19 | ✅ v1.4.0 (CC0, keyless API) |
| [Dynasties/regimes](dynasties/) | 49 | ✅ base table |
| [Era names](reign_eras/) | 551 | ✅ incl. Ten Kingdoms & Western Xia |
| [Places](places/) | 31 | ✅ with modern names & coordinates |
| [Museums](museums/) | 6 | ✅ with open-data license status |

## 📐 Three design decisions (what differs from the poetry repo)

1. **ID anchors from day one**: readable slug (`person.qin.yingzheng`) + UUID. Persons, events, artifacts, places cross-reference by id; ids are frozen on publish and never reused
2. **Dual-track time**: original reign-era notation ("秦始皇三十七年七月丙寅") + normalized Gregorian year (`-210` = 210 BC) + `circa` for approximations + `disputed[]` for competing scholarly claims — disputes are never voted away, each value keeps its own source
3. **Mandatory provenance + reproducible production**: every record's generating model and prompt version are logged in `_meta`; human verification is marked via `verified_by`

## ⚠️ When NOT to use it

- **Academic research** → use [CBDB](https://cbdb.fas.harvard.edu/) (Harvard/Academia Sinica/PKU). This repo optimizes for developer-friendliness and Chinese-first access, not scholarly depth
- **If you need human-verified reliability** → most records are currently `ai-pipeline` generated with empty `verified_by`. Check `sources` yourself; corrections via PR are welcome
- **If you need full texts of the Twenty-Four Histories** → we store structured facts, not full source texts

## 🗺️ Roadmap

- ✅ **M0 Infrastructure**: schemas, CI validator, base tables (dynasties / eras / places / museums)
- ✅ **M1 Qin cold start**: 3 rulers + 15 related figures + 20 events
- ✅ **M2 Han scale-up**: 31 imperial figures + 74 era names + 19 major events
- ✅ **M2.5 Wei-Jin & N/S Dynasties**: 86 rulers + 182 era names + 12 major events
- ✅ **M2.6 Sui-Tang & Five Dynasties**: 39 rulers + 95 era names + 15 major events
- ✅ **M2.7 Song-Liao-Jin**: 37 rulers + 100 era names + 12 major events
- ✅ **v1.0.0 Yuan-Ming-Qing**: imperial line complete, 221 BC – 1912
- ✅ **v1.1.0**: 34 rulers + 41 ministers + 24 Met CC0 artifacts
- ✅ **v1.2.0**: +41 ministers, +61 events, +15 Smithsonian artifacts
- ✅ **v1.3.0**: 94% Wikidata alignment + 3 BM artifacts
- ✅ **v1.4.0**: 19 Cleveland CC0 artifacts (current)
- 🔜 **M3 Artifacts**: CC0 Chinese artifacts from Met / Smithsonian open collections
- 🔜 **M3+**: SQLite builder is ready (`python3 tools/build_sqlite.py`); release automation in `.github/workflows/release.yml`
- 🔜 **M4**: all dynasties' emperors, showcase gallery

## 💬 Built something with this data?

Made an app (site / app / visualization / AI project)? Open an issue with a link and we'll feature it. Data corrections via PR **must cite sources** — see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📝 Changelog

- **2026-10-25** v1.4.0: +19 Cleveland CC0 artifacts; 1224 entities
- **2026-10-25** v1.3.0: 94% Wikidata alignment + 3 BM artifacts; 1204 entities
- **2026-10-24** v1.2.0: +41 ministers, +61 events, +15 Smithsonian artifacts; 1201 entities
- **2026-10-24** v1.1.0: +34 rulers, +41 ministers, +24 Met artifacts; 1084 entities
- **2026-10-24** v1.0.0: Yuan-Ming-Qing; 922 entities; imperial line complete through 1912
- **2026-10-23** v0.4.0: Song-Liao-Jin — 37 rulers, 100 era names, 12 events; 815 entities total
- **2026-10-23** v0.3.0: Sui-Tang & Five Dynasties — 39 rulers, 95 era names, 15 events; 660 entities total
- **2026-10-23** v0.2.0: Wei-Jin & N/S Dynasties — 86 rulers, 182 era names, 12 events; 503 entities total
- **2026-10-23** M2.1: 19 Han major events + SQLite builder; 203 entities total
- **2026-10-23** M2: 31 Han imperial figures + 74 era names; 179 entities total
- **2026-10-23** M0+M1: repo skeleton, CI validator, Qin seed data (18 persons + 20 events)

## License

| Content | License |
|---|---|
| Tooling code | [MIT](LICENSE-CODE) |
| Factual data (dates, genealogy, holdings) | [CC0](LICENSE-DATA) |
| Descriptive texts (bio/description, original) | [CC BY-SA 4.0](LICENSE-DATA) |
| Artifact images | per-record source license; non-CC0 images are linked, never hosted |
