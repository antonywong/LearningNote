# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
from dal import mssql
import option as base

def analyze(oidf: pd.DataFrame):
    result = []

    deals = mssql.queryAll(f"SELECT underlying,expire_day,strike_price,time,long_call_cost,long_put_cost,underlying_cost,short_call_cost,short_put_cost FROM OptionDeal WHERE close_time IS null")
    if len(deals):
        result.append(f"========DEALS========")

    for deal in deals:
        new_info = oidf[oidf['标的'] == deal['underlying']][oidf['到期日'] == deal['expire_day']][oidf['行权价'] == deal['strike_price']].iloc[0]

        open_position_cost = 0
        open_position_cost += 0 if deal['long_call_cost'] == 0 or deal['long_put_cost'] == 0 else (deal['long_call_cost'] + deal['long_put_cost'] - base.OPTION_COMMISSION)
        open_position_cost += 0 if deal['underlying_cost'] == 0 else (deal['underlying_cost'] - abs(deal['underlying_cost']) * base.STACK_COMMISSION_RATE)
        open_position_cost += 0 if deal['short_call_cost'] == 0 or deal['short_put_cost'] == 0 else (deal['short_call_cost'] + deal['short_put_cost'] - base.OPTION_COMMISSION)

        close_position_cost = 0
        if deal['long_call_cost'] != 0 and deal['long_put_cost'] != 0:
            close_position_cost += new_info['↑买价'] * 10000 - base.OPTION_COMMISSION - new_info['↓卖价'] * 10000 - base.OPTION_COMMISSION
        if deal['underlying_cost'] != 0:
            close_position_cost += (-1 if deal['underlying_cost'] > 0 else 1) * new_info['标的价格'] * 10 - abs(new_info['标的价格']) * 10 * base.STACK_COMMISSION_RATE
        if deal['short_call_cost'] != 0 and deal['short_put_cost'] != 0:
            close_position_cost += new_info['↓买价'] * 10000 - base.OPTION_COMMISSION - new_info['↑卖价'] * 10000 - base.OPTION_COMMISSION

        profit = round(open_position_cost + close_position_cost, 2)

        deal_date = deal['time'].date()
        today = datetime.today().date()
        delta_days = (today - deal_date).days + 1
        yearly_profit = profit / delta_days * 365
        price_msg = f"|{deal['underlying']}|{deal['expire_day']}|{deal['strike_price']}|开仓/{open_position_cost}|平仓/{close_position_cost}|获利/{profit}|年化/{round(yearly_profit, 2)}"

        yearly_profit_rate = round(yearly_profit / (abs(deal['underlying_cost']) + base.OPTION_MARGIN) * 100, 2)
        result.append(f"{yearly_profit_rate}\t{price_msg}")

    return result