from .latex_generator import LatexGenerator, PlariLatexGenerator
from .statistics_generator import StatisticsGenerator

GENERATORS = [
    LatexGenerator,
    PlariLatexGenerator,
    StatisticsGenerator
]

GENERATOR_MAP = dict([(generator.__name__, generator) for generator in GENERATORS])