from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import busio
import board
from machine import Pin
import machine
import time
from Tactile_MP import Foot #found on my github
import hcsr04

class Rig:
    """
    Pinout

    I2C GP14 and GP15
    The buttons must be connceted to
    GP0,GP1 GP2 and GP3 each corrosponding to axis x,y,z,a
    Stepper motors must be x to board 1 y to board 1 z to board 2 a to board 2
    The foot or pressure sensor should be connected either through:
        I2C on 14 and 15
        or
        GP12, GP11, GP10, GP9 and the access pin to ground
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
        button_pins = [Pin(2,machine.Pin.IN,Pin.PULL_DOWN), Pin(8,machine.Pin.IN,Pin.PULL_DOWN), Pin(1,machine.Pin.IN,Pin.PULL_DOWN), Pin(0,machine.Pin.IN,Pin.PULL_DOWN)] #arduino 2,3,4,5
        
        # Initialize an array to hold the button objects
        self.buttons=button_pins
        #Initialise the plate
        self.plate=plate_mode
        if self.plate==1: #option one is normal plate
            self.sensor_plate=Foot([12,11,10,9],26,alpha=0.4)
        elif self.plate==2: #plate is i2c
           self.sensor_plate=Plate(Pin(26,machine.Pin.OUT),i2c=None,address=0x21,sda=None,scl=None,alpha=0.4)
        self.memory={"x":-1000,"y":-5200,"z":0,"a":0,"cx":0,"cy":0,"cz":0,"ca":0,"dist":9}
        self.inPosition=False
        #self.zero()
        trigger_pin = Pin(4, Pin.OUT)  # Change this to the pin connected to the trigger
        echo_pin = Pin(3, Pin.IN)      # Change this to the pin connected to the echo

        # Initialize the ultrasonic sensor
        self.sensor = hcsr04.HCSR04(trigger_pin, echo_pin)
    def reset(self,exclude=[1]):
        #move the rig till in the reset position
        buttons=self.readButtons()
        while 0 in [buttons[i] if i not in exclude else 1 for i in range(len(buttons))]: #loop till all pressed
            states=[(1-buttons[i])*100 for i in range(len(buttons))]
            self.moveMotors(states[3],states[2],states[0],states[1]) #only move ones not pressed
            buttons=self.readButtons()
    def getSensor(self):
        d=self.sensor.distance_cm()
        print(d)
        return d
    def moveMotors(self,x,y,z,a,style=stepper.DOUBLE):
        #move each motor by each value
        motors=[z*-1,a*1,y*1,x*1] #multiply by direction bias
        actualDir=[1 if x >= 0 else -1 for x in [z,a,y,x]]
        directions=[stepper.BACKWARD if motors[i]<0 else stepper.FORWARD for i in range(len(motors))]
        motors=[abs(motors[i]) for i in range(len(motors))]
        keys=["cz","ca","cy","cx"]
        top=max(motors)
        buttons=[0,0,0,0]
        for i in range(top): #schedule together
            for j in range(len(motors)):
                if i%2==0:#read every 2
                    buttons=self.readButtons()
                if motors[j]>0 and (buttons[j]==0 or actualDir[j]==-1):
                    self.motors[j].onestep(direction=directions[j], style=style)
                    motors[j]-=1
                    if self.inPosition: #if moved to position track movements
                        self.memory[keys[j]]-=actualDir[j]*1 #reverse direction to get back    
        print("moved")
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
    def lowerSensor(self,average=5000):
        av=0
        turns=0
        alpha=0.5
        read=self.readBase()
        last_av=(sum(read)/len(read))
        while av<average:
            self.moveMotors(0,0,-50,0)
            read=self.readBase()
            av=(sum(read)/len(read))*alpha + (1-alpha)*last_av
            last_av=av
            print(av)
            turns-=50
        self.memory['z']=turns
    def setPerfect(self):
        self.memory['dist']=self.getSensor()
    def centre(self):
        reading=self.getSensor()
        dist=reading-self.memory["dist"]
        while abs(dist)>1.5:
            if dist>0: #move one way
                self.moveMotors(0,-10,0,0)
            else: #move other
                self.moveMotors(0,10,0,0)
            reading=self.getSensor()
            dist=reading-self.memory["dist"]
        
    def central(self):
        self.moveMotors(self.memory['x'],self.memory['y'],self.memory['z'],0)
        #extra movement
        self.centre()
        self.inPosition=True
    def close(self):
        pass
    def zero(self):
        nums=0
        for i in range(250):
            plate=self.readBase()
            nums+=(sum(plate)/len(plate))
        nums/=250
        self.zero_fact=nums

class client:
    def listen_for_command(self,command=""): #listen for command from the data
        return command
    def send(self,message):
        print(f">{message}<")

