from Rig_control import Rig, client
import time

rig=Rig(plate_mode=1) #create rig

def pressure():
    s=""
    vals=rig.readBase()
    if type(vals)==type([]):
        for char in vals:
            s+=str(char)+","
        print(s[:-1]) #send data of pads back
    else:
        print(vals)
def move(x,y,z,a):
    array=[x,y,z,a]
    rig.moveMotors(*array) #move the motors
def reset():
    rig.reset()

#1500
#3000
#z auto
#rig.reset()
#rig.lowerSensor()
#calibrate
#rig.reset()
#print("reset")
#rig.central()



