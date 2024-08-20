class ResidualNetwork:
    
    def __init__(self):
        self.topologyName = "ResidualNetwork"

    def create(self, i_size, o_size):
        from tensorflow.keras.layers import Input, Dense, ReLU # type: ignore
        from tensorflow.keras.models import Model # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        input_layer = Input(shape=(i_size,))

        # First hidden layer
        x = Dense(128, activation='relu')(input_layer)
        # Residual block 1
        residual = Dense(128, activation=None)(x)
        x = ReLU()(residual + x)
        # Residual block 2
        residual = Dense(128, activation=None)(x)
        x = ReLU()(residual + x)

        # Output layers for p and q
        output = Dense(o_size, activation='sigmoid', name='output')(x)

        # Define the model
        self.model = Model(inputs=input_layer, outputs=[output])

        # Compile the model
        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])