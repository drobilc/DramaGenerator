import argparse
from drama_generator.data_extractors.facebook import FacebookHTMLDataExtractor

parser = argparse.ArgumentParser(description='Make a drama out of your chats')
parser.add_argument('path', type=str, nargs=1, help='path to the chat directory')

args = parser.parse_args()

path = args.path[0]

facebook_html_extractor = FacebookHTMLDataExtractor(path)
messages = facebook_html_extractor.extract_data()
print(messages)