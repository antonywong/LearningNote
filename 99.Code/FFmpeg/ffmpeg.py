#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import threading
import minterpolate

__ffmpeg = "ffmpeg"
__file_path = ""
__temp_path = ""
__targ_path = ""
__thread_num = 0
__target_fps = 59.94

def run():
    global __ffmpeg, __file_path, __temp_path, __targ_path, __thread_num, __target_fps

    # 参数check
    args = sys.argv[1:]
    if len(args) < 4:
        print('缺少参数:1视频路径,2临时路径,3临时路径,4线程数')
        return
    __file_path = args[0][1:-1]
    print('视频路径: ', __file_path)
    __temp_path = args[1][1:-1]
    print('临时路径: ', __temp_path)
    __targ_path = args[2][1:-1]
    print('目标路径: ', __targ_path)
    __thread_num = int(args[3])
    print('线程数: ', __thread_num)
    print('----------------------------------------------------------------------------')

    # 获取视频分辨率与时长
    cmd = 'ffprobe -v error -select_streams v:0 -show_entries format=duration:stream=coded_width,coded_height -of default=noprint_wrappers=1:nokey=1 "%s"' \
        % __file_path
    print(cmd)
    result = subprocess.getoutput(cmd) # 执行命令，并返回输出结果
    duration = float(result.split("\n")[2])
    print(result)
    print('----------------------------------------------------------------------------')

    # 清空临时文件夹
    try:
        clear(__temp_path)
    except Exception as e:
        print('删除失败: %s' % (e))
        return
        
    # 分割视频
    seg_time = int(duration / __thread_num) + 1
    cmd = 'ffmpeg -hwaccel d3d11va -i "%s" -f segment -segment_time %s -vcodec copy -acodec copy -reset_timestamps 1 "%s\\%%04d.mp4"' \
        % (__file_path, seg_time, __temp_path)
    print(cmd)
    subprocess.getoutput(cmd, errors='ignore') # 执行命令，并返回输出结果
    all_temp_filename = os.listdir(__temp_path)
    print(all_temp_filename)
    print('----------------------------------------------------------------------------')

    # 创建线程列表
    threads = []    
    # 创建并启动线程
    for i in range(len(all_temp_filename)):
        thread = minterpolate.minterpolate_thread(__temp_path, all_temp_filename[i], __target_fps)
        threads.append(thread)
        thread.start()    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    print('----------------------------------------------------------------------------')
    
    # 合并视频
    changed_file = [os.path.join(__temp_path, s + '.ts') for s in all_temp_filename]  
    cmd = 'ffmpeg -y -i "concat:%s" -vcodec copy -acodec copy "%s"' \
        % ("|".join(changed_file), __targ_path)
    print(cmd)
    subprocess.getoutput(cmd, errors='ignore')
    print('合并完成')
    print('----------------------------------------------------------------------------')

    # 清空临时文件夹
    try:
        clear(__temp_path)
    except Exception as e:
        print('删除失败: %s' % (e))
        return
    print('DONE', end='')

def clear(temp_path):
    # 清空临时文件夹
    for filename in os.listdir(temp_path):
        temp_file = os.path.join(temp_path, filename)
        os.remove(temp_file)


run()