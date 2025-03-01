# -*- coding: utf-8 -*-

from typing import List
from datetime import datetime
from decimal import Decimal
from stock import _core, akshare_collecter

COLLECTER = akshare_collecter

def collect(codes: List[str] = [], scale: int = 240, datalen: int = 48):
    return COLLECTER.collect(codes, scale, datalen)

def volatility(code: str) -> Decimal:
    return _core.volatility(code)
