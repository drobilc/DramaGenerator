from .facebook import FacebookHTMLParser
from .telegram import TelegramJSONParser
from .whatsapp import WhatsAppParser

PARSERS = [
    FacebookHTMLParser,
    TelegramJSONParser,
    WhatsAppParser
]

PARSER_MAP = dict([(parser.__name__, parser) for parser in PARSERS])