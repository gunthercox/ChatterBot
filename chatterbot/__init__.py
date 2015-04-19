class ChatBot(object):

    def __init__(self, name, adapter="chatterbot.adapters.jsondb.JsonDatabaseAdapter", database="database.db", logging=True):


        self.name = name
        self.log = logging

        #Adapter = self.import_adapter(adapter)
        #self.database = Adapter(database)

        from jsondb.db import Database
        self.database = Database(database)

        self.last_statements = []

    def import_adapter(self, adapter):
        module_parts = module_path.split(".")
        module_path = ".".join(module_parts[:-1])
        module = importlib.import_module(module_path)

        return getattr(module, module_parts[-1])

    def get_last_statement(self):
        """
        Returns the last statement that was issued to the chat bot.
        """

        # If there was no last statements, return None
        if len(self.last_statements) == 0:
            return None

        return self.last_statements[-1]

    def timestamp(self, fmt="%Y-%m-%d-%H-%M-%S"):
        """
        Returns a string formatted timestamp of the current time.
        """
        import datetime
        return datetime.datetime.now().strftime(fmt)

    def update_occurrence_count(self, key):
        """
        Increment the occurrence count for a given statement in the database.
        The key parameter is a statement that exists in the database.
        """
        database_values = self.database[key]

        # If an occurence count does not exist then initialize it
        if not "occurrence" in database_values:
            database_values["occurrence"] = 0

        database_values["occurrence"] += 1

        # Save the changes to the database
        self.database[key] = database_values

    def update_response_list(self, key, previous_statement):
        """
        Update the list of statements that a know statement has responded to.
        """

        database_values = self.database[key]

        if not "in_response_to" in database_values:
            database_values["in_response_to"] = []

        # TODO:
        '''
        In the future, the in_response_to list should become a dictionary
        of the response statements with a value of the number of times each statement
        has occured. This should make selecting likely responces more accurate.
        '''

        if previous_statement:
            # Check to make sure that the statement does not already exist
            if not previous_statement in database_values["in_response_to"]:
                database_values["in_response_to"].append(previous_statement)

        self.database[key] = database_values

    def train(self, conversation):
        for i in range(0, len(conversation)):

            statement = conversation[i]

            # Create an entry if the statement does not exist in the database
            if not statement in self.database:
                self.database[statement] = {}

            database_values = self.database[statement]

            database_values["date"] = self.timestamp()

            self.database[statement] = database_values

            self.update_occurrence_count(statement)
            self.update_response_list(statement, self.get_last_statement())

            self.last_statements.append(statement)

    def update_log(self, data):

        statement = list(data.keys())[0]
        values = data[statement]

        # Create the statement if it doesn't exist in the database
        if not statement in self.database:
            self.database[statement] = {}

        # Get the existing values from the database
        database_values = self.database[statement]

        database_values["name"] = values["name"]
        database_values["date"] = values["date"]

        # Update the database with the changes
        self.database[statement] = database_values

        self.update_occurrence_count(statement)
        self.update_response_list(statement, self.get_last_statement())

    # TODO, change user_name and input_text into a single dict
    def get_response_data(self, user_name, input_text):
        """
        Returns a dictionary containing the following data:
        * user: The user's statement meta data
        * bot: The bot's statement meta data
        """
        from chatterbot.algorithms.engram import Engram
        from chatterbot.matching import closest

        # Use the closest known matching statement
        closest_statement = closest(input_text, self.database)
        response_statement = Engram(closest_statement, self.database)
        self.last_statements.append(response_statement.get())

        statement_text = list(self.get_last_statement().keys())[0]

        user = {
            input_text: {
                "name": user_name,
                "date": self.timestamp()
            }
        }

        # Update the database before selecting a response if logging is enabled
        if self.log:
            self.update_log(user)

        return {user_name: user, "bot": statement_text}

    def get_response(self, input_text, user_name="user"):
        """
        Return only the bot's response text from the input
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

                bot_input = self.get_response(user_input)
                print(bot_input)

            except (KeyboardInterrupt, EOFError, SystemExit):
                break


class TalkWithCleverbot(ChatBot):

    def __init__(self):
        super(TalkWithCleverbot, self).__init__()
        from chatterbot.cleverbot.cleverbot import Cleverbot

        self.running = True
        self.cleverbot = Cleverbot()

    def begin(self, bot_input="Hi. How are you?"):
        import time
        from random import randint 
        from chatterbot.apis import clean

        print(self.name, bot_input)

        while self.running:
            cb_input = self.cleverbot.ask(bot_input)
            print("cleverbot:", cb_input)
            cb_input = clean(cb_input)

            bot_input = self.get_response(cb_input, "cleverbot")
            print(self.name, bot_input)
            bot_input = clean(bot_input)

            # Delay a random number of seconds.
            time.sleep(1.05 + randint(0, 9))


class SocialBot(object):
    """
    Check for online mentions on social media sites.
    The bot will follow the user who mentioned it and
    favorite the post in which the mention was made.
    """

    def __init__(self, **kwargs):
        from chatterbot.apis.twitter import Twitter

        chatbot = ChatBot()

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
