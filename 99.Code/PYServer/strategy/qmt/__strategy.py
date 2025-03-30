#encoding:gbk

import requests
import json


def init(C):
	C.test = 0
	C.server_url = "http://10.10.10.17:5000"
	C.underlying = "sh588000"
	C.expire_month = "2504"
	C.interval = 5

	C.run_time("run", str(C.interval) + "nSecond", "2025-01-01 00:00:00")


def run(C):
	#account变量是模型交易界面 添加策略时选择的资金账号 不需要手动填写
	#快速交易参数(quickTrade )填2 passorder函数执行后立刻下单 不会等待k线走完再委托。 可以在after_init函数 run_time函数注册的回调函数里进行委托 
	#a=passorder(52, 1101, account, '10008131.SHO', 6, 0, 1, C)
	#print(a)
	#return

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


		print("查询账号结果：", end="\t")
		accounts=get_trade_detail_data(account, "STOCK_OPTION", "ACCOUNT")
		for dt in accounts:
			print(f'总资产: {dt.m_dBalance:.2f}, 净资产: {dt.m_dAssureAsset:.2f}, 总市值: {dt.m_dInstrumentValue:.2f}', 
			f'总负债: {dt.m_dTotalDebit:.2f}, 可用金额: {dt.m_dAvailable:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')


		print(f"查询持仓结果：", end="\t")
		position_contracts = []
		positions = get_trade_detail_data(account, "STOCK_OPTION", 'position')
		for dt in positions:
			if dt.m_nVolume != 0:
				position_contracts.append((dt.m_strInstrumentID, dt.m_nDirection, dt.m_nVolume))
		print(position_contracts)


		print('回传进行分析：', end="\t")
		url = C.server_url + "/v1/api/qmt/delta"
		body = {
			"test": C.test,
			"balance": accounts[0].m_dBalance,
			"position_contracts": position_contracts,
			"underlying": C.underlying,
			"expire_month": C.expire_month }
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
				passorder(opType, 1101, account, code, prType, price, vol, C)
			print((opType, 1101, account, code, prType, price, vol))

	except Exception as e:
		print(f"{e}")
		return

