class AutoencoderFeatureExtraction:
    
    def __init__(self):
        self.topologyName = "AutoencoderFeatureExtraction"

    def create(self, sizes):
        i_size = sizes[0][1]
        o_size = sizes[1][1]
        from tensorflow.keras.layers import Input, Dense # type: ignore
        from tensorflow.keras.models import Model # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        # Encoder
        input_layer = Input(shape=(i_size,))
        encoded = Dense(i_size // 2, activation='relu')(input_layer)
        encoded = Dense(i_size// 4, activation='relu')(encoded)
        encoded_output = Dense(i_size // 8, activation='relu')(encoded)

        # Decoder
        decoded_p = Dense(i_size // 4, activation='relu')(encoded_output)
        decoded_p = Dense(i_size // 2, activation='relu')(decoded_p)
        output = Dense(o_size, activation='sigmoid', name='output')(decoded_p)

        self.model = Model(inputs=input_layer, outputs=[output])

        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])