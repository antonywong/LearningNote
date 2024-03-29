# -*- coding: utf-8 -*-
import pandas as pd
from typing import Dict, Tuple
from datetime import datetime

from dal import mssql


def calculate(underlying, allPrice) -> pd.DataFrame:
    result = []

    sql = f"SELECT underlying, expire_day, strike_price, is_call, code FROM OptionInfo WHERE underlying='{underlying}' ORDER BY expire_day, strike_price, is_call"
    ois = mssql.queryAll(sql)
    for i in range(0, len(ois), 2):

        underlying_price = allPrice[underlying][1]

        sp = float(ois[i]['strike_price'])
        c_price = allPrice[ois[i + 1]["code"]]
        p_price = allPrice[ois[i]["code"]]

        expire_day = ois[i]['expire_day']

        oi = {
            "标的": int(underlying_price * 10000),
            "到期": expire_day,
            "行权价": int(sp),
            "|看涨": "|看涨:",
            # "↑code": ois[i + 1]["code"],
            "↑买": int(c_price[0] * 10000),
            "↑卖": int(c_price[1] * 10000),
            "|看跌": "|看跌:",
            # "↓code": ois[i]["code"],
            "↓买": int(p_price[0] * 10000),
            "↓卖": int(p_price[1] * 10000),
            "|合成↑:": "|合成↑:",
            "|合成↓:": "|合成↓:",
        }

        oi["↑平衡价"] = int(sp * 10) + oi['↑卖'] - oi['↓买']
        oi["↓平衡价"] = int(sp * 10) + oi['↑买'] - oi['↓卖']
        oi["↑升水"] = oi["↑平衡价"] - oi['标的']
        oi["↓升水"] = oi["↓平衡价"] - oi['标的']

        expire_date = datetime.strptime(expire_day, '%Y%m%d').date()
        today = datetime.today().date()
        delta_days = (expire_date - today).days + 1
        oi["剩余"] = delta_days

        oi["↑收益"] = round(0, 1)
        oi["↓收益"] = round((oi["↓升水"] - oi["标的"] * 0.00008 * 2 - 2.6 * 3) / (oi["标的"] + 1000 + oi['↓卖']) * 100, 4)

        oi["↑年化升水"] = round(oi["↑升水"] / delta_days * 365, 1)
        oi["↑年化收益"] = round(oi["↑收益"] / delta_days * 365, 2)
        oi["↓年化升水"] = round(oi["↓升水"] / delta_days * 365, 1)
        oi["↓年化收益"] = round(oi["↓收益"] / delta_days * 365, 2)

        result.append(oi)
    return pd.DataFrame(result, columns=["标的", "到期", "剩余", "行权价",
        "|看涨", "↑买", "↑卖",
        "|看跌", "↓买", "↓卖",
        "|合成↑:","↑平衡价", "↑升水", "↑年化升水", "↑收益", "↑年化收益",
        "|合成↓:","↓平衡价", "↓升水", "↓年化升水", "↓收益", "↓年化收益"])
