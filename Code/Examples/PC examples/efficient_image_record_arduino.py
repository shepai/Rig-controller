import sys
sys.path.insert(1, '/home/dexter/Documents/Rig-controller/Code/')
sys.path.insert(1, '/home/dexter/Documents/TactileSensor/Code') 
###################################################
import time
from Controller import Arduino_Rig as Controller
import cv2
import numpy as np
import matplotlib.pyplot as plt
import TactileSensor as ts
import os

class experiment:
    def __init__(self,name,FORCE,presstip=False):
        clear = lambda: os.system('clear')
        path="/home/dexter/Documents/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
        path_to_save="/home/dexter/Documents/data/"
        c= Controller("/dev/ttyACM1")
        THRESH=0
        Pressure_extra=935  #935 for normal, 450 for foam, 680 for carpet, 
        #c.reset()
        #c.calibrate(value=THRESH,lower=False,val=Pressure_extra) #takes a while - only want to do once
        #####################
        # Set up secondary sensor
        ####################
        print("Connecting to sensor")
        if not presstip:
            connected=False
            i=0
            while not connected:
                cap = cv2.VideoCapture(i)
                if not cap.isOpened():
                    print("Error: Unable to access the webcam.")
                    i+=1
                else:
                    print("CAmera channel",i)
                    connected=True
            ret, frame = cap.read()
        else: #presstip is there
            self.B=ts.Board()
            #get serial boards and connect to first one
            print("Connecting to sensor")
            self.B.connect("/dev/ttyACM1")
            print("Running file")
            self.B.runFile("/home/dexter/Documents/TactileSensor/Code/TactileSensor/Board side/boardSide.py")
            print("File ran")
            frame=np.array(list(self.B.getSensor(type_="round",num=16)))
        self.presstip=presstip
        print("COMPONENTS",frame.shape)


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
                    c.reset_trial() #return to center position
                    c.move(EDGE_VALUE+0,50,50-FORCE,0)
                    #move sensor across surface
                    t1=time.time()
                    x_vector=10*dirs[0]
                    y_vector=10*dirs[1]
                    if not self.presstip:
                        ret, frame = cap.read()
                        if not ret:
                            print("incorrect")
                            frame=np.zeros((100,100))
                    else:
                        frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                    ar=np.zeros((50,*frame.shape),dtype=np.uint8)
                    for i in range(0,50):
                        c.move(x_vector,y_vector,0,0)
                        if not self.presstip:
                            ret, frame = cap.read()
                            if not ret:
                                print("incorrect")
                                frame=np.zeros((100,100,1))
                        else:
                            frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                        ar[i]=frame
                        
                        cv2.imshow('TacTip Feed', frame)
                        # Check for the 'q' key to exit the loop
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    return ar
        data=np.zeros((num_experiments,num_of_trials,len(np.arange(0,1,0.1)),len(np.arange(0,1,0.1)),50,*frame.shape),dtype=np.uint8)
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
                            c.move(0,0,-500,0)
                        except KeyboardInterrupt:
                            c.reset_trial()
                            c.move(0,0,-500,0)
                            print("Paused... do you want to continue (ENTER yes ctrl-C no)")
                            input(">")
                if trial%10==0:
                    np.save(path_to_save+"/"+name,data) #constant backups

        #plt.show()
        print("TOTAL EXECUTION TIME:",(time.time()-starttime)/(60*60),"hours")



