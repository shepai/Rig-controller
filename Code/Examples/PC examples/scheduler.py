#from TacTip import experiment
from efficient_image_record import experiment
import time
pe=-480
#-480 for normal -880 for Foam -230 for cork and carpets, -500 flat

t1=time.time()
e1=experiment(Pressure_extra=pe)
e1.runLinear("TTB/TTB_LacedMatt_P60",60)
e1.runLinear("TTB/TTB_LacedMatt_P80",80)
e1.runLinear("TTB/TTB_LacedMatt_P100",100)

#circle
e1.runCircle("TTB/non_linear/circle_TTB_LacedMatt_P60",60)
e1.runCircle("TTB/non_linear/circle_TTB_LacedMatt_P80",80)
e1.runCircle("TTB/non_linear/circle_TTB_LacedMatt_P100",100)

#pressure
e1.runPressure("TTB/non_linear/pressure_TTB_LacedMatt_P60",60)
e1.runPressure("TTB/non_linear/pressure_TTB_LacedMatt_P80",80)
e1.runPressure("TTB/non_linear/pressure_TTB_LacedMatt_P100",100)

t2=time.time()

print("TOTAL TIME",(t2-t1)/(60*60),"Hours")