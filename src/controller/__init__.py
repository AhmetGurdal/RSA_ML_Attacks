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
    resultFile = "./data/results.txt"
    bitGroups = [256,512,1024,2048]

    def check_directories():
        from os import makedirs
        from os.path import exists
        directories = [Console.bitGroupPath, 
                       Console.processedDataPath,
                       Console.topologyPath, 
                       Console.figurePath]
        for directory in directories:
            if(not exists(directory)):
                makedirs(directory)
        for bitGroup in Console.bitGroups:
            directory = f"{Console.processedDataPath}/{bitGroup}"
            if(not exists(directory)):
                makedirs(directory)
    def clear():
        from os import system, name as os_name
        system('cls' if os_name == 'nt' else 'clear')

    def filter_models(self, model_list : list):
        new_list = []
        for model in model_list:
            if(self.dataConf.bit_group in model and 
               self.dataConf.model.modelName in model):
                new_list.append(model)
        return new_list


    def __init__(self):
        from src.helper.ArgHandler import ArgHandler
        self.arghandler = ArgHandler()
        Console.check_directories()
        self.stage = ConsoleStages.DC_DataDecision
        self.dataConf : DataConfiguration = None
        self.topologyConf : Topology = None
        self.bitLength = None
        self.df = None
        self.isAutomated = False


    def setDataConf(self, modelName : str, bitGroup : str):
        from numpy import load
        self.dataConf = DataConfiguration(modelName, int(bitGroup))
        inputs = load(f"{Console.processedDataPath}/{bitGroup}/{modelName}_inputs.npy")
        outputs = load(f"{Console.processedDataPath}/{bitGroup}/{modelName}_outputs.npy")
        self.dataConf.setPostData(inputs,outputs)
        

    def start(self):
        if(vars(self.arghandler.args).get("dc") != None):
            self.isAutomated = True
            self.currentTopology = 0
            self.setDataConf(vars(self.arghandler.args).get("dc"), self.arghandler.args.get("bg"))
            self.stage = ConsoleStages.TC_TopologyTypeSelection
        from os import listdir
        inp = None
        while True:
            Console.clear()
            if(inp == "q"):
                break
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
                bit_group = None
                while True:
                    print("Select bit group")
                    for i,b in enumerate(self.bitGroups):
                        print(f"{i+1}- {b}")
                    bit_group = input(":")
                    if(int(bit_group) < 1 or int(bit_group) > len(self.bitGroups)):
                        print("Wrong selection, please try again.") 
                    else:
                        bit_group = str(self.bitGroups[int(bit_group)-1])
                        break
                data_list = listdir(f"{Console.processedDataPath}/{bit_group}")
                if(len(data_list) == 0):
                    print("No data found! Type ENTER to create!")
                    input()
                    self.stage = ConsoleStages.DC_DataSelection
                    continue

                data_set = list(set([i.split("_")[0] for i in data_list]))
                for i,v in enumerate(data_set):
                    print(f"{i+1}-{v}")
                
                try:
                    inp = input(":")
                    self.setDataConf(data_set[int(inp)-1], bit_group)
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
                pre_inputs = self.df[self.dataConf.model.inputColumns].to_numpy()
                pre_outputs = self.df[self.dataConf.model.outputColumns].to_numpy()
                self.dataConf.setPreData(pre_inputs,pre_outputs)
                
                self.dataConf.process()
               
                if(self.isAutomated):
                    self.stage = ConsoleStages.TC_TopologyTypeSelection

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
                model_list = self.filter_models(model_list)
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
                    if(self.currentTopology > len(Topology.topologies)):
                        exit()
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
                    self.topologyConf.setEpoch(int(vars(self.arghandler.args).get("e")))
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
                self.topologyConf.test(self.resultFile)
                self.stage = ConsoleStages.Testing_SaveGraph

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
        