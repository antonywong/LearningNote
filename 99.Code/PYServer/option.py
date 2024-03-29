#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import threading
import win32gui
from pynput import keyboard

import config
import data_panel


def listenKeyboard():
    """监听键盘键入，按q退出
    """
    global __dataPanel, __isRunning, __currentWindowHandle
    with keyboard.Events() as events:
        for event in events:
            if __currentWindowHandle != win32gui.GetForegroundWindow():
                continue

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
__currentWindowHandle = win32gui.GetForegroundWindow()

args = sys.argv[1:]
if len(args) > 0 and args[0] in ['prd']:
    print('生成环境，更新基础数据...', end='')
    __dataPanel.update_option_info()
    print('DONE')
if len(args) > 0 and args[0] in ['prd', 'test']:
    threading.Thread(target=listenKeyboard).start()
    threading.Thread(target=collect).start()
if len(args) == 0:
    threading.Thread(target=listenKeyboard).start()
    print("test")
