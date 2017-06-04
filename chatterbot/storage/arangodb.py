from chatterbot.conversation import Response
from chatterbot.storage import StorageAdapter


class ArangoStorageAdapter(StorageAdapter):
    """
    The ArangoStorageAdapter is a Storage Adapter that allows Chatterbot
    to store messages in ArangoDB in Document Collection

    :keyword username: The UserName of user to be used for authentication.
    :type username: str

    .. code-block:: python

    :keyword password: The Password of user to be used for authentication.
    :type password: str

    :keyword database_name: The name of database to be used to be used by ChatterBot
                       Note: it should be created before being used here.
                       Default: chatterbot-database
    :type database_name: str

    :keyword collection: The name of collection to be used by Chatterbot.
                         Note: it should be created before being used here.
                         Default: statements
    :type collection: str

    :keyword host: The host name where ArangoDB can be accessed.
                   Default: localhost
    :type host: str

    :keyword port: The name of collection in database to be used by ChatterBot.
                   Default: 8529
    :type port: int

    :keyword logging: Whether the logging should be enabled or not in ArangoDB.
                      Default: true
    :type logging: bool

    :keyword protocol: The protocol used to connect to ArangoDB. Default: http
    :type protocol: str
    """

    def __init__(self, username, password, **kwargs):
        """

        :param username: The Username of ArangoDB user for auth.
        :param password: The password of ArangoDB user for auth
        :param kwargs: Other parameters such as database_name, collection,
                        host, port, loggin, protocol for ArangoDB
        """

        super(ArangoStorageAdapter, self).__init__(**kwargs)
        from arango import ArangoClient

        # Initialize all variables
        self.database_username = username
        self.database_password = password
        self.database_name = self.kwargs.get('database_name', 'chatterbot-database')
        self.database_collection = self.kwargs.get('collection', 'statements')
        self.database_host = self.kwargs.get('host', 'localhost')
        self.database_port = self.kwargs.get('port', '8529')
        self.database_logging = self.kwargs.get('logging', True)
        self.database_protocol = self.kwargs.get('protocol', 'http://')

        # Use the default host and port
        self.client = ArangoClient(protocol=self.database_protocol,
                                   host=self.database_host,
                                   port=self.database_port,
                                   username=self.database_username,
                                   password=self.database_password,
                                   enable_logging=self.database_logging)

        # Specify the name of the database
        self.database = self.client.db(name=self.database_name)

        # The Arango collection of statement documents
        self.statements = self.database.collection(self.database_collection)

        # Set a requirement for the text attribute to be unique
        if not any(x['fields'] == ['text'] for x in self.statements.indexes()):
            self.statements.add_hash_index(fields=['text'], unique=True)

    def count(self):
        return self.statements.count()

    def arango_to_object(self, val):
        """
        This converts data from arango object to Statement object
        :param val: Arango object
        :return: Statement object
        """
        val = val.copy()

        # Delete the elements used by arango but useless to Chatterbot
        del val['_key']
        del val['_rev']
        del val['_id']

        # Build the objects for the response list
        val['in_response_to'] = self.deserialize_responses(
            val['in_response_to']
        )

        # Remove the text attribute from the values
        text = val.pop('text')

        return self.Statement(text, **val)

    def deserialize_responses(self, response_list):
        """
        Takes the list of response items and returns
        the list converted to Response objects.
        """
        proxy_statement = self.Statement('')

        for response in response_list:
            data = response.copy()
            text = data['text']
            del data['text']

            proxy_statement.add_response(
                Response(text, **data)
            )

        return proxy_statement.in_response_to

    def find(self, statement_text):
        """
        Returns a object from the database if it exists
        """
        # crsr = self.statements.find({'text': statement_text})
        crsr = self.database.aql.execute('FOR s IN ' + self.database_collection + ' FILTER s.text == ' + statement_text
                                         + ' COLLECT a = s RETURN a')

        if crsr.count() == 0:
            return None

        value = crsr.next()

        return self.arango_to_object(value)

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        for statement in self.filter(in_response_to__contains=statement_text):
            statement.remove_response(statement_text)
            self.update(statement)

        self.statements.delete_many([x for x in self.statements.find({'text': statement_text})])

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain
        all listed attributes and in which all values
        match for all listed attributes will be returned.
        """

        order_by = kwargs.pop('order_by', None)

        rq = 'FOR s IN statements '

        # Convert Response objects to data
        if 'in_response_to__contains' in kwargs:
            rq += 'FOR t IN s.in_response_to FILTER t.text == "' + \
                  kwargs['in_response_to__contains'] + '" COLLECT a = s '

            del kwargs['in_response_to__contains']

        # TODO work on this part, currently it returns like containing only
        elif 'in_response_to' in kwargs:
            serialized_responses = []
            for response in kwargs['in_response_to']:
                serialized_responses.append({'text': response})

            rq += str(serialized_responses) + 'ALL IN s.in_response_to[*].text COLLECT a = s '

            del kwargs['in_response_to']

        if order_by:
            direction = 'ASC'

            # Sort so that newer datetimes appear first
            if order_by == 'created_at':
                direction = 'DESC'

            rq += 'SORT a.' + order_by + direction

        rq += ' RETURN a'

        # List comprehension for results
        results = [self.arango_to_object(z) for z in self.database.aql.execute(rq)]

        return results

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        import json
        from datetime import datetime

        # Serialize and change format from datetime.datetime -> isoformat
        # This is for bypassing TypeError in json.dumps()
        data = statement.serialize()
        if isinstance(data['created_at'], datetime):
            data['created_at'] = data['created_at'].isoformat()

        # This is INSERT data
        insrt = json.dumps(data)

        # Query to UPSERT INSERT or UPDATE
        query = 'UPSERT ' + json.dumps({'text': data.pop('text')}) + ' INSERT ' + insrt + ' UPDATE ' + \
                json.dumps(data) + ' IN ' + self.database_collection

        # Execute query in ArangoDB
        self.database.aql.execute(query)

        # Make sure that an entry for each response exists
        for response_statement in statement.in_response_to:
            response = self.find(response_statement.text)
            if not response:
                # These are not found
                self.update(self.Statement(response_statement.text))

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        lst = [x for x in self.database.aql.execute("FOR s IN statements SORT RAND() LIMIT 1 RETURN s")]

        if len(lst) < 1:
            raise self.EmptyDatabaseException

        return self.arango_to_object(lst[0])

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        self.client.delete_database(self.database_name)

    def get_response_statements(self):
        """
        Return only statements that are in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.

        This method may be overridden by a child class to provide more a
        efficient method to get these results.
        """
        q = 'FOR s IN statements FOR t in s.in_response_to FOR z IN statements ' \
            'FILTER z.text == t.text COLLECT a = z RETURN a'
        return [self.arango_to_object(a) for a in self.database.aql.execute(q)]

    class EmptyDatabaseException(Exception):

        def __init__(self, value='The database currently contains no entries. '
                                 'At least one entry is expected. '
                                 'You may need to train your chat bot to populate your database.'):
            self.value = value

        def __str__(self):
            return repr(self.value)

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when a storage adapter method has not been implemented.
        Typically this indicates that the method should be implement in a subclass.
        """
        pass
