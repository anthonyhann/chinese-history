<div align="center">

# chinese-history 📜

### 人物 · 事件 · 文物：中华历史的开源结构化数据库

49 位历史人物 · 39 个历史事件 · 77 个年号 · 17 个朝代——全部 JSON 分发，clone 即用

[![代码许可: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![事实数据: CC0](https://img.shields.io/badge/facts-CC0-green.svg)](LICENSE-DATA)
[![描述文本: CC BY-SA 4.0](https://img.shields.io/badge/text-CC%20BY--SA%204.0-orange.svg)](LICENSE-DATA)
[![实体记录: 179](https://img.shields.io/badge/entities-203-red.svg)](#-数据集)
[![数据校验: 通过](https://img.shields.io/badge/validation-passing-brightgreen.svg)](tools/validate.py)

[🚀 快速开始](#-快速开始) · [📦 数据集](#-数据集) · [📐 Schema](schema/) · [🤝 贡献](CONTRIBUTING.md) · [English](README.en.md) · [llms.txt](llms.txt)

</div>

---

> 灵感来自 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry)：古诗词有了最全的开源数据库，历史也该有一个。
> 区别在于：历史数据有学术争议，所以本项目把**出处和存疑标注**做成了一等公民。

## 📖 长这样

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

一行命令查数据：

```bash
jq '.[] | select(.titles[]? | contains("秦始皇"))' persons/qin/person.qin.0.json
```

## 🚀 快速开始

**3 步，零依赖（仅 Python 标准库）：**

```bash
git clone https://github.com/anthonyhann/chinese-history.git  # ① 拿数据
cd chinese-history
python3 tools/validate.py                                     # ② 验证数据完整性（203 条）
jq '.[] | .name' persons/han/person.han.0.json                # ③ 开始用（或任何语言的 JSON 库）
```

**给你的 AI Agent 用**（把这句话粘贴给它）：

> 请阅读 https://github.com/anthonyhann/chinese-history/blob/master/llms.txt ，了解 chinese-history 的结构与 Schema 后，帮我基于它的数据构建应用。

## 📦 数据集

每条数据必带出处（`sources`），无出处无法通过 CI——这是本仓库与"AI 内容农场"的分界线。

| 数据集 | 记录数 | 状态 |
|---|---:|---|
| [人物 · 秦](persons/qin/) | 18 | ✅ M1 种子 |
| [人物 · 汉](persons/han/) | 31 | ✅ M2 已放量（两汉全部帝系） |
| [事件 · 秦](events/qin/) | 20 | ✅ M1 种子 |
| [事件 · 汉](events/han/) | 19 | ✅ M2 新增 |
| [文物](artifacts/qin/) | 1 | 🔬 Schema 验证样例，M3 放量 |
| [朝代](dynasties/) | 17 | ✅ 基础表 |
| [年号纪年](reign_eras/) | 77（秦 3 + 汉 74） | ✅ 秦含"无年号"记录 |
| [地名](places/) | 14 | ✅ 含今地名与坐标 |
| [博物馆](museums/) | 6 | ✅ 含各馆开放数据许可状态 |

## 📐 三个设计决策（与诗词库的关键差异）

1. **id 锚点第一天就有**：`person.qin.yingzheng` 可读 slug + UUID 双标识，人物/事件/文物/地名互相引用，发布即冻结，永不复用
2. **时间双轨制**：史料原文纪年（"秦始皇三十七年七月丙寅"）+ 归一化公历（`-210`）+ `circa` 约数 + `disputed[]` 学术争议多值并存——争议不投票，各标出处
3. **出处强制 + 生产可复现**：每条数据的 AI 生成模型与 prompt 版本记录在 `_meta`，人工核验后标 `verified_by`

## ⚠️ 什么时候别用它（诚实边界）

- **做学术研究/论文** → 请用 [CBDB](https://cbdb.fas.harvard.edu/) 等专业学术库。本库定位是开发者友好与中文优先，不是学术深度
- **需要经人工核验的可靠性** → 当前多数条目标记为 `ai-pipeline` 生成、`verified_by` 为空。请以 `sources` 自行核对，纠错请提 PR
- **需要完整二十四史全文** → 我们只存结构化事实，不存史料全文

## 🗺️ 路线图

- ✅ **M0 基建**：Schema / CI 校验器 / 朝代·年号·地名·博物馆基础表
- ✅ **M1 秦朝冷启动**：3 帝 + 15 关联人物 + 20 事件
- ✅ **M2 汉代放量**：两汉 31 帝系 + 74 年号 + 19 个重大事件（当前）
- 🔜 **M3 文物**：Met / Smithsonian 等 CC0 开放馆藏中华文物清洗导入
- 🔜 **M3+**：SQLite 构建器已可用（`python3 tools/build_sqlite.py`），release 自动化见 `.github/workflows/release.yml`
- 🔜 **M4**：历代皇帝全量、案例展示

## 💬 用了我们的数据？

做了应用（网站/App/可视化/AI 项目）？开一个 issue 附上链接，我们会收录进案例展示。数据纠错 PR 请**注明出处**，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📝 更新日志

- **2026-10-23** M2 补：汉代 19 个重大事件 + SQLite 构建器，实体总数 203
- **2026-10-23** M2：汉代 31 帝系人物 + 74 个年号入库，实体总数 179
- **2026-10-23** M0+M1：仓库骨架、CI 校验器、秦朝 18 人物 + 20 事件种子数据

## License

| 内容 | 许可 |
|---|---|
| 工具链代码 | [MIT](LICENSE-CODE) |
| 事实数据（年代、谱系、收藏地等） | [CC0](LICENSE-DATA) |
| 描述文本（bio/description，均为原创） | [CC BY-SA 4.0](LICENSE-DATA) |
| 文物图片 | 逐条标注源站许可，非 CC0 只放链接 |
