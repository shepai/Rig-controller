#from TacTip import experiment
from efficient_image_record import experiment
import time
t1=time.time()
e1=experiment("TTA_Leather_P60",60)
del e1
e1=experiment("TTA_Leather_flat_P80",80)
del e1
e1=experiment("TTA_Leather_flat_P100",100)
del e1 
t2=time.time()

print("TOTAL TIME",(t2-t1)/(60*60),"Hours")