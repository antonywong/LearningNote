# -*- coding: utf-8 -*-
from dal import mssql
from crawler import etf_option as etf_op_crawler
import option as base

def update_etf_contract():
    """更新ETF期权所有合约
    """
    # 行权日
    contract_month = etf_op_crawler.get_contract_month()
    expire_day = list(map(lambda x: etf_op_crawler.get_expire_day(x)[0].replace("-", ""), contract_month))
    print('到期日：', end='')
    print(expire_day)

    # 标的代码
    underlyings = []
    for x in base.UNDERLYING:
        underlyings.extend(x['etf'])
    print('标的ETF代码：', end='')
    print(underlyings)

    # 合约代码
    option_info = etf_op_crawler.get_codes(expire_day, underlyings)
    codes = set(option_info['code'])

    # 删除旧合约
    select_sql = "SELECT code FROM OptionInfo"
    old_codes = set(row["code"] for row in mssql.queryAll(select_sql))
    delete_codes = list(old_codes - codes)
    if(len(delete_codes) > 0):
        delete_sql = ["DELETE FROM OptionInfo WHERE code in ('%s')" % "','".join(delete_codes)]
        mssql.run(delete_sql)

    # 插入新合约
    insert_codes = list(codes - old_codes)
    if(len(insert_codes) > 0):
        all_price = etf_op_crawler.get_price(insert_codes)
        data = [(row["code"], row["is_call"], row["expire_day"], row["underlying"], int(float(all_price[row["code"]].loc[7, "值"]) * 1000))
                for i, row in option_info[option_info["code"].isin(insert_codes)].iterrows()]
        insert_sql = ["INSERT INTO OptionInfo (code,is_call,expire_day,underlying,strike_price) VALUES ('%s', %s, '%s', '%s',%s)" % x for x in data]
        mssql.run(insert_sql)