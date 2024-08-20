from enum import Enum

from src.dataConfigurations import DataConfiguration
from src.topologies import  Topology

class ConsoleStages(Enum):
    DC_DataDecision = 0
    DC_LoadDataSelection = 1
    DC_DataSelection = 2
    DC_DataTypeSelection = 3
    DC_DataProcessing = 4
    DC_Saving = 5

    TC_TopologyDecision = 10
    TC_LoadTopologySelection = 11
    TC_TopologyTypeSelection = 12
    TC_TopologyEpoch = 13
    TC_Training = 14
    TC_SaveTopology = 15

    Testing_Accuracy = 20
    Testing_ShowGraph = 21
    Testing_SaveGraph = 22

class Console:
    bitGroupPath = "./data/groups"
    processedDataPath = "./data/processed"
    topologyPath = "./data/models"
    figurePath = "./data/figures"
    bitGroups = [256,512,1024,2048]

    def check_directories():
        from os import makedirs
        from os.path import exists
        directories = [Console.bitGroupPath, 
                       Console.processedDataPath, 
                       Console.topologyPath, 
                       Console.figurePath]
        for dir in directories:
            if(not exists(dir)):
                makedirs(dir)
    def clear():
        from os import system, name as os_name
        system('cls' if os_name == 'nt' else 'clear')

    def __init__(self):
        Console.check_directories()
        self.stage = ConsoleStages.DC_DataDecision
        self.dataConf : DataConfiguration = None
        self.topologyConf : Topology = None
        self.bitLength = None
        self.df = None
        self.isAutomated = False


    def setDataConf(self, dataset : str):
        from numpy import load
        modelName, bitGroup = dataset.split("_")[:2]
        self.dataConf = DataConfiguration(modelName, int(bitGroup))
        inputs = load(f"{Console.processedDataPath}/{modelName}_{bitGroup}_inputs.npy")
        outputs = load(f"{Console.processedDataPath}/{modelName}_{bitGroup}_outputs.npy")
        self.dataConf.setPostData(inputs,outputs)
        

    def start(self):
        from src.helper import Helper
        args = Helper.processArgs()
        if(args["dataConfig"] != None):
            self.isAutomated = True
            self.currentTopology = 0
            self.setDataConf(args["dataConfig"])
            self.stage = ConsoleStages.TC_TopologyTypeSelection
        from os import listdir
        inp = None
        while True:
            try:
                Console.clear()
                if(inp == "q"):
                    from sys import exit
                    exit()

                if(self.stage == ConsoleStages.DC_DataDecision):
                    print("Select the data preparation option")
                    print("1- Create new dataset")
                    print("2- Load processed dataset")
                    inp = input(":")
                    if(inp == "1"):
                        self.stage = ConsoleStages.DC_DataSelection
                    if(inp == "2"):
                        self.stage = ConsoleStages.DC_LoadDataSelection
                
                elif(self.stage == ConsoleStages.DC_LoadDataSelection):
                    data_list = listdir(Console.processedDataPath)
                    if(len(data_list) == 0):
                        print("No data found! Type ENTER to create!")
                        input()
                        self.stage = ConsoleStages.DC_DataSelection
                        continue

                    data_set = list(set(["_".join(i.split("_")[:2]) for i in data_list]))
                    for i,v in enumerate(data_set):
                        print(f"{i+1}-{v}")
                    
                    try:
                        inp = input(":")
                        self.setDataConf(data_set[int(inp)-1])
                        self.stage = ConsoleStages.TC_TopologyDecision
                    except:
                        break

                elif(self.stage == ConsoleStages.DC_DataSelection):
                    from pandas import read_csv
                    data_list = listdir(Console.bitGroupPath)
                    for i,v in enumerate(data_list):
                        print(f"{i + 1} - {v}")
                    
                    try:
                        inp = input(":")
                        self.df = read_csv(f"{Console.bitGroupPath}/{data_list[int(inp)-1]}", 
                                        names=["p","q","n","phi","e","d"])
                        self.bitLength = int(data_list[int(inp)-1].split(".")[0].split("_")[1])
                        self.stage = ConsoleStages.DC_DataTypeSelection
                    except:
                        continue

                elif(self.stage == ConsoleStages.DC_DataTypeSelection):
                    models = [e for e in DataConfiguration.dataTypes]
                
                    try:
                        print("Select Data Processing Type")
                        for i,v in enumerate(models):
                            print(f"{i+1}-{v}")
                        inp = input(":")
                        selectedModelType = models[int(inp)-1]
                        print(f"{selectedModelType} is selected!")
                        self.dataConf = DataConfiguration(selectedModelType,
                                                            self.bitLength)
                        self.stage = ConsoleStages.DC_DataProcessing
                    except:
                        continue
                
                elif(self.stage == ConsoleStages.DC_DataProcessing):
                    # TODO : Input Output generations dynamicaly to model requirements!
                    print("inputColumns",self.dataConf.model.inputColumns)
                    print("outputColumns",self.dataConf.model.outputColumns)
                    inputs = self.df[self.dataConf.model.inputColumns].to_numpy()
                    outputs = self.df[self.dataConf.model.outputColumns].to_numpy()
                    self.dataConf.setPreData(inputs,outputs)
                    self.dataConf.process()
                    self.stage = ConsoleStages.DC_Saving

                elif(self.stage == ConsoleStages.DC_Saving):
                    print("Input  shape",self.dataConf.model.inputs.shape)
                    print("Output shape",self.dataConf.model.outputs.shape)
                    print("Save processed data file (y/n)(default:y)")
                    inp = input(":")
                    if(inp != "n" and inp != "N"):
                        self.dataConf.save()
                    self.stage = ConsoleStages.TC_TopologyDecision
                
                elif(self.stage == ConsoleStages.TC_TopologyDecision):
                    print("Model Configuration", self.dataConf.model.modelName, "is ready")
                    print("1- Create new model")
                    print("2- Load keras file")
                    inp = input(":")
                    if(inp == "1"):
                        self.stage = ConsoleStages.TC_TopologyTypeSelection
                    if(inp == "2"):
                        self.stage = ConsoleStages.TC_LoadTopologySelection

                elif(self.stage == ConsoleStages.TC_LoadTopologySelection):
                    model_list = listdir(Console.topologyPath)
                    
                    #try:
                    print("Select a model to load!")
                    if(len(model_list) == 0):
                        print("No data found! Type ENTER to create!")
                        input()
                        self.stage = ConsoleStages.TC_TopologyTypeSelection
                        continue
                    for i,v in enumerate(model_list):
                        print(f"{i+1}-{v}")
                    inp = input(":")
                    split = model_list[int(inp) - 1].split(".")[0].split("_")
                    selectedTopologyName = split[0]
                    self.topologyConf = Topology(selectedTopologyName,self.dataConf)
                    self.topologyConf.setEpoch(int(split[-1][1:]))
                    path = f"{Console.topologyPath}/{model_list[int(inp) - 1]}"
                    print(f"Loading {path}")
                    self.topologyConf.load_model(path)
                    
                    self.stage = ConsoleStages.Testing_Accuracy

                    # except:
                    #    continue


                elif(self.stage == ConsoleStages.TC_TopologyTypeSelection):
                    if(self.isAutomated):
                        selectedTopologyName  = Topology.topologies[self.currentTopology]
                        print(f"{selectedTopologyName} is selected!")
                        self.topologyConf = Topology(selectedTopologyName,self.dataConf)
                    else:
                        print("Select Model Type")
                        for i,v in enumerate(Topology.topologies):
                            print(f"{i+1}-{v}")
                        inp = input(":")
                        selectedTopologyName = Topology.topologies[int(inp)-1]
                        print(f"{selectedTopologyName} is selected!")
                        self.topologyConf = Topology(selectedTopologyName,self.dataConf)
                    self.stage = ConsoleStages.TC_TopologyEpoch

                elif(self.stage == ConsoleStages.TC_TopologyEpoch):
                    if(self.isAutomated):
                        self.topologyConf.setEpoch(int(args["epoch"]))
                        self.stage = ConsoleStages.TC_Training
                    else:
                        try:
                            inp = input("Epoch:")
                            self.topologyConf.setEpoch(int(inp))
                            self.stage = ConsoleStages.TC_Training
                        except:
                            print("Wrong Epoch!")
                        
                elif(self.stage == ConsoleStages.TC_Training):
                    self.topologyConf.train()
                    self.stage = ConsoleStages.TC_SaveTopology

                elif(self.stage == ConsoleStages.TC_SaveTopology):
                    if(self.isAutomated):
                        self.topologyConf.save()
                    else:
                        print("Save trained model file (y/n)(default:y)")
                        inp = input(":")
                        if(inp != "n" and inp != "N"):
                            self.topologyConf.save()
                    self.stage = ConsoleStages.Testing_Accuracy


                elif(self.stage == ConsoleStages.Testing_Accuracy):
                    self.topologyConf.test()
                    self.stage = ConsoleStages.Testing_SaveGraph
                    
                    #print("Show graph? (y/n)")
                    #inp = input(":")
                    #if(inp != "n" and inp != "N"):
                    #    self.stage = ConsoleStages.Testing_ShowGraph
                    #else:

                # elif(self.stage == ConsoleStages.Testing_ShowGraph):
                #     self.topologyConf.graph()
                #     self.stage = ConsoleStages.Testing_SaveGraph

                elif(self.stage == ConsoleStages.Testing_SaveGraph):
                    if(self.isAutomated):
                        print("Saving Faulty Bit Position Graph!")
                        self.topologyConf.graph()
                        self.topologyConf.saveGraph(Console.figurePath)
                        self.currentTopology += 1
                        self.stage = ConsoleStages.TC_TopologyTypeSelection
                    else:
                        print("Create and Save Faulty Bit Position Graph? (y/n)(default:y)")
                        inp = input(":")
                        if(inp != "n" and inp != "N"):
                            self.topologyConf.graph()
                            self.topologyConf.saveGraph(Console.figurePath)
                        break
            except:
                if(self.isAutomated):
                    self.currentTopology += 1
                    self.stage = ConsoleStages.TC_TopologyTypeSelection
                pass