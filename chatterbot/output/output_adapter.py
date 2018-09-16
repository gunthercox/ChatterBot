from chatterbot.adapters import Adapter


class OutputAdapter(Adapter):
    """
    A generic class that can be overridden by a subclass to provide extended
    functionality, such as delivering a response to an API endpoint.
    """

    def process_response(self, statement):
        """
        Override this method in a subclass to implement customized functionality.

        :param statement: The statement that the chat bot has produced in response to some input.

        :returns: The response statement.
        """
        return statement
