# -*- coding: utf-8 -*-
# 动态delta中性双卖套利-期权合约属性模型

from dataclasses import dataclass
from decimal import Decimal

@dataclass
class ModelOptionProperty:
    op_code: str
    holding_cost: float
    delta: float
    gamma: float
    vega: float
    theta: float
    strike_price: Decimal
    op_name: str
