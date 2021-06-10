#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dal


def insert(Ks, kType = "D"):
    if len(Ks) != 0:
        sql = "INSERT INTO StockK%s (code,day,open,high,low,close,volume) VALUES " % kType
        for k in Ks:
            sql += "('%s','%s',%s,%s,%s,%s,%s)," % (k[0], k[1], k[2], k[3], k[4], k[5], k[6])
        sql = sql.strip(",") + ";"

        dal.run(sql)
    print("INSERT %d" % len(Ks))