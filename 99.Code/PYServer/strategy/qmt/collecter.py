# # -*- coding: utf-8 -*-

from decimal import Decimal
from datetime import datetime, timedelta
from config import trading_day
from dal import mssql
import option
    

def get_all_code():
    if not trading_day.is_pre_trading_updated():
        return "PRE_TRADING_NOT_UPDATED"

    expire_months = [day[0:4] for day in option.get_etf_option_expire_day()]
    result = []
    for u in option.UNDERLYING:
        index = u["index"]
        result.append(index[2:] + "." + index[0:2].upper())
        for etf in u["etf"]:
            result.append(etf[2:] + "." + etf[0:2].upper())
            for expire_month in expire_months:
                option_t = option.get_option_t(etf, expire_month)
                result.extend([code+".SZO" if code[0]=="9" else code+".SHO" for t in option_t for code in (t["cCode"], t["pCode"])])
    return result


def get_option_code(underlying: str, expire_month: str):
    if not trading_day.is_pre_trading_updated():
        return "PRE_TRADING_NOT_UPDATED"
    if not trading_day.is_after_trading_updated():
        return "AFTER_TRADING_NOT_UPDATED"
    
    option_t = option.get_option_t(underlying, expire_month)
    return [code for t in option_t for code in (t["cCode"], t["pCode"])]


def post_option_code(all_contracts) -> str:
    print('更新ETF期权所有合约...')
    # 例：['588000.SH', '10008861', 20250924, 1.1, 'PUT']
    min_expire_month = str(min([c[2] for c in all_contracts]))[2:6]
    codes = set([c[1] for c in all_contracts])

    # 旧合约
    select_sql = "SELECT code FROM OptionCode WHERE expire_month>='%s'"
    old_codes = set(row["code"] for row in mssql.queryAll(select_sql % min_expire_month))
    insert_codes = list(codes - old_codes)

    # 插入新合约
    if insert_codes:
        insert_sql = [__gen_insert_sql(c) for c in all_contracts if c[1] in insert_codes]
        mssql.run(insert_sql)
    
    # 更新旧合约
    update_codes = list(codes - set(insert_codes))
    if update_codes:
        update_sql = [__gen_update_sql(c) for c in all_contracts if c[1] in update_codes]
        mssql.run(update_sql)

    trading_day.update_pre_trading()
    return ""


def __gen_insert_sql(contract) -> str:
    # 例：['588000.SH', '10008861', 20250924, 1.1, 'PUT']
    underlying = contract[0][-2:].lower() + contract[0][0:6]
    is_call = 1 if contract[4].upper() == "CALL" else 0
    expire_day = str(contract[2])
    is_standard = 1 if Decimal(contract[3]).quantize(Decimal('0.000000')) == option.get_strike_price_etf(Decimal(contract[3])).quantize(Decimal('0.000000')) else 0
    para = (contract[1], underlying, is_call, contract[3], expire_day[2:6], expire_day[-2:], is_standard)                 
    return "INSERT INTO OptionCode (code,underlying,is_call,strike_price,expire_month,expire_day,is_standard) VALUES ('%s','%s','%s','%s','%s','%s','%s')" % para


def __gen_update_sql(contract) -> str:
    is_standard = 1 if Decimal(contract[3]).quantize(Decimal('0.000000')) == option.get_strike_price_etf(Decimal(contract[3])).quantize(Decimal('0.000000')) else 0
    para = (contract[3], is_standard, contract[1])                 
    return "UPDATE OptionCode SET strike_price='%s', is_standard='%s' WHERE code='%s'" % para


def post_tick(request_json: dict) -> str:
    if not trading_day.is_pre_trading_updated():
        return "PRE_TRADING_NOT_UPDATED"
    if not trading_day.is_after_trading_updated():
        return "AFTER_TRADING_NOT_UPDATED"

    # print(request_json["tick"])
    time = datetime.min
    underlying = request_json["underlying"]
    expire_month = request_json["expire_month"]
    underlying_price = request_json["underlying_price"]
    data = {}
    for key, value in request_json["tick"].items():
        timetag = datetime.strptime(value["timetag"][0:17], "%Y%m%d %H:%M:%S")
        timetag_minute = timetag.hour * 100 + timetag.minute
        if timetag_minute < 930 or 1500 < timetag_minute:
            continue

        time = max([time, timetag])
        data[key[0:8]] = __to_price(value)
        data[key[0:8]].append([timetag])
        
    if not data:
        print("TICK_IS_NONE")
        return ""

    option.save_tick(time, underlying, underlying_price, expire_month, data)
    return ""


