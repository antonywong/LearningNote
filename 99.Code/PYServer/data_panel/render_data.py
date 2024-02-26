# -*- coding: utf-8 -*-
import pandas as pd
from typing import Dict, Tuple
from datetime import datetime

from dal import mssql


def calculate(underlying, allPrice) -> pd.DataFrame:
    result = pd.DataFrame(columns=["标的价格", "到期日","剩余天数", "行权价",
    "|看涨:", "↑买价", "↑卖价",
    "|看跌:", "↓买价", "↓卖价",
    "|合成↑:","↑平衡价", "↑升水", "↑年化升水",
    "|合成↓:","↓平衡价", "↓升水", "↓年化升水"])

    sql = f"SELECT underlying, expire_day, strike_price, is_call, code FROM OptionInfo WHERE underlying='{underlying}' ORDER BY expire_day, strike_price, is_call"
    ois = mssql.queryAll(sql)
    for i in range(0, len(ois), 2):

        underlying_price = allPrice[underlying][1]

        sp = float(ois[i]['strike_price'])
        c_price = allPrice[ois[i + 1]["code"]]
        p_price = allPrice[ois[i]["code"]]

        expire_day = ois[i]['expire_day']

        oi = {
            "标的价格": int(underlying_price * 1000),
            "到期日": expire_day,
            "行权价": int(sp),
            "|看涨:": "|看涨:",
            # "↑code": ois[i + 1]["code"],
            "↑买价": int(c_price[0] * 10000),
            "↑卖价": int(c_price[1] * 10000),
            "|看跌:": "|看跌:",
            # "↓code": ois[i]["code"],
            "↓买价": int(p_price[0] * 10000),
            "↓卖价": int(p_price[1] * 10000),
            "|合成↑:": "|合成↑:",
            "|合成↓:": "|合成↓:",
        }

        oi["↑平衡价"] = int(sp * 10) + oi['↑卖价'] - oi['↓买价']
        oi["↓平衡价"] = int(sp * 10) + oi['↑买价'] - oi['↓卖价']
        oi["↑升水"] = oi["↑平衡价"] - oi['标的价格'] * 10
        oi["↓升水"] = oi["↓平衡价"] - oi['标的价格'] * 10

        expire_date = datetime.strptime(expire_day, '%Y%m%d').date()
        today = datetime.today().date()
        delta_days = (expire_date - today).days + 1
        oi["剩余天数"] = delta_days

        oi["↑年化升水"] = round(oi["↑升水"] / delta_days * 365, 1)
        oi["↓年化升水"] = round(oi["↓升水"] / delta_days * 365, 1)

        result = pd.concat([result, pd.DataFrame([oi])], ignore_index=True)

    return result
