
from enum import Enum

from src.modelConfigurations import ModelConfiguration

class Topologies(Enum):
    MultiDense = "MultiDense"
    VariousLayers = "VariousLayers"
    # Add new network topology type here!

class Topology:
    def __init__(self, type : Topologies, conf : ModelConfiguration):
        self.conf = conf
        self.type = type
        self.topology = None
        self.fig = None
        self.errors = None
        self.epoch = None
        if(type == Topologies.MultiDense):
            from src.topologies.multidense import MultiDense
            self.topology = MultiDense()
        elif(type == Topologies.VariousLayers):
            from topologies.variouslayers import VariousLayers
            self.topology = VariousLayers()
        
        # Add new network topology type condition here!
        assert self.topology != None, "Topology is null!"
        

    def load_model(self,path):
        from tensorflow.keras.models import load_model # type: ignore
        self.topology.model = load_model(path)

    def setEpoch(self, epoch):
        self.epoch = epoch

    def train(self):
        self.topology.create(self.conf.model.sizes[0][1],
                             self.conf.model.sizes[1][1])
        inputs = self.conf.model.inputs
        outputs = self.conf.model.outputs
        self.topology.model.fit(inputs[:50000], 
                                outputs[:50000], 
                                epochs=self.epoch, 
                                verbose=2,
                                validation_data=(inputs[50000:], 
                                                 outputs[50000:]))
    
    def save(self):
        from src.controller import Console
        self.topology.model.save(f'{Console.topologyPath}/{self.topology.topologyName}_{self.conf.model.modelName}_b{self.conf.bit_group}_e{self.epoch}.keras')

    def test(self):
        from numpy import isnan
        inputs = self.conf.model.inputs[50000:]
        targets = self.conf.model.outputs[50000:]

        print("Creating Predictions")
        predictions = self.topology.model.predict(inputs)
        print("Please wait for calculating the accuracy!")
        total = 0
        correct = 0
        self.errors = {}
        for i in range(len(predictions)):
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
                
        print(f"{correct}/{total}")
        print(f"Acc: {correct/total}")

        
    def graph(self):
        from numpy import array
        import matplotlib.pyplot as plt
        xs = array(sorted(list(self.errors.keys())))
        ys = array([self.errors[i] for i in xs])

        self.fig, ax = plt.subplots()
        ax.plot(xs,ys)
        max_y = 100 if len(self.errors) == 0 else max(self.errors.values()) + 1000
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
