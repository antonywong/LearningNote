# -*- coding: utf-8 -*-
from typing import List, Tuple

import option as op
from crawler import etf_option as etf_op_crawler, cffex_option as cffex_op_crawler
from dal import mssql


def get_etf_option_info() -> List[Tuple]:
    contract_month = etf_op_crawler.get_contract_month()
    expire_day = list(
        map(lambda x: etf_op_crawler.get_expire_day(x)[0].replace("-", ""),
            contract_month))
    underlyings = []
    for x in op.UNDERLYING:
        underlyings.extend(x['etf'])
    option_info = etf_op_crawler.get_codes(expire_day, underlyings)

    codes = option_info['code'].values.tolist()
    all_price = etf_op_crawler.get_price(codes)

    return [(row["code"], row["is_call"], row["expire_day"], row["underlying"],
             int(float(all_price[row["code"]].loc[7, "值"]) * 1000))
            for i, row in option_info.iterrows()]


def get_cffex_option_info() -> List[Tuple]:
    op_type = map(lambda x: x['cffex'], op.UNDERLYING)
    op_type = list(filter(lambda x: x != '', op_type))

    contract_month = cffex_op_crawler.get_contract_month()
    codes = [(x + y) for x in op_type for y in contract_month]
    data_list = []
    for x in codes:
        data_list.extend(get_cffex_option_info_by_code(x))

    return data_list


def get_cffex_option_info_by_code(code: str) -> List[Tuple]:
    underlying = {}
    for x in op.UNDERLYING:
        if x['cffex'] != '':
            underlying[x['cffex']] = x['index']

    result = []
    all_price = cffex_op_crawler.get_price(code)
    for i, row in all_price.iterrows():
        c1 = row["看涨合约-标识"]
        result.append((c1, 1, row["到期日"], underlying[c1[:2]], row["行权价"]))
        c2 = row["看跌合约-标识"]
        result.append((c2, 0, row["到期日"], underlying[c2[:2]], row["行权价"]))
    return result


def update_database(data: List[Tuple]):
    sql = ["DELETE FROM OptionInfo"]
    insert_sql = "INSERT INTO OptionInfo (code,is_call,expire_day,underlying,strike_price) VALUES ('%s', %s, '%s', '%s',%s)"
    sql.extend([insert_sql % x for x in data])
    mssql.run(sql)
