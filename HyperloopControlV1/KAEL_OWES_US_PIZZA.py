import os
from ESC import ESC
import time
from time import sleep
from datetime import datetime
import csv
import keyboard
import RPi.GPIO as GPIO
import numpy as np
import threading
import serial

arduino1odo_Data = ""
arduino2ct_Data = ""
arduino3ct_Data = ""

arduino1Port = '/dev/ttyUSB0'
arduino2Port = '/dev/ttyACM0'
#arduino3Port = '/dev/ttyACM1'
arduino3Port = '/dev/ttyUSB1'
baudrate = 250000

class HyperloopControlV1:
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
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(brakePin, GPIO.OUT)
        GPIO.output(self.brakePin, GPIO.HIGH)

    def deltaTime_Seconds(self):
        endTime = datetime.now()
        temp = str(endTime - self.startTime)
        temp2 = temp.split(":")
        seconds = (float(temp2[0]))*3600 + (float(temp2[1]))*60 + (float(temp2[2]))
        return(seconds)

    def system_check(self):
        print("Press enter if Arduino 1 is working, ESC if not working")
        while True: #arduino 1 odometry
            arduinoData = getArduinoData()
            arduino1odo = arduinoData[0]
            print("d1: " + arduino1odo[0] + ", d2: " + arduino1odo[1] + ", v1: " + arduino1odo[2] + ", v2: " + arduino1odo[3]) 
            if keyboard.is_pressed('enter'):
                break
            if keyboard.is_pressed('esc'):
                print("Issue with Arduino 1")
                return False

        print("Press enter if Arduino 2 is working, ESC if not working")
        while True: #arduino 2 temp and current
            arduinoData = getArduinoData()
            arduino2ct = arduinoData[1]
            print("temp1: " + arduino2ct[0] + ", temp2: " + arduino2ct[1] + ", current1: " + arduino2ct[2] +
                  ", current2: " + arduino2ct[3] + ", current3: " + arduino2ct[4] + ", current4: " + arduino2ct[5])
            if keyboard.is_pressed('enter'):
                break
            if keyboard.is_pressed('esc'):
                print("Issue with Arduino 2")
                return False

        print("Press enter if Arduino 3 is working, ESC if not working")
        while True: #arduino 3 temp and current
            arduinoData = getArduinoData()
            arduino3ct = arduinoData[2]
            print("temp1: " + arduino3ct[0] + ", temp2: " + arduino3ct[1] + ", current1: " + arduino3ct[2] +
                  ", current2: " + arduino3ct[3] + ", current3: " + arduino3ct[4] + ", current4: " + arduino3ct[5])
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

    def failsafe(self):
        arduinoData = getArduinoData()
        arduino1odo = arduinoData[0]
        arduino2ct = arduinoData[1]
        arduino3ct = arduinoData[2]

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

    def go(self):
        arduinoData = getArduinoData()
        arduino1odo = arduinoData[0]
        arduino2ct = arduinoData[1]
        arduino3ct = arduinoData[2]
    
        if(arduino2ct[2] >= self.optimalCurrent and arduino2ct[3] >= self.optimalCurrent and arduino2ct[4] >= self.optimalCurrent and 
           arduino2ct[5] >= self.optimalCurrent and arduino3ct[2] >= self.optimalCurrent and arduino3ct[3] >= self.optimalCurrent and 
           arduino3ct[4] >= self.optimalCurrent and arduino3ct[5] >= self.optimalCurrent):
            self.setRate -= 1

        elif(arduino2ct[2] <= self.optimalCurrent and arduino2ct[3] <= self.optimalCurrent and arduino2ct[4] <= self.optimalCurrent and 
             arduino2ct[5] <= self.optimalCurrent and arduino3ct[2] <= self.optimalCurrent and arduino3ct[3] <= self.optimalCurrent and 
             arduino3ct[4] <= self.optimalCurrent and arduino3ct[5] <= self.optimalCurrent):
            self.setRate += 1

        self.esc.pwm(self.setRate)

    def stop(self):
        self.esc.pwm(0)
        GPIO.output(self.brakePin, GPIO.LOW)

def mainRun():
    time.sleep(5)
    pod = HyperloopControlV1()
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

    while(pod.failsafe() == True):
        pod.go()

    pod.stop()

def updateArduino1odo_Data(port, baudrate):
    global arduino1odo_Data
    ser = serial.Serial(port, baudrate)
    ser.flushInput()
    while(True):
        try:
            ser_bytes = ser.readline()
            decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            arduino1odo_Data = decoded_bytes
        except:
            pass
            #print("Dropped")

def updateArduino2ct_Data(port, baudrate):
    global arduino2ct_Data
    ser = serial.Serial(port, baudrate)
    ser.flushInput()
    while(True):
        try:
            ser_bytes = ser.readline()
            decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            arduino2ct_Data = decoded_bytes
        except:
            pass
            #print("Dropped")

def updateArduino3ct_Data(port, baudrate):
    global arduino3ct_Data
    ser = serial.Serial(port, baudrate)
    ser.flushInput()
    while(True):
        try:
            ser_bytes = ser.readline()
            decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
            arduino3ct_Data = decoded_bytes
        except:
            pass
            #print("Dropped")

def getArduinoData():
    global arduino1odo_Data
    global arduino2ct_Data
    global arduino3ct_Data
    arduino1odo_Float = [0.0,0.0,0.0,0.0]
    arduino1odo_Data_Split = arduino1odo_Data.split(',')
    for i in range(len(arduino1odo_Data_Split)):
        arduino1odo_Float[i] = float(arduino1odo_Data_Split[i])
    arduino2ct_Float = [0.0,0.0,0.0,0.0,0.0,0.0]
    arduino2ct_Data_Split = arduino2ct_Data.split(',')
    for i in range(len(arduino2ct_Data_Split)):
        arduino2ct_Float[i] = float(arduino2ct_Data_Split[i])
    arduino3ct_Float = [0.0,0.0,0.0,0.0,0.0,0.0]
    arduino3ct_Data_Split = arduino3ct_Data.split(',')
    for i in range(len(arduino3ct_Data_Split)):
        arduino3ct_Float[i] = float(arduino3ct_Data_Split[i])
    return [arduino1odo_Float, arduino2ct_Float, arduino3ct_Float]


if __name__ == '__main__':
    thread1 = threading.Thread(target=mainRun, args=())
    thread2 = threading.Thread(target=updateArduino1odo_Data, args=(arduino1Port,baudrate))
    thread3 = threading.Thread(target=updateArduino2ct_Data, args=(arduino2Port,baudrate))
    thread4 = threading.Thread(target=updateArduino3ct_Data, args=(arduino3Port,baudrate))
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
