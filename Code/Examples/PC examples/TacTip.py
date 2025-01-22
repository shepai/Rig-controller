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
filename=""
sensor=[]
class experiment:
    def __init__(self,name,FORCE):
        global filename
        global sensor
        clear = lambda: os.system('cls')
        path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
        path_to_save="C:/Users/dexte/Documents/AI/XML_sensors/"
        #name="TacTip_Efoam_P100"
        #FORCE=100 #0, 10, 20, 30, 40, 50, 60, 70, 80 ,90
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
        Pressure_extra=40  #-200 for carpet #-100 for plastic #0 for normal #-350 for cork#350 for foam #-10 for pressurepad
        c.calibrate(value=THRESH,lower=False,val=-500-Pressure_extra) #takes a while - only want to do once
        #c.move(0,0,900,0)
        #c.move(0,0,-500-Pressure_extra,0)
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
            global filename
            c.reset_trial() #return to center position
            c.move(EDGE_VALUE+0,50,50-FORCE,0)
            #move sensor across surface
            t1=time.time()
            x_vector=10*dirs[0]
            y_vector=10*dirs[1]
            ar=[]
            for i in range(0,100):
                c.move(x_vector,y_vector,0,0)
                ret, frame = cap.read()
                if not ret:
                    print("incorrect")
                    frame=np.zeros((100,100,1))
                data_sensor=list(frame.flatten())
                ar.append(data_sensor)
                SAVER.upload(filename,time.time(),[x_vector+i,y_vector+i]+[0,0])
                sensor.append(data_sensor)
                if len(sensor)>100: #prevent too many values
                    sensor.pop(0)
                cv2.imshow('TacTip Feed', frame)
                # Check for the 'q' key to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            ar=np.array(ar)
            np.savez_compressed(path_to_save+"_"+filename,ar)
        #####################
        #Experiment hyperparameters
        ####################
        num_experiments=1
        num_of_trials=2
        angle=0
        speed=100
        texture="Plastic"
        experiment=dx.Experiment(0,texture,angle,speed)
        starttime=time.time()
        total_operations=(num_of_trials*(len(np.arange(0,1,0.1))**2))*num_experiments
        EDGE_VALUE=0


        for exp in range(num_experiments):
            experiment.create_experiment(exp,texture,angle,speed)
            for trial in range(num_of_trials): #gives you the ability to average over number of trials
                total_operations_left=(num_experiments-exp)*(num_of_trials-trial)
                for i,y in enumerate(np.arange(0,1,0.1)): #move y along surface 
                    for x in reversed(np.arange(0,1,0.1)): #move direction of x along
                        total_operations_left=(num_experiments-exp)*(num_of_trials-trial)*(len(np.arange(0,1,0.1))*(len(np.arange(0,1,0.1))-i))
                        time_taken=(time.time()-starttime)/max(total_operations-total_operations_left,0.001)
                        clear()
                        print("Experiment",exp+1,"Trial",trial+1)
                        print("CURRENT EXECUTION TIME:",(time.time()-starttime)/(60),"minutes","\n\tEstimated time left:",(time_taken*total_operations_left)/(60*60),"hours")
                        
                        try:
                            experiment.create_trial()
                            filename=str(trial)+"-"+str(y)+"-"+str(x)
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

class experiment_2:
    def __init__(self,name,FORCE):
        global filename
        global sensor
        clear = lambda: os.system('cls')
        path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
        path_to_save="C:/Users/dexte/Documents/AI/XML_sensors/"
        #name="TacTip_Efoam_P100"
        #FORCE=100 #0, 10, 20, 30, 40, 50, 60, 70, 80 ,90
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
        Pressure_extra=0  #-200 for carpet #-100 for plastic #0 for normal #-350 for cork#350 for foam #-10 for pressurepad
        c.calibrate(value=THRESH,lower=False,val=10) #takes a while - only want to do once
        #c.sendCommand("CALIB") #do if already calibrated
        #####################
        # Set up secondary sensor
        ####################
        print("Connecting to sensor")
        cap = cv2.VideoCapture(0)
        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Unable to access the webcam.")
            exit()
        ret, frame = cap.read()
        print("COMPONENTS",frame.shape)
        sensor=[]
        def runTrial(SAVER,dirs=[0,0]):
            global sensor
            global filename
            c.reset_trial() #return to center position
            c.move(EDGE_VALUE+0,50,50-FORCE,0)
            #move sensor across surface
            t1=time.time()
            x_vector=10*dirs[0]
            y_vector=10*dirs[1]
            ar=[]
            for i in range(0,100):
                c.move(x_vector,y_vector,0,0)
                ret, frame = cap.read()
                if not ret:
                    print("incorrect")
                    frame=np.zeros((100,100,1))
                data_sensor=list(frame.flatten())
                ar.append(data_sensor)
                SAVER.upload(filename,time.time(),[x_vector+i,y_vector+i]+[0,0])
                sensor.append(data_sensor)
                if len(sensor)>100: #prevent too many values
                    sensor.pop(0)
                cv2.imshow('TacTip Feed', frame)
                # Check for the 'q' key to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            ar=np.array(ar)
            np.savez_compressed(path_to_save+"_"+filename,ar)
        #####################
        #Experiment hyperparameters
        ####################
        num_experiments=1
        num_of_trials=100
        angle=0
        speed=100
        texture="Plastic"
        experiment=dx.Experiment(0,texture,angle,speed)
        starttime=time.time()
        total_operations=(num_of_trials*(len(np.arange(0,1,0.1))**2))*num_experiments
        EDGE_VALUE=0


        for exp in range(num_experiments):
            experiment.create_experiment(exp,texture,angle,speed)
            for trial in range(num_of_trials): #gives you the ability to average over number of trials
                
                clear()
                print("Experiment",exp+1,"Trial",trial+1)
                
                try:
                    experiment.create_trial()
                    x=0
                    y=1
                    filename=str(trial)+"-"+str(y)+"-"+str(x)
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

