#from TacTip import experiment
from PressTip2 import experiment_2 as experiment
import time
t1=time.time()
e1=experiment("pressTip_big_flat_P60",60)
del e1
e1=experiment("pressTip_big_flat_P80",80)
del e1
e1=experiment("pressTip_big_flat_P100",100)
del e1 
t2=time.time()

print("TOTAL TIME",(t2-t1)/(60*60),"Hours")