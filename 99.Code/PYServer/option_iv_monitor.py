# -*- coding: utf-8 -*-

from config import trading_day
import arbitrage._04

arbitrage._04.run("sz159915", trading_day.get_etf_option_expire_day()[0][0:4])
