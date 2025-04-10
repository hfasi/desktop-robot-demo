#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 交互main文件
# 连接按键串口，监听按键信息

import threading
import time
import serial_port
from recorder_sd import *
import wave
import threading
import sys
import os
from datetime import datetime
import json
import pyaudio
import json
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import utils_speech
from utils_speech import *
import utils_vlm

PIC_PATH = "egg_bowl.jpg"
AUDIO_PATH = "output.wav"
recorder = AudioRecorder()

# SERIAL_PORT_NUMBER = "/dev/ttyTHS4"
SERIAL_PORT_NUMBER = "/dev/ttyUSB0"
BAUD_RATE = 9600

sys.path.append('/home/rob/ros2/hall_robot')
 

def serial_callback(data):
    """ 接收按键串口数据 """
    print("serial data: " + str(data))
    print(f"recorder is recording: {recorder.is_recording}")
    if serial_port.SERIAL_DATA_START == data and not recorder.is_recording: 
        recorder.start_record()
    elif serial_port.SERIAL_DATA_STOP == data and recorder.is_recording:
        recorder.stop_record()
        # recorder.save()
        # 判断音频是否录制成功
        length = os.path.getsize(AUDIO_PATH)
        if length < 44:
            utils_speech.tts("不好意思，我没听清呢")
        else:
            utils_speech.tts("好的，我开始思考了")
            asr(AUDIO_PATH, asr_success_callback, asr_error_callback)

rk3328 = serial_port.SerialPort(SERIAL_PORT_NUMBER, BAUD_RATE)
rk3328.register_callback(serial_callback)
serial_thread = threading.Thread(target=rk3328.open)

def start():
    print("inter llm start. serial + asr + llm + tts start.")
    serial_thread.start()
    try:
        while True:
            time.sleep(1)  # 主线程保持运行，但不做任何操作
    except KeyboardInterrupt:
        print("程序终止")
        rk3328.close()
        serial_thread.join()   
        
def stop():
    print("inter llm stop.")
    rk3328.close() 
    serial_thread.join()             
                
                
def asr_success_callback(result):
    print(f"ASR success: {result}")
    try: 
        utils_vlm.ling_yi_vlm(gpt_callback, result[0], PIC_PATH)
    except Exception as e:
        print(f"ASR error: {e}")
        utils_speech.tts("不好意思，出现了一点小问题，正在努力，请给我一点时间")

def asr_error_callback(error):
    print(f"ASR error: {error}")
    utils_speech.tts("不好意思，我没听清呢")
    
def gpt_callback(result):
    print(f"GPT success: {result}")
    parse_response(result)
    
def parse_response(result):
    try:
        parsed_data = json.loads(result)
        start = parsed_data["start"]
        end = parsed_data["end"]
        response = parsed_data["response"]
        call_action(start, end)
        print("response vision:", response)
        utils_speech.tts(response)
    except ValueError as e:
        print(f"response language: {result}")
        utils_speech.tts(result)

def call_action(start, end):
    if detect_learned(start, end):
        print(f"call_action, start: {start}, end: {end}")
        print(f"此处调用团队其他成员开发的接口，进行{start}的位置坐标识别，识别到坐标后，将此坐标传给团队另外成员，进行机械臂路径规划，进行抓取。")
        
    
def detect_learned(start, end):
    """ 判断是否是已经学会的物体 """
    items = ["cola", "water", "screwdriver", "egg", "bowl", "lemon", ""]
    if (start not in items) or (end not in items):
        utils_speech.tts("不好意思，这个我还没学会呢，换一个试试")
        print(f"detect learned: {start} or {end} is not in items")
        return False
    else:
        return True
    

def main3():
    print("程序开始，请按 'S' 开始录音，'T' 停止录音，或 'Q' 退出程序")
    while True:
        try:
            key = input().strip().upper()
            if key == 'S':
                recorder.start_record()
            elif key == 'T':
                recorder.stop_record()
                # recorder.save()
                asr(AUDIO_PATH, asr_success_callback, asr_error_callback)
            elif key == 'Q':
                print("退出程序")
                break
            else:
                print("无效的输入，请按 'S' 开始录音，'T' 停止录音，或 'Q' 退出程序")
        except KeyboardInterrupt:
            print("\n程序被中断")
            break


from playsound import playsound
from utils_net import *

PATH_NET_ERROR = 'net_error.mp3'

def detect_network_status():
    if not is_connected():
        playsound(PATH_NET_ERROR)
    


if __name__ == '__main__':
    main3()
    
    
    
    
    