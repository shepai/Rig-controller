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
import matplotlib.pyplot as plt

path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
path_to_save="C:/Users/dexte/Documents/AI/XML_sensors/sensor_P40"
c= Controller.Controller('COM19',file=path)
THRESH=5500
c.calibrate(value=THRESH) #takes a while - only want to do once
#c.sendCommand("CALIB") #do if already calibrated
#####################
# Set up secondary sensor
####################
B=ts.Board()
#get serial boards and connect to first one
print("Connecting to sensor")
B.connect("COM24")
print("Running file")
B.runFile("C:/Users/dexte/Documents/GitHub/TactileSensor/Code/TactileSensor/Board side/boardSide.py")
print("File ran")
sensor=[]
def runTrial(SAVER,dirs=[0,0]):
    global sensor
    c.reset_trial() #return to center position
    c.move(0,50,50,0)
    #move sensor across surface
    t1=time.time()
    x_vector=10*dirs[0]
    y_vector=10*dirs[1]
    for i in range(0,100):
        c.move(x_vector,y_vector,0,0)
        data_sensor=list(B.getSensor(type_="round",num=16))
        SAVER.upload(data_sensor,time.time(),[x_vector+i,y_vector+i]+[0,0])
        sensor.append(data_sensor)
        if len(sensor)>100: #prevent too many values
            sensor.pop(0)
        #plt.cla()
        #plt.plot(sensor) #show sensor 
        #plt.title("Live stream from sensor")
        #plt.pause(0.009)
    #plt.cla()
#####################
#Experiment hyperparameters
####################
num_experiments=1
num_of_trials=5
angle=0
speed=100
texture="C40"
experiment=dx.Experiment(0,texture,angle,speed)
starttime=time.time()
total_operations=num_of_trials*num_experiments
for exp in range(num_experiments):
    experiment.create_experiment(exp,texture,angle,speed)
    for trial in range(num_of_trials): #gives you the ability to average over number of trials
        print("Experiment",exp+1,"Trial",trial+1)
        total_operations_left=(num_experiments-exp)*(num_of_trials-trial)
        time_taken=(time.time()-starttime)/max(total_operations-total_operations_left,0.001)
        print("CURRENT EXECUTION TIME:",(time.time()-starttime)/(60),"minutes","\n\tEstimated time left:",(time_taken*total_operations_left)/(60),"minutes")
        for y in np.arange(0,1,0.1): #move y along surface 
            for x in reversed(np.arange(0,1,0.1)): #move direction of x along
                try:
                    experiment.create_trial()
                    runTrial(experiment,dirs=[x,y]) #send vector through
                    c.move(0,0,500,0)
                except KeyboardInterrupt:
                    c.reset_trial()
                    c.move(0,0,1000,0)
                    print("Paused... do you want to continue (ENTER yes ctrl-C no)")
                    input(">")
            experiment.save(path_to_save) #constant backups

#plt.show()
print("TOTAL EXECUTION TIME:",(time.time()-starttime)/(60*60),"hours")
