from .processor import Processor

class RemovePersonsProcessor(Processor):

    def _setup_argument_parser(self, argument_parser):
        argument_parser.add_argument(
            '-e', '--exclude',
            dest='excluded_persons',
            type=str,
            help='exclude certain person\'s messages, use like --exclude "first person,second person,third person"'
        )
    
    def should_run(self):
        return self.arguments.excluded_persons is not None
    
    def process(self, messages):
        persons = self.arguments.excluded_persons.split(",")

        for message in reversed(messages):
            for person in persons:
                if message.sender == person:
                    messages.remove(message)
        
        return messages