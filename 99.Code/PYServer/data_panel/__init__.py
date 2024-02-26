# -*- coding: utf-8 -*-
import os
import time
import pandas as pd
from typing import Dict, Tuple

from data_panel import option_info, option_price, render_data

__collectTime = None
"""最后一次采集报价的时间
"""

__allPrice: Dict[str, Tuple] = {}
"""所有最新的报价
Dict[编号, (申买价, 申卖价)]
"""

__allRenderData: Dict[str, pd.DataFrame] = {}

# 标签列表
__tabs: Tuple = ('sh510050', 'sh510300', 'sz159915', 'sh588000')
__name: Tuple = (' 上证50 ', '沪深300 ', ' 创业板 ', ' 科创50 ')

# 当前选中的标签
__tabIndex: int = 0


def render(tabMovement: int = 0):
    """呈现数据面板
    """
    global __tabs, __name, __tabIndex
    # 清空控制台输出
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    else:
        raise Exception('操作系统异常')

    #
    i = __tabIndex + tabMovement
    if i < 0:
        __tabIndex = len(__tabs) - 1
    elif i >= len(__tabs):
        __tabIndex = 0
    else:
        __tabIndex = i

    # 控制台尺寸
    terminalSize = os.get_terminal_size()

    # 输出tab bar
    for i, tab in enumerate(__tabs):
        tabBar = '| {} |' if i != __tabIndex else '\033[1m\033[7m\033[30m| {} |\033[0m'
        print(tabBar.format(tab), end='')
    print('')

    # 输出tab bar name
    for i, tab in enumerate(__name):
        tabBar = '| {} |' if i != __tabIndex else '\033[1m\033[7m\033[30m| {} |\033[0m'
        print(tabBar.format(tab), end='')
    print('')

    # 输出分割线
    for i in range(terminalSize.columns):
        print('^', end='')
    print('')

    # 输出采集结果
    underlying = __tabs[__tabIndex]
    if underlying not in __allRenderData.keys():
        __allRenderData[underlying] = render_data.calculate(underlying, __allPrice)
    print(__allRenderData[underlying])


def collect():
    global __collectTime, __allPrice, __allRenderData, __tabs, __tabIndex
    __collectTime = time.localtime()
    print(time.strftime('%Y-%m-%d %H:%M:%S', __collectTime))
    current_min = __collectTime.tm_hour * 100 + __collectTime.tm_min
    if (__collectTime.tm_wday < 5 and
        (930 < current_min and current_min <= 1130
         or 1300 <= current_min and current_min < 1457)) or __allPrice == {}:
        __allPrice.update(option_price.get_etf_option_price())
        __allPrice.update(option_price.get_cffex_option_price())
        __allPrice.update(option_price.get_index_price())
        __allPrice.update(option_price.get_etf_price())
        __allRenderData.clear()
    underlying = __tabs[__tabIndex]
    __allRenderData[underlying] = render_data.calculate(underlying, __allPrice)


def update_option_info() -> str:
    data = []
    data.extend(option_info.get_etf_option_info())
    data.extend(option_info.get_cffex_option_info())
    option_info.update_database(data)
    return ''
