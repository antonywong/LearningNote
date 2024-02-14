# -*- coding: utf-8 -*-

UNDERLYING = [
    # 上证50
    {
        'index': '000016',
        'etf': ['sh510050'],
        'cffex': 'ho'
    },
    # 深证100
    {
        'index': '399330',
        'etf': ['sz159901']
    },
    # 沪深300
    {
        'index': '000300',
        'etf': ['sh510300','sz159919'],
        'cffex': 'io'
    },
    # 创业板
    {
        'index': '399006',
        'etf': ['sz159915']
    },
    # 科创50
    {
        'index': '000688',
        'etf': ['sh588000','sh588080']
    },
    # 中证500
    {
        'index': '000905',
        'etf': ['sh510500','sz159922']
    },
    # 中证1000指数
    {
        'index': '000852',
        'cffex': 'mo'
    }
]

STACK_COMMISSION_RATE = 0.0001
OPTION_COMMISSION = 3
OPTION_MARGIN = 5000

WATCHLIST_COUNT = 6
