#coding:utf-8
import os
import time
import re

def process(log):
    pattern = re.compile(r'MESSAGE_BLUETOOTH_STATE_CHANGE: ?(.+)')
    #conn_state = pattern.search(log,re.I)
    conn_state = pattern.findall(log)
    return conn_state

def screen():
    print("later")

def export():
    if not os.path.exists('logcat.txt'):
        print('Not exists file logcat.txt!')
        command = "adb logcat -d > logcat.txt"
        os.system(command)
    
    now	= time.strftime('%m%d%H%M%S')
    f = open('logcat.txt')
    w = open('./log_analysis_{}.txt'.format(now),'a+')
    line = f.readline()
    while line:
        log = line.strip()
        out = process(log)
        #if not out is None:
        if out != [] : 
            w.write(log+'\n')
            print(log)
            print(out[0])
        line = f.readline()
    w.close()
    f.close()
    
    print('log analysis has finished,please open log_analysis_{}.txt.'.format(now))

comment = input('please enter a comment [0:screen,1:file] --> ')
if comment == 0 :
    screen()
elif comment == 1:
    export()


