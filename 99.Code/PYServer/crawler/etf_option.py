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


def get_daily(code: str) -> pd.DataFrame:
    """期权日频率数据
    """
    # print(f'crawler.cffex_option.get_daily...', end='')
    return sina_option.option_sse_daily_sina(code)
