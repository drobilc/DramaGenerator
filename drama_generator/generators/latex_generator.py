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

    def _generate_latex_for_message(self, message):
        """ Convert message objects into strings to be written in LaTeX file """
        return [
            Command('Line', arguments=[message.sender, message.message])
        ]
    
    def _generate_scene_list(self, messages, silence_length=8):
        """Create a list of lists of messages that belong in the same scene"""
        # A scene consists of a stream of messages that doesn't have a pause
        # longer than specified time.
        # The default silence length is 8 hours (the average sleep time of an adult)
        if len(messages) <= 0:
            return []

        scenes = []

        current_scene = [messages[0]]
        last_message_date = messages[0].date
        
        for message in messages[1:]:

            time_difference = message.date - last_message_date

            if time_difference.total_seconds() / 3600 > silence_length:
                scenes.append(current_scene)
                current_scene = []

            current_scene.append(message)
            last_message_date = message.date
        
        if len(current_scene) > 0:
            scenes.append(current_scene)

        return scenes


    def generate(self, output_path):
        """ Assemble the LaTeX file """

        # Create an output document
        latex_document = Document(output_path)

        # Use custom document class - drama.cls
        latex_document.documentclass = Command(
            'documentclass',
            arguments=['drama']
        )

        # Add a title page to latex document
        authors = ', '.join(self.authors())
        latex_document.append(Command('TitlePage', [self.title, authors]))

        # A scene consists of a stream of messages that doesn't have a pause
        # longer than specified time (for example 8 hours)
        scenes = self._generate_scene_list(self.messages)

        # Write a list of messages in scenes to latex document
        for scene in scenes:
            latex_document.append(Command('Scene'))
            for message in scene:
                latex_document.extend(self._generate_latex_for_message(message))

        # Generate a pdf drama based on LaTeX file assembled above. 
        # Set clean_tex=True if you want .tex file deleted after it is compiled to pdf.
        latex_document.generate_pdf(clean_tex=True, compiler='xelatex')