class ChatBot(object):

    def __init__(self, name="bot", logging=True):
        super(ChatBot, self).__init__()

        self.TIMESTAMP = self.timestamp()

        self.name = name
        self.log = logging
        self.log_directory = "conversation_engrams/"

    def timestamp(self, fmt="%Y-%m-%d-%H-%M-%S"):
        """
        Returns a string formatted timestamp of the current time.
        """
        import datetime
        return datetime.datetime.now().strftime(fmt)

    def update_log(self, data):
        import csv

        logfile = open(self.log_directory + self.TIMESTAMP, "a")
        logwriter = csv.writer(logfile, delimiter=",")

        logwriter.writerow([
            data["user"]["name"],
            data["user"]["date"],
            data["user"]["text"]
        ])

        for line in data["bot"]:
            logwriter.writerow([
                line["name"],
                line["date"],
                line["text"]
            ])

        logfile.close()

    def get_response_data(self, user_name, input_text):
        """
        Returns a dictionary containing the following data:
        * user:
            * The name of the user who instigated a response
            * The timestamp at which the user issued their statement
            * The user's statement
        * bot:
            * The name of the chat bot instance
            * The timestamp of the chat bot's response
            * The chat bot's response text
        """
        from chatterbot.algorithms.engram import engram

        # Check if a name was mentioned
        if self.name in input_text:
            pass

        bot = []
        user = {}

        user["name"] = user_name
        user["text"] = input_text
        user["date"] = self.timestamp()

        output = engram(input_text, self.log_directory)

        for out in output:
            out.update_timestamp()
            out.set_name(self.name)
            bot.append(dict(out))

        data = {
            "user": user,
            "bot": bot
        }

        if self.log:
            self.update_log(data)

        return data

    def get_response(self, input_text, user_name="user"):
        """
        Return only the response text from the input
        """
        return self.get_response_data(user_name, input_text)["bot"]


class Terminal(ChatBot):

    def __init__(self):
        super(Terminal, self).__init__()

    def begin(self, user_input="Type something to begin..."):
        import sys

        print(user_input)

        while True:
            try:
                # 'raw_input' is just 'input' in python3
                if sys.version_info[0] < 3:
                    user_input = str(raw_input())
                else:
                    user_input = input()

                # End the session if the exit command is issued
                if "exit()" == user_input:
                    import warnings
                    warnings.warn("'exit()' is deprecated. Use 'ctrl c' or 'ctrl d' to end a session.")
                    break

                bot_input = self.get_response(user_input)
                for line in bot_input:
                    print(line["name"], line["text"])

            except (KeyboardInterrupt, EOFError, SystemExit):
                break


class TalkWithCleverbot(object):

    def __init__(self, log_directory="GitHub/salvius/conversation_engrams/"):
        super(TalkWithCleverbot, self).__init__()
        from chatterbot.cleverbot.cleverbot import Cleverbot

        self.running = True

        self.cleverbot = Cleverbot()
        self.chatbot = ChatBot()
        self.chatbot.log_directory = log_directory

    def begin(self, bot_input="Hi. How are you?"):
        import time
        from chatterbot.apis import clean

        print(self.chatbot.name, bot_input)

        while self.running:
            cb_input = self.cleverbot.ask(bot_input)
            print("cleverbot:", cb_input)
            cb_input = clean(cb_input)

            bot_input = self.chatbot.get_response(cb_input, "cleverbot")
            print(self.chatbot.name, bot_input[0]["text"])
            bot_input = clean(bot_input[0]["text"])

            time.sleep(1.05)
