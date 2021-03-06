#coding:utf-8
import os
import time
import re
import sys

# log time 
def timestamp(log):
    pattern = re.compile(r'\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d{1,3}')
    time = pattern.findall(log)
    return time

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
def bong_none():
    return "none"

def bong_bonding():
    return "bonding"

def bong_bonded():
    return "bonded"

def bond_state_change(arg):
    switcher={
        '10':bong_none,
        '11':bong_bonding,
        '12':bong_bonded,
        None:lambda:"no"
    }
    func=switcher.get(arg,lambda:"no")
    return func()

def bond_state(log):
    pattern = re.compile(r'Bond State Change Intent:(\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}) OldState: (\d{1,2}) NewState: (\d{1,2})')
    state = pattern.search(log)
    if not state is None: 
        bd_OldState = bond_state_change(state.group(2)) 
        bd_NewState = bond_state_change(state.group(3)) 
        state2 = '{:^17}{}{:44}{:^17}'.format(state.group(1),'\n',' ',(bd_OldState+'-->'+bd_NewState))
        return state2 
    else:
        state2 = '{}'.format(' ')
        return state2

#a2dp state
def a2dp_disconnected():
    return "disconnected"

def a2dp_connecting():
    return "connecting"

def a2dp_connected():
    return "connected"

def a2dp_disconnecting():
    return "disconnecting"

def a2dp_playing():
    return "playing"

def a2dp_not_playing():
    return "not_playing"

def a2dp_state_change(arg):
    switcher={
        '0':a2dp_disconnected,
        '1':a2dp_connecting,
        '2':a2dp_connected,
        '3':a2dp_disconnecting,
        '10':a2dp_playing,
        '11':a2dp_not_playing,
        None:lambda:"no"
    }
    func=switcher.get(arg,lambda:"no")
    return func()

def a2dp_state(log):
    pattern = re.compile(r'A2dpStateMachine: Connection state (\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}): (\d{1})->(\d{1})')
    pattern_play = re.compile(r'A2dpStateMachine: A2DP Playing state : device: (\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}) State:(\d{2})->(\d{2})')
    state = pattern.search(log)
    play_state = pattern_play.search(log)
    if not state is None:
        ad_oldstate = a2dp_state_change(state.group(2))
        ad_newstate = a2dp_state_change(state.group(3))
        ad_state = '{}->{}'.format(ad_oldstate,ad_newstate)
        return ad_state
    elif not play_state is None:
        play_oldstate = a2dp_state_change(play_state.group(2))
        play_newstate = a2dp_state_change(play_state.group(3))
        play_state = '{}->{}'.format(play_oldstate,play_newstate)
        return play_state
    else:
        ad_state = '{}'.format(' ')
        return ad_state

#hfp state
def hfp_disconnected():
    return "disconnected"

def hfp_connecting():
    return "connecting"

def hfp_connected():
    return "connected"

def hfp_disconnecting():
    return "disconnecting"

def hfp_slc_connected():
    return "slc_connected"

def audio_mode_normal():
    return "normal"

def audio_mode_ringtone():
    return "ringtone"

def audio_mode_in_call():
    return "in_call"

def audio_mode_in_communication():
    return "in_communication"

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

def audio_state_change(arg):
    switcher={
        '0':audio_mode_normal,
        '1':audio_mode_ringtone,
        '2':audio_mode_in_call,
        '3':audio_mode_in_communication,
        '10':hfp_disconnected,
        '11':hfp_connecting,
        '12':hfp_connected,
        None:lambda:"no"
    }
    func=switcher.get(arg,lambda:"no")
    return func()

def hfp_state(log):
    pattern = re.compile(r'HeadsetStateMachine: Connection state (\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:) (\d{1})->(\d{1})|\
                            HeadsetStateMachine: broadcastConnectionState (\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:) (\d{1})->(\d{1})')
    pattern_audio = re.compile(r'HeadsetStateMachine: Audio state (\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:) (\d{2})->(\d{2})')
    pattern_mode = re.compile(r'setPhoneState(\D{1,2}) state (\d{1})')
    state = pattern.search(log)
    audio_state = pattern_audio.search(log)
    audio_mode = pattern_mode.search(log)
    if not state is None:
        hf_oldstate = hfp_state_change(state.group(2))
        hf_newstate = hfp_state_change(state.group(3))
        hf_state = '{}->{}'.format(hf_oldstate,hf_newstate)
        return hf_state
    elif not audio_state is None:
        audio_oldstate = audio_state_change(audio_state.group(2))
        audio_newstate = audio_state_change(audio_state.group(3))
        audio_state = 'Audio:{}->{}'.format(audio_oldstate,audio_newstate)
        return audio_state
    elif not audio_mode is None:
        audio_mode_t = audio_state_change(audio_mode.group(2))
        audio_mode_s = 'Audio Mode:{}'.format(audio_mode_t)
        return audio_mode_s
    else:
        hf_state = '{}'.format(' ')
        return hf_state

