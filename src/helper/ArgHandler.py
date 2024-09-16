import argparse

class ArgHandler:

    def __init__(self):
        self.args = {}
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-dc', type=str, help='Train models with the defined <data_config> name. Must have input and output files in ./data/processed/<bit_group>/, start with the given value for this argument.\n Example value: ModelNPQ')
        self.parser.add_argument('-bg', type=str, help='Selected bit group, the folder names in ./data/processed/, Example: 256')
        self.parser.add_argument("-t", type=str, help='Train a specific model. (Default : all)', default="all")
        self.parser.add_argument("-e", type=int, help='Epoch (Default : 100)', default=100)
        self.args = self.parser.parse_args()
        