# -*- coding: utf-8 -*-
# 动态delta中性双卖套利

import json
from typing import List, Dict
from decimal import Decimal
from datetime import datetime, timedelta
import option
from dal import mssql
import arbitrage._05


def run(request_json: dict) -> dict:
    print(request_json)
    option.calculate_index()

    is_test = request_json["test"]
    underlying = request_json["underlying"]
    expire_month = request_json["expire_month"]
    result = { "msg": "", "code": "" }

    option_price = arbitrage._05.get_option_price(underlying, expire_month)
    if not is_test and abs((datetime.now() - option_price["time"]).seconds) > 5:
        result["msg"] = "无最新价格"
        return result

    select_sql = "SELECT strike_price,cCode,pCode FROM VOptionT WHERE underlying='%s' AND expire_month='%s' AND is_standard=1 ORDER BY strike_price"
    option_t = mssql.queryAll(select_sql % (underlying, expire_month))
    oprations = []
    for t_row in option_t:
        oprations.append(arbitrage._05.cal(True, True, t_row["cCode"], t_row["strike_price"], option_price))
        oprations.append(arbitrage._05.cal(True, False, t_row["cCode"], t_row["strike_price"], option_price))
        oprations.append(arbitrage._05.cal(False, True, t_row["pCode"], t_row["strike_price"], option_price))
        oprations.append(arbitrage._05.cal(False, False, t_row["pCode"], t_row["strike_price"], option_price))

    contracts = []
    for op in oprations:
        delta = op[2]
        theta = op[3]
        sell1 = op[5]
        buy1 = op[6]
        handicap = sell1/ buy1 - 1
        if 0.1 < abs(delta) and 0.1 < theta and 0.0001 < sell1 and 0.0001 < buy1 and handicap < 0.02:
            contracts.append(op)
    contracts = sorted(contracts, key=lambda x: x[3], reverse=True)

    gear = 1
    old_delta = 0.2
    for contract in contracts:
        print(contract)
        contract_delta = contract[2]
        if abs(old_delta + contract_delta * gear) < abs(old_delta):
            result["is_open"] = True
            result["gear"] = gear
            result["oprations"] = contract[7]
            return result

    return result
