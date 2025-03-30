# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import config
from dal import mssql

START_HOUR = 9
START_MINUTE = 15

def __get_last_trading_day() -> dict:
    global START_HOUR, START_MINUTE
    now = (datetime.now() - timedelta(hours=START_HOUR, minutes=START_MINUTE)).strftime("%Y-%m-%d")

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


def get_last() -> str:
    last_day = __get_last_trading_day()['day']
    return last_day


def is_pre_trading_updated() -> bool:
    return __get_last_trading_day()['pre_trading_updated']


def is_after_trading_updated() -> bool:
    global START_HOUR, START_MINUTE
    start_minute = START_HOUR * 100 + START_MINUTE
    minute = datetime.now().hour * 100 + datetime.now().minute
    return __get_last_trading_day()['after_trading_updated'] or (start_minute < minute < 1530)


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

