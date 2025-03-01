# -*- coding: utf-8 -*-

import math
from datetime import datetime, timedelta
from decimal import Decimal
import numpy as np
from dal import mssql

def volatility(code: str) -> Decimal:
    """计算历史波动率
    """
    select_sql = "SELECT TOP(61) [close] FROM StockK WHERE code='%s' AND type=240 ORDER BY day DESC"
    close = [float(row["close"]) for row in mssql.queryAll(select_sql % code)]
    if len(close) == 0:
        return 0.0
    increase = np.array([math.log(close[i] / close[i - 1]) for i in range(1, len(close))])

    return Decimal(np.std(increase) * np.sqrt(252)).quantize(Decimal('0.000000'))
