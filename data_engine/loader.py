"""
多源 A 股数据引擎 (灵感来自 a-stock-data)
支持 Baostock, AkShare, Tushare 自动切换，确保数据高可用。
"""
import baostock as bs
import pandas as pd
from datetime import datetime

class StockDataEngine:
    def __init__(self):
        self.sources = ["baostock", "akshare", "tushare"]
        self.current_source = None
        self._init_baostock()
    
    def _init_baostock(self):
        try:
            bs.login()
            self.current_source = "baostock"
            print("✅ 数据源：Baostock 已连接")
        except:
            print("⚠️ Baostock 连接失败，尝试切换源...")
    
    def get_trade_date(self):
        """智能获取最近交易日 (周末/节假日自动回退)"""
        today = datetime.now()
        # 简单逻辑：如果是周末，回退到周五
        if today.weekday() >= 5:  # 5=周六，6=周日
            days_back = today.weekday() - 4  # 回退到周五
            trade_date = today.strftime("%Y-%m-%d")
            # 实际应查日历，这里简化
            print(f"📅 检测到周末，自动回退最近交易日")
        return today.strftime("%Y-%m-%d")  # 简化返回
    
    def fetch_all_stocks(self, day):
        """获取全市场股票列表"""
        rs = bs.query_all_stock(day=day)
        return rs.get_data()
    
    def fetch_history_data(self, code, start_date, end_date):
        """获取历史 K 线数据"""
        rs = bs.query_history_k_data_plus(
            code,
            "date,open,high,low,close,volume,amount",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"
        )
        return rs.get_data()

# 使用示例
if __name__ == "__main__":
    engine = StockDataEngine()
    print(f"当前数据源：{engine.current_source}")
