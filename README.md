<div align="center">

# chinese-history 📜

### 人物 · 事件 · 文物：中华历史的开源结构化数据库

370 位历史人物（94% 已对齐 Wikidata QID） · 154 个历史事件 · 551 个年号 · 49 个朝代/政权——全部 JSON 分发，clone 即用

[![Release](https://img.shields.io/github/v/release/anthonyhann/chinese-history?label=release)](https://github.com/anthonyhann/chinese-history/releases)
[![SQLite 下载](https://img.shields.io/badge/%E2%AC%87%20SQLite-1.8MB-brightgreen)](https://github.com/anthonyhann/chinese-history/releases/latest)
[![JSON 快照](https://img.shields.io/badge/%E2%AC%87%20JSON%20zip-311KB-brightgreen)](https://github.com/anthonyhann/chinese-history/releases/latest)
[![实体记录](https://img.shields.io/badge/entities-1224-red.svg)](#-数据集)
[![CI 校验](https://github.com/anthonyhann/chinese-history/actions/workflows/validate.yml/badge.svg)](https://github.com/anthonyhann/chinese-history/actions/workflows/validate.yml)

[![代码许可: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![事实数据: CC0](https://img.shields.io/badge/facts-CC0-green.svg)](LICENSE-DATA)
[![描述文本: CC BY-SA 4.0](https://img.shields.io/badge/text-CC%20BY--SA%204.0-orange.svg)](LICENSE-DATA)

[🚀 快速开始](#-快速开始) · [📦 数据集](#-数据集) · [📐 Schema](schema/) · [🤝 贡献](CONTRIBUTING.md) · [English](README.en.md) · [llms.txt](llms.txt)

</div>

---

> 灵感来自 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry)：古诗词有了最全的开源数据库，历史也该有一个。
>
> 但历史比诗词难做得多——生卒年在争、纪年要换算、出处要考证。所以本项目把**「出处」做成一等公民**：没有 `sources` 的记录过不了 CI，学术争议不投票而是多值并存，每条 AI 生成的数据都留了模型和 prompt 版本。
>
> **一句话定位**：给开发者和 AI Agent 用的一份干净的中华历史结构化数据，clone 即用，不用爬百科、不用担心版权。

**不想 clone？** 直接下载单文件数据库 → [最新 Release](https://github.com/anthonyhann/chinese-history/releases/latest)（SQLite 1.8MB 全库 / JSON zip）

**想先看设计思路？** 三条铁律为什么这么定、各自付出了什么代价 → [《给中华历史数据建 Schema 时，我踩的三个坑和付出的代价》](https://juejin.cn/post/7700407749293768739)

---

**如果这个项目对你有用，点个 ⭐ Star 是最实际的帮助。** 它不会让数据变得更准，但决定了这个库能不能被更多需要它的人看见——也是我能不能找到 co-maintainer 的前提。

当前需要帮忙的具体位置：[`disputed[]` 争议多值目前只覆盖 9/370 人](https://github.com/anthonyhann/chinese-history/issues/4)，以及[还没有任何一条数据经过人工核验](https://github.com/anthonyhann/chinese-history/issues/5)。你熟悉哪段历史，就带着书目来提 PR，一条一个 PR，出处要能核。长期共建见 [#6 招募 co-maintainer](https://github.com/anthonyhann/chinese-history/issues/6)。

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
python3 tools/validate.py                                     # ② 验证数据完整性（1224 条）
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
| [人物 · 魏晋南北朝](persons/) | 86 | ✅ v0.2.0（魏/蜀/吴/两晋/十六国/南北朝） |
| [人物 · 隋唐五代](persons/) | 39 | ✅ v0.3.0（隋 4/唐 21 含武则天/五代 14） |
| [人物 · 宋辽金](persons/) | 37 | ✅ v0.4.0（北宋 9/南宋 9/辽 9/金 10） |
| [人物 · 元明清](persons/) | 43 | ✅ v1.0.0（帝系贯通至 1912） |
| [人物 · 十国/西夏/大理](persons/) | 34 | ✅ v1.1.0（帝系拼图补齐） |
| [人物 · 名臣将相](persons/) | 82 | ✅ 两批（商鞅/白起/诸葛亮/魏征/李白/王安石/苏轼/岳飞/于谦/王阳明/曾国藩/林则徐等） |
| [事件 · 秦](events/qin/) | 20 | ✅ M1 种子 |
| [事件 · 汉](events/han/) | 19 | ✅ M2 新增 |
| [事件 · 魏晋南北朝](events/) | 12 | ✅ v0.2.0（官渡/赤壁/淝水/侯景等） |
| [事件 · 隋唐](events/) | 15 | ✅ v0.3.0（大运河/玄武门/贞观/安史之乱等） |
| [事件 · 宋辽金](events/) | 12 | ✅ v0.4.0（陈桥兵变/澶渊之盟/靖康之变/崖山等） |
| [事件 · 元明清](events/) | 15 | ✅ v1.0.0（蒙古西征/郑和下西洋/鸦片战争/辛亥革命） |
| [事件 · 各朝加密](events/) | 61 | ✅ v1.2.0（参合陂/高平/白江口/胡蓝之狱/萨尔浒/洋务运动等） |
| [文物 · 秦陵博物院](artifacts/qin/) | 1 | 🔬 Schema 样例 |
| [文物 · 大都会博物馆](artifacts/met/) | 24 | ✅ v1.1.0（CC0 图片直连） |
| [文物 · 史密森尼亚洲艺术馆](artifacts/smithsonian/) | 15 | ✅ v1.2.0（商周青铜/玉器/唐俑，CC0） |
| [文物 · 大英博物馆](artifacts/british-museum/) | 3 | ✅ v1.3.0（NC 许可仅链接） |
| [文物 · 克利夫兰](artifacts/cleveland/) | 19 | ✅ v1.4.0（商方卣/汉博山炉/北魏苦行僧/唐乐伎俑等，CC0） |
| [朝代/政权](dynasties/) | 49 | ✅ 基础表 |
| [年号纪年](reign_eras/) | 551 | ✅ 秦汉至明清 + 十国西夏（建元 → 宣统） |
| [地名](places/) | 31 | ✅ 含今地名与坐标 |
| [博物馆](museums/) | 6 | ✅ 含各馆开放数据许可状态 |

## 📐 三个设计决策（与诗词库的关键差异）

1. **id 锚点第一天就有**：`person.qin.yingzheng` 可读 slug + UUID 双标识，人物/事件/文物/地名互相引用，发布即冻结，永不复用
2. **时间双轨制**：史料原文纪年（"秦始皇三十七年七月丙寅"）+ 归一化公历（`-210`）+ `circa` 约数 + `disputed[]` 学术争议多值并存——争议不投票，各标出处
3. **出处强制 + 生产可复现**：`sources` 为空直接过不了 CI；每条数据的生成模型与 prompt 版本记录在 `_meta`，可追溯、可重跑

## ⚠️ 什么时候别用它（诚实边界）

- **做学术研究/论文** → 请用 [CBDB](https://cbdb.fas.harvard.edu/) 等专业学术库。本库定位是开发者友好与中文优先，不是学术深度
- **需要经人工核验的可靠性** → 当前全部记录由 AI 流水线生成并做过部分抽查，**没有任何一条经过逐条人工核验**。`_meta` 记录的是生成模型与 prompt 版本（用于追溯），不是正确性保证。请以 `sources` 自行核对，纠错请提 PR
- **需要完整二十四史全文** → 我们只存结构化事实，不存史料全文

## 🗺️ 路线图

- ✅ **M0 基建**：Schema / CI 校验器 / 朝代·年号·地名·博物馆基础表
- ✅ **M1 秦朝冷启动**：3 帝 + 15 关联人物 + 20 事件
- ✅ **M2 汉代放量**：两汉 31 帝系 + 74 年号 + 19 个重大事件
- ✅ **M2.5 魏晋南北朝**：86 帝王 + 182 年号 + 12 重大事件
- ✅ **M2.6 隋唐五代**：39 帝王 + 95 年号 + 15 重大事件
- ✅ **M2.7 宋辽金**：37 帝王 + 100 年号 + 12 重大事件
- ✅ **v1.0.0 元明清**：43 帝王 + 46 年号 + 15 重大事件——帝系全程贯通（前221年–1912年）
- ✅ **v1.1.0 补全**：十国/西夏/大理 34 帝 + 名臣将相 41 人 + Met CC0 文物 24 件
- ✅ **v1.2.0 加密**：名臣第二批 41 人 + 事件加密 61 个 + Smithsonian CC0 文物 15 件
- ✅ **v1.3.0 对齐**：348/370 人物挂上 Wikidata QID + 大英博物馆文物 3 件
- ✅ **v1.4.0 馆藏通道**：克利夫兰 CC0 文物 19 件（当前）
- 🔜 **M3 文物**：Met / Smithsonian 等 CC0 开放馆藏中华文物清洗导入
- 🔜 **M3+**：SQLite 构建器已可用（`python3 tools/build_sqlite.py`），release 自动化见 `.github/workflows/release.yml`
- 🔜 **M4**：历代皇帝全量、案例展示

## 💬 参与进来

**最快的参与方式**：点 ⭐ Star。Star 数决定这个库能不能被更多需要它的人搜到，也是招募 co-maintainer 的前提。

**能直接贡献的**（都比想象中好上手）：

| 想做的事 | 怎么做 |
|---|---|
| 补一条有学术争议的生卒年 | 往 `disputed[]` 加一个带书目的值，一条一个 PR → [#4](https://github.com/anthonyhann/chinese-history/issues/4) |
| 核验一条现有数据 | 对着 `sources` 读原书，确认无误后告诉我们，这是当前最缺的 → [#5](https://github.com/anthonyhann/chinese-history/issues/5) |
| 补你家乡博物馆的中华文物 | 按 `artifacts/` 现有 Schema 添加，注意图片许可逐条标注 |
| 长期共建 | 数据校订 / 前端可视化 / 贡献流程，任一方向都欢迎 → [#6](https://github.com/anthonyhann/chinese-history/issues/6) |
| 用了这个数据做了东西 | 开 issue 附链接，收录进案例展示 |

数据纠错 PR 请**注明出处**，无出处不合并，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📝 更新日志

- **2026-10-25** v1.4.0：克利夫兰 CC0 文物 19 件，实体总数 1224
- **2026-10-25** v1.3.0：Wikidata 对齐 94% + 大英博物馆文物 3 件，实体总数 1204
- **2026-10-24** v1.2.0：名臣第二批 41 + 事件加密 61 + Smithsonian 文物 15，实体总数 1201
- **2026-10-24** v1.1.0：十国/西夏/大理 34 帝 + 名臣将相 41 人 + Met 文物 24 件，实体总数 1084
- **2026-10-24** v1.0.0：元明清放量，实体总数 922，帝系全程贯通至 1912 年
- **2026-10-23** v0.4.0：宋辽金放量——37 位帝王、100 个年号、12 个重大事件，实体总数 815
- **2026-10-23** v0.3.0：隋唐五代放量——39 位帝王、95 个年号、15 个重大事件，实体总数 660
- **2026-10-23** v0.2.0：魏晋南北朝放量——86 位帝王、182 个年号、12 个重大事件，实体总数 503
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
