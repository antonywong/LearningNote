#encoding:gbk

import requests
import json


def init(C):
	C.test = 1
	C.account = "118000007553"
	C.server_url = "http://10.10.10.17:5000"
	C.underlying = "sz159915"
	C.expire_month = "2503"

	url = C.server_url + "/v1/api/option/code"
	params = {"underlying": C.underlying, "expire_month": C.expire_month}
	r = requests.get(url, params=params, timeout=2.5)
	data_json = r.json()
	C.stock_list = [code+".SZO" if code[0]=="9" else code+".SHO" for code in data_json]
	print(C.stock_list)

def handlebar(C):
	if not C.is_last_bar():
		return

	print("handlebar:", end="\t")

	try:
		etf_code = C.underlying[2:] + "." + C.underlying[0:2].upper()
		underlying_tick = C.get_full_tick([etf_code])
		tick = C.get_full_tick(C.stock_list)
		url = C.server_url + "/v1/api/tick/qmt"
		body = {
			"underlying": C.underlying,
			"underlying_price": underlying_tick[etf_code]["lastPrice"],
			"expire_month": C.expire_month,
			"tick": tick }
		r = requests.post(url, json.dumps(body), headers={'Content-Type': 'application/json'}, timeout=2.5)
		data_json = r.json()
		if data_json:
			print(data_json)
			return
		else:
			print("tick posted!")



		accounts=get_trade_detail_data(C.account, "STOCK_OPTION", "ACCOUNT")
		print('查询账号结果：', end="\t")
		for dt in accounts:
			print(f'总资产: {dt.m_dBalance:.2f}, 净资产: {dt.m_dAssureAsset:.2f}, 总市值: {dt.m_dInstrumentValue:.2f}', 
			f'总负债: {dt.m_dTotalDebit:.2f}, 可用金额: {dt.m_dAvailable:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')
		
		positions = get_trade_detail_data(C.account, "STOCK_OPTION", 'position')
		print('查询持仓结果：', end="\t")
		for dt in positions:
			print(f'股票代码: {dt.m_strInstrumentID}, 市场类型: {dt.m_strExchangeID}, 证券名称: {dt.m_strInstrumentName}, 持仓量: {dt.m_nVolume}, 可用数量: {dt.m_nCanUseVolume}',
			f'成本价: {dt.m_dOpenPrice:.2f}, 市值: {dt.m_dInstrumentValue:.2f}, 持仓成本: {dt.m_dPositionCost:.2f}, 盈亏: {dt.m_dPositionProfit:.2f}')

		orders = get_trade_detail_data(C.account, "STOCK_OPTION", 'order')
		print('查询委托结果：', end="\t")
		for o in orders:
			print(f'股票代码: {o.m_strInstrumentID}, 市场类型: {o.m_strExchangeID}, 证券名称: {o.m_strInstrumentName}, 买卖方向: {o.m_nOffsetFlag}',
			f'委托数量: {o.m_nVolumeTotalOriginal}, 成交均价: {o.m_dTradedPrice}, 成交数量: {o.m_nVolumeTraded}, 成交金额:{o.m_dTradeAmount}')

		url = C.server_url + "/v1/api/_05/qmt"
		body = {
			"test": C.test,
			"balance": accounts[0].m_dBalance,
			"positions": {},
			"underlying": C.underlying,
			"expire_month": C.expire_month }
		r = requests.post(url, json.dumps(body), headers={'Content-Type': 'application/json'}, timeout=2.5)
		data_json = r.json()
		print(data_json)
		if data_json["msg"]:
			print(data_json["msg"])
			return
		else:
			print("strategy run!")



	except Exception as e:
		print(f"{e}")
		return
