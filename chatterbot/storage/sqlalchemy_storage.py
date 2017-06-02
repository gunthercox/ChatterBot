import json
import random

from chatterbot.storage import StorageAdapter
from chatterbot.conversation import Response
from chatterbot.conversation import Statement

Base = None

try:
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()


    class StatementTable(Base):
        from sqlalchemy import Column, Integer, String, PickleType
        from sqlalchemy.orm import relationship

        __tablename__ = 'StatementTable'

        def get_statement(self):
            stmt = Statement(self.text, **self.extra_data)
            for resp in self.in_response_to:
                stmt.add_response(resp.get_response())
            return stmt

        def get_statement_serialized(context):
            params = context.current_parameters
            del params['text_search']
            return json.dumps(params)

        id = Column(Integer)
        text = Column(String, primary_key=True)
        extra_data = Column(PickleType)
        # relationship:
        in_response_to = relationship("ResponseTable", back_populates="statement_table")
        text_search = Column(String, primary_key=True, default=get_statement_serialized)


    class ResponseTable(Base):
        from sqlalchemy import Column, Integer, String, ForeignKey
        from sqlalchemy.orm import relationship

        __tablename__ = 'ResponseTable'

        def get_reponse_serialized(context):
            params = context.current_parameters
            del params['text_search']
            return json.dumps(params)

        id = Column(Integer)
        text = Column(String, primary_key=True)
        occurrence = Column(Integer)
        statement_text = Column(String, ForeignKey('StatementTable.text'))

        statement_table = relationship("StatementTable", back_populates="in_response_to", cascade="all", uselist=False)
        text_search = Column(String, primary_key=True, default=get_reponse_serialized)

        def get_response(self):
            occ = {"occurrence": self.occurrence}
            return Response(text=self.text, **occ)

except ImportError:
    pass


def get_statement_table(statement):
    responses = list(map(get_response_table, statement.in_response_to))
    return StatementTable(text=statement.text, in_response_to=responses, extra_data=statement.extra_data)


def get_response_table(response):
    return ResponseTable(text=response.text, occurrence=response.occurrence)


class SQLAlchemyDatabaseAdapter(StorageAdapter):
    """
    SQLAlchemyDatabaseAdapter allows ChatterBot to store conversation
    data semi-structutered T-SQL database, virtually, any database that SQL Alchemy supports.
    
    Notes:
        Tables may change (and will), so, save your training data. There is no data migration (yet).
        Performance test not done yet.
        Tests using others databases not finished.
 
    All parameters all optional, default is sqlite database in memory.
    
    It will check if tables is present, if not, it will attempt to create required tables.

    :keyword database: Used for sqlite database. Ignored if database_uri especified.
    :type database: str
    
    :keyword database_uri: eg: sqlite:///database_test.db", # use database_uri or database, database_uri 
    can be especified to choose database driver (database parameter will be igored).
    :type database_uri: str
    
    :keyword read_only: False by default, makes all operations read only,  has priority over all DB operations
    so, create, update, delete will NOT be executed
    :type read_only: bool
    
    :keyword create: Force Recreate ChatterBot only tables in database, default False, 
    if read_only is True create is ignored.
    :type create: bool


    Simple use:
    
    chatbot = ChatBot(
           "My ChatterBot",
            storage_adapter="chatterbot.storage.SQLAlchemyDatabaseAdapter"
    )    

    """

    def __init__(self, **kwargs):
        super(SQLAlchemyDatabaseAdapter, self).__init__(**kwargs)

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        import sqlalchemy
        from sqlalchemy import MetaData

        self.database_name = self.kwargs.get("database")

        if self.database_name:
            # if some annoying blank space wrong...
            db_name = self.database_name.strip()
            # if set dbname only will create sql file.
            self.database_uri = self.kwargs.get(
                "database_uri", "sqlite:///" + db_name + ".db"
            )

        # default uses sqlite memory database.
        self.database_uri = self.kwargs.get(
            "database_uri", "sqlite://"
        )

        self.engine = create_engine(self.database_uri)

        self.read_only = self.kwargs.get(
            "read_only", False
        )

        # To force recreate tables
        create = self.kwargs.get("create", False)

        if not self.read_only and create:
            self.drop()
            self.create()

        if not self.read_only and not create:  # create tables already done
            tables_needed = Base.metadata.sorted_tables  # current tables
            metadata = MetaData()
            metadata.reflect(self.engine)
            tables = metadata.tables.values()
            if not tables:
                self.create()
            else:
                for table in tables_needed:
                    if not self.engine.dialect.has_table(self.engine, table.name):
                        # If table don't exist, Create.
                        Base.metadata.create_all(self.engine, tables=[table])

        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)

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

        self._session_finish(session, statement_text)

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
                        _query = _query.filter(ResponseTable.text_search.like('%' + _filter + '%'))
                    else:
                        _response_query = session.query(ResponseTable)
                        _query = _response_query.filter(ResponseTable.text_search.like('%' + _filter + '%'))

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

            if record:
                # update
                if statement.text:
                    record.text = statement.text
                if statement.extra_data:
                    record.extra_data = dict[statement.extra_data]
                if statement.in_response_to:
                    record.in_response_to = list(map(get_response_table, statement.in_response_to))
                session.add(record)
            else:
                session.add(get_statement_table(statement))

            self._session_finish(session)

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
        from sqlalchemy.exc import DatabaseError
        try:
            if not self.read_only:
                session.commit()
            else:
                session.rollback()
        except DatabaseError as e:
            self.logger.error(statement_text, str(e.orig))
        finally:
            session.close()
