from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import busio
import board
from machine import Pin
import machine
import time
from Tactile_MP import Foot #found on my github

class Rig:
    """
    Pinout

    I2C GP14 and GP15
    The buttons must be connceted to
    GP4,GP5 GP6 and GP7 each corrosponding to axis x,y,z,a
    Stepper motors must be x to board 1 y to board 1 z to board 2 a to board 2
    The foot or pressure sensor should be connected either through:
        I2C on 14 and 15
        or
        GP8, GP9, GP2, GP3 and the access pin to either ground or GP20
    """
    def __init__(self,plate_mode=0):    
        #set up all i2c devices and motors
        self.i2c = busio.I2C(scl=board.GP25, sda=board.GP24)
        self.kit1 = MotorKit(address=0x70,i2c=self.i2c)
        self.kit2 = MotorKit(address=0x60,i2c=self.i2c)
        self.position=[-1,-1,-1,-1]
        self.motors=[self.kit1.stepper1,self.kit1.stepper2,self.kit2.stepper1,self.kit2.stepper2]
        #set up buttons
        # Define the pins for the buttons
        button_pins = [Pin(2,machine.Pin.OUT), Pin(3,machine.Pin.OUT), Pin(1,machine.Pin.OUT), Pin(0,machine.Pin.OUT)] #arduino 2,3,4,5
        
        # Initialize an array to hold the button objects
        self.buttons=button_pins
        #Initialise the plate
        self.plate=plate_mode
        if self.plate==1: #option one is normal plate
            pins=[Pin(4,machine.Pin.OUT), Pin(5,machine.Pin.OUT), Pin(6,machine.Pin.OUT), Pin(7,machine.Pin.OUT)]
            self.sensor_plate=Foot(pins,Pin(26,machine.Pin.OUT),Pin(20,machine.Pin.OUT),alpha=0.2)
        elif self.plate==2: #plate is i2c
           self.sensor_plate=Plate(Pin(26,machine.Pin.OUT),i2c=None,address=0x21,sda=None,scl=None,alpha=0.1)
    def resetRig(self):
        #move the rig till in the reset position
        while 0 in self.readButtons(): #loop till all pressed
            states=[(1-self.readButtons()[i])*100 for i in range(len(self.readButtons()))]
            self.moveMotors(states[2],states[3],states[1],states[0]) #only move ones not pressed
    def moveMotors(self,x,y,z,a,style=stepper.INTERLEAVE):
        #move each motor by each value
        motors=[z*-1,a*1,y*-1,x*1] #multiply by direction bias
        actualDir=[0 if x >= 0 else -1 for x in [z,a,y,x]]
        directions=[stepper.BACKWARD if motors[i]<0 else stepper.FORWARD for i in range(len(motors))]
        motors=[abs(motors[i]) for i in range(len(motors))]
        for i in range(max(motors)): #schedule together
            for j in range(len(motors)):
                if motors[j]>0 and (self.readButtons()[j]==0 or actualDir[j]==-1):
                    self.motors[j].onestep(direction=directions[j], style=style)
                    motors[j]-=1
    def readBase(self):
        #read the force on rig
        if self.plate>0:
            return self.sensor_plate.read()
        return -1
    def readButtons(self):
        states = []
        for button in self.buttons:
            states.append(button.value())
        return states

class client:
    def listen_for_command(self,command=""): #listen for command from the data
        return command
    def send(self,message):
        print(f">{message}<")
    

