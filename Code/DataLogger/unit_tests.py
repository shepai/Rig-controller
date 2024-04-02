from data_xml import *

class Test:
    def __init__(self):
        self.passes=0
        self.setup()
        try:
            self.test1()
            self.passes+=1
        except AssertionError as e:
            print(e)
        self.tearDon()
        self.setup()
        try:
            self.test2()
            self.passes+=1
        except AssertionError as e:
            print(e)
        self.tearDon()
        self.setup()
        try:
            self.test3()
            self.passes+=1
        except AssertionError as e:
            print(e)
        print("Tests passed",self.passes,"/3")
    def setup(self):
        self.test=Experiment(1,"ss",80,20)
    def tearDon(self):
        del self.test
    def test1(self):
        #setup one expriment
        self.test.create_trial()
        self.test.upload([0,1,1,0],0.1,[1,2,3])
        self.test.upload([0,1,1,0],0.1,[1,2,3])
        ids=[]
        for exp in self.test.root.findall("Trial"):
            data=exp.get("No")
            ids.append(data)
        assert len(ids)==1,"1: Incorrect number of Experiments "+str(len(ids))
        #check it adds more on trials
        self.test.create_trial()
        self.test.upload([0,1,1,0],0.1,[1,2,3])
        self.test.upload([0,1,1,0],0.1,[1,2,3])
        ids=[]
        for exp in self.test.root.findall("Trial"):
            data=exp.get("No")
            ids.append(data)
        assert len(ids)==2,"2: Incorrect number of Experiments "+str(len(ids))
        for i in range(100):
            #check it adds more on trials
            self.test.create_trial()
            self.test.upload([0,1,1,0],0.1,[1,2,3])
            self.test.upload([0,1,1,0],0.1,[1,2,3])
            ids=[]
        #check it does it for many
        for exp in self.test.root.findall("Trial"):
                data=exp.get("No")
                ids.append(data)
        assert len(ids)==102,"2: Incorrect number of Experiments "+str(len(ids))
    def test2(self):
        #check if you can add more experiments
        for i in range(10):
            #check it adds more on trials
            self.test.create_trial()
            self.test.upload([0,1,1,0],0.1,[1,2,3])
            self.test.upload([0,1,1,0],0.1,[1,2,3])
        self.test.create_experiment(2,"eee",23,200)
        for i in range(10):
            #check it adds more on trials
            self.test.create_trial()
            self.test.upload([0,1,1,0],0.1,[1,2,3])
            self.test.upload([0,1,1,0],0.1,[1,2,3])
        ids=[]
        for exp in self.test.dataset.findall("Experiment"):
            data=exp.get("ID")
            ids.append(data)
        assert len(ids)==2,"Incorrect ID size "+str(ids)
    def test3(self):
        #check if you can come back and load
        for i in range(10):
            #check it adds more on trials
            self.test.create_trial()
            self.test.upload([0,1,1,0],0.1,[1,2,3])
            self.test.upload([0,1,1,0],0.1,[1,2,3])
        self.test.create_experiment(2,"eee",23,200)
        for i in range(10):
            #check it adds more on trials
            self.test.create_trial()
            self.test.upload([0,1,1,0],0.1,[1,2,3])
            self.test.upload([0,1,1,0],0.1,[1,2,3])
        self.test.save("temp")
        self.tearDon()
        self.setup()
        self.test.load("temp")
        self.test.create_experiment(3,"eee",23,200)
        for i in range(10):
            #check it adds more on trials
            self.test.create_trial()
            self.test.upload([0,1,1,0],0.1,[1,2,3])
            self.test.upload([0,1,1,0],0.1,[1,2,3])
        ids=[]
        for exp in self.test.dataset.findall("Experiment"):
            data=exp.get("ID")
            ids.append(data)
        assert len(ids)==3,"Incorrect ID size "+str(ids)
        

t=Test()