class pressure:
    def __init__(self,name,FORCE):
        global filename
        global sensor
        path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
        path_to_save="C:/Users/dexte/Documents/AI/XML_sensors/"
        self.c= Controller.Controller('COM19',file=path)
        THRESH=6000
        Pressure_extra=-150  #-200 for carpet #-100 for plastic #0 for normal #-350 for cork#350 for foam #-10 for pressurepad
        #self.c.calibrate(value=THRESH,lower=False,val=-500-Pressure_extra) #takes a while - only want to do once
        self.FORCE=FORCE
        #self.c.move(0,0,-50,0)
    def move(self,pressure):
        #self.c.reset_trial() #return to center position
        self.c.move(0,0,(pressure)*-1,0)
        time.sleep(5)
        self.c.move(0,0,pressure,0)

class experiment_np:
    def __init__(self,name,FORCE):
        global filename
        global sensor
        clear = lambda: os.system('cls')
        path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
        path_to_save="C:/Users/dexte/Documents/AI/XML_sensors/"
        #name="TacTip_Efoam_P100"
        #FORCE=100 #0, 10, 20, 30, 40, 50, 60, 70, 80 ,90
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
        Pressure_extra=40  #-200 for carpet #-100 for plastic #0 for normal #-350 for cork#350 for foam #-10 for pressurepad
        c.calibrate(value=THRESH,lower=False,val=-500-Pressure_extra) #takes a while - only want to do once
        #c.move(0,0,900,0)
        #c.move(0,0,-500-Pressure_extra,0)
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
            global filename
            c.reset_trial() #return to center position
            c.move(EDGE_VALUE+0,50,50-FORCE,0)
            #move sensor across surface
            t1=time.time()
            x_vector=10*dirs[0]
            y_vector=10*dirs[1]
            ar=[]
            for i in range(0,100):
                c.move(x_vector,y_vector,0,0)
                ret, frame = cap.read()
                if not ret:
                    print("incorrect")
                    frame=np.zeros((100,100,1))
                data_sensor=list(frame.flatten())
                ar.append(data_sensor)
                SAVER.upload(filename,time.time(),[x_vector+i,y_vector+i]+[0,0])
                sensor.append(data_sensor)
                if len(sensor)>100: #prevent too many values
                    sensor.pop(0)
                cv2.imshow('TacTip Feed', frame)
                # Check for the 'q' key to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            ar=np.array(ar)
            return ar
        #####################
        #Experiment hyperparameters
        ####################
        num_experiments=1
        num_of_trials=2
        angle=0
        speed=100
        texture="Plastic"
        #experiment=dx.Experiment(0,texture,angle,speed)
        starttime=time.time()
        total_operations=(num_of_trials*(len(np.arange(0,1,0.1))**2))*num_experiments
        EDGE_VALUE=0

        dataset=[]
        for exp in range(num_experiments):
            #experiment.create_experiment(exp,texture,angle,speed)
            for trial in range(num_of_trials): #gives you the ability to average over number of trials
                total_operations_left=(num_experiments-exp)*(num_of_trials-trial)
                for i,y in enumerate(np.arange(0,1,0.1)): #move y along surface 
                    for x in reversed(np.arange(0,1,0.1)): #move direction of x along
                        total_operations_left=(num_experiments-exp)*(num_of_trials-trial)*(len(np.arange(0,1,0.1))*(len(np.arange(0,1,0.1))-i))
                        time_taken=(time.time()-starttime)/max(total_operations-total_operations_left,0.001)
                        clear()
                        print("Experiment",exp+1,"Trial",trial+1)
                        print("CURRENT EXECUTION TIME:",(time.time()-starttime)/(60),"minutes","\n\tEstimated time left:",(time_taken*total_operations_left)/(60*60),"hours")
                        
                        try:
                            #experiment.create_trial()
                            filename=str(trial)+"-"+str(y)+"-"+str(x)
                            data=runTrial(dirs=[x,y]) #send vector through
                            dataset.append(data)
                            c.move(0,0,500,0)
                        except KeyboardInterrupt:
                            c.reset_trial()
                            c.move(0,0,1000,0)
                            print("Paused... do you want to continue (ENTER yes ctrl-C no)")
                            input(">")
                    
                    np.savez_compressed(path_to_save+"/"+name,np.array(dataset).astype(np.uint8)) #constant backups

        #plt.show()
        print("TOTAL EXECUTION TIME:",(time.time()-starttime)/(60*60),"hours")