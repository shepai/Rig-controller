#from TacTip import experiment
from efficient_image_record_arduino import experiment
from efficient_image_record_arduino import experiment_circle as experiment1
from efficient_image_record_arduino import experiment_pressure as experiment2
import time
t1=time.time()
e1=experiment("TTC_Leather_P60",60)
del e1
e1=experiment("TTC_Leather_flat_P80",80)
del e1
e1=experiment("TTC_Leather_flat_P100",100)
del e1 
t2=time.time()

#circle
e1=experiment1("circle_TTC_Leather_P60",60)
del e1
e1=experiment1("circle_TTC_Leather_P80",80)
del e1
e1=experiment1("circle_TTC_Leather_P100",100)
del e1 

#pressure
e1=experiment2("pressure_TTC_Leather_P60",60)
del e1
e1=experiment2("pressure_TTC_Leather_P80",80)
del e1
e1=experiment2("pressure_TTC_Leather_P100",100)


print("TOTAL TIME",(t2-t1)/(60*60),"Hours")
