#encoding:gbk

from datetime import datetime
import requests
import json


def init(C):
	C.test = 1
	C.server_url = "http://10.10.10.18:5000"
	C.underlying = ["sh588000", "sz159915"]
	C.underlying_index = ["000688.SH", "399006.SZ"]
	C.expire_month = ["2505", "2506"]
	C.stock_list = {}
	C.balance_underlying = "sz159915"
	C.balance_expire_month = "2505"

	url = C.server_url + "/v1/api/qmt/option/code"
	for u in C.underlying:
		for m in C.expire_month:
			params = {"underlying": u, "expire_month": m}
			r = requests.get(url, params=params)
			data_json = r.json()
			#print(data_json)
			if data_json == "PRE_TRADING_NOT_UPDATED":
				print(data_json)
				update_pre_trading(C)
				r = requests.get(url, params=params)
				data_json = r.json()
			if data_json == "AFTER_TRADING_NOT_UPDATED":
				print(data_json)
				update_after_trading(C)
				r = requests.get(url, params=params)
				data_json = r.json()
			key = (u, m)
			C.stock_list[key] = [code+".SZO" if code[0]=="9" else code+".SHO" for code in data_json]
	print(C.stock_list)

def handlebar(C):
	if not C.is_last_bar():
		return

	print("回传TICK数据：", end="\t")
	url = C.server_url + "/v1/api/qmt/tick"
	for u in C.underlying:
		for m in C.expire_month:
			try:
				etf_code = u[2:] + "." + u[0:2].upper()
				underlying_tick = C.get_full_tick([etf_code])
				key = (u, m)
				tick = C.get_full_tick(C.stock_list[key])
				body = {
					"underlying": u,
					"underlying_price": underlying_tick[etf_code]["lastPrice"],
					"expire_month": m,
					"tick": tick }
				r = requests.post(url, json.dumps(body), headers={'Content-Type': 'application/json'}, timeout=1)
				data_json = r.json()
				if data_json == "PRE_TRADING_NOT_UPDATED":
					print(data_json)
					update_pre_trading(C)
					return
				elif data_json == "AFTER_TRADING_NOT_UPDATED":
					print(data_json)
					update_after_trading(C)
					return
				elif data_json:
					print(data_json)
				else:
					print(f"{key} POSTED")
			except Exception as e:
				print(f"{e}")

	try:
		data_json = update_k_1m(C, C.underlying_index, 1)
		if data_json:
			print(data_json)
		else:
			print(f"{C.underlying_index} POSTED")
	except Exception as e:
		print(f"{e}")

	try:
		body = get_body(C)
		url = C.server_url + "/v1/api/qmt/delta"
		r = requests.post(url, json.dumps(body), headers={'Content-Type': 'application/json'}, timeout=1)
		data_json = r.json()
		if data_json["msg"]:
			print(data_json["msg"])
			return
		else:
			print("STRATEGY_GET:%s" % len(data_json["orders"]))
	except Exception as e:
		print(f"{e}")

def update_pre_trading(C):
	all_underlyings = [
		"510050.SH",             # 上证50
		"588000.SH","588080.SH", # 科创50
		"159901.SZ",             # 深证100
		"159915.SZ",             # 创业板
		"510300.SH","159919.SZ", # 沪深300
		"510500.SH","159922.SZ", # 中证500
	]
	all_contracts = []
	for u in all_underlyings:
		for o in C.get_option_list(u, datetime.now().strftime("%Y%m%d")):
			op_data = C.get_option_detail_data(o)
			all_contracts.append([u, op_data["InstrumentID"], op_data["ExpireDate"], op_data["OptExercisePrice"], op_data["optType"]])
	url = C.server_url + "/v1/api/qmt/option/code"
	#print(all_contracts)
	r = requests.post(url, json.dumps(all_contracts), headers={'Content-Type': 'application/json'})
	data_json = r.json()
	if data_json:
		print(data_json)
	else:
		print(f"ALL_CONTRACTS_POSTED")

def update_after_trading(C):
	url = C.server_url + "/v1/api/qmt/all_code"
	r = requests.get(url)
	all_code = r.json()

	try:
		group_size = 1
		for i in range(0, len(all_code), group_size):
			codes = all_code[i:i + group_size]
			data_json = update_k_1m(C, codes)
			if data_json:
				print(data_json)
				return
	except Exception as e:
		print(f"{e}")
		return

	update_url = C.server_url + "/v1/api/qmt/after_trading"
	r = requests.post(update_url, json.dumps(""), headers={'Content-Type': 'application/json'})

def update_k_1m(C, codes: list, timeout: int = 0) -> str:
	get_time_url = C.server_url + "/v1/api/qmt/k_1m_time"
	post_url = C.server_url + "/v1/api/qmt/k_1m"

	if timeout:
		r = requests.post(get_time_url, json.dumps(codes), headers={'Content-Type': 'application/json'}, timeout=timeout)
	else:
		r = requests.post(get_time_url, json.dumps(codes), headers={'Content-Type': 'application/json'})
	latest_time = r.json()
	a = C.get_market_data_ex(stock_code=codes, period='1m', start_time=latest_time)
	body = []
	rows = 0
	for key, df in a.items():
		for row in df.itertuples():
			row_dict = {
				"code": key,
				"day": row.Index,
				"open": row.open,
				"high": row.high,
				"low": row.low,
				"close": row.close,
				"volume": row.volume
			}
			rows += 1
			body.append(row_dict)
	if timeout:
		r = requests.post(post_url, json.dumps(body), headers={'Content-Type': 'application/json'}, timeout=timeout)
	else:
		r = requests.post(post_url, json.dumps(body), headers={'Content-Type': 'application/json'})
	data_json = r.json()
	if data_json:
		return data_json
	else:
		print("最新时间：", latest_time, "\t数据量：", rows, f"\t{codes} POSTED")
		return ""


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
		"underlying": C.balance_underlying,
		"expire_month": C.balance_expire_month,
		"alarm": 1 }