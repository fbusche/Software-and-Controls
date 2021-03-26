#Made by Manav Tailor and Manav Tailor
import os
from time import sleep
import RPi.GPIO as GPIO
from tkinter import messagebox

class ESC:
    MIN_VALUE = 0
    MAX_VALUE = 100
    def __init__(self, pin, frequency=10000):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.MIN_VALUE = MIN_VALUE
        self.MAX_VALUE = MAX_VALUE
        self.pwm = GPIO.PWM(18, frequency)
        self.pwm.start(0)

    def pwm(self, duty_cycle: int):
        self.pwm.ChangeDutyCycle(duty_cycle)

    def calibrate(self):
        print("Calibrating...")
        messagebox.showinfo('Disconnect the battery and press Enter')
        self.pwm(duty_cycle=self.MAX_VALUE)
        sleep(2)
        self.pwm(duty_cycle=self.MIN_VALUE)
        sleep(4)
        print("DONE")

    def arm(self):
        print("Arming...")
        self.pwm(duty_cycle=self.MIN_VALUE)
        sleep(4)
        print("Armed...")

    def halt(self):
        print("Halting")
        self.pwm(duty_cycle=self.MIN_VALUE)
        sleep(1)
        self.pwm.stop()
        print("Halted")
