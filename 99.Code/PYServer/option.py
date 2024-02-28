#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import threading
from pynput import keyboard

import config
import data_panel
from stock import monitorD, monitor05, tdx, kd, k05, kw, k30, high_low
from crawler import etf_option, cffex_option


def listenKeyboard():
    """监听键盘键入，按q退出，按t测试
    """
    global __dataPanel, __isRunning
    with keyboard.Events() as events:
        for event in events:
            if isinstance(event, keyboard.Events.Release):
                try:
                    if event.key == keyboard.KeyCode.from_char('q'):
                        __isRunning = False
                        print('退出{}'.format(event))
                        break
                    elif event.key == keyboard.Key.left:
                        __dataPanel.render(-1)
                    elif event.key == keyboard.Key.right:
                        __dataPanel.render(1)
                    elif event.key == keyboard.Key.up:
                        __dataPanel.render(0, -1)
                    elif event.key == keyboard.Key.down:
                        __dataPanel.render(0, 1)
                    elif event.key == keyboard.KeyCode.from_char('t'):
                        print("test")
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
    global __dataPanel, __isRunning
    while __isRunning:
        __dataPanel.collect()
        __dataPanel.render()
        # 等待一定时间后再次调用采集程序
        time.sleep(config.analyzeRecordInterval)


__dataPanel = data_panel
__isRunning = True

args = sys.argv[1:]
if args[0] in ['prd']:
    print('生成环境，更新基础数据...', end='')
    __dataPanel.update_option_info()
    print('DONE')
if args[0] in ['prd', 'test']:
    threading.Thread(target=listenKeyboard).start()
    threading.Thread(target=collect).start()
else:
    print("test")

# df = None
# # 定义定时调用采集程序的函数
# def run_collector():
#     global df
#     while True:
#         message = []
#         current_time = time.localtime()
#         current_time_str = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
#         current_min = current_time.tm_hour * 100 + current_time.tm_min
#         if current_time.tm_wday < 5 and (\
#         930 < current_min and current_min <= 1130\
#         or\
#         1300 <= current_min and current_min < 1457\
#         ):
#             # 调用采集程序
#             df = option_info.collect()
#             # 保存当前分析结果
#             option_info.record(df, current_time_str)
#             # 输出分析结果
#             message.extend(option_reminder.analyze(df))
#             message.extend(option_deal.analyze(df))

#             refresh_output(message)
#         elif df is None:
#             # 调用采集程序
#             df = option_info.collect()
#             # 输出分析结果
#             message.extend(option_reminder.analyze(df))
#             message.extend(option_deal.analyze(df))

#             refresh_output(message)

#         print(current_time_str, end="====", flush=True)
#         # 等待一定时间后再次调用采集程序
#         time.sleep(int(const.DICT["ANALYZE_RECORD_INTERVAL"]))


# option_info.sync()
