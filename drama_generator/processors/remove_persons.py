from .processor import Processor

class RemovePersonsProcessor(Processor):
    
    def process_persons(self, messages, persons_str):
        persons = persons_str.split(",")

        for message in reversed(messages):
            for person in persons:
                if message.sender == person:
                    messages.remove(message)
        
        return messages