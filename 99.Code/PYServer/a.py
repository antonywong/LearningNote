# -*- coding: utf-8 -*-
import time
import const
import pandas as pd
from arbitrage import info


# 定义刷新控制台输出的函数
def refresh_output(price_order):    
    # 清空控制台输出
    # print('\033c', end='')

    field_list = ['价位', '名称', '可做多空', '升贴水']
    df = pd.DataFrame(price_order, columns=field_list)
    df = df.set_index(['升贴水', '可做多空'])
    df = df.sort_index(ascending=[False, True])
    df = df.reset_index()

    df.insert(2, '标记', '·')
    call_index = df.loc[df['可做多空'] == '空'].first_valid_index()
    put_index = df.loc[df['可做多空'] == '多'].last_valid_index()
    df.loc[call_index, '标记'] = '㊣'
    df.loc[put_index, '标记'] = '㊣'
    #styler = df.style.apply(lambda x: ['background: yellow' if x.name in [first_one,last_one] else '' for i in x], axis=1)

    print(df)


price_order = None
# 定义定时调用采集程序的函数
def run_collector():
    global price_order
    while True:
        current_time = time.localtime()
        current_time_str = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
        current_min = current_time.tm_hour * 100 + current_time.tm_min
        try:
            if current_time.tm_wday < 5 and (\
            930 < current_min and current_min <= 1130\
            or\
            1300 <= current_min and current_min < 1457\
            ):
                # 调用采集程序
                price_order = info.collect()
                # 保存当前分析结果
                info.record(price_order)

                refresh_output(price_order)
            elif not price_order:
                # 调用采集程序
                price_order = info.collect()

                refresh_output(price_order)

            print(current_time_str, end="====", flush=True)
        except:
            time.sleep(30)
            print('挂了', flush=True)
            print(current_time_str, end="====", flush=True)

        # 等待一定时间后再次调用采集程序
        time.sleep(int(const.DICT["ANALYZE_RECORD_INTERVAL"]))


info.sync()

# 调用定时调用采集程序的函数，每15秒钟调用一次
run_collector()