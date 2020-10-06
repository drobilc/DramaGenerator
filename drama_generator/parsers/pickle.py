from .parser import Parser
from datetime import datetime

import pickle

class PickleParser(Parser):

    def parse(self):
        with open(self.directory, 'rb') as input_file:
            return pickle.load(input_file)
        return []