import logging


class StorageAdapter(object):
    """
    This is an abstract class that represents the interface
    that all storage adapters should implement.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize common attributes shared by all storage adapters.

        :param str tagger_language: The language that the tagger uses to remove stopwords.
        """
        self.logger = kwargs.get('logger', logging.getLogger(__name__))

        self.raise_on_missing_search_text = kwargs.get(
            'raise_on_missing_search_text', True
        )

    def get_model(self, model_name):
        """
        Return the model class for a given model name.

        model_name is case insensitive.
        """
        get_model_method = getattr(self, 'get_%s_model' % (
            model_name.lower(),
        ))

        return get_model_method()

    def get_object(self, object_name):
        """
        Return the class for a given object name.

        object_name is case insensitive.
        """
        get_model_method = getattr(self, 'get_%s_object' % (
            object_name.lower(),
        ))

        return get_model_method()

    def get_statement_object(self):
        from chatterbot.conversation import Statement

        StatementModel = self.get_model('statement')

        Statement.statement_field_names.extend(
            StatementModel.extra_statement_field_names
        )

        return Statement

    def count(self) -> int:
        """
        Return the number of entries in the database.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `count` method is not implemented by this adapter.'
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

        :param page_size: The maximum number of records to load into
            memory at once when returning results.
            Defaults to 1000

        :param order_by: The field name that should be used to determine
            the order that results are returned in.
            Defaults to None

        :param tags: A list of tags. When specified, the results will only
            include statements that have a tag in the provided list.
            Defaults to [] (empty list)

        :param exclude_text: If the ``text`` of a statement is an exact match
            for the value of this parameter the statement will not be
            included in the result set.
            Defaults to None

        :param exclude_text_words: If the ``text`` of a statement contains a
            word from this list then the statement will not be included in
            the result set.
            Defaults to [] (empty list)

        :param persona_not_startswith: If the ``persona`` field of a
            statement starts with the value specified by this parameter,
            then the statement will not be returned in the result set.
            Defaults to None

        :param search_text_contains: If the ``search_text`` field of a
            statement contains a word that is in the string provided to
            this parameter, then the statement will be included in the
            result set.
            Defaults to None

        :param search_in_response_to: If the ``search_in_response_to`` field
            of a statement contains a word that is in the string provided to
            this parameter, then the statement will be included in the
            result set.
            Defaults to None
        """
        raise self.AdapterMethodNotImplementedError(
            'The `filter` method is not implemented by this adapter.'
        )

    def create(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `create` method is not implemented by this adapter.'
        )

    def create_many(self, statements):
        """
        Creates multiple statement entries.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `create_many` method is not implemented by this adapter.'
        )

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `update` method is not implemented by this adapter.'
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

    class EmptyDatabaseException(Exception):

        def __init__(self, message=None):
            default = 'The database currently contains no entries. At least one entry is expected. You may need to train your chat bot to populate your database.'
            super().__init__(message or default)

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when a storage adapter method has not been implemented.
        Typically this indicates that the method should be implement in a subclass.
        """
        pass
