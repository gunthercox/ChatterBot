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

        PluginChooser = import_module("chatterbot.adapters.plugins.PluginChooser")
        self.plugin_chooser = PluginChooser(**kwargs)

        StorageAdapter = import_module(storage_adapter)
        self.storage = StorageAdapter(**kwargs)

        LogicAdapter = import_module(logic_adapter)
        self.logic = LogicAdapter(**kwargs)

        IOAdapter = import_module(io_adapter)
        self.io = IOAdapter(**kwargs)

        self.trainer = None

        self.recent_statements = []

    def get_last_statement(self):
        """
        Return the last statement that was received.
        """
        if self.recent_statements:
            return self.recent_statements[-1]
        return None

    def get_most_frequent_response(self, input_statement, response_list):
        """
        Returns the statement with the greatest number of occurrences.
        """

        # Initialize the matching responce to the first response.
        # This will be returned in the case that no match can be found.
        matching_response = response_list[0]
        occurrence_count = 0

        for statement in response_list:
            count = statement.get_response_count(input_statement)

            # Keep the more common statement
            if count >= occurrence_count:
                matching_response = statement
                occurrence_count = count

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

        # Applying plugin logic to see whether the chatbot should respond in this way
        plugin_response = self.plugin_chooser.choose( input_statement )

        if not plugin_response is False:
            return plugin_response

        # If no responses exist, return the input statement
        if not self.storage.count():
            self.storage.update(input_statement)
            self.recent_statements.append(input_statement)

            # Process the response output with the IO adapter
            return self.io.process_response(input_statement)

        all_statements = self.storage.filter()

        '''
        Filter out all statements that are not in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.
        '''
        # Copy the list of statements to prevent changing the size of the list while iterating over it
        all_statements_copy = list(all_statements)
        for statement in all_statements_copy:
            response_exists = False
            for s in all_statements_copy:
                if statement in s.in_response_to:
                    response_exists = True
                    break # Exit for loop since one exists

            if not response_exists:
                all_statements.remove(statement)

        # It will not be possible to select a match from an empty list of statements
        if not all_statements:
            previous_statement = self.get_last_statement()

            if previous_statement:
                input_statement.add_response(previous_statement)

            # Update the database after selecting a response
            self.storage.update(input_statement)

            # Return a random response
            response = self.storage.get_random()

            self.recent_statements.append(response)

            return self.io.process_response(response)

        # Select the closest match to the input statement
        closest_match = self.logic.get(
            input_statement,
            all_statements,
            self.recent_statements
        )

        # Get all statements that are in response to the closest match
        response_list = self.storage.filter(
            in_response_to__contains=closest_match.text
        )

        if response_list:
            #response = self.get_most_frequent_response(closest_match, response_list)
            response = self.get_first_response(response_list)
            #response = self.get_random_response(response_list)
        else:
            response = self.storage.get_random()

        #if input_statement.text == closest_match.text:
        #    input_statement = closest_match

        # TODO: Why is checking if the input is equal to the closest match not the same here?
        existing_statement = self.storage.find(input_statement.text)

        if existing_statement:
            input_statement = existing_statement

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
