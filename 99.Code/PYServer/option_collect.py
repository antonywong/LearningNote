#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from datetime import datetime
from config import trading_day
import config
import stock
import option

def collect():
    """定义定时调用采集程序的函数
    """
    global __isRunning
    while __isRunning:
        now  = datetime.now()
        try:
            option.collect(underlyings=[], expire_months=[trading_day.get_etf_option_expire_day()[0][0:4]])
            print(now, end="开始,耗时(微秒):")
            print((datetime.now() - now).microseconds)
        except Exception as e:
            print(f"发生未知错误: {e}")
            print(f"！！！静默一个周期！！！")
            time.sleep(config.collectionInterval)
        # 等待一定时间后再次调用采集程序
        time.sleep(config.collectionInterval)

#print('测试')
#stock.collect(stock.collect([y for x in option.UNDERLYING for y in x['etf']]))
#option.collect(underlyings=[], expire_months=[trading_day.get_etf_option_expire_day()[0][0:4]])

__isRunning = True
collect()
