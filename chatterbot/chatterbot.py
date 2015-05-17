class ChatBot(object):

    def __init__(self, name,
            storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
            logic_adapter="chatterbot.adapters.logic.EngramAdapter",
            io_adapter="chatterbot.adapters.io.TerminalAdapter",
            database="database.db", logging=True):

        self.name = name
        self.log = logging

        StorageAdapter = self.import_adapter(storage_adapter)
        self.database = StorageAdapter(database)

        IOAdapter = self.import_adapter(io_adapter)
        self.io = IOAdapter()

        self.recent_statements = []

    def import_adapter(self, adapter):
        import importlib

        module_parts = adapter.split(".")
        module_path = ".".join(module_parts[:-1])
        module = importlib.import_module(module_path)

        return getattr(module, module_parts[-1])

    def get_last_statement(self):
        """
        Returns the last statement that was issued to the chat bot.
        """

        # If there was no last statements, return None
        if len(self.recent_statements) == 0:
            return None

        return self.recent_statements[-1]

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
        database_values = self.database.find(key)
        count = 0

        # If an occurence count exists then initialize it
        if "occurrence" in database_values:
            count = database_values["occurrence"]

        count += 1

        # Save the changes to the database
        self.database.update(key, occurrence=count)

    def update_response_list(self, key, previous_statement):
        """
        Update the list of statements that a know statement has responded to.
        """

        database_values = self.database.find(key)
        responses = []

        if "in_response_to" in database_values:
            responses = database_values["in_response_to"]

        # TODO:
        '''
        In the future, the in_response_to list should become a dictionary
        of the response statements with a value of the number of times each statement
        has occured. This should make selecting likely responces more accurate.
        '''

        if previous_statement:
            # Check to make sure that the statement does not already exist
            if not previous_statement in responses:
                responses.append(previous_statement)

        self.database.update(key, in_response_to=responses)

    def train(self, conversation):
        for statement in conversation:

            database_values = self.database.find(statement)

            # Create an entry if the statement does not exist in the database
            if not database_values:
                self.database.insert(statement, {})

            self.database.update(statement, date=self.timestamp())

            self.update_occurrence_count(statement)
            self.update_response_list(statement, self.get_last_statement())

            self.recent_statements.append(statement)

    def update_log(self, data):
        statement = list(data.keys())[0]
        values = data[statement]

        # Create the statement if it doesn't exist in the database
        if not self.database.find(statement):
            self.database.insert(statement, {})

        # Update the database with the changes
        self.database.update(statement, name=values["name"], date=values["date"])

        self.update_occurrence_count(statement)
        self.update_response_list(statement, self.get_last_statement())

    # TODO, change user_name and input_text into a single dict
    def get_response_data(self, user_name, input_text):
        """
        Returns a dictionary containing the following data:
        * user: The user's statement meta data
        * bot: The bot's statement meta data
        """
        from .algorithms.engram import Engram
        from .matching import closest

        if input_text:
            # Use the closest known matching statement
            closest_statement = closest(input_text, self.database)
        else:
            # If the input is blank, return a random statement
            closest_statement = self.database.get_random()

        response_statement = Engram(closest_statement, self.database)
        self.recent_statements.append(response_statement.get())

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
