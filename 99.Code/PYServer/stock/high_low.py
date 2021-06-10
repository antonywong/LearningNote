#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import dal


def syn(code = ""):
    if code:
        getStockDays(code)
    else:
        sql = "SELECT code FROM Stock ORDER BY updateDate"
        for stock in dal.queryAll(sql):
            getStockDays(stock[0])


def getStockDays(code):
    sql = "SELECT * FROM StockKD WHERE code='%s' ORDER BY day" % code
    days = dal.queryAll(sql)

    today = days[-1][2]

    oldHighDays = 1
    oldHigh = float(days[-2][4])
    for i in range(1, len(days)):
        day = days[-1 - i]
        if oldHigh < float(day[4]):
            oldHighDays = i - 1
            break
        else:
            oldHighDays = i - 1
            continue

    highDays = 1
    todayHigh = float(days[-1][4])
    for i in range(0, len(days)):
        day = days[-1 - i]
        if todayHigh < float(day[4]):
            highDays = i
            break
        else:
            highDays = i
            continue

    oldLowDays = 1
    oldLow = float(days[-2][5])
    for i in range(1, len(days)):
        day = days[-1 - i]
        if float(day[5]) < oldLow:
            oldLowDays = i - 1
            break
        else:
            oldLowDays = i - 1
            continue

    lowDays = 1
    todayLow = float(days[-1][5])
    for i in range(0, len(days)):
        day = days[-1 - i]
        if float(day[5]) < todayLow:
            lowDays = i
            break
        else:
            lowDays = i
            continue

    sql = "UPDATE Stock SET oldHighDays=%d,newHighDays=%d,oldLowDays=%d,newLowDays=%d,updateDate='%s' WHERE code='%s'" % (oldHighDays, highDays, oldLowDays, lowDays, today, code)
    rowc = dal.run(sql)
    print("计算高低值", code, "--", oldHighDays, "--", highDays, "--", oldLowDays, "--", lowDays, "--", rowc)
