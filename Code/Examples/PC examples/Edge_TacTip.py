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
import os

def Experiment(name,FORCE):
    path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
    path_to_save="C:/Users/dexte/Documents/AI/XML_sensors/"
    path_ = os.path.join(path_to_save, name) 
    try:
        os.remove(path_)
    except:
        pass
    try:
        os.mkdir(path_) 
    except:
        pass
    path_to_save=path_to_save+name+"/"+name
    c= Controller.Controller('COM19',file=path)
    THRESH=6000
    Pressure_extra=-100 #0 for normal #-350 for cork#350 for foam
    c.calibrate(value=THRESH,lower=False,val=-500-Pressure_extra) #takes a while - only want to do once
    c.move(0,-3000,100,0) #0,-3000,-100,0
    num_experiments=1
    num_of_trials=4
    angle=0
    speed=100
    texture="Plastic"
    print("Connecting to sensor")
    cap = cv2.VideoCapture(1)
    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Unable to access the webcam.")
        exit()
    ret, frame = cap.read()
    print("COMPONENTS",frame.shape)
    experiment=dx.Experiment(0,texture,angle,speed)
    starttime=time.time()
    total_operations=(num_of_trials*(len(np.arange(0,1,0.1))**2))*num_experiments
    EDGE_VALUE=0
    for exp in range(num_experiments):
        experiment.create_experiment(exp,texture,angle,speed)
        for trial in range(num_of_trials): #gives you the ability to average over number of trials
            experiment.create_trial()
            #for rotation in range(0,100,20):
                #c.move(0,0,0,rotation) #0,-3000,-100,0
            ar=[]
            for i in range(10):
                #move down
                c.move(0,0,-1*(200+FORCE),0) #0,-3000,-100,0
                #record
                ret, frame = cap.read()
                if not ret:
                    print("incorrect")
                    frame=np.zeros((100,100,1))
                cv2.imshow('TacTip Feed', frame)
                # Check for the 'q' key to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                data_sensor=list(frame.flatten())
                ar.append(data_sensor)
                #print("record",30+(2*i),"% on edge")
                time.sleep(1)
                #move up and along
                c.move(0,20,(200+FORCE),0) 
            c.move(0,20,500,0) 
            c.reset_trial(centering=False)
            c.move(0,-3000,100,0) #0,-3000,-100,0
            ar=np.array(ar)
            filename=str(trial)+"-"+str(i)
            np.savez_compressed(path_to_save+"_"+filename,ar)
            experiment.upload(filename,time.time(),[0,0]+[0,0])
            experiment.save(path_to_save) #constant backups       

#Experiment("test",0)