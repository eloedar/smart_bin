#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

TRIG = 11  # send-pin
ECHO = 12  # receive-pin


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO, GPIO.IN)


def distance():
    GPIO.output(TRIG, 1)  # 给Trig一个10US以上的高电平
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    # 等待低电平结束，然后记录时间
    while GPIO.input(ECHO) == 0:  # 捕捉 echo 端输出上升沿
        pass
    time1 = time.time()

    # 等待高电平结束，然后记录时间
    while GPIO.input(ECHO) == 1:  # 捕捉 echo 端输出下降沿
        pass
    time2 = time.time()

    during = time2 - time1
    # ECHO高电平时刻时间减去低电平时刻时间，所得时间为超声波传播时间
    return during * 340 / 2 * 100


# 超声波传播速度为340m/s,最后单位米换算为厘米，所以乘以100
def loop():
    while True:
        dis = distance()
        print(dis, 'cm')
        print('')
        time.sleep(0.3)


def destroy():
    GPIO.cleanup()


if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
