from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from chatterbot.conversation import StatementMixin
from chatterbot import constants


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
    Column('statement_id', Integer, ForeignKey('statement.id'))
)


class Tag(Base):
    """
    A tag that describes a statement.
    """

    name = Column(
        String(constants.TAG_NAME_MAX_LENGTH)
    )


class Statement(Base, StatementMixin):
    """
    A Statement represents a sentence or phrase.
    """

    text = Column(
        String(constants.STATEMENT_TEXT_MAX_LENGTH),
        unique=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    tags = relationship(
        'Tag',
        secondary=lambda: tag_association_table,
        backref='statements'
    )

    extra_data = Column(PickleType)

    in_response_to = relationship(
        'Response',
        back_populates='statement_table'
    )

    def get_tags(self):
        """
        Return a list of tags for this statement.
        """
        return [tag.name for tag in self.tags]

    def get_statement(self):
        from chatterbot.conversation import Statement as StatementObject
        from chatterbot.conversation import Response as ResponseObject

        statement = StatementObject(
            self.text,
            tags=[tag.name for tag in self.tags],
            extra_data=self.extra_data
        )
        for response in self.in_response_to:
            statement.add_response(
                ResponseObject(text=response.text, occurrence=response.occurrence)
            )
        return statement


class Response(Base):
    """
    Response, contains responses related to a given statement.
    """

    text = Column(
        String(constants.STATEMENT_TEXT_MAX_LENGTH)
    )

    conversation = Column(
        String(constants.CONVERSATION_LABEL_MAX_LENGTH)
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    occurrence = Column(
        Integer,
        default=1
    )

    statement_text = Column(
        String(constants.STATEMENT_TEXT_MAX_LENGTH),
        ForeignKey('statement.text')
    )

    statement_table = relationship(
        'Statement',
        back_populates='in_response_to',
        cascade='all',
        uselist=False
    )
