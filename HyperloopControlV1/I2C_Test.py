from smbus2 import SMBus
import time

SLAVE_ADDRESS = 0x06

bus = SMBus(1)

#bus.write_byte(SLAVE_ADDRESS, 0xFF)

def writeToArduino(value):
    bus.write_byte(SLAVE_ADDRESS, 0, value)

def readNumberFromArduino():
    global byteSize
    writeToArduino(1)
    byteSize = bus.read_byte_data(SLAVE_ADDRESS, 0)


def readMessageFromArduino(byteSize: int):
    global message
    message = ""
    data_from_arduino = bus.read_i2c_block_data(SLAVE_ADDRESS, 0,byteSize)
    for i in range(len(data_from_arduino)):
        message += chr(data_from_arduino[i])

    print(message.encode('utf-8'))
    data_from_arduino = ""


byteSize = 0
message = ""
if __name__ == '__main__':
    readNumberFromArduino()
    print(byteSize)
    readMessageFromArduino()
    print(message)
