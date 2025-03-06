# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from typing import List
import config
from dal import mssql


def __get_last_trading_day():
    now = (datetime.now() - timedelta(hours=9, minutes=30)).strftime("%Y-%m-%d")

    if not config.CACHE_NEXT_TRADING_DAY["day"] or config.CACHE_NEXT_TRADING_DAY["day"] <= now:
        """填充新的TradingDay"""
        sql = f"SELECT MAX(day) AS max, COUNT(0) AS count FROM TradingDay WHERE day>='{now}'"
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

        """获取今明两天"""
        sql = f"""
SELECT TOP(1) day,pre_trading_updated,after_trading_updated FROM TradingDay WHERE day<='{now}'
UNION
SELECT day,pre_trading_updated,after_trading_updated FROM TradingDay WHERE day>'{now}'
ORDER BY day"""
        days = mssql.queryAll(sql)
        config.CACHE_LAST_TRADING_DAY = days[0]
        config.CACHE_NEXT_TRADING_DAY = days[1]

    return config.CACHE_LAST_TRADING_DAY


def get_last() -> datetime:
    last_day = __get_last_trading_day()['day']
    return datetime.strptime(last_day, "%Y-%m-%d")


def is_pre_trading_updated() -> bool:
    return __get_last_trading_day()['pre_trading_updated'] == 1


def is_after_trading_updated() -> bool:
    minute = datetime.now().hour * 100 + datetime.now().minute
    return __get_last_trading_day()['after_trading_updated'] == 1 or minute < 1530


def update_pre_trading() -> bool:
    last_day = __get_last_trading_day()
    last_day["pre_trading_updated"] = True
    sql = [f"UPDATE TradingDay SET pre_trading_updated=1 WHERE day<='{last_day['day']}'"]
    mssql.run(sql)


def update_after_trading() -> bool:
    last_day = __get_last_trading_day()
    last_day["after_trading_updated"] = True
    sql = [f"UPDATE TradingDay SET after_trading_updated=1 WHERE day<='{last_day['day']}'"]
    mssql.run(sql)


def is_trading_time() -> bool:
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    last_day = __get_last_trading_day()["day"]
    minute = now.hour * 100 + now.minute
    return last_day == today and (930 <= minute and minute < 1130 or 1300 <= minute and minute <= 1500)


def get_etf_option_expire_day() -> List[str]:
    last_day = __get_last_trading_day()["day"].replace('-', '')

    if len(config.CACHE_ETF_OPTION_EXPIRE_DAY) == 0 or config.CACHE_ETF_OPTION_EXPIRE_DAY[0] < last_day:
        sql = "SELECT DISTINCT expire_month+expire_day AS day FROM OptionCode where '20'+expire_month+expire_day >= FORMAT(GETDATE(),'yyyyMMdd') ORDER BY day"
        config.CACHE_ETF_OPTION_EXPIRE_DAY = [row["day"] for row in mssql.queryAll(sql)]

    return config.CACHE_ETF_OPTION_EXPIRE_DAY


