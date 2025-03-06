# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import config
from config import trading_day
import option
import arbitrage._04, arbitrage._03
from bot import mail

underlying = ""
expire_month = ""

# 创建图表
fig, ax = plt.subplots()
x = ["0"]
y = [0]
line, = ax.plot(x, y)

def update(frame):
    """更新图表数据的函数"""
    option.calculate_index()

    # 获取新数据
    x, y, strike_price = arbitrage._04.get_new_data(underlying, expire_month)
    volume_increase = arbitrage._04.get_volume_increase(underlying)

    option_price = arbitrage._03.get_option_price(underlying, expire_month)
    option_t = arbitrage._03.cal(underlying, expire_month, option_price)
    delta = 0
    for t in option_t:
        c_delta = round(t["c_delta"] * 10000)
        p_delta = round(t["p_delta"] * 10000)
        c_lot = (t["cLot"] if t["cLot"] else 0) + (t["cLotTemp"] if t["cLotTemp"] else 0)
        p_lot = (t["pLot"] if t["pLot"] else 0) + (t["pLotTemp"] if t["pLotTemp"] else 0)
        delta += c_delta * c_lot + p_delta * p_lot
    if trading_day.is_trading_time() and abs(delta) > 2000:
        mail.send_message("1411038526@qq.com", "组合delta预警", f"组合delta：{delta}")

    ax.set_title(f'[{strike_price}]=[volume:{round(volume_increase * 100, 2)}%]=[delta:{delta}]')

    # 更新线条数据
    line.set_data(x, y)
    
    # 自动调整坐标轴范围
    ax.relim()        # 重新计算数据范围
    ax.autoscale_view()  # 自动调整坐标轴

    return line,

# 创建动画对象
ani = animation.FuncAnimation(
    fig,         # 图表对象
    update,      # 更新函数
    interval = config.collectionInterval * 1000,
    blit=False   # 禁用blit以支持坐标轴更新
)

def run(u: str, e: str):
    global underlying, expire_month
    underlying = u
    expire_month = e
    # 显示图表
    plt.show()

    update(None)