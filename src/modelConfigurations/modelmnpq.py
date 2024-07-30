class ModelMNPQ:
    def __init__(self):
        
        self.inputColumns=["n"]
        self.outputColumns=["p","q"]
        self.modelName = "ModelMNPQ"
        ### Model n-pq
        """
        - Model input is n in binary form as a matrix.
        - Model output is the combination of p and q primes in binary form in order as a matrix.
        """
    def getSizes(self, size, bit_group):
        from src.helpers import Helper
        msizes = Helper.matrixSizes(bit_group*2)
        self.sizes = ((size,msizes[0],msizes[1],1), (size,msizes[0],msizes[1],1))
        
    def process(self, inputs, outputs, bit_group):
        from numpy import empty, array
        from src.helpers import Helper
        
        assert len(inputs) == len(outputs), "Input-Output data sizes do not match!"
        assert type(outputs[0]) == type(list()), "In Modelnpq - each row of output should be an array!"
        assert len(outputs[0]) == 2, "In Modelnpq - output array size should be 2(both primes)!"
        
        size = len(inputs)
        msizes = Helper.matrixSizes(bit_group*2)
        #Empty data
        self.inputs = empty(shape=self.sizes[0])
        self.outputs = empty(shape=self.sizes[1])

        for i in range(size):
            # Input Data
            n_bin = str(bin(int(inputs[i])))[2:]
            n_bin = n_bin.zfill(self.sizes[0][1])

            # Output Data
            q_bin = str(bin(int(outputs[i][0])))[2:]
            q_bin = q_bin.zfill(self.sizes[1][1]/2)
            p_bin = str(bin(int(outputs[i][1])))[2:]
            p_bin = p_bin.zfill(self.sizes[1][1]/2)

            # Assigning
            self.inputs[i] = [int(i) for i in list(n_bin)]
            self.outputs[i] = [int(i) for i in list(p_bin + q_bin)]
            
            
        self.inputs = array([array([j[i:i+msizes[1]] for i in range(0,msizes[0])]) for j in inputs])
        self.outputs = array([array([j[i:i+msizes[1]] for i in range(0,msizes[0])]) for j in outputs])
        
            
