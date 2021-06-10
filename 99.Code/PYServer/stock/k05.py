#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dal
import stock
from stock import k30
import stockMA


def syn(code = ""):
    sql = "SELECT code,(SELECT day FROM StockK05 k WHERE k.code=s.code ORDER BY day DESC LIMIT 1 OFFSET 0) AS lastK FROM Stock s"
    if code:
        sql += " WHERE code='%s'" % code
    stocks = dal.queryAll(sql)
    for s in stocks:
        getStockK(s[0], s[1])

    k30.syn(code)


def getStockK(code, lastKStr):
    print("05", "获取K线", code)
    if not lastKStr:
        lastKStr = "1989-01-01 00:00:00"
    sql = "SELECT CONVERT(CHAR(19),day,25) AS day,[open],high,low,[close],volume FROM StockK05 WHERE code='%s' AND day>=CONVERT(DATETIME,'%s') ORDER BY day" % (code, lastKStr)
    k01s = dal.mssql.queryAll(sql)
    if len(k01s) != 0:
        sql = "DELETE FROM StockK05 WHERE code='%s' AND day>='%s'" % (code, k01s[0]["day"])
        dal.run(sql)

        ks = []
        for k in k01s:
            ks.append((code, k["day"], k["open"], k["high"], k["low"], k["close"], k["volume"]))
            if len(ks) == 500:
                stock.insert(ks, "05")
                ks = []
        
        stock.insert(ks, "05")
        ks = []

        stockMA.syn("05", code)