# -*- coding: utf-8 -*-
from typing import Dict, Tuple

import option as op
from crawler import (etf_option as etf_op_crawler, index as index_crawler,
                     cffex_option as cffex_op_crawler, stock as stock_crawler)
from dal import mssql


def get_etf_option_price() -> Dict[str, Tuple]:
    sql = 'SELECT code FROM OptionInfo WHERE LEN(code)=8'
    op_infos = mssql.queryAll(sql)
    codes = [x['code'] for x in op_infos]
    all_price = etf_op_crawler.get_price(codes)
    return {
        k: (float(v.loc[22, "值"]), float(v.loc[20, "值"]))
        for k, v in all_price.items()
    }


def get_cffex_option_price() -> Dict[str, Tuple]:
    sql = 'SELECT DISTINCT LEFT(code,6) AS code FROM OptionInfo WHERE LEN(code)=11'
    op_infos = mssql.queryAll(sql)
    codes = [x['code'] for x in op_infos]
    result = {}
    for code in codes:
        all_price = cffex_op_crawler.get_price(code)
        for i, row in all_price.iterrows():
            result[row["看涨合约-标识"]] = (row["看涨合约-买价"], row["看涨合约-卖价"])
            result[row["看跌合约-标识"]] = (row["看跌合约-买价"], row["看跌合约-卖价"])
    return result


def get_index_price() -> Dict[str, Tuple]:
    index_list = [x['index'] for x in op.UNDERLYING if x['cffex'] != '']
    all_price = index_crawler.get_price()

    result = {}
    for i in index_list:
        price = float(all_price.loc[all_price['代码'] == i, '最新价'].values[0])
        result[i] = (price, price)
    return result


def get_etf_price() -> Dict[str, Tuple]:
    etf_list = [y for x in op.UNDERLYING if x['etf'] != [] for y in x['etf']]
    all_price = stock_crawler.get_price(etf_list)
    return {
        x: (float(all_price.loc[i, '买价位一']), float(all_price.loc[i, '卖价位一']))
        for i, x in enumerate(etf_list)
    }
