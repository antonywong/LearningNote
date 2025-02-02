# -*- coding: utf-8 -*-
import math
from dal import mssql
from crawler import etf_option as etf_op_crawler
import pandas as pd

COMMISSION = 2.6
MARGIN_RITE = 1.15

def collect(underlying, expire_day):
    select_sql = "SELECT code, is_call, strike_price FROM OptionInfo WHERE underlying='%s' AND expire_day='%s' ORDER BY strike_price, is_call DESC"
    contracts = mssql.queryAll(select_sql % (underlying, expire_day))

    contract_codes = [row["code"] for row in contracts]
    all_price = etf_op_crawler.get_price(contract_codes)
    # print(all_price)

    for row in contracts:
        row["strike_price"] = int(row["strike_price"])
        row["卖价一"] = int(float(all_price[row["code"]].loc[20, "值"]) * 10000)
        row["卖量一"] = int(all_price[row["code"]].loc[21, "值"])
        row["买价一"] = int(float(all_price[row["code"]].loc[22, "值"]) * 10000)
        row["买量一"] = int(all_price[row["code"]].loc[23, "值"])
    # df = pd.DataFrame(contracts)
    # print(df)

    price = []
    for i in range(0, len(contracts), 2):
        row1= contracts[i]
        row2= contracts[i + 1]
        p = { "strike_price": row1["strike_price"] }
        p['合成多'] = row1['strike_price'] * 10 + row1['卖价一'] - row2['买价一']
        p['合成空'] = row2['strike_price'] * 10 + row1['买价一'] - row2['卖价一']
        p['组合数量'] = min(row1["卖量一"], row1["买量一"], row2["卖量一"], row2["买量一"])
        price.append(p)
    # df2 = pd.DataFrame(price)
    # print(df2)

    group = []
    for long in price:
        long_price = long['合成多']
        long_strike_price = long['strike_price']
        for short in price:
            short_price = short['合成空']
            profit = short_price - long_price - COMMISSION * 6
            if profit <= 0:
                continue

            short_strike_price = short['strike_price']
            margin = abs(long_strike_price - short_strike_price) * 20 * MARGIN_RITE
            g = { "策略": "L%s:S%s" % (long_strike_price, short_strike_price), "收益": profit, "收益率": profit / margin * 100 }
            group.append(g)
    group = sorted(group, key = lambda x: x['收益率'])
    if len(group) == 0:
        print("无")
    else:
        df3 = pd.DataFrame(group)
        print(df3)