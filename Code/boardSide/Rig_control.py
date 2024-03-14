from adafruit_motorkit import MotorKit
import Code.boardSide.Rig_control as Rig_control
import busio
import time
import supervisor
from adafruit_motor import stepper
import digitalio
import ulab.numpy as np
from Tactile_CP import * #found on my github

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
        self.i2c = busio.I2C(Rig_control.GP14, Rig_control.GP15)
        self.kit1 = MotorKit(i2c=self.i2c)
        self.kit2 = MotorKit(address=0x71,i2c=self.i2c)
        self.position=[-1,-1,-1,-1]
        self.motors=[self.kit1.stepper1,self.kit1.stepper2,self.kit2.stepper1,self.kit2.stepper2]
        #set up buttons
        # Define the pins for the buttons
        button_pins = [Rig_control.GP4, Rig_control.GP5, Rig_control.GP6, Rig_control.GP7] #arduino 2,3,4,5

        # Initialize an array to hold the button objects
        buttons = []
        for pin in button_pins:
            button = digitalio.DigitalInOut(pin)
            button.direction = digitalio.Direction.INPUT
            button.pull = digitalio.Pull.UP
            buttons.append(button)
        self.buttons=buttons
        #Initialise the plate
        self.plate=plate_mode
        if self.plate==1: #option one is normal plate
            pins=[Rig_control.GP8, Rig_control.GP9, Rig_control.GP2, Rig_control.GP3]
            self.sensor_plate=Foot(pins,Rig_control.GP26,Rig_control.GP20,alpha=0.2)
        elif self.plate==2: #plate is i2c
           self.sensor_plate=Plate(Rig_control.GP26,i2c=None,address=0x21,sda=None,scl=None,alpha=0.1)

    def resetRig(self):
        #move the rig till in the reset position
        while sum(self.readButtons())>0: #loop till all pressed
            states=np.ones((4,))*np.array(self.readButtons())
            self.moveMotors(states[0],states[1],states[2],states[3]) #only move ones not pressed
    def moveMotors(self,x,y,z,a,style=stepper.SINGLE):
        #move each motor by each value
        motors=[x,y,z,a]
        directions=[stepper.BACKWARD if motors[i]<0 else stepper.FORWARD for i in range(len(motors))]
        for i in range(max(motors)): #schedule together
            for j in range(len(motors)):
                if motors[j]>0:
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
            states.append(button.value)
        return states

class client:
    def listen_for_command(self): #listen for command from the data
        value=""
        while value=="":
            if supervisor.runtime.serial_bytes_available:
                value = input().strip()
        return value
    def send(self,message):
        print(f">{message}<")
    