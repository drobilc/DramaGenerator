from pylatex import Document, Section, Subsection, Command, NewLine
from pylatex.utils import italic, NoEscape, bold

class LatexGenerator(object):

    def __init__(self, messages):
        self.messages = messages

    def _generate_latex_for_message(self, message):
        return [
            bold(message.sender),
            ': ',
            message.message
        ]

    def generate(self, output_path):
        latex_document = Document(output_path)        
        
        for message in self.messages:
            latex_document.extend(self._generate_latex_for_message(message))
            latex_document.append(NewLine())

        latex_document.generate_pdf(clean_tex=True, compiler='xelatex')