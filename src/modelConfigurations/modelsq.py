class ModelSQ:
    def __init__(self):
        self.inputColumns=["n"]
        self.outputColumns=["q"]
        self.modelName = "ModelSQ"
        ### Model s-q
        """
        - Provide n,p -> get s,q
        - Model input is closest even to the square root of n
        - Model output is binary of prime q.
        """

    def setSizes(self, size, bit_group):
        self.sizes = ((size,bit_group), (size,bit_group))

    def process(self, inputs, outputs, bit_group):
        from decimal import Decimal, localcontext
        from numpy import empty
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

                # Input Data
                RS_bin =  str(bin(int(round(S))))[2:]
                RS_bin = RS_bin.zfill(self.sizes[0][1])
                
                # Output Data
                q_bin = str(bin(int(outputs[i])))[2:]
                q_bin = q_bin.zfill(self.sizes[1][1])

                # Assigning
                self.inputs[i] = [int(i) for i in list(RS_bin)]
                self.outputs[i] = [int(i) for i in list(q_bin)]