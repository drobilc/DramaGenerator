from .processor import Processor
from datetime import datetime

def filter_by_date(messages, date_from, date_to):
    
    for message in reversed(messages):
        
        current_date = message.date
        
        if date_from is not None:
            if current_date < date_from:
                messages.remove(message)
        
        if date_to is not None:
            if current_date > date_to:
                messages.remove(message)
    return messages

class FilterByDateProcessor(Processor):

    def _setup_argument_parser(self, argument_parser):
        argument_parser.add_argument(
            '-a', '--after',
            dest='date_from',
            type=str,
            help='take only messages after given time in format YYYY-MM-DD-HH:MM:SS.UUUUUU, eg. 2020-03-27 or 2020-03-27-07:31:22.000000'
        )
        argument_parser.add_argument(
            '-b', '--before',
            dest='date_to',
            type=str,
            help='take only messages after given time in format YYYY-MM-DD-HH:MM:SS.UUUUUU, eg. 2020-03-27 or 2020-03-27-07:31:22.000000'
        )

    def should_run(self):
        return self.arguments.date_from is not None or self.arguments.date_to is not None
    
    def process(self, messages):
        # Get datetime object for date_from and date_to
        date_from, date_to = None, None
        if self.arguments.date_from is not None:
            if len(self.arguments.date_from) > 10: # YYYY-MM-DD-HH:MM:SS.UUUUUU
                date_from = datetime.strptime(self.arguments.date_from, "%Y-%m-%d-%H:%M:%S")
            else: # YYYY-MM-DD, len = 10
                date_from = datetime.strptime(self.arguments.date_from, "%Y-%m-%d")
        if self.arguments.date_to is not None:
            if len(self.arguments.date_to) > 10: # YYYY-MM-DD-HH:MM:SS.UUUUUU
                date_to = datetime.strptime(self.arguments.date_to, "%Y-%m-%d-%H:%M:%S")
            else: # YYYY-MM-DD, len = 10
                date_to = datetime.strptime(self.arguments.date_to, "%Y-%m-%d")

        messages = filter_by_date(messages, date_from, date_to)

        return messages