class IOAdapterNotImplementedError(NotImplementedError):
    def __init__(self, message="This method must be overridden in a subclass method."):
        self.message = message


class IOAdapter(object):

    def get_output(self, input_value):
        """
        Takes an input value.
        Returns an output value.
        """
        raise DatabaseAdapterNotImplementedError()
