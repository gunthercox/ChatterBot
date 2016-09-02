import json
import random

from sqlalchemy import Column, ForeignKey
from sqlalchemy import PickleType
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

from chatterbot.adapters.storage import StorageAdapter
from chatterbot.conversation import Response
from chatterbot.conversation import Statement

Base = declarative_base()


def get_statement_table_data(context):
    print(context.get_statement)
    pass


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
    # in_response_to = relationship("ResponseTable", back_populates="statement_table")
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
    statement_table = relationship("StatementTable", backref=backref('in_response_to'), cascade="all, delete-orphan",
                                   single_parent=True)
    text_search = Column(String, primary_key=True, default=get_reponse_serialized)

    def get_response(self):
        occ = {"occurrence": self.occurrence}
        return Response(text=self.text, **occ)


def get_statement_table(statement):
    responses = []
    for resp in statement.in_response_to:
        responses.append(get_response_table(resp))
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

    def find(self, statement_text):
        """
        Returns a object from the database if it exists
        """
        session = self.__get_session()

        std = session.query(StatementTable).filter_by(text=statement_text).first()

        if std:
            return std.get_statement()
        else:
            return None

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """

        session = self.__get_session()

        std = session.query(StatementTable).filter_by(text=statement_text).first()
        session.delete(std)

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
        session.query()
        stmts = []
        for fp in filter_parameters:
            stmts.extend(session.query(ResponseTable).filter(
                ResponseTable.text_search.like('%' + filter_parameters[fp] + '%')).all())

        results = []
        for st in stmts:
            if st and st.statement_table:
                results.append(st.statement_table.get_statement())

        return results

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """

        if statement:
            session = self.__get_session()
            std = session.query(StatementTable).filter_by(text=statement.text).first()
            if std:
                # update
                if statement.text:
                    std.text = statement.text
                if statement.extra_data:
                    std.extra_data = dict[statement.extra_data]
                session.add(std)
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
