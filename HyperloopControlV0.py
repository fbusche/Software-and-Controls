# HyperloopControlV0
# Main Script (will use this since we're not using GUI anymore)


import os
from ESC import ESC
# import someArduinoFile as arduino
import time
from time impoprt sleep
from datetime import datetime
import logging
import csv


class HyperloopControlV0:

    # Assign variables
    temperature = self.arduino.getTemperature()
    voltage = self.arduino.getVoltage()

    #set variables
    startTime = datetime.now()
    maxTemperature = 0
    maxVoltage = 0
    maxTime = 0
    trackLength = 0
    timeElapsed = 0
    setRate = 0

    #calculated from these global variables
    distanceRequiredToBreak = deceleration * velocity
    distanceRemaining = trackLength - position
    #if track if 400m long, set track length to 350m

    #list of all the pins
    nano = {}
    sensors = {}


    #Time function 
    def deltaTime_Seconds():
        endTime = datetime.now()
        temp = str(endTime - startTime)
        temp2 = temp.split(":")
        seconds = (float(temp2[0]))*3600 + 
                    (float(temp2[1]))*60 + 
                    (float(temp2[2]))
        print(seconds)

    # Run system check --> NOT AT ALL DONE
        # Set up (each step will have user input, start check, pause, stop check)
        # Odometry data
        # Temp
        # Pressure
        # Test brakes: disengage and then engage
        # Arm ESCs


    # Failsafe Loop (post system check)
        # Velocity - need
        # Position - need
        # Time - done

    while timeElapsed < maxTime:
                
        if setRate < self.esc.MAX_VALUE:

            #start pod
            self.esc.pwm(setRate)
            #start clock
            timeElapsed += self.deltaTime_Seconds()


            #making sure we have enough space to break
            if distanceRemaining =< distanceRequiredToBreak:
                self.esc.halt()
            else:
                        
                #loops through each nano (there's gonna be 3)
                #gonna run "analogRead()" which is part of what Talhah is doing to get data from Arduino
                for i in nanos:
                    for j in sensor:
                        #checking that temperature isn't too high
                        #also gonna get this from the arduino
                        if temperature > maxTemperature:
                            self.esc.halt()
                        #checks voltage of nano
                        if voltage > maxVoltage:
                            setRate -= 1
                        elif voltage < maxVoltage:
                            setRate += 1
        #raise the rate (can't start at max because 0-max is too sudden all at once)
        setRate += 10

    #this halts the system by turning off the motors... but we need to add in a part that actually turns ON the brakes
    self.esc.halt()
