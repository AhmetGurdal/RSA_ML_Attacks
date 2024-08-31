class PolynomialRegressionModel:
    
    def __init__(self):
        self.topologyName = "PolynomialRegressionModel"

    def create(self, i_size, o_size):
        from tensorflow.keras.layers import Input, Dense # type: ignore
        from tensorflow.keras.models import Model # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        input_layer = Input(shape=(i_size,))

        # Dense layers
        x = Dense(i_size//2, activation='relu')(input_layer)
        x = Dense(i_size//4, activation='relu')(x)

        output = Dense(o_size, activation='sigmoid', name='output')(x)

        self.model = Model(inputs=input_layer, outputs=[output])

        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
