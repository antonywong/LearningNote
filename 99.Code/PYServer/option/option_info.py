# -*- coding: utf-8 -*-
import pandas as pd
from datetime import datetime
from dal import mssql
import option as base
from crawler import option
import const
from bot import we_com


COLLECTION_TITLE = ["标的", "标的价格", "到期日","剩余天数", "行权价",
    "|看涨:", "↑code", "↑买量", "↑买价", "↑卖价", "↑卖量",
    "|看跌:", "↓code", "↓买量", "↓买价", "↓卖价", "↓卖量",
    "合成做多:","↑平衡价", "↑升水", "↑年化升水",
    "合成做空:","↓平衡价", "↓升水", "↓年化升水"]


def sync():    
    contract_month = option.get_contract_month()
    expire_day = list(map(lambda x: option.get_expire_day(x)[0].replace("-", ""), contract_month))

    optionInfo = option.get_codes(expire_day, base.UNDERLYINGS)
    sql = ["DELETE FROM OptionInfo"]
    insert_sql = "INSERT INTO OptionInfo (Code, is_call, expire_day, underlying) VALUES ('{}', {}, '{}', '{}')"
    sql.extend([insert_sql.format(row["code"], row["is_call"], row["expire_day"], row["underlying"]) for index, row in optionInfo.iterrows()])
    mssql.run(sql)


def collect() -> pd.DataFrame:
    oi_codes = mssql.queryAll(f"SELECT code FROM OptionInfo")
    codes = list(map(lambda x: x["code"], oi_codes))
    allPrice = option.get_price(codes)

    sql = []
    update_sql = "UPDATE OptionInfo SET strike_price={} WHERE Code='{}'"
    sql.extend([update_sql.format(allPrice[c].loc[7, "值"], c) for c in codes])
    mssql.run(sql)

    result = pd.DataFrame(columns=COLLECTION_TITLE)

    underlying_prices = {}
    ois = mssql.queryAll(f"SELECT underlying, expire_day, strike_price, is_call, code FROM OptionInfo ORDER BY underlying, expire_day, strike_price, is_call")
    for i in range(0, len(ois), 2):

        underlying = ois[i + 1]["underlying"]
        if underlying not in underlying_prices.keys():
            underlying_prices[underlying] = float(option.get_underlying_price(underlying).loc[3, "值"])
        underlying_price = underlying_prices[underlying]

        sp = float(ois[i]['strike_price'])
        call = allPrice[ois[i + 1]["code"]]
        put = allPrice[ois[i]["code"]]
        
        expire_day = ois[i]['expire_day']

        oi = {
            "标的": underlying,
            "标的价格": int(underlying_price * 1000),
            "到期日": expire_day,
            "行权价": int(sp * 1000),
            "|看涨:": "|看涨:",
            "↑code": ois[i + 1]["code"],
            "↑买量": int(call.loc[0, "值"]),
            "↑买价": float(call.loc[1, "值"]),
            "↑卖价": float(call.loc[3, "值"]),
            "↑卖量": int(call.loc[4, "值"]),
            "|看跌:": "|看跌:",        
            "↓code": ois[i]["code"],
            "↓买量": int(put.loc[0, "值"]),
            "↓买价": float(put.loc[1, "值"]),
            "↓卖价": float(put.loc[3, "值"]),
            "↓卖量": int(put.loc[4, "值"]),
            "合成做多:": "|合成↑:",
            "合成做空:": "|合成↓:",
        }

        oi["↑平衡价"] = sp + oi['↑卖价'] - oi['↓买价']
        oi["↓平衡价"] = sp + oi['↑买价'] - oi['↓卖价']
        oi["↑升水"] = oi["↑平衡价"] - underlying_price
        oi["↓升水"] = oi["↓平衡价"] - underlying_price        

        expire_date = datetime.strptime(expire_day, '%Y%m%d').date()
        today = datetime.today().date()
        delta_days = (expire_date - today).days + 1
        oi["剩余天数"] = delta_days

        oi["↑年化升水"] = round(oi["↑升水"] / delta_days * 365, 4)
        oi["↓年化升水"] = round(oi["↓升水"] / delta_days * 365, 4)

        result = pd.concat([result, pd.DataFrame([oi])], ignore_index=True)

    return result


def record(oidf: pd.DataFrame, now: str):
    sql = []
    insert_sql = "INSERT INTO OptionRecord (underlying,expire_day,strike_price,time,long_price,underlying_price,short_price) VALUES ('{}','{}',{},'{}',{},{},{})"
    sql.extend([insert_sql.format(oi["标的"], oi["到期日"], oi["行权价"], now, int(round(oi["↑平衡价"] * 10000, 0)), oi["标的价格"] * 10, int(round(oi["↓平衡价"] * 10000, 0))) for index, oi in oidf.iterrows()])
    mssql.run(sql)