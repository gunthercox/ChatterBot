from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr, declarative_base


class ModelBase(object):
    """
    An augmented base class for SqlAlchemy models.
    """

    @declared_attr
    def __tablename__(cls):
        """
        Return the lowercase class name as the name of the table.
        """
        return cls.__name__.lower()

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


Base = declarative_base(cls=ModelBase)


tag_association_table = Table(
    'tag_association',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('statement_id', Integer, ForeignKey('StatementTable.id'))
)

class Tag(Base):
    """
    A tag that describes a statement.
    """

    name = Column(String)

class StatementTable(Base):
    """
    StatementTable, placeholder for a sentence or phrase.
    """

    __tablename__ = 'StatementTable'

    def get_statement(self):
        from chatterbot.conversation import Statement as StatementObject

        statement = StatementObject(self.text, extra_data=self.extra_data)
        for response in self.in_response_to:
            statement.add_response(response.get_response())
        return statement

    text = Column(String, unique=True)

    tags = relationship(
        'Tag',
        secondary=lambda: tag_association_table,
        backref='statements'
    )

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
        from chatterbot.conversation import Response as ResponseObject
        occ = {'occurrence': self.occurrence}
        return ResponseObject(text=self.text, **occ)

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

    statements = relationship(
        'StatementTable',
        secondary=lambda: conversation_association_table,
        backref='conversations'
    )
