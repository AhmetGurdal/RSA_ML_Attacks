class Hierarchical:
    
    def __init__(self):
        self.topologyName = "Hierarchical"

    def create(self, i_size, o_size):
        from tensorflow.keras.layers import Input, Dense, Concatenate # type: ignore
        from tensorflow.keras.models import Model # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        # First stage model: Predict an intermediate value
        input_layer = Input(shape=(i_size,))
        intermediate = Dense(128, activation='relu')(input_layer)
        intermediate = Dense(64, activation='relu')(intermediate)
        intermediate_output = Dense(1, activation='linear', name='intermediate_output')(intermediate)

        # Second stage model: Predict p and q using intermediate value
        second_input = Concatenate()([input_layer, intermediate_output])
        hidden = Dense(128, activation='relu')(second_input)
        hidden = Dense(64, activation='relu')(hidden)
        output = Dense(o_size, activation='sigmoid', name='output')(hidden)

        # Define the model
        self.model = Model(inputs=input_layer, outputs=[output])

        # Compile the model
        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
