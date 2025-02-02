#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from datetime import datetime

import config
import option
import arbitrage._01


def collect():
    """定义定时调用采集程序的函数
    """
    global __isRunning
    while __isRunning:
        print(datetime.now())
        arbitrage._01.collect("sh510500", "20241127")
        # 等待一定时间后再次调用采集程序
        time.sleep(config.analyzeRecordInterval)


__isRunning = True

print('更新基础数据...')
option.update_etf_contract()

collect()

# arbitrage._01.collect("sh510500", "20241127")
