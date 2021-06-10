#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dal
import stock
from stock import high_low, kw
import stockMA


def syn(code = ""):
    sql = "SELECT code,(SELECT day FROM StockKD k WHERE k.code=s.code ORDER BY day DESC LIMIT 1 OFFSET 0) AS lastK FROM Stock s"
    if code:
        sql += " WHERE code='%s'" % code
    print(sql)
    stocks = dal.queryAll(sql)
    for s in stocks:
        getStockK(s[0], s[1])

    kw.syn(code)


def getStockK(code, lastKStr):
    print("获取日线", code)
    if not lastKStr:
        lastKStr = "1989-01-01"
    sql = "SELECT TOP(500) CONVERT(CHAR(10),day,23) AS day,[open],high,low,[close],volume FROM StockKD WHERE code='%s' AND day>=CONVERT(DATETIME,'%s') ORDER BY day DESC" % (code, lastKStr)
    k01s = dal.mssql.queryAll(sql)
    if len(k01s) != 0:
        sql = "DELETE FROM StockKD WHERE code='%s' AND day>='%s'" % (code, lastKStr)
        dal.run(sql)

        ks = []
        for k in k01s:
            ks.append((code, k["day"], k["open"], k["high"], k["low"], k["close"], k["volume"]))
            if len(ks) == 500:
                stock.insert(ks, "D")
                ks = []
        
        stock.insert(ks, "D")
        ks = []

        stockMA.syn("D", code)
        high_low.syn(code)