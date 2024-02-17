# -*- coding: utf-8 -*-
import requests
import pandas as pd


def get_price() -> pd.DataFrame:
    df1 = stock_zh_index_spot_em("上证系列指数")
    df2 = stock_zh_index_spot_em("指数成份")
    return pd.concat([df1, df2])


def stock_zh_index_spot_em(symbol: str = "上证系列指数") -> pd.DataFrame:
    """
    东方财富网-行情中心-沪深京指数
    https://quote.eastmoney.com/center/gridlist.html#index_sz
    :param symbol: "上证系列指数"; choice of {"上证系列指数", "深证系列指数", "指数成份", "中证系列指数"}
    :type symbol: str
    :return: 指数的实时行情数据
    :rtype: pandas.DataFrame
    """
    url = "https://48.push2.eastmoney.com/api/qt/clist/get"
    symbol_map = {
        "上证系列指数": "m:1 s:2",
        "深证系列指数": "m:0 t:5",
        "指数成份": "m:1 s:3,m:0 t:5",
        "中证系列指数": "m:2",
    }
    params = {
        'pn': '1',
        'pz': '5000',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'wbp2u': '|0|0|0|web',
        'fid': 'f3',
        'fs': symbol_map[symbol],
        'fields':
        'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152',
        '_': '1704327268532',
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.reset_index(inplace=True)
    temp_df['index'] = temp_df['index'] + 1
    temp_df.rename(columns={
        'index': '序号',
        'f2': '最新价',
        'f3': '涨跌幅',
        'f4': '涨跌额',
        'f5': '成交量',
        'f6': '成交额',
        'f7': '振幅',
        'f10': '量比',
        'f12': '代码',
        'f14': '名称',
        'f15': '最高',
        'f16': '最低',
        'f17': '今开',
        'f18': '昨收',
    },
                   inplace=True)
    temp_df = temp_df[[
        '序号',
        '代码',
        '名称',
        '最新价',
        '涨跌幅',
        '涨跌额',
        '成交量',
        '成交额',
        '振幅',
        '最高',
        '最低',
        '今开',
        '昨收',
        '量比',
    ]]
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors="coerce")
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors="coerce")
    temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'], errors="coerce")
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'], errors="coerce")
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'], errors="coerce")
    temp_df['振幅'] = pd.to_numeric(temp_df['振幅'], errors="coerce")
    temp_df['最高'] = pd.to_numeric(temp_df['最高'], errors="coerce")
    temp_df['最低'] = pd.to_numeric(temp_df['最低'], errors="coerce")
    temp_df['今开'] = pd.to_numeric(temp_df['今开'], errors="coerce")
    temp_df['昨收'] = pd.to_numeric(temp_df['昨收'], errors="coerce")
    temp_df['量比'] = pd.to_numeric(temp_df['量比'], errors="coerce")
    return temp_df
