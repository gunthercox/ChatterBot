class ChatBot(object):

    def __init__(self, algorithm=None, log=True):
        from pymongo import MongoClient
        from chatterbot.algorithms.engram import engram

        if not algorithm:
            algorithm = engram

        self.response_algorithm = algorithm
        self.logging = log
        self.connection = MongoClient("localhost", 27017)
        self.database = self.connection["chatterbot"]

        self.profile_id = None
        self.speaker_profile_id = None

        self.profile(name="Chat Bot")
        self.current_speaker(name="User Name")

    def profile(self, **kwargs):
        """
        Uses given data to find an existing profile for the chat bot.
        Assigns that profile id to the chat bot for later reference.
        If no arguments are given, the current profile object will be returned.
        """
        people = self.database.people

        if "name" in kwargs:
            profile = people.find_one({"name": kwargs["name"]})
            if profile:
                self.profile_id = profile["_id"]
            else:
                profile_id = people.insert({
                    "name": kwargs["name"],
                    "statements": []
                })
                self.profile_id = profile_id

        if "id" in kwargs:
            self.profile_id = kwargs["id"]

        return people.find_one({"id": self.profile_id})

    def current_speaker(self, **kwargs):
        """
        Sets the name of the person speaking to the chat bot.
        """
        people = self.database.people

        if "name" in kwargs:
            profile = people.find_one({"name": kwargs["name"]})
            if profile:
                self.speaker_profile_id = profile["_id"]
            else:
                profile_id = people.insert({
                    "name": kwargs["name"],
                    "statements": []
                })
                self.speaker_profile_id = profile_id

        if "id" in kwargs:
            self.speaker_profile_id = kwargs["id"]

        return people.find_one({"id": self.speaker_profile_id})

    def get_latest_statement(self):
        """
        Returns the latest statement object that exists in the database.
        This is used to keep track of what needs to be marked as a response.
        """
        return self.database.statements.find().sort("last_accessed")[0]

    def response(self, text):
        """
        Takes text input and a response algorithm object
        as parameters.
        Returns a dictionary containing the data for the
        input statement and resulting response.
        """
        import datetime

        people = self.database.people
        statements = self.database.statements

        output_statement = self.response_algorithm(self, text)

        '''
        If logging is enabled, increment the
        occurance count for the input text.
        Create a new entry if needed.
        '''
        if self.logging:
            statements.update(
                {"text": text},
                {
                    "$inc": {"occurrences": 1},
                    "$set": {"text": text, "last_accessed": datetime.datetime.now()},
                    "$addToSet": { "in_response_to": self.get_latest_statement()["_id"]}
                },
                upsert=True
            )

        input_statement = statements.find_one({"text": text})

        # Update the count of the statement's occurrences
        statements.update(
            {"_id": output_statement["_id"]},
            {
                "$inc": {"occurrences": 1},
                "$set": {"last_accessed": datetime.datetime.now()},
                "$addToSet": {"in_response_to": input_statement["_id"]}
            },
            upsert=True
        )

        return output_statement

    def train(self, conversation):
        """
        Train the chatterbot by loading sample conversations.
        """
        people = self.database.people
        statements = self.database.statements

        previous_statement_id = None

        for statement in conversation:
            user, text = statement

            if previous_statement_id:
                statements.update(
                    {"text": text},
                    {"$inc": {"occurrences": 1},
                    "$addToSet": {"in_response_to": previous_statement_id}},
                    upsert=True
                )
            else:
                statements.update(
                    {"text": text},
                    {"$inc": {"occurrences": 1}},
                    upsert=True
                )

            input_statement = statements.find_one({"text": text})
            previous_statement_id = input_statement["_id"]

            people.update(
                {"name": user},
                {"$addToSet": {"statements": input_statement["_id"]}},
                upsert=True
            )

            input_user = statements.find_one({"text": text})


class Terminal(ChatBot):

    def __init__(self, algorithm, log=True):
        super(Terminal, self).__init__(algorithm, log=True)

    def begin(self, user_input=None):
        import sys

        if not user_input:
            user_input = self.get_latest_statement()["text"]

        # If there is no latest statement, display a prompt
        if not user_input:
            user_input = "Type something to begin..."

        print(user_input)

        while True:
            try:
                # 'raw_input' is just 'input' in python3
                if sys.version_info[0] < 3:
                    user_input = str(raw_input())
                else:
                    user_input = input()

                bot_response = self.response(user_input)
                print(bot_response["text"])

            except (KeyboardInterrupt, EOFError, SystemExit):
                break

        # close the connection to MongoDB
        self.connection.close()


class TalkWithCleverbot(ChatBot):

    def __init__(self, algorithm, log=True):
        super(TalkWithCleverbot, self).__init__(algorithm, log=True)
        from chatterbot.cleverbot.cleverbot import Cleverbot

        self.cleverbot = Cleverbot()

    def begin(self, bot_input="Hi. How are you?"):
        import time
        from chatterbot.apis import clean

        print(bot_input)

        while True:
            try:
                cb_input = self.cleverbot.ask(bot_input)
                #cb_input = clean(cb_input)
                print("cleverbot: ", cb_input)

                bot_input = self.response(cb_input)["text"]
                #bot_input = clean(bot_input)
                print("chatterbot:", str(bot_input))

                time.sleep(1.55)

            except (KeyboardInterrupt, EOFError, SystemExit):
                break

        # close the connection to MongoDB
        self.connection.close()


class SocialBot(ChatBot):
    """
    Check for online mentions on social media sites.
    The bot will follow the user who mentioned it and
    favorite the post in which the mention was made.
    """

    def __init__(self, **kwargs):
        super(SocialBot, self).__init__()

        from chatterbot.apis.twitter import Twitter

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
                    response = self.get_response(text)

                    print(text)
                    print(response)

                    follow(screen_name)
                    favorite(mention["id"])
                    reply(mention["id"], response)
