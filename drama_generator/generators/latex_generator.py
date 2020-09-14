from pylatex import Document, Section, Subsection, Command, NewLine, PageStyle, Package
from pylatex.utils import italic, NoEscape, bold

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
        """ USAGE:
        latex_document.packages.append(Package('packagename', ['option1', 'option2', 'option3']))
        """
        latex_document.packages.append(Package('titling'))
        latex_document.packages.append(Package('geometry', ['textwidth=350pt', 'textheight=600pt'])) # specify the dimensions of text area

        # Define and set variables
        """ USAGE:
        \command{value} -> latex_document.preamble.append(Command('command', 'value'))
        \command{multiple}{values} -> latex_document.preamble.append(Command('command', ['multiple', 'values']))
        if \subcommand appears among values -> NoEscape(r'\subcommand')
        """
        latex_document.preamble.append(Command('title', 'The Drama'))
        latex_document.preamble.append(Command('author', 'Drama Generator 2000'))
        latex_document.preamble.append(Command('date', NoEscape(r'\today')))
        latex_document.preamble.append(Command('fontsize', ['12pt', '20pt'])) # [font size, space between ines]
        latex_document.preamble.append(Command('setlength', [NoEscape(r'\parindent'), '0pt'])) # remove indent at the begining of paragraphs

        # Create a title page
        latex_document.append(NoEscape(r'\begin{titlingpage}'))
        latex_document.append(NoEscape(r'\maketitle'))
        latex_document.append(NoEscape(r'\end{titlingpage}'))

        # Write drama - currently commented out because smileys cause compilation errors

        # for message in self.messages:
        #     latex_document.extend(self._generate_latex_for_message(message))
        #     latex_document.append(NewLine())

        # TODO: For encoding problems with smileys see https://www.overleaf.com/learn/how-to/What_file_encodings_and_line_endings_should_I_use%3F
        
        # Sample text to clearly see the text area, font size and space between the lines
        latex_document.append('tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text tetx text')

        # Generate a pdf drama based on LaTeX file assembled above. 
        # Set clean_tex=True if you want .tex file deleted after it is compiled to pdf.
        latex_document.generate_pdf(clean_tex=False, compiler='xelatex')