from typing import TYPE_CHECKING as _TYPE_CHECKING, Any as _Any

if _TYPE_CHECKING:
    from chatterbot.chatterbot import ChatBot


class Adapter(object):
    """
    A superclass for all adapter classes.

    :param chatbot: A ChatBot instance.
    """

    def __init__(self, chatbot: 'ChatBot', **kwargs: _Any) -> None:
        self.chatbot = chatbot

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when an adapter method has not been implemented.
        Typically this indicates that the developer is expected to implement the
        method in a subclass.
        """

        def __init__(
            self,
            message: str = 'This method must be overridden in a subclass method.'
        ) -> None:
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
