# -*- coding: utf-8 -*-
import os
import time
import pandas as pd
from typing import Tuple, List, Dict

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
__tabs: Tuple = ('sh510500', 'sz159915', 'sh588000', 'sh510300', 'sh510050')
__name: Tuple = ('中证500 ', ' 创业板 ', ' 科创50 ', '沪深300 ', ' 上证50 ')

# 当前选中的标签
__tabIndex: int = 0

# 当前需要呈现的数据
__renderData: Dict[str, pd.DataFrame] = {}

# 标签列表
__groups: List = []

# 当前选中的分组
__groupIndex: int = 0


def render(tabMovement: int = 0, groupMovement: int = 0):
    """呈现数据面板
    """
    global __tabs, __name, __tabIndex, __renderData, __groups, __groupIndex
    # 清空控制台输出
    if os.name == 'nt':
        os.system('cls')
    elif os.name == 'posix':
        os.system('clear')
    else:
        raise Exception('操作系统异常')

    #
    tabIndex = __tabIndex + tabMovement
    if tabIndex < 0:
        __tabIndex = len(__tabs) - 1
    elif tabIndex >= len(__tabs):
        __tabIndex = 0
    else:
        __tabIndex = tabIndex
    underlying = __tabs[__tabIndex]
    # 获取tab对应的数据
    if underlying not in __allRenderData.keys():
        __allRenderData[underlying] = render_data.calculate(
            underlying, __allPrice)
    __renderData = __allRenderData[underlying]
    __groups = __renderData['到期'].drop_duplicates().values

    #
    groupIndex = __groupIndex + groupMovement
    if groupIndex < 0:
        __groupIndex = len(__groups) - 1
    elif groupIndex >= len(__groups):
        __groupIndex = 0
    else:
        __groupIndex = groupIndex

    # 控制台尺寸
    terminalSize = os.get_terminal_size()

    # 输出tab bar
    for tabIndex, tab in enumerate(__tabs):
        tabBar = '| {} |' if tabIndex != __tabIndex else '\033[1m\033[7m\033[30m| {} |\033[0m'
        print(tabBar.format(tab), end='')
    print('')

    # 输出tab bar name
    for tabIndex, tab in enumerate(__name):
        tabBar = '| {} |' if tabIndex != __tabIndex else '\033[1m\033[7m\033[30m| {} |\033[0m'
        print(tabBar.format(tab), end='')
    print('')

    # 输出分割线
    for tabIndex in range(terminalSize.columns):
        print('^', end='')
    print('')

    print(__renderData[__renderData['到期'] == __groups[__groupIndex]])

    # 输出分割线
    for tabIndex in range(terminalSize.columns):
        print('^', end='')
    print('')

    # 输出group
    for groupIndex, group in enumerate(__groups):
        groupBar = ' >>>{}<<< ' if groupIndex != __groupIndex else '\033[1m\033[7m\033[30m >>>{}<<< \033[0m'
        print(groupBar.format(group), end='')
    print('')


def collect():
    global __collectTime, __allPrice, __allRenderData, __tabs, __tabIndex
    __collectTime = time.localtime()
    # print(time.strftime('%Y-%m-%d %H:%M:%S', __collectTime))
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
