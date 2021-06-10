#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import dal
import stock
import stockMA


def syn(code = ""):
    sql = "SELECT code,(SELECT day FROM StockKW k WHERE k.code=s.code ORDER BY day DESC LIMIT 1 OFFSET 1) AS lastK FROM Stock s"
    if code:
        sql += " WHERE code='%s'" % code
    stocks = dal.queryAll(sql)
    for stock in stocks:
        getStockK(stock[0], stock[1])


kws = []
def getStockK(code, lastKStr):
    print("kw", "KL", code)
    global kws
    sql = "SELECT day,open,high,low,close,volume FROM StockKD WHERE code='%s'" % code
    sqlDelete = "DELETE FROM StockKW WHERE code='%s'" % code
    if lastKStr:
        sql += " AND day>'%s'" % lastKStr
        sqlDelete += " AND day>'%s'" % lastKStr
    sql += " ORDER BY day"
    dal.run(sqlDelete)
    kds = dal.queryAll(sql)
    week = 0
    ks = []
    for kd in kds:
        day = datetime.strptime(kd[0], '%Y-%m-%d')
        firstDay = datetime.strptime("1989-01-01", '%Y-%m-%d')
        w = int((day - firstDay).days / 7)
        if w != week:
            geneW(code, ks)
            week = w
            ks = [kd]
        else:
            ks.append(kd)
    geneW(code, ks)

    stock.insert(kws, "W")
    kws = []

    stockMA.syn("W", code)


def geneW(code, ks):
    if len(ks) != 0:
        day = ks[-1][0]
        ope = ks[0][1]
        hig = max(list(map(lambda x: x[2], ks)))
        low = min(list(map(lambda x: x[3], ks)))
        clo = ks[-1][4]
        vol = sum(list(map(lambda x: x[5], ks)))
        kws.append((code, day, ope, hig, low, clo, vol))
