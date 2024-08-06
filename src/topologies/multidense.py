
# Create a simple neural network model
class MultiDense:

    def __init__(self):
        self.topologyName = "MultiDense"


    def create(self, i_size,o_size):
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense
        self.model = Sequential([
            Dense(i_size, activation='relu', input_shape=(i_size,)),
            Dense(i_size, activation='relu', input_shape=(i_size,)),
            Dense(i_size, activation='relu', input_shape=(i_size,)),
            Dense(i_size, activation='relu', input_shape=(i_size,)),
            Dense(i_size, activation='relu', input_shape=(i_size,)),
            Dense(i_size, activation='relu', input_shape=(i_size,)),
            Dense(i_size, activation='relu', input_shape=(i_size,)),
            Dense(i_size, activation='relu', input_shape=(i_size,)),
            Dense(i_size, activation='relu'),
            Dense(o_size, activation='sigmoid')
        ])

        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])