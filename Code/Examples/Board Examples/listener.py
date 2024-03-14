from Rig_control import Rig, client

c=client() #create client
rig=Rig() #create rig

while True:
    command=c.listen_for_command()
    #print("Device",command)
    assert type(command)==type(""), "Incorrect command format"
    if command=="pressure": #send pressure 
        s=""
        for char in rig.readBase():
            s+=str(char)+","
        print(">"+s[:,]+"<") #send data of pads back
    elif "MOVE" in command: #move the rig in direction
        command=command.replace("MOVE","").replace(":","")
        dirs=command.split(",")
        ar={}
        for dir_ in dirs:
            dim=dir_.split(":")
            ar[dim[0]]=int(dim[1]) #split letter from key
        assert len(list(ar.keys()))==4, "Incorrect number of motor positions"
        array=[ar['x'],ar['y'],ar['z'],ar['a']]
        rig.moveMotors(*array) #move the motors
    elif "RESET"==command: #reset the rig
        rig.resetRig()
    else:
        print(">incorrect command<")


