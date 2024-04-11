#for the sake of running on my device - comment out
import sys
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/Rig-controller/Code/')
###################################################
import time
import Controller

path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
c= Controller.Controller('COM19',file=path)

print(c.getPressure())
#c.move(10,10,10,10)
c.calibrate() #takes a while - only want to do once
#c.sendCommand("CALIB") #SAY THAT IT IS ALREADY Calibrated
print(c.sendCommand("getmove"))
c.move(500,100,0,0) #move to new space
print(c.sendCommand("getmove"))
c.reset_trial() #return to center position
print(c.sendCommand("getmove"))