#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import dal
import stock
import stockMA


def syn(code = ""):
    sql = "SELECT code,(SELECT day FROM StockK30 k WHERE k.code=s.code ORDER BY day DESC LIMIT 1 OFFSET 1) AS lastK FROM Stock s"
    if code:
        sql += " WHERE code='%s'" % code
    stocks = dal.queryAll(sql)
    for stock in stocks:
        getStockK(stock[0], stock[1])


k30s = []
def getStockK(code, lastKStr):
    print("30", "获取K线", code)
    global k30s
    sql = "SELECT day,open,high,low,close,volume FROM StockK05 WHERE code='%s'" % code
    if lastKStr:
        sql += " AND day>'%s'" % lastKStr
    sql += " ORDER BY day"
    k01s = dal.queryAll(sql)
    ks = []
    for k in k01s:
        ks.append(k)
        if len(ks) == 6:
            gene30(code, ks)
            ks = []
    sql = "DELETE FROM StockK30 WHERE code='%s' AND day>'%s'" % (code, lastKStr)
    dal.run(sql)

    stock.insert(k30s, "30")
    k30s = []

    stockMA.syn("30", code)


def gene30(code, ks):
    day = ks[5][0]
    ope = ks[0][1]
    hig = max([ks[0][2], ks[1][2], ks[2][2], ks[3][2], ks[4][2], ks[5][2]])
    low = min([ks[0][3], ks[1][3], ks[2][3], ks[3][3], ks[4][3], ks[5][3]])
    clo = ks[5][4]
    vol = sum([ks[0][5], ks[1][5], ks[2][5], ks[3][5], ks[4][5], ks[5][5]])
    k30s.append((code, day, ope, hig, low, clo, vol))
