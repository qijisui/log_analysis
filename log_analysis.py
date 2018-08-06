#coding:utf-8
import os
import time
import re
# log time 
def timestamp(log):
    pattern = re.compile(r'\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d{1,3}')
    time = pattern.findall(log)
    return time

#bong state transition
def bong_none():
    return "BOND_NONE"

def bong_boning():
    return "BOND_BONDING"

def bong_bonded():
    return "BOND_BONDED"

def state_change(arg):
    switcher={
        '10':bong_none,
        '11':bong_boning,
        '12':bong_bonded,
        None:lambda:"no"
    }
    func=switcher.get(arg,lambda:"no")
    return func()

#bluetooth state
global state1
state1 = 'a'
def bluetooth_state(log):
    pattern = re.compile(r'MESSAGE_BLUETOOTH_STATE_CHANGE: ?(.+)')
    #conn_state = pattern.search(log,re.I)
    state = pattern.search(log)   
    if not state is None:
        state1= '{:^24}'.format(state.group(1))  
        return state1
    else:
        state1 = '{:24}'.format(' ')
        return state1

#bong state
def bond_state(log):
    pattern = re.compile(r'Bond State Change Intent:(\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}) OldState: (\d{1,2}) NewState: (\d{1,2})')
    state = pattern.search(log)
    if not state is None: 
        bd_OldState = state_change(state.group(2)) 
        bd_NewState = state_change(state.group(3)) 
        state2 = '{:^24}{}{:44}{:^24}'.format(state.group(1),'\n',' ',(bd_OldState+'>'+bd_NewState))
        return state2 
    else:
        state2 = '{:24}'.format(' ')
        return state2

def process(log):
    log_time = timestamp(log)
    bt_state = bluetooth_state(log)
    bd_state = bond_state(log)
    if log_time != [] and bt_state != bd_state:
        w = open('log_analysis.txt','a+')
        out = '{}|{}|{}|'.format(log_time[0],bt_state,bd_state)
        print(out)
        #w = open('./log_analysis_{}.txt'.format(now),'a+')
        w.write(out+'\n')
        w.close()

def exit():
    print("later")

def export():
    if not os.path.exists('logcat.txt'):
        print('Could not find file logcat.txt!')
        print('Command: adb logcat -d > logcat.txt')
        command = 'adb logcat -d > logcat.txt'
        os.system(command)
        time.sleep(3)
    
    f = open('logcat.txt')
    print('*******Time*******|****Bluetooth State*****|*******bond state*******|')
    line = f.readline()
    while line:
        log = line.strip()
        out = process(log)
        #print out[0]
        #out1 = bond_state(log)
        #print out
    #    if not out1 is None:
    #        print out1[0]
        #if out != []:
        #    print('{}|{}'.format(out[0],out[1]))
        #     
        line = f.readline()
    f.close()
    
    
now	= time.strftime('%m%d%H%M%S')
print('The file to be processed should be named logcat.txt.')
command = input('please enter a command [1:continue,2:exit] --> ')
if command == 1 or command == "continue" :
    export()
    print''
    print('Log analysis has finished,please open log_analysis_{}.txt.'.format(now))
elif command == 2 or command == "exit" :
    exit()


