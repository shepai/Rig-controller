from adafruit_motorkit import MotorKit
import board
import busio
import time
import supervisor

class Rig:
    def __init__(self):    
        #set up all i2c devices and motors
        self.i2c=i2c = busio.I2C(board.GP14, board.GP15)
        self.kit = MotorKit(i2c=self.i2c)
        self.kit = MotorKit(address=0x71,i2c=self.i2c)
        self.position=[-1,-1,-1,-1]
    def resetRig(self):
        #move the rig till in the reset position
        pass
    def moveMotors(self,x,y,z,a):
        #move each motor by each value
        pass
    def readBase(self):
        #read the force on rig
        pass

class client:
    def listen_for_command(self): #listen for command from the data
        value=""
        while value=="":
            if supervisor.runtime.serial_bytes_available:
                value = input().strip()
        return value
    def send(self,message):
        print(f">{message}<")
    