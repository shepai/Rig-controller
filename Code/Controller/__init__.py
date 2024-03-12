import time
import serial

class controller:
    def __init__(self,COM):
        self.ser = serial.Serial(COM, 115200)  # open serial port

    def listen_for_data(self):
        #keep searching till client pings back
        value=""
        while "<" not in value:
            a = self.ser.read()
            if a== b'\r':
                break
            else:
                value += a
        return value
    def sendCommand(self,message):
        self.ser.write(message.encode())