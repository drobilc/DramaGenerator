from .parser import Parser
from ..message_objects.message import Message
from datetime import datetime
import glob
import json

import datetime
import json

def datetime_parser(json_dict):
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
        except:
            pass
    return json_dict

class TelegramJSONParser(Parser):

    DEFAULT_SENDER_NAME = 'Unknown'

    def _read_message_file(self, encoding='utf-8'):
        all_json_files = glob.glob('{}/*.json'.format(self.directory))
        assert len(all_json_files) >= 1
        chat_file = open(all_json_files[0], encoding=encoding)
        return chat_file
    
    def _parse_message(self, message_json):
        if 'type' not in message_json:
            return None
        
        if message_json['type'] != 'message':
            return None

        if 'from' in message_json and message_json['from'] is not None:
            sender = message_json['from']
        else:
            sender = TelegramJSONParser.DEFAULT_SENDER_NAME
        
        text = message_json['text']
        if isinstance(text, list):
            parts = []
            for part in text:
                if isinstance(part, str):
                    parts.append(part)
                elif isinstance(part, dict) and 'text' in part:
                    parts.append(part['text'])
            text = ' '.join(parts)
        
        date = message_json['date']

        return Message(sender, text, date)

    def parse(self):
        json_file = self._read_message_file()
        json_file_content = json.load(json_file, object_hook=datetime_parser)

        assert 'messages' in json_file_content

        messages = []
        for message in json_file_content['messages']:
            parsed_message = self._parse_message(message)
            if parsed_message is not None:
                messages.append(parsed_message)

        return messages