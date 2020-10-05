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
    
    def process_date(self, messages, date_from_str, date_to_str):
        # Get datetime object for date_from and date_to
        if date_from_str is not None:
            if len(date_from_str) > 10: # YYYY-MM-DD-HH:MM:SS.UUUUUU
                date_from = datetime.strptime(date_from_str, "%Y-%m-%d-%H:%M:%S")
            else: # YYYY-MM-DD, len = 10
                date_from = datetime.strptime(date_from_str, "%Y-%m-%d")
        if date_to_str is not None:
            if len(date_to_str) > 10: # YYYY-MM-DD-HH:MM:SS.UUUUUU
                date_to = datetime.strptime(date_to_str, "%Y-%m-%d-%H:%M:%S")
            else: # YYYY-MM-DD, len = 10
                date_to = datetime.strptime(date_to_str, "%Y-%m-%d")

        messages = filter_by_date(messages, date_from, date_to)

        return messages