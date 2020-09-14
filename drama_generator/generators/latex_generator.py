from pylatex import Document, Section, Subsection, Command, NewLine, PageStyle, Package
from pylatex.utils import italic, NoEscape, bold
import pylatex.config

class LatexGenerator(object):

    def __init__(self, messages):
        self.messages = messages

    """ Convert message objects into strings to be written in LaTeX file """
    def _generate_latex_for_message(self, message):
        return [
            bold(message.sender),
            ': ',
            message.message
        ]

    """ Assemble the LaTeX file """
    def generate(self, output_path):
        # Create an output document
        latex_document = Document(output_path)  

        # Import LaTeX packages
        latex_document.packages.append(Package('titling'))   

        # Define and set variables
        latex_document.preamble.append(Command('title', 'The Drama'))
        latex_document.preamble.append(Command('author', 'Drama Generator 2000'))
        latex_document.preamble.append(Command('date', NoEscape(r'\today')))

        # Create a title page
        """
        \begin{titlingpage}
            \maketitle
        \end{titlingpage}
        """
        latex_document.append(NoEscape(r'\begin{titlingpage}'))
        latex_document.append(NoEscape(r'\maketitle'))
        latex_document.append(NoEscape(r'\end{titlingpage}'))

        # Write drama
        for message in self.messages:
            latex_document.extend(self._generate_latex_for_message(message))
            latex_document.append(NewLine())

        # Generate a pdf drama based on LaTeX file assembled above
        latex_document.generate_pdf(clean_tex=True, compiler='xelatex')