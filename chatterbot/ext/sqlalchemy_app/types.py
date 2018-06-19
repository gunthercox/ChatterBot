from sqlalchemy.types import TypeDecorator, Unicode


class UnicodeString(TypeDecorator):
    """
    Type for unicode strings.
    """

    impl = Unicode
