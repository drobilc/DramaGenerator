from .generator import Generator
from datetime import datetime
import logging
import string
import collections

from bs4 import BeautifulSoup

import plotly.graph_objects as go
import plotly

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

    def _get_default_plot_theme(self):
        layout = plotly.graph_objects.Layout(
            font={'family': 'Montserrat', 'color': 'white'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            colorscale={
                'sequential': [[0.0, 'rgba(0, 0, 0, 0)'], [1.0, '#28b998']],
                'diverging': [[0.0, 'rgba(0, 0, 0, 0)'], [1.0, '#28b998']],
                'sequentialminus': [[0.0, 'rgba(0, 0, 0, 0)'], [1.0, '#28b998']],
            },
            colorway=['#28b998'],
            yaxis={
                'gridcolor': StatisticsGenerator.PRIMARY_COLOR,
                'showgrid': False
            },
            xaxis={
                'gridcolor': StatisticsGenerator.PRIMARY_COLOR,
                'showgrid': False
            }
        )
        return plotly.graph_objects.layout.Template(
            layout=layout
        )

    def _generate_contributions_graph(self, html):
        messages_by_sender = self._messages_by_sender(self.messages)

        # Get a list of people and number of messages that each one of them sent
        people = list(messages_by_sender.keys())
        values = list(map(len, messages_by_sender.values()))

        figure = go.Figure()
        figure.update_layout(template=self._get_default_plot_theme())
        
        figure.add_traces(go.Bar(
            x=values, y=people,
            text=values, textposition='auto',
            marker_color=StatisticsGenerator.PRIMARY_COLOR,
            orientation='h'
        ))

        generated_plot_html = plotly.offline.plot(figure, include_plotlyjs=False, output_type='div')
        plot_html = BeautifulSoup(generated_plot_html, 'html.parser')

        # Export graph as SVG and insert it into our document
        contribution_graph_container = total_messages_element = html.find('div', { 'id': 'contributions-graph' })
        contribution_graph_container.append(plot_html)
    
    def _generate_number_of_messages_per_day_graph(self, html):
        messages_by_sender = self._messages_by_sender(self.messages)

        figure = go.Figure()
        figure.update_layout(template=self._get_default_plot_theme())

        for sender, messages in messages_by_sender.items():
            messages_by_day = self._messages_by_day(messages)
            days = list(messages_by_day.keys())
            values = list(map(len, messages_by_day.values()))

            figure.add_traces(
                go.Bar(
                    name=sender,
                    x=days, y=values,
                    # marker_color=StatisticsGenerator.PRIMARY_COLOR
                )
            )
        
        figure.update_layout(barmode='stack')

        generated_plot_html = plotly.offline.plot(figure, include_plotlyjs=False, output_type='div')
        plot_html = BeautifulSoup(generated_plot_html, 'html.parser')

        # Export graph as SVG and insert it into our document
        contribution_graph_container = total_messages_element = html.find('div', { 'id': 'number-of-messages-per-day-graph' })
        contribution_graph_container.append(plot_html)
    
    def _generate_messages_heatmap(self, html):
        heatmap_data = [[0 for hour in range(24)] for day in range(7)]
        
        for message in self.messages:
            day = message.date.weekday()
            hour = message.date.hour
            heatmap_data[day][hour] += 1

        figure = go.Figure()
        figure.update_layout(template=self._get_default_plot_theme())
        
        figure.add_traces(go.Heatmap(
            x=['{}h'.format(i) for i in range(24)],
            y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            z=heatmap_data,
            colorscale=[[0.0, '#2b2b41'], [1.0, '#6affdc']]
        ))

        generated_plot_html = plotly.offline.plot(figure, include_plotlyjs=False, output_type='div')
        plot_html = BeautifulSoup(generated_plot_html, 'html.parser')

        # Export graph as SVG and insert it into our document
        message_heatmap_container = total_messages_element = html.find('div', { 'id': 'message-heatmap' })
        message_heatmap_container.append(plot_html)

    def generate(self, output_path):
        if len(self.messages) <= 0:
            raise Exception('There are no messages')

        with open('drama_generator/generators/templates/statistics_template.html', 'r', encoding='utf-8') as template_file:
            template = template_file.read()
        
        html = BeautifulSoup(template, 'html.parser')

        first_message, last_message = self.messages[0], self.messages[-1]
        first_message_date = first_message.date.strftime('%d %B %Y')
        last_message_date = last_message.date.strftime('%d %B %Y')
        chat_date_string = '{} - {}'.format(first_message_date, last_message_date)
        date_range_element = html.find('div', { 'id': 'date-range' })
        date_range_element.string.replace_with('{}'.format(chat_date_string))

        # Total number of messages
        total_messages = len(self.messages)

        # Number of messages that contain images
        messages_with_images = filter(lambda message: len(message.images) > 0, self.messages)
        total_images = len(list(messages_with_images))

        # Total chat time
        total_chat_time = '2m 7d'

        # Write total number of messages to HTML document
        total_messages_element = html.find('div', { 'id': 'total-messages' })
        total_messages_element.string.replace_with('{}'.format(total_messages))

        # Write total number of images to SVG document
        total_images_element = html.find('div', { 'id': 'total-images' })
        total_images_element.string.replace_with('{}'.format(total_images))

        # Generate fun facts for HTML document
        self._generate_fun_facts(html)

        self._generate_contributions_graph(html)

        self._generate_number_of_messages_per_day_graph(html)

        self._generate_messages_heatmap(html)

        # Write the modified SVG graphics to output file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(str(html))