class PolynomialRegressionModel:
    
    def __init__(self):
        self.topologyName = "PolynomialRegressionModel"

    def create(self, i_size, o_size):
        from tensorflow.keras.layers import Input, Dense # type: ignore
        from tensorflow.keras.models import Model # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        # Assuming polynomial features are precomputed and passed as input
        input_layer = Input(shape=(i_size,))

        # Dense layers
        x = Dense(64, activation='relu')(input_layer)
        x = Dense(32, activation='relu')(x)

        # Output layers for p and q
        output = Dense(o_size, activation='sigmoid', name='output')(x)

        # Define the model
        self.model = Model(inputs=input_layer, outputs=[output])

        # Compile the model
        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
