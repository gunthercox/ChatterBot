from chatterbot.utils.module_loading import import_module


class StorageController(object):

    def __init__(self, adapter, database_name):

        StorageAdapter = import_module(adapter)
        self.storage_adapter = StorageAdapter(database_name)

        self.recent_statements = []

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
        #if "occurrence" in data:
        #    return data["occurrence"] + 1

        return data.get("occurrence", 0) + 1

    def get_occurrence_count(self, statement):
        """
        Return the number of times a statement occurs in the database
        """
        # If the number of occurences has not been set then return 1
        return statement.get("occurrence", 1)

    def get_responses(self, statement):
        """
        Returns the list of responses for a given statement.
        """

        #TODO: Don't make this lookup here
        statement = self.storage_adapter.find(statement)

        responses = statement.get("in_response_to", [])

        return responses

    def update_response_list(self, key, previous_statement):
        """
        Update the list of statements that a know statement has responded to.
        """
        responses = []

        values = self.storage_adapter.find(key)

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

    def save_statement(self, **kwargs):
        statement = list(kwargs.keys())[0]
        values = kwargs[statement]

        # Update the database with the changes
        self.storage_adapter.update(statement, **values)

    def train(self, conversation):

        for statement in conversation:

            values = self.storage_adapter.find(statement)

            # Create an entry if the statement does not exist in the database
            if not values:
                values = {}

            values["occurrence"] = self.update_occurrence_count(values)

            previous_statement = self.get_last_statement()
            values["in_response_to"] = self.update_response_list(statement, previous_statement)

            self.storage_adapter.update(statement, **values)

    def get_statements_in_response_to(self, input_statement):
        """
        Returns a list of statement objects that are
        in response to a specified statement object.
        """
        # TODO: Call to _keys is bad
        statements = self.storage_adapter._keys()

        results = []

        for statement in statements:
            if input_statement in self.get_responses(statement):
                results.append(statement)

        return results

    def get_most_frequent_response(self, closest_statement):
        """
        Returns the statement with the greatest number of occurrences.
        """

        response_list = self.get_statements_in_response_to(closest_statement)
        # TODO: if list empty

        # Initialize the matching responce to the closest statement.
        # This will be returned in the case that no match can be found.
        matching_response = closest_statement

        # The statement passed in must be an existing statement within the database.
        statement_data = self.storage_adapter.find(matching_response)
        occurrence_count = self.get_occurrence_count(statement_data)

        for statement in response_list:

            statement_data = self.storage_adapter.find(statement)

            statement_occurrence_count = self.get_occurrence_count(statement_data)

            # Keep the more common statement
            if statement_occurrence_count >= occurrence_count:
                matching_response = statement
                occurrence_count = statement_occurrence_count

            #TODO? If the two statements occure equaly in frequency, should we keep one at random

        # Choose the most common selection of matching response
        return {matching_response: self.storage_adapter.find(matching_response)}
