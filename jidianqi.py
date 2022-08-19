#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

makerobo_RelayPin = 4
makerobo_RelayPin2 = 26

GPIO.setmode(GPIO.BCM)  # 采用实际的物理管脚模式
# GPIO.setwarning(False)          # 去除GPIO警告
GPIO.setup(makerobo_RelayPin, GPIO.OUT)  # 设置Pin模式为输出模式
GPIO.output(makerobo_RelayPin, GPIO.LOW)  # 关闭继电器
GPIO.setup(makerobo_RelayPin2, GPIO.OUT)  # 设置Pin模式为输出模式
GPIO.output(makerobo_RelayPin2, GPIO.LOW)  # 关闭继电器


# 循环函数
def makerobo_loop():
    click = 0;  # 俺当做节拍器来用
    GPIO.output(makerobo_RelayPin, GPIO.HIGH)
    GPIO.output(makerobo_RelayPin2, GPIO.HIGH)
    time.sleep(0.5)  # 延时500ms
        # 继电器关闭



# 释放资源
def makerobo_destroy():
    GPIO.output(makerobo_RelayPin, GPIO.LOW)  # 关闭继电器
    GPIO.output(makerobo_RelayPin2, GPIO.LOW)
    #GPIO.cleanup()  # 释放资源


# # 程序入口
# if __name__ == '__main__':
#
#     try:
#         makerobo_loop()  # 调用循环函数
#     except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
#         makerobo_destroy()  # 释放资源
