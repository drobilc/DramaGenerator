import argparse
from datetime import datetime

class Generator(object):

    def __init__(self, messages, arguments=[]):
        self.messages = messages
        
        # Construct a new argument parser
        argument_parser = argparse.ArgumentParser()

        # Each subclass of the Generator class should extend the Genarators
        # _setup_argument_parser(argument_parser) method, which should add
        # arguments to argument parser (if needed, otherwise it should do
        # nothing)
        self._setup_argument_parser(argument_parser)

        argument_parser.add_argument('-t', '--title',
            dest='title',
            type=str,
            help='title for the generated drama or infografic',
            default='The Drama'
        )

        # Use argument parser to actually parse received arguments
        self.arguments, other_arguments = argument_parser.parse_known_args(arguments)

        # If no title is provided, a default title should be inserted instead
        self.title = self.arguments.title
    
    def _setup_argument_parser(self, argument_parser):
        """Add additional arguments to argument parser if needed"""
        pass

    def generate(self, output_path):
        """Generate and write a document to the output_path"""
        pass