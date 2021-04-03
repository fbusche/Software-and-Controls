import os
import time
from adafruit_servokit import Servokit

class ESC:
    MIN_VALUE = 0
    MAX_VALUE = 180
    def __init__(self):
        self.kit = ServoKit(channels = 16)
        for i in range(8):
            self.kit.servo[i].angle = MIN_VALUE

    def pwm(self, speed: int):
        if(speed <= MIN_VALUE):
            for i in range(8):
                self.kit.servo[i].angle = MIN_VALUE
        elif(speed >= MAX_VALUE):
            for i in range(8):
                self.kit.servo[i].angle = MAX_VALUE
        else:
            for i in range(8):
                self.kit.servo[i].angle = speed

    def calibrate(self):
        messagebox.showinfo('Disconnect the battery and press Enter')
        self.pwm(speed=MAX_VALUE)
        time.sleep(2)
        self.pwm(speed=MIN_VALUE)
        time.sleep(4)
