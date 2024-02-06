# -*- coding: utf-8 -*-
import pandas as pd
from crawler import sina_option, sina_common
from typing import List


def get_spot(code) -> pd.DataFrame:
    return sina_common.get_stock_spot(code)


def get_contract_month(symbol: str = "50ETF", exchange: str = "null") -> List[str]:
    return sina_option.option_sse_list_sina(symbol, exchange)


def get_expire_day(trade_date) -> List[str]:
    return sina_option.option_sse_expire_day_sina(trade_date)


def get_codes(contract_months, underlying) -> pd.DataFrame:
    return sina_option.option_sse_codes_sina(contract_months, underlying)


def get_price(codes):
    return sina_option.option_sse_spot_price_sina(codes)


def get_underlying_price(code):
    return sina_option.option_sse_underlying_spot_price_sina(code)



