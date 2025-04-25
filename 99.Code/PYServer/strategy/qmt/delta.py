# -*- coding: utf-8 -*-
# 动态delta中性双卖套利

from decimal import Decimal
from datetime import datetime, date
from config.console import Console
from config import trading_day
import option
import arbitrage._05
from bot import mail


IS_RUNNING = False
TOTAL_INDEX = {}


def pre(request_json: dict) -> str:
    try:
        print(request_json)
        account = request_json["account"]
        underlying = request_json["underlying"]
        expire_month = request_json["expire_month"]
        option_price = option.get_latest_option_price(underlying, expire_month)

        option_t = option.get_option_t(underlying, expire_month)
        oprations = []
        for t_row in option_t:
            oprations.append(arbitrage._05.cal(True, True, t_row["cCode"], t_row["strike_price"], option_price))
            oprations.append(arbitrage._05.cal(True, False, t_row["cCode"], t_row["strike_price"], option_price))
            oprations.append(arbitrage._05.cal(False, True, t_row["pCode"], t_row["strike_price"], option_price))
            oprations.append(arbitrage._05.cal(False, False, t_row["pCode"], t_row["strike_price"], option_price))
        position_contracts = []
        for res_pc in request_json["position_contracts"]:
            for i in range(res_pc[2]):
                if res_pc[1] == 48:
                    position_contracts.append("+" + res_pc[0])
                elif res_pc[1] == 49:
                    position_contracts.append("-" + res_pc[0])

        #计算持仓量
        opration_dict = {op.op_code: op for op in oprations}
        position_total = sum([opration_dict[pc].holding_cost for pc in position_contracts])

        #仓位上限
        console = Console()
        position_rate = round(position_total / console.get_balance(account) + 0.0005, 3)
        console.set_position_rate(account, position_rate)

        return ""
    except Exception as e:
        print(e)

