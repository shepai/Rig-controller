from Rig_control import Rig, client

c=client() #create client
rig=Rig() #create rig

def pressure():
    s=""
    vals=rig.readBase()
    if type(vals)==type([]):
        for char in vals:
            s+=str(char)+","
        print(s[:,-1]) #send data of pads back
    else:
        print(vals)
def move(x,y,z,a):
    array=[a,z,y,x]
    rig.moveMotors(*array) #move the motors
def reset():
    rig.resetRig()