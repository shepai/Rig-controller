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
            try:
                if "RESET" in message:
                    self.COM.exec('rig.reset()')
                elif "CALIB" in message:
                    self.COM.exec('rig.inPosition=True')
                elif "BUTTONS" in message:
                    b=self.COM.exec("print(rig.readButtons())").decode("utf-8").replace("\r\n","").replace("[","").replace("]","").replace(" ","")
                    ar=[]
                    for val in b.split(","):
                        ar.append(int(val))
                    return ar
                elif "MOVE:" in message:
                    com=message.replace("MOVE:","")
                    com=com.split(",")
                    self.COM.exec('move('+(com[0])+','+(com[1])+','+(com[2])+','+(com[3])+')')
                elif "pressure" in message:
                    return self.COM.exec('pressure()').decode("utf-8").replace("\r\n","")
                elif "getmove" in message: #get all the rig values
                    b=self.COM.exec('print([rig.memory[key] for key in ["x","y","z","cx","cy","cz"]])').decode("utf-8").replace("\r\n","").replace("[","").replace("]","").replace(" ","")
                    ar=[]
                    for val in b.split(","):
                        ar.append(int(val))
                    return ar
                elif "setmove" in message: #reset the values to be 0
                    for key in ["cx","cy","cz"]:
                        self.COM.exec("rig.memory["+key+"]=0")
                elif "lower" in message: #lower sensor on to base
                    average=message.replace("lower=","")
                    self.COM.exec_raw_no_follow("rig.lowerSensor("+str(average)+")")
                elif "ZERO" in message:
                    self.COM.exec_raw_no_follow("rig.zero()")
            except pyboard.PyboardError as e:
                pass
    def reset_trial(self):
        movements=self.sendCommand("getmove")[3:]
        self.move(*movements,0)
    def reset(self,exclude=[1]):
        #self.sendCommand("RESET")
        buttons=self.sendCommand("BUTTONS")
        while 0 in [buttons[i] if i not in exclude else 1 for i in range(len(buttons))]: #loop till all pressed
            states=[(1-buttons[i])*100 for i in range(len(buttons))]
            self.move(states[3],states[2],states[0],states[1]) #only move ones not pressed
            buttons=self.sendCommand("BUTTONS")
    def calibrate(self):
        self.reset()
        #use the movement coords to get to point
        #the movements are preset to match those in self.sendCommand("getmove")[0:3]
        for i in range(15):
            self.sendCommand("MOVE:-100,-100,0,0")
        for i in range(45):
            self.sendCommand("MOVE:0,-100,0,0")
        self.sendCommand("lower=8000")
        print("Lowered to point")
        self.sendCommand("CALIB")
        print("Calibration done")
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

