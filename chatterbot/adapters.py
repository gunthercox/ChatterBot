import logging


class Adapter(object):
    """
    A superclass for all adapter classes.
    """

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger', logging.getLogger(__name__))
        self.chatbot = None

    def set_chatbot(self, chatbot):
        """
        Gives the adapter access to an instance of the ChatBot class.
        """
        self.chatbot = chatbot

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when an adapter method has not been implemented.
        Typically this indicates that the developer is expected to implement the
        method in a subclass.
        """

        def __init__(self, message=None):
            """
            Set the message for the esception.
            """
            if not message:
                message = 'This method must be overridden in a subclass method.'
            self.message = message

        def __str__(self):
            return self.message

    class InvalidAdapterTypeException(Exception):
        """
        An exception to be raised when an adapter of an unexpected class type is recieved.
        """
        pass
