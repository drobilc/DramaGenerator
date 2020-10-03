from .parser import Parser
from ..message_objects.message import Message
from datetime import datetime
import glob
import os.path

class WhatsAppParser(Parser):

    SERVICE_MESSAGE_SENDER = 'WhatsApp'
    DEFAULT_DATETIME_FORMAT = '%d/%m/%Y, %H:%M'

    def _setup_argument_parser(self, argument_parser):
        # Allow users to override default datetime format that is used when
        # parsing messages. Documentation can be found at
        # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        argument_parser.add_argument(
            '--date-format',
            dest='date_format',
            help='datetime format to use while parsing your file',
            default=WhatsAppParser.DEFAULT_DATETIME_FORMAT
        )
    
    def _read_messages_file(self, encoding='utf-8'):
        # Find a txt file inside the self.directory folder
        search_path = os.path.join(self.directory, '*.txt')
        found_files = glob.glob(search_path)

        # If there is no .txt file, raise an exception
        assert len(found_files) >= 1

        # Read the first found .txt file
        chat_file = open(found_files[0], encoding=encoding)
        return chat_file
    
    def _parse_message(self, line):
        # WhatsApp messages are in the following format:
        # date - sender: message
        date, other = line.split('-', 1)
        
        try:
            sender, message = other.split(':', 1)
        except Exception as e:
            # The message could not be split into sender and message. This
            # usually means that this is WhatsApp service message - somebody has
            # left / joined the group, ...
            sender = WhatsAppParser.SERVICE_MESSAGE_SENDER
            message = other
        
        # Convert date from string to datetime object
        parsed_date = datetime.strptime(date.strip(), self.arguments.date_format)

        # Construct a new message and return it
        return Message(sender.strip(), message.strip(), parsed_date)
    
    def parse(self):
        # Find HTML file in directory and read it
        chat_file = self._read_messages_file()

        messages = []
        
        # Parse each line in txt_file
        for line in chat_file:
            try:
                parsed_message = self._parse_message(line.strip())
                if parsed_message is not None:
                    messages.append(parsed_message)
            except Exception as e:
                print(e)
        
        return messages