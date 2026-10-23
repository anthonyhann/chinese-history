# chinese-history 实现方案

> **定位**：最全中华历史事件与人物、文物（全世界各个博物馆内的中华珍稀历史文物）开源结构化数据库
> **对标**：chinese-poetry（53.8k stars 的方法论已验证）
> **冷启动切片**：秦朝 · 皇帝（3 位）→ 历代皇帝（约 420 位）
> **生产模式**：AI 重度自动化流水线 + 人工审核
> **版本**：v0.1 ｜ 日期：2026-10-23

---

## 目录

1. [从 chinese-poetry 继承什么、修正什么](#一从-chinese-poetry-继承什么修正什么)
2. [数据模型设计（Schema 定稿 v1）](#二数据模型设计schema-定稿-v1)
3. [仓库目录结构与分片规范](#三仓库目录结构与分片规范)
4. [数据源策略与许可合规](#四数据源策略与许可合规)
5. [AI 生产流水线（核心）](#五ai-生产流水线核心)
6. [质量控制体系](#六质量控制体系)
7. [构建产物与分发](#七构建产物与分发)
8. [分期路线图](#八分期路线图)
9. [治理与贡献规范](#九治理与贡献规范)
10. [风险登记册](#十风险登记册)
11. [附录：种子数据示例（秦始皇）](#附录种子数据示例秦始皇)

---

## 一、从 chinese-poetry 继承什么、修正什么

### 继承（已被 53.8k stars 验证的正确决策）

| 决策 | 说明 |
|---|---|
| Data as Code | JSON 纯文本 + Git + PR 评审，clone 即数据库 |
| 分片存储 | 每文件 ≤1000 条，文件名即索引，绕开 GitHub 单文件限制 |
| MIT 许可证（代码） | 工具链代码全部 MIT |
| README 增长引擎 | 规模数字 + 可视化图 + 案例展示 + Star History |
| 低贡献门槛 | 改 JSON 提 PR，无需懂架构 |
| 情怀叙事 | "让中华历史数据像古诗词一样触手可及" |

### 修正（chinese-poetry 用 10 年踩坑换来的教训）

| chinese-poetry 的坑 | 本项目的对策 |
|---|---|
| id 是后期补加的 | **第一天所有实体带稳定 id**（可读 slug + UUID 双标识） |
| CI 只校验 JSON 能解析 | **CI 强制 JSON Schema 校验 + 引用完整性 + 出处必填** |
| 数据无出处，纠错靠信任 | **sources 是一等字段，无出处的数据不允许合并** |
| 无 release，下游无法锁定版本 | **语义化版本 tag + 每次 release 自动产出 SQLite/CSV** |
| 求 MySQL 版盖了 24 层楼靠百度网盘分发 | **GitHub Actions 自动构建 SQLite/duckdb，发布到 Releases** |
| 采集过程不可复现 | **所有 AI 生成数据保留 prompt + 原始来源记录于 `_meta`** |
| 维护者单点，issue 堆积 | M1 起招募 co-maintainer；issue 模板 + 机器人自动分类 |
| 数据许可模糊（MIT 管不了数据） | **许可分层：代码 MIT / 事实数据 CC0 / 描述文本 CC BY-SA / 图片按源站许可逐条标注** |
| 繁简之争 | 数据以繁体（古籍原貌）为准存一份，**CI 自动用 OpenCC 构建简体 release 产物** |

---

## 二、数据模型设计（Schema 定稿 v1）

### 2.1 实体关系总览

```
dynasty（朝代）──┐
reign_era（年号）─┤  基础设施表（先行建设，全局复用）
place（地名）─────┤
                 │
person（人物）─── participates ──→ event（事件）
   │  ↑ reigns_as_emperor            │
   └── related ────────→ artifact（文物）
                            │
                        holder → museum（博物馆/收藏机构）
```

**设计原则**：
- 关系用 **id 引用内嵌**（如 `event.participants: ["person.qin.yingzheng"]`），不建泛化三元组表——降低贡献门槛，chinese-poetry 式的极简主义。
- **时间双轨制**：所有时间字段 = 原始表述（年号/干支/农历原文）+ 归一化公历区间 + circa 标记 + 存疑多值。这是历史数据区别于诗词数据的核心设计。
- **出处强制**：每个实体必须有 `sources[]`；争议字段用 `disputed[]` 存多值，不删不改原值。

### 2.2 person.json（人物）

```json
{
  "id": "person.qin.yingzheng",
  "uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "嬴政",
  "name_traditional": "嬴政",
  "titles": ["秦始皇", "始皇帝", "祖龙"],
  "courtesy_name": null,
  "category": ["emperor"],
  "dynasty": "dynasty.qin",
  "birth": {
    "year": -259, "circa": false,
    "original": "秦昭襄王四十八年正月",
    "disputed": []
  },
  "death": {
    "year": -210, "circa": false,
    "original": "秦始皇三十七年七月丙寅",
    "disputed": []
  },
  "reign": {
    "start": -221, "end": -210,
    "as_emperor_start": -221,
    "note": "前259年即位为秦王，前221年称始皇帝"
  },
  "family": {
    "father": "person.qin.zichu",
    "mother": "person.qin.zhaoji",
    "children": ["person.qin.fusu", "person.qin.huhai"]
  },
  "predecessor": null,
  "successor": "person.qin.huhai",
  "bio": "（原创描述文本，CC BY-SA）",
  "events": ["event.qin.unification", "event.qin.fenshu-kengru"],
  "artifacts": ["artifact.qin.terracotta-army"],
  "wikidata": "Q7192",
  "sources": [
    {"title": "史记·秦始皇本纪", "type": "primary", "ref": "卷六"},
    {"title": "Wikidata Q7192", "type": "reference", "url": "https://www.wikidata.org/wiki/Q7192"}
  ],
  "_meta": {
    "created_by": "ai-pipeline",
    "model": "claude-x", "prompt_version": "person-v1.2",
    "verified_by": "human:@hanqiang", "verified_at": "2026-11-01",
    "version": 1
  }
}
```

### 2.3 event.json（事件）

```json
{
  "id": "event.qin.unification",
  "uuid": "...",
  "name": "秦灭六国",
  "name_traditional": "秦滅六國",
  "category": ["war", "unification"],
  "time": {
    "start": -230, "end": -221,
    "original": "秦王政十七年至二十六年",
    "precision": "year"
  },
  "place": ["place.guannei", "place.shandong"],
  "participants": [
    {"person": "person.qin.yingzheng", "role": "commander"},
    {"person": "person.qin.wangjian", "role": "general"}
  ],
  "related_events": ["event.qin.mie-han", "event.qin.mie-chu"],
  "description": "（原创描述）",
  "outcome": "秦统一中国，建立第一个中央集权王朝",
  "sources": [{"title": "史记·秦始皇本纪", "type": "primary"}],
  "_meta": {}
}
```

### 2.4 artifact.json（文物）—— 本项目独有，chinese-poetry 没有的品类

```json
{
  "id": "artifact.qin.terracotta-general",
  "uuid": "...",
  "name": "秦高级军吏俑",
  "name_traditional": "秦高級軍吏俑",
  "name_en": "Armored General, Terracotta Army",
  "dynasty": "dynasty.qin",
  "date": {"start": -221, "end": -206, "original": "秦代", "circa": true},
  "category": ["雕塑", "陶俑"],
  "material": ["陶土"],
  "dimensions": "高196厘米",
  "description": "（原创描述）",
  "current_holder": {
    "museum": "museum.emperor-qinshihuangs-mausoleum",
    "city": "西安", "country": "中国"
  },
  "provenance": "1974年陕西临潼秦始皇陵兵马俑坑出土",
  "related_persons": ["person.qin.yingzheng"],
  "related_events": [],
  "images": [
    {"url": "https://...", "license": "CC0", "source": "Metropolitan Museum Open Access"}
  ],
  "sources": [{"title": "秦始皇帝陵博物院藏品目录", "type": "institutional"}],
  "data_license": "CC0",
  "_meta": {}
}
```

> **关键合规设计**：文物的**事实数据**（年代、尺寸、收藏地）无版权，走 CC0；**图片**按各博物馆源站许可逐条标注（Met/Smithsonian 是 CC0 可直接用，大英博物馆 CC BY-NC-SA 不能商用，台北故宫 CC BY 4.0 需署名）。`images[].license` 字段强制必填。

### 2.5 基础设施表（先于一切业务数据建设）

| 表 | 内容 | 规模 | 用途 |
|---|---|---|---|
| `dynasties/` | 朝代：起讫、都城、世系 | ~30 条 | 全局锚点 |
| `reign_eras/` | 年号：年号→公历映射 | ~700 条 | 时间双轨制的换算引擎 |
| `places/` | 历史地名→今地名/坐标 | 渐进 | 地理可视化基础 |
| `museums/` | 收藏机构清单 | ~100 条 | 文物归属引用 |

`reign_eras` 示例：
```json
{"id": "era.qin.shihuang", "dynasty": "dynasty.qin", "emperor": "person.qin.yingzheng",
 "era_name": "（秦始皇以事记年，无年号）", "start": -221, "end": -210,
 "note": "秦汉之际以王公在位年数纪年，汉武帝始创年号"}
```

---

## 三、仓库目录结构与分片规范

```
chinese-history/
├── README.md                  # 增长引擎：数字+图+案例+Star History
├── LICENSE-CODE               # MIT（工具链）
├── LICENSE-DATA               # 数据许可分层说明
├── CONTRIBUTING.md            # 贡献规范（含纠错流程、出处要求）
│
├── schema/                    # JSON Schema 定义（CI 强制校验的依据）
│   ├── person.schema.json
│   ├── event.schema.json
│   ├── artifact.schema.json
│   └── common/time.schema.json
│
├── dynasties/                 # 朝代表（dynasties.json 单文件）
├── reign_eras/                # 年号表（按朝代分片）
├── places/                    # 地名表
├── museums/                   # 博物馆表
│
├── persons/                   # 人物：按朝代分目录，1000条/片
│   └── qin/
│       ├── person.qin.0.json
│       └── README.md          # 本目录说明+数据状态
├── events/
│   └── qin/
│       └── event.qin.0.json
├── artifacts/
│   └── qin/
│       └── artifact.qin.0.json
│
├── tools/                     # 全部 MIT
│   ├── validate.py            # CI 校验器（schema+引用+出处）
│   ├── build_sqlite.py        # JSON → SQLite 构建器
│   ├── build_opencc.py        # 繁→简 release 构建
│   ├── pipeline/              # AI 生产流水线脚本
│   │   ├── seed_list.py       # 种子清单生成
│   │   ├── research_agent.py  # 单实体深度研究生成
│   │   └── verify_agent.py    # 交叉核验
│   └── stats.py               # 统计与可视化图生成（README用）
│
├── dist/                      # （gitignore，CI 构建产物）
└── .github/
    ├── workflows/
    │   ├── validate.yml       # PR 门禁：JSON Schema + 引用完整性 + 出处检查
    │   └── release.yml        # tag 触发：构建 SQLite/CSV/简体版 → Release
    ├── ISSUE_TEMPLATE/        # 数据纠错 / 新增请求 / 案例展示
    └── PULL_REQUEST_TEMPLATE.md
```

**分片命名规范**：`{entity}.{dynasty_slug}.{start_index}.json`，每片 ≤1000 条。与 chinese-poetry 的 `poet.tang.0.json` 完全同构，降低老用户迁移成本。

---

## 四、数据源策略与许可合规

### 4.1 人物与事件

| 数据源 | 内容 | 许可 | 用法 |
|---|---|---|---|
| Wikidata | 人物/事件结构化事实（生卒年、朝代、亲属） | **CC0** | ✅ 主力冷启动源，SPARQL 批量拉取 |
| 中文维基百科 | 描述文本、时间线 | CC BY-SA 4.0 | ⚠️ 仅作 AI 参考，**描述文本必须原创改写**，否则继承 BY-SA 且需署名 |
| 史记/二十四史（Chinese Text Project 等公有领域版本） | 一手史料原文 | 公有领域 | ✅ sources 的"primary"类型主力 |
| 百度百科等现代整理站 | — | 受限 | ❌ 不直接抓取，仅人工参考 |

### 4.2 文物（海外开放博物馆 API 是宝藏）

| 机构 | 开放程度 | 许可 | 中华文物规模 |
|---|---|---|---|
| Metropolitan Museum (Met) | Open Access API | **CC0** | 中国藏品 ~1.4 万件全开放 |
| Smithsonian (Freer Gallery 等) | Open Access | **CC0** | 亚洲艺术重镇 |
| 大英博物馆 | Collection Online | 数据可用，图片 CC BY-NC-SA | 大量，但**图片禁商用**，逐条标注 |
| 台北故宫 | Open Data 平台 | CC BY 4.0（需署名） | 顶级中华文物 |
| 北京故宫 | 官网数字文物库 | 无开放许可 | ❌ 仅记录公开事实信息，不抓图 |
| Rijksmuseum / 吉美 / V&A | API | 各异 | 逐源核查 |

> **军规**：每条文物数据落库前，`tools/pipeline/` 自动记录源站许可快照到 `_meta.source_license`。宁缺毋滥。

---

## 五、AI 生产流水线（核心）

你的资源是"全部 AI 费用"——所以流水线的目标是：**AI 干 95% 的活，人只做终审**。

### 5.1 五阶段流水线

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ ① 种子清单 │ → │ ② 深度研究 │ → │ ③ 交叉核验 │ → │ ④ CI 校验 │ → │ ⑤ 人工PR │
│ AI 生成   │   │ AI 逐条产出 │   │ 另一模型核查│   │ 机器守门  │   │ 终审合并  │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

**① 种子清单**（`seed_list.py`）：让 LLM 生成"秦朝皇帝完整清单"，再与 Wikidata SPARQL 结果自动比对去重，产出待生产队列 `queue.json`。
- 秦朝产出：`嬴政`、`胡亥`、`子婴`（另可选：是否收录追尊君主/秦国君主，写入目录 README 的收录范围声明）

**② 深度研究**（`research_agent.py`）：每个实体一次深度 agent 调用——
- 输入：种子条目 + Wikidata 结构化事实 + schema 模板
- 要求：每个字段给出处；生卒年标注 disputed；描述文本**必须原创**（防 CC BY-SA 污染）
- 输出：schema 合规的 JSON 草稿 + 完整 prompt/响应存档到 `_meta`（**可复现性**，修正 chinese-poetry 采集不可复现的坑）

**③ 交叉核验**（`verify_agent.py`）：**用不同的模型**做核查员——
- 检查事实与 sources 是否一致（防幻觉）
- 检查 id 引用是否存在于库中
- 标记置信度：high / medium / low，low 的进人工复审队列
- 这一步是把"AI 内容农场"和"可信数据库"区分开的关键，**预算的大头应花在这里**

**④ CI 校验**（`validate.py`，GitHub Actions）：
- JSON Schema 校验（字段、类型、枚举）
- 引用完整性（所有 id 引用可解析）
- 出处检查（`sources` 非空；`artifact.images[].license` 必填）
- 重复检测（name + dynasty + birth_year 指纹）

**⑤ 人工终审**：你只审两件事——核验标记为 medium/low 的条目 + 描述文本的史实常识错误。通过即合并。

### 5.2 成本估算（量级参考）

| 阶段 | 数据量 | 单次 AI 调用 | 估算费用 |
|---|---|---|---|
| M1 秦朝皇帝+关联事件 | ~3 人物 + ~20 事件 | 23 × (研究+核验) | < ¥10 |
| M2 历代皇帝 | ~420 人物 + 关联事件 ~200 | ~620 × 2 次深度调用 | ¥100–300 |
| M3 文物（Met 中国藏品筛选） | 先有 API 结构化数据，AI 只做清洗+中文描述 | ~5000 条 | ¥200–500 |

结论：**历代皇帝全集的 AI 成本在一顿火锅和一部手机之间**，完全可行。瓶颈不在钱，在核验质量和流程设计。

---

## 六、质量控制体系

| 层级 | 机制 | 防什么 |
|---|---|---|
| L1 机器 | CI：Schema + 引用 + 出处必填 | 格式错误、悬空引用（chinese-poetry 的 rank 数据不一致问题） |
| L2 模型 | 双模型交叉核验 + 置信度分级 | AI 幻觉 |
| L3 人工 | 维护者终审 + 争议数据 `disputed[]` 共存 | 史实错误、学术争议一刀切 |
| L4 社区 | issue 纠错模板（**强制要求填写出处**）+ PR 评审 | 长尾错误 |
| L5 版本 | 每 release 打 tag + CHANGELOG 记录数据修正 | 下游可回溯 |

**收录与争议的社区规则**（写进 CONTRIBUTING.md）：
- 收录范围争议 → issue 投票（chinese-poetry 同款机制）
- 史实争议 → 不投票，多值并存 + 各标出处
- 数据修正 PR → 必须附出处，否则不合并且关闭

---

## 七、构建产物与分发

每次打 tag，GitHub Actions 自动产出（写死，不依赖任何个人网盘）：

| 产物 | 格式 | 受众 |
|---|---|---|
| `chinese-history.sqlite` | 单文件数据库 | 求 MySQL 版的那 24 层楼用户 |
| `chinese-history-simplified.zip` | OpenCC 简体全量 JSON | 简体需求方（终结繁简之争） |
| `chinese-history.csv.zip` | 平铺 CSV | Excel/数据分析用户 |
| `chinese-history.duckdb` | 分析型数据库 | 数据科学/NLP 用户 |

发布渠道：GitHub Releases（主）+ 未来可上 Hugging Face Datasets（AI 训练圈流量入口）。

---

## 八、分期路线图

| 里程碑 | 内容 | 验收标准 | 预估周期 |
|---|---|---|---|
| **M0 基建** | 仓库骨架、4 套 JSON Schema、CI 校验器、朝代表、年号表（秦汉部分）、README/CONTRIBUTING/LICENSE | CI 绿 + 基建表入库 | 1 周（AI 辅助） |
| **M1 冷启动：秦朝皇帝** | 3 位皇帝 + 关联人物（吕不韦/赵高/扶苏等 ~15 人）+ 关联事件 ~20 条，跑通五阶段流水线 | 全部数据 high 置信度；流水线文档化 | 2 周 |
| **M2 历代皇帝放量** | 秦→清约 420 位皇帝 + 年号表补全；发布 v1.0（第一个 SQLite release） | README 可打"最全历代皇帝"叙事；v1.0 tag | 1–2 月 |
| **M3 文物启动** | museums 表 + Met/Smithsonian CC0 中国文物清洗导入 + 秦汉文物精读 | 1000+ 文物条，许可逐条合规 | 1–2 月 |
| **M4 事件扩展 + 生态** | 重大历史事件系统化；招募 co-maintainer；案例展示页；HF Datasets | 3+ 下游案例；维护者 ≥2 人 | 持续 |

**M1 的收录范围声明**（写进 `persons/qin/README.md`）：
> 收录秦朝（前221–前207）正式称帝/称王者 3 人：嬴政、胡亥、子婴。秦国先君（秦襄公至秦庄襄王）规划于 M2 阶段以 `category: ["monarch"]` 收录，与 `emperor` 区分。

---

## 九、治理与贡献规范

- **分支模型**：`master` 受保护，一切经 PR；数据 PR 必须过 CI 四道检查
- **issue 模板**：数据纠错（必填：条目 id / 错误字段 / 正确值 / 出处）｜收录请求 ｜案例展示 ｜其他
- **maintainer 策略**：M2 完成时在 README 和 issue 区公开招募 co-maintainer（优先从高质量 PR 贡献者中邀请），避免 chinese-poetry 的单点困境
- **资金**：爱发电/Patreon 链接照抄 chinese-poetry 模式，但明确资金用途=AI 生产费用，形成"赞助→更多数据"的正循环叙事

---

## 十、风险登记册

| 风险 | 概率 | 影响 | 对策 |
|---|---|---|---|
| 范围爆炸（"全中华"无限大） | 高 | 致命 | 死守分期；README 明确"当前进度路线图"；收录范围声明逐目录化 |
| AI 幻觉污染数据 | 高 | 高 | 双模型核验 + 出处强制 + 置信度分级 + low 必人审 |
| 描述文本版权（洗稿维基） | 中 | 高 | 描述全部 AI 原创；CI 可加相似度抽检 |
| 文物图片许可误标 | 中 | 高 | 源站许可快照入库；非 CC0 图片默认不放，只放链接 |
| 史实争议引战 | 中 | 中 | disputed[] 多值机制 + 社区规则写明"史实争议不投票" |
| 维护者单点 | 中 | 高 | M2 招募 co-maintainer；流水线文档化到"换人能接手" |
| 与 CBDB 等学术库正面竞争 | 低 | 低 | 差异化定位：开发者友好 + CC0 + 中文优先，不做学术深度 |

---

## 附录：种子数据示例（秦始皇）

见 [二、数据模型设计](#二数据模型设计schema-定稿-v1) 中 2.2 节的 `person.qin.yingzheng` 完整示例。

**秦朝 3 位皇帝的 id 规划**：
- `person.qin.yingzheng` — 秦始皇（前259–前210；前221 称帝）
- `person.qin.huhai` — 秦二世（前230–前207；前210–前207 在位）
- `person.qin.ziying` — 秦王子婴（？–前206；在位 46 天，降刘邦，后被项羽所杀）

**M1 关联事件首批清单**（约 20 条）：
秦灭韩/赵/魏/楚/燕/齐、称始皇帝、统一度量衡与文字、书同文车同轨、修驰道、北击匈奴修长城、焚书坑儒、沙丘之变、指鹿为马、大泽乡起义、巨鹿之战、刘邦入关中、子婴投降、新安坑杀……

---

## 下一步行动

1. 你确认本方案（重点确认：Schema 字段、M1 收录范围、许可分层策略）
2. 我可以立即动手：**搭建仓库骨架（目录+Schema+CI）并产出秦朝 3 位皇帝的完整种子数据**，作为 M0+M1 的可运行演示
3. 仓库名建议 `chinese-history/chinese-history`（组织名+仓库名，已核查可用）；也可放在你的个人账号下先行起步
