#for the sake of running on my device - comment out
import sys
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/Rig-controller/Code/')
###################################################
import time
import Controller
c= Controller.Controller('COM14')
print("Connected")
while True:
    c.sendCommand("work please")
    print(">")
    d=c.listen_for_data()
    if d:
        print(d)

print("Done")