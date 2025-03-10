# # -*- coding: utf-8 -*-

import time
import json
from datetime import datetime
from typing import List
from config import trading_day
from dal import mssql
from crawler import etf_option as etf_op_crawler, stock as stock_crawler
import option as base


def post_tick(request_json: dict) -> str:
    time = None
    underlying = request_json["underlying"]
    underlying_price = request_json["underlying_price"]
    expire_month = request_json["expire_month"]
    data = {}
    for key, value in request_json["tick"].items():
        time = datetime.strptime(value["timetag"][0:17], '%Y%m%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        code = key[0:8]
        data[code] = __to_price(value)        
        
    select_sql = "SELECT COUNT(0) AS count FROM OptionPrice WHERE time='%s' AND underlying='%s' AND expire_month='%s'"
    if mssql.queryAll(select_sql % (time, underlying, expire_month))[0]["count"] == 0:
        para = (time, underlying, underlying_price, expire_month, json.dumps(data, separators=(',', ':')))
        insert_sql=["INSERT INTO OptionPrice (time,underlying,underlying_price,expire_month,data) VALUES ('%s','%s','%s','%s','%s')" % para]
        mssql.run(insert_sql)

    return ""


def __to_price(price):
    """
    Returns:
        List:
            [0:卖一价, 1:卖一量],
            [0:买一价, 1:买一量],
            [0:最新价],
    """
    #print(price)
    return [
        [round(price["askPrice"][0], 4), int(price["askVol"][0])],
        [round(price["bidPrice"][0], 4), int(price["bidVol"][0])],
        [round(price["lastPrice"], 4)]
    ]