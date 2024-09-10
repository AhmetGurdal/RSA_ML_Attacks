from src.classes.dataModel import DataModel

class ModelSOA(DataModel):
    def __init__(self):
        self.inputColumns=["n"]
        self.outputColumns=["p"]
        self.modelName = "ModelSOA"
        ### Model so-a
        """
        - Model input is closest odd to the square root of n.
        - Model output is the binary of the distance between closest odd to the square and prime p.
        """
    def setSizes(self, size, bit_group):
        self.sizes = ((size,bit_group), (size,bit_group))

    def process(self, inputs, outputs, bit_group):
        from decimal import Decimal, localcontext
        from numpy import empty
        from src.helper import Helper
        assert len(inputs) == len(outputs), "Input-Output data sizes do not match!"

        size = len(inputs)
        self.sizes = ((size,bit_group), (size,bit_group))
        
        #Empty data
        self.inputs = empty(shape=self.sizes[0])
        self.outputs = empty(shape=self.sizes[1])
        with localcontext() as ctx:
            ctx.prec = 300
            for i in range(size):

                N = Decimal(int(inputs[i]))
                S = N.sqrt()
                p = Decimal(int(outputs[i]))
                RS = Helper.roundodd(S,1)
                a = Decimal(RS) - p

                # Input Data
                RS_bin =  str(bin(int(RS)))[2:]
                RS_bin = RS_bin.zfill(self.sizes[0][1])
                
                # Output Data
                a_bin = str(bin(int(a)))[2:]
                a_bin = a_bin.zfill(self.sizes[1][1])

                # Assigning
                self.inputs[i] = [int(i) for i in list(RS_bin)]
                self.outputs[i] = [int(i) for i in list(a_bin)]