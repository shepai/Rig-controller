import xml.etree.ElementTree as ET
import pandas as pd

class Experiment:
    def __init__(self,ID,texture,angle,speed):
        # Create the root element
        self.dataset=ET.Element("Dataset")
        self.create_experiment(ID,texture,angle,speed)
    def save(self,name): # Save the file
        name=name.replace(".xml","")
        tree = ET.ElementTree(self.dataset)
        tree.write(name+".xml", encoding='utf-8', xml_declaration=True, method="xml", short_empty_elements=False)
    def load(self,filename): # Load a previous file and begin here left off
        filename=filename.replace(".xml","")
        tree = ET.parse(filename+".xml")
        # Get the root element
        self.dataset = tree.getroot()
    def create_experiment(self,ID,texture,angle,speed): #create ne 
        self.root=ET.SubElement(self.dataset,"Experiment")
        self.root.set("ID", str(ID))
        self.root.set("Texture", str(texture))
        self.root.set("Angle", str(angle))
        self.root.set("Speed", str(speed))
        self.currentExp=None
        self.id=0
    def create_trial(self): # Call each time you begin a ne trial 
        self.currentExp = ET.SubElement(self.root, "Trial")
        self.currentExp.set("No",str(self.id))
        self.id+=1
    def upload(self,data_sensor,time,position_s): #upload each reading
        trial = ET.SubElement(self.currentExp, "Reading")
        trial.set("Time",str(time))
        position = ET.SubElement(trial, "Position")
        position.text=str(position_s)
        data = ET.SubElement(trial, "Data")
        data.text=str(data_sensor)

class Loader: #class for generating datasets and labels from the gathered experiments
    def __init__(self,filename):
        filename=filename.replace(".xml","")
        tree = ET.parse(filename+".xml")
        # Get the root element
        self.dataset = tree.getroot()
    def convertText(self,data):
        data=data.replace("[","").replace("]","").replace(" ","")
        data=data.split(",")
        ints=[]
        for entry in data:
            ints.append(int(entry))
        return ints
    def getByExperiment(self):
        label=[]
        positions=[]
        readings=[]
        trials=[]
        times=[]
        for exp in self.dataset.findall("Experiment"):
            for trial in exp.findall("Trial"):
                for reading in trial.findall("Reading"):
                    for position,data in zip(reading.findall("Position"),reading.findall("Data")):
                        trials.append(trial.get("No"))
                        label.append(exp.get("Texture"))
                        readings.append(self.convertText(data.text))
                        positions.append(self.convertText(position.text))
                        times.append(reading.get("Time"))
                    
        data = {
            "Trial": trials,
            "Textures": label,
            "Positions": positions,
            "Readings": readings
        }
        df = pd.DataFrame(data)
        return df
    def getByPressure(self):
        pass
    def getBySpeed(self):
        pass
    def getByAngle(self):
        pass
    def getByDirection(self):
        pass

loader=Loader("C:/Users/dexte/Documents/GitHub/Rig-controller/Code/DataLogger/test.xml")
frame=loader.getByExperiment()
print(frame)
"""test=Experiment(1,"ss",80,20)
test.create_trial()
test.upload([0,1,1,0],0.1,[1,2,3])
test.upload([0,1,1,0],0.1,[1,2,3])
test.upload([0,1,1,0],0.1,[1,2,3])
test.upload([0,1,1,0],0.1,[1,2,3])

test.create_trial()
test.upload([0,1,1,0],0.1,[1,2,3])
test.upload([0,1,1,0],0.1,[1,2,3])
test.upload([0,1,1,0],0.1,[1,2,3])
test.upload([0,1,1,0],0.1,[1,2,3])

test.save("C:/Users/dexte/Documents/AI/XML_sensors/test")
del test
test=Experiment(1,"ss",80,20)
test.load("C:/Users/dexte/Documents/AI/XML_sensors/test")
test.create_trial()
test.upload([0,1,1,0],0.1,[1,2,3])
test.upload([0,1,1,0],0.1,[1,2,3])
test.upload([0,1,1,0],0.1,[1,2,3])
test.upload([0,1,1,0],0.1,[1,2,3])

"""