class experiment_circle:
    def __init__(self,name,FORCE,presstip=False):
        clear = lambda: os.system('clear')
        path="/home/dexter/Documents/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
        path_to_save="/home/dexter/Documents/data/"
        c= Controller("/dev/ttyACM1",file=path)
        THRESH=6000
        Pressure_extra=935  #-480 for normal -880 for foam -230 for cork and carpets -500 for flat
        #####################
        # Set up secondary sensor
        ####################
        print("Connecting to sensor")
        if not presstip:
            connected=False
            i=0
            while not connected:
                cap = cv2.VideoCapture(i)
                if not cap.isOpened():
                    print("Error: Unable to access the webcam.")
                    i+=1
                else:
                    print("CAmera channel",i)
                    connected=True
            ret, frame = cap.read()
        else:
            self.B=ts.Board()
            #get serial boards and connect to first one
            print("Connecting to sensor")
            self.B.connect("/dev/ttyACM2")
            print("Running file")
            self.B.runFile("/home/dexter/Documents/TactileSensor/Code/TactileSensor/Board side/boardSide.py")
            print("File ran")
            frame=np.array(list(self.B.getSensor(type_="round",num=16)))
            Pressure_extra-=400
        self.presstip=presstip
        c.calibrate(value=THRESH,lower=False,val=Pressure_extra) #takes a while - only want to do once
        print("COMPONENTS",frame.shape)


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
                    c.reset_trial() #return to center position
                    c.move(EDGE_VALUE+0,50,50-FORCE,0)
                    #move sensor across surface
                    t1=time.time()
                    if not self.presstip:
                        ret, frame = cap.read()
                        if not ret:
                            print("incorrect")
                            frame=np.zeros((100,100))
                    else:
                        frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                    ar=np.zeros((50,*frame.shape),dtype=np.uint8)
                    for i,t in enumerate(np.arange(0,5,0.1)):
                        x = radius * np.sin(t)
                        y = radius * np.cos(t)
                        c.move(x,y,0,0)
                        if not self.presstip:
                            ret, frame = cap.read()
                            if not ret:
                                print("incorrect")
                                frame=np.zeros((100,100))
                        else:
                            frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                        ar[i]=frame
                        
                        cv2.imshow('TacTip Feed', frame)
                        # Check for the 'q' key to exit the loop
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    return ar
        data=np.zeros((num_experiments,num_of_trials,len(np.arange(10,400,40)),50,*frame.shape),dtype=np.uint8)
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
                            c.move(0,0,-500,0)
                        except KeyboardInterrupt:
                            c.reset_trial()
                            c.move(0,0,-1000,0)
                            print("Paused... do you want to continue (ENTER yes ctrl-C no)")
                            input(">")
                if trial%10==0:
                    np.save(path_to_save+"/"+name,data) #constant backups

        #plt.show()
        print("TOTAL EXECUTION TIME:",(time.time()-starttime)/(60*60),"hours")



class experiment_pressure:
    def __init__(self,name,FORCE,presstip=False):
        clear = lambda: os.system('clear')
        path="/home/dexter/Documents/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
        path_to_save="/home/dexter/Documents/data/"
        c= Controller("/dev/ttyACM0",file=path)
        THRESH=6000
        Pressure_extra=935  #-480 for normal -880 for foam -230 for cork and carpets, -500 flat
        
        #####################
        # Set up secondary sensor
        ####################
        print("Connecting to sensor")
        if not presstip:
            connected=False
            i=0
            while not connected:
                cap = cv2.VideoCapture(i)
                if not cap.isOpened():
                    print("Error: Unable to access the webcam.")
                    i+=1
                else:
                    print("CAmera channel",i)
                    connected=True
            ret, frame = cap.read()
        else:
            self.B=ts.Board()
            #get serial boards and connect to first one
            print("Connecting to sensor")
            self.B.connect("/dev/ttyACM2")
            print("Running file")
            self.B.runFile("/home/dexter/Documents/TactileSensor/Code/TactileSensor/Board side/boardSide.py")
            print("File ran")
            frame=np.array(list(self.B.getSensor(type_="round",num=16)))
            Pressure_extra-=400
        self.presstip=presstip
        c.calibrate(value=THRESH,lower=False,val=Pressure_extra) #takes a while - only want to do once
        print("COMPONENTS",frame.shape)


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
                    c.reset_trial() #return to center position
                    c.move(EDGE_VALUE+0,50,50-FORCE,0)
                    #move sensor across surface
                    t1=time.time()
                    if not self.presstip:
                        ret, frame = cap.read()
                        if not ret:
                            print("incorrect")
                            frame=np.zeros((100,100))
                    else:
                        frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                    ar=np.zeros((50,*frame.shape),dtype=np.uint8)
                    increase=0
                    for i,t in enumerate(np.arange(0,5,0.1)):
                        x = radius * np.sin(t)
                        y = radius * np.cos(t)
                        c.move(x,y,increase*-1,0)
                        if not self.presstip:
                            ret, frame = cap.read()
                            if not ret:
                                print("incorrect")
                                frame=np.zeros((100,100))
                        else:
                            frame=np.array(list(self.B.getSensor(type_="round",num=16)))
                        ar[i]=frame
                        
                        cv2.imshow('TacTip Feed', frame)
                        # Check for the 'q' key to exit the loop
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                        increase+=0.01
                    return ar
                    
        data=np.zeros((num_experiments,num_of_trials,len(np.arange(10,400,40)),50,*frame.shape),dtype=np.uint8)
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
                            c.move(0,0,-500,0)
                        except KeyboardInterrupt:
                            c.reset_trial()
                            c.move(0,0,-1000,0)
                            print("Paused... do you want to continue (ENTER yes ctrl-C no)")
                            input(">")
                if trial%10==0:
                    np.save(path_to_save+"/"+name,data) #constant backups

        #plt.show()
        print("TOTAL EXECUTION TIME:",(time.time()-starttime)/(60*60),"hours")