
# Create a simple neural network model
class MultiDense:

    def __init__(self):
        self.topologyName = "MultiDense"


    def create(self, i_size,o_size):
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense
        from tensorflow.keras.optimizers import Adam 
        
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

        optimizer = Adam(learning_rate=0.001) 
        self.model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])