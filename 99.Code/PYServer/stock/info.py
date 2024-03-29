#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

from dal import mssql
from crawler import sina_common


def syn(codes: List[str] = []):

    if len(codes) == 0:
        sql = "SELECT code FROM Stock ORDER BY updateDate"
        data = mssql.queryAll(sql)
        codes = [d['code'] for d in data]
    getStockInfo(codes)


def getStockInfo(codes):
    df = sina_common.get_stock_spot(codes)
    # print(df)

    update_sql = "UPDATE Stock SET name='%s' WHERE code='%s';"
    sqls = []
    for i, row in df.iterrows():
        if row['证券简称']:
            sqls.append(update_sql % (row['证券简称'], codes[i]))
            print("更新名称--", codes[i], "--", row['证券简称'])

    mssql.run(sqls)
