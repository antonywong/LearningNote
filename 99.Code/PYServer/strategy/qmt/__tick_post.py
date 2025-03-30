#encoding:gbk

from datetime import datetime
import requests
import json


def init(C):
	C.server_url = "http://10.10.10.17:5000"
	C.underlying = ["sh588000", "sz159915"]
	C.expire_month = ["2504", "2505"]
	C.stock_list = {}

	url = C.server_url + "/v1/api/qmt/option/code"
	for u in C.underlying:
		for m in C.expire_month:
			params = {"underlying": u, "expire_month": m}
			r = requests.get(url, params=params)
			data_json = r.json()
			#print(data_json)
			if data_json == "PRE_TRADING_NOT_UPDATED":
				update_pre_trading(C)
				r = requests.get(url, params=params)
				data_json = r.json()
			if data_json == "AFTER_TRADING_NOT_UPDATED":
				update_after_trading(C)
				r = requests.get(url, params=params)
				data_json = r.json()
			key = (u, m)
			C.stock_list[key] = [code+".SZO" if code[0]=="9" else code+".SHO" for code in data_json]
	#print(C.stock_list)

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
					update_pre_trading(C)
					return
				elif data_json == "AFTER_TRADING_NOT_UPDATED":
					update_after_trading(C)
					return
				elif data_json:
					print(data_json)
				else:
					print(f"{key} POSTED")
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

	get_time_url = C.server_url + "/v1/api/qmt/k_1m_time"
	post_url = C.server_url + "/v1/api/qmt/k_1m"
	group_size = 10
	for i in range(0, len(all_code), group_size):
		try:
			codes = all_code[i:i + group_size]
			r = requests.post(get_time_url, json.dumps(codes), headers={'Content-Type': 'application/json'})
			a = C.get_market_data_ex(stock_code=codes, period='1m',start_time=r.json())
			body = []
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
					body.append(row_dict)
			r = requests.post(post_url, json.dumps(body), headers={'Content-Type': 'application/json'})
			data_json = r.json()
			if data_json:
				print(data_json)
				return
			else:
				print(f"{codes} POSTED")
		except Exception as e:
			print(f"{e}")
			return

	update_url = C.server_url + "/v1/api/qmt/after_trading"
	r = requests.post(update_url, json.dumps(""), headers={'Content-Type': 'application/json'})
