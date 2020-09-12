import argparse
from drama_generator.data_extractors.facebook import FacebookHTMLDataExtractor
from drama_generator.generators.latex_generator import LatexGenerator
from drama_generator.processors import *

parser = argparse.ArgumentParser(description='Make a drama out of your chats')
parser.add_argument('path', type=str, nargs=1, help='path to the chat directory')
parser.add_argument('output_file', type=str, nargs=1, help='output file path')

args = parser.parse_args()

path = args.path[0]
output_file = args.output_file[0]

facebook_html_extractor = FacebookHTMLDataExtractor(path)
messages = facebook_html_extractor.extract_data()

PROCESSORS = [
    UpperCaseMessageProcessor
]

for processor in PROCESSORS:
    drama_processor = processor()
    messages = drama_processor.process(messages)

generator = LatexGenerator(messages)
generator.generate(output_file)