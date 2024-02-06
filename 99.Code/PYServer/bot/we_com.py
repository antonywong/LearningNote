# -*- coding: utf-8 -*-
import requests
from typing import Dict, List, Tuple


headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "qyapi.weixin.qq.com",
    "Pragma": "no-cache",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
}


def send_message(bot_key: str, message: str):
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot_key}"
    data = f'{{"msgtype":"text","text":{{"content":"{message}"}}}}'.encode("utf-8")
    r = requests.post(url, data)
    data_json = r.json()
    return data_json