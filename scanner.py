"""
每日机会扫描器 (v3.2 修复版)
适配：股票代码格式自动转换
"""
from data_engine.loader import FreeDataLoader
import pandas as pd

def run_daily_scan():
    loader = FreeDataLoader()
    
    print("="*60)
    print("🔍 开始每日机会扫描 (免费版 v3.2)")
    print("="*60)
    
    # 1. 获取涨停池
    print("\n--- 1. 获取昨日涨停池 ---")
    limit_up_df = loader.get_daily_limit_up()
    print(f"✅ 昨日涨停 {len(limit_up_df)} 只")
    
    # 2. 扫描回马枪
    print("\n--- 2. 策略扫描 ---")
    opportunities = []
    for _, row in limit_up_df.head(10).iterrows(): # 演示前 10 只
        code = row['代码']
        name = row['名称']
        print(f"📈 获取 {code} K 线...")
        
        df = loader.get_kline(code)
        if df is not None and len(df) > 5:
            # 简单逻辑：收盘价 > 5 日线
            close = df['close'].iloc[-1]
            ma5 = df['close'].rolling(5).mean().iloc[-1]
            if close >= ma5:
                opportunities.append({"代码": code, "名称": name, "信号": "站稳 5 日线"})
    
    # 3. 输出
    print("\n--- 3. 扫描结果 ---")
    if opportunities:
        print(f"🎯 发现 {len(opportunities)} 只机会:")
        print(pd.DataFrame(opportunities).to_string(index=False))
    else:
        print("   暂无符合策略的机会。")
    
    print("\n✅ 扫描完成！")

if __name__ == "__main__":
    run_daily_scan()
