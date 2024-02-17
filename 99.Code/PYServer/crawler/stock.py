# -*- coding: utf-8 -*-
import pandas as pd
from crawler import sina_option, sina_common
from typing import List


def get_price(code: List[str]) -> pd.DataFrame:
    return sina_common.get_stock_spot(code)
