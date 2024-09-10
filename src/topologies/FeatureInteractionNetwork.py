class FeatureInteractionNetwork:
    
    def __init__(self):
        self.topologyName = "FeatureInteractionNetwork"

    def create(self, sizes):
        i_size = sizes[0][1]
        o_size = sizes[1][1]
        from tensorflow.keras.layers import Input, Dense # type: ignore
        from tensorflow.keras.models import Model # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        input_layer = Input(shape=(i_size,))

        # Feature interaction layers
        interaction = Dense(i_size // 2, activation='relu')(input_layer)
        interaction = Dense(i_size // 4, activation='relu')(interaction)

        output = Dense(o_size, activation='sigmoid', name='output')(interaction)

        self.model = Model(inputs=input_layer, outputs=[output])

        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
