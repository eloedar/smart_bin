import time
from duo import loop
import duo
from hand_recognition import get_dis, detect
from gpiozero import LED

led = LED(9)
if __name__ == '__main__':
    while True:
        time.sleep(0.5)
        if get_dis() < 30:
            led.on()
            detect()
        else:
            led.off()
            loop()
            continue
