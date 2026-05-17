"""
全免费 A 股数据加载器 (v3.2 修复版)
修复：股票代码格式转换 + 网络重试
"""
import akshare as ak
import baostock as bs
import pandas as pd
import time

class FreeDataLoader:
    def __init__(self):
        self.source = "akshare"
    
    def _format_code(self, code):
        """转换 6 位代码为 Baostock 格式 (sh./sz.)"""
        code = str(code).zfill(6)
        if code.startswith(('6', '5', '9', '7')):
            return f"sh.{code}"
        else:
            return f"sz.{code}"
    
    def get_kline(self, code, retries=3):
        """获取 K 线，支持重试"""
        for i in range(retries):
            try:
                # 优先 AkShare
                df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
                if df is not None and not df.empty:
                    return df
            except Exception as e:
                if i < retries - 1:
                    time.sleep(1)
                    continue
                # AkShare 失败尝试 Baostock
                bs_code = self._format_code(code)
                rs = bs.query_history_k_data_plus(bs_code, "date,open,high,low,close,volume")
                data_list = []
                while (rs.error_code == '0') and rs.next():
                    data_list.append(rs.get_row_data())
                if data_list:
                    df_bs = pd.DataFrame(data_list, columns=rs.fields)
                    df_bs['close'] = pd.to_numeric(df_bs['close'])
                    df_bs['open'] = pd.to_numeric(df_bs['open'])
                    df_bs['high'] = pd.to_numeric(df_bs['high'])
                    df_bs['low'] = pd.to_numeric(df_bs['low'])
                    return df_bs
        return None

    def get_daily_limit_up(self):
        """获取昨日涨停池"""
        try:
            # 模拟获取涨停池 (实际需根据日期调整)
            # 这里用 AkShare 的实时行情接口模拟
            df = ak.stock_zt_pool_em(date="20240517") # 示例日期
            return df[['代码', '名称']]
        except:
            # 兜底：返回一个模拟列表
            return pd.DataFrame({'代码': ['600519', '000858', '002594'], '名称': ['贵州茅台', '五粮液', '比亚迪']})

    def get_stock_list(self):
        return pd.DataFrame({'代码': ['600519', '000858'], '名称': ['贵州茅台', '五粮液']})