def __to_price(price):
    """
    Returns:
        List:
            [0:卖一价, 1:卖一量],
            [0:买一价, 1:买一量],
            [0:最新价],
            [0:盘口平均价]
    """
    return [
        [round(price["askPrice"][0], 4), int(price["askVol"][0])],
        [round(price["bidPrice"][0], 4), int(price["bidVol"][0])],
        [round(price["lastPrice"], 4)],
        [round((price["askPrice"][0] + price["bidPrice"][0]) / 2.0, 5)]
    ]

def get_k_1m_time(request_json: dict) -> dict:
    code_dict = {}
    for qmt_code in request_json:
        code_part = qmt_code.split('.')
        if len(code_part[0]) == 6:
            code_dict[qmt_code] = code_part[1].lower() + code_part[0]
        elif len(code_part[0]) == 8:
            code_dict[qmt_code] = code_part[0]

    select_sql = "SELECT code,max(day) AS day FROM K WHERE type=1 AND code in ('%s') GROUP BY code"
    codes = [r for key, r in code_dict.items()]
    option_time = {row["code"]: row["day"] for row in mssql.queryAll(select_sql % "','".join(codes))}

    for key, r in code_dict.items():
        if r not in option_time.keys():
            date = datetime.now() - timedelta(days=300)
            return date.strftime("%Y%m") + "15093000"

    return min([day for key, day in option_time.items()]).strftime("%Y%m%d%H%M%S")

def post_k_1m(request_json: dict) -> str:
    sql = []
    for data in request_json:
        if not data["open"] and not data["high"] and not data["low"] and not data["close"]:
            continue

        code_part = data["code"].split('.')
        if len(code_part[0]) == 6:
            code = code_part[1].lower() + code_part[0]
        elif len(code_part[0]) == 8:
            code = code_part[0]
        else:
            continue
        day = datetime.strptime(data["day"], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        sql.append("DELETE FROM K WHERE type=1 AND code='%s' AND day='%s'" % (code, day))
        para = (code, day, round(data["open"], 6), round(data["high"], 6), round(data["low"], 6), round(data["close"], 6), int(data["volume"]))
        sql.append("INSERT INTO K (type,code,day,[open],high,low,[close],volume) VALUES (1,'%s','%s',%s,%s,%s,%s,%s)" % para)

    mssql.run(sql)
    print(f"DEAL_K_{len(sql) / 2}")
    return ""


def update_after_trading() -> str:
    try:
        underlyings = [u["index"] for u in option.UNDERLYING]
        underlyings.extend([etf for u in option.UNDERLYING for etf in u["etf"]])
        for underlying in underlyings:
            __update_k_1d(underlying)
        option.recalculate_k_index()
        trading_day.update_after_trading()
        return ""
    except Exception as e:
        print(f"update_after_trading({underlying}): {e}")
        return f"update_after_trading({underlying})失败: {e}"


def __update_k_1d(underlying):
    print(f"__update_k_1d({underlying})")
    select_sql = "SELECT TOP(1) day FROM K WHERE type=240 AND code='%s' ORDER BY day DESC"
    days = mssql.queryAll(select_sql % underlying)
    last_day = days[0]["day"] if days else datetime(2025, 3, 27)
    while last_day < datetime.now():
        last_day_str = last_day.strftime("%Y-%m-%d")
        select_sql = "SELECT [open],high,low,[close],volume FROM K WHERE type=1 AND code='%s' AND CONVERT(CHAR(10), day, 20)='%s' ORDER BY day DESC"
        minutes = mssql.queryAll(select_sql % (underlying, last_day_str))
        if len(minutes) != 241:
            last_day = last_day + timedelta(days=1)
            continue

        sql = ["DELETE FROM K WHERE type=240 AND code='%s' AND day='%s 00:00:00'" % (underlying, last_day_str)]
        high = max([m["high"] for m in minutes])
        low = min([m["low"] for m in minutes])
        volume = sum([m["volume"] for m in minutes]) * 100
        para = (underlying, last_day_str, minutes[-1]["open"], high, low, minutes[0]["close"], volume)
        sql.append("INSERT INTO K (type,code,day,[open],high,low,[close],volume) VALUES (240,'%s','%s 00:00:00','%s','%s','%s','%s','%s')" % para)
        mssql.run(sql)

        last_day = last_day + timedelta(days=1)