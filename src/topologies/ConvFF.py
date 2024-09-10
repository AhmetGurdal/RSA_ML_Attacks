
class ConvFF:
    
    def __init__(self):
        self.topologyName = "ConvFF"

    def create(self, sizes):
        i_size = sizes[0][1]
        o_size = sizes[1][1]
        from tensorflow.keras.models import Sequential # type: ignore
        from tensorflow.keras.layers import Dense, Dropout, Conv1D, Flatten # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore
        self.model = Sequential([
            Conv1D(i_size, 3, activation='relu', input_shape=(i_size, 1)),
            Flatten(),
            Dense(i_size, activation='relu'),
            Dropout(0.2),
            Dense(i_size, activation='relu'),
            Dense(o_size, activation='softmax')
        ])

        optimizer = Adam(learning_rate=0.001) 
        self.model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        