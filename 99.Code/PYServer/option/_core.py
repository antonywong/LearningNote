# -*- coding: utf-8 -*-

import json
import numpy as np
from scipy import stats
from datetime import datetime, date
from decimal import Decimal
from scipy import stats
from typing import List
from dal import mssql
import config
from config import trading_day
import option, option.akshare_collecter
import stock


BS_RISK_FREE_RATE = 0.01
BS_UNDERLYING_DIVIDEND_RATE = 0.0


def recalculate_index():
    select_sql = "SELECT id,time,underlying,underlying_price,expire_month,data FROM OptionPrice WHERE calculated=0"
    for price_data in mssql.queryAll(select_sql):
        time = price_data["time"]
        underlying = price_data["underlying"]
        underlying_price = price_data["underlying_price"]
        expire_month =  price_data["expire_month"]
        data = json.loads(price_data["data"])
        v = float(stock.volatility(option.GET_UNDERLYING_INDEX(underlying))) # 历史波动率
        codes = sorted(data.keys())
        sorted_data = {}
        option_codes = option.get_option_info(codes)
        days = (date(int("20" + expire_month[0:2]), int(expire_month[2:4]), int(option_codes[0]["expire_day"])) - time.date()).days + 1
        contracts = {row["code"]: row for row in option_codes}
        for code in codes:
            c = contracts[code]
            d = data[code]
            # d[2] 以最新成交价计算各类指标
            #d[2] = _core.calculate_index(float(underlying_price), float(c["strike_price"]), days, d[2][0], c["is_call"])
            #d[2][4] = v # 历史波动率
            data[code][2] = data[code][2][0:1]
            # d[3] 以买一卖一平均价计算各类指标
            d[3] = calculate_index(float(underlying_price), float(c["strike_price"]), days, d[3][0], c["is_call"])
            d[3][4] = v # 历史波动率
            sorted_data[code] = d
        
        para = (json.dumps(sorted_data, separators=(',', ':')), price_data["id"])
        insert_sql = ["UPDATE OptionPrice SET data='%s', calculated=1 WHERE id='%s'" % para]
        mssql.run(insert_sql)


"""计算d1
:param S: 标的资产价格
:param X: 行权价
:param r: 无风险利率
:param q: 标的资产股息率
:param T: 到期时间（以年为单位）
:param sigma: 波动率
:param is_call: 期权类型（看涨期权=True，看跌期权=False）
Returns:
    List:
        [0:卖一价, 1:卖一量],
        [0:买一价, 1:买一量],
        [0:最近成交价, 1:内在价值, 2:时间价值, 3:隐含波动率, 4:历史波动率, 5:delta, 6:gamma, 7:vega, 8:theta, 9:rho],
        [0:盘口平均价, 1:内在价值, 2:时间价值, 3:隐含波动率, 4:历史波动率, 5:delta, 6:gamma, 7:vega, 8:theta, 9:rho],
"""
def calculate_index(underlying_price: float, strike_price: float, days: float, option_price: float, is_call: bool) -> List:
    value = (underlying_price - strike_price) * (1 if is_call else -1)
    time_value = option_price - value
    iv = bsm_implied_volatility(underlying_price, strike_price, days, option_price, is_call)
    T = days / 360.0
    delta = bsm_delta(underlying_price, strike_price, BS_RISK_FREE_RATE, BS_UNDERLYING_DIVIDEND_RATE, T, iv, is_call).item()
    gamma = bsm_gamma(underlying_price, strike_price, BS_RISK_FREE_RATE, BS_UNDERLYING_DIVIDEND_RATE, T, iv).item()
    vega = bsm_vega(underlying_price, strike_price, BS_RISK_FREE_RATE, BS_UNDERLYING_DIVIDEND_RATE, T, iv).item()
    theta = bsm_theta(underlying_price, strike_price, BS_RISK_FREE_RATE, BS_UNDERLYING_DIVIDEND_RATE, T, iv, is_call).item()
    rho = bsm_rho(underlying_price, strike_price, BS_RISK_FREE_RATE, BS_UNDERLYING_DIVIDEND_RATE, T, iv, is_call).item()
    return [option_price, round(value, 6), round(time_value, 6), round(iv, 6), None, round(delta, 6), round(gamma, 6), round(vega, 6), round(theta, 6), round(rho, 6)]

def bsm_d1(S: float, K: float, r: float, q: float, T: float, sigma: float):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return d1