#avrcp
def keycode_play():
    return "play"

def keycode_pause():
    return "pause"

def keycode_stop():
    return "stop"

def keycode_next():
    return "next"

def keycode_previous():
    return "previous"

def keycode_rewind():
    return "rewind"

def keycode_play_pause():
    return "play_pause"

def keycode_fast_forward():
    return "fast_forward"

def keycode_volume_up():
    return "volume_up"

def keycode_volume_dowm():
    return "volume_down"

def keycode_event(arg):
    switcher={
        'KEYCODE_MEDIA_PLAY':keycode_play,
        'KEYCODE_MEDIA_PAUSE':keycode_pause,
        'KEYCODE_MEDIA_STOP':keycode_stop,
        'KEYCODE_MEDIA_NEXT':keycode_next,
        'KEYCODE_MEDIA_PREVIOUS':keycode_previous,
        'KEYCODE_MEDIA_REWIND':keycode_rewind,
        'KEYCODE_MEDIA_PLAY_PAUSE':keycode_play_pause,
        'KEYCODE_MEDIA_FAST_FORWARD':keycode_fast_forward,
        'KEYCODE_VOLUME_UP':keycode_volume_up,
        'KEYCODE_VOLUME_DOWN':keycode_volume_dowm,
        None:lambda:"no"
    }
    func=switcher.get(arg,lambda:"no")
    return func()

def avrcp(log):
    pattern = re.compile(r'recordKeyDispatched: KeyEvent { action=(\w.+), keyCode=(\w.+), scanCode')
    state = pattern.search(log)
    if not state is None:
        key = keycode_event(state.group(2))
        ctl_state = '{:^12}{}{:117}{:^12}'.format(state.group(1),'\n',' ',key)
        return ctl_state
    else:
        ctl_state = '{}'.format(' ')
        return ctl_state

#log process
def process(log):
    log_time = timestamp(log)
    bt_state = bluetooth_state(log)
    bd_state = bond_state(log)
    ad_state = a2dp_state(log)
    hf_state = hfp_state(log)
    ctl_state = avrcp(log)
    
    if log_time != [] and ((bt_state != ' ') or (bd_state != ' ') or (ad_state != ' ') or (hf_state != ' ') or (ctl_state != ' ')):
        #w = open('loga.txt','a+')
        out = '{}|{:24}|{:17}|{:^24}|{:29}|{:12}'.format(log_time[0],bt_state,bd_state,ad_state,hf_state,ctl_state)
        print(out)
        return out

def exit():
    print("later")

def export():
    if not os.path.exists('logcat.txt'):
        print('Could not find file logcat.txt!')
        print('Command: adb logcat -d > logcat.txt')
        command = 'adb logcat -d > logcat.txt'
        os.system(command)
        time.sleep(5)
    
    f = open('./logcat.txt')
    w = open('./loga_{}.txt'.format(now),'a+')
    sys.stdout.write('*******Time*******|****Bluetooth State*****|')
    sys.stdout.write('****bond state***|*******a2dp state*******|')
    sys.stdout.write('**********hfp state**********|***avrcp***|')
    w.write('*******Time*******|****Bluetooth State*****|')
    w.write('****bond state***|*******a2dp state*******|')
    w.write('**********hfp state**********|***avrcp***|')
    line = f.readline()
    while line:
        log = line.strip()
        out = process(log)
        if not out is None:
            w.write(out+'\n') #将结果写入到loga.txt
        line = f.readline()
    w.close()
    f.close()
    
    
now = time.strftime('%m%d%H%M%S')
print('The file to be processed should be named: logcat.txt')
command = input('please enter a command [1:continue,2:exit] --> ')
if command == 1 or command == "continue" :
    print(" 2")
    export()
    print('')
    print('Log analysis has finished,please open loga_{}.txt.'.format(now))
elif command == 2 or command == "exit" :
    exit()


