# 社交平台短文（即刻/微博/小红书/X 中文）

## 即刻 / 微博（短）

我把中华五千年做成了开源数据库 🔥

266 位帝王从秦始皇到溥仪全收录，154 个重大事件全带《史记》卷次出处，551 个年号表，62 件流落海外的中华珍宝（女史箴图、大维德瓶、唐三彩女骑俑，大都会/史密森尼图片可直接用）。

JSON + SQLite，clone 即用：https://github.com/anthonyhann/chinese-history

对标 chinese-poetry（53.8k⭐），历史版来了。

#开源 #历史 #数据库

## 小红书（长一点）

标题：姐妹们！流落海外博物馆的中华珍宝，我做成了免费数据库 😭

正文：
大英博物馆的女史箴图、纽约大都会的唐宫侍女俑、华盛顿亚洲艺术馆的商代青铜觥、克利夫兰的汉博山炉……

这些我们再也见不到的国宝，我把它们的资料全部整理成了开源数据库：名字、年代、尺寸、馆藏地、流传经历，全部带出处。能合法用的图片（CC0）直接给链接，连大英博物馆禁止商用、只能放链接这种细节都标好了。

还有 266 位皇帝从秦始皇到溥仪的完整档案、154 个历史大事件、551 个年号换算表。全部免费开源。

GitHub 搜 chinese-history 就能找到。欢迎捉虫补充 🙏

#文物 #博物馆 #历史 #开源 #国宝

## X/Twitter 中文 thread

1/ 中华历史开源数据库 chinese-history 发布 v1.4.0 📜
370 人物（266 帝）· 154 事件 · 551 年号 · 62 文物
帝系前221→1912 全程贯通
94% 人物已对齐 Wikidata
JSON/SQLite，clone 即用
https://github.com/anthonyhann/chinese-history

2/ 和 53k⭐ 的 chinese-poetry 不同，历史数据有学术争议。所以我们把「出处」做成了一等公民：
- 无出处 → CI 拒收
- 争议 → disputed[] 多值并存
- AI 生成 → _meta 记录模型与 prompt，可复现
- 文物图片 → 按馆方许可逐条标注

3/ 流落海外的中华珍宝，62 件已入库：
女史箴图（大英）、大维德至正青花瓶、唐彩绘骑马女俑（大都会）、商青铜方卣（克利夫兰）、玉琮（史密森尼）……
能用的 CC0 图直接给，禁商用只放链接。

4/ 上手只要三条命令：
git clone → python3 tools/validate.py → python3 tools/build_sqlite.py
打 tag 自动出 Release（SQLite + JSON），数据与产物同源。

5/ 欢迎捉虫、补充、共建。PR 唯一硬性要求：带出处。
Star 一个再走 → https://github.com/anthonyhann/chinese-history ⭐
