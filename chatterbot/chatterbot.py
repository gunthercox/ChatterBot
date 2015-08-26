from .utils.module_loading import import_module
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
        self.storage = StorageAdapter(**kwargs)

        LogicAdapter = import_module(logic_adapter)
        self.logic = LogicAdapter()

        IOAdapter = import_module(io_adapter)
        self.io = IOAdapter()

        self.recent_statements = []

    def get_last_statement(self):
        """
        Returns the last statement that was issued to the chat bot.
        If there was no last statement then return None.
        """
        if len(self.recent_statements) == 0:
            return None

        return self.recent_statements[-1]

    def get_most_frequent_response(self, closest_statement):
        """
        Returns the statement with the greatest number of occurrences.
        """
        response_list = self.storage.filter(
            in_response_to__contains=closest_statement
        )

        # Initialize the matching responce to the closest statement.
        # This will be returned in the case that no match can be found.
        matching_response = closest_statement

        # The statement passed in must be an existing statement within the database
        found_statement = self.storage.find(matching_response.text)

        occurrence_count = found_statement.get_occurrence_count()

        for statement in response_list:

            statement_data = self.storage.find(statement.text)

            statement_occurrence_count = statement_data.get_occurrence_count()

            # Keep the more common statement
            if statement_occurrence_count >= occurrence_count:
                matching_response = statement
                occurrence_count = statement_occurrence_count

            #TODO? If the two statements occure equaly in frequency, should we keep one at random

        # Choose the most commonly occuring matching response
        return matching_response

    def get_response(self, input_text):
        """
        Return the bot's response based on the input.
        """
        from .adapters.exceptions import EmptyDatabaseException

        statement = Statement(input_text)

        try:
            # Instantiate the response as a random statement
            response = self.storage.get_random()
        except EmptyDatabaseException:
            # Use the input statement if the database is empty
            response = statement

        if statement.text.strip():
            text_of_all_statements = self.storage._keys()

            match = self.logic.get(statement.text, text_of_all_statements)

            if match:
                match = self.storage.find(match)
                if match:
                    response = self.get_most_frequent_response(match)

        previous_statement = self.get_last_statement()
        self.recent_statements.append(statement)

        if previous_statement:
            statement.add_response(previous_statement)
        statement.update_occurrence_count()

        # Update the database after selecting a response
        self.storage.update(statement)

        # Process the response output with the IO adapter
        response = self.io.process_response(response)

        return response

    def get_input(self):
        return self.io.process_input()

    def train(self, conversation):
        """
        Update or create the data for a statement.
        """
        for text in conversation:
            statement = self.storage.find(text)

            # Create the statement if a match was not found
            if not statement:
                statement = Statement(text)
            else:
                statement.update_occurrence_count()

            previous_statement = self.get_last_statement()

            if previous_statement:
                statement.add_response(previous_statement)

            self.recent_statements.append(statement)
            self.storage.update(statement)

