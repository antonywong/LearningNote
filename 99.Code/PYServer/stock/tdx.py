#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import struct
import os
import config
import dal
import stock


def syn():
    getFiles("sh")
    getFiles("sz")


def getFiles(type):
    d = "%svipdoc/%s/fzline/" % (config.tdxDir, type)
    files = os.listdir(d)
    for f in files:
        getStockK(d + f, f.split(".")[0])


def getStockK(fileName, code):
    sql = "SELECT top(1) CONVERT(CHAR(19),day,25) AS day FROM StockK05 WHERE code='%s' ORDER BY day desc" % code
    ks = dal.mssql.queryAll(sql)
    lastKStr = "1989-01-01 00:00:00"
    if len(ks) != 0:
        lastKStr = ks[0]["day"]
    lastK = datetime.strptime(lastKStr, '%Y-%m-%d %H:%M:%S')
    print(code, lastK)

    ofile = open(fileName, 'rb')
    buf=ofile.read()
    ofile.close()

    kLines = []
    for i in range(int(len(buf) / 32)):
        all = buf[i * 32 : (i + 1) * 32]
        dateOri = struct.unpack('H', all[0:2])
        year = int(dateOri[0] / 2048) + 2004
        month = int(dateOri[0] % 2048 / 100)
        day = dateOri[0] % 2048 % 100
        timeOri = struct.unpack('H', all[2:4])
        hour = int(timeOri[0] / 60)
        minute = timeOri[0] % 60
        now = datetime.strptime("%d-%02d-%02d %02d:%02d:00" % (year, month, day, hour, minute), '%Y-%m-%d %H:%M:%S')

        if now > lastK:
            ope = '%.2f' % struct.unpack('f', all[4:8])[0]
            hig = '%.2f' % struct.unpack('f', all[8:12])[0]
            low = '%.2f' % struct.unpack('f', all[12:16])[0]
            clo = '%.2f' % struct.unpack('f', all[16:20])[0]
            vol = '%d' % struct.unpack('I', all[24:28])[0]
            kLines.append((code, now.strftime("%Y-%m-%d %H:%M:%S"), ope, hig, low, clo, vol))
            if len(kLines) == 900:
                insert(kLines)
                kLines = []
    insert(kLines)


def insert(ks):
    if len(ks) != 0:
        sql = "INSERT INTO StockK05 VALUES "
        for k in ks:
            sql += "('%s','%s',%s,%s,%s,%s,%s)," % (k[0], k[1], k[2], k[3], k[4], k[5], k[6])
        sql = sql.strip(",") + ";"

        dal.mssql.run(sql)
    print(len(ks))