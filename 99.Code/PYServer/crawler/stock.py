# -*- coding: utf-8 -*-
import pandas as pd
from crawler import sina_option, sina_common
from typing import List

from datetime import datetime
from urllib import request
import json
import time
import dal


def get_price(code: List[str]) -> pd.DataFrame:
    return sina_common.get_stock_spot(code)


def get_k(code: str, scale: int, datalen: int) -> pd.DataFrame:
    url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=%d&datalen=%d" % (code, scale, datalen)
    with request.urlopen(url) as f:
        data = json.loads(f.read().decode('gb2312'))
        return pd.DataFrame(data)
