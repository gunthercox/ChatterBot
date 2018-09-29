class Adapter(object):
    """
    A superclass for all adapter classes.

    :param chatbot: A ChatBot instance.
    """

    def __init__(self, chatbot, **kwargs):
        self.chatbot = chatbot

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when an adapter method has not been implemented.
        Typically this indicates that the developer is expected to implement the
        method in a subclass.
        """

        def __init__(self, message='This method must be overridden in a subclass method.'):
            """
            Set the message for the exception.
            """
            super().__init__(message)

    class InvalidAdapterTypeException(Exception):
        """
        An exception to be raised when an adapter
        of an unexpected class type is received.
        """
        pass
