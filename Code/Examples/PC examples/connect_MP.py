#for the sake of running on my device - comment out
import sys
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/Rig-controller/Code/')
###################################################
import time
import Controller

path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
c= Controller.Controller('COM15',file=path)

print(c.getPressure())
c.move(10,10,10,10)