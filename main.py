"""
A 股全能量化系统 (A-Share Quant System)
统一入口：扫描、回测、可视化
"""
from strategies.limit_up_pullback import LimitUpPullback
from strategies.gap_strategy import GapStrategy
from strategies.leader_strategy import LeaderStrategy
from backtester import SimpleBacktester
from utils.visualizer import plot_kline
import pandas as pd

def main():
    print("="*60)
    print("🚀 A 股全能量化系统 v3.0 (终极版)")
    print("="*60)
    
    # 1. 策略扫描
    print("\n--- 1. 每日机会扫描 ---")
    pool = ["sh.603667", "sh.688017", "sz.300161"]
    
    s1 = LimitUpPullback()
    opps1 = s1.scan(pool)
    
    s2 = GapStrategy()
    opps2 = s2.scan(None)
    
    s3 = LeaderStrategy()
    opps3 = s3.scan(None)
    
    # 2. 策略回测
    print("\n--- 2. 策略历史回测 ---")
    bt = SimpleBacktester()
    bt.run(s1, None)
    bt.run(s2, None)
    
    # 3. 可视化示例
    print("\n--- 3. 可视化示例 ---")
    # 模拟数据
    dates = pd.date_range(start="2026-05-01", periods=15)
    df = pd.DataFrame({
        "date": dates,
        "close": [10+i*0.5 for i in range(15)]
    })
    print("✅ 系统初始化完成！(可视化需本地运行)")
    
    print("\n" + "="*60)
    print("✅ 所有模块就绪！")
    print("="*60)

if __name__ == "__main__":
    main()
