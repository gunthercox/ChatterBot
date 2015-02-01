class ChatBot(object):

    def __init__(self, name="bot", logging=True):
        from jsondb.db import Database

        self.name = name
        self.log = logging
        self.log_directory = "database.db"
        self.last_statement = None
        self.database = Database(self.log_directory)

    def timestamp(self, fmt="%Y-%m-%d-%H-%M-%S"):
        """
        Returns a string formatted timestamp of the current time.
        """
        import datetime
        return datetime.datetime.now().strftime(fmt)

    def train(self, conversation):
        for i in range(0, len(conversation)):

            statement = conversation[i]

            # Create an entry if the statement does not exist in the database
            if not statement in self.database:
                self.database[statement] = {}

            database_values = self.database[statement]

            database_values["date"] = self.timestamp()

            if not "occurrence" in database_values:
                database_values["occurrence"] = 0
            database_values["occurrence"] += 1

            if not "in_response_to" in database_values:
                database_values["in_response_to"] = []

            # Add the previous statement for all statements except the first one
            if i > 0:
                # Check to make sure that the statement does not already exist
                if not conversation[i - 1] in database_values["in_response_to"]:
                    database_values["in_response_to"].append(conversation[i - 1])

            self.database[statement] = database_values

    def update_log(self, data):

        key = list(data.keys())[0]
        values = data[key]

        # Create the key if it does not exist in the database
        if not key in self.database:
            self.database[key] = {}

        # Get the existing values from the database
        database_values = self.database[key]

        database_values["name"] = values["name"]
        database_values["date"] = values["date"]

        if not "occurrence" in database_values:
            database_values["occurrence"] = 0
        database_values["occurrence"] += 1

        if not "in_response_to" in database_values:
            database_values["in_response_to"] = []

        # If a previous statement exists
        if self.last_statement:
            statement_text = list(self.last_statement.keys())[0]

            # If the statement is not already in the list
            if not statement_text in database_values["in_response_to"]:
                database_values["in_response_to"].append(statement_text)

        # Update the database with the changes
        self.database[key] = database_values

    # TODO, change user_name and input_text into a single dict
    def get_response_data(self, user_name, input_text):
        """
        Returns a dictionary containing the following data:
        * user: The user's meta data
        * bot: The statement's meta data
        """
        from chatterbot.algorithms.engram import engram

        # Check if a name was mentioned
        if self.name in input_text:
            pass

        bot = {}

        user = {
            input_text: {
                "name": user_name,
                "date": self.timestamp()
            }
        }

        # If logging is enabled, add the user's input to the database before selecting a response.
        if self.log:
            self.update_log(user)

        self.last_statement = engram(input_text, self.log_directory)
        statement_text = list(self.last_statement.keys())[0]

        if self.log:
            values = self.database[input_text]
            if not "in_response_to" in values:
                values["in_response_to"] = []
            if not statement_text in values["in_response_to"]:
                values["in_response_to"].append(statement_text)
                self.database[input_text] = values

        return {"user": user, "bot": self.last_statement}

    def get_response(self, input_text, user_name="user"):
        """
        Return only the response text from the input
        """
        response = self.get_response_data(user_name, input_text)["bot"]

        # Return the text for the statement
        return list(response.keys())[0]


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
                print(bot_input)

            except (KeyboardInterrupt, EOFError, SystemExit):
                break


class TalkWithCleverbot(object):

    def __init__(self, log_directory="conversation_engrams/"):
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


class SocialBot(object):
    """
    Check for online mentions on social media sites.
    The bot will follow the user who mentioned it and
    favorite the post in which the mention was made.
    """

    def __init__(self, log_directory="conversation_engrams/", **kwargs):
        from chatterbot.apis.twitter import Twitter

        chatbot = ChatBot()
        chatbot.log_directory = log_directory

        if "twitter" in kwargs:
            twitter_bot = Twitter(kwargs["twitter"])

            for mention in twitter_bot.get_mentions():

                '''
                Check to see if the post has been favorited
                We will use this as a check for whether or not to respond to it.
                Only respond to unfavorited mentions.
                '''

                if not mention["favorited"]:
                    screen_name = mention["user"]["screen_name"]
                    text = mention["text"]
                    response = chatbot.get_response(text)

                    print(text)
                    print(response)

                    follow(screen_name)
                    favorite(mention["id"])
                    reply(mention["id"], response)
