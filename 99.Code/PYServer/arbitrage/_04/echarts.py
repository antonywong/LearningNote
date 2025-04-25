# -*- coding: utf-8 -*-

from decimal import Decimal
import option
import arbitrage._04
from strategy.qmt import delta


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
        
        # 行权价
        option_prices = option.get_latest_option_price(underlying, expire_month)
        underlying_price = Decimal(option_prices["underlying_price"])
        strike_price, secondary_strike_price = option.get_strike_price_etf(underlying_price, True)

        # 获取标题
        volume_increase = arbitrage._04.get_volume_increase(underlying)
        d = ",".join([f"{key}:{round(data["delta"], 4)}"  for key, data in delta.TOTAL_INDEX.items()])
        result["title"] = f'[{option_prices["time"]}] - [{int(strike_price*100)}] - [volume:{round(volume_increase * 100, 2)}%] - [delta:{d}]'

        # 获取新数据
        codes = list(set([position[1:] for key, data in delta.TOTAL_INDEX.items() for position in data["position_contracts"]]))
        x, y = arbitrage._04.get_new_data(codes)
        result["x"] = x
        result["y"] = [round(f, 4) for f in y]

        return result,
    except Exception as e:
        print(e)
    finally:
        IS_RUNNING = False