from chatterbot.adapters import Adapter


class StorageAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all storage adapters should implement.
    """

    def __init__(self, base_query=None, *args, **kwargs):
        """
        Initialize common attributes shared by all storage adapters.
        """
        super(StorageAdapter, self).__init__(**kwargs)

        self.kwargs = kwargs
        self.read_only = kwargs.get('read_only', False)
        self.adapter_supports_queries = True
        self.base_query = None

    @property
    def Statement(self):
        """
        Create a storage-aware statement.
        """
        import os

        if 'DJANGO_SETTINGS_MODULE' in os.environ:
            from chatterbot.ext.django_chatterbot.models import Statement
            return Statement
        else:
            from chatterbot.conversation.statement import Statement
            statement = Statement
            statement.storage = self
            return statement

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
        raise self.AdapterMethodNotImplementedError()

    def find(self, statement_text):
        """
        Returns a object from the database if it exists
        """
        raise self.AdapterMethodNotImplementedError()

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        raise self.AdapterMethodNotImplementedError()

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain
        all listed attributes and in which all values
        match for all listed attributes will be returned.
        """
        raise self.AdapterMethodNotImplementedError()

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        raise self.AdapterMethodNotImplementedError()

    def get_random(self):
        """
        Returns a random statement from the database
        """
        raise self.AdapterMethodNotImplementedError()

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        raise self.AdapterMethodNotImplementedError()

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

        def __init__(self, value="The database currently contains no entries. At least one entry is expected. You may need to train your chat bot to populate your database."):
            self.value = value

        def __str__(self):
            return repr(self.value)
