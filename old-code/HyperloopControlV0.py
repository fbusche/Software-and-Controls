# HyperloopControlV0
# Main Script (will use this since we're not using GUI anymore)

import os
from ESC import ESC
import ArduinoSerialConvert as convert #converts to floats in an array
import time
from time import sleep
from datetime import datetime
import logging
import csv

class HyperloopControlV0:

    # Assign variables
    temperature = self.arduino.getTemperature()
    voltage = self.arduino.getVoltage()

    #set variables
    startTime = datetime.now()
    maxTemperature = 0.0
    minTemperature = 0.0
    maxVoltage = 0.0
    minVoltage - 0.0
    maxTime = 2.0
    trackLength = 0.0
    timeElapsed = 0.0
    setRate = 0.0

    #calculated from these global variables
    distanceRequiredToBreak = deceleration * velocity
    distanceRemaining = trackLength - position
    #if track if 400m long, set track length to 350m

    #this fills in nanos with the data from all the sensors on each nano
    nanos = {}
    nanoNum = range(3)
    sensors = []

    for i in nanoNum:
        sensors = self.convert.decode()
        for j in sensors:
            nanos[i][j] = sensors[j]

    def __init__():
        self.deltaTime_Seconds()
        if self.system_check(odometryInput1, odometryInput2, nanos, brakeInput, ESCInput) == True:
            self.go()

    #Time function 
    def deltaTime_Seconds():
        endTime = datetime.now()
        temp = str(endTime - startTime)
        temp2 = temp.split(":")
        seconds = (float(temp2[0]))*3600 + 
                    (float(temp2[1]))*60 + 
                    (float(temp2[2]))
        print(seconds)

    # Run system check
    # Set up (each step will have user input, start check, pause, stop check)
    def system_check(odometryInput1, odometryInput2, nanos, brakeInput, ESCInput):
        results = True
        # Odometry data (position)
        if odometryInput1 != expectedTrackLength:
            print("Track length wrong, check odometry")
            results = False
        elif odometryInput2 != expectedCurrentPosition:
            print("Current position wrong, check odometry")
            results = False
        # Temp and voltage
        for key, value in nanos.items():
            while nanos[key] < 5:
                if nanos[key][value] !< maxTemperature:
                    print("Nano " nanos[key] " sensor " nanos[key][value] " temp is too high")
                    results = False
                elif nanos[key][value] !> minTemperature:
                    print("Nano " nanos[key] " sensor " nanos[key][value] " temp is too low")
                    results = False
            if nanos[key][value] !< maxVoltage:
                print("Nano " nanos[key] " sensor " nanos[key][value] " voltage is too high")
                results = False
            elif nanos[key][value] !> minVoltage:
                print("Nano " nanos[key] " sensor " nanos[key][value] " voltage is too low")
                results = False
        # Test brakes: disengage and then engage
        if brakeInput == True:
            print("Brakes engaged, running test")
            brakesEngaged = brakeInput
        else:
            print("Brakes were NOT engaged yet")
            results = False
            #do the thing to engage the brakes & set brakesEngaged to true
            if brakesEngaged == True:
                print("Brakes now engaged, running test")
            else:
                print("Brakes STILL not engaged, cannot run tests")
                results = False
        print("Disengaging brakes...")
        # do the thing to disengage the brakes & set brakesEngaged to false
        if brakesEngaged == False:
            print("Brakes successfully disengaged")
            sleep(1) #waiting a hot second before we engage them again
            print("Engaging brakes...")
            # do the thing to engage the brakes & set brakesEngaged to true
            if brakesEngaged == True:
                print("Brakes successfully re-engaged")
            else:
                print("Brakes NOT successfully re-engaged")
                results = False
        else:
            print("Brakes NOT successfully disengaged")
            results = False
        # Calibrate ESCs
        self.esc.calibrate()

        if results == True:
            print("System check passed")
        
        return results


    def go():    
        # Failsafe Loop (post system check)
            # Velocity - need
            # Position - need
            # Time - done

        while timeElapsed < maxTime:
            if setRate < self.esc.MAX_VALUE:
                self.esc.pwm(setRate)
                timeElapsed += self.deltaTime_Seconds()
                if distanceRemaining =< distanceRequiredToBreak:
                    self.esc.pwm(0)
                else:
                    for key, value in nanos:
                        if temperature > maxTemperature:
                            self.esc.pwm(0)
                        if voltage > maxVoltage:
                            setRate -= 1
                        elif voltage < maxVoltage:
                            setRate += 1
            setRate += 10

        #this halts the system by turning off the motors... but we need to add in a part that actually turns ON the brakes
        self.esc.pwm(0)

if __name__ == '__main__':
    
    HyperloopControlV0.mainloop()
