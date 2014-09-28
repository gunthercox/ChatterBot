from fuzzywuzzy import process
import os
import csv
import StringIO

from twitter_api import TwitterAPI

# This is needed to import settings from the parent directory
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from settings import TWITTER


api = TwitterAPI(TWITTER["CONSUMER_KEY"], TWITTER["CONSUMER_SECRET"])

#print api.get_list("salviusrobot", "Robots")
#api.tweet_to_friends("salviusrobot", "Robots", debug=True)

tweet = {}
tweet["id_str"] = "508654764713050112"
#print api.favorite(tweet)

def get_next_line(lines, index):
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
    line_data = csv.reader(StringIO.StringIO(line))

    data = list(line_data)
    user, date, message = data[0]

    # Set index to the next line
    #index += 1

    line = lines[index]
    next_line_data = csv.reader(StringIO.StringIO(line))
    next_user, next_date, next_message = list(next_line_data)[0]

    # If the line's user is the same as the current line's user
    while (next_user == user) and (iter_count <= max_skipps):
        index += 1
        next_user, next_date, message, i = get_next_line(lines, index)

    return user, date, message, index

def engram(input_text):
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

    for datafile in os.listdir(directory):
        filename = directory + "/" + datafile
        with open(filename, "r") as f:
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
            user, date, message, next_index = get_next_line(lines, index)

            #print index, next_index, len(lines)

            if next_index and (next_index < len(lines)):
                # Closest ==> Next line
                possible_choices[lines[index]] = lines[next_index]


    if possible_choices.keys():
        closest, ratio = process.extractOne(input_text, possible_choices.keys())
        response = csv.reader(StringIO.StringIO(possible_choices[closest]))

    # If the difference ratio is too low, or the choice list is empty, seek a better response
    if (not possible_choices.keys()) or (ratio < 90):
        print "salvius: ..."

        search = api.get_related_messages(input_text)

        # If results were found
        if len(search) > 0:
            import random
            return random.choice(search)

    temp = list(response)[0]
    user, date, message = temp

    return message


def terminal(log=True):
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

        response = engram(user_input)
        print(response)

        # Write the conversation to a file
        if log:
            logfile.write("user," + logtime + ",\"" + user_input + "\"\n")
            logfile.write("salvius," + logtime + ",\"" + response + "\"\n")
            logfile.close()

def talk_with_cleverbot(log=True):
    import datetime
    from cleverbot.cleverbot import Cleverbot
    import time

    fmt = "%Y-%m-%d-%H-%M-%S"
    timestamp = datetime.datetime.now().strftime(fmt)
    user_input = "Hi. How are you?"

    cb = Cleverbot()

    print "salvius:", user_input

    while True:

        if log:
            logfile = open("conversation_engrams/" + timestamp, "a")

        logtime = datetime.datetime.now().strftime(fmt)

        cb_input = cb.ask(user_input)
        cb_input = api.clean(cb_input)
        print "cleverbot:", cb_input

        user_input = engram(cb_input)
        user_input = api.clean(user_input)
        print "salvius:", user_input

        if log:
            logfile.write("cleverbot," + logtime + ",\"" + cb_input + "\"\n")
            logfile.write("salvius," + logtime + ",\"" + user_input + "\"\n")
            logfile.close()

        time.sleep(1.05)


#talk_with_cleverbot(True)
terminal(False)
