from .processor import Processor

class UpperCaseMessageProcessor(Processor):

    def _setup_argument_parser(self, argument_parser):
        argument_parser.add_argument(
            '--shout',
            dest='shout',
            action='store_true',
            help='write everything using only uppercase letters'
        )

    def should_run(self):
        return self.arguments.shout
    
    def process(self, messages):
        for message in messages:
            message.message = message.message.upper()
        return messages