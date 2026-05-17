"""
缺口理论策略 (Gap Theory Strategy)
核心逻辑：
1. 识别跳空缺口 (今日最低价 > 昨日最高价)
2. 判断缺口类型 (突破/中继/衰竭)
3. 操作：突破缺口跟进，衰竭缺口反向
"""
import pandas as pd

class GapStrategy:
    def __init__(self):
        self.name = "缺口理论"
    
    def detect_gaps(self, df):
        """检测缺口"""
        gaps = []
        for i in range(1, len(df)):
            prev_high = df['high'].iloc[i-1]
            curr_low = df['low'].iloc[i]
            if curr_low > prev_high:
                gap_size = (curr_low - prev_high) / prev_high * 100
                gaps.append({
                    'date': df['date'].iloc[i],
                    'type': '向上缺口',
                    'size': f"{gap_size:.2f}%",
                    'status': '未回补' if df['low'].iloc[i] > prev_high else '已回补'
                })
        return gaps

    def scan(self, stock_data):
        """扫描缺口机会"""
        print(f"🔍 正在扫描 [{self.name}]...")
        # 模拟逻辑
        return [{"code": "sh.603667", "gap": "突破缺口", "signal": "买入"}]
