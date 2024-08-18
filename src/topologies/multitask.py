
class MultiTask:
    
    def __init__(self):
        self.topologyName = "MultiTask"

    def create(self, i_size, o_size):
        from tensorflow.keras.layers import Input, Dense
        from tensorflow.keras.models import Model

        # Define the input layer
        input_layer = Input(shape=(i_size,))  # input_dim is the dimension of your input (e.g., n and s)

        # Shared hidden layers
        shared = Dense(128, activation='relu')(input_layer)
        shared = Dense(64, activation='relu')(shared)

        # Output layers for p and q
        p_output = Dense(o_size, activation='sigmoid', name='p_output')(shared)  # output_dim corresponds to the binary representation of p
        q_output = Dense(o_size, activation='sigmoid', name='q_output')(shared)

        # Define the model
        model = Model(inputs=input_layer, outputs=[p_output, q_output])

        # Compile the model
        model.compile(optimizer='adam', loss={'p_output': 'binary_crossentropy', 'q_output': 'binary_crossentropy'}, metrics=['accuracy'])

        #optimizer = Adam(learning_rate=0.001) 
        #self.model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        


