"""
A 股机会扫描器 (A-Share Opportunity Scanner)
统一入口：一键运行所有策略，输出机会列表
"""
from strategies.limit_up_pullback import LimitUpPullback
from data_engine.loader import StockDataEngine

def run_daily_scan():
    print("="*50)
    print("🚀 A 股每日机会扫描器 (Daily Scanner)")
    print("="*50)
    
    # 1. 初始化数据引擎
    engine = StockDataEngine()
    
    # 2. 获取全市场股票列表 (简化：仅用示例池)
    # real_pool = engine.fetch_all_stocks(engine.get_trade_date())
    demo_pool = ["sh.603667", "sh.688017", "sz.300161", "sz.002896", "sh.600031"]
    print(f"📦 加载股票池：{len(demo_pool)} 只 (演示模式)")
    
    # 3. 运行策略
    print("\n--- 策略 1: 涨停回马枪 ---")
    strategy1 = LimitUpPullback()
    opps1 = strategy1.scan(demo_pool)
    
    print("\n--- 策略 2: 缺口理论 (开发中) ---")
    # strategy2 = GapStrategy()
    # opps2 = strategy2.scan(demo_pool)
    
    print("\n" + "="*50)
    print("✅ 扫描结束！")
    print("="*50)

if __name__ == "__main__":
    run_daily_scan()
