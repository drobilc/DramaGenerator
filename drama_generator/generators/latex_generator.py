from .generator import Generator
from pylatex import Document, Section, Subsection, Command, NewLine, PageStyle, Package
from pylatex.utils import italic, NoEscape, bold

from datetime import datetime

class LatexGenerator(Generator):

    DEFAULT_TITLE = 'The drama'

    def __init__(self, messages, title=None, arguments=[]):
        super().__init__(messages, title=title, arguments=arguments)
    
    def _setup_argument_parser(self, argument_parser):
        # Add arguments to argument parser
        argument_parser.add_argument('--no-acts',
            dest='generate_acts',
            action='store_false',
            help='should the generated scenes be grouped in acts'
        )
    
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

    def _generate_act_list(self, scenes):
        if len(scenes) <= 0:
            return []
        
        acts = []

        current_act = [scenes[0]]
        current_act_start = scenes[0][0].date
        # TODO: Scene can be empty, ...
        for scene in scenes[1:]:
            scene_start = scene[0].date
            
            if current_act_start.year != scene_start.year or current_act_start.month != scene_start.month:
                acts.append({
                    'date': current_act_start,
                    'scenes': current_act
                })
                current_act = []
                current_act_start = scene_start
            
            current_act.append(scene)
        
        if len(current_act) > 0:
            acts.append({
                'date': current_act_start,
                'scenes': current_act
            })

        return acts

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

        # After the scenes have been generated, construct a list of acts. An act
        # is a group of scenes that appear in a certain time period (a month, ...)
        if self.arguments.generate_acts:
            acts = self._generate_act_list(scenes)
        else:
            acts = [{ 'date': datetime.now(), 'scenes': scenes }]

        # Write a list of messages in scenes to latex document
        for act in acts:

            if self.arguments.generate_acts:
                act_date = act['date'].strftime("%B %Y")
                latex_document.append(Command('Act', arguments=[act_date]))
            
            for scene in act['scenes']:
                latex_document.append(Command('Scene'))
                for message in scene:
                    latex_document.extend(self._generate_latex_for_message(message))

        # Generate a pdf drama based on LaTeX file assembled above. 
        # Set clean_tex=True if you want .tex file deleted after it is compiled to pdf.
        latex_document.generate_pdf(clean_tex=True, compiler='xelatex')