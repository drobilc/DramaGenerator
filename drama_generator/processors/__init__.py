from .uppercase_message import UpperCaseMessageProcessor
from .remove_emojis import RemoveEmojisProcessor
from .filter_by_date import FilterByDateProcessor
from .remove_persons import RemovePersonsProcessor

PROCESSORS = [
    UpperCaseMessageProcessor,
    RemoveEmojisProcessor,
    FilterByDateProcessor,
    RemovePersonsProcessor,
]