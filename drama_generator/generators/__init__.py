from .latex_generator import LatexGenerator, PlariLatexGenerator
from .statistics_generator import StatisticsGenerator
from .pickle_generator import PickleGenerator

GENERATORS = [
    PickleGenerator,
    LatexGenerator,
    PlariLatexGenerator,
    StatisticsGenerator
]

GENERATOR_MAP = dict([(generator.__name__, generator) for generator in GENERATORS])