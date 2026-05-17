"""
🔍 涨停回马枪监控脚本：回踩5日线 + 缩倍量
功能：实时监控指定股票池，发现符合"回踩5日线 + 缩倍量"或"突破拉升"信号时报警。
运行：python scanner_ma5_monitor.py
"""

import akshare as ak
import pandas as pd
import time
from datetime import datetime

# === 配置区 ===
STOCK_POOL = [
    '002918', '001259', '002407', '688549', 
    '603078', '603082', '002156', '300605'
]
CHECK_INTERVAL = 30  # 检查间隔 (秒)
VOL_RATIO_THRESHOLD = 0.55  # 缩量阈值 (小于昨日量的 55%)
MA5_TOLERANCE = 0.02  # 5 日线容忍度 (±2%)

def get_realtime_data(code):
    """获取实时行情和 K 线"""
    try:
        # 获取实时行情
        df_rt = ak.stock_zh_a_spot_em()
        rt_row = df_rt[df_rt['代码'] == code]
        if rt_row.empty:
            return None
        current_price = rt_row['最新价'].values[0]
        vol_now = rt_row['成交量'].values[0]
        
        # 获取 K 线 (日线)
        df_k = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20260501")
        if len(df_k) < 5:
            return None
            
        # 计算 5 日线
        ma5 = df_k['收盘'].iloc[-5:].mean()
        
        # 昨日成交量
        vol_yesterday = df_k['成交量'].iloc[-2]
        
        return {
            'price': current_price,
            'ma5': ma5,
            'vol_now': vol_now,
            'vol_yesterday': vol_yesterday,
            'vol_ratio': vol_now / vol_yesterday if vol_yesterday > 0 else 1
        }
    except Exception as e:
        return None

def check_signal(code, data):
    """检查是否触发信号"""
    if not data:
        return None
        
    price = data['price']
    ma5 = data['ma5']
    vol_ratio = data['vol_ratio']
    
    # 信号 1: 回踩 5 日线 + 缩倍量
    near_ma5 = abs(price - ma5) / ma5 <= MA5_TOLERANCE
    shrink_vol = vol_ratio <= VOL_RATIO_THRESHOLD
    
    if near_ma5 and shrink_vol:
        return f"🟢【低吸信号】{code} 回踩 5 日线 ({price:.2f})，缩量 {int(vol_ratio*100)}%"
    
    # 信号 2: 突破拉升 (放量 > 昨日 150%)
    if vol_ratio > 1.5 and price > ma5 * 1.03:
        return f"🔴【突破信号】{code} 放量拉升 ({price:.2f})，量能 {int(vol_ratio*100)}%"
    
    return None

def main():
    print(f"🚀 启动监控：{len(STOCK_POOL)} 只股票，间隔 {CHECK_INTERVAL} 秒...")
    print(f"股票池：{', '.join(STOCK_POOL)}\n")
    
    alerted_stocks = set()  # 避免重复报警
    
    while True:
        now = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{now}] 扫描中...")
        
        for code in STOCK_POOL:
            if code in alerted_stocks:
                continue
                
            data = get_realtime_data(code)
            signal = check_signal(code, data)
            
            if signal:
                print(f"⚠️ {signal}")
                alerted_stocks.add(code)
                # 这里可以扩展：发送飞书消息/邮件/短信
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 监控已手动停止。")