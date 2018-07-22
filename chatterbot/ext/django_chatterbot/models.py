from chatterbot.ext.django_chatterbot.abstract_models import AbstractBaseStatement, AbstractBaseResponse, AbstractBaseTag


class Statement(AbstractBaseStatement):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """
    pass


class Response(AbstractBaseResponse):
    """
    A connection between a statement and anther statement
    that response to it.
    """
    pass


class Tag(AbstractBaseTag):
    """
    A label that categorizes a statement.
    """
    pass
