# -*- coding: utf-8 -*-

from typing import List
from datetime import datetime
from decimal import Decimal
from option import _core, _core_tick_task

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


def GET_UNDERLYING_INDEX(etf: str) -> str:
    for u in UNDERLYING:
        if etf in u["etf"]:
            return u["index"]
    return ""


def save_tick(time: datetime, underlying: str, underlying_price: float, expire_month: str, data: dict):
    return _core_tick_task.save_tick(time, underlying, underlying_price, expire_month, data)


def recalculate_k_index():
    return _core.recalculate_k_index()


def get_etf_option_expire_day() -> List[str]:
    return _core.get_etf_option_expire_day()


def get_option_info(codes: List[str] = []) -> dict:
    return _core.get_option_info(codes)


def get_option_t(underlying: str, expire_month: str) -> dict:
    return _core.get_option_t(underlying, expire_month)


def get_strike_price_etf(underlying_price: float, need_secondary: bool = False) -> Decimal:
    return _core.get_strike_price_etf(underlying_price, need_secondary)


def get_seller_holding_cost(is_call: bool, underlying_price: Decimal, strike_price: Decimal) -> Decimal:
    return _core.get_seller_holding_cost(is_call, underlying_price, strike_price)


def get_latest_option_price(underlying: str, expire_month: str) -> dict:
    return _core.get_latest_option_price(underlying, expire_month)


def volatility(code: str) -> Decimal:
    return _core.volatility(code)

