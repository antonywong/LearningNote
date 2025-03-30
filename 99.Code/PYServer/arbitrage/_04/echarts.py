# -*- coding: utf-8 -*-

from config import trading_day
import option
import arbitrage._04, arbitrage._03
from bot import mail


IS_RUNNING = False


def fetch(underlying: str):
    global IS_RUNNING
    result = { "msg": "", "title": "", "x": [], "y": [] }
    if IS_RUNNING:
        print("IS_RUNNING")
        result["msg"] = "IS_RUNNING"
        return result

    try:
        IS_RUNNING = True
        """更新图表数据的函数"""
        expire_month = option.get_etf_option_expire_day()[0][0:4]
        # 获取新数据
        x, y, strike_price = arbitrage._04.get_new_data(underlying, expire_month, None)
        volume_increase = arbitrage._04.get_volume_increase(underlying)

        option_price = option.get_latest_option_price(underlying, expire_month)
        option_t = arbitrage._03.cal(underlying, expire_month, option_price)
        delta = 0
        for t in option_t:
            c_delta = round(t["c_delta"] * 10000)
            p_delta = round(t["p_delta"] * 10000)
            c_lot = (t["cLot"] if t["cLot"] else 0) + (t["cLotTemp"] if t["cLotTemp"] else 0)
            p_lot = (t["pLot"] if t["pLot"] else 0) + (t["pLotTemp"] if t["pLotTemp"] else 0)
            delta += c_delta * c_lot + p_delta * p_lot
        if trading_day.is_trading_time() and abs(delta) > 40000:
            mail.send_message("1411038526@qq.com", "组合delta预警", f"组合delta：{delta}")

        result["title"] = f'[{option_price["time"]}] - [{strike_price}] - [volume:{round(volume_increase * 100, 2)}%] - [delta:{delta}]'
        result["x"] = x
        result["y"] = [round(f, 4) for f in y]

        return result,
    except Exception as e:
        print(e)
    finally:
        IS_RUNNING = False