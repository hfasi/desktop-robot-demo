# -*- coding: utf-8 -*-
# 连接按键串口，并接收串口数据

import serial
import time

NO_NEED_TO_HANDLE = "NO_NEED_TO_HANDLE"
IS_DEBUG = False
SERIAL_DATA_START = 1
SERIAL_DATA_STOP = 0

class SerialPort:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = None
        self.callback = None
        self.data_list = []
        self.is_running = False
        
    def register_callback(self, callback):
        self.callback = callback

    def open(self):
        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
            print(f"打开串口 {self.port}，波特率: {self.baud_rate}")
            self.is_running = True
            
            while self.is_running:
                if self.ser.in_waiting > 0:
                    raw_data = self.ser.read(self.ser.in_waiting)
                    wake_up_data = self.handle_data(raw_data)
                    if NO_NEED_TO_HANDLE != wake_up_data:
                        self.callback(wake_up_data)
                time.sleep(0.1)
        except serial.SerialException as e:
            print(f"串口错误: {e}")
        finally:
            self.close()
                
    def close(self):
        self.is_running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("关闭串口")
            
    def handle_data(self, data):
        serial_data_0 = "key,0\r\n"
        serial_data_1 = "key,1\r\n"
        
        if not isinstance(data, bytes):
            return NO_NEED_TO_HANDLE
        
        try:
            decode_data = data.decode('utf-8')
            if serial_data_0 == decode_data:
                return SERIAL_DATA_STOP
            elif serial_data_1 == decode_data:
                return SERIAL_DATA_START
            else:
                return NO_NEED_TO_HANDLE
        except UnicodeDecodeError:
            print("串口数据不是utf-8编码")
            return NO_NEED_TO_HANDLE
        
        
