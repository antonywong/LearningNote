# -*- coding: utf-8 -*-
# 合成策略升贴水套利

import json
from typing import List
from decimal import Decimal
import option
from dal import mssql
from config import trading_day

def run(underlyings: List[str], expire_months: List[str], is_test: bool = False):  
    if not is_test and not trading_day.is_trading_time():
        return

    if len(underlyings) == 0:
        underlyings = [y for x in option.UNDERLYING for y in x['etf']]
    
    if len(expire_months) == 0:
        print("无过期月")
        return

    for underlying in underlyings:
        for expire_month in expire_months:
            # 最新买卖价
            select_sql = "SELECT top(1) time,underlying_price,data FROM OptionPrice WHERE underlying='%s' AND expire_month='%s'"
            option_price = mssql.queryAll(select_sql % (underlying, expire_month))[0]
            price_data = json.loads(option_price['data'])

            # T型报价
            select_sql = "SELECT strike_price,cCode,pCode FROM VOptionT WHERE underlying='%s' AND expire_month='%s' AND is_standard=1 ORDER BY strike_price"
            option_t = mssql.queryAll(select_sql % (underlying, expire_month))

            for row in option_t:
               strike_price = row["strike_price"]
               c_price = price_data[row["cCode"]]
               p_price = price_data[row["pCode"]]
               row["long_c_price"] = c_price[0][0]
               row["long_s_price"] = p_price[1][0]
               row["short_c_price"] = c_price[1][0]
               row["short_s_price"] = p_price[0][0]
               row["long"] = (strike_price + Decimal(row["long_c_price"]) - Decimal(row["long_s_price"])).quantize(Decimal('0.00000'))
               row["short"] = (strike_price + Decimal(row["short_c_price"]) - Decimal(row["short_s_price"] )).quantize(Decimal('0.00000'))

            result = {}
            for l_row in option_t:
                for s_row in option_t:                    
                    l_strike_price = (l_row["strike_price"] * 10000).quantize(Decimal('0'))
                    s_strike_price = (s_row["strike_price"] * 10000).quantize(Decimal('0'))                    
                    long_c_price = round(l_row["long_c_price"] * 10000)
                    long_s_price = round(l_row["long_s_price"] * 10000)
                    short_c_price = round(s_row["short_c_price"] * 10000)
                    short_s_price = round(s_row["short_s_price"] * 10000)
                    if long_c_price == 0 or long_s_price == 0 or short_c_price == 0 or short_s_price == 0:
                        continue
                    long = (l_row["long"] * 10000).quantize(Decimal('0'))
                    short = (s_row["short"] * 10000).quantize(Decimal('0'))
                    earn = short - long - option.OPTION_COMMISSION * 2
                    if earn > 0 and (underlying not in result.keys() or result[underlying]["earn"] < earn):
                        result[underlying] = {
                            "earn": earn,
                            "log": f"★合成套利 {option_price['time']} {underlying} 合成多{l_strike_price:>5}(+{long_c_price}-{long_s_price})={long:<6}\t合成空{s_strike_price:>5}(+{short_c_price}-{short_s_price})={short:<6}\t盈利:{earn}"
                        }

            for underlying in result.keys():
                print(result[underlying]["log"])