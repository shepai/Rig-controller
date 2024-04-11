#for the sake of running on my device - comment out
import sys
sys.path.insert(1, 'C:/Users/dexte/Documents/GitHub/Rig-controller/Code/')
###################################################
import time
import Controller
import DataLogger.data_xml as dx

path="C:/Users/dexte/Documents/GitHub/Rig-controller/Code/Examples/Board Examples/listener_MP.py"
path_to_save="C:/Users/dexte/Documents/AI/XML_sensors/sensor_trial_one"
c= Controller.Controller('COM19',file=path)
c.calibrate() #takes a while - only want to do once
#####################
# Set up secondary sensor
####################
#TODO

def runTrial(SAVER,dirs=[0,0]):
    c.reset_trial() #return to center position
    #move sensor across surface
    toMoveX=0
    toMoveY=0
    t1=time.time()
    for i in range(max(dirs)):
        #prevent negative
        if dirs[0]>0: toMoveX=min(dirs[0],10)
        else: toMoveX=0
        if dirs[1]>0: toMoveY=min(dirs[1],10)
        else: toMoveY=0
        c.move(toMoveX,toMoveY,0,0)
        #reduce by step
        dirs[0]-=toMoveX
        dirs[1]-=toMoveY
        data_sensor=["empty array to be replaced by sensor"] #TODO
        SAVER.upload(data_sensor,time.time()-t1,dirs+[0,0])

#####################
#Experiment hyperparameters
####################
num_experiments=1
num_of_trials=100
angle=0
speed=100
texture="none"
experiment=dx.Experiment(0,texture,80,20)
for exp in range(num_experiments):
    experiment.create_experiment(exp,texture,angle,speed)
    for trial in range(num_of_trials): #gives you the ability to average over number of trials
        print("Experiment",exp+1,"Trial",trial+1)
        for y in range(0,200,10): #move y along surface 
            for x in reversed(range(0,200,10)): #move direction of x along
                experiment.create_trial()
                runTrial(experiment,dirs=[x,y])
                c.move(0,0,100,0)
        experiment.save(path_to_save)



