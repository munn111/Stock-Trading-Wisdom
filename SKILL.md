---
name: stock-trading-wisdom
description: "A股交易方���论与实战技能核心库 v3.0 — 涨停板战法、龙头战法、卡脖子选股、六维选股、云赛同款形态、情绪周期、每日工作流SOP、报告三件套规范、数据工具踩坑集。触发词：股票分析、A股、涨停、龙头战法、选股、复盘、情绪周期、卡脖子、打板、连板、龙虎榜。Do NOT trigger on: 美股分析、港股分析、加密货币、期货（这些应走其他专用skill）。"
version: 3.1.0
allowed-tools: Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Skill
metadata:
  clawdbot:
    emoji: "\U0001F4C8"
    requires:
      bins:
        - python
        - node
display_name: "股票交易智慧库"
display_name_en: "Stock Trading Wisdom"
agent_created: true
---

# Stock Trading Wisdom v3.0 — A股交易方法论与实战技能核心库

> 定位：WorkBuddy 股票分析核心技能，所有A股分析请求的默认入口

## 何时使用

当用户请求以下任务时，加载本技能：
- A股复盘 / 涨停分析 / 连板梯队
- 选股（龙头/六维/卡脖子/形态）
- 情绪周期判定
- 每日午盘/收盘报告
- 板块/事件驱动分析
- 报告生成（三件套：MD+HTML+PPT）

## 不适用场景

- 美股/港股分析 → 使用 stock-analysis 或 stock-analyzer skill
- 加密货币 → 使用 stock-analysis skill
- 纯公司基本面尽职调查 → 首先使用 qcc-company MCP

## 架构

本技能基于Stock-Trading-Wisdom v3.0，采用6层架构：

```
methods/    — 交易战法 (涨停板/缺口/龙头/卡脖子/六维/形态)
strategies/ — 策略引擎 (Python可执行)
data_engine/— 数据引擎
memory/     — 情绪周期记忆
skills/     — 分析SOP + 盘前报告流程
docs/       — 工作流/报告规范/踩坑集/方法论
examples/   — 案例库
```

## 核心方法论速查

### 情绪周期判定
- 冰点: 涨停<40/断板率>60%/涨跌比<0.2 → 试错新首板
- 复苏: 涨停40-70/封板率>70% → 加仓核心
- 高潮: 涨停>80/涨跌比>5:1 → ⚠️减仓，不追补涨
- 退潮: 高标A杀/主线破位 → 清仓空仓

### 龙头识别五要素
辨识度 | 题材高度 | 封单硬度 | 换手率 | 板块地位

### 四大打板形态
首板打板 | 低吸回封 | 连板接力 | 龙头首阴低吸

### 六维选股
政策赛道 | ROE≥15% | PEG≤1.2 | 技术共振 | 安全边际 | 资金面

### 报告三件套铁律
所有分析必须产出：MD(真相源) + HTML(深色科技风) + PPT(16:9深空蓝)

配色：背景#070b16 | 涨红#ff5a5f | 跌绿#1ed760 | 强调#00d4ff

## 数据源

| 数据 | 首选 | 备选 |
|---|---|---|
| 行情/K线 | westock-data skill | tdx-connector MCP |
| 涨停筛选 | tdx-connector tdx_screener | - |
| 板块排行 | westock-data sector ranking | - |
| 基本面 | qcc-company MCP | - |
| 新闻/研报 | tdx-connector wenda_news_query | - |

## 关键陷阱速查

1. westock-data quote: 代码须sh/sz前缀，返回嵌套在data[].data
2. sector ranking: mainNetInflow是字符串，需float()
3. tdx_quotes: 只接受单��code+setcode，不支持数组批量
4. python-pptx: 表格列宽必须整数EMU
5. 午盘窗口(11:30): quote可能报SKILL_004，改用tdx-connector

详见: docs/09_数据工具实战踩坑集.md

## 使用流程

```
1. 接收用户A股分析请求
2. 读取相关 methods/ 文件确定框架
3. 使用数据工具获取实时数据
4. 按 docs/08_报告输出三件套规范.md 产出报告
5. 产出三件套：MD + HTML + PPT
```

## 参考文件

- [README.md](README.md) — 完整项目说明
- [methods/04_leader_playbook_2026W29.md](methods/04_leader_playbook_2026W29.md) — 龙头战法总纲(最重要)
- [docs/08_报告输出三件套规范.md](docs/08_报告输出三件套规范.md) — 报告规范
- [docs/09_数据工具实战踩坑集.md](docs/09_数据工具实战踩坑集.md) — 踩坑速查
- [docs/10_每日工作流实战演进.md](docs/10_每日工作流实战演进.md) — 工作流
- [memory/emotion_cycle.md](memory/emotion_cycle.md) — 情绪周期
- [skills/analysis_sop.md](skills/analysis_sop.md) — 分析SOP（v3.1 连板天梯四维结构化）
- [skills/analysis_sop.md#21-连板天梯结构化v31-新增--核心升级](skills/analysis_sop.md#21-连板天梯结构化v31-新增--核心升级) — 连板天梯使用指南【v3.1 必读】

---

## v3.1 核心升级：连板天梯

涨停复盘从一维列表升级为**四维结构化**：
1. **全市场主线分布表** — 涨停数/占比/龙头，一眼看共识
2. **连板天梯时间戳表** — 每只连板股标注涨停时间到分钟
3. **涨停时间分级诊断** — 早盘秒板(强) → 尾盘封板(弱信号)
4. **连板板块归属树** — 涨停全量按主线分叉展示
5. **梯队健康度诊断** — 每条主线独立评估

基本判断法则：
- **尾盘封板率 >30% = 警惕次日高开低走**
- **09:30-09:45涨停的连板股，次日继续涨停概率 >> 14:00后涨停的**
- **主线涨停合计 >30% = 共识形成；<20% = 无主线混乱期**

---

⚠️ 所有内容仅供学习交流，不构成投资建议。股市有风险，入市需谨慎。
