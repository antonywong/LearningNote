# -*- coding: utf-8 -*-
import pandas as pd
import arbitrage as base
import const
import akshare as ak
from datetime import datetime
from typing import List, Dict, Optional, Union
from dal import mssql
from crawler import stock, futures, option


def __private_get_target() -> List[Dict]:
    arbitrageMonth = mssql.queryAll(f"SELECT month,cffex_delivery_day,etf_delivery_day,index_code,etf_code,futures_code_prefix,option_code_prefix FROM ArbitrageMonth")
    return [
        {
            'targetMonth': [am['month'], am['cffex_delivery_day'], am['etf_delivery_day']],
            'targetIndex': [am['index_code'], am['etf_code'], am['futures_code_prefix'], am['option_code_prefix']]
        } for am in arbitrageMonth
    ]


def sync():
    sql = ["DELETE FROM ArbitrageETFOptionInfo"]
    insert_sql = "INSERT INTO ArbitrageETFOptionInfo (Code, is_call, expire_day, underlying) VALUES ('{}', {}, '{}', '{}')"
    update_sql = "UPDATE ArbitrageETFOptionInfo SET strike_price={}*1000 WHERE Code='{}'"
    etf_option_codes = []

    # 保存ETF期权合约基础信息
    for arbitrageMonth in __private_get_target():
        expire_day = '20' + arbitrageMonth['targetMonth'][0] + arbitrageMonth['targetMonth'][2]
        etf_option_info_df = option.get_codes([expire_day], [arbitrageMonth['targetIndex'][1]])
        sql.extend([insert_sql.format(row["code"], row["is_call"], row["expire_day"], row["underlying"]) for index, row in etf_option_info_df.iterrows()])
        etf_option_codes = [row["code"] for index, row in etf_option_info_df.iterrows()]

    # 保存ETF期权合约行权价
    all_price = option.get_price(etf_option_codes)
    sql.extend([update_sql.format(all_price[code].loc[7, "值"], code) for code in etf_option_codes])
    
    mssql.run(sql)


def collect() -> List[List]:
    for arbitrageMonth in __private_get_target():
        price_order = collect_month(arbitrageMonth['targetMonth'], arbitrageMonth['targetIndex'])
        return price_order


def collect_month(targetMonth, targetIndex) -> List[List]:
    # [价位,名称,可做多空,升贴水]
    price_order = []

    # 标的物：指数和ETF
    stock_df = stock.get_spot(targetIndex[0:2])
    print(stock_df)
    idx_val = stock_df.loc[0, '最近成交价']
    etf_val = stock_df.loc[1, '卖价位一']
    price_order.append([expand(idx_val), '指数', '无', 0])
    price_order.append([expand(etf_val, 1000), 'ETF', '多', 0])

    # 股指期货
    futures_code = targetIndex[2] + targetMonth[0]
    futures_df = futures.get_spot('上证50指数期货')
    futures_row = futures_df[futures_df['symbol'] == futures_code].reset_index(drop=True)
    print(futures_row)

    futures_c_price = expand(futures_row.loc[0, '卖价位一'])
    futures_p_price = expand(futures_row.loc[0, '买价位一'])

    price_order.append([futures_c_price, '股指期货', '多', futures_c_price - price_order[0][0]])
    price_order.append([futures_p_price, '股指期货', '空', futures_p_price - price_order[0][0]])

    # 股指期权
    idx_option_type = targetIndex[3] + targetMonth[0]
    idx_option_df = option.get_spot_cffex(idx_option_type)
    idx_option_df['合成做多'] = [expand(row['行权价'] + row['看涨合约-卖价'] - row['看跌合约-买价']) for index, row in idx_option_df.iterrows()]
    idx_option_df['合成做空'] = [expand(row['行权价'] + row['看涨合约-买价'] - row['看跌合约-卖价']) for index, row in idx_option_df.iterrows()]
    print(idx_option_df)

    idx_option_df = idx_option_df.sort_values(by=['合成做多', '看涨合约-持仓量'], ascending=[True, False]).reset_index(drop=True)
    idx_option_c_price = idx_option_df.loc[0, '合成做多']
    idx_option_c_name = idx_option_df.loc[0, '行权价']
    price_order.append([idx_option_c_price, f'股指期权{idx_option_c_name}', '多', idx_option_c_price - price_order[0][0]])

    idx_option_df = idx_option_df.sort_values(by=['合成做空', '看涨合约-持仓量'], ascending=[False, False]).reset_index(drop=True)
    idx_option_p_price = idx_option_df.loc[0, '合成做空']
    idx_option_p_name = idx_option_df.loc[0, '行权价']
    price_order.append([idx_option_p_price, f'股指期权{idx_option_p_name}', '空', idx_option_p_price - price_order[0][0]])

    # ETF期权    
    etf_option_info = mssql.queryAll(f"SELECT code FROM ArbitrageETFOptionInfo")
    etf_option_codes = [x["code"] for x in etf_option_info]
    etf_option_df = option.get_spot(etf_option_codes)
    etf_option_df['合成做多'] = [expand(row['行权价'] + row['看涨合约-卖价'] - row['看跌合约-买价']) for index, row in etf_option_df.iterrows()]
    etf_option_df['合成做空'] = [expand(row['行权价'] + row['看涨合约-买价'] - row['看跌合约-卖价']) for index, row in etf_option_df.iterrows()]
    print(etf_option_df)

    etf_option_df = etf_option_df.sort_values(by=['合成做多', '看涨合约-持仓量'], ascending=[True, False]).reset_index(drop=True)
    etf_option_c_price = etf_option_df.loc[0, '合成做多']
    etf_option_c_name = etf_option_df.loc[0, '行权价']
    price_order.append([etf_option_c_price, f'ETF期权{etf_option_c_name}', '多', etf_option_c_price - price_order[1][0]])

    etf_option_df = etf_option_df.sort_values(by=['合成做空', '看涨合约-持仓量'], ascending=[False, False]).reset_index(drop=True)
    etf_option_p_price = etf_option_df.loc[0, '合成做空']
    etf_option_p_name = etf_option_df.loc[0, '行权价']
    price_order.append([etf_option_p_price, f'ETF期权{etf_option_p_name}', '空', etf_option_p_price - price_order[1][0]])

    print(price_order)
    return price_order

    
def expand(num, rate: int = 1) -> int:
    n = num if num is float else float(num)
    return int(round(n * rate * 10))


def record(price_order: List):
    sql = []
    insert_sql = "INSERT INTO ArbitrageRecord VALUES (getdate(),{},{},{},{},{},{},{},{},{},{},{},{},{},{})"
    sql.append(insert_sql.format(
        price_order[0][0],
        price_order[1][0],
        price_order[2][0],
        price_order[2][3],
        price_order[3][0],
        price_order[3][3],
        price_order[4][0],
        price_order[4][3],
        price_order[5][0],
        price_order[5][3],
        price_order[6][0],
        price_order[6][3],
        price_order[7][0],
        price_order[7][3])
    )
    mssql.run(sql)






