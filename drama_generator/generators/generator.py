import argparse
from datetime import datetime

class Generator(object):

    DEFAULT_TITLE = 'The drama'

    def __init__(self, messages, title=None, arguments=[]):
        self.messages = messages
        
        # If no title is provided, a default title should be inserted instead
        self.title = title
        if self.title is None:
            self.title = Generator.DEFAULT_TITLE
        
        # Construct a new argument parser
        argument_parser = argparse.ArgumentParser()

        # Each subclass of the Generator class should extend the Genarators
        # _setup_argument_parser(argument_parser) method, which should add
        # arguments to argument parser (if needed, otherwise it should do
        # nothing)
        self._setup_argument_parser(argument_parser)

        # Use argument parser to actually parse received arguments
        self.arguments = argument_parser.parse_args(arguments)
    
    def _setup_argument_parser(self, argument_parser):
        """Add additional arguments to argument parser if needed"""
        pass

    def generate(self, output_path):
        """Generate and write a document to the output_path"""
        pass