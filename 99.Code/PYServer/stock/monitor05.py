#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from urllib import request
import json
import time
import dal
from dal import mssql
import stock

def syn(isLoop = True):
    con = True
    while con:
        sql = "SELECT code FROM Stock s"
        stocks = dal.queryAll(sql)
        for s in stocks:
            getStockK(s[0])
            time.sleep(1.2)

        stock.k05.syn()
        con = isLoop


def getStockK(code):
    print("爬虫获取五分钟线", code)
    sql = "SELECT top(1) CONVERT(CHAR(19),day,25) AS day FROM StockK05 WHERE code='%s' ORDER BY day desc" % code
    ks = mssql.queryAll(sql)
    lastKStr = "1989-01-01 00:00:00"
    if len(ks) != 0:
        lastKStr = ks[0]["day"]
    lastK = datetime.strptime(lastKStr, '%Y-%m-%d %H:%M:%S')
    url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=5&datalen=240" % code
    with request.urlopen(url) as f:
        data = json.loads(f.read().decode('gb2312'))
        kLines = []
        for kLine in data:
            kTime = datetime.strptime(kLine["day"], '%Y-%m-%d %H:%M:%S')
            if kTime >= lastK:
                kLines.append((code, kLine["day"], kLine["open"], kLine["high"], kLine["low"], kLine["close"], kLine["volume"]))
                lastK = kTime

        if len(kLines) == 0:
            return

        sql = "DELETE FROM StockK05 WHERE code='%s' AND day>=CONVERT(DATETIME,'%s',102)" % (kLines[0][0], kLines[0][1])
        dal.mssql.run(sql)
        stock.tdx.insert(kLines)