#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import threading
from pynput import keyboard

import config
import data_panel
from stock import monitorD, monitor05, tdx, kd, k05, kw, k30, high_low
from crawler import etf_option, cffex_option


def listenKeyboard():
    """监听键盘键入，按q退出，按u更新基础数据，按t测试
    """
    global __isRunning, __dataPanel
    with keyboard.Events() as events:
        for event in events:
            if isinstance(event, keyboard.Events.Release):
                try:
                    if event.key == keyboard.KeyCode.from_char('q'):
                        __isRunning = False
                        print('退出{}'.format(event))
                        break
                    elif event.key == keyboard.KeyCode.from_char('u'):
                        print('更新数据...', end='')
                        __dataPanel.update_option_info()
                        print('DONE')
                    elif event.key == keyboard.Key.left:
                        __dataPanel.rander(-1)
                    elif event.key == keyboard.Key.right:
                        __dataPanel.rander(1)
                    elif event.key == keyboard.KeyCode.from_char('t'):
                        test = cffex_option.get_price('ho2402')
                        print(test)
                    else:
                        #print(event)
                        continue
                except Exception as e:
                    print(e)
            elif isinstance(event, keyboard.Events.Press):
                continue


def collect():
    """定义定时调用采集程序的函数
    """
    global __isRunning
    while __isRunning:
        print('collect')
        # 等待一定时间后再次调用采集程序
        time.sleep(config.analyzeRecordInterval)


__dataPanel = data_panel
__isRunning = True
threading.Thread(target=listenKeyboard).start()
# threading.Thread(target=collect).start()

# kd.syn()
# def printHelp():
#     print('exit:退出')
#     print('m:监控五分钟K线')
#     print('tdx:从通达信获取完整五分钟K线')
#     print('kd:获取最新日K线')
#     print('k05:获取最新五分钟K线')
#     print('hl:计算高低值')
#     print('ma:计算均值')
#     print('maa:均值缠论分析')

# while True:
#     printHelp()
#     print('input com:')
#     com = input()

#     if com == "help":
#         printHelp()
#     elif com == "exit":
#         break
#     elif com == "m":
#         monitor05.syn(False)
#     elif com == "tdx":
#         tdx.syn()
#     elif com == "kd":
#         monitorD.syn(datetime.strftime(datetime.now(), "%Y-%m-%d"))
#     elif com == "k05":
#         k05.syn()
#     elif com == "hl":
#         high_low.syn()
#     elif com == "ma":
#         stockMA.syn("W")
#         stockMA.syn("D")
#         stockMA.syn("30")
#         stockMA.syn("05")

#     print('')
