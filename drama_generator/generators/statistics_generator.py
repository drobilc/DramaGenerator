from .generator import Generator
from datetime import datetime
import logging
import string
import collections
import math

from bs4 import BeautifulSoup

class StatisticsGenerator(Generator):
    
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
    
    def generate(self, output_path):
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

        # Write the modified SVG graphics to output file
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(str(html))