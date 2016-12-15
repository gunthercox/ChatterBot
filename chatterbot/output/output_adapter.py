from chatterbot.adapters import Adapter


class OutputAdapter(Adapter):
    """
    A generic class that can be overridden by a subclass to provide extended
    functionality, such as delivering a response to an API endpoint.
    """

    def process_response(self, statement, confidence, session_id=None):
        """
        Override this method in a subclass to implement customized functionality.

        :param statement: The statement that the chat bot has produced in response to some input.

        :param confidence: The confidence with which the chat bot 'thinks' the
                           given statement is the correct response.

        :param session_id: The unique id of the current chat session.

        :returns: The response statement.
        """
        return statement
