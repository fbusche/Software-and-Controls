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
        pass

    def failsafe(self):
        pass

    def go(self):
        pass

def mainRun():
    time.sleep(5)
    while(True):
        arduinoData = getArduinoData()
        print(arduinoData)


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