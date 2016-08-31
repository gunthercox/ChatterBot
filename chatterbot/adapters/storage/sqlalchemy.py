from sqlalchemy import Table, MetaData, Column, Integer, ForeignKey
from sqlalchemy import Text
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper

from chatterbot.adapters.storage import StorageAdapter
from chatterbot.conversation import Response
from chatterbot.conversation import Statement


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

        metadata = MetaData(self.engine)

        self.response = Table('response', metadata,
                              Column('id', Integer, primary_key=True),
                              Column('text', Text),
                              Column('occurrence', Text),
                              )

        mapper(Response, self.response)

        self.statement = Table('statement', metadata,
                               Column('id', Integer, primary_key=True),
                               Column('response_id', Integer, ForeignKey('response.id')),
                               Column('text', Text),
                               Column('extra_data', Text)
                               )

        # mapper(Statement, self.statement, properties={
        #     'statement': relationship(Response, backref='response', order_by=self.statement.c.id)
        # })

        mapper(Statement, self.statement)

        self.statement.create()
        self.response.create()

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
        self.engine.connect()
        self.statement.select().execute()

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


# Base = declarative_base()
#
#
# class ResponseTable(Base):
#     __tablename__ = 'Response'
#
#     id = Column(Integer, primary_key=True)
#     text = Column(String)
#     occurrence = Column(String)
#     statement = Column(ForeignKey('Statement.id'))
#
#     def __init__(self, response):
#         self.text = response.text
#         self.occurrence = response.occurrence
#
#     def get_response(self):
#         return Response(self.text, self.occurrence)
#
#
# class StatementTable(Base):
#     __tablename__ = 'Statement'
#
#     id = Column(Integer, primary_key=True)
#     text = Column(String)
#     extra_data = Column(String)
#     in_response_to = relationship("Response", backref="response", order_by="Response.id")
#
#     def get_statement(self):
#         return Statement(self.text, self.in_response_to, self.extra_data)
#
#     def __init__(self, statement):
#         self.text = statement.text
#         self.in_response_to = statement.in_response_to
#         self.extra_data = statement.extra_data
