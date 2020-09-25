from pylatex import Document, Section, Subsection, Command, NewLine, PageStyle, Package
from pylatex.utils import italic, NoEscape, bold

class LatexGenerator(object):

    DEFAULT_TITLE = 'The drama'

    def __init__(self, messages, title=None):
        self.messages = messages
        
        self.title = title
        if self.title is None:
            self.title = LatexGenerator.DEFAULT_TITLE
    
    def authors(self):
        authors = set([])
        for message in self.messages:
            authors.add(message.sender)
        return list(authors)

    """ Convert message objects into strings to be written in LaTeX file """
    def _generate_latex_for_message(self, message):
        return [
            Command('Line', arguments=[message.sender, message.message])
        ]

    """ Assemble the LaTeX file """
    def generate(self, output_path):
        # Create an output document
        latex_document = Document(output_path)

        # Use custom document class - drama.cls
        latex_document.documentclass = Command(
            'documentclass',
            arguments=['drama']
        )

        authors = ', '.join(self.authors())
        latex_document.append(Command('TitlePage', [self.title, authors]))

        # Write a list of messages to document
        for message in self.messages:
            latex_document.extend(self._generate_latex_for_message(message))

        # Generate a pdf drama based on LaTeX file assembled above. 
        # Set clean_tex=True if you want .tex file deleted after it is compiled to pdf.
        latex_document.generate_pdf(clean_tex=False, compiler='xelatex')