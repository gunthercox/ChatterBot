from chatterbot.adapters.output import OutputAdapter
from chatterbot.utils.read_input import input_function


class TerminalAdapter(OutputAdapter):
    """
    A simple adapter that allows ChatterBot to
    communicate through the terminal.
    """

    def process_input(self, *args, **kwargs):
        """
        Read the user's input from the terminal.
        """
        user_input = input_function()
        return user_input

    def process_response(self, statement):
        """
        Print the response to the user's input.
        """
        print(statement.text)
        return statement.text
