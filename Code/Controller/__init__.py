import time
import serial
from mpremote import pyboard

class Controller:
    def __init__(self,COM,variant="micropython",file=""):
        self.variant=variant.lower()
        if self.variant=="circuitpython":
            self.ser = serial.Serial(COM, 9600, timeout=1,write_timeout = 3)  # open serial port
        else:
            self.COM=pyboard.Pyboard(COM) #connect to board
            self.COM.enter_raw_repl() #open for commands
            self.COM.execfile(file)
            print("Successfully connected")
    def listen_for_data(self):
        #keep searching till client pings back
        if self.variant=="circuitpython":
            t1=time.time()
            t2=time.time()
            value=""
            response = self.ser.readline()
            if response:
                value=response.decode().strip()
            return value.replace(">","").replace("<","")
        raise SystemError("Need to be on circuitpython mode for this to work")
    def sendCommand(self,message):
        if self.variant=="circuitpython":
            try:
                self.ser.write((message+"\n").encode())
            except serial.serialutil.SerialTimeoutException:
                print("serial issue")
        else: #micropython send command
            if "RESET" in message:
                self.COM.exec_raw_no_follow('reset()')
            elif "MOVE:" in message:
                com=message.replace("MOVE:","")
                com=com.split(",")
                self.COM.exec_raw_no_follow('move('+(com[0])+','+(com[1])+','+(com[2])+','+(com[3])+')')
            elif "pressure" in message:
                return self.COM.exec('pressure()').decode("utf-8").replace("\r\n","")
    def reset(self):
        self.sendCommand("RESET")
    def move(self,x,y,z,a):
        #move the rig by these amounts
        self.sendCommand("MOVE:"+str(x)+","+str(y)+","+str(z)+","+str(a))
    def getPressure(self):
        #find weight of sensor touch
        pressure=""
        if self.variant=="circuitpython":
            self.sendCommand("pressure")
            pressure=self.listen_for_data()
        else:
           pressure=self.sendCommand("pressure")
        ar=[]
        for item in pressure.split(","):
            ar.append(int(item))
        return ar

