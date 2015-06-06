from .controllers import StorageController
from .utils.module_loading import import_module


class ChatBot(object):

    def __init__(self, name,
            storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
            logic_adapter="chatterbot.adapters.logic.ClosestMatchAdapter",
            io_adapter="chatterbot.adapters.io.TerminalAdapter",
            database="database.db", logging=True):

        self.name = name
        self.log = logging

        self.storage = StorageController(storage_adapter, database)

        LogicAdapter = import_module(logic_adapter)
        self.logic = LogicAdapter(self.storage.storage_adapter)

        IOAdapter = import_module(io_adapter)
        self.io = IOAdapter()

    def train(self, conversation):

        if not self.log:
            raise Exception("Logging is disabled. Enable logging to allow training.")

        self.storage.train(conversation)

    def get_response_data(self, data):
        """
        Returns a dictionary containing the meta data for
        the current response.
        """

        if "text" in data:
            match = self.logic.get(data["text"])

            if match:
                response = self.storage.get_most_frequent_response(match)
            else:
                response = self.storage.storage_adapter.get_random()

        else:
            # If the input is blank, return a random statement
            response = self.storage.storage_adapter.get_random()

        statement = list(response.keys())[0]
        values = response[statement]

        previous_statement = self.storage.get_last_statement()
        response_list = self.storage.update_response_list(statement, previous_statement)

        count = self.storage.update_occurrence_count(values)

        name = data["name"]

        values["name"] = name
        values["occurrence"] = count
        values["in_response_to"] = response_list

        self.storage.recent_statements.append(list(response.keys())[0])

        response_data = {
            name: {
                data["text"]: values
            },
            "bot": response
        }

        # Update the database before selecting a response if logging is enabled
        if self.log:
            self.storage.update_log(**response_data[name])

        return response_data

    def get_response(self, input_text, user_name="user"):
        """
        Return the bot's response based on the input.
        """
        response = self.get_response_data({"name":user_name, "text": input_text})

        return list(response["bot"].keys())[0]
