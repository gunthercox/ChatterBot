import random

from chatterbot.storage import StorageAdapter
from chatterbot.conversation import Response
from chatterbot.conversation import Statement

try:
    from chatterbot.ext.sqlalchemy_app.models import Base
    from sqlalchemy.orm import relationship
    from sqlalchemy.sql import func
    from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, PickleType


    class StatementTable(Base):
        """
        StatementTable, placeholder for a sentence or phrase.
        """

        __tablename__ = 'StatementTable'

        def get_statement(self):
            statement = Statement(self.text, extra_data=self.extra_data)
            for response in self.in_response_to:
                statement.add_response(response.get_response())
            return statement

        text = Column(String, unique=True)

        extra_data = Column(PickleType)

        in_response_to = relationship(
            'ResponseTable',
            back_populates='statement_table'
        )

    class ResponseTable(Base):
        """
        ResponseTable, contains responses related to a givem statment.
        """

        __tablename__ = 'ResponseTable'

        text = Column(String)

        created_at = Column(
            DateTime(timezone=True),
            server_default=func.now()
        )

        occurrence = Column(Integer, default=1)

        statement_text = Column(String, ForeignKey('StatementTable.text'))

        statement_table = relationship(
            'StatementTable',
            back_populates='in_response_to',
            cascade='all',
            uselist=False
        )

        def get_response(self):
            occ = {'occurrence': self.occurrence}
            return Response(text=self.text, **occ)

    conversation_association_table = Table(
        'conversation_association',
        Base.metadata,
        Column('conversation_id', Integer, ForeignKey('conversation.id')),
        Column('statement_id', Integer, ForeignKey('StatementTable.id'))
    )

    class Conversation(Base):
        """
        A conversation.
        """

        __tablename__ = 'conversation'

        id = Column(Integer, primary_key=True)

        statements = relationship(
            'StatementTable',
            secondary=lambda: conversation_association_table,
            backref='conversations'
        )

except ImportError:
    pass


def get_response_table(response):
    return ResponseTable(text=response.text, occurrence=response.occurrence)


class SQLStorageAdapter(StorageAdapter):
    """
    SQLStorageAdapter allows ChatterBot to store conversation
    data semi-structutered T-SQL database, virtually, any database that SQL Alchemy supports.

    Notes:
        Tables may change (and will), so, save your training data. There is no data migration (yet).
        Performance test not done yet.
        Tests using others databases not finished.

    All parameters are optional, by default a sqlite database is used.

    It will check if tables is present, if not, it will attempt to create required tables.
    :keyword database: Used for sqlite database. Ignored if database_uri especified.
    :type database: str

    :keyword database_uri: eg: sqlite:///database_test.db", # use database_uri or database, database_uri
        can be especified to choose database driver (database parameter will be igored).
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
            self.database_uri = "sqlite:///" + database_name + ".db"

        self.engine = create_engine(self.database_uri, convert_unicode=True)

        self.read_only = self.kwargs.get(
            "read_only", False
        )

        if not self.engine.dialect.has_table(self.engine, 'StatementTable'):
            self.create()

        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)

        # ChatterBot's internal query builder is not yet supported for this adapter
        self.adapter_supports_queries = False

    def count(self):
        """
        Return the number of entries in the database.
        """
        session = self.Session()
        statement_count = session.query(StatementTable).count()
        session.close()
        return statement_count

    def __statement_filter(self, session, **kwargs):
        """
        Apply filter operation on StatementTable

        rtype: query
        """
        _query = session.query(StatementTable)
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
        session = self.Session()

        filter_parameters = kwargs.copy()

        statements = []
        # _response_query = None
        _query = None
        if len(filter_parameters) == 0:
            _response_query = session.query(StatementTable)
            statements.extend(_response_query.all())
        else:
            for i, fp in enumerate(filter_parameters):
                _filter = filter_parameters[fp]
                if fp in ['in_response_to', 'in_response_to__contains']:
                    _response_query = session.query(StatementTable)
                    if isinstance(_filter, list):
                        if len(_filter) == 0:
                            _query = _response_query.filter(
                                StatementTable.in_response_to == None)  # NOQA Here must use == instead of is
                        else:
                            for f in _filter:
                                _query = _response_query.filter(
                                    StatementTable.in_response_to.contains(get_response_table(f)))
                    else:
                        if fp == 'in_response_to__contains':
                            _query = _response_query.join(ResponseTable).filter(ResponseTable.text == _filter)
                        else:
                            _query = _response_query.filter(StatementTable.in_response_to == None)  # NOQA
                else:
                    if _query:
                        _query = _query.filter(ResponseTable.statement_text.like('%' + _filter + '%'))
                    else:
                        _response_query = session.query(ResponseTable)
                        _query = _response_query.filter(ResponseTable.statement_text.like('%' + _filter + '%'))

                if _query is None:
                    return []
                if len(filter_parameters) == i + 1:
                    statements.extend(_query.all())

        results = []

        for statement in statements:
            if isinstance(statement, ResponseTable):
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
        if statement:
            session = self.Session()
            query = self.__statement_filter(session, **{"text": statement.text})
            record = query.first()

            # Create a new statement entry if one does not already exist
            if not record:
                record = StatementTable(text=statement.text)

            record.extra_data = dict(statement.extra_data)

            if statement.in_response_to:
                # Get or create the response records as needed
                for response in statement.in_response_to:
                    _response = session.query(ResponseTable).filter_by(
                        text=response.text,
                        statement_text=statement.text
                    ).first()

                    if _response:
                        _response.occurrence += 1
                    else:
                        # Create the record
                        _response = ResponseTable(
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
        session = self.Session()

        conversation = Conversation()

        session.add(conversation)
        session.flush()

        session.refresh(conversation)
        conversation_id = conversation.id

        session.commit()
        session.close()

        return conversation_id

    def add_to_converation(self, conversation_id, statement, response):
        """
        Add the statement and response to the conversation.
        """
        session = self.Session()

        conversation = session.query(Conversation).get(conversation_id)

        statement_query = session.query(StatementTable).filter_by(
            text=statement.text
        ).first()
        response_query = session.query(StatementTable).filter_by(
            text=response.text
        ).first()

        # Make sure the statements exist
        if not statement_query:
            self.update(statement)
            statement_query = session.query(StatementTable).filter_by(
                text=statement.text
            ).first()

        if not response_query:
            self.update(response)
            response_query = session.query(StatementTable).filter_by(
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
        session = self.Session()
        statement = None

        statement_query = session.query(
            StatementTable
        ).filter(
            StatementTable.conversations.any(id=conversation_id)
        ).order_by(StatementTable.id.desc()).limit(2).first()

        if statement_query:
            statement = statement_query.get_statement()

        session.close()

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        session = self.Session()
        count = self.count()
        if count < 1:
            raise self.EmptyDatabaseException()

        rand = random.randrange(0, count)
        stmt = session.query(StatementTable)[rand]

        statement = stmt.get_statement()

        session.close()
        return statement

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        Base.metadata.drop_all(self.engine)

    def create(self):
        """
        Populate the database with the tables.
        """
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
