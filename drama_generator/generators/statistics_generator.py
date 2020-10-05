from .generator import Generator
from datetime import datetime
import logging
import string
import collections

import io

import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc

from bs4 import BeautifulSoup

class StatisticsGenerator(Generator):

    PRIMARY_COLOR = '#28b998'
    
    def _setup_argument_parser(self, argument_parser):
        argument_parser.add_argument(
            '--stopwords',
            dest='stopwords',
            help='path to file containing a list of stopwords, each in its own line',
        )
    
    def _most_used_words(self, messages):
        messages_list = [message.message for message in messages]
        messages_text = ' '.join(messages_list)

        # Split all text into words by whitespace
        words_dirty = messages_text.split()

        # Remove punctuation from words using the translate function
        table = messages_text.maketrans('', '', string.punctuation)
        words = [word.translate(table) for word in words_dirty]

        # Lowercase all words in our words list
        words = map(lambda word: word.lower(), words)
        # Remove empty strings from our words list
        words = filter(lambda word: len(word) > 0, words)

        # If user has supplied us with a stopwords list, remove those words from
        # our wordlist
        if self.arguments.stopwords is not None:
            stopwords = []
            with open(self.arguments.stopwords, 'r', encoding='utf-8') as stopwords_file:
                stopwords = stopwords_file.read().splitlines()
            
            words = filter(lambda word: word not in stopwords, words)

        counter = collections.Counter()
        for word in words:
            counter[word] += 1
        
        return counter

    def _messages_by_day(self, messages):
        days = {}
        for message in messages:
            message_date = message.date.date()
            if message_date not in days:
                days[message_date] = []
            days[message_date].append(message)
        return days
    
    def _messages_by_sender(self, messages):
        groups = {}
        for message in messages:
            if message.sender not in groups:
                groups[message.sender] = []
            groups[message.sender].append(message)
        return groups
    
    def _generate_fun_facts(self, html):
        messages_by_date = self._messages_by_day(self.messages)

        # First, find all relevant fact elements in our HTML
        longest_message_element = html.find('div', { 'id': 'longest-message' })
        one_word_replies_element = html.find('div', { 'id': 'one-word-replies' })
        dirty_emojis_element = html.find('div', { 'id': 'dirty-emojis' })
        total_words_element = html.find('div', { 'id': 'total-words' })
        bibles_written_element = html.find('div', { 'id': 'bibles-written' })
        average_messages_per_day_element = html.find('div', { 'id': 'average-messages-per-day' })
        longest_monologue_element = html.find('div', { 'id': 'longest-monologue' })

        # Set the average messages per day fun fact
        average_messages_per_day = int(len(self.messages) / len(messages_by_date.keys()))
        average_messages_per_day_element.string.replace_with('{} messages'.format(average_messages_per_day))

        longest_message = 0
        one_word_replies = 0
        total_words = 0
        total_characters = 0
        dirty_emojis = 0
        longest_monologue = 0
        current_sender, current_messages = None, 0
        for message in self.messages:
            if message.sender != current_sender:
                longest_monologue = max(longest_monologue, current_messages)
                current_messages = 0
                current_sender = message.sender
            else:
                current_messages += 1

            longest_message = max(longest_message, len(message.message))
            total_characters += len(message.message)

            # TODO: Move dirty emojis into class variable containing all
            # possible dirty emojis
            dirty_emojis += message.message.count(u'🍆') + message.message.count(u'🍑')

            words = message.message.split()
            if len(words) == 1:
                one_word_replies += 1
            
            total_words += len(words)

        longest_message_element.string.replace_with('{} characters'.format(longest_message))
        one_word_replies_element.string.replace_with('{} messages'.format(one_word_replies))
        total_words_element.string.replace_with('{} words'.format(total_words))
        dirty_emojis_element.string.replace_with('{} emojis'.format(dirty_emojis))
        longest_monologue_element.string.replace_with('{} messages'.format(longest_monologue))

        BIBLE_CHARACTERS = 3116480
        bibles_written = total_characters / BIBLE_CHARACTERS
        bibles_written_element.string.replace_with('{} bibles'.format(round(bibles_written, 3)))
    
    def _get_default_plot_styling(self):
        figure, axes = plt.subplots()

        plt.yticks(fontname = "Montserrat")
        plt.xticks(fontname = "Montserrat")

        axes.tick_params(axis='x', colors=StatisticsGenerator.PRIMARY_COLOR)
        axes.tick_params(axis='y', colors=StatisticsGenerator.PRIMARY_COLOR)

        for child in axes.get_children():
            if isinstance(child, matplotlib.spines.Spine):
                child.set_color((0, 0, 0, 0))

        return figure, axes
    
    def _plot_to_svg(self, plt):
         # Construct a SVG file, but don't write it to disk
        in_memory_file = io.BytesIO()
        plt.savefig(in_memory_file, format='svg', transparent=True)
        svg = in_memory_file.getvalue().decode('utf-8')

        svg_parsed = BeautifulSoup(svg, 'lxml')
        return svg_parsed

    def _generate_contributions_graph(self, html):
        messages_by_sender = self._messages_by_sender(self.messages)

        # Get a list of people and number of messages that each one of them sent
        people = list(messages_by_sender.keys())
        values = list(map(len, messages_by_sender.values()))

        # TODO: Try using [plotly](https://plotly.com/) library

        # Plot char using matplotlib library
        figure, axes = self._get_default_plot_styling()
        plt.tight_layout()

        y_positions = list(range(len(people)))

        # Currently using matplotlib
        # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.barh.html#matplotlib.axes.Axes.barh
        axes.barh(
            y_positions,
            values,
            height=0.3,
            color=StatisticsGenerator.PRIMARY_COLOR
        )
        axes.set_yticks(y_positions)
        axes.set_yticklabels(people)
        axes.invert_yaxis()
        axes.invert_xaxis()
        
        svg = self._plot_to_svg(plt)

        # Export graph as SVG and insert it into our document
        contribution_graph_container = total_messages_element = html.find('div', { 'id': 'contributions-graph' })
        contribution_graph_container.append(svg)

    def generate(self, output_path):
        if len(self.messages) <= 0:
            raise Exception('There are no messages')
        
        messages_by_sender = self._messages_by_sender(self.messages)

        # Total number of messages
        total_messages = len(self.messages)

        # Number of messages that contain images
        messages_with_images = filter(lambda message: len(message.images) > 0, self.messages)
        total_images = len(list(messages_with_images))

        # Total chat time
        total_chat_time = '2m 7d'

        with open('drama_generator/generators/templates/statistics_template.html', 'r', encoding='utf-8') as template_file:
            template = template_file.read()
        
        html = BeautifulSoup(template, 'html.parser')

        # Write total number of messages to HTML document
        total_messages_element = html.find('div', { 'id': 'total-messages' })
        total_messages_element.string.replace_with('{}'.format(total_messages))

        # Write total number of images to SVG document
        total_images_element = html.find('div', { 'id': 'total-images' })
        total_images_element.string.replace_with('{}'.format(total_images))

        # Generate fun facts for HTML document
        self._generate_fun_facts(html)

        self._generate_contributions_graph(html)

        # Write the modified SVG graphics to output file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(str(html))