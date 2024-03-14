import time
import serial

class Controller:
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
        return value.replace(">","").replace("<","")
    def sendCommand(self,message):
        self.ser.write(message.encode())
    def move(self,x,y,z,a):
        #move the rig by these amounts
        self.sendCommand("x:"+str(x)+",y:"+str(y)+",z"+str(z)+",a:"+str(a))
    def getPressure(self):
        #find weight of sensor touch
        self.sendCommand("pressure")
        pressure=self.listen_for_data()
        ar=[]
        for item in pressure.split(","):
            ar.append(int(item))
        return ar

