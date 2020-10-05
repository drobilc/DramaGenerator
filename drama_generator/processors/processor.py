import argparse

class Processor(object):

    def __init__(self, arguments=[]):
        # Construct a new argument parser
        argument_parser = argparse.ArgumentParser()

        # Each subclass of the Generator class should extend the Genarators
        # _setup_argument_parser(argument_parser) method, which should add
        # arguments to argument parser (if needed, otherwise it should do
        # nothing)
        self._setup_argument_parser(argument_parser)

        # Use argument parser to actually parse received arguments
        self.arguments, other_arguments = argument_parser.parse_known_args(arguments)
    
    def should_run(self):
        """Whether the processor should run or not"""
        return False
    
    def _setup_argument_parser(self, argument_parser):
        """Add additional arguments to argument parser if needed"""
        pass
    
    def process(self, messages):
        return messages