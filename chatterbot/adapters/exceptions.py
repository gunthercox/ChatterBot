class AdapterNotImplementedError(NotImplementedError):
    def __init__(self, message="This method must be overridden in a subclass method."):
        self.message = message


class EmptyDatabaseException(Exception):
    def __init__(self, message="The database currently contains no entries. At least one entry is expected. Make sure that you have read_only set to False."):
        self.message = message

