import sys
sys.path.insert(1, '/home/dexter/Documents/Rig-controller/Code/')
sys.path.insert(1, '/home/dexter/Documents/TactileSensor/Code') 
###################################################
import time
import Controller
import cv2
import numpy as np
import matplotlib.pyplot as plt
import TactileSensor as ts
import os
clear = lambda: os.system('clear')

class experiment:
    def __init__(self,presstip=False,Pressure_extra=-480):
        
        path="/home/dexter/Documents/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
        self.path_to_save="/home/dexter/Documents/data/"
        self.c= Controller.Controller("/dev/ttyACM1",file=path)
        THRESH=6000
        #Pressure_extra=-480  #-480 for normal -880 for foam -230 for cork and carpets
        #####################
        # Set up secondary sensor
        ####################
        print("Connecting to sensor")
        connected=False
        i=0
        self.cap=None
        if not presstip:
            while not connected:
                self.cap = cv2.VideoCapture(i)
                if not self.cap.isOpened():
                    print("Error: Unable to access the webcam.")
                    i+=1
                else:
                    print("CAmera channel",i)
                    connected=True
            ret, self.frame = self.cap.read()
        else: #presstip is there
            self.B=ts.Board()
            #get serial boards and connect to first one
            print("Connecting to sensor")
            self.B.connect("/dev/ttyACM2")
            print("Running file")
            self.B.runFile("/home/dexter/Documents/TactileSensor/Code/TactileSensor/Board side/boardSide.py")
            print("File ran")
            self.frame=np.array(list(self.B.getSensor(type_="round",num=16)))#
            Pressure_extra-=350
        self.presstip=presstip
        
        self.pressure_extra=Pressure_extra
        self.c.calibrate(value=THRESH,lower=False,val=Pressure_extra) #takes a while - only want to do once
        print("COMPONENTS",self.frame.shape)
    def getCamera(self):
        ret, frame = self.cap.read()
        if not ret:
            print("incorrect")
            i=0
            while not ret:
                self.cap = cv2.VideoCapture(i)
                if not self.cap.isOpened():
                    print("Error: Unable to access the webcam.")
                    i+=1
                else:
                    print("CAmera channel",i)
                    connected=True
                    ret, frame = self.cap.read()
                if i>10: i=0
            
        return frame
    def runLinear(self,name,FORCE):
        self.FORCE=FORCE
        #####################
        #Experiment hyperparameters
        ####################
        num_experiments=1
        num_of_trials=2
        starttime=time.time()
        total_operations=(num_of_trials*(len(np.arange(0,1,0.1))**2))*num_experiments
        EDGE_VALUE=0
        def runTrial(SAVER,dirs=[0,0]):
                    global sensor
                    global filename
                    self.c.reset_trial() #return to center position
                    self.c.move(EDGE_VALUE+0,50,50-self.FORCE,0)
                    #move sensor across surface
                    t1=time.time()
                    x_vector=10*dirs[0]
                    y_vector=10*dirs[1]
                    if not self.presstip:
                        frame=self.getCamera()
                    else:
                        frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                    ar=np.zeros((50,*frame.shape),dtype=np.uint8)
                    for i in range(0,50):
                        self.c.move(x_vector,y_vector,0,0)
                        if not self.presstip:
                            frame=self.getCamera()
                        else:
                            frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                        ar[i]=frame
                        
                        cv2.imshow('TacTip Feed', frame)
                        # Check for the 'q' key to exit the loop
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    return ar
        data=np.zeros((num_experiments,num_of_trials,len(np.arange(0,1,0.1)),len(np.arange(0,1,0.1)),50,*self.frame.shape),dtype=np.uint8)+1
        for exp in range(num_experiments):
            for trial in range(num_of_trials): #gives you the ability to average over number of trials
                for i,y in enumerate(np.arange(0,1,0.1)): #move y along surface 
                    for j,x in enumerate(reversed(np.arange(0,1,0.1))): #move direction of x along
                        total_operations_left=(num_experiments-exp)*(num_of_trials-trial)*(len(np.arange(0,1,0.1))*(len(np.arange(0,1,0.1))-i))
                        time_taken=(time.time()-starttime)/max(total_operations-total_operations_left,0.001)
                        clear()
                        print("Experiment",exp+1,"Trial",trial+1)
                        print("CURRENT EXECUTION TIME:",(time.time()-starttime)/(60),"minutes","\n\tEstimated time left:",
                            (time_taken*total_operations_left)/(60*60),"hours")                           
                        try:

                            dat=runTrial(experiment,dirs=[x,y]) #send vector through
                            data[exp][trial][i][j]=dat.copy()
                            self.c.move(0,0,500,0)
                        except KeyboardInterrupt:
                            self.c.reset_trial()
                            self.c.move(0,0,1000,0)
                            print("Paused... do you want to continue (ENTER yes ctrl-C no)")
                            input(">")
                if trial%10==0:
                    np.save(self.path_to_save+"/"+name,data) #constant backups
        del data
        #plt.show()
        print("TOTAL EXECUTION TIME:",(time.time()-starttime)/(60*60),"hours")

    def runCircle(self,name,FORCE):
        self.FORCE=FORCE
        #####################
        #Experiment hyperparameters
        ####################
        num_experiments=1
        num_of_trials=2
        starttime=time.time()
        total_operations=(num_of_trials*(len(np.arange(0,1,0.1))**2))*num_experiments
        EDGE_VALUE=0
        def runTrial(SAVER,radius):
                    global sensor
                    global filename
                    self.c.reset_trial() #return to center position
                    self.c.move(EDGE_VALUE+0,50,50-self.FORCE,0)
                    #move sensor across surface
                    global cap
                    t1=time.time()
                    if not self.presstip:
                        frame=self.getCamera()
                    else:
                        frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                    ar=np.zeros((50,*frame.shape),dtype=np.uint8)
                    for i,t in enumerate(np.arange(0,5,0.1)):
                        x = radius * np.sin(t)
                        y = radius * np.cos(t)
                        self.c.move(x,y,0,0)
                        if not self.presstip:
                            frame=self.getCamera()
                        else:
                            frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                        ar[i]=frame
                        
                        cv2.imshow('TacTip Feed', frame)
                        # Check for the 'q' key to exit the loop
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    return ar
        data=np.zeros((num_experiments,num_of_trials,len(np.arange(10,400,40)),50,*self.frame.shape),dtype=np.uint8)
        for exp in range(num_experiments):
            for trial in range(num_of_trials): #gives you the ability to average over number of trials
                for i,y in enumerate(np.arange(10,100,10)): #chose radius
                        total_operations_left=(num_experiments-exp)*(num_of_trials-trial)*(len(np.arange(0,1,0.1))*(len(np.arange(0,1,0.1))-i))
                        time_taken=(time.time()-starttime)/max(total_operations-total_operations_left,0.001)
                        clear()
                        print("Experiment",exp+1,"Trial",trial+1)
                        print("CURRENT EXECUTION TIME:",(time.time()-starttime)/(60),"minutes","\n\tEstimated time left:",
                            (time_taken*total_operations_left)/(60*60),"hours")                           
                        try:

                            dat=runTrial(experiment,y) #send vector through
                            data[exp][trial][i]=dat.copy()
                            self.c.move(0,0,500,0)
                        except KeyboardInterrupt:
                            self.c.reset_trial()
                            self.c.move(0,0,1000,0)
                            print("Paused... do you want to continue (ENTER yes ctrl-C no)")
                            input(">")
                if trial%10==0:
                    np.save(self.path_to_save+"/"+name,data) #constant backups
        del data
        #plt.show()
        print("TOTAL EXECUTION TIME:",(time.time()-starttime)/(60*60),"hours")
    
    def runPressure(self,name,FORCE):
        self.FORCE=FORCE
        #####################
        #Experiment hyperparameters
        ####################
        num_experiments=1
        num_of_trials=2
        starttime=time.time()
        total_operations=(num_of_trials*(len(np.arange(0,1,0.1))**2))*num_experiments
        EDGE_VALUE=0
        def runTrial(SAVER,radius):
                    global sensor
                    global filename
                    self.c.reset_trial() #return to center position
                    self.c.move(EDGE_VALUE+0,50,50-self.FORCE,0)
                    #move sensor across surface
                    t1=time.time()
                    if not self.presstip:
                        frame=self.getCamera()
                    else:
                        frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                    ar=np.zeros((50,*frame.shape),dtype=np.uint8)
                    increase=0
                    for i,t in enumerate(np.arange(0,5,0.1)):
                        x = radius * np.sin(t)
                        y = radius * np.cos(t)
                        self.c.move(x,y,increase*-1,0)
                        if not self.presstip:
                            frame=self.getCamera()
                        else:
                            frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                        ar[i]=frame
                        
                        cv2.imshow('TacTip Feed', frame)
                        # Check for the 'q' key to exit the loop
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                        increase+=0.01
                    return ar
                    
        data=np.zeros((num_experiments,num_of_trials,len(np.arange(10,400,40)),50,*self.frame.shape),dtype=np.uint8)
        for exp in range(num_experiments):
            for trial in range(num_of_trials): #gives you the ability to average over number of trials
                for i,y in enumerate(np.arange(10,100,10)): #chose radius
                        total_operations_left=(num_experiments-exp)*(num_of_trials-trial)*(len(np.arange(0,1,0.1))*(len(np.arange(0,1,0.1))-i))
                        time_taken=(time.time()-starttime)/max(total_operations-total_operations_left,0.001)
                        clear()
                        print("Experiment",exp+1,"Trial",trial+1)
                        print("CURRENT EXECUTION TIME:",(time.time()-starttime)/(60),"minutes","\n\tEstimated time left:",
                            (time_taken*total_operations_left)/(60*60),"hours")                           
                        try:

                            dat=runTrial(experiment,y) #send vector through
                            data[exp][trial][i]=dat.copy()
                            self.c.move(0,0,500,0)
                        except KeyboardInterrupt:
                            self.c.reset_trial()
                            self.c.move(0,0,1000,0)
                            print("Paused... do you want to continue (ENTER yes ctrl-C no)")
                            input(">")
                if trial%10==0:
                    np.save(self.path_to_save+"/"+name,data) #constant backups
        del data
        #plt.show()
        print("TOTAL EXECUTION TIME:",(time.time()-starttime)/(60*60),"hours")
