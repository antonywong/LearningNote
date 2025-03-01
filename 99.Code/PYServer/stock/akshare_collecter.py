# # -*- coding: utf-8 -*-

import time
from typing import List
from dal import mssql
from crawler import stock as stock_crawler


def collect(codes: List[str], scale: int, datalen: int):
    for i, code in enumerate(codes):
        time.sleep(3)

        print("%s/%s:" % (i + 1, len(codes)), end="")    
        ks = stock_crawler.get_k(code, scale, datalen)
        sql = ["DELETE FROM StockK WHERE type=%s AND code='%s' AND day=CONVERT(DATETIME,'%s',102)" % (scale, code, row["day"]) for i, row in ks.iterrows()]
        sql.extend(["INSERT INTO StockK (type,code,day,[open],high,low,[close],volume) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"
                    % (scale, code, row["day"], row["open"], row["high"], row["low"], row["close"], row["volume"])
                    for i, row in ks.iterrows()])
        mssql.run(sql)
        print("K线数量%s" % int(len(sql) / 2))
    
