# -*- coding: utf-8 -*-
import os
import time

from data_panel import option_info, option_price

# 标签列表
__tabs = ('common', 'other1', 'other2')

# 当前选中的标签
__tabIndex = 0


def rander(tabMovement: int = 0):
    """呈现数据面板
    """
    global __tabs, __tabIndex
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

    # 输出分割线
    for i in range(terminalSize.columns):
        print('^', end='')
    print('')

    # 输出采集结果
    print(__tabIndex)


def collect(collect_time: str):
    print(collect_time)
    # option_price = {}
    # option_price.update(option_price.get_etf_option_price())
    # option_price.update(option_price.get_cffex_option_price())
    underlying_price = {}
    # underlying_price.update(option_price.get_index_price())
    underlying_price.update(option_price.get_etf_price())
    print(underlying_price)

def update_option_info():
    data = []
    data.extend(option_info.get_etf_option_info())
    data.extend(option_info.get_cffex_option_info())
    option_info.update_database(data)
