from smbus2 import SMBus
from time import sleep

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
        print("REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        plswork(address)

def send(address, value):
    try:
        with SMBus(1) as bus:
            bus.write_byte_data(address, 0, value)
    except:
        print("Send Failed, Resending")
        send(address, value)

while(False):
    print(plswork(4))
    #sleep(0.01)

while(False):
    for i in range(180):
        send(7, i)
        sleep(0.01)

while(True):
    print(plswork(4))
    for i in range(0, 180, 10):
        send(7, i)
        sleep(0.01)
