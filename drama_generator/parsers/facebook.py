from .parser import Parser
from ..message_objects.message import Message
from datetime import datetime
import glob
from bs4 import BeautifulSoup

class FacebookHTMLParser(Parser):

    def __init__(self, directory, date_format='%b %d, %Y, %I:%M %p'):
        super().__init__(directory)
        self.date_format = date_format
    
    def _read_message_file(self, encoding='utf-8'):
        # TODO: Don't read the whole file at once
        all_html_files = glob.glob('{}/*.html'.format(self.directory))

        # Check that there is a file we can read from
        assert len(all_html_files) >= 1 
        chat_file = open(all_html_files[0], encoding=encoding)
        return chat_file
    
    def _parse_date(self, date_element):
        return datetime.strptime(date_element.text, self.date_format)
    
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
        assert len(children) == 3
        
        sender_element, message_element, date_element = children
        
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
    
    def parse(self):
        # Find HTML file in directory and read it
        html_file = self._read_message_file()
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
                print(e)
        
        # After all messages have been parsed, reverse them, because Facebook
        # contains them in a reverse date order
        return list(reversed(messages))