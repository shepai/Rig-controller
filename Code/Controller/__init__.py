import time
import serial
try:
    from mpremote import pyboard
except:
    print("No python device")
import subprocess
import serial.tools.list_ports

def disconnect_from_device(COM):
    # Make sure to properly close the connection and release the serial port
    try:

        COM.exit_raw_repl()  # Ensure the REPL is exited
        COM.close()  # Close the serial connection properly
    except Exception as e:
        print(f"Error during disconnect: {e}")
def is_serial_port_available(port):
    """Check if a serial port is available for connection."""
    available_ports = [p.device for p in serial.tools.list_ports.comports()]
    print(available_ports)
    return port in available_ports
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
            
        self.file=file
        self.COM_=COM
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
        reconnect=True
        while reconnect:
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
                        keys=["cx","cy","cz"]
                        if "setmove1" in message: keys=["cx","cy"] #dont reset all
                        for key in keys:
                            self.COM.exec("rig.memory['"+key+"']=0")
                    elif "lower" in message: #lower sensor on to base
                        average=message.replace("lower=","") 
                        self.COM.exec("rig.lowerSensor("+str(average)+")")
                    elif "ZERO" in message:
                        self.COM.exec("rig.zero()")
                    elif "DIST" in message:
                        return float(self.COM.exec('rig.getSensor()').decode("utf-8").replace("\r\n",""))
                    elif "centre" in message:
                        self.COM.exec("rig.centre()")
                    elif "perfect" in message:
                        self.COM.exec("rig.setPerfect()")
                    reconnect=False
                except pyboard.PyboardError as e:
                    print("Pyboard issue",e)
                    disconnect_from_device(self.COM)
                    self.COM=pyboard.Pyboard(self.COM_) #connect to board
                    self.COM.enter_raw_repl() #open for commands
                    self.COM.execfile(self.file)
                except serial.serialutil.SerialException as e:
                    print("Serial problem...")
                    disconnect_from_device(self.COM)
                    while not is_serial_port_available(self.COM_):
                        print(f"Waiting for port {self.COM_} to be available...")
                        time.sleep(2)
                    self.COM=pyboard.Pyboard(self.COM_) #connect to board
                    self.COM.enter_raw_repl() #open for commands
                    self.COM.execfile(self.file)
                    
    def reset_trial(self,centering=0):
        movements=self.sendCommand("getmove")[3:]
        if centering: self.sendCommand("centre")
        self.move(*movements,0)
    def reset(self,exclude=[1]):
        #self.sendCommand("RESET")
        buttons=self.sendCommand("BUTTONS")
        while 0 in [buttons[i] if i not in exclude else 1 for i in range(len(buttons))]: #loop till all pressed
            states=[(1-buttons[i])*100 for i in range(len(buttons))]
            self.move(states[3],states[2],states[0],1) #only move ones not pressed
            buttons=self.sendCommand("BUTTONS")
    def calibrate(self,value=7500,lower=True,val=0):
        self.reset()
        #use the movement coords to get to point
        #the movements are preset to match those in self.sendCommand("getmove")[0:3]
        for i in range(15):
            self.sendCommand("MOVE:-100,-100,0,0")
        for i in range(45):
            self.sendCommand("MOVE:0,-100,0,0")
        for i in range(4):
            self.sendCommand("MOVE:-100,-100,0,0")
        print("Centred...")
        self.sendCommand("setmove")
        print("calibrating position...")
        if lower:
            self.sendCommand("lower="+str(value))
            print("Lowered to point")
        else:
            self.sendCommand("MOVE:0,0,"+str(val)+",0")
            print("Resetting..")
            self.reset_trial()
            
        self.sendCommand("CALIB")
        #self.sendCommand("centre")
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

class Arduino_Rig:
    def __init__(self,COM="/dev/ttyACM0"):
        # Set up serial connection (adjust 'COM3' to your port and baudrate to match Arduino)
        self.arduino = serial.Serial(port=COM, baudrate=921600, timeout=1)
        time.sleep(2)  # Allow time for Arduino to reset

    def send_command(self,command):
        self.arduino.write((command + '\n').encode())

    def send_command_await(self,command):
        print(command)
        self.arduino.write((command + '\n').encode())
        while True:
            response = self.arduino.readline().decode('utf-8').strip()
            if response:
                print(f"Arduino response: {response}")
                if "done" in response:
                    break

    def reset_trial(self):
        self.send_command_await("ZERO")

    def calibrate(self,value=7500,lower=True,val=0):
        self.send_command_await("CALIB")
        self.send_command_await("MOVE,0,0,"+str(val)+",2")
        self.send_command_await("CENTRE")
    def reset(self):
        self.send_command_await("RESET")

    def move(self,x,y,z,a,step=5):
        self.send_command_await("MOVE,"+str(int(x))+","+str(int(y))+","+str(int(z))+","+str(step))
    def reset_trial(self):
        self.send_command_await("ZERO")

if __name__ == "__main__":
    start=time.time()
    arduino_test=Arduino_Rig()
    arduino_test.reset()
    print("reset device")
    arduino_test.calibrate()
    print("calibrated")
    arduino_test.move(-1000,100,100)
    print("moved")
    arduino_test.reset_trial()
    print("returned to state")
    print("setup time:",(time.time()-start)/60,"minutes")
    #arduino_test.move(10,10,10)