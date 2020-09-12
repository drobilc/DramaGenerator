from .facebook import FacebookHTMLDataExtractor
from .telegram import TelegramJSONDataExtractor

EXTRACTORS = [
    FacebookHTMLDataExtractor,
    TelegramJSONDataExtractor
]

EXTRACTOR_MAP = dict([(extractor.__name__, extractor) for extractor in EXTRACTORS])