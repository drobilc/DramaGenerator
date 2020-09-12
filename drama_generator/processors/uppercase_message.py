from .processor import Processor

class UpperCaseMessageProcessor(Processor):
    
    def process(self, messages):
        for message in messages:
            message.message = message.message.upper()
        return messages