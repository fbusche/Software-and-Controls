#imports
import os
import sys
import time
from time import sleep
from datetime import datetime
import keyboard
import RPi.GPIO as GPIO
import numpy as np
import threading
from smbus2 import SMBus
from tkinter import messagebox

#GLOBAL VARIABLES
arduino1ctData = [0,0,0,0,0,0]
arduino2ctData = [0,0,0,0,0,0]
arduino3odData = [0,0,0,0]
arduino1ct_ADDRESS = 4
arduino2ct_ADDRESS = 5
arduino3ct_ADDRESS = 6




class HyperloopControlV2:
    def __init__(self):
        self.esc = ESC()
        self.startTime = datetime.now()
        self.trackLength = 100       #meters
        self.brakingDistance1 = 0    #meters, distance it takes to break
        self.brakingDistance2 = 0    #meters, distance it takes to break
        self.deceleration = 20       #m/s/s, how quickly we can slow down
        self.maxTemp = 40            #celsius
        self.maxCurrent = 100        #amps
        self.optimalCurrent = 10     #amps
        self.maxRunTime = 3.0        #seconds
        self.brakePin = 2            #braking solenoid control pin
        self.setRate = 0
        self.MIN_VALUE = 0
        self.MAX_VALUE = 180
        self.arduino4mega_ADDRESS = 7
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(brakePin, GPIO.OUT)
        GPIO.output(self.brakePin, GPIO.LOW)

    def deltaTime_Seconds(self):
        endTime = datetime.now()
        temp = str(endTime - self.startTime)
        temp2 = temp.split(":")
        seconds = (float(temp2[0]))*3600 + (float(temp2[1]))*60 + (float(temp2[2]))
        return(seconds)

    def system_check(self):  #Returns TRUE when everything is good
        global arduino1ctData, arduino2ctData, arduino3odData
        print("Press ENTER if Arduino 1 (CT) is working, Press ESC if not working")
        while True:
            print(arduino1ctData)
            sleep(0.5)
            if keyboard.is_pressed("enter"):
                break
            elif keyboard.is_pressed("esc"):
                return False

        print("Press ENTER if Arduino 2 (CT) is working, Press ESC if not working")
        while True:
            print(arduino2ctData)
            sleep(0.5)
            if keyboard.is_pressed("enter"):
                break
            elif keyboard.is_pressed("esc"):
                return False

        print("Press ENTER if Arduino 3 (OD) is working, Press ESC if not working")
        while True:
            print(arduino3odData)
            sleep(0.5)
            if keyboard.is_pressed("enter"):
                break
            elif keyboard.is_pressed("esc"):
                return False

        print("Press ENTER to disengage brakes")
        while True:
            if keyboard.is_pressed("enter"):
                GPIO.output(self.brakePin, GPIO.HIGH)
                break
        print("Press ENTER if brakes are working, else press ESC")
        while True:
            if keyboard.is_pressed("enter"):
                GPIO.output(self.brakePIN, GPIO.LOW)
                print("Breaks engaged, will disengage when armed")
                break
            elif keyboard.is_pressed("esc"):
                print("Issue with breaking system")
                return False

        return True


    def failsafe(self):
        global arduino1ctData, arduino2ctData, arduino3odData

        self.brakingDistance1 = (arduino1odData[2]**2) / (2*self.deceleration)
        self.brakingDistance2 = (arduino1odData[3]**2) / (2*self.deceleration)

        if(arduino3odData[0] >= (self.trackLength - self.brakingDistance1) or arduino3odData[1] >= (self.trackLength - self.brakingDistance2)):
            return False
        elif(arduino1ctData[0] >= self.maxTemp or arduino1ct[1] >= self.maxTemp or arduino2ct[0] >= self.maxTemp or arduino2ct[1] >= self.maxTemp):
            return False
        elif(arduino1ctData[2] >= self.maxCurrent or arduino1ctData[3] >= self.maxCurrent or arduino1ctData[4] >= self.maxCurrent or 
           arduino1ctData[5] >= self.maxCurrent or arduino2ctData[2] >= self.maxCurrent or arduino2ctData[3] >= self.maxCurrent or 
           arduino2ctData[4] >= self.maxCurrent or arduino2ctData[5] >= self.maxCurrent):
            return False
        elif(deltaTime_Seconds() >= self.maxRunTime):
            return False
        elif keyboard.is_pressed(" "):
            return False
        else:
            return True

    def go(self):
        global arduino1ctData, arduino2ctData, arduino3odData
        if(arduino1ctData[2] >= self.optimalCurrent and arduino1ctData[3] >= self.optimalCurrent and arduino1ctData[4] >= self.optimalCurrent and 
           arduino1ctData[5] >= self.optimalCurrent and arduino2ctData[2] >= self.optimalCurrent and arduino2ctData[3] >= self.optimalCurrent and 
           arduino2ctData[4] >= self.optimalCurrent and arduino2ctData[5] >= self.optimalCurrent):
            self.setRate -= 1

        elif(arduino1ctData[2] <= self.optimalCurrent and arduino1ctData[3] <= self.optimalCurrent and arduino1ctData[4] <= self.optimalCurrent and 
             arduino1ctData[5] <= self.optimalCurrent and arduino2ctData[2] <= self.optimalCurrent and arduino2ctData[3] <= self.optimalCurrent and 
             arduino2ctData[4] <= self.optimalCurrent and arduino2ctData[5] <= self.optimalCurrent):
            self.setRate += 1
        
        if(self.setRate > 180):
            self.setRate = 180
        if(self.setRate < 0):
            self.setRate = 0

        pwm(self.setRate)

    def stop(self):
        self.setRate = 0
        pwm(self.setRate)
        GPIO.output(self.brakePin, GPIO.LOW)

    def pwm(self, value: int):
        with SMBus(1) as bus:
            bus.write_byte_data(self.arduino4mega_ADDRESS, 0, value)

    def calibrate(self):
        print("-------RUNNING CALIBRATION SEQUENCE-------")
        print("DISENGAGING BRAKES")
        GPIO.output(self.brakePin, GPIO.LOW)
        pwm(self.MAX_VALUE)
        print("PWM set to HGH")
        print("Connect the motors, then press ENTER")
        while True:
            if keyboard.is_pressed("enter"):
                break
        pwm(self.MIN_VALUE)
        print("PWM set to LOW")
        sleep(4)
        print("Press UP/DOWN to Increase/Decrease, Press ESC to finish")
        while True:
            if keyboard.is_pressed("up"):
                self.setRate += 1
            if keyboard.is_pressed("down"):
                self.setRate -= 1
            if keyboard.is_pressed("esc"):
                self.setRate = self.MIN_VALUE
                pwm(self.setRate)
                break
            pwm(self.setRate)

    def arm(self):
        GPIO.output(self.brakePin, GPIO.HIGH)
        self.setRate = self.MIN_VALUE
        print("POD ARMED")


