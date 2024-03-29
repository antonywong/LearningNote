#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import time

from dal import mssql
from config import trading_day
from crawler import stock as stock_crawler

def syn(code = ""):
    if code:
        getStockK(code)
        # kd.syn(code)
    else:
        sql = "SELECT code FROM Stock ORDER BY code"
        for s in mssql.queryAll(sql):
            if getStockK(s['code']):
                time.sleep(4)
        # kd.syn()


def getStockK(code):
    print("爬虫获取日线", code, end='')

    sql = "SELECT TOP(1) day FROM StockK WHERE code='%s' AND type=240 ORDER BY day DESC" % code
    day = mssql.queryAll(sql)
    lastK = datetime(2000,1,1,0,0,0) if len(day) == 0 else day[0]["day"]

    LastTradingDay = trading_day.get_last()
    days = (LastTradingDay - lastK).days
    if days < 1:
        print("\t0")
        return False
    allK = stock_crawler.get_k(code, 240, min(days + 14, 500))

    sqls = []
    sql_insert = "INSERT INTO StockK (code,[day],[type],[open],[high],[low],[close],[volume],[ma005],[ma010],[ma030]) VALUES ('%s','%s',240,%s,%s,%s,%s,%s,%s,%s,%s);"
    for i, row in allK.iterrows():
        if datetime.strptime(row["day"], '%Y-%m-%d') > lastK:
            sqls.append(sql_insert % (code, row["day"], row["open"], row["high"], row["low"], row["close"], row["volume"], row["ma_price5"], row["ma_price10"], row["ma_price30"]))
    if len(sqls) != 0:
        mssql.run(sqls)

    print(f"\t{len(sqls)}")    
    
    sql = "SELECT TOP(500) day FROM StockK WHERE code='%s' AND type=240 ORDER BY day DESC" % code
    stockKs = mssql.queryAll(sql)
    if len(stockKs) != 0:
        firstDay = stockKs[-1]["day"]    
        sql = [f"DELETE FROM StockK WHERE code='{code}' AND type=240 AND day<'{firstDay}'"]
        mssql.run(sql)

    return True
