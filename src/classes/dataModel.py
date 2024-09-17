class DataModel:

    def __init__(self):
        self.inputColumns = None
        self.outputColumns = None
        self.inputs = None
        self.modelName = None
        self.inputs = None
        self.outputs = None

    def setPostSizes(self, i_size, o_size):
        self.sizes = (i_size, o_size)

    def setSizes(self, size, bit_group):
        pass

    def process(self, inputs, outputs, bit_group):
        pass