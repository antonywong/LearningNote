# -*- coding: utf-8 -*-

import random
import time

def generate_data():
    """生成当前时间和随机数据"""
    current_time = time.strftime("%H:%M:%S", time.localtime())
    y_value = random.randint(1, 100)
    return current_time, y_value