def run(request_json: dict) -> dict:
    global IS_RUNNING, TOTAL_INDEX
    result = {"msg": "", "orders": []}
    if IS_RUNNING:
        print("IS_RUNNING")
        result["msg"] = "IS_RUNNING"
        return result
    IS_RUNNING = True

    try:
        is_test = request_json["test"]
        if not is_test and not (trading_day.is_trading_time() and datetime.now().hour * 100 + datetime.now().minute < 1457):
            result["msg"] = "NOT_TRADING_TIME"
            return result

        print(request_json)        
        if not request_json["position_contracts"]:
            print("NO_CONTRACTS")
            result["msg"] = "NO_CONTRACTS"
            return result

        account = request_json["account"]
        underlying = request_json["underlying"]
        expire_month = request_json["expire_month"]
        option_price = option.get_latest_option_price(underlying, expire_month)
        time = option_price["time"]
        if not is_test and abs((datetime.now() - time).seconds) > 3:
            print(f"无最新价价格，延迟{(datetime.now() - time).seconds}秒\t", time)
            result["msg"] = f"无最新价价格，延迟{(datetime.now() - time).seconds}秒\t"
            return result

        option_t = option.get_option_t(underlying, expire_month)
        oprations = []
        for t_row in option_t:
            oprations.append(arbitrage._05.cal(True, True, t_row["cCode"], t_row["strike_price"], option_price))
            oprations.append(arbitrage._05.cal(True, False, t_row["cCode"], t_row["strike_price"], option_price))
            oprations.append(arbitrage._05.cal(False, True, t_row["pCode"], t_row["strike_price"], option_price))
            oprations.append(arbitrage._05.cal(False, False, t_row["pCode"], t_row["strike_price"], option_price))

        console = Console()
        position_contracts = []
        for res_pc in request_json["position_contracts"]:
            for i in range(res_pc[2]):
                if res_pc[1] == 48:
                    position_contracts.append("+" + res_pc[0])
                elif res_pc[1] == 49:
                    position_contracts.append("-" + res_pc[0])
        position_contracts_posi_delta = []
        position_contracts_nega_delta = []
        #总持仓金额
        position_total = 0.0
        #总delta
        delta_total = 0.0
        #总gamma
        gamma_total = 0.0
        #仓位上限
        position_upper = console.get_balance(account) * console.get_position_rate(account)
        #计算持仓各参数之和
        opration_dict = {op.op_code: op for op in oprations}
        for pc in position_contracts:
            if pc in opration_dict.keys():
                op = opration_dict[pc]
                position_total += op.holding_cost
                delta_total += op.delta
                gamma_total += op.gamma
                if op.delta > 0:
                    position_contracts_posi_delta.append(op)
                else:
                    position_contracts_nega_delta.append(op)

        #缓存参数
        if account not in TOTAL_INDEX.keys():
            TOTAL_INDEX[account] = {}
        TOTAL_INDEX[account]["delta"] = delta_total
        TOTAL_INDEX[account]["gamma"] = gamma_total
        TOTAL_INDEX[account]["position_contracts"] = position_contracts

        #参数报警
        print(f"position:{round(position_total, 0)}/{round(position_upper, 0)}, delta_total:{delta_total}, gamma_total:{gamma_total}")
        if request_json["alarm"]:
            gamma_final = console.get_balance(account) / 1000 * 7
            gamma_times = int(abs(delta_total) * 1000 / gamma_final)
            expire_day = [day for day in option.get_etf_option_expire_day() if day[0:4] == expire_month][0]            
            days =(date(int("20" + expire_day[0:2]), int(expire_day[2:4]), int(expire_day[4:6])) - datetime.now().date()).days
            if days == 0:
                result["msg"] = f"THE_LAST_DAY"
                return result
            days = 6 - (date(int("20" + expire_day[0:2]), int(expire_day[2:4]), int(expire_day[4:6])) - datetime.now().date()).days
            if days < 0:
                days = 0
            alarm_level = gamma_times - 2 - days
            is_alarm_tick = alarm_level > 0 and (int(datetime.now().second / 3) % round(20 / alarm_level) == 0)
            if is_alarm_tick:
                mail.send_message("1411038526@qq.com", f"{account}组合delta预警", f"{account}组合delta：{round(delta_total, 4)}，已超过{gamma_times}倍gamma_final({round(gamma_final, 4)})。")
            result["msg"] = f"JUST_CHECKED_ALARM__{round(delta_total, 4)}__{gamma_times}_*_{round(gamma_final, 4)}"
            return result


        available_money = position_upper - position_total
        if available_money > 0:
            #开仓操作
            oprations = sorted(oprations, key=lambda x: x.theta, reverse=True)
            opration_posi_delta = next((op for op in oprations if op.delta > 0), None)
            opration_posi_delta_code = opration_posi_delta.op_code[1:]
            opration_posi_delta_is_buy = opration_posi_delta.op_code[0] == "+"
            opration_nega_delta = next((op for op in oprations if op.delta < 0), None)
            opration_nega_delta_code = opration_nega_delta.op_code[1:]
            opration_nega_delta_is_buy = opration_nega_delta.op_code[0] == "+"

            if available_money > (opration_posi_delta.holding_cost + opration_nega_delta.holding_cost) * 2:
                print(f"OPEN_A_GROUP")
                result["orders"].append({ "code": opration_posi_delta_code, "is_buy": opration_posi_delta_is_buy, "is_open": True })
                available_money -= opration_posi_delta.holding_cost
                delta_total += opration_posi_delta.delta
                result["orders"].append({ "code": opration_nega_delta_code, "is_buy": opration_nega_delta_is_buy, "is_open": True })
                available_money -= opration_nega_delta.holding_cost
                delta_total += opration_nega_delta.delta

            #测试是否需要通过开仓调整delta
            if delta_total > 0 and available_money > opration_nega_delta.holding_cost and delta_total > (console.DELTA_TOLERANCE - gamma_total * 2 / 1000 + abs(opration_nega_delta.delta)):
                print(f"CHANGE_DELTA_BY_OPEN:delta_total({delta_total}) > TOLERANCE({console.DELTA_TOLERANCE}) - gamma({gamma_total * 2}) + delta({abs(opration_nega_delta.delta)})")
                result["orders"].append({ "code": opration_nega_delta_code, "is_buy": opration_nega_delta_is_buy, "is_open": True })
                return merge_order(result)
            elif delta_total < 0 and available_money > opration_posi_delta.holding_cost and delta_total < (gamma_total * 2 / 1000 - console.DELTA_TOLERANCE - abs(opration_posi_delta.delta)):
                print(f"CHANGE_DELTA_BY_OPEN:delta_total({delta_total}) < gamma({gamma_total * 2}) - TOLERANCE({console.DELTA_TOLERANCE}) - delta({abs(opration_posi_delta.delta)})")
                result["orders"].append({ "code": opration_posi_delta_code, "is_buy": opration_posi_delta_is_buy, "is_open": True })
                return merge_order(result)

        #减仓操作
        position_contracts_posi_delta = sorted(position_contracts_posi_delta, key=lambda x: x.theta, reverse=False)
        position_contracts_nega_delta = sorted(position_contracts_nega_delta, key=lambda x: x.theta, reverse=False)
        while available_money < 0:
            print(f"CLOSE_TO_BELOW_UPPER")
            if delta_total > 0:
                if not position_contracts_posi_delta:
                    break
                close_contract = position_contracts_posi_delta.pop(0)
            else:
                if not position_contracts_nega_delta:
                    break
                close_contract = position_contracts_nega_delta.pop(0)
            result["orders"].append({ "code": close_contract.op_code[1:], "is_buy": close_contract.op_code[0] == "-", "is_open": False })

            available_money += close_contract.holding_cost
            delta_total -= close_contract.delta

        #测试是否需要通过平仓调整delta
        if delta_total > 0 and position_contracts_posi_delta:
            close_contract = position_contracts_posi_delta.pop(0)
            if delta_total > (console.DELTA_TOLERANCE * 2 - gamma_total * 2 / 1000 + abs(close_contract.delta)):
                print(f"CHANGE_DELTA_BY_CLOSE:delta_total({delta_total}) > TOLERANCE({console.DELTA_TOLERANCE * 2 }) - gamma({gamma_total * 2}) + delta({abs(close_contract.delta)})")
                result["orders"].append({ "code": close_contract.op_code[1:], "is_buy": close_contract.op_code[0] == "-", "is_open": False })
                return merge_order(result)
        elif delta_total < 0 and position_contracts_nega_delta:
            close_contract = position_contracts_nega_delta.pop(0)
            if delta_total < (gamma_total * 2 / 1000 - console.DELTA_TOLERANCE * 2 - abs(close_contract.delta)):
                print(f"CHANGE_DELTA_BY_CLOSE:delta_total({delta_total}) < gamma({gamma_total * 2}) - TOLERANCE({console.DELTA_TOLERANCE * 2 }) - delta({abs(close_contract.delta)})")
                result["orders"].append({ "code": close_contract.op_code[1:], "is_buy": close_contract.op_code[0] == "-", "is_open": False })
                return merge_order(result)

        return merge_order(result)
    except Exception as e:
        print(e)
    finally:
        IS_RUNNING = False


def merge_order(result: dict) -> dict:
    order_count = {}
    op_count = {}
    for o in result["orders"]:
        order_key = o["code"]
        op_key = (o["code"], o["is_buy"], o["is_open"])
        order_count[order_key] = order_count.get(order_key, 0) + (1 if o["is_buy"] else -1)
        op_count[op_key] = op_count.get(op_key, 0) + 1

    changed_orders = []
    for (code, is_buy, is_open), count in op_count.items():
        if order_count[code] != 0:
            changed_orders.append({ "code": code,  "is_buy": is_buy, "is_open": is_open, "vol": count })

    result["orders"] = changed_orders
    return result
