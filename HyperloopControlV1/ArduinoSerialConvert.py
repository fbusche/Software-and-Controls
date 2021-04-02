import serial

class ArduinoSerialConvert:
    def __init__(self, serialPort, baudrate: int):
        self.ser = serial.Serial(
            port='COM4',\
            baudrate=9600,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS)

    def readSerial(self):
        for c in self.ser.read():
            seq.append(chr(c))
            self.joined_seq = ''.join(str(v) for v in seq)

    def decode(self):
        command = "x = " + self.joined_seq
        exec(command)
        return x
