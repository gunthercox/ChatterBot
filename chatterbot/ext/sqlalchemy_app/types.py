from sqlalchemy.types import TypeDecorator, Unicode


class UnicodeString(TypeDecorator):
    """
    Type for unicode strings.
    """

    impl = Unicode

    def process_bind_param(self, value, dialect):
        """
        Coerce Python bytestrings to unicode before
        saving them to the database.
        """
        import sys

        if sys.version_info[0] < 3:
            if isinstance(value, str):
                value = value.decode('utf-8')
        return value
