# -*- coding: utf-8 -*-
# 隐含波动率统计

import json
from datetime import datetime
import option
from dal import mssql
import arbitrage._04.chart_pyplot as chart_pyplot

def run(underlying: str, expire_month: str): 
    chart_pyplot.run(underlying, expire_month)

def get_new_data(underlying: str, expire_month: str):
    # 最新买卖价
    select_sql = "SELECT top(3500) time,underlying,underlying_price,data FROM OptionPrice WHERE underlying='%s' AND expire_month='%s' AND calculated=1 AND DATEPART(HOUR,time)*100+DATEPART(MINUTE,time)<1457"
    option_prices = mssql.queryAll(select_sql % (underlying, expire_month))

    # T型报价
    strike_price, secondary_strike_price = option.get_strike_price_etf(option_prices[0]['underlying_price'], True)
    select_sql = "SELECT strike_price,cCode,pCode FROM VOptionT WHERE underlying='%s' AND expire_month='%s' AND is_standard=1 AND (strike_price='%s'" % (underlying, expire_month, strike_price)
    if secondary_strike_price:
        select_sql += " OR strike_price='%s'" % secondary_strike_price
    option_ts = mssql.queryAll(select_sql + ")")
    codes = []
    for t in option_ts:
        codes.extend([t["cCode"], t["pCode"]])

    price_data = [{"time": option_price['time'], "data": json.loads(option_price['data'])} for option_price in option_prices]
    main_price_data = {}
    for price in price_data:
        minute = datetime.strptime(price["time"].strftime("%Y%m%d%H%M"), "%Y%m%d%H%M")

        if minute not in main_price_data.keys():
            main_price_data[minute] = []
        for code in codes:
            main_price_data[minute].extend([price['data'][code][2][3], price['data'][code][3][3]])

    main_price_ivs = [{"time": key, "ivs": [iv for iv in main_price_data[key] if iv > 0.0001]} for key in main_price_data.keys()]
    main_price_iv = [{"time": ivs["time"], "iv": sum(ivs["ivs"]) / len(ivs["ivs"])} for ivs in main_price_ivs]
    main_price_iv = sorted(main_price_iv, key=lambda x: x["time"], reverse=False)

    # 更新数据集
    new_x = [pd["time"].strftime("%m%d%H%M") for pd in main_price_iv]
    new_y = [pd["iv"] for pd in main_price_iv]
    return new_x, new_y, strike_price


def get_volume_increase(underlying: str) -> float:
    index = option.GET_UNDERLYING_INDEX(underlying)
    sql = f"""SELECT * FROM (
        SELECT CAST(day AS DATE) AS day, SUM(volume) AS volume FROM (
            SELECT day,volume,CAST(GETDATE() AS DATE) AS today, DATEADD(DAY, -7, CAST(GETDATE() AS DATE)) AS first,
            DATEPART(HOUR,GETDATE())*100 + DATEPART(MINUTE,GETDATE()) AS now
            FROM StockK WHERE type=5 AND code='{index}'
        ) AS t1 WHERE first<=CAST(day AS DATE) AND CAST(day AS DATE)<=today AND DATEPART(HOUR, day)*100 + DATEPART(MINUTE, day) <= now
        GROUP BY CAST(day AS DATE)
    ) t2 ORDER BY day DESC"""
    volumes = mssql.queryAll(sql)
    if len(volumes) < 2:
        return 0.0
    today = float(volumes[0]["volume"])
    before = [float(volumes[i]["volume"]) for i in range(1, len(volumes))]
    return today / sum(before) * len(before) - 1.0
