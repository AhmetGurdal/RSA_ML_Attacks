class HybridConvLSTM:
    
    def __init__(self):
        self.topologyName = "HybridConvLSTM"

    def create(self, sizes):
        i_size = sizes[0][1]
        o_size = sizes[1][1]
        from tensorflow.keras.models import Sequential # type: ignore
        from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dropout, Flatten, LSTM, Dense # type: ignore
        from tensorflow.keras.optimizers import Adam # type: ignore

        self.model = Sequential()

        # Convolutional Layer
        self.model.add(Conv1D(filters=64, kernel_size=3, padding='same', activation='relu', input_shape=(i_size, 1)))

        # Max Pooling Layer
        self.model.add(MaxPooling1D(pool_size=2))

        # LSTM Layer
        self.model.add(LSTM(i_size//4, activation='tanh', return_sequences=True))

        # Dropout Layer
        self.model.add(Dropout(0.3))

        # Flatten the output from LSTM to feed into the dense layer
        self.model.add(Flatten())

        # Output Layer
        self.model.add(Dense(o_size, activation='sigmoid'))
 
        optimizer = Adam(learning_rate=0.001) 
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy')