class LogicAdapterNotImplementedError(NotImplementedError):
    def __init__(self, message="This method must be overridden in a subclass method."):
        self.message = message


class LogicAdapter(object):

    def get_response(self):
        raise DatabaseAdapterNotImplementedError()
