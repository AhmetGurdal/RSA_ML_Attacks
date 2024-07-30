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

    Testing_ShowGraph = 20
    Testing_SaveGraph = 21

# import pandas as pd

# from src.modelConfigurations import ModelConfiguration, ModelConfigurations
# from src.topologies import Topology, Topologies

# df = pd.read_csv("./data/groups/rsa_256.csv",header=None)

# modelConf = ModelConfiguration(ModelConfigurations.ModelNP,
#                                256)
# modelConf.process(df[2].to_list(),
#                   df[0].to_list())
# modelConf.save()

# topology = Topology(Topologies.MultiDense,
#                     modelConf)

# topology.train()
# topology.save()

# topology.test()
class Console:
    bitGroupPath = "./data/groups"
    processedDataPath = "./data/processed"
    topologyPath = "./data/models"
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
                print("1- Process data")
                print("2- Load processed data")
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
                for i,v in enumerate(data_list):
                    print(f"{i+1}-{v}")
                inp = input(":")
                modelName, bitGroup = data_list[int(inp)-1].split(".")[0].split("_")
                
                self.modelConf = ModelConfiguration(ModelConfigurations[modelName], int(bitGroup))
                data = load(f"{Console.processedDataPath}/{modelName}_{bitGroup}.npy")
                self.modelConf.setData(data[0],data[1])
                self.stage = ConsoleStages.TC_TopologyDecision

            elif(self.stage == ConsoleStages.MC_DataSelection):
                from pandas import read_csv
                data_list = listdir(Console.bitGroupPath)
                for i,v in enumerate(data_list):
                    print(f"{i + 1} - {v}")
                inp = input(":")
                self.df = read_csv(f"{Console.bitGroupPath}/{data_list[int(inp)-1]}", 
                                   names=["p","q","n","phi","e","d"])
                self.stage = ConsoleStages.MC_ModelTypeSelection

            elif(self.stage == ConsoleStages.MC_ModelTypeSelection):
                models = [e.value for e in ModelConfigurations]
                print("Select Model Type")
                for i,v in enumerate(models):
                    print(f"{i+1}-{v}")
                
                inp = input(":")
                selectedModelType = models[int(inp)-1]
                print(f"{selectedModelType} is selected!")

                print("Select Bit Length")
                for i, bit in enumerate(Console.bitGroups):
                    print(f"{i+1}-{bit}")
                inp = input(":")
                selectedBitLength = Console.bitGroups[int(inp)-1]
                
                self.modelConf = ModelConfiguration(ModelConfigurations[selectedModelType],
                                                    selectedBitLength)
                self.stage = ConsoleStages.MC_DataProcessing
            
            elif(self.stage == ConsoleStages.MC_DataProcessing):
                # TODO : Input Output generations dynamicly to model requirements!
                inputs = self.df[self.modelConf.model.inputColumns].to_numpy()
                outputs = self.df[self.modelConf.model.outputColumns].to_numpy()
                self.modelConf.setData(inputs,outputs)
                self.modelConf.process()
                self.stage = ConsoleStages.MC_Saving

            elif(self.stage == ConsoleStages.MC_Saving):
                print("Saving file (y/n)")
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
                print(f"Loading{Console.topologyPath}/{model_list[int(inp) - 1]}")
                self.topologyConf.load_model(path)
                self.stage = ConsoleStages.Testing_ShowGraph

            elif(self.stage == ConsoleStages.TC_TopologyTypeSelection):
                topologies = [e.value for e in Topologies]
                print("Select Model Type")
                for i,v in enumerate(topologies):
                    print(f"{i+1}-{v}")
                
                inp = input(":")
                selectedTopology = topologies[int(inp)-1]
                print(f"{selectedTopology} is selected!")

                self.topologyConf = Topology(Topologies[selectedTopology],self.modelConf)
                self.stage = ConsoleStages.TC_Training
            
            elif(self.stage == ConsoleStages.TC_Training):
                self.topologyConf.train()
                self.stage = ConsoleStages.TC_SaveTopology

            elif(self.stage == ConsoleStages.TC_SaveTopology):
                print("Saving file (y/n)")
                inp = input(":")
                if(inp != "n" and inp != "N"):
                    self.topologyConf.save()
                self.stage = ConsoleStages.Testing_ShowGraph

            elif(self.stage == ConsoleStages.Testing_ShowGraph):
                self.topologyConf.test(self.topologyConf.topology.model, 
                                       [self.modelConf.inputs, 
                                        self.modelConf.outputs])
                print("Finished!")
                break

            elif(self.stage == ConsoleStages.Testing_SaveGraph):
                pass