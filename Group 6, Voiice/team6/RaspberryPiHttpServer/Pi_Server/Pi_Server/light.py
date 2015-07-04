#!/usr/bin/env python
import time, RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

while 1:
    GPIO.output(4, 0)


  
