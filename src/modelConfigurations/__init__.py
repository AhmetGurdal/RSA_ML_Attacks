from enum import Enum
class ModelConfigurations(Enum):
    ModelNPQ = "ModelNPQ"
    ModelNP = "ModelNP"
    ModelNQ = "ModelNQ"
    ModelSP = "ModelSP"
    ModelSQ = "ModelSQ"
    ModelSEP = "ModelSEP"
    ModelSOP = "ModelSOP"
    ModelSOA = "ModelSOA"
    ModelNPHI = "ModelNPHI"
    ModelMNPQ = "ModelMNPQ"
    ModelNP2 = "ModelNP2"
    # Add new data configuration type here!

class ModelConfiguration:
    def __init__(self, model, bit_group):
        self.model = None
        self.bit_group = bit_group
        if(model == ModelConfigurations.ModelNPQ):
            from src.modelConfigurations.modelnpq import ModelNPQ
            self.model = ModelNPQ()
        elif(model == ModelConfigurations.ModelNP):
            from src.modelConfigurations.modelnp import ModelNP
            self.model = ModelNP()
        elif(model == ModelConfigurations.ModelNQ):
            from src.modelConfigurations.modelnq import ModelNQ
            self.model = ModelNQ()
        elif(model == ModelConfigurations.ModelSP):
            from src.modelConfigurations.modelsp import ModelSP
            self.model = ModelSP()
        elif(model == ModelConfigurations.ModelSQ):
            from src.modelConfigurations.modelsq import ModelSQ
            self.model = ModelSQ()
        elif(model == ModelConfigurations.ModelSEP):
            from src.modelConfigurations.modelsep import ModelSEP
            self.model = ModelSEP()
        elif(model == ModelConfigurations.ModelSOP):
            from src.modelConfigurations.modelsop import ModelSOP
            self.model = ModelSOP()
        elif(model == ModelConfigurations.ModelSOA):
            from src.modelConfigurations.modelsoa import ModelSOA
            self.model = ModelSOA()
        elif(model == ModelConfigurations.ModelNPHI):
            from src.modelConfigurations.modelnphi import ModelNPHI
            self.model = ModelNPHI()
        elif(model == ModelConfigurations.ModelMNPQ):
            from src.modelConfigurations.modelmnpq import ModelMNPQ
            self.model = ModelMNPQ()
        elif(model == ModelConfigurations.ModelNP2):
            from src.modelConfigurations.modelnp2 import ModelNP2
            self.model = ModelNP2()
        else:
            print("No Model Found!")
        # Add new data configuration type condition before the else condition!

        assert self.model != None, "Model is null!"

    def setPreData(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.model.setSizes(len(inputs), self.bit_group)

    def setPostData(self, inputs, outputs):
        self.model.inputs = inputs
        self.model.outputs = outputs
        self.model.setSizes(len(inputs), self.bit_group)
        

    def process(self):
        print("Please wait while processing the data!")
        self.model.process(self.inputs, self.outputs, self.bit_group)

    def save(self):
        from numpy import save
        from src.controller import Console
        print(self.model.inputs.shape)
        print(self.model.outputs.shape)
        save(f"{Console.processedDataPath}/{self.model.modelName}_{self.bit_group}_inputs.npy",
             self.model.inputs)
        save(f"{Console.processedDataPath}/{self.model.modelName}_{self.bit_group}_outputs.npy",
             self.model.outputs)
        
