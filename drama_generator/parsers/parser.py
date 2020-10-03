import argparse
from datetime import datetime

class Parser(object):
    
    def __init__(self, directory, arguments=[]):
        self.directory = directory

        # Construct a new argument parser
        argument_parser = argparse.ArgumentParser()

        # Each subclass of the Generator class should extend the Genarators
        # _setup_argument_parser(argument_parser) method, which should add
        # arguments to argument parser (if needed, otherwise it should do
        # nothing)
        self._setup_argument_parser(argument_parser)

        # Use argument parser to actually parse received arguments
        self.arguments, other_arguments = argument_parser.parse_known_args(arguments)
    
    def _setup_argument_parser(self, argument_parser):
        """Add additional arguments to argument parser if needed"""
        pass
    
    def parse(self):
        """Convert directory object to a list of Message objects"""
        return []