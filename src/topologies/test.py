
# Create a simple neural network model
class Test:

    def __init__(self):
        self.topologyName = "Test"


    def create(self, i_size,o_size):
        print("I Size", i_size)
        print("O Size", o_size)
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense
        self.model = Sequential([
            LSTM(1, input_shape=(i_size,1), return_sequences=False),
            Dense(activation='sigmoid', units=o_size)
        ])

        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])