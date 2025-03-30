# -*- coding: utf-8 -*-

import time
from datetime import datetime
import config
import option.akshare_collecter

def collect():
    """定义定时调用采集程序的函数
    """
    global __isRunning
    while __isRunning:
        now  = datetime.now()
        try:
            option.akshare_collecter.collect("http://10.10.10.17:5000", ["sz159915"], [option.get_etf_option_expire_day()[0][0:4]])
            print(now, end="开始,耗时(微秒):")
            print((datetime.now() - now).microseconds)
        except Exception as e:
            print(f"发生未知错误: {e}")
            print(f"！！！静默一个周期！！！")
            time.sleep(config.collectionInterval)
        # 等待一定时间后再次调用采集程序
        time.sleep(config.collectionInterval)

__isRunning = True
collect()
