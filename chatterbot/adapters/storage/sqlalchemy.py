import json

from sqlalchemy import Column, ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

from chatterbot.adapters.storage import StorageAdapter
from chatterbot.conversation import Response
from chatterbot.conversation import Statement

Base = declarative_base()


class StatementTable(Base):
    __tablename__ = 'StatementTable'

    # id = Column(Integer)
    text = Column(String, primary_key=True)
    extra_data = Column(String)
    in_response_to = relationship("ResponseTable", back_populates="statementTable")

    # in_response_to = relationship("Response", backref="response", order_by="Response.id")
    def get_statement(self):
        return Statement(self.text, self.in_response_to.text,
                         self.extra_data)

        # def __init__(self, text, extra_data, in_response_to):
        #     std = StatementTable
        #     std.text = st1.text
        #     std.extra_data = st1.extra_data
        #     # if statement.in_response_to:
        #     # self.in_response_to = statement.in_response_to
        #     # self.extra_data =
        #     return std


class ResponseTable(Base):
    __tablename__ = 'ResponseTable'

    # id = Column(Integer)
    text = Column(String, primary_key=True)
    occurrence = Column(String)
    statement_text = Column(String, ForeignKey('StatementTable.text'))
    statementTable = relationship("StatementTable", back_populates="in_response_to")

    # def __init__(self, response):
    #     self.text = response.text
    #     self.occurrence = response.occurrence

    def get_response(self):
        return Response(self.text, self.occurrence)


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
        Session = sessionmaker(bind=self.engine)
        session = Session()

        return session.query(StatementTable).count()

    def find(self, statement_text):
        """
        Returns a object from the database if it exists
        """
        Session = sessionmaker(bind=self.engine)
        session = Session()

        std = session.query(StatementTable).filter_by(text=statement_text).first()
        # extra_data = json.loads(std.extra_data)
        # if extra_data:
        # extra_data = dict[extra_data]
        # TODO Extra data
        if std:
            return Statement(std.text)
        else:
            return None

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """

        Session = sessionmaker(bind=self.engine)
        session = Session()

        std = session.query(StatementTable).filter_by(text=statement_text).firs()
        session.delete(std)
        session.commit()

        # raise self.AdapterMethodNotImplementedError()

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

        if statement:
            Session = sessionmaker(bind=self.engine)
            session = Session()
            std = session.query(StatementTable).filter_by(text=statement.text).first()
            if std:
                # update
                if statement.text:
                    std.text = statement.text
                if statement.extra_data:
                    std.extra_data = json.dumps(statement.extra_data)
                session.add(std)
            else:
                session.add(StatementTable(text=statement.text))

            session.commit()

            # raise self.AdapterMethodNotImplementedError()

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
