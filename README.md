# 📈 Stock Trading Wisdom (股票交易智慧库) v2.0


### 📅 2026-05-19 更新
- 📊 **每日策略**: [daily/2026-05-19.md](daily/2026-05-19.md)
- 🤖 **重点方向**: AI 应用 (影视/短剧)、人形机器人、618 消费
- 🚀 **核心个股**: 五洲新春 (龙头)、风语筑 (晋级)、珀莱雅 (趋势)
- 🔗 **网页预览**: [GitHub Pages](https://munn111.github.io/Stock-Trading-Wisdom/)


> **核心理念**：市场是情绪的集合，技术是情绪的载体。不预测，只跟随；不博弈，只确认。
> **架构灵感**：深度参考 [a-stock-data](https://github.com/simonlin1212/a-stock-data) 的 6 层数据架构，实现从"文档"到"可执行系统"的升级。

---

## 🏗️ 系统架构 (6-Layer Architecture)

借鉴专业量化系统，本项目分为以下 6 层：

| 层级 | 模块 | 功能描述 |
|:---|:---|:---|
| **L1: Data Source** | `data_engine/` | 整合 Baostock, AkShare, Tushare 等 8 大源，自动容错切换 |
| **L2: Data Clean** | `data_engine/cleaner.py` | 清洗原始数据，统一字段格式 (open, close, volume) |
| **L3: Factor** | `utils/factors.py` | 计算技术指标 (MA, MACD, 涨停标记, 缺口检测) |
| **L4: Signal** | `strategies/` | **核心战法引擎**：涨停回马枪、缺口理论、龙头战法 |
| **L5: Portfolio** | `portfolio/` | 仓位管理，风险控制 (待实现) |
| **L6: Execution** | `main.py` | 信号输出，交易建议生成 (待实现) |

---

## 📚 核心内容

### 1. 交易战法 (`methods/`)
- **涨停板战法**：回马枪、连板接力、首板挖掘
- **缺口理论**：突破缺口、中继缺口、衰竭缺口
- **龙头战法**：生命周期、情绪周期、操作纪律

### 2. 策略引擎 (`strategies/`)
- `LimitUpStrategy`: 涨停回马枪自动扫描
- `GapStrategy`: 缺口检测与回补判断
- `LeaderStrategy`: 板块龙头识别

### 3. 数据引擎 (`data_engine/`)
- 多源自动切换，确保数据永不中断
- 智能交易日判断 (周末/节假日自动回退)

---

## 🚀 快速开始

```python
from data_engine.loader import StockDataEngine
from strategies.core_strategies import run_strategy

# 1. 初始化数据引擎
engine = StockDataEngine()

# 2. 获取数据
data = engine.fetch_all_stocks("2026-05-15")

# 3. 运行策略
strategy = run_strategy("limit_up", data)
strategy.check_pattern("sh.603667")  # 五洲新春
```

## 📝 经典案例
- [五洲新春 2026 年 5 月走势推演](examples/case_wuzhou.md)

## 🔐 安全提示
本项目仅供学习交流，不构成投资建议。股市有风险，入市需谨慎。

- **📘 交易方法论**: [主线识别与错杀博弈 (2026-W21)](methodology_weekly_review.md)
