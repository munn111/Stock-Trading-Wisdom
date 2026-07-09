---
name: daily-panqian-report
description: "生成每日盘前报告（A股/港股/美股盘前综合解读）。自动搜索微信公众号近24小时「盘前」类文章，过滤出标题/摘要/发布时间/公众号，并综合成结构化「今日盘前解读」（含昨日复盘验证/自我纠偏维度 + 外盘、最强主线、A股局面、关注方向与风险）。触发词：盘前报告、每日盘前、盘前分析、盘前解读、pre-market digest、早盘前瞻。注意：本技能依赖 wechat-article-search 技能的 search_wechat.js 脚本，复盘验证依赖 tdx-connector（通达信）拉真实涨跌。"
version: 1.0.0
allowed-tools: Bash,Read,Write,Edit,Glob
metadata:
  clawdbot:
    emoji: "\U0001F4CA"
    requires:
      bins:
        - node
        - npm.cmd
display_name: "每日盘前报告"
display_name_en: "Daily Pre-Market Report"
---

# 每日盘前报告（方法论 + 执行流程）

把"搜公众号盘前文章 → 过滤 → 综合解读 → 出报告"沉淀为可复用流程。
核心产物：一份 HTML 解读报告 + 一份 JSON 结构化数据。

## 何时用
- 用户要"每日盘前报告 / 盘前分析 / 早盘前瞻"，或定时任务（如每天 9:00）触发。
- 也适用于任何"按关键词搜公众号文章并做综述"的需求（改关键词即可）。

## 依赖
- `wechat-article-search` 技能的脚本：`scripts/search_wechat.js`（位于 `~/.workbuddy/skills/` 下，可用 Glob 查找 `**/search_wechat.js`）。
- `cheerio`（受管环境必须用 `npm.cmd` 装到 `~/.workbuddy/binaries/node/workspace`，见 wechat-article-search 技能的步骤1）。

## 执行步骤

### 1. 搜索（受管运行时）
```bash
NODE_PATH=C:\Users\Administrator\.workbuddy\binaries\node\workspace/node_modules \
  C:\Users\Administrator\.workbuddy\binaries\node\versions\22.22.2\node.exe \
  <search_wechat.js 路径> "盘前" -n 30 -o panqian_raw.json
```
- 若脚本路径不确定：`Glob` 在 `~/.workbuddy/skills` 找 `**/search_wechat.js`。
- 结果为搜狗微信中转链接（已可点击跳转原文），真实 URL 反爬强，一般无需 `-r`。

### 2. 过滤（最近 24 小时）
读 `panqian_raw.json`，按 `datetime` 字段过滤 `>= 当前时间 - 24h`，提取：
`标题 / 摘要 / 发布时间 / 公众号(source)`。排序按时间倒序。
> 若当天命中不足，可放宽到最近 7 天（cutoff = now - 7d）以保底。

### 3. 综合「今日盘前解读」
从过滤后的文章里提炼 5 个维度（用 Python/Node 或直接写 HTML 均可）：
0. **昨日复盘验证（自我纠偏）**：拿昨天的盘前解读里"关注方向 & 风险"做对标——昨天看好的方向（如半导体/券商/养殖）今天实际怎么走？昨天提示的风险（如高开低走、外围扰动）是否应验？用 `tdx-connector`（通达信）拉相关板块/个股真实涨跌来校验，在报告中标注"昨日预判 ✅/❌"，并据此调整今天判断的置信度。若没有昨天的报告或行情数据，跳过本维度并在报告中注明。
1. **外盘**：美股（道指/纳指/半导体指数如费城半导体）、亚太（日韩港股）分化情况。涨用红、跌用绿（中国配色）。
2. **最强主线**：被多篇反复提及的共识方向（例：AI/半导体、高盛资本开支预期、政策受益板块）。
3. **A股当日局面**：当日特殊背景（如新规首日）、资金聚焦点、整体定性（如"弱平衡"）。
4. **关注方向 & 潜在风险**：看修复/看政策/看延续的具体板块 + 外围扰动项。

### 4. 出报告
- **HTML**：标题 + 一句话定调 + 卡片/表格（昨日复盘验证、外盘、主线、A股、风险），文末加「非投资建议」声明。
- **JSON**：`{keyword, filter, count, articles:[{title,summary,publish_time,account}]}`。
- 保存到当前工作区，并给一段简短文字总结。

## 方法论要点（沉淀）
- **数据源**：搜狗微信搜索是公众号文章最易拿到的入口；结果按时间倒序，盘前类文章天然集中在发布当日早间。
- **过滤口径**：daily 报告用 24h；复盘/周报可用 7d。cutoff 用本地时区（中国 GMT+8）。
- **综合而非罗列**：解读价值在于"提炼共识主线 + 提示风险"，不是把标题堆砌。
- **自我纠偏**：每日用 `tdx-connector` 校验昨日预判（✅/❌），让判断可累积进化，而非重复喊单；复盘命中率本身也是该技能最有价值的长期产物。
- **配色约定**：中国股市红涨绿跌（region 约定）。
- **合规**：文末必须附"非投资建议"声明；仅学习研究用途，勿商业爬取。

## 常见问题
- 搜索为空：换关键词（如"早盘""盘前策略"）、减少特殊字符、或稍后重试。
- cheerio 报错 `Cannot find module`：受管环境漏设 `NODE_PATH` 或未用 `npm.cmd` 安装 → 按步骤1重来。
- 文章时间缺失：脚本已尽量解析时间戳，缺失的按 `date_description` 兜底，过滤时跳过无法解析的。
