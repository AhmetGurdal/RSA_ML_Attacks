class ModelNQ:
    def __init__(self):
        self.inputColumns=["n"]
        self.outputColumns=["q"]
        self.modelName = "ModelNQ"
        ### Model n-pq
        """
        - Model input is n in binary form.
        - Model output is the prime q in binary form in order.
        """

    def setSizes(self, size, bit_group):
        self.sizes = ((size,bit_group*2), (size,bit_group*2))

    def process(self, inputs, outputs, bit_group):
        from numpy import empty
        assert len(inputs) == len(outputs), "Input-Output data sizes do not match!"

        size = len(inputs)
        self.sizes = ((size,bit_group*2), (size,bit_group*2))
        
        #Empty data
        self.inputs = empty(shape=self.sizes[0])
        self.outputs = empty(shape=self.sizes[1])

        for i in range(size):
            # Input Data
            n_bin = str(bin(int(inputs[i])))[2:]
            n_bin = n_bin.zfill(self.sizes[0][1])

            # Output Data
            q_bin = str(bin(int(outputs[i])))[2:]
            q_bin = q_bin.zfill(self.sizes[1][1])

            # Assigning
            self.inputs[i] = [int(i) for i in list(n_bin)]
            self.outputs[i] = [int(i) for i in list(q_bin)]