# -*- coding: utf-8 -*-
import os
import option as op
from crawler import etf_option as etf_op_crawler, cffex_option as cffex_op_crawler
from dal import mssql

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


def update_option_info():
    update_etf_option_info()
    update_cffex_option_info()


def update_etf_option_info():
    contract_month = etf_op_crawler.get_contract_month()
    expire_day = list(
        map(lambda x: etf_op_crawler.get_expire_day(x)[0].replace("-", ""),
            contract_month))
    underlyings = []
    for x in op.UNDERLYING:
        underlyings.extend(x['etf'])
    optionInfo = etf_op_crawler.get_codes(expire_day, underlyings)

    codes = optionInfo['code'].values.tolist()
    all_price = etf_op_crawler.get_price(codes)

    sql = ["DELETE FROM OptionInfo"]
    insert_sql = "INSERT INTO OptionInfo (Code,is_call,expire_day,underlying,strike_price) VALUES ('{}', {}, '{}', '{}',{}*1000)"
    sql.extend([
        insert_sql.format(row["code"], row["is_call"], row["expire_day"],
                          row["underlying"], all_price[row["code"]].loc[7, "值"])
        for index, row in optionInfo.iterrows()
    ])
    mssql.run(sql)


def update_cffex_option_info():
    contract_month = cffex_op_crawler.get_contract_month()

    # expire_day = list(
    #     map(lambda x: etf_op_crawler.get_expire_day(x)[0].replace("-", ""),
    #         contract_month))
    # underlyings = []
    # for x in op.UNDERLYING:
    #     underlyings.extend(x['etf'])
    # optionInfo = etf_op_crawler.get_codes(expire_day, underlyings)

    # codes = optionInfo['code'].values.tolist()
    # all_price = etf_op_crawler.get_price(codes)

    # sql = ["DELETE FROM OptionInfo"]
    # insert_sql = "INSERT INTO OptionInfo (Code,is_call,expire_day,underlying,strike_price) VALUES ('{}', {}, '{}', '{}',{}*1000)"
    # sql.extend([
    #     insert_sql.format(row["code"], row["is_call"], row["expire_day"],
    #                       row["underlying"], all_price[row["code"]].loc[7, "值"])
    #     for index, row in optionInfo.iterrows()
    # ])
    # mssql.run(sql)
