
# Create a simple neural network model
class Test:

    def __init__(self):
        self.topologyName = "Test"


    def create(self, i_size,o_size):
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dropout, Flatten, LSTM, Dense
        from tensorflow.keras.optimizers import Adam 
        print("I Size", i_size)
        print("O Size", o_size)

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

        
        
        #self.model = Sequential()
        # Add an LSTM layer
        #self.model.add(LSTM(1, input_shape=(i_size, 1), return_sequences=True))
        # Add a dense layer for output
        #self.model.add(Dense(1, activation='sigmoid'))
        
        # Compile the model
        optimizer = Adam(learning_rate=0.001) 
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy')
        
        # self.model = Sequential([
        #     LSTM(1, input_shape=(i_size,1), return_sequences=False),
        #     Dense(activation='sigmoid', units=o_size)
        # ])
        # self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])