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

        self.database_uri = self.kwargs.get("database_uri", False)

        # None results in a sqlite in-memory database as the default
        if self.database_uri is None:
            self.database_uri = "sqlite://"

        # Create a file database if the database is not a connection string
        if not self.database_uri:
            self.database_uri = "sqlite:///db.sqlite3"

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
            self.create_database()

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

    def find(self, statement_text):
        """
        Returns a statement if it exists otherwise None
        """
        Statement = self.get_model('statement')
        session = self.Session()

        query = session.query(Statement).filter_by(text=statement_text)
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
        Statement = self.get_model('statement')
        session = self.Session()

        query = session.query(Statement).filter_by(text=statement_text)
        record = query.first()

        session.delete(record)

        self._session_finish(session)

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain all
        listed attributes and in which all values match
        for all listed attributes will be returned.
        """
        Statement = self.get_model('statement')
        Response = self.get_model('response')

        session = self.Session()

        kwargs.pop('order_by', None)
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

    def create(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        tags = kwargs.pop('tags', [])

        statement = Statement(**kwargs)

        statement.tags.extend([
            Tag(name=tag) for tag in tags
        ])

        session.add(statement)

        self._session_finish(session)

        return statement

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

            query = session.query(Statement).filter_by(text=statement.text)
            record = query.first()

            # Create a new statement entry if one does not already exist
            if not record:
                record = Statement(text=statement.text)

            if statement.extra_data is None:
                statement.extra_data = {}

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
                        conversation=response.conversation,
                        occurrence=response.occurrence
                    )

                # Make sure a statement exists for the response text
                if response.text != statement.text:
                    response_statement_query = session.query(Statement).filter_by(
                        text=response.text
                    )

                    if not response_statement_query.count():
                        _response_statement = Statement(
                            text=response.text
                        )
                        session.add(_response_statement)

                record.in_response_to.append(_response)

            session.add(record)

            self._session_finish(session)

    def get_latest_response(self, conversation):
        """
        Returns the latest response in a conversation if it exists.
        Returns None if a matching conversation cannot be found.
        """
        Statement = self.get_model('statement')
        Response = self.get_model('response')

        session = self.Session()
        statement = None
        response = None

        response_query = session.query(Response).filter(
            Response.conversation == conversation
        ).order_by(Response.id)

        if response_query.count():
            response = response_query[-1].text

        # Get the statement for the response
        if response:
            statement = session.query(Statement).filter(
                Statement.text == response
            ).first()
            if statement:
                statement = statement.get_statement()

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

    def create_database(self):
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
