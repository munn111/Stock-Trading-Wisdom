# Stock Trading Wisdom (股票交易智慧库) v3.0

> **最后更新**: 2026-07-29 | **版本**: v3.0 (2026年7月实战演进版)
> **定位**: AI驱动的A股交易方法论与实战技能库 — WorkBuddy 股票分析核心技能

---

## 核心理念

> 市场是情绪的集合，技术是情绪的载体。不预测，只跟随；不博弈，只确认。
> **先看情绪周期定仓位 → 选最高辨识度龙头 → 按形态找买点 → 按纪律设止损。**
> **冰点试错、高潮打板、退潮离场，活下来比抓涨停更重要。**

---

## v3.0 升级要点 (2026-07-29)

本版本沉淀了2026年7月整整一个月的实盘分析经验，主要升级：

| 升级项 | 内容 |
|---|---|
| **报告输出铁律** | 三件套强制：MD(单一真相源) + HTML(深色科技风) + PPT(16:9深空蓝底) |
| **数据源定型** | westock-data(skill)行情/选股/K线 + tdx-connector(MCP)深度行情 + qcc-company(MCP)基本面 |
| **新战法** | 卡脖子理论六步选股、云赛同款形态(首板→洗盘→二板)、获利比例选股、六维选股体系 |
| **实战坑集** | westock-data API陷阱、python-pptx踩坑、tdx-connector参数细节 |
| **情绪周期校准** | 基于7月极端行情(单日V反/创业板-7.35%/5195家上涨→次日翻脸)重新校准 |

---

## 系统架构 (6-Layer Architecture)

| 层级 | 模块 | 功能描述 |
|:---|:---|:---|
| **L1: Data Source** | `data_engine/` | westock-data(skill) + tdx-connector(MCP) + 东方财富/同花顺/企查查 |
| **L2: Data Clean** | `data_engine/cleaner.py` | 清洗原始数据，统一字段格式 (open, close, volume) |
| **L3: Factor** | `utils/factors.py` | 计算技术指标 (MA, MACD, 涨停标记, 缺口检测) |
| **L4: Signal** | `strategies/` | **核心战法引擎**：涨停回马枪、缺口理论、龙头战法 |
| **L5: Portfolio** | `portfolio/` | 仓位管理，风险控制 (待实���) |
| **L6: Execution** | `main.py` | 信号输出，交易建议生成 (待实现) |

---

## 数据源约定 (v3.0定型)

| 数据类型 | 首选工具 | 备选 |
|---|---|---|
| 行情/指数/K线 | **westock-data** skill (builtin) | tdx-connector MCP |
| 涨停/连板筛选 | **tdx-connector** `tdx_screener` | westock-data |
| 板块排行/资金流向 | **westock-data** `sector ranking` | tdx-connector |
| 公司基本面/财务 | **qcc-company** MCP | 东方财富F10 |
| 新闻/公告/研报 | **tdx-connector** `wenda_news_query` | 微信公众号搜索 |
| 热搜/人气 | **westock-data** `hot stock/board` | - |

### 关键API陷阱速查
- westock-data `quote`：代码须加 sh/sz 前缀，返回结构嵌套在 `data[].data` 下
- westock-data `sector ranking`：`mainNetInflow` 是**字符串**，须 `float()` 转换
- tdx-connector `tdx_quotes`：只接受单只 `code`+`setcode`，**不支持数组批量**
- tdx-connector setcode规则：上证/科创=1, 深证/创业=0, 北证=2

---

## 核心内容

### 1. 交易战法 (`methods/`)

| 文件 | 内容 | 状态 |
|---|---|---|
| `01_limit_up_strategy.md` | 涨停板战法：回马枪/连板接力/首板挖掘 | ✅ |
| `02_gap_theory.md` | 缺口理论：突破/中继/衰竭/岛形反转 | ✅ |
| `03_leader_strategy.md` | 龙头战法：生命周期/情绪周期/操作纪律 | ✅ |
| `04_leader_playbook_2026W29.md` | ⭐ 龙头战法总纲(7月实盘沉淀)：情绪四阶段+龙头五要素+四大打板形态+冰点特训 | ✅ NEW |
| `05_kanbazi_theory.md` | ⭐ 卡脖子理论六步选股：识别瓶颈→替代紧迫度→国产化率→龙头壁垒→订单兑现→估值动量 | ✅ NEW |
| `06_six_dim_picking.md` | ⭐ 六维选股体系：政策/景气/ROE/PEG/技术面/安全边际 + 3331仓位法则 | ✅ NEW |
| `07_yunsai_pattern.md` | ⭐ 云赛同款形态：首板→中继洗盘→缩量二板接力，带筛选条件和K线复核流程 | ✅ NEW |

