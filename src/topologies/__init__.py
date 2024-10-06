from src.dataConfigurations import DataConfiguration
from importlib import import_module

class Topology:
    train_test_rate = 0.9
    
    # @staticmethod
    def getTopologies():
        from os import listdir
        from os.path import dirname
        from inspect import getmembers, isclass
        
        class_names = []
        test_folder = dirname(__file__)
        for file_name in listdir(test_folder):
            if file_name.endswith('.py') and file_name != '__init__.py' and not file_name.startswith("."):
                module_name = file_name[:-3]
                module = import_module(f'src.topologies.{module_name}')
                for name, obj in getmembers(module, isclass):
                    if obj.__module__ == module.__name__:
                        class_names.append(name)
        return class_names
    
    topologies = getTopologies()

    def __init__(self, type : str, conf : DataConfiguration):
        self.conf = conf
        self.type = type
        self.topology = None
        self.fig = None
        self.errors = None
        self.epoch = None
        self.accuracy = None
        self.split_index = int(len(self.conf.model.inputs) * Topology.train_test_rate)
        module = import_module(f'src.topologies.{type}')
        cls = getattr(module, type)
        self.topology = cls()
        # Add new network topology type condition here!
        assert self.topology != None, "Topology is null!"
        

    def load_model(self,path):
        from tensorflow.keras.models import load_model # type: ignore
        self.topology.model = load_model(path)

    def setEpoch(self, epoch):
        self.epoch = epoch

    def train(self):
        
        self.topology.create(self.conf.model.sizes)
        inputs = self.conf.model.inputs
        outputs = self.conf.model.outputs
        self.topology.model.fit(inputs[:self.split_index], 
                                outputs[:self.split_index], 
                                epochs=self.epoch, 
                                verbose=2,
                                validation_data=(inputs[self.split_index:], 
                                                 outputs[self.split_index:]))
    
    def save(self):
        from src.controller import Console
        self.topology.model.save(f'{Console.topologyPath}/{self.topology.topologyName}_{self.conf.model.modelName}_b{self.conf.bit_group}_e{self.epoch}.keras')

    def test(self, resultFile):
        from numpy import isnan, ndarray
        
        inputs = self.conf.model.inputs[self.split_index:]
        targets = self.conf.model.outputs[self.split_index:]

        print("Creating Predictions")
        predictions = self.topology.model.predict(inputs)

        print("Please wait for calculating the accuracy!")

        self.errors = {}
        total = 0
        correct = 0
        if(type(predictions[0][0]) == ndarray):
            correct,total = self.test2D(targets, predictions)
        else:
            for i in range(len(predictions)):
                #print("Target", targets[i])
                #print("Prediction", predictions[i])
                target = targets[i]
                for j in range(len(predictions[i])):
                    total += 1
                    if(isnan(predictions[i][j])):
                        continue
                    elif(round(predictions[i][j]) == target[j]):
                        correct += 1
                    else:
                        if(j in self.errors):
                            self.errors[j] += 1
                        else:
                            self.errors[j] = 1
        self.accuracy = correct/total
        with open(resultFile, "a") as f:
            f.write(f"{self.topology.topologyName} - {self.conf.model.modelName} - Acc : {self.accuracy}\n")
        print(f"{correct}/{total}")
        print(f"Acc: {self.accuracy}")


    def test2D(self, targets, predictions):
        from numpy import isnan
        total = 0
        correct = 0
        for i in range(len(predictions)):
            target = targets[i]
            pred = predictions[i]
            for x in range(len(pred)):
                for y in range(len(pred[x])):
                    total += 1
                    if(isnan(pred[x][y][0])):
                        continue
                    elif(round(pred[x][y][0]) == target[x][y][0]):
                        correct += 1
                    else:
                        ind = (x*(len(pred[x])) + y)
                        if(ind in self.errors):
                            self.errors[ind] += 1
                        else:
                            self.errors[ind] = 1
        return correct,total
        
    def graph(self):
        from numpy import array
        import matplotlib.pyplot as plt
        xs = array(sorted(list(self.errors.keys())))
        ys = array([self.errors[i] for i in xs])

        self.fig, ax = plt.subplots()
        ax.plot(xs,ys)
        max_y = len(self.conf.model.outputs[self.split_index:])
        ax.text(len(xs)//2 - len(xs)//6, max_y + 30, f'Acc : {round(self.accuracy, 4)}', fontsize = 14)
        ax.set_ylim([0, max_y])
        # def annot_max(x,y,i, ax=None):
        #     text= "x={}, y={}".format(x+1, y)
        #     if not ax:
        #         ax=plt.gca()
        #     bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        #     arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
        #     kw = dict(xycoords='data',textcoords="axes fraction",
        #             arrowprops=arrowprops, bbox=bbox_props, ha="center", va="top")
        #     ax.annotate(text, xy=(x, y), xytext=(0.3,0.9 - (i * 0.1)), **kw)
        #plt.show()

    def saveGraph(self, path):
        from pickle import dump
        dump(self.fig,open(f"{path}/{self.topology.topologyName}_{self.conf.model.modelName}_b{self.conf.bit_group}_e{self.epoch}.pickle",'wb'))
        self.fig.savefig(f"{path}/{self.topology.topologyName}_{self.conf.model.modelName}_b{self.conf.bit_group}_e{self.epoch}.png")
