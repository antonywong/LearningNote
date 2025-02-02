#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import threading


class minterpolate_thread(threading.Thread):

    def __init__(self, path, filename, fps):
        super().__init__()
        self._path = path
        self._filename = filename
        self._fps = fps

    def run(self):
        file = os.path.join(self._path, self._filename)
        cmd = 'ffmpeg '
        cmd += '-i "%s" -vcodec libx265 -acodec aac ' % file
        cmd += '-strict -2 -q:v 1 '
        cmd += '-vf "mpdecimate=0,minterpolate=\'fps=%s\':' % self._fps
        cmd += 'mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" '
        cmd += '-x265-params crf=15:tu-intra-depth=4:tu-inter-depth=4:max-tu-size=16:'
        cmd += 'me=umh:merange=48:subme=5:max-merge=4:ref=3:min-keyint=5:keyint=720:bframes=16:b-adapt=2:radl=3:bframe-bias=20:'
        cmd += 'crqpoffs=-4:cbqpoffs=-2:ipratio=1.6:pbratio=1.3:psy-rdoq=2.3:rdoq-level=2:aq-strength=0.9:qg-size=8:'
        cmd += 'rd=3:limit-refs=1:rskip=1:rc-lookahead=150:psy-rd=1.5:rdpenalty=2:deblock=0,-1:hash=2 '
        cmd += '-pix_fmt yuv420p10le '
        cmd += '"%s.ts"' % file
        # print(cmd)
        subprocess.getoutput(cmd, errors='ignore')
        print('完成：%s' % file)
