# -*- coding: utf-8 -*-
import pandas as pd
from dal import mssql
import option as base
import const
from bot import we_com

def analyze(oidf: pd.DataFrame):
    result = []
    # result.append(', '.join(oidf.columns.tolist()))

    for underlying, underlying_group in oidf.groupby("标的"):
        result.append(f"========{underlying}========")
        for days, group in underlying_group.groupby("剩余天数"):
            # 挑选最低的合成做多价和最高的合成做空价
            temppd = pd.concat([ \
                group.sort_values(by='↑平衡价').head(1), \
                group.sort_values(by='↓平衡价', ascending=False).head(1)] \
                , ignore_index=True)
            # result += temppd.to_string(index=False, header=False).split("\n")

            price1 = int(round(temppd.loc[0, "↑平衡价"] * 10000, 0))
            strike_price1 =temppd.loc[0, "行权价"]
            underlying_price = temppd.loc[0, "标的价格"] * 10
            price2 = int(round(temppd.loc[1, "↓平衡价"] * 10000, 0))
            strike_price2 = temppd.loc[1, "行权价"]

            profit = cal_profit(price1, strike_price1, underlying_price, price2, strike_price2)
            yearly_profit = int(round((profit[7] - profit[6]) / days * 365, 0))

            prices = profit[0:5] + [f"{profit[5]}|获利/{profit[7]}|佣金/{round(profit[6], 2)}|剩余{days}天|年化/{yearly_profit}"]
            price_msg = "|{}{}{}{}{}|{}".format(*prices)

            yearly_profit_rate = round(yearly_profit / (prices[2] + base.OPTION_MARGIN) * 100, 2)
            result.append(f"{yearly_profit_rate}\t{price_msg}")

    return result + analyze_watchlist(oidf)

def analyze_watchlist(oidf: pd.DataFrame):
    latest_deal = mssql.queryAll(f"SELECT TOP(1) underlying,expire_day FROM OptionDeal ORDER BY [time] DESC")
    if not len(latest_deal):
       return ""
    underlying = latest_deal[0]['underlying']
    oidf = oidf[oidf['标的'] == underlying]

    expire_day = latest_deal[0]['expire_day']
    oidf = oidf[oidf['到期日'] == expire_day]

    oidf = oidf.reset_index()

    price = oidf.at[0, "标的价格"]
    inter = 50 if price < 3000 else 100

    strike_prices = [0 for i in range(base.WATCHLIST_COUNT * 2 + 1)]
    strike_prices[base.WATCHLIST_COUNT] = int(round(float(price) / inter, 0)) * inter
    for i in range(base.WATCHLIST_COUNT):
        strike_prices[base.WATCHLIST_COUNT - 1 - i] = analyze_watchlist_price(strike_prices[base.WATCHLIST_COUNT - i], -1)
        strike_prices[base.WATCHLIST_COUNT + 1 + i] = analyze_watchlist_price(strike_prices[base.WATCHLIST_COUNT + i], 1)

    result = ["========WATCHLIST========"]
    remind_message = ""
    for sp in strike_prices:
        new_df = oidf[oidf['行权价'] == sp]
        if new_df.empty:
            continue
        new_info = new_df.iloc[0]
        days = new_info["剩余天数"]

        price1 = int(round(new_info["↑平衡价"] * 10000, 0))
        strike_price1 = sp
        underlying_price = new_info["标的价格"] * 10
        price2 = int(round(new_info["↓平衡价"] * 10000, 0))
        strike_price2 = sp

        profit = cal_profit(price1, strike_price1, underlying_price, price2, strike_price2)
        yearly_profit = int(round((profit[7] - profit[6]) / days * 365, 0))

        prices = profit[0:5] + [f"{profit[5]}|获利/{profit[7]}|佣金/{round(profit[6], 2)}|剩余{days}天|年化/{yearly_profit}|{expire_day[0:6]}"]
        price_msg = "|{}{}{}{}{}|{}".format(*prices)

        yearly_profit_rate = round(yearly_profit / (prices[2] + base.OPTION_MARGIN) * 100, 2)
        result.append(f"{yearly_profit_rate}\t{price_msg}")

        remind_message += analyze_watchlist_remind(underlying, expire_day, sp)

    if remind_message:
        # result.append(remind_message)
        we_com.send_message(const.DICT["WE_COM_OPTION_BOT_KEY"], remind_message)
    return result


def analyze_watchlist_price(price, direction):
    inter = 50 if price < 3000 or (price == 3000 and direction == -1) else 100 
    return price + direction * inter


def analyze_watchlist_remind(underlying, expire_day, strike_price):
    top = 14400 // int(const.DICT["ANALYZE_RECORD_INTERVAL"])
    records = mssql.queryAll(f"SELECT TOP({top}) long_profit, short_profit FROM VOptionRecord01 WHERE underlying='{underlying}' AND expire_day='{expire_day}' AND strike_price={strike_price} ORDER BY time DESC")
    if len(records) < 200:
        return ""
    profits = [r["long_profit"] for r in records] if records[0]["long_profit"] > records[0]["short_profit"] else [r["short_profit"] for r in records]
    latest_profit = profits[0]
    profits = sorted(profits[1:], reverse=True)
    profits = profits[:len(records) // 200]
    if latest_profit > profits[-1]:
        return f"{strike_price}升贴水进入高估区间\n"
    else:
        return ""


def cal_profit(price1, strike_price1, underlying_price, price2, strike_price2):
    # 计算标的价格与期权合成价格的关系[price1,升贴水1,underlying_price,升贴水2,price2,操作,佣金,毛利]
    result = [0,"",0,"",0,"", 0, 0]
    result[0] = price1
    result[2] = underlying_price
    result[4] = price2
    result[1] = "↗" if result[0]  < result[2] else "↘"
    result[3] = "↗" if result[2]  < result[4] else "↘"

    if result[1] == "↗" and result[3] == "↗":
        result[5] = f'+期权({strike_price1})/-期权({strike_price2})'
        result[6] = base.OPTION_COMMISSION * 3 * 2
        result[7] = result[4] - result[0]
    elif result[1] == "↗" and result[3] == "↘":
        result[5] = f'+期权({strike_price1})/-标的'
        result[6] = result[2] * base.STACK_COMMISSION_RATE * 2 + base.OPTION_COMMISSION * 3
        result[7] = result[2] - result[0]
    elif result[1] == "↘" and result[3] == "↗":
        result[5] = f'+标的/-期权({strike_price2})'
        result[6] = result[2] * base.STACK_COMMISSION_RATE * 2 + base.OPTION_COMMISSION * 3
        result[7] = result[4] - result[2]
    else:
        result[5] = "无套利空间"
    
    return result