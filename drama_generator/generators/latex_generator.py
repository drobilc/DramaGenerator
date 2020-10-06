from .generator import Generator
from pylatex import Document, Section, Subsection, Command, NewLine, PageStyle, Package
from pylatex.utils import italic, NoEscape, bold, escape_latex

from datetime import datetime

class LatexGenerator(Generator):
    
    def _setup_argument_parser(self, argument_parser):
        # Add arguments to argument parser
        argument_parser.add_argument('--no-acts',
            dest='no_acts',
            action='store_true',
            help='turn off grouping of generated scenes into acts'
        )
        argument_parser.add_argument('--no-scenes',
            dest='no_scenes',
            action='store_true',
            help='turn off grouping of messages into scenes'
        )
        argument_parser.add_argument('--new-scene-time',
            dest='new_scene_time',
            type=float,
            help='minimal time in hours that has to pass between two consecutive messages so that one scene ends and another one starts',
            default=8
        )
    
    def _generate_scene_list(self, messages, silence_length):
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
        """Create a list of scenes in the same act"""
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
    
    def authors(self):
        authors = set([])
        for message in self.messages:
            authors.add(message.sender)
        return list(authors)
    
    def _construct_latex_document(self, output_path):
        # Create an output document
        latex_document = Document(output_path, fontenc=None)

        # TODO: set fixed path to drama.cls
        # Use custom document class - drama.cls
        latex_document.documentclass = Command(
            'documentclass',
            arguments=['drama']
        )

        return latex_document
    
    def _construct_title_page(self):
        authors = ', '.join(self.authors())
        return [
            Command('TitlePage', [self.title, authors])
        ]
    
    def _construct_table_of_contents(self):
        return []
    
    def _generate_latex_for_act(self, act):
        act_latex = []

        act_date = act['date'].strftime("%B %Y")
        act_latex.append(Command('Act', arguments=[act_date]))

        for scene in act['scenes']:
            act_latex.extend(self._generate_latex_for_scene(scene))
        
        return act_latex
    
    def _generate_latex_for_scene(self, scene):
        scene_latex = []

        scene_latex.append(Command('Scene'))
        for message in scene:
            scene_latex.extend(self._generate_latex_for_message(message))

        return scene_latex

    def _generate_latex_for_message(self, message):
        """ Convert message objects into strings to be written in LaTeX file """
        return [
            Command('Line', arguments=[message.sender, message.message])
        ]

    def generate(self, output_path):
        """Assemble the LaTeX file"""
        # Create a new latex document
        latex_document = self._construct_latex_document(output_path)
        
        # Add a title page
        latex_document.extend(self._construct_title_page())

        # Add a list of chapters
        latex_document.extend(self._construct_table_of_contents())

        # If the --no-scenes command line argument is received, skip scene
        # generation and only write messages in the document. Also skip act 
        # generation since we have no scenes to be grouped into acts.
        # Otherwise, group messsages into scenes and the write them to document.
        if not self.arguments.no_scenes:
            scenes = self._generate_scene_list(self.messages, self.arguments.new_scene_time)
            
            # If --no-scenes aplies, we do not create acts

            # If the --no-acts command line argument is received, skip act
            # generation and only write scenes in the document. Otherwise, group
            # scenes into acts and the write them to document.
            if not self.arguments.no_acts:
                acts = self._generate_act_list(scenes)
                for act in acts:
                    latex_document.extend(self._generate_latex_for_act(act))
            else:
                for scene in scenes:
                    latex_document.extend(self._generate_latex_for_scene(scene))
        else:
            for message in self.messages:
                latex_document.extend(self._generate_latex_for_message(message))

        # Compile latex document
        latex_document.generate_pdf(clean_tex=True, compiler='xelatex')

class PlariLatexGenerator(LatexGenerator):

    def _construct_latex_document(self, output_path):
        # Create an output document
        latex_document = Document(output_path, fontenc=None)

        # Use plari document class
        latex_document.documentclass = Command(
            'documentclass',
            arguments=['plari']
        )

        return latex_document
    
    def _construct_title_page(self):
        authors = '\\\\ '.join([escape_latex(a) for a in self.authors()])
        return [
            Command('title', [self.title]),
            NoEscape('\\author{{ \\textbf{{Authors}} \\\\ {} }}'.format(authors)),
            Command('maketitle'),
        ]
    
    def _generate_latex_for_act(self, act):
        act_latex = []

        act_date = act['date'].strftime("%B %Y")
        act_latex.append(NoEscape('\\newact{{ {} }}\n\n'.format(escape_latex(act_date))))

        for scene in act['scenes']:
            act_latex.extend(self._generate_latex_for_scene(scene))
        
        return act_latex

    def _generate_latex_for_scene(self, scene):
        scene_latex = []

        scene_latex.append(NoEscape('\\newscene\n\n'))
        for message in scene:
            scene_latex.extend(self._generate_latex_for_message(message))

        return scene_latex

    def _generate_latex_for_message(self, message):
        return [
            NoEscape('\\repl{{ {} }} {}\n\n'.format(escape_latex(message.sender), escape_latex(message.message))),
        ]