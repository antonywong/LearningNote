# -*- coding: utf-8 -*-
# 动态delta中性双卖套利

from decimal import Decimal
from datetime import datetime
from config.console import Console
from config import trading_day
import option
import arbitrage._05

IS_RUNNING = False


def run(request_json: dict) -> dict:
    global IS_RUNNING
    result = {"msg": "", "orders": []}
    if IS_RUNNING:
        print("IS_RUNNING")
        result["msg"] = "IS_RUNNING"
        return result
    IS_RUNNING = True

    try:
        is_test = request_json["test"]
        if not is_test and not trading_day.is_trading_time():
            result["msg"] = "NOT_TRADING_TIME"
            return result

        print(request_json)
        underlying = request_json["underlying"]
        expire_month = request_json["expire_month"]
        option_price = option.get_latest_option_price(underlying, expire_month)
        time = option_price["time"]
        if not is_test and time.hour * 100 + time.minute >= 1457:
            result["msg"] = "NOT_TRADING_TIME"
            return result
        if not is_test and abs((datetime.now() - time).seconds) > 5:
            result["msg"] = "无最新价格"
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
        position_upper = request_json["balance"] * console.POSITION_RATE
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
        print(f"position:{round(position_total, 0)}/{round(position_upper, 0)}, delta_total:{delta_total}, gamma_total:{gamma_total}")

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
