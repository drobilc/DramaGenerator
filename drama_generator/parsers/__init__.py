from .facebook import FacebookHTMLParser
from .telegram import TelegramJSONParser
from .whatsapp import WhatsAppParser
from .pickle import PickleParser

PARSERS = [
    PickleParser,
    FacebookHTMLParser,
    TelegramJSONParser,
    WhatsAppParser
]

PARSER_MAP = dict([(parser.__name__, parser) for parser in PARSERS])