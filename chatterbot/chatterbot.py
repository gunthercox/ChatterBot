from .controllers import StorageController
from .utils.module_loading import import_module


class ChatBot(object):

    def __init__(self, name, **kwargs):

        storage_adapter = kwargs.get("storage_adapter",
            "chatterbot.adapters.storage.JsonDatabaseAdapter"
        )

        logic_adapter = kwargs.get("logic_adapter",
            "chatterbot.adapters.logic.ClosestMatchAdapter"
        )

        io_adapter = kwargs.get("io_adapter",
            "chatterbot.adapters.io.TerminalAdapter"
        )

        database = kwargs.get("database", "database.db")

        self.name = name
        self.log = kwargs.get("logging", True)

        self.storage = StorageController(storage_adapter, database)

        LogicAdapter = import_module(logic_adapter)
        self.logic = LogicAdapter()

        IOAdapter = import_module(io_adapter)
        self.io = IOAdapter()

    def train(self, conversation):

        if not self.log:
            raise Exception("Logging is disabled. Enable logging to allow training.")

        for statement in conversation:
            self.storage.train(statement)

    def get_response_data(self, data):
        """
        Returns a dictionary containing the meta data for
        the current response.
        """

        if "text" in data:
            text_of_all_statements = self.storage.list_statements()

            match = self.logic.get(data["text"], text_of_all_statements)

            if match:
                response = self.storage.get_most_frequent_response(match)
            else:
                response = self.storage.get_random_statement()

        else:
            # If the input is blank, return a random statement
            response = self.storage.get_random_statement()

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
            self.storage.save_statement(**response_data[name])

        return response_data

    def get_response(self, input_text, user_name="user"):
        """
        Return the bot's response based on the input.
        """
        response = self.io.get_response(
            self, {"name":user_name, "text": input_text}
        )

        return response
