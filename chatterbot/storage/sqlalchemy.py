import json
import random

from sqlalchemy import Column, ForeignKey
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from chatterbot.storage import StorageAdapter
from chatterbot.conversation import Response
from chatterbot.conversation import Statement

Base = declarative_base()


class StatementTable(Base):
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

    # id = Column(Integer)
    text = Column(String, primary_key=True)
    extra_data = Column(PickleType)
    # Old: in_response_to = relationship("ResponseTable", back_populates="statement_table")
    # relationship:
    in_response_to = relationship("ResponseTable", back_populates="statement_table")

    text_search = Column(String, primary_key=True, default=get_statement_serialized)


class ResponseTable(Base):
    __tablename__ = 'ResponseTable'

    def get_reponse_serialized(context):
        params = context.current_parameters
        del (params['text_search'])
        return json.dumps(params)

    # id = Column(Integer)
    text = Column(String, primary_key=True)
    occurrence = Column(String)
    statement_text = Column(String, ForeignKey('StatementTable.text'))

    # Old:  statement_table = relationship("StatementTable", backref=backref('in_response_to'), cascade="all, delete-orphan", single_parent=True)
    # Test relationship:
    statement_table = relationship("StatementTable", back_populates="in_response_to", cascade="all",
                                   uselist=False)

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
    def __init__(self, **kwargs):
        super(SQLAlchemyDatabaseAdapter, self).__init__(**kwargs)

        self.database_name = self.kwargs.get(
            "database", "chatterbot-database"
        )

        # if some annoing blank space wrong...
        db_name = self.database_name.strip()

        # default uses sqlite
        self.database_uri = self.kwargs.get(
            "database_uri", "sqlite:///" + db_name + ".db"
        )

        self.engine = create_engine(self.database_uri)

        # metadata = MetaData(self.engine)

        # Recreate database
        # metadata.drop_all()
        #
        # self.response = Table('response', metadata,
        #                       Column('id', Integer, primary_key=True),
        #                       Column('text', Text),
        #                       Column('occurrence', Text),
        #                       )
        #
        # self.statement = Table('statement', metadata,
        #                        Column('id', Integer, primary_key=True),
        #                        Column('text', Text),
        #                        Column('in_response_to', Integer, ForeignKey('response.id')),
        #                        Column('extra_data', Text)
        #                        )
        #
        # # mapper(Response, self.response,
        # #        # non_primary=True,
        # #        properties={
        # #            'statement': relationship(Statement, backref='response')
        # #        }, )
        # mapper(Statement, self.statement)
        # mapper(Response, self.response)

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
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def __statement_filter(self, session, **kwargs):
        """
        Apply filter opeartion on StatementTable

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

    read_only = False

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

        if not self.read_only:
            session.commit()
        else:
            session.rollback()
            # raise self.AdapterMethodNotImplementedError()

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

        if len(filter_parameters) == 0:
            _response_query = session.query(StatementTable)
            statements.extend(_response_query.all())
        else:
            for fp in filter_parameters:
                _like = filter_parameters[fp]
                if fp == 'in_response_to':
                    _response_query = session.query(StatementTable)
                    if isinstance(_like, list):
                        if len(_like) == 0:
                            query = _response_query.filter(StatementTable.in_response_to == None,
                                                           StatementTable.subject_id != None)
                        else:
                            query = _response_query.filter(StatementTable.in_response_to.contain(_like))
                    else:
                        query = _response_query.filter(StatementTable.in_response_to.like('%' + _like + '%'))


                else:
                    _response_query = session.query(ResponseTable)
                    query = _response_query.filter(ResponseTable.text_search.like('%' + _like + '%'))

                statements.extend(query.all())

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
                session.add(record)
            else:
                session.add(get_statement_table(statement))

        if not self.read_only:
            session.commit()
        else:
            session.rollback()

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
