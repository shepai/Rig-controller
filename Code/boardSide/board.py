from adafruit_motorkit import MotorKit
import board
import busio
import time

class Rig:
    def __init__(self):    
        #set up all i2c devices and motors
        self.i2c=i2c = busio.I2C(board.GP14, board.GP15)
        self.kit = MotorKit(i2c=self.i2c)
        self.kit = MotorKit(address=0x71,i2c=self.i2c)
        self.position=[-1,-1,-1,-1]
    def resetRig(self):
        #move the rig till in the reset position

