from fuzzywuzzy import process
import os
import csv
import StringIO


def get_next_line(lines, index):
    """
    Returns the response to a known statement.

    If the user name on the next line is the same as
    the one on the current line then the line will be skipped
    until a different user name is found.
    """

    # If the line is the last line in the file
    if (index + 1) == len(lines):
        return "default", "0", "\"I'm not sure what to say.\"", 0

    # Maximum number of lines that can be skipped
    max_skipps = 100
    iter_count = 0

    line = lines[index]
    line_data = csv.reader(StringIO.StringIO(line))
    user, date, message = list(line_data)[0]

    # Set index to the next line
    index += 1

    line = lines[index]
    next_line_data = csv.reader(StringIO.StringIO(line))
    next_user, next_date, next_message = list(next_line_data)[0]

    # If the next line's user is the same as the current line's user
    while (next_user == user) and (iter_count <= max_skipps):
        index += 1
        next_user, next_date, message, i = get_next_line(lines, index)

    return user, date, message, index

def engram(input_text):
    """
    Takes a message from a conversation.
    Returns the closest match based on known conversations.
    """

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

            # Get the closest matching line in the file
            closest, ratio = process.extractOne(input_text, lines)
            index = lines.index(closest)
            user, date, message, next_index = get_next_line(lines, index)

            # Closest ==> Next line
            possible_choices[lines[index]] = lines[next_index]

    closest, ratio = process.extractOne(input_text, possible_choices.keys())
    response = csv.reader(StringIO.StringIO(possible_choices[closest]))

    # If the difference ration is too low, seek a better response
    #print ratio

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
    import cleverbot
    import time

    fmt = "%Y-%m-%d-%H-%M-%S"
    timestamp = datetime.datetime.now().strftime(fmt)
    user_input = "Hi. How are you?"

    cb = cleverbot.Cleverbot()

    print user_input

    while True:

        if log:
            logfile = open("conversation_engrams/" + timestamp, "a")

        logtime = datetime.datetime.now().strftime(fmt)

        try:
            cb_input = cb.ask(user_input)
            user_input = engram(cb_input)

            print(cb_input)
            print(user_input)

            if log:
                logfile.write("cleverbot," + logtime + ",\"" + cb_input + "\"\n")
                logfile.write("salvius," + logtime + ",\"" + user_input + "\"\n")
                logfile.close()

        except(IndexError):
            print("IndexError detected")

        time.sleep(0.45)


#talk_with_cleverbot(True)
terminal(False)
