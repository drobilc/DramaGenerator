from .generator import Generator
from datetime import datetime
import pickle

class PickleGenerator(Generator):

    def generate(self, output_path):
        with open(output_path, 'wb') as output_file:
            pickle.dump(self.messages, output_file)