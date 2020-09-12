from .data_extractor import DataExtractor
from ..message_objects.message import Message
from datetime import datetime
import glob
from bs4 import BeautifulSoup

class FacebookHTMLDataExtractor(DataExtractor):
    
    def _read_message_file(self, encoding='utf-8'):
        # TODO: Don't read the whole file at once
        all_html_files = glob.glob('{}/*.html'.format(self.directory))
        assert len(all_html_files) >= 1
        chat_file = open(all_html_files[0], encoding=encoding)
        return chat_file
    
    def _parse_date(self, date_element, date_format='%b %d, %Y, %I:%M %p'):
        return datetime.strptime(date_element.text, date_format)
    
    def _parse_message_content(self, message_element):
        image_elements = message_element.find_all('img')
        
        images = []
        if len(image_elements) > 0:
            for image_element in image_elements:
                image_url = image_element['src']
                images.append(image_url)
                
                # Remove image parent if it is a link to an image, so that we can later find links in HTMl 
                if image_element.parent and image_element.parent.tag == 'a':
                    image_element.parent.decompose()            
        
        reactions = []
        reaction_element = message_element.find('ul')
        if reaction_element is not None:
            reaction_elements = reaction_element.find_all('li')
            for reaction_element in reaction_elements:
                reactions.append(reaction_element.text)            
        
        return {
            'images': images,
            'text': message_element.text,
            'reactions': reactions
        }
    
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
    
    def extract_data(self):
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
        
        return messages