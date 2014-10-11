from ChatBot.engram import Engram


class ChatBot(Engram):

    def __init__(self, fmt="%Y-%m-%d-%H-%M-%S"):
        self.timestamp = datetime.datetime.now().strftime(fmt)

    def update_log(user_name, bot_name, user_input, bot_input):
        import datetime

        logtime = datetime.datetime.now().strftime(fmt)

        # TODO: use csv writer here.
        logfile = open(self.log_directory + self.timestamp, "a")
        logfile.write(user_name + logtime + ",\"" + user_input + "\"\n")
        logfile.write(bot_name + logtime + ",\"" + bot_input + "\"\n")
        logfile.close()


class Terminal(ChatBot):

    def begin(self, log=True, user_input="Type something to begin..."):

        print(user_input)

        while "end program" not in user_input:

            # raw_input is just input in python3
            user_input = str(raw_input())

            bot_input = self.engram(user_input)
            print(bot_input)

            # Write the conversation to a file
            if log:
                update_log("user", "salvius", user_input, bot_input)

class TalkWithCleverbot(ChatBot):

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
