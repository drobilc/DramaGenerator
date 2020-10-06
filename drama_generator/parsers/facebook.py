from .parser import Parser
from ..message_objects.message import Message
import logging
from datetime import datetime
import glob
from bs4 import BeautifulSoup
import locale

class FacebookHTMLParser(Parser):

    DEFAULT_DATETIME_FORMAT = '%b %d, %Y, %I:%M %p'
    DEFAULT_LOCALE = 'english_us'
    
    def _setup_argument_parser(self, argument_parser):
        # Allow users to override default datetime format that is used when
        # parsing messages. Documentation can be found at
        # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        argument_parser.add_argument(
            '--date-format',
            dest='date_format',
            help='datetime format to use while parsing your file',
            default=FacebookHTMLParser.DEFAULT_DATETIME_FORMAT
        )

        # Also allow users to add locale for parsing date in case their date
        # format contains localized date strings such as 'Marec'
        argument_parser.add_argument(
            '--locale',
            dest='locale',
            help='locale to be used when parsing dates',
            default=FacebookHTMLParser.DEFAULT_LOCALE
        )
    
    def _find_chat_files(self):
        return glob.glob('{}/*.html'.format(self.directory))
    
    def _parse_date(self, date_element):
        return datetime.strptime(date_element.text.lower().strip(), self.arguments.date_format)
    
    # Parse non-ordinary-text content form a single message object
    def _parse_message_content(self, message_element):
        image_elements = message_element.find_all('img')
        
        images = []
        if len(image_elements) > 0:
            # Get all images
            for image_element in image_elements:
                image_url = image_element['src']
                images.append(image_url)
                
                # Remove image from HTML
                if image_element.parent and image_element.parent.tag == 'a':
                    image_element.parent.decompose()            
        
        # Get all reactions
        reactions = []
        reaction_element = message_element.find('ul')
        if reaction_element is not None:
            reaction_elements = reaction_element.find_all('li')
            for reaction_element in reaction_elements:
                reactions.append(reaction_element.text)
        
            # Remove list of reactions from HTML, so it doesn't appear in message
            # text
            reaction_element.decompose()
        
        return {
            'images': images,
            'text': message_element.text,
            'reactions': reactions
        }
    
    # Turn html divs into a Message objects
    def _parse_message(self, message_html):
        children = list(message_html.children)
        assert len(children) >= 3
        
        sender_element, message_element, date_element = children[0], children[1], children[2]
        
        # Extract sender, message and date information from message
        sender = sender_element.text
        message = self._parse_message_content(message_element)
        date = self._parse_date(date_element)
        
        return Message(
            sender,
            message['text'],
            date,
            images=message['images'],
            reactions=message['reactions']
        )

    def parse_messages_from_file(self, html_file):
        html_file_content = html_file.read()
        
        # Parse it using the BeautifulSoup library
        html = BeautifulSoup(html_file_content, 'html.parser')
        
        # Find all message containers in the document
        message_elements = html.find_all('div', {'class': 'uiBoxWhite'})
        
        # Parse each message
        messages = []
        for message_element in message_elements:
            try:
                messages.append(self._parse_message(message_element))
            except Exception as e:
                logging.error(e)
        
        return messages
    
    def parse(self, encoding='utf-8'):
        if self.arguments.locale is not None:
            locale.setlocale(locale.LC_ALL, self.arguments.locale)
        
        # Find all Facebook chat files (message_1.html, ...)
        chat_files = self._find_chat_files()
        logging.info('Found {} chat files'.format(len(chat_files)))

        # Iterate over all of them, don't bother sorting files, because messages
        # will be sorted at the end
        messages = []
        for filename in chat_files:
            try:
                logging.info('Parsing: {}'.format(filename))
                chat_file = open(filename, encoding=encoding)
                additional_messages = self.parse_messages_from_file(chat_file)
                messages.extend(additional_messages)
            except Exception:
                logging.info('Could not read chat file {}'.format(filename))
        
        # Sort message by date
        logging.info('Sorting messages')
        messages.sort(key=lambda message: message.date)
        
        return messages