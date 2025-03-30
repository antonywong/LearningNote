# -*- coding: utf-8 -*-

import json
import numpy as np
from scipy import stats
from datetime import datetime, date
from decimal import Decimal
from scipy import stats
from typing import List
from dal import mssql
import config
from config import trading_day
import option
from option import _core
import stock
import threading
import time

# 状态机控制变量
is_running = False
cache = []
cache_lock = threading.Lock()
processing_lock = threading.Lock()


def save_tick(time: datetime, underlying: str, underlying_price: float, expire_month: str, data: dict):
    global is_running, cache
    
    if 1457 <= time.hour * 100 + time.minute < 1500:
        return

    with cache_lock:
        cache.append((time, underlying, underlying_price, expire_month, data))
        
    if not is_running:
        with processing_lock:
            if not is_running:  # 双重检查锁定
                is_running = True
                # 启动异步处理线程
                threading.Thread(target=__process_data).start()

def __process_data():
    global is_running, cache
    while True:
        with cache_lock:
            if not cache:
                is_running = False
                break
            current_batch = cache.copy()
            cache.clear()
        
        # 实际处理逻辑（原save_tick中的业务）
        for data in current_batch:
            __save_tick(data)
        
        time.sleep(0.001)  # 防止CPU空转

def __save_tick(tick_data):
    time = tick_data[0]
    underlying = tick_data[1]
    underlying_price = round(tick_data[2], 6)
    expire_month = tick_data[3]
    data = tick_data[4]

    cache_key = (underlying, expire_month)
    if cache_key in config.CACHE_LATEST_OPTION_PRICE.keys() and config.CACHE_LATEST_OPTION_PRICE[cache_key]["time"] >= time:
        return
    
    v = float(stock.volatility(option.GET_UNDERLYING_INDEX(underlying))) # 历史波动率
    codes = sorted(data.keys())
    sorted_data = {}
    option_codes = option.get_option_info(codes)
    days = (date(int("20" + expire_month[0:2]), int(expire_month[2:4]), int(option_codes[0]["expire_day"])) - time.date()).days + 1
    contracts = {row["code"]: row for row in option_codes}
    for code in codes:
        c = contracts[code]
        d = data[code]
        # d[2] 以最新成交价计算各类指标
        #d[2] = _core.calculate_index(float(underlying_price), float(c["strike_price"]), days, d[2][0], c["is_call"])
        #d[2][4] = v # 历史波动率
        # d[3] 以买一卖一平均价计算各类指标
        d[3] = _core.calculate_index(float(underlying_price), float(c["strike_price"]), days, d[3][0], c["is_call"])
        d[3][4] = v # 历史波动率
        sorted_data[code] = d

    para = (time, underlying, underlying_price, expire_month, json.dumps(sorted_data, separators=(',', ':')))
    insert_sql = ["INSERT INTO OptionPrice (time,underlying,underlying_price,expire_month,data) VALUES ('%s','%s','%s','%s','%s')" % para]
    mssql.run(insert_sql)

    cache_value = {"time": time, "underlying": underlying, "underlying_price": underlying_price, "expire_month": expire_month, "data": data}
    config.CACHE_LATEST_OPTION_PRICE[cache_key] = cache_value

