from .utils.module_loading import import_module
from .controllers import StorageController
from .conversation import Statement


class ChatBot(object):

    def __init__(self, name, **kwargs):
        self.name = name

        storage_adapter = kwargs.get("storage_adapter",
            "chatterbot.adapters.storage.JsonDatabaseAdapter"
        )

        logic_adapter = kwargs.get("logic_adapter",
            "chatterbot.adapters.logic.ClosestMatchAdapter"
        )

        io_adapter = kwargs.get("io_adapter",
            "chatterbot.adapters.io.TerminalAdapter"
        )

        StorageAdapter = import_module(storage_adapter)
        self.storage_adapter = StorageAdapter(**kwargs)

        self.storage = StorageController(self.storage_adapter)

        LogicAdapter = import_module(logic_adapter)
        self.logic = LogicAdapter()

        IOAdapter = import_module(io_adapter)
        self.io = IOAdapter()

    def train(self, conversation):
        """
        Update or create the data for a statement.
        """
        for text in conversation:
            statement = self.storage_adapter.find(text)
            statement.update_occurrence_count()

            previous_statement = self.storage.get_last_statement()

            statement.add_response(previous_statement)
            self.storage.recent_statements.append(previous_statement)

            self.storage_adapter.update(statement.text, **statement.serialize())

    def get_response_data(self, statement_text):
        """
        Returns a dictionary containing the meta data for
        the current response.
        """
        statement = Statement(statement_text)

        if statement_text.strip():
            text_of_all_statements = self.storage.list_statements()

            match = self.logic.get(statement_text, text_of_all_statements)

            if match:
                response = self.storage.get_most_frequent_response(match)
            else:
                response = self.storage_adapter.get_random()

        else:
            # If the input is blank, return a random statement
            response = self.storage_adapter.get_random()

        previous_statement = self.storage.get_last_statement()
        statement.add_response(previous_statement)

        statement.update_occurrence_count()

        self.storage.recent_statements.append(list(response.keys())[0])

        response_data = response.serialize()

        # Update the database after selecting a response
        self.storage.save_statement(**response_data)

        return response_data

    def get_response(self, input_text):
        """
        Return the bot's response based on the input.
        """
        response_data = self.get_response_data(input_text)
        response = self.io.process_response(response_data)

        return response

    def get_input(self):
        return self.io.process_input()

