# -*- coding: utf-8 -*-
# 深度实值折价双买套利

import json
from typing import List
import option
from dal import mssql
from config import trading_day

def run(underlyings: List[str], expire_months: List[str], is_test: bool = False):    
    if not is_test and not trading_day.is_trading_time():
        return

    if len(underlyings) == 0:
        underlyings = [y for x in option.UNDERLYING for y in x['etf']]
    
    if len(expire_months) == 0:
        print("无过期月")
        return

    for underlying in underlyings:
        for expire_month in expire_months:
            # 最新买卖价
            select_sql = "SELECT top(1) time,underlying_price,data FROM OptionPrice WHERE underlying='%s' AND expire_month='%s'"
            option_price = mssql.queryAll(select_sql % (underlying, expire_month))[0]
            price_data = json.loads(option_price['data'])

            # T型报价
            select_sql = "SELECT CAST(strike_price*10000 AS INT) AS strike_price,cCode,pCode FROM VOptionT WHERE underlying='%s' AND expire_month='%s' AND is_standard=1 ORDER BY strike_price"
            option_t = mssql.queryAll(select_sql % (underlying, expire_month))

            for i in range(len(option_t)):
                for j in range(i + 1, len(option_t)):
                    c_strike_price = option_t[i]["strike_price"]
                    p_strike_price = option_t[j]["strike_price"]
                    c_price = price_data[option_t[i]["cCode"]][0]
                    p_price = price_data[option_t[j]["pCode"]][0]
                    c_sell_price = round(c_price[0] * 10000)
                    p_sell_price = round(p_price[0] * 10000)
                    c_sell_volume = c_price[1]
                    p_sell_volume = p_price[1]
                    if c_sell_price == 0 or p_sell_price == 0 or c_sell_volume == 0 or p_sell_volume == 0:
                        continue
                    cost = c_sell_price + p_sell_price + option.OPTION_COMMISSION * 2 + option.OPTION_STRIKE_COMMISSION * 2
                    rece = p_strike_price - c_strike_price
                    earn = rece - cost
                    rate = int(earn * 10000 / cost)
                    if earn > 0:
                        if earn > 0:
                            print("★", end="")
                        else:
                            print("◇", end="")
                        print("双买套利", option_price['time'], underlying, end=" ")
                        print(f"{c_strike_price:>5}", end="")
                        print(f"{json.dumps(c_price, separators=(',', ':')):<13}", end="")
                        print(f"{p_strike_price:>5}", end="")
                        print(f"{json.dumps(p_price, separators=(',', ':')):<13}", end="成本:")
                        print(c_sell_price, end="+")
                        print(p_sell_price, end="+")
                        print(option.OPTION_COMMISSION * 2 + option.OPTION_STRIKE_COMMISSION * 2, end="=")
                        print(f"{cost:<7}", end="\t盈利:")
                        print(-cost, end="+")
                        print(rece, end="=")
                        print(earn, end="\t收益率:")
                        print(rate, end="")
                        print("/10000")

