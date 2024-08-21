import argparse

class ArgHandler:

    def __init__(self):
        self.args = {}
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-dc', type=str, help='Train models with the defined <data_config> name. Must have input and output files under ./data/processed, start with the given value for this argument.\n Example value: ModelNPQ_256')
        self.parser.add_argument("-t", type=str, help='Train a specific model. (Default : all)', default="all")
        self.parser.add_argument("-e", type=int, help='Epoch (Default : 100)', default=100)
        self.args = self.parser.parse_args()
        