from .utils.module_loading import import_module
from .conversation import Statement, Response


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
        self.storage = StorageAdapter(**kwargs)

        LogicAdapter = import_module(logic_adapter)
        self.logic = LogicAdapter()

        IOAdapter = import_module(io_adapter)
        self.io = IOAdapter()

        self.trainer = None

        self.recent_statements = []

    def get_last_statement(self):
        """
        Return the last statement that was received.
        """
        if self.recent_statements:
            return self.recent_statements[-1]
        return None

    def get_most_frequent_response(self, response_list):
        """
        Returns the statement with the greatest number of occurrences.
        """

        # Initialize the matching responce to the first response.
        # This will be returned in the case that no match can be found.
        matching_response = response_list[0]
        occurrence_count = 0

        for statement in response_list:

            statement_data = self.storage.find(statement.text)
            statement_occurrence_count = statement_data.get_response_count()

            # Keep the more common statement
            if statement_occurrence_count >= occurrence_count:
                matching_response = statement
                occurrence_count = statement_occurrence_count

        # Choose the most commonly occuring matching response
        return matching_response

    def get_first_response(self, response_list):
        """
        Return the first statement in the response list.
        """
        return response_list[0]

    def get_random_response(self, response_list):
        """
        Choose a random response from the selection.
        """
        from random import choice
        return choice(response_list)

    def get_response(self, input_text):
        """
        Return the bot's response based on the input.
        """
        input_statement = Statement(input_text)

        # If no responses exist, use the input text
        if not self.storage.count():
            response = Statement(input_text)
            self.storage.update(response)
            self.recent_statements.append(response)

            # Process the response output with the IO adapter
            response = self.io.process_response(response)

            return response

        all_statements = self.storage.filter()

        # Select the closest match to the input statement
        closest_match_text = self.logic.get(
            input_text,
            all_statements,
            self.recent_statements
        )

        # Get all statements that are in response to the closest match
        response_list = self.storage.filter(
            in_response_to__contains=closest_match_text
        )

        if response_list:
            #response = self.get_most_frequent_response(response_list)
            response = self.get_first_response(response_list)
            #response = self.get_random_response(response_list)
        else:
            response = self.storage.get_random()

        previous_statement = self.get_last_statement()

        if previous_statement:
            input_statement.add_response(previous_statement)

        # Update the database after selecting a response
        self.storage.update(input_statement)

        self.recent_statements.append(response)

        # Process the response output with the IO adapter
        response = self.io.process_response(response)

        return response

    def get_input(self):
        return self.io.process_input()

    def train(self, conversation=None, *args, **kwargs):
        """
        Train the chatbot based on input data.
        """
        from .training import Trainer

        self.trainer = Trainer(self)

        if isinstance(conversation, str):
            corpora = list(args)
            corpora.append(conversation)

            if corpora:
                self.trainer.train_from_corpora(corpora)
        else:
            self.trainer.train_from_list(conversation)

