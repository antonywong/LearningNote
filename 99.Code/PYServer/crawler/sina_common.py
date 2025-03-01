# -*- coding: utf-8 -*-
import requests
import pandas as pd
import numpy as np
from typing import List

headers = {
    "Accept":
    "*/*",
    "Accept-Encoding":
    "gzip, deflate, br",
    "Accept-Language":
    "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control":
    "no-cache",
    "Connection":
    "keep-alive",
    "Host":
    "hq.sinajs.cn",
    "Pragma":
    "no-cache",
    "Referer":
    "https://stock.finance.sina.com.cn/",
    "sec-ch-ua":
    '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    "sec-ch-ua-mobile":
    "?0",
    "sec-ch-ua-platform":
    '"Windows"',
    "Sec-Fetch-Dest":
    "script",
    "Sec-Fetch-Mode":
    "no-cors",
    "Sec-Fetch-Site":
    "cross-site",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
}


def get_stock_spot(codes: List[str]) -> pd.DataFrame:
    result = []

    group_size = 200
    # 分组获取，防止HTTP 431
    for i in range(0, len(codes), group_size):
        url = f"http://hq.sinajs.cn/list={','.join(codes[i:i + group_size])}"
        res = requests.get(url, headers=headers).text
        res_data = [
            x[x.find('"') + 1:x.rfind('"')].split(",")[:-1]
            for x in res.split(";\n") if x
        ]
        if len(res_data) == 32:
            res_data.append("00")
        result.extend(res_data)

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

    return pd.DataFrame(result, columns=field_list)