def bsm_d2(d1: float, T: float, sigma: float):
    d2 = d1 - sigma  * np.sqrt(T)
    return d2

def bsm_delta(S: float, K: float, r: float, q: float, T: float, sigma: float, is_call: bool):
    d1 = bsm_d1(S, K, r, q, T, sigma)
    if is_call:
        return np.exp(-1 * q * T) * stats.norm.cdf(d1)
    else:
        return np.exp(-1 * q * T) * (stats.norm.cdf(d1) - 1)

def bsm_gamma(S: float, K: float, r: float, q: float, T: float, sigma: float):
    d1 =bsm_d1(S, K, r, q, T, sigma)
    return stats.norm.pdf(d1) * np.exp(-1 * q * T) / (S * sigma * np.sqrt(T))

def bsm_vega(S: float, K: float, r: float, q: float, T: float, sigma: float):
    d1 = bsm_d1(S, K, r, q, T, sigma)
    return S * np.sqrt(T) * stats.norm.pdf(d1) * np.exp(-1 * q * T)

def bsm_theta(S: float, K: float, r: float, q: float, T: float, sigma: float, is_call: bool):
    d1 = bsm_d1(S, K, r, q, T, sigma)
    d2 = bsm_d2(d1, T, sigma)
    if is_call:
        return -1 * S * stats.norm.pdf(d1) * sigma * np.exp(-1 * q * T) / (2 * np.sqrt(T)) + q * S * stats.norm.cdf(d1) * np.exp(-1 * q * T) - r * K * np.exp(-1 * r * T) * stats.norm.cdf(d2)
    else:
        return -1 * S * stats.norm.pdf(d1) * sigma * np.exp(-1 * q * T) / (2 * np.sqrt(T)) - q * S * stats.norm.cdf(-1 * d1) * np.exp(-1 * q * T) + r * K * np.exp(-1 * r * T) * stats.norm.cdf(-1 * d2)

def bsm_rho(S: float, K: float, r: float, q: float, T: float, sigma: float, is_call: bool):
    d1 = bsm_d1(S, K, r, q, T, sigma)
    d2 = bsm_d2(d1, T, sigma)
    if is_call:
        return K * T * np.exp(-1 * r * T) * stats.norm.cdf(d2)
    else:
        return -1 * K * T * np.exp(-1 * r * T) * stats.norm.cdf(-1 * d2)

def bsm_price(S: float, K: float, r: float, T: float, sigma: float, is_call: bool):
    d1 = bsm_d1(S, K, r, BS_UNDERLYING_DIVIDEND_RATE, T, sigma)
    d2 = bsm_d2(d1, T, sigma)
    if is_call:
        return S * stats.norm.cdf(d1) - K * np.exp(-r * T) * stats.norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * stats.norm.cdf(-d2) - S * stats.norm.cdf(-d1)

def bsm_implied_volatility(underlying_price: float, strike_price: float, days: float, option_price: float, is_call: bool, precision = 0.0001, max_iter = 1000):
    """计算隐含波动率
    :param precision: 精度要求
    :param max_iter: 最大迭代次数
    :return: 隐含波动率
    """
    T = days / 360.0
    sigma = 0.25
    for i in range(max_iter):
        price = bsm_price(underlying_price, strike_price, BS_RISK_FREE_RATE, T, sigma, is_call)
        vega = bsm_vega(underlying_price, strike_price, BS_RISK_FREE_RATE, BS_UNDERLYING_DIVIDEND_RATE, T, sigma)
        if vega < precision:
            return precision
        diff = option_price - price
        if abs(diff) < precision:
            return sigma
        sigma = sigma + diff / vega

    return sigma


def get_etf_option_expire_day() -> List[str]:
    """获取ETF期权合约到期日"""
    last_day = trading_day.get_last()[2:].replace("-", "")
    if len(config.CACHE_ETF_OPTION_EXPIRE_DAY) == 0 or config.CACHE_ETF_OPTION_EXPIRE_DAY[0] < last_day:
        sql = "SELECT DISTINCT expire_month+expire_day AS day FROM OptionCode where '20'+expire_month+expire_day >= FORMAT(GETDATE(),'yyyyMMdd') ORDER BY day"
        config.CACHE_ETF_OPTION_EXPIRE_DAY = [row["day"] for row in mssql.queryAll(sql)]

    return config.CACHE_ETF_OPTION_EXPIRE_DAY


