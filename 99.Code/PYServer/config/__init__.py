# -*- coding: utf-8 -*-

import os


# SQL Server连接字符串参数
mssqlConnStr = (
    os.getenv("MSSQL_HOST", "192.168.2.42"),
    os.getenv("MSSQL_USER", "sa"),
    os.getenv("MSSQL_PASSWORD", "sql@0512"),
    os.getenv("MSSQL_DB", "CH_Stock")
    )

# 自动采集数据的时间间隔（秒）
collectionInterval = 30

sqliteFile = "Z:/StockTool.db"


## trading_day缓存
# 缓存-当前的最后一个交易日
CACHE_LAST_TRADING_DAY = { "day": None, "pre_trading_updated": None, "after_trading_updated": None }
# 缓存-当前的下一个交易日
CACHE_NEXT_TRADING_DAY = { "day": None, "pre_trading_updated": None, "after_trading_updated": None }
# 缓存-当前的ETF期权到期日
CACHE_ETF_OPTION_EXPIRE_DAY = []


