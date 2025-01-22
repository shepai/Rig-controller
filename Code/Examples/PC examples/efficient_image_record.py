import sys
sys.path.insert(1, '/home/dexter/Documents/Rig-controller/Code/')
sys.path.insert(1, '/home/dexter/Documents/TactileSensor/Code') 
###################################################
import time
import Controller
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

class experiment:
    def __init__(self,name,FORCE):
        clear = lambda: os.system('cls')
        path="/home/dexter/Documents/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
        path_to_save="/home/dexter/Documents/data/"
        c= Controller.Controller("/dev/ttyACM1",file=path)
        THRESH=6000
        Pressure_extra=0  #-200 for carpet #-100 for plastic #0 for normal #-350 for cork#350 for foam #-10 for pressurepad
        #c.calibrate(value=THRESH,lower=False,val=10) #takes a while - only want to do once
        #####################
        # Set up secondary sensor
        ####################
        print("Connecting to sensor")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Unable to access the webcam.")
            exit()
        ret, frame = cap.read()
        print("COMPONENTS",frame.shape)


        #####################
        #Experiment hyperparameters
        ####################
        num_experiments=1
        num_of_trials=100
        angle=0
        speed=100
        texture="Plastic"
        starttime=time.time()
        total_operations=(num_of_trials*(len(np.arange(0,1,0.1))**2))*num_experiments
        EDGE_VALUE=0
        def runTrial(SAVER,dirs=[0,0]):
                    global sensor
                    global filename
                    c.reset_trial() #return to center position
                    c.move(EDGE_VALUE+0,50,50-FORCE,0)
                    #move sensor across surface
                    t1=time.time()
                    x_vector=10*dirs[0]
                    y_vector=10*dirs[1]
                    ret, frame = cap.read()
                    ar=np.zeros((100,*frame.shape),dtype=np.uint8)
                    for i in range(0,100):
                        c.move(x_vector,y_vector,0,0)
                        ret, frame = cap.read()
                        if not ret:
                            print("incorrect")
                            frame=np.zeros((100,100,1))
                        ar[i]=frame
                        
                        cv2.imshow('TacTip Feed', frame)
                        # Check for the 'q' key to exit the loop
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    return ar
        data=np.zeros((num_experiments,num_of_trials,100,*frame.shape),dtype=np.uint8)
        for exp in range(num_experiments):
            for trial in range(num_of_trials): #gives you the ability to average over number of trials
                clear()
                print("Experiment",exp+1,"Trial",trial+1)
                try:
                    x=0
                    y=1
                    dat=runTrial(experiment,dirs=[x,y]) #send vector through
                    data[exp][trial]=dat.copy()
                    c.move(0,0,500,0)
                except KeyboardInterrupt:
                    c.reset_trial()
                    c.move(0,0,1000,0)
                    print("Paused... do you want to continue (ENTER yes ctrl-C no)")
                    input(">")
                if trial%10==0:
                    np.save(path_to_save+"/"+name,data) #constant backups

        #plt.show()
        print("TOTAL EXECUTION TIME:",(time.time()-starttime)/(60*60),"hours")