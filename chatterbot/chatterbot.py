class ChatBot(object):

    def __init__(self, name,
            storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
            logic_adapter="chatterbot.adapters.logic.EngramAdapter",
            io_adapter="chatterbot.adapters.io.TerminalAdapter",
            database="database.db", logging=True):

        self.name = name
        self.log = logging

        StorageAdapter = self.import_adapter(storage_adapter)
        self.storage = StorageAdapter(database)

        LogicAdapter = self.import_adapter(logic_adapter)
        self.logic = LogicAdapter(self.storage)

        IOAdapter = self.import_adapter(io_adapter)
        self.io = IOAdapter()

        self.recent_statements = []

    def import_adapter(self, adapter):
        import importlib

        module_parts = adapter.split(".")
        module_path = ".".join(module_parts[:-1])
        module = importlib.import_module(module_path)

        return getattr(module, module_parts[-1])

    def timestamp(self, fmt="%Y-%m-%d-%H-%M-%S"):
        """
        Returns a string formatted timestamp of the current time.
        """
        import datetime
        return datetime.datetime.now().strftime(fmt)

    def get_last_statement(self):
        """
        Returns the last statement that was issued to the chat bot.
        If there was no last statement then return None.
        """
        if len(self.recent_statements) == 0:
            return None

        return self.recent_statements[-1]

    def update_occurrence_count(self, key):
        """
        Increment the occurrence count for a given statement in the database.
        The key parameter is a statement that exists in the database.
        """
        database_values = self.storage.find(key)
        count = 0

        # If an occurence count exists then initialize it
        if "occurrence" in database_values:
            count = database_values["occurrence"]

        count += 1

        # Save the changes to the database
        self.storage.update(key, occurrence=count)

    def update_response_list(self, key):
        """
        Update the list of statements that a know statement has responded to.
        """

        # TODO:
        '''
        In the future, the in_response_to list should become a dictionary
        of the response statements with a value of the number of times each statement
        has occured. This should make selecting likely responces more accurate.
        '''

        previous_statement = self.get_last_statement()

        database_values = self.storage.find(key)
        responses = []

        if "in_response_to" in database_values:
            responses = database_values["in_response_to"]

        if previous_statement:
            statement = list(previous_statement.keys())[0]

            # Check to make sure that the statement does not already exist
            if not previous_statement in responses:
                responses.append(previous_statement)

        self.storage.update(key, in_response_to=responses)

    def train(self, conversation):
        for statement in conversation:

            database_values = self.storage.find(statement)

            # Create an entry if the statement does not exist in the database
            if not database_values:
                self.storage.insert(statement, {})

            self.update_occurrence_count(statement)
            self.update_response_list(statement)

            data = self.storage.update(statement, date=self.timestamp())
            self.recent_statements.append(data)

    def update_log(self, data):
        statement = list(data.keys())[0]

        values = data[statement]

        # Create the statement if it doesn't exist in the database
        if not self.storage.find(statement):
            self.storage.insert(statement, {})

        self.update_occurrence_count(statement)

        # Update the database with the changes
        self.storage.update(statement, name=values["name"], date=values["date"])

    # TODO, change user_name and input_text into a single dict
    def get_response_data(self, user_name, input_text):
        """
        Returns a dictionary containing the following data:
        * user: The user's statement meta data
        * bot: The bot's statement meta data
        """

        if input_text:
            response_statement = self.logic.get(input_text)
        else:
            # If the input is blank, return a random statement
            response_statement = self.storage.get_random()

        self.recent_statements.append(response_statement)

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
        Return the bot's response based on the input.
        """
        return self.io.get_response(self, input_text, user_name)
