# -*- coding: utf-8 -*-
import requests
import pandas as pd
from typing import Dict, List, Tuple


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "hq.sinajs.cn",
    "Pragma": "no-cache",
    "Referer": "https://stock.finance.sina.com.cn/",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
}


def option_sse_list_sina(symbol: str = "50ETF", exchange: str = "null") -> List[str]:
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName"
    params = {"exchange": f"{exchange}", "cate": f"{symbol}"}
    r = requests.get(url, params=params)
    data_json = r.json()
    date_list = data_json["result"]["data"]["contractMonth"]
    return ["".join(i.split("-")) for i in date_list][1:]


def option_sse_expire_day_sina(trade_date: str = "202102", symbol: str = "50ETF", exchange: str = "null") -> Tuple[str, int]:
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay"
    params = {
        "exchange": f"{exchange}",
        "cate": f"{symbol}",
        "date": f"{trade_date[:4]}-{trade_date[4:]}",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    data = data_json["result"]["data"]
    if int(data["remainderDays"]) < 0:
        url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay"
        params = {
            "exchange": f"{exchange}",
            "cate": f"{'XD' + symbol}",
            "date": f"{trade_date[:4]}-{trade_date[4:]}",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        data = data_json["result"]["data"]
    return data["expireDay"], int(data["remainderDays"])


def option_sse_codes_sina(expire_days: List[str], underlyings: List[str]) -> pd.DataFrame:

    contract_months = dict(map(lambda x: (x[-6:-2], x), expire_days))
    underlying_codes = dict(map(lambda x: (x[2:], x), underlyings))
    params = []
    for month in contract_months.keys():
        for underlying in underlying_codes.keys():
            params.append("OP_UP_" + underlying + month)
            params.append("OP_DOWN_" + underlying + month)            
    url = f"http://hq.sinajs.cn/list={','.join(params)}"
    res = requests.get(url, headers=headers).text
    
    result = pd.DataFrame(columns=["code", "is_call", "expire_day", "underlying"])
    for data_text in res.split(";"):
        data_text = data_text.strip().strip("var hq_str_OP_").strip(",\"")
        if data_text == "":
            continue

        data_part = data_text.split("=\"")
        data_info = data_part[0].split("_")

        for data_code in data_part[1].split(","):
            oi = {
                "code": data_code[7:],
                "is_call": 1 if data_info[0] == "UP" else 0,
                "expire_day": contract_months[data_info[1][-4:]],
                "underlying": underlying_codes[data_info[1][-10:-4]],
            }
            result = pd.concat([result, pd.DataFrame([oi])], ignore_index=True)

    return result


def option_sse_spot_price_sina(codes) -> Dict[str, pd.DataFrame]:
    result = {}

    params = map(lambda x: "CON_OP_" + x, codes)
    url = f"http://hq.sinajs.cn/list={','.join(params)}"
    res = requests.get(url, headers=headers).text
    for data_text in res.split(";"):
        data_text = data_text.strip()
        if data_text == "":
            continue
    
        code = data_text[data_text.find('CON_OP_') + 7 : data_text.find('=')]
        data_list = data_text[
            data_text.find('"') + 1 : data_text.rfind('"')
        ].split(",")
        field_list = [
            "买量",
            "买价",
            "最新价",
            "卖价",
            "卖量",
            "持仓量",
            "涨幅",
            "行权价",
            "昨收价",
            "开盘价",
            "涨停价",
            "跌停价",
            "申卖价五",
            "申卖量五",
            "申卖价四",
            "申卖量四",
            "申卖价三",
            "申卖量三",
            "申卖价二",
            "申卖量二",
            "申卖价一",
            "申卖量一",
            "申买价一",
            "申买量一 ",
            "申买价二",
            "申买量二",
            "申买价三",
            "申买量三",
            "申买价四",
            "申买量四",
            "申买价五",
            "申买量五",
            "行情时间",
            "主力合约标识",
            "状态码",
            "标的证券类型",
            "标的股票",
            "期权合约简称",
            "振幅",
            "最高价",
            "最低价",
            "成交量",
            "成交额",
        ]
        data_df = pd.DataFrame(
            list(zip(field_list, data_list)), columns=["字段", "值"]
        )
        result[code] = data_df
    return result


def option_sse_underlying_spot_price_sina(symbol: str = "sh510050") -> pd.DataFrame:
    url = f"http://hq.sinajs.cn/list={symbol}"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Host": "hq.sinajs.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://vip.stock.finance.sina.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    }
    r = requests.get(url, headers=headers)
    data_text = r.text
    data_list = data_text[
        data_text.find('"') + 1 : data_text.rfind('"')
    ].split(",")
    field_list = [
        "证券简称",
        "今日开盘价",
        "昨日收盘价",
        "最近成交价",
        "最高成交价",
        "最低成交价",
        "买入价",
        "卖出价",
        "成交数量",
        "成交金额",
        "买数量一",
        "买价位一",
        "买数量二",
        "买价位二",
        "买数量三",
        "买价位三",
        "买数量四",
        "买价位四",
        "买数量五",
        "买价位五",
        "卖数量一",
        "卖价位一",
        "卖数量二",
        "卖价位二",
        "卖数量三",
        "卖价位三",
        "卖数量四",
        "卖价位四",
        "卖数量五",
        "卖价位五",
        "行情日期",
        "行情时间",
        "停牌状态",
    ]
    data_df = pd.DataFrame(
        list(zip(field_list, data_list)), columns=["字段", "值"]
    )
    return data_df




