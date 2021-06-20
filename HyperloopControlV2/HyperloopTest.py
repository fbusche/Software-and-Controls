import os
import sys
import time
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO
import numpy as np
from smbus2 import SMBus

a = False
brakePin = 2
startTime = datetime.now()
arduino4mega_ADDRESS = 7
arduinoODO_ADDRESS = 5
MIN_PWM = 0
MAX_PWM = 180

def pwm(value: int):
    with SMBus(1) as bus:
        bus.write_byte_data(arduino4mega_ADDRESS, 0, value)

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(brakePin, GPIO.OUT)
    GPIO.output(brakePin, GPIO.HIGH)
    pwm(MIN_PWM)

def deltaTime_Seconds():
        endTime = datetime.now()
        temp = str(endTime - startTime)
        temp2 = temp.split(":")
        seconds = (float(temp2[0]))*3600 + (float(temp2[1]))*60 + (float(temp2[2]))
        return(seconds)

def brake(state):
    if(state == True):
        GPIO.output(brakePin, GPIO.LOW)
    elif(state == False):
        GPIO.output(brakePin, GPIO.HIGH)

def stop():
    pwm(MIN_PWM)
    sleep(0.01)
    brake(True)
    print("brake Applied")

def go_direct(speed, time):
    startTime = datetime.now()
    pwm(speed)
    while True:
        print("Run Time: " + deltaTime_Seconds + " seconds")
        if(deltaTime_Seconds() >= time):
            stop()

def go_linear(speed, speed_increment, time):
    startTime = datetime.now()
    for i in range(start=MIN_PWM, stop=speed, step=speed_increment):
        print("Run Time: " + deltaTime_Seconds + " seconds")
        if(deltaTime_Seconds() >= time):
            stop()
            break
        if(i < MAX_PWM and i > MIN_PWM):
            pwm(i)
        elif(i > MAX_PWM):
            pwm(MAX_PWM)
        elif(i < MIN_PWM):
            pwm(MIN_PWM)
        sleep(0.05)
    

def go_exponential(speed, speed_increment, time):
    startTime = datetime.now()
    for i in range(start=MIN_PWM, stop=speed, step=speed_increment):
        print("Run Time: " + deltaTime_Seconds + " seconds")
        if(deltaTime_Seconds() >= time):
            stop()
            break
        if(i < MAX_PWM and i > MIN_PWM):
            pwm(i)
        elif(i > MAX_PWM):
            pwm(MAX_PWM)
        elif(i < MIN_PWM):
            pwm(MIN_PWM)
        sleep(0.05)

def readODO(address=arduinoODO_ADDRESS):
    with SMBus(1) as bus:
        data0 = bus.read_byte_data(address, 0)
        data1 = bus.read_byte_data(address, 1)
        data2 = bus.read_byte_data(address, 2)
        data3 = bus.read_byte_data(address, 3)
        return data0, data1, data2, data3
        

if __name__ == '__main__' and a == True:
	try:
		init()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("Terminating, Interupt or Error Occurred")
		stop()
		sys.exit(0)