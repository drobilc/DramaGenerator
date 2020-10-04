import argparse
import os.path
import logging
from drama_generator.parsers import *
from drama_generator.generators import *
from drama_generator.processors import *

# Setup logger that will be used to output data to the user
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Create an argument parser and add arguments to it
argument_parser = argparse.ArgumentParser(description='Make a drama out of your chats')
# The only required parameter is INPUT_DIRECTORY, if no output_file argument is
# passed to the program, a default value is created using input directory name
argument_parser.add_argument('INPUT_DIRECTORY', type=str, help='path to the chat directory')
argument_parser.add_argument('-o', '--output-file', dest='output_file', type=str, help='output file path')

argument_parser.add_argument('-p', '--parser', dest='parser', choices=PARSER_MAP.keys(), help='which parser to use to extract data from directory', default='FacebookHTMLParser')
argument_parser.add_argument('-g', '--generator', dest='generator', choices=GENERATOR_MAP.keys(), help='which generator to use to generate output file', default='LatexGenerator')

argument_parser.add_argument('-t','--title', dest='title', type=str, help='title for the generated drama or infografic')
argument_parser.add_argument('-a','--from', dest='date_from', type=str, help='take only messages after given time in format YYYY-MM-DD-HH:MM:SS.UUUUUU, eg. 2020-03-27 or 2020-03-27-07:31:22.000000')
argument_parser.add_argument('-b','--to', dest='date_to', type=str, help='take only messages after given time in format YYYY-MM-DD-HH:MM:SS.UUUUUU, eg. 2020-03-27 or 2020-03-27-07:31:22.000000')
argument_parser.add_argument('-e','--exclude', dest='excluded_persons', type=str, help='exclude certain person\'s messages, use like --exclude "first person,second person,third person"')

# Additional arguments for message processors
argument_parser.add_argument('--shout', dest='shout', action='store_true', help='write everything using only uppercase letters')

# Because we need the `parser` argument to construct a new parser, but also want
# to allow parsers to have their own arguments, we don't want to call the
# argument_parser.parse_args() as it will raise an exception if it encounters
# unknown argument.
# We should first parse the known arguments, construct a new parser and pass it
# the unparsed arguments so it can parse them further.
# https://docs.python.org/3/library/argparse.html#partial-parsing
arguments, other_arguments = argument_parser.parse_known_args()

# Parse a list of arguments received
input_directory = arguments.INPUT_DIRECTORY
output_file = arguments.output_file

# Build a list of processors that will be applied to a list of messages (use
# arguments to construct it)
message_processors = []

message_processors.append(RemoveEmojisProcessor)

if arguments.shout:
    message_processors.append(UpperCaseMessageProcessor)


has_date_from = arguments.date_from is not None
has_date_to = arguments.date_to is not None
if has_date_from or has_date_to:
    date_from = arguments.date_from
    date_to = arguments.date_to
    message_processors.append(FilterByDateProcessor)

# If output file is not provided, generate it using input directory argument
if output_file is None:
    output_file_name = os.path.basename(os.path.normpath(input_directory))
    output_file = os.path.join('generated_dramas', output_file_name)

logging.info('Input directory: {}'.format(input_directory))
logging.info('Output file: {}'.format(output_file))

logging.info('Parsing messages from input directory')
# Based on the received parser name, generate a new parser and parse directory
parser = PARSER_MAP[arguments.parser]
message_parser = parser(input_directory, arguments=other_arguments)
messages = message_parser.parse()
logging.info('Messages parsed')

logging.info('Applying processors to list of messages')
# Apply each processor to a list of messages
for processor in message_processors:
    logging.info('Applying message processor: {}'.format(processor.__name__))
    drama_processor = processor()
    if str(processor.__name__) == "FilterByDateProcessor":
        messages = drama_processor.process_date(messages, date_from, date_to)
    else:
        messages = drama_processor.process(messages)
logging.info('Processors applied')

logging.info('Generating output file')

# Use LaTeX generator to generate drama and save it to output file
generator_class = GENERATOR_MAP[arguments.generator]
generator = generator_class(messages, arguments=other_arguments)
generator.generate(output_file)
logging.info('Output file generated')