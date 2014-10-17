from fuzzywuzzy import process
import os
import csv


class Engram(object):

    def __init__(self):
        self.api = None

    def enable_twitter_api(consumer_key, consumer_secret):
        """
        Takes the public key and private key and enables the api.
        """
        from twitter_api import TwitterAPI

        self.api = TwitterAPI(consumer_key, consumer_secret)

    def get_next_line(self, lines, index):
        """
        Returns the response to a known statement.

        If the user name on the next line is the same as
        the one on the current line then the line will be skipped
        until a different user name is found.
        """

        # If the line is the last line in the file
        if (index + 1) >= len(lines):
            return None, None, None, None

        # Maximum number of lines that can be skipped
        max_skipps = 50
        iter_count = 0

        line = lines[index]

        line_data = list(csv.reader([line]))[0]
        user, date, message = line_data

        # Set index to the next line
        #index += 1

        line = lines[index]

        next_line_data = list(csv.reader([line]))[0]
        next_user, next_date, next_message = next_line_data

        # If the line's user is the same as the current line's user
        while (next_user == user) and (iter_count <= max_skipps):
            index += 1
            next_user, next_date, message, i = self.get_next_line(lines, index)

        return user, date, message, index

    def engram(self, text, log_directory):
        """
        Takes a message from a conversation.
        Returns the closest match based on known conversations.
        """

        # Check to make sure that valid text was passed in
        if not text.strip():
            return ""

        possible_choices = {}

        for log in os.listdir(log_directory):
            filename = log_directory + "/" + log
            f = open(filename, "rb")

            lines = f.read().splitlines()

            # Do not continue if the file is empty
            if os.stat(filename).st_size == 0:
                break

            # Do not continue if lines is empty
            if not lines:
                break

            #---------------------------------#
            # Ensure that the input text is a string
            text = str(text)

            # Make sure each line is a string
            i = 0
            for line in lines:
                lines[i] = str(line)
                i += 1
            #---------------------------------#

            # Get the closest matching line in the file
            closest, ratio = process.extractOne(text, lines)

            index = lines.index(closest)
            user, date, message, next_index = self.get_next_line(lines, index)

            if next_index and (next_index < len(lines)):
                # Closest ==> Next line
                possible_choices[lines[index]] = lines[next_index]

        # If the difference ratio is too low or the choice list is empty seek a better response
        if ((not possible_choices.keys()) or (ratio < 90)) and self.api:
            print("...")

            search = api.get_related_messages(text)

            # If results were found
            if len(search) > 0:
                import random
                return random.choice(search)

        if not possible_choices.keys():
            return "Error"

        closest, ratio = process.extractOne(text, list(possible_choices.keys()))
        response = list(csv.reader([possible_choices[closest]]))[0]

        user, date, message = response
        return message

