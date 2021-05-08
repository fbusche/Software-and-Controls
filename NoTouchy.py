import keyboard
from time import sleep
from smbus2 import SMBus

throttle = 0
MIN = 0
MAX = 180
rate = 1
time_delay = 0.005

def plswork(address):
    try:
        with SMBus(1) as bus:
            block = bus.read_i2c_block_data(address, 1, 1)
            Size = block[0]
            block1 = bus.read_i2c_block_data(address, 2, Size)

            String1 = ""
            for i in range(len(block1)):
                String1 += chr(block1[i])
            return String1
    except:
        plswork(address)

def send(address, value):
    try:
        with SMBus(1) as bus:
            bus.write_byte_data(address, 0, value)
    except:
        print("Send Failed, Resending")
        send(address, value)

while(True):
    if(keyboard.is_pressed("UP")):
        if(throttle+rate <= MAX):
            throttle+=rate
        print(throttle)
        sleep(time_delay)
    if(keyboard.is_pressed("DOWN")):
        if(throttle-rate >= MIN):
            throttle-=rate
        print(throttle)
        sleep(time_delay)
    if(keyboard.is_pressed("LEFT")):
        throttle = MIN
        print(throttle)
    if(keyboard.is_pressed("RIGHT")):
        throttle = MAX
        print(throttle)
    plswork(7, throttle)
