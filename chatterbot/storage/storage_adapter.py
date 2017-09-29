import logging


class StorageAdapter(object):
    """
    This is an abstract class that represents the interface
    that all storage adapters should implement.
    """

    def __init__(self, base_query=None, *args, **kwargs):
        """
        Initialize common attributes shared by all storage adapters.
        """
        self.kwargs = kwargs
        self.logger = kwargs.get('logger', logging.getLogger(__name__))
        self.adapter_supports_queries = True
        self.base_query = None

    def get_model(self, model_name):
        """
        Return the model class for a given model name.
        """

        # The string must be lowercase
        model_name = model_name.lower()

        kwarg_model_key = '%s_model' % (model_name, )

        if kwarg_model_key in self.kwargs:
            return self.kwargs.get(kwarg_model_key)

        get_model_method = getattr(self, 'get_%s_model' % (model_name, ))

        return get_model_method()

    def generate_base_query(self, chatterbot, session_id):
        """
        Create a base query for the storage adapter.
        """
        if self.adapter_supports_queries:
            for filter_instance in chatterbot.filters:
                self.base_query = filter_instance.filter_selection(chatterbot, session_id)

    def count(self):
        """
        Return the number of entries in the database.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `count` method is not implemented by this adapter.'
        )

    def find(self, statement_text):
        """
        Returns a object from the database if it exists
        """
        raise self.AdapterMethodNotImplementedError(
            'The `find` method is not implemented by this adapter.'
        )

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove` method is not implemented by this adapter.'
        )

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain
        all listed attributes and in which all values
        match for all listed attributes will be returned.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `filter` method is not implemented by this adapter.'
        )

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `update` method is not implemented by this adapter.'
        )

    def get_latest_response(self, conversation_id):
        """
        Returns the latest response in a conversation if it exists.
        Returns None if a matching conversation cannot be found.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `get_latest_response` method is not implemented by this adapter.'
        )

    def create_conversation(self):
        """
        Creates a new conversation.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `create_conversation` method is not implemented by this adapter.'
        )

    def add_to_conversation(self, conversation_id, statement, response):
        """
        Add the statement and response to the conversation.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `add_to_conversation` method is not implemented by this adapter.'
        )

    def get_random(self):
        """
        Returns a random statement from the database.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `get_random` method is not implemented by this adapter.'
        )

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `drop` method is not implemented by this adapter.'
        )

    def get_response_statements(self):
        """
        Return only statements that are in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.

        This method may be overridden by a child class to provide more a
        efficient method to get these results.
        """
        statement_list = self.filter()

        responses = set()
        to_remove = list()
        for statement in statement_list:
            for response in statement.in_response_to:
                responses.add(response.text)
        for statement in statement_list:
            if statement.text not in responses:
                to_remove.append(statement)

        for statement in to_remove:
            statement_list.remove(statement)

        return statement_list

    class EmptyDatabaseException(Exception):

        def __init__(self, value='The database currently contains no entries. At least one entry is expected. You may need to train your chat bot to populate your database.'):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when a storage adapter method has not been implemented.
        Typically this indicates that the method should be implement in a subclass.
        """
        pass
