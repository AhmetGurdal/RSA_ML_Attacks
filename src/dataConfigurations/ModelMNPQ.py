from src.classes.dataModel import DataModel

class ModelMNPQ(DataModel):
    #TODO : needs fixing
    def __init__(self):
        
        self.inputColumns=["n"]
        self.outputColumns=["p","q"]
        self.modelName = "ModelMNPQ"
        
        """
        - Model input is n in binary form as a matrix.
        - Model output is the combination of p and q primes in binary form in order as a matrix.
        """
    def setSizes(self, size, bit_group):
        from src.helper import Helper
        msizes = Helper.matrixSizes(bit_group*2)
        self.sizes = ((size,msizes[0],msizes[1]), (size,msizes[0],msizes[1]))
        
    def process(self, inputs, outputs, bit_group):
        from numpy import empty
        
        assert len(inputs) == len(outputs), "Input-Output data sizes do not match!"
        
        input_size = len(inputs)
        self.setSizes(input_size,bit_group)

        self.inputs = empty(shape=(self.sizes[0]))
        self.outputs = empty(shape=(self.sizes[1]))

        for i in range(input_size):

            # Input Data
            n_bin = str(bin(int(inputs[i])))[2:]
            n_bin = n_bin.zfill(bit_group * 2)
            self.inputs[i] = [[int(j) for j in list(i)] 
                              for i in [n_bin[ind:ind + self.sizes[0][-1]] 
                                            for ind in range(0,len(n_bin),self.sizes[0][-1])]]
            
            # Output Data
            q_bin = str(bin(int(outputs[i][0])))[2:]
            q_bin = q_bin.zfill(bit_group)
            p_bin = str(bin(int(outputs[i][1])))[2:]
            p_bin = p_bin.zfill(bit_group) 
            
            combination = p_bin + q_bin
            self.outputs[i] = [[int(j) for j in list(i)] 
                              for i in [combination[ind:ind + self.sizes[0][-1]] 
                                    for ind in range(0,len(combination),self.sizes[0][-1])]]

        self.inputs = self.inputs.reshape(-1,self.sizes[0][1],self.sizes[0][2],1)
        self.outputs = self.outputs.reshape(-1,self.sizes[1][1],self.sizes[1][2],1)
        self.sizes=((self.sizes[0][0],self.sizes[0][1],self.sizes[0][2],1), 
                    (self.sizes[1][0],self.sizes[1][1],self.sizes[1][2],1))