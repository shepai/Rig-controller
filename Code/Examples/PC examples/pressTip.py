#for the sake of running on my device - comment out
import sys
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/Rig-controller/Code/')
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/TactileSensor/Code') 
###################################################
import time
import Controller
import DataLogger.data_xml as dx
import TactileSensor as ts
import numpy as np

path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
path_to_save="C:/Users/dexte/Documents/AI/XML_sensors/sensor_baseline"
c= Controller.Controller('COM19',file=path)
c.calibrate() #takes a while - only want to do once
#####################
# Set up secondary sensor
####################
B=ts.Board()
#get serial boards and connect to first one
print("Connecting to sensor")
B.connect("COM24")
B.runFile("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/TactileSensor/Board side/boardSide.py")
#B.autoConnect(file="C:/Users/dexte/Documents/GitHub/TactileSensor/Code/TactileSensor/Board side/boardSide.py")

def runTrial(SAVER,dirs=[0,0]):
    c.reset_trial() #return to center position
    #move sensor across surface
    t1=time.time()
    x_vector=10*dirs[0]
    y_vector=10*dirs[1]
    for i in range(0,100):
        c.move(x_vector,y_vector,0,0)
        data_sensor=list(B.getSensor(type_="round",num=16))
        SAVER.upload(data_sensor,time.time()[x_vector+i,y_vector+i]+[0,0])

#####################
#Experiment hyperparameters
####################
num_experiments=1
num_of_trials=100
angle=0
speed=100
texture="none"
experiment=dx.Experiment(0,texture,80,20)
starttime=time.time()
for exp in range(num_experiments):
    experiment.create_experiment(exp,texture,angle,speed)
    for trial in range(num_of_trials): #gives you the ability to average over number of trials
        print("Experiment",exp+1,"Trial",trial+1)
        for y in np.arange(0,1,0.1): #move y along surface 
            for x in reversed(np.arange(0,1,0.1)): #move direction of x along
                experiment.create_trial()
                runTrial(experiment,dirs=[x,y]) #send vector through
                c.move(0,0,500,0)
            experiment.save(path_to_save) #constant backups


print("EXECUTION TIME:",time.time()-starttime)
