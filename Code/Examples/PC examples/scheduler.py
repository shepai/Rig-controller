#from TacTip import experiment
from efficient_image_record import experiment
from efficient_image_record import experiment_circle as experiment1
from efficient_image_record import experiment_pressure as experiment2
import time
t1=time.time()
e1=experiment("TTA_Cork_P60",60)
del e1
e1=experiment("TTA_Cork_P80",80)
del e1
e1=experiment("TTA_Cork_P100",100)
del e1 

#circle
e1=experiment1("circle_TTA_Cork_P60",60)
del e1
e1=experiment1("circle_TTA_Cork_P80",80)
del e1
e1=experiment1("circle_TTA_Cork_P100",100)
del e1 

#pressure
e1=experiment2("pressure_TTA_Cork_P60",60)
del e1
e1=experiment2("pressure_TTA_Cork_P80",80)
del e1
e1=experiment2("pressure_TTA_Cork_P100",100)
del e1 
t2=time.time()

print("TOTAL TIME",(t2-t1)/(60*60),"Hours")