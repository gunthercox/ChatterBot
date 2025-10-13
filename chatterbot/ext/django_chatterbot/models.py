from chatterbot.ext.django_chatterbot.abstract_models import AbstractBaseStatement, AbstractBaseTag


class Statement(AbstractBaseStatement):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.

    This model can be swapped for a custom model by setting
    CHATTERBOT_STATEMENT_MODEL in your Django settings.
    """

    class Meta:
        swappable = 'CHATTERBOT_STATEMENT_MODEL'


class Tag(AbstractBaseTag):
    """
    A label that categorizes a statement.

    This model can be swapped for a custom model by setting
    CHATTERBOT_TAG_MODEL in your Django settings.
    """

    class Meta:
        swappable = 'CHATTERBOT_TAG_MODEL'
