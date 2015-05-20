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

    def update_occurrence_count(self, data):
        """
        Increment the occurrence count for a given statement.
        """
        if "occurrence" in data:
            return data["occurrence"] + 1

        return 1

    def update_response_list(self, key, previous_statement):
        """
        Update the list of statements that a know statement has responded to.
        """
        responses = []
        values = self.storage.find(key)

        if not values:
            values = {}

        if "in_response_to" in values:
            responses = values["in_response_to"]

        if previous_statement:

            # Check to make sure that the statement does not already exist
            if not previous_statement in responses:
                responses.append(previous_statement)

        self.recent_statements.append(key)
        return responses

    def train(self, conversation):
        for statement in conversation:

            values = self.storage.find(statement)

            # Create an entry if the statement does not exist in the database
            if not values:
                values = self.storage.insert(statement, {})

            count = self.update_occurrence_count(values)
            timestamp = self.timestamp()

            previous_statement = self.get_last_statement()
            response_list = self.update_response_list(statement, previous_statement)

            self.storage.update(statement, date=timestamp, occurrence=count, in_response_to=response_list)

    def update_log(self, data):
        statement = list(data.keys())[0]
        values = data[statement]

        # Create the statement if it doesn't exist in the database
        if not self.storage.find(statement):
            self.storage.insert(statement, {})

        count = self.update_occurrence_count(values)
        username = values["name"]
        timestamp = values["date"]

        previous_statement = self.get_last_statement()
        response_list = self.update_response_list(statement, previous_statement)

        # Update the database with the changes
        data = self.storage.update(statement, name=username, date=timestamp, occurrence=count, in_response_to=response_list)

        #print "YYYY", count, data

    # TODO, change user_name and input_text into a single dict
    def get_response_data(self, user_name, input_text):
        """
        Returns a dictionary containing the meta data for
        the current response.
        """

        if input_text:
            response = self.logic.get(input_text)
        else:
            # If the input is blank, return a random statement
            response = self.storage.get_random()

        user = {
            input_text: {
                "name": user_name,
                "date": self.timestamp()
            }
        }

        self.recent_statements.append(list(response.keys())[0])

        return {
            user_name: user,
            "bot": response
        }

    def get_response(self, input_text, user_name="user"):
        """
        Return the bot's response based on the input.
        """
        response = self.get_response_data(user_name, input_text)

        # Update the database before selecting a response if logging is enabled
        if self.log:
            self.update_log(response[user_name])

        return list(response["bot"].keys())[0]
