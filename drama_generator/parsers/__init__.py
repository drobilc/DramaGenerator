from .facebook import FacebookHTMLParser
from .telegram import TelegramJSONParser

PARSERS = [
    FacebookHTMLParser,
    TelegramJSONParser
]

PARSER_MAP = dict([(parser.__name__, parser) for parser in PARSERS])