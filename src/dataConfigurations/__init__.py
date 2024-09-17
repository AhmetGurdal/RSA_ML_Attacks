from importlib import import_module
from src.classes.dataModel import DataModel

class DataConfiguration:

    @staticmethod
    def getDataProcessingTypes():
        from os import listdir
        from os.path import dirname
        from inspect import getmembers, isclass
        
        class_names = []
        test_folder = dirname(__file__)
        for file_name in listdir(test_folder):
            if file_name.endswith('.py') and file_name != '__init__.py' and not file_name.startswith("."):
                module_name = file_name[:-3]
                module = import_module(f'src.dataConfigurations.{module_name}')
                for name, obj in getmembers(module, isclass):
                    if obj.__module__ == module.__name__:
                        class_names.append(name)
        return class_names
    dataTypes = getDataProcessingTypes()

    def __init__(self, type : str, bit_group):
        self.model : DataModel = None
        self.bit_group = bit_group
        module = import_module(f'src.dataConfigurations.{type}')
        cls = getattr(module, type)
        self.model = cls()
        assert self.model != None, "Data Configuration is null!"

    def setPreData(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.model.setSizes(len(inputs), self.bit_group)

    def setPostData(self, inputs, outputs):
        self.model.inputs = inputs
        self.model.outputs = outputs
        self.model.setPostSizes(inputs.shape, outputs.shape)
        
    def process(self):
        print("Please wait while processing the data!")
        self.model.process(self.inputs, self.outputs, self.bit_group)

    def save(self):
        from numpy import save
        from src.controller import Console
        print(self.model.inputs.shape)
        print(self.model.outputs.shape)
        save(f"{Console.processedDataPath}/{self.bit_group}/{self.model.modelName}_inputs.npy",
             self.model.inputs)
        save(f"{Console.processedDataPath}/{self.bit_group}/{self.model.modelName}_outputs.npy",
             self.model.outputs)
        
