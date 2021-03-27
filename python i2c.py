import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels = 16)


kit.servo[0].angle = motor_speed #MOTOR_SPEED MUST BE IN DEGREES FROM 0-180
kit.servo[1].angle = motor_speed
kit.servo[2].angle = motor_speed
kit.servo[3].angle = motor_speed
kit.servo[4].angle = motor_speed
kit.servo[5].angle = motor_speed
kit.servo[6].angle = motor_speed
kit.servo[7].angle = motor_speed