def get_option_t(underlying: str, expire_month: str) -> list:
    """获取合约T型报价（标准合约）"""
    if not underlying or not expire_month:
        return []
    
    last_trading_day = trading_day.get_last()
    if not config.CACHE_OPTION_T["time"] or config.CACHE_OPTION_T["time"] != last_trading_day:
        config.CACHE_OPTION_T["time"] = last_trading_day
        config.CACHE_OPTION_T["t"] = {}

    cache_key = (underlying, expire_month)
    if cache_key not in config.CACHE_OPTION_T["t"].keys():
        select_sql = "SELECT strike_price,cCode,pCode FROM VOptionT WHERE underlying='%s' AND expire_month='%s' AND is_standard=1 ORDER BY strike_price"
        config.CACHE_OPTION_T["t"][cache_key] = mssql.queryAll(select_sql % cache_key)
    
    return config.CACHE_OPTION_T["t"][cache_key]


def get_option_info(codes: list = []) -> list:
    """获取合约信息"""
    last_trading_day = trading_day.get_last()
    if not config.CACHE_OPTION_INFO["time"] or config.CACHE_OPTION_INFO["time"] != last_trading_day:        
        # 盘前数据更新
        if not trading_day.is_pre_trading_updated():
            option.akshare_collecter.update_etf_contract()
            trading_day.update_pre_trading()

        config.CACHE_OPTION_INFO["time"] = last_trading_day
        select_sql = "SELECT code,underlying,is_call,strike_price,expire_month,expire_day,is_standard FROM OptionCode WHERE expire_month>='%s'"
        config.CACHE_OPTION_INFO["info"] = mssql.queryAll(select_sql % option.get_etf_option_expire_day()[0][0:4])
    
    if codes:
        return [info for info in config.CACHE_OPTION_INFO["info"] if info["code"] in codes]
    else:
        return config.CACHE_OPTION_INFO["info"]


def get_strike_price_etf(underlying_price: Decimal, need_secondary: bool) -> Decimal:
    """计算ETF当前价对应的行权价"""
    underlying_price += Decimal("0.001")
    multi = Decimal("100.000000")
    if underlying_price < 3:
        interval = 5
    elif  underlying_price < 5:
        interval = 10
    else:
        interval = 25
    strike_price = (underlying_price * multi / interval).quantize(Decimal("0")) * interval
    if need_secondary:
        secondary_strike_price = None
        if underlying_price < strike_price:
            secondary_strike_price = strike_price - interval
        elif underlying_price > strike_price:
            secondary_strike_price = strike_price + interval
        return strike_price / multi, secondary_strike_price / multi
    else:
        return strike_price / multi


def get_seller_holding_cost(is_call: bool, underlying_price: Decimal, strike_price: Decimal) -> Decimal:
    """获取持仓成本
    认购=Max(12%×标的价-认购期权虚值, 7%×标的价)  认购期权虚值=Max(行权价-标的价, 0)
    认沽=Max(12%×标的价-认沽期权虚值, 7%×行权价)  认沽期权虚值=Max(标的价-行权价, 0)"""
    if is_call:
        cost = max(
            Decimal("0.12") * underlying_price - max(strike_price - underlying_price, Decimal("0")),
            Decimal("0.07") * underlying_price)
    else:
        cost = max(
            Decimal("0.12") * underlying_price - max(underlying_price - strike_price, Decimal("0")),
            Decimal("0.07") * strike_price)
    cost = cost * Decimal("10000") * Decimal(option.OPTION_MARGIN_RATE)
    return cost.quantize(Decimal("0.00"))


def get_latest_option_price(underlying: str, expire_month: str) -> dict:
    """获取当前数据库最新的合约价格数据（标准合约）"""
    cache_key = (underlying, expire_month)
    if underlying and expire_month and cache_key not in config.CACHE_LATEST_OPTION_PRICE.keys():
        select_sql = "SELECT top(1) time,underlying_price,data FROM OptionPrice WHERE underlying='%s' AND expire_month='%s' ORDER BY time DESC"
        option_prices = mssql.queryAll(select_sql % cache_key)
        if len(option_prices) > 0:
            price = option_prices[0]
            config.CACHE_LATEST_OPTION_PRICE[cache_key] = {
                "time": price["time"],
                "underlying": underlying,
                "underlying_price": price["underlying_price"],
                "expire_month": expire_month,
                "data": json.loads(price["data"])
            }
    return config.CACHE_LATEST_OPTION_PRICE[cache_key]