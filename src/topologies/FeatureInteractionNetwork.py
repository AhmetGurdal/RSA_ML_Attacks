class FeatureInteractionNetwork:
    
    def __init__(self):
        self.topologyName = "FeatureInteractionNetwork"

    def create(self, i_size, o_size):
        from tensorflow.keras.layers import Input, Dense # type: ignore
        from tensorflow.keras.models import Model # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        input_layer = Input(shape=(i_size,))

        # Feature interaction layers
        interaction = Dense(128, activation='relu')(input_layer)
        interaction = Dense(64, activation='relu')(interaction)

        # Output layers for p and q
        output = Dense(o_size, activation='sigmoid', name='output')(interaction)

        # Define the model
        self.model = Model(inputs=input_layer, outputs=[output])

        # Compile the model
        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
