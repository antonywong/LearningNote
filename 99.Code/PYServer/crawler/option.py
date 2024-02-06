# -*- coding: utf-8 -*-
import pandas as pd
import akshare as ak
from crawler import sina_option
from typing import List
from dal import mssql


def get_contract_month(symbol: str = "50ETF", exchange: str = "null") -> List[str]:
    return sina_option.option_sse_list_sina(symbol, exchange)


def get_expire_day(trade_date) -> List[str]:
    return sina_option.option_sse_expire_day_sina(trade_date)


def get_codes(expire_days: List[str], underlyings: List[str]) -> pd.DataFrame:
    return sina_option.option_sse_codes_sina(expire_days, underlyings)


def get_price(codes):
    return sina_option.option_sse_spot_price_sina(codes)


def get_underlying_price(code):
    return sina_option.option_sse_underlying_spot_price_sina(code)


def get_spot_cffex(code: str) -> pd.DataFrame:
    code_type = code[0:2].upper()
    if code_type == 'HO':
        return ak.option_cffex_sz50_spot_sina(code)
    elif  code_type == 'IO':
        return ak.option_cffex_hs300_spot_sina(code)
    elif  code_type == 'MO':
        return ak.option_cffex_zz1000_spot_sina(code)
    else:
        return None


def get_spot(etf_option_codes: List[str]) -> pd.DataFrame:
    all_price = get_price(etf_option_codes)
    #print(all_price)

    result = []
    option_info = mssql.queryAll(f"SELECT underlying, expire_day, strike_price, is_call, code FROM ArbitrageETFOptionInfo ORDER BY underlying, expire_day, strike_price, is_call")
    for i in range(0, len(option_info), 2):
        call = all_price[option_info[i + 1]["code"]]
        put = all_price[option_info[i]["code"]]
        result.append({
            "标的": option_info[i]["underlying"],
            "到期日": option_info[i]['expire_day'],
            "行权价": option_info[i]['strike_price'],
            "看涨合约-代码": option_info[i + 1]["code"],
            "看涨合约-买价": float(call.loc[1, "值"]) * 1000,
            "看涨合约-卖价": float(call.loc[3, "值"]) * 1000,
            "看涨合约-持仓量": int(call.loc[5, "值"]),
            "看跌合约-代码": option_info[i]["code"],
            "看跌合约-买价": float(put.loc[1, "值"]) * 1000,
            "看跌合约-卖价": float(put.loc[3, "值"]) * 1000
        })

    return pd.DataFrame(result)