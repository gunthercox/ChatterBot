from chatterbot.storage import StorageAdapter


def get_response_table(response):
    from chatterbot.ext.sqlalchemy_app.models import Response
    return Response(text=response.text, occurrence=response.occurrence)


class SQLStorageAdapter(StorageAdapter):
    """
    SQLStorageAdapter allows ChatterBot to store conversation
    data semi-structured T-SQL database, virtually, any database
    that SQL Alchemy supports.

    Notes:
        Tables may change (and will), so, save your training data.
        There is no data migration (yet).
        Performance test not done yet.
        Tests using other databases not finished.

    All parameters are optional, by default a sqlite database is used.

    It will check if tables are present, if they are not, it will attempt
    to create the required tables.

    :keyword database: Used for sqlite database. Ignored if database_uri is specified.
    :type database: str

    :keyword database_uri: eg: sqlite:///database_test.db", use database_uri or database,
        database_uri can be specified to choose database driver (database parameter will be ignored).
    :type database_uri: str

    :keyword read_only: False by default, makes all operations read only, has priority over all DB operations
        so, create, update, delete will NOT be executed
    :type read_only: bool
    """

    def __init__(self, **kwargs):
        super(SQLStorageAdapter, self).__init__(**kwargs)

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        default_uri = "sqlite:///db.sqlite3"

        database_name = self.kwargs.get("database", False)

        # None results in a sqlite in-memory database as the default
        if database_name is None:
            default_uri = "sqlite://"

        self.database_uri = self.kwargs.get(
            "database_uri", default_uri
        )

        # Create a sqlite file if a database name is provided
        if database_name:
            self.database_uri = "sqlite:///" + database_name

        self.engine = create_engine(self.database_uri, convert_unicode=True)

        from re import search

        if search('^sqlite://', self.database_uri):
            from sqlalchemy.engine import Engine
            from sqlalchemy import event

            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                dbapi_connection.execute('PRAGMA journal_mode=WAL')
                dbapi_connection.execute('PRAGMA synchronous=NORMAL')

        self.read_only = self.kwargs.get(
            "read_only", False
        )

        if not self.engine.dialect.has_table(self.engine, 'Statement'):
            self.create()

        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)

        # ChatterBot's internal query builder is not yet supported for this adapter
        self.adapter_supports_queries = False

    def get_statement_model(self):
        """
        Return the statement model.
        """
        from chatterbot.ext.sqlalchemy_app.models import Statement
        return Statement

    def get_response_model(self):
        """
        Return the response model.
        """
        from chatterbot.ext.sqlalchemy_app.models import Response
        return Response

    def get_conversation_model(self):
        """
        Return the conversation model.
        """
        from chatterbot.ext.sqlalchemy_app.models import Conversation
        return Conversation

    def get_tag_model(self):
        """
        Return the conversation model.
        """
        from chatterbot.ext.sqlalchemy_app.models import Tag
        return Tag

    def count(self):
        """
        Return the number of entries in the database.
        """
        Statement = self.get_model('statement')

        session = self.Session()
        statement_count = session.query(Statement).count()
        session.close()
        return statement_count

    def __statement_filter(self, session, **kwargs):
        """
        Apply filter operation on Statement

        rtype: query
        """
        Statement = self.get_model('statement')

        _query = session.query(Statement)
        return _query.filter_by(**kwargs)

    def find(self, statement_text):
        """
        Returns a statement if it exists otherwise None
        """
        session = self.Session()
        query = self.__statement_filter(session, **{"text": statement_text})
        record = query.first()
        if record:
            statement = record.get_statement()
            session.close()
            return statement

        session.close()
        return None

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        session = self.Session()
        query = self.__statement_filter(session, **{"text": statement_text})
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain
        all listed attributes and in which all values
        match for all listed attributes will be returned.
        """
        Statement = self.get_model('statement')
        Response = self.get_model('response')

        session = self.Session()

        filter_parameters = kwargs.copy()

        statements = []
        _query = None

        if len(filter_parameters) == 0:
            _response_query = session.query(Statement)
            statements.extend(_response_query.all())
        else:
            for i, fp in enumerate(filter_parameters):
                _filter = filter_parameters[fp]
                if fp in ['in_response_to', 'in_response_to__contains']:
                    _response_query = session.query(Statement)
                    if isinstance(_filter, list):
                        if len(_filter) == 0:
                            _query = _response_query.filter(
                                Statement.in_response_to == None  # NOQA Here must use == instead of is
                            )
                        else:
                            for f in _filter:
                                _query = _response_query.filter(
                                    Statement.in_response_to.contains(get_response_table(f)))
                    else:
                        if fp == 'in_response_to__contains':
                            _query = _response_query.join(Response).filter(Response.text == _filter)
                        else:
                            _query = _response_query.filter(Statement.in_response_to == None)  # NOQA
                else:
                    if _query:
                        _query = _query.filter(Response.statement_text.like('%' + _filter + '%'))
                    else:
                        _response_query = session.query(Response)
                        _query = _response_query.filter(Response.statement_text.like('%' + _filter + '%'))

                if _query is None:
                    return []
                if len(filter_parameters) == i + 1:
                    statements.extend(_query.all())

        results = []

        for statement in statements:
            if isinstance(statement, Response):
                if statement and statement.statement_table:
                    results.append(statement.statement_table.get_statement())
            else:
                if statement:
                    results.append(statement.get_statement())

        session.close()

        return results

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        Statement = self.get_model('statement')
        Response = self.get_model('response')
        Tag = self.get_model('tag')

        if statement:
            session = self.Session()
            query = self.__statement_filter(session, **{"text": statement.text})
            record = query.first()

            # Create a new statement entry if one does not already exist
            if not record:
                record = Statement(text=statement.text)

            record.extra_data = dict(statement.extra_data)

            for _tag in statement.tags:
                tag = session.query(Tag).filter_by(name=_tag).first()

                if not tag:
                    # Create the record
                    tag = Tag(name=_tag)

                record.tags.append(tag)

            # Get or create the response records as needed
            for response in statement.in_response_to:
                _response = session.query(Response).filter_by(
                    text=response.text,
                    statement_text=statement.text
                ).first()

                if _response:
                    _response.occurrence += 1
                else:
                    # Create the record
                    _response = Response(
                        text=response.text,
                        statement_text=statement.text,
                        occurrence=response.occurrence
                    )

                record.in_response_to.append(_response)

            session.add(record)

            self._session_finish(session)

    def create_conversation(self):
        """
        Create a new conversation.
        """
        Conversation = self.get_model('conversation')

        session = self.Session()
        conversation = Conversation()

        session.add(conversation)
        session.flush()

        session.refresh(conversation)
        conversation_id = conversation.id

        session.commit()
        session.close()

        return conversation_id

    def add_to_conversation(self, conversation_id, statement, response):
        """
        Add the statement and response to the conversation.
        """
        Statement = self.get_model('statement')
        Conversation = self.get_model('conversation')

        session = self.Session()
        conversation = session.query(Conversation).get(conversation_id)

        statement_query = session.query(Statement).filter_by(
            text=statement.text
        ).first()
        response_query = session.query(Statement).filter_by(
            text=response.text
        ).first()

        # Make sure the statements exist
        if not statement_query:
            self.update(statement)
            statement_query = session.query(Statement).filter_by(
                text=statement.text
            ).first()

        if not response_query:
            self.update(response)
            response_query = session.query(Statement).filter_by(
                text=response.text
            ).first()

        conversation.statements.append(statement_query)
        conversation.statements.append(response_query)

        session.add(conversation)
        self._session_finish(session)

    def get_latest_response(self, conversation_id):
        """
        Returns the latest response in a conversation if it exists.
        Returns None if a matching conversation cannot be found.
        """
        Statement = self.get_model('statement')

        session = self.Session()
        statement = None

        statement_query = session.query(
            Statement
        ).filter(
            Statement.conversations.any(id=conversation_id)
        ).order_by(Statement.id).limit(2).first()

        if statement_query:
            statement = statement_query.get_statement()

        session.close()

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        import random

        Statement = self.get_model('statement')

        session = self.Session()
        count = self.count()
        if count < 1:
            raise self.EmptyDatabaseException()

        rand = random.randrange(0, count)
        stmt = session.query(Statement)[rand]

        statement = stmt.get_statement()

        session.close()
        return statement

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        from chatterbot.ext.sqlalchemy_app.models import Base
        Base.metadata.drop_all(self.engine)

    def create(self):
        """
        Populate the database with the tables.
        """
        from chatterbot.ext.sqlalchemy_app.models import Base
        Base.metadata.create_all(self.engine)

    def _session_finish(self, session, statement_text=None):
        from sqlalchemy.exc import InvalidRequestError
        try:
            if not self.read_only:
                session.commit()
            else:
                session.rollback()
        except InvalidRequestError:
            # Log the statement text and the exception
            self.logger.exception(statement_text)
        finally:
            session.close()
