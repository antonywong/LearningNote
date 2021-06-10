#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from urllib import request
import json
import time
import dal
from stock import kd


now = None
def syn(nowDate, code = ""):
    global now
    now = datetime.strptime(nowDate,'%Y-%m-%d')
    if code:
        getStockK(code)
        kd.syn(code)
    else:
        sql = "SELECT code FROM Stock ORDER BY code"
        for s in dal.queryAll(sql):
            result = getStockK(s[0])
            if result:
                time.sleep(1.2)
        kd.syn()


def getStockK(code):
    print("爬虫获取日线", code)
    sql = "SELECT top(1) day FROM StockKD WHERE code='%s' ORDER BY day DESC" % code
    day = dal.mssql.queryAll(sql)
    lastK = datetime(1989,1,1,0,0,0)
    if len(day) != 0:
        lastK = datetime.strptime(str(day[0]["day"]),'%Y-%m-%d')

    if lastK >= now:
        return False

    today = datetime.now()
    days = (today - lastK).days + 1
    url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=240&datalen=%d" % (code, days)
    with request.urlopen(url) as f:
        data = json.loads(f.read().decode('gb2312'))
        kLines = []
        for kLine in data:
            if datetime.strptime(kLine["day"], '%Y-%m-%d') > lastK:
                kLines.append(kLine)

        record(code, kLines)
    return True


def record(code, kLines):
    Ks = []
    for k in kLines:
        Ks.append((code, k["day"], k["open"], k["high"], k["low"], k["close"], k["volume"]))
        if len(Ks) == 900:
            insert(Ks)
            Ks = []
    insert(Ks)


def insert(Ks):
    if len(Ks) > 0:
        sql = "INSERT INTO StockKD VALUES "
        for k in Ks:
            sql += "('%s','%s',%s,%s,%s,%s,%s)," % (k[0], k[1], k[2], k[3], k[4], k[5], k[6])
        sql = sql.strip(",") + ";"

        dal.mssql.run(sql)
    print("INSERT %d" % len(Ks))