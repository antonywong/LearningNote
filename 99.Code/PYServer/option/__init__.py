# -*- coding: utf-8 -*-

from typing import List
from decimal import Decimal
import stock
from config import trading_day
from option import _core, akshare_collecter

UNDERLYING = [
    {"index":"sh000016","etf":["sh510050"],"cffex":"ho"},             # 上证50
    {"index":"sh000688","etf":["sh588000","sh588080"],"cffex":""},    # 科创50
    {"index":"sz399330","etf":["sz159901"],"cffex":""},               # 深证100
    {"index":"sz399006","etf":["sz159915"],"cffex":""},               # 创业板
    {"index":"sz399300","etf":["sh510300","sz159919"],"cffex":"io"},  # 沪深300
    {"index":"sz399905","etf":["sh510500","sz159922"],"cffex":""},    # 中证500
    {"index":"sz399852","etf":[],"cffex":"mo"}                        # 中证1000指数
]

STACK_COMMISSION_RATE = 0.00008
OPTION_COMMISSION = 2
OPTION_STRIKE_COMMISSION = 1
OPTION_MARGIN = 5000
OPTION_MARGIN_RATE = 1.1

STOCK_COLLECTER = stock
OPTION_COLLECTER = akshare_collecter


def GET_UNDERLYING_INDEX(etf: str) -> str:
    for u in UNDERLYING:
        if etf in u["etf"]:
            return u["index"]
    return ""


def collect(underlyings: List[str] = [], expire_months: List[str] = []):
    # 盘前数据更新
    if not trading_day.is_pre_trading_updated():
        OPTION_COLLECTER.update_etf_contract()
        trading_day.update_pre_trading()

    # 盘后数据更新
    if not trading_day.is_after_trading_updated():
        OPTION_COLLECTER.get_daily([], expire_months)
        stock_codes = [y for x in UNDERLYING for y in x["etf"]]
        stock_codes.extend([x["index"]for x in UNDERLYING])
        STOCK_COLLECTER.collect(stock_codes)
        trading_day.update_after_trading()

    if trading_day.is_trading_time():
        OPTION_COLLECTER.collect([], expire_months)
        stock_codes = list(set(GET_UNDERLYING_INDEX(u) for u in underlyings)) if len(underlyings) > 0 else [u["index"] for u in UNDERLYING]
        STOCK_COLLECTER.collect(stock_codes, 5)


def calculate_index():
    return _core.calculate_index()


def get_option_code(underlying: str, expire_month: str) ->  List[str]:
    return _core.get_option_code(underlying, expire_month)


def get_strike_price_etf(underlying_price: float, need_secondary: bool = False):
    return _core.get_strike_price_etf(underlying_price, need_secondary)


def get_seller_holding_cost(is_call: bool, underlying_price: Decimal, strike_price: Decimal) -> Decimal:
    return _core.get_seller_holding_cost(is_call, underlying_price, strike_price)
