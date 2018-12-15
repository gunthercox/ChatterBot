from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
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
        String(constants.TAG_NAME_MAX_LENGTH),
        unique=True
    )


class Statement(Base, StatementMixin):
    """
    A Statement represents a sentence or phrase.
    """

    text = Column(
        String(constants.STATEMENT_TEXT_MAX_LENGTH)
    )

    search_text = Column(
        String(constants.STATEMENT_TEXT_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    conversation = Column(
        String(constants.CONVERSATION_LABEL_MAX_LENGTH),
        nullable=False,
        server_default=''
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

    in_response_to = Column(
        String(constants.STATEMENT_TEXT_MAX_LENGTH),
        nullable=True
    )

    search_in_response_to = Column(
        String(constants.STATEMENT_TEXT_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    persona = Column(
        String(constants.PERSONA_MAX_LENGTH),
        nullable=False,
        server_default=''
    )

    def get_tags(self):
        """
        Return a list of tags for this statement.
        """
        return [tag.name for tag in self.tags]
