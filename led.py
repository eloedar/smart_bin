import RPi.GPIO as GPIO
from gpiozero import LED
led = LED(5)
led.on()