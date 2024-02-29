# -*- coding: utf-8 -*-
import pandas as pd
from typing import List, Dict
from crawler import sina_option


def get_contract_month() -> List[str]:
    """ETF期权合约到期月份列表
    """
    # print('crawler.etf_option.get_contract_month...', end='')
    return sina_option.option_sse_list_sina()


def get_expire_day(trade_month) -> List[str]:
    """指定到期月份指定品种的剩余到期时间
    """
    # print('crawler.etf_option.get_expire_day...', end='')
    return sina_option.option_sse_expire_day_sina(trade_month)


def get_codes(expire_days: List[str], underlyings: List[str]) -> pd.DataFrame:
    """所有看涨和看跌合约的代码
    """
    # print('crawler.etf_option.get_codes...', end='')
    return sina_option.option_sse_codes_sina(expire_days, underlyings)


def get_price(codes: List[str]) -> Dict[str, pd.DataFrame]:
    """期权实时数据
    """
    # print(f'crawler.etf_option.get_price...{len(codes)}...', end='')
    return sina_option.option_sse_spot_price_sina(codes)
    


# def get_spot(etf_option_codes: List[str]) -> pd.DataFrame:
#     all_price = get_price(etf_option_codes)
#     #print(all_price)

#     result = []
#     option_info = mssql.queryAll(f"SELECT underlying, expire_day, strike_price, is_call, code FROM ArbitrageETFOptionInfo ORDER BY underlying, expire_day, strike_price, is_call")
#     for i in range(0, len(option_info), 2):
#         call = all_price[option_info[i + 1]["code"]]
#         put = all_price[option_info[i]["code"]]
#         result.append({
#             "标的": option_info[i]["underlying"],
#             "到期日": option_info[i]['expire_day'],
#             "行权价": option_info[i]['strike_price'],
#             "看涨合约-代码": option_info[i + 1]["code"],
#             "看涨合约-买价": float(call.loc[1, "值"]) * 1000,
#             "看涨合约-卖价": float(call.loc[3, "值"]) * 1000,
#             "看涨合约-持仓量": int(call.loc[5, "值"]),
#             "看跌合约-代码": option_info[i]["code"],
#             "看跌合约-买价": float(put.loc[1, "值"]) * 1000,
#             "看跌合约-卖价": float(put.loc[3, "值"]) * 1000
#         })

#     return pd.DataFrame(result)
