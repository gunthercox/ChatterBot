from chatterbot.ext.django_chatterbot.abstract_models import AbstractBaseStatement, AbstractBaseTag


class Statement(AbstractBaseStatement):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """
    class Meta:
        db_table = 'statement'


class Tag(AbstractBaseTag):
    """
    A label that categorizes a statement.
    """
    class Meta:
        db_table = 'tag' 