### 2. 策略引擎 (`strategies/`)
- `LimitUpStrategy`: 涨停回马枪自动扫描
- `GapStrategy`: 缺口检测与回补判断
- `LeaderStrategy`: 板块龙头识别

### 3. 数据引擎 (`data_engine/`)
- 多源自动切换，确保数据永不中断
- 智能交易日判断 (周末/节假日自动回退)

---

## 报告输出规范 (v3.0 三件套铁律)

**所有分析/选股/研报/总结类输出，必须同时产出三件套：**

| 产物 | 格式 | 定位 | 技术要求 |
|---|---|---|---|
| **MD文件** | Markdown | 单一真相源，结构化文本 | 标题层级 + 表格 + 数据 + 结论 |
| **HTML文件** | 单文件HTML | 深色科技风，浏览器预览 | 深空蓝底 #070b16，涨红 #ff5a5f，跌绿 #1ed760 |
| **PPT文件** | .pptx (16:9) | 演示版，同款主题 | python-pptx 生成，托管 venv |

**配色标准**：深空蓝底 `#070b16` | 涨红 `#ff5a5f` | 跌绿 `#1ed760` | 文字 `#e0e6f0` | 强调 `#00d4ff`
**生成环境**：`C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\python.exe`

### PPT 生成要点
- 表格列宽**必须是整数 EMU**，用 `Inches(x)` 而非浮点相乘
- 中文引号在 Python f-string 中可���导致语法错误，用 Unicode 转义
- 多行文本辅助函数接受 3/4 元组 (text, size, color, bold=默认False)

---

## 每日工作流 SOP

### 盘前 (盘前报告)
1. 搜索微信公众号盘前文章 (wechat-article-search skill)
2. 外盘扫描 (美股/日韩/港股)
3. 昨日复盘验证 (用tdx-connector 检查昨日预判命中率)
4. 今日关注方向 + 风险提示

### 午盘 (午盘总结)
1. 五大指数行情 (westock-data quote 或 tdx-connector)
2. 板块涨跌榜 (sector ranking)
3. 涨跌分布 (changedist)
4. 涨停/连板梯队 (tdx_screener)
5. 资金流向 + 风格轮动
6. 关键事件复盘

### 收盘后 (涨停复盘)
1. 涨停全表 + 主线分类 + 事件催化
2. 连板梯队 + 龙虎榜 (盘后)
3. 封单TOP榜 + 20cm弹性
4. 与昨日预判对照验证

### 周�� (方法论升级)
1. 本周模式沉淀到对应 methods/ 文件
2. 有效案例加入 examples/
3. 脚本自动化部分更新

---

## 实战踩坑集 (`docs/09_数据工具实战踩坑集.md`)

记录了7月全月使用 `westock-data` 和 `tdx-connector` 过程中踩过的所有坑：
- westock-data `quote` 对五大指数午盘窗口可能全部报错 [SKILL_004]
- `sector ranking` 只给涨榜，跌榜需手动 quote SW1 代码
- `wenda_news_query` 参数名是 `query` 不是 `message`
- 码前缀规则：sh(沪市) / sz(深市) / bj(北交所)
- [详见完整踩坑文档](docs/09_数据工具实战踩坑集.md)

---

## 工具链

- **Python**: `C:\Users\Administrator\.workbuddy\binaries\python\envs\default\` (托管 venv, python-pptx已装)
- **Node**: `C:\Users\Administrator\.workbuddy\binaries\node\versions\22.22.2\node.exe`
- **westock-data入口**: `node scripts/index.js` (builtin skill路径)
- **MCP**: tdx-connector (通达信) / qcc-company (企查查) / github

---

## 经典案例
- [五洲新春 2026年5月走势推演](examples/case_wuzhou.md)
- [龙头战法实盘特训 W29 (7.13-7.15)](methods/04_leader_playbook_2026W29.md)
- [云赛智联 5天二板 K线形态拆解](examples/case_yunsai.md)
- [六维选股10只精选 2026-07-16](methods/06_six_dim_picking.md)

---

## 安全提示
本项目仅供学习交流，不构成投资建议。股市有风险，入市需谨慎。
所有报告文末须附「非投资建议」声明。

---

> **一句话心法**：事件只是入口，产业链决定范围，梯队决定强弱，K线位置决定能不能下手，风控决定能不能活到下一次机会。
