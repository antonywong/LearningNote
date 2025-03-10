# -*- coding: utf-8 -*-
# 动态delta中性双卖套利

import json
from typing import List, Dict
from decimal import Decimal
from datetime import datetime
import option
from dal import mssql


def run(underlying: str, expire_month: str):
    option_price = get_option_price(underlying, expire_month)
    select_sql = "SELECT strike_price,cCode,pCode,cLot,pLot,cLotTemp,pLotTemp FROM VOptionTLot WHERE underlying='%s' AND expire_month='%s' AND is_standard=1 ORDER BY strike_price"
    option_t = mssql.queryAll(select_sql % (underlying, expire_month))
    result = []
    for t_row in option_t:
        result.append(cal(True, True, t_row["cCode"], t_row["strike_price"], option_price))
        result.append(cal(True, False, t_row["cCode"], t_row["strike_price"], option_price))
        result.append(cal(False, True, t_row["pCode"], t_row["strike_price"], option_price))
        result.append(cal(False, False, t_row["pCode"], t_row["strike_price"], option_price))

    result = sorted(result, key=lambda x: x[1], reverse=False)
    for r in result:
        if 0.001 < abs(r[1]) and abs(r[1]) < 0.999:
            print(r)


def get_option_price(underlying: str, expire_month: str, time: datetime = None) -> dict:
    # 最新买卖价
    select_sql = "SELECT top(1) time,underlying_price,data FROM OptionPrice WHERE underlying='%s' AND expire_month='%s' AND calculated=1"
    if time:
        select_sql += " AND time <= '%s'" % datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    select_sql += " ORDER BY time DESC"
    return mssql.queryAll(select_sql % (underlying, expire_month))[0]


def cal(is_call: bool, is_buy: bool, code: str, strike_price: Decimal, option_price: dict):
    underlying_price = option_price['underlying_price']
    price_data = json.loads(option_price['data'])

    delta = price_data[code][3][5]
    theta = price_data[code][3][8]
    opration = ""
    holding_cost = 0
    if is_buy:
        opration += "买"
        holding_cost = (Decimal(price_data[code][3][0]) * Decimal("10000")).quantize(Decimal("0.00"))
    else:
        opration += "卖"
        delta *= -1
        theta *= -1
        holding_cost = option.get_seller_holding_cost(is_call, underlying_price, strike_price)

    if is_call:
        opration += "购"
    else:
        opration += "沽"

    return (code, strike_price.quantize(Decimal("0.00")), delta, theta, holding_cost, price_data[code][0][0], price_data[code][1][0], opration)
