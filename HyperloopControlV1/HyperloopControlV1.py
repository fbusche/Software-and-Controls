import os
from ESC import ESC
from ArduinoSerialConvert import ArduinoSerialConvert
import time
from time import sleep
from datetime import datetime
import csv
import keyboard
import RPi.GPIO as GPIO
import numpy as np

class HyperloopControlV1:

    #Variables
    arduino1Port = ''
    arduino2Port = ''
    arduino3Port = ''
    baudrate = 115200


    def __init__(self):
        self.arduino1odo = ArduinoSerialConvert(arduino1Port, baudrate)
        self.arduino2ct = ArduinoSerialConvert(arduino2Port, baudrate)
        self.arduino3ct = ArduinoSerialConvert(arduino3Port, baudrate)
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
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(2, GPIO.OUT)
        GPIO.output(self.brakePin, GPIO.HIGH)

    def getArduinoData(self):
        return [self.arduino1odo.readSerial(),self.arduino2ct.readSerial(),self.arduino3ct.readSerial()]

    def deltaTime_Seconds():
        endTime = datetime.now()
        temp = str(endTime - startTime)
        temp2 = temp.split(":")
        seconds = (float(temp2[0]))*3600 + (float(temp2[1]))*60 + (float(temp2[2]))
        return(seconds)


    def system_check(self):
        print("Press enter if Arduino 1 is working, ESC if not working")
        while True: #arduino 1 odometry
            arduino1odo = self.arduino1odo.readSerial() #Serial.print("["+d1+", "+d2+", "+v1+", "+v2+"]");
            print("d1: " + arduino1odo[0] + ", d2: " + arduino1odo[1] + ", v1: " + arduino1odo[2] + ", v2: " + arduino1odo[3]) 
            if keyboard.is_pressed('enter'):
                break
            if keyboard.is_pressed('esc'):
                print("Issue with Arduino 1")
                return False

        print("Press enter if Arduino 2 is working, ESC if not working")
        while True: #arduino 2 temp and current
            arduino2ct = self.arduino2ct.readSerial()  #2 temps, 4 currents
            print("temp1: " + arduino3ct[0] + ", temp2: " + arduino3ct[1] + ", current1: " + arduino3ct[2] +
                  ", current2: " + arduino3ct[3] + ", current3: " + arduino3ct[4] + ", current4: " + arduino3ct[5])
            if keyboard.is_pressed('enter'):
                break
            if keyboard.is_pressed('esc'):
                print("Issue with Arduino 2")
                return False

        print("Press enter if Arduino 3 is working, ESC if not working")
        while True: #arduino 3 temp and current
            arduino3ct = self.arduino3ct.readSerial()  #2 temps, 4 currents 
            print("temp1: " + arduino2ct[0] + ", temp2: " + arduino2ct[1] + ", current1: " + arduino2ct[2] +
                  ", current2: " + arduino2ct[3] + ", current3: " + arduino2ct[4] + ", current4: " + arduino2ct[5])
            if keyboard.is_pressed('enter'):
                break
            if keyboard.is_pressed('esc'):
                print("Issue with Arduino 3")
                return False

        while True: #brakes
            print("Press enter to disengage brakes")
            if keyboard.is_pressed('enter'):
                GPIO.output(self.brakePin, GPIO.LOW)
                #sleep(3) #Time the breaks will be turned on for
                #GPIO.output(self.brakePin, GPIO.HIGH)

                print("Press enter if brakes are working, ESC if not working")
                if keyboard.is_pressed('enter'):
                    break
                if keyboard.is_pressed('esc'):
                    print("Issue with braking system")
                    return false
        

    def failsafe(self, arduino1odo, arduino2ct, arduino3ct): #return true if tripped, else false
        self.brakingDistance1 = (arduino1odo[2]**2) / (2*self.deceleration)
        self.brakingDistance2 = (arduino1odo[3]**2) / (2*self.deceleration)

        if(arduino1odo[0] >= (self.trackLength - self.brakingDistance1) or arduino1odo[1] >= (self.trackLength - self.brakingDistance2)):
             return False
        if(arduino2ct[0] >= self.maxTemp or arduino2ct[1] >= self.maxTemp or arduino3ct[0] >= self.maxTemp or arduino3ct[1] >= self.maxTemp):
            return False
        if(arduino2ct[2] >= self.maxCurrent or arduino2ct[3] >= self.maxCurrent or arduino2ct[4] >= self.maxCurrent or 
           arduino2ct[5] >= self.maxCurrent or arduino3ct[2] >= self.maxCurrent or arduino3ct[3] >= self.maxCurrent or 
           arduino3ct[4] >= self.maxCurrent or arduino3ct[5] >= self.maxCurrent):
            return False
        if(deltaTime_Seconds() >= self.maxRunTime):
            return False
        if(keyboard.is_pressed(' ')):
            return False
        else:
            return True
        

    def go(self, arduino2ct, arduino3ct):
        if(arduino2ct[2] >= self.optimalCurrent and arduino2ct[3] >= self.optimalCurrent and arduino2ct[4] >= self.optimalCurrent and 
           arduino2ct[5] >= self.optimalCurrent and arduino3ct[2] >= self.optimalCurrent and arduino3ct[3] >= self.optimalCurrent and 
           arduino3ct[4] >= self.optimalCurrent and arduino3ct[5] >= self.optimalCurrent):
            self.setRate -= 1

        elif(arduino2ct[2] <= self.optimalCurrent and arduino2ct[3] <= self.optimalCurrent and arduino2ct[4] <= self.optimalCurrent and 
             arduino2ct[5] <= self.optimalCurrent and arduino3ct[2] <= self.optimalCurrent and arduino3ct[3] <= self.optimalCurrent and 
             arduino3ct[4] <= self.optimalCurrent and arduino3ct[5] <= self.optimalCurrent):
            self.setRate += 1

        self.esc.pwm(self.setRate)


if __name__ == '__main__':

    pod = HyperloopControlV1()

    dataArray = np.array([])

    while not (pod.system_check()):
        pass

    print("Press enter to start the pod")
    while not (keyboard.is_pressed('enter')):
        pass
    
    print("Press the space bar to stop the pod during run")
    print("Pod Starting in...")
    for i in range(3):
        print(i + "...")
        sleep(1)
    
    arduinoData = pod.getArduinoData()
    #dataArray = np.append(arduinoData, axis=0)

    while(pod.failsafe(arduinoData[0], arduinoData[1], arduinoData[2]) == True):
        go(arduinoData[1], arduinoData[2])

    self.esc.pwm(0)                       #turn off motors
    GPIO.output(self.brakePin, GPIO.LOW)  #engage brakes
    print("Did it explode?...yes")

    #csvFileName = datetime.now().strftime("%H_%M_%S")

    #with open()