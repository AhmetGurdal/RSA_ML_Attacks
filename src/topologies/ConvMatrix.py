class ConvMatrix:

    def __init__(self) -> None:
        self.topologyName = "ConvMatrix"

    def create(self, sizes):
        i_size = sizes[0][1:3]
        o_size = sizes[1][1:3]
        
        # assert i_size.length == 2, "input size is not suitable for this model"
        # assert o_size.length == 2, "output size is not suitable for this model"

        from tensorflow.keras.models import Sequential # type: ignore
        from tensorflow.keras.layers import Conv2D # type: ignore
        from tensorflow.keras.optimizers import Adam  # type: ignore

        self.model = Sequential()

        self.model.add(Conv2D(4, i_size, activation='relu', padding='same'))
        self.model.add(Conv2D(2, i_size, activation='relu', padding='same'))
        self.model.add(Conv2D(2, i_size, activation='relu', padding='same'))
        self.model.add(Conv2D(1, o_size, activation='sigmoid', padding='same'))

        optimizer = Adam(learning_rate=0.001) 
        self.model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
        