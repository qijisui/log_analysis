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

def bond_state_change(arg):
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
        state1 = '{}'.format(' ')
        return state1

#bong state
def bond_state(log):
    pattern = re.compile(r'Bond State Change Intent:(\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}) OldState: (\d{1,2}) NewState: (\d{1,2})')
    state = pattern.search(log)
    if not state is None: 
        bd_OldState = bond_state_change(state.group(2)) 
        bd_NewState = bond_state_change(state.group(3)) 
        state2 = '{:^24}{}{:44}{:^24}'.format(state.group(1),'\n',' ',(bd_OldState+'>'+bd_NewState))
        return state2 
    else:
        state2 = '{}'.format(' ')
        return state2

#a2dp state
def a2dp_disconnected():
    return "CONNECTION_STATE_DISCONNECTED"

def a2dp_connecting():
    return "CONNECTION_STATE_CONNECTING"

def a2dp_connected():
    return "CONNECTION_STATE_CONNECTED"

def a2dp_disconnecting():
    return "CONNECTION_STATE_DISCONNECTING"

def a2dp_state_change(arg):
    switcher={
        '0':a2dp_disconnected,
        '1':a2dp_connecting,
        '2':a2dp_connected,
        '3':a2dp_disconnecting,
        None:lambda:"no"
    }
    func=switcher.get(arg,lambda:"no")
    return func()

def a2dp_state(log):
    pattern = re.compile(r'A2dpStateMachine: processConnectionEvent state = (\d{1})')
    state = pattern.search(log)
    if not state is None:
        ad_state = a2dp_state_change(state.group(1))
        ad_state = '{:^29}'.format(ad_state)
        return ad_state
    else:
        ad_state = '{}'.format(' ')
        return ad_state

#hfp state
def hfp_disconnected():
    return "CONNECTION_STATE_DISCONNECTED"

def hfp_connecting():
    return "CONNECTION_STATE_CONNECTING"

def hfp_connected():
    return "CONNECTION_STATE_CONNECTED"

def hfp_disconnecting():
    return "CONNECTION_STATE_DISCONNECTING"

def hfp_slc_connected():
    return "CONNECTION_STATE_SLC_CONNECTED"

def hfp_state_change(arg):
    switcher={
        '0':hfp_disconnected,
        '1':hfp_connecting,
        '2':hfp_connected,
        '3':hfp_slc_connected,
        '4':hfp_disconnecting,
        None:lambda:"no"
    }
    func=switcher.get(arg,lambda:"no")
    return func()

def hfp_state(log):
    pattern = re.compile(r'HeadsetStateMachine: processConnectionEvent state = (\d{1})')
    state = pattern.search(log)
    if not state is None:
        hf_state = hfp_state_change(state.group(1))
        hf_state = '{:^30}'.format(hf_state)
        return hf_state
    else:
        hf_state = '{}'.format(' ')
        return hf_state

#log process
def process(log):
    log_time = timestamp(log)
    bt_state = bluetooth_state(log)
    bd_state = bond_state(log)
    ad_state = a2dp_state(log)
    hf_state = hfp_state(log)

    if log_time != [] and bt_state != bd_state:
        w = open('log_analysis.txt','a+')
        out = '{}|{:24}|{:24}|{:29}|{:30}'.format(log_time[0],bt_state,bd_state,ad_state,hf_state)
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
        time.sleep(5)
    
    f = open('logcat.txt')
    print('*******Time*******|****Bluetooth State*****|*******bond state*******|**********a2dp state*********|***********hfp state***********|')
    line = f.readline()
    while line:
        log = line.strip()
        out = process(log)   
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


