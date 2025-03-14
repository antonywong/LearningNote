# -*- coding: utf-8 -*-

import json
import numpy as np
from scipy import stats
from datetime import datetime
from decimal import Decimal
from scipy import stats
from typing import List
from dal import mssql
import option
import stock

BS_RISK_FREE_RATE = 0.01
BS_UNDERLYING_DIVIDEND_RATE = 0.0


def calculate_index():
    select_sql = "SELECT id,CAST(time AS date) AS time,underlying,underlying_price,data FROM OptionPrice WHERE calculated=0"
    option_prices = mssql.queryAll(select_sql)
    for option_price in option_prices:
        v = float(stock.volatility(option.GET_UNDERLYING_INDEX(option_price["underlying"]))) # 历史波动率
        underlying_price = option_price["underlying_price"]
        data = json.loads(option_price["data"])
        codes = data.keys()
        select_sql = "SELECT code,is_call,strike_price,expire_month,expire_day FROM OptionCode WHERE code IN ('%s')" % "','".join(codes)        
        option_codes = mssql.queryAll(select_sql)
        contracts = {row["code"]: row for row in option_codes}
        time = datetime.strptime(option_price["time"], "%Y-%m-%d")
        for code in codes:
            is_call = contracts[code]["is_call"]
            expire_month = contracts[code]["expire_month"]
            days = (datetime(int("20" + expire_month[0:2]), int(expire_month[2:4]), int(contracts[code]["expire_day"])) - time).days + 1
            # print(code)
            # data[code][2] 以最新成交价计算各类指标
            price = data[code][2][0]
            data[code][2] = __calculate_index(float(underlying_price), float(contracts[code]["strike_price"]), days, price, is_call)
            data[code][2][4] = v # 历史波动率
            # data[code][3] 以买一卖一平均价计算各类指标
            if len(data[code]) <= 3:
                data[code].append([])
            avg = round((data[code][0][0] + data[code][1][0]) / 2.0, 6)
            data[code][3] = __calculate_index(float(underlying_price), float(contracts[code]["strike_price"]), days, avg, is_call)
            data[code][3][4] = v # 历史波动率
    
        insert_sql = ["UPDATE OptionPrice SET data='%s',calculated=1 WHERE id=%s" % (json.dumps(data, separators=(',', ':')), option_price["id"])]
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
def __calculate_index(underlying_price: float, strike_price: float, days: float, option_price: float, is_call: bool) -> List:
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


def get_option_code(underlying: str, expire_month: str) ->  List[str]:
    if not underlying or not expire_month:
        return []

    select_sql = "SELECT code FROM OptionCode WHERE underlying='%s' AND expire_month='%s' AND is_standard=1"
    codes = mssql.queryAll(select_sql % (underlying, expire_month))
    return [row["code"] for row in codes]


def get_strike_price_etf(underlying_price: Decimal, need_secondary: bool) -> Decimal:
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
    """
    认购=Max(12%×标的价-认购期权虚值, 7%×标的价)  认购期权虚值=Max(行权价-标的价, 0)
    认沽=Max(12%×标的价-认沽期权虚值, 7%×行权价)  认沽期权虚值=Max(标的价-行权价, 0)"""
    if is_call:
        cost = max(Decimal("0.12") * underlying_price - max(strike_price - underlying_price, Decimal("0")), Decimal("0.07") * underlying_price)
    else:
        cost = max(Decimal("0.12") * underlying_price - max(underlying_price - strike_price, Decimal("0")), Decimal("0.07") * strike_price)
    cost = cost * Decimal("10000") * Decimal(option.OPTION_MARGIN_RATE)
    return cost.quantize(Decimal("0.00"))


