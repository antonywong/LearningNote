#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import dal


def syn(kType, para = 5, code = ""):
    if not code:
        sql = "SELECT code FROM Stock s"
        stocks = dal.queryAll(sql)
        for s in stocks:
            getStockK(kType, para, s[0])
    else:
        getStockK(kType, para, code)


def getStockK(kType, para, code):
    print(kType, "分析均值", code)
    sql = "SELECT day,ma5,ma10 FROM StockK%s WHERE code='%s' ORDER BY day desc LIMIT %d OFFSET 0" % (kType, code, para * 40)
    kLines = dal.queryAll(sql)
    states = []
    for k in kLines:
        if k[1] and k[2]:
            state = { "day": k[0], "ma": float(k[1]) - float(k[2]), "matype": 0, "state": "吻"}
            if state["ma"] > 0:
                state["matype"] = 1
            elif state["ma"] < 0:
                state["matype"] = -1
            states.insert(0, state)

    for i in range(para - 1, len(states)):
        if states[i]["state"] == 0:
            states[i]["state"] = states[i - 1]["state"]

        isTrend = True
        for j in range(1, para):
            if states[i - j]["matype"] != states[i]["matype"]:
                isTrend = False
                break
        if isTrend:
            state = "男"
            if states[i]["matype"] == 1:
                state = "女"
            for j in range(0, para):
                states[i - j]["state"] = state

    trands = []
    trand = {"day": states[0]["day"], "area": 0.0, "avg": 0.0, "state": states[0]["state"]}
    area = states[0]["ma"]
    count = 1
    for i in range(1, len(states)):
        if states[i]["state"] == states[i - 1]["state"]:
            area += states[i]["ma"]
            count += 1
        else:
            trand["area"] = area
            trand["avg"] = area / count
            trands.append(trand)
            trand = {"day": states[i]["day"], "area": 0.0, "avg": 0.0, "state": states[i]["state"]}
            area = states[i]["ma"]
            count = 1

    trand["area"] = area
    trand["avg"] = area / count
    trands.append(trand)

    s = summary(trands)
    sql = "UPDATE Stock SET ma%s='%s' WHERE code='%s';" % (kType, s, code)
    dal.run(sql)


def summary(trands):
    realTrands = []
    lastState = trands[-1]["state"]

    if len(trands) < 2:
        return ""

    now = "线段"
    if lastState == "吻":
        now = "中枢"
        realTrands = getRealTrands(trands[0 : len(trands) - 1])
    else:
        realTrands = getRealTrands(trands)

    trand = "↓"
    if realTrands[0]["state"] == "女":
        trand = "↑"

    count = len(realTrands)

    bc = 0
    if len(realTrands) > 1 and abs(realTrands[0]["avg"]) < abs(realTrands[1]["avg"]):
        bc = 1
    if len(realTrands) > 2:
        for i in range(2, len(realTrands)):
            if abs(realTrands[i - 1]["area"]) < abs(realTrands[i]["area"]):
                bc += 1
            else:
                break

    result = "%s-%d-%s-%d" % (trand, count, now, bc)
    return result


def getRealTrands(trands):
    realTrands = []
    lastState = trands[-1]["state"]
    if lastState == "女":
        for i in range(0, len(trands)):
            t = trands[-1 - i]
            if t["state"] =='吻':
                continue
            elif t["state"] =='男':
                break
            else:
                realTrands.append(t)
    elif lastState == "男":
        for i in range(0, len(trands)):
            t = trands[-1 - i]
            if t["state"] =='吻':
                continue
            elif t["state"] =='女':
                break
            else:
                realTrands.append(t)
    return realTrands