def requestFromArduino(address):
    try:
        with SMBus(1) as bus:
            block = bus.read_i2c_block_data(address, 1, 1)
            Size = block[0]
            block1 = bus.read_i2c_block_data(address, 2, Size)

            String1 = ""
            for i in range(len(block1)):
                String1 += chr(block1[i])

            StringValues = String1.split(",")
            intArray = [0] * len(StringValues)
            for i in range(len(StringValues)):
                intArray[i] = int(StringValues[i])

            return intArray

    except:
        print("Read Failed")
        plswork(address)


def mainRun():
    runStatus = False
    pod = HyperloopControlV2()
    runStatus = pod.system_check()
    if(runStatus == False):
        sys.exit()
    print("Press ENTER if all other system are good")
    while True:
        if keyboard.is_pressed("enter"):
            break
    print("Press ENTER to arm the pod")
    while True:
        if keyboard.is_pressed("enter"):
            pod.arm()
            print("POD IS ARMED, connect batteries")
            break
    print("Are the batteries connected, press ENTER if so")
    while True:
        if keyboard.is_pressed("enter"):
            break
    print("All systems are go, once the track is clear, press ENTER")
    while True:
        if keyboard.is_pressed("enter"):
            break
    print("Press Enter to Launch")
    while True:
        if keyboard.is_pressed("enter"):
            print("POD GO VROOOOOOOOOOM")
            self.startTime = datetime.now()
            break
    while not(pod.failsafe()):
        pod.go()
    pod.stop()

def readI2C():
    arduino1ctData = requestFromArduino(arduino1ct_ADDRESS)
    arduino2ctData = requestFromArduino(arduino2ct_ADDRESS)
    arduino3odData = requestFromArduino(arduino3od_ADDRESS)

if __name__ == '__main__':
    thread1 = threading.Thread(target=mainRun, args=())
    thread2 = threading.Thread(target=readI2C, args=())
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
