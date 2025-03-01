# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
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


def option_sse_list_sina(symbol: str = "50ETF",
                         exchange: str = "null") -> List[str]:
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName"
    params = {"exchange": f"{exchange}", "cate": f"{symbol}"}
    r = requests.get(url, params=params)
    data_json = r.json()
    date_list = data_json["result"]["data"]["contractMonth"]
    return ["".join(i.split("-")) for i in date_list][1:]


def option_sse_expire_day_sina(trade_date: str,
                               symbol: str = "50ETF",
                               exchange: str = "null") -> Tuple[str, int]:
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


def option_sse_codes_sina(expire_days: List[str],
                          underlyings: List[str]) -> pd.DataFrame:
    contract_months = dict(map(lambda x: (x[-6:-2], x), expire_days))
    underlying_codes = dict(map(lambda x: (x[2:], x), underlyings))
    params = []
    for month in contract_months.keys():
        for underlying in underlying_codes.keys():
            params.append("OP_UP_" + underlying + month)
            params.append("OP_DOWN_" + underlying + month)
    url = f"http://hq.sinajs.cn/list={','.join(params)}"
    res = requests.get(url, headers=headers).text

    result = pd.DataFrame(
        columns=["code", "is_call", "expire_day", "underlying"])
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


def option_sse_spot_price_sina(codes: List[str]) -> Dict[str, pd.DataFrame]:
    result = {}

    group_size = 200
    # 分组获取，防止HTTP 431
    for i in range(0, len(codes), group_size):
        params = map(lambda x: "CON_OP_" + x, codes[i:i + group_size])
        url = f"http://hq.sinajs.cn/list={','.join(params)}"
        res = requests.get(url, headers=headers).text
        for data_text in res.split(";"):
            data_text = data_text.strip()
            if data_text == "":
                continue

            code = data_text[data_text.find('CON_OP_') + 7:data_text.find('=')]
            data_list = data_text[data_text.find('"') + 1:data_text.rfind('"')].split(",")
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
            data_df = pd.DataFrame(list(zip(field_list, data_list)), columns=["字段", "值"])
            result[code] = data_df
    return result


def option_sse_daily_sina(symbol: str) -> pd.DataFrame:
    url = "https://stock.finance.sina.com.cn/futures/api/jsonp_v2.php//StockOptionDaylineService.getSymbolInfo"
    params = {"symbol": f"CON_OP_{symbol}"}
    
    nheaders = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://stock.finance.sina.com.cn/option/quotes.html",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "script",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/97.0.4692.71 Safari/537.36",
    }
    data_text = requests.get(url, params=params, headers=nheaders).text
    data_json = json.loads(data_text[data_text.find("(") + 1 : data_text.rfind(")")])
    temp_df = pd.DataFrame(data_json)
    temp_df.columns = ["日期", "开盘", "最高", "最低", "收盘", "成交量"]
    temp_df["日期"] = pd.to_datetime(temp_df["日期"], errors="coerce").dt.date
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"], errors="coerce")
    temp_df["最高"] = pd.to_numeric(temp_df["最高"], errors="coerce")
    temp_df["最低"] = pd.to_numeric(temp_df["最低"], errors="coerce")
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"], errors="coerce")
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"], errors="coerce")
    return temp_df


def option_cffex_sz50_list_sina() -> List[str]:
    """
    新浪财经-中金所-上证 50 指数-所有合约, 返回的第一个合约为主力合约
    目前新浪财经-中金所有上证 50 指数，沪深 300 指数和中证 1000 指数
    :return: 中金所-上证 50 指数-所有合约
    :rtype: dict
    """
    url = "https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    temp_attr = soup.find(attrs={"id": "option_suffix"}).find_all("li")
    return [item.text[2:] for item in temp_attr]


def option_cffex_spot_sina(product: str, symbol: str) -> pd.DataFrame:
    """
    中金所-上证 50 指数-指定合约-实时行情
    https://stock.finance.sina.com.cn/futures/view/optionsCffexDP.php/ho/cffex
    :param symbol: 合约代码; 用 ak.option_cffex_sz300_list_sina() 函数查看
    :type symbol: str
    :return: 中金所-上证 50 指数-指定合约-看涨看跌实时行情
    :rtype: pd.DataFrame
    """
    url = "https://stock.finance.sina.com.cn/futures/api/openapi.php/OptionService.getOptionData"
    params = {
        "type": "futures",
        "product": product,
        "exchange": "cffex",
        "pinzhong": symbol,
    }
    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find("{"):data_text.rfind("}") + 1])
    option_call_df = pd.DataFrame(
        data_json["result"]["data"]["up"],
        columns=[
            "看涨合约-买量",
            "看涨合约-买价",
            "看涨合约-最新价",
            "看涨合约-卖价",
            "看涨合约-卖量",
            "看涨合约-持仓量",
            "看涨合约-涨跌",
            "行权价",
            "看涨合约-标识",
        ],
    )
    option_put_df = pd.DataFrame(
        data_json["result"]["data"]["down"],
        columns=[
            "看跌合约-买量",
            "看跌合约-买价",
            "看跌合约-最新价",
            "看跌合约-卖价",
            "看跌合约-卖量",
            "看跌合约-持仓量",
            "看跌合约-涨跌",
            "看跌合约-标识",
        ],
    )
    data_df = pd.concat([option_call_df, option_put_df], axis=1)
    data_df["看涨合约-买量"] = pd.to_numeric(data_df["看涨合约-买量"], errors="coerce")
    data_df["看涨合约-买价"] = pd.to_numeric(data_df["看涨合约-买价"], errors="coerce")
    data_df["看涨合约-最新价"] = pd.to_numeric(data_df["看涨合约-最新价"], errors="coerce")
    data_df["看涨合约-卖价"] = pd.to_numeric(data_df["看涨合约-卖价"], errors="coerce")
    data_df["看涨合约-卖量"] = pd.to_numeric(data_df["看涨合约-卖量"], errors="coerce")
    data_df["看涨合约-持仓量"] = pd.to_numeric(data_df["看涨合约-持仓量"], errors="coerce")
    data_df["看涨合约-涨跌"] = pd.to_numeric(data_df["看涨合约-涨跌"], errors="coerce")
    data_df["行权价"] = pd.to_numeric(data_df["行权价"], errors="coerce")
    data_df["看跌合约-买量"] = pd.to_numeric(data_df["看跌合约-买量"], errors="coerce")
    data_df["看跌合约-买价"] = pd.to_numeric(data_df["看跌合约-买价"], errors="coerce")
    data_df["看跌合约-最新价"] = pd.to_numeric(data_df["看跌合约-最新价"], errors="coerce")
    data_df["看跌合约-卖价"] = pd.to_numeric(data_df["看跌合约-卖价"], errors="coerce")
    data_df["看跌合约-卖量"] = pd.to_numeric(data_df["看跌合约-卖量"], errors="coerce")
    data_df["看跌合约-持仓量"] = pd.to_numeric(data_df["看跌合约-持仓量"], errors="coerce")
    data_df["看跌合约-涨跌"] = pd.to_numeric(data_df["看跌合约-涨跌"], errors="coerce")
    expire_date = data_json["result"]["data"]["info"]["expire_date"].replace(
        '-', '')
    data_df["到期日"] = expire_date
    return data_df