"""
K 线可视化工具 (K-Line Visualizer)
功能：绘制 K 线，标记买卖点，保存图表
"""
import matplotlib.pyplot as plt
import pandas as pd

def plot_kline(df, title="K 线图", buy_points=None, sell_points=None, save_path=None):
    """
    绘制 K 线图
    df: 包含 open, high, low, close 的 DataFrame
    buy_points: 买入日期列表
    sell_points: 卖出日期列表
    """
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # 简单绘制收盘价
    ax.plot(df['date'], df['close'], label='Close Price', linewidth=2)
    
    # 标记买卖点
    if buy_points:
        for date in buy_points:
            ax.axvline(x=date, color='g', linestyle='--', alpha=0.7, label='Buy' if date==buy_points[0] else "")
    if sell_points:
        for date in sell_points:
            ax.axvline(x=date, color='r', linestyle='--', alpha=0.7, label='Sell' if date==sell_points[0] else "")
    
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)
    
    if save_path:
        plt.savefig(save_path)
        print(f"✅ 图表已保存：{save_path}")
    else:
        plt.show()
