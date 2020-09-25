import argparse
import os.path
from drama_generator.parsers import *
from drama_generator.generators.latex_generator import LatexGenerator
from drama_generator.processors import *

# Create an argument parser and add arguments to it
argument_parser = argparse.ArgumentParser(description='Make a drama out of your chats')
# The only required parameter is INPUT_DIRECTORY, if no output_file argument is
# passed to the program, a default value is created using input directory name
argument_parser.add_argument('INPUT_DIRECTORY', type=str, help='path to the chat directory')
argument_parser.add_argument('-o', '--output-file', dest='output_file', type=str, help='output file path')

argument_parser.add_argument('-p', '--parser', dest='parser', choices=PARSER_MAP.keys(), help='which parser to use to extract data from directory', default='FacebookHTMLParser')
argument_parser.add_argument('--title', dest='title', type=str, help='title for the generated drama or infografic')
argument_parser.add_argument('--from', dest='date_from', type=str, help='take only messages after given time in format YYYY-MM-DD, eg. 2020-03-27')
argument_parser.add_argument('--to', dest='date_to', type=str, help='take only messages after given time in format YYYY-MM-DD, eg. 2020-03-27')
argument_parser.add_argument('--exclude', nargs='+', type=str, help='exclude certain person\'s messages, use like --exclude \'first person\' \'second person\'')

# Additional arguments for message processors
argument_parser.add_argument('--shout', dest='shout', action='store_true', help='write everything using only uppercase letters')

arguments = argument_parser.parse_args()

# Parse a list of arguments received
input_directory = arguments.INPUT_DIRECTORY
output_file = arguments.output_file

# Build a list of processors that will be applied to a list of messages (use
# arguments to construct it)
message_processors = []

if arguments.shout:
    message_processors.append(UpperCaseMessageProcessor)

# If output file is not provided, generate it using input directory argument
if output_file is None:
    output_file_name = os.path.basename(os.path.normpath(input_directory))
    output_file = os.path.join('generated_dramas', output_file_name)

print('Input directory: {}'.format(input_directory))
print('Output file: {}'.format(output_file))

print('Parsing messages from input directory')
# Based on the received parser name, generate a new parser and parse directory
parser = PARSER_MAP[arguments.parser]
message_parser = parser(input_directory)
messages = message_parser.parse()
print('Messages parsed')

print('Applying processors to list of messages')
# Apply each processor to a list of messages
for processor in message_processors:
    drama_processor = processor()
    messages = drama_processor.process(messages)
print('Processors applied')

print('Generating output file')
# Use LaTeX generator to generate drama and save it to output file
generator = LatexGenerator(messages)
generator.generate(output_file)
print('Output file generated')