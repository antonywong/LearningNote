# -*- coding: utf-8 -*-

import time
from datetime import datetime
import config
import stock
import option
from option import akshare_collecter
import arbitrage._01, arbitrage._02, arbitrage._03, arbitrage._05
from config import trading_day
from bot import mail

def run():
    """定义定时调用采集程序的函数
    """
    global __isRunning
    while __isRunning:
        print("----", datetime.now())
        option.calculate_index()
        expire_months = [trading_day.get_etf_option_expire_day()[0][0:4]]
        arbitrage._01.run(underlyings=[], expire_months=expire_months)
        arbitrage._02.run(underlyings=[], expire_months=expire_months)
        # arbitrage._03.run(underlyings=["sz159915"], expire_months=expire_months)
        # 等待一定时间后再次调用采集程序
        time.sleep(config.collectionInterval)

# print('测试')
# trading_day.get_etf_option_expire_day()
# stock.volatility("sz399006", datetime.now(), datetime.now())
# stock.collect(["sz399006"], 5, 60)
# option.calculate_index()
# akshare_collecter.get_daily([], [])
# arbitrage._01.run(underlyings=[], expire_months=[trading_day.get_etf_option_expire_day()[0][0:4]], is_test=True)
# arbitrage._02.run(underlyings=[], expire_months=[trading_day.get_etf_option_expire_day()[0][0:4]], is_test=True)
# arbitrage._03.run(underlyings=["sz159915"], expire_months=[trading_day.get_etf_option_expire_day()[0][0:4]])
# arbitrage._05.run()
# mail.send_message("1411038526@qq.com", "测试", "测试")

__isRunning = True
run()
