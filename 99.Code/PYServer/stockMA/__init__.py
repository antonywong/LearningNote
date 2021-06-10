#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dal


def syn(kType, code = ""):
    if not code:
        sql = "SELECT code FROM Stock s"
        stocks = dal.queryAll(sql)
        for s in stocks:
            getStockK(kType, s[0])
    else:
        getStockK(kType, code)


def getStockK(kType, code):
    print(kType, "计算均值", code)
    sql = "SELECT id,close,ma10,high,low FROM StockK%s WHERE code='%s' ORDER BY day" % (kType, code)
    kLines = dal.queryAll(sql)
    calMA(kType, kLines)
    calMACD(kType, code, kLines)


def calMA(kType, kLines):
    if len(kLines) > 10:
        for i in range(9, len(kLines)):
            if kLines[i][2]:
                continue

            k5close = list(map(lambda x: x[1], kLines[i - 4 : i + 1]))
            ma5 = sum(k5close) / 5

            k10close = list(map(lambda x: x[1], kLines[i - 9 : i + 1]))
            ma10 = sum(k10close) / 10

            sql = "UPDATE StockK%s SET ma5=%.4f,ma10=%.4f WHERE id='%s'" % (kType, ma5, ma10, kLines[i][0])
            dal.run(sql)


def calMACD(kType, code, kLines):
    if len(kLines) == 0:
        return

    ks = list(map(lambda x: {"id": x[0], "close": x[1], "high": x[3], "low": x[4]}, kLines))
    ks[0]["EMA12"] = ks[0]["close"]
    ks[0]["EMA26"] = ks[0]["close"]
    ks[0]["DIF"] = 0
    ks[0]["DEA"] = 0
    ks[0]["MACD"] = 0
    
    for i in range(1, len(ks)):
        ks[i]["EMA12"] = EMA(12, ks[i - 1]["EMA12"], ks[i]["close"])
        ks[i]["EMA26"] = EMA(26, ks[i - 1]["EMA26"], ks[i]["close"])
        ks[i]["DIF"] = ks[i]["EMA12"] - ks[i]["EMA26"]
        ks[i]["DEA"] = EMA(9, ks[i - 1]["DEA"], ks[i]["DIF"])
        ks[i]["MACD"] = (ks[i]["DIF"] - ks[i]["DEA"]) * 2

    trend = ""
    now = {}
    k1 = ks[-1]
    k2 = ks[-2]
    k3 = ks[-3]
    if k3["MACD"] < k2["MACD"] and k2["MACD"] < k1["MACD"]:
        trend = "+"
        now = k1
    elif k3["MACD"] < k2["MACD"] and k2["MACD"] > k1["MACD"]:
        trend = "+"
        now = k2
    elif k3["MACD"] > k2["MACD"] and k2["MACD"] > k1["MACD"]:
        trend = "-"
        now = k1
    elif k3["MACD"] > k2["MACD"] and k2["MACD"] < k1["MACD"]:
        trend = "-"
        now = k2

    macds = []
    for i in range(2, len(ks) - 1):
        ak = ks[-1 - i + 1]
        k = ks[-1 - i]
        pk = ks[-1 - i - 1]
        if (trend == "+" and k["MACD"] > ak["MACD"] and k["MACD"] > pk["MACD"]) or (trend == "-" and k["MACD"] < ak["MACD"] and k["MACD"] < pk["MACD"]):
            macds.append(k)
            if len(macds) >= 5:
                break

    # for k in macds:
    #     print(k)
    # print(trend, now)

    bl = 0
    for k in macds:
        if (trend == "+" and (now["high"] <= k["high"] or now["MACD"] > k["MACD"])) or (trend == "-" and (now["low"] >= k["low"] or now["MACD"] < k["MACD"])):
            break
        bl += 1

    result = ""
    if bl > 0:
        result += "%s%d" % (trend, bl)
    sql = "UPDATE Stock SET ma%s='%s' WHERE code='%s';" % (kType, result, code)
    dal.run(sql)


def EMA(length, lastEMA, value):
    return lastEMA * (length - 1) / (length + 1) + value * 2 / (length + 1)