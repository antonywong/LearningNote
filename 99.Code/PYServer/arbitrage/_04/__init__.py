# -*- coding: utf-8 -*-
# 日内波动率套利

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import talib
from typing import List
import option
from dal import mssql
from config import trading_day

def run(underlyings: List[str], expire_months: List[str]):    
    if len(underlyings) == 0:
        underlyings = [y for x in option.UNDERLYING for y in x['etf']]
    
    if len(expire_months) == 0:
        print("无过期月")
        return

    for underlying in underlyings:
        for expire_month in expire_months:
            # 最新买卖价
            select_sql = "SELECT top(2500) time,underlying,underlying_price,data FROM OptionPrice WHERE underlying='%s' AND expire_month='%s'"
            option_prices = mssql.queryAll(select_sql % (underlying, expire_month))
            underlying_price = option_prices[0]['underlying_price']
            strike_price = option.get_strike_price_etf(underlying_price)

            # T型报价
            select_sql = "SELECT strike_price,cCode,pCode FROM VOptionT WHERE underlying='%s' AND expire_month='%s' AND is_standard=1 AND strike_price='%s'"
            option_t = mssql.queryAll(select_sql % (underlying, expire_month, strike_price))[0]

            price_data = [{"time": option_price['time'], "data": json.loads(option_price['data'])} for option_price in option_prices]
            main_price_data = [{"time": price['time'], "c_price_data": price['data'][option_t["cCode"]], "p_price_data": price['data'][option_t["pCode"]]}
                               for price in price_data]
            main_price_data = sorted(main_price_data, key=lambda x: x["time"], reverse=False)

            c_price_data = [mpd for mpd in main_price_data if mpd["c_price_data"][3][3] > 0.01]
            iv = [pd["c_price_data"][3][3] for pd in c_price_data]
            iv = talib.SMA(np.array(iv), timeperiod=6)
            chart_data = pd.DataFrame({
                'x': [pd["time"].strftime("%m%d%H%M%S") for pd in c_price_data],
                'iv': iv
            })

            # 绘制柱状图
            chart_data.plot(kind='line', x='x', y='iv', title=f"strike_price[{strike_price}]")
            plt.show()

