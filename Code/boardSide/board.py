from adafruit_motorkit import MotorKit
import board
import busio
import time
import supervisor
from adafruit_motor import stepper
import digitalio
import numpy as np

class Rig:
    def __init__(self):    
        #set up all i2c devices and motors
        self.i2c=i2c = busio.I2C(board.GP14, board.GP15)
        self.kit1 = MotorKit(i2c=self.i2c)
        self.kit2 = MotorKit(address=0x71,i2c=self.i2c)
        self.position=[-1,-1,-1,-1]
        self.motors=[self.kit1.stepper1,self.kit1.stepper2,self.kit2.stepper1,self.kit2.stepper2]
        #set up buttons
        # Define the pins for the buttons
        button_pins = [board.GP2, board.GP3, board.GP4, board.GP5]

        # Initialize an array to hold the button objects
        buttons = []

        # Initialize the button objects
        for pin in button_pins:
            button = digitalio.DigitalInOut(pin)
            button.direction = digitalio.Direction.INPUT
            button.pull = digitalio.Pull.UP
            buttons.append(button)
        self.buttons=buttons
    def resetRig(self):
        #move the rig till in the reset position
        while sum(self.readButtons())>0: #loop till all pressed
            states=np.ones((4,))*np.array(self.readButtons())
            self.moveMotors(states[0],states[1],states[2],states[3]) #only move ones not pressed
    def moveMotors(self,x,y,z,a):
        #move each motor by each value
        motors=[x,y,z,a]
        directions=[stepper.BACKWARD if motors[i]<0 else stepper.FORWARD for i in range(len(motors))]
        for i in range(max(motors)): #schedule together
            for j in range(len(motors)):
                if motors[j]>0:
                    self.motors[j].onestep(direction=directions[j], style=stepper.SINGLE)
                    motors[j]-=1
    def readBase(self):
        #read the force on rig
        pass
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
    