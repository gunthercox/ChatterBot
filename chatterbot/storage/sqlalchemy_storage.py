import json
import random

from chatterbot.storage import StorageAdapter
from chatterbot.conversation import Response
from chatterbot.conversation import Statement

_base = None
try:
    from sqlalchemy.ext.declarative import declarative_base

    _base = declarative_base()
except:
    pass


class StatementTable(_base):
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
        del (params['text_search'])
        return json.dumps(params)

    id = Column(Integer)
    text = Column(String, primary_key=True)
    extra_data = Column(PickleType)
    # relationship:
    in_response_to = relationship("ResponseTable", back_populates="statement_table")
    text_search = Column(String, primary_key=True, default=get_statement_serialized)


class ResponseTable(_base):
    from sqlalchemy import Column, Integer, String, ForeignKey
    from sqlalchemy.orm import relationship
    __tablename__ = 'ResponseTable'

    def get_reponse_serialized(context):
        params = context.current_parameters
        del (params['text_search'])
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


def get_statement_table(statement):
    responses = list(map(get_response_table, statement.in_response_to))
    return StatementTable(text=statement.text, in_response_to=responses, extra_data=statement.extra_data)


def get_response_table(response):
    return ResponseTable(text=response.text, occurrence=response.occurrence)


class SQLAlchemyDatabaseAdapter(StorageAdapter):
    read_only = False
    drop_create = False

    def __init__(self, **kwargs):
        super(SQLAlchemyDatabaseAdapter, self).__init__(**kwargs)

        from sqlalchemy import create_engine

        self.database_name = self.kwargs.get(
            "database", "chatterbot-database"
        )

        # if some annoying blank space wrong...
        db_name = self.database_name.strip()

        # default uses sqlite
        self.database_uri = self.kwargs.get(
            "database_uri", "sqlite:///" + db_name + ".db"
        )

        self.engine = create_engine(self.database_uri)

        self.read_only = self.kwargs.get(
            "read_only", False
        )

        self.drop_create = self.kwargs.get(
            "drop_create", False
        )

        if not self.read_only and self.drop_create:
            Base.metadata.drop_all(self.engine)
            Base.metadata.create_all(self.engine)

    def count(self):
        """
        Return the number of entries in the database.
        """
        session = self.__get_session()
        return session.query(StatementTable).count()

    def __get_session(self):
        """
        :rtype: Session
        """
        from sqlalchemy.orm import sessionmaker

        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

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
        session = self.__get_session()
        query = self.__statement_filter(session, **{"text": statement_text})
        record = query.first()
        if record:
            return record.get_statement()
        return None

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        session = self.__get_session()
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

        filter_parameters = kwargs.copy()

        session = self.__get_session()
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
                                StatementTable.in_response_to == None)  # Here must use == instead of is
                        else:
                            for f in _filter:
                                _query = _response_query.filter(
                                    StatementTable.in_response_to.contains(get_response_table(f)))
                    else:
                        if fp == 'in_response_to__contains':
                            _query = _response_query.join(ResponseTable).filter(ResponseTable.text == _filter)
                        else:
                            _query = _response_query.filter(StatementTable.in_response_to == None)
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

        return results

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        session = self.__get_session()
        if statement:
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
        count = self.count()
        if count < 1:
            raise self.EmptyDatabaseException()

        rand = random.randrange(0, count)
        session = self.__get_session()
        stmt = session.query(StatementTable)[rand]

        return stmt.get_statement()

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        Base.metadata.drop_all(self.engine)

    def _session_finish(self, session, statement_text=None):
        from sqlalchemy.exc import DatabaseError
        try:
            if not self.read_only:
                session.commit()
            else:
                session.rollback()
        except DatabaseError as e:
            self.logger.error(statement_text, str(e.orig))
