# # -*- coding: utf-8 -*-

import time
import requests
import json
from datetime import datetime
from typing import List
from config import trading_day
from dal import mssql
from crawler import etf_option as etf_op_crawler, stock as stock_crawler
import option
import stock


def collect(server_url: str, underlyings: list = [], expire_months: list = [], is_test: bool = False):
    # 盘后数据更新
    if not trading_day.is_after_trading_updated():
        get_daily([], expire_months)
        stock_codes = [y for x in option.UNDERLYING for y in x["etf"]]
        stock_codes.extend([x["index"]for x in option.UNDERLYING])
        stock.collect(stock_codes)
        trading_day.update_after_trading()

    if is_test or trading_day.is_trading_time():
        __collect(server_url, underlyings, expire_months)
        stock_codes = list(set(option.GET_UNDERLYING_INDEX(u) for u in underlyings)) if len(underlyings) > 0 else [u["index"] for u in option.UNDERLYING]
        stock.collect(stock_codes, 5)


def __collect(server_url: str, underlyings: List[str], expire_months: List[str]):
    options = option.get_option_info()
    if underlyings:
        options = [row for row in options if row["underlying"] in underlyings]
    if expire_months:
        options = [row for row in options if row["expire_month"] in expire_months]

    time = datetime.now()    
    expire_months = list(set(row["expire_month"] for row in options))
    underlyings = list(set(row["underlying"] for row in options))
    underlying_prices = stock_crawler.get_price(underlyings)
    all_price = etf_op_crawler.get_price([row["code"] for row in options])
    for i in range(len(underlyings)):
        underlying = underlyings[i]
        underlying_price = underlying_prices.loc[i, "最近成交价"]
        for expire_month in expire_months:
            sub_codes = [row["code"] for row in options if row["expire_month"] == expire_month and row["underlying"] == underlying]
            body = {
                "time": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "underlying": underlying,
                "underlying_price": underlying_price,
                "expire_month": expire_month,
                "data": { key: __to_price(all_price[key]) for key in all_price.keys() if key in sub_codes }
            }
            r = requests.post(server_url + "/v1/api/tick", json.dumps(body), headers={'Content-Type': 'application/json'}, timeout=2.5)


def __to_price(price_df):
    """
    Returns:
        List:
            [0:卖一价, 1:卖一量],
            [0:买一价, 1:买一量],
            [0:最新价],
            [0:卖一买一平均价]
    """
    return [
        [float(price_df.loc[20, "值"]), int(price_df.loc[21, "值"])],
        [float(price_df.loc[22, "值"]), int(price_df.loc[23, "值"])],
        [float(price_df.loc[2, "值"])],
        [round((float(price_df.loc[20, "值"]) + float(price_df.loc[22, "值"])) / 2.0, 5)]
    ]



def update_etf_contract():
    print('更新ETF期权所有合约...')
    # 行权日
    contract_month = etf_op_crawler.get_contract_month()
    expire_day = [etf_op_crawler.get_expire_day(x)[0].replace("-", "") for x in contract_month]
    print('到期日：', end='')
    print(expire_day)

    # 标的代码
    underlyings = [y for x in option.UNDERLYING for y in x['etf']]
    print('标的ETF代码：', end='')
    print(underlyings)

    # 合约代码
    option_info = etf_op_crawler.get_codes(expire_day, underlyings)
    codes = set(option_info['code'])
    all_price = etf_op_crawler.get_price(list(codes))

    # 旧合约
    select_sql = "SELECT code FROM OptionCode"
    old_codes = set(row["code"] for row in mssql.queryAll(select_sql))
    insert_codes = list(codes - old_codes)

    # 插入新合约
    if len(insert_codes) > 0:
        data = [(row["code"],
                 row["underlying"],
                 row["is_call"],
                 all_price[row["code"]].loc[7, "值"],
                 row["expire_day"][2:6],
                 row["expire_day"][6:8],
                 0 if all_price[row["code"]].loc[37, "值"][-1] == "A" else 1) for i, row in
                option_info[option_info["code"].isin(insert_codes)].iterrows()]
        insert_sql = [
            "INSERT INTO OptionCode (code,underlying,is_call,strike_price,expire_month,expire_day,is_standard) VALUES ('%s','%s','%s','%s','%s','%s','%s')"
            % x for x in data
        ]
        mssql.run(insert_sql)
    
    # 更新旧合约
    update_codes = list(codes - set(insert_codes))
    if len(update_codes) > 0:
        data = [(row["expire_day"][6:8],
                 all_price[row["code"]].loc[7, "值"],
                 0 if all_price[row["code"]].loc[37, "值"][-1] == "A" else 1,
                 row["code"]) for i, row in
                option_info[option_info["code"].isin(update_codes)].iterrows()]
        update_sql = [
            "UPDATE OptionCode SET expire_day='%s', strike_price='%s', is_standard='%s' WHERE code='%s'"
            % x for x in data
        ]
        mssql.run(update_sql)

def get_daily(underlyings: List[str], expire_months: List[str]):
    now = datetime.now()
    select_sql = "SELECT code FROM OptionCode WHERE expire_month"
    # 到期月筛选
    if len(expire_months) == 0:
        select_sql += ">='" + f"{now.year}{now.month:02d}'"[2:]
    else:
        select_sql += " in ('" + "','".join(expire_months) + "')"
    # 标的物筛选
    if len(underlyings) > 0:
        select_sql += " AND underlying in ('" + "','".join(underlyings) + "')"

    codes = [row["code"] for row in mssql.queryAll(select_sql)]
    last_trading_day = datetime.strptime(trading_day.get_last(), "%Y-%m-%d")
    print("期权日K线")
    for i, code in enumerate(codes):
        time.sleep(3)

        print("%s/%s:" % (i + 1, len(codes)), end="")
        select_sql = "SELECT TOP(1) day FROM K WHERE type=240 AND code='%s' ORDER BY day DESC" % code
        last_daily = mssql.queryAll(select_sql)
        if len(last_daily) > 0 and last_daily[0]["day"] == last_trading_day:
            print("已完成")
            continue

        ks = etf_op_crawler.get_daily(code).drop_duplicates()
        sql = ["DELETE FROM K WHERE code='%s' AND type=240 AND day=CONVERT(DATETIME,'%s',102)" % (code, row["日期"]) for i, row in ks.iterrows()]
        sql.extend(["INSERT INTO K (code,type,day,[open],high,low,[close],volume) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"
                    % (code, "240", row["日期"], row["开盘"], row["最高"], row["最低"], row["收盘"], row["成交量"])
                    for i, row in ks.iterrows()])
        mssql.run(sql)
        print("K线数量%s" % int(len(sql) / 2))
    
    delete_sql = "DELETE FROM K WHERE (SELECT MIN(day) FROM TradingDay)<=day AND day<=(SELECT MAX(day) FROM TradingDay) AND CAST(day as DATE) NOT IN (SELECT day FROM TradingDay)"
    mssql.run([delete_sql])