# -*- coding: utf-8 -*-
import pandas as pd
import akshare as ak
from crawler import sina_option
from typing import List


def get_symbol_mark() -> pd.DataFrame:
    return ak.futures_symbol_mark()


def get_spot(symbol) -> pd.DataFrame:
    df = ak.futures_zh_realtime(symbol)
    #print(df)
    field_list = [
        'symbol',
        'exchange',
        'name',
        '最近成交价',
        '结算价',
        '昨日结算价',
        '今日开盘价',
        '最高成交价',
        '最低成交价',
        'close',
        '买价位一',
        '卖价位一',
        '买数量一',
        '卖数量一',
        '成交量',
        '持仓量',
        '行情时间',
        '行情日期',
        'preclose',
        '涨幅',
        'bid',
        'ask',
        'prevsettlement'
    ]
    df.columns = field_list
    return df


