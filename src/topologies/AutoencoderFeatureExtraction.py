class AutoencoderFeatureExtraction:
    
    def __init__(self):
        self.topologyName = "AutoencoderFeatureExtraction"

    def create(self, i_size, o_size):
        from tensorflow.keras.layers import Input, Dense # type: ignore
        from tensorflow.keras.models import Model # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        # Encoder
        input_layer = Input(shape=(i_size,))
        encoded = Dense(128, activation='relu')(input_layer)
        encoded = Dense(64, activation='relu')(encoded)
        encoded_output = Dense(32, activation='relu')(encoded)

        # Decoder for predicting p and q
        decoded_p = Dense(64, activation='relu')(encoded_output)
        decoded_p = Dense(128, activation='relu')(decoded_p)
        output = Dense(o_size, activation='sigmoid', name='output')(decoded_p)

        # Define the model
        self.model = Model(inputs=input_layer, outputs=[output])

        # Compile the model
        optimizer = Adam(learning_rate=0.001)
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])