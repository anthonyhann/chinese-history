# persons/han 汉朝人物

## 收录范围声明

- **皇帝**：西汉 12 帝（高帝、惠帝、前少帝、后少帝、文帝、景帝、武帝、昭帝、废帝刘贺、宣帝、元帝、成帝、哀帝、平帝——含两位少帝与废帝）+ 东汉 14 帝（光武、明、章、和、殇、安、顺、冲、质、桓、灵、少帝刘辩、献帝）。
- **君主（正统性存疑/未即位者）**：孺子婴（王莽居摄，未即位）、更始帝刘玄（玄汉）、建世帝刘盆子（赤眉所立）、北乡侯刘懿（阎氏所立，正史多不视为正统）。以 `category: ["monarch"]` 收录。
- **不包含**：新朝王莽（规划于独立 `dynasty.xin` 阶段）、蜀汉/汉赵等后世政权。

## 数据文件

`person.han.0.json` —— 31 条（含从 `persons/qin` 迁移的刘邦：id 由 `person.qin.liubang` 更名为 `person.han.liubang`，UUID 不变）。

## 已知命名冲突处理

- 后少帝**刘弘**（西汉）→ `person.han.liuhong`；灵帝**刘宏**（东汉）→ `person.han.liuhong-lingdi`
- 惠帝**刘盈** → `person.han.liuying`；**孺子婴**刘婴 → `person.han.ruzi-ying`

## 质量状态

AI 生成 + 待人工核验（`_meta.created_by: ai-pipeline`）。主要出处为《史记》《汉书》《后汉书》诸帝纪。生卒年个别存疑处已标注 `circa` 或 `disputed`。
