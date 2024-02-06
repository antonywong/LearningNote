# -*- coding: utf-8 -*-
import time
import option
from option import option_info, option_reminder, option_deal
import const


# 定义刷新控制台输出的函数
def refresh_output(messages):
    # 清空控制台输出
    print('\033c', end='')
    # 输出采集结果
    for m in messages:
        print(m)


df = None
# 定义定时调用采集程序的函数
def run_collector():
    global df
    while True:
        message = []
        current_time = time.localtime()
        current_time_str = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
        current_min = current_time.tm_hour * 100 + current_time.tm_min
        if current_time.tm_wday < 5 and (\
        930 < current_min and current_min <= 1130\
        or\
        1300 <= current_min and current_min < 1457\
        ):
            # 调用采集程序
            df = option_info.collect()
            # 保存当前分析结果
            option_info.record(df, current_time_str)
            # 输出分析结果
            message.extend(option_reminder.analyze(df))
            message.extend(option_deal.analyze(df))

            refresh_output(message)
        elif df is None:
            # 调用采集程序
            df = option_info.collect()
            # 输出分析结果
            message.extend(option_reminder.analyze(df))
            message.extend(option_deal.analyze(df))

            refresh_output(message)

        print(current_time_str, end="====", flush=True)
        # 等待一定时间后再次调用采集程序
        time.sleep(int(const.DICT["ANALYZE_RECORD_INTERVAL"]))


option_info.sync()


# 调用定时调用采集程序的函数，每15秒钟调用一次
run_collector()