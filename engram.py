from fuzzywuzzy import process
import os
import csv

from ChatBot.twitter_api import TwitterAPI


enable_api_search = True

# This is needed to import settings from the parent directory
try:
    import os, sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0, parentdir)
    from settings import TWITTER

    api = TwitterAPI(TWITTER["CONSUMER_KEY"], TWITTER["CONSUMER_SECRET"])
except ImportError:
    print("Unable to import settings, api searches will not be avalable.")
    enable_api_search = False

#print(api.get_list("salviusrobot", "Robots"))
#api.tweet_to_friends("salviusrobot", "Robots", debug=True)

tweet = {}
tweet["id_str"] = "508654764713050112"
#print(api.favorite(tweet))

class Engram():

    def __init__(self, enable_search=True):
        self.enable_search = enable_api_search

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
        max_skipps = 100
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

    def engram(self, input_text):
        """
        Takes a message from a conversation.
        Returns the closest match based on known conversations.
        """

        # Check to make sure that valid text was passed in
        if not input_text.strip():
            return ""

        # Check if a name was mentioned
        if "Salvius" in input_text:
            pass

        possible_choices = {}
        directory = "conversation_engrams"

        for log in os.listdir(directory):
            filename = directory + "/" + log
            f = open(filename, "rb")

            lines = f.read().splitlines()

            # Do not continue if the file is empty
            if os.stat(filename).st_size == 0:
                break

            # Do not continue if lines is empty
            if not lines:
                break

            # Get the closest matching line in the file
            closest, ratio = process.extractOne(input_text, lines)

            index = lines.index(closest)
            user, date, message, next_index = self.get_next_line(lines, index)

            #print(index, next_index, len(lines))

            if next_index and (next_index < len(lines)):
                # Closest ==> Next line
                possible_choices[lines[index]] = lines[next_index]


        if possible_choices.keys():
            closest, ratio = process.extractOne(input_text, possible_choices.keys())
            response = list(csv.reader([possible_choices[closest]]))[0]

        # If the difference ratio is too low, or the choice list is empty, seek a better response
        if ((not possible_choices.keys()) or (ratio < 90)) and self.enable_search:
            print("salvius: ...")

            search = api.get_related_messages(input_text)

            # If results were found
            if len(search) > 0:
                import random
                return random.choice(search)

        user, date, message = response

        return message


    def terminal(self, log=True):
        import datetime

        fmt = "%Y-%m-%d-%H-%M-%S"
        timestamp = datetime.datetime.now().strftime(fmt)
        user_input = ""

        print("Type something to begin")
        while "end program" not in user_input:
            if log:
                logfile = open("conversation_engrams/" + timestamp, "a")

            logtime = datetime.datetime.now().strftime(fmt)

            # raw_input is just input in python3
            user_input = str(raw_input())

            response = self.engram(user_input)
            print(response)

            # Write the conversation to a file
            if log:
                logfile.write("user," + logtime + ",\"" + user_input + "\"\n")
                logfile.write("salvius," + logtime + ",\"" + response + "\"\n")
                logfile.close()

    def talk_with_cleverbot(self, log=True):
        import datetime
        from cleverbot.cleverbot import Cleverbot
        import time

        fmt = "%Y-%m-%d-%H-%M-%S"
        timestamp = datetime.datetime.now().strftime(fmt)
        user_input = "Hi. How are you?"

        cb = Cleverbot()

        print("salvius:", user_input)

        while True:

            if log:
                logfile = open("conversation_engrams/" + timestamp, "a")

            logtime = datetime.datetime.now().strftime(fmt)

            cb_input = cb.ask(user_input)
            cb_input = api.clean(cb_input)
            print("cleverbot:", cb_input)

            user_input = self.engram(cb_input)
            user_input = api.clean(user_input)
            print("salvius:", user_input)

            if log:
                logfile.write("cleverbot," + logtime + ",\"" + cb_input + "\"\n")
                logfile.write("salvius," + logtime + ",\"" + user_input + "\"\n")
                logfile.close()

            time.sleep(1.05)

