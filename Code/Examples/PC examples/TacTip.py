#for the sake of running on my device - comment out
import sys
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/Rig-controller/Code/')

###################################################
import time
import Controller
import DataLogger.data_xml as dx
import cv2
import numpy as np
import matplotlib.pyplot as plt

path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
path_to_save="C:/Users/dexte/Documents/AI/XML_sensors/TacTip_Flat"
c= Controller.Controller('COM19',file=path)
THRESH=6000
Pressure_extra=0
c.calibrate(value=THRESH,lower=False,val=-500-Pressure_extra) #takes a while - only want to do once
#c.sendCommand("CALIB") #do if already calibrated
#####################
# Set up secondary sensor
####################
print("Connecting to sensor")
cap = cv2.VideoCapture(1)
# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()
ret, frame = cap.read()
print("COMPONENTS",frame.shape)
sensor=[]
def runTrial(SAVER,dirs=[0,0]):
    global sensor
    c.reset_trial() #return to center position
    c.move(EDGE_VALUE+0,50,50,0)
    #move sensor across surface
    t1=time.time()
    x_vector=10*dirs[0]
    y_vector=10*dirs[1]
    for i in range(0,100):
        c.move(x_vector,y_vector,0,0)
        ret, frame = cap.read()
        if not ret:
            print("incorrect")
            frame=np.zeros((100,100,1))
        data_sensor=list(frame.shape)
        SAVER.upload(data_sensor,time.time(),[x_vector+i,y_vector+i]+[0,0])
        sensor.append(data_sensor)
        if len(sensor)>100: #prevent too many values
            sensor.pop(0)
        cv2.imshow('TacTip Feed', frame)
        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
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
EDGE_VALUE=0

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
