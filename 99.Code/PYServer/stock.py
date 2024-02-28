#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from stock import monitorD, monitor05, tdx, kd, k05, kw, k30, high_low

kd.syn()
def printHelp():
    print('exit:退出')
    print('m:监控五分钟K线')
    print('tdx:从通达信获取完整五分钟K线')
    print('kd:获取最新日K线')
    print('k05:获取最新五分钟K线')
    print('hl:计算高低值')
    print('ma:计算均值')
    print('maa:均值缠论分析')

while True:
    printHelp()
    print('input com:')
    com = input()

    if com == "help":
        printHelp()
    elif com == "exit":
        break
    elif com == "m":
        monitor05.syn(False)
    elif com == "tdx":
        tdx.syn()
    elif com == "kd":
        monitorD.syn(datetime.strftime(datetime.now(), "%Y-%m-%d"))
    elif com == "k05":
        k05.syn()
    elif com == "hl":
        high_low.syn()
    # elif com == "ma":
    #     stockMA.syn("W")
    #     stockMA.syn("D")
    #     stockMA.syn("30")
    #     stockMA.syn("05")

    print('')
