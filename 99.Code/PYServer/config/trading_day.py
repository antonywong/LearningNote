#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from dal import mssql


def get_last() -> datetime:
    day = datetime.now() - timedelta(hours=15)

    sql = f"SELECT TOP(1) day FROM TradingDay WHERE day<='{day.year}-{day.month:02d}-{day.day:02d}' ORDER BY day DESC"
    lastDay = mssql.queryAll(sql)[0]['day']

    sql = f"SELECT MAX(day) AS max, COUNT(0) AS count FROM TradingDay WHERE day>='{lastDay}'"
    max = mssql.queryAll(sql)[0]
    maxDay = max['max']
    dayCount = max['count']

    sql = []
    for i in range(dayCount, 300):
        maxDay = maxDay + timedelta(days=1)
        if maxDay.isoweekday() in (6, 7):
            continue
        sql.append(f"INSERT INTO TradingDay (day) VALUES ('{maxDay}');")
    mssql.run(sql)

    return day