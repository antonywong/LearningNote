# -*- coding: utf-8 -*-
# 日内波动率套利

import json
from typing import List, Dict
from decimal import Decimal
from datetime import datetime
import numpy as np
import pandas as pd
import talib
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
            for l in __cal(underlying, expire_month):
                print(l) 

def __cal(underlying: str, expire_month: str, time: datetime = None) -> List[str]:
    # T型报价
    select_sql = "SELECT strike_price,cCode,pCode FROM VOptionT WHERE underlying='%s' AND expire_month='%s' AND is_standard=1 ORDER BY strike_price"
    option_t = mssql.queryAll(select_sql % (underlying, expire_month))

    # 最新买卖价
    select_sql = "SELECT top(1) time,underlying_price,data FROM OptionPrice WHERE underlying='%s' AND expire_month='%s' AND calculated=1"
    if time:
        select_sql += " AND time <= '%s'" % datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    select_sql += " ORDER BY time DESC"
    option_price = mssql.queryAll(select_sql % (underlying, expire_month))[0]
    underlying_price = option_price['underlying_price']
    main_strike_price = option.get_strike_price_etf(underlying_price)
    price_data =  json.loads(option_price['data'])

    # 扩充T型报价
    for i, t_row in enumerate(option_t):
        t_row["strike_price"] = t_row["strike_price"].quantize(Decimal('0.00'))
        if t_row["strike_price"] == main_strike_price:
            t_row["main"] = "☷"
            if underlying_price < main_strike_price and i > 0:
                option_t[i - 1]["main"] = "☰"
            elif main_strike_price < underlying_price and i < len(option_t) - 1:
                option_t[i + 1]["main"] = "☰"
        elif "main" not in t_row.keys():
            t_row["main"] = ""
        __cal_t(t_row, "c", price_data)
        __cal_t(t_row, "p", price_data)

    result = []
    for t_row in option_t:
        if not t_row["c_v_log"] and not t_row["p_v_log"]:
            continue
        log = f"{t_row["main"]:^2}{t_row["strike_price"]:^6}{t_row["main"]:^2}"
        log = f"{t_row["c_delta_log"]:>5} {log} {t_row["p_delta_log"]:>5}"
        log = f"{t_row["c_v_log"]:>18} {log} {t_row["p_v_log"]:<18}"
        result.append(log)
    return result

def __cal_t(t_row: Dict[str, object], cp: str, price_data: Dict[str, List[list]]):
    code = t_row[cp + "Code"]
    data = price_data[code]

    # [0:卖一价, 1:卖一量]
    t_row[cp + "_sell"] = data[0]
    # [0:买一价, 1:买一量]
    t_row[cp + "_buy"] = data[1]
    # [0:盘口平均价, 1:内在价值, 2:时间价值, 3:隐含波动率, 4:历史波动率, 5:delta, 6:gamma, 7:vega, 8:theta, 9:rho]
    t_row[cp + "_index"] = data[3]

    # 波动率日志
    iv = round(data[3][3] * 10000)
    hv = round(data[3][4] * 10000)
    t_row[cp + "_v_log"] = f"{iv:>5}-{hv:<5}={iv-hv:>5}" if iv > 1 else ""

    # delta日志
    t_row[cp + "_delta_log"] = f"{round(data[3][5] * 10000)}"
