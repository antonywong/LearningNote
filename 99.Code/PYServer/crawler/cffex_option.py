# -*- coding: utf-8 -*-
import pandas as pd
from typing import List, Dict
from crawler import sina_option


def get_contract_month() -> List[str]:
    """股指期权合约到期月份列表
    """
    # print('crawler.cffex_option.get_contract_month...', end='')
    return sina_option.option_cffex_sz50_list_sina()


def get_price(symbol: str) -> Dict[str, pd.DataFrame]:
    """期权实时数据
    """
    # print(f'crawler.cffex_option.get_price...', end='')
    return sina_option.option_cffex_spot_sina(symbol[:2], symbol)
