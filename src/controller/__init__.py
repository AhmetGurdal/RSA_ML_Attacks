from enum import Enum

from src.modelConfigurations import ModelConfiguration, ModelConfigurations
from src.topologies import Topologies, Topology

class ConsoleStages(Enum):
    MC_DataDecision = 0
    MC_LoadDataSelection = 1
    MC_DataSelection = 2
    MC_ModelTypeSelection = 3
    MC_DataProcessing = 4
    MC_Saving = 5

    TC_TopologyDecision = 10
    TC_LoadTopologySelection = 11
    TC_TopologyTypeSelection = 12
    TC_Training = 13
    TC_SaveTopology = 14

    Testing_Accuracy = 20
    Testing_ShowGraph = 21
    Testing_SaveGraph = 22

class Console:
    bitGroupPath = "./data/groups"
    processedDataPath = "./data/processed"
    topologyPath = "./data/models"
    figurePath = "./data/figures"
    bitGroups = [256,512,1024,2048]

    def clear():
        from os import system, name as os_name
        system('cls' if os_name == 'nt' else 'clear')

    def __init__(self):
        self.stage = ConsoleStages.MC_DataDecision
        self.modelConf : ModelConfiguration = None
        self.topologyConf : Topology = None
        self.df = None

    def start(self):
        
        from os import listdir
        inp = None
        while True:
            Console.clear()
            if(self.stage == ConsoleStages.MC_DataDecision):
                print("Select the data preparation option")
                print("1- Create new dataset")
                print("2- Load processed dataset")
                inp = input(":")
                if(inp == "1"):
                    self.stage = ConsoleStages.MC_DataSelection
                if(inp == "2"):
                    self.stage = ConsoleStages.MC_LoadDataSelection
            
            elif(self.stage == ConsoleStages.MC_LoadDataSelection):
                from numpy import load
                data_list = listdir(Console.processedDataPath)
                if(len(data_list) == 0):
                    print("No data found! Type ENTER to create!")
                    input()
                    self.stage = ConsoleStages.MC_DataSelection
                    continue

                data_set = set(["_".join(i.split("_")[:2]) for i in data_list])
                for i,v in enumerate(data_set):
                    print(f"{i+1}-{v}")
                while True:
                    try:
                        inp = input(":")
                        modelName, bitGroup = data_list[int(inp)-1].split(".")[0].split("_")[:2]
                        
                        self.modelConf = ModelConfiguration(ModelConfigurations[modelName], int(bitGroup))
                        inputs = load(f"{Console.processedDataPath}/{modelName}_{bitGroup}_inputs.npy")
                        outputs = load(f"{Console.processedDataPath}/{modelName}_{bitGroup}_outputs.npy")
                        self.modelConf.setPostData(inputs,outputs)
                        self.stage = ConsoleStages.TC_TopologyDecision
                        break
                    except:
                        continue

            elif(self.stage == ConsoleStages.MC_DataSelection):
                from pandas import read_csv
                data_list = listdir(Console.bitGroupPath)
                for i,v in enumerate(data_list):
                    print(f"{i + 1} - {v}")
                while True:
                    try:
                        inp = input(":")
                        self.df = read_csv(f"{Console.bitGroupPath}/{data_list[int(inp)-1]}", 
                                        names=["p","q","n","phi","e","d"])
                        self.stage = ConsoleStages.MC_ModelTypeSelection
                        break
                    except:
                        continue

            elif(self.stage == ConsoleStages.MC_ModelTypeSelection):
                models = [e.value for e in ModelConfigurations]
                while True:
                    try:
                        print("Select Model Type")
                        for i,v in enumerate(models):
                            print(f"{i+1}-{v}")
                        inp = input(":")
                        selectedModelType = models[int(inp)-1]
                        print(f"{selectedModelType} is selected!")
                        print("------------------------------------\n")
                        print("Select Bit Length")
                        for i, bit in enumerate(Console.bitGroups):
                            print(f"{i+1}-{bit}")
                        inp = input(":")
                        selectedBitLength = Console.bitGroups[int(inp)-1]
                        self.modelConf = ModelConfiguration(ModelConfigurations[selectedModelType],
                                                            selectedBitLength)
                        self.stage = ConsoleStages.MC_DataProcessing
                        break
                    except:
                        continue
            
            elif(self.stage == ConsoleStages.MC_DataProcessing):
                # TODO : Input Output generations dynamicly to model requirements!
                print("inputColumns",self.modelConf.model.inputColumns)
                print("outputColumns",self.modelConf.model.outputColumns)
                inputs = self.df[self.modelConf.model.inputColumns].to_numpy()
                outputs = self.df[self.modelConf.model.outputColumns].to_numpy()
                self.modelConf.setPreData(inputs,outputs)
                self.modelConf.process()
                self.stage = ConsoleStages.MC_Saving

            elif(self.stage == ConsoleStages.MC_Saving):
                print("Input  shape",self.modelConf.model.inputs.shape)
                print("Output shape",self.modelConf.model.outputs.shape)
                print("Save processed data file (y/n)(default:y)")
                inp = input(":")
                if(inp != "n" and inp != "N"):
                    self.modelConf.save()
                self.stage = ConsoleStages.TC_TopologyDecision
            
            elif(self.stage == ConsoleStages.TC_TopologyDecision):
                print("1- Create new model")
                print("2- Load keras file")
                inp = input(":")
                if(inp == "1"):
                    self.stage = ConsoleStages.TC_TopologyTypeSelection
                if(inp == "2"):
                    self.stage = ConsoleStages.TC_LoadTopologySelection

            elif(self.stage == ConsoleStages.TC_LoadTopologySelection):
                model_list = listdir(Console.topologyPath)
                while True:
                    try:
                        print("Select a model to load!")
                        if(len(model_list) == 0):
                            print("No data found! Type ENTER to create!")
                            input()
                            self.stage = ConsoleStages.TC_TopologyTypeSelection
                            continue
                        for i,v in enumerate(model_list):
                            print(f"{i+1}-{v}")
                        inp = input(":")
                        selectedTopologyName = model_list[int(inp) - 1].split("_")[0]
                        self.topologyConf = Topology(Topologies[selectedTopologyName],self.modelConf)
                        path = f"{Console.topologyPath}/{model_list[int(inp) - 1]}"
                        print(f"Loading {Console.topologyPath}/{model_list[int(inp) - 1]}")
                        self.topologyConf.load_model(path)
                        self.stage = ConsoleStages.Testing_Accuracy
                        break
                    except:
                        continue


            elif(self.stage == ConsoleStages.TC_TopologyTypeSelection):
                topologies = [e.value for e in Topologies]
                while True:
                    try:
                        print("Select Model Type")
                        for i,v in enumerate(topologies):
                            print(f"{i+1}-{v}")
                        
                        inp = input(":")
                        selectedTopology = topologies[int(inp)-1]
                        print(f"{selectedTopology} is selected!")

                        self.topologyConf = Topology(int(inp)-1,self.modelConf)
                        self.stage = ConsoleStages.TC_Training
                        break
                    except:
                        continue

            elif(self.stage == ConsoleStages.TC_Training):
                self.topologyConf.train()
                self.stage = ConsoleStages.TC_SaveTopology

            elif(self.stage == ConsoleStages.TC_SaveTopology):
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

            elif(self.stage == ConsoleStages.Testing_ShowGraph):
                self.topologyConf.graph()
                self.stage = ConsoleStages.Testing_SaveGraph

            elif(self.stage == ConsoleStages.Testing_SaveGraph):
                print("Create and Save Faulty Bit Position Graph? (y/n)")
                inp = input(":")
                if(inp != "n" and inp != "N"):
                    self.topologyConf.graph()
                    self.topologyConf.saveGraph(Console.figurePath)
                break