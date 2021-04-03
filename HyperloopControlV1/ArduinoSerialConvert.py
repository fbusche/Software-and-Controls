import serial

class ArduinoSerialConvert:
    def __init__(self, serialPort, baudrate: int):
        self.ser = serial.Serial(
            port=serialPort,\
            baudrate=baudrate,\
            parity=serial.PARITY_NONE,\
            stopbits=serial.STOPBITS_ONE,\
            bytesize=serial.EIGHTBITS)

    def readSerial(self):
        for c in self.ser.read():
            seq.append(chr(c))
            joined_seq = ''.join(str(v) for v in seq)
        command = "x = " + joined_seq
        exec(command)
        return x
