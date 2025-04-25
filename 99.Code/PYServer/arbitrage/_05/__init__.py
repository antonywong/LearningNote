# -*- coding: utf-8 -*-
# 动态delta中性双卖套利

from datetime import datetime, timedelta
from decimal import Decimal
from dal import mssql
import option
from arbitrage._05.ModelOptionProperty import ModelOptionProperty


def cal(is_call: bool, is_buy: bool, code: str, strike_price: Decimal, option_price: dict) -> ModelOptionProperty:
    underlying_price = Decimal(option_price['underlying_price'])
    price_data = option_price['data']

    #选择买一卖一均价作为参数基准
    properties = price_data[code][3]
    result = ModelOptionProperty(
        op_code = "+" + code,
        holding_cost = float(round(properties[0] * 10000, 2)),
        time_value = float(properties[2]),
        delta = float(properties[5]),
        gamma = float(properties[6]),
        vega = float(properties[7]),
        theta = float(properties[8]),
        strike_price = strike_price.quantize(Decimal("0.00")),
        op_name = "买"
    )
    if not is_buy:
        result.op_code = "-" + code
        result.holding_cost = float(option.get_seller_holding_cost(is_call, underlying_price, strike_price))
        result.delta *= -1
        result.theta *= -1
        result.gamma *= -1
        result.vega *= -1
        result.op_name = "卖"

    if is_call:
        result.op_name += "购"
    else:
        result.op_name += "沽"

    return result