import time
from time import sleep
from RPi import GPIO

servo_pin = 19  # 舵机信号线接树莓派GPIO19
TRIG = 2  # send-pin
ECHO = 3  # receive-pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(servo_pin, GPIO.OUT, initial=False)
p = GPIO.PWM(servo_pin, 50)  # 初始频率为50HZ


# 旋转角度转换到PWM占空比
def angleToDutyCycle(angle):
    return 2.5 + angle / 180.0 * 10


def open_top():
    p.start(angleToDutyCycle(100))  # 舵机初始化角度为90
    sleep(3)
    p.ChangeDutyCycle(0)


def close_top():
    p.start(angleToDutyCycle(0))
    sleep(1)
    p.ChangeDutyCycle(0)


# 超声波测距函数
def get_dis():
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
    # if random.random() > 0.5:
    print("get" + str(during * 340 / 2 * 100))
    return during * 340 / 2 * 100
