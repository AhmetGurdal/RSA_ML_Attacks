class ModelNPQ:
    def __init__(self):
        self.inputColumns=["n"]
        self.outputColumns=["p","q"]
        self.modelName = "ModelNPQ"
        ### Model n-pq
        """
        - Model input is n in binary form.
        - Model output is the combination of p and q primes in binary form in order.
        """
    
    def setSizes(self, size, bit_group):
        self.sizes = ((size,bit_group*2), (size,bit_group*2))

    def process(self, inputs, outputs, bit_group):
        from numpy import empty,ndarray
        assert len(inputs) == len(outputs), "Input-Output data sizes do not match!"
        assert type(outputs[0]) == ndarray, "In Modelnpq - each row of output should be an array!"
        assert len(outputs[0]) == 2, "In Modelnpq - output array size should be 2(both primes)!"

        size = len(inputs)
        self.sizes = ((size,bit_group*2), (size,bit_group*2))
        print(self.sizes)
        
        #Empty data
        self.inputs = empty(shape=self.sizes[0])
        self.outputs = empty(shape=self.sizes[1])

        for i in range(size):
            # Input Data
            n_bin = str(bin(int(inputs[i])))[2:]
            n_bin = n_bin.zfill(self.sizes[0][1])

            # Output Data
            q_bin = str(bin(int(outputs[i][0])))[2:]
            q_bin = q_bin.zfill(self.sizes[1][1]//2)
            p_bin = str(bin(int(outputs[i][1])))[2:]
            p_bin = p_bin.zfill(self.sizes[1][1]//2)

            # Assigning
            self.inputs[i] = [int(i) for i in list(n_bin)]
            self.outputs[i] = [int(i) for i in list(p_bin + q_bin)]
        
            
