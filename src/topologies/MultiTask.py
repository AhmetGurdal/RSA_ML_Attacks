
class MultiTask:
    
    def __init__(self):
        self.topologyName = "MultiTask"

    def create(self, i_size, o_size):
        from tensorflow.keras.layers import Input, Dense # type: ignore
        from tensorflow.keras.models import Model # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        # Define the input layer
        input_layer = Input(shape=(i_size,))  # input_dim is the dimension of your input (e.g., n and s)

        # Shared hidden layers
        shared = Dense(128, activation='relu')(input_layer)
        shared = Dense(64, activation='relu')(shared)

        # Output layers for p and q
        output = Dense(o_size, activation='sigmoid', name='output')(shared)  # output_dim corresponds to the binary representation of p

        # Define the model
        self.model = Model(inputs=input_layer, outputs=[output])


        optimizer = Adam(learning_rate=0.001) 
        self.model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        


