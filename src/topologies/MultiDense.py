class MultiDense:
    
    def __init__(self):
        self.topologyName = "MultiDense"

    def create(self,sizes):

        assert len(sizes[0]) == 2, "input size is not suitable for this model"
        assert len(sizes[1]) == 2, "output size is not suitable for this model"
        
        i_size = sizes[0][1]
        o_size = sizes[1][1]
        from tensorflow.keras.models import Sequential # type: ignore
        from tensorflow.keras.layers import Dense # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore
        
        self.model = Sequential([
            Dense(i_size, activation='relu', input_shape=(i_size,)),
            Dense(i_size, activation='relu'),
            Dense(i_size, activation='relu'),
            Dense(i_size, activation='relu'),
            Dense(i_size, activation='relu'),
            Dense(i_size, activation='relu'),
            Dense(i_size, activation='relu'),
            Dense(i_size, activation='relu'),
            Dense(i_size, activation='relu'),
            Dense(o_size, activation='sigmoid')
        ])

        optimizer = Adam(learning_rate=0.001) 
        self.model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])