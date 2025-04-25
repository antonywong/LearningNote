#encoding:gbk

import requests
import json


def init(C):
	C.test = 0
	C.server_url = "http://10.10.10.18:5000"
	C.underlying = "sz159915"
	C.expire_month = "2505"
	C.interval = 5

	body = get_body(C)
	url = C.server_url + "/v1/api/qmt/pre_delta"
	r = requests.post(url, json.dumps(body), headers={'Content-Type': 'application/json'})
	data_json = r.json()
	if data_json:
		print(data_json)
		return
	else:
		print("PRE_DELTA_COMPLETED")
		C.run_time("run", str(C.interval) + "nSecond", "2025-01-01 00:00:00")


def run(C):
	try:
		print("STRATEGY_START")

		print("查询委托结果：", end="\t")
		orders = get_trade_detail_data(account, "STOCK_OPTION", 'order')
		unfinished_orders = []
		for o in orders:
			if o.m_nOrderStatus not in (53, 54, 56, 57):
				unfinished_orders.append((o.m_strOrderSysID, o.m_nOrderStatus))
		print(unfinished_orders)
		if len(unfinished_orders) > 0:
			print("未成交，先撤单")
			for uo in unfinished_orders:
				cancel(uo[0], account, 'STOCK_OPTION', C)
			return


		print('回传进行分析：', end="\t")
		body = get_body(C)
		url = C.server_url + "/v1/api/qmt/delta"
		r = requests.post(url, json.dumps(body), headers={'Content-Type': 'application/json'}, timeout=(C.interval-1))
		data_json = r.json()
		if data_json["msg"]:
			print(data_json["msg"])
			return
		else:
			print("STRATEGY_GET:%s" % len(data_json["orders"]))

		for order in data_json["orders"]:
			code = order["code"]
			code = code+".SZO" if code[0]=="9" else code+".SHO"
			if order["is_buy"]:
				if order["is_open"]:
					opType = 50
				else:
					opType = 53
				prType = 3
			else:
				if order["is_open"]:
					opType = 52
				else:
					opType = 51
				prType = 7
			price = 0
			vol = order["vol"]

			if C.test:
				#print(data_json)
				print("TEST_MODE_NO_ORDER", end="\t")
			else:
				print("********ORDER**********", end="\t")
				passorder(opType, 1101, account, code, prType, price, vol, "delta", 2, "", C)
			print((opType, 1101, account, code, prType, price, vol))

	except Exception as e:
		print(f"{e}")
		return


def get_body(C):
	print(f"查询持仓结果：", end="\t")
	position_contracts = []
	positions = get_trade_detail_data(account, "STOCK_OPTION", 'position')
	for dt in positions:
		if dt.m_nVolume != 0:
			position_contracts.append((dt.m_strInstrumentID, dt.m_nDirection, dt.m_nVolume))
	print(position_contracts)

	return {
		"test": C.test,
		"account": account,
		"position_contracts": position_contracts,
		"underlying": C.underlying,
		"expire_month": C.expire_month,
		"alarm": 0  }