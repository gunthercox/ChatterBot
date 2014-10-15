from chatterbot.engram import Engram
import datetime


class ChatBot(Engram):

    def __init__(self, fmt="%Y-%m-%d-%H-%M-%S"):
        super(ChatBot, self).__init__()

        self.date_fmt=fmt
        self.timestamp = datetime.datetime.now().strftime(self.date_fmt)

    def update_log(self, user_name, bot_name, user_input, bot_input):
        import datetime
        import csv

        logtime = datetime.datetime.now().strftime(self.date_fmt)
        logfile = open(self.log_directory + self.timestamp, "a")

        logwriter = csv.writer(logfile, delimiter=",")
        logwriter.writerow([user_name, logtime, user_input])
        logwriter.writerow([bot_name, logtime, bot_input])

        logfile.close()


class Terminal(ChatBot):

    def __init__(self):
        super(Terminal, self).__init__()

    def begin(self, log=True, user_input="Type something to begin..."):
        import sys

        print(user_input)

        while "exit()" not in user_input:

            # raw_input is just input in python3
            if sys.version_info[0] < 3:
                user_input = str(raw_input())
            else:
                user_input = input()

            bot_input = self.engram(user_input)
            print(bot_input)

            # Write the conversation to a file
            if log:
                self.update_log("user", "salvius", user_input, bot_input)


class TalkWithCleverbot(ChatBot):

    def __init__(self):
        super(TalkWithCleverbot, self).__init__()

    def begin(self, log=True, bot_input="Hi. How are you?"):
        from cleverbot.cleverbot import Cleverbot
        import time

        cb = Cleverbot()

        print("salvius:", bot_input)

        while True:
            cb_input = cb.ask(bot_input)
            cb_input = api.clean(cb_input)
            print("cleverbot:", cb_input)

            bot_input = self.engram(cb_input)
            bot_input = api.clean(bot_input)
            print("salvius:", bot_input)

            if log:
                update_log("cleverbot", "salvius", cb_input, bot_input)

            time.sleep(1.05)
