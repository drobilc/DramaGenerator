from .latex_generator import LatexGenerator, PlariLatexGenerator

GENERATORS = [
    LatexGenerator,
    PlariLatexGenerator
]

GENERATOR_MAP = dict([(generator.__name__, generator) for generator in GENERATORS])