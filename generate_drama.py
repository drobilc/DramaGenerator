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

# Additional arguments for message processors
argument_parser.add_argument('--no_acts', dest='no_acts', action='store_true', help='use if you want drama not to be divided into acts')
argument_parser.add_argument('--no_scenes', dest='no_scenes', action='store_true', help='use if you want drama not to be divided into scenes')
argument_parser.add_argument('--new_scene_time', dest='new_scene_time', type=float, help='minimal time in hours that has to pass between two consecutive messages so that one scene ends and another one starts')

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

logging.info('Processors:')
for ProcessorClass in PROCESSORS:
    processor = ProcessorClass(arguments=other_arguments)
    should_run_processor = processor.should_run()
    logging.info('[{}] {}'.format(
        'x' if should_run_processor else ' ',
        ProcessorClass.__name__
    ))
    if should_run_processor:
        message_processors.append(processor)

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
    logging.info('Applying message processor: {}'.format(processor.__class__.__name__))
    messages = processor.process(messages)
    
logging.info('Processors applied')

logging.info('Generating output file')

# Use LaTeX generator to generate drama and save it to output file
generator_class = GENERATOR_MAP[arguments.generator]
generator = generator_class(messages, arguments=other_arguments)
generator.generate(output_file)
logging.info('Output file generated')