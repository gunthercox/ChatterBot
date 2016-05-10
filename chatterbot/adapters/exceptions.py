class EmptyDatabaseException(Exception):

    def __init__(self, message="The database currently contains no entries. At least one entry is expected. Make sure that you have read_only set to False."):
        self.message = message

    def __str__(self):
        return self.message


class EmptyDatasetException(Exception):

    def __init__(self, message="An empty collection of elements was received when at least one entry was expected."):
        self.message = message

    def __str__(self):
        return self.message
