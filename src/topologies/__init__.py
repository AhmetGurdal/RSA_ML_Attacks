
from enum import Enum

from src.modelConfigurations import ModelConfiguration

class Topologies(Enum):
    MultiDense = "MultiDense"
    Test = "Test"
    # Add new network topology type here!

class Topology:
    def __init__(self, type : Topologies, conf : ModelConfiguration):
        self.conf = conf
        self.type = type
        self.topology = None
        self.fig = None
        self.errors = None

        if(type == Topologies.MultiDense):
            from src.topologies.multidense import MultiDense
            self.topology = MultiDense()
        elif(type == Topologies.Test):
            from src.topologies.test import Test
            self.topology = Test()
        # Add new network topology type condition here!

    def load_model(self,path):
        from tensorflow.keras.models import load_model
        self.topology.model = load_model(path)

    def train(self):
        self.topology.create(self.conf.model.sizes[0][1],
                             self.conf.model.sizes[1][1])
        inputs = self.conf.model.inputs
        outputs = self.conf.model.outputs
        self.topology.model.fit(inputs[:50000], 
                                outputs[:50000], 
                                epochs=100, 
                                validation_data=(inputs[50000:], 
                                                 outputs[50000:]))
    
    def save(self):
        from src.controller import Console
        self.topology.model.save(f'{Console.topologyPath}/{self.topology.topologyName}_{self.conf.model.modelName}_{self.conf.bit_group}.keras')

    def test(self):
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
                if(round(predictions[i][j]) == target[j]):
                    correct += 1
                else:
                    if(j in self.errors):
                        self.errors[j] += 1
                    else:
                        self.errors[j] = 1
                total += 1
        print(f"{correct}/{total}")
        print(f"Acc: {correct/total}")

        
    def graph(self):
        from numpy import array
        import matplotlib.pyplot as plt
        xs = array(sorted(list(self.errors.keys())))
        ys = array([self.errors[i] for i in xs])

        self.fig, ax = plt.subplots()
        ax.plot(xs,ys)
        ax.set_ylim([0, max(self.errors.values()) + 1000])
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
        dump(self.fig,open(f"{path}/{self.topology.topologyName}_{self.conf.model.modelName}_{self.conf.bit_group}.pickle",'wb'))
        self.fig.savefig(f"{path}/{self.topology.topologyName}_{self.conf.model.modelName}_{self.conf.bit_group}.png")
