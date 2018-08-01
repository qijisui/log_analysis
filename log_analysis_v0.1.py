#coding:utf-8
import os
import time
import re
from numpy import *

def screen():
    print("later")

def bluetooth_log(log):
    bt = re.search(r'a2dp',log,re.I)
    return bt

def access_file():
    if not os.path.exists('logcat.txt'):
        print('Not exists file logcat.txt!')
        command = "adb logcat -d > logcat.txt"
        os.system(command)
    
    f = open('logcat.txt')
    line = f.readline()
    while line:
        log = line.strip()
        out = bluetooth_log(log)
        if not out is None:
            now	= time.strftime('%m%d%H%M%S')
            w = open('./log_analysis_{}.txt'.format(now),'a+')
            w.write(log+'\n')
            #print(log)
        line = f.readline()
    f.close()
    w.close()
    print('log analysis has finished,please open log_analysis_{}.txt.'.format(now))

comment = input('please enter a comment [0:screen,1:file] --> ')
if comment == 0 :
    screen()
elif comment == 1:
    access_file()


