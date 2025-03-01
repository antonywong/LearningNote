# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from typing import List
from dal import mssql


def __get_last_date() -> datetime:
    day = datetime.now() - timedelta(hours=9, minutes=30)

    sql = f"SELECT TOP(1) day,pre_trading_updated,after_trading_updated FROM TradingDay WHERE day<='{day.year}-{day.month:02d}-{day.day:02d}' ORDER BY day DESC"
    return mssql.queryAll(sql)[0]


def get_last() -> datetime:
    lastDay = __get_last_date()['day']

    sql = f"SELECT MAX(day) AS max, COUNT(0) AS count FROM TradingDay WHERE day>='{lastDay}'"
    max = mssql.queryAll(sql)[0]
    maxDay = datetime.strptime(max['max'], "%Y-%m-%d")
    dayCount = max['count']

    sql = []
    for i in range(dayCount, 100):
        maxDay = maxDay + timedelta(days=1)
        if maxDay.isoweekday() in (6, 7):
            continue
        sql.append(f"INSERT INTO TradingDay (day) VALUES ('{maxDay}');")
    mssql.run(sql)

    return datetime.strptime(lastDay, "%Y-%m-%d")


def is_pre_trading_updated() -> bool:
    return __get_last_date()['pre_trading_updated'] == 1


def is_after_trading_updated() -> bool:
    minute = datetime.now().hour * 100 + datetime.now().minute
    return __get_last_date()['after_trading_updated'] == 1 or minute < 1530


def update_pre_trading() -> bool:
    lastDay = __get_last_date()['day']
    sql = [f"UPDATE TradingDay SET pre_trading_updated=1 WHERE day<='{lastDay}'"]
    mssql.run(sql)


def update_after_trading() -> bool:
    lastDay = __get_last_date()['day']
    sql = [f"UPDATE TradingDay SET after_trading_updated=1 WHERE day<='{lastDay}'"]
    mssql.run(sql)


def is_trading_day() -> bool:
    day = datetime.now()
    sql = f"SELECT COUNT(0) AS C FROM TradingDay WHERE day='{day.year}-{day.month:02d}-{day.day:02d}'"
    return mssql.queryAll(sql)[0]["C"] > 0


def is_trading_time() -> bool:
    now = datetime.now()
    minute = now.hour * 100 + now.minute
    return is_trading_day() and (930 <= minute and minute < 1130 or 1300 <= minute and minute <= 1500)


def get_etf_option_expire_day() -> List[str]:
    sql = "SELECT DISTINCT expire_month+expire_day AS day FROM OptionCode where '20'+expire_month+expire_day >= FORMAT(GETDATE(),'yyyyMMdd') ORDER BY day"
    return [row["day"] for row in mssql.queryAll(sql